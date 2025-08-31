from openai import OpenAI
from openai.types.beta import Assistant
import json
import time

from pathlib import Path


class RAGServiceAA:
    def __init__(self, openai_client: OpenAI, assistant: Assistant) -> None:
        self.openai_client = openai_client
        self.assistant = assistant

        base_dir = Path(__file__).resolve().parent.parent.parent
        data_dir = base_dir / "data"
        self.mapping_path = data_dir / "user2vector.json"

        if not self.mapping_path.is_file():
            with self.mapping_path.open("w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)


    def generate_answer(self, query: str, user_id: int) -> str:
        with self.mapping_path.open("r", encoding="utf-8") as f:
            try:
                self.map_user2vecstor = json.load(f)
            except json.JSONDecodeError:
                self.map_user2vecstor = {}

        str_user_id = str(user_id)

        if str_user_id not in self.map_user2vecstor:
            raise ValueError(f"Нет vector_store для user_id={user_id}")
        
        vector_store_id = self.map_user2vecstor[str_user_id]

        thread = self.openai_client.beta.threads.create(
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store_id]
                }
            }
        )

        self.openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )

        run = self.openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
        )

        while True:
            run = self.openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run.status in ("completed", "failed"):
                break
            time.sleep(0.5)

        msgs = self.openai_client.beta.threads.messages.list(thread_id=thread.id)
        for msg in reversed(msgs.data):
            if msg.role == "assistant":
                answer = msg.content[0].text.value
                return answer
            
        return "Ответа не найдено"



