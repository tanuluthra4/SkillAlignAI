def extract_jd_requirements(jd_text):
    jd_text = jd_text.lower()
    required_skills = []

    skill_keywords = [
        "python", "java", "c++", "sql", "flask", "node",
        "javascript", "rest api", "data structures", "algorithms",
        "docker"
    ]

    for skill in skill_keywords:
        if skill in jd_text:
            required_skills.append(skill)

    return {
        "required_skills": required_skills,
        "raw_text": jd_text
    }