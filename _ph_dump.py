import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    
    ph = None
    for tab in edge.contexts[0].pages:
        if "/submission" in tab.url:
            ph = tab
            break
    if not ph:
        print("no tab")
        await p.stop()
        return
    
    await ph.bring_to_front()
    
    # Dump ALL input fields with ALL attributes
    dump = await ph.evaluate("""
        () => {
            const all = document.querySelectorAll("input, textarea");
            return Array.from(all).map(el => ({
                tag: el.tagName,
                type: el.type || "",
                id: el.id,
                name: el.name || "",
                placeholder: el.placeholder || "",
                value: el.value || "",
                cls: (el.className || "").slice(0, 30),
                required: el.required || false,
                'aria-label': el.getAttribute("aria-label") || "",
                'data-test': el.getAttribute("data-test") || "",
                rows: el.rows || 0,
            }));
        }
    """)
    
    for d in dump:
        print(f"[{d['tag']}] type={d['type']} id={d['id']} name={d['name']}")
        print(f"  ph='{d['placeholder'][:40]}' val='{d['value'][:30]}' req={d['required']}")
    
    await p.stop()

asyncio.run(main())
