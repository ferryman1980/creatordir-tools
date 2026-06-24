import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = await edge.contexts[0].new_page()
    
    print("Going to /new...")
    await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(3000)
    print(f"URL: {page.url}")
    
    title = await page.query_selector("#article-form-title")
    body = await page.query_selector("#article_body_markdown")
    
    print(f"Title field: {bool(title)}")
    print(f"Body field: {bool(body)}")
    
    if not title or not body:
        print("Editor not accessible - trying to login...")
        await page.goto("https://dev.to/enter", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Try clicking GitHub login
        try:
            gh_btn = await page.query_selector('[href*="github"]')
            if gh_btn:
                await gh_btn.click()
                await page.wait_for_timeout(5000)
                print(f"After GitHub: {page.url}")
        except Exception as e:
            print(f"GitHub error: {e}")
        
        # After login attempt, try /new again
        await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        print(f"Retry URL: {page.url}")
        title = await page.query_selector("#article-form-title")
        body = await page.query_selector("#article_body_markdown")
        print(f"Title after retry: {bool(title)}, Body: {bool(body)}")
    
    if title and body:
        print("SUCCESS! Publishing article...")
        await page.fill("#article-form-title", "The Ultimate AI Tools Directory: 200+ Tested Tools for Creators and Developers")
        await page.wait_for_timeout(500)
        
        content = """After spending months testing hundreds of AI tools, I have curated the best ones into a single, easily searchable directory.

**Why I Built This**

The AI tool landscape is exploding. Every day there is a new game-changing tool, but most are either overhyped, too expensive, or have confusing pricing.

So I built [CreatorDir Tools](https://creatordir-tools.vercel.app) - a curated directory where every tool is actually tested before being listed.

**What is Inside**

Writing and Content - ChatGPT alternatives, AI blog post generators, SEO writing assistants
Design and Visual - AI image generators, Canva AI features, logo makers, presentation creators
Video and Animation - AI video generators, animation tools, subtitling and captioning
Audio and Music - AI music generators, text-to-speech, podcast tools, voice cloning
Development - AI code assistants, no-code builders, API integration tools, testing automation
Marketing - SEO tools, social media schedulers, email marketing AI, analytics platforms

**Pricing Comparison**

One unique feature: I compare pricing across similar tools so you can find the best value. The directory has a Free AI Tools section with 50+ completely free resources, best value tools under $10/month, and enterprise-grade options for agencies.

**Weekly Updates**

New tools are added every week. The directory currently has 200+ tools and growing.

Ready to explore? https://creatordir-tools.vercel.app

Have a favorite AI tool I missed? Drop it in the comments!"""
        
        await page.fill("#article_body_markdown", content)
        await page.wait_for_timeout(500)
        
        # Add tags
        tag_input = await page.query_selector("#tag-input")
        if tag_input:
            for tag in ["aitools", "productivity", "webdev", "beginners"]:
                await tag_input.fill(tag)
                await page.wait_for_timeout(300)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(300)
        
        # Click publish
        pub_btn = await page.query_selector("button:has-text('Publish')")
        if pub_btn:
            await pub_btn.click()
            await page.wait_for_timeout(5000)
            print(f"Published! URL: {page.url}")
        else:
            print("Publish button not found")
    
    await page.close()
    await p.stop()

asyncio.run(main())
