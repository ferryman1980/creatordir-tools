import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=30000)
        page = browser.contexts[0].pages[1]
        await page.goto("https://www.awin.com/gb/publishers/sign-up", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        await page.evaluate("window.UC_UI && UC_UI.acceptAllConsents()")
        await page.wait_for_timeout(2000)
        result = await page.evaluate("Array.from(document.querySelectorAll('input:not([type=hidden]), select, textarea')).filter(i => i.offsetParent).map(i => ({n:i.name||i.id||'',t:i.type||'',p:(i.placeholder||'').substring(0,20)}))")
        print(f"Visible inputs: {len(result)}")
        for inp in result:
            print("  name=" + inp["n"] + " type=" + inp["t"] + " place=" + inp["p"])
        await browser.close()

asyncio.run(main())
