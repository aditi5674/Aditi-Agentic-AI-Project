# CampusPath — Intelligent Student Support Agent

**Course:** Agentic AI Engineering | PGDM (Big Data Analytics / AI & Data Science) | Batch 2025–27  
**Implementation:** Python, Groq, Streamlit, BM25-style handbook retrieval, JSON persistence

## Overview

CampusPath is an academic demonstration of a student-support agent. It routes student questions to application tools, retrieves relevant sections from a sample handbook, uses saved preferences where appropriate, and generates grounded responses with a Groq language model.

This is an independently structured reference implementation. A student preparing their own submission should review the code, understand each workflow, run the tests and personalise the work honestly.

## Capabilities

- Student fee, scholarship and academic-profile lookups.
- Tool-level owner checks: a selected student can only access records matching that student ID.
- Handbook retrieval with a lightweight BM25-style ranking implementation.
- Persistent preference memory with password/OTP and temporary-content filters.
- Support-ticket creation.
- Fee-adjustment requests that remain pending until a reviewer approves or rejects them.
- Audit records for access decisions, requests and review outcomes.
- Persistent per-turn traces with latency, token usage, tool route, evidence and sensitive-text redaction.
- Streamlit chat UI and terminal interface.
- Local Assignment 2 safety workflow tests and optional live LLM measurements.

## Project layout

```text
Friends-Agentic-Assignment/
├── app.py
├── main.py
├── evaluate.py
├── requirements.txt
├── README.md
├── EVALUATION_REPORT.md
├── .env                 # Blank key placeholder; add your own key
├── .env.example
├── data/
│   ├── students.json
│   ├── student_handbook.md
│   ├── memory.json
│   ├── tickets.json
│   ├── approval_requests.json
│   ├── audit_log.jsonl
│   ├── agent_trace.jsonl
│   ├── sample_audit_evidence.jsonl
│   └── sample_approval_evidence.json
└── src/
    ├── agent.py
    ├── approvals.py
    ├── audit.py
    ├── config.py
    ├── memory.py
    ├── retrieval.py
    ├── security.py
    ├── storage.py
    ├── tracing.py
    └── tools.py
```

## Installation

Python 3.10 or 3.11 is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configure Groq

Open `.env` and insert your own API key:

```env
GROQ_API_KEY=your_own_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Do not share the key or submit a key belonging to another person. If the configured model is not enabled for the account, set `GROQ_MODEL` to a model available in that Groq account.

## Run the application

Browser interface:

```powershell
python -m streamlit run app.py
```

Terminal interface:

```powershell
python main.py
```

## Test the privacy and approval workflows

```powershell
python evaluate.py
```

This runs local application-level tests without requiring an API key. It checks own-record access, cross-student denial, pending approval, rejection without execution, approval execution, sensitive-memory rejection and audit generation. If a Groq key is configured, it also runs five live sample conversations and reports response latency and API token usage.

The local test runner writes example audit/approval evidence under `data/` so that the demonstration records can be inspected.

## Important demonstration limitations

- The student selector is a demo identity selector, not authenticated login. Ownership is checked against the selected student ID, but the application does not prove the real-world identity of the browser user.
- The reviewer identifier is a demonstration value and is not backed by a separately authenticated reviewer role.
- Local JSON files are used as sample storage; they are not designed for concurrent production use.
- The model's responses depend on the configured Groq model and API availability. The included sample data and policies are fictional teaching data.
- The local safety tests are deterministic application tests. The live LLM test reports measurements but does not by itself prove semantic correctness; review responses during the demonstration.

## Submission preparation

Before submitting, add a personal Groq API key locally, run `python evaluate.py`, review the outputs, and update `EVALUATION_REPORT.md` with the actual results from that run. Never include a private API key in a public repository or shareable archive.
