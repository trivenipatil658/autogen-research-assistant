from autogen_agentchat.agents import AssistantAgent  # AutoGen's built-in conversational agent class
from config.llm_config import get_model_client  # Factory function that returns the configured Groq LLM client


def create_summarizer_agent():
    # Factory function — creates and returns the Summarizer Agent

    model_client = get_model_client()  # Get the shared LLM client (Groq API)

    summarizer_agent = AssistantAgent(
        name="summarizer_agent",  # Unique name used to identify this agent in the pipeline
        model_client=model_client,  # The LLM client this agent will use to generate responses
        system_message=(
            # System prompt that defines the agent's role and behavior
            "You are a Summarizer Agent in a multi-agent student research system. "
            "Your job is to take research content and convert it into a short, clear, "
            "well-structured summary. Keep important points, remove repetition, "
            "and make the content easy for students to understand. "
            "Do not fact-check and do not write the final full report."  # Restrict scope — summarizing only
        ),
    )

    return summarizer_agent  # Return the configured agent for use in the pipeline
