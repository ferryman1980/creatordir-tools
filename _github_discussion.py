
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
            page = browser.contexts[0].pages[0]
            
            # Go to GitHub Discussions
            print("Navigating to GitHub Discussions...")
            await page.goto("https://github.com/ferryman1980/creatordir-tools/discussions/new", timeout=20000)
            await page.wait_for_timeout(3000)
            print(f"URL: {page.url[:80]}")
            
            # Check login status
            html = await page.content()
            if "login" in page.url.lower():
                print("Not logged in - redirecting to alternative")
                await page.goto("https://github.com/ferryman1980/creatordir-tools", timeout=15000)
                await page.wait_for_timeout(2000)
                print(f"GitHub URL: {page.url[:70]}")
            else:
                print("Logged in! Trying to fill Discussion form...")
                # Look for the category dropdown
                selects = await page.query_selector_all("select")
                print(f"Select elements: {len(selects)}")
                
                # Look for title input
                title_input = await page.query_selector("input[placeholder*='Title'], input[name*='title'], #title")
                if title_input:
                    await title_input.fill("CreatorAI Tools - 200+ AI Tools Directory for Content Creators")
                    print("Title filled!")
                
                # Look for body
                body_area = await page.query_selector("textarea, [contenteditable]")
                if body_area:
                    await body_area.fill("I built a curated directory of 200+ AI tools for content creators. Check it out!\n\nhttps://creatordir-tools.vercel.app\n\nFeatures:\n- 200+ articles with honest reviews\n- AI Writing, Design, Video, Audio tools\n- Comparisons and tutorials\n- Open source on GitHub")
                    print("Body filled!")
            
            await browser.close()
        except Exception as e:
            print(f"Error: {str(e)[:80]}")

asyncio.run(main())
