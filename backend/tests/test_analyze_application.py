from backend.rejection_engine import analyze_application

def test_analyze_application_basic():
    resume_text = "Python developer with experience in Flask and SQL."
    job_description_text = "Looking for a Python developer with Flask, Docker, and SQL skills"

    result = analyze_application(resume_text, job_description_text)

    assert isinstance(result, dict)
    assert "match_percentage" in result 
    assert "weak_skills" in result 
    assert "rejection_summary" in result 
    assert "improvement_suggestions" in result 

    assert isinstance(result["match_percentage"], int)
    assert isinstance(result["missing_skills"], list)

    assert result["match_percentage"] == 75
    assert "docker" in result["missing_skills"]
    assert len(result["missing_skills"]) == 1
    assert any("docker" in s for s in result["improvement_suggestions"])

def test_no_required_skills_in_jd():
    resume_text = "Python developer with Flask experience"
    job_description_text = "We are hiring passionate engineers"

    result = analyze_application(resume_text, job_description_text)

    assert result["match_percentage"] == 0
    assert result["missing_skills"] == []
    assert isinstance(result["rejection_summary"], str)