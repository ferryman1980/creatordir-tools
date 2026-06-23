
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pages = browser.contexts[0].pages
        
        # Futurepedia - examine buttons
        page = pages[1]
        await page.bring_to_front()
        await page.wait_for_timeout(2000)
        
        # Get ALL buttons with their text
        buttons = await page.evaluate("""() => {
            const btns = document.querySelectorAll("button, a");
            return Array.from(btns).map(b => ({
                text: (b.innerText || b.textContent || "").trim().substring(0, 40),
                href: b.href || "",
                visible: b.offsetParent !== null
            })).filter(b => b.text || b.href);
        }""")
        
        print("=== Futurepedia Buttons/Links ===")
        for b in buttons[:30]:
            print(f'  {b["text"][:40]:40s} visible={b["visible"]} href={b["href"][:50]}')
        
        # Try clicking "Submit Tool" or similar
        for b in buttons:
            t = b["text"].lower()
            if "submit" in t or "add" in t or "list" in t:
                print(f"\nClicking: {b['text']}")
                # Find and click the element
                el = await page.query_selector(f"button:has-text('{b['text'][:20]}')")
                if el:
                    await el.click()
                    await page.wait_for_timeout(3000)
                    print(f"  After click URL: {page.url[:70]}")
                    
                    # Check for new inputs
                    inputs = await page.query_selector_all("input:visible, textarea:visible")
                    print(f"  Visible inputs now: {len(inputs)}")
                    for inp in inputs:
                        ph = (await inp.get_attribute("placeholder") or "")
                        nm = (await inp.get_attribute("name") or "")
                        print(f"    {nm}: {ph}")
                    break
        
        # Check if there's a navigation
        nav_links = await page.evaluate("""() => {
            const links = document.querySelectorAll("nav a, header a, .menu a");
            return Array.from(links).map(l => ({
                text: l.innerText.trim().substring(0, 30),
                href: l.href
            }));
        }""")
        print("\n=== Navigation Links ===")
        for l in nav_links:
            print(f'  {l["text"]:30s} -> {l["href"][:60]}')
        
        await browser.close()

asyncio.run(main())
