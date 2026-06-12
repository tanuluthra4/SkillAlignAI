from backend.agents import (
    resume_agent, 
    jd_agent,
    scoring_agent,
    decision_agent,
    explanation_agent,
    validation_agent,
    recovery_agent
)
from backend.report_generator import generate_report

def run_pipeline(resume_text, jd_text):
    agent_trace = []

    try:
        # 1. Resume Agent 
        resume_data = resume_agent(resume_text)
        agent_trace.append({
            "agent": "ResumeAgent",
            "output": resume_data
        })
        
        # 2. JD Agent 
        jd_data = jd_agent(jd_text)
        agent_trace.append({
            "agent": "JDAgent",
            "output": jd_data
        })

        # 3. Validation Agent
        validation = validation_agent(resume_data, jd_data)
        agent_trace.append({
            "agent": "ValidationAgent",
            "output": validation
        })

        # 4. Conditional Recovery 
        if not validation["is_valid"]:
            recovery = recovery_agent(resume_data, jd_data, validation)
            agent_trace.append({
                "agent": "RecoveryAgent",
                "output": recovery.get("actions", [])
            })

            resume_data = recovery["resume_data"]
            jd_data = recovery["jd_data"]

        # 5. Scoring Agent 
        score_data = scoring_agent(resume_data, jd_data)
        score_data["role"] = jd_data.get("role")
        agent_trace.append({
            "agent": "ScoringAgent",
            "output": score_data
        })

        # 6. Confidence-based Recheck 
        if score_data.get("match_score", 0) < 20:
            agent_trace.append ({
                "agent": "ReevaluationAgent",
                "output": "Low confidence score detected"
            })

        # 7. Decision Agent 
        decision_data = decision_agent(score_data)
        agent_trace.append({
            "agent": "DecisionAgent",
            "output": decision_data
        })

        # 8. Explanation Agent 
        explanation_data = explanation_agent(resume_data, jd_data, score_data, decision_data)
        agent_trace.append({
            "agent": "ExplanationAgent",
            "output": explanation_data
        })

        # Final Response 
        final_output = {
            "decision": decision_data["decision"],

            "match_percentage": score_data.get("match_score", 0),
            "required_match_percentage": score_data.get("required_match", 0),
            "preferred_match_percentage": score_data.get("preferred_match", 0),
            "domain_match_percentage": score_data.get("domain_match_percentage", 0),

            "skill_contributions": score_data.get("skill_contributions", []),
            "score_explanation": score_data.get("score_explanation", {}),

            "matched_skills": score_data.get("matched_skills", []),
            "matched_preferred_skills":score_data.get("matched_preferred_skills", []),
            "matched_domain_skills": score_data.get("matched_domain_skills", []),
            
            "missing_skills": score_data.get("missing_skills", []),
            "missing_preferred_skills": score_data.get("missing_preferred_skills", []),

            "rejection_summary": explanation_data.get("summary", ""),
            "rejection_report": explanation_data.get("rejection_report", []),
            "improvement_suggestions": explanation_data.get("improvement_suggestions", []),
            "resume_enhancement_suggestions": explanation_data.get("resume_enhancement_suggestions", []),
            "failure_analysis": explanation_data.get("failure_analysis", {}),
            "impact_metrics": explanation_data.get("impact_metrics", {}),

            "agent_trace": agent_trace
        }

        final_output["export_report"] = generate_report(final_output)
        
        return final_output
    
    except Exception as e:
        return {
            "decision": "Failed",
            "error": str(e),
            "agent_trace": agent_trace
        }