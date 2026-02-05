def extract_resume_info(resume_text):
    resume_text = resume_text.lower()
    skills = []

    common_skills = [
        "python", "java", "c++", "sql", "flask", "node", "docker",
        "javascript", "html", "css", "machine learning", "data structures"
    ]

    for skill in common_skills:
        if skill in resume_text:
            skills.append(skill)

    return {
        "skills": skills,
        "raw_text": resume_text
    }