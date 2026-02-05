# SkillAlignAI - System Architecture & Decision Flow 

SkillAlignAI is a backend-first application that analyzes resume-job description alignment and explains rejection reasons using a deterministic core, optionally enhanced by AI. 

## High-Level Architecture 

The system is intentionally split into three layers: 

1. Extraction Layer 
2. Decision Layer 
3. Narration Layer (AI-optional)

This separation ensures explainability, testability, and graceful degradation when AI services are unavailable.

## 1. Extraction Layer 

Responsible for converting unstructured text into structured data. 

### Components 
- `resume_parser.py`
- `jd_analyzer.py`

### Responsibilities 
- Normalize input text 
- Extract skills using a controlled vocabulary 
- Avoid inference or guessing 

### Output 
```json 
{
    "skills": ["python", "flask", "sql"]
}
```

## 2. Decision Layer (Deterministic Core)
Responsible for all rejection logic 

### Components 
- `rejection_engine.py`
- `rejection_report.py`

### Responsibilities 
- Compute skill match percentage 
- Identify missing and weak skills 
- Generate a structured rejection report 
- Make decision without AI dependency 

### Output 
```json 
[
    {
        "reason": "Missing required skills",
        "severity": "High",
        "details": ["docker"]
    }
]
```

This layer defines truth in the system 

## 3. Narration Layer (Optional AI)
Responsible only for coverting structured decisions into human-readable explanations. 

### Components 
- `gemini_client.py`
- `fallback_explainer.py`

### Behavior 
- Uses Gemini AI when available 
- Falls back to deterministic explanation when AI fails 
- Never alters decisions 

This ensures system stability and explainability. 

## End-to-End Flow 

1. Resume and job description are received 
2. Skills are extracted deterministically 
3. Match percentage is calculated 
4. Rejection report is generated 
5. Explanation is produced (AI or fallback)
6. Structured response is returned to the client 

## Design Principles 

- Deterministic over probabilistic 
- Explainability over accuracy illusions 
- AI as enhancement, not authority 
- Clear contracts between layers 

## Why This Design Matters 

This architecture:
- Works without AI 
- Is fully testable 
- Is easy to extend (frontend, APIs, analytics)
- Holds up in technical interviews 

SkillAlignAI is designed as an engineering system, not a demo.  