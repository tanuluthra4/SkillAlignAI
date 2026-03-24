def generate_report(data): 
    return {
        "candidate_evaluation": {
            "decision": data.get("decision"),
            "match_percentage": data.get("match_percentage"),
            "required_match": data.get("required_match_percentage"),
            "preferred_match": data.get("preferred_match_percentage")
        },
        "skill_analysis": {
            "matched_required": data.get("matched_skills", []),
            "matched_preferred": data.get("matched_preferred_skills", []),
            "missing_required": data.get("missing_skills", []),
            "missing_preferred": data.get("missing_preferred_skills", [])
        },
        "failure_analysis": data.get("failure_analysis", {}),
        "impact_metrics": data.get("impact_metrics", {}),
        "recommendations": data.get("improvement_suggestions", []),
        "explanation": data.get("rejection_summary", "")
    }