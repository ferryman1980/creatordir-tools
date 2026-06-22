import json, os, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = os.getcwd()
os.chdir(BASE)
with open("data/ai_news.json", "r", encoding="utf-8") as f:
    news_data = json.load(f)
items = news_data.get("data", [])
seen = set()
unique = []
for item in items:
    url = item.get("url", "")
    if url and url not in seen:
        seen.add(url)
        unique.append(item)
for item in unique:
    item["score"] = item.get("score", 0)
top_news = sorted(unique, key=lambda x: -x.get("score", 0))[:5]
print(f"Top {len(top_news)} news items selected")

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove old section
old_start = html.find("<!-- ===== Top AI News")
if old_start > 0:
    next_sec = html.find("Browse by Category", old_start)
    if next_sec > old_start:
        sec_end = html.rfind("</section>", old_start, next_sec)
        if sec_end > old_start:
            sec_end = html.find("</section>", sec_end) + len("</section>")
            html = html[:old_start] + html[sec_end:]

insert_target = "Browse by Category"
insert_at = html.find(insert_target)
if insert_at < 0:
    insert_at = html.find("Popular Sections")
if insert_at < 0:
    insert_at = html.find('<footer class="site-footer">')
if insert_at < 0:
    print("ERROR: Cannot find insertion point")
    exit(1)

before = html[:insert_at]
after = html[insert_at:]
emojis = {"Launches":"🚀", "Research":"🔬", "Industry":"🏢", "Tutorials":"📖"}
block = '\n  <!-- ===== Top AI News (Auto-generated) ===== -->\n'
block += '  <section class="section" style="background:linear-gradient(135deg,#0f172a,#1e1b4b);color:#fff">\n'
block += '    <div class="container">\n'
block += '      <div class="section-header">\n'
block += '        <h2 style="color:#fff">📰 Top AI News</h2>\n'
block += '        <p style="color:#94a3b8">The most important AI stories right now, curated from global sources.</p>\n'
block += '      </div>\n'
block += '      <div class="card-grid">\n'

for item in top_news:
    title = item.get("title", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")[:120]
    summary = item.get("summary", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")[:150]
    url = item.get("url", "#")
    source = item.get("source", "AI News")
    cat = item.get("cat", "Industry")
    date = item.get("date", "")
    score = item.get("score", 0)
    emoji = emojis.get(cat, "📰")
    block += '        <div class="card" style="border-top:3px solid #8b5cf6;background:rgba(255,255,255,0.05);backdrop-filter:blur(10px)">\n'
    block += '          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">\n'
    block += '            <span style="font-size:0.75rem;padding:2px 10px;border-radius:12px;background:rgba(139,92,246,0.2);color:#a78bfa;font-weight:600">' + emoji + ' ' + cat + '</span>\n'
    if score:
        block += '            <span style="font-size:0.8rem;color:#f59e0b">⭐ ' + str(score) + '</span>\n'
    block += '          </div>\n'
    block += '          <h3 style="font-size:1rem;font-weight:700;color:#fff;line-height:1.3;margin-bottom:6px"><a href="' + url + '" target="_blank" rel="noopener" style="color:#fff;text-decoration:none">' + title + '</a></h3>\n'
    block += '          <p style="font-size:0.85rem;color:#94a3b8;line-height:1.4;margin-bottom:8px">' + summary + '</p>\n'
    block += '          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.75rem;color:#64748b">\n'
    block += '            <span>' + source + '</span>\n'
    if date:
        block += '            <span>' + date + '</span>\n'
    block += '          </div>\n'
    block += '          <a href="news.html" style="display:inline-block;margin-top:10px;font-size:0.8rem;color:#a78bfa;font-weight:600;text-decoration:none">View all news →</a>\n'
    block += '        </div>\n'

block += '      </div>\n    </div>\n  </section>\n'
html = before + block + after

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"Homepage updated: {len(html)} bytes")

