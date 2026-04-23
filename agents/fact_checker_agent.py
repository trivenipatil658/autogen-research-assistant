from autogen_agentchat.agents import AssistantAgent
from config.llm_config import get_model_client


def create_fact_checker_agent():
    model_client = get_model_client()

    fact_checker_agent = AssistantAgent(
        name="fact_checker_agent",
        model_client=model_client,
        system_message=(
            "You are a Fact-Checker Agent in a multi-agent system. "
            "Your job is to verify the correctness of the given content. "
            "Identify any incorrect, outdated, or misleading information. "
            "If everything is correct, say it is accurate. "
            "If there are issues, clearly point them out and suggest corrections. "
            "Keep your response clear and structured."
        ),
    )

    return fact_checker_agent