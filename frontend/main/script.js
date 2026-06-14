const analyzeBtn = document.getElementById("analyzeBtn");
const optimizeBtn = document.getElementById("optimizeResumeBtn");
const downloadBtn = document.getElementById("downloadReport");
let allCandidates = [];

const BASE_URL =
    window.location.hostname === "127.0.0.1" ||
        window.location.hostname === "localhost"
        ? "http://127.0.0.1:5000"
        : "https://skillalignai.onrender.com";

const fileInput = document.getElementById("resumeFile");
const fileName = document.getElementById("fileName");

const sampleResumeBtn = document.getElementById("sampleResumeBtn");
const sampleJdBtn = document.getElementById("sampleJdBtn");

const sampleResumeText = `
Tanu Luthra
B.Tech Computer Science Engineering Student

Skills:
Python, C++, MySQL, Flask, Git, GitHub, Data Structures, Algorithms, OOP, SQLite

Projects:
Built SkillAlignAI – Resume–JD Matching Engine using NLP and semantic skill matching.
Developed JINI – AI-based desktop assistant using Python and Gemini API.
Created Command-Line Job Scheduler using C++ with recurring task execution.

Experience:
AWS APAC Solutions Architecture Job Simulation (Forage)

Education:
B.Tech CSE – J.C. Bose University of Science and Technology, YMCA
CGPA: 8.89
`;

const sampleJdText = `
Software Engineering Intern (Backend)

Requirements:
Strong knowledge of Python and object-oriented programming
Understanding of REST APIs and backend development
Experience with databases like MySQL or SQLite
Knowledge of Git/GitHub and debugging skills
Good understanding of Data Structures and Algorithms

Preferred:
Experience with Flask, automation tools, and problem-solving mindset
`;

if (sampleResumeBtn) {
    sampleResumeBtn.addEventListener("click", function () {
        document.getElementById("resume").value = sampleResumeText;
    });
}

if (sampleJdBtn) {
    sampleJdBtn.addEventListener("click", function () {
        document.getElementById("job").value = sampleJdText;
    });
}

if (fileInput && fileName) {
    fileInput.addEventListener("change", function () {
        fileName.textContent = this.files[0]
            ? this.files[0].name
            : "No file selected";
    });
}

const errorBox = document.getElementById("error-message");

errorBox.style.display = "none";

