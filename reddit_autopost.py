import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Make sure we're on the submit page
    if "/submit" not in pg.url:
        await pg.goto("https://www.reddit.com/submit?type=TEXT", timeout=20000)
        await asyncio.sleep(3)
    
    print("URL:", pg.url)
    
    # Step 1: Choose a subreddit  
    # Find and click the subreddit selector
    sr_chooser = pg.locator('[role="combobox"] input, input[name="subredditName"]')
    sr_count = await sr_chooser.count()
    print(f"Subreddit inputs: {sr_count}")
    
    # Try clicking on the area to choose a subreddit
    # Find all the contenteditable areas
    editors = pg.locator('[contenteditable], div[role="textbox"]')
    count = await editors.count()
    print(f"Editors found: {count}")
    
    for i in range(count):
        ph = await editors.nth(i).get_attribute("placeholder") or ""
        aria = await editors.nth(i).get_attribute("aria-label") or ""
        print(f"  Editor {i}: placeholder=[{ph}] aria=[{aria}]")
    
    # The first editor is likely title, second is body
    # Fill title
    if count >= 1:
        title_el = editors.nth(0)
        await title_el.click()
        await title_el.fill("I built a directory of 200+ AI tools for content creators - all tested and reviewed")
        print("Title filled")
    
    # Fill body
    if count >= 2:
        body_el = editors.nth(1)
        await body_el.click()
        await body_el.fill("After months of testing AI tools, I created a curated directory at https://creatordir-tools.vercel.app

Features: 200+ articles, 54 tool reviews, comparisons, and tutorials

All free, open source on GitHub. Would love feedback from the community!")
        print("Body filled")
    
    await asyncio.sleep(2)
    
    # Try to find and click post button
    post_btns = await pg.evaluate("""() => {
        const btns = document.querySelectorAll("button");
        return Array.from(btns).map(b => ({
            text: b.textContent.trim().substring(0,30),
            disabled: b.disabled,
            type: b.type
        }));
    }""")
    print(f"\nButtons ({len(post_btns)}):")
    for b in post_btns:
        print(f"  [{b['text']}] disabled={b['disabled']}")
    
    await p.stop()

asyncio.run(main())
