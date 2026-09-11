"""Typed instrument control with deterministic policy enforcement.

The model never receives a raw-SCPI escape hatch. Drivers translate validated semantic
actions into vendor commands after the policy layer authorizes the exact action digest.
"""

from __future__ import annotations

import hashlib
import json
import math
import socket
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol

from .evidence import EvidenceRecord, EvidenceStore


READ_CAPABILITIES = {"identify", "measure_voltage", "measure_current", "capture_waveform"}
WRITE_CAPABILITIES = {"set_voltage", "set_current_limit", "configure_channel", "configure_trigger"}
STATE_CAPABILITIES = {"set_output"}


@dataclass(slots=True)
class InstrumentDescriptor:
    instrument_id: str
    kind: str
    manufacturer: str
    model: str
    serial_number: str
    firmware_version: str
    capabilities: list[str]


@dataclass(slots=True)
class InstrumentAction:
    instrument_id: str
    capability: str
    parameters: dict[str, Any] = field(default_factory=dict)
    hardware_revision: str | None = None
    requested_by: str = "system"

    @property
    def digest(self) -> str:
        canonical = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class ActionApproval:
    action_digest: str
    approved_by: str
    expires_at: str
    reason: str

    def valid_for(self, action: InstrumentAction) -> bool:
        try:
            expiry = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
        except ValueError:
            return False
        return (
            self.action_digest == action.digest
            and bool(self.approved_by.strip())
            and expiry > datetime.now(timezone.utc)
        )


@dataclass(slots=True)
class SafetyEnvelope:
    allowed_instruments: list[str]
    allowed_hardware_revisions: list[str]
    min_voltage_v: float = 0.0
    max_voltage_v: float = 5.5
    max_current_a: float = 1.0
    output_enable_requires_approval: bool = True


@dataclass(slots=True)
class InstrumentResult:
    action_digest: str
    instrument_id: str
    capability: str
    timestamp_utc: str
    value: Any
    units: str | None
    settings: dict[str, Any]
    evidence_ref: str | None = None


class InstrumentDriver(Protocol):
    descriptor: InstrumentDescriptor

    def execute(self, action: InstrumentAction) -> tuple[Any, str | None, dict[str, Any]]: ...


class InstrumentPolicy:
    def __init__(self, envelope: SafetyEnvelope):
        self.envelope = envelope

    def authorize(
        self,
        action: InstrumentAction,
        descriptor: InstrumentDescriptor,
        approval: ActionApproval | None = None,
    ) -> str:
        if action.instrument_id != descriptor.instrument_id:
            raise PermissionError("action and driver instrument identities differ")
        if action.instrument_id not in self.envelope.allowed_instruments:
            raise PermissionError("instrument is not in the safety envelope")
        if action.capability not in descriptor.capabilities:
            raise PermissionError("instrument does not declare the requested capability")
        if action.capability not in READ_CAPABILITIES | WRITE_CAPABILITIES | STATE_CAPABILITIES:
            raise PermissionError("unknown or raw instrument capability is prohibited")

        if action.capability in WRITE_CAPABILITIES | STATE_CAPABILITIES:
            if not action.hardware_revision:
                raise PermissionError("state-changing action requires hardware_revision")
            if action.hardware_revision not in self.envelope.allowed_hardware_revisions:
                raise PermissionError("hardware revision is outside the approved envelope")

        if action.capability == "set_voltage":
            voltage = _finite_number(action.parameters, "voltage_v")
            if not self.envelope.min_voltage_v <= voltage <= self.envelope.max_voltage_v:
                raise PermissionError("requested voltage is outside deterministic limits")
        elif action.capability == "set_current_limit":
            current = _finite_number(action.parameters, "current_a")
            if not 0 < current <= self.envelope.max_current_a:
                raise PermissionError("requested current limit is outside deterministic limits")
        elif action.capability == "set_output":
            enabled = action.parameters.get("enabled")
            if not isinstance(enabled, bool):
                raise ValueError("set_output requires boolean enabled")
            if enabled and self.envelope.output_enable_requires_approval:
                if approval is None or not approval.valid_for(action):
                    raise PermissionError("output enable requires approval for the exact action digest")

        return "P4" if action.capability in READ_CAPABILITIES else (
            "P6" if action.capability == "set_output" and action.parameters.get("enabled") else "P5"
        )


