from fastapi import FastAPI

from app.auth_routes import router as auth_router

from app.user_routes import router as user_router
from app.customer_routes import router as customer_router
from app.product_routes import router as product_router

from app.order_routes import router as order_router
from app.order_item_routes import router as order_item_router

from app.quotation_routes import router as quotation_router
from app.quotation_item_routes import router as quotation_item_router

from app.invoice_routes import router as invoice_router
from app.invoice_item_routes import router as invoice_item_router

from app.init_db import init_db

app = FastAPI()

init_db()

app.include_router(auth_router)

app.include_router(user_router)
app.include_router(customer_router)
app.include_router(product_router)

app.include_router(order_router)
app.include_router(order_item_router)

app.include_router(quotation_router)
app.include_router(quotation_item_router)

app.include_router(invoice_router)
app.include_router(invoice_item_router)


@app.get("/")
def root():
    return {"message": "Hello from FastAPI + SQLAlchemy!"}




# docker-compose up --build      -- build für neuen Code
# http://localhost:8001/docs
# uvicorn app.api:app --reload --host 127.0.0.1 --port 8000