# SkillAlignAI

SkillAlignAI is an AI-powered tool that explains why a job application may be rejected based on **resume–job description alignment**. It identifies missing required skills, highlights limited skill coverage, and provides actionable suggestions to improve future applications.

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
├── frontend/               # Currently empty, can be used for UI later
├── docs/
│ ├── problem.md
│ ├── user_flow.md
│ └── solution.md
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

## Contributing 
1. Fork the repository.
2. Create a feature branch: git checkout -b feature-name
3. Commit your changes: git commit -m "Add feature"
4. Push to the branch: git push origin feature-name
5. Create a pull request 


