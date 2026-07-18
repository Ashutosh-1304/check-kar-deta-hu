import os
import pytest
from app.parser.docx_parser import DocxParser
from app.parser.models import HeadingModel

def test_docx_parser():
    # Make sure we run from the backend directory root where examples/ is present
    sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "examples", "sample_document.docx")
    assert os.path.exists(sample_path), f"Run generate_sample.py first. Could not find {sample_path}"
    
    parser = DocxParser()
    doc_model = parser.parse(sample_path)
    
    # Verify Metadata
    assert doc_model.metadata.title == "Sample Compliance Document"
    assert doc_model.metadata.author == "Test Author"
    
    # Verify Sections / Margins
    assert len(doc_model.sections) >= 1
    section = doc_model.sections[0]
    assert section.page_properties.margin_top == 1.0
    assert section.page_properties.margin_left == 1.25
    
    # Verify Heading
    assert len(section.paragraphs) >= 2 # 1 heading + 1 paragraph
    heading = section.paragraphs[0]
    assert heading.text == "Main Title"
    assert isinstance(heading, HeadingModel)
    assert heading.level == 1
    
    # Verify Paragraph & Runs
    para = section.paragraphs[1]
    assert "bold text" in para.text
    # find the bold run
    bold_run = next((r for r in para.runs if r.bold), None)
    assert bold_run is not None
    assert bold_run.text == "bold text"
    
    # Verify Table
    assert len(section.tables) == 1
    table = section.tables[0]
    assert table.rows == 2
    assert table.cols == 2
