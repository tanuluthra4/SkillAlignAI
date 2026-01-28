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
    return response.text 
