import re
import time
from . import config, storage
from . import tools, approvals, memory, retrieval
from .audit import record_event
from .tracing import record_turn

SYSTEM_PROMPT = """You are CampusPath, a careful university student-services assistant. Answer using only the supplied student data, retrieved handbook excerpts, and saved preferences. Do not invent policies, fees, dates, eligibility, or actions. Explain uncertainty and recommend contacting student services when information is missing. Never reveal another student's private data. A fee adjustment is only requested through the approval workflow and must never be described as completed until an approval result confirms it."""


class StudentAgent:
    def __init__(self):
        self.last_usage = {"prompt_tokens": 0, "completion_tokens": 0}

    def _route(self, question: str, student_id: str):
        q = question.lower()
        other = re.search(r"\b(S-\d{4})\b", question.upper())
        requested_id = other.group(1) if other else student_id
        if any(k in q for k in ["waive", "fee adjustment", "reduce my fee", "fee concession"]):
            amount = re.search(r"(?:₹|rs\.?\s*)?(\d[\d,]*(?:\.\d{1,2})?)", question, re.I)
            if amount:
                reason = question
                result = approvals.request_fee_adjustment(student_id, float(amount.group(1).replace(",", "")), reason)
                return "approval_request", result
            return "approval_request", {"ok": False, "error": "Please specify the requested amount. No fee change has been made."}
        if any(k in q for k in ["fee status", "pending fee", "fee balance", "paid amount", "tuition balance"]):
            return "get_fee_status", tools.get_fee_status(student_id, requested_id)
        if any(k in q for k in ["scholarship", "financial aid", "merit aid"]):
            return "get_scholarship_status", tools.get_scholarship_status(student_id, requested_id)
        if any(k in q for k in ["my profile", "academic record", "my cgpa", "my advisor", "my programme"]):
            return "get_academic_profile", tools.get_academic_profile(student_id, requested_id)
        if any(k in q for k in ["raise a ticket", "support ticket", "create a case", "complaint"]):
            result = tools.create_support_ticket(student_id, "Student support request", question)
            return "create_support_ticket", result
        if "remember that" in q or "please remember" in q:
            accepted = memory.remember_preference(student_id, question)
            return "memory_write", {"ok": accepted, "message": "Preference saved." if accepted else "Sensitive or temporary information was not saved."}
        return "policy_retrieval", retrieval.retrieve(question)

    def answer(self, question: str, student_id: str, history=None):
        start = time.perf_counter()
        route, result = self._route(question, student_id)
        if isinstance(result, dict) and result.get("ok") is False:
            text = result.get("error", "The requested action could not be completed.")
            result = {"answer": text, "tool": route, "latency": time.perf_counter() - start,
                      "usage": {"prompt_tokens": 0, "completion_tokens": 0}, "evidence": []}
            record_turn(student_id, question, result)
            return result
        if route in {"get_fee_status", "get_scholarship_status", "get_academic_profile", "create_support_ticket", "approval_request", "memory_write"}:
            evidence = [f"Application tool result: {route}", str(result)]
        else:
            evidence = [f"Handbook: {x['heading']} — {x['text']}" for x in result]
        memories = memory.get_memories(student_id)
        if memories:
            evidence.append("Saved student preferences: " + "; ".join(memories))
        try:
            client = config.get_client()
            user_context = "\n\n".join(evidence) if evidence else "No matching policy section was retrieved. Do not invent an answer."
            response = client.chat.completions.create(
                model=config.MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": f"Student ID: {student_id}\nQuestion: {question}\n\nRelevant context:\n{user_context}"}],
                temperature=0.2,
            )
            answer = response.choices[0].message.content or "I could not generate a response. Please contact student services."
            usage = {"prompt_tokens": getattr(response.usage, "prompt_tokens", 0) or 0,
                     "completion_tokens": getattr(response.usage, "completion_tokens", 0) or 0}
        except Exception as exc:
            answer = f"The live AI service could not complete this request ({type(exc).__name__}). Check your Groq API key, model access and connection, then try again."
            usage = {"prompt_tokens": 0, "completion_tokens": 0}
        result = {"answer": answer, "tool": route, "latency": time.perf_counter() - start,
                  "usage": usage, "evidence": evidence[:4]}
        record_turn(student_id, question, result)
        return result
