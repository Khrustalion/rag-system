from openai import OpenAI
from tempfile import NamedTemporaryFile

from io import BytesIO

from pathlib import Path

import json


class RepositoryAA:
    def __init__(self, openai_client: OpenAI) -> None:
        self.openai_client = openai_client

        base_dir = Path(__file__).resolve().parent.parent.parent
        data_dir = base_dir / "data"
        self.mapping_path = data_dir / "user2vector.json"

        if not self.mapping_path.is_file():
            with self.mapping_path.open("w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)



    def create_vector_store(self) -> str:
        return self.openai_client.vector_stores.create().id
    

    def save(self, data: str, filename: str, user_ids: list[int]) -> str:
        with self.mapping_path.open("r", encoding="utf-8") as f:
            try:
                self.map_user2vecstor = json.load(f)
            except json.JSONDecodeError:
                self.map_user2vecstor = {}
                
        buf = BytesIO(data.encode("utf-8"))
        file_id = self.openai_client.files.create(file=(filename, buf), purpose="assistants").id

        updated = False

        for user_id in user_ids:
            user_id = str(user_id)
            if user_id in self.map_user2vecstor:
                try:
                    self.openai_client.vector_stores.retrieve(self.map_user2vecstor[user_id])
                except:
                    self.map_user2vecstor[user_id] = self.create_vector_store()

                    updated = True
            else:
                self.map_user2vecstor[user_id] = self.create_vector_store()

                updated = True

            vs_id = self.map_user2vecstor[user_id]

            try:
                self.openai_client.vector_stores.file_batches.create_and_poll(
                    vector_store_id=vs_id,
                    file_ids=[file_id],
                )
            except Exception as e:
                raise RuntimeError(f"Failed to attach file to vector store for user {user_id}: {e}") from e

        if updated:
            with self.mapping_path.open("w+", encoding="utf-8") as f:
                json.dump(self.map_user2vecstor, f)

        return file_id