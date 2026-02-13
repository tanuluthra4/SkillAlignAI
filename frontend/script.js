const analyzeBtn = document.getElementById("analyzeBtn");

analyzeBtn.addEventListener("click", async function () {
    const resumeText = document.getElementById("resume").value;
    const jobText = document.getElementById("job").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
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

        displayResult(data);

    } catch (error) {
        console.error("Error:", error);
    }

});

function displayResult(data) {
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = `
    <h3>Match Percentage: ${data.match_percentage}%</h3>
    <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ")}</p>
    <p><strong>Suggestions:</strong> ${data.improvement_suggestions.join(", ")}</p>
    <p><strong>Summary:</strong></p>
    <p>${data.rejection_summary}</p>
    `;
}