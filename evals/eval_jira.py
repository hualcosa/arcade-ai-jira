from arcade.sdk import ToolCatalog
from arcade.sdk.eval import BinaryCritic, EvalRubric, EvalSuite, SimilarityCritic, tool_eval

from arcade_jira.tools.issues import (
    create_issue,
    delete_issue,
    get_issue_transitions,
    list_project_issues,
    transition_issue,
)

# Evaluation rubric
rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
)

catalog = ToolCatalog()
catalog.add_tool(create_issue, "Jira")
catalog.add_tool(transition_issue, "Jira")
catalog.add_tool(list_project_issues, "Jira")
catalog.add_tool(delete_issue, "Jira")
catalog.add_tool(get_issue_transitions, "Jira")


@tool_eval()
def jira_issues_eval_suite() -> EvalSuite:
    """Create an evaluation suite for Jira issue management tools."""
    suite = EvalSuite(
        name="Jira Issues Tools Evaluation",
        system_message=(
            "You are an AI assistant that can manage Jira issues using the provided tools."
        ),
        catalog=catalog,
        rubric=rubric,
    )

    # Create Issue Cases
    suite.add_case(
        name="Create bug issue",
        user_message=(
            "Create a bug in the ARCADE project. The login button is not"
            " working on Safari browsers. Title it 'Login Button Safari Issue'"
        ),
        expected_tool_calls=[
            (
                create_issue,
                {
                    "project_key": "ARCADE",
                    "summary": "Login Button Safari Issue",
                    "description": "The login button is not working on Safari browsers.",
                    "issue_type": "Bug",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="project_key", weight=0.25),
            SimilarityCritic(critic_field="summary", weight=0.25),
            SimilarityCritic(critic_field="description", weight=0.25),
            BinaryCritic(critic_field="issue_type", weight=0.25),
        ],
    )

    suite.add_case(
        name="Create story with minimal info",
        user_message="make a story ticket in the ARCADE project called 'User Authentication Flow'",
        expected_tool_calls=[
            (
                create_issue,
                {
                    "project_key": "ARCADE",
                    "summary": "User Authentication Flow",
                    "description": "User Authentication Flow story",
                    "issue_type": "Story",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="project_key", weight=0.25),
            SimilarityCritic(critic_field="summary", weight=0.25),
            SimilarityCritic(critic_field="description", weight=0.25),
            BinaryCritic(critic_field="issue_type", weight=0.25),
        ],
    )

    # List Project Issues Cases
    suite.add_case(
        name="List project issues with default limit",
        user_message="show me all the issues in the ARCADE project",
        expected_tool_calls=[
            (
                list_project_issues,
                {
                    "project_key": "ARCADE",
                    "max_results": 50,
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="project_key", weight=0.6),
            BinaryCritic(critic_field="max_results", weight=0.4),
        ],
    )

    suite.add_case(
        name="List project issues with custom limit",
        user_message="get me the first 10 issues from the ARCADE project",
        expected_tool_calls=[
            (
                list_project_issues,
                {
                    "project_key": "ARCADE",
                    "max_results": 10,
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="project_key", weight=0.6),
            BinaryCritic(critic_field="max_results", weight=0.4),
        ],
    )

    # Transition Issue Cases
    history_with_transitions = [
        {"role": "user", "content": "what are the possible transitions for ARCADE-123?"},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "call_abc123",
                    "type": "function",
                    "function": {
                        "name": "Jira_GetIssueTransitions",
                        "arguments": '{"issue_key": "ARCADE-123"}',
                    },
                }
            ],
        },
        {
            "role": "tool",
            "content": '[{"id": "21", "name": "In Progress"}, {"id": "31", "name": "Done"}]',
            "tool_call_id": "call_abc123",
            "name": "Jira_GetIssueTransitions",
        },
    ]

    suite.add_case(
        name="Transition issue with history context",
        user_message="move ARCADE-123 to In Progress",
        expected_tool_calls=[
            (
                transition_issue,
                {
                    "issue_key": "ARCADE-123",
                    "transition_id": "21",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="issue_key", weight=0.5),
            BinaryCritic(critic_field="transition_id", weight=0.5),
        ],
        additional_messages=history_with_transitions,
    )

    suite.add_case(
        name="Get issue transitions",
        user_message="what status changes are available for ARCADE-456?",
        expected_tool_calls=[
            (
                get_issue_transitions,
                {
                    "issue_key": "ARCADE-456",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="issue_key", weight=1.0),
        ],
    )

    # Delete Issue Cases
    suite.add_case(
        name="Delete issue",
        user_message="please remove ARCADE-789 from Jira",
        expected_tool_calls=[
            (
                delete_issue,
                {
                    "issue_key": "ARCADE-789",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="issue_key", weight=1.0),
        ],
    )

    # Complex Multi-Tool Cases
    # suite.add_case(
    #     name="Create and transition issue",
    #     user_message=(
    # "create a task in ARCADE called 'Update Dependencies' and move it to In Progress"
    # ),
    #     expected_tool_calls=[
    #         (
    #             create_issue,
    #             {
    #                 "project_key": "ARCADE",
    #                 "summary": "Update Dependencies",
    #                 "description": "Task to update dependencies",
    #                 "issue_type": "Task",
    #             },
    #         ),
    #         (
    #             get_issue_transitions,
    #             {
    #                 "issue_key": "<created_issue_key>",
    #             },
    #         ),
    #         (
    #             transition_issue,
    #             {
    #                 "issue_key": "<created_issue_key>",
    #                 "transition_id": "<transition_id>",
    #             },
    #         ),
    #     ],
    #     critics=[
    #         BinaryCritic(critic_field="project_key", weight=0.2),
    #         SimilarityCritic(critic_field="summary", weight=0.2),
    #         BinaryCritic(critic_field="issue_type", weight=0.2),
    #         BinaryCritic(critic_field="issue_key", weight=0.2),
    #         BinaryCritic(critic_field="transition_id", weight=0.2),
    #     ],
    # )

    return suite
