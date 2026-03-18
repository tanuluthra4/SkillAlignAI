import re

def extract_resume_info(resume_text):
    resume_text = resume_text.lower()
    skills = []

    common_skills = [
        "python", "py", "java", "c++", "sql", "flask", "node", "nodejs", "docker", "c", "javascript", "js", "html", "css", "machine learning", "ml", "data structures", "rest api", "algorithms", "react.js", "react", "ai", "artificial intelligence"
    ]

    for skill in common_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, resume_text):
            skills.append(skill)

    return {
        "skills": skills,
        "raw_text": resume_text
    }