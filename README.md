# SkillAlignAI

## Problem Statement 

Job applicants often receive rejection emails without any explanation of which skills caused the rejection. Recruiter feedback is usually unavailable or generic, making it difficult for candidates to understand gaps in their resumes and improve future applications. This project addresses the lack of structured, explanable feedback for resume-job description mismatches. 

## What This Project Does (Guaranteed Output)

- Accepts a resume and a job description as input  
- Extracts relevant technical and role-specific skills from both inputs   
- Computes a skill match percentage based on skill overlap  
- Identifies missing and weak skills required by the job description  
Generates a structured, human-readable rejection explanation with actionable improvement suggestions    

## What This Project Does Not DO 

- Does not rank candidates against other applicants   
- Does not predict hiring or interview outcomes  
- Does not auto-apply to jobs  
- Does not replace recruiter or ATS decision-making  
- Does not guarantee job selection or interviews  

## High-Level Architecture 

- Resume Parser 
- Job Description Analyzer  
- Skill Matching Engine  
- Rejection Explanation Generator  
- Backend API Layer  

## Overview 

SkillAlignAI is a backend-focused project designed to explain why a job application may be rejected based on **resume–job description alignment**. Instead of providing generic feedback, it produces structured explanations highlighting missing skills, limited skill coverage, and improvement areas.  

The system prioritizes explainability and determinism in skill matching while using AI-assisted language generation only for explanation clarity. 

## Features

- Detects **missing required skills** and assigns severity levels.
- Highlights **secondary factors** affecting application success.
- Provides **clear, professional, and actionable advice** for candidates.
- Generates explanations in **plain, understandable language**.

## Folder Structure

```text
SkillAlignAI/
├── backend/
│ ├── .env
│ ├── app.py
│ ├── gemini_client.py
│ ├── jd_analyzer.py
│ ├── rejection_engine.py
│ └── resume_parser.py
├── frontend/               # Placeholder for future UI
├── docs/
│ ├── problem.md            # Detailed problem analysis 
│ ├── user_flow.md          # User interaction flow 
│ └── solution.md           # System design explanation  
├── README.md
├── .gitignore
└── requirements.txt
```


## Installation

```bash
git clone https://github.com/tanuluthra4/SkillAlignAI.git
cd SkillAlignAI
pip install -r requirements.txt
```

⚠️ Make sure to create a .env file in the backend/ folder with your API keys and configuration before running the project.

## Usage 

```text
# 1. Place your resume file and job description file in appropriate folder.
# 2. Run the backend server: 
cd backend
python app.py
```
```text
# 3. Use the API (or frontend, once implemented) to analyze applications:
from rejection_engine import generate_explanation
response = generate_explanation(resume_data, jd_data, rejection_reasons)
print(response)
```

## Documentation 

Detailed design decisions and flows are available in the docs/ folder: 

- problem.md: problem definition and motivation 
- solution.md: system approach and reasoning 
- user_flow.md: end-to-end user interaction flow  

## Contribution
1. Fork the repository.
2. Create a feature branch: 
```bash
git checkout -b feature-name
```
3. Commit your changes: 
```bash 
git commit -m "Add feature"
```
4. Push to the branch: 
```bash 
git push origin feature-name
```
5. Open a pull request 


