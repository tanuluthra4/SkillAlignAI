from backend.agents import (
    resume_agent, 
    jd_agent,
    scoring_agent,
    decision_agent,
    explanation_agent
)

def run_pipeline(resume_text, jd_text):
    agent_trace = []

    try:
        # 1. Resume Agent 
        resume_data = resume_agent(resume_text)
        agent_trace.append({
            "agent": "ResumeAgent",
            "output": resume_data
        })

        if "error" in resume_data:
            return {
                "decision": "Failed",
                "error": resume_data["error"],
                "agent_trace": agent_trace
            }
        
        # 2. JD Agent 
        jd_data = jd_agent(jd_text, resume_text)
        agent_trace.append({
            "agent": "JDAgent",
            "output": jd_data
        })

        # 3. Scoring Agent 
        score_data = scoring_agent(resume_data, jd_data)
        agent_trace.append({
            "agent": "ScoringAgent",
            "output": score_data
        })

        # 4. Decision Agent 
        decision_data = decision_agent(score_data)
        agent_trace.append({
            "agent": "DecisionAgent",
            "output": decision_data
        })

        # 5. Explanation Agent 
        explanation_data = explanation_agent(score_data, decision_data)
        agent_trace.append({
            "agent": "ExplanationAgent",
            "output": explanation_data
        })

        # Final Response 
        return {
            "decision": decision_data["decision"],

            "match_percentage": score_data.get("match_score", 0),
            "required_match_percentage": score_data.get("required_match", 0),
            "preferred_match_percentage": score_data.get("preferred_match", 0),

            "matched_skills": score_data.get("matched_skills", []),
            "missing_skills": score_data.get("missing_skills", []),
            "missing_preferred_skills": score_data.get("missing_preferred_skills", []),

            "rejection_summary": explanation_data.get("summary", ""),
            "rejection_report": explanation_data.get("rejection_report", []),
            "improvement_suggestions": explanation_data.get("improvement_suggestions", []),

            "agent_trace": agent_trace
        }
    
    except Exception as e:
        return {
            "decision": "Failed",
            "error": str(e),
            "agent_trace": agent_trace
        }