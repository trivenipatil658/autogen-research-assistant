def build_manager_task(topic: str) -> str:
    # Builds the task prompt for the Manager Agent
    # Tells it to create a structured execution plan for all other agents based on the topic
    return (
        f"The user wants a research workflow on this topic: {topic}. "
        "Create a short execution plan for the research agent, summarizer agent, "
        "fact-checker agent, writer agent, and reviewer agent."
    )


def build_research_task(topic: str, manager_text: str, web_context: str = "") -> str:
    # Builds the task prompt for the Research Agent
    # Includes the manager's plan and optional web search results as context
    web_section = f"\n\nWeb Search Context:\n{web_context}" if web_context else ""  # Only add web section if results exist
    return (
        f"Topic: {topic}\n\n"
        f"Manager plan:\n{manager_text}"
        f"{web_section}\n\n"
        "Now research this topic in a clear and structured way. Cite sources using [n] where relevant."
    )


def build_summary_task(topic: str, manager_text: str, research_text: str) -> str:
    # Builds the task prompt for the Summarizer Agent
    # Passes the manager plan and full research output so it can condense it for students
    return (
        f"Topic: {topic}\n\n"
        f"Manager plan:\n{manager_text}\n\n"
        f"Research content:\n{research_text}\n\n"
        "Summarize this clearly for students."
    )


def build_fact_check_task(topic: str, manager_text: str, summary_text: str) -> str:
    # Builds the task prompt for the Fact-Checker Agent
    # Passes the summary so it can verify accuracy and flag any misleading claims
    return (
        f"Topic: {topic}\n\n"
        f"Manager plan:\n{manager_text}\n\n"
        f"Summary to verify:\n{summary_text}\n\n"
        "Check correctness, clarity, and misleading claims. Suggest corrections if needed."
    )


def build_writer_task(topic: str, manager_text: str, summary_text: str, fact_check_text: str, citations: str = "") -> str:
    # Builds the task prompt for the Writer Agent
    # Passes verified summary + fact-check notes + citations so it can produce the final report and PPT outline
    return (
        f"Topic: {topic}\n\n"
        f"Manager plan:\n{manager_text}\n\n"
        "Using the verified content below, generate:\n"
        "1. A clean final report\n"
        "2. A slide-wise PPT outline (label each slide clearly as 'Slide N: Title')\n\n"
        f"SUMMARY:\n{summary_text}\n\n"
        f"FACT-CHECK NOTES:\n{fact_check_text}"
        + (f"\n\nCITATIONS:\n{citations}" if citations else "")  # Append citations only if they exist
    )


def build_reviewer_task(topic: str, manager_text: str, writer_text: str) -> str:
    # Builds the task prompt for the Reviewer Agent
    # Passes the writer's output so it can polish, restructure, and improve the final report
    return (
        f"Topic: {topic}\n\n"
        f"Manager plan:\n{manager_text}\n\n"
        "Review and improve the following final output. "
        "Make it clearer, more professional, better structured, and remove repetition "
        "without changing the meaning.\n\n"
        f"{writer_text}"
    )
