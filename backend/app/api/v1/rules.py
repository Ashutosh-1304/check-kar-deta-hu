from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.rule_template import RuleTemplate
from app.rules.schemas import DocumentRuleTemplate

router = APIRouter()

@router.get("/rules", response_model=List[dict])
def list_rules(db: Session = Depends(get_db)):
    rules = db.query(RuleTemplate).filter(RuleTemplate.is_active == True).all()
    return [{"id": str(r.id), "name": r.name, "version": r.version} for r in rules]

@router.post("/rules", status_code=201)
def create_rule(rule: DocumentRuleTemplate, db: Session = Depends(get_db)):
    # Simple creation, defaults to version 1
    db_rule = RuleTemplate(
        name=rule.name,
        description=rule.description,
        version=1,
        rule_config=rule.model_dump()
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return {"id": str(db_rule.id), "name": db_rule.name, "version": db_rule.version}

@router.put("/rules/{rule_id}")
def update_rule(rule_id: int, rule: DocumentRuleTemplate, db: Session = Depends(get_db)):
    existing = db.query(RuleTemplate).filter(RuleTemplate.id == rule_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Rule not found")
        
    # Bump version and append row
    new_rule = RuleTemplate(
        name=existing.name,
        description=rule.description,
        version=existing.version + 1,
        rule_config=rule.model_dump()
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return {"id": str(new_rule.id), "name": new_rule.name, "version": new_rule.version}

@router.delete("/rules/{rule_id}", status_code=204)
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    existing = db.query(RuleTemplate).filter(RuleTemplate.id == rule_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Rule not found")
        
    existing.is_active = False
    db.commit()
    return None
