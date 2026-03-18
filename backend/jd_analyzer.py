import re

def extract_jd_requirements(jd_text):
    jd_text = jd_text.lower()
    required_skills = []
    preferred_skills = []

    skill_keywords = [
        "python", "py", "java", "c++", "sql", "flask", "node", "nodejs",  "html", "javascript", "js", "rest api", "data structures", "algorithms", "docker", "css", "c", "machine learning", "ml", "react.js", "react", "ai", "artificial intelligence"
    ]

    # Split JD into sections
    preferred_markers = ["preferred", "nice to have", "bonus"]

    preferred_section = ""
    required_section = jd_text

    for marker in preferred_markers:
        if marker in jd_text:
            parts = jd_text.split(marker, 1)
            required_section = parts[0]
            preferred_section = parts[1]
            break

    # Detect required skills 
    for skill in skill_keywords:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, required_section):
            required_skills.append(skill)

    # Detect preferred skills 
    for skill in skill_keywords:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if preferred_section and re.search(pattern, preferred_section):
            preferred_skills.append(skill)

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "raw_text": jd_text
    }