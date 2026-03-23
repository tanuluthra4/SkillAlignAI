from backend.resume_parser import extract_resume_info
from backend.jd_analyzer import extract_jd_requirements
from backend.rejection_engine import compute_match_score, generate_rejection_data
from backend.gemini_client import generate_explanation
from backend.fallback_explainer import generate_fallback_summary

def resume_agent(resume_text):
    if not resume_text.strip():
        return {
            "error": "Empty resume", 
        }
    
    parsed = extract_resume_info(resume_text)

    return {
        "raw_text": resume_text,
        "skills": parsed.get("skills", []),
        "projects": parsed.get("projects", []),
        "experience": parsed.get("experience", [])
    }

def jd_agent(jd_text, resume_text):
    analyzed = extract_jd_requirements(jd_text)

    return {
        "raw_text": jd_text,
        "required_skills": analyzed.get("required_skills", []),
        "preferred_skills": analyzed.get("preferred_skills", [])
    }

def scoring_agent(resume_data, jd_data):
    result = compute_match_score(
        resume_data,
        jd_data
    )

    return {
        "match_score": result.get("match_score", 0),
        "required_match": result.get("required_match", 0),
        "preferred_match": result.get("preferred_match", 0),
        "matched_skills": result.get("matched_skills", []),
        "missing_skills": result.get("missing_skills", []),
        "missing_preferred_skills": result.get("missing_preferred_skills", []),
        "rejection_report": result.get("rejection_report", [])
    }

def decision_agent(score_data):
    score = score_data.get("match_score", 0)

    if score > 70:
        decision = "Strong Fit"
    elif score > 40: 
        decision = "Borderline"
    else:
        decision = "Reject"

    return {
        "decision": decision
    }

def explanation_agent(score_data, decision_data):
    rejection_data = generate_rejection_data(score_data)
    try: 
        explanation = generate_explanation(
            score_data, 
            decision_data, 
            rejection_data["rejection_report"]
        )
    except Exception:
        explanation = generate_fallback_summary(
            rejection_data["rejection_report"]
        )

    return {
        "summary": explanation,
        "rejection_report": rejection_data["rejection_report"],
        "improvement_suggestions": rejection_data["improvement_suggestions"],
        "failure_analysis": rejection_data["failure_analysis"],
        "impact_metrics": rejection_data["impact_metrics"]
    }

def validation_agent(resume_data, jd_data):
    issues = []

    if not resume_data.get("skills"):
        issues.append("No skills found in resume")
    
    if not jd_data.get("required_skills"):
        issues.append("No required skills found in JD")

    return {
        "is_valid": len(issues) == 0,
        "issues": issues
    }

def recovery_agent(resume_data, jd_data, validation_result):
    issues = validation_result.get("issues", [])
    actions = []

    # Case 1: JD missing skills 
    if "No required skills found in JD" in issues:
        if resume_data.get("skills"):
            jd_data["required_skills"] = resume_data["skills"]
            actions.append("Filled JD required_skills from resume")

    # Case 2: Resume missing skills 
    if "No skills found in resume" in issues:
        resume_data["skills"] = []
        actions.append("Initialized empty resume skills")

    return {
        "resume_data": resume_data,
        "jd_data": jd_data,
        "recovered": True,
        "actions": actions
    }