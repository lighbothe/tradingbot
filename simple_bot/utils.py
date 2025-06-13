"""Utility functions for simple_bot."""

from __future__ import annotations

import datetime
import yaml
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv


COLORS = {
    "INFO": "\033[94m",
    "ERROR": "\033[91m",
    "ENDC": "\033[0m",
}


def log(level: str, message: str) -> None:
    """Print colored log message with timestamp.

    Args:
        level: Log level string.
        message: Message to print.
    """
    color = COLORS.get(level, "")
    endc = COLORS["ENDC"] if color else ""
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"{color}[{timestamp}] {level}: {message}{endc}")


def load_cfg(path: str | Path) -> Dict[str, Any]:
    """Load YAML configuration and environment variables.

    Args:
        path: Path to YAML config.

    Returns:
        Parsed configuration as dictionary.
    """
    load_dotenv()
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg
