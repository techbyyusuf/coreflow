from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.document_service import DocumentService
from schemas.document_schemas import DocumentCreateSchema, DocumentUpdateStatusSchema
from app.dependencies import get_db

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/")
def get_all_documents(db: Session = Depends(get_db)):
    """Retrieve all documents"""
    service = DocumentService(db)
    try:
        return service.get_all_documents()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_document(payload: DocumentCreateSchema, db: Session = Depends(get_db)):
    """Create a new document"""
    service = DocumentService(db)
    try:
        service.create_document(
            document_type=payload.document_type,
            customer_id=payload.customer_id,
            user_id=payload.user_id,
            issue_date=payload.issue_date,
            due_date=payload.due_date,
            delivery_date=payload.delivery_date,
            invoice_number=payload.invoice_number,
            status=payload.status,
            reference=payload.reference,
            notes=payload.notes
        )
        return {"message": "Document created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{document_id}/status")
def update_document_status(document_id: int, payload: DocumentUpdateStatusSchema, db: Session = Depends(get_db)):
    """Update document status"""
    service = DocumentService(db)
    try:
        service.update_document_status(document_id, payload.new_status)
        return {"message": "Document status updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document"""
    service = DocumentService(db)
    try:
        service.delete_document(document_id)
        return {"message": "Document deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
