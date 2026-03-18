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
                body:formData
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

    resultDiv.innerHTML = `
    <h3>Match Percentage: ${data.match_percentage}%</h3>
    <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ")}</p>
    <p><strong>Suggestions:</strong> ${data.improvement_suggestions.join(", ")}</p>
    <p><strong>Summary:</strong></p>
    <p>${data.rejection_summary}</p>
    `;
}