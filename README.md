# Multi-Agent Research Assistant for Students

A real AutoGen framework project using the Groq API as the LLM backend, with web search, citations, Streamlit UI, and multi-format export.

## Features
- 🔍 **Web Search** — DuckDuckGo search (no API key needed) injected into the research step
- 📎 **Citation Support** — Sources cited with `[n]` notation throughout the report
- 🖥️ **Streamlit UI** — Interactive browser UI with live step output and download buttons
- 📊 **Auto PPT Export** — Slide-wise PowerPoint generated automatically from writer output
- 📄 **Multiple Output Formats** — Export as `.pptx`, `.md`, `.docx`, `.pdf`

## Agents
1. Manager Agent — creates execution plan
2. Research Agent — gathers research + web search results with citations
3. Summarizer Agent — condenses research for students
4. Fact-Checker Agent — verifies accuracy
5. Writer Agent — produces final report + PPT outline
6. Reviewer Agent — improves and polishes final output

## Workflow
```
Manager → Research (+ Web Search) → Summarize → Fact Check → Write → Review → Export
```

## Tech Stack
- Python
- AutoGen (`autogen-agentchat`, `autogen-ext`)
- Groq API (via OpenAI-compatible client)
- Streamlit
- python-pptx, python-docx, fpdf2
- DuckDuckGo Instant Answer API
- python-dotenv

## Project Structure
```text
autogen_research_assistant/
├── .venv/
├── .env
├── app.py                  ← Streamlit UI
├── main.py                 ← CLI entry point
├── requirements.txt
├── README.md
├── agents/
│   ├── __init__.py
│   ├── manager_agent.py
│   ├── research_agent.py   ← web search wired in
│   ├── summarizer_agent.py
│   ├── fact_checker_agent.py
│   ├── writer_agent.py
│   └── reviewer_agent.py
├── config/
│   └── llm_config.py
├── utils/
│   ├── prompts.py
│   ├── web_search.py       ← DuckDuckGo search + citation formatter
│   └── export.py           ← PPT / DOCX / PDF / Markdown export
└── outputs/                ← all generated files (gitignored)
```

## Setup

1. Clone the repo and create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```env
   GROQ_API_KEY=<your_groq_api_key>
   GROQ_BASE_URL=https://api.groq.com/openai/v1
   GROQ_MODEL=llama3-70b-8192
   ```

## Usage

### Streamlit UI (recommended)
```bash
streamlit run app.py
```

### CLI
```bash
python main.py
```
You will be prompted for a topic and export formats (`pptx,md,docx,pdf`).

## Output Files
All outputs are saved to `outputs/` and gitignored:
- `final_reviewed_output.txt`
- `full_pipeline_output.txt`
- `<topic>.pptx`
- `<topic>.md`
- `<topic>.docx`
- `<topic>.pdf`
