from openai import OpenAI
import numpy as np


class VectorizerOpenAI:
    def __init__(self, client: OpenAI) -> None:
        self.client = client


    def get_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        embedding = response.data[0].embedding
        norm = np.linalg.norm(embedding)


        return (np.array(embedding) / norm).tolist()