from app.validators.base import BaseValidator, ValidationResult
from app.parser.models import DocumentModel
from app.rules.schemas import DocumentRuleTemplate

class TableValidator(BaseValidator):
    def validate(self, doc: DocumentModel, rules: DocumentRuleTemplate) -> ValidationResult:
        # Passthrough for now, can implement table style rules here
        return ValidationResult()
