from flask import Flask, request, jsonify
from rejection_engine import analyze_application

app = Flask(__name__)

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
        result = analyze_application(resume_text, job_description_text)
        return jsonify(result), 200
    
    except Exception:
        return jsonify({
            "error": "An internal error occurred while analyzing the application."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)