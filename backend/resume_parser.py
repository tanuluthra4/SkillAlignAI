import re
from backend.utils.normalizer import is_similar, normalize_skills

def extract_resume_info(resume_text):
    resume_text = resume_text.lower()

    skills = set()
    projects = []
    experience = []

    common_skills = [
        "python", "py", "java", "c++", "sql", "flask", "node", "nodejs", "docker", "c", "javascript", "html", "css", "data structures", "rest api", "algorithms", "react.js", "react", "api", "django", "fast api", "express", "tensorflow", "pytorch", "scikit-learn", "mysql", "postgresql", "pandas", "deep learning"
    ]

    # Skill detection
    tokens = set(re.findall(r'\b\w+\b', resume_text))

    for skill in common_skills:
        if " " in skill:
            if skill in resume_text:
                skills.add(skill)
        else:
            for token in tokens:
                if is_similar(token, skill):
                    skills.add(skill)
    
    DOMAIN_SKILLS = [
        "ml", "machine learning", "ai", "artificial intelligence"
    ]
    
    domain_skills = set()

    for skill in DOMAIN_SKILLS:
        if " " in skill:
            if skill in resume_text:
                domain_skills.add(skill)
        else:
            for token in tokens:
                if is_similar(token, skill):
                    domain_skills.add(skill)
    
    domain_skills = normalize_skills(list(domain_skills))

    # Project Detection 
    project_matches = re.findall(r'(project|built|developed)(.*)', resume_text)
    projects = [match[1].strip() for match in project_matches]

    # Experience Detection 
    exp_matches = re.findall(r'(intern|experience|worked)(.*)', resume_text)
    experience = [match[1] for match in exp_matches]

    return {
        "skills": list(skills),
        "domain_skills": domain_skills,
        "projects": projects,
        "experience": experience,
        "raw_text": resume_text
    }