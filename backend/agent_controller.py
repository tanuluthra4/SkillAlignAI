from backend.resume_parser import extract_resume_info
from backend.jd_analyzer import extract_jd_requirements
from backend.rejection_engine import analyze_application

def run_pipeline(resume_text, jd_text):
    print("Step 1: Processing input")
    resume_data = extract_resume_info(resume_text)

    print("Step 2: Analyzing JD")
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