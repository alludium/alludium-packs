#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest
from pathlib import Path

import yaml
import validate_pack as validator


class ConnectedAppDiscoveryTests(unittest.TestCase):
    def templates(self):
        for agent_id in validator.CONNECTED_APP_AGENT_BUNDLES:
            path = validator.ROOT / "alludium" / "agent-templates" / f"{agent_id}.yaml"
            yield agent_id, yaml.safe_load(path.read_text())

    def test_all_four_roles_validate(self):
        self.assertEqual(set(validator.CONNECTED_APP_AGENT_BUNDLES), {
            "vc_deal_manager", "vc_deal_pipeline_manager", "vc_pipeline_autopilot", "vc_deal_analyst",
        })
        for agent_id, template in self.templates():
            with self.subTest(agent=agent_id):
                validator.validate_connected_app_agent(agent_id, template)

    def test_rejects_missing_or_expanded_bundles_for_every_role(self):
        for agent_id, template in self.templates():
            for bundle in template["capabilityProfile"]["bundles"]:
                changed = copy.deepcopy(template)
                changed["capabilityProfile"]["bundles"].remove(bundle)
                with self.subTest(agent=agent_id, missing=bundle), self.assertRaises(SystemExit):
                    validator.validate_connected_app_agent(agent_id, changed)
            for extra in ("UNKNOWN_BUNDLE", "PROJECT_OPERATIONS", "TASK_FOLLOW_UP"):
                changed = copy.deepcopy(template)
                changed["capabilityProfile"]["bundles"].append(extra)
                with self.subTest(agent=agent_id, extra=extra), self.assertRaises(SystemExit):
                    validator.validate_connected_app_agent(agent_id, changed)

    def test_rejects_policy_baseline_and_static_list_regressions(self):
        for agent_id, template in self.templates():
            for field, value in (("policy", "EXPLICIT_TOOLS"), ("connectedApplicationExecutionMode", None), ("connectedApplicationExecutionMode", "UNRESTRICTED")):
                changed = copy.deepcopy(template)
                changed["capabilityAccess"]["tools"][field] = value
                with self.subTest(agent=agent_id, field=field, value=value), self.assertRaises(SystemExit):
                    validator.validate_connected_app_agent(agent_id, changed)
            changed = copy.deepcopy(template)
            changed["capabilityProfile"]["baseline"] = "STANDARD_PLATFORM_AGENT"
            with self.subTest(agent=agent_id, baseline=True), self.assertRaises(SystemExit):
                validator.validate_connected_app_agent(agent_id, changed)
            for app in ("alludium-platform", "new-provider"):
                changed = copy.deepcopy(template)
                changed["mcpServers"] = {app: {"tools": [{"name": "some.operation"}]}}
                with self.subTest(agent=agent_id, app=app), self.assertRaises(SystemExit):
                    validator.validate_connected_app_agent(agent_id, changed)

    def test_manifest_cannot_drop_any_target_role(self):
        for agent_id in validator.CONNECTED_APP_AGENT_BUNDLES:
            manifest = {"surfaces": {"alludiumAgentTemplates": {
                "ids": [candidate for candidate in validator.CONNECTED_APP_AGENT_BUNDLES if candidate != agent_id],
            }}}
            with self.subTest(agent=agent_id), self.assertRaises(SystemExit):
                validator.validate_templates(manifest, set())


if __name__ == "__main__":
    unittest.main()
