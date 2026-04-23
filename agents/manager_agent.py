from autogen_agentchat.agents import AssistantAgent  # AutoGen's built-in conversational agent class
from config.llm_config import get_model_client  # Factory function that returns the configured Groq LLM client


def create_manager_agent():
    # Factory function — creates and returns the Manager Agent

    model_client = get_model_client()  # Get the shared LLM client (Groq API)

    manager_agent = AssistantAgent(
        name="manager_agent",  # Unique name used to identify this agent in the pipeline
        model_client=model_client,  # The LLM client this agent will use to generate responses
        system_message=(
            # System prompt that defines the agent's role and behavior
            "You are the Manager Agent in a multi-agent research system. "
            "Your job is to understand the user's topic and create a clear execution plan "
            "for the other agents. "
            "You should define what needs to be researched, summarized, fact-checked, "
            "written, and reviewed. "
            "Your response should be structured, short, and actionable. "
            "Do not write the final report yourself."  # Restrict scope — planning only
        ),
    )

    return manager_agent  # Return the configured agent for use in the pipeline
