
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

EMAIL = "346010735@qq.com"
PASS = "Ckyhy388"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        pages = browser.contexts[0].pages
        print(f"Pages: {len(pages)}")
        
        for pg in pages:
            url = pg.url
            if "awin" in url.lower() or "shareasale" in url.lower():
                await pg.bring_to_front()
                await pg.wait_for_timeout(2000)
                print(f"\nAwin page: {url[:60]}")
                
                # Scroll down to find form
                await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await pg.wait_for_timeout(2000)
                
                # Get ALL form elements
                all_info = await pg.evaluate("""
                    () => Array.from(document.querySelectorAll("input, textarea, select, button, a"))
                        .filter(el => el.offsetParent !== null)
                        .map(el => ({
                            tag: el.tagName,
                            type: el.type || "",
                            name: el.name || "",
                            id: el.id || "",
                            ph: el.placeholder || "",
                            text: (el.innerText || el.textContent || "").trim().substring(0, 30),
                            href: el.href || ""
                        }))
                """)
                
                print(f"Visible elements: {len(all_info)}")
                for f in all_info[:20]:
                    print(f"  [{f['tag']}] {f['type']} name={f['name'][:15]} ph={f['ph'][:15]} text={f['text'][:15]}")
                
                # Fill email and password fields
                for f in all_info:
                    txt = (f["name"] + " " + f["id"] + " " + f["ph"]).lower()
                    val = None
                    if "email" in txt:
                        val = EMAIL
                    elif "password" in txt or "pass" in txt:
                        val = PASS
                    elif "first" in txt or "fname" in txt:
                        val = "Creator"
                    elif "last" in txt or "lname" in txt:
                        val = "AI"
                    elif "company" in txt or "business" in txt:
                        val = "CreatorAI Tools"
                    elif "website" in txt or "url" in txt:
                        val = "https://creatordir-tools.vercel.app"
                    
                    if val and f["tag"] == "INPUT":
                        try:
                            sel = f"#{f['id']}" if f["id"] else f"[name='{f['name']}']"
                            el = await pg.query_selector(sel)
                            if el:
                                await el.fill(val)
                                print(f"  FILLED {f['name'][:15]}: {val[:20]}")
                        except: pass
                break
        
        await browser.close()

asyncio.run(main())
