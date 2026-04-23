import asyncio  # Provides tools to run async functions (needed for AutoGen agents)
from pathlib import Path  # Cross-platform file path handling
from agents.manager_agent import create_manager_agent  # Imports factory function for Manager Agent
from agents.research_agent import create_research_agent, get_web_context  # Research Agent + web search helper
from agents.summarizer_agent import create_summarizer_agent  # Imports factory function for Summarizer Agent
from agents.fact_checker_agent import create_fact_checker_agent  # Imports factory function for Fact-Checker Agent
from agents.writer_agent import create_writer_agent  # Imports factory function for Writer Agent
from agents.reviewer_agent import create_reviewer_agent  # Imports factory function for Reviewer Agent
from utils.prompts import (  # Imports all prompt-builder functions used to instruct each agent
    build_manager_task,
    build_research_task,
    build_summary_task,
    build_fact_check_task,
    build_writer_task,
    build_reviewer_task,
)
from utils.web_search import format_citations  # Formats raw search results into a references section
from utils.export import export_all  # Handles exporting the final report to pptx/md/docx/pdf


async def run_pipeline(topic: str, export_formats: list[str] | None = None):
    # Main pipeline function — runs all 6 agents in sequence for a given topic

    if export_formats is None:
        export_formats = ["pptx", "md"]  # Default export formats if none are provided

    # Create all 6 agents using their factory functions
    manager_agent = create_manager_agent()
    research_agent = create_research_agent()
    summarizer_agent = create_summarizer_agent()
    fact_checker_agent = create_fact_checker_agent()
    writer_agent = create_writer_agent()
    reviewer_agent = create_reviewer_agent()

    print("\n--- STEP 0: MANAGER AGENT ---\n")
    # Run the Manager Agent — it creates an execution plan for the other agents
    manager_result = await manager_agent.run(task=build_manager_task(topic))
    manager_text = manager_result.messages[-1].content  # Extract the last message (the agent's response)
    print(manager_text)

    print("\n--- Fetching web search results... ---\n")
    # Perform a DuckDuckGo web search for the topic and get formatted context + raw results
    web_context, raw_results = get_web_context(topic)
    citations = format_citations(raw_results)  # Format raw results into a numbered references list

    print("\n--- STEP 1: RESEARCH AGENT ---\n")
    # Run the Research Agent — gathers structured research notes using the manager plan + web results
    research_result = await research_agent.run(
        task=build_research_task(topic, manager_text, web_context)
    )
    research_text = research_result.messages[-1].content  # Extract the agent's research output
    print(research_text)

    print("\n--- STEP 2: SUMMARIZER AGENT ---\n")
    # Run the Summarizer Agent — condenses the research into a student-friendly summary
    summary_result = await summarizer_agent.run(
        task=build_summary_task(topic, manager_text, research_text)
    )
    summary_text = summary_result.messages[-1].content  # Extract the summarized output
    print(summary_text)

    print("\n--- STEP 3: FACT-CHECKER AGENT ---\n")
    # Run the Fact-Checker Agent — verifies the summary for accuracy and flags any issues
    fact_check_result = await fact_checker_agent.run(
        task=build_fact_check_task(topic, manager_text, summary_text)
    )
    fact_check_text = fact_check_result.messages[-1].content  # Extract the fact-check notes
    print(fact_check_text)

    print("\n--- STEP 4: WRITER AGENT ---\n")
    # Run the Writer Agent — produces a final report + slide-wise PPT outline from verified content
    writer_result = await writer_agent.run(
        task=build_writer_task(topic, manager_text, summary_text, fact_check_text, citations)
    )
    writer_text = writer_result.messages[-1].content  # Extract the written report + PPT outline
    print(writer_text)

    print("\n--- STEP 5: REVIEWER AGENT ---\n")
    # Run the Reviewer Agent — polishes and improves the writer's output for clarity and professionalism
    reviewer_result = await reviewer_agent.run(
        task=build_reviewer_task(topic, manager_text, writer_text)
    )
    reviewer_text = reviewer_result.messages[-1].content  # Extract the final reviewed output
    print(reviewer_text)

    output_dir = Path("outputs")  # Define the output directory path
    output_dir.mkdir(exist_ok=True)  # Create the outputs/ folder if it doesn't already exist

    # Save the final reviewed report (with citations) to a text file
    (output_dir / "final_reviewed_output.txt").write_text(reviewer_text + citations, encoding="utf-8")

    # Save the full pipeline output (all agent responses) to a single text file for reference
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

    # Export the report to all requested formats (pptx, md, docx, pdf)
    exported = export_all(writer_text, reviewer_text + citations, topic, export_formats, output_dir)
    print("\nExported files:")
    for fmt, path in exported.items():
        print(f"  [{fmt.upper()}] {path}")  # Print each exported file path

    # Return a dictionary of all agent outputs + exported file paths (used by the Streamlit UI)
    return {
        "manager": manager_text,
        "research": research_text,
        "summary": summary_text,
        "fact_check": fact_check_text,
        "writer": writer_text,
        "reviewer": reviewer_text,
        "citations": citations,
        "exported": {k: str(v) for k, v in exported.items()},  # Convert Path objects to strings
    }


async def main():
    # CLI entry point — prompts the user for a topic and export formats
    topic = input("Enter your research topic: ").strip()  # Read and clean the topic input
    if not topic:
        print("Error: Topic cannot be empty.")  # Validate that topic is not blank
        return

    # Read export format preferences; default to pptx and md if nothing is entered
    fmt_input = input("Export formats (comma-separated: pptx,md,docx,pdf) [default: pptx,md]: ").strip()
    formats = [f.strip() for f in fmt_input.split(",")] if fmt_input else ["pptx", "md"]

    await run_pipeline(topic, formats)  # Run the full pipeline with the given inputs


if __name__ == "__main__":
    asyncio.run(main())  # Entry point — runs the async main() function using asyncio
