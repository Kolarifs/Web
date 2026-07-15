# 1. Легковесный базовый образ Python
FROM python:3.11-slim

# 2. Установка рабочей папки внутри контейнера
WORKDIR /app

# 3. Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копирование исходного кода сервера
COPY main.py .

# 5. КРИТИЧЕСКИЙ СДВИГ: Запуск Uvicorn на динамическом порту $PORT, который требует Koyeb/HuggingFace
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
