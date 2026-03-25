"""
OpenGen  - Task Executor
========================

Executes research tasks assigned by the Master Agent.
Uses the worker's own LLM API key.

Status: Skeleton (Phase 4).
"""

from opengen.models.shared import WorkerTask
from opengen.worker.config import get_worker_settings


class TaskExecutor:
    """
    Executes a single research task in a sandboxed environment.

    The executor calls the LLM using the worker's own API key,
    processes the response, and returns the result text.
    """

    def __init__(self):
        self.settings = get_worker_settings()

    def execute(self, task: WorkerTask) -> str:
        """
        Execute a task and return the result text.

        In Phase 4, this will:
        1. Set up a Docker sandbox
        2. Call the LLM with the task instructions
        3. Validate the response
        4. Return the result

        Currently returns a placeholder.
        """
        # TODO: Implement actual task execution
        # 1. Select LLM provider based on task.model_preference
        # 2. Build prompt from task.question + task.context + task.instructions
        # 3. Call LLM API with worker's own API key
        # 4. Validate response (check for errors, empty content)
        # 5. Return result text

        raise NotImplementedError(
            "Task execution is not yet implemented (Phase 4). "
            "The Master Agent API must be deployed first."
        )


if __name__ == "__main__":
    print("Task executor is a skeleton  - implementation in Phase 4.")
    print("Run the full worker: python -m opengen.worker.client")
