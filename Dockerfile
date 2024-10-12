FROM python:3.9-slim

# еобходимые зависимости
RUN apt-get update && apt-get install -y \
    python3-opencv \
    python3-tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# рабочая директория
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY . .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# запуск приложения
CMD ["python", "create_video_meeting_screen.py"]
