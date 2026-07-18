from app.validators.base import BaseValidator, ValidationResult, ValidationIssue
from app.parser.models import DocumentModel, HeadingModel
from app.rules.schemas import DocumentRuleTemplate

class HeadingValidator(BaseValidator):
    def validate(self, doc: DocumentModel, rules: DocumentRuleTemplate) -> ValidationResult:
        result = ValidationResult()
        
        if not rules.headings:
            return result
            
        rule_map = {r.level: r for r in rules.headings}
        
        for sec_idx, section in enumerate(doc.sections):
            for para_idx, para in enumerate(section.paragraphs):
                if isinstance(para, HeadingModel):
                    h_rule = rule_map.get(para.level)
                    if not h_rule:
                        continue # No specific rule for this heading level
                    
                    context = para.text[:50] + '...' if len(para.text) > 50 else para.text
                    
                    # Check Alignment
                    if h_rule.alignment:
                        result.passed_checks += 1
                        if para.alignment != h_rule.alignment:
                            result.passed_checks -= 1
                            result.failed_checks += 1
                            result.issues.append(ValidationIssue(
                                element_type="HeadingAlignment",
                                expected_value=h_rule.alignment,
                                actual_value=str(para.alignment),
                                message=f"Heading level {para.level} has incorrect alignment.",
                                paragraph_index=para.paragraph_index,
                                page_number=para.page_number,
                                context_text=para.text[:60] + '...' if len(para.text) > 60 else para.text
                            ))
                            
                    # Check Font
                    if h_rule.font:
                        allowed_fams = h_rule.font.allowed_families
                        exact_size = h_rule.font.exact_size
                        
                        for run in para.runs:
                            context = run.text.strip()
                            if not context:
                                continue
                            if len(context) > 60:
                                context = context[:60] + '...'

                            if allowed_fams:
                                result.passed_checks += 1
                                if run.font_family not in allowed_fams:
                                    result.passed_checks -= 1
                                    result.failed_checks += 1
                                    result.issues.append(ValidationIssue(
                                        element_type="HeadingFontFamily",
                                        expected_value=f"One of {allowed_fams}",
                                        actual_value=str(run.font_family),
                                        message=f"Heading level {para.level} has invalid font family.",
                                        paragraph_index=para.paragraph_index,
                                        page_number=para.page_number,
                                        context_text=context
                                    ))
                            
                            if exact_size is not None:
                                result.passed_checks += 1
                                if run.font_size != exact_size:
                                    result.passed_checks -= 1
                                    result.failed_checks += 1
                                    result.issues.append(ValidationIssue(
                                        element_type="HeadingFontSize",
                                        expected_value=str(exact_size),
                                        actual_value=str(run.font_size),
                                        message=f"Heading level {para.level} has invalid font size.",
                                        paragraph_index=para.paragraph_index,
                                        page_number=para.page_number,
                                        context_text=context
                                    ))
                                    
        return result
