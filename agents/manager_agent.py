from autogen_agentchat.agents import AssistantAgent
from config.llm_config import get_model_client


def create_manager_agent():
    model_client = get_model_client()

    manager_agent = AssistantAgent(
        name="manager_agent",
        model_client=model_client,
        system_message=(
            "You are the Manager Agent in a multi-agent research system. "
            "Your job is to understand the user's topic and create a clear execution plan "
            "for the other agents. "
            "You should define what needs to be researched, summarized, fact-checked, "
            "written, and reviewed. "
            "Your response should be structured, short, and actionable. "
            "Do not write the final report yourself."
        ),
    )

    return manager_agent