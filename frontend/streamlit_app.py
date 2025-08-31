from typing import Any, Dict

import requests
import streamlit as st
from dotenv import load_dotenv

import os

load_dotenv()

st.set_page_config(layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL")

USERS = {}

def _post_json(url, json):
    try:
        r = requests.post(url, json=json)
        r.raise_for_status()
        return r.json()
    except requests.HTTPError as e:
        detail = None
        if e.response is not None:
            try:
                detail = e.response.json().get("detail")
            except Exception:
                detail = e.response.text

        msg = f"{e.response.status_code} {e.response.reason}"
        if detail:
            msg += f" | detail: {detail}"
        raise RuntimeError(msg)


def _put_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        r = requests.put(url, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
    except requests.HTTPError as e:
        detail = None
        if e.response is not None:
            try:
                detail = e.response.json().get("detail")
            except Exception:
                detail = e.response.text
        msg = f"{e.response.status_code} {e.response.reason}"
        if detail:
            msg += f" | detail: {detail}"
        raise RuntimeError(msg)
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")
    

def generate_answer(query: str, user_id: int) -> str:
    """
    Generate an answer to the given query by sending a POST request to the backend

    Args:
        query (str): The query to answer
        user_id (int): The id of user

    Returns:
        str: The generated answer
    """
    print(f"{BACKEND_URL}/rag/generate_answer")
    response = _post_json(f"{BACKEND_URL}/rag/generate_answer", json={"query": query, "user_id": user_id})
    answer: Dict[str, Any] = response
    return answer["text"]


def add_text(text: str, user_ids: list[int], filename: str) -> str:
    """
    Upload plain text to RAG storage for specific users.

    Args:
        text (str): text of document for uploading
        user_ids: The ids of users 

    Returns:
        str: The file id
    
    """
    url = f"{BACKEND_URL}/rag/text/upload"
    payload = {"data": text, "user_ids": user_ids, "filename": filename}
    resp = _put_json(url, payload)
    return str(resp["file_id"])

def page_add_text():
    st.header("📜 Добавление текста в RAG")

    if not USERS:
        st.info("Список пользователей пуст. Заполни словарь USERS в коде.")
        return

    selected_users = st.multiselect(
        "Выберите одного или нескольких пользователей:",
        options=list(USERS.keys()),
        default=[],
        key="add_text_user_multiselect",
    )

    filename = st.text_input(
        "Название файла (с расширением):",
        placeholder="document.txt",
        key="add_text_filename",
    )

    text = st.text_area("Введите текст:", height=200, key="add_text_textarea")

    clicked = st.button("Добавить текст", key="btn_add_text_submit")
    if clicked:
        if not text.strip():
            st.warning("Сначала введите текст.")
            return
        if not selected_users:
            st.warning("Выберите хотя бы одного пользователя.")
            return
        if not filename.strip():
            st.warning("Укажите название файла (например, document.txt).")
            return

        # Простая нормализация: если нет точки — добавим .txt
        norm_filename = filename.strip()
        if "." not in norm_filename:
            norm_filename += ".txt"

        try:
            file_id = add_text(
                text,
                user_ids=[USERS[u] for u in selected_users],
                filename=norm_filename,
            )
            st.success("Файл успешно добавлен:")
            st.code(file_id, language="text")
        except Exception as e:
            st.error(f"Ошибка при загрузке текста: {e}")

def page_ask():
    st.header("🧠 Интеллектуальный чат-бот помощник")

    if not USERS:
        st.info("Список пользователей пуст. Заполни словарь USERS в коде.")
        return

    user_names = list(USERS.keys())
    default_index = 0 if user_names else -1

    selected_user = st.selectbox(
        "Выберите пользователя:",
        options=user_names,
        index=default_index,
        key="ask_user_select",
    )

    query = st.text_area("Введите вопрос:", height=200, key="ask_query_textarea")

    clicked = st.button("Сгенерировать ответ", key="btn_generate_answer")
    if clicked:
        if not query.strip():
            st.warning("Сначала введите вопрос.")
            return

        try:
            answer = generate_answer(query, user_id=USERS[selected_user])
            st.success("Ответ успешно сгенерирован:")
            st.code(answer, language="text")
        except Exception as e:
            st.error(f"Ошибка при генерации: {e}")


def main():
    st.set_page_config(page_title="RAG UI", page_icon="🧩", layout="wide")

    st.sidebar.title("Навигация")
    page = st.sidebar.radio(
        "Раздел",
        ["Задать вопрос", "Добавить текст"],
        index=0,
        key="nav_radio",
    )


    if page == "Задать вопрос":
        page_ask()
    else:
        page_add_text()

if __name__ == "__main__":
    main()