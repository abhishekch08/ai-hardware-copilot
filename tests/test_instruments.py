import tempfile
import unittest
from datetime import datetime, timedelta, timezone

from ai_hardware_copilot.evidence import EvidenceStore
from ai_hardware_copilot.instruments import (
    BenchController,
    GenericScpiDmm,
    GenericScpiOscilloscope,
    InstrumentAction,
    InstrumentDescriptor,
    InstrumentPolicy,
    MockInstrument,
    SafetyEnvelope,
    approval_for,
)


class FakeTransport:
    def __init__(self, replies=None):
        self.replies = replies or {}
        self.commands = []

    def write(self, command):
        self.commands.append(command)

    def query(self, command):
        self.commands.append(command)
        return self.replies[command]


class InstrumentTests(unittest.TestCase):
    def make_controller(self, temporary):
        descriptor = InstrumentDescriptor(
            instrument_id="PSU-1", kind="power_supply", manufacturer="Mock",
            model="SIM", serial_number="001", firmware_version="1.0",
            capabilities=["identify", "set_voltage", "set_current_limit", "set_output", "measure_current"],
        )
        driver = MockInstrument(descriptor, {"measure_current": (0.004, "A")})
        envelope = SafetyEnvelope(["PSU-1"], ["REV-A"], max_voltage_v=4.2, max_current_a=0.1)
        controller = BenchController([driver], InstrumentPolicy(envelope), EvidenceStore(temporary))
        return controller, driver

    def test_overvoltage_and_unapproved_enable_are_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            controller, _ = self.make_controller(temporary)
            with self.assertRaises(PermissionError):
                controller.execute(InstrumentAction(
                    "PSU-1", "set_voltage", {"voltage_v": 5.0}, "REV-A", "AI-09"
                ))
            enable = InstrumentAction("PSU-1", "set_output", {"enabled": True}, "REV-A", "AI-09")
            with self.assertRaises(PermissionError):
                controller.execute(enable)

    def test_exact_action_approval_and_measurement_are_audited(self):
        with tempfile.TemporaryDirectory() as temporary:
            controller, driver = self.make_controller(temporary)
            enable = InstrumentAction("PSU-1", "set_output", {"enabled": True}, "REV-A", "AI-09")
            expiry = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
            result = controller.execute(enable, approval_for(enable, "human@example", expiry, "bench test"))
            self.assertTrue(result.value)
            self.assertTrue(driver.state["output_enabled"])
            measured = controller.execute(InstrumentAction(
                "PSU-1", "measure_current", {}, "REV-A", "AI-09"
            ))
            self.assertEqual(measured.units, "A")
            self.assertTrue(controller.evidence.verify(measured.evidence_ref))

    def test_typed_dmm_and_scope_drivers_emit_only_driver_owned_scpi(self):
        dmm_transport = FakeTransport({"MEAS:VOLT:DC?": "1.8001"})
        dmm_descriptor = InstrumentDescriptor(
            "DMM-1", "dmm", "Example", "DMM", "2", "1.0",
            ["measure_voltage"],
        )
        dmm = GenericScpiDmm(dmm_descriptor, dmm_transport)
        value, units, _ = dmm.execute(InstrumentAction("DMM-1", "measure_voltage"))
        self.assertEqual((value, units), (1.8001, "V"))
        self.assertEqual(dmm_transport.commands, ["MEAS:VOLT:DC?"])

        scope_transport = FakeTransport({"WAV:DATA?": "0.0,0.5,1.0"})
        scope_descriptor = InstrumentDescriptor(
            "SCOPE-1", "oscilloscope", "Example", "SCOPE", "3", "1.0",
            ["configure_channel", "capture_waveform"],
        )
        scope = GenericScpiOscilloscope(scope_descriptor, scope_transport)
        scope.execute(InstrumentAction(
            "SCOPE-1", "configure_channel",
            {"channel": 2, "scale_v_per_div": 0.5, "offset_v": 0.0}, "REV-A",
        ))
        points, units, settings = scope.execute(InstrumentAction(
            "SCOPE-1", "capture_waveform", {"channel": 2}, "REV-A",
        ))
        self.assertEqual(points, [0.0, 0.5, 1.0])
        self.assertEqual(units, "V")
        self.assertEqual(settings["points"], 3)

    def test_scope_rejects_nonfinite_waveform(self):
        transport = FakeTransport({"WAV:DATA?": "0.0,nan"})
        descriptor = InstrumentDescriptor(
            "SCOPE-1", "oscilloscope", "Example", "SCOPE", "3", "1.0",
            ["capture_waveform"],
        )
        scope = GenericScpiOscilloscope(descriptor, transport)
        with self.assertRaises(ValueError):
            scope.execute(InstrumentAction("SCOPE-1", "capture_waveform"))


if __name__ == "__main__":
    unittest.main()
