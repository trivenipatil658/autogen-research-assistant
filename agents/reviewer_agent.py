from autogen_agentchat.agents import AssistantAgent
from config.llm_config import get_model_client


def create_reviewer_agent():
    model_client = get_model_client()

    reviewer_agent = AssistantAgent(
        name="reviewer_agent",
        model_client=model_client,
        system_message=(
            "You are a Reviewer Agent in a multi-agent research system. "
            "Your job is to review the final written output and improve it. "
            "Make the content clearer, more professional, well-structured, "
            "and easy for students to understand. "
            "Remove repetition, improve formatting, and refine the language. "
            "Keep the meaning the same, but make the final result better."
        ),
    )

    return reviewer_agent