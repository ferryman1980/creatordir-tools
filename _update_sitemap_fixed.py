import os, glob
from datetime import date

today = date.today().isoformat()
articles_dir = os.path.join("D:", os.sep, "项目", "工作区", "工作5", "articles")
output = os.path.join("D:", os.sep, "项目", "工作区", "工作5", "sitemap.xml")

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
for page in ["deals-comparison", "promote", "submission-guide", "about", "privacy", "terms", "deals", "extensions", "free-ai-tools", "index", "news", "top-picks", "trending", "404"]:
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

