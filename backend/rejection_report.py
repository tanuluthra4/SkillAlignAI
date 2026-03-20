def build_rejection_report(match_percentage, missing_skills, missing_preferred_skills, weak_skills):
    reasons = []

    if missing_skills:
        reasons.append({
            "reason": "Missing required skills",
            "severity": "High",
            "details": missing_skills
        })

    if match_percentage < 50: 
        reasons.append({
            "reason": "Low overall skill match", 
            "severity": "High", 
            "details": f"Only {match_percentage}% of required skills matched"
        })

    if weak_skills:
        reasons.append({
            "reason": "Weak skill coverage", 
            "severity": "Medium", 
            "details": weak_skills
        })

    if missing_preferred_skills:
        reasons.append({
            "reason": "Missing Preferred Skills",
            "severity": "Medium",
            "details": missing_preferred_skills
        })

    if not reasons:
        reasons.append({
            "reason": "Profile is generally aligned",
            "severity": "Low",
            "details": []
        })

    return reasons