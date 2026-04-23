from autogen_agentchat.agents import AssistantAgent  # AutoGen's built-in conversational agent class
from config.llm_config import get_model_client  # Factory function that returns the configured Groq LLM client
from utils.web_search import search_web, format_search_context, format_citations  # Web search utilities


def create_research_agent():
    # Factory function — creates and returns the Research Agent

    model_client = get_model_client()  # Get the shared LLM client (Groq API)

    research_agent = AssistantAgent(
        name="research_agent",  # Unique name used to identify this agent in the pipeline
        model_client=model_client,  # The LLM client this agent will use to generate responses
        system_message=(
            # System prompt that defines the agent's role and behavior
            "You are a Research Agent in a multi-agent student research system. "
            "Your job is to collect useful, clear, topic-focused research notes. "
            "Give well-structured points, key concepts, important facts, and short explanations. "
            "When web search results are provided, use them and cite sources with [n] notation. "  # Use web context if available
            "Do not write the final report. Do not summarize too much. "  # Restrict scope — research only
            "Your role is to gather and organize research material for the next agents."
        ),
    )

    return research_agent  # Return the configured agent for use in the pipeline


def get_web_context(topic: str) -> tuple[str, list]:
    """Return (formatted_context_str, raw_results) for a topic."""
    results = search_web(topic)  # Perform a DuckDuckGo search and get raw result dicts
    return format_search_context(results), results  # Return formatted string for prompt + raw list for citations
