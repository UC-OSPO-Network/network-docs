-- Shortcodes that read _data/places.json (written by scripts/build_places.py
-- from _data/places.yml in the book's pre-render step).
--
--   {{< on-campus tz >}}   the "On campus today" box for one project
--   {{< places-map >}}     the Leaflet map, plus a text list of every place
--
-- HTML output only. Other formats get nothing.

local places, by_id

local function load()
  if places then return end
  local path = quarto.project.directory .. "/_data/places.json"
  local f = io.open(path, "r")
  if not f then
    error("places.lua: " .. path .. " not found. Run scripts/build_places.py.")
  end
  places = quarto.json.decode(f:read("a"))
  f:close()
  by_id = {}
  for _, p in ipairs(places) do by_id[p.id] = p end
end

local function esc(s)
  s = tostring(s or "")
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local function present(v) return v ~= nil and v ~= "" and v ~= quarto.json.null end

local KIND_ORDER = { "unit", "steward", "project", "heritage", "archive", "campus" }
local KIND_LABEL = {
  unit = "Campus unit", steward = "Who runs it now", project = "Project",
  heritage = "Heritage site", archive = "Archives and sources", campus = "Campus",
}

local function links_html(p)
  local groups, out = {}, {}
  for _, l in ipairs(p.links or {}) do
    groups[l.kind] = groups[l.kind] or {}
    table.insert(groups[l.kind], string.format('<a href="%s">%s</a>', esc(l.url), esc(l.label)))
  end
  for _, kind in ipairs(KIND_ORDER) do
    if groups[kind] then
      table.insert(out, string.format("<dt>%s</dt><dd>%s</dd>", KIND_LABEL[kind], table.concat(groups[kind], " · ")))
    end
  end
  return "<dl>" .. table.concat(out) .. "</dl>"
end

local function section_href(p)
  if not present(p.chapter) then return nil end
  return p.chapter:gsub("%.qmd$", ".html") .. "#" .. p.id
end

local function on_campus(args)
  if not quarto.doc.is_format("html") then return pandoc.Null() end
  load()
  local id = pandoc.utils.stringify(args[1] or "")
  local p = by_id[id]
  if not p then error("on-campus: no place with id '" .. id .. "' in places.yml") end
  local html = { '<div class="on-campus" role="note" aria-label="On campus today: ' .. esc(p.name) .. '">',
    '<p class="on-campus-title">On campus today</p>',
    string.format('<p class="on-campus-place"><strong>%s</strong>, %s</p>', esc(p.place or "Online"), esc(p.campus)) }
  if p.place_at_time == false and present(p.prior) then
    table.insert(html, '<p class="on-campus-prior">' .. esc(p.prior) .. "</p>")
  end
  table.insert(html, links_html(p))
  if present(p.heritage_visit) then
    table.insert(html, '<p class="on-campus-visit"><strong>Visiting:</strong> ' .. esc(p.heritage_visit) .. "</p>")
  end
  table.insert(html, '<p class="on-campus-map"><a href="map.html">See it on the map</a></p></div>')
  return pandoc.RawBlock("html", table.concat(html, "\n"))
end

local LEAFLET = [[
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
  integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
]]

local MAP_JS = [[
<script>
(function () {
  var places = JSON.parse(document.getElementById("places-data").textContent);
  var el = document.getElementById("places-map");
  if (!window.L || !el) return;
  var map = L.map(el, { scrollWheelZoom: false });
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);
  function esc(s) { var d = document.createElement("div"); d.textContent = s == null ? "" : s; return d.innerHTML; }
  function icon(cls) { return L.divIcon({ className: "places-pin " + cls, iconSize: [16, 16], iconAnchor: [8, 8], popupAnchor: [0, -8] }); }
  var layers = { history: L.layerGroup(), today: L.layerGroup() };
  var bounds = [];
  places.forEach(function (p) {
    if (!p.pin || !layers[p.layer]) return;
    var html = "<strong>" + esc(p.name) + "</strong><br>" + esc(p.place) + ", " + esc(p.campus);
    if (p.layer === "history" && p.chapter) {
      html += '<br><a href="' + p.chapter.replace(/\.qmd$/, ".html") + "#" + p.id + '">Read the story</a>';
    }
    var home = (p.links || []).filter(function (l) { return l.kind === "unit" || l.kind === "project"; })[0];
    if (home) html += '<br><a href="' + esc(home.url) + '">' + esc(home.label) + "</a>";
    L.marker([p.lat, p.lon], { icon: icon("pin-" + p.layer), title: p.name, alt: p.name, zIndexOffset: p.layer === "history" ? 1000 : 0 })
      .bindPopup(html).addTo(layers[p.layer]);
    bounds.push([p.lat, p.lon]);
  });
  // Today first, so the history pins draw on top where both share a campus.
  layers.today.addTo(map);
  layers.history.addTo(map);
  L.control.layers(null, {
    '<span class="places-key pin-history"></span> Where the work happened': layers.history,
    '<span class="places-key pin-today"></span> Network campuses today': layers.today
  }, { collapsed: false }).addTo(map);
  map.fitBounds(bounds, { padding: [24, 24] });
})();
</script>
]]

local function places_map()
  if not quarto.doc.is_format("html") then return pandoc.Null() end
  load()
  local hist, today, related = {}, {}, {}
  for _, p in ipairs(places) do
    if p.layer == "history" then
      local href = section_href(p)
      local name = href and string.format('<a href="%s">%s</a>', esc(href), esc(p.name)) or esc(p.name)
      local where = esc(p.place or "Online") .. ", " .. esc(p.campus)
      if not p.pin then where = where .. " (no pin: not tied to one place)" end
      table.insert(hist, "<li>" .. name .. ". " .. where .. "</li>")
    else
      local home = nil
      for _, l in ipairs(p.links or {}) do
        if l.kind == "unit" then home = l break end
      end
      local name = home and string.format('<a href="%s">%s</a>', esc(home.url), esc(p.name)) or esc(p.name)
      local item = "<li><strong>" .. esc(p.campus) .. "</strong>: " .. name .. ". " .. esc(p.place) .. "</li>"
      table.insert(p.layer == "today" and today or related, item)
    end
  end
  local html = {
    LEAFLET,
    '<div id="places-map" class="places-map" role="region" aria-label="Map of UC open source places. The same places are listed as text below the map."></div>',
    '<script type="application/json" id="places-data">' .. quarto.json.encode(places):gsub("</", "<\\/") .. "</script>",
    MAP_JS,
    '<h2 id="places-list-history">Where the work happened</h2><ul class="places-list">' .. table.concat(hist) .. "</ul>",
    '<h2 id="places-list-today">Network campuses today</h2><ul class="places-list">' .. table.concat(today) .. "</ul>",
    '<h2 id="places-list-related">Other UC units</h2><p>These campuses are not Network members. Each has a related unit. They are listed here and not pinned.</p><ul class="places-list">' .. table.concat(related) .. "</ul>",
  }
  return pandoc.RawBlock("html", table.concat(html, "\n"))
end

return {
  ["on-campus"] = on_campus,
  ["places-map"] = places_map,
}
