
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=30000)
        page = browser.contexts[0].pages[1]
        await page.wait_for_timeout(2000)
        print("URL:", page.url[:80])
        
        inputs = await page.evaluate("""() => {
            const ins = document.querySelectorAll("input, select, textarea, button");
            return Array.from(ins).slice(0, 30).map(i => ({
                tag: i.tagName,
                name: i.name || "",
                id: i.id || "",
                type: i.type || "",
                placeholder: (i.placeholder || "").substring(0, 25),
                text: (i.innerText || "").trim().substring(0, 25)
            }));
        }""")
        for inp in inputs:
            print(f'  [{inp["tag"]}] name={inp["name"]} id={inp["id"]} type={inp["type"]} place={inp["placeholder"]} text={inp["text"]}')
        
        await browser.close()

asyncio.run(main())
