FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

COPY . . 

RUN chmod +x scripts/wait-for-it.sh

ENV PYTHONPATH=/app

#CMD ["scripts/wait-for-it.sh", "db", "5432", "python", "app/main.py"]
CMD ["scripts/wait-for-it.sh", "db", "5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

