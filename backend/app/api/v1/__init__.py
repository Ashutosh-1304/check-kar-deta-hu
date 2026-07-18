from fastapi import APIRouter
from app.api.v1.upload import router as upload_router
from app.api.v1.rules import router as rules_router
from app.api.v1.validate import router as validate_router
from app.api.v1.reports import router as reports_router
from app.api.v1.auth import router as auth_router

api_router = APIRouter()
api_router.include_router(upload_router, tags=["Upload"])
api_router.include_router(rules_router, tags=["Rules"])
api_router.include_router(validate_router, tags=["Validation"])
api_router.include_router(reports_router, tags=["Reports"])
api_router.include_router(auth_router, tags=["Authentication"])
