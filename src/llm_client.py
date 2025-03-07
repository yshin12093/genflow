import json
import requests
from config import LLM_PROVIDER, OPENAI_API_KEY, DEEPSEEK_API_KEY, CLAUDE_API_KEY

class LLMClient:
    """Unified interface for multiple LLM providers (DeepSeek, OpenAI, Claude)."""

    def __init__(self) -> None:
        """Initialize the LLM client with the configured provider."""
        self.provider = LLM_PROVIDER.lower()
        self.api_key = self._get_api_key()

    def _get_api_key(self) -> str:
        """Retrieve API key based on selected LLM provider."""
        if self.provider == "deepseek":
            return DEEPSEEK_API_KEY
        elif self.provider == "openai":
            return OPENAI_API_KEY
        elif self.provider == "anthropic":
            return CLAUDE_API_KEY
        else:
            raise ValueError(f"❌ Unsupported LLM provider: {self.provider}")

    def call_llm(self, system_message: str, user_message: str) -> dict:
        """Route the request to the configured LLM provider."""
        if self.provider == "deepseek":
            return self._call_deepseek(system_message, user_message)
        elif self.provider == "openai":
            return self._call_openai(system_message, user_message)
        elif self.provider == "anthropic":
            return self._call_claude(system_message, user_message)
        else:
            raise ValueError(f"❌ Unsupported LLM provider: {self.provider}")

    def _call_deepseek(self, system_message: str, user_message: str) -> dict:
        """Call DeepSeek API."""
        url = "https://api.deepseek.com/v1/chat/completions"
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            "stream": False
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.post(url, json=payload, headers=headers)
        return self._format_response(response)

    def _call_openai(self, system_message: str, user_message: str) -> dict:
        """Call OpenAI API."""
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.post(url, json=payload, headers=headers)
        return self._format_response(response)

    def _call_claude(self, system_message: str, user_message: str) -> dict:
        """Call Claude API (Anthropic)."""
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": "claude-2",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.post(url, json=payload, headers=headers)
        return self._format_response(response)

    def _format_response(self, response: requests.Response) -> dict:
        """Format the API response."""
        if response.status_code == 200:
            chat_response = response.json()["choices"][0]["message"]["content"]
            return {"statusCode": 200, "body": json.dumps({"response": chat_response})}
        else:
            return {
                "statusCode": response.status_code,
                "body": json.dumps({"error": response.text}),
            }

# Initialize LLM client
llm_client = LLMClient()
