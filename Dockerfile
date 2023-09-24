# Используйте официальный образ Python
FROM python:3.8

# Установка зависимостей
RUN pip install -r requirements.txt

# Копирование кода приложения в контейнер
COPY . /app
WORKDIR /app

# Запуск вашего скрипта при старте контейнера
CMD ["python", "parser.py"]
