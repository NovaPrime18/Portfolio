/* Small, dependency-free behaviour layer. */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- sticky header --------------------------------------------------- */
  var head = document.querySelector(".site-head");
  if (head) {
    var onScroll = function () {
      head.dataset.stuck = window.scrollY > 24 ? "true" : "false";
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* --- mobile nav ------------------------------------------------------ */
  var toggle = document.querySelector(".nav-toggle");
  if (toggle && head) {
    toggle.addEventListener("click", function () {
      var open = head.dataset.open === "true";
      head.dataset.open = open ? "false" : "true";
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
    });
    head.addEventListener("click", function (e) {
      if (e.target.closest(".nav a")) {
        head.dataset.open = "false";
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* --- reveal on scroll ------------------------------------------------ */
  var items = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]"));
  if (items.length) {
    if (reduced || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-in"); });
    } else {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.06 }
      );
      items.forEach(function (el, i) {
        var group = el.parentElement ? el.parentElement.querySelectorAll("[data-reveal]") : [el];
        var idx = Array.prototype.indexOf.call(group, el);
        el.style.setProperty("--d", Math.min(idx, 4) * 70 + "ms");
        io.observe(el);
      });
      // if the observer never fires (old browser, print, odd embedding), don't ship blank space
      setTimeout(function () {
        items.forEach(function (el) {
          if (el.classList.contains("is-in")) return;
          if (el.getBoundingClientRect().top < window.innerHeight + 200) el.classList.add("is-in");
        });
      }, 1500);
    }
  }

  /* --- copy email ------------------------------------------------------ */
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var value = btn.getAttribute("data-copy");
      var done = function () {
        var label = btn.querySelector("span");
        if (!label) return;
        var old = label.textContent;
        label.textContent = "Copied";
        setTimeout(function () { label.textContent = old; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(done, function () {});
      } else {
        var ta = document.createElement("textarea");
        ta.value = value;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  });

  /* --- current year ---------------------------------------------------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
