const analyzeBtn = document.getElementById("analyzeBtn");

const BASE_URL =
    window.location.hostname === "127.0.0.1" ||
        window.location.hostname === "localhost"
        ? "http://127.0.0.1:5000"
        : "https://skillalignai.onrender.com";

analyzeBtn.addEventListener("click", async function () {
    let resumeText = document.getElementById("resume").value;
    const jobText = document.getElementById("job").value;
    const resumeFile = document.getElementById("resumeFile").files[0];

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

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        displayResult(data);

    } catch (error) {
        console.error("Error:", error);
    }

});

function displayResult(data) {
    const resultDiv = document.getElementById("result");

    const missingSKills =
        data.missing_skills && data.missing_skills.length
            ? data.missing_skills.join(", ")
            : "None";

    const missingPreferred =
        data.missing_preferred_skills && data.missing_preferred_skills.length
            ? data.missing_preferred_skills.join(", ")
            : "None";

    const suggestions =
        data.improvement_suggestions && data.improvement_suggestions.length
            ? data.improvement_suggestions.join(", ")
            : "None";

    let rejectionreportHTML = "";

    if (data.rejection_report && data.rejection_report.length) {
        rejectionreportHTML = data.rejection_report.map(r => `
            <li>
            <strong>${r.reason}</strong> (Severity: ${r.severity})
            </li>
            `).join("");
    }

    resultDiv.innerHTML = `
    <h3>Match Percentage: ${data.match_percentage}%</h3>
    <p><strong>Missing Required Skills:</strong> ${missingSKills}</p>
    <p><strong>Missing Preferred Skills:</strong> ${missingPreferred}</p>
    <p><strong>Suggestions:</strong> ${suggestions}</p>
    <h4>Screening Report</h4>
    <ul>
        ${rejectionreportHTML}
    </ul>

    <h4>Detailed Explanation</h4>
    <div style="max-height:400px; overflow-y:auto; border:1px solid #ccc; padding:10px; white-space:pre-wrap;">
        ${data.rejection_summary}
    </div>
    `;
}