from pathlib import Path

from ai_hardware_copilot.config import load_yaml
from ai_hardware_copilot.directory import AgentDirectory
from ai_hardware_copilot.models import TaskManifest
from ai_hardware_copilot.routing import RoutingPolicy


ROOT = Path(__file__).resolve().parents[1]


def directory() -> AgentDirectory:
    return AgentDirectory.from_directory(ROOT / "config" / "agents")


def routing(agent_directory: AgentDirectory | None = None) -> RoutingPolicy:
    agent_directory = agent_directory or directory()
    return RoutingPolicy(
        agent_directory,
        load_yaml(ROOT / "config" / "mandatory_review_rules.yaml"),
        load_yaml(ROOT / "config" / "capability_graph.yaml"),
    )


def product_task(**changes) -> TaskManifest:
    value = {
        "task_id": "test-product-001",
        "title": "Wearable sensor board product architecture",
        "objective": "Design a wearable sensor board with safe power, BLE and optical sensing.",
        "description": "New PCB, battery charger, PMIC, PPG AFE, BLE antenna, firmware and validation.",
        "task_type": "new_product_design",
        "risk_tier": "T3",
        "domains": ["systems", "product", "electrical", "embedded"],
        "interfaces": ["pcb", "power", "battery", "rf", "sensor"],
        "keywords": ["wearable", "ppg", "ble", "charging", "firmware"],
        "requirements": ["Safe charging", "Traceable sensor data"],
        "constraints": ["Small battery", "On-body operation"],
        "evidence_refs": ["evidence/reference-requirements.md"],
        "proposal": {"revision": "A"},
        "physical_action": False,
    }
    value.update(changes)
    return TaskManifest.from_dict(value)

