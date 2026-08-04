// =========================================================
// EDUTRACK APP — shared interactions for dashboard/auth pages
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

  const sidebar = document.querySelector(".sidebar");
  const toggle = document.querySelector(".sidebar-toggle");

  if (sidebar && toggle) {
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("menu-open");
    });

    // Close the menu after a link is tapped (mobile)
    sidebar.querySelectorAll(".sidebar-menu a").forEach(function (link) {
      link.addEventListener("click", function () {
        sidebar.classList.remove("menu-open");
      });
    });
  }

  /* Animate progress bars in from 0 on load (progress.html) */
  document.querySelectorAll(".progress-fill").forEach(function (bar) {
    const target = bar.style.width;
    bar.style.width = "0%";
    requestAnimationFrame(function () {
      setTimeout(function () {
        bar.style.width = target;
      }, 100);
    });
  });

});