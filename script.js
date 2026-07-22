// InsureSense - UI interactions

document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("sidebarToggle");
  const sidebar = document.getElementById("sidebar");

  if (toggle && sidebar) {
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("open");
    });

    document.addEventListener("click", function (e) {
      if (
        sidebar.classList.contains("open") &&
        !sidebar.contains(e.target) &&
        !toggle.contains(e.target)
      ) {
        sidebar.classList.remove("open");
      }
    });
  }

  // Animate probability bar fill on prediction page (if present)
  const fillBar = document.querySelector(".probability-bar-fill");
  if (fillBar) {
    const target = fillBar.getAttribute("data-width") || "0%";
    requestAnimationFrame(() => {
      fillBar.style.width = target;
    });
  }

  // Auto-dismiss flash alerts
  document.querySelectorAll(".alert-flash").forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity 0.4s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 400);
    }, 4500);
  });
});
