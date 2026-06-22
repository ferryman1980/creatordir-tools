import os, re

DIR = r"D:\项目\工作区\工作5\articles"
TEMPLATE_FILE = os.path.join(DIR, "ai-article-writer-2026.html")

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    sample = f.read()

template_before = sample[:sample.index('<article class="article-content">')]
template_after = sample[sample.index("</article>") + 10:]

def make_article(filename, title, desc, h1, body):
    url = "https://creatordir-tools.vercel.app/articles/" + filename
    og_title = title + " - CreatorAI Tools"
    
    head_block = f'''<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "x5gn56sdfi");
</script>
<meta name="msvalidate.01" content="12DE03330024456C4B6D9FF9E4B9C31C" />
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://creatordir-tools.vercel.app/images/og-default.svg">
<meta property="og:site_name" content="CreatorAI Tools">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{desc}">
<title>{og_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<link rel="stylesheet" href="../css/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{h1}","datePublished":"2026-06-23","author":{{"@type":"Organization","name":"CreatorAI Tools"}}}}
</script>
<!-- Vercel Web Analytics -->
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}};</script>
<script defer src="/_vercel/insights/script.js"></script>'''
    
    idx = template_before.index("<!-- Microsoft Clarity -->")
    html = template_before[:idx] + head_block
    html += template_before[template_before.index("</head>"):]
    html += f'\n<article class="article-content">\n<h1>{h1}</h1>\n<p class="article-meta">Published: 2026-06-23</p>\n{body}\n<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">☕ Support this guide on Ko-fi</a></p>\n</article>\n'
    html += template_after
    
    with open(os.path.join(DIR, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created: {filename}")

def aff11():
    return '<a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a>'

def affHost():
    return '<a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger</a>'
