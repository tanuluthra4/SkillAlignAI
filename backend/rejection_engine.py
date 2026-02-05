from backend.resume_parser import extract_resume_info
from backend.jd_analyzer import extract_jd_requirements
from backend.gemini_client import generate_explanation

def analyze_application(resume_text: str, job_description_text: str) -> dict:
    # 1. Parse inputs
    resume_data = extract_resume_info(resume_text)
    jd_data = extract_jd_requirements(job_description_text)

    # 2. Run rule-based rejection analysis 
    rejection_reasons = analyze_rejection(resume_data, jd_data)

    # 3. Compute skill match percentage 
    resume_skills = set(resume_data.get("skills", []))
    required_skills = set(jd_data.get("required_skills", []))

    if not required_skills:
        match_percentage = 0
    else:
        match_percentage = int(
            (len(resume_skills & required_skills) / len(required_skills)) * 100
        )

    # 4. Derive structured fields 
    missing_skills = list(required_skills - resume_skills)
    weak_skills = [] # can evolve later 

    # 5. Generate explanation text (AI-assisted)
    try:
        rejection_summary = generate_explanation(
            resume_data, 
            jd_data,
            rejection_reasons
        )
    
    except Exception:
        rejection_summary = (
            "The resume does not sufficiently align with the job requirements."
            "Several required skills are missing or underrepresented."
        )

    # 6. Improvement suggestions (deterministic)
    improvement_suggestions = [
        f"Add or strengthen experience in {skill}"
        for skill in missing_skills
    ]

    return {
        "match_percentage": match_percentage,
        "missing_skills": missing_skills,
        "weak_skills": weak_skills,
        "rejection_summary": rejection_summary,
        "improvement_suggestions": improvement_suggestions
    }

def analyze_rejection(resume_data, jd_data):
    resume_skills = set(resume_data["skills"])
    required_skills = set(jd_data["required_skills"])

    missings_skills = list(required_skills - resume_skills)

    reasons = []

    if missings_skills:
        reasons.append({
            "reason": "Missing required skills",
            "severity": "High",
            "details": missings_skills
        })

    if len(resume_skills) < 3:
        reasons.append({
            "reason": "Limited skill coverage",
            "severity": "Medium",
            "details": []
        })

    return reasons