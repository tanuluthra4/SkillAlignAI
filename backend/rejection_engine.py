from backend.resume_parser import extract_resume_info
from backend.jd_analyzer import extract_jd_requirements
from backend.gemini_client import generate_explanation
from backend.rejection_report import build_rejection_report
from backend.contracts import SkillAlignResponse
from backend.fallback_explainer import generate_fallback_summary

SKILL_NORMALIZATION = {
    "javascript": "js",
    "node": "nodejs",
    "react.js": "react",
    "machine learning": "ml",
    "ai": "artificial intelligence",
    "python": "py"
}

def normalize_skills(skill_list):
    normalized = []

    for skill in skill_list:
        skill = skill.lower().strip()

        if skill in SKILL_NORMALIZATION:
            skill = SKILL_NORMALIZATION[skill]

        normalized.append(skill)

    return normalized

def analyze_application(resume_text: str, job_description_text: str) -> SkillAlignResponse:
    # 1. Parse inputs
    resume_data = extract_resume_info(resume_text)
    jd_data = extract_jd_requirements(job_description_text)

    # 2. Compute skill match percentage 
    resume_skills = set(normalize_skills(resume_data.get("skills", [])))
    required_skills = set( normalize_skills(jd_data.get("required_skills", [])))
    preferred_skills = set(normalize_skills(jd_data.get("preferred_skills", [])))

    REQUIRED_WEIGHT = 0.8
    PREFERRED_WEIGHt = 0.2

    required_match = 0
    preferred_match = 0

    if required_skills:
        required_match = len(resume_skills & required_skills) / len(required_skills)
    if preferred_skills:
        preferred_match = (len(resume_skills & preferred_skills) / len(preferred_skills))

    match_score = (REQUIRED_WEIGHT * required_match) + (PREFERRED_WEIGHt * preferred_match)

    match_percentage = int(match_score * 100)

    # 3. Derive structured fields 
    missing_skills = list(required_skills - resume_skills)
    missing_preferred_skills = list(preferred_skills - resume_skills)
    weak_skills = [] # can evolve later 

    # 4. Rule based rejection report
    rejection_report = build_rejection_report(
        match_percentage,
        missing_skills,
        missing_preferred_skills,
        weak_skills
    ) 

    # 5. Generate explanation text (AI-assisted)
    resume_data["skills"] = list(resume_skills)
    jd_data["required_skills"] = list(required_skills)
    jd_data["preferred_skills"] = list(preferred_skills)
    
    try:
        rejection_summary = generate_explanation(
            resume_data, 
            jd_data,
            rejection_report
        )
    
    except Exception:
        rejection_summary = generate_fallback_summary(rejection_report)

    # 6. Improvement suggestions (deterministic)
    improvement_suggestions = [
        f"Add or strengthen experience in {skill}"
        for skill in missing_skills
    ]

    improvement_suggestions += [
        f"Learning {skill} could improve competitiveness for this role."
        for skill in missing_preferred_skills
    ]

    return {
        "match_percentage": match_percentage,
        "missing_skills": missing_skills,
        "missing_preferred_skills": missing_preferred_skills,
        "weak_skills": weak_skills,
        "rejection_report": rejection_report,
        "rejection_summary": rejection_summary,
        "improvement_suggestions": improvement_suggestions
    }