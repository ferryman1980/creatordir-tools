
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        page = browser.contexts[0].pages[0]
        
        # Try Dev.to signup
        await page.goto("https://dev.to/enter", timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"Dev.to: {page.url[:60]}")
        print(f"Inputs: {await page.evaluate('document.querySelectorAll(\"input\").length')}")
        
        text = (await page.evaluate("document.body.innerText") or "")[:300]
        print(f"Text: {text[:200]}")
        
        # Check for email signup option
        buttons = await page.evaluate("""
            () => Array.from(document.querySelectorAll("button, a"))
                .filter(el => el.offsetParent !== null)
                .map(el => (el.innerText || el.textContent || "").trim().substring(0, 25))
                .filter(t => t.length > 0 && (t.toLowerCase().includes("email") || t.toLowerCase().includes("sign") || t.toLowerCase().includes("github")))
        """)
        print(f"Signup options: {buttons[:5]}")
        
        await browser.close()

asyncio.run(main())
