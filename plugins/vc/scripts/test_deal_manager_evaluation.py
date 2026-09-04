#!/usr/bin/env python3
"""Failure-injection checks for the live evaluation's deterministic oracle."""
import unittest

from evaluate_deal_manager import DEFINITION, TASK, evaluate


class DealManagerEvaluationTests(unittest.TestCase):
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

    def test_fund_clarification_must_name_the_missing_fund(self):
        self.assertTrue(evaluate({"mayCreateTasks": False, "askOneFocusedQuestion": True,
                                  "unresolvedField": "fund_id"}, [], "Proceed?", "Proceed?", True))


if __name__ == "__main__":
    unittest.main()
