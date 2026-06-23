import asyncio, json, os, re
from playwright.async_api import async_playwright

async def try_submit():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        
        # Test each directory one by one with its own context
        dirs_to_test = [
            ("ThatAICollection2", "https://thataicollection.com/en/submit/"),
        ]
        
        for name, url in dirs_to_test:
            ctx = await browser.new_context()
            page = await ctx.new_page()
            try:
                await page.goto(url, timeout=20000, wait_until="domcontentloaded")
                await asyncio.sleep(3)
                # Check if there are visible input fields
                inputs = await page.query_selector_all("input[type=text], input[type=url], input[type=email], textarea")
                print(f"[{name}] Found {len(inputs)} input fields")
                for inp in inputs[:5]:
                    placeholder = await inp.get_attribute("placeholder") or "none"
                    input_type = await inp.get_attribute("type") or "text"
                    name_attr = await inp.get_attribute("name") or "none"
                    print(f"  type={input_type} name={name_attr} placeholder={placeholder}")
                
                submits = await page.query_selector_all("button[type=submit], input[type=submit]")
                print(f"[{name}] Found {len(submits)} submit buttons")
                
            except Exception as e:
                print(f"[{name}] Error: {str(e)[:60]}")
            finally:
                await page.close()
                await ctx.close()
        await browser.close()

asyncio.run(try_submit())
