import pytest
from app.parser.models import (
    DocumentModel, DocumentMetadata, SectionModel, PageProperties,
    ParagraphModel, RunModel, HeadingModel
)
from app.rules.schemas import DocumentRuleTemplate, MarginRule, FontRule, HeadingRule
from app.validators.margin import MarginValidator
from app.validators.font import FontValidator
from app.validators.heading import HeadingValidator
from app.validators.pipeline import ValidationPipeline

def test_margin_validator():
    doc = DocumentModel(
        metadata=DocumentMetadata(title="Test"),
        sections=[
            SectionModel(
                page_properties=PageProperties(margin_top=1.0, margin_bottom=1.5, margin_left=1.25, margin_right=1.25)
            )
        ]
    )
    
    # Valid rule
    rules = DocumentRuleTemplate(
        name="Test",
        margins=MarginRule(top=1.0, bottom=1.5, left=1.25, right=1.25, tolerance=0.01)
    )
    
    val = MarginValidator()
    res = val.validate(doc, rules)
    assert res.failed_checks == 0
    assert res.passed_checks == 4
    
    # Invalid rule
    rules_invalid = DocumentRuleTemplate(
        name="Test",
        margins=MarginRule(top=2.0)
    )
    res2 = val.validate(doc, rules_invalid)
    assert res2.failed_checks == 1
    assert res2.passed_checks == 0
    assert "top" in res2.issues[0].message.lower()

def test_font_validator():
    doc = DocumentModel(
        metadata=DocumentMetadata(),
        sections=[
            SectionModel(
                page_properties=PageProperties(),
                paragraphs=[
                    ParagraphModel(
                        text="Test para",
                        runs=[
                            RunModel(text="Test para", font_family="Arial", font_size=12.0),
                            RunModel(text="Invalid font", font_family="Comic Sans", font_size=14.0)
                        ]
                    )
                ]
            )
        ]
    )
    
    rules = DocumentRuleTemplate(
        name="Test",
        body_font=FontRule(allowed_families=["Arial"], max_size=12.0)
    )
    
    val = FontValidator()
    res = val.validate(doc, rules)
    # Paragraph 1, Run 1: valid family, valid size (2 passed)
    # Paragraph 1, Run 2: invalid family, invalid size (2 failed)
    assert res.failed_checks == 2
    assert res.passed_checks == 2
    assert len(res.issues) == 2

def test_heading_validator():
    doc = DocumentModel(
        metadata=DocumentMetadata(),
        sections=[
            SectionModel(
                page_properties=PageProperties(),
                paragraphs=[
                    HeadingModel(
                        text="Heading 1", level=1, alignment="CENTER",
                        runs=[RunModel(text="Heading 1", font_family="Arial", font_size=16.0)]
                    )
                ]
            )
        ]
    )
    
    rules = DocumentRuleTemplate(
        name="Test",
        headings=[
            HeadingRule(level=1, alignment="CENTER", font=FontRule(allowed_families=["Arial"], exact_size=16.0))
        ]
    )
    
    val = HeadingValidator()
    res = val.validate(doc, rules)
    # 1 alignment check + 1 font family check + 1 exact size check = 3 passes
    assert res.failed_checks == 0
    assert res.passed_checks == 3

def test_pipeline():
    doc = DocumentModel(
        metadata=DocumentMetadata(),
        sections=[
            SectionModel(
                page_properties=PageProperties(margin_top=1.0), # margin pass
                paragraphs=[
                    ParagraphModel(
                        text="Body",
                        runs=[RunModel(text="Body", font_family="Comic Sans", font_size=10.0)] # font fail
                    )
                ]
            )
        ]
    )
    
    rules = DocumentRuleTemplate(
        name="Test",
        margins=MarginRule(top=1.0),
        body_font=FontRule(allowed_families=["Arial"])
    )
    
    pipeline = ValidationPipeline(validators=[
        MarginValidator(),
        FontValidator(),
        HeadingValidator()
    ])
    
    report = pipeline.evaluate(doc, rules)
    
    assert report["total_checks"] == 2
    assert report["passed_checks"] == 1
    assert report["failed_checks"] == 1
    assert report["score"] == 50.0
    assert len(report["issues"]) == 1
