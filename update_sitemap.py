import os, glob
from datetime import date

today = date.today().isoformat()
articles_dir = "D:\\项目\\工作区\\工作5\\articles"
output = "D:\\项目\\工作区\\工作5\\sitemap.xml"

# Get all article files
html_files = glob.glob(os.path.join(articles_dir, "*.html"))
article_names = sorted([os.path.basename(f) for f in html_files])

# Build sitemap
urls = []
# Homepage
urls.append(f'''  <url>
    <loc>https://creatordir-tools.vercel.app/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>''')
# Key pages
for page in ["deals-comparison", "promote", "submission-guide", "about", "privacy", "terms"]:
    urls.append(f'''  <url>
    <loc>https://creatordir-tools.vercel.app/{page}.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>''')
# Articles
for name in article_names:
    urls.append(f'''  <url>
    <loc>https://creatordir-tools.vercel.app/articles/{name}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>''')

sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

with open(output, "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"Sitemap generated: {len(urls)} URLs")
print(f"Articles in sitemap: {len(article_names)}")
print(f"File size: {len(sitemap)} bytes")

# Submit to IndexNow
import urllib.request
import json

indexnow_url = "https://www.bing.com/indexnow"
payload = {
    "host": "creatordir-tools.vercel.app",
    "key": "x5gn56sdfi",
    "keyLocation": "https://creatordir-tools.vercel.app/x5gn56sdfi.txt",
    "urlList": [f"https://creatordir-tools.vercel.app/articles/{n}" for n in article_names[:10]] + ["https://creatordir-tools.vercel.app/"]
}
try:
    req = urllib.request.Request(indexnow_url, 
        data=json.dumps(payload).encode(), 
        headers={"Content-Type": "application/json"},
        method="POST")
    resp = urllib.request.urlopen(req, timeout=10)
    print(f"\nIndexNow submission: HTTP {resp.status}")
except Exception as e:
    print(f"\nIndexNow submission: {e}")
