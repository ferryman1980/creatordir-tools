import asyncio
from playwright.async_api import async_playwright

async def main():
    print("Starting...")
    p = await async_playwright().start()
    browser = await p.chromium.connect_over_cdp("ws://127.0.0.1:9222/devtools/browser/3d547708-be2e-405e-a141-f0029cfacd1c")
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    print(f"Page: {page.url}")
    
    # GitHub Issue
    await page.goto("https://github.com/ferryman1980/creatordir-tools/issues/new", timeout=30000, wait_until="domcontentloaded")
    await asyncio.sleep(3)
    print(f"GitHub URL: {page.url}")
    
    if "issues/new" in page.url or "issues/new/choose" in page.url:
        try:
            link = page.get_by_role("link", name="Open a blank issue")
            if await link.count() > 0:
                await link.click()
                await asyncio.sleep(2)
        except:
            pass
        try:
            await page.fill('input[name="issue[title]"]', "Submit to 177+ AI Directories - Tracking", timeout=5000)
            print("Title OK")
        except Exception as e:
            print(f"Title: {e}")
        body = "## AI Directory Submission Plan\n\nSubmitting CreatorAI Tools to 177+ directories."
        try:
            await page.fill('textarea[name="issue[body]"]', body, timeout=5000)
            print("Body OK")
        except Exception as e:
            print(f"Body: {e}")
        try:
            btn = page.get_by_role("button", name="Submit new issue")
            if await btn.count() > 0:
                await btn.click()
                await asyncio.sleep(2)
                print("Issue submitted!")
        except Exception as e:
            print(f"Submit: {e}")
    else:
        print("Not on issue page")
    
    # Now submit to a few directories
    dirs = [
        ("AI Wizard", "https://aizwizard.com/submit"),
        ("AI Tool Guru", "https://aitoolguru.com/submit-tool"),
        ("Futurepedia", "https://www.futurepedia.io/submit-tool"),
    ]
    for name, url in dirs:
        print(f"\n--- {name}: {url} ---")
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            await asyncio.sleep(3)
            print(f"Loaded: {page.url}")
        except Exception as e:
            print(f"Error: {e}")
    
    await browser.close()
    await p.stop()
    print("\nDone!")

asyncio.run(main())
