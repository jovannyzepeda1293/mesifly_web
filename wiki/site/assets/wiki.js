// Búsqueda local sobre search.json (sin dependencias) + resaltado del índice "En esta página".
(function () {
  var input = document.getElementById("q"), box = document.getElementById("res");
  var norm = function (s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
  var data = null, loading = null, sel = -1;
  var base = document.querySelector('link[rel=stylesheet][href$="wiki.css"]').getAttribute("href").replace("wiki.css", "");

  function load() {
    loading = loading || fetch(base + "search.json").then(function (r) {
      if (!r.ok) throw new Error("search.json " + r.status + " en " + r.url); // nginx devolvió su página de error, no el JSON
      return r.json();
    }).then(function (d) {
      data = d.map(function (x) { x.n = [norm(x.t), norm(x.k), norm(x.r), norm(x.x)]; return x; });
    }).catch(function (e) { console.error(e); data = []; });
    return loading;
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function show(open) { box.hidden = !open; input.setAttribute("aria-expanded", open); sel = -1; }

  function search() {
    var words = norm(input.value).split(/\s+/).filter(Boolean);
    if (!words.length) return show(false);
    var hits = data.map(function (x) {
      var score = 0;
      for (var i = 0; i < words.length; i++) {
        var w = words[i], s = 0;
        if (x.n[0].indexOf(w) > -1) s += 10; if (x.n[1].indexOf(w) > -1) s += 6;
        if (x.n[2].indexOf(w) > -1) s += 3; if (x.n[3].indexOf(w) > -1) s += 1;
        if (!s) return null; // todas las palabras deben aparecer
        score += s;
      }
      return { x: x, s: score };
    }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 8);
    box.innerHTML = hits.length ? hits.map(function (h) {
      return '<li role="option"><a href="' + h.x.u + '"><strong>' + esc(h.x.t) + "</strong><span>" + esc(h.x.r) + "</span></a></li>";
    }).join("") : '<li class="none">Sin resultados. Prueba con otra palabra.</li>';
    show(true);
  }

  if (input) {
    input.addEventListener("input", function () { load().then(search); });
    input.addEventListener("focus", load);
    input.addEventListener("keydown", function (e) {
      var links = box.querySelectorAll("a");
      if (e.key === "Escape") { show(false); input.blur(); }
      else if ((e.key === "ArrowDown" || e.key === "ArrowUp") && links.length) {
        e.preventDefault();
        sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
        links.forEach(function (a, i) { a.setAttribute("aria-selected", i === sel); });
      } else if (e.key === "Enter" && links.length) { links[Math.max(sel, 0)].click(); }
    });
    document.addEventListener("click", function (e) { if (!e.target.closest(".search")) show(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); input.focus(); }
    });
    var q = new URLSearchParams(location.search).get("q"); // lo usa el SearchAction del JSON-LD
    if (q) { input.value = q; load().then(search); }
  }

  var links = document.querySelectorAll(".toc a");
  if (links.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) links.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + e.target.id); });
      });
    }, { rootMargin: "-80px 0px -70% 0px" });
    links.forEach(function (a) { var h = document.getElementById(a.getAttribute("href").slice(1)); if (h) io.observe(h); });
  }
})();
