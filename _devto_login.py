import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    
    page = await edge.contexts[0].new_page()
    
    # Go to Dev.to
    print("Opening Dev.to...")
    await page.goto("https://dev.to/enter", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(2000)
    
    print(f"URL: {page.url}")
    
    # Check if we need to login
    page_text = await page.evaluate("document.body.innerText")
    if "github" in page_text.lower() or "GitHub" in page_text:
        # Click GitHub login
        print("GitHub login option found, clicking...")
        try:
            github_btn = await page.query_selector('button:has-text("GitHub")')
            if not github_btn:
                github_btn = await page.query_selector('a:has-text("GitHub")')
            if not github_btn:
                github_btn = await page.query_selector('[href*="github"]')
            if github_btn:
                await github_btn.click()
                await page.wait_for_timeout(5000)
                print(f"After GitHub click: {page.url}")
        except Exception as e:
            print(f"GitHub click error: {e}")
    
    await page.wait_for_timeout(2000)
    print(f"Final URL: {page.url}")
    print(f"Page text (first 500): {(await page.evaluate('document.body.innerText'))[:500]}")
    
    await page.close()
    await p.stop()

asyncio.run(main())
