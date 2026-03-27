from difflib import SequenceMatcher

def is_similar(a, b, threshold=0.8):
    return SequenceMatcher(None, a, b).ratio() >= threshold

ALL_KNOWN_SKILLS = [
    "python", "py", "java", "c++", "sql", "flask", "node", "nodejs",  "html", "javascript", "rest api", "data structures", "algorithms", "docker", "css", "c", "react.js", "react", "api", "django", "fast api", "express", "tensorflow", "pytorch", "scikit-learn", "mysql", "postgresql", "machine learning", "ai"
]

def correct_typos(skill):
    best_match = skill
    best_score = 0

    for known in ALL_KNOWN_SKILLS:
        score = SequenceMatcher(None, skill, known).ratio()
        if score > best_score:
            best_score = score
            best_match = known

    if best_score > 0.8:
        return best_match
    
    return skill

SKILL_NORMALIZATION = {
    "js": "javascript",
    "nodejs": "node",
    "react.js": "react",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "py": "python"
}

def normalize_skills(skill_list):
    normalized = []

    for skill in skill_list:
        skill = skill.lower().strip()
        skill = correct_typos(skill)

        if skill in SKILL_NORMALIZATION:
            skill = SKILL_NORMALIZATION[skill]

        normalized.append(skill)

    return normalized