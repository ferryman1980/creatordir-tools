
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"
PHONE = "18991377556"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        page = browser.contexts[0].pages[0]
        
        # Direct Dev.to registration URL
        await page.goto("https://dev.to/users/sign_up", timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"Direct signup URL: {page.url[:60]}")
        
        # Check for form
        inputs = await page.evaluate("""
            () => Array.from(document.querySelectorAll("input:not([type=hidden])"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({name: el.name, type: el.type, ph: el.placeholder, id: el.id}))
        """)
        print(f"Inputs: {len(inputs)}")
        for f in inputs:
            print(f"  {f['name'] or f['ph']}: type={f['type']}")
        
        # Get all buttons/links
        actions = await page.evaluate("""
            () => Array.from(document.querySelectorAll("button, a, input[type=submit]"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({
                    tag: el.tagName,
                    text: (el.innerText || el.textContent || el.value || "").trim().substring(0, 30),
                    type: el.type || "",
                    href: el.href || ""
                }))
                .filter(el => el.text.length > 0 || el.href.length > 0)
        """)
        print(f"\nActions: {len(actions)}")
        for a in actions[:10]:
            print(f"  [{a['tag']}] {a['text'][:25]} {a['type']}")
        
        await browser.close()

asyncio.run(main())
