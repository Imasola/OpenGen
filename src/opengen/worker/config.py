"""
OpenGen  - Worker Configuration
===============================

Connection settings for the worker client.
Loaded from the .env file.
"""

from pydantic_settings import BaseSettings


class WorkerSettings(BaseSettings):
    """
    Configuration for the OpenGen worker.

    The worker connects to the Master Agent, receives tasks,
    executes them using its own LLM API key, and returns results.
    """

    # Connection to Master Agent
    master_url: str = "https://api.opengen.live"
    worker_token: str = ""
    worker_name: str = "anonymous-worker"

    # LLM API keys (worker provides its own)
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # LLM settings
    default_provider: str = "anthropic"
    default_model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096

    # Worker behavior
    poll_interval_seconds: int = 10
    max_concurrent_tasks: int = 1
    task_timeout_seconds: int = 300

    # Logging
    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


def get_worker_settings() -> WorkerSettings:
    """Create and return the worker settings instance."""
    return WorkerSettings()


if __name__ == "__main__":
    settings = get_worker_settings()

    print("=" * 50)
    print("  OpenGen  - Worker Configuration")
    print("=" * 50)
    print(f"  Master URL:  {settings.master_url}")
    print(f"  Worker name: {settings.worker_name}")
    print(f"  Provider:    {settings.default_provider}")
    print(f"  Model:       {settings.default_model}")
    print(f"  Poll every:  {settings.poll_interval_seconds}s")
    print(f"  Max tasks:   {settings.max_concurrent_tasks}")
    print(f"  Timeout:     {settings.task_timeout_seconds}s")
    print()

    if settings.worker_token:
        print("  [ok] Worker token found")
    else:
        print("  [!!] No worker token  - add it to .env")

    if settings.anthropic_api_key:
        print("  [ok] Anthropic API key found")
    else:
        print("  [!!] No Anthropic API key  - add it to .env")

    print("=" * 50)
