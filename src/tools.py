from . import storage
from .security import authorize_student
from .audit import record_event


def _student(student_id: str):
    students = storage.load_json("students.json", {})
    return students.get(student_id)


def get_fee_status(active_student_id: str, requested_student_id: str | None = None):
    target = requested_student_id or active_student_id
    if not authorize_student(active_student_id, target, "get_fee_status"):
        return {"ok": False, "error": "Access denied: you may only view your own fee record."}
    student = _student(target)
    if not student:
        return {"ok": False, "error": "Student record was not found."}
    fees = student["fees"]
    return {"ok": True, "student_id": target, "total_fee": fees["total_fee"],
            "paid_amount": fees["paid_amount"], "pending_balance": fees["pending_balance"],
            "due_date": fees["due_date"]}


def get_scholarship_status(active_student_id: str, requested_student_id: str | None = None):
    target = requested_student_id or active_student_id
    if not authorize_student(active_student_id, target, "get_scholarship_status"):
        return {"ok": False, "error": "Access denied: you may only view your own scholarship record."}
    student = _student(target)
    if not student:
        return {"ok": False, "error": "Student record was not found."}
    return {"ok": True, "student_id": target, **student.get("scholarship", {})}


def get_academic_profile(active_student_id: str, requested_student_id: str | None = None):
    target = requested_student_id or active_student_id
    if not authorize_student(active_student_id, target, "get_academic_profile"):
        return {"ok": False, "error": "Access denied: you may only view your own academic profile."}
    student = _student(target)
    if not student:
        return {"ok": False, "error": "Student record was not found."}
    return {"ok": True, "student_id": target, "name": student["name"],
            "programme": student["programme"], "semester": student["semester"],
            "cgpa": student["cgpa"], "advisor": student["advisor"]}


def create_support_ticket(student_id: str, subject: str, description: str):
    if not authorize_student(student_id, student_id, "create_support_ticket"):
        return {"ok": False, "error": "Unable to verify student context."}
    tickets = storage.load_json("tickets.json", [])
    ticket_id = f"CASE-{len(tickets) + 301:04d}"
    ticket = {"ticket_id": ticket_id, "student_id": student_id,
              "subject": subject[:120], "description": description[:1000], "status": "OPEN",
              "created_at": storage.timestamp()}
    tickets.append(ticket)
    storage.save_json("tickets.json", tickets)
    record_event(student_id, "create_support_ticket", student_id, True,
                 "not_required", "ticket_created", {"ticket_id": ticket_id})
    return {"ok": True, **ticket}
