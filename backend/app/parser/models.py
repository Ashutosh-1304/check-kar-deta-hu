from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class RunModel(BaseModel):
    text: str
    font_family: Optional[str] = None
    font_size: Optional[float] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None
    color: Optional[str] = None

class ParagraphModel(BaseModel):
    text: str
    runs: List[RunModel] = Field(default_factory=list)
    style: Optional[str] = None
    alignment: Optional[str] = None
    first_line_indent: Optional[float] = None
    space_after: Optional[float] = None

class HeadingModel(ParagraphModel):
    level: int

class TableModel(BaseModel):
    rows: int
    cols: int
    # Can expand this to hold cells if required for deep validation
    style: Optional[str] = None

class ImageModel(BaseModel):
    width: Optional[float] = None
    height: Optional[float] = None

class PageProperties(BaseModel):
    page_width: Optional[float] = None
    page_height: Optional[float] = None
    margin_top: Optional[float] = None
    margin_bottom: Optional[float] = None
    margin_left: Optional[float] = None
    margin_right: Optional[float] = None

class SectionModel(BaseModel):
    page_properties: PageProperties
    paragraphs: List[ParagraphModel] = Field(default_factory=list)
    tables: List[TableModel] = Field(default_factory=list)
    images: List[ImageModel] = Field(default_factory=list)
    # headers and footers can be added as ParagraphModel lists
    headers: List[ParagraphModel] = Field(default_factory=list)
    footers: List[ParagraphModel] = Field(default_factory=list)

class DocumentMetadata(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    core_properties: dict = Field(default_factory=dict)

class DocumentModel(BaseModel):
    metadata: DocumentMetadata
    sections: List[SectionModel] = Field(default_factory=list)
