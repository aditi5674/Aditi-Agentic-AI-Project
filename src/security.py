from . import storage
from .audit import record_event


def authorize_student(requester_id: str | None, target_student_id: str | None, action: str):
    """Application-level ownership check. Identity is demo-selected, not login-authenticated."""
    allowed = bool(requester_id and target_student_id and requester_id == target_student_id)
    result = "owner_access_allowed" if allowed else "cross_student_access_blocked"
    record_event(requester_id or "UNKNOWN", action, target_student_id, allowed,
                 "not_required", result)
    return allowed
