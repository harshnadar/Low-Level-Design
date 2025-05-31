import json
import re
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from models.entities import *
from models.config import *

class ConfigurableResumeParser:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: str) -> ResumeParserConfig:
        """Load and parse configuration from JSON file"""
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        # Parse config into structured format
        entities = {}
        for entity_name, entity_config in config_data['entities'].items():
            fields = None
            item_schema = None
            
            if 'fields' in entity_config:
                fields = {}
                for field_name, field_config in entity_config['fields'].items():
                    fields[field_name] = FieldConfig(**field_config)
            
            if 'item_schema' in entity_config:
                item_schema = {}
                for field_name, field_config in entity_config['item_schema'].items():
                    item_schema[field_name] = FieldConfig(**field_config)
            
            entities[entity_name] = EntityConfig(
                entity_type=entity_config['entity_type'],
                fields=fields,
                item_schema=item_schema,
                array_key_mappings=entity_config.get('array_key_mappings', [])
            )
        
        parsing_rules = ParsingRules(**config_data.get('parsing_rules', {}))
        
        return ResumeParserConfig(entities=entities, parsing_rules=parsing_rules)
    
    def parse(self, resume_data: Dict[str, Any]) -> ParsedResume:
        """Parse resume data according to configuration"""
        parsed_resume = ParsedResume(raw_data=resume_data)
        
        # Parse personal info
        if 'personal_info' in self.config.entities:
            entity_config = self.config.entities['personal_info']
            if entity_config.entity_type == EntityType.OBJECT.value:
                personal_info = self._parse_personal_info(resume_data, entity_config)
                if personal_info:
                    parsed_resume.personal_info = personal_info
        
        # Parse education
        if 'education' in self.config.entities:
            entity_config = self.config.entities['education']
            if entity_config.entity_type == EntityType.ARRAY.value:
                education_list = self._parse_education(resume_data, entity_config)
                parsed_resume.education = education_list
        
        # Parse experience
        if 'experience' in self.config.entities:
            entity_config = self.config.entities['experience']
            if entity_config.entity_type == EntityType.ARRAY.value:
                experience_list = self._parse_experience(resume_data, entity_config)
                parsed_resume.experience = experience_list
        
        # Parse skills
        if 'skills' in self.config.entities:
            entity_config = self.config.entities['skills']
            if entity_config.entity_type == EntityType.ARRAY.value:
                skills_list = self._parse_skills(resume_data, entity_config)
                parsed_resume.skills = skills_list
        
        return parsed_resume
    
    def _parse_personal_info(self, data: Dict, entity_config: EntityConfig) -> Optional[PersonalInfo]:
        """Parse personal info object"""
        if not entity_config.fields:
            return None
        
        parsed_fields = {}
        for field_name, field_config in entity_config.fields.items():
            value = self._extract_value(data, field_config)
            if value is not None:
                # Validate the value
                if field_config.validations:
                    is_valid, error = self._validate_field(value, field_config)
                    if not is_valid and field_config.required:
                        print(f"Validation error for {field_name}: {error}")
                        continue
                
                parsed_fields[field_name] = value
            elif field_config.required:
                print(f"Required field {field_name} not found")
                return None
        
        try:
            return PersonalInfo(**parsed_fields)
        except Exception as e:
            print(f"Error creating PersonalInfo: {e}")
            return None
    
    def _parse_education(self, data: Dict, entity_config: EntityConfig) -> List[Education]:
        """Parse education array"""
        if not entity_config.item_schema:
            return []
        
        results = []
        array_data = self._find_array_data(data, entity_config)
        
        for item in array_data:
            parsed_item = {}
            for field_name, field_config in entity_config.item_schema.items():
                value = self._extract_value(item, field_config)
                if value is not None:
                    parsed_item[field_name] = value
                elif field_config.required:
                    break
            else:
                try:
                    results.append(Education(**parsed_item))
                except Exception as e:
                    print(f"Error creating Education: {e}")
        
        return results
    
    def _parse_experience(self, data: Dict, entity_config: EntityConfig) -> List[Experience]:
        """Parse experience array"""
        if not entity_config.item_schema:
            return []
        
        results = []
        array_data = self._find_array_data(data, entity_config)
        
        for item in array_data:
            parsed_item = {}
            for field_name, field_config in entity_config.item_schema.items():
                value = self._extract_value(item, field_config)
                if value is not None:
                    parsed_item[field_name] = value
                elif field_config.required:
                    break
            else:
                try:
                    results.append(Experience(**parsed_item))
                except Exception as e:
                    print(f"Error creating Experience: {e}")
        
        return results
    
    def _parse_skills(self, data: Dict, entity_config: EntityConfig) -> List[Skill]:
        """Parse skills array"""
        if not entity_config.item_schema:
            return []
        
        results = []
        array_data = self._find_array_data(data, entity_config)
        
        for item in array_data:
            if isinstance(item, str):
                # Handle case where skills are just strings
                results.append(Skill(skill_name=item))
            elif isinstance(item, dict):
                parsed_item = {}
                for field_name, field_config in entity_config.item_schema.items():
                    value = self._extract_value(item, field_config)
                    if value is not None:
                        parsed_item[field_name] = value
                
                if parsed_item:
                    try:
                        results.append(Skill(**parsed_item))
                    except Exception as e:
                        print(f"Error creating Skill: {e}")
        
        return results
    
    def _extract_value(self, data: Union[Dict, Any], field_config: FieldConfig) -> Optional[Any]:
        """Extract value from data using key mappings"""
        if not isinstance(data, dict):
            return None
            
        for key_mapping in field_config.key_mappings:
            value = self._get_nested_value(data, key_mapping)
            if value is not None:
                try:
                    return self._convert_type(value, field_config.data_type)
                except Exception as e:
                    print(f"Error converting type for {key_mapping}: {e}")
                    continue
        
        return field_config.default
    
    def _get_nested_value(self, data: Dict, key_path: str) -> Optional[Any]:
        """Get value from nested dictionary using dot notation"""
        if not isinstance(data, dict):
            return None
            
        if not self.config.parsing_rules.case_sensitive:
            return self._get_value_case_insensitive(data, key_path)
        
        keys = key_path.split(self.config.parsing_rules.nested_key_separator)
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    def _get_value_case_insensitive(self, data: Dict, key_path: str) -> Optional[Any]:
        """Case-insensitive value extraction"""
        if not isinstance(data, dict):
            return None
            
        keys = key_path.split(self.config.parsing_rules.nested_key_separator)
        current = data
        
        for key in keys:
            if isinstance(current, dict):
                found = False
                for k in current.keys():
                    if k.lower() == key.lower():
                        current = current[k]
                        found = True
                        break
                if not found:
                    return None
            else:
                return None
        
        return current
    
    def _find_array_data(self, data: Dict, entity_config: EntityConfig) -> List[Dict]:
        """Find array data in the input using array key mappings"""
        if entity_config.array_key_mappings:
            for key_mapping in entity_config.array_key_mappings:
                value = self._get_nested_value(data, key_mapping)
                if isinstance(value, list):
                    return value
        
        # Fallback: search for any list in the data
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                # Check if it matches the expected structure
                if isinstance(value[0], dict) or isinstance(value[0], str):
                    return value
        
        return []
    
    def _convert_type(self, value: Any, data_type: str) -> Any:
        """Convert value to specified data type"""
        if value is None:
            return None
            
        try:
            if data_type == DataType.STRING.value:
                return str(value)
            elif data_type == DataType.INTEGER.value:
                return int(value)
            elif data_type == DataType.FLOAT.value:
                return float(value)
            elif data_type == DataType.BOOLEAN.value:
                return bool(value)
        except ValueError:
            return value
        
        return value
    
    def _validate_field(self, value: Any, field_config: FieldConfig) -> tuple[bool, Optional[str]]:
        """Validate field value based on configuration"""
        if not field_config.validations:
            return True, None
        
        validations = field_config.validations
        
        # String validations
        if isinstance(value, str):
            if 'min_length' in validations and len(value) < validations['min_length']:
                return False, f"Value too short (min: {validations['min_length']})"
            
            if 'max_length' in validations and len(value) > validations['max_length']:
                return False, f"Value too long (max: {validations['max_length']})"
            
            if 'pattern' in validations:
                try:
                    if not re.match(validations['pattern'], value):
                        return False, "Value doesn't match required pattern"
                except re.error:
                    return False, "Invalid regex pattern"
        
        # Numeric validations
        if isinstance(value, (int, float)):
            if 'min' in validations and value < validations['min']:
                return False, f"Value too small (min: {validations['min']})"
            
            if 'max' in validations and value > validations['max']:
                return False, f"Value too large (max: {validations['max']})"
        
        return True, None