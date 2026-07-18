from app.validators.base import BaseValidator, ValidationResult, ValidationIssue
from app.parser.models import DocumentModel
from app.rules.schemas import DocumentRuleTemplate

class MarginValidator(BaseValidator):
    def validate(self, doc: DocumentModel, rules: DocumentRuleTemplate) -> ValidationResult:
        result = ValidationResult()
        
        if not rules.margins:
            return result
        
        tolerance = rules.margins.tolerance
        
        for idx, section in enumerate(doc.sections):
            props = section.page_properties
            
            # Helper to check margin
            def check_margin(name: str, actual: float, expected: float):
                result.passed_checks += 1
                if actual is None or abs(actual - expected) > tolerance:
                    result.passed_checks -= 1
                    result.failed_checks += 1
                    result.issues.append(ValidationIssue(
                        element_type="Margin",
                        expected_value=str(expected),
                        actual_value=str(actual),
                        message=f"Section {idx+1} {name} margin out of bounds."
                    ))
            
            if rules.margins.top is not None:
                check_margin("top", props.margin_top, rules.margins.top)
            if rules.margins.bottom is not None:
                check_margin("bottom", props.margin_bottom, rules.margins.bottom)
            if rules.margins.left is not None:
                check_margin("left", props.margin_left, rules.margins.left)
            if rules.margins.right is not None:
                check_margin("right", props.margin_right, rules.margins.right)
                
        return result
