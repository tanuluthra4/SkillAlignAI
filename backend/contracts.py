from typing import List, Dict, TypedDict

class RejectionReason(TypedDict):
    reason: str
    severity: str
    details: list 

class SkillAlignResponse(TypedDict):
    match_percentage: int
    missing_skills: List[str]
    weak_skills: List[str]
    rejection_report: List[RejectionReason]
    rejection_summary: str
    improvement_suggestions: List[str]
    