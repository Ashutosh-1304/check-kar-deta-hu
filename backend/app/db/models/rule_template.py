import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint, JSON

from app.db.models.base import Base

class RuleTemplate(Base):
    __tablename__ = "rule_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    description = Column(String, nullable=True)
    
    # Store the actual rule configuration as JSON
    rule_config = Column(JSON, nullable=False)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    __table_args__ = (
        UniqueConstraint('name', 'version', name='uq_rule_template_name_version'),
    )
