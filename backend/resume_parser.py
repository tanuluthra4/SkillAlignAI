import re

def extract_resume_info(resume_text):
    resume_text = resume_text.lower()

    skills = set()
    projects = []
    experience = []

    common_skills = [
        "python", "py", "java", "c++", "sql", "flask", "node", "nodejs", "docker", "c", "javascript", "html", "css", "machine learning", "ml", "data structures", "rest api", "algorithms", "react.js", "react", "ai", "artificial intelligence", "api"
    ]

    # Skill detection
    tokens = set(re.findall(r'\b\w+\b', resume_text))

    for skill in common_skills:
        if " " in skill:
            if skill in resume_text:
                skills.add(skill)
        else:
            if skill in tokens:
                skills.add(skill)

    # Project Detection 
    project_matches = re.findall(r'(project|built|developed)(.*)', resume_text)
    projects = [match[1] for match in project_matches]

    # Experience Detection 
    exp_matches = re.findall(r'(intern|experience|worked)(.*)', resume_text)
    experience = [match[1] for match in exp_matches]

    return {
        "skills": list(skills),
        "projects": projects,
        "experience": experience,
        "raw_text": resume_text
    }