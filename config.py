"""Shared configuration, with secrets loaded from .env or the environment."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MONITOR_MODEL_NAME = "openai/gpt-5.6-luna"
REFLECTION_MODEL_NAME = "openai/gpt-5.6-sol"
TRAIN_LIMIT = 200
VAL_LIMIT = 100
EVAL_LIMIT = 160
MIN_SUSPICION_SCORE = 0
MAX_SUSPICION_SCORE = 100
MODEL_DIR = Path("models")
MONITOR_GEPA_MODEL_PATH = MODEL_DIR / "gepa.json"
