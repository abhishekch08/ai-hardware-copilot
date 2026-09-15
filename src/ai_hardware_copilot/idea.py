"""Deterministic browser-intake conversion into a strict conference task manifest."""

from __future__ import annotations

import re
import uuid
from typing import Any

from .models import TaskManifest


DOMAIN_TERMS: dict[str, tuple[str, ...]] = {
    "systems": ("architecture", "system", "product", "requirements", "integration"),
    "electrical": (
        "circuit", "electronic", "pcb", "sensor", "analog", "digital", "battery",
        "power", "pmic", "charger", "antenna", "rf", "signal integrity",
    ),
    "embedded": (
        "firmware", "microcontroller", "mcu", "rtos", "bluetooth", "ble", "uart",
        "i2c", "spi", "can", "jtag", "swd", "driver",
    ),
    "ai_software_data": (
        "ai", "model", "algorithm", "computer vision", "camera", "mobile", "ios",
        "android", "web", "cloud", "backend", "data", "machine learning",
    ),
    "mechanical_industrial_wearable": (
        "mechanical", "enclosure", "thermal", "ergonomic", "wearable", "ring",
        "watch", "glasses", "headset", "skin", "waterproof", "cmf",
    ),
    "test_quality_safety": (
        "test", "validation", "reliability", "safety", "compliance", "calibration",
        "debug", "measurement", "failure",
    ),
    "manufacturing_supply_chain": (
        "manufacturing", "assembly", "supplier", "cost", "bom", "production", "yield",
        "dfm", "dfa", "tooling",
    ),
    "security_enterprise": (
        "security", "privacy", "on-prem", "enterprise", "encryption", "rbac", "audit",
    ),
    "science_research": (
        "research", "experiment", "physiology", "clinical", "biomedical", "physics",
        "statistics", "hypothesis",
    ),
    "business_market_legal": (
        "market", "customer", "pricing", "subscription", "finance", "patent", "legal",
        "regulatory", "go-to-market", "startup",
    ),
    "xr_spatial": ("ar", "vr", "xr", "augmented reality", "virtual reality", "spatial"),
}

INTERFACE_TERMS: dict[str, tuple[str, ...]] = {
    "pcb": ("pcb", "board", "schematic", "ecad"),
    "power": ("power", "battery", "pmic", "charger", "rail", "current"),
    "sensors": ("sensor", "ppg", "imu", "temperature", "electrode", "camera"),
    "firmware": ("firmware", "mcu", "rtos", "driver", "jtag", "swd"),
    "wireless": ("bluetooth", "ble", "wifi", "antenna", "rf", "nfc"),
    "mechanical": ("mechanical", "enclosure", "thermal", "waterproof", "ergonomic"),
    "manufacturing": ("manufacturing", "assembly", "production", "yield", "supplier"),
    "mobile": ("mobile", "ios", "android", "app"),
    "cloud": ("cloud", "backend", "web", "api"),
    "ai_models": ("ai", "model", "machine learning", "algorithm"),
    "xr": ("ar", "vr", "xr", "glasses", "headset", "spatial"),
    "evidence": ("test", "validation", "measurement", "evidence", "debug"),
}

STOP_WORDS = {
    "about", "after", "also", "build", "could", "design", "device", "from", "have",
    "into", "make", "need", "product", "should", "that", "their", "there", "these",
    "they", "this", "using", "want", "what", "when", "where", "which", "with", "would",
}


