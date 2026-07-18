from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.document import ValidationReport

router = APIRouter()

@router.get("/reports/{report_id}")
def get_report(report_id: str, db: Session = Depends(get_db)):
    report = db.query(ValidationReport).filter(ValidationReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    return {
        "report_id": str(report.id),
        "status": report.status,
        "overall_score": report.overall_score,
        "metrics": report.metrics,
        "issues": report.issues
    }
