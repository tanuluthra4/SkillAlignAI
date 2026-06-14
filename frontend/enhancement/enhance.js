document
  .getElementById("copyResumeBtn")
  .addEventListener("click", () => {

    const text =
      document.getElementById(
        "enhancedResume"
      ).textContent;

    navigator.clipboard.writeText(text);

    alert("Resume copied!");
  });

document
  .getElementById("downloadResumeBtn")
  .addEventListener("click", () => {

    const text =
      document.getElementById(
        "enhancedResume"
      ).textContent;

    const blob = new Blob(
      [text],
      { type: "text/plain" }
    );

    const url =
      URL.createObjectURL(blob);

    const a =
      document.createElement("a");

    a.href = url;
    a.download = "optimized_resume.txt";

    a.click();

    URL.revokeObjectURL(url);
  });

function formatResume(text) {

  if (!text) return "No resume found.";

  return text
    .replace("Skills:", "<h3>🛠 Skills</h3>")
    .replace("Projects:", "<h3>🚀 Projects</h3>")
    .replace("Experience:", "<h3>💼 Experience</h3>")
    .replace("Education:", "<h3>🎓 Education</h3>");
}

function renderSkillsAsTags(resumeText) {

  const skillsMatch =
    resumeText.match(/Skills:\s*([\s\S]*?)(Projects:|Experience:|Education:|$)/i);

  if (!skillsMatch) {
    return resumeText;
  }

  const skillsText = skillsMatch[1];

  const skills = skillsText
    .split(",")
    .map(skill => skill.trim())
    .filter(Boolean);

  const skillsHtml = `
        <h3>🛠 Skills</h3>
        <div class="skill-tags">
            ${skills.map(skill =>
    `<span class="skill-tag">${skill}</span>`
  ).join("")}
        </div>
    `;

  return resumeText.replace(
    skillsMatch[0],
    skillsHtml
  );
}

window.addEventListener("DOMContentLoaded", () => {
  const currentResume = localStorage.getItem("currentResume");
  const enhancedResume = localStorage.getItem("enhancedResume");
  const bulletChangesRaw = localStorage.getItem("bulletChanges");

  // Current Resume
  document.getElementById("currentResume").innerHTML =
    formatResume(currentResume);

  // Enhanced Resume
  document.getElementById("enhancedResume").innerHTML =
    renderSkillsAsTags(enhancedResume);

  const changes =
    JSON.parse(
      localStorage.getItem("bulletChanges") || "[]"
    );

  document.getElementById(
    "bulletsImproved"
  ).textContent = changes.length;

  let skillsAdded = 0;

  changes.forEach(change => {
    if (
      change.reason &&
      change.reason.toLowerCase().includes("skill")
    ) {
      skillsAdded++;
    }
  });

  document.getElementById(
    "skillsAdded"
  ).textContent = skillsAdded;

  // Bullet Changes
  let bulletChanges = [];
  if (bulletChangesRaw && bulletChangesRaw !== "undefined") {
    try {
      bulletChanges = JSON.parse(bulletChangesRaw);
    } catch (e) {
      console.error("Failed to parse bulletChanges:", e);
    }
  }

  const score =
    Math.min(
      100,
      50 + (changes.length * 10)
    );

  document.getElementById(
    "optimizationScore"
  ).textContent = score + "%";

  let enhanced =
    enhancedResume || "";

  const keywords = [
    "REST API",
    "Backend Development",
    "Python",
    "Flask",
    "MySQL"
  ];

  keywords.forEach(keyword => {
    enhanced =
      enhanced.replaceAll(
        keyword,
        `<mark>${keyword}</mark>`
      );
  });

  document.getElementById(
    "enhancedResume"
  ).innerHTML = enhanced;

  const summary =
    document.getElementById(
      "optimizationSummary"
    );

  summary.innerHTML = `
<li>Added ATS-friendly keywords</li>
<li>Strengthened project descriptions</li>
<li>Improved action verbs</li>
<li>Aligned resume with job requirements</li>
<li>Enhanced technical terminology</li>
`;

  const bulletChangesContainer =
    document.getElementById("bulletChanges");

  bulletChangesContainer.innerHTML = "";

  changes.forEach((change, index) => {

    bulletChangesContainer.innerHTML += `
  <div class="change-card">

      <div class="change-header">
          Improvement #${index + 1}
      </div>

      <div class="comparison">

          <div class="before">
              <h4>❌ Before</h4>
              <p>${change.original}</p>
          </div>

          <div class="after">
              <h4>✅ After</h4>
              <p>${change.rewritten}</p>
          </div>

      </div>

      <div class="reason">
          <h4>💡 Why This Helps ATS</h4>
          <p>${change.reason}</p>
      </div>

  </div>
`;
  });
});
