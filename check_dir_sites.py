import urllib.request, json, re
sites = [
    "https://futurepedia.io/submit-tool",
    "https://theresanaiforthat.com/submit/",
    "https://topai.tools/submit",
    "https://toolsfu.com/submit-tool",
    "https://aitoolsdirectory.com/submit",
    "https://saasaitools.com/submit",
    "https://aitoolhunt.com/submit",
    "https://futuretools.io/submit-a-tool"
]
for url in sites:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=8)
        html = resp.read().decode("utf-8", errors="ignore")
        forms = re.findall(r"<form[^>]*action=\"([^\"]+)\"", html[:5000])
        print(f"OK {url[:50]} -> forms: {len(forms)}")
        for f in forms[:3]:
            print(f"  {f[:60]}")
    except Exception as e:
        print(f"ERR {url[:50]} -> {str(e)[:40]}")
