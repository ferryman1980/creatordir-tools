import os
DIR = r"D:\项目\工作区\工作5\articles"
TEMP = os.path.join(DIR, "ai-article-writer-2026.html")
with open(TEMP, "r", encoding="utf-8") as f:
    sample = f.read()
tb = sample[:sample.index('<article class="article-content">')]
ta = sample[sample.index("</article>") + 10:]

def mkart(fn, title, desc, h1, body):
    url = "https://creatordir-tools.vercel.app/articles/" + fn
    og = title + " - CreatorAI Tools"
    hb = '''<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "x5gn56sdfi");
</script>
<meta name="msvalidate.01" content="12DE03330024456C4B6D9FF9E4B9C31C" />
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:title" content="''' + og + '''">
<meta property="og:description" content="''' + desc + '''">
<meta property="og:type" content="article">
<meta property="og:url" content="''' + url + '''">
<meta property="og:image" content="https://creatordir-tools.vercel.app/images/og-default.svg">
<meta property="og:site_name" content="CreatorAI Tools">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="''' + og + '''">
<meta name="twitter:description" content="''' + desc + '''">
<title>''' + og + '''</title>
<meta name="description" content="''' + desc + '''">
<link rel="canonical" href="''' + url + '''">
<meta name="robots" content="index, follow">
<link rel="stylesheet" href="../css/style.css">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"''' + h1 + '''","datePublished":"2026-06-23","author":{"@type":"Organization","name":"CreatorAI Tools"}}
</script>
<!-- Vercel Web Analytics -->
<script>window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments)};</script>
<script defer src="/_vercel/insights/script.js"></script>'''
    i = tb.index("<!-- Microsoft Clarity -->")
    html = tb[:i] + hb + tb[tb.index("</head>"):]
    art = '\n<article class="article-content">\n<h1>' + h1 + '</h1>\n<p class="article-meta">Published: 2026-06-23</p>\n' + body + '\n<p style="margin-top:2rem"><a href="https://ko-fi.com/kangjian" target="_blank" rel="noopener">\u2615 Support this guide on Ko-fi</a></p>\n</article>\n'
    html += art + ta
    with open(os.path.join(DIR, fn), "w", encoding="utf-8") as f:
        f.write(html)
    print("Created:", fn)

def el():
    return '<a href="https://try.elevenlabs.io/ebksqtv6a5m6" target="_blank" rel="nofollow sponsored">ElevenLabs</a>'
def ho():
    return '<a href="https://www.hostinger.com?REFERRALCODE=ECA346010F8J" target="_blank" rel="nofollow sponsored">Hostinger</a>'
