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

  // Home hero: cycle through the example conversations, or jump to one from its tab.
  var sceneData = document.getElementById("demo-scenes");
  var chat = document.querySelector(".chat");
  if (sceneData && chat) {
    var scenes = JSON.parse(sceneData.textContent);
    var tabs = document.querySelectorAll(".demo-tabs button");
    var stamp = document.querySelector(".phone-top small");
    var caption = document.querySelector(".demo figcaption");
    var current = 0;
    var timer;
    var show = function (next) {
      current = next;
      chat.textContent = "";
      scenes[next].msgs.forEach(function (message) {
        var bubble = document.createElement("p");
        bubble.className = message[0] ? "msg me" : "msg";
        bubble.textContent = message[1];
        chat.appendChild(bubble);
      });
      stamp.textContent = scenes[next].time;
      caption.textContent = scenes[next].caption;
      tabs.forEach(function (tab, n) { tab.setAttribute("aria-selected", String(n === next)); });
    };
    var cycle = function () {
      timer = setInterval(function () { show((current + 1) % scenes.length); }, 9000);
    };
    tabs.forEach(function (tab, n) {
      tab.addEventListener("click", function () {
        clearInterval(timer);
        show(n);
        cycle();
      });
    });
    cycle();
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
