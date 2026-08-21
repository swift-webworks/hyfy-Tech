document.addEventListener("DOMContentLoaded", function () {
  // --- Preloader: fade out quickly, never block the page ---
  var preloader = document.getElementById("preloader");
  if (preloader) {
    var hide = function () { preloader.classList.add("hide"); };
    // Hide as soon as the page is interactive, capped at ~1.2s max.
    window.setTimeout(hide, 600);
    window.addEventListener("load", hide);
  }

  // --- Expandable contact FAB ---
  var fabMenu = document.getElementById("fabMenu");
  var fabToggle = document.getElementById("fabToggle");
  if (fabToggle && fabMenu) {
    fabToggle.addEventListener("click", function () {
      var isOpen = fabMenu.classList.toggle("open");
      fabToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
    document.addEventListener("click", function (e) {
      if (!fabMenu.contains(e.target)) {
        fabMenu.classList.remove("open");
        fabToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // --- Interactive trust/experience cards ---
  document.querySelectorAll(".trust-card").forEach(function (card) {
    var toggle = function () {
      var isOpen = card.classList.toggle("open");
      card.setAttribute("aria-expanded", isOpen ? "true" : "false");
    };
    card.addEventListener("click", toggle);
    card.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggle();
      }
    });
  });

  // --- Enquiry form: record render time for spam-timing check ---
  document.querySelectorAll('input[name="form_rendered_at"]').forEach(function (field) {
    if (!field.value) {
      field.value = Date.now() / 1000;
    }
  });

  // --- Pause marquees on hover for readability ---
  document.querySelectorAll(".marquee").forEach(function (marquee) {
    var track = marquee.querySelector(".marquee-track");
    if (!track) return;
    marquee.addEventListener("mouseenter", function () { track.style.animationPlayState = "paused"; });
    marquee.addEventListener("mouseleave", function () { track.style.animationPlayState = "running"; });
  });
});
