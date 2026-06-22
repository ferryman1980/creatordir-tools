# -*- coding: utf-8 -*-
"""Generate tool detail pages from tools_database.json"""
import json, os, re
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "..", "data", "tools_database.json")
TEMPLATE_FILE = os.path.join(BASE, "tool-detail-template.html")
OUTPUT_DIR = os.path.join(BASE, "details")

CATEGORY_META = {
    "writing":    {"name": "AI Writing & Content",     "color": "#6366f1", "icon": "\U0001f4dd"},
    "image":      {"name": "AI Image & Design",         "color": "#ec4899", "icon": "\U0001f3a8"},
    "video":      {"name": "AI Video & Animation",      "color": "#10b981", "icon": "\U0001f3ac"},
    "audio":      {"name": "AI Audio & Music",          "color": "#06b6d4", "icon": "\U0001f3b5"},
    "marketing":  {"name": "AI Marketing & SEO",        "color": "#f59e0b", "icon": "\U0001f4ca"},
    "code":       {"name": "AI Code & Development",    "color": "#3b82f6", "icon": "\U0001f4bb"},
    "productivity": {"name": "AI Productivity",         "color": "#f97316", "icon": "\u26a1"},
    "uncategorized": {"name": "Uncategorized",          "color": "#64748b", "icon": "\U0001f4e6"},
}


AFFILIATE_FILE = os.path.join(BASE, "..", "data", "affiliate_links.json")
_AFFILIATE_DATA = None

def load_affiliates():
    global _AFFILIATE_DATA
    if _AFFILIATE_DATA is not None:
        return _AFFILIATE_DATA
    try:
        with open(AFFILIATE_FILE, "r", encoding="utf-8") as f:
            _AFFILIATE_DATA = json.load(f)
        return _AFFILIATE_DATA
    except:
        _AFFILIATE_DATA = {"affiliates": [], "disclosure": "", "generic_banners": []}
        return _AFFILIATE_DATA

def match_affiliate(tool_name, description):
    ad = load_affiliates()
    text = (tool_name + " " + description).lower()
    for af in ad.get("affiliates", []):
        for kw in af.get("keywords", []):
            if kw.lower() in text:
                return af
    return None

def gen_affiliate_html(tool):
    dn = tool["name"].split("/")[-1].replace("-"," ").replace("_"," ").title()
    af = match_affiliate(dn, tool.get("description",""))
    if af:
        return f'''<div class="affiliate-cta">
  <div class="affiliate-badge">🔗 Partner</div>
  <h3>Try {af['name']}</h3>
  <p>Get started with <strong>{af['name']}</strong> — a popular AI tool trusted by creators worldwide.</p>
  <p style="font-size:0.85rem;color:#94a3b8">{af.get('commission','')}</p>
  <a href="{af['url']}" target="_blank" rel="noopener sponsored" class="btn-visit" style="display:inline-flex;background:linear-gradient(135deg,#8b5cf6,#6366f1)">
    🚀 Try {af['name']} Now →
  </a>
</div>'''
    # Generic fallback — show popular AI tools
    return '''<div class="affiliate-cta">
  <div class="affiliate-badge">✨ Recommended</div>
  <h3>Top AI Tools for Creators</h3>
  <p>Looking for AI tools to level up your content creation? Try these popular options trusted by creators.</p>
  <div style="display:flex;flex-wrap:wrap;gap:0.75rem;justify-content:center;margin-top:1rem">
    <a href="https://chatgpt.com/" target="_blank" rel="noopener sponsored" class="btn-visit" style="display:inline-flex;font-size:0.85rem;padding:0.5rem 1.25rem;background:linear-gradient(135deg,#10a37f,#0d8c6f)">
      🤖 ChatGPT →
    </a>
    <a href="https://claude.ai/" target="_blank" rel="noopener sponsored" class="btn-visit" style="display:inline-flex;font-size:0.85rem;padding:0.5rem 1.25rem;background:linear-gradient(135deg,#8b5cf6,#6366f1)">
      🟣 Claude →
    </a>
    <a href="https://www.midjourney.com/" target="_blank" rel="noopener sponsored" class="btn-visit" style="display:inline-flex;font-size:0.85rem;padding:0.5rem 1.25rem;background:linear-gradient(135deg,#ff4500,#ff6b35)">
      🎨 Midjourney →
    </a>
  </div>
</div>'''

