
import streamlit as st
import textwrap
from html import escape

from src import storage
from src.agent import StudentAgent
from src.approvals import (
    request_fee_adjustment,
    pending_requests,
    decide_request
)
from src.config import get_client


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CampusPath | Student Services",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. COMPLETE LIGHT THEME CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');


/* ==========================================================
   GLOBAL COLOUR SYSTEM
   ========================================================== */

:root {
    color-scheme: light !important;

    --background-color: #f5f7fa;
    --secondary-background-color: #edf2f7;
    --text-color: #26364d;
    --primary-color: #4267a9;

    --bg: #f5f7fa;
    --surface: #ffffff;
    --sidebar: #edf2f7;

    --navy: #172b4d;
    --text: #26364d;
    --muted: #718096;

    --blue: #4267a9;
    --blue-dark: #304f89;
    --blue-soft: #eaf0f9;

    --border: #dce4ed;
    --green: #237653;
}


/* ==========================================================
   GLOBAL APPLICATION BACKGROUND
   ========================================================== */

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {

    background-color: var(--bg) !important;
    color: var(--text) !important;
    color-scheme: light !important;

    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background: var(--bg) !important;
}

.block-container {
    max-width: 1280px;
    padding-top: 1.8rem;
    padding-bottom: 5rem;
}


/* ==========================================================
   UNIVERSAL TEXT COLOUR CORRECTION
   ========================================================== */

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {

    color: var(--navy) !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 750 !important;
}

