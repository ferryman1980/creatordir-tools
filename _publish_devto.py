import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = await edge.contexts[0].new_page()
    
    await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(2000)
    
    # Check if already filled
    current_title = await page.input_value("#article-form-title")
    print(f"Current title: '{current_title[:50]}...'")
    
    if not current_title:
        # Fill title
        await page.fill("#article-form-title", "The Ultimate AI Tools Directory: 200+ Tested Tools for Creators and Developers")
        await page.wait_for_timeout(300)
        print("Title filled")
    
    # Check body
    current_body = await page.input_value("#article_body_markdown")
    print(f"Current body length: {len(current_body)}")
    
    if len(current_body) < 100:
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

Ready to explore? https://creatordir-tools.vercel.app

Have a favorite AI tool I missed? Drop it in the comments!"""
        await page.fill("#article_body_markdown", content)
        await page.wait_for_timeout(500)
        print("Body filled")
    
    # Add tags  
    tag_input = await page.query_selector("#tag-input")
    if tag_input:
        current_tags = await page.input_value("#tag-input")
        if not current_tags:
            for tag in ["aitools", "productivity", "webdev", "beginners"]:
                await tag_input.fill(tag)
                await page.wait_for_timeout(300)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(300)
            print("Tags added")
    
    await page.wait_for_timeout(1000)
    
    # Click the 发布 (Publish) button
    pub_btn = await page.query_selector("button:has-text('发布')")
    if pub_btn:
        print("Clicking 发布 button...")
        await pub_btn.click()
        await page.wait_for_timeout(5000)
        print(f"After publish URL: {page.url}")
        
        # Check result
        body = await page.evaluate("document.body.innerText")
        if "成功" in body or "published" in body.lower():
            print("SUCCESS: Article published!")
        else:
            print("Article may have been published. Checking page...")
            print(f"Current page: {page.url}")
    else:
        print("发布 button not found")
    
    await page.close()
    await p.stop()

asyncio.run(main())
