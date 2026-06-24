import asyncio, subprocess
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    
    subprocess.run(["taskkill", "/f", "/im", "msedge.exe"], capture_output=True)
    await asyncio.sleep(2)
    
    edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    subprocess.Popen([edge_path, "--remote-debugging-port=9222", "--no-first-run", "--new-window", "about:blank"])
    await asyncio.sleep(6)
    
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0] if edge.contexts else await edge.new_context()
    pages = ctx.pages
    page = pages[0] if pages else await ctx.new_page()
    
    try:
        # ===== DEV.TO ARTICLE 2 =====
        print("=== Dev.to Article 2 ===")
        await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        await page.eval_on_selector("#article-form-title", "el => el.value = arguments[1]", "How Solo Developers Can Use AI to Ship Side Projects 10x Faster")
        # Actually let me use fill() which is cleaner
        await page.fill("#article-form-title", "How Solo Developers Can Use AI to Ship Side Projects 10x Faster")
        await page.wait_for_timeout(400)
        
        content = """Building side projects solo used to mean doing everything yourself. With AI in 2026, one person can do the work of a team.

**AI Code Generation** - ChatGPT and Claude help generate apps from natural language.

**AI Design** - Canva AI for mockups, Midjourney for logos.

**AI Content** - Write blogs, social posts, and demos with AI.

**AI Support** - Chatbots, auto-responses, FAQ generation.

**Real Example**: I built CreatorDir Tools (https://creatordir-tools.vercel.app) solo - now 200+ curated AI tools.

**Recommended**: Hostinger (https://www.hostinger.com?REFERRALCODE=ECA346010F8J) for hosting, ChatGPT/Claude for coding.

What side project are you building?"""
        
        await page.fill("#article_body_markdown", content)
        await page.wait_for_timeout(500)
        
        pub_btn = await page.query_selector("button:has-text('发布')")
        if pub_btn:
            await pub_btn.click()
            await page.wait_for_timeout(5000)
            print(f"Article 2 URL: {page.url}")
        else:
            print("No publish button - trying alternatives")
            # Check for any submit buttons
            buttons = await page.eval_on_selector_all("button", "els => els.map(e => e.innerText)")
            print(f"Buttons: {[b for b in buttons if b.strip()]}")
        
        # ===== REDDIT CHECK =====
        print("\n=== Reddit Check ===")
        await page.goto("https://www.reddit.com", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        
        cookies = await page.context.cookies()
        token = None
        for c in cookies:
            if c.get("name") == "token_v2":
                token = c.get("value")
                break
        
        if token:
            result = await page.evaluate(f"""
                async () => {{
                    const resp = await fetch("https://oauth.reddit.com/api/v1/me", {{
                        headers: {{ "Authorization": "Bearer {token}" }}
                    }});
                    const me = await resp.json();
                    const testResp = await fetch("https://oauth.reddit.com/api/submit", {{
                        method: "POST",
                        headers: {{
                            "Authorization": "Bearer {token}",
                            "Content-Type": "application/x-www-form-urlencoded"
                        }},
                        body: new URLSearchParams({{
                            api_type: "json", kind: "self", sr: "test",
                            title: "t" + Date.now(), text: "t", sendreplies: "false"
                        }}).toString()
                    }});
                    const d = await testResp.json();
                    return {{ user: me.name, errors: d.json ? d.json.errors : [] }};
                }}
            """)
            print(f"Reddit user: {result.get('user')}")
            print(f"Reddit errors: {result.get('errors')}")
        else:
            print("No Reddit token found")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await page.close()
        await p.stop()
    
    print("\n=== ALL DONE ===")

asyncio.run(main())
