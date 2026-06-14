from fastapi import logger
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.utils.pdf_parser import extract_text_from_pdf
from backend.agent_controller import run_pipeline
from backend.gemini_client import rewrite_resume_bullet, optimize_resume

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

CORS(app)
logger.info("SkillAlignAI server started.")

@app.route("/analyze", methods=["POST"])
def analyze():
    logger.info("/analyze endpoint called")
 
    data = request.get_json(force=True)
    resume_text = data.get("resume_text")
    job_description_text = data.get("job_description_text")

    resume_text = resume_text or ""
    job_description_text = job_description_text or ""

    result = run_pipeline(resume_text, job_description_text)
    logger.info(
        f"Analysis completed. Match score: {result.get('match_percentage')}%"
    )

    if result.get("decision") == "Failed":
        return jsonify(result), 400
    
    return jsonify(result), 200
    
@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    logger.info("/upload_resume endpoint called")

    if "resume_file" not in request.files:
        return jsonify({
            "error": "No file provided"
        }), 400
    
    file = request.files["resume_file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400
    
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Only PDF files are supported"
        }), 400
    
    try:
        logger.info(
            f"Resume uploaded: {file.filename}"
        )
        resume_text = extract_text_from_pdf(file)

        return jsonify({
            "resume_text": resume_text
        }), 200
    
    except Exception:
        logger.exception(
            "Error occurred in /upload_resume"
        )

        return jsonify({
            "error": "Failed to process PDF file"
        }), 500
    
@app.route("/rewrite_bullet", methods=["POST"])
def rewrite_bullet():
    logger.info("/rewrite_bullet endpoint called")

    data = request.get_json(force=True)

    bullet = data.get("bullet", "")
    target_role = data.get("target_role", "")

    if not bullet.strip():
        return jsonify({
            "error": "Bullet text is required"
        }), 400

    try:
        rewritten = rewrite_resume_bullet(
            bullet,
            target_role
        )

        return jsonify({
            "original": bullet,
            "rewritten": rewritten
        }), 200

    except Exception:
        logger.exception(
            "Error occurred in /rewrite_bullet"
        )

        return jsonify({
            "error": "Internal Server Error"
        }), 500
    
@app.route("/optimize_resume", methods=["POST"])
def optimize_resume_route():
    logger.info("/optimize_resume endpoint called")
    data = request.get_json(force=True)

    resume_text = data.get("resume_text", "")
    job_description_text = data.get("job_description_text", "")

    try:
        analysis = run_pipeline(resume_text, job_description_text)
        missing_skills = analysis.get("missing_skills", [])

        optimized_resume, bullet_changes = optimize_resume(
            resume_text,
            job_description_text,
            missing_skills
        )

        logger.info(
            "Resume optimization completed successfully."
        )

        return jsonify({
            "optimized_resume": optimized_resume,
            "missing_skills": missing_skills,
            "bullet_changes": bullet_changes or []
        }), 200

    except Exception:
        logger.exception(
            "Error occurred in /optimize_resume"
        )

        return jsonify({
            "error": "Internal Server Error"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)