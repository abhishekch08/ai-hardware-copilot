"""Revision-aware project ingestion for a narrow, testable MVP path.

Supported inputs are KiCad schematic/PCB S-expressions, CSV BOMs and firmware/source
trees. Native formats remain authoritative; this index preserves source evidence IDs.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .evidence import EvidenceStore


@dataclass(slots=True)
class GraphNode:
    node_id: str
    kind: str
    attributes: dict[str, Any]
    evidence_ref: str


@dataclass(slots=True)
class GraphEdge:
    source: str
    relation: str
    target: str
    evidence_ref: str


@dataclass(slots=True)
class ProjectIndex:
    project_id: str
    hardware_revision: str
    firmware_revision: str | None
    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)
    source_evidence: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ProjectIngestor:
    def __init__(self, evidence: EvidenceStore):
        self.evidence = evidence

    def ingest(self, manifest: dict[str, Any], project_root: str | Path) -> ProjectIndex:
        unknown_manifest = set(manifest) - {
            "project_id", "hardware_revision", "firmware_revision", "sources"
        }
        if unknown_manifest:
            raise ValueError(f"unknown project manifest fields: {sorted(unknown_manifest)}")
        root = Path(project_root).resolve()
        project_id = _required_text(manifest, "project_id")
        hardware_revision = _required_text(manifest, "hardware_revision")
        firmware_revision = manifest.get("firmware_revision")
        sources = manifest.get("sources")
        if not isinstance(sources, list) or not sources:
            raise ValueError("project manifest requires a non-empty sources list")
        index = ProjectIndex(project_id, hardware_revision, firmware_revision)
        configuration = {
            "project_id": project_id,
            "hardware_revision": hardware_revision,
            "firmware_revision": firmware_revision,
        }

        for source in sources:
            if not isinstance(source, dict):
                raise ValueError("each project source must be a mapping")
            unknown_source = set(source) - {"kind", "path"}
            if unknown_source:
                raise ValueError(f"unknown project source fields: {sorted(unknown_source)}")
            kind = _required_text(source, "kind")
            relative = Path(_required_text(source, "path"))
            path = (root / relative).resolve()
            _require_within(root, path)
            if kind == "firmware_tree":
                self._ingest_firmware_tree(path, index, configuration)
                continue
            record = self.evidence.register_file(path, kind=kind, configuration=configuration)
            index.source_evidence.append(record.evidence_id)
            if kind == "kicad_schematic":
                self._ingest_kicad_schematic(path, record.evidence_id, index)
            elif kind == "kicad_pcb":
                self._ingest_kicad_pcb(path, record.evidence_id, index)
            elif kind == "bom_csv":
                self._ingest_bom(path, record.evidence_id, index)
            else:
                index.warnings.append(f"registered unsupported source kind without parsing: {kind}")

        index.nodes = _deduplicate_nodes(index.nodes)
        index.edges = _deduplicate_edges(index.edges)
        graph_record = self.evidence.register_json(
            index.as_dict(),
            kind="engineering_project_index",
            source_uri=f"project://{project_id}/{hardware_revision}",
            configuration=configuration,
            derived_from=index.source_evidence,
        )
        index.source_evidence.append(graph_record.evidence_id)
        return index

    def _ingest_kicad_schematic(self, path: Path, evidence_ref: str, index: ProjectIndex) -> None:
        root = parse_sexpr(path.read_text(encoding="utf-8", errors="replace"))
        for symbol in find_forms(root, "symbol"):
            properties = _properties(symbol)
            reference = properties.get("Reference")
            if not reference or reference.startswith("#"):
                continue
            index.nodes.append(GraphNode(
                node_id=f"component:{reference}",
                kind="component",
                attributes={
                    "reference": reference,
                    "value": properties.get("Value", ""),
                    "footprint": properties.get("Footprint", ""),
                    "source": path.name,
                },
                evidence_ref=evidence_ref,
            ))
        for form_name in ("label", "global_label", "hierarchical_label"):
            for form in find_forms(root, form_name):
                if len(form) > 1 and isinstance(form[1], str):
                    net = form[1]
                    index.nodes.append(GraphNode(
                        node_id=f"net:{net}", kind="net",
                        attributes={"name": net, "source": path.name},
                        evidence_ref=evidence_ref,
                    ))

    def _ingest_kicad_pcb(self, path: Path, evidence_ref: str, index: ProjectIndex) -> None:
        root = parse_sexpr(path.read_text(encoding="utf-8", errors="replace"))
        net_names: dict[str, str] = {}
        for net_form in find_forms(root, "net"):
            if len(net_form) >= 3:
                net_names[str(net_form[1])] = str(net_form[2])
                index.nodes.append(GraphNode(
                    node_id=f"net:{net_form[2]}", kind="net",
                    attributes={"name": str(net_form[2]), "source": path.name},
                    evidence_ref=evidence_ref,
                ))
        for footprint in find_forms(root, "footprint"):
            properties = _properties(footprint)
            reference = properties.get("Reference") or _find_fp_text_reference(footprint)
            if not reference:
                continue
            at = _first_child(footprint, "at")
            component_id = f"component:{reference}"
            index.nodes.append(GraphNode(
                node_id=component_id,
                kind="component",
                attributes={
                    "reference": reference,
                    "footprint": str(footprint[1]) if len(footprint) > 1 else "",
                    "x_mm": _number(at, 1),
                    "y_mm": _number(at, 2),
                    "rotation_deg": _number(at, 3),
                    "source": path.name,
                },
                evidence_ref=evidence_ref,
            ))
            for pad in _direct_children(footprint, "pad"):
                pad_number = str(pad[1]) if len(pad) > 1 else ""
                pad_id = f"pad:{reference}:{pad_number}"
                net_form = _first_child(pad, "net")
                net_name = None
                if net_form and len(net_form) >= 3:
                    net_name = str(net_form[2])
                elif net_form and len(net_form) >= 2:
                    net_name = net_names.get(str(net_form[1]))
                index.nodes.append(GraphNode(
                    node_id=pad_id,
                    kind="pad",
                    attributes={"number": pad_number, "component": reference, "net": net_name},
                    evidence_ref=evidence_ref,
                ))
                index.edges.append(GraphEdge(component_id, "HAS_PAD", pad_id, evidence_ref))
                if net_name:
                    index.edges.append(GraphEdge(pad_id, "CONNECTED_TO", f"net:{net_name}", evidence_ref))

    def _ingest_bom(self, path: Path, evidence_ref: str, index: ProjectIndex) -> None:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = csv.DictReader(handle)
            if not rows.fieldnames:
                raise ValueError(f"BOM has no header: {path}")
            normalized = {name.lower().strip(): name for name in rows.fieldnames}
            reference_key = next(
                (normalized[key] for key in ("reference", "references", "ref", "designator") if key in normalized),
                None,
            )
            if reference_key is None:
                raise ValueError(f"BOM missing reference/designator column: {path}")
            for row in rows:
                references = re.split(r"[,;\s]+", row.get(reference_key, "").strip())
                attributes = {key: value for key, value in row.items() if key and value}
                for reference in filter(None, references):
                    index.nodes.append(GraphNode(
                        node_id=f"component:{reference}", kind="component",
                        attributes={"reference": reference, "bom": attributes},
                        evidence_ref=evidence_ref,
                    ))

    def _ingest_firmware_tree(
        self, path: Path, index: ProjectIndex, configuration: dict[str, Any]
    ) -> None:
        if not path.is_dir():
            raise ValueError(f"firmware_tree is not a directory: {path}")
        revision = _git_revision(path)
        if index.firmware_revision and not revision:
            raise ValueError(
                "firmware_revision was supplied but the firmware tree has no verifiable Git revision"
            )
        if index.firmware_revision and revision and revision != index.firmware_revision:
            raise ValueError(
                f"firmware revision mismatch: manifest={index.firmware_revision}, repository={revision}"
            )
        suffixes = {".c", ".h", ".cc", ".cpp", ".hpp", ".rs", ".py", ".dts", ".dtsi"}
        source_count = 0
        for source in sorted(item for item in path.rglob("*") if item.suffix.lower() in suffixes):
            if ".git" in source.parts or source.stat().st_size > 2_000_000:
                continue
            source_count += 1
            if source_count > 5_000:
                raise ValueError("firmware tree exceeds the 5000-source-file ingestion limit")
            record = self.evidence.register_file(source, kind="firmware_source", configuration=configuration)
            index.source_evidence.append(record.evidence_id)
            text = source.read_text(encoding="utf-8", errors="replace")
            for symbol, symbol_kind in _source_symbols(text):
                index.nodes.append(GraphNode(
                    node_id=f"firmware:{symbol}", kind="firmware_symbol",
                    attributes={
                        "name": symbol,
                        "symbol_kind": symbol_kind,
                        "path": source.relative_to(path).as_posix(),
                        "revision": revision,
                    },
                    evidence_ref=record.evidence_id,
                ))


TOKEN = re.compile(r'\s*(?:(\()|(\))|"((?:\\.|[^"\\])*)"|([^\s()]+))')


def parse_sexpr(text: str) -> list[Any]:
    """Parse the S-expression subset used by KiCad while preserving string atoms."""
    stack: list[list[Any]] = []
    roots: list[Any] = []
    position = 0
    for match in TOKEN.finditer(text):
        if match.start() != position and text[position:match.start()].strip():
            raise ValueError(f"unparsed S-expression text near byte {position}")
        position = match.end()
        if match.group(1):
            value: list[Any] = []
            (stack[-1] if stack else roots).append(value)
            stack.append(value)
        elif match.group(2):
            if not stack:
                raise ValueError("unbalanced closing parenthesis")
            stack.pop()
        else:
            atom = _unescape_quoted(match.group(3)) if match.group(3) is not None else match.group(4)
            (stack[-1] if stack else roots).append(atom)
    if stack:
        raise ValueError("unbalanced opening parenthesis")
    if text[position:].strip():
        raise ValueError(f"unparsed S-expression tail near byte {position}")
    return roots


def find_forms(value: Any, name: str) -> Iterable[list[Any]]:
    if isinstance(value, list):
        if value and value[0] == name:
            yield value
        for item in value:
            yield from find_forms(item, name)


def _direct_children(form: list[Any], name: str) -> Iterable[list[Any]]:
    return (item for item in form[1:] if isinstance(item, list) and item and item[0] == name)


def _first_child(form: list[Any], name: str) -> list[Any] | None:
    return next(_direct_children(form, name), None)


def _properties(form: list[Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in _direct_children(form, "property"):
        if len(item) >= 3:
            result[str(item[1])] = str(item[2])
    return result


def _find_fp_text_reference(footprint: list[Any]) -> str | None:
    for item in _direct_children(footprint, "fp_text"):
        if len(item) >= 3 and item[1] == "reference":
            return str(item[2])
    return None


def _number(form: list[Any] | None, index: int) -> float | None:
    if not form or len(form) <= index:
        return None
    try:
        return float(form[index])
    except (TypeError, ValueError):
        return None


def _unescape_quoted(value: str) -> str:
    replacements = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}
    return re.sub(r"\\(.)", lambda match: replacements.get(match.group(1), match.group(1)), value)


def _source_symbols(text: str) -> set[tuple[str, str]]:
    result = {(match.group(1), "macro") for match in re.finditer(r"(?m)^\s*#\s*define\s+([A-Za-z_]\w*)", text)}
    result.update(
        (match.group(1), "function")
        for match in re.finditer(
            r"(?m)^\s*(?:static\s+)?(?:inline\s+)?(?:[A-Za-z_]\w*[\s*]+)+([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{",
            text,
        )
        if match.group(1) not in {"if", "for", "while", "switch"}
    )
    result.update((name, "register_or_gpio") for name in re.findall(r"\b(?:GPIO|REG|CTRL|STATUS)_[A-Z0-9_]+\b", text))
    return result


def _git_revision(path: Path) -> str | None:
    try:
        return subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def _deduplicate_nodes(nodes: list[GraphNode]) -> list[GraphNode]:
    merged: dict[str, GraphNode] = {}
    for node in nodes:
        if node.node_id not in merged:
            merged[node.node_id] = node
        else:
            current = merged[node.node_id]
            current.attributes = _deep_merge(current.attributes, node.attributes)
    return [merged[key] for key in sorted(merged)]


def _deduplicate_edges(edges: list[GraphEdge]) -> list[GraphEdge]:
    unique = {(edge.source, edge.relation, edge.target, edge.evidence_ref): edge for edge in edges}
    return [unique[key] for key in sorted(unique)]


def _deep_merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in update.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        elif value not in (None, ""):
            result[key] = value
    return result


def _required_text(value: dict[str, Any], key: str) -> str:
    result = value.get(key)
    if not isinstance(result, str) or not result.strip():
        raise ValueError(f"required text field missing: {key}")
    return result.strip()


def _require_within(root: Path, path: Path) -> None:
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"project source escapes project root: {path}") from exc
