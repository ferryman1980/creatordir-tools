import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    br = await p.chromium.launch(channel="msedge", headless=False)
    pg = await br.new_page()
    
    await pg.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
    await pg.wait_for_timeout(3000)
    print(f"URL: {pg.url}")
    
    title_el = await pg.query_selector("#article-form-title")
    body_el = await pg.query_selector("#article_body_markdown")
    print(f"Title: {bool(title_el)}, Body: {bool(body_el)}")
    
    if title_el and body_el:
        await pg.fill("#article-form-title", "10 AI Tools That Saved Me 20 Hours Per Week as a Solo Developer")
        await pg.wait_for_timeout(400)
        
        content = """As a solo developer, time is my most valuable asset. Here are 10 AI tools that genuinely save me hours every week.

1. ChatGPT for Code - Cuts coding time by ~40%. Great for boilerplate and debugging.
2. Claude for Writing - Handles blog posts and documentation with 100K token context.
3. Canva AI for Design - Social media graphics and logos in minutes.
4. GitHub Copilot - Autocomplete that predicts what you want to write.
5. ElevenLabs for Voice - Text-to-speech for tutorial voiceovers.
6. Descript for Video - Edit video by editing text.
7. CapCut - Free video editor with AI captions and background removal.
8. Notion AI - Project management with AI assistance.
9. Runway - Generate short video clips from text.
10. Perplexity - AI search with cited answers for research.

I curate all these tools and more at CreatorDir Tools (https://creatordir-tools.vercel.app) with pricing comparisons.

Which AI tool saves you the most time? Share in the comments!"""
        
        await pg.fill("#article_body_markdown", content)
        await pg.wait_for_timeout(500)
        
        pub = await pg.query_selector("button:has-text('发布')")
        if pub:
            await pub.click()
            await pg.wait_for_timeout(5000)
            print(f"Published: {pg.url}")
        else:
            print("No publish button")
    else:
        print("Editor not accessible")
        await pg.screenshot(path="D:\\项目\\工作区\\工作5\\devto_debug.png")
    
    await pg.close()
    await br.close()
    await p.stop()

asyncio.run(main())
