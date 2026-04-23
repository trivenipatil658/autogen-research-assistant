from autogen_agentchat.agents import AssistantAgent
from config.llm_config import get_model_client


def create_writer_agent():
    model_client = get_model_client()

    writer_agent = AssistantAgent(
        name="writer_agent",
        model_client=model_client,
        system_message=(
            "You are a Writer Agent in a multi-agent research system. "
            "Your job is to convert the verified content into a clean final output. "
            "Generate two sections:\n"
            "1. A well-structured REPORT (with headings and explanation)\n"
            "2. A PPT OUTLINE (bullet points slide-wise)\n\n"
            "Make the content clear, professional, and suitable for students. "
            "Do not include unnecessary repetition."
        ),
    )

    return writer_agent