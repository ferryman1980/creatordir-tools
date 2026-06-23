
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://creatordir-tools.vercel.app"
NAME = "CreatorAI Tools"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        pages = browser.contexts[0].pages
        
        # Find ThatAICollection
        for pg in pages:
            if "thataicollection" in pg.url:
                await pg.bring_to_front()
                await pg.wait_for_timeout(2000)
                print(f"ThatAICollection: {pg.url[:60]}")
                
                # Check all inputs including hidden ones
                all_inputs = await pg.evaluate("""
                    () => {
                        const inputs = document.querySelectorAll("input, textarea");
                        return Array.from(inputs).map(el => ({
                            name: el.name || "",
                            id: el.id || "",
                            ph: el.placeholder || "",
                            type: el.type || "",
                            value: el.value || "",
                            tag: el.tagName,
                            visible: el.offsetParent !== null
                        }));
                    }
                """)
                print(f"Total inputs: {len(all_inputs)}")
                for f in all_inputs:
                    print(f"  [{f['tag']}] {f['name']:20s} type={f['type']:10s} val={f['value'][:20]:20s} visible={f['visible']}")
                
                # Fill name and URL fields specifically
                for f in all_inputs:
                    txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
                    sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                    try:
                        el = await pg.query_selector(sel)
                        if not el: continue
                        
                        if "tool_name" in txt or "name" in txt or "title" in txt:
                            await el.fill(NAME)
                            print(f"  >>> FILLED NAME: {NAME}")
                        elif "tool_url" in txt or "url" in txt or "website" in txt:
                            await el.fill(SITE)
                            print(f"  >>> FILLED URL: {SITE}")
                    except Exception as e:
                        print(f"  {f['name']}: {str(e)[:20]}")
                
                # Try all buttons
                btns = await pg.evaluate("""
                    () => Array.from(document.querySelectorAll("button, input[type=submit]"))
                        .filter(el => el.offsetParent !== null)
                        .map(el => ({text: (el.innerText || el.value || "").trim().substring(0, 20), tag: el.tagName}))
                """)
                print(f"\nButtons: {[b['text'] for b in btns]}")
                
                break
        
        await browser.close()

asyncio.run(main())
