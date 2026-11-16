// CampusRoute web client. No frameworks, no innerHTML with data:
// everything from the API is safely inserted with textContent or DOM elements.
"use strict";

const $ = (id) => document.getElementById(id);
const SVG = "http://www.w3.org/2000/svg";
let campus = { places: [], edges: [] };

const CROWD_LABELS = {
  quiet: "Sakin",
  moderate: "Orta Yoğunluk",
  busy: "Kalabalık",
  packed: "Aşırı Yoğun / Tıkabasa",
};

async function api(path, params = {}) {
  const url = new URL(path, window.location.origin);
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== "") url.searchParams.set(k, v);
  }
  const res = await fetch(url);
  const body = await res.json();
  if (!res.ok) throw new Error(body.error || res.statusText);
  return body;
}

function el(tag, text, cls) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (cls) node.className = cls;
  return node;
}

function svg(tag, attrs) {
  const node = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  return node;
}

function drawMap(routePath = []) {
  const map = $("map");
  map.replaceChildren();
  const byId = Object.fromEntries(campus.places.map((p) => [p.id, p]));
  const onRoute = new Set();
  for (let i = 0; i + 1 < routePath.length; i++) {
    onRoute.add([routePath[i], routePath[i + 1]].sort().join("|"));
  }

  // Draw Edges
  for (const e of campus.edges) {
    const a = byId[e.a], b = byId[e.b];
    if (!a || !b) continue;
    const key = [e.a, e.b].sort().join("|");
    const cls = [
      "edge",
      e.stairs ? "stairs" : "",
      e.covered ? "covered" : "",
      onRoute.has(key) ? "route" : "",
    ].filter(Boolean).join(" ");
    map.append(svg("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, class: cls }));
  }

  // Draw Nodes
  for (const p of campus.places) {
    const isJunction = p.kind === "junction";
    const isOnRoute = routePath.includes(p.id);
    const g = svg("g", {
      class: "place " + p.kind + (isOnRoute ? " on" : ""),
      "data-id": p.id,
      "data-name": p.name,
    });

    const circle = svg("circle", { cx: p.x, cy: p.y, r: isJunction ? 5 : 12 });
    g.append(circle);

    if (!isJunction) {
      const label = svg("text", { x: p.x, y: p.y - 18, "text-anchor": "middle" });
      label.textContent = p.name;
      g.append(label);

      // Interactive: clicking a place sets it as destination
      g.style.cursor = "pointer";
      g.addEventListener("click", () => {
        $("to").value = p.name;
        findRoute();
      });
    }

    map.append(g);
  }
}

async function findRoute(event) {
  if (event) event.preventDefault();
  const steps = $("route-steps");
  steps.replaceChildren();
  try {
    const r = await api("/api/route", {
      from: $("from").value,
      to: $("to").value,
      avoid_stairs: $("avoid-stairs").checked ? "1" : "",
    });

    const stairInfo = r.has_stairs
      ? " ⚠️ (merdiven içerir)"
      : " ✨ (düz ayak / engelsiz)";
    $("route-summary").textContent =
      `${r.names[0]} → ${r.names[r.names.length - 1]}: ${r.meters} m, yaklaşık ${r.minutes} dk` + stairInfo;

    for (const s of r.steps) {
      steps.append(el("li", s));
    }
    drawMap(r.path);
  } catch (err) {
    $("route-summary").textContent = "⚠ Rota bulunamadı: " + err.message;
    drawMap();
  }
}

let searchTimer;
function onSearch() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(async () => {
    const list = $("results");
    list.replaceChildren();
    const q = $("q").value.trim();
    if (!q) return;
    try {
      const { results } = await api("/api/search", { q });
      if (!results.length) {
        list.append(el("li", "Aramanızla eşleşen yer bulunamadı.", "muted"));
        return;
      }
      for (const hit of results) {
        const li = el("li");
        const btn = el("button", "📍 " + hit.label, "search-item-btn");
        btn.type = "button";
        btn.addEventListener("click", () => {
          $("to").value = hit.id;
          findRoute();
        });
        li.append(btn);
        list.append(li);
      }
    } catch (err) {
      list.append(el("li", "Arama hatası: " + err.message, "muted"));
    }
  }, 200);
}

async function refreshNow() {
  const now = $("now").value;
  const box = $("next");
  box.replaceChildren();

  try {
    const n = await api("/api/next-class", { now });
    if (n.current) {
      box.append(el("p", "Şu Anki Ders: " + n.current));
    }
    if (n.next) {
      box.append(el("p", `Sıradaki: ${n.next.session} — ${n.next.in_minutes} dk içinde`, "summary"));
      if (n.next.place) {
        const btn = el("button", "📍 Oraya Rota Çiz", "link");
        btn.type = "button";
        btn.addEventListener("click", () => {
          $("to").value = n.next.place;
          findRoute();
        });
        box.append(btn);
      }
    } else {
      box.append(el("p", "Yakın zamanda planlanmış ders bulunmuyor.", "muted"));
    }
  } catch (err) {
    box.append(el("p", "Ders bilgisi alınamadı.", "muted"));
  }

  // Crowd status
  const crowd = $("crowd");
  crowd.replaceChildren();
  try {
    const { levels } = await api("/api/crowd", { now });
    const names = Object.fromEntries(campus.places.map((p) => [p.id, p.name]));
    const entries = Object.entries(levels);
    if (!entries.length) {
      crowd.append(el("li", "Son zamanlarda yoğunluk bildirimi yok", "muted"));
    }
    for (const [id, level] of entries) {
      const placeName = names[id] || id;
      const levelText = CROWD_LABELS[level] || level;
      const item = el("li", "", "crowd-badge " + level);
      item.append(el("strong", placeName));
      item.append(el("span", levelText));
      crowd.append(item);
    }
  } catch (err) {
    crowd.append(el("li", "Yoğunluk bilgisi alınamadı", "muted"));
  }
}

async function init() {
  campus = await api("/api/places");
  const list = $("place-list");
  for (const p of campus.places) {
    if (p.kind === "junction") continue;
    const option = document.createElement("option");
    option.value = p.name;
    list.append(option);
  }

  drawMap();

  $("route-form").addEventListener("submit", findRoute);
  $("q").addEventListener("input", onSearch);
  $("now").addEventListener("change", refreshNow);

  // Swap button (⇄)
  const swapBtn = $("swap-btn");
  if (swapBtn) {
    swapBtn.addEventListener("click", () => {
      const fromVal = $("from").value;
      $("from").value = $("to").value;
      $("to").value = fromVal;
      findRoute();
    });
  }

  // Quick Chips
  document.querySelectorAll(".quick-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const query = chip.getAttribute("data-search");
      $("q").value = query;
      onSearch();
    });
  });

  await findRoute();
  await refreshNow();
}

init().catch((err) => {
  $("route-summary").textContent = "⚠ API sunucusuna erişilemedi: " + err.message;
});