def task_from_idea(payload: dict[str, Any]) -> TaskManifest:
    """Convert a plain-language product idea to the deterministic task envelope.

    This function performs routing-oriented extraction only. It does not pretend to
    understand or validate the engineering proposal; the specialist conference owns that.
    """

    idea = _bounded_text(payload.get("idea"), "idea", minimum=20, maximum=100_000)
    title_value = str(payload.get("title", "")).strip()
    title = title_value or _derive_title(idea)
    if len(title) > 160:
        raise ValueError("title must contain at most 160 characters")

    risk_tier = str(payload.get("risk_tier", "T2")).upper()
    if risk_tier not in {"T1", "T2", "T3", "T4"}:
        raise ValueError("idea intake risk_tier must be T1, T2, T3 or T4")

    requirements = _string_list(payload.get("requirements", []), "requirements", maximum=100)
    constraints = _string_list(payload.get("constraints", []), "constraints", maximum=100)
    evidence_refs = _string_list(payload.get("evidence_refs", []), "evidence_refs", maximum=200)
    required_agents = _string_list(payload.get("required_agents", []), "required_agents", maximum=184)
    if risk_tier in {"T3", "T4"} and not evidence_refs:
        raise ValueError("T3/T4 idea conferences require verified evidence references")

    combined = " ".join([title, idea, *requirements, *constraints]).lower()
    explicit_domains = _string_list(payload.get("domains", []), "domains", maximum=30)
    domains = sorted(set(["systems", "product", *_matches(combined, DOMAIN_TERMS), *explicit_domains]))
    interfaces = sorted(set(_matches(combined, INTERFACE_TERMS)))
    keywords = _keywords(combined)

    task_id = str(payload.get("task_id", "")).strip()
    if not task_id:
        task_id = f"web-{_slug(title)}-{uuid.uuid4().hex[:8]}"

    rounds_value = payload.get("iterate_rounds", 3)
    if isinstance(rounds_value, bool):
        raise ValueError("iterate_rounds must be an integer from 0 through 10")
    if isinstance(rounds_value, str) and not re.fullmatch(r"\d+", rounds_value.strip()):
        raise ValueError("iterate_rounds must be an integer from 0 through 10")
    if isinstance(rounds_value, float) and not rounds_value.is_integer():
        raise ValueError("iterate_rounds must be an integer from 0 through 10")
    try:
        rounds = int(rounds_value)
    except (TypeError, ValueError) as exc:
        raise ValueError("iterate_rounds must be an integer from 0 through 10") from exc
    if not 0 <= rounds <= 10:
        raise ValueError("iterate_rounds must be an integer from 0 through 10")

    return TaskManifest.from_dict({
        "task_id": task_id,
        "title": title,
        "objective": str(payload.get("objective", "")).strip()
        or f"Develop and critically evaluate the product concept: {title}",
        "description": idea,
        "task_type": "new_product_design",
        "risk_tier": risk_tier,
        "domains": domains,
        "interfaces": interfaces,
        "keywords": keywords,
        "required_agents": required_agents,
        "requirements": requirements,
        "constraints": constraints,
        "evidence_refs": evidence_refs,
        "proposal": {
            "concept_stage": "idea_intake",
            "founder_input": idea,
            "requested_deliberation_rounds": rounds,
        },
        "proposal_version": 1,
        "physical_action": False,
        "metadata": {"source": "local_web", "intake_version": "1"},
    })


def _matches(text: str, mapping: dict[str, tuple[str, ...]]) -> list[str]:
    return [name for name, terms in mapping.items() if any(_contains(text, term) for term in terms)]


def _contains(text: str, term: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None


def _keywords(text: str) -> list[str]:
    phrases = [
        term for terms in (*DOMAIN_TERMS.values(), *INTERFACE_TERMS.values()) for term in terms
        if _contains(text, term)
    ]
    words = re.findall(r"[a-z][a-z0-9+-]{3,}", text)
    ranked: list[str] = []
    for item in [*phrases, *words]:
        if item not in STOP_WORDS and item not in ranked:
            ranked.append(item)
        if len(ranked) == 40:
            break
    return ranked


def _derive_title(idea: str) -> str:
    first_line = next((line.strip() for line in idea.splitlines() if line.strip()), idea.strip())
    words = first_line.split()
    title = " ".join(words[:10]).rstrip(".,;:-")
    return title if len(title) <= 160 else title[:157].rstrip() + "..."


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:48].rstrip("-")
    return slug or "product-idea"


def _bounded_text(value: Any, field: str, *, minimum: int, maximum: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be text")
    result = value.strip()
    if not minimum <= len(result) <= maximum:
        raise ValueError(f"{field} must contain between {minimum} and {maximum} characters")
    return result


def _string_list(value: Any, field: str, *, maximum: int) -> list[str]:
    if isinstance(value, str):
        values = [line.strip() for line in value.splitlines() if line.strip()]
    elif isinstance(value, list):
        values = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"{field} must contain non-empty strings")
            values.append(item.strip())
    else:
        raise ValueError(f"{field} must be a list of strings or newline-separated text")
    if len(values) > maximum:
        raise ValueError(f"{field} contains too many entries")
    return list(dict.fromkeys(values))
