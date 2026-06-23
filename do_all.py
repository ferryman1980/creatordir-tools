import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    pages = ctx.pages
    print("=== CURRENT OPEN PAGES ===")
    for i, pg in enumerate(pages):
        print(f"  [{i}] {pg.url[:120]}")
    
    # ===== STEP 1: Check Dev.to page (page[1]) =====
    devto = None
    for pg in pages:
        if "dev.to" in pg.url:
            devto = pg
            break
    if devto:
        await devto.bring_to_front()
        await devto.wait_for_timeout(2000)
        print(f"\n=== DEV.TO ===")
        print(f"URL: {devto.url}")
        text = await devto.evaluate("document.body.innerText")
        print(text[:2000])
    
    # ===== STEP 2: Open ClickBank signup =====
    print("\n=== Opening ClickBank ===")
    cb = await ctx.new_page()
    await cb.goto("https://accounts.clickbank.com/register", wait_until="domcontentloaded", timeout=20000)
    await cb.wait_for_timeout(3000)
    print(f"URL: {cb.url}")
    text = await cb.evaluate("document.body.innerText")
    print(text[:1500])
    await cb.close()
    
    # ===== STEP 3: Try Amazon Associates =====
    print("\n=== Opening Amazon Associates ===")
    amz = await ctx.new_page()
    await amz.goto("https://affiliate-program.amazon.com/", wait_until="domcontentloaded", timeout=20000)
    await amz.wait_for_timeout(3000)
    print(f"URL: {amz.url}")
    text = await amz.evaluate("document.body.innerText")
    print(text[:1500])
    await amz.close()
    
    print("\nDone! Check results above.")
    await p.stop()

asyncio.run(main())
