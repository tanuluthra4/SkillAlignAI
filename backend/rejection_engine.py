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

    failure_analysis = generate_failure_analysis(score_data)

    return {
        "rejection_report": rejection_report,
        "rejection_summary": rejection_summary,
        "improvement_suggestions": improvement_suggestions,
        "failure_analysis": failure_analysis
    }

def generate_failure_analysis(score_data):
    missing_required = score_data.get("missing_skills", [])
    missing_preferred = score_data.get("missing_preferred_skills", [])
    match = score_data.get("match_score", 0)

    if missing_required:
        return {
            "primary_reason": "Core skill gap",
            "impact": "High",
            "confidence": f"{min(100, match + 20)}%",
            "explanation": ( 
                f"The candidate lacks mandatory skills required to perform the role effectively."
                f"Missing: {', '.join(missing_required)}"
            ),
            "fix_action": f"Focus on learning: {', '.join(missing_required)}",
            "priority": 1
        }

    elif missing_preferred:
        return {
            "primary_reason": "Competitive disadvantage",
            "impact": "Medium",
            "confidence": f"{min(100, match + 10)}%",
            "explanation": (
                "The candidate meets core requirements but lacks preferred skills that increase competitiveness."
                f"Missing: {', '.join(missing_preferred)}"
            ),
            "fix_action": f"Improve profile by adding: {', '.join(missing_preferred)}",
            "priority": 2
        }

    else:
        return {
            "primary_reason": "Strong alignment",
            "impact": "Low",
            "confidence": f"{match}%",
            "explanation": "Candidate aligns well with job requirements",
            "fix_action": "No major improvements needed.",
            "priority": 3
        }