.stApp p,
.stApp li,
.stApp label {

    color: var(--text) !important;
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {

    color: var(--muted) !important;
}


/* ==========================================================
   HEADER
   ========================================================== */

[data-testid="stHeader"] {
    background: var(--bg) !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

[data-testid="stSidebar"] {

    background: var(--sidebar) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div {

    background: var(--sidebar) !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {

    color: var(--navy) !important;
}

.brand {

    font-family: 'Manrope', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--navy) !important;
    letter-spacing: -0.7px;
}

.brand-subtitle {

    color: var(--muted) !important;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.profile-card {

    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 15px;
    margin: 12px 0;
}

.profile-label {

    font-size: 0.7rem;
    color: var(--muted) !important;
    font-weight: 700;
    letter-spacing: 1px;
}

.profile-value {

    font-size: 0.95rem;
    color: var(--navy) !important;
    font-weight: 700;
    overflow-wrap: anywhere;
}


/* ==========================================================
   HERO SECTION
   ========================================================== */

.hero {

    background: linear-gradient(
        120deg,
        #203b66,
        #365d91 60%,
        #537eac
    );

    padding: 2.2rem 2.3rem;
    border-radius: 19px;
    margin-bottom: 1.5rem;

    box-shadow: 0 9px 24px rgba(32, 59, 102, 0.12);
}

.hero .eyebrow {

    color: #d3e2f7 !important;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero h1 {

    color: #ffffff !important;
    font-size: 2.5rem;
    line-height: 1.2;
    margin: 0.7rem 0;
}

.hero p {

    color: #e1eaf6 !important;
    font-size: 1rem;
    line-height: 1.7;
    max-width: 750px;
}

.pill {

    display: inline-block;
    padding: 6px 12px;
    border-radius: 30px;

    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);

    color: #ffffff !important;
    font-size: 0.76rem;
    font-weight: 600;

    margin: 3px 5px 3px 0;
}


/* ==========================================================
   DASHBOARD METRIC CARDS
   ========================================================== */

.metric {

    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 15px;

    padding: 18px;
    min-height: 110px;

    box-shadow: 0 4px 14px rgba(30, 52, 84, 0.04);
}

.metric-label {

    color: var(--muted) !important;
    font-size: 0.82rem;
    font-weight: 600;
}

.metric-value {

    color: var(--navy) !important;
    font-family: 'Manrope', sans-serif;

    font-size: 1.55rem;
    font-weight: 800;

    margin-top: 8px;
}


/* ==========================================================
   STREAMLIT METRICS
   ========================================================== */

[data-testid="stMetric"] {

    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;

    padding: 16px !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {

    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {

    color: var(--navy) !important;
}


/* ==========================================================
   CRITICAL FIX: MARKDOWN TABLES
   ========================================================== */

/* Target all Markdown-rendered tables */

[data-testid="stMarkdownContainer"] table,
.stMarkdown table,
[data-testid="stChatMessage"] table {

    width: 100% !important;
    border-collapse: collapse !important;

    background: #ffffff !important;

    color: #26364d !important;

    border: 1px solid #dce4ed !important;
    border-radius: 10px !important;

    overflow: hidden !important;

    margin: 12px 0 !important;
}


/* Table headers */

[data-testid="stMarkdownContainer"] table thead,
.stMarkdown table thead,
[data-testid="stChatMessage"] table thead {

    background: #e8eef7 !important;
}

[data-testid="stMarkdownContainer"] table th,
.stMarkdown table th,
[data-testid="stChatMessage"] table th {

    background: #e8eef7 !important;

    color: #172b4d !important;

    font-weight: 750 !important;
    text-align: left !important;

    padding: 12px 15px !important;

    border-bottom: 2px solid #d2ddec !important;
}


/* Table body cells */

[data-testid="stMarkdownContainer"] table td,
.stMarkdown table td,
[data-testid="stChatMessage"] table td {

    background: #ffffff !important;

    color: #26364d !important;

    padding: 12px 15px !important;

    border-bottom: 1px solid #e5eaf1 !important;

    font-size: 0.92rem !important;
}


/* Alternating table rows */

[data-testid="stMarkdownContainer"] table tbody tr:nth-child(even),
.stMarkdown table tbody tr:nth-child(even),
[data-testid="stChatMessage"] table tbody tr:nth-child(even) {

    background: #f4f7fb !important;
}

[data-testid="stMarkdownContainer"] table tbody tr:nth-child(even) td,
.stMarkdown table tbody tr:nth-child(even) td,
[data-testid="stChatMessage"] table tbody tr:nth-child(even) td {

    background: #f4f7fb !important;
    color: #26364d !important;
}


/* Last row */

[data-testid="stMarkdownContainer"] table tbody tr:last-child td {

    border-bottom: none !important;
}


/* Ensure strong and bold table text is readable */

[data-testid="stMarkdownContainer"] table strong,
[data-testid="stMarkdownContainer"] table b,
.stMarkdown table strong,
.stMarkdown table b {

    color: #172b4d !important;
}


/* ==========================================================
   OTHER MARKDOWN CONTENT
   ========================================================== */

[data-testid="stMarkdownContainer"] {

    color: var(--text) !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {

    color: var(--text) !important;
    line-height: 1.7;
}

[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {

    color: var(--navy) !important;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {

    color: var(--navy) !important;
}


/* ==========================================================
   CHAT MESSAGE CONTAINERS
   ========================================================== */

[data-testid="stChatMessage"] {

    background: #ffffff !important;

    border: 1px solid var(--border) !important;
    border-radius: 15px !important;

    padding: 1rem !important;
    margin-bottom: 0.8rem;

    box-shadow: 0 3px 12px rgba(30, 52, 84, 0.035);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] strong {

    color: #26364d !important;
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {

    background: #eaf0f9 !important;
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {

    background: #ffffff !important;
}


/* ==========================================================
   CHAT INPUT
   ========================================================== */

[data-testid="stChatInput"] {

    background: #ffffff !important;
    border: 1px solid #cbd7e7 !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {

    background: #ffffff !important;
    color: #172b4d !important;
    -webkit-text-fill-color: #172b4d !important;
}

[data-testid="stChatInput"] textarea::placeholder {

    color: #8998ad !important;
    -webkit-text-fill-color: #8998ad !important;
}


/* ==========================================================
   TEXT INPUTS AND TEXT AREAS
   ========================================================== */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {

    background: #ffffff !important;

    color: #172b4d !important;
    -webkit-text-fill-color: #172b4d !important;

    border: 1px solid #cbd7e7 !important;
    border-radius: 9px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {

    color: #8998ad !important;
    -webkit-text-fill-color: #8998ad !important;
}


/* ==========================================================
   SELECTBOX AND DROPDOWNS
   ========================================================== */

[data-baseweb="select"] > div {

    background: #ffffff !important;
    border-color: #cbd7e7 !important;
    color: #172b4d !important;
}

[data-baseweb="select"] * {

    color: #172b4d !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {

    background: #ffffff !important;
}

[data-baseweb="menu"] * {

    color: #172b4d !important;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button,
.stFormSubmitButton > button {

    background: #ffffff !important;

    color: #304f89 !important;

    border: 1px solid #cbd7e7 !important;
    border-radius: 10px !important;

    font-weight: 650 !important;

    transition: all 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {

    background: #4267a9 !important;

    color: #ffffff !important;

    border-color: #4267a9 !important;
}


/* ==========================================================
   FORMS
   ========================================================== */

[data-testid="stForm"] {

    background: #ffffff !important;

    border: 1px solid var(--border) !important;
    border-radius: 15px !important;

    padding: 1.2rem !important;
}


/* ==========================================================
   EXPANDERS
   ========================================================== */

[data-testid="stExpander"] {

    background: #ffffff !important;

    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {

    color: #172b4d !important;
    font-weight: 650;
}

[data-testid="stExpander"] p,
[data-testid="stExpander"] span,
[data-testid="stExpander"] li {

    color: #26364d !important;
}


/* ==========================================================
   ALERTS
   ========================================================== */

[data-testid="stAlert"] {

    border-radius: 11px !important;
}

[data-testid="stAlert"] p {

    color: #26364d !important;
}


/* ==========================================================
   CODE BLOCKS
   ========================================================== */

[data-testid="stCode"] {

    background: #eef2f8 !important;
    border-radius: 10px !important;
}

[data-testid="stCode"] code {

    color: #243d63 !important;
}


/* ==========================================================
   DIVIDERS AND FOOTER
   ========================================================== */

hr {

    border-color: var(--border) !important;
}

footer {

    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. LOAD STUDENT DATA
# ============================================================

students = storage.load_json("students.json", {})

if not students:

    st.error(
        "No demonstration student records found "
        "in data/students.json."
    )

    st.stop()



# ============================================================
# SIDEBAR — CAMPUSPATH STUDENT WORKSPACE
# ============================================================

with st.sidebar:

    # Sidebar-specific styling
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: #edf2f7 !important;
        border-right: 1px solid #dce4ed !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #cbd7e7 !important;
        border-radius: 9px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #172b4d !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: #ffffff !important;
        color: #304f89 !important;
        border: 1px solid #cbd7e7 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        text-align: left !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #4267a9 !important;
        color: #ffffff !important;
        border-color: #4267a9 !important;
    }

    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: #e5edf8 !important;
        border: 1px solid #d1deef !important;
    }

    [data-testid="stSidebar"] [data-testid="stAlert"] p {
        color: #304f89 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #d5deea !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Brand identity
    st.markdown(
        "## 🌿 CampusPath"
    )

    st.caption("STUDENT SERVICES COMPANION")

    st.divider()

    # Student selection
    st.markdown("### Student workspace")

    ids = list(students.keys())

    active_id = st.selectbox(
        "Demo student identity",
        ids,
        format_func=lambda x: (
            f"{students[x].get('name', x)} · {x}"
        ),
        key="campuspath_student_selector"
    )

    # IMPORTANT: Define student before displaying the profile
    student = students[active_id]

    # Demo identity disclaimer
    st.info(
        "Demonstration identity selector — "
        "this is not an authenticated login."
    )

    # Student profile using native Streamlit components
    with st.container(border=True):

        st.caption("ACTIVE STUDENT")

        st.markdown(
            f"**{student.get('name', active_id)}**"
        )

        st.divider()

        st.caption("PROGRAMME")

        st.markdown(
            f"**{student.get('programme', 'Not specified')}**"
        )

        st.divider()

        st.caption("ACADEMIC DETAILS")

        st.markdown(
            f"**Semester {student.get('semester', 'N/A')} "
            f"· CGPA {student.get('cgpa', 'N/A')}**"
        )

    st.divider()

    # Quick navigation prompts
    st.markdown("### Shortcuts")

    if st.button(
        "💳  My fee position",
        use_container_width=True
    ):
        st.session_state.pending_prompt = (
            "What is my current fee status?"
        )

    if st.button(
        "🎓  Scholarship details",
        use_container_width=True
    ):
        st.session_state.pending_prompt = (
            "Show my scholarship status and renewal criteria."
        )

    if st.button(
        "🛠️  Payment portal help",
        use_container_width=True
    ):
        st.session_state.pending_prompt = (
            "The payment portal failed. What should I do?"
        )

    st.divider()

    # Footer information
    st.caption(
        "🌿 CampusPath · Student Services AI"
    )

    st.caption(
        "Live AI requires your own Groq API key in .env."
    )



# ============================================================
# 5. HERO SECTION
# ============================================================

hero_html = (
    '<div class="hero">'
    '<div class="eyebrow">STUDENT SERVICES · AI ASSISTANT</div>'
    '<h1>Your campus, made easier.</h1>'
    '<p>Your intelligent student services companion. '
    'Ask about fees, scholarships, academic records '
    'and institutional policies.</p>'
    '<span class="pill">● Policy-aware assistant</span>'
    '<span class="pill">Student-scoped tools</span>'
    '<span class="pill">Human approval workflow</span>'
    '</div>'
)

st.markdown(hero_html, unsafe_allow_html=True)


# ============================================================
# 6. STUDENT METRICS
# ============================================================

fee = student["fees"]

c1, c2, c3 = st.columns(3)

metrics = [
    (c1, "Outstanding balance",
     f"₹{fee['pending_balance']:,.0f}"),

    (c2, "Current semester",
     str(student["semester"])),

    (c3, "Academic advisor",
     str(student["advisor"]))
]

for col, title, value in metrics:

    with col:

        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">{escape(title)}</div>
                <div class="metric-value">{escape(value)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.write("")


# ============================================================
# 7. CHAT SESSION
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


for item in st.session_state.messages:

    with st.chat_message(item["role"]):

        st.markdown(item["content"])

        if item.get("meta"):
            st.caption(item["meta"])


# ============================================================
# 8. CHAT INPUT AND AGENT EXECUTION
# ============================================================

prompt = st.chat_input(
    "Ask CampusPath a question..."
)

if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        agent = StudentAgent()

        with st.chat_message("assistant"):

            with st.spinner(
                "Checking student information and policies..."
            ):

                result = agent.answer(prompt, active_id)

            answer = result["answer"]

            st.markdown(answer)

            meta = (
                f"Route: {result['tool']} · "
                f"{result['latency']:.2f}s · "
                f"Tokens: {result['usage']['prompt_tokens']} in / "
                f"{result['usage']['completion_tokens']} out"
            )

            st.caption(meta)

            if result.get("evidence"):

                with st.expander(
                    "📚 What information was used"
                ):

                    for evidence in result["evidence"]:
                        st.write(evidence)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "meta": meta
        })

    except Exception as e:

        st.error(
            f"An error occurred while processing your request: {e}"
        )


# ============================================================
# 9. FEE ADJUSTMENT
# ============================================================

st.divider()

st.markdown("## 💰 Fee Adjustment & Approval Centre")

st.caption(
    "Submit fee adjustment requests for institutional review. "
    "Balances are not changed until an authorised approval action "
    "is processed by the demonstration workflow."
)

left, right = st.columns([1.05, 1], gap="large")


with left:

    st.subheader("Submit a fee adjustment request")

    with st.form(
        "adjustment_form",
        clear_on_submit=True
    ):

        amount = st.number_input(
            "Requested amount (₹)",
            min_value=1.0,
            max_value=float(max(fee["pending_balance"], 1)),
            value=min(
                5000.0,
                float(max(fee["pending_balance"], 1))
            ),
            step=500.0
        )

        reason = st.text_area(
            "Reason for request",
            placeholder="Briefly explain your request."
        )

        submitted = st.form_submit_button(
            "Submit for human review",
            use_container_width=True
        )

    if submitted:

        response = request_fee_adjustment(
            active_id,
            amount,
            reason
        )

        if response.get("ok"):

            st.success(
                f"Request {response['request_id']} submitted as PENDING. "
                "Your balance has not changed."
            )

        else:

            st.error(
                response.get(
                    "error",
                    "Request could not be created."
                )
            )


# ============================================================
# 10. APPROVAL PANEL
# ============================================================

with right:

    st.subheader("Review pending requests")

    st.caption(
        "Demonstration reviewer control — "
        "not authenticated reviewer access."
    )

    reviewer = st.text_input(
        "Reviewer identifier",
        value="REVIEWER-DEMO"
    )

    pending = pending_requests()

    if not pending:

        st.info("No pending fee-adjustment requests.")

    else:

        labels = {
            (
                f"{r['request_id']} · "
                f"{r['student_id']} · "
                f"₹{r['amount']:,.0f}"
            ): r
            for r in pending
        }

        chosen_label = st.selectbox(
            "Select pending request",
            list(labels.keys())
        )

        chosen = labels[chosen_label]

        st.write("**Request reason:**")
        st.write(chosen["reason"])

        a, b = st.columns(2)

        with a:

            if st.button(
                "✅ Approve",
                use_container_width=True
            ):

                result = decide_request(
                    chosen["request_id"],
                    "APPROVE",
                    reviewer
                )

                if result.get("ok"):

                    st.success(
                        f"Approved. Result: {result.get('result')}"
                    )

                else:

                    st.error(result.get("error"))

        with b:

            if st.button(
                "❌ Reject",
                use_container_width=True
            ):

                result = decide_request(
                    chosen["request_id"],
                    "REJECT",
                    reviewer
                )

                if result.get("ok"):

                    st.warning(
                        f"Rejected. Result: {result.get('result')}"
                    )

                else:

                    st.error(result.get("error"))


# ============================================================
# 11. AUDIT TRAIL
# ============================================================

st.divider()

st.markdown("## 🔍 System Audit Trail")

st.caption(
    "Recent records of fee adjustment requests, "
    "review decisions and recorded system actions."
)

with st.expander(
    "View recent audit records",
    expanded=False
):

    audit_path = storage.data_dir() / "audit_log.jsonl"

    if audit_path.exists() and audit_path.stat().st_size:

        lines = [
            line
            for line in audit_path.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ][-12:]

        st.code(
            "\n".join(lines),
            language="json"
        )

    else:

        st.info(
            "No audit actions have been recorded yet."
        )


# ============================================================
# 12. FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:1.3rem 0;
        color:#718096;
        font-size:0.82rem;
    ">
        <strong style="color:#304f89">
            🌿 CampusPath
        </strong>
        <br>
        Intelligent Student Services Companion
        <br>
        Academic demonstration project · Agentic AI Engineering
    </div>
    """,
    unsafe_allow_html=True
)
