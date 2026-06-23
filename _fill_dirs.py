
import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pages = browser.contexts[0].pages
        
        # Futurepedia (page 2)
        page = pages[1]
        await page.bring_to_front()
        await page.wait_for_timeout(2000)
        print("=== Futurepedia ===")
        
        # Scroll to show form
        await page.evaluate("window.scrollTo(0, 800)")
        await page.wait_for_timeout(1000)
        
        # Get visible inputs
        fields = await page.evaluate("""() => {
            const els = document.querySelectorAll("input, textarea");
            return Array.from(els).map(el => ({
                tag: el.tagName, type: el.type, name: el.name,
                id: el.id, ph: el.placeholder, visible: el.offsetParent !== null
            }));
        }""")
        
        for f in fields:
            if f["visible"]:
                print(f'  visible: {f["tag"]} name={f["name"]} ph={f["ph"]}')
        
        # Fill inputs by querying directly
        text_inputs = await page.query_selector_all("input:visible")
        textareas = await page.query_selector_all("textarea:visible")
        
        for inp in text_inputs + textareas:
            try:
                ph = (await inp.get_attribute("placeholder") or "").lower()
                nm = (await inp.get_attribute("name") or "").lower()
                combined = ph + " " + nm
                
                if "name" in combined or "title" in combined:
                    await inp.fill("CreatorAI Tools")
                    print(f"  Filled NAME: {nm or ph}")
                elif "url" in combined or "website" in combined:
                    await inp.fill("https://creatordir-tools.vercel.app")
                    print(f"  Filled URL: {nm or ph}")
                elif "desc" in combined or "about" in combined:
                    await inp.fill("Curated directory of 200+ AI tools for content creators")
                    print(f"  Filled DESC: {nm or ph}")
                elif "email" in combined:
                    await inp.fill("346010735@qq.com")
                    print(f"  Filled EMAIL: {nm or ph}")
            except:
                pass
        
        # Try to find and click submit
        try:
            submit_btn = None
            btns = await page.query_selector_all("button:visible")
            for btn in btns:
                text = (await btn.inner_text()).lower()
                if any(w in text for w in ["submit", "add", "list", "send"]):
                    submit_btn = btn
                    print(f"  Found submit: {text[:30]}")
                    break
            
            if submit_btn:
                await submit_btn.click()
                await page.wait_for_timeout(3000)
                print(f"  Submitted! URL: {page.url[:80]}")
        except Exception as e:
            print(f"  Submit error: {str(e)[:50]}")
        
        # === ToolPilot (page 3) ===
        print("\n=== ToolPilot ===")
        page2 = pages[2]
        await page2.bring_to_front()
        await page2.wait_for_timeout(2000)
        await page2.evaluate("window.scrollTo(0, 800)")
        await page2.wait_for_timeout(1000)
        
        tinputs = await page2.query_selector_all("input:visible, textarea:visible")
        print(f"Visible inputs: {len(tinputs)}")
        for inp in tinputs:
            try:
                ph = (await inp.get_attribute("placeholder") or "").lower()
                nm = (await inp.get_attribute("name") or "").lower()
                print(f"  input: name={nm[:30]} ph={ph[:30]}")
            except:
                pass
        
        await browser.close()
        print("\nDone!")

asyncio.run(main())
