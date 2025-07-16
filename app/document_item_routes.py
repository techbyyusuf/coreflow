from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.document_item_service import DocumentItemService
from schemas.document_item_schemas import DocumentItemCreateSchema, DocumentItemUpdateSchema
from app.dependencies import get_db

router = APIRouter(prefix="/document-items", tags=["document-items"])


@router.get("/")
def get_all_document_items(db: Session = Depends(get_db)):
    """Retrieve all document items"""
    service = DocumentItemService(db)
    try:
        return service.get_all_items()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_document_item(payload: DocumentItemCreateSchema, db: Session = Depends(get_db)):
    """Create a new document item"""
    service = DocumentItemService(db)
    try:
        service.create_document_item(
            document_id=payload.document_id,
            product_id=payload.product_id,
            quantity=payload.quantity,
            unit_price=payload.unit_price
        )
        return {"message": "Document item created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}")
def update_document_item(item_id: int, payload: DocumentItemUpdateSchema, db: Session = Depends(get_db)):
    """Update document item (quantity & unit price)"""
    service = DocumentItemService(db)
    try:
        service.update_document_item(
            item_id=item_id,
            new_quantity=payload.new_quantity,
            new_unit_price=payload.new_unit_price
        )
        return {"message": "Document item updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}")
def delete_document_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a document item"""
    service = DocumentItemService(db)
    try:
        service.delete_document_item(item_id)
        return {"message": "Document item deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
