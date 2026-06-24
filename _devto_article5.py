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
    await page.fill("#article-form-title", "I Compared 50+ Free AI Tools - Here Are the Ones Actually Worth Using")
    await page.wait_for_timeout(300)
    
    content = """After testing 50+ free AI tools, I found that most are not worth your time. Here are the ones that actually deliver value without costing a cent.

**Best Free AI Writing Tools**
- ChatGPT (free tier) - Still the best all-around. Great for drafting, editing, and brainstorming.
- Claude (free tier) - Better for long-form content and analysis.
- Google Gemini - Integrated with Google Workspace. Great for research.

**Best Free AI Design Tools**
- Canva (free) - The most generous free tier. Thousands of templates with AI features.
- Leonardo AI - 150 free credits daily for image generation.
- Playground AI - Free daily generations with good quality.

**Best Free AI Video Tools**
- CapCut - Completely free video editor with AI auto-captions, background removal, and text-to-speech.
- Runway (free tier) - 12 free video generations to start.

**Best Free AI Audio Tools**
- ElevenLabs (free) - 10,000 characters per month of text-to-speech.
- Suno (free) - 10 free song generations daily.
- TTSMaker - Completely free text-to-speech with natural voices.

**Best Free AI Development Tools**
- GitHub Copilot (free for students/OSS) - AI pair programming.
- Tabnine (free) - AI code completion.
- Google Colab - Free GPU for machine learning.

**Full List**
I maintain a comprehensive directory of 50+ free AI tools at CreatorDir Tools (https://creatordir-tools.vercel.app/free-ai-tools.html) with detailed reviews of each.

What free AI tools do you rely on? Drop your favorites in the comments!"""
    
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
