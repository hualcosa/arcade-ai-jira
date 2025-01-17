import json
from typing import Annotated

from arcade.sdk import tool

from arcade_jira.tools.constants import JiraConfig
from arcade_jira.tools.utils import _handle_jira_api_error, _send_jira_request


@tool()
async def create_issue(
    project_key: Annotated[str, "The project key where the issue will be created"],
    summary: Annotated[str, "The issue summary/title"],
    description: Annotated[str, "The issue description"],
    issue_type: Annotated[str, "The type of issue (e.g., 'Bug', 'Task', 'Story')"],
) -> Annotated[str, "The key of the created issue"]:
    """Create a new issue in Jira."""
    jira_config = JiraConfig.from_env()

    # Format description as Atlassian Document Format
    description_adf = {
        "version": 1,
        "type": "doc",
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}],
    }

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description_adf,
            "issuetype": {"name": issue_type},
        }
    }

    response = await _send_jira_request("POST", "/issue", jira_config, json_data=payload)

    if response.status_code == 201:
        data: dict[str, str] = response.json()
        return data["key"]

    _handle_jira_api_error(response)
    return ""


@tool()
async def transition_issue(
    issue_key: Annotated[str, "The issue key (e.g., 'PROJECT-123')"],
    transition_id: Annotated[str, "The ID of the transition to perform"],
) -> Annotated[bool, "True if the transition was successful"]:
    """Transition a Jira issue to a new status."""
    jira_config = JiraConfig.from_env()

    payload = {"transition": {"id": transition_id}}

    response = await _send_jira_request(
        "POST", f"/issue/{issue_key}/transitions", jira_config, json_data=payload
    )

    if response.status_code == 204:
        return True

    _handle_jira_api_error(response)
    return False


@tool()
async def list_project_issues(
    project_key: Annotated[str, "The project key to list issues from"],
    max_results: Annotated[int, "Maximum number of issues to return"] = 50,
) -> Annotated[
    list[str],
    "List of JSON strings representing issues, each containing key and fields "
    "with summary, status, and issuetype information",
]:
    """List issues in a Jira project."""
    jira_config = JiraConfig.from_env()

    params = {
        "jql": f'project = "{project_key}"',
        "maxResults": max_results,
        "fields": "summary,status,issuetype",
        "validateQuery": "strict",
    }

    response = await _send_jira_request("GET", "/search", jira_config, params=params)

    if response.status_code == 200:
        data = response.json()
        # Convert each issue to a JSON string
        return [json.dumps(issue) for issue in data["issues"]]

    _handle_jira_api_error(response)
    return []


@tool()
async def delete_issue(
    issue_key: Annotated[str, "The issue key to delete"],
) -> Annotated[bool, "True if the issue was successfully deleted"]:
    """Delete a Jira issue."""
    jira_config = JiraConfig.from_env()

    response = await _send_jira_request("DELETE", f"/issue/{issue_key}", jira_config)

    if response.status_code == 204:
        return True

    _handle_jira_api_error(response)
    return False


@tool()
async def get_issue_transitions(
    issue_key: Annotated[str, "The issue key (e.g., 'PROJECT-123')"],
) -> Annotated[
    list[str],
    "List of JSON strings representing transitions, each containing id, name, "
    "and destination status information",
]:
    """Get all available transitions for a Jira issue."""
    jira_config = JiraConfig.from_env()

    response = await _send_jira_request(
        "GET",
        f"/issue/{issue_key}/transitions",
        jira_config,
        params={"expand": "transitions.fields"},
    )

    if response.status_code == 200:
        data = response.json()
        return [json.dumps(transition) for transition in data["transitions"]]

    _handle_jira_api_error(response)
    return []
