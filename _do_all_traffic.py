import asyncio, time
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    
    # Start Edge with CDP
    import subprocess
    subprocess.run(["taskkill", "/f", "/im", "msedge.exe"], capture_output=True)
    await asyncio.sleep(2)
    
    edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    proc = subprocess.Popen([edge_path, "--remote-debugging-port=9222", "--no-first-run", "--new-window", "about:blank"])
    await asyncio.sleep(6)
    
    # Connect
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0] if edge.contexts else await edge.new_context()
    page = await ctx.new_page() if not ctx.pages else ctx.pages[0]
    
    try:
        # ===== DEV.TO ARTICLE 2 =====
        print("=== Article 2: Side Projects ===")
        await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        await page.evaluate("document.getElementById('article-form-title').value = arguments[0]", 
            "How Solo Developers Can Use AI to Ship Side Projects 10x Faster")
        await page.wait_for_timeout(300)
        
        content = """Building side projects solo used to mean doing everything yourself. With AI in 2026, one person can do the work of a team.

**AI Code Generation** - ChatGPT and Claude help generate apps from natural language, debug code, and write tests in seconds.

**AI Design** - Canva AI for mockups, Midjourney for logos, AI builders for landing pages.

**AI Content** - Write blogs, social posts, product descriptions, and demo videos with AI tools.

**AI Support** - Chatbots, auto-responses, FAQ generation, sentiment analysis.

**Real Example**: I built CreatorDir Tools (https://creatordir-tools.vercel.app) solo - now 200+ curated AI tools.

**Recommended**: Hostinger (https://www.hostinger.com?REFERRALCODE=ECA346010F8J) for hosting, ChatGPT/Claude for coding, Canva for design, Vercel for deployment.

What side project are you building?"""
        
        await page.evaluate("document.getElementById('article_body_markdown').value = arguments[0]", content)
        await page.wait_for_timeout(500)
        
        pub_btn = await page.query_selector("button:has-text('\u53d1\u5e03')")
        if pub_btn:
            await pub_btn.click()
            await page.wait_for_timeout(5000)
            print(f"Article 2 URL: {page.url}")
        else:
            print("No publish button")
        
        # ===== REDDIT CHECK =====
        print("\n=== Reddit ===")
        await page.goto("https://www.reddit.com", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        
        cookies = await page.context.cookies()
        token = None
        for c in cookies:
            if c.get("name") == "token_v2":
                token = c.get("value")
                break
        
        if token:
            result = await page.evaluate("""
                async (token) => {
                    const resp = await fetch("https://oauth.reddit.com/api/v1/me", {
                        headers: { "Authorization": "Bearer " + token }
                    });
                    const me = await resp.json();
                    const testResp = await fetch("https://oauth.reddit.com/api/submit", {
                        method: "POST",
                        headers: {
                            "Authorization": "Bearer " + token,
                            "Content-Type": "application/x-www-form-urlencoded"
                        },
                        body: new URLSearchParams({
                            api_type: "json", kind: "self", sr: "test",
                            title: "t" + Date.now(), text: "t", sendreplies: "false"
                        }).toString()
                    });
                    const d = await testResp.json();
                    return { user: me.name, errors: d.json ? d.json.errors : [] };
                }
            """, token)
            print(f"Reddit user: {result.get('user')}")
            print(f"Reddit errors: {result.get('errors')}")
        else:
            print("No Reddit token")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await page.close()
        await p.stop()
    
    print("\n=== ALL DONE ===")

asyncio.run(main())
