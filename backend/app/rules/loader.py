import yaml
import json
from pathlib import Path
from typing import Union

from app.rules.schemas import DocumentRuleTemplate

class RuleLoader:
    """
    Utility class to load and validate rule configurations
    from YAML or JSON files against the DocumentRuleTemplate schema.
    """
    
    @staticmethod
    def load_from_yaml(file_path: Union[str, Path]) -> DocumentRuleTemplate:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return DocumentRuleTemplate(**data)
        
    @staticmethod
    def load_from_json(file_path: Union[str, Path]) -> DocumentRuleTemplate:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return DocumentRuleTemplate(**data)
    
    @staticmethod
    def load_from_dict(data: dict) -> DocumentRuleTemplate:
        return DocumentRuleTemplate(**data)
