import base64

import httpx
from arcade.sdk.errors import ToolExecutionError

from arcade_jira.tools.constants import JiraConfig


async def _send_jira_request(
    method: str,
    endpoint: str,
    jira_config: JiraConfig,
    params: dict | None = None,
    json_data: dict | None = None,
) -> httpx.Response:
    """
    Send an asynchronous request to the Jira API.

    Args:
        method: The HTTP method (GET, POST, PUT, DELETE, etc.).
        endpoint: The API endpoint path (e.g., "/issue").
        jira_config: The Jira configuration object.
        params: Query parameters to include in the request.
        json_data: JSON data to include in the request body.

    Returns:
        The response object from the API request.

    Raises:
        ToolExecutionError: If the request fails for any reason.
    """
    url = f"{jira_config.base_url}/rest/api/3{endpoint}"

    # Create Basic Auth header
    auth_str = f"{jira_config.email}:{jira_config.api_token}"
    auth_bytes = auth_str.encode("ascii")
    auth_b64 = base64.b64encode(auth_bytes).decode("ascii")

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method, url, headers=headers, params=params, json=json_data
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            raise ToolExecutionError(str(e)) from e

    return response


def _handle_jira_api_error(response: httpx.Response) -> None:
    """
    Handle errors from the Jira API by mapping common status codes to ToolExecutionErrors.

    Args:
        response: The response object from the API request.

    Raises:
        ToolExecutionError: If the response contains an error status code.
    """
    status_code_map = {
        401: ToolExecutionError("Unauthorized: Invalid credentials"),
        403: ToolExecutionError("Forbidden: Insufficient permissions"),
        404: ToolExecutionError("Not Found: The requested resource does not exist"),
        429: ToolExecutionError("Too Many Requests: Rate limit exceeded"),
    }

    if response.status_code in status_code_map:
        raise status_code_map[response.status_code]
    elif response.status_code >= 400:
        error_msg = f"Error: {response.status_code} - {response.text}"
        raise ToolExecutionError(error_msg)


def _send_jira_request_sync(
    method: str,
    endpoint: str,
    jira_config: JiraConfig,
    params: dict | None = None,
    json_data: dict | None = None,
) -> httpx.Response:
    """
    Send a synchronous request to the Jira API.

    Args:
        method: The HTTP method (GET, POST, PUT, DELETE, etc.).
        endpoint: The API endpoint path (e.g., "/issue").
        jira_config: The Jira configuration object.
        params: Query parameters to include in the request.
        json_data: JSON data to include in the request body.

    Returns:
        The response object from the API request.

    Raises:
        ToolExecutionError: If the request fails for any reason.
    """
    url = f"{jira_config.base_url}/rest/api/3{endpoint}"

    # Create Basic Auth header
    auth_str = f"{jira_config.email}:{jira_config.api_token}"
    auth_bytes = auth_str.encode("ascii")
    auth_b64 = base64.b64encode(auth_bytes).decode("ascii")

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/json",
    }

    with httpx.Client() as client:
        try:
            response = client.request(method, url, headers=headers, params=params, json=json_data)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise ToolExecutionError(str(e)) from e

    return response
