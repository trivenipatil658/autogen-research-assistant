from autogen_agentchat.agents import AssistantAgent
from config.llm_config import get_model_client


def create_summarizer_agent():
    model_client = get_model_client()

    summarizer_agent = AssistantAgent(
        name="summarizer_agent",
        model_client=model_client,
        system_message=(
            "You are a Summarizer Agent in a multi-agent student research system. "
            "Your job is to take research content and convert it into a short, clear, "
            "well-structured summary. Keep important points, remove repetition, "
            "and make the content easy for students to understand. "
            "Do not fact-check and do not write the final full report."
        ),
    )

    return summarizer_agent