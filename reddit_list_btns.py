import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    print("URL:", pg.url)

    # List all buttons with details
    result = await pg.evaluate("""() => {
        const btns = document.querySelectorAll("button");
        return Array.from(btns).map(b => ({
            text: b.textContent.trim().substring(0,40),
            disabled: b.disabled,
            type: b.type,
            cls: (b.className || "").substring(0,40),
            visible: b.offsetParent !== null
        }));
    }""")
    print(f"All buttons ({len(result)}):")
    for b in result:
        print(f"  [{b['text']}] disabled={b['disabled']} visible={b['visible']} type={b['type']}")
    await p.stop()

asyncio.run(main())