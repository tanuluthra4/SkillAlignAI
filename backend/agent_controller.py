from backend.resume_parser import extract_resume_info
from backend.jd_analyzer import extract_jd_requirements
from backend.rejection_engine import analyze_application

def run_pipeline(resume_text, jd_text):
    try:
        print("Step 1: Processing input")
        if not resume_text.strip():
            return {
                "error": "Resume is empty. Please provide valid input.",
                "decision": "Failed"
            }
        resume_data = extract_resume_info(resume_text)

        print("Step 2: Analyzing JD")
        if not jd_text.strip():
            print("Recovery: Empty JD -> using fallback")
            jd_text = resume_text
        jd_data = extract_jd_requirements(jd_text)

        print("Step 3: Matching Skills")
        result = analyze_application(resume_text, jd_text)

        print("Step 4: Decision Making")
        if result["match_percentage"] > 70:
            decision = "Strong Fit"
        elif result["match_percentage"] > 40:
            decision = "Borderline"
        else:
            decision = "Reject"

        print("Step 5: Generating Explanation")
        result["decision"] = decision

        return result 
    
    except Exception as e:
        print("Recovery: System error detected -> fallback response")

        return {
            "match_percentage": 0,
            "required_match_percentage": 0, 
            "preferred_match_percentage": 0,
            "missing_skills": [],
            "missing_preferred_skills": [],
            "rejection_report": [],
            "rejection_summary": "System encountered an issue but recovered safely.",
            "improvement_suggestions": [],
            "decision": "Failed"
        }