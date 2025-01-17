import json

import pytest

from arcade_jira.tools.issues import (
    create_issue,
    delete_issue,
    get_issue_transitions,
    list_project_issues,
    transition_issue,
)

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_create_issue() -> None:
    project_key = "TEST"
    summary = "Test Issue from Automated Test"
    description = "This is a test issue created by automated testing"
    issue_type = "Task"

    try:
        # Create the issue
        issue_key = await create_issue(
            project_key=project_key,
            summary=summary,
            description=description,
            issue_type=issue_type,
        )

        # Verify the response format
        assert isinstance(issue_key, str)
        assert issue_key.startswith(f"{project_key}-")
        assert len(issue_key.split("-")) == 2  # Format should be "PROJECT-123"
        assert issue_key.split("-")[1].isdigit()  # Issue number should be numeric

        # Clean up
        await delete_issue(issue_key)
    except Exception as e:
        pytest.fail(f"Test failed: {e!s}")


@pytest.mark.asyncio
async def test_list_project_issues() -> None:
    project_key = "TEST"
    max_results = 10
    try:
        # Create a test issue
        issue_key = await create_issue(
            project_key=project_key,
            summary="Test Issue for Listing",
            description="This is a test issue for testing list functionality",
            issue_type="Task",
        )
        # Test listing issues
        issues = await list_project_issues(project_key, max_results=max_results)

        # Verify response format
        assert isinstance(issues, list)
        assert len(issues) > 0
        assert len(issues) <= max_results

        # Verify each issue is a valid JSON string containing the expected fields
        for issue_str in issues:
            assert isinstance(issue_str, str)
            issue = json.loads(issue_str)  # Should parse without error
            assert "key" in issue
            assert issue["key"].startswith(f"{project_key}-")
            assert "fields" in issue
            fields = issue["fields"]
            assert "summary" in fields
            assert "status" in fields
            assert "issuetype" in fields

        # Clean up
        await delete_issue(issue_key)
    except Exception as e:
        pytest.fail(f"Test failed: {e!s}")


@pytest.mark.asyncio
async def test_transition_issue() -> None:
    project_key = "TEST"

    try:
        # Create a test issue
        issue_key = await create_issue(
            project_key=project_key,
            summary="Test Issue for Transition",
            description="This is a test issue for testing transition functionality",
            issue_type="Task",
        )

        # Get available transitions for the issue
        transitions = await get_issue_transitions(issue_key)
        assert len(transitions) > 0

        # Parse transitions and find "In Progress"
        parsed_transitions = [json.loads(t) for t in transitions]
        transition = next(t for t in parsed_transitions if t["to"]["name"].lower() == "in progress")

        # Test transitioning the issue using the found transition ID
        transition_success = await transition_issue(issue_key, transition_id=transition["id"])
        assert transition_success is True

        # Clean up
        await delete_issue(issue_key)
    except Exception as e:
        pytest.fail(f"Test failed: {e!s}")


@pytest.mark.asyncio
async def test_get_issue_transitions() -> None:
    project_key = "TEST"

    try:
        # Create a test issue
        issue_key = await create_issue(
            project_key=project_key,
            summary="Test Issue for Getting Transitions",
            description="This is a test issue for testing get transitions functionality",
            issue_type="Task",
        )

        # Get transitions
        transitions = await get_issue_transitions(issue_key)

        # Verify response format
        assert isinstance(transitions, list)
        assert len(transitions) > 0

        # Verify structure of each transition
        for transition_str in transitions:
            assert isinstance(transition_str, str)
            transition = json.loads(transition_str)  # Should parse without error
            assert "id" in transition
            assert "name" in transition
            assert "to" in transition
            assert isinstance(transition["to"], dict)
            assert "name" in transition["to"]
            assert "id" in transition["to"]

        # Clean up
        await delete_issue(issue_key)
    except Exception as e:
        pytest.fail(f"Test failed: {e!s}")


@pytest.mark.asyncio
async def test_delete_issue() -> None:
    project_key = "TEST"

    try:
        # Create a test issue
        issue_key = await create_issue(
            project_key=project_key,
            summary="Test Issue for Deletion",
            description="This is a test issue for testing deletion functionality",
            issue_type="Task",
        )

        # Test deletion
        # API returns 204 on success which our function converts to True
        deletion_success = await delete_issue(issue_key)
        assert deletion_success is True

    except Exception as e:
        pytest.fail(f"Test failed: {e!s}")
