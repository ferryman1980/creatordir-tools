import asyncio, json, os, re
from playwright.async_api import async_playwright

SITE = "https://creatordir-tools.vercel.app"
NAME = "CreatorAI Tools"
DESC = "Curated directory of 160+ AI tools for content creators with honest reviews and comparisons."

async def submit_to_directory(page, url, name_field, url_field, desc_field):
    try:
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # Try to fill common form fields
        inputs = await page.query_selector_all("input[type=\"text\"], input[type=\"url\"], textarea")
        filled = 0
        for inp in inputs:
            placeholder = (await inp.get_attribute("placeholder") or "").lower()
            name_attr = (await inp.get_attribute("name") or "").lower()
            id_attr = (await inp.get_attribute("id") or "").lower()
            
            if any(w in placeholder + name_attr + id_attr for w in ["name", "title", "tool"]):
                await inp.fill(NAME)
                filled += 1
            elif any(w in placeholder + name_attr + id_attr for w in ["url", "website", "link", "site"]):
                await inp.fill(SITE)
                filled += 1
            elif any(w in placeholder + name_attr + id_attr for w in ["desc", "about", "detail"]):
                await inp.fill(DESC)
                filled += 1
        
        if filled > 0:
            print(f"  Filled {filled} fields at {url}")
        
        # Try to click submit button
        buttons = await page.query_selector_all("button[type=\"submit\"], input[type=\"submit\"], button:has-text(\"Submit\"), button:has-text(\"Add\")")
        if buttons:
            await buttons[0].click()
            await page.wait_for_timeout(3000)
            print(f"  Submitted! Current URL: {page.url}")
            return True
        else:
            print(f"  No submit button found at {url}")
            return False
    except Exception as e:
        print(f"  Error: {str(e)[:60]}")
        return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0]
        
        directories = [
            ("https://www.aiwizard.ai/submit", "name", "url", "description"),
            ("https://aitoolguru.com/submit-tool", "name", "url", "description"),
            ("https://aivalley.ai/submit-tool", "tool_name", "tool_url", "tool_description"),
            ("https://www.aixploria.com/en/submit-tool/", "name", "url", "description"),
            ("https://www.toolpilot.ai/submit-tool", "name", "url", "description"),
            ("https://saasguru.co/submit-tool/", "name", "url", "description"),
            ("https://www.toolify.ai/submit-tool", "name", "url", "description"),
            ("https://aitoolsdirectory.com/submit/", "name", "url", "description"),
            ("https://www.aitoolnet.com/submit", "name", "url", "description"),
            ("https://aitoolhunt.com/submit-tool", "name", "url", "description"),
        ]
        
        for url, nf, uf, df in directories:
            page = await ctx.new_page()
            print(f"\nSubmitting to: {url}")
            try:
                ok = await submit_to_directory(page, url, nf, uf, df)
                if ok:
                    print(f"  [OK] {url}")
                else:
                    print(f"  [--] {url}")
            except Exception as e:
                print(f"  [FAIL] {str(e)[:60]}")
            await page.close()
        
        await browser.close()
        print("\nDone submitting to directories!")

asyncio.run(main())
