import re

def extract_resume_info(resume_text):
    resume_text = resume_text.lower()
    skills = set()

    common_skills = [
        "python", "py", "java", "c++", "sql", "flask", "node", "nodejs", "docker", "c", "javascript", "js", "html", "css", "machine learning", "ml", "data structures", "rest api", "algorithms", "react.js", "react", "ai", "artificial intelligence"
    ]

    tokens = set(re.findall(r'\b\w+\b', resume_text))

    for skill in common_skills:
        if " " in skill:
            if skill in resume_text:
                skills.add(skill)
        else:
            if skill in tokens:
                skills.add(skill)

    return {
        "skills": list(skills),
        "raw_text": resume_text
    }