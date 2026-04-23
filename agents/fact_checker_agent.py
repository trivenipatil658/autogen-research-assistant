from autogen_agentchat.agents import AssistantAgent  # AutoGen's built-in conversational agent class
from config.llm_config import get_model_client  # Factory function that returns the configured Groq LLM client


def create_fact_checker_agent():
    # Factory function — creates and returns the Fact-Checker Agent

    model_client = get_model_client()  # Get the shared LLM client (Groq API)

    fact_checker_agent = AssistantAgent(
        name="fact_checker_agent",  # Unique name used to identify this agent in the pipeline
        model_client=model_client,  # The LLM client this agent will use to generate responses
        system_message=(
            # System prompt that defines the agent's role and behavior
            "You are a Fact-Checker Agent in a multi-agent system. "
            "Your job is to verify the correctness of the given content. "
            "Identify any incorrect, outdated, or misleading information. "
            "If everything is correct, say it is accurate. "  # Confirm accuracy when no issues found
            "If there are issues, clearly point them out and suggest corrections. "  # Flag and fix errors
            "Keep your response clear and structured."
        ),
    )

    return fact_checker_agent  # Return the configured agent for use in the pipeline
