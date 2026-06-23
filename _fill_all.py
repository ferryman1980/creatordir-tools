
import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=8000)
            pages = browser.contexts[0].pages
            print(f"Connected: {len(pages)} pages")
            
            for i, page in enumerate(pages):
                url = page.url
                print(f"\nPage {i+1}: {url[:60]}")
                await page.wait_for_timeout(2000)
                
                # Get visible inputs
                info = await page.evaluate("""
                    () => {
                        const inputs = document.querySelectorAll("input:not([type=hidden]):not([type=checkbox]):not([type=radio]), textarea");
                        return Array.from(inputs).filter(i => i.offsetParent !== null).map(i => ({
                            name: i.name || "",
                            id: i.id || "", 
                            ph: i.placeholder || "",
                            tag: i.tagName
                        }));
                    }
                """)
                
                for f in info:
                    txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
                    val = None
                    if "name" in txt or "title" in txt: val = "CreatorAI Tools"
                    elif "url" in txt or "site" in txt or "website" in txt: val = "https://creatordir-tools.vercel.app"
                    elif "desc" in txt or "about" in txt: val = "Curated directory of 200+ AI tools"
                    elif "email" in txt: val = "346010735@qq.com"
                    
                    if val:
                        sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']" if f["name"] else ""
                        try:
                            if sel:
                                el = await page.query_selector(sel)
                                if el:
                                    await el.fill(val)
                                    print(f"  FILLED [{f['name'] or f['ph']}]: {val[:20]}")
                        except:
                            pass
                
                # Try submit buttons
                btn_info = await page.evaluate("""
                    () => Array.from(document.querySelectorAll("button:visible"))
                        .map(b => ({text: (b.innerText || "").trim().substring(0, 20)}))
                        .filter(b => b.text && (b.text.toLowerCase().includes("submit") || b.text.toLowerCase().includes("add") || b.text.toLowerCase().includes("list")))
                """)
                for b in btn_info:
                    print(f"  SUBMIT BUTTON: {b['text']}")
                
            await browser.close()
        except Exception as e:
            print(f"Error: {str(e)[:60]}")

asyncio.run(main())
