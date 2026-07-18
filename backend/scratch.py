import docx

doc = docx.Document("tests/examples/sample_document.docx")

page_num = 1
for i, para in enumerate(doc.paragraphs):
    # Check for lastRenderedPageBreak in the paragraph XML
    if '<w:lastRenderedPageBreak' in para._p.xml:
        page_num += 1
        print(f"Page break detected before Paragraph {i+1}. Now on Page {page_num}")

print(f"Total Pages detected: {page_num}")
