import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    browser = await p.chromium.launch(channel="msedge", headless=False)
    page = await browser.new_page()
    
    EMAIL = "346010735@qq.com"
    PASSWORD = "Ckyhy388"
    PHONE = "18991377556"
    SITE = "https://creatordir-tools.vercel.app"
    
    results = []
    
    # 1. Namecheap Affiliates
    print("\n=== 1. Namecheap Affiliates ===")
    try:
        await page.goto("https://www.namecheap.com/affiliates/apply/", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url}")
        
        # Try to find signup form
        inputs = await page.$$("input:visible")
        for inp in inputs:
            try:
                name = await inp.evaluate("el => el.name || el.id || el.placeholder || ''")
                if "email" in name.lower():
                    await inp.fill(EMAIL)
                    print(f"  Filled email")
                elif "pass" in name.lower():
                    await inp.fill(PASSWORD)
                    print(f"  Filled password")
                elif "first" in name.lower() or "fname" in name.lower():
                    await inp.fill("Kang")
                    print(f"  Filled first name")
                elif "last" in name.lower() or "lname" in name.lower():
                    await inp.fill("Jian")
                    print(f"  Filled last name")
                elif "site" in name.lower() or "website" in name.lower() or "url" in name.lower():
                    await inp.fill(SITE)
                    print(f"  Filled website")
            except:
                pass
        
        results.append(("Namecheap", "Form filled - check browser"))
    except Exception as e:
        results.append(("Namecheap", f"Error: {str(e)[:60]}"))
    
    # 2. Bluehost Affiliates
    print("\n=== 2. Bluehost Affiliates ===")
    try:
        await page.goto("https://www.bluehost.com/affiliates/", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url}")
        
        # Click signup/apply button
        btns = await page.$$("a:visible, button:visible")
        for btn in btns:
            try:
                text = await btn.inner_text()
                if "apply" in text.lower() or "sign up" in text.lower() or "join" in text.lower() or "register" in text.lower():
                    await btn.click()
                    print(f"  Clicked: {text[:40]}")
                    await page.wait_for_timeout(3000)
                    break
            except:
                pass
        
        # Fill form
        inputs = await page.$$("input:visible")
        for inp in inputs:
            try:
                name = await inp.evaluate("el => el.name || el.id || el.placeholder || ''")
                if "email" in name.lower():
                    await inp.fill(EMAIL)
                    print(f"  Filled email")
                elif "pass" in name.lower():
                    await inp.fill(PASSWORD)
            except:
                pass
        
        results.append(("Bluehost", "Form filled - check browser"))
    except Exception as e:
        results.append(("Bluehost", f"Error: {str(e)[:60]}"))
    
    # 3. ConvertKit Affiliates  
    print("\n=== 3. ConvertKit Affiliates ===")
    try:
        await page.goto("https://convertkit.com/affiliates", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url}")
        results.append(("ConvertKit", "Page loaded - find signup button"))
    except Exception as e:
        results.append(("ConvertKit", f"Error: {str(e)[:60]}"))
    
    # 4. GetResponse Affiliates
    print("\n=== 4. GetResponse Affiliates ===")
    try:
        await page.goto("https://www.getresponse.com/affiliates", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url}")
        results.append(("GetResponse", "Page loaded"))
    except Exception as e:
        results.append(("GetResponse", f"Error: {str(e)[:60]}"))
    
    # 5. Elegant Themes Affiliates
    print("\n=== 5. Elegant Themes (Divi) ===")
    try:
        await page.goto("https://www.elegantthemes.com/affiliates/", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        print(f"Loaded: {page.url}")
        results.append(("ElegantThemes", "Page loaded"))
    except Exception as e:
        results.append(("ElegantThemes", f"Error: {str(e)[:60]}"))
    
    # Print summary
    print("\n\n=== REGISTRATION SUMMARY ===")
    for name, status in results:
        print(f"  {name}: {status}")
    print("\nBrowser is open - please check each tab and complete any verifications needed!")
    print("Press Enter in the terminal when you are done...")
    
    # Keep browser open for user
    await page.wait_for_timeout(300000)  # 5 minutes
    
    await browser.close()
    await p.stop()

asyncio.run(main())
