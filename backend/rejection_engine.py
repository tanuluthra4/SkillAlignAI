from backend.rejection_report import build_rejection_report
from backend.fallback_explainer import generate_fallback_summary
from backend.utils.normalizer import normalize_skills, is_similar
from backend.utils.skill_weights import SKILL_WEIGHTS
from backend.utils.skill_categories import SKILL_CATEGORIES
from backend.utils.skill_map import expand_skills_with_confidence, REVERSE_SEMANTIC_MAP, SEMANTIC_SKILL_MAP

def get_weight(skill, role=None): 
    base_weight = SKILL_WEIGHTS.get(skill, 0.6) # default weight

    multiplier = 1.0

    if role:
        for category, skills in SKILL_CATEGORIES.items():
            if skill in skills:
                if role == category:
                    multiplier *= 1.5  # boost relevant skills
            
                else:
                    multiplier *= 0.7 # penalize irrelevant
        
    return base_weight * multiplier

def get_fuzzy_matches(resume_skills, jd_skills):
    matched = set()

    for jd_skill in jd_skills:
        for res_skill in resume_skills:
            if res_skill == jd_skill or is_similar(res_skill, jd_skill):
                matched.add(jd_skill)
                break

    return matched 

def get_skill_strength(skill, resume_data):
    strength = 1.0

    text = resume_data.get("raw_text", "")

    # frequency boost 
    freq = text.count(skill)
    if freq >= 3:
        strength *= 1.3
    elif freq == 2:
        strength *= 1.15

    # Project boost
    if skill in " ".join(resume_data.get("projects", [])):
        strength *= 1.5

    # Experience boost
    if skill in " ".join(resume_data.get("experience", [])):
        strength *= 2.0

    return strength

def compute_domain_alignment(resume_data, jd_data):
    resume_domains = set(resume_data.get("domain_skills", []))
    jd_domains = set(jd_data.get("domain_skills", []))

    if not jd_domains:
        return set(), None  # no domain constraint
    
    matched_domain_skills = resume_domains & jd_domains

    match = len(matched_domain_skills)
    total = len(jd_domains)

    return matched_domain_skills, (match / total)

def get_project_relevance(skill, resume_data, jd_data):
    relevance = 1.0

    projects = resume_data.get("projects", [])
    jd_skills = jd_data.get("required_skills", [])

    for project in projects:
        if skill in project:
            match_count = sum(1 for jd_skill in jd_skills if jd_skill in project)

            if match_count > 0:
                relevance *= (1+ 0.2 * match_count) # scalable boost
            else:
                relevance *= 1.1 # weak relevance

    return min(relevance, 2.0)

def compute_match_score(resume_data, jd_data): 
    resume_skill_map = expand_skills_with_confidence(
        normalize_skills(resume_data.get("skills", []))
    )
    resume_skills = set(resume_skill_map.keys())

    required_skills = set(
        normalize_skills(jd_data.get("required_skills", []))
    )

    preferred_skills = set(
        normalize_skills(jd_data.get("preferred_skills", []))
    )

    role = jd_data.get("role", None)

    matched_skills = set()

    for jd_skill in required_skills:

        # direct match
        if jd_skill in resume_skills:
            matched_skills.add(jd_skill)

        else:
            # reverse transfer check
            reverse = REVERSE_SEMANTIC_MAP.get(jd_skill)

            if reverse:
                parent_skill, confidence = reverse

                if parent_skill in resume_skills:
                    matched_skills.add(jd_skill)

                    # inject confidence for scoring
                    resume_skill_map[jd_skill] = confidence

            # sibling transfer check
            for parent, children in SEMANTIC_SKILL_MAP.items():
                if jd_skill in children:
                    for resume_skill in resume_skills:
                        if resume_skill in children:
                            matched_skills.add(jd_skill)

                            # assign sibling confidence
                            resume_skill_map[jd_skill] = max(
                                resume_skill_map.get(jd_skill, 0),
                                0.5   # sibling strength
                            )

            # fuzzy fallback (weakest signal)
            if jd_skill not in matched_skills:
                for resume_skill in resume_skills:
                    if get_fuzzy_matches(resume_skill, jd_skill) > 0.8:
                        matched_skills.add(jd_skill)

                        # low confidence
                        resume_skill_map[jd_skill] = max(
                            resume_skill_map.get(jd_skill, 0),
                            0.3   # weakest confidence
                        )

    matched_preferred_skills = set()

    for jd_skill in preferred_skills:

        # direct match
        if jd_skill in resume_skills:
            matched_preferred_skills.add(jd_skill)

        else:
            # reverse transfer check
            reverse = REVERSE_SEMANTIC_MAP.get(jd_skill)

            if reverse:
                parent_skill, confidence = reverse

                if parent_skill in resume_skills:
                    matched_preferred_skills.add(jd_skill)

                    # inject confidence for scoring
                    resume_skill_map[jd_skill] = confidence

            # sibling transfer check
            for parent, children in SEMANTIC_SKILL_MAP.items():
                if jd_skill in children:
                    for resume_skill in resume_skills:
                        if resume_skill in children:
                            matched_preferred_skills.add(jd_skill)

                            # assign sibling confidence
                            resume_skill_map[jd_skill] = max(
                                resume_skill_map.get(jd_skill, 0),
                                0.5   # sibling strength
                            )
                
                # fuzzy fallback (weakest signal)
                if jd_skill not in matched_preferred_skills:
                    for resume_skill in resume_skills:
                        if get_fuzzy_matches(resume_skill, jd_skill) > 0.8:
                            matched_preferred_skills.add(jd_skill)

                            # low confidence
                            resume_skill_map[jd_skill] = max(
                                resume_skill_map.get(jd_skill, 0),
                                0.3   # weakest confidence
                            )

    total_required_weight = sum(
        get_weight(s, role)
        * 1.0
        * get_skill_strength(s, resume_data)
        * get_project_relevance(s, resume_data, jd_data)
        for s in required_skills
    )
    matched_required_weight = sum(
        get_weight(s, role) 
        * resume_skill_map.get(s, 0)
        * get_skill_strength(s, resume_data)
        * get_project_relevance(s, resume_data, jd_data)
        for s in matched_skills
    )

    total_preferred_weight = sum(
        get_weight(s, role) 
        * resume_skill_map.get(s, 0)
        * get_skill_strength(s, resume_data) 
        * get_project_relevance(s, resume_data, jd_data)
        for s in preferred_skills
    )
    matched_preferred_weight = sum(
        get_weight(s, role) 
        * get_skill_strength(s, resume_data)
        * get_project_relevance(s, resume_data, jd_data)
        for s in matched_preferred_skills
    )

    required_match = 0
    preferred_match = None

    if required_skills:
        required_match = matched_required_weight / total_required_weight
    else:
        required_match = 1

    if preferred_skills:
        preferred_match = matched_preferred_weight / total_preferred_weight
    else:
        preferred_match = None

    matched_domain_skills, domain_match = compute_domain_alignment(resume_data, jd_data)

    if preferred_match is not None:
        base_score = (
            0.8 * required_match + 
            0.2 * preferred_match
        )
    else:
        base_score = required_match

    if domain_match is not None:
        match_score = base_score * (0.7 + 0.3 * domain_match)
    else:
        match_score = base_score

    required_match_percentage = int(required_match * 100)
    
    if preferred_match is not None:
        preferred_match_percentage = int(preferred_match * 100)
    else:
        preferred_match_percentage = "N/A"
    match_percentage = int(match_score * 100)

    if domain_match is not None:
        domain_match_percentage = int(domain_match * 100)
    else:
        domain_match_percentage = "N/A"

    score_explanation = {
        "formula": "Base: 0.8 × required + 0.2 × preferred\nFinal: Base × (0.7 + 0.3 × domain)",
        "required_match": required_match_percentage,
        "preferred_match": preferred_match_percentage,
        "domain_match_percentage": domain_match_percentage,
        "final_score": match_percentage
    }

    missing_skills = list(required_skills - resume_skills)
    missing_preferred_skills = list(preferred_skills - resume_skills)

    return {
        "match_score": match_percentage,
        "required_match": required_match_percentage,
        "preferred_match": preferred_match_percentage,
        "domain_match_percentage": domain_match_percentage,
        "matched_skills": list(matched_skills),
        "matched_preferred_skills": list(matched_preferred_skills),
        "matched_domain_skills": list(matched_domain_skills),
        "missing_skills": missing_skills,
        "missing_preferred_skills": missing_preferred_skills,
        "score_explanation": score_explanation
    }

