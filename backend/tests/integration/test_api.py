import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.db.models.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_api.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_api.db"):
        try:
            os.remove("./test_api.db")
        except PermissionError:
            pass
            
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_auth_login():
    response = client.post("/api/v1/auth/login")
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_full_validation_workflow():
    import uuid
    unique_name = f"API Test Rule {uuid.uuid4()}"
    rule_payload = {
        "name": unique_name,
        "description": "Rule for testing API",
        "margins": {
            "top": 1.0,
            "bottom": 1.0,
            "left": 1.0,
            "right": 1.0
        }
    }
    response = client.post("/api/v1/rules", json=rule_payload)
    assert response.status_code == 201
    rule_id = response.json()["id"]
    
    # 2. List rules
    response = client.get("/api/v1/rules")
    assert response.status_code == 200
    assert len(response.json()) > 0
    
    # 3. Upload a document
    # Using the generated sample document from phase 3
    sample_doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "examples", "sample_document.docx"))
    
    with open(sample_doc_path, "rb") as f:
        response = client.post("/api/v1/upload", files={"file": ("sample_document.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")})
        
    assert response.status_code == 200
    doc_id = response.json()["document_id"]
    
    # 4. Trigger validation
    val_payload = {
        "document_id": doc_id,
        "rule_template_id": int(rule_id)
    }
    response = client.post("/api/v1/validate", json=val_payload)
    assert response.status_code == 202
    report_id = response.json()["report_id"]
    
    # 5. Get report
    response = client.get(f"/api/v1/reports/{report_id}")
    assert response.status_code == 200
    report_data = response.json()
    assert report_data["status"] == "COMPLETED"
    assert "overall_score" in report_data
    assert "metrics" in report_data
