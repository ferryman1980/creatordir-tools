import urllib.request, json, re
import os

# Read sitemap using os path to handle Chinese chars
sitemap_path = os.path.join("D:", os.sep, "项目", "工作区", "工作5", "sitemap.xml")
print(f"Reading: {sitemap_path}")

with open(sitemap_path, "r", encoding="utf-8") as f:
    sitemap = f.read()

urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
print(f"Total URLs: {len(urls)}")

KEY = "e8f3c7a1b2d4e5f6a7b8c9d0e1f2a3b4"
payload = json.dumps({
    "host": "creatordir-tools.vercel.app",
    "key": KEY,
    "keyLocation": f"https://creatordir-tools.vercel.app/{KEY}.txt",
    "urlList": urls
}).encode("utf-8")

for endpoint, name in [("https://api.indexnow.org/indexnow", "IndexNow"),
                        ("https://www.bing.com/indexnow", "Bing")]:
    try:
        req = urllib.request.Request(
            endpoint, data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=15)
        print(f"{name}: HTTP {resp.status}")
    except Exception as e:
        print(f"{name}: {e}")

print("Done!")
