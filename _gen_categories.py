import os, json
from datetime import datetime

base = "D:/项目/工作区/工作5"

with open(os.path.join(base, "data", "tools_database.json"), "r", encoding="utf-8") as f:
    db = json.load(f)

CATEGORY_INFO = {
    "writing": {"name": "AI Writing & Content", "emoji": "\U0001f4dd", "color": "#6366f1", "desc": "AI-powered writing tools for content creation, copywriting, translation, and summarization."},
    "image": {"name": "AI Image & Design", "emoji": "\U0001f3a8", "color": "#ec4899", "desc": "Image generation, editing, design, and visual content creation with AI."},
    "video": {"name": "AI Video & Animation", "emoji": "\U0001f3ac", "color": "#10b981", "desc": "Video generation, editing, subtitles, and animation tools powered by AI."},
    "audio": {"name": "AI Audio & Music", "emoji": "\U0001f3b5", "color": "#06b6d4", "desc": "Text-to-speech, music generation, transcription, voice cloning and audio production."},
    "marketing": {"name": "AI Marketing & SEO", "emoji": "\U0001f4ca", "color": "#f59e0b", "desc": "SEO, analytics, email marketing, social media, and advertising AI tools."},
    "code": {"name": "AI Code & Development", "emoji": "\U0001f4bb", "color": "#3b82f6", "desc": "Code assistants, generation, debugging, CLI tools and API development with AI."},
    "productivity": {"name": "AI Productivity", "emoji": "\u26a1", "color": "#f97316", "desc": "Notes, knowledge management, task automation, and productivity tools."},
}

today = datetime.now().strftime("%Y-%m-%d")

def make_page(html_content, title, desc, rel_path):
    """Wrap content in full HTML page."""
    level = rel_path.count("/") - 1
    if level < 0: level = 0
    prefix = "../" * level if level > 0 else ""
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc[:200]}">
<link rel="canonical" href="https://creatordir-tools.vercel.app/{rel_path}">
<meta name="robots" content="index, follow">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}css/style.css">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc[:200]}">
<meta property="og:url" content="https://creatordir-tools.vercel.app/{rel_path}">
<meta name="twitter:card" content="summary_large_image">
</head>
<body>
<header class="site-header">
  <div class="container">
    <a href="{prefix}" class="logo">\u26a1 CreatorAI</a>
    <button class="hamburger" onclick="this.classList.toggle(\'active\');document.querySelector(\'.nav-links\').classList.toggle(\'open\')"><span></span><span></span><span></span></button>
    <nav>
      <ul class="nav-links">
        <li><a href="{prefix}">Home</a></li>
        <li><a href="{prefix}tools/" class="active">Tools</a></li>
        <li><a href="{prefix}articles/">Guides</a></li>
        <li><a href="{prefix}resources/">Resources</a></li>
        <li><a href="{prefix}compare/">Compare</a></li>
        <li><a href="{prefix}about.html">About</a></li>
      </ul>
    </nav>
  </div>
</header>
<main>
  <div class="container">
    <nav class="breadcrumb"><a href="{prefix}">Home</a> / <a href="{prefix}tools/">Tools</a> / <span>Categories</span></nav>
  </div>
  {html_content}
</main>
<footer class="site-footer">
  <div class="container">
    <p><strong>CreatorAI Tools</strong> \u2014 AI tools for content creators worldwide</p>
    <p>&copy; 2026 CreatorAI &middot; <a href="{prefix}privacy.html">Privacy</a> &middot; <a href="{prefix}terms.html">Terms</a> &middot; <a href="{prefix}sitemap.xml">Sitemap</a></p>
  </div>
</footer>
<script src="{prefix}js/main.js"></script>
<script src="{prefix}js/smart-bar.js"></script>
</body>
</html>'''

# ===== 1. Category Directory Page =====
cats_html = '''<section class="section" style="padding-top:2rem">
  <div class="container">
    <div class="section-header">
      <h1>\U0001f4ca AI Tools by Category</h1>
      <p>Browse {total} AI tools organized into {cat_count} categories. Find the right tool for every creative task.</p>
    </div>
    <div class="card-grid">'''

for cat_key in CATEGORY_INFO:
    info = CATEGORY_INFO[cat_key]
    tools = db["data"].get(cat_key, [])
    top_stars = max((t["stars"] for t in tools), default=0)
    top_stars_str = f"{top_stars:,}" if top_stars else "N/A"
    
    cats_html += f'''
      <div class="card" style="border-top:3px solid {info['color']}">
        <div class="card-icon" style="background:{info['color']}15">{info['emoji']}</div>
        <h3><a href="{cat_key}-tools.html">{info['name']}</a></h3>
        <p class="card-desc">{info['desc'][:80]}</p>
        <div class="tool-features">
          <span class="tool-feature">{len(tools)} tools</span>
          <span class="tool-feature" style="background:{info['color']}15;color:{info['color']}">\u2b50 Top {top_stars_str}</span>
        </div>
      </div>'''

cats_html += '''
    </div>
  </div>
