import asyncio, json
from playwright.async_api import async_playwright

REDDIT_SUBREDDITS = ["webdev", "SideProject", "SaaS", "alphaAI", "artificial", "microsaas", "indiehacking"]

POST_TITLE = "I built a curated directory of 200+ AI tools - all tested and organized by use case"
POST_TEXT = """Hey everyone! 👋

After testing hundreds of AI tools, I've curated the best ones into a single directory:

🔧 **CreatorDir Tools** → https://creatordir-tools.vercel.app

What's inside:
✅ 200+ AI tools organized by category (writing, design, video, audio, coding, marketing)
✅ Each tool has been tested and reviewed
✅ Compare pricing and features side by side
✅ Weekly updates with new additions
✅ Free tools section with 50+ completely free AI resources

Whether you're a content creator, developer, or business owner, there's something here for you.

Would love to hear which AI tools you're using right now! 🚀"""

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    
    # Get token from Reddit page cookies
    page = await edge.contexts[0].new_page()
    await page.goto("https://www.reddit.com", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(2000)
    
    cookies = await page.context.cookies()
    token_v2 = None
    for c in cookies:
        if c.get("name") == "token_v2":
            token_v2 = c.get("value")
            break
    
    if not token_v2:
        # Try from localStorage
        try:
            ls = await page.evaluate("() => localStorage.getItem('chat:access-token')")
            if ls:
                data = json.loads(ls)
                token_v2 = data.get("token")
        except:
            pass
    
    if not token_v2:
        print("ERROR: No OAuth token found")
        await page.close()
        await p.stop()
        return
    
    print(f"Token found: {token_v2[:50]}...")
    
    # Post to each subreddit
    results = []
    for sr in REDDIT_SUBREDDITS:
        try:
            # Create post via API
            post_data = {
                "api_type": "json",
                "kind": "self",
                "sr": sr,
                "title": POST_TITLE,
                "text": POST_TEXT,
                "sendreplies": True
            }
            
            resp = await page.evaluate(f"""
                async () => {{
                    const resp = await fetch("https://oauth.reddit.com/api/submit", {{
                        method: "POST",
                        headers: {{
                            "Authorization": "Bearer {token_v2}",
                            "Content-Type": "application/x-www-form-urlencoded"
                        }},
                        body: new URLSearchParams({json.dumps(post_data)}).toString()
                    }});
                    const data = await resp.json();
                    return {{ status: resp.status, data: data }};
                }}
            """)
            
            if resp.get("data",{}).get("json",{}).get("errors"):
                errs = resp["data"]["json"]["errors"]
                results.append(f"[{sr}] FAILED: {errs}")
                print(f"[{sr}] FAILED: {errs}")
            else:
                url = resp.get("data",{}).get("json",{}).get("data",{}).get("url","")
                results.append(f"[{sr}] ✅ POSTED: {url}")
                print(f"[{sr}] ✅ POSTED: {url}")
            
            await page.wait_for_timeout(3000)  # Rate limit delay
            
        except Exception as e:
            results.append(f"[{sr}] ERROR: {e}")
            print(f"[{sr}] ERROR: {e}")
    
    print("\n=== SUMMARY ===")
    for r in results:
        print(r)
    
    await page.close()
    await p.stop()

asyncio.run(main())
