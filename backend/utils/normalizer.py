from difflib import SequenceMatcher

def is_similar(a, b, threshold=0.8):
    return SequenceMatcher(None, a, b).ratio() >= threshold

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

        if skill in SKILL_NORMALIZATION:
            skill = SKILL_NORMALIZATION[skill]

        normalized.append(skill)

    return normalized