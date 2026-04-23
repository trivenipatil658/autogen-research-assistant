import asyncio
from pathlib import Path
from agents.manager_agent import create_manager_agent
from agents.research_agent import create_research_agent, get_web_context
from agents.summarizer_agent import create_summarizer_agent
from agents.fact_checker_agent import create_fact_checker_agent
from agents.writer_agent import create_writer_agent
from agents.reviewer_agent import create_reviewer_agent
from utils.prompts import (
    build_manager_task,
    build_research_task,
    build_summary_task,
    build_fact_check_task,
    build_writer_task,
    build_reviewer_task,
)
from utils.web_search import format_citations
from utils.export import export_all


async def run_pipeline(topic: str, export_formats: list[str] | None = None):
    if export_formats is None:
        export_formats = ["pptx", "md"]

    manager_agent = create_manager_agent()
    research_agent = create_research_agent()
    summarizer_agent = create_summarizer_agent()
    fact_checker_agent = create_fact_checker_agent()
    writer_agent = create_writer_agent()
    reviewer_agent = create_reviewer_agent()

    print("\n--- STEP 0: MANAGER AGENT ---\n")
    manager_result = await manager_agent.run(task=build_manager_task(topic))
    manager_text = manager_result.messages[-1].content
    print(manager_text)

    print("\n--- Fetching web search results... ---\n")
    web_context, raw_results = get_web_context(topic)
    citations = format_citations(raw_results)

    print("\n--- STEP 1: RESEARCH AGENT ---\n")
    research_result = await research_agent.run(
        task=build_research_task(topic, manager_text, web_context)
    )
    research_text = research_result.messages[-1].content
    print(research_text)

    print("\n--- STEP 2: SUMMARIZER AGENT ---\n")
    summary_result = await summarizer_agent.run(
        task=build_summary_task(topic, manager_text, research_text)
    )
    summary_text = summary_result.messages[-1].content
    print(summary_text)

    print("\n--- STEP 3: FACT-CHECKER AGENT ---\n")
    fact_check_result = await fact_checker_agent.run(
        task=build_fact_check_task(topic, manager_text, summary_text)
    )
    fact_check_text = fact_check_result.messages[-1].content
    print(fact_check_text)

    print("\n--- STEP 4: WRITER AGENT ---\n")
    writer_result = await writer_agent.run(
        task=build_writer_task(topic, manager_text, summary_text, fact_check_text, citations)
    )
    writer_text = writer_result.messages[-1].content
    print(writer_text)

    print("\n--- STEP 5: REVIEWER AGENT ---\n")
    reviewer_result = await reviewer_agent.run(
        task=build_reviewer_task(topic, manager_text, writer_text)
    )
    reviewer_text = reviewer_result.messages[-1].content
    print(reviewer_text)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    (output_dir / "final_reviewed_output.txt").write_text(reviewer_text + citations, encoding="utf-8")
    (output_dir / "full_pipeline_output.txt").write_text(
        f"TOPIC: {topic}\n\n"
        f"--- MANAGER ---\n{manager_text}\n\n"
        f"--- RESEARCH ---\n{research_text}\n\n"
        f"--- SUMMARY ---\n{summary_text}\n\n"
        f"--- FACT-CHECK ---\n{fact_check_text}\n\n"
        f"--- WRITER ---\n{writer_text}\n\n"
        f"--- REVIEWER ---\n{reviewer_text}\n\n"
        f"{citations}",
        encoding="utf-8",
    )

    exported = export_all(writer_text, reviewer_text + citations, topic, export_formats, output_dir)
    print("\nExported files:")
    for fmt, path in exported.items():
        print(f"  [{fmt.upper()}] {path}")

    return {
        "manager": manager_text,
        "research": research_text,
        "summary": summary_text,
        "fact_check": fact_check_text,
        "writer": writer_text,
        "reviewer": reviewer_text,
        "citations": citations,
        "exported": {k: str(v) for k, v in exported.items()},
    }


async def main():
    topic = input("Enter your research topic: ").strip()
    if not topic:
        print("Error: Topic cannot be empty.")
        return

    fmt_input = input("Export formats (comma-separated: pptx,md,docx,pdf) [default: pptx,md]: ").strip()
    formats = [f.strip() for f in fmt_input.split(",")] if fmt_input else ["pptx", "md"]

    await run_pipeline(topic, formats)


if __name__ == "__main__":
    asyncio.run(main())
