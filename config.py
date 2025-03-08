import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Graph Database Configuration
GRAPH_DB_TYPE = os.getenv("GRAPH_DB_TYPE")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER")  # deepseek, openai, anthropic
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
