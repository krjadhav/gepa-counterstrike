"""Fine-tune the monitor using successful traces from its GEPA prompt."""

import random

import dspy

from config import (
    MONITOR_GEPA_FINETUNE_MODEL_PATH,
    MONITOR_GEPA_MODEL_PATH,
    MONITOR_MODEL_NAME,
    OPENAI_API_KEY,
    TRAIN_LIMIT,
)
from data import build_examples_from_samples, load_samples
from metric import finetune_metric
from monitor import MonitorTrainerProgram, dspy_monitor_program


def main() -> None:
    if not MONITOR_GEPA_MODEL_PATH.is_file():
        raise SystemExit("Run `uv run monitor.py` to create the GEPA checkpoint first.")
    if not OPENAI_API_KEY:
        raise SystemExit("Set OPENAI_API_KEY in the environment or .env before training.")
    if TRAIN_LIMIT <= 0:
        raise ValueError("TRAIN_LIMIT must be positive.")

    examples = build_examples_from_samples(load_samples())
    # Match the GEPA split so validation examples stay out of fine-tuning.
    random.Random(0).shuffle(examples)
    train_examples = examples[:TRAIN_LIMIT]
    if not train_examples:
        raise ValueError("The dataset must contain a nonempty training split.")

    lm = dspy.LM(
        MONITOR_MODEL_NAME,
        cache=False,
        temperature=1.0,
        max_tokens=20000,
        api_key=OPENAI_API_KEY,
    )
    gepa_program = dspy_monitor_program(lm, model_path=MONITOR_GEPA_MODEL_PATH)
    monitor_trainer_program = MonitorTrainerProgram(gepa_program)

    finetune_optimizer = dspy.BootstrapFinetune(metric=finetune_metric)
    finetune_trainer_program = finetune_optimizer.compile(
        monitor_trainer_program,
        trainset=train_examples,
    )

    finetune_program = finetune_trainer_program.monitor_program
    MONITOR_GEPA_FINETUNE_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    finetune_program.save(MONITOR_GEPA_FINETUNE_MODEL_PATH)
    print(f"Saved fine-tuned monitor to {MONITOR_GEPA_FINETUNE_MODEL_PATH}")


if __name__ == "__main__":
    main()
