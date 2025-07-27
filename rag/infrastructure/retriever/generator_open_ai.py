from openai import OpenAI
from typing import Optional


class GeneratorOpenAI:
    def __init__(self, client: OpenAI) -> None:
        self.client = client


    def generate(self, prompt: str, model: str, temperature: Optional[float] = None) -> str:
        response = self.client.responses.create(
            model=model,
            input=prompt,
            temperature=temperature
        )

        return response.output_text