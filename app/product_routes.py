from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.product_service import ProductService
from app.dependencies import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    try:
        service = ProductService(db)
        return service.get_all_products()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_product(
    user_id: int,
    name: str,
    unit_price: float,
    unit: int,
    description: str = None,
    db: Session = Depends(get_db)
):
    try:
        service = ProductService(db)
        service.create_product(user_id, name, unit_price, unit, description)
        return {"message": "Product created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}/name")
def update_product_name(product_id: int, new_name: str, db: Session = Depends(get_db)):
    try:
        service = ProductService(db)
        service.update_product_name(product_id, new_name)
        return {"message": "Product name updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}/price")
def update_product_price(product_id: int, new_price: float, db: Session = Depends(get_db)):
    try:
        service = ProductService(db)
        service.update_product_price(product_id, new_price)
        return {"message": "Product price updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}/unit")
def update_product_unit(product_id: int, new_unit: int, db: Session = Depends(get_db)):
    try:
        service = ProductService(db)
        service.update_product_unit(product_id, new_unit)
        return {"message": "Product unit updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}/description")
def update_product_description(product_id: int, new_description: str, db: Session = Depends(get_db)):
    try:
        service = ProductService(db)
        service.update_product_description(product_id, new_description)
        return {"message": "Product description updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        service = ProductService(db)
        service.delete_product(product_id)
        return {"message": "Product deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
