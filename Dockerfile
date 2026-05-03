# 1. Берем базовый образ: легкий Linux (Alpine) с уже установленным Python 3
FROM python:3.12-alpine

# 2. Создаем рабочую папку внутри контейнера
WORKDIR /app

# Драйвер для PostgreSQL
RUN pip install psycopg2-binary

# 3. Копируем наш код бэкенда с ноутбука внутрь контейнера
COPY backend/main.py /app/main.py

# 4. Говорим, какой порт будет слушать наше приложение
EXPOSE 8080

# 5. Команда, которая выполнится при старте контейнера
CMD ["python", "main.py"]