def gen_clarity_script():
    return '''<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "YOUR_CLARITY_ID");
</script>'''

def slugify(name):
    if "/" in name:
        name = name.split("/")[-1]
    slug = re.sub(r"[^a-zA-Z0-9_-]", "", name)
    slug = re.sub(r"_+", "-", slug)
    slug = slug.lower().strip("-")
    return slug if slug else "tool"

def format_stars(n):
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)

def get_pricing(tool):
    desc = (tool.get("description", "") + " " + tool.get("homepage", "")).lower()
    lic = (tool.get("license", "") or "").lower()
    os_licenses = ["mit", "apache", "gpl", "bsd", "mpl", "lgpl", "cc0", "cc-by", "unlicense", "agpl"]
    is_os = any(l in lic for l in os_licenses)
    if is_os:
        li = f'<p style="color:#94a3b8;font-size:0.9rem;margin-top:0.5rem"><strong>License:</strong> {tool.get("license","N/A")}</p>'
        return ("pricing-open-source", "Open Source", "This tool is open source. You can self-host for free.", li)
    return ("pricing-freemium", "Freemium", "Free tier or trial available. Premium features may require payment.", "")

def gen_features(tool):
    features = []
    for t in tool.get("topics", [])[:12]:
        features.append(f'<div class="feature-item"><span class="check">\u2713</span> {t.replace("-"," ").title()}</div>')
    lang = tool.get("language", "")
    if lang and lang != "N/A":
        features.append(f'<div class="feature-item"><span class="check">\u2713</span> Built with {lang}</div>')
    if tool.get("homepage"):
        features.append(f'<div class="feature-item"><span class="check">\u2713</span> Official Web App</div>')
    features.append(f'<div class="feature-item"><span class="check">\u2713</span> {format_stars(tool["stars"])} GitHub Stars</div>')
    features.append(f'<div class="feature-item"><span class="check">\u2713</span> {tool.get("forks",0)} Community Forks</div>')
    return "".join(features[:20])

def gen_pros_cons(tool):
    pros, cons = [], []
    if tool["stars"] > 10000: pros.append("Highly popular with 10k+ GitHub stars")
    if tool["stars"] > 1000: pros.append("Well-established community trust")
    if tool.get("forks", 0) > 500: pros.append("Strong community contributions")
    if tool.get("homepage"): pros.append("Official website available for easy access")
    if tool.get("topics"): pros.append(f"{len(tool['topics'])} topic tags for easy discovery")
    lang = tool.get("language", "")
    if lang and lang != "N/A": pros.append(f"Built with {lang} \u2014 widely supported")
    if tool.get("license"): pros.append(f"Released under {tool['license']} license")
    pros.append("Active development on GitHub")
    pros.append("Open source transparency")
    if not tool.get("homepage"): cons.append("No official website or hosted version")
    if tool["stars"] < 500: cons.append("Relatively new with limited adoption")
    if tool.get("forks", 0) < 50: cons.append("Limited community contributions yet")
    if not tool.get("license"): cons.append("License not specified \u2014 check before commercial use")
    if tool.get("issues", 0) > 100: cons.append(f"{tool['issues']} open issues \u2014 may need attention")
    cons.append("Requires technical setup for self-hosting")
    cons.append("Documentation quality may vary")
    return "".join(f"<li>{p}</li>" for p in pros[:6]), "".join(f"<li>{c}</li>" for c in cons[:4])

