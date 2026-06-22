import urllib.request, json, re

# Check futurepedia submit page
req = urllib.request.Request("https://futurepedia.io/submit-tool", headers={"User-Agent": "Mozilla/5.0"})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    html = resp.read().decode("utf-8")
    print(f"HTML length: {len(html)}")
    
    apis = re.findall(r"https?://[^\"\']*api[^\"\']*", html)
    print(f"API endpoints: {len(apis)}")
    for a in apis[:5]: print(f"  {a}")
    
    actions = re.findall(r'<form[^>]*action=["\x27]([^"\x27]+)["\x27]', html)
    print(f"Form actions: {actions[:5] if actions else 'none'}")
    
    # Try to find what API the page fetches
    next_data = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if next_data:
        data = json.loads(next_data.group(1))
        print(f"Next.js: buildId={data.get('buildId', 'N/A')}")
        props = data.get("props", {}).get("pageProps", {})
        print(f"Page props keys: {list(props.keys())[:10]}")
except Exception as e:
    print(f"Error: {e}")
