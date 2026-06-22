# -*- coding: utf-8 -*-
"""Update tools/index.html with hot tools, filter bar, sort, view details links"""
import json, os, re

BASE = r"D:\项目\工作区\工作5"
DATA_FILE = os.path.join(BASE, "data", "tools_database.json")
INDEX_FILE = os.path.join(BASE, "tools", "index.html")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Collect top tools
all_tools = []
cat_names = {
    "writing": "AI Writing", "image": "AI Image", "video": "AI Video",
    "audio": "AI Audio", "marketing": "AI Marketing", "code": "AI Code",
    "productivity": "AI Productivity", "uncategorized": "Other"
}
cat_colors = {
    "writing": "#6366f1", "image": "#ec4899", "video": "#10b981",
    "audio": "#06b6d4", "marketing": "#f59e0b", "code": "#3b82f6",
    "productivity": "#f97316", "uncategorized": "#64748b"
}

for cat_slug, items in data["data"].items():
    if not isinstance(items, list):
        continue
    cm = cat_names.get(cat_slug, "Other")
    cc = cat_colors.get(cat_slug, "#64748b")
    for t in items:
        if not isinstance(t, dict) or "name" not in t:
            continue
        repo_part = t["name"].split("/")[-1] if "/" in t["name"] else t["name"]
        slug = re.sub(r"[^a-zA-Z0-9_-]", "", repo_part).lower().strip("-")
        display = slug.replace("-", " ").replace("_", " ").title()
        desc = (t.get("description", "") or "")[:100]
        all_tools.append({
            "slug": slug, "display": display, "stars": t["stars"],
            "cat": cm, "color": cc, "desc": desc
        })

all_tools.sort(key=lambda x: x["stars"], reverse=True)
total = len(all_tools)
top9 = all_tools[:9]

def fmt(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)

# Build hot tools HTML
hot_cards = ""
for t in top9:
    hot_cards += f"""<div class="hot-tool-card" data-stars="{t['stars']}" data-name="{t['display']}">
      <div class="hot-name"><a href="details/{t['slug']}.html">{t['display']}</a></div>
      <div class="hot-meta">
        <span class="tag" style="background:{t['color']}20;color:{t['color']};border:1px solid {t['color']}40;font-size:0.75rem">{t['cat']}</span>
        <span>\u2b50 {fmt(t['stars'])}</span>
      </div>
      <div class="hot-desc">{t['desc']}...</div>
      <a href="details/{t['slug']}.html" class="view-details-link">View Details \u2192</a>
    </div>"""

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add CSS before </head>
css_block = """<style>
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1.5rem 0;
  align-items: center;
}
.filter-bar .filter-label {
  color: #94a3b8;
  font-size: 0.85rem;
  font-weight: 600;
  margin-right: 0.5rem;
}
.filter-tag {
  padding: 0.35rem 0.9rem;
  border-radius: 20px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #334155;
  background: transparent;
  color: #cbd5e1;
  text-decoration: none;
  display: inline-block;
}
.filter-tag:hover, .filter-tag.active {
  border-color: #8b5cf6;
  background: rgba(139,92,246,0.15);
  color: #a78bfa;
}
.sort-bar {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 1rem;
}
.sort-btn {
  padding: 0.35rem 0.9rem;
  border-radius: 8px;
  font-size: 0.8rem;
  cursor: pointer;
  border: 1px solid #334155;
  background: transparent;
  color: #94a3b8;
  transition: all 0.2s;
}
.sort-btn:hover, .sort-btn.active {
  border-color: #f59e0b;
  color: #f59e0b;
  background: rgba(245,158,11,0.1);
}
.view-details-link {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  color: #8b5cf6;
  font-size: 0.85rem;
  font-weight: 500;
  text-decoration: none;
  margin-top: 0.5rem;
  transition: all 0.2s;
}
.view-details-link:hover {
  color: #a78bfa;
  gap: 0.5rem;
}
.hot-tool-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1.25rem;
  transition: all 0.2s;
}
.hot-tool-card:hover {
  border-color: #8b5cf6;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(139,92,246,0.15);
}
.hot-tool-card .hot-name {
  font-size: 1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
}
.hot-tool-card .hot-name a {
  color: #e2e8f0;
  text-decoration: none;
}
.hot-tool-card .hot-name a:hover {
  color: #8b5cf6;
}
.hot-tool-card .hot-meta {
  display: flex;
  gap: 1rem;
  color: #94a3b8;
  font-size: 0.8rem;
  margin-top: 0.5rem;
  align-items: center;
}
.hot-tool-card .hot-desc {
  color: #64748b;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  line-height: 1.5;
}
</style>
</head>"""
html = html.replace("</head>", css_block)

