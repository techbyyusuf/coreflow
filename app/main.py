print("Starte main.py")
from fastapi import FastAPI

from app.user_routes import router as user_router
from app.init_db import init_db

print("FASTAPI importiert")

app = FastAPI()

print("FASTAPI-Objekt erstellt")

# Optional:
#init_db()

app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Hello from FastAPI + SQLAlchemy!"}


# http://localhost:8000/docs
# uvicorn app.api:app --reload --host 127.0.0.1 --port 8000