</section>'''

cats_html = cats_html.replace("{total}", str(db["total"])).replace("{cat_count}", str(len(CATEGORY_INFO)))

with open(os.path.join(base, "tools", "categories.html"), "w", encoding="utf-8") as f:
    f.write(make_page(cats_html, "AI Tools Categories - Browse by Type - CreatorAI Tools", "Browse AI tools organized by category. Writing, image, video, audio, marketing, code, and productivity tools.", "tools/categories.html"))
print("Created: tools/categories.html")

# ===== 2. Individual Category Pages =====
for cat_key, info in CATEGORY_INFO.items():
    tools = db["data"].get(cat_key, [])
    tools = sorted(tools, key=lambda x: -x["stars"])
    
    html = f'''<section class="section" style="padding-top:2rem">
  <div class="container">
    <div class="section-header">
      <h1>{info["emoji"]} {info["name"]}</h1>
      <p>{info["desc"]} <strong>{len(tools)} tools</strong> curated from GitHub, ranked by stars.</p>
    </div>
    
    <!-- Filters -->
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:1.5rem;padding:12px;background:#1e293b;border-radius:12px;border:1px solid #334155;">
      <span style="color:#94a3b8;font-size:13px;padding:6px 0;">\U0001f50d Filter:</span>
      <button class="tool-feature" onclick="sortTools('stars')" style="cursor:pointer;">\u2b50 Stars</button>
      <button class="tool-feature" onclick="sortTools('name')" style="cursor:pointer;">A-Z</button>
      <button class="tool-feature" onclick="sortTools('updated')" style="cursor:pointer;">\U0001f504 Recent</button>
      <span style="color:#94a3b8;font-size:13px;padding:6px 0;margin-left:auto;">Sorted by stars</span>
    </div>
    
    <div id="tool-list" class="card-grid" style="grid-template-columns:1fr;">'''
    
    for t in tools:
        stars = f"{t['stars']:,}"
        lang = t["language"][:15] if t["language"] else ""
        topics = " ".join([f'<span class="tool-feature">{tp[:15]}</span>' for tp in t["topics"][:4]])
        desc = t["description"][:200] + ("..." if len(t["description"]) > 200 else "")
        
        html += f'''
      <div class="tool-item">
        <div class="tool-icon" style="background:{info['color']}15;color:{info['color']};font-size:1rem;">GH</div>
        <div class="tool-body">
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            <h3 style="margin:0;"><a href="{t['url']}" target="_blank" rel="noopener">{t['name']}</a></h3>
            {f'<a href="{t["homepage"]}" target="_blank" rel="noopener" class="tool-feature" style="text-decoration:none;">\U0001f310 Website</a>' if t["homepage"] else ''}
          </div>
          <p>{desc}</p>
          <div class="tool-features">
            <span class="tool-feature">\u2b50 {stars}</span>
            <span class="tool-feature" style="background:{info['color']}15;color:{info['color']}">{lang}</span>
            <span class="tool-feature">{t["forks"]} forks</span>
            {topics}
          </div>
        </div>
      </div>'''
    
    html += '''</div>
  </div>
</section>'''
    
    with open(os.path.join(base, "tools", f"{cat_key}-tools.html"), "w", encoding="utf-8") as f:
        f.write(make_page(html, f"{info['name']} - {len(tools)} AI Tools - CreatorAI Tools", f"{info['desc']} Browse and compare {len(tools)} AI tools for {info['name'].lower()}.", f"tools/{cat_key}-tools.html"))
    print(f"Created: tools/{cat_key}-tools.html ({len(tools)} tools)")

print(f"\n=== Generated {len(CATEGORY_INFO)} category pages + 1 directory page ===")
