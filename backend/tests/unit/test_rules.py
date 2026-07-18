import os
import pytest
from app.rules.schemas import DocumentRuleTemplate, MarginRule
from app.rules.loader import RuleLoader
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models.base import Base
from app.db.models.rule_template import RuleTemplate
import sqlalchemy.exc

# Test Data setup
def test_rule_schema_validation():
    # Valid data
    valid_data = {
        "name": "Test Rule",
        "margins": {
            "top": 1.0,
            "bottom": 1.0,
            "left": 1.25,
            "right": 1.25
        }
    }
    rule = DocumentRuleTemplate(**valid_data)
    assert rule.name == "Test Rule"
    assert rule.margins.top == 1.0
    
    # Invalid data (string instead of float)
    invalid_data = {
        "name": "Invalid Rule",
        "margins": {
            "top": "not a number"
        }
    }
    with pytest.raises(ValidationError):
        DocumentRuleTemplate(**invalid_data)

def test_yaml_loader():
    sample_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "examples", "sample_rules.yaml"))
    
    rule = RuleLoader.load_from_yaml(sample_path)
    
    assert rule.name == "Standard Corporate Policy"
    assert rule.margins.top == 1.0
    assert "Arial" in rule.body_font.allowed_families
    
    # Check heading rule
    assert len(rule.headings) == 2
    h1 = rule.headings[0]
    assert h1.level == 1
    assert h1.font.exact_size == 16.0

# Database Integration Test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rules.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("./test_rules.db"):
            try:
                os.remove("./test_rules.db")
            except PermissionError:
                pass

def test_database_persistence(db_session):
    new_rule = RuleTemplate(
        name="Test DB Policy",
        version=1,
        rule_config={"margins": {"top": 1.0}}
    )
    db_session.add(new_rule)
    db_session.commit()
    db_session.refresh(new_rule)
    
    assert new_rule.id is not None
    assert new_rule.name == "Test DB Policy"
    assert new_rule.version == 1
    
    # Test unique constraint on name/version
    duplicate_rule = RuleTemplate(
        name="Test DB Policy",
        version=1,
        rule_config={}
    )
    db_session.add(duplicate_rule)
    
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db_session.commit()
    
    db_session.rollback()

    # Test version incrementing
    v2_rule = RuleTemplate(
        name="Test DB Policy",
        version=2,
        rule_config={}
    )
    db_session.add(v2_rule)
    db_session.commit()
    assert v2_rule.id is not None
