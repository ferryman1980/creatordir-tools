import asyncio
from playwright.async_api import async_playwright

async def main():
    browser = await async_playwright().start()
    edge = await browser.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]

    # List open pages
    pages = ctx.pages
    print("=== OPEN PAGES ===")
    for i, p in enumerate(pages):
        print(f"  [{i}] {p.url[:120]}")
    
    # Close Awin page
    for p in pages:
        url = p.url
        if "awin" in url:
            await p.close()
            print("Closed Awin page - geo-blocked")
    
    # === 1. PartnerStack ===
    print("\n=== PartnerStack Registration ===")
    ps = await ctx.new_page()
    try:
        await ps.goto("https://app.partnerstack.com/signup", wait_until="domcontentloaded", timeout=20000)
        await ps.wait_for_timeout(3000)
        print(f"URL: {ps.url}")
        text = await ps.evaluate("document.body.innerText")
        print(text[:1500])
        
        # Look for register link
        register_btn = await ps.query_selector('a:has-text("注册"), a:has-text("Sign Up"), button:has-text("注册"), button:has-text("Sign Up")')
        if register_btn:
            await register_btn.click()
            await ps.wait_for_timeout(3000)
            print(f"After click: {ps.url}")
    except Exception as e:
        print(f"Error: {e}")
    
    await ps.close()
    
    # === 2. Try direct publisher signup for Impact ===
    print("\n=== Impact via shareasale ===")
    imp = await ctx.new_page()
    try:
        await imp.goto("https://account.shareasale.com/signup.cfm", wait_until="domcontentloaded", timeout=20000)
        await imp.wait_for_timeout(3000)
        print(f"URL: {imp.url}")
        text = await imp.evaluate("document.body.innerText")
        print(text[:1500])
    except Exception as e:
        print(f"Error: {e}")
    
    await imp.close()
    
    await browser.close()
    print("\nDone!")

asyncio.run(main())
