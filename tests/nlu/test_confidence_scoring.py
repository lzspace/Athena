
import pytest
from assistant_core.modules.nlu.nlu_pipeline import compute_confidence

def test_exact_match():
    intent, score = compute_confidence("add_appointment", ["add_appointment", "delete_appointment"])
    print(f"Close match: intent={intent}, score={score}")
    assert intent == "add_appointment"
    assert score == 1.0

def test_close_match():
    intent, score = compute_confidence("add apointment", ["add_appointment", "delete_appointment"])
    print(f"Close match: intent={intent}, score={score}")
    assert intent == "add_appointment"
    assert score > 0.8

def test_low_confidence():
    intent, score = compute_confidence("banana", ["add_appointment", "delete_appointment"])
    print(f"Close match: intent={intent}, score={score}")
    assert score < 0.3

def log_low_confidence(input_text: str, predicted: str, score: float):
    if score < 0.75:
        from pathlib import Path
        log_file = Path("logs/low_confidence.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as f:
            f.write(f"{input_text} → {predicted} (score: {score:.2f})\\n")
