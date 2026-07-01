import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

SEARCH_TERMS = ["Grammarly", "Semrush", "Shopify", "Canva", "Bluehost"]

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    tabs = ctx.pages
    print(f"Edge tabs: {len(tabs)}")
    for i, t in enumerate(tabs):
        print(f"  Tab {i}: {t.url[:80]}")
    
    # Use the Impact tab (last one we opened) or create new
    pg = None
    for t in tabs:
        if "impact" in t.url.lower() or "pxa" in t.url.lower():
            pg = t
            pg.bring_to_front()
            break
    
    if not pg:
        pg = await ctx.new_page()
        await pg.goto("https://pxa.impact.com/student/catalog", wait_until="domcontentloaded", timeout=20000)
    
    await pg.wait_for_timeout(3000)
    print(f"\nPage title: {await pg.title()}")
    
    # Try to find search input
    search_selectors = [
        'input[placeholder*="search" i]',
        'input[placeholder*="Search" i]', 
        'input[type="search"]',
        'input[name*="search" i]',
        'input[id*="search" i]',
        'input[class*="search" i]',
    ]
    
    search_input = None
    for sel in search_selectors:
        el = await pg.query_selector(sel)
        if el:
            search_input = el
            print(f"Found search: {sel}")
            break
    
    if search_input:
        for term in SEARCH_TERMS:
            print(f"\nSearching: {term}...")
            await search_input.click()
            await search_input.fill("")
            await pg.wait_for_timeout(500)
            await search_input.fill(term)
            await pg.wait_for_timeout(3000)
            
            # Look for Apply buttons
            apply_btns = await pg.query_selector_all(
                'button:has-text("Apply"), '
                'a:has-text("Apply"), '
                'button:has-text("apply"), '
                '[class*="apply"] button, '
                '[class*="Apply"] button, '
                'button[class*="primary"], '
                'button[class*="Primary"]'
            )
            
            if apply_btns:
                for btn in apply_btns:
                    try:
                        txt = await btn.text_content()
                        print(f"  Found button: {txt.strip()[:30]}")
                        await btn.click()
                        await pg.wait_for_timeout(2000)
                        print(f"  Clicked Apply for {term}!")
                        break
                    except:
                        pass
            else:
                print(f"  No Apply button found for {term}")
            
            # Also try to find cards/items and click
            cards = await pg.query_selector_all('[class*="card"], [class*="Card"], [class*="item"], [class*="Item"], [class*="result"], [class*="Result"], li, tr')
            print(f"  Found {len(cards)} result items")
    else:
        print("No search input found - dumping page structure...")
        page_text = await pg.evaluate("document.body.innerText")
        print(page_text[:500] if page_text else "Empty body")
    
    print("\nDone!")
    await p.stop()

asyncio.run(main())
