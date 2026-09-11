import tempfile
import unittest
from pathlib import Path

from ai_hardware_copilot.evidence import EvidenceStore
from ai_hardware_copilot.project import ProjectIngestor, parse_sexpr


class ProjectIngestionTests(unittest.TestCase):
    def test_unknown_manifest_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                ProjectIngestor(EvidenceStore(temporary)).ingest(
                    {
                        "project_id": "demo",
                        "hardware_revision": "A",
                        "sources": [{"kind": "document", "path": "missing.txt"}],
                        "silently_ignored": True,
                    },
                    temporary,
                )

    def test_kicad_bom_and_firmware_create_revision_aware_graph(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "board.kicad_sch").write_text(
                '(kicad_sch (symbol (property "Reference" "U1") '
                '(property "Value" "TPS62843")) (global_label "1V8_SYS"))',
                encoding="utf-8",
            )
            (root / "board.kicad_pcb").write_text(
                '(kicad_pcb (net 1 "GND") (net 2 "1V8_SYS") '
                '(footprint "QFN" (at 10 20 90) (property "Reference" "U1") '
                '(pad "1" smd rect (net 1 "GND")) '
                '(pad "2" smd rect (net 2 "1V8_SYS"))))',
                encoding="utf-8",
            )
            (root / "bom.csv").write_text(
                "Reference,Value,MPN\nU1,TPS62843,TPS62843YBG\n",
                encoding="utf-8",
            )
            firmware = root / "firmware"
            firmware.mkdir()
            (firmware / "power.c").write_text(
                "#define GPIO_REG_EN 17\nvoid enable_regulator(void) { GPIO_REG_EN; }\n",
                encoding="utf-8",
            )
            manifest = {
                "project_id": "demo-board",
                "hardware_revision": "A",
                "sources": [
                    {"kind": "kicad_schematic", "path": "board.kicad_sch"},
                    {"kind": "kicad_pcb", "path": "board.kicad_pcb"},
                    {"kind": "bom_csv", "path": "bom.csv"},
                    {"kind": "firmware_tree", "path": "firmware"},
                ],
            }
            index = ProjectIngestor(EvidenceStore(root / "evidence")).ingest(manifest, root)
            nodes = {node.node_id: node for node in index.nodes}
            edges = {(edge.source, edge.relation, edge.target) for edge in index.edges}
            self.assertEqual(nodes["component:U1"].attributes["x_mm"], 10.0)
            self.assertEqual(nodes["component:U1"].attributes["bom"]["MPN"], "TPS62843YBG")
            self.assertIn("net:1V8_SYS", nodes)
            self.assertIn("firmware:enable_regulator", nodes)
            self.assertIn(("pad:U1:2", "CONNECTED_TO", "net:1V8_SYS"), edges)
            self.assertTrue(all(ref.startswith("evidence://sha256/") for ref in index.source_evidence))

    def test_source_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = {
                "project_id": "bad", "hardware_revision": "A",
                "sources": [{"kind": "bom_csv", "path": "../outside.csv"}],
            }
            with self.assertRaises(ValueError):
                ProjectIngestor(EvidenceStore(root / "evidence")).ingest(manifest, root)

    def test_unbalanced_sexpression_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_sexpr("(kicad_pcb (net 1 GND)")


if __name__ == "__main__":
    unittest.main()
