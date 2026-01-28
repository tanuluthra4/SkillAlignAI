from flask import Flask, request, jsonify
from gemini_client import generate_explanation
from resume_parser import extract_resume_info
from jd_analyzer import extract_jd_requirements
from rejection_engine import analyze_rejection

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    # 1. Get input 
    data = request.get_json(force=True)
    resume_text = data.get("resume", "")
    job_description = data.get("job_description", "")

    if not resume_text or not job_description:
        return jsonify({
            "error": "resume and job_description are required"
        }), 400

    # 2. Parse resume and JD
    resume_data = extract_resume_info(resume_text)
    jd_data = extract_jd_requirements(job_description)

    # 3. Rule-based rejection 
    rejection_reasons = analyze_rejection(resume_data, jd_data)

    # 4. Gemini explanation 
    ai_explanation = generate_explanation(resume_data, jd_data, rejection_reasons)

    # 5. Return full response 
    return jsonify({
        "rejection_reasons": rejection_reasons,
        "ai_explanation": ai_explanation
    })

if __name__ == "__main__":
    app.run(debug=True)