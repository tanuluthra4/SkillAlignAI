# SkillAlignAI 🚀  

An intelligent resume–job description alignment engine that evaluates candidate fit using **semantic skill matching, domain awareness, and explainable weighted scoring**.

---

## 🎯 Problem

Most hiring systems:
- ❌ Provide no feedback after rejection  
- ❌ Use naive keyword matching  
- ❌ Fail to capture real skill relationships  
- ❌ Do not explain *why* a candidate is rejected  

Result → Candidates cannot improve effectively.

---

## 💡 Solution

SkillAlignAI builds a **transparent ATS-style evaluation system** that:

- Separates **skills**, **domain**, and **scoring logic**
- Uses **semantic relationships (parent–child–sibling skills)**
- Applies **confidence-based weighted scoring**
- Generates **clear, structured rejection insights**

---

## ⚙️ Core Capabilities

- Resume + Job Description analysis (text or PDF)
- Semantic skill matching (not just keywords)
- Multi-layer scoring:
  - Required Match %
  - Preferred Match %
  - Domain Alignment %
- Confidence-based scoring (direct, inferred, fuzzy)
- Structured rejection analysis + suggestions

---

## 🧠 What Makes It Different

Unlike basic ATS clones, this system:

- ✅ Handles **skill hierarchies** (React → JavaScript)  
- ✅ Supports **sibling inference** (TensorFlow ↔ PyTorch)  
- ✅ Uses **confidence scoring** (1.0 / 0.5 / 0.3)  
- ✅ Separates **domain vs skill matching**  
- ✅ Prevents **false positives (Java ≠ JavaScript)**  
- ✅ Handles **typos using fuzzy matching**

---

## 🧮 Scoring Logic
```text
Base Score = 0.8 × Required Match + 0.2 × Preferred Match
Final Score = Base × (0.7 + 0.3 × Domain Match)
```

### Interpretation:
- **Required Match** → Core competency  
- **Preferred Match** → Competitive advantage  
- **Domain Match** → Contextual alignment  

---

## ⚡ Example Evaluation

**Input:**
``` text 
Resume: html, css, ml
JD: machine learning 
```

**Output:**
- Required Match: 0%  
- Domain Match: 100%  
- Final Score: 0%  

**Interpretation:**  
Candidate shows interest in ML domain but lacks required technical skills.

---

## 🏗️ System Architecture

### Pipeline
```text
Frontend → API → Parsing → Normalization → Matching → Scoring → Explanation → Response
```

### Modules

1. **Resume Parser** – Extracts skills, projects, and experience  
2. **JD Analyzer** – Identifies required and preferred skills  
3. **Normalization Layer** – Standardizes skill variations  
4. **Semantic Matching Engine** – Handles parent-child & sibling relationships  
5. **Scoring Engine** – Computes weighted alignment scores  
6. **Domain Detection Engine** – Extracts contextual domain from raw text  
7. **Explanation Generator** – Produces structured feedback  

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **AI Integration:** Gemini API  
- **Testing:** Pytest  
- **Utilities:** python-dotenv  

---

## 📁 Project Structure

```text
SkillAlignAI/
│
├── backend/
│   ├── .env
│   ├── agent_controller.py
│   ├── agents.py
│   ├── app.py
│   ├── contracts.py
│   ├── fallback_explainer.py
│   ├── gemini_client.py
│   ├── jd_analyzer.py
│   ├── rejection_engine.py
│   ├── rejection_report.py
│   ├── report_generator.py
│   ├── resume_parser.py
│   │
│   ├── utils/
│   │    ├── normalizer.py
│   │    ├── pdf_parser.py
│   │    ├── role_map.py
│   │    ├── skill_categories.py
│   │    ├── skill_map.py
│   │    └── skill_weights.py      
│   │
│   └── tests/
│       └── test_analyze_application.py
│
├── frontend/
│   ├── index.html              # User interface
│   ├── script.js               # API calls + UI logic
│   └── style.css               # Basic styling
│
├── docs/
│   ├── api_contract.md         # API request/response specification
│   ├── problem.md              # Problem definition
│   ├── user_flow.md            # User interaction flow
│   └── solution.md             # System design explanation
│
├── Procfile                    # Render deployment configuration
├── README.md
├── .gitignore
└── requirements.txt
```

---

## 🚀 Installation

```bash
git clone https://github.com/tanuluthra4/SkillAlignAI.git
cd SkillAlignAI
pip install -r requirements.txt
```

Create a .env file inside backend/ and configure required API keys.

## ▶️ Usage 

```bash
pip install -r requirements.txt
python -m backend.app 
```

Then open ```frontend/index.html``` in your browser 

### 🔌 API Endpoint 

POST/analyze

Request Body
```json
{
    "resume_text": "string",
    "job_description_text": "string"
}
```

Example Response 
```json
{
  "match_score": 76,
  "required_match": 70,
  "preferred_match": "N/A",
  "domain_match_percentage": "N/A",
  "matched_skills": ["python"],
  "missing_skills": [],
  "score_explanation": {
    "formula": "Base: 0.8 × required + 0.2 × preferred\nFinal: Base × (0.7 + 0.3 × domain)",
    "final_score": 76
  }
}
```

---

## 🌐 Live Demo

Frontend: https://skillalignai-1.onrender.com  
Backend API: https://skillalignai.onrender.com/analyze

---

## 📈 Roadmap

- 🔥 Embedding-based semantic matching (next upgrade)
- 📊 Multi-candidate comparison dashboard
- 📄 Advanced resume parsing (structured sections)
- 🤖 AI-generated interview insights
- 🔐 Authentication & recruiter panel

---

## 🧠 Key Learnings

- Importance of separating skills vs domain vs scoring
- Handling ambiguity in NLP pipelines
- Designing explainable AI systems
- Preventing bias and score inflation

---

## 🤝 Contribution

1. Fork the repository.
2. Create a feature branch: 
```bash
git checkout -b feature-name
```
3. Commit your changes: 
```bash 
git commit -m "Add feature"
```
4. Push to the branch: 
```bash 
git push origin feature-name
```
5. Open a pull request 

---

## 📌 Why This Project Matters 

Most job application systems provide little to no feedback after rejection. SkillAlignAI bridges this gap by:

- Explaining why a candidate may be rejected 
- Providing actionable improvement insights
- Simulating how ATS systems evaluate resumes 

This makes the system useful not only as a tool, but also as a learning aid for job seekers.