#!/usr/bin/env python3
"""Guard Origination's external discovery and execution boundary."""
from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_pack", ROOT / "scripts/validate_pack.py")
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
AGENTS = (
    "vc_origination_manager",
    "vc_origination_candidate_manager",
    "vc_sourcing_line_manager",
    "vc_origination_scout",
    "vc_sourcing_operator",
)


class OriginationConnectedAppsTests(unittest.TestCase):
    def test_current_agent_contracts_allow_connected_reads(self) -> None:
        for agent in AGENTS:
            with self.subTest(agent=agent):
                template = yaml.safe_load((ROOT / f"alludium/agent-templates/{agent}.yaml").read_text())
                VALIDATOR.validate_origination_connected_app_access(agent, template)

    def test_rejects_missing_or_static_tool_discovery(self) -> None:
        for policy in (None, "EXPLICIT_TOOLS"):
            with self.subTest(policy=policy), self.assertRaises(SystemExit):
                VALIDATOR.validate_origination_connected_app_access(
                    "vc_sourcing_operator",
                    {"capabilityAccess": {"tools": {
                        "policy": policy, "connectedApplicationExecutionMode": "READ_ONLY",
                    }}},
                )

    def test_rejects_implicit_or_unrestricted_external_execution(self) -> None:
        template = {"capabilityAccess": {"tools": {"policy": "ALL_CONNECTED_APPS"}}}
        for mode in (None, "READ_WRITE"):
            value = copy.deepcopy(template)
            if mode is not None:
                value["capabilityAccess"]["tools"]["connectedApplicationExecutionMode"] = mode
            with self.subTest(mode=mode), self.assertRaises(SystemExit):
                VALIDATOR.validate_origination_connected_app_access("vc_sourcing_operator", value)


if __name__ == "__main__":
    unittest.main()
