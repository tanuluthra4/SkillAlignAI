import re

def extract_resume_info(resume_text):
    resume_text = resume_text.lower()
    skills = []

    common_skills = [
        "python", "java", "c++", "sql", "flask", "node", "docker", "c", "javascript", "html", "css", "machine learning", "data structures", "rest api", "algorithms"
    ]

    for skill in common_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, resume_text):
            skills.append(skill)

    return {
        "skills": skills,
        "raw_text": resume_text
    }