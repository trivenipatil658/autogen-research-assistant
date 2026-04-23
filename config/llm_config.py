import os  # Used to read environment variables from the system
from dotenv import load_dotenv  # Loads variables from the .env file into the environment
from autogen_ext.models.openai import OpenAIChatCompletionClient  # OpenAI-compatible client used to connect to Groq

load_dotenv()  # Reads the .env file and loads GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL into os.environ

# Read each required config value from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")    # Your Groq API key for authentication
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")  # Groq's OpenAI-compatible API base URL
GROQ_MODEL = os.getenv("GROQ_MODEL")        # The LLM model name to use (e.g. llama3-70b-8192)


def get_model_client():
    # Factory function — creates and returns a configured LLM client for use by all agents

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in .env file")  # Stop early if API key is missing

    if not GROQ_BASE_URL:
        raise ValueError("GROQ_BASE_URL not found in .env file")  # Stop early if base URL is missing

    if not GROQ_MODEL:
        raise ValueError("GROQ_MODEL not found in .env file")  # Stop early if model name is missing

    # Create the OpenAI-compatible client pointed at Groq's API
    model_client = OpenAIChatCompletionClient(
        model=GROQ_MODEL,        # The LLM model to use for completions
        api_key=GROQ_API_KEY,    # API key for authenticating with Groq
        base_url=GROQ_BASE_URL,  # Groq's API endpoint (OpenAI-compatible)
        model_info={
            "vision": False,           # This model does not support image/vision inputs
            "function_calling": True,  # This model supports function/tool calling
            "json_output": True,       # This model can return structured JSON output
            "family": "unknown",       # Model family — set to unknown for Groq models
            "structured_output": True, # This model supports structured output schemas
        },
    )

    return model_client  # Return the ready-to-use LLM client
