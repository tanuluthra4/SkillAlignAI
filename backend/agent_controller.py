from backend.rejection_engine import analyze_application

def run_pipeline(resume_text, jd_text):
    audit_trail = []

    try:
        audit_trail.append("[Input Agent] Processing input")
        if not resume_text.strip():
            audit_trail.append("Resume is empty")
            return {
                "error": "Resume is empty. Please provide valid input.",
                "decision": "Failed",
                "audit_trail": audit_trail
            }

        audit_trail.append("[JD Analysis Agent] Analyzing JD")
        if not jd_text.strip():
            audit_trail.append("[Recovery Agent] Empty JD detected")

            if resume_text.strip():
                jd_text = resume_text
                audit_trail.append("[Recovery Agent] Fallback applied: Using resume as JD")
            else:
                audit_trail.append("[Recovery Agent] Failure: Both inputs empty")
                return {
                    "error": "Both resume and job description are empty.",
                    "decision": "Failed",
                    "audit_trail": audit_trail
                }

        audit_trail.append("[Matching Agent] Matching Skills")
        result = analyze_application(resume_text, jd_text)

        audit_trail.append("[Decision Agent] Decision Making")
        if result["match_percentage"] > 70:
            decision = "Strong Fit"
        elif result["match_percentage"] > 40:
            decision = "Borderline"
        else:
            decision = "Reject"

        audit_trail.append(f"[Decision Agent] Decision: {decision}")

        audit_trail.append("[Explanation Agent] Generating Explanation")
        result["decision"] = decision
        result["audit_trail"] = audit_trail

        return result 
    
    except Exception as e:
        audit_trail.append("Recovery: System error detected -> fallback response")

        return {
            "match_percentage": 0,
            "required_match_percentage": 0, 
            "preferred_match_percentage": 0,
            "missing_skills": [],
            "missing_preferred_skills": [],
            "rejection_report": [],
            "rejection_summary": "System encountered an issue but recovered safely.",
            "improvement_suggestions": [],
            "decision": "Failed", 
            "audit_trail": audit_trail
        }