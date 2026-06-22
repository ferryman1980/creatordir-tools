
import asyncio, json, os, sys
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pages = browser.contexts[0].pages
        print(f"Connected! Pages: {len(pages)}")
        
        # Use the first page to go to GitHub
        page = pages[0]
        await page.goto("https://github.com/ferryman1980/creatordir-tools/discussions/new", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        print(f"Current: {page.url}")
        
        # Create a Discussion (promotion post)
        category = await page.query_selector("select")
        if category:
            await category.select_option("Show and tell")
            await page.wait_for_timeout(1000)
        
        title_input = await page.query_selector("input[placeholder*='Title']")
        if title_input:
            await title_input.fill("CreatorAI Tools - 200+ AI Tools Directory for Content Creators")
        
        body_editor = await page.query_selector("textarea, div[contenteditable]")
        if body_editor:
            body_text = "I built a curated directory of 200+ AI tools for content creators.\n\n"
            body_text += "https://creatordir-tools.vercel.app\n\n"
            body_text += "Features:\n"
            body_text += "- 200+ articles with honest reviews\n"
            body_text += "- AI Writing, Design, Video, Audio tools\n"
            body_text += "- Comparisons and tutorials\n"
            body_text += "- Open source on GitHub\n\n"
            body_text += "Would love feedback!"
            await body_editor.fill(body_text)
        
        print("Form filled, ready for submit")
        await page.screenshot(path="D:/项目/工作区/工作5/github_discussion.png")
        print("Screenshot saved")
        
        await browser.close()

asyncio.run(main())
