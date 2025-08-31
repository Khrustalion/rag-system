from typing import Any, Dict

import requests
import streamlit as st
from dotenv import load_dotenv

import os

load_dotenv()

st.set_page_config(layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL")

USERS = {}


def generate_answer(query: str, user_id: int) -> str:
    """
    Generate an answer to the given query by sending a POST request to the backend

    Args:
        query (str): The query to answer

    Returns:
        str: The generated answer
    """
    print(f"{BACKEND_URL}/rag/generate_answer")
    response = requests.post(f"{BACKEND_URL}/rag/generate_answer", json={"query": query, "user_id": user_id})
    response.raise_for_status()
    answer: Dict[str, Any] = response.json()
    return answer["text"]

def main_page():
    st.title("🧠 Интеллектуальный чат-бот помощник")

    selected_user = st.selectbox(
        "Выберите пользователя:",
        options=USERS,
        index=0,
        key="user_select",
    )

    query = st.text_area("Введите вопрос:", height=175)

    if st.button("Сгенерировать ответ"):
        if not query.strip():
            st.warning("Сначала введите вопрос.")
            return

        try:
            # Передаём user_id в бэкенд
            answer = generate_answer(query, user_id=USERS[selected_user])

            text_generation_task_status_placeholder = st.empty()
            text_generation_task_status_placeholder.success("Ответ успешно сгенерирован:")

            generated_text_placeholder = st.empty()
            generated_text_placeholder.code(answer, language="text")

        except Exception as e:
            st.error(f"Ошибка при генерации: {str(e)}")


if __name__ == "__main__":
    main_page()