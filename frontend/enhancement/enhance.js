window.addEventListener("DOMContentLoaded", () => {
  const currentResume = localStorage.getItem("currentResume");
  const enhancedResume = localStorage.getItem("enhancedResume");
  const bulletChangesRaw = localStorage.getItem("bulletChanges");

  // Current Resume
  document.getElementById("currentResume").innerHTML =
    (currentResume || "No resume found.").replace(/\n/g, "<br>");

  // Enhanced Resume (only text, not JSON)
  document.getElementById("enhancedResume").innerHTML =
    (enhancedResume || "No enhanced resume found.").replace(/\n/g, "<br>");

  // Bullet Changes
  let bulletChanges = [];
  if (bulletChangesRaw && bulletChangesRaw !== "undefined") {
    try {
      bulletChanges = JSON.parse(bulletChangesRaw);
    } catch (e) {
      console.error("Failed to parse bulletChanges:", e);
    }
  }

  const bulletList = document.getElementById("bulletChanges");
  if (bulletChanges.length > 0) {
    bulletList.innerHTML = bulletChanges.map(change => `
      <li>
        <p><strong>Original:</strong> ${change.original}</p>
        <p><strong>Rewritten:</strong> ${change.rewritten}</p>
        <p><em>Reason:</em> ${change.reason}</p>
      </li>
    `).join("");
  } else {
    bulletList.innerHTML = "<li>No changes available</li>";
  }
});
