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

// THEME TOGGLE (CR-15)
function initTheme() {
  const storedTheme = localStorage.getItem("campusroute-theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const currentTheme = storedTheme || (prefersDark ? "dark" : "light");

  applyTheme(currentTheme);

  const toggleBtn = $("theme-toggle");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      const active = document.documentElement.getAttribute("data-theme") || (prefersDark ? "dark" : "light");
      const nextTheme = active === "dark" ? "light" : "dark";
      applyTheme(nextTheme);
    });
  }
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("campusroute-theme", theme);
  const icon = $("theme-icon");
  if (icon) {
    icon.textContent = theme === "dark" ? "☀️" : "🌙";
  }
}

// DRAW CAMPUS SVG MAP
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

// FIND ROUTE
async function findRoute(event) {
  if (event) event.preventDefault();
  const steps = $("route-steps");
  steps.replaceChildren();
  const statsRow = $("route-stats");

  try {
    const r = await api("/api/route", {
      from: $("from").value,
      to: $("to").value,
      avoid_stairs: $("avoid-stairs").checked ? "1" : "",
    });

    const stairInfo = r.has_stairs
      ? " ⚠️ (merdiven içerir)"
      : " ✨ (düz ayak / engelsiz rota)";
    $("route-summary").textContent =
      `${r.names[0]} → ${r.names[r.names.length - 1]}: ${r.meters} m, yaklaşık ${r.minutes} dk` + stairInfo;

    // Health & Eco Stats
    if (statsRow) {
      statsRow.style.display = "flex";
      $("stat-calories").textContent = `~${r.calories || Math.round(r.meters * 0.05)} kcal`;
      $("stat-carbon").textContent = `${r.co2_saved_g || Math.round(r.meters * 0.14)} g CO₂`;
    }

    for (const s of r.steps) {
      steps.append(el("li", s));
    }
    drawMap(r.path);
  } catch (err) {
    $("route-summary").textContent = "⚠ Rota bulunamadı: " + err.message;
    if (statsRow) statsRow.style.display = "none";
    drawMap();
  }
}

// SEARCH
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

      const byId = Object.fromEntries(campus.places.map((p) => [p.id, p]));

      for (const hit of results) {
        const li = el("li");
        const btn = el("button", "", "search-item-btn");
        btn.type = "button";

        const textSpan = el("span", "📍 " + hit.label);
        btn.append(textSpan);

        // Check opening status (CR-11)
        const targetPlace = byId[hit.place_id || hit.id];
        if (targetPlace && targetPlace.hours) {
          const isOpen = targetPlace.open_now;
          if (isOpen !== undefined && isOpen !== null) {
            const badge = el(
              "span",
              isOpen ? "Açık" : "Kapalı",
              "open-pill " + (isOpen ? "open" : "closed")
            );
            btn.append(badge);
          }
        }

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

// REFRESH NOW & CROWD
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

  // Reload places to update open_now badges
  try {
    campus = await api("/api/places", { now });
  } catch (_) {}
}

// EVENTS CALENDAR (CR-16)
async function loadEvents() {
  const eventsList = $("events-list");
  if (!eventsList) return;
  eventsList.replaceChildren();

  try {
    const { events } = await api("/api/events");
    if (!events || !events.length) {
      eventsList.append(el("li", "Bugün için planlanmış etkinlik bulunmuyor.", "muted"));
      return;
    }

    for (const ev of events) {
      const item = el("li", "", "event-card-item");

      const top = el("div", "", "event-top");
      top.append(el("span", ev.category || "Etkinlik", "event-category-badge"));
      top.append(el("span", ev.time, "event-time"));
      item.append(top);

      item.append(el("span", ev.title, "event-title"));

      const btm = el("div", "", "event-bottom");
      btm.append(el("span", "📍 " + (ev.place_name || ev.place), "event-place"));

      const routeBtn = el("button", "Rotayı Çiz", "event-route-btn");
      routeBtn.type = "button";
      routeBtn.addEventListener("click", () => {
        $("to").value = ev.place_name || ev.place;
        findRoute();
      });
      btm.append(routeBtn);

      item.append(btm);
      eventsList.append(item);
    }
  } catch (err) {
    eventsList.append(el("li", "Etkinlikler yüklenemedi.", "muted"));
  }
}

// INITIALIZE
async function init() {
  initTheme();
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

  // Print button
  const printBtn = $("print-route-btn");
  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
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
  await loadEvents();
}

init().catch((err) => {
  $("route-summary").textContent = "⚠ API sunucusuna erişilemedi: " + err.message;
});
