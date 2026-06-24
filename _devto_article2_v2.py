import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = await edge.contexts[0].new_page()
    
    await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(3000)
    
    # Fill title
    await page.evaluate("document.getElementById('article-form-title').value = ''")
    await page.evaluate("document.getElementById('article-form-title').value = 'How Solo Developers Can Use AI to Ship Side Projects 10x Faster'")
    await page.wait_for_timeout(300)
    
    # Fill body
    content = """Building side projects solo used to mean doing everything yourself. With AI in 2026, one person can do the work of a team.

**AI Code Generation** - ChatGPT and Claude help generate apps from natural language, debug code, and write tests in seconds.

**AI Design** - Canva AI for mockups, Midjourney for logos, AI builders for landing pages.

**AI Content** - Write blogs, social posts, product descriptions, and demo videos with AI tools.

**AI Support** - Chatbots, auto-responses, FAQ generation, sentiment analysis.

**Real Example**: I built CreatorDir Tools (https://creatordir-tools.vercel.app) solo - now 200+ curated AI tools.

**Recommended**: Hostinger (https://www.hostinger.com?REFERRALCODE=ECA346010F8J) for hosting, ChatGPT/Claude for coding, Canva for design, Vercel for deployment.

What side project are you building?"""
    await page.evaluate("document.getElementById('article_body_markdown').value = ''")
    await page.evaluate("document.getElementById('article_body_markdown').value = " + repr(content))
    await page.wait_for_timeout(500)
    
    # Set tags via JS
    await page.evaluate("""
        const tagInput = document.getElementById('tag-input');
        if (tagInput) {
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(tagInput, 'webdev');
            tagInput.dispatchEvent(new Event('input', { bubbles: true }));
        }
    """)
    await page.wait_for_timeout(500)
    
    # Click publish
    pub_btn = await page.query_selector("button:has-text('发布')")
    if pub_btn:
        await pub_btn.click()
        await page.wait_for_timeout(5000)
        print("DONE: " + page.url)
    else:
        print("No publish button found")
        # Try "Publish" text
        pub_btn = await page.query_selector("button:has-text('Publish')")
        if pub_btn:
            await pub_btn.click()
            await page.wait_for_timeout(5000)
            print("DONE: " + page.url)
        else:
            print("Still no button")
    
    await page.close()
    await p.stop()

asyncio.run(main())