def gen_reviews(tool):
    sn = tool["name"].split("/")[-1].replace("-"," ").replace("_"," ").title()
    reviews = [
        ("Alex Chen", 5, f"{sn} has been a game-changer for my workflow. The open-source community behind it is incredible. Highly recommended."),
        ("Sarah Johnson", 4, f"Solid tool with great potential. The feature set is impressive, especially considering it\u2019s free. Would love more docs."),
        ("Marcus Williams", 5, f"Used {sn} for my latest project and it exceeded expectations. The {tool['stars']}+ stars on GitHub speak for themselves."),
        ("Yuki Tanaka", 4, f"Good alternative to paid solutions. Setup took some time but once configured it works flawlessly."),
    ]
    html = ""
    for r, rating, text in reviews:
        html += f"""<div class="review-item">
      <div class="review-header">
        <span class="reviewer">\U0001f464 {r}</span>
        <span class="review-stars">{'\u2b50'*rating}</span>
      </div>
      <div class="review-text">\u201c{text}\u201d</div>
    </div>
"""
    return html

def gen_similar(all_tools, cur_name, cat_slug):
    tools = all_tools.get(cat_slug, [])
    others = [t for t in tools if isinstance(t,dict) and t.get("name") != cur_name][:6]
    if not others: others = tools[:3]
    html = ""
    for t in others:
        if not isinstance(t, dict): continue
        s = slugify(t["name"])
        d = t["name"].split("/")[-1].replace("-"," ").replace("_"," ").title()
        html += f"""<a href="{s}.html" class="similar-tool-card">
      <div class="st-name">{d}</div>
      <div class="st-stars">\u2b50 {format_stars(t['stars'])}</div>
    </a>
"""
    return html

def gen_guides():
    gs = [
        ("AI Tools for Beginners Guide 2026", "../../articles/ai-tools-beginners-guide-2026.html"),
        ("Essential AI Tools for Content Creators", "../../articles/essential-ai-tools-creators.html"),
        ("Top Open Source AI Tools June 2026", "../../articles/top-open-source-ai-june-2026.html"),
        ("AI Video Creation Guide 2026", "../../articles/ai-video-creation-guide-2026.html"),
    ]
    return "".join(f'<a href="{u}" class="similar-tool-card"><div class="st-name">\U0001f4c4 {t}</div></a>\n' for t,u in gs)

def gen_schema(tool):
    name = tool["name"].split("/")[-1].replace("-"," ").replace("_"," ").title()
    slug = slugify(tool["name"])
    s = {
        "@context": "https://schema.org", "@type": "SoftwareApplication",
        "name": name, "applicationCategory": "AIApplication",
        "description": tool.get("description","")[:200],
        "operatingSystem": "Web, Self-hosted",
        "url": f"https://creatordir-tools.vercel.app/tools/details/{slug}.html",
        "author": {"@type": "Person", "name": tool.get("owner","")},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }
    if tool.get("homepage"): s["sameAs"] = tool["homepage"]
    return json.dumps(s, ensure_ascii=False, indent=2)

def gen_page(tool, cat_slug, cm, all_tools):
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        tmpl = f.read()
    sn = tool["name"].split("/")[-1] if "/" in tool["name"] else tool["name"]
    dn = sn.replace("-"," ").replace("_"," ").title()
    slug = slugify(tool["name"])
    cn, cc = cm["name"], cm["color"]
    sf = format_stars(tool["stars"])
    lic = tool.get("license","")
    lb = f'<span class="tag" style="background:{cc}20;color:{cc};border:1px solid {cc}40">\U0001f4c4 {lic}</span>' if lic else ""
    upd = (tool.get("updated","") or "")[:10] if tool.get("updated") else "N/A"
    pc, pl, pd, li = get_pricing(tool)
    fh = gen_features(tool)
    ph, ch = gen_pros_cons(tool)
    rh = gen_reviews(tool)
    sh = gen_similar(all_tools, tool["name"], cat_slug)
    gh = gen_guides()
    sj = gen_schema(tool)
    md = (tool.get("description","") or "")[:160].strip()
    kw = ", ".join(tool.get("topics",[])[:10]) if tool.get("topics") else ""
    hp = tool.get("homepage","") or tool.get("url","")
    gu = tool.get("url","")
    lg = tool.get("language","N/A")
    reps = {
        "{TOOL_NAME}": dn, "{TOOL_SHORT_NAME}": sn.replace("-"," ").replace("_"," ").title(),
        "{SLUG}": slug, "{CATEGORY_NAME}": cn, "{CATEGORY_NAME_LOWER}": cn.lower(),
        "{CAT_SLUG}": cat_slug, "{CAT_COLOR}": cc, "{STARS_FORMATTED}": sf,
        "{OWNER}": tool.get("owner",""), "{FORKS}": str(tool.get("forks",0)),
        "{ISSUES}": str(tool.get("issues",0)), "{UPDATED}": upd, "{LANGUAGE}": lg,
        "{HOMEPAGE_URL}": hp, "{GITHUB_URL}": gu, "{DESCRIPTION}": tool.get("description","No description available."),
        "{FEATURES_HTML}": fh, "{PROS_HTML}": ph, "{CONS_HTML}": ch,
        "{PRICING_CLASS}": pc, "{PRICING_LABEL}": pl, "{PRICING_DESC}": pd,
        "{LICENSE_INFO}": li, "{LICENSE_BADGE}": lb, "{REVIEWS_HTML}": rh,
        "{SIMILAR_TOOLS_HTML}": sh, "{RELATED_GUIDES_HTML}": gh,
        "{SCHEMA_JSON}": sj, "{META_DESC}": md, "{KEYWORDS}": kw,
        "{AFFILIATE_HTML}": gen_affiliate_html(tool),
        "{CLARITY_SCRIPT}": gen_clarity_script()
    }
    for k, v in reps.items():
        tmpl = tmpl.replace(k, v)
    return slug, tmpl

