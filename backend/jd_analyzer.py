import re
from backend.utils.role_map import ROLE_SKILL_MAP

def detect_role(jd_text):
    jd_text = jd_text.lower()

    role_patterns = {
        "frontend": r"\b(frontend|front-end)\b",
        "backend": r"\b(backend|back-end)\b",
        "ai": r"\b(ai|machine learning|ml)\b",
        "full stack": r"\b(full stack|full-stack|fullstack)\b"
    }

    for role, pattern in role_patterns.items():
        if re.search(pattern, jd_text):
            return role
        
    return None

def extract_jd_requirements(jd_text):
    jd_text = jd_text.lower()
    required_skills = set()
    preferred_skills = set()

    skill_keywords = [
        "python", "py", "java", "c++", "sql", "flask", "node", "nodejs",  "html", "javascript", "rest api", "data structures", "algorithms", "docker", "css", "c", "react.js", "react", "api", "django", "fast api", "express", "tensorflow", "pytorch", "scikit-learn", "mysql", "postgresql", "pandas", "deep learning"
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

    domain_skills = set()

    if "machine learning" in jd_text or "ml" in jd_text:
        domain_skills.add("machine learning")

    if "ai" in jd_text or "artificial intelligence" in jd_text:
        domain_skills.add("artificial intelligence")

    role = detect_role(jd_text)

    # fallback if role not explicitly found
    if not role: 

        if "react" in required_skills or "html" in required_skills or "css" in required_skills:
            role = "frontend"

        elif "node" in required_skills or "sql" in required_skills or "flask" in required_skills:
            role = "backend"
        
        elif "machine learning" in required_skills or "ai" in required_skills:
            role = "ai"

    if role and len(required_skills) < 2:
        role_skills = ROLE_SKILL_MAP.get(role, [])
        required_skills = required_skills.union(role_skills[:2])

    return {
        "required_skills": list(required_skills),
        "preferred_skills": list(preferred_skills),
        "domain_skills": list(domain_skills),
        "raw_text": jd_text,
        "role": role
    }