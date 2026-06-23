import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    pages = ctx.pages
    print(f"Open pages: {len(pages)}")
    
    # ===== 1. Amazon Associates Registration =====
    print("\n========== AMAZON ASSOCIATES ==========")
    
    # Check if there's already an Amazon page
    amz_page = None
    for pg in pages:
        if "amazon.com" in pg.url and "affiliate" in pg.url:
            amz_page = pg
            break
    
    if not amz_page:
        amz_page = await ctx.new_page()
        await amz_page.goto("https://affiliate-program.amazon.com/", wait_until="domcontentloaded", timeout=20000)
        await amz_page.wait_for_timeout(2000)
    
    await amz_page.bring_to_front()
    print(f"URL: {amz_page.url}")
    
    # Click the Sign Up button
    try:
        signup_btn = await amz_page.query_selector('a:has-text("注册"), a:has-text("Sign up"), a[href*="signup"], a[href*="register"]')
        if not signup_btn:
            signup_btn = await amz_page.query_selector('input[value*="Sign"], button:has-text("注册"), button:has-text("Sign")')
        if signup_btn:
            await signup_btn.click()
            await amz_page.wait_for_timeout(5000)
            print(f"Clicked signup. URL: {amz_page.url}")
            text = await amz_page.evaluate("document.body.innerText")
            print(text[:2000])
        else:
            print("No signup button found, trying to get page HTML")
            html = await amz_page.content()
            # Look for signup links
            links = await amz_page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a')).map(a => ({href: a.href, text: a.textContent.trim()})).filter(x => x.text.includes('Sign') || x.text.includes('sign') || x.href.includes('sign') || x.href.includes('regist'))
            }''')
            print(f"Signup links found: {links}")
    except Exception as e:
        print(f"Error clicking signup: {e}")
    
    await amz_page.wait_for_timeout(3000)
    
    # ===== 2. Dev.to - Check current state =====
    print("\n========== DEV.TO ==========")
    devto = None
    for pg in ctx.pages:
        if "dev.to" in pg.url:
            devto = pg
            break
    
    if devto:
        await devto.bring_to_front()
        await devto.wait_for_timeout(2000)
        print(f"Dev.to URL: {devto.url}")
        
        # Read the article content
        article_path = "D:\\项目\\工作区\\工作5\\promo_articles\\best-free-ai-tools-small-business-2026.md"
        with open(article_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract title
        lines = content.split("\n")
        title = lines[0].replace("# ", "").strip()
        
        print(f"Article title: {title}")
        print(f"Content length: {len(content)} chars")
        
        # The form is empty. Let me check what fields are available
        # Try to fill in the form
        try:
            # Check for title field
            title_input = await devto.query_selector('input[placeholder*="title"], input[placeholder*="Title"], textarea[placeholder*="title"], textarea[placeholder*="Title"]')
            if title_input:
                await title_input.click()
                await title_input.fill(title)
                print(f"Filled title: {title}")
            else:
                print("Title input not found")
                # Check what's on the page
                inputs = await devto.evaluate('''() => {
                    const els = document.querySelectorAll('input, textarea');
                    return Array.from(els).map(e => ({tag: e.tagName, type: e.type, placeholder: e.placeholder, id: e.id, name: e.name, className: e.className.substring(0,50)}));
                }''')
                print(f"Form fields: {inputs}")
        except Exception as e:
            print(f"Error filling Dev.to form: {e}")
    else:
        print("No Dev.to page found")
    
    print("\nDone!")
    await p.stop()

asyncio.run(main())
