import re
from . import storage

SENSITIVE = re.compile(r"\b(password|passwd|passcode|otp|one[- ]time code|api key|secret token|cvv|card number)\b", re.I)


def _safe(value):
    if isinstance(value, str):
        return "[REDACTED SENSITIVE TEXT]" if SENSITIVE.search(value) else value[:2000]
    if isinstance(value, list):
        return [_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _safe(item) for key, item in value.items()}
    return value


def record_turn(student_id: str, question: str, result: dict):
    record = {
        "timestamp": storage.timestamp(),
        "student_id": student_id,
        "question": question,
        "route": result.get("tool"),
        "response": result.get("answer"),
        "latency_seconds": round(float(result.get("latency", 0)), 4),
        "usage": result.get("usage", {}),
        "retrieved_evidence": result.get("evidence", []),
    }
    storage.append_jsonl("agent_trace.jsonl", _safe(record))
