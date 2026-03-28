# 🚀 SkillAlignAI — API Contract 

## 📌 Overview

SkillAlignAI provides an explainable resume–job matching API that evaluates candidate fit using semantic skill matching, weighted scoring, and AI-generated feedback.

## 🔗 Endpoint 
``` 
POST /analyze 
```

## Request Schema 
The API accepts plain text input for both resume (Extracts text content from a PDF resume for further analysis) and job description 

```json
{
    "resume_text": "string",
    "job_description_text": "string"
}
```

### Field Description 
- resume_text: Full resume content in plain text format 
- job_description_text: Full job description content in plain text format  

## Response Schema 
The API returns a structured analysis explaining resume-job description alignment.   
```json 
{
    "match_percentage": 72,
    "required_match_percentage": 65,
    "preferred_match_percentage": 80,
    "domain_match_percentage": 70,

    "matched_skills": ["Python", "SQL"],
    "missing_skills": ["Docker", "System Design"],
    "missing_preferred_skills": ["Kubernetes"],

    "decision": "Borderline",

    "impact_metrics": {
        "hire_probability": "Medium",
        "resume_strength": "Moderate",
        "risk_level": "Medium"
    },

    "failure_analysis": {
        "primary_reason": "Missing required skill: Docker",
        "impact": "High impact on shortlisting",
        "confidence": "High"
    },

    "rejection_summary": "The candidate lacks key required skills such as Docker and has only partial alignment with the job requirements. While some core skills are present, the absence of critical tools reduces overall competitiveness.",

    "improvement_suggestions": [
        "Gain hands-on experience with Docker",
        "Add system design projects",
        "Highlight relevant backend experience"
    ]
}
```

## 📊 Key Capabilities

- ✅ Weighted Scoring Model: Combines required, preferred, and domain skill alignment
- ✅ Explainable AI Feedback: Generates human-readable rejection reasoning
- ✅ Failure Analysis Engine: Identifies primary rejection cause and impact
- ✅ Skill Gap Detection: Highlights missing and weak areas  

## Error Handling 

### 400 - Bad Request 
Returned when input validation fails.   

Causes:    
- Empty resume text   
- Empty job description text   
- Missing required fields  

Example:   
```json 
{
    "error": "Resume text and job description text must not be empty."
}
```

### 422 - Unprocessable Entity 
Returned when input format is unsupported or cannot be processed.    

Example:    
```json
{
    "error": "Unsupported input format."
}
```

### 500 - Internal Server Error 
Returned when an unexpected error occurs during processing. 

Example: 
```json
{
    "error": "An internal error occured while analyzing the applicaton."
}
```

## 🧠 Notes
- The system uses deterministic skill extraction + AI explanation layer
- Response structure is stable and production-ready
- Designed for ATS systems, hiring platforms, and candidate feedback tools
