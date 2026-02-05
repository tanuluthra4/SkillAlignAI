from backend.resume_parser import extract_resume_info
from backend.jd_analyzer import extract_jd_requirements
from backend.gemini_client import generate_explanation
from backend.rejection_report import build_rejection_report
from backend.contracts import SkillAlignResponse
from backend.fallback_explainer import generate_fallback_summary

def analyze_application(resume_text: str, job_description_text: str) -> SkillAlignResponse:
    # 1. Parse inputs
    resume_data = extract_resume_info(resume_text)
    jd_data = extract_jd_requirements(job_description_text)

    # 2. Compute skill match percentage 
    resume_skills = set(resume_data.get("skills", []))
    required_skills = set(jd_data.get("required_skills", []))

    if not required_skills:
        match_percentage = 0
    else:
        match_percentage = int(
            (len(resume_skills & required_skills) / len(required_skills)) * 100
        )

    # 3. Derive structured fields 
    missing_skills = list(required_skills - resume_skills)
    weak_skills = [] # can evolve later 

    # 4. Rule based rejection report
    rejection_report = build_rejection_report(
        match_percentage,
        missing_skills,
        weak_skills
    ) 

    # 5. Generate explanation text (AI-assisted)
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

    return {
        "match_percentage": match_percentage,
        "missing_skills": missing_skills,
        "weak_skills": weak_skills,
        "rejection_report": rejection_report,
        "rejection_summary": rejection_summary,
        "improvement_suggestions": improvement_suggestions
    }