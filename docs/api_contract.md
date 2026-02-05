# SkillAlignAI - API Contract 

## Endpoint  
POST /analyze 

## Request Schema 
The API accepts plain text input for both resume and job description 

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
    "missing_skills": ["Docker", "System Design"],
    "weak_skills": ["Python"],
    "rejection_summary": "The resume does not sufficiently match tha required skills for the role.",
    "improvement_suggestions": [
        "Add hands-on experience with Docker",
        "Include system design related projects"
    ]
}
```

### Field Description 
- match_percentage: Integer value (0-100) indicating skill overlap. 
- missing_skills: Skills required by the job description but absent in the resume. 
- weak_skills: Skills mentioned in the resume but with insufficient depth. 
- rejection_summary: Human-readable explanation of rejection reasons. 
- improvement_suggestions: Actionable steps to improve future applications.  

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

## Notes
- This API is backend-only and does not handle file uploads.    
- Skill extraction logic is deterministic; AI is used only for explanation generation. 
- The response structure is guaranteed and stable.  