def generate_rejection_data(score_data):
    match_percentage = score_data["match_score"]

    missing_skills = score_data["missing_skills"]
    missing_preferred_skills = score_data["missing_preferred_skills"]

    weak_skills = []

    rejection_report = build_rejection_report(
        match_percentage, 
        missing_skills,
        missing_preferred_skills,
        weak_skills
    )

    try:
        rejection_summary = generate_fallback_summary(rejection_report)
    except Exception:
        rejection_summary = "Could not generate summary"

    improvement_suggestions = [
        f"Add or strengthen experience in {skill}"
        for skill in missing_skills
    ]

    improvement_suggestions += [
        f"Learning {skill} could improve competitiveness"
        for skill in missing_preferred_skills
    ]

    failure_analysis = generate_failure_analysis(score_data)
    impact_metrics = generate_impact_metrics(score_data)

    return {
        "rejection_report": rejection_report,
        "rejection_summary": rejection_summary,
        "improvement_suggestions": improvement_suggestions,
        "failure_analysis": failure_analysis,
        "impact_metrics": impact_metrics
    }

def generate_failure_analysis(score_data):
    missing_required = score_data.get("missing_skills", [])
    missing_preferred = score_data.get("missing_preferred_skills", [])
    match = score_data.get("match_score", 0)

    if missing_required:
        return {
            "primary_reason": "Core skill gap",
            "impact": "High",
            "confidence": f"{min(100, match + 20)}%",
            "explanation": ( 
                f"The candidate lacks mandatory skills required to perform the role effectively."
                f"Missing: {', '.join(missing_required)}"
            ),
            "fix_action": f"Focus on learning: {', '.join(missing_required)}",
            "priority": 1
        }

    elif missing_preferred:
        return {
            "primary_reason": "Competitive disadvantage",
            "impact": "Medium",
            "confidence": f"{min(100, match + 10)}%",
            "explanation": (
                "The candidate meets core requirements but lacks preferred skills that increase competitiveness."
                f"Missing: {', '.join(missing_preferred)}"
            ),
            "fix_action": f"Improve profile by adding: {', '.join(missing_preferred)}",
            "priority": 2
        }

    else:
        return {
            "primary_reason": "Strong alignment",
            "impact": "Low",
            "confidence": f"{match}%",
            "explanation": "Candidate aligns well with job requirements",
            "fix_action": "No major improvements needed.",
            "priority": 3
        }
    
def generate_impact_metrics(score_data):
    score = score_data.get("match_score", 0)

    # Hire Probability
    hire_probability = f"{min(95, max(5, score + 10))}%"

    # Resume Strength
    if score >= 75:
        strength = "Strong"
    elif score >= 50:
        strength = "Moderate"
    else:
        strength = "Weak"

    # Risk Level 
    if score >= 75:
        risk = "Low"
    elif score >= 50:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "hire_probability": hire_probability,
        "resume_strength": strength,
        "risk_level": risk
    }