from autogen_agentchat.agents import AssistantAgent
from config.llm_config import get_model_client
from utils.web_search import search_web, format_search_context, format_citations


def create_research_agent():
    model_client = get_model_client()

    research_agent = AssistantAgent(
        name="research_agent",
        model_client=model_client,
        system_message=(
            "You are a Research Agent in a multi-agent student research system. "
            "Your job is to collect useful, clear, topic-focused research notes. "
            "Give well-structured points, key concepts, important facts, and short explanations. "
            "When web search results are provided, use them and cite sources with [n] notation. "
            "Do not write the final report. Do not summarize too much. "
            "Your role is to gather and organize research material for the next agents."
        ),
    )

    return research_agent


def get_web_context(topic: str) -> tuple[str, list]:
    """Return (formatted_context_str, raw_results) for a topic."""
    results = search_web(topic)
    return format_search_context(results), results