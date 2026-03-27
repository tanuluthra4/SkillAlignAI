SEMANTIC_SKILL_MAP = {
    "python": ["flask", "django", "fastapi"],
    "javascript": ["react", "node", "express"],
    "machine learning": ["tensorflow", "pytorch", "scikit-learn"],
    "sql": ["mysql", "postgresql"],
}

REVERSE_SEMANTIC_MAP = {
    "flask": ("python", 0.4),
    "django": ("python", 0.4),
    "fastapi": ("python", 0.4),
    "react": ("javascript", 0.4),
    "node": ("javascript", 0.4), 
    "express": ("javascript", 0.4),
    "tensorflow": ("machine learning", 0.4),
    "pytorch": ("machine learning", 0.4),
    "scikit-learn": ("machine learning", 0.4),
    "mysql": ("sql", 0.4),
    "postgresql": ("sql", 0.4)
}

def expand_skills_with_confidence(skills):
    if not skills:
        return {}
    
    expanded = {}

    for skill in skills:
        if not skill:
            continue

        expanded[skill] = 1.0

        for parent, children in SEMANTIC_SKILL_MAP.items():
            if not children:
                continue
            
            if skill in children:
                expanded[parent] = max(expanded.get(parent, 0), 0.7)

    return expanded