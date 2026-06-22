#!/usr/bin/env python3
# Generate news.html from crawled AI news data
import os, json, sys, io
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"D:\\项目\\工作区\\工作5"
os.chdir(BASE)

# Load news data
with open("data/ai_news.json", "r", encoding="utf-8") as f:
    news_data = json.load(f)

all_items = news_data.get("data", [])
# Deduplicate by URL
seen = set()
unique = []
for item in all_items:
    url = item.get("url","")
    if url and url not in seen:
        seen.add(url)
        unique.append(item)

all_items = unique[:50]  # Max 50
cat_emojis = {"Launches":"\U0001f680","Research":"\U0001f52c","Industry":"\U0001f3e2","Tutorials":"\U0001f4d6"}

# Build JavaScript news items array
js_items = []
for item in all_items:
    title = item.get("title","").replace("\\","\\\\").replace("'","\\'").replace(chr(10)," ")[:200]
    summary = item.get("summary","").replace("\\","\\\\").replace("'","\\'").replace(chr(10)," ")[:300]
    url = item.get("url","#").replace("'","%27")
    date = item.get("date","") or datetime.now().strftime("%b %d, %Y")
    cat = item.get("cat","Industry")
    source = item.get("source","AI News").replace("'","\\'")
    js_items.append(f"{{title:'{title}',date:'{date}',cat:'{cat}',summary:'{summary}',source:'{source}',url:'{url}'}}")

js_array = "[\n  " + ",\n  ".join(js_items) + "\n]"

# Read existing news.html and replace the news data section
with open("news.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find and replace the newsItems array
import re
pattern = r"const newsItems = \\[.*?\\];"
replacement = "const newsItems = " + js_array + ";"
html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Update hero stats
cat_count = len(set(i.get("cat","") for i in all_items))
html = re.sub(r'<span class="num">\d+\+*</span><span class="label">Stories</span>', f'<span class="num">{len(all_items)}+</span><span class="label">Stories</span>', html)
html = re.sub(r'<span class="num">\d+</span><span class="label">Categories</span>', f'<span class="num">{cat_count}</span><span class="label">Categories</span>', html)

with open("news.html", "w", encoding="utf-8") as f:
    f.write(html)

cats = {}
for item in all_items:
    c = item.get("cat","Industry")
    cats[c] = cats.get(c,0) + 1

print(f"News page generated: {len(all_items)} items, {len(cats)} categories")
for c, n in sorted(cats.items()):
    print(f"  {cat_emojis.get(c,'')} {c}: {n}")