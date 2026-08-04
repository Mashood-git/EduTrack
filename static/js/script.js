// =========================================================
// EDUTRACK LANDING PAGE — INTERACTIONS
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

  /* ---------- Navbar shrink + mobile toggle ---------- */
  const navbar = document.querySelector(".landing-navbar");
  const navToggle = document.querySelector(".nav-toggle");

  function handleScroll() {
    if (window.scrollY > 40) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }

    scrollTopBtn.classList.toggle("visible", window.scrollY > 500);
  }

  window.addEventListener("scroll", handleScroll);
  handleScroll();

  if (navToggle) {
    navToggle.addEventListener("click", function () {
      navbar.classList.toggle("mobile-open");
    });
  }

  // Close mobile menu when a link is tapped
  document.querySelectorAll(".landing-menu a").forEach(function (link) {
    link.addEventListener("click", function () {
      navbar.classList.remove("mobile-open");
    });
  });

  /* ---------- Scroll-reveal for cards & timeline ---------- */
  const revealTargets = document.querySelectorAll(
    ".course-card, .feature-card, .timeline-step"
  );

  const revealObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  revealTargets.forEach(function (el, index) {
    el.style.transitionDelay = (index % 4) * 0.08 + "s";
    revealObserver.observe(el);
  });

  /* ---------- Animated stat counters ---------- */
  const counters = document.querySelectorAll("[data-count]");

  const counterObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  counters.forEach(function (el) {
    counterObserver.observe(el);
  });

  function animateCounter(el) {
    const target = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || "";
    const duration = 1400;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = target * eased;
      el.textContent =
        (target % 1 === 0 ? Math.round(value) : value.toFixed(1)) + suffix;
      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    }

    requestAnimationFrame(tick);
  }

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll(".faq-question").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const item = btn.closest(".faq-item");
      const answer = item.querySelector(".faq-answer");
      const isActive = item.classList.contains("active");

      document.querySelectorAll(".faq-item").forEach(function (el) {
        el.classList.remove("active");
        el.querySelector(".faq-answer").style.maxHeight = null;
      });

      if (!isActive) {
        item.classList.add("active");
        answer.style.maxHeight = answer.scrollHeight + "px";
      }
    });
  });

  /* ---------- Scroll to top ---------- */
  const scrollTopBtn = document.querySelector(".scroll-top");
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
});