import re
from . import storage
from .audit import record_event

SENSITIVE = re.compile(r"\b(password|passwd|passcode|otp|one[- ]time code|pin number|cvv|card number|api key|secret token)\b", re.I)
TEMPORARY = re.compile(r"\b(today|right now|currently|this morning|temporary|for a few hours)\b", re.I)


def remember_preference(student_id: str, text: str):
    if SENSITIVE.search(text) or TEMPORARY.search(text):
        record_event(student_id, "memory_write", student_id, False,
                     "not_required", "sensitive_or_temporary_content_rejected")
        return False
    memories = storage.load_json("memory.json", {})
    memories.setdefault(student_id, [])
    fact = text.strip()[:240]
    if fact and fact not in memories[student_id]:
        memories[student_id].append(fact)
        storage.save_json("memory.json", memories)
    return True


def get_memories(student_id: str):
    return storage.load_json("memory.json", {}).get(student_id, [])
