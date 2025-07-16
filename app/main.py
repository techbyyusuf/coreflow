from fastapi import FastAPI

from app.user_routes import router as user_router
from app.customer_routes import router as customer_router
from app.product_routes import router as product_router
from app.document_routes import router as document_router
from app.document_item_routes import router as document_item_router
from app.init_db import init_db

app = FastAPI()

init_db()

app.include_router(user_router)
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(document_router)
app.include_router(document_item_router)


@app.get("/")
def root():
    return {"message": "Hello from FastAPI + SQLAlchemy!"}



# docker-compose up --build      -- build für neuen Code
# http://localhost:8000/docs
# uvicorn app.api:app --reload --host 127.0.0.1 --port 8000