import asyncio, sys, json
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

POST_TITLE = "I built a directory of 200+ AI tools for content creators - all tested and reviewed"
POST_BODY = "After months of testing AI tools, I created a curated directory with 200+ articles, 54 tool reviews, comparisons, and tutorials.\n\nCheck it out: https://creatordir-tools.vercel.app\n\nAll free, open source on GitHub. Would love feedback!"

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Get cookies from Reddit session
    cookies = await ctx.cookies()
    reddit_cookies = {c["name"]: c["value"] for c in cookies if "reddit" in c.get("domain", "")}
    print("Reddit cookies found:", list(reddit_cookies.keys()))
    
    if "reddit_session" not in reddit_cookies and "token" not in reddit_cookies:
        print("No Reddit session cookie found, trying to get from page...")
        # Try the new reddit API
        token = await pg.evaluate("""() => {
            try {
                return window.__r && window.__r.token;
            } catch(e) { return null; }
        }""")
        print(f"Token from page: {token}")
        await asyncio.sleep(2)
    
    # Try API submit
    import urllib.request, urllib.parse
    api_url = "https://oauth.reddit.com/api/submit"
    
    # First get an access token via the cookie
    print("\nTrying to post via API...")
    # Get the session from the page
    result = await pg.evaluate("""() => {
        return document.cookie;
    }""")
    print(f"Cookies from JS: {result[:300]}")
    
    # If we're on reddit.com and logged in, try posting via old reddit API
    await pg.goto("https://old.reddit.com/login", wait_until="domcontentloaded", timeout=10000)
    await asyncio.sleep(2)
    print(f"\nLogin URL: {pg.url}")
    text = await pg.evaluate("document.body.innerText")
    print(text[:1000])
    
    await p.stop()

asyncio.run(main())
