from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum

class DataType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"

class EntityType(Enum):
    OBJECT = "object"
    ARRAY = "array"

@dataclass
class Validation:
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    min: Optional[float] = None
    max: Optional[float] = None

@dataclass
class FieldConfig:
    key_mappings: List[str]
    data_type: str
    required: bool = False
    default: Any = None
    validations: Optional[Dict[str, Any]] = None

@dataclass
class EntityConfig:
    entity_type: str
    fields: Optional[Dict[str, FieldConfig]] = None
    item_schema: Optional[Dict[str, FieldConfig]] = None
    array_key_mappings: Optional[List[str]] = None

@dataclass
class ParsingRules:
    case_sensitive: bool = False
    nested_key_separator: str = "."
    array_indicators: List[str] = field(default_factory=list)

@dataclass
class ResumeParserConfig:
    entities: Dict[str, EntityConfig]
    parsing_rules: ParsingRules