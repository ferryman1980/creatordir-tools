#!/usr/bin/env python3
"""Generate search-index.json for CreatorAI Tools website."""
import os, json, re
from html.parser import HTMLParser
from collections import Counter

SITE_ROOT = r"D:\项目\工作区\工作5"
OUTPUT = os.path.join(SITE_ROOT, "search-index.json")

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.h1 = ""
        self.body_text = []
        self._in_title = False
        self._in_h1 = False
        self._in_body = False
        self._in_script = False
        self._in_style = False
        self._skip_depth = 0
    def handle_starttag(self, tag, attrs):
        tl = tag.lower()
        if tl == "title": self._in_title = True
        elif tl == "h1": self._in_h1 = True
        elif tl == "body": self._in_body = True
        elif tl in ("script", "style"):
            self._in_script = True; self._in_style = tl == "style"
        elif tl in ("nav", "header", "footer") and self._in_body:
            self._skip_depth += 1
        elif tl == "meta":
            d = dict(attrs)
            if d.get("name", "").lower() == "description":
                self.description = d.get("content", "")
    def handle_endtag(self, tag):
        tl = tag.lower()
        if tl == "title": self._in_title = False
        elif tl == "h1": self._in_h1 = False
        elif tl in ("script", "style"):
            self._in_script = False; self._in_style = False
        elif tl in ("nav", "header", "footer") and self._skip_depth > 0:
            self._skip_depth -= 1
    def handle_data(self, data):
        if self._in_title: self.title += data.strip()
        elif self._in_h1: self.h1 += data.strip()
        elif self._in_body and not self._in_script and not self._in_style and self._skip_depth == 0:
            s = data.strip()
            if s: self.body_text.append(s)

def infer_category(rel_path):
    rp = rel_path.replace("\\", "/")
    fn = os.path.basename(rel_path).lower()
    if "tools/details/" in rp: return "tool"
    if rp.startswith("articles/"): return "article"
    if "tools/" in rp and fn != "index.html": return "tool_category"
    if fn in ("deals.html", "deals-comparison.html"): return "deals"
    if fn in ("trending.html", "news.html"): return "news"
    if "promo_articles/" in rp: return "promo"
    if "compare/" in rp: return "comparison"
    if fn in ("extensions.html",): return "extension"
    return "page"

def extract_tags(title, description, h1, body):
    text = (title + " " + description + " " + h1 + " " + body).lower()
    tags = set()
    km = {
        "writing": ["writing","writer","article","blog","copy","content"],
        "image": ["image","photo","picture","design","art"],
        "video": ["video","editing","editor"],
        "audio": ["audio","voice","music","sound","podcast"],
        "seo": ["seo","search engine"],
        "marketing": ["marketing","email","social media"],
        "free": ["free","no credit card"],
        "open-source": ["open source","github","oss"],
        "code": ["code","coding","developer","programming"],
        "chatbot": ["chatbot","chat","conversation"],
        "translation": ["translation","translate","translator"],
        "productivity": ["productivity","automation","workflow"],
        "data": ["data","analytics","analysis"],
    }
    for tn, kws in km.items():
        if any(kw in text for kw in kws): tags.add(tn)
    return sorted(tags)

def main():
    print("Scanning: " + SITE_ROOT)
    entries = []
    skip_dirs = {"node_modules","__pycache__","images","screenshots","assets","go","data"}
    for root, dirs, files in os.walk(SITE_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
        for f in files:
            if not f.endswith(".html") or f.startswith("."): continue
            fp = os.path.join(root, f)
            rp = os.path.relpath(fp, SITE_ROOT)
            try:
                with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
            except: continue
            parser = PageParser()
            try: parser.feed(content)
            except: continue
            title = (parser.title or parser.h1 or f).strip()
            url_rp = rp.replace("\\", "/")
            url = "/" if url_rp == "index.html" else "/" + url_rp
            desc = parser.description or parser.h1 or title
            body_preview = " ".join(parser.body_text)[:300]
            body_preview = re.sub(r"\s+", " ", body_preview).strip()
            category = infer_category(rp)
            tags = extract_tags(title, desc, parser.h1, body_preview)
            entries.append({"title": title, "url": url, "description": desc, "category": category, "tags": tags})
    cat_order = {"tool":0,"tool_category":1,"article":2,"comparison":3,"deals":4,"news":5,"extension":6,"promo":7,"page":8}
    entries.sort(key=lambda e: (cat_order.get(e["category"],99), e["title"].lower()))
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print("OK: " + OUTPUT + " (" + str(len(entries)) + " entries)")
    for cat, cnt in sorted(Counter(e["category"] for e in entries).items()):
        print("  " + cat + ": " + str(cnt))

if __name__ == "__main__": main()
