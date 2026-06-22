import os
base = r'D:\项目\工作区\工作5'
adir = os.path.join(base, 'articles')
tpl = os.path.join(base, 'sitemap.xml')

articles = sorted([f for f in os.listdir(adir) if f.endswith('.html') and f != 'index.html'])
urls = []
for a in articles:
    url = 'https://creatordir-tools.vercel.app/articles/' + a
    urls.append('  <url>\n    <loc>' + url + '</loc>\n    <lastmod>2026-06-23</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>')

sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://creatordir-tools.vercel.app/</loc>
    <lastmod>2026-06-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://creatordir-tools.vercel.app/deals.html</loc>
    <lastmod>2026-06-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
''' + '\n'.join(urls) + '\n</urlset>'

with open(tpl, 'w', encoding='utf-8') as f:
    f.write(sitemap)

print('Sitemap updated with ' + str(len(articles)) + ' articles')
print('Total URLs: ' + str(len(articles) + 2))
