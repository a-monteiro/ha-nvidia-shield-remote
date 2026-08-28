"""Focused unit tests for the native Shield accessory-locator request."""

from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
import sys
import unittest


PROTOCOL_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "nvidia_shield_remote"
    / "protocol.py"
)
SPEC = importlib.util.spec_from_file_location("shield_protocol", PROTOCOL_PATH)
assert SPEC is not None and SPEC.loader is not None
protocol = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = protocol
SPEC.loader.exec_module(protocol)


class AccessoryLocatorPayloadTests(unittest.TestCase):
    """Verify the app-derived locator payload remains exact."""

    def test_find_all_payload_is_expected_protobuf_envelope(self) -> None:
        self.assertEqual(
            bytes.fromhex(protocol.ACCESSORY_LOCATOR_FIND_ALL_PAYLOAD),
            bytes.fromhex("08 f3 07 12 02 08 01"),
        )

    def test_locator_uses_the_command_transport(self) -> None:
        client = protocol.ShieldProtocolClient(
            "127.0.0.1",
            8987,
            credentials=protocol.ShieldCredentials("cert", "key"),
        )
        payloads: list[str] = []
        client._send_command_payloads = payloads.extend

        client._locate_remote()

        self.assertEqual(payloads, [protocol.ACCESSORY_LOCATOR_FIND_ALL_PAYLOAD])

    def test_locator_requires_pairing_credentials(self) -> None:
        client = protocol.ShieldProtocolClient("127.0.0.1", 8987)

        with self.assertRaises(protocol.ShieldNotPairedError):
            client._locate_remote()


class AccessoryLocatorAsyncTests(unittest.TestCase):
    """Verify the public async API dispatches its worker method."""

    def test_async_locator_dispatches(self) -> None:
        client = protocol.ShieldProtocolClient("127.0.0.1", 8987)
        called = False

        def fake_locate() -> None:
            nonlocal called
            called = True

        client._locate_remote = fake_locate
        asyncio.run(client.async_locate_remote())
        self.assertTrue(called)
