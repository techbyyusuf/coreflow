from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.product_service import ProductService
from app.database.session import get_db
from security.dependencies import require_admin, require_self_or_admin, require_employee
from schemas.product_schemas import (
    ProductCreate,
    ProductUpdateName,
    ProductUpdatePrice,
    ProductUpdateUnit,
    ProductUpdateDescription,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def get_all_products(
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    try:
        service = ProductService(db)
        return service.get_all_products()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_product(
        payload: ProductCreate,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    try:
        service = ProductService(db)
        service.create_product(
            name=payload.name,
            unit_price=payload.unit_price,
            unit=payload.unit,
            description=payload.description,
        )
        return {"message": "Product created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}/name")
def update_product_name(
        product_id: int,
        payload: ProductUpdateName,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    try:
        service = ProductService(db)
        service.update_product_name(product_id, payload.new_name)
        return {"message": "Product name updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}/price")
def update_product_price(
        product_id: int,
        payload: ProductUpdatePrice,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    try:
        service = ProductService(db)
        service.update_product_price(product_id, payload.new_price)
        return {"message": "Product price updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}/unit")
def update_product_unit(
        product_id: int,
        payload: ProductUpdateUnit,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    try:
        service = ProductService(db)
        service.update_product_unit(product_id, payload.new_unit)
        return {"message": "Product unit updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}/description")
def update_product_description(
        product_id: int,
        payload: ProductUpdateDescription,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    try:
        service = ProductService(db)
        service.update_product_description(product_id, payload.new_description)
        return {"message": "Product description updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}")
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    try:
        service = ProductService(db)
        service.delete_product(product_id)
        return {"message": "Product deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
