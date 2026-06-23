
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
        
        print("Awin page...")
        await page.wait_for_timeout(2000)
        print(f"URL: {page.url[:60]}")
        
        # Click "开始" or "Get Started" button
        try:
            start_btn = await page.query_selector("a:has-text('开始'), button:has-text('开始'), a:has-text('Get Started'), a:has-text('Sign Up')")
            if start_btn:
                print("Clicking 开始...")
                await start_btn.click()
                await page.wait_for_timeout(3000)
                print(f"New URL: {page.url[:60]}")
        except Exception as e:
            print(f"Click error: {str(e)[:40]}")
        
        # Now look for form
        await page.evaluate("window.scrollTo(0, 300)")
        await page.wait_for_timeout(1000)
        
        # Get all form elements
        forms = await page.evaluate("""
            () => Array.from(document.querySelectorAll("input, textarea, select, button"))
                .filter(el => el.offsetParent !== null)
                .map(el => ({
                    tag: el.tagName,
                    type: el.type || "",
                    name: el.name || "", 
                    id: el.id || "",
                    ph: el.placeholder || "",
                    text: (el.innerText || el.textContent || "").trim().substring(0, 20)
                }))
        """)
        
        print(f"Visible elements: {len(forms)}")
        for f in forms[:25]:
            txt = f["text"] or f["ph"] or f["name"]
            print(f"  [{f['tag']}] {f['type']:8s} {txt[:20]}")
        
        # Fill what we can
        for f in forms:
            combined = (f["name"] + " " + f["id"] + " " + f["ph"] + " " + f["text"]).lower()
            val = None
            if "email" in combined: val = EMAIL
            elif "password" in combined: val = PASS
            elif "first" in combined or "fname" in combined: val = "Creator"
            elif "last" in combined or "lname" in combined: val = "AI"
            elif "company" in combined or "business" in combined: val = "CreatorAI Tools"
            elif "website" in combined or "url" in combined: val = "https://creatordir-tools.vercel.app"
            
            if val and f["tag"] == "INPUT":
                try:
                    sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                    el = await page.query_selector(sel)
                    if el:
                        await el.fill(val)
                        print(f"  FILLED: {f['name'][:15]} = {val[:20]}")
                except: pass
        
        # Take screenshot
        await page.screenshot(path="D:/项目/工作区/工作5/awin_form.png")
        print("\nScreenshot saved to awin_form.png")
        
        await browser.close()

asyncio.run(main())