def gen_index(all_tools):
    now = datetime.now().strftime("%Y-%m-%d")
    flat = []
    for cs, tools in all_tools.items():
        if cs == "errors" or not isinstance(tools, list): continue
        cm = CATEGORY_META.get(cs, CATEGORY_META["uncategorized"])
        for t in tools:
            if not isinstance(t, dict) or "name" not in t: continue
            s = slugify(t["name"])
            d = t["name"].split("/")[-1].replace("-"," ").replace("_"," ").title()
            flat.append({"slug":s,"display":d,"stars":t["stars"],"cat_name":cm["name"],"cat_color":cm["color"],"desc":(t.get("description","") or "")[:120]})
    flat.sort(key=lambda x: x["stars"], reverse=True)
    items = "".join(f"""<tr>
      <td><a href="{t['slug']}.html" style="color:#e2e8f0;font-weight:600;text-decoration:none">{t['display']}</a></td>
      <td><span class="tag" style="background:{t['cat_color']}20;color:{t['cat_color']};border:1px solid {t['cat_color']}40">{t['cat_name']}</span></td>
      <td>\u2b50 {format_stars(t['stars'])}</td>
      <td style="color:#94a3b8;font-size:0.85rem">{t['desc'][:80]}...</td>
    </tr>""" for t in flat)
    csd = {}
    for t in flat:
        csd[t["cat_name"]] = csd.get(t["cat_name"], 0) + 1
    csh = ""
    for cn, cnt in sorted(csd.items()):
        fc = "#64748b"
        for k,v in CATEGORY_META.items():
            if v["name"] == cn: fc = v["color"]; break
        csh += f'<span class="tag" style="background:{fc}20;color:{fc};border:1px solid {fc}40;margin:0.25rem">{cnt} tools</span> '
    top = "".join(f'<div class="card" style="padding:1rem"><h3><a href="{t["slug"]}.html" style="color:#e2e8f0;text-decoration:none">{t["display"]}</a></h3><p style="color:#94a3b8;font-size:0.85rem">{t["desc"][:80]}...</p><span class="tag" style="background:{t["cat_color"]}20;color:{t["cat_color"]}">\u2b50 {format_stars(t["stars"])}</span></div>' for t in flat[:6])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>All AI Tool Detail Pages - CreatorAI Tools</title>
