import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    browser = await p.chromium.launch(channel="msedge", headless=False)
    page = await browser.new_page()
    
    EMAIL = "346010735@qq.com"
    SITE = "https://creatordir-tools.vercel.app"
    
    results = []
    
    # Helper to fill inputs
    async def fill_fields(page, fields):
        inputs = await page.query_selector_all("input, textarea")
        for inp in inputs:
            try:
                is_visible = await inp.is_visible()
                if not is_visible:
                    continue
                name = (await inp.get_attribute("name") or "")
                pid = (await inp.get_attribute("id") or "")
                ph = (await inp.get_attribute("placeholder") or "")
                combined = (name + " " + pid + " " + ph).lower()
                
                for key, val in fields.items():
                    if key in combined:
                        await inp.fill(val)
                        print(f"  Filled: {key} -> {val[:30]}...")
                        break
            except:
                pass
    
    # 1. Namecheap
    print("\n=== 1. Namecheap ===")
    try:
        await page.goto("https://www.namecheap.com/affiliates/apply/", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url[:60]}")
        await fill_fields(page, {"email": EMAIL, "site": SITE, "website": SITE, "url": SITE})
        results.append(("Namecheap", "Open"))
    except Exception as e:
        results.append(("Namecheap", str(e)[:50]))
    
    # 2. Bluehost
    print("\n=== 2. Bluehost ===")
    try:
        await page.goto("https://www.bluehost.com/affiliates/", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url[:60]}")
        # Try clicking join
        for text in ["Apply", "Sign Up", "Join", "Get Started"]:
            btn = await page.query_selector(f"a:has-text('{text}'), button:has-text('{text}')")
            if btn:
                await btn.click()
                print(f"  Clicked '{text}'")
                await page.wait_for_timeout(3000)
                break
        await fill_fields(page, {"email": EMAIL, "site": SITE})
        results.append(("Bluehost", "Open"))
    except Exception as e:
        results.append(("Bluehost", str(e)[:50]))
    
    # 3. ConvertKit
    print("\n=== 3. ConvertKit ===")
    try:
        await page.goto("https://convertkit.com/affiliates", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url[:60]}")
        results.append(("ConvertKit", "Open"))
    except Exception as e:
        results.append(("ConvertKit", str(e)[:50]))
    
    # 4. SiteGround
    print("\n=== 4. SiteGround ===")
    try:
        await page.goto("https://www.siteground.com/affiliates/", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url[:60]}")
        await fill_fields(page, {"email": EMAIL, "site": SITE})
        results.append(("SiteGround", "Open"))
    except Exception as e:
        results.append(("SiteGround", str(e)[:50]))
    
    # 5. Elegant Themes
    print("\n=== 5. Elegant Themes ===")
    try:
        await page.goto("https://www.elegantthemes.com/affiliates/", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url[:60]}")
        results.append(("ElegantThemes", "Open"))
    except Exception as e:
        results.append(("ElegantThemes", str(e)[:50]))
    
    # Summary
    print("\n\n=== REGISTRATION STATUS ===")
    for name, status in results:
        print(f"  {name}: {status}")
    print("\nBrowser is OPEN - please complete any verification codes in the browser tabs.")
    print("Type 'done' in terminal and press Enter when finished...")
    
    # Wait for user input
    await page.wait_for_timeout(600000)  # 10 min timeout
    
    await browser.close()
    await p.stop()

asyncio.run(main())
