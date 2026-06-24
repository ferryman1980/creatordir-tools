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
    
    # Fill title
    await page.evaluate("document.getElementById('article-form-title').value = ''")
    await page.fill("#article-form-title", title)
    await page.wait_for_timeout(300)
    
    # Fill body
    content = """Building side projects as a solo developer used to mean doing everything yourself. With AI tools in 2026, one person can accomplish what used to require a team.

**The Solo Developer AI Stack**

**1. AI Code Generation**

Tools like ChatGPT and Claude have transformed how solo developers write code. Instead of spending hours on boilerplate, you can generate entire CRUD applications from natural language descriptions, get debugging help in real-time, and write tests in seconds.

**2. AI Design Assistant**

No design skills? No problem. Use Canva AI to create professional UI mockups, generate logos with Midjourney, create product screenshots automatically, and design landing pages with AI builders.

**3. AI Content Creation**

Marketing your side project is often harder than building it. Write blog posts with AI writing tools, generate social media content in bulk, create product descriptions, and produce demo videos with AI video tools.

**4. AI for Customer Support**

Set up AI chatbots for common questions, auto-respond to support emails, generate FAQ sections automatically, and monitor user feedback with AI sentiment analysis.

**5. AI Marketing Automation**

Use SEO optimization tools, email marketing automation, social media scheduling, and A/B testing with AI recommendations.

**Real Example: Building an AI Tools Directory**

I built CreatorDir Tools (https://creatordir-tools.vercel.app) as a solo developer using exactly this stack. It now has 200+ curated AI tool reviews.

**Tools I Recommend for Solo Developers**

1. Hostinger (https://www.hostinger.com?REFERRALCODE=ECA346010F8J) - Affordable hosting
2. ChatGPT/Claude - Code generation and debugging
3. Canva - Design assets
4. Vercel - Free hosting for web apps
5. Supabase - Free backend/database

**Start Small, Ship Fast**

The key is to start with free tools and upgrade only when your project generates revenue.

What side project are you building? Drop it in the comments!"""
    
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
    
    # Click publish
    pub_btn = await page.query_selector("button:has-text('\u53d1\u5e03')")
    if pub_btn:
        await pub_btn.click()
        await page.wait_for_timeout(5000)
        print("Article 2 URL: " + page.url)
    
    await page.close()
    await p.stop()

asyncio.run(main())
