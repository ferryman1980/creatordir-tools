import os, glob
from datetime import date

today = date.today().isoformat()
base = r"D:\项目\工作区\工作5"
articles_dir = os.path.join(base, "articles")
tools_details_dir = os.path.join(base, "tools", "details")
output = os.path.join(base, "sitemap.xml")

# Get all article files
html_files = glob.glob(os.path.join(articles_dir, "*.html"))
article_names = sorted([os.path.basename(f) for f in html_files])
print(f"Articles: {len(article_names)}")

# Get all tools/details files
tool_files = glob.glob(os.path.join(tools_details_dir, "*.html"))
tool_names = sorted([os.path.basename(f) for f in tool_files])
print(f"Tool details: {len(tool_names)}")

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
for page in ["deals-comparison", "promote", "submission-guide", "about", "privacy", "terms", "deals", "extensions", "free-ai-tools", "index", "news", "top-picks", "trending"]:
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
# Tool detail pages
for name in tool_names:
    urls.append(f'''  <url>
    <loc>https://creatordir-tools.vercel.app/tools/details/{name}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>''')

sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

with open(output, "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"Total URLs in sitemap: {len(urls)}")
print(f"File size: {len(sitemap)} bytes")
