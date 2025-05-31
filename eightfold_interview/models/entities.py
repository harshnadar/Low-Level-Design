from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class PersonalInfo:
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None

@dataclass
class Education:
    school_name: str
    degree: str
    field_of_study: Optional[str] = None
    graduation_year: Optional[int] = None

@dataclass
class Experience:
    company: str
    title: str
    duration: Optional[str] = None
    description: Optional[str] = None

@dataclass
class Skill:
    skill_name: str

@dataclass
class ParsedResume:
    personal_info: Optional[PersonalInfo] = None
    education: List[Education] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    skills: List[Skill] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    parsed_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert parsed resume to dictionary"""
        return {
            "personal_info": {
                "full_name": self.personal_info.full_name if self.personal_info else None,
                "email": self.personal_info.email if self.personal_info else None,
                "phone": self.personal_info.phone if self.personal_info else None,
                "location": self.personal_info.location if self.personal_info else None
            } if self.personal_info else None,
            "education": [
                {
                    "school_name": edu.school_name,
                    "degree": edu.degree,
                    "field_of_study": edu.field_of_study,
                    "graduation_year": edu.graduation_year
                } for edu in self.education
            ],
            "experience": [
                {
                    "company": exp.company,
                    "title": exp.title,
                    "duration": exp.duration,
                    "description": exp.description
                } for exp in self.experience
            ],
            "skills": [
                {"skill_name": skill.skill_name} for skill in self.skills
            ],
            "parsed_at": self.parsed_at.isoformat()
        }