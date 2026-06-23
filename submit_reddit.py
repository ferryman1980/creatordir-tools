import asyncio, sys, json, urllib.request, urllib.parse, http.cookiejar
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    # Get cookies from existing browser
    from playwright.async_api import async_playwright
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Get session info
    cookies = await ctx.cookies()
    session_str = ""
    token_v2 = ""
    for c in cookies:
        if "reddit" in c.get("domain", ""):
            if c["name"] == "reddit_session": session_str = c["value"]
            if c["name"] == "token_v2": token_v2 = c["value"]
    
    # Get modhash
    await pg.goto("https://www.reddit.com/api/me.json", wait_until="domcontentloaded", timeout=10000)
    await asyncio.sleep(1)
    json_text = await pg.evaluate("document.body.innerText")
    data = json.loads(json_text)
    modhash = data.get("data", {}).get("modhash", "")
    username = data.get("data", {}).get("name", "")
    print(f"Logged in as: {username}")
    print(f"Modhash: {modhash[:15]}...")
    
    # Post to Reddit via API
    post_data = {
        "kind": "self",
        "sr": "ArtificialIntelligence",
        "title": "I built a directory of 200+ AI tools for content creators - all tested and reviewed",
        "text": "After months of testing AI tools, I created a curated directory at https://creatordir-tools.vercel.app\n\nFeatures: 200+ articles, 54 tool reviews, comparisons, and tutorials\n\nAll free, open source on GitHub. Would love feedback from the community!",
        "uh": modhash,
        "api_type": "json",
        "sendreplies": "true"
    }
    
    # Build cookie header
    cookie_header = f"reddit_session={session_str}; token_v2={token_v2}"
    
    req = urllib.request.Request(
        "https://www.reddit.com/api/submit",
        data=urllib.parse.urlencode(post_data).encode(),
        headers={
            "User-Agent": "python:creatordir-tools:v1.0 (by /u/" + username + ")",
            "Cookie": cookie_header,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read().decode())
        print(f"\nAPI Response: {json.dumps(result, indent=2)[:1000]}")
        
        if result.get("json", {}).get("errors"):
            print(f"\nERRORS: {result['json']['errors']}")
        else:
            print(f"\n✅ POST SUCCESSFUL!")
            print(f"Post URL: https://www.reddit.com/r/ArtificialIntelligence/comments/{result.get('json',{}).get('data',{}).get('id','')}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        print(e.read().decode()[:500])
    except Exception as e:
        print(f"Error: {e}")
    
    await p.stop()

asyncio.run(main())
