import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    page = ctx.pages[0]
    
    await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(3000)
    
    await page.evaluate("document.getElementById('article-form-title').value = ''")
    await page.fill("#article-form-title", "10 AI Tools That Saved Me 20 Hours Per Week as a Solo Developer")
    await page.wait_for_timeout(300)
    
    content = """As a solo developer, time is my most valuable asset. Here are 10 AI tools that genuinely save me hours every week.
    
1. ChatGPT for Code - Cuts coding time by ~40%. Great for boilerplate and debugging.
2. Claude for Writing - Handles blog posts and docs with 100K token context.
3. Canva AI for Design - Graphics and logos in minutes.
4. GitHub Copilot - Autocomplete your code as you type.
5. ElevenLabs for Voice - Text-to-speech for tutorials.
6. Descript for Video - Edit video by editing text.
7. CapCut - Free AI video editor with auto captions.
8. Notion AI - Project management with AI writing.
9. Runway - Generate video clips from text.
10. Perplexity - AI search with cited answers.

I curate all these at CreatorDir Tools (https://creatordir-tools.vercel.app) with pricing comparisons.

Which AI tool saves you the most time? Share below!"""
    
    await page.evaluate("document.getElementById('article_body_markdown').value = ''")
    await page.fill("#article_body_markdown", content)
    await page.wait_for_timeout(500)
    
    pub = await page.query_selector("button:has-text('\u53d1\u5e03')")
    if pub:
        await pub.click()
        await page.wait_for_timeout(5000)
        print("Published: " + page.url)
    else:
        print("No button")
    
    await page.close()
    await p.stop()

asyncio.run(main())
