import logging

from openai import OpenAI

from genaidrivenetl.config import LLM_MODELS, OPENROUTER_API_KEY

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )

    def generate(self, prompt: str) -> str:
        for model in LLM_MODELS:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system",
                         "content": "You are a helpful " +
                                    "data engineering assistant."},
                        {"role": "user", "content": prompt},
                    ]
                )
                return response.choices[0].message.content
            except Exception:
                continue

        raise RuntimeError("No free models available")
