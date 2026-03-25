"""
OpenGen  - Hardware Detection
=============================

Detects the worker's hardware capabilities.
Used during registration to help the Master Agent assign appropriate tasks.
"""

import os
import platform
import sys


def detect_hardware() -> dict:
    """
    Detect available hardware and return a summary.

    Returns a dictionary with:
    - cpu_cores: number of CPU cores
    - ram_gb: total RAM in gigabytes
    - gpu_name: GPU name (if detectable)
    - gpu_vram_gb: GPU VRAM in gigabytes (if detectable)
    - os: operating system
    - python_version: Python version string
    """
    info = {
        "cpu_cores": os.cpu_count() or 0,
        "ram_gb": _get_ram_gb(),
        "gpu_name": "",
        "gpu_vram_gb": 0.0,
        "os": f"{platform.system()} {platform.release()}",
        "python_version": platform.python_version(),
    }

    gpu = _detect_gpu()
    if gpu:
        info["gpu_name"] = gpu.get("name", "")
        info["gpu_vram_gb"] = gpu.get("vram_gb", 0.0)

    return info


def _get_ram_gb() -> float:
    """Get total system RAM in gigabytes."""
    try:
        if platform.system() == "Linux":
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal"):
                        kb = int(line.split()[1])
                        return round(kb / 1024 / 1024, 1)
        elif platform.system() == "Darwin":
            import subprocess
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True,
            )
            if result.returncode == 0:
                return round(int(result.stdout.strip()) / 1024 / 1024 / 1024, 1)
        elif platform.system() == "Windows":
            import subprocess
            result = subprocess.run(
                ["wmic", "computersystem", "get", "TotalPhysicalMemory"],
                capture_output=True, text=True,
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) >= 2:
                    return round(int(lines[1].strip()) / 1024 / 1024 / 1024, 1)
    except Exception:
        pass
    return 0.0


def _detect_gpu() -> dict | None:
    """Attempt to detect an NVIDIA GPU using nvidia-smi."""
    try:
        import subprocess
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split(",")
            if len(parts) >= 2:
                return {
                    "name": parts[0].strip(),
                    "vram_gb": round(float(parts[1].strip()) / 1024, 1),
                }
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass
    return None


if __name__ == "__main__":
    info = detect_hardware()

    print("=" * 50)
    print("  OpenGen  - Hardware Detection")
    print("=" * 50)
    print(f"  OS:             {info['os']}")
    print(f"  Python:         {info['python_version']}")
    print(f"  CPU cores:      {info['cpu_cores']}")
    print(f"  RAM:            {info['ram_gb']} GB")

    if info["gpu_name"]:
        print(f"  GPU:            {info['gpu_name']}")
        print(f"  VRAM:           {info['gpu_vram_gb']} GB")
    else:
        print("  GPU:            Not detected (NVIDIA only)")

    print()
    print("  This information is sent to the Master Agent")
    print("  during registration to optimize task assignment.")
    print("=" * 50)
