"""Compatibility checks for the Home Assistant config flow."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest


COMPONENTS_PATH = Path(__file__).parents[1] / "custom_components"
sys.path.insert(0, str(COMPONENTS_PATH))


class ConfigFlowCompatibilityTests(unittest.TestCase):
    """The integration must register a handler on supported HA versions."""

    def test_config_flow_import_registers_domain_handler(self) -> None:
        from homeassistant import config_entries
        from nvidia_shield_remote.config_flow import NvidiaShieldRemoteConfigFlow

        self.assertIs(
            config_entries.HANDLERS.get("nvidia_shield_remote"),
            NvidiaShieldRemoteConfigFlow,
        )
