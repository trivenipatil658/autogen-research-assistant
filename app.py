import asyncio
import streamlit as st
from pathlib import Path
from main import run_pipeline

st.set_page_config(page_title="AI Research Assistant", page_icon="🔬", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: #f8fafc; }

    /* Hero header */
    .hero {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #818cf8 100%);
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 24px rgba(99,102,241,.25);
    }
    .hero h1 { font-size: 2.4rem; font-weight: 700; color: #ffffff; margin: 0 0 0.5rem; }
    .hero p  { color: rgba(255,255,255,.85); font-size: 1rem; margin: 0; }
    .badge {
        display: inline-block;
        background: rgba(255,255,255,.2);
        border: 1px solid rgba(255,255,255,.4);
        color: #ffffff;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: .75rem;
        font-weight: 500;
        margin: 0 4px;
    }

    /* Download buttons */
    .dl-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: .75rem 1rem;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,.06);
        margin-bottom: .5rem;
    }
    .dl-card p {
        margin: 0 0 .5rem;
        font-size: .8rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: .05em;
    }
    .dl-card .stDownloadButton { margin: 0; }
    .dl-card .stDownloadButton > button {
        width: 100% !important;
        margin: 0 !important;
    }

    /* Success banner */
    .success-banner {
        background: linear-gradient(90deg, #ecfdf5, #d1fae5);
        border: 1px solid #6ee7b7;
        border-radius: 10px;
        padding: .9rem 1.5rem;
        color: #065f46;
        font-weight: 600;
        text-align: center;
        margin: 1.5rem 0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: .6rem 2rem !important;
        color: white !important;
        transition: opacity .2s;
        box-shadow: 0 2px 8px rgba(99,102,241,.35) !important;
    }
    .stButton > button[kind="primary"]:hover { opacity: .88; }

    /* Download button */
    .stDownloadButton > button {
        background: #ffffff !important;
        border: 1.5px solid #6366f1 !important;
        border-radius: 8px !important;
        color: #4f46e5 !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    .stDownloadButton > button:hover {
        background: #eef2ff !important;
    }

    /* Text input */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #1e293b !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
    }

    /* Spinner */
    .stSpinner > div { border-top-color: #6366f1 !important; }

    /* Hide default Streamlit branding */
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    export_formats = st.multiselect(
        "Export formats",
        ["pptx", "md", "docx", "pdf"],
        default=["pptx", "md"],
    )
    st.markdown("---")
    st.markdown("**Pipeline**")
    pipeline_steps = [
        ("📋", "Manager"),
        ("🔍", "Research"),
        ("📝", "Summarize"),
        ("✅", "Fact-Check"),
        ("✍️", "Write"),
        ("🔎", "Review"),
    ]
    for icon, name in pipeline_steps:
        st.markdown(f"{icon} &nbsp; {name}", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        "<span class='badge' style='background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);color:#4f46e5;border-radius:20px;padding:3px 12px;font-size:.75rem;font-weight:500;margin:0 4px;display:inline-block'>AutoGen</span>"
        "<span class='badge' style='background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);color:#4f46e5;border-radius:20px;padding:3px 12px;font-size:.75rem;font-weight:500;margin:0 4px;display:inline-block'>Groq</span>"
        "<span class='badge' style='background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);color:#4f46e5;border-radius:20px;padding:3px 12px;font-size:.75rem;font-weight:500;margin:0 4px;display:inline-block'>DuckDuckGo</span>",
        unsafe_allow_html=True,
    )

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔬 Multi-Agent Research Assistant</h1>
    <p>Powered by <strong style="color:rgba(255,255,255,.95)">AutoGen</strong> &amp;
       <strong style="color:rgba(255,255,255,.95)">Groq</strong> &nbsp;·&nbsp;
       Web Search &nbsp;·&nbsp; Citations &nbsp;·&nbsp; Multi-format Export</p>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")
with col_input:
    topic = st.text_input("Research Topic", placeholder="Enter a research topic — e.g. Quantum Computing", label_visibility="collapsed")
with col_btn:
    run_btn = st.button("🚀 Run", type="primary", disabled=not topic.strip(), use_container_width=True)

# ── Pipeline ──────────────────────────────────────────────────────────────────
STEPS = [
    ("manager",    "📋", "Manager Agent"),
    ("research",   "🔍", "Research Agent"),
    ("summary",    "📝", "Summarizer Agent"),
    ("fact_check", "✅", "Fact-Checker Agent"),
    ("writer",     "✍️", "Writer Agent"),
    ("reviewer",   "🔎", "Reviewer Agent"),
]

MIME = {
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "md":   "text/markdown",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "pdf":  "application/pdf",
}

if run_btn and topic.strip():
    placeholders = {}

    st.markdown("#### 🔄 Pipeline Progress")
    for key, icon, label in STEPS:
        with st.expander(f"{icon} {label}", expanded=False):
            placeholders[key] = st.empty()

    citations_ph = st.empty()

    with st.spinner("Running research pipeline…"):
        try:
            results = asyncio.run(run_pipeline(topic.strip(), export_formats or ["pptx", "md"]))
        except Exception as e:
            st.error(f"Pipeline error: {e}")
            st.stop()

    for key, icon, label in STEPS:
        placeholders[key].markdown(results.get(key, "_No output_"))

    if results.get("citations"):
        citations_ph.markdown(results["citations"])

    st.markdown('<div class="success-banner">✅ Pipeline complete — your report is ready!</div>', unsafe_allow_html=True)

    # ── Downloads ─────────────────────────────────────────────────────────────
    exported = results.get("exported", {})
    if exported:
        st.markdown("#### ⬇️ Download Report")
        fmt_icons = {"pptx": "📊", "md": "📝", "docx": "📄", "pdf": "📕"}
        valid = [(fmt, Path(p)) for fmt, p in exported.items() if Path(p).exists()]
        dl_cols = st.columns(len(valid))
        for col, (fmt, path) in zip(dl_cols, valid):
            with col:
                st.download_button(
                    label=f"{fmt_icons.get(fmt,'📁')} Download {fmt.upper()}",
                    data=path.read_bytes(),
                    file_name=path.name,
                    mime=MIME.get(fmt, "application/octet-stream"),
                    use_container_width=True,
                )

    # ── Full report ───────────────────────────────────────────────────────────
    with st.expander("📄 Full Reviewed Report", expanded=True):
        st.markdown(results.get("reviewer", "") + results.get("citations", ""))
