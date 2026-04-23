import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")
GROQ_MODEL = os.getenv("GROQ_MODEL")


def get_model_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in .env file")

    if not GROQ_BASE_URL:
        raise ValueError("GROQ_BASE_URL not found in .env file")

    if not GROQ_MODEL:
        raise ValueError("GROQ_MODEL not found in .env file")

    model_client = OpenAIChatCompletionClient(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": True,
        },
    )

    return model_client