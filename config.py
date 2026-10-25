"""Shared settings loaded from the project's .env and environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def _nonnegative_int(name: str) -> int:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Set {name} in .env or the environment")
    try:
        result = int(value)
    except ValueError:
        raise ValueError(f"{name} must be a non-negative integer") from None
    if result < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return result


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONITOR_MODEL_NAME = os.getenv("MONITOR_MODEL_NAME")
REFLECTION_MODEL_NAME = os.getenv("REFLECTION_MODEL_NAME")
TRAIN_LIMIT = _nonnegative_int("TRAIN_LIMIT")
VAL_LIMIT = _nonnegative_int("VAL_LIMIT")
EVAL_LIMIT = _nonnegative_int("EVAL_LIMIT")
