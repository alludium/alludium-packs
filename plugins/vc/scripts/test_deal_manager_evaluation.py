#!/usr/bin/env python3
"""Failure-injection and prompt-contract checks for Deal Manager evaluation."""
from pathlib import Path
import unittest

import yaml

from evaluate_deal_manager import DEFINITION, TASK, aggregate_usage, evaluate


ROOT = Path(__file__).resolve().parents[3]
DEAL_MANAGER_TEMPLATES = (
    ROOT / "plugins/vc/alludium/agent-templates/vc_deal_manager.yaml",
    ROOT / "plugins/vc/alludium/agent-templates/vc_deal_pipeline_manager.yaml",
)


class DealManagerEvaluationTests(unittest.TestCase):
    def test_user_facing_guidance_translates_internal_diligence_language(self):
        for path in DEAL_MANAGER_TEMPLATES:
            with self.subTest(template=path.name):
                template = yaml.safe_load(path.read_text(encoding="utf-8"))
                prompt = template["prompt"]["template"]
                self.assertIn("plain investment-workflow language", prompt)
                self.assertIn("missing evidence or decision question", prompt)
                self.assertIn("what the user should do next", prompt)
                self.assertIn('"bounded validation program"', prompt)

    def test_pipeline_manager_prompt_preserves_waivers_and_handles_empty_fund_searches(self):
        template_path = Path(__file__).parents[1] / "alludium" / "agent-templates" / "vc_deal_pipeline_manager.yaml"
        prompt = yaml.safe_load(template_path.read_text())[
            "prompt"
        ]["template"]
        for phrase in (
            "An explicit user waiver of a nonessential gap remains in force for the current authorized workflow",
            "Yes, please",
            "do not treat a zero-result filtered Fund lookup as evidence that no Fund exists",
            "repeat the bounded lookup without a query",
            "company, market, traction, and team",
            "one concrete next action",
        ):
            self.assertIn(phrase, prompt)

    def test_usage_aggregates_every_case_not_just_the_last(self):
        results = [{"usage": {"inputTokens": 10, "outputTokens": 2, "totalTokens": 12}},
                   {"usage": {"inputTokens": 30, "outputTokens": 4, "totalTokens": 34}}]
        self.assertEqual({"inputTokens": 40, "outputTokens": 6, "totalTokens": 46}, aggregate_usage(results))

    def test_redundant_confirmation_fails_without_creation(self):
        errors = evaluate({"mayCreateTasks": True, "requiresRedundantConfirmation": False}, [],
                          "Please confirm that I should create the task.",
                          "Please confirm that I should create the task.", True)
        self.assertTrue(any("creation" in error for error in errors))
        self.assertTrue(any("another user response" in error for error in errors))

    def test_agent_origin_creation_attempt_fails_even_when_tool_rejects_it(self):
        calls = [{"name": "task-management_createTask", "input": {}, "error": "Forbidden"}]
        self.assertTrue(any("without authorization" in error for error in
                            evaluate({"mayCreateTasks": False}, calls, "May I proceed?", "May I proceed?", True)))

    def test_duplicate_creation_fails(self):
        calls = [{"name": "task-management_createTask", "input": {"taskDefinitionId": DEFINITION}}]
        self.assertTrue(evaluate({"mayCreateTasks": False, "readBackExistingTaskId": "screening-task-1"},
                                 calls, "Started.", "Started.", True))

    def test_claimed_success_without_readback_fails(self):
        calls = [{"name": "project-task_listByProject", "input": {}},
                 {"name": "task-management_createTask", "input": {"taskDefinitionId": DEFINITION}}]
        self.assertTrue(any("read back" in error for error in evaluate(
            {"mayCreateTasks": True, "readBackCreatedTask": True}, calls, "Started.", "Started.", True)))

    def test_wrong_typed_definition_fails(self):
        calls = [{"name": "task-management_createTask", "input": {"taskDefinitionId": "wrong"}}]
        self.assertTrue(any("typed definition" in error for error in
                            evaluate({"mayCreateTasks": True}, calls, "Started.", "Started.", True)))

    def test_wrong_workflow_slug_fails(self):
        calls = [{"name": "task-management_createTask", "input": {"taskDefinitionId": DEFINITION},
                  "resolvedTaskDefinitionSlug": "wrong-workflow"}]
        self.assertTrue(any("workflow slug" in error for error in evaluate(
            {"mayCreateTasks": True, "selectedTaskDefinitionSlug": "run-investment-fit-screen"}, calls, "Started.", "Started.", True)))

    def test_negative_case_cannot_claim_execution_without_tools(self):
        self.assertTrue(evaluate({"mayCreateTasks": False}, [], "I created the task.", "I created the task.", True))

    def test_valid_creation_and_readback_pass(self):
        calls = [{"name": "project-task_listByProject", "input": {}},
                 {"name": "task-management_createTask", "input": {"taskDefinitionId": DEFINITION}},
                 {"name": "task-management_getTaskDetail", "input": {"taskId": TASK}}]
        self.assertEqual([], evaluate({"mayCreateTasks": True, "readBackCreatedTask": True,
                                       "requiresRedundantConfirmation": False}, calls, "Started.", "Started.", True))

    def test_unfinished_model_turn_fails(self):
        self.assertTrue(evaluate({"mayCreateTasks": False}, [], "", "", False))

    def test_repeated_clarification_question_fails(self):
        text = "What should I produce? A summary or a screen?"
        self.assertTrue(evaluate({"mayCreateTasks": False, "askOneFocusedQuestion": True},
                                 [], text, text, True))

    def test_agent_recommendation_requests_approval_without_mutation(self):
        text = "Deal Analyst recommends screening this deck. Do you approve starting that work?"
        self.assertEqual([], evaluate({"mayCreateTasks": False, "requiresHumanApproval": True},
                                      [], text, text, True))

    def test_fund_clarification_must_name_the_missing_fund(self):
        self.assertTrue(evaluate({"mayCreateTasks": False, "askOneFocusedQuestion": True,
                                  "unresolvedField": "fund_id"}, [], "Proceed?", "Proceed?", True))


if __name__ == "__main__":
    unittest.main()
