from backend.rejection_engine import analyze_application

def run_pipeline(resume_text, jd_text):
    audit_trail = []

    try:
        audit_trail.append("Step 1: Processing input")
        if not resume_text.strip():
            audit_trail.append("Resume is empty")
            return {
                "error": "Resume is empty. Please provide valid input.",
                "decision": "Failed",
                "audit_trail": audit_trail
            }

        audit_trail.append("Step 2: Analyzing JD")
        if not jd_text.strip():
            audit_trail.append("Recovery: Empty JD -> using fallback")

            if resume_text.strip():
                jd_text = resume_text
                audit_trail.append("Fallback applied: Using resume as JD")
            else:
                audit_trail.append("Failure: Both inputs empty")
                return {
                    "error": "Both resume and job description are empty.",
                    "decision": "Failed",
                    "audit_trail": audit_trail
                }

        audit_trail.append("Step 3: Matching Skills")
        result = analyze_application(resume_text, jd_text)

        audit_trail.append("Step 4: Decision Making")
        if result["match_percentage"] > 70:
            decision = "Strong Fit"
        elif result["match_percentage"] > 40:
            decision = "Borderline"
        else:
            decision = "Reject"

        audit_trail.append(f"Decision: {decision}")

        audit_trail.append("Step 5: Generating Explanation")
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