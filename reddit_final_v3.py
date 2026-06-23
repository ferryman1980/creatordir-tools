import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    if "/submit" not in pg.url:
        await pg.goto("https://www.reddit.com/submit?type=TEXT", timeout=20000)
        await asyncio.sleep(3)
    print("URL:", pg.url)

    js_code = """() => {
        const editors = document.querySelectorAll('div[contenteditable="true"]');
        if (editors.length >= 1) {
            editors[0].focus();
            editors[0].textContent = "I built a directory of 200+ AI tools for content creators - all tested and reviewed";
        }
        if (editors.length >= 2) {
            editors[1].focus();
            editors[1].textContent = "After months of testing AI tools, I created a curated directory at https://creatordir-tools.vercel.app\\n\\nFeatures: 200+ articles, 54 tool reviews, comparisons, and tutorials\\n\\nAll free, open source on GitHub. Would love feedback from the community!";
        }
        return editors.length;
    }"""
    result = await pg.evaluate(js_code)
    print(f"Filled {result} editors")
    await asyncio.sleep(2)

    click_code = """() => {
        const btns = document.querySelectorAll("button");
        for (const b of btns) {
            const txt = b.textContent.trim();
            if (txt.includes("Post") || txt.includes("\u53d1\u5e03")) {
                b.disabled = false;
                b.click();
                return "Clicked: " + txt.substring(0,20);
            }
        }
        for (const b of btns) { if (!b.disabled && b.textContent.trim().length > 0) {
            b.click(); return "Clicked first non-disabled: " + b.textContent.trim().substring(0,20);
        } }
        return "no";
    }"""
    result2 = await pg.evaluate(click_code)
    print("Post:", result2)
    await asyncio.sleep(3)
    print("Final URL:", pg.url)
    await p.stop()

asyncio.run(main())