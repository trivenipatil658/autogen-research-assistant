from autogen_agentchat.agents import AssistantAgent  # AutoGen's built-in conversational agent class
from config.llm_config import get_model_client  # Factory function that returns the configured Groq LLM client


def create_writer_agent():
    # Factory function — creates and returns the Writer Agent

    model_client = get_model_client()  # Get the shared LLM client (Groq API)

    writer_agent = AssistantAgent(
        name="writer_agent",  # Unique name used to identify this agent in the pipeline
        model_client=model_client,  # The LLM client this agent will use to generate responses
        system_message=(
            # System prompt that defines the agent's role and behavior
            "You are a Writer Agent in a multi-agent research system. "
            "Your job is to convert the verified content into a clean final output. "
            "Generate two sections:\n"
            "1. A well-structured REPORT (with headings and explanation)\n"  # Section 1: full written report
            "2. A PPT OUTLINE (bullet points slide-wise)\n\n"               # Section 2: slide outline for export
            "Make the content clear, professional, and suitable for students. "
            "Do not include unnecessary repetition."  # Keep output concise and clean
        ),
    )

    return writer_agent  # Return the configured agent for use in the pipeline
