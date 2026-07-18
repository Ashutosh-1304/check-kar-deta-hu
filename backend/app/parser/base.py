from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path
from io import BytesIO

from app.parser.models import DocumentModel

class BaseParser(ABC):
    """
    Abstract Base Class for Document Parsers.
    All future parsers (e.g. PDFParser) must implement this interface
    so that the Validation Engine can process them uniformly.
    """
    
    @abstractmethod
    def parse(self, file: Union[str, Path, BytesIO]) -> DocumentModel:
        """
        Parses a document file and returns a structured DocumentModel.
        
        Args:
            file: A file path (str/Path) or a binary stream (BytesIO) containing the document.
            
        Returns:
            DocumentModel: The unified internal representation of the document.
        """
        pass
