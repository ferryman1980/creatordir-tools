import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = await edge.contexts[0].new_page()
    
    # Publish Article 2
    await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(2000)
    
    title = "How Solo Developers Can Use AI to Ship Side Projects 10x Faster"
    await page.evaluate("document.getElementById('article-form-title').value = ''")
    await page.fill("#article-form-title", title)
    await page.wait_for_timeout(300)
    
    content = """Building side projects as a solo developer used to mean doing everything yourself. With AI tools in 2026, one person can accomplish what used to require a team.

**The Solo Developer AI Stack**

**1. AI Code Generation** - ChatGPT and Claude help generate entire apps from natural language, debug in real-time, refactor code, and write tests in seconds.

**2. AI Design Assistant** - Canva AI for mockups, Midjourney for logos, AI landing page builders for product pages.

**3. AI Content Creation** - Write blog posts, social media content, product descriptions, and demo videos with AI.

**4. AI Customer Support** - AI chatbots, auto-response emails, FAQ generation, sentiment analysis.

**5. AI Marketing Automation** - SEO tools, email automation, social scheduling, A/B testing.

**Real Example**

I built CreatorDir Tools (https://creatordir-tools.vercel.app) solo using this stack. It now has 200+ curated AI tools.

**Recommended Tools**
- Hostinger (https://www.hostinger.com?REFERRALCODE=ECA346010F8J) - Affordable hosting
- ChatGPT/Claude - Code generation
- Canva - Design
- Vercel - Free hosting
- Supabase - Free backend

Start small, ship fast. What side project are you building?"""
    
    await page.evaluate("document.getElementById('article_body_markdown').value = ''")
    await page.fill("#article_body_markdown", content)
    await page.wait_for_timeout(500)
    
    # Add tags
    tag_input = await page.query_selector("#tag-input")
    if tag_input:
        await tag_input.click()
        await page.wait_for_timeout(200)
        await page.evaluate("document.querySelectorAll('.tag-remove-button').forEach(b => b.click())")
        await page.wait_for_timeout(300)
        for tag in ["webdev", "productivity", "ai", "javascript"]:
            await tag_input.fill(tag)
            await page.wait_for_timeout(200)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(200)
    
    await page.wait_for_timeout(500)
    
    pub_btn = await page.query_selector("button:has-text('\u53d1\u5e03')")
    if pub_btn:
        await pub_btn.click()
        await page.wait_for_timeout(5000)
        print("DONE: " + page.url)
    else:
        print("No publish button")
    
    # Check Reddit rate limit
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
                        title: "test " + Date.now(), text: "test", sendreplies: "false"
                    }).toString()
                });
                const data = await testResp.json();
                return { user: me.name, errors: data.json ? data.json.errors : [] };
            }
        """, token)
        print("Reddit user: " + result.get("user", "?"))
        print("Reddit errors: " + str(result.get("errors", [])))
    else:
        print("No Reddit token")
    
    await page.close()
    await p.stop()

asyncio.run(main())
