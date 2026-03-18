import re

def extract_jd_requirements(jd_text):
    jd_text = jd_text.lower()
    required_skills = []

    skill_keywords = [
        "python", "py", "java", "c++", "sql", "flask", "node", "nodejs",  "html", "javascript", "js", "rest api", "data structures", "algorithms", "docker", "css", "c", "machine learning", "ml", "react.js", "react", "ai", "artificial intelligence"
    ]

    for skill in skill_keywords:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, jd_text):
            required_skills.append(skill)

    return {
        "required_skills": required_skills,
        "raw_text": jd_text
    }