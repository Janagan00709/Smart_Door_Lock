document.addEventListener("DOMContentLoaded", function() {
    const statusElement = document.getElementById("lockStatus");
    if (statusElement) {
      const status = statusElement.textContent.trim();
      if (status === "Locked") {
        statusElement.style.color = "#dc3545";
      } else if (status === "Unlocked") {
        statusElement.style.color = "#28a745";
      }
    }
  });
  