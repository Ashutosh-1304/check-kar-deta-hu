from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/login")
def login():
    # Stub authentication endpoint for future enterprise features
    return {"access_token": "mock-jwt-token-xyz123", "token_type": "bearer"}
