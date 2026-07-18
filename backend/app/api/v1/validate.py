import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models.document import UploadedDocument, ValidationReport
from app.db.models.rule_template import RuleTemplate
from app.rules.schemas import DocumentRuleTemplate
from app.parser.docx_parser import DocxParser
from app.validators.pipeline import ValidationPipeline
from app.validators.margin import MarginValidator
from app.validators.font import FontValidator
from app.validators.heading import HeadingValidator

router = APIRouter()

class ValidateRequest(BaseModel):
    document_id: str
    rule_template_id: int

class ValidateResponse(BaseModel):
    report_id: str
    status: str

@router.post("/validate", response_model=ValidateResponse, status_code=202)
def validate_document(req: ValidateRequest, db: Session = Depends(get_db)):
    # 1. Fetch document and rule
    doc = db.query(UploadedDocument).filter(UploadedDocument.id == req.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    rule_tpl = db.query(RuleTemplate).filter(RuleTemplate.id == req.rule_template_id).first()
    if not rule_tpl:
        raise HTTPException(status_code=404, detail="Rule template not found")
        
    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="File missing on disk")
        
    # 2. Parse Document
    parser = DocxParser()
    try:
        doc_model = parser.parse(doc.file_path)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse document: {str(e)}")
        
    # 3. Load Rule config into Pydantic
    rule_schema = DocumentRuleTemplate(**rule_tpl.rule_config)
    
    # 4. Validate
    from app.plugins.manager import PluginManager
    plugin_manager = PluginManager()
    plugin_manager.discover_and_load()
    
    validators = [
        MarginValidator(),
        FontValidator(),
        HeadingValidator()
    ]
    validators.extend(plugin_manager.get_plugin_instances())
    
    pipeline = ValidationPipeline(validators)
    
    report_data = pipeline.evaluate(doc_model, rule_schema)
    
    # 5. Save Report
    metrics = {
        "passed_checks": report_data["passed_checks"],
        "failed_checks": report_data["failed_checks"],
        "total_checks": report_data["total_checks"]
    }
    
    report = ValidationReport(
        document_id=doc.id,
        rule_template_id=str(rule_tpl.id),
        status="COMPLETED",
        overall_score=report_data["score"],
        metrics=metrics,
        issues=report_data["issues"]
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return ValidateResponse(report_id=report.id, status="VALIDATING")
