import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

EMAIL = "346010735@qq.com"
PWD = "Ckyhy388$"
SITE = "creatordir-tools.vercel.app"

async def main():
    p = await async_playwright().start()
    b = await p.chromium.launch(channel="msedge", headless=False)
    ctx = await b.new_context()
    pg = await ctx.new_page()
    
    # Login to Impact
    print("Opening Impact login...")
    await pg.goto("https://app.impact.com/auth/login", wait_until="domcontentloaded", timeout=20000)
    await pg.wait_for_timeout(2000)
    print(f"Page: {await pg.title()}")
    
    # Fill login
    for s in ['input[type="email"]', 'input[name*="email"]', 'input[id*="email"]']:
        el = await pg.query_selector(s)
        if el:
            await el.fill(EMAIL)
            print("Email filled")
            break
    
    for s in ['input[type="password"]']:
        el = await pg.query_selector(s)
        if el:
            await el.fill(PWD)
            print("Password filled")
            break
    
    btn = await pg.query_selector('button[type="submit"]')
    if btn:
        await btn.click()
        await pg.wait_for_timeout(5000)
        print(f"After login: {pg.url[:80]}")
    
    # Check if we got to dashboard
    if "dashboard" in pg.url.lower() or "campaign" in pg.url.lower():
        print("LOGGED IN! Setting up account...")
        
        # Add website
        await pg.goto("https://app.impact.com/secure/account/profile/websites", wait_until="domcontentloaded", timeout=15000)
        await pg.wait_for_timeout(3000)
        print(f"Websites page: {await pg.title()}")
        
        # Find and fill website form
        for s in ['input[name*="url"]', 'input[placeholder*="site"]', 'input[placeholder*="URL"]']:
            el = await pg.query_selector(s)
            if el:
                await el.fill(f"https://{SITE}")
                print("Website URL filled")
                break
    
    print("Done")
    await p.stop()

asyncio.run(main())
