from typing import List, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from app.parser.models import DocumentModel
from app.rules.schemas import DocumentRuleTemplate

class ValidationIssue(BaseModel):
    element_type: str
    expected_value: str
    actual_value: str
    message: str
    severity: str = "ERROR" # e.g. ERROR, WARNING

class ValidationResult(BaseModel):
    passed_checks: int = 0
    failed_checks: int = 0
    issues: List[ValidationIssue] = Field(default_factory=list)

class BaseValidator(ABC):
    """
    Abstract Base Class for all compliance validators.
    """
    @abstractmethod
    def validate(self, doc: DocumentModel, rules: DocumentRuleTemplate) -> ValidationResult:
        pass
