#!/usr/bin/env python3
"""Compile the canonical Markdown registry into one validated YAML file per agent."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


PREFIX_DOMAIN = {
    "SYS": "systems",
    "PROD": "product",
    "EE": "electrical",
    "EMB": "embedded",
    "AI": "ai_software_data",
    "ME": "mechanical",
    "XR": "xr_spatial",
    "TEST": "test_quality_safety",
    "MFG": "manufacturing_supply_chain",
    "SCI": "science_research",
    "BIZ": "business_strategy",
    "FIN": "finance",
    "HR": "people",
    "OPS": "operations",
    "LEG": "legal_ip",
    "REG": "regulatory",
    "GOV": "governance",
    "SEC": "security",
    "INFRA": "infrastructure",
    "MKT": "market_marketing",
    "APP": "applications_solutions",
    "SALES": "sales",
    "DOC": "documentation_knowledge",
    "CS": "customer_success",
    "EDU": "training_enablement",
    "META": "orchestration",
}

DEFAULT_TOOLS = {
    "electrical": ["calculator", "datasheet_retrieval", "eda_read", "simulation"],
    "embedded": ["source_repository", "compiler_tests", "debugger", "instrument_simulator"],
    "ai_software_data": ["source_repository", "code_execution", "evaluation_harness"],
    "mechanical": ["cad_read", "calculation", "simulation", "test_evidence"],
    "xr_spatial": ["camera_data", "calibration_data", "spatial_evaluation"],
    "test_quality_safety": ["instrument_evidence", "calculation", "test_database"],
    "manufacturing_supply_chain": ["bom", "process_data", "supplier_evidence"],
    "science_research": ["primary_source_retrieval", "calculation", "statistical_analysis"],
    "security": ["source_repository", "configuration_audit", "threat_model"],
    "legal_ip": ["primary_legal_sources", "patent_search", "evidence_audit"],
    "regulatory": ["primary_regulatory_sources", "standards", "evidence_audit"],
    "finance": ["calculation", "spreadsheet_model", "market_evidence"],
}

BLOCK_RIGHTS = {
    "electrical": ["unsafe electrical action", "unverified electrical release"],
    "test_quality_safety": ["invalid measurement", "unsafe experiment", "unverified release"],
    "security": ["uncontrolled access or data exposure", "unsafe tool permission"],
    "legal_ip": ["unsupported legal or IP conclusion"],
    "regulatory": ["unsupported regulated claim or release"],
    "governance": ["unaccepted material risk"],
    "manufacturing_supply_chain": ["unmanufacturable or uncontrolled production release"],
}

MANDATORY_CONTEXT = [
    "agents/00_PRODUCT_MISSION_AND_REFERENCE_DOMAINS.md",
    "governance/OPERATING_CONSTITUTION.md",
    "agents/AGENT_RUNTIME_STANDARD.md",
    "schemas/UNIVERSAL_REASONING_SCHEMA.md",
]

STOPWORDS = {
    "agent", "and", "the", "with", "for", "from", "into", "that", "this", "owns",
    "builds", "design", "engineering", "produces", "product", "system", "systems",
}


def clean_cell(value: str) -> str:
    value = re.sub(r"\*\*", "", value).replace("<br>", " ")
    return re.sub(r"\s+", " ", value).strip()


def registry_rows(registry: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in registry.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*([A-Z]+-\d{2})\s*\|(.*)\|\s*$", line)
        if not match:
            continue
        cells = [clean_cell(cell) for cell in match.group(2).split("|")]
        if len(cells) != 4:
            raise ValueError(f"expected four registry columns after ID: {line}")
        rows.append({
            "agent_id": match.group(1),
            "name": cells[0],
            "capability_level": cells[1],
            "exact_specialization": cells[2],
            "summary": cells[3],
        })
    return rows


def handbook_map(agents_dir: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    ignored = {
        "AGENT_REGISTRY.md",
        "AGENT_RUNTIME_STANDARD.md",
        "00_PRODUCT_MISSION_AND_REFERENCE_DOMAINS.md",
        "13_WEARABLE_XR_INDUSTRY_INTELLIGENCE.md",
    }
    for path in sorted(agents_dir.glob("*.md")):
        if path.name in ignored:
            continue
        text = path.read_text(encoding="utf-8")
        for agent_id in re.findall(r"^##\s+([A-Z]+-\d{2})(?:\s+—|\s+/)", text, re.MULTILINE):
            if agent_id in mapping:
                raise ValueError(f"duplicate handbook definition for {agent_id}")
            mapping[agent_id] = f"agents/{path.name}"
    return mapping


def activation_keywords(row: dict[str, str]) -> list[str]:
    text = " ".join((row["name"], row["exact_specialization"], row["summary"]))
    words = re.findall(r"[A-Za-z][A-Za-z0-9+./-]{1,}", text.lower())
    result: list[str] = []
    for word in words:
        normalized = word.strip(".,;:/-")
        if normalized and normalized not in STOPWORDS and normalized not in result:
            result.append(normalized)
    return result[:48]


def compile_configs(repo_root: Path, output_dir: Path) -> int:
    rows = registry_rows(repo_root / "agents" / "AGENT_REGISTRY.md")
    handbooks = handbook_map(repo_root / "agents")
    ids = {row["agent_id"] for row in rows}
    if len(rows) != len(ids):
        raise ValueError("registry contains duplicate agent IDs")
    if ids != set(handbooks):
        raise ValueError(
            f"registry/handbook mismatch; registry_only={sorted(ids-set(handbooks))}, "
            f"handbook_only={sorted(set(handbooks)-ids)}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    expected_files: set[str] = set()
    for row in rows:
        prefix = row["agent_id"].split("-")[0]
        domain = PREFIX_DOMAIN[prefix]
        config = {
            **row,
            "domains": [domain],
            "activation_keywords": activation_keywords(row),
            "handbook": handbooks[row["agent_id"]],
            "mandatory_context": list(MANDATORY_CONTEXT),
            "default_tools": DEFAULT_TOOLS.get(domain, ["primary_source_retrieval", "calculation"]),
            "can_block": BLOCK_RIGHTS.get(domain, []),
            "status": "configured",
        }
        destination = output_dir / f"{row['agent_id']}.yaml"
        expected_files.add(destination.name)
        destination.write_text(
            yaml.safe_dump(config, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )

    for existing in output_dir.glob("*.yaml"):
        if existing.name not in expected_files:
            existing.unlink()
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or args.repo_root / "config" / "agents"
    count = compile_configs(args.repo_root, output)
    print(f"compiled {count} agent configurations into {output}")


if __name__ == "__main__":
    main()

