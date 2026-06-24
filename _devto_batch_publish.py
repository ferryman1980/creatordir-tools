import asyncio
from playwright.async_api import async_playwright

async def publish_article(page, title, content, tags):
    await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(2000)
    
    # Clear and fill title
    await page.evaluate("document.getElementById('article-form-title').value = ''")
    await page.fill("#article-form-title", title)
    await page.wait_for_timeout(300)
    
    # Clear and fill body
    await page.evaluate("document.getElementById('article_body_markdown').value = ''")
    await page.fill("#article_body_markdown", content)
    await page.wait_for_timeout(500)
    
    # Add tags - clear existing first
    tag_input = await page.query_selector("#tag-input")
    if tag_input:
        await tag_input.click()
        await page.wait_for_timeout(200)
        # Clear any existing tags
        await page.evaluate("document.querySelectorAll('.tag-remove-button').forEach(b => b.click())")
        await page.wait_for_timeout(300)
        
        for tag in tags:
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
        return page.url
    return "Publish button not found"

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = await edge.contexts[0].new_page()
    
    # Article 1: Free AI Tools
    print("=== Article 1: Free AI Tools ===")
    url1 = await publish_article(page,
        "50+ Completely Free AI Tools You Can Use Right Now (2026 Guide)",
        """The AI revolution is here, but not all tools require a subscription. I have compiled 50+ completely free AI tools that deliver real value.

**Why Free AI Tools Matter**

Many people think you need to spend hundreds of dollars monthly to leverage AI. The truth is, there are excellent free options for almost every use case.

**Free AI Writing Tools**

1. **ChatGPT (Free tier)** - https://chat.openai.com - Still one of the best for brainstorming, drafting, and editing
2. **Claude (Free tier)** - https://claude.ai - Excellent for long-form content and analysis
3. **Google Gemini** - Deep integration with Google Workspace
4. **Perplexity AI** - AI-powered search with citations
5. **Hugging Face Chat** - Open-source models, completely free

**Free AI Image Generators**

1. **DALL-E 3 (Bing)** - https://www.bing.com/create - 15 free generations per day
2. **Stable Diffusion Web** - Various free web interfaces
3. **Leonardo AI** - 150 free credits daily
4. **Ideogram** - Free tier with watermark
5. **Playground AI** - Free daily generations

**Free AI Video Tools**

1. **CapCut** - https://capcut.com - Free video editor with AI features
2. **Runway (Free)** - 12 free video generations
3. **Canva Video** - Free tier with AI video features
4. **Descript (Free)** - Limited but capable free tier

**Free AI Audio Tools**

1. **ElevenLabs (Free)** - https://try.elevenlabs.io/ebksqtv6a5m6 - 10,000 characters monthly
2. **Suno (Free)** - 10 free song generations daily
3. **TTSMaker** - Completely free text-to-speech
4. **Mubert** - Free AI music generation

**Free AI Development Tools**

1. **GitHub Copilot (Free)** - Free for students and open source
2. **Tabnine (Free)** - AI code completion
3. **Replit AI** - Free AI-assisted coding
4. **Google Colab** - Free GPU for ML projects

**Free AI Marketing Tools**

1. **Canva (Free)** - Design with AI features
2. **Mailchimp (Free)** - Up to 500 contacts
3. **Buffer (Free)** - Schedule up to 3 social accounts
4. **Google Analytics** - Completely free

**The Complete List**

For the full curated list of free AI tools with detailed reviews, visit:
https://creatordir-tools.vercel.app/free-ai-tools.html

Which free AI tool do you use most? Share in the comments!""",
        ["ai", "productivity", "free", "beginners"]
    )
    print(f"Article 1 URL: {url1}")
    
    # Article 2: AI for Side Projects
    print("\n=== Article 2: AI for Side Projects ===")
    url2 = await publish_article(page,
        "How Solo Developers Can Use AI to Ship Side Projects 10x Faster",
        """Building side projects as a solo developer used to mean doing everything yourself. With AI tools in 2026, one person can accomplish what used to require a team.

**The Solo Developer AI Stack**

**1. AI Code Generation**

Tools like ChatGPT and Claude have transformed how solo developers write code. Instead of spending hours on boilerplate, you can:

- Generate entire CRUD applications from natural language descriptions
- Get debugging help in real-time
- Refactor code automatically
- Write tests in seconds instead of hours

**2. AI Design Assistant**

No design skills? No problem:

- Use Canva AI to create professional UI mockups
- Generate logos and brand assets with Midjourney
- Create product screenshots automatically
- Design landing pages with AI landing page builders

**3. AI Content Creation**

Marketing your side project is often harder than building it:

- Write blog posts and documentation with AI writing tools
- Generate social media content in bulk
- Create product descriptions and landing page copy
- Produce demo videos with AI video tools

**4. AI for Customer Support**

- Set up AI chatbots for common questions
- Auto-respond to support emails
- Generate FAQ sections automatically
- Monitor user feedback with AI sentiment analysis

**5. AI Marketing Automation**

- SEO optimization with tools like Semrush
- Email marketing automation
- Social media scheduling
- A/B testing with AI recommendations

**Real Example: Building an AI Tools Directory**

I built [CreatorDir Tools](https://creatordir-tools.vercel.app) as a solo developer using exactly this stack:

- **Frontend**: Generated with AI assistance in hours
- **Content**: 200+ AI tool reviews written with AI help
- **Design**: Canva AI for all graphics
- **Marketing**: AI-generated social posts and SEO content
- **Deployment**: Automated with Vercel

**Tools I Recommend for Solo Developers**

1. [Hostinger](https://www.hostinger.com?REFERRALCODE=ECA346010F8J) - Affordable hosting to test ideas
2. ChatGPT/Claude - Code generation and debugging
3. Canva - Design assets
4. Vercel - Free hosting for web apps
5. Supabase - Free backend/database

**Start Small, Ship Fast**

The key is to start with free tools and upgrade only when your project generates revenue. Most AI tools have generous free tiers.

What side project are you building? Drop it in the comments!""",
        ["webdev", "productivity", "ai", "beginners"]
    )
    print(f"Article 2 URL: {url2}")
    
    await page.close()
    await p.stop()

asyncio.run(main())
