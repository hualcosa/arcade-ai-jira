import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from ~/.arcade/arcade.env
arcade_env_path = Path.home() / ".arcade" / "arcade.env"
load_dotenv(arcade_env_path)


@dataclass
class JiraConfig:
    base_url: str | None
    email: str | None
    api_token: str | None

    MISSING_ENV_ERROR = (
        "JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN must be set in ~/.arcade/arcade.env"
    )

    @classmethod
    def from_env(cls) -> "JiraConfig":
        base_url = os.getenv("JIRA_BASE_URL")
        email = os.getenv("JIRA_EMAIL")
        api_token = os.getenv("JIRA_API_TOKEN")

        if any(var is None for var in [base_url, email, api_token]):
            raise ValueError(cls.MISSING_ENV_ERROR)

        return cls(base_url=base_url, email=email, api_token=api_token)
