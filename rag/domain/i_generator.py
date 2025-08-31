from typing import Protocol, Optional

class IGenerator(Protocol):
    def generate(self, prompt: str, model: str, temperature: Optional[float] = None) -> str: ...
