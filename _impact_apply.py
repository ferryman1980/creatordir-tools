import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

TERMS = ["Grammarly", "Semrush", "Shopify", "Bluehost", "HostGator", "Canva", "WPForms", "Elegant Themes"]

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    # Find Impact tab
    pg = None
    for tab in ctx.pages:
        u = tab.url
        if "impact" in u.lower() or "pxa" in u.lower():
            pg = tab
            print(f"Found Impact tab: {u[:80]}")
            break
    
    if not pg:
        pg = await ctx.new_page()
        await pg.goto("https://pxa.impact.com/student/catalog", wait_until="domcontentloaded", timeout=20000)
        await pg.wait_for_timeout(3000)
    
    print(f"Title: {await pg.title()}")
    
    # Look for search box
    search_sel = 'input[placeholder*="search" i], input[placeholder*="Search" i], input[type="search"], input[name*="search"], input[id*="search"]'
    
    for term in TERMS:
        try:
            el = await pg.query_selector(search_sel)
            if el:
                await el.fill("")
                await el.fill(term)
                await pg.wait_for_timeout(3000)
                print(f"  Searched: {term}")
                
                # Click apply on first result
                btns = await pg.query_selector_all("button:has-text('Apply'), a:has-text('Apply'), button:has-text('+'), [aria-label*='Apply']")
                if btns:
                    await btns[0].click()
                    await pg.wait_for_timeout(2000)
                    print(f"    -> Applied!")
                else:
                    print(f"    -> No apply button")
        except Exception as e:
            print(f"  {term}: {str(e)[:40]}")
    
    print("Done")
    await p.stop()

asyncio.run(main())