# 2. Add the hot tools section before </main>
hot_section = f"""  <section class="section">
    <div class="container">
      <div class="section-header">
        <h1>\U0001f525 Hot AI Tools Right Now</h1>
        <p>Top trending open-source AI tools by GitHub stars</p>
      </div>
      <div class="filter-bar">
        <span class="filter-label">\U0001f3f7\ufe0f Filter by category:</span>
        <a href="categories.html" class="filter-tag active">All</a>
        <a href="writing-tools.html" class="filter-tag">\U0001f4dd Writing</a>
        <a href="image-tools.html" class="filter-tag">\U0001f3a8 Image</a>
        <a href="video-tools.html" class="filter-tag">\U0001f3ac Video</a>
        <a href="audio-tools.html" class="filter-tag">\U0001f3b5 Audio</a>
        <a href="marketing-tools.html" class="filter-tag">\U0001f4ca Marketing</a>
        <a href="code-tools.html" class="filter-tag">\U0001f4bb Code</a>
        <a href="productivity-tools.html" class="filter-tag">\u26a1 Productivity</a>
        <a href="details/index.html" class="filter-tag" style="border-color:#8b5cf6;color:#8b5cf6">\U0001f4cb All {total} Tools</a>
      </div>
      <div class="sort-bar">
        <span class="filter-label">\U0001f500 Sort:</span>
        <button class="sort-btn active" onclick="sortTools('stars')">\u2b50 By Stars</button>
        <button class="sort-btn" onclick="sortTools('name')">\U0001f521 By Name</button>
      </div>
      <div class="card-grid" id="hot-tools-grid">
        {hot_cards}
      </div>
      <p style="text-align:center;margin-top:1.5rem">
        <a href="details/index.html" style="color:#8b5cf6;font-weight:500;text-decoration:none;font-size:1rem">
          \U0001f4cb Browse All {total} Tool Detail Pages \u2192
        </a>
      </p>
    </div>
  </section>
  <script>
  function sortTools(by) {{
    const grid = document.getElementById('hot-tools-grid');
    const items = Array.from(grid.children);
    document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    items.sort((a, b) => {{
      if (by === 'stars') return parseInt(b.dataset.stars) - parseInt(a.dataset.stars);
      return a.dataset.name.localeCompare(b.dataset.name);
    }});
    items.forEach(item => grid.appendChild(item));
  }}
  </script>
</main>"""

html = html.replace("</main>", hot_section)

# 3. Add "View Details" links to category cards
# Writing (7 tools)
html = html.replace(
    '<span class="tag">7 tools</span>\n        </div>',
    '<span class="tag">7 tools</span>\n          <a href="writing-tools.html" class="view-details-link">View Details \u2192</a>\n        </div>'
)
# Image (6 tools)
html = html.replace(
    '<span class="tag">6 tools</span>\n        </div>',
    '<span class="tag">6 tools</span>\n          <a href="image-tools.html" class="view-details-link">View Details \u2192</a>\n        </div>'
)
# Video (8 tools)
html = html.replace(
    '<span class="tag">8 tools</span>\n        </div>',
    '<span class="tag">8 tools</span>\n          <a href="video-tools.html" class="view-details-link">View Details \u2192</a>\n        </div>'
)

# Audio card (6 tools, followed by marketing card with bg #fef3c7)
html = html.replace(
    '<span class="tag">6 tools</span>\n        </div>\n        <div class="card">\n          <div class="card-icon" style="background:#fef3c7">',
    '<span class="tag">6 tools</span>\n          <a href="audio-tools.html" class="view-details-link">View Details \u2192</a>\n        </div>\n        <div class="card">\n          <div class="card-icon" style="background:#fef3c7">'
)

# Code card (6 tools, followed by All Categories card)
html = html.replace(
    '<span class="tag">6 tools</span>\n        </div>        <div class="card">',
    '<span class="tag">6 tools</span>\n          <a href="code-tools.html" class="view-details-link">View Details \u2192</a>\n        </div>        <div class="card">'
)

# All Categories
html = html.replace(
    '<span class="tag">7 categories</span>\n        </div>',
    '<span class="tag">7 categories</span>\n          <a href="categories.html" class="view-details-link">Browse All \u2192</a>\n        </div>'
)

# 4. Update counts in meta
html = html.replace("Browse 30+ AI tools", f"Browse {total} AI tools")
html = html.replace("Browse 30+ AI tools for content creators. Categories", f"Browse {total} AI tools for content creators. Categories")

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated tools/index.html with {total} tools, hot tools section, and detail links")
