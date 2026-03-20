import re

def extract_jd_requirements(jd_text):
    jd_text = jd_text.lower()
    required_skills = set()
    preferred_skills = set()

    skill_keywords = [
        "python", "py", "java", "c++", "sql", "flask", "node", "nodejs",  "html", "javascript", "js", "rest api", "data structures", "algorithms", "docker", "css", "c", "machine learning", "ml", "react.js", "react", "ai", "artificial intelligence"
    ]

    # Split JD into sections
    preferred_markers = ["preferred", "nice to have", "bonus"]

    preferred_section = ""
    required_section = jd_text

    for marker in preferred_markers:
        if marker in jd_text:
            parts = re.split(rf"{marker}\s*:", jd_text, maxsplit=1)
            if len(parts) == 2:
                required_section = parts[0]
                preferred_section = parts[1]
            break

    # Detect required skills 
    token1 = set(re.findall(r'\b\w+\b', required_section))
    for skill in skill_keywords:
        if " " in skill:
            if skill in required_section:
                required_skills.add(skill)
        else:
            if skill in token1:
                required_skills.add(skill)

    # Detect preferred skills 
    token2 = set(re.findall(r'\b\w+\b', preferred_section))
    for skill in skill_keywords:
        if " " in skill:
            if skill in preferred_section:
                preferred_skills.add(skill)
        else:
            if skill in token2:
                preferred_skills.add(skill)


    return {
        "required_skills": list(required_skills),
        "preferred_skills": list(preferred_skills),
        "raw_text": jd_text
    }