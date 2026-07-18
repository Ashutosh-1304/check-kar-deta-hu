from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.document import ValidationReport
from app.report.html_generator import generate_html_report

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
        "issues": report.issues  # Keeping for backwards compatibility
    }

@router.get("/reports/{report_id}/issues")
def get_report_issues(
    report_id: str, 
    skip: int = Query(0, ge=0), 
    limit: int = Query(50, ge=1, le=1000), 
    db: Session = Depends(get_db)
):
    report = db.query(ValidationReport).filter(ValidationReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    # In-memory pagination since issues are stored as a JSON array
    issues = report.issues or []
    paginated_issues = issues[skip : skip + limit]
    
    return {
        "total": len(issues),
        "skip": skip,
        "limit": limit,
        "data": paginated_issues
    }

@router.get("/reports/{report_id}/html", response_class=HTMLResponse)
def get_report_html(report_id: str, db: Session = Depends(get_db)):
    report = db.query(ValidationReport).filter(ValidationReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    html_content = generate_html_report(report)
    return HTMLResponse(content=html_content)
