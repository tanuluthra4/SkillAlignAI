from backend.rejection_report import build_rejection_report
from backend.fallback_explainer import generate_fallback_summary
from backend.utils.normalizer import normalize_skills

def compute_match_score(resume_data, jd_data): 
    resume_skills = set(normalize_skills(resume_data.get("skills", [])))
    required_skills = set(normalize_skills(jd_data.get("required_skills", [])))
    preferred_skills = set(normalize_skills(jd_data.get("preferred_skills", [])))

    REQUIRED_WEIGHT = 0.8
    PREFERRED_WEIGHT = 0.2

    required_match = 0
    preferred_match = 0

    if required_skills:
        required_match = len(resume_skills & required_skills) / len(required_skills)
    else:
        required_match = 1

    if preferred_skills:
        preferred_match = (len(resume_skills & preferred_skills) / len(preferred_skills))
    else:
        preferred_match = 1

    match_score = (REQUIRED_WEIGHT * required_match) + (PREFERRED_WEIGHT * preferred_match)

    required_match_percentage = int(required_match * 100)
    preferred_match_percentage = int(preferred_match * 100)
    match_percentage = int(match_score * 100)

    matched_skills = list(resume_skills  & required_skills)
    missing_skills = list(required_skills - resume_skills)
    missing_preferred_skills = list(preferred_skills - resume_skills)

    return {
        "match_score": match_percentage,
        "required_match": required_match_percentage,
        "preferred_match": preferred_match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "missing_preferred_skills": missing_preferred_skills
    }

def generate_rejection_data(score_data):
    match_percentage = score_data["match_score"]

    missing_skills = score_data["missing_skills"]
    missing_preferred_skills = score_data["missing_preferred_skills"]

    weak_skills = []

    rejection_report = build_rejection_report(
        match_percentage, 
        missing_skills,
        missing_preferred_skills,
        weak_skills
    )

    try:
        rejection_summary = generate_fallback_summary(rejection_report)
    except Exception:
        rejection_summary = "Could not generate summary"

    improvement_suggestions = [
        f"Add or strengthen experience in {skill}"
        for skill in missing_skills
    ]

    improvement_suggestions += [
        f"Learning {skill} could improve competitiveness"
        for skill in missing_preferred_skills
    ]

    return {
        "rejection_report": rejection_report,
        "rejection_summary": rejection_summary,
        "improvement_suggestions": improvement_suggestions
    }