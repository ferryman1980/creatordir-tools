
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
        page = browser.contexts[0].pages[0]
        await page.goto("https://www.grammarly.com/affiliates", timeout=20000)
        await page.wait_for_timeout(2000)
        
        # Get all links
        links = await page.evaluate("""
            () => Array.from(document.querySelectorAll("a"))
                .filter(a => a.innerText.toLowerCase().includes("affiliate") || a.href.includes("affiliate"))
                .map(a => ({text: a.innerText.trim().substring(0, 30), href: a.href.substring(0, 80)}))
        """)
        for l in links:
            print(f"{l['text']:30s} -> {l['href']}")
        
        # Also check the "Become an affiliate" button specifically
        btn_link = await page.evaluate("""
            () => {
                const btns = document.querySelectorAll("a");
                for (let b of btns) {
                    if (b.innerText.toLowerCase().includes("become an affiliate")) {
                        return b.href;
                    }
                }
                return "NOT FOUND";
            }
        """)
        print(f"\nBecome an affiliate link: {btn_link}")
        
        await browser.close()

asyncio.run(main())
