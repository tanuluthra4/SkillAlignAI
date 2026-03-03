# SkillAlignAI

Explainable resume–job description alignment engine that generates structured rejection feedback via a REST API

## Problem Statement 

Job applicants often receive rejection emails without any explanation of which skills caused the rejection. Recruiter feedback is usually unavailable or generic, making it difficult for candidates to understand gaps in their resumes and improve future applications. This project addresses the lack of structured, explanable feedback for resume-job description mismatches. 

## What This Project Does (System Output)

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

## System Architecture

SkillAlignAI follows a modular pipeline:

1. **Resume Parser** – Extracts technical and role-specific skills from candidate resumes.
2. **Job Description Analyzer** – Identifies required and preferred skills from job postings.
3. **Skill Matching Engine** – Computes overlap, highlights missing/weak skills, and assigns severity levels.
4. **Rejection Explanation Generator** – Produces structured, human-readable feedback using deterministic logic + AI-assisted phrasing.
5. **Backend API Layer** – Exposes endpoints for resume/job analysis and integrates with a future frontend UI.

### Data Flow
```text
Frontend → REST API → Parsing → Skill Matching → Explanation → JSON Response → Frontend
```

### Tech Stack
- **Backend:** Python, Flask
- **AI Integration:** Gemini API
- **Frontend:** HTML, CSS, JavaScript (Fetch API)
- **Testing:** Pytest
- **Configuration:** python-dotenv

### Design Priorities
- Deterministic skill matching for transparency
- AI-assisted language generation for clarity
- Modular components for scalability

## Overview 

SkillAlignAI is designed to explain why a job application may be rejected based on **resume–job description alignment**. Instead of providing generic feedback, it produces structured explanations highlighting missing skills, limited skill coverage, and improvement areas.  

The system prioritizes explainability and determinism in skill matching while using AI-assisted language generation only for explanation clarity. 

## Features

- Detects **missing required skills** and assigns severity levels.
- Highlights **secondary factors** affecting application success.
- Provides **clear, professional, and actionable advice** for candidates.
- Generates explanations in **plain, understandable language**.

## Folder Structure

```text
SkillAlignAI/
|
├── backend/
│ ├── .env
│ ├── app.py
| ├── contracts.py
| ├── fallback_explainer.py
│ ├── gemini_client.py
│ ├── jd_analyzer.py
│ ├── rejection_engine.py
| ├── rejection_report.py
│ ├── resume_parser.py
| └── tests/
│       └── test_analyze_application.py  
| 
├── frontend/
│ ├── index.html       
│ ├── script.js         
│ └── style.css  
|            
├── docs/
| ├── api_contract.md       # Structure and API behavior 
│ ├── problem.md            # Detailed problem analysis 
│ ├── user_flow.md          # User interaction flow 
│ └── solution.md           # System design explanation 
| 
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

Create a .env file inside backend/ and configure required API keys.

## Usage 

### Running Locally 

```bash
pip install -r requirements.txt
python -m backend.app 
```

Then open ```frontend/index.html``` in your browser 

### API Endpoint 

POST/analyze

Request Body
```json
{
    "resume_text": "string",
    "job_description_text": "string"
}
```

Example Response 
```json
{
  "match_percentage": 68,
  "missing_skills": ["Docker", "AWS"],
  "weak_skills": ["System Design"],
  "explanation": "Your resume demonstrates strong alignment with the role, but lacks experience in Docker and AWS. System Design is mentioned but needs more depth."
}
```

### Workflow

1. Upload or paste your resume text. 
2. Provide the job description text.
3. The backend analyzes both and returns:
- Match Percentage - overall alignment score 
- Missing Skills - critical gaps 
- Weak Skills - areas needing improvement 
- Explanation - human-readable feedback

## Documentation 

The docs/ folder contains system-level documentation and API specifications:

- api_contract.md: Defines request/response structure and API behavior
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

## Roadmap 

- Deploy backend (Render/Railway)
- Deploy frontend (Vercel)
- Add authentication layer 
- Add resume file upload (PDF parsing)
- Add skill weighting system 
- Add dashboard with match analytics 