# Evaluation Report — CampusPath Student Support Agent

**Course:** Agentic AI Engineering | PGDM (Big Data Analytics / AI & Data Science) | Batch 2025–27  
**Status:** Evaluation template supplied with runnable tests

## 1. Assignment 1 capability checks

The project contains five live LLM demonstration scenarios in `evaluate.py`: fee status, payment portal policy, scholarship status, sensitive-memory filtering, and a policy-gap question. Run them with a valid Groq key to capture actual response latency and API-reported input/output tokens. Those live measurements are intentionally not pre-filled because they depend on the user's API account, model and network.

| Measure | Result |
|---|---|
| Live scenario count | 5 configured; run `python evaluate.py` to measure |
| Mean response latency | Populate from actual run |
| Input tokens | Populate from actual Groq usage |
| Output tokens | Populate from actual Groq usage |

## 2. Assignment 2 local privacy and approval tests

Run:

```powershell
python evaluate.py
```

The local deterministic tests verify:

| Scenario | Expected behaviour |
|---|---|
| Own student record | Allowed |
| Cross-student record | Blocked in Python tool code |
| Sensitive fee adjustment | Stored as PENDING; balance unchanged |
| Rejected adjustment | Rejected; balance unchanged |
| Approved adjustment | Executed only after approval; adjustment recorded separately from payments |
| Password in memory request | Rejected from persistent memory |
| Audit evidence | Records generated for access and approval events |

The script prints the actual PASS/FAIL results. Record the output and date here after running it.

## 3. Trace and audit evidence

- `data/audit_log.jsonl`: live audit events from app usage.
- `data/agent_trace.jsonl`: per-turn trace records with route, latency, token usage and evidence; sensitive credential-like text is redacted.
- `data/sample_audit_evidence.jsonl`: labelled sample evidence for the required ownership and approval scenarios.
- `data/sample_approval_evidence.json`: generated approval decisions after running `python evaluate.py`.

Each audit event records requester, action, target student, whether the action was allowed, approval state and result.

## 4. Identity and security limitations

The student selector is a demonstration identity selector rather than authenticated login. The reviewer identifier is also a demo value and is not authenticated independently. The project demonstrates application-level ownership checks and approval gating; it is not production authentication. Sample data is fictional.

## 5. Interpretation

Do not report unmeasured latency, token usage or accuracy as achieved results. Use actual output from the live evaluation after configuring the student's own Groq API key, and retain the local safety test results as separate application-level evidence.
