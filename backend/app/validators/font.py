from app.validators.base import BaseValidator, ValidationResult, ValidationIssue
from app.parser.models import DocumentModel, HeadingModel
from app.rules.schemas import DocumentRuleTemplate

class FontValidator(BaseValidator):
    def validate(self, doc: DocumentModel, rules: DocumentRuleTemplate) -> ValidationResult:
        result = ValidationResult()
        
        if not rules.body_font:
            return result
            
        allowed_families = rules.body_font.allowed_families
        min_size = rules.body_font.min_size
        max_size = rules.body_font.max_size
        
        for sec_idx, section in enumerate(doc.sections):
            for para_idx, para in enumerate(section.paragraphs):
                # Skip headings, they are evaluated by HeadingValidator
                if isinstance(para, HeadingModel):
                    continue
                
                for run_idx, run in enumerate(para.runs):
                    context = para.text[:50] + '...' if len(para.text) > 50 else para.text
                    
                    # Check Family
                    if allowed_families:
                        result.passed_checks += 1
                        if run.font_family not in allowed_families:
                            result.passed_checks -= 1
                            result.failed_checks += 1
                            result.issues.append(ValidationIssue(
                                element_type="FontFamily",
                                expected_value=f"One of {allowed_families}",
                                actual_value=str(run.font_family),
                                message=f"Invalid font family in Section {sec_idx+1}, Paragraph {para.paragraph_index}.",
                                paragraph_index=para.paragraph_index,
                                context_text=context
                            ))
                    
                    # Check Size
                    if min_size is not None or max_size is not None:
                        result.passed_checks += 1
                        valid = True
                        if min_size is not None and (run.font_size is None or run.font_size < min_size):
                            valid = False
                        if max_size is not None and (run.font_size is None or run.font_size > max_size):
                            valid = False
                            
                        if not valid:
                            result.passed_checks -= 1
                            result.failed_checks += 1
                            result.issues.append(ValidationIssue(
                                element_type="FontSize",
                                expected_value=f"Between {min_size} and {max_size}",
                                actual_value=str(run.font_size),
                                message=f"Invalid font size in Section {sec_idx+1}, Paragraph {para.paragraph_index}.",
                                paragraph_index=para.paragraph_index,
                                context_text=context
                            ))
                            
        return result