analyzeBtn.addEventListener("click", async function () {

    errorBox.style.display = "none";
    errorBox.textContent = "";

    let resumeText = document.getElementById("resume").value;
    const jobText = document.getElementById("job").value;
    const resumeFile = document.getElementById("resumeFile").files[0];
    const reportList = document.getElementById("reportList")

    if (reportList) {
        reportList.innerHTML = "";
    }
    document.getElementById("explanation").textContent = "";
    const auditTrailEl = document.getElementById("auditTrail");
    if (auditTrailEl) {
        auditTrailEl.innerHTML = "";
    }

    document.getElementById("result").style.opacity = "0.2";
    document.getElementById("loaderOverlay").classList.remove("hidden");

    try {
        if (resumeFile) {
            const formData = new FormData();
            formData.append("resume_file", resumeFile);

            const uploadResponse = await fetch(`${BASE_URL}/upload_resume`, {
                method: "POST",
                body: formData
            });

            const uploadData = await uploadResponse.json();

            if (!uploadResponse.ok) {
                errorBox.textContent = uploadData.error;
                errorBox.style.display = "block";

                document.getElementById("loaderOverlay")
                    .classList.add("hidden");

                document.getElementById("result")
                    .style.opacity = "1";

                return;
            }

            resumeText = uploadData.resume_text;
        }

        const response = await fetch(`${BASE_URL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                resume_text: resumeText,
                job_description_text: jobText
            })
        });

        const data = await response.json();

        if (!response.ok) {
            errorBox.textContent = data.error;
            errorBox.style.display = "block";

            document.getElementById("loaderOverlay")
                .classList.add("hidden");

            document.getElementById("result")
                .style.opacity = "1";

            return;
        }

        document.getElementById("loaderOverlay")
            .classList.add("hidden");

        document.getElementById("result")
            .style.opacity = "1";

        displayResult(data);

        document.getElementById("result")
            .scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        console.log("FULL RESPONSE:", data);
        if (!response.ok) {
            document.getElementById("loaderOverlay").classList.add("hidden");
            document.getElementById("result").style.opacity = "1";

            const auditTrail = document.getElementById("auditTrail");

            if (auditTrail) {
                auditTrail.innerHTML = "";

                (data.audit_trail || []).forEach(step => {
                    const li = document.createElement("li");
                    li.textContent = step;
                    auditTrail.appendChild(li);
                });
            }
            return;
        }

        document.getElementById("loaderOverlay").classList.add("hidden");
        document.getElementById("result").style.opacity = "1";
        displayResult(data);

        window.latestData = data;

        // store candidate 
        allCandidates.push({
            name: `Candidate ${allCandidates.length + 1}`,
            score: data.match_percentage,
            decision: data.decision,
            missing: data.missing_skills,
            data: data
        });

    } catch (error) {
        document.getElementById("loaderOverlay").classList.add("hidden");
        document.getElementById("result").style.opacity = "1";

        console.error(error)

        return;
    }

});

optimizeBtn.addEventListener("click", async function () {
    const resumeText = document.getElementById("resume").value;
    const jobText = document.getElementById("job").value;

    const response = await fetch(`${BASE_URL}/optimize_resume`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            resume_text: resumeText,
            job_description_text: jobText
        })
    });

    const data = await response.json();

    if (!response.ok) {
        errorBox.textContent = data.error;
        errorBox.style.display = "block";

        document.getElementById("loaderOverlay")
            .classList.add("hidden");

        document.getElementById("result")
            .style.opacity = "1";

        return;
    }

    console.log("Optimize Response:", data);

    localStorage.setItem("currentResume", resumeText);
    localStorage.setItem("enhancedResume", data.optimized_resume || "");
    localStorage.setItem(
        "bulletChanges",
        JSON.stringify(data.bullet_changes || [])
    );

    window.location.href = "../enhancement/enhance.html";
});

downloadBtn.onclick = function (e) {
    e.preventDefault();
    e.stopPropagation();

    if (!window.latestData || !window.latestData.export_report) return;

    const dataStr = JSON.stringify(window.latestData.export_report, null, 2)

    const blob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "SkillAlign_Report.json";
    a.click();

    URL.revokeObjectURL(url);
};

document.getElementById("downloadPDF").addEventListener("click", function () {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const data = window.latestData;

    let y = 10;

    function addLine(text) {
        doc.text(text, 10, y);
        y += 8
    }

    // Title
    doc.setFontSize(16);
    addLine("SkillAlignAI Report");

    doc.setFontSize(12);
    y += 5;

    // Basic Info
    addLine(`Decision: ${data.decision}`);
    addLine(`Match Score: ${data.match_percentage}%`);

    y += 5;

    // Skills
    addLine("Matched Required Skills:")
    addLine((data.matched_skills || []).join(", ") || "None");

    y += 5;

    addLine("Missing Skills:");
    addLine((data.missing_skills || []).join(", ") || "None");

    y += 5;

    // Failure Analysis
    const fa = data.failure_analysis || {};
    addLine("Failure Analysis:");
    addLine(`Reason: ${fa.primary_reason || "-"}`);
    addLine(`Impact: ${fa.impact || "-"}`);

    y += 5

    // Suggestions
    addLine("Suggestions:");
    addLine((data.improvement_suggestions || []).join(", ") || "None");

    // Save
    doc.save("SkillAlign_Report.pdf");
});

function compareCandidates(c1, c2) {
    let reasons = [];

    // Score comparison
    if (c1.score > c2.score) {
        reasons.push(`Higher match score (${c1.score}% vs ${c2.score}%)`);
    }

    // Risk comparison 
    const riskOrder = { Low: 1, Medium: 2, High: 3 };

    const r1 = c1.data?.impact_metrics?.risk_level;
    const r2 = c2.data?.impact_metrics?.risk_level;

    if (r1 && r2 && riskOrder[r1] < riskOrder[r2]) {
        reasons.push(`Lower risk level (${r1} vs ${r2})`);
    }

    // Missing required skills 
    const m1 = c1.data?.missing_skills?.length || 0;
    const m2 = c2.data?.missing_skills?.length || 0;

    if (m1 < m2) {
        reasons.push(`Fewer missing required skills (${m1} vs ${m2})`);
    }

    return reasons;
}

document.getElementById("compareBtn").onclick = function () {
    const table = document.getElementById("comparisonTable");
    table.innerHTML = "";

    function computeRankScore(candidate) {
        let score = candidate.score;

        const risk = candidate.data?.impact_metrics?.risk_level;

        // Penalize risk 
        if (risk === "High") score -= 30;
        else if (risk === "Medium") score -= 15;

        // Penalize missing required skills heavily
        if (candidate.data?.missing_skills?.length > 0) {
            score -= 25;
        }

        // Boost strong fits
        if (candidate.decision === "Strong Fit") {
            score += 10;
        }

        return score;
    }

    // sort by score DESC 
    const sorted = [...allCandidates].sort((a, b) =>
        computeRankScore(b) - computeRankScore(a)
    );

    const comparisonBox = document.getElementById("comparisonExplanation");

    if (sorted.length >= 2) {
        const best = sorted[0];
        const second = sorted[1];

        const reasons = compareCandidates(best, second);

        comparisonBox.innerHTML = `
            <div class="card">
                <h3>Why ${best.name} ranks higher than ${second.name}</h3>
                <ul>
                    ${reasons.map(r => `<li>${r}</li>`).join("")}
                </ul>
            </div>
        `;
    }

    sorted.forEach((c, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>#${index + 1}</td>
            <td>${c.name}</td>
            <td>${computeRankScore(c)}</td>
            <td>${c.score}</td>
            <td>${c.decision}</td>
            <td>${c.missing?.join(", ") || "None"}</td>
        `;

        table.appendChild(row);
        if (index === 0) {
            row.classList.add("top-candidate");
        }
    });

    document.getElementById("comparisonTable").scrollIntoView({
        behavior: "smooth"
    });
}

document.getElementById("clearCandidates").onclick = function () {
    allCandidates = [];
    document.getElementById("comparisonTable").innerHTML = "";
}

document
    .getElementById("rewriteBtn")
    .addEventListener("click", async () => {

        const bullet =
            document.getElementById("bulletInput").value;

        const targetRole =
            document.getElementById("targetRole").value;

        const response = await fetch(
            `${BASE_URL}/rewrite_bullet`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    bullet,
                    target_role: targetRole
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            errorBox.textContent =
                data.error;

            errorBox.style.display =
                "block";

            return;
        }

        document.getElementById(
            "rewriteResult"
        ).innerHTML = `
        <p><strong>Original:</strong></p>
        <p>${data.original}</p>

        <p><strong>Rewritten:</strong></p>
        <p>${data.rewritten}</p>
    `;
    });

function renderTags(containerId, items) {
    const el = document.getElementById(containerId);
    if (!el) return;

    if (!items || items.length == 0) {
        el.innerHTML = "None";
        return;
    }

    el.innerHTML = items.map(skill =>
        `<span class="tag">${skill}</span>`
    ).join(" ");
}

document.addEventListener("click", function (e) {
    if (e.target && e.target.id === "toggleExplain") {

        const full = document.getElementById("fullExplanation");

        if (!full) return;

        if (full.classList.contains("hidden")) {
            full.classList.remove("hidden");
            e.target.textContent = "Hide Detailed Explanation";
        } else {
            full.classList.add("hidden");
            e.target.textContent = "Show Detailed Explanation";
        }
    }
});

function formatText(rawText) {
    if (!rawText) return "<p class='explanation-text'>No explanation available</p>";

    // 🔹 Step 1 — Clean markdown noise
    const cleanText = rawText
        .replace(/\*\*/g, "")
        .replace(/\*/g, "")
        .replace(/\n+/g, " ")
        .trim();

    // 🔹 Step 2 — Extract sections using keywords
    const primaryMatch = cleanText.split(/Primary rejection reason/i)[1] || "";
    const secondaryMatch = cleanText.split(/Secondary factors/i)[1] || "";
    const screeningMatch = cleanText.split(/What mattered most/i)[1] || "";
    const actionMatch = cleanText.split(/How to improve next time/i)[1] || "";

    // 🔹 Step 3 — Helper to convert sentence → list
    function toList(text) {
        return text
            .split(". ")
            .filter(s => s.trim().length > 0)
            .map(s => `<li>${s.trim()}.</li>`)
            .join("");
    }

    // 🔹 Step 4 — Build structured HTML
    return `
        <div class="explain-section">
            <h4>🚫 Primary Reason</h4>
            <p>${primaryMatch.split("Secondary factors")[0] || primaryMatch}</p>
        </div>

        <div class="explain-section">
            <h4>📉 Supporting Evidence</h4>
            <ul>${toList(secondaryMatch.split("What mattered most")[0] || secondaryMatch)}</ul>
        </div>

        <div class="explain-section">
            <h4>🧠 Screening Insight</h4>
            <p>${screeningMatch.split("How to improve next time")[0] || screeningMatch}</p>
        </div>

        <div class="explain-section">
            <h4>🚀 Action Plan</h4>
            <ul>${toList(actionMatch)}</ul>
        </div>
    `;
}

function displayResult(data) {
    const heroScore = document.getElementById("heroScore");
    const heroDecision = document.getElementById("heroDecision");
    const heroIssue = document.getElementById("heroIssue");
    const heroStrength = document.getElementById("heroStrength");
    const heroMissing = document.getElementById("heroMissing");

    const breakdownBox = document.getElementById("scoreBreakdown");
    const requiredScore = document.getElementById("requiredScore");
    const preferredScore = document.getElementById("preferredScore");
    const finalScore = document.getElementById("finalScore");

    const suggestions = document.getElementById("suggestions");
    const reportList = document.getElementById("reportList");
    const failureAnalysisDiv = document.getElementById("failureAnalysis");
    const enhancementBox = document.getElementById("resumeEnhancements");
    const impactBox = document.getElementById("impactMetrics");
    const explanation = document.getElementById("explanation");
    const auditTrail = document.getElementById("auditTrail");

    data.matched_skills = data.matched_skills || [];
    data.missing_skills = data.missing_skills || [];
    data.missing_preferred_skills = data.missing_preferred_skills || [];

    window.latestData = data;

    // Score
    heroScore.textContent = (data.match_percentage ?? 0) + "%";

    // Decision badge color
    heroDecision.textContent = data.decision;

    heroDecision.className = "badge";
    if (data.decision === "Strong Fit") {
        heroDecision.classList.add("green");
    } else if (data.decision === "Borderline") {
        heroDecision.classList.add("yellow");
    } else {
        heroDecision.classList.add("red");
    }

    // Primary Issue (from failure analysis)
    heroIssue.textContent =
        data.failure_analysis?.primary_reason || "Not specified";

    // Strength (top 2 matched skills)
    heroStrength.textContent =
        data.matched_skills?.slice(0, 2).join(", ") || "None";

    // Missing (top 2 gaps)
    heroMissing.textContent =
        data.missing_skills?.slice(0, 2).join(", ") || "None";

    const verdictLine = document.getElementById("verdictLine");

    if (verdictLine) {
        const reason = data.failure_analysis?.primary_reason || "key skill gaps";
        const strength = data.matched_skills?.[0] || "relevant skills";

        verdictLine.textContent =
            `💡 Verdict: Candidate ${data.decision.toLowerCase()} due to ${reason}, despite strength in ${strength}.`;
    }

    if (data.decision === "Strong Fit") {
        verdictLine.style.borderLeftColor = "#22c55e";
    }
    else if (data.decision === "Borderline") {
        verdictLine.style.borderLeftColor = "#f59e0b";
    }
    else {
        verdictLine.style.borderLeftColor = "#ef4444";
    }

    // Scores
    requiredScore.textContent = (data.required_match_percentage ?? 0) + "%";

    const pref = data.preferred_match_percentage
    preferredScore.textContent = pref !== "N/A" ? pref + "%" : "N/A";

    const domain = data.domain_match_percentage;

    document.getElementById("domainScore").textContent =
        domain !== "N/A" ? domain + "%" : "N/A";

    finalScore.textContent = (data.match_percentage ?? data.match_score ?? 0) + "%";

    if (breakdownBox) {
        breakdownBox.innerHTML = `
        <li><strong>Base:</strong> 0.8 × required + 0.2 × preferred</li>
        <li><strong>Final:</strong> Base × (0.7 + 0.3 × domain)</li>
    `;
    }

    // Matched Skills 
    renderTags("matchedRequired", data.matched_skills);
    renderTags("matchedPreferred", data.matched_preferred_skills);

    // Missing Skills 
    renderTags("missingRequired", data.missing_skills);
    renderTags("missingPreferred", data.missing_preferred_skills);
    if (document.getElementById("domainSkills")) {
        renderTags("domainSkills", data.matched_domain_skills);
    }

    // Report 
    if (reportList) {
        reportList.innerHTML = "";
        if (data.rejection_report && data.rejection_report.length) {
            data.rejection_report.forEach(r => {
                const li = document.createElement("li");
                li.textContent = `${r.reason} (Severity: ${r.severity})`;
                reportList.appendChild(li);
            });
        }
    }

    if (failureAnalysisDiv && data.failure_analysis) {
        const fa = data.failure_analysis;

        failureAnalysisDiv.innerHTML = `
            <div class="card">
                <ul>
                    <li><strong>Primary Reason:</strong> ${fa.primary_reason}</li>
                    <li><strong>Impact:</strong> ${fa.impact}</li>
                    <li><strong>Confidence:</strong> ${fa.confidence}</li>
                </ul>
                
                <p><strong>Explanation:</strong><br>${fa.explanation}</p>
                <p><strong>Action:</strong><br>${fa.fix_action}</p>
            </div>
        `;
    }

    if (enhancementBox) {
        enhancementBox.innerHTML =
            (data.resume_enhancement_suggestions || [])
                .map(item => `<li>${item}</li>`)
                .join("")
            || "<li>No enhancement suggestions available</li>";
    }

    if (impactBox) {

        impactBox.innerHTML = "";
        if (data.impact_metrics) {
            const im = data.impact_metrics;

            const risk = im.risk_level;

            let color = '#2ecc71'; // low

            if (risk == "Medium") color = "#f1c40f";
            if (risk == "High") color = "#e74c3c";

            impactBox.innerHTML = `
            <p><strong>Hire Probability: </strong> ${im.hire_probability}</p>
            <p><strong>Resume Strength: </strong> ${im.resume_strength}</p>
            <p><strong>Risk Level: </strong> <span style="color:${color}; font-weight:bold;"> ${risk}</span></p>
        `;
        }
    }

    suggestions.innerHTML = (data.improvement_suggestions || [])
        .map(s => `<li>${s}</li>`)
        .join("") || "<li>No suggestions</li>";

    // Explantion
    const shortExplanation = data.rejection_summary
        ? data.rejection_summary.split(". ").slice(0, 2).join(". ") + "."
        : "No explanation available";

    if (explanation) {
        explanation.innerHTML = `
        <div class="card">
            <h3>🧠 AI Explanation</h3>

            <p>${formatText(shortExplanation)}</p>

            <button id="toggleExplain">Show Detailed Explanation</button>

            <div id="fullExplanation" class="hidden">
                <p>${formatText(data.rejection_summary)}</p>
            </div>
        </div>
        `;
    }

    // Audit Trail 
    if (auditTrail) {
        auditTrail.innerHTML = "";

        if (data.agent_trace && data.agent_trace.length) {
            data.agent_trace.forEach(step => {
                const li = document.createElement("li");
                li.textContent = `${step.agent} -> executed`;
                auditTrail.appendChild(li);
                console.log(step.output)
            });
        }
        else if (data.audit_trail) {
            data.audit_trail.forEach(step => {
                const li = document.createElement("li");
                li.textContent = step;
                auditTrail.appendChild(li);
            });
        }
    }

}