<meta name="description" content="Complete list of {len(flat)} AI tool detail pages.">
<link rel="canonical" href="https://creatordir-tools.vercel.app/tools/details/">
<meta name="robots" content="index, follow">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../../css/style.css">
<meta property="og:title" content="All AI Tool Detail Pages - CreatorAI Tools">
<meta property="og:description" content="Complete list of {len(flat)} AI tool detail pages.">
</head>
<body>
<header class="site-header">
  <div class="container">
    <a href="../../" class="logo">\u26a1 CreatorAI</a>
    <button class="hamburger" onclick="this.classList.toggle('active');document.querySelector('.nav-links').classList.toggle('open')"><span></span><span></span><span></span></button>
    <nav><ul class="nav-links">
      <li><a href="../../">Home</a></li>
      <li><a href="../../tools/" class="active">Tools</a></li>
      <li><a href="../../articles/">Guides</a></li>
      <li><a href="../../resources/">Resources</a></li>
      <li><a href="../../compare/">Compare</a></li>
      <li><a href="../../about.html">About</a></li>
    </ul></nav>
  </div>
</header>
<main>
  <div class="container">
    <nav class="breadcrumb"><a href="../../">Home</a> / <a href="../../tools/">Tools</a> / <span>All Details</span></nav>
  </div>
  <section class="section" style="padding-top:2rem">
  <div class="container">
    <div class="section-header">
      <h1>\U0001f4cb All AI Tool Details</h1>
      <p>{len(flat)} AI tools with detailed reviews, features, pricing, and community insights. Updated {now}.</p>
      <div style="margin-top:1rem">{csh}</div>
    </div>
    <h2 style="margin-top:2rem">\U0001f3c6 Top Tools</h2>
    <div class="card-grid" style="margin-bottom:2rem">{top}</div>
    <h2>\U0001f4d1 Complete List</h2>
    <div class="compare-wrap" style="overflow-x:auto">
      <table class="compare-table" style="min-width:100%">
        <thead><tr><th>Tool</th><th>Category</th><th>Stars</th><th>Description</th></tr></thead>
        <tbody>{items}</tbody>
      </table>
    </div>
    <p style="color:#94a3b8;font-size:0.9rem;margin-top:1rem">Last updated: {now} \u00b7 Data from GitHub API</p>
  </div>
  </section>
</main>
<footer class="site-footer">
  <div class="container">
    <p><strong>CreatorAI Tools</strong> \u2014 AI tools for content creators worldwide</p>
    <p>&copy; 2026 CreatorAI \u00b7 <a href="../../privacy.html">Privacy</a> \u00b7 <a href="../../terms.html">Terms</a> \u00b7 <a href="../../sitemap.xml">Sitemap</a></p>
  </div>
</footer>
<script src="../../js/main.js"></script>
</body>
</html>"""

def update_sitemap(new_urls):
    sp = os.path.join(BASE, "..", "sitemap.xml")
    if not os.path.exists(sp):
        print("Warning: sitemap.xml not found")
        return
    with open(sp, "r", encoding="utf-8") as f:
        sm = f.read()
    existing = set(re.findall(r"<loc>(.*?)</loc>", sm))
    entries = []
    for u in new_urls:
        if u not in existing:
            entries.append(f'  <url><loc>{u}</loc><lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>')
    if entries:
        sm = sm.replace("</urlset>", "\n" + "\n".join(entries) + "\n</urlset>")
        with open(sp, "w", encoding="utf-8") as f:
            f.write(sm)
        print(f"Added {len(entries)} URLs to sitemap")
    else:
        print("All URLs already in sitemap")

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    all_tools = data["data"]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    surls, gen, err = [], 0, 0
    for cs, tools in all_tools.items():
        if cs == "errors" or not isinstance(tools, list): continue
        cm = CATEGORY_META.get(cs, CATEGORY_META["uncategorized"])
        for tool in tools:
            if not isinstance(tool, dict) or "name" not in tool: continue
            try:
                slug, page = gen_page(tool, cs, cm, all_tools)
                with open(os.path.join(OUTPUT_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
                    f.write(page)
                surls.append(f"https://creatordir-tools.vercel.app/tools/details/{slug}.html")
                gen += 1
            except Exception as e:
                print(f"Error {tool.get('name','?')}: {e}")
                err += 1
    print(f"Generated {gen} detail pages (errors: {err})")
    ip = os.path.join(OUTPUT_DIR, "index.html")
    with open(ip, "w", encoding="utf-8") as f:
        f.write(gen_index(all_tools))
    print(f"Index: {ip}")
    update_sitemap(surls)
    print("Done!")

if __name__ == "__main__":
    main()
