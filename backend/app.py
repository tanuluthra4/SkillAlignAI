from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.utils.pdf_parser import extract_text_from_pdf
from backend.agent_controller import run_pipeline

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
 
    data = request.get_json(force=True)
    resume_text = data.get("resume_text")
    job_description_text = data.get("job_description_text")

    if not resume_text or not job_description_text:
        return jsonify({
            "error": "resume and job_description_text must not be empty"
        }), 400

    try: 
        result = run_pipeline(resume_text, job_description_text)
        return jsonify(result), 200
    
    except Exception:
        return jsonify({
            "error": "An internal error occurred while analyzing the application."
        }), 500
    
@app.route("/upload_resume", methods=["POST"])
def upload_resume():

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
        resume_text = extract_text_from_pdf(file)

        return jsonify({
            "resume_text": resume_text
        }), 200
    
    except Exception:
        return jsonify({
            "error": "failed to process PDF"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)