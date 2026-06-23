import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    
    # Go to subreddit page directly
    await pg.goto("https://www.reddit.com/r/ArtificialIntelligence/", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(4)
    
    # Take screenshot for debugging
    await pg.screenshot(path="D:\项目\工作区\工作5\screenshots\reddit_sub.png", full_page=True)
    print("Screenshot saved")
    
    # Check for Create Post button
    buttons = await pg.evaluate("""() => {
        const btns = document.querySelectorAll("button, a, [role='button']");
        return Array.from(btns).map(b => ({
            text: (b.textContent || "").trim().substring(0,50),
            href: b.href || "",
            class: (b.className || "").substring(0,40)
        })).filter(x => 
            x.text.toLowerCase().includes("create") || 
            x.text.toLowerCase().includes("post") ||
            x.text.includes("帖子")
        );
    }""")
    print("\nCreate Post buttons:")
    for b in buttons:
        print(f"  [{b['text']}]")
    
    # Check the page for any post creation elements
    create_btns = await pg.locator('[role="button"]:has-text("Create"), button:has-text("Create Post"), a:has-text("Create Post")').count()
    print(f"\nCreate Post count by locator: {create_btns}")
    
    await p.stop()

asyncio.run(main())
