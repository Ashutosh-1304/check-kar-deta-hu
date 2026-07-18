from app.validators.base import BaseValidator, ValidationResult
from app.parser.models import DocumentModel
from app.rules.schemas import DocumentRuleTemplate

class ParagraphValidator(BaseValidator):
    def validate(self, doc: DocumentModel, rules: DocumentRuleTemplate) -> ValidationResult:
        # Passthrough for now, can implement paragraph spacing/indentation rules here
        return ValidationResult()
