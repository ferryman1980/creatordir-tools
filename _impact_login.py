import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    # Find PXA tab, navigate to marketplace
    target = None
    for tab in ctx.pages:
        if "pxa" in tab.url:
            target = tab
            break
    
    if not target:
        target = await ctx.new_page()
    
    await target.goto("https://app.impact.com/login.user", wait_until="domcontentloaded", timeout=20000)
    await target.wait_for_timeout(3000)
    print(f"Login page: {await target.title()}")
    
    # Fill forms using evaluate
    await target.evaluate("""
        () => {
            const inputs = document.querySelectorAll('input');
            inputs.forEach(i => {
                const t = i.type;
                const n = i.name;
                if (t === 'email' || n === 'username' || n === 'email' || (i.placeholder || '').toLowerCase().includes('email')) {
                    i.value = '346010735@qq.com';
                    i.dispatchEvent(new Event('input', {bubbles: true}));
                    i.dispatchEvent(new Event('change', {bubbles: true}));
                }
                if (t === 'password') {
                    i.value = 'Ckyhy388$';
                    i.dispatchEvent(new Event('input', {bubbles: true}));
                    i.dispatchEvent(new Event('change', {bubbles: true}));
                }
            });
        }
    """)
    print("Form filled via evaluate")
    await target.wait_for_timeout(1000)
    
    # Click login button
    await target.evaluate("""
        () => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                if (b.textContent.toLowerCase().includes('log') || 
                    b.textContent.includes('登录') ||
                    b.textContent.toLowerCase().includes('sign') ||
                    b.type === 'submit') {
                    b.click();
                    return;
                }
            }
        }
    """)
    print("Login clicked")
    await target.wait_for_timeout(5000)
    print(f"After login URL: {target.url[:80]}")
    
    # Navigate to marketplace catalog
    await target.goto("https://app.impact.com/secure/marketplace/advertiser-catalog", wait_until="domcontentloaded", timeout=20000)
    await target.wait_for_timeout(3000)
    print(f"Catalog URL: {target.url[:80]}")
    print(f"Catalog Title: {await target.title()}")
    
    page_text = await target.evaluate("document.body.innerText")
    print(f"Page content: {page_text[:400]}")
    
    # If we got to catalog, search for programs
    if "marketplace" in target.url.lower() or "catalog" in target.url.lower():
        terms = ["Grammarly", "Semrush", "Shopify", "Canva", "Bluehost"]
        for term in terms:
            # Find search
            await target.evaluate(f"document.querySelector('input')?.focus()")
            await target.fill('input[placeholder*="search" i], input[placeholder*="Search" i], input[type="search"]', term)
            await target.wait_for_timeout(2000)
            
            # Click Apply
            btns = await target.query_selector_all('button:has-text("Apply"), a:has-text("Apply")')
            if btns:
                for btn in btns:
                    try:
                        if await btn.is_visible():
                            await btn.click()
                            print(f"  Applied to {term}!")
                            await target.wait_for_timeout(2000)
                            break
                    except:
                        pass
            else:
                print(f"  No apply button for {term}")
    
    print("\nDone")
    await p.stop()

asyncio.run(main())
