const analyzeBtn = document.getElementById("analyzeBtn");

const BASE_URL =
    window.location.hostname === "127.0.0.1" ||
        window.location.hostname === "localhost"
        ? "http://127.0.0.1:5000"
        : "https://skillalignai.onrender.com";

analyzeBtn.addEventListener("click", async function () {
    const resultDiv = document.getElementById("result");
    let resumeText = document.getElementById("resume").value;
    const jobText = document.getElementById("job").value;
    const resumeFile = document.getElementById("resumeFile").files[0];

    document.getElementById("reportList").innerHTML = "";
    document.getElementById("explanation").textContent = "";
    document.getElementById("auditTrail").innerHTML = "";
    document.getElementById("result").style.opacity = "0.2";
    document.getElementById("loaderOverlay").classList.remove("hidden");
    document.getElementById("decisionBox").textContent = "Analyzing... ";

    try {
        if (resumeFile) {
            const formData = new FormData();
            formData.append("resume_file", resumeFile);

            const uploadResponse = await fetch(`${BASE_URL}/upload_resume`, {
                method: "POST",
                body: formData
            });

            const uploadData = await uploadResponse.json();
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
        console.log("FULL RESPONSE:", data);
        if (!response.ok) {
            document.getElementById("loaderOverlay").classList.add("hidden");
            document.getElementById("result").style.opacity = "1";
            document.getElementById("decisionBox").textContent = data.error || "Something went wrong";

            document.getElementById("decisionBox").className = "card decision-box decision-reject";

            const auditTrail = document.getElementById("auditTrail");
            auditTrail.innerHTML = "";

            (data.audit_trail || []).forEach(step => {
                const li = document.createElement("li");
                li.textContent = step;
                auditTrail.appendChild(li);
            });

            return;
        }

        document.getElementById("loaderOverlay").classList.add("hidden");
        document.getElementById("result").style.opacity = "1";
        displayResult(data);
        window.latestData = data;

        const downloadBtn = document.getElementById("downloadReport");

        downloadBtn.onclick = function (e) {
            e.preventDefault();
            e.stopPropagation();

            if (!window.latestData || !window.latestData.export_report) return;

            const dataStr = JSON.stringify(window.latestData.export_report, null, 2)

            const blob = new Blob([dataStr], {type: "application/json"});
            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "SkillAlign_Report.json";
            a.click();

            URL.revokeObjectURL(url);
        };

    } catch (error) {
        document.getElementById("loaderOverlay").classList.add("hidden");
        document.getElementById("result").style.opacity = "1";
        const decisionBox = document.getElementById("decisionBox");

        decisionBox.textContent = "Unable to connect to server";
        decisionBox.className = "card decision-box decision-reject";

        return;
    }

});

function displayResult(data) {
    const decisionBox = document.getElementById("decisionBox");
    const breakdownBox = document.getElementById("scoreBreakdown");
    const requiredScore = document.getElementById("requiredScore");
    const preferredScore = document.getElementById("preferredScore");
    const finalScore = document.getElementById("finalScore");

    const matchedRequired = document.getElementById("matchedRequired");
    const matchedPreferred = document.getElementById("matchedPreferred");

    const missingRequired = document.getElementById("missingRequired");
    const missingPreferred = document.getElementById("missingPreferred");

    const suggestions = document.getElementById("suggestions");
    const reportList = document.getElementById("reportList");
    const failureBox = document.getElementById("failureBox");
    const impactBox = document.getElementById("impactMetrics");
    const explanation = document.getElementById("explanation");
    const auditTrail = document.getElementById("auditTrail");
    const reportPreview = document.getElementById("reportPreview");

    data.matched_skills = data.matched_skills || [];
    data.missing_skills = data.missing_skills || [];
    data.missing_preferred_skills = data.missing_preferred_skills || [];

    // Decision 
    decisionBox.className = "card decision-box";

    if (data.decision === "Strong Fit") {
        decisionBox.classList.add("decision-strong");
    }
    else if (data.decision === "Borderline") {
        decisionBox.classList.add("decision-borderline");
    }
    else {
        decisionBox.classList.add("decision-reject");
    }

    decisionBox.textContent = data.decision;

    // Scores
    requiredScore.textContent = (data.required_match_percentage ?? 0) + "%";
    preferredScore.textContent = (data.preferred_match_percentage ?? 0) + "%";
    finalScore.textContent = (data.match_percentage ?? data.match_score ?? 0) + "%";

    breakdownBox.innerHTML = "";
    if (data.score_explanation) {
        const s = data.score_explanation;

        breakdownBox.innerHTML = `
        <li><strong>Formula: </strong> ${s.formula}</li>
        `;
    }

    // Matched Skills 
    matchedRequired.textContent = data.matched_skills?.length ? data.matched_skills.join(", ") : "None";

    matchedPreferred.textContent = data.matched_preferred_skills?.length ? data.matched_preferred_skills.join(", ") : "None";

    // Missing Skills 
    missingRequired.textContent = data.missing_skills?.length ? data.missing_skills.join(", ") : "None";

    missingPreferred.textContent = data.missing_preferred_skills?.length ? data.missing_preferred_skills.join(", ") : "None";

    // Report 
    reportList.innerHTML = "";
    if (data.rejection_report && data.rejection_report.length) {
        data.rejection_report.forEach(r => {
            const li = document.createElement("li");
            li.textContent = `${r.reason} (Severity: ${r.severity})`;
            reportList.appendChild(li);
        });
    }

    failureBox.innerHTML = "";
    if (data.failure_analysis) {
        const f = data.failure_analysis;

        failureBox.innerHTML = `
        <li><strong>Primary Reason: </strong> ${f.primary_reason}</li>
        <li><strong>Impact: </strong> ${f.impact}</li>
        <li><strong>Confidence: </strong> ${f.confidence}</li>
        <li><strong>Explanation: </strong> ${f.explanation}</li>
        <li><strong>Action: </strong> ${f.fix_action}</li>
        `;
    }

    impactBox.innerHTML = "";
    if(data.impact_metrics) {
        const im = data.impact_metrics;

        impactBox.innerHTML = `
        <li><strong>Hire Probability: </strong> ${im.hire_probability}</li>
        <li><strong>Resume Strength: </strong> ${im.resume_strength}</li>
        <li><strong>Risk Level: </strong> ${im.risk_level}</li>
        `;
    }

    suggestions.textContent = data.improvement_suggestions?.length ? data.improvement_suggestions.join(", ") : "None";

    // Explantion 
    explanation.textContent = data.explanation || data.rejection_summary || "No explanation available";

    // Audit Trail 
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

    reportPreview.innerHTML = `
    <div><strong>Decision: </strong>${data.decision}</div>
    <div><strong>Match: </strong>${data.match_percentage}%</div>
    <div><strong>Missing Skills: </strong>${data.missing_skills.join(", ") || "None"}</div>
    <div style="margin-top:10px;"><strong>Summary:</strong></div>
    <div> ${data.rejection_summary} </div>
    `;
}