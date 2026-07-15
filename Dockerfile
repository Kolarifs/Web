# 1. Берем официальный чистый образ Python на Linux
FROM python:3.11-slim

# 2. Создаем рабочую папку приложения внутри сервера
WORKDIR /app

# 3. Копируем список библиотек и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем основной код бэкенда в сервер
COPY main.py .

# 5. Открываем порт 8000 для приема интернет-запросов
EXPOSE 8000

# 6. Команда для запуска сервера через высокопроизводительный uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
