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
    const requiredScore = document.getElementById("requiredScore");
    const preferredScore = document.getElementById("preferredScore");
    const finalScore = document.getElementById("finalScore");

    const missingRequired = document.getElementById("missingRequired");
    const missingPreferred = document.getElementById("missingPreferred");

    const suggestions = document.getElementById("suggestions");
    const reportList = document.getElementById("reportList");
    const explanation = document.getElementById("explanation");
    const auditTrail = document.getElementById("auditTrail");

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
    requiredScore.textContent = data.required_match_percentage + "%";
    preferredScore.textContent = data.preferred_match_percentage + "%";
    finalScore.textContent = data.match_percentage + "%";

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

    suggestions.textContent = data.improvement_suggestions?.length ? data.improvement_suggestions.join(", ") : "None";

    // Explantion 
    explanation.textContent = data.rejection_summary;

    // Audit Trail 
    auditTrail.innerHTML = ""
    if (data.audit_trail && data.audit_trail.length) {
        data.audit_trail.forEach(step => {
            const li = document.createElement("li");
            li.textContent = step;
            auditTrail.appendChild(li);
        });
    }
}