import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = await edge.contexts[0].new_page()
    
    await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(2000)
    
    # Fill title to make sure we can publish
    await page.fill("#article-form-title", "The Ultimate AI Tools Directory: 200+ Tested Tools for Creators and Developers")
    await page.wait_for_timeout(300)
    
    # Check all buttons
    btns = await page.evaluate("""() => {
        const allBtns = document.querySelectorAll('button');
        return Array.from(allBtns).map(b => ({
            text: b.innerText.trim().slice(0,30),
            visible: b.offsetParent !== null,
            classes: b.className.slice(0,50),
            id: b.id
        }));
    }""")
    print("Buttons found:")
    for b in btns:
        if b["text"]:
            print(f"  [{b['text']}] visible={b['visible']}")
    
    # Also check for publish/draft buttons
    save_btns = await page.evaluate("""() => {
        const all = document.querySelectorAll('button, input[type=submit], a');
        return Array.from(all)
            .filter(el => {
                const t = (el.innerText || el.value || "").toLowerCase();
                return t.includes('publish') || t.includes('save') || t.includes('发布') || t.includes('draft');
            })
            .map(el => ({
                tag: el.tagName,
                text: (el.innerText || el.value || "").trim().slice(0,40),
                type: el.getAttribute('type') || ''
            }));
    }""")
    print(f"\nPublish/Save buttons:")
    for b in save_btns:
        print(f"  {b}")
    
    await page.close()
    await p.stop()

asyncio.run(main())
