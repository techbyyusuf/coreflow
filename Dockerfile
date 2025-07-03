FROM python:3.12-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN apt-get update && apt-get install -y netcat-openbsd


COPY . .


RUN chmod +x scripts/wait-for-it.sh


CMD ["scripts/wait-for-it.sh", "db", "5432", "python", "main.py"]
