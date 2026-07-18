from typing import List, Dict, Any
from app.parser.models import DocumentModel
from app.rules.schemas import DocumentRuleTemplate
from app.validators.base import BaseValidator

class ValidationPipeline:
    def __init__(self, validators: List[BaseValidator]):
        self.validators = validators
        
    def evaluate(self, doc: DocumentModel, rules: DocumentRuleTemplate) -> Dict[str, Any]:
        total_passed = 0
        total_failed = 0
        all_issues = []
        
        for validator in self.validators:
            result = validator.validate(doc, rules)
            total_passed += result.passed_checks
            total_failed += result.failed_checks
            all_issues.extend(result.issues)
            
        total_checks = total_passed + total_failed
        score = 0.0
        if total_checks > 0:
            score = (total_passed / total_checks) * 100.0
            
        # Optional: return a structured dictionary or a custom ReportModel
        return {
            "score": round(score, 2),
            "passed_checks": total_passed,
            "failed_checks": total_failed,
            "total_checks": total_checks,
            "issues": [issue.model_dump() for issue in all_issues]
        }
