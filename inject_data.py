# -*- coding: utf-8 -*-
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "github_crawl_output.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

resources_path = os.path.join(BASE, "resources", "index.html")
with open(resources_path, "r", encoding="utf-8") as f:
    html = f.read()

for i, snippet in enumerate(data["html_snippets"]):
    s = snippet
    s = s.replace("<h2>W Trending GitHub: Writing AI Tools</h2>", "<h2>\U0001f4e6 Trending GitHub: Writing AI Tools</h2>")
    s = s.replace("<h2>I Trending GitHub: Image AI Tools</h2>", "<h2>\U0001f4e6 Trending GitHub: Image AI Tools</h2>")
    s = s.replace("<h2>V Trending GitHub: Video AI Tools</h2>", "<h2>\U0001f4e6 Trending GitHub: Video AI Tools</h2>")
    data["html_snippets"][i] = s

github_html = "\n".join(data["html_snippets"])

marker = "<!-- Newsletter -->"
if marker in html:
    html = html.replace(marker, github_html + "\n\n  " + marker)
    with open(resources_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Injected GitHub data successfully!")
else:
    print("Could not find Newsletter marker")
