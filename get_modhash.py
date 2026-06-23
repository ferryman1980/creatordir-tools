import asyncio, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Get cookies
    cookies = await ctx.cookies()
    session_cookie = ""
    csrf_token = ""
    for c in cookies:
        if "reddit" in c.get("domain", ""):
            if c["name"] == "reddit_session":
                session_cookie = c["value"]
            if c["name"] == "csrf_token":
                csrf_token = c["value"]
    
    print(f"reddit_session: {session_cookie[:30]}...")
    print(f"csrf_token: {csrf_token[:20]}...")
    
    # Get modhash
    await pg.goto("https://www.reddit.com/api/me.json", wait_until="domcontentloaded", timeout=10000)
    await asyncio.sleep(2)
    json_text = await pg.evaluate("document.body.innerText")
    print(f"\nMe API response: {json_text[:500]}")
    
    # Parse modhash
    try:
        data = json.loads(json_text)
        modhash = data.get("data", {}).get("modhash", "")
        print(f"Modhash: {modhash[:20] if modhash else 'NOT FOUND'}")
    except:
        print("Could not parse JSON")
        modhash = ""
    
    await p.stop()

asyncio.run(main())
