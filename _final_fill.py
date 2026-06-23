
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
        pages = browser.contexts[0].pages
        
        # Find ShareASale page
        sas_page = None
        for pg in pages:
            url = pg.url
            if "shareasale" in url.lower() or "signup" in url.lower():
                sas_page = pg
                print(f"Found ShareASale: {url[:60]}")
                break
        
        if sas_page:
            await sas_page.bring_to_front()
            await sas_page.wait_for_timeout(2000)
            
            # Try to click "Continue" button
            try:
                # Look for any "Continue" or "Get Started" button
                btn = await sas_page.query_selector("button:has-text('Continue'), a:has-text('Continue'), input[value*='Continue'], button:has-text('Get Started')")
                if btn:
                    await btn.click()
                    await sas_page.wait_for_timeout(3000)
                    print(f"Clicked Continue! New URL: {sas_page.url[:60]}")
                
                # Check for form fields
                fields = await sas_page.evaluate("""
                    () => Array.from(document.querySelectorAll("input:not([type=hidden]), textarea, select"))
                        .filter(el => el.offsetParent !== null)
                        .slice(0, 15)
                        .map(el => ({name: el.name, type: el.type, ph: el.placeholder, id: el.id}))
                """)
                print(f"Form fields: {len(fields)}")
                for f in fields:
                    print(f"  {f['name']}: {f['ph']}")
            except Exception as e:
                print(f"Error: {str(e)[:40]}")
        
        # Also check ThatAICollection 
        for pg in pages:
            if "thataicollection" in pg.url:
                await pg.bring_to_front()
                await pg.wait_for_timeout(1000)
                # Fill URL field if empty
                try:
                    url_input = await pg.query_selector("input[placeholder*='your-ai-tool'], input[name*='url'], input[type='url']")
                    if url_input:
                        current = await url_input.input_value()
                        if not current or "your-ai-tool" in current:
                            await url_input.fill("https://creatordir-tools.vercel.app")
                            print(f"Filled URL on ThatAICollection")
                except: pass
        
        await browser.close()

asyncio.run(main())
