FROM python:3.10

WORKDIR /app

COPY requirements.txt .

COPY /rag /app/rag

RUN pip install --no-cache-dir -r requirements.txt
