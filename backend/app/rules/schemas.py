from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class MarginRule(BaseModel):
    top: Optional[float] = None
    bottom: Optional[float] = None
    left: Optional[float] = None
    right: Optional[float] = None
    tolerance: float = Field(default=0.01, description="Acceptable deviation in inches")

class FontRule(BaseModel):
    allowed_families: List[str] = Field(default_factory=list)
    min_size: Optional[float] = None
    max_size: Optional[float] = None
    exact_size: Optional[float] = None

class HeadingRule(BaseModel):
    level: int
    font: FontRule
    alignment: Optional[str] = None

class DocumentRuleTemplate(BaseModel):
    name: str
    description: Optional[str] = None
    margins: Optional[MarginRule] = None
    body_font: Optional[FontRule] = None
    headings: List[HeadingRule] = Field(default_factory=list)
    
    # Allows adding future rules without breaking the schema immediately
    model_config = {"extra": "ignore"}
