(function () {
  var root = document.documentElement;
  root.classList.add("js");

  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  var rot = document.querySelector(".rot");
  if (rot) {
    var words = rot.getAttribute("data-words").split("|");
    var index = 0;
    setInterval(function () {
      rot.classList.add("out");
      setTimeout(function () {
        index = (index + 1) % words.length;
        rot.textContent = words[index];
        rot.classList.remove("out");
      }, 300);
    }, 2200);
  }

  var items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
    return;
  }
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("in");
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px" });
  items.forEach(function (el) { observer.observe(el); });
})();
