from uuid import uuid4
from . import storage
from .audit import record_event


def request_fee_adjustment(student_id: str, amount: float, reason: str):
    students = storage.load_json("students.json", {})
    student = students.get(student_id)
    if not student:
        record_event(student_id, "request_fee_adjustment", student_id, False,
                     "not_requested", "student_not_found")
        return {"ok": False, "error": "Student record was not found."}
    try:
        amount = round(float(amount), 2)
    except (TypeError, ValueError):
        return {"ok": False, "error": "Enter a valid adjustment amount."}
    balance = float(student["fees"]["pending_balance"])
    if amount <= 0 or amount > balance:
        return {"ok": False, "error": "Adjustment must be positive and cannot exceed the outstanding balance."}
    requests = storage.load_json("approval_requests.json", [])
    request_id = "APR-" + uuid4().hex[:8].upper()
    request = {"request_id": request_id, "student_id": student_id,
               "amount": amount, "reason": reason.strip(), "status": "PENDING",
               "balance_at_request": balance, "requested_at": storage.timestamp(),
               "reviewer_id": None, "decision_at": None, "result": "awaiting_human_approval"}
    requests.append(request)
    storage.save_json("approval_requests.json", requests)
    record_event(student_id, "request_fee_adjustment", student_id, True,
                 "pending", "awaiting_human_approval", {"request_id": request_id, "amount": amount})
    return {"ok": True, **request}


def pending_requests():
    return [r for r in storage.load_json("approval_requests.json", []) if r.get("status") == "PENDING"]


def decide_request(request_id: str, decision: str, reviewer_id: str):
    decision = decision.strip().upper()
    if decision not in {"APPROVE", "REJECT"}:
        return {"ok": False, "error": "Decision must be APPROVE or REJECT."}
    requests = storage.load_json("approval_requests.json", [])
    request = next((r for r in requests if r["request_id"] == request_id), None)
    if not request:
        return {"ok": False, "error": "Approval request was not found."}
    if request["status"] != "PENDING":
        return {"ok": False, "error": "This request has already been decided."}
    students = storage.load_json("students.json", {})
    student = students.get(request["student_id"])
    if not student:
        return {"ok": False, "error": "Student record was not found."}
    fees = student["fees"]
    current_balance = float(fees["pending_balance"])
    if decision == "REJECT":
        request.update({"status": "REJECTED", "reviewer_id": reviewer_id,
                        "decision_at": storage.timestamp(), "result": "rejected_no_change"})
        storage.save_json("approval_requests.json", requests)
        record_event(reviewer_id, "decide_fee_adjustment", request["student_id"], True,
                     "rejected", "rejected_no_change", {"request_id": request_id})
        return {"ok": True, "status": "REJECTED", "result": "rejected_no_change",
                "pending_balance": current_balance}
    if abs(current_balance - float(request["balance_at_request"])) > 0.001:
        return {"ok": False, "error": "Balance changed after the request. Review is required before approval."}
    if float(request["amount"]) > current_balance:
        return {"ok": False, "error": "Adjustment exceeds the current outstanding balance."}
    fees["pending_balance"] = round(current_balance - float(request["amount"]), 2)
    fees.setdefault("adjustments", []).append({"request_id": request_id,
            "type": "approved_fee_adjustment", "amount": float(request["amount"]),
            "approved_by": reviewer_id, "approved_at": storage.timestamp()})
    request.update({"status": "APPROVED", "reviewer_id": reviewer_id,
                    "decision_at": storage.timestamp(), "result": "adjustment_applied"})
    storage.save_json("students.json", students)
    storage.save_json("approval_requests.json", requests)
    record_event(reviewer_id, "decide_fee_adjustment", request["student_id"], True,
                 "approved", "adjustment_applied", {"request_id": request_id,
                 "amount": request["amount"], "new_pending_balance": fees["pending_balance"]})
    return {"ok": True, "status": "APPROVED", "result": "adjustment_applied",
            "pending_balance": fees["pending_balance"]}
