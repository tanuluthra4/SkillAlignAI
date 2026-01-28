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