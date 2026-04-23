import asyncio  # Needed to run the async pipeline function from a sync Streamlit context
import streamlit as st  # Streamlit — the web UI framework
from pathlib import Path  # Cross-platform file path handling for reading exported files
from main import run_pipeline  # The main async pipeline that runs all 6 agents in sequence

# Configure the Streamlit page — sets browser tab title, icon, and uses full-width layout
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
with st.sidebar:  # Everything inside this block renders in the left sidebar
    st.markdown("### ⚙️ Settings")
    st.markdown("---")  # Horizontal divider
    export_formats = st.multiselect(
        "Export formats",
        ["pptx", "md", "docx", "pdf"],  # All supported export formats
        default=["pptx", "md"],          # Pre-selected formats on first load
    )
    st.markdown("---")
    st.markdown("**Pipeline**")  # Section label for the pipeline step list
    pipeline_steps = [  # List of (icon, label) tuples for each pipeline step
        ("📋", "Manager"),
        ("🔍", "Research"),
        ("📝", "Summarize"),
        ("✅", "Fact-Check"),
        ("✍️", "Write"),
        ("🔎", "Review"),
    ]
    for icon, name in pipeline_steps:
        st.markdown(f"{icon} &nbsp; {name}", unsafe_allow_html=True)  # Render each step with icon
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
# Split the row into a wide input column and a narrow button column
col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")
with col_input:
    # Text input for the research topic; label is hidden but provided for accessibility
    topic = st.text_input("Research Topic", placeholder="Enter a research topic — e.g. Quantum Computing", label_visibility="collapsed")
with col_btn:
    # Run button — disabled until the user types a non-empty topic
    run_btn = st.button("🚀 Run", type="primary", disabled=not topic.strip(), use_container_width=True)

# ── Pipeline ──────────────────────────────────────────────────────────────────
# Ordered list of (result_key, icon, display_label) for each pipeline step
STEPS = [
    ("manager",    "📋", "Manager Agent"),
    ("research",   "🔍", "Research Agent"),
    ("summary",    "📝", "Summarizer Agent"),
    ("fact_check", "✅", "Fact-Checker Agent"),
    ("writer",     "✍️", "Writer Agent"),
    ("reviewer",   "🔎", "Reviewer Agent"),
]

# MIME types for each export format — used by st.download_button to set the correct file type
MIME = {
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "md":   "text/markdown",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "pdf":  "application/pdf",
}

if run_btn and topic.strip():  # Only run when the button is clicked and topic is not empty
    placeholders = {}  # Dict to hold st.empty() placeholders for each agent's output

    st.markdown("#### 🔄 Pipeline Progress")
    # Create a collapsed expander for each step — output will be filled in after the pipeline runs
    for key, icon, label in STEPS:
        with st.expander(f"{icon} {label}", expanded=False):
            placeholders[key] = st.empty()  # Reserve a spot for this agent's output

    citations_ph = st.empty()  # Placeholder for the citations section

    with st.spinner("Running research pipeline…"):  # Show a loading spinner while pipeline runs
        try:
            # Run the async pipeline synchronously using asyncio.run (required in Streamlit)
            results = asyncio.run(run_pipeline(topic.strip(), export_formats or ["pptx", "md"]))
        except Exception as e:
            st.error(f"Pipeline error: {e}")  # Show error message if pipeline fails
            st.stop()  # Stop further execution of the script

    # Fill each agent's expander with its output now that the pipeline has completed
    for key, icon, label in STEPS:
        placeholders[key].markdown(results.get(key, "_No output_"))  # Show output or fallback text

    if results.get("citations"):  # Only show citations section if there are any
        citations_ph.markdown(results["citations"])

    # Show a styled green success banner
    st.markdown('<div class="success-banner">✅ Pipeline complete — your report is ready!</div>', unsafe_allow_html=True)

    # ── Downloads ─────────────────────────────────────────────────────────────
    exported = results.get("exported", {})  # Get the dict of {format: file_path} from pipeline results
    if exported:
        st.markdown("#### ⬇️ Download Report")
        fmt_icons = {"pptx": "📊", "md": "📝", "docx": "📄", "pdf": "📕"}  # Icon per format
        # Filter to only formats whose output files actually exist on disk
        valid = [(fmt, Path(p)) for fmt, p in exported.items() if Path(p).exists()]
        dl_cols = st.columns(len(valid))  # Create one equal-width column per valid export
        for col, (fmt, path) in zip(dl_cols, valid):  # Pair each column with its format
            with col:
                st.download_button(
                    label=f"{fmt_icons.get(fmt,'📁')} Download {fmt.upper()}",  # Button label with icon
                    data=path.read_bytes(),  # Read the file bytes for download
                    file_name=path.name,     # Suggest the original filename for the download
                    mime=MIME.get(fmt, "application/octet-stream"),  # Set correct MIME type
                    use_container_width=True,  # Make button fill its column width
                )

    # ── Full report ───────────────────────────────────────────────────────────
    with st.expander("📄 Full Reviewed Report", expanded=True):  # Show full report expanded by default
        st.markdown(results.get("reviewer", "") + results.get("citations", ""))  # Combine report + citations
