import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = await edge.contexts[0].pages()[0]
    
    await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(3000)
    
    # Fill new article
    await page.evaluate("document.getElementById('article-form-title').value = ''")
    await page.fill("#article-form-title", "10 AI Tools That Saved Me 20 Hours Per Week as a Solo Developer")
    await page.wait_for_timeout(300)
    
    content = """As a solo developer, time is my most valuable asset. Here are 10 AI tools that genuinely save me hours every week.

1. **ChatGPT for Code** - Cuts coding time by about 40%. Great for boilerplate and debugging.
2. **Claude for Writing** - Handles blog posts and documentation with 100K token context.
3. **Canva AI for Design** - Social media graphics and logos in minutes.
4. **GitHub Copilot** - Autocomplete that predicts your next lines of code.
5. **ElevenLabs for Voice** - Text-to-speech for tutorial voiceovers. Saves hours of recording.
6. **Descript for Video** - Edit video by editing text. Game changer for content creators.
7. **CapCut** - Free video editor with AI captions and background removal.
8. **Notion AI** - Project management with AI writing assistance.
9. **Runway** - Generate short video clips from text descriptions.
10. **Perplexity** - AI-powered search with cited answers for research.

I curate all these tools and more at **CreatorDir Tools** (https://creatordir-tools.vercel.app) with pricing comparisons and exclusive deals.

Which AI tool saves you the most time? Share in the comments!"""
    
    await page.evaluate("document.getElementById('article_body_markdown').value = ''")
    await page.fill("#article_body_markdown", content)
    await page.wait_for_timeout(500)
    
    pub = await page.query_selector("button:has-text('\u53d1\u5e03')")
    if pub:
        await pub.click()
        await page.wait_for_timeout(5000)
        print(f"Published: {page.url}")
    else:
        print("No publish button")
    
    await page.close()
    await p.stop()

asyncio.run(main())
