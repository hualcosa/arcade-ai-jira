import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from ~/.arcade/arcade.env
arcade_env_path = Path.home() / ".arcade" / "arcade.env"
load_dotenv(arcade_env_path)


@dataclass
class JiraConfig:
    base_url: str
    email: str
    api_token: str

    @classmethod
    def from_env(cls) -> "JiraConfig":
        base_url = os.getenv("JIRA_BASE_URL")
        email = os.getenv("JIRA_EMAIL")
        api_token = os.getenv("JIRA_API_TOKEN")

        if not all([base_url, email, api_token]):
            raise ValueError(
                "JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN must be set in ~/.arcade/arcade.env"
            )

        # After the check above, we know these are not None
        assert base_url is not None
        assert email is not None
        assert api_token is not None

        return cls(base_url=base_url, email=email, api_token=api_token)
