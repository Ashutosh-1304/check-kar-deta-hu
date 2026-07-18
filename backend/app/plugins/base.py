from typing import List, Dict, Any
from app.validators.base import BaseValidator
from docx import Document

class PluginValidator(BaseValidator):
    """
    Base class for dynamically loaded enterprise plugins.
    External modules should inherit from this to be automatically discovered
    and injected into the validation pipeline.
    """
    
    @property
    def plugin_name(self) -> str:
        """Name of the plugin"""
        return self.__class__.__name__

    @property
    def plugin_version(self) -> str:
        """Version of the plugin"""
        return "1.0.0"

    def validate(self, doc: Document, rule: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Overridden by the concrete plugin implementation.
        Must return a list of issue dictionaries.
        """
        return super().validate(doc, rule)
