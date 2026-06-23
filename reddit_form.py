import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    await pg.goto("https://www.reddit.com/register/", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(3)
    
    # Get all interactive elements
    all_els = await pg.evaluate("""() => {
        const all = document.querySelectorAll("*");
        const results = [];
        for (const el of all) {
            if (el.tagName === "INPUT" || el.tagName === "BUTTON" || el.tagName === "A" || el.tagName === "SELECT" || el.getAttribute("role") === "button" || el.contentEditable === "true") {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    results.push({
                        tag: el.tagName,
                        type: el.type || el.getAttribute("type") || "",
                        text: (el.textContent || "").trim().substring(0,30),
                        placeholder: el.placeholder || "",
                        id: el.id || "",
                        name: el.name || "",
                        role: el.getAttribute("role") || "",
                        aria_label: el.getAttribute("aria-label") || "",
                        class: (el.className || "").substring(0,40)
                    });
                }
            }
        }
        return results;
    }""")
    print(f"Interactive elements ({len(all_els)}):")
    for e in all_els:
        print(f"  {e['tag']} type={e['type']} text=[{e['text']}] placeholder=[{e['placeholder']}] role=[{e['role']}] aria=[{e['aria_label']}]")
    
    await p.stop()

asyncio.run(main())
