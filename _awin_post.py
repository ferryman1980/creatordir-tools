import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

EMAIL = "346010735@qq.com"
PWD = "Ckyhy388$"

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    # Find Awin tab
    pg = None
    for tab in ctx.pages:
        if "awin" in tab.url.lower() or "shareasale" in tab.url.lower():
            pg = tab
            break
    
    if not pg:
        pg = await ctx.new_page()
        await pg.goto("https://www.awin.com/gb/affiliates/register", wait_until="domcontentloaded", timeout=15000)
    
    await pg.bring_to_front()
    await pg.wait_for_timeout(2000)
    print(f"Awin: {await pg.title()}")
    print(f"Awin URL: {pg.url()[:80]}")
    
    # Check if registration form is available
    page_text = await pg.evaluate("document.body.innerText")
    print(f"Content: {page_text[:300]}")
    
    # Look for form fields
    inputs = await pg.evaluate("""
        () => Array.from(document.querySelectorAll("input")).map(i => ({
            id: i.id, type: i.type, name: i.name, ph: i.placeholder, cls: i.className.slice(0,20)
        }))
    """)
    print(f"Found {len(inputs)} inputs")
    for inp in inputs[:10]:
        print(f"  id={inp['id']} type={inp['type']} name={inp['name']} ph={inp['ph']}")
    
    await p.stop()

asyncio.run(main())
