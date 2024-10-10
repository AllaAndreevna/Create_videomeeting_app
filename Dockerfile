FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1

RUN pip install --no-cache-dir numpy==1.22.3

RUN pip install --no-cache-dir opencv-python --force-reinstall

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENV NAME=World

CMD ["python", "video_meeting_screen.py"]