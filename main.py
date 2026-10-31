from src.agent import StudentAgent
from src.config import API_KEY
from src import storage
from src.approvals import pending_requests, decide_request, request_fee_adjustment


def main():
    students = storage.load_json("students.json", {})
    print("\nCAMPUSPATH — STUDENT SERVICES ASSISTANT")
    print("Demo identity selector; this is not authenticated login.")
    for sid, student in students.items():
        print(f"  {sid}: {student['name']} — {student['programme']}")
    sid = input("Select student ID: ").strip().upper()
    if sid not in students:
        print("Unknown student ID.")
        return
    agent = StudentAgent()
    print("Type a question, or /help for commands. Type exit to quit.")
    while True:
        text = input(f"[{sid}] > ").strip()
        if text.lower() in {"exit", "quit"}:
            break
        if text == "/help":
            print("/request-adjustment <amount> <reason> | /pending | /approve <id> | /reject <id> | exit")
            continue
        if text.startswith("/request-adjustment "):
            parts = text.split(maxsplit=2)
            if len(parts) < 3:
                print("Usage: /request-adjustment <amount> <reason>")
            else:
                print(request_fee_adjustment(sid, float(parts[1]), parts[2]))
            continue
        if text == "/pending":
            print(pending_requests())
            continue
        if text.startswith("/approve ") or text.startswith("/reject "):
            action, request_id = text.split(maxsplit=1)
            reviewer = input("Reviewer ID (demo value): ").strip() or "REVIEWER-DEMO"
            print(decide_request(request_id, "APPROVE" if action == "/approve" else "REJECT", reviewer))
            continue
        result = agent.answer(text, sid)
        print("\n" + result["answer"])
        print(f"[{result['tool']} | {result['latency']:.2f}s | {result['usage']}]\n")

if __name__ == "__main__":
    main()
