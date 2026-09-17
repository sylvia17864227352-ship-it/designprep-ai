import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMProvider:
    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ):
        self.model = (
            model
            or os.getenv("LLM_MODEL")
        )

        self.base_url = (
            base_url
            or os.getenv("LLM_BASE_URL")
        )

        self.api_key = (
            api_key
            or os.getenv("LLM_API_KEY")
        )

        if not self.model:
            raise ValueError(
                "LLM model is not configured."
            )

        if not self.api_key:
            raise ValueError(
                "LLM API key is not configured."
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )

        return (
            response
            .choices[0]
            .message
            .content
            or ""
        ).strip()
