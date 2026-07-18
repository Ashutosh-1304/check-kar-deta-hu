from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.config import settings
from app.core.logging import logger
from app.db.session import get_db
from app.api.v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for the Document Compliance Checker",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Document Compliance Checker backend...")

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Check database connectivity
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Database connection failed during health check: {str(e)}")
        return {"status": "error", "database": "disconnected", "detail": str(e)}

app.include_router(api_router, prefix="/api/v1")
