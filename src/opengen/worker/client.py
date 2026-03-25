"""
OpenGen  - Worker Client
========================

Connects to the Master Agent, receives tasks, and submits results.
This is the main entry point for running an OpenGen worker.

Status: Skeleton (Phase 4). The Master Agent API is not yet available.
"""

import time

from opengen.models.shared import (
    WorkerHeartbeat,
    WorkerRegistration,
    WorkerResult,
    WorkerTask,
)
from opengen.worker.config import get_worker_settings
from opengen.worker.hardware import detect_hardware


class WorkerClient:
    """
    OpenGen worker client.

    Lifecycle:
    1. Register with the Master Agent
    2. Poll for tasks
    3. Execute tasks using local LLM API key
    4. Submit results
    5. Send periodic heartbeats
    6. Repeat
    """

    def __init__(self):
        self.settings = get_worker_settings()
        self.worker_id: str = ""
        self.is_registered: bool = False
        self.tasks_completed: int = 0
        self.start_time: float = 0.0

    def register(self) -> bool:
        """
        Register this worker with the Master Agent.

        Sends hardware info and supported LLM providers.
        Returns True if registration was accepted.
        """
        hardware = detect_hardware()

        registration = WorkerRegistration(
            worker_name=self.settings.worker_name,
            cpu_cores=hardware.get("cpu_cores", 0),
            ram_gb=hardware.get("ram_gb", 0.0),
            gpu_name=hardware.get("gpu_name", ""),
            gpu_vram_gb=hardware.get("gpu_vram_gb", 0.0),
            has_api_key=bool(self.settings.anthropic_api_key or self.settings.openai_api_key),
            supported_providers=self._get_supported_providers(),
            os=hardware.get("os", ""),
            python_version=hardware.get("python_version", ""),
        )

        print(f"  Registering with {self.settings.master_url}...")
        print(f"  Hardware: {registration.cpu_cores} cores, {registration.ram_gb:.1f}GB RAM")
        if registration.gpu_name:
            print(f"  GPU: {registration.gpu_name} ({registration.gpu_vram_gb:.1f}GB)")

        # TODO: Send registration to Master Agent API
        # response = httpx.post(f"{self.settings.master_url}/api/v1/worker/register", ...)
        # self.worker_id = response.json()["worker_id"]

        print("  [NOTE] Master Agent API not yet available (Phase 4)")
        print("  Registration will work once the Master Agent is deployed.")
        return False

    def poll_for_task(self) -> WorkerTask | None:
        """
        Poll the Master Agent for available tasks.

        Returns a WorkerTask if one is available, None otherwise.
        """
        # TODO: Poll Master Agent API
        # response = httpx.get(f"{self.settings.master_url}/api/v1/worker/tasks/next", ...)
        # return WorkerTask(**response.json()) if response.status_code == 200 else None
        return None

    def submit_result(self, result: WorkerResult) -> bool:
        """
        Submit a completed task result to the Master Agent.

        Returns True if the Master Agent accepted the result.
        """
        # TODO: Submit to Master Agent API
        # response = httpx.post(f"{self.settings.master_url}/api/v1/worker/tasks/{result.task_id}/result", ...)
        # return response.status_code == 200
        return False

    def send_heartbeat(self) -> None:
        """Send a health signal to the Master Agent."""
        heartbeat = WorkerHeartbeat(
            worker_id=self.worker_id,
            status="active",
            tasks_completed=self.tasks_completed,
            uptime_seconds=time.time() - self.start_time,
        )
        # TODO: Send heartbeat to Master Agent API
        # httpx.post(f"{self.settings.master_url}/api/v1/worker/heartbeat", ...)

    def run(self) -> None:
        """
        Main worker loop.

        Registers, then continuously polls for tasks and executes them.
        """
        print("=" * 60)
        print("  OpenGen Worker")
        print("=" * 60)

        self.start_time = time.time()

        if not self.register():
            print("\n  Worker cannot start  - registration failed.")
            print("  The Master Agent API is not yet available (Phase 4).")
            print("  In the meantime, you can:")
            print("    - Explore the data models: python -m opengen.models.shared")
            print("    - Check your hardware:     python -m opengen.worker.hardware")
            print("    - Star the repo and watch for updates")
            print("=" * 60)
            return

        print(f"\n  Worker '{self.settings.worker_name}' registered.")
        print(f"  Polling every {self.settings.poll_interval_seconds}s...")
        print("  Press Ctrl+C to stop.\n")

        try:
            while True:
                task = self.poll_for_task()
                if task:
                    self._execute_task(task)
                else:
                    time.sleep(self.settings.poll_interval_seconds)
                self.send_heartbeat()
        except KeyboardInterrupt:
            print("\n  Worker stopped by user.")

    def _execute_task(self, task: WorkerTask) -> None:
        """Execute a single task and submit the result."""
        from opengen.worker.executor import TaskExecutor

        print(f"  Task received: {task.question[:80]}...")
        executor = TaskExecutor()
        result_content = executor.execute(task)

        result = WorkerResult(
            task_id=task.id,
            worker_id=self.worker_id,
            content=result_content,
            model_used=self.settings.default_model,
        )

        if self.submit_result(result):
            self.tasks_completed += 1
            print(f"  Task completed. Total: {self.tasks_completed}")
        else:
            print("  Task submission failed.")

    def _get_supported_providers(self) -> list[str]:
        """Detect which LLM providers this worker can use."""
        providers = []
        if self.settings.anthropic_api_key:
            providers.append("anthropic")
        if self.settings.openai_api_key:
            providers.append("openai")
        return providers


if __name__ == "__main__":
    client = WorkerClient()
    client.run()
