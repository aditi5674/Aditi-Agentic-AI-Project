from . import storage


def record_event(requester_id: str, action: str, target_student_id: str | None,
                 allowed: bool, approval_status: str, result: str, details: dict | None = None):
    event = {
        "timestamp": storage.timestamp(),
        "requester_id": requester_id or "UNKNOWN",
        "action": action,
        "target_student_id": target_student_id,
        "allowed": bool(allowed),
        "approval_status": approval_status,
        "result": result,
        "details": details or {},
    }
    storage.append_jsonl("audit_log.jsonl", event)
    return event
