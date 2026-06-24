import asyncio, json
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    
    # Open Reddit to get OAuth token
    page = await edge.contexts[0].new_page()
    await page.goto("https://www.reddit.com", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(3000)
    
    # Try to get OAuth token from cookies
    cookies = await page.context.cookies()
    reddit_cookies = [c for c in cookies if "reddit" in c.get("domain","")]
    
    token = None
    for c in reddit_cookies:
        print(f"Cookie: {c.get('name')} = {c.get('value','')[:50]}...")
        if "token" in c.get("name","").lower():
            token = c.get("value")
    
    # Also try from localStorage
    try:
        ls_data = await page.evaluate("""() => {
            const items = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if(key) items[key] = localStorage.getItem(key);
            }
            return items;
        }""")
        for k, v in ls_data.items():
            if k and v and isinstance(v, str) and len(v) > 20:
                print(f"LS: {k[:30]} = {v[:80]}...")
                if "token" in k.lower() or "bearer" in k.lower() or "access" in k.lower():
                    token = v
    except Exception as e:
        print(f"LS error: {e}")
    
    print(f"\n--- TOKEN FOUND: {bool(token)} ---")
    
    # Also check if already logged in
    try:
        body_text = await page.evaluate("document.body.innerText")
        if "log in" in body_text[:1000].lower() or "sign up" in body_text[:1000].lower():
            print("Status: NOT logged in")
        else:
            print("Status: Might be logged in (checking further...)")
            # Check for user menu
            has_menu = await page.evaluate("!!document.querySelector('[data-testid=\"user-menu-button\"]')")
            print(f"Has user menu: {has_menu}")
    except:
        pass
    
    await page.close()
    await p.stop()

asyncio.run(main())
