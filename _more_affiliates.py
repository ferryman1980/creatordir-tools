
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://creatordir-tools.vercel.app"
EMAIL = "346010735@qq.com"

async def check_page(page, name, url):
    print(f"\n=== {name} ===")
    print(f"URL: {url}")
    try:
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"Final: {page.url[:70]}")
        text = (await page.evaluate("document.body.innerText") or "")[:200]
        print(f"Text: {text}")
        inputs = await page.evaluate("document.querySelectorAll('input').length")
        print(f"Inputs: {inputs}")
    except Exception as e:
        print(f"Error: {str(e)[:40]}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
        page = browser.contexts[0].pages[0]
        
        # Try different affiliate networks
        sites = [
            ("ShareASale", "https://account.shareasale.com/signup.cfm"),
            ("CJ Affiliate", "https://www.cj.com/publisher-signup"),
            ("Rakuten", "https://rakutenadvertising.com/"),
            ("PartnerStack Alt", "https://partnerships.partnerstack.com/partners/signup"),
        ]
        
        for name, url in sites:
            await check_page(page, name, url)
            await page.wait_for_timeout(2000)
        
        await browser.close()

asyncio.run(main())
