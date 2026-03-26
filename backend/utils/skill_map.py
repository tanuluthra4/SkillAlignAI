SEMANTIC_SKILL_MAP = {
    "python": ["flask", "django", "fastapi"],
    "javascript": ["react", "node", "express"],
    "machine learning": ["tensorflow", "pytorch", "scikit-learn"],
    "sql": ["mysql", "postgresql"],
}

def expand_skills(skills):
    if not skills:
        return []
    
    expanded = set()

    for skill in skills:
        if not skill:
            continue

        expanded.add(skill)

        for parent, children in SEMANTIC_SKILL_MAP.items():
            if not children:
                continue
            
            if skill in children:
                expanded.add(parent)

    return list(expanded)