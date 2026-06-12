from urllib import response

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv() # Load GEMINI_API_KEY from .env

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_explanation(resume_data, jd_data, rejection_reasons):
    prompt = f"""
You are an AI system that explains likely job application rejections based on resume-job matching.

Context:
- Resume skills: {resume_data['skills']}
- job required skills: {jd_data['required_skills']}
- Detected rejection reasons (with severity): {rejection_reasons}

Instructions:
1. First, identify the SINGLE most critical rejection reason (highest severity).
    Explain why this alone could cause rejection.
2. Then list secondary contributing factors (if any), clearly separating from the primary reason.
3. Explain what hiring systems usually prioritize in such cases.
4. Give concrete, resume focused improvement steps.

Constraints: 
- Treat this as a probabilistic explanation, not a definitive verdict.
- Reflect severity levels in tone (High = deal breaker, Medium = improvement areas)
- Be concise, factual and professional.
- Avoid motivational or generic career advice. 
- Do NOT repeat the input verbatim.
- Add a one-line disclaimer that this is a likely explanation based on resume–JD comparison, not a confirmed employer decision.

Output Format:
- Primary rejection reason
- Secondary factors
- What mattered most in screening 
- How to improve next time (choose one path):
  ~ If targeting this role type
  ~ If targeting better-aligned roles
"""
    
    response = model.generate_content(prompt)
    
    if not response or not getattr(response, "text", None):
        return None
    
    return response.text

def rewrite_resume_bullet(bullet_text, target_role=None):
    prompt = f"""
You are an expert resume writer.

Rewrite the resume bullet to be:

- ATS friendly
- Achievement focused
- Professional
- Strong action verbs
- Concise

IMPORTANT:
- Never invent numbers, percentages, users, revenue, metrics, scale, or results.
- Only use information explicitly present in the original bullet.
- If metrics are missing, improve wording without fabricating them.

Target Role:
{target_role}

Original Bullet:
{bullet_text}

Return only the improved bullet.
"""

    response = model.generate_content(prompt)

    if not response or not getattr(response, "text", None):
        return bullet_text

    return response.text.strip()

print(
    rewrite_resume_bullet(
        "Built a Flask website for students",
        "Backend Developer"
    )
)

def optimize_resume(
    resume_text,
    job_description_text,
    missing_skills
):
    prompt = f"""
You are an expert ATS resume optimizer.

Resume:
{resume_text}

Job Description:
{job_description_text}

Missing Skills:
{missing_skills}

Tasks:

1. Improve resume bullets.
2. Naturally incorporate missing skills if realistic.
3. Use ATS-friendly language.
4. Add measurable impact where possible.
5. Keep information truthful.
6. Do NOT invent jobs, projects or achievements.

Return ONLY the optimized resume text.
"""
    response = model.generate_content(prompt)

    return response.text.strip() if response and getattr(response, "text", None) else resume_text