class BenchController:
    def __init__(
        self,
        drivers: list[InstrumentDriver],
        policy: InstrumentPolicy,
        evidence: EvidenceStore,
    ):
        self.drivers = {driver.descriptor.instrument_id: driver for driver in drivers}
        self.policy = policy
        self.evidence = evidence

    def execute(
        self, action: InstrumentAction, approval: ActionApproval | None = None
    ) -> InstrumentResult:
        try:
            driver = self.drivers[action.instrument_id]
        except KeyError as exc:
            raise KeyError(f"unknown instrument: {action.instrument_id}") from exc
        permission = self.policy.authorize(action, driver.descriptor, approval)
        value, units, settings = driver.execute(action)
        result = InstrumentResult(
            action_digest=action.digest,
            instrument_id=action.instrument_id,
            capability=action.capability,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            value=value,
            units=units,
            settings={"permission": permission, **settings},
        )
        evidence_record = self.evidence.register_json(
            asdict(result),
            kind="instrument_result",
            source_uri=f"instrument://{action.instrument_id}/{action.capability}",
            configuration={
                "instrument": asdict(driver.descriptor),
                "hardware_revision": action.hardware_revision,
                "action_digest": action.digest,
            },
            metadata={"requested_by": action.requested_by},
        )
        result.evidence_ref = evidence_record.evidence_id
        return result


class MockInstrument:
    """Deterministic instrument simulator for safety and orchestration tests."""

    def __init__(
        self,
        descriptor: InstrumentDescriptor,
        measurements: dict[str, tuple[Any, str | None]] | None = None,
    ):
        self.descriptor = descriptor
        self.measurements = measurements or {}
        self.state: dict[str, Any] = {"output_enabled": False, "voltage_v": 0.0, "current_limit_a": 0.0}

    def execute(self, action: InstrumentAction) -> tuple[Any, str | None, dict[str, Any]]:
        if action.capability == "identify":
            return asdict(self.descriptor), None, dict(self.state)
        if action.capability == "set_voltage":
            self.state["voltage_v"] = float(action.parameters["voltage_v"])
            return self.state["voltage_v"], "V", dict(self.state)
        if action.capability == "set_current_limit":
            self.state["current_limit_a"] = float(action.parameters["current_a"])
            return self.state["current_limit_a"], "A", dict(self.state)
        if action.capability == "set_output":
            self.state["output_enabled"] = bool(action.parameters["enabled"])
            return self.state["output_enabled"], None, dict(self.state)
        if action.capability in self.measurements:
            value, units = self.measurements[action.capability]
            return value, units, dict(self.state)
        if action.capability in {"configure_channel", "configure_trigger"}:
            self.state[action.capability] = dict(action.parameters)
            return True, None, dict(self.state)
        raise ValueError(f"mock has no response for capability: {action.capability}")


class ScpiTransport(Protocol):
    def write(self, command: str) -> None: ...
    def query(self, command: str) -> str: ...


class TcpScpiTransport:
    def __init__(self, host: str, port: int = 5025, timeout_s: float = 5.0, max_reply_bytes: int = 1_000_000):
        self.host = host
        self.port = port
        self.timeout_s = timeout_s
        self.max_reply_bytes = max_reply_bytes

    def write(self, command: str) -> None:
        _validate_generated_scpi(command)
        with socket.create_connection((self.host, self.port), timeout=self.timeout_s) as connection:
            connection.sendall((command + "\n").encode("ascii"))

    def query(self, command: str) -> str:
        _validate_generated_scpi(command)
        with socket.create_connection((self.host, self.port), timeout=self.timeout_s) as connection:
            connection.sendall((command + "\n").encode("ascii"))
            chunks: list[bytes] = []
            total = 0
            while True:
                block = connection.recv(min(65536, self.max_reply_bytes - total + 1))
                if not block:
                    break
                chunks.append(block)
                total += len(block)
                if total > self.max_reply_bytes:
                    raise ValueError("SCPI reply exceeds configured maximum")
                if b"\n" in block:
                    break
        return b"".join(chunks).decode("ascii", errors="strict").strip()


class GenericScpiPowerSupply:
    """Minimal common-SCPI PSU driver; every real model needs a conformance fixture."""

    def __init__(self, descriptor: InstrumentDescriptor, transport: ScpiTransport):
        self.descriptor = descriptor
        self.transport = transport

    def execute(self, action: InstrumentAction) -> tuple[Any, str | None, dict[str, Any]]:
        channel = int(action.parameters.get("channel", 1))
        if channel < 1 or channel > 16:
            raise ValueError("channel outside supported range")
        if action.capability == "identify":
            return self.transport.query("*IDN?"), None, {"channel": channel}
        if action.capability == "set_voltage":
            value = float(action.parameters["voltage_v"])
            self.transport.write(f"INST:NSEL {channel}")
            self.transport.write(f"VOLT {value:.9g}")
            return value, "V", {"channel": channel}
        if action.capability == "set_current_limit":
            value = float(action.parameters["current_a"])
            self.transport.write(f"INST:NSEL {channel}")
            self.transport.write(f"CURR {value:.9g}")
            return value, "A", {"channel": channel}
        if action.capability == "set_output":
            enabled = bool(action.parameters["enabled"])
            self.transport.write(f"INST:NSEL {channel}")
            self.transport.write("OUTP ON" if enabled else "OUTP OFF")
            return enabled, None, {"channel": channel}
        if action.capability == "measure_voltage":
            return float(self.transport.query(f"MEAS:VOLT? (@{channel})")), "V", {"channel": channel}
        if action.capability == "measure_current":
            return float(self.transport.query(f"MEAS:CURR? (@{channel})")), "A", {"channel": channel}
        raise ValueError(f"unsupported PSU capability: {action.capability}")


class GenericScpiDmm:
    """Minimal SCPI DMM adapter for read-only DC voltage/current acquisition."""

    def __init__(self, descriptor: InstrumentDescriptor, transport: ScpiTransport):
        self.descriptor = descriptor
        self.transport = transport

    def execute(self, action: InstrumentAction) -> tuple[Any, str | None, dict[str, Any]]:
        if action.capability == "identify":
            return self.transport.query("*IDN?"), None, {}
        if action.capability == "measure_voltage":
            return _finite_reply(self.transport.query("MEAS:VOLT:DC?")), "V", {"mode": "DC"}
        if action.capability == "measure_current":
            return _finite_reply(self.transport.query("MEAS:CURR:DC?")), "A", {"mode": "DC"}
        raise ValueError(f"unsupported DMM capability: {action.capability}")


class GenericScpiOscilloscope:
    """Narrow ASCII-waveform SCPI adapter; real models require conformance fixtures."""

    def __init__(
        self,
        descriptor: InstrumentDescriptor,
        transport: ScpiTransport,
        *,
        max_waveform_points: int = 100_000,
    ):
        self.descriptor = descriptor
        self.transport = transport
        self.max_waveform_points = max_waveform_points

    def execute(self, action: InstrumentAction) -> tuple[Any, str | None, dict[str, Any]]:
        if action.capability == "identify":
            return self.transport.query("*IDN?"), None, {}
        channel = _channel(action.parameters)
        if action.capability == "configure_channel":
            scale = _positive_finite_number(action.parameters, "scale_v_per_div")
            offset = _finite_number(action.parameters, "offset_v")
            self.transport.write(f"CHAN{channel}:SCAL {scale:.9g}")
            self.transport.write(f"CHAN{channel}:OFFS {offset:.9g}")
            return True, None, {
                "channel": channel,
                "scale_v_per_div": scale,
                "offset_v": offset,
            }
        if action.capability == "configure_trigger":
            level = _finite_number(action.parameters, "level_v")
            source = _channel({"channel": action.parameters.get("source_channel", channel)})
            self.transport.write(f"TRIG:EDGE:SOUR CHAN{source}")
            self.transport.write(f"TRIG:EDGE:LEV {level:.9g}")
            return True, None, {"source_channel": source, "level_v": level}
        if action.capability == "capture_waveform":
            self.transport.write(f"WAV:SOUR CHAN{channel}")
            self.transport.write("WAV:FORM ASC")
            reply = self.transport.query("WAV:DATA?")
            points = [] if not reply else [_finite_reply(item) for item in reply.split(",")]
            if len(points) > self.max_waveform_points:
                raise ValueError("waveform exceeds configured point limit")
            return points, "V", {"channel": channel, "encoding": "ASCII", "points": len(points)}
        raise ValueError(f"unsupported oscilloscope capability: {action.capability}")


def approval_for(action: InstrumentAction, approved_by: str, expires_at: str, reason: str) -> ActionApproval:
    return ActionApproval(action.digest, approved_by, expires_at, reason)


def _finite_number(parameters: dict[str, Any], key: str) -> float:
    if key not in parameters:
        raise ValueError(f"missing action parameter: {key}")
    value = float(parameters[key])
    if not math.isfinite(value):
        raise ValueError(f"action parameter must be finite: {key}")
    return value


def _positive_finite_number(parameters: dict[str, Any], key: str) -> float:
    value = _finite_number(parameters, key)
    if value <= 0:
        raise ValueError(f"action parameter must be positive: {key}")
    return value


def _finite_reply(value: str) -> float:
    result = float(value.strip())
    if not math.isfinite(result):
        raise ValueError("instrument returned a non-finite numeric value")
    return result


def _channel(parameters: dict[str, Any]) -> int:
    value = parameters.get("channel", 1)
    if isinstance(value, bool) or int(value) != float(value):
        raise ValueError("channel must be an integer")
    channel = int(value)
    if not 1 <= channel <= 16:
        raise ValueError("channel outside supported range")
    return channel


def _validate_generated_scpi(command: str) -> None:
    if not command or len(command) > 512 or any(character in command for character in "\r\n;"):
        raise ValueError("invalid generated SCPI command")
    try:
        command.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("SCPI command must be ASCII") from exc
