import datetime
import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from app.db.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"
    
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, default="UPLOADED") # UPLOADED, VALIDATING, VALIDATED, FAILED
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

class ValidationReport(Base):
    __tablename__ = "validation_reports"
    
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    document_id = Column(String, ForeignKey("uploaded_documents.id"), nullable=False)
    rule_template_id = Column(String, nullable=False)
    status = Column(String, default="COMPLETED")
    overall_score = Column(Float, nullable=False)
    metrics = Column(JSON, nullable=False)
    issues = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
