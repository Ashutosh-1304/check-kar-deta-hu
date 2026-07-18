import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.document import UploadedDocument
from pydantic import BaseModel

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    doc = UploadedDocument(
        filename=file.filename,
        file_path=file_path,
        status="UPLOADED"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    return UploadResponse(
        document_id=doc.id,
        filename=doc.filename,
        status=doc.status
    )
