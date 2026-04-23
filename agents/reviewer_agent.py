from autogen_agentchat.agents import AssistantAgent  # AutoGen's built-in conversational agent class
from config.llm_config import get_model_client  # Factory function that returns the configured Groq LLM client


def create_reviewer_agent():
    # Factory function — creates and returns the Reviewer Agent

    model_client = get_model_client()  # Get the shared LLM client (Groq API)

    reviewer_agent = AssistantAgent(
        name="reviewer_agent",  # Unique name used to identify this agent in the pipeline
        model_client=model_client,  # The LLM client this agent will use to generate responses
        system_message=(
            # System prompt that defines the agent's role and behavior
            "You are a Reviewer Agent in a multi-agent research system. "
            "Your job is to review the final written output and improve it. "
            "Make the content clearer, more professional, well-structured, "
            "and easy for students to understand. "
            "Remove repetition, improve formatting, and refine the language. "  # Polish the output
            "Keep the meaning the same, but make the final result better."      # Do not change facts
        ),
    )

    return reviewer_agent  # Return the configured agent for use in the pipeline
