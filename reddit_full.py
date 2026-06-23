import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Go to register
    await pg.goto("https://www.reddit.com/register/", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(4)
    print("Step 1: Filling email...")
    
    # Fill email and submit
    email_input = pg.locator('input[name="email"]')
    await email_input.wait_for(state="visible", timeout=10000)
    await email_input.fill("346010735@qq.com")
    print("Email filled")
    
    # Press Enter to submit
    await email_input.press("Enter")
    await asyncio.sleep(3)
    print(f"URL after email: {pg.url}")
    
    # Wait for step 2 - username form
    try:
        username_input = pg.locator('input[name="username"]')
        await username_input.wait_for(state="visible", timeout=10000)
        print("Username field appeared!")
    except:
        print("No username field, checking page...")
        text = await pg.evaluate("document.body.innerText")
        print(text[:1000])
        text = await pg.evaluate("document.body.innerText")
        print(text[:1000])
        return
    
    # Fill username and password
    await username_input.fill("CreatorAI_Tools")
    print("Username filled")
    
    # Fill password
    pw_input = pg.locator('input[name="password"]')
    await pw_input.fill("Ckyhy388")
    print("Password filled")
    
    # Click submit/continue
    submit_btn = pg.locator('button:has-text("继续"), button:has-text("Continue"), button[type="submit"]')
    await submit_btn.first.click()
    print("Clicked submit")
    
    await asyncio.sleep(5)
    print(f"\nFinal URL: {pg.url}")
    text = await pg.evaluate("document.body.innerText")
    print(text[:1500])
    
    await p.stop()

asyncio.run(main())
