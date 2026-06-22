import urllib.request, json, re

req = urllib.request.Request("https://futurepedia.io/submit-tool", headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode("utf-8")

# Get next.js data
match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    # Look for API routes
    pages = data.get("props", {}).get("pageProps", {})
    print(f"Keys: {list(pages.keys())}")
    
    # Look for build ID and routes
    print(f"Build ID: {data.get('buildId', 'N/A')}")
    print(f"Runtime config: {json.dumps(data.get('runtimeConfig', {}))[:500]"  )
else:
    print("No Next.js data found")

# Look for fetch calls in the page source
fetches = re.findall(r'["\x27](/api/[^"\x27]+)["\x27]', html)
print(f"API fetches: {len(fetches)}")
for f in list(set(fetches))[:15]:
    print(f"  {f}")
