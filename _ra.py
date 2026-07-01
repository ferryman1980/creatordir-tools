import asyncio
from playwright.async_api import async_playwright

EMAIL = "346010735@qq.com"
PWD = "Ckyhy388"
SITE = "https://creatordir-tools.vercel.app"

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    
    targets = [
        ("Namecheap", "https://www.namecheap.com/affiliates/"),
        ("Bluehost", "https://bluehost.com/affiliates"),
        ("HostGator", "https://www.hostgator.com/affiliates"),
        ("ConvertKit", "https://kit.com/affiliate"),
        ("ElegantThemes", "https://www.elegantthemes.com/affiliates/"),
        ("WPForms", "https://wpforms.com/affiliates/"),
        ("Shopify", "https://www.shopify.com/affiliates"),
        ("Grammarly", "https://www.grammarly.com/affiliates"),
    ]
    
    for name, url in targets:
        try:
            page = await edge.contexts[0].new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(2000)
            print(f"[{name}] {await page.title()}")
            await page.close()
        except Exception as e:
            print(f"[{name}] ERR: {str(e)[:60]}")
    
    await p.stop()
    print("DONE - All 8 affiliate pages opened")

asyncio.run(main())
