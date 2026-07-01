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
        print("No submission tab")
        await p.stop()
        return
    
    await ph.bring_to_front()
    print(f"PH: {await ph.title()}")
    
    # Fill using Playwright fill() which triggers React events
    inputs = await ph.query_selector_all("input")
    for inp in inputs:
        ph_text = (await inp.get_attribute("placeholder") or "").lower()
        try:
            if "name" in ph_text or "发射名称" in ph_text:
                await inp.fill("CreatorDir - AI Tools Directory")
                print("Name filled")
            elif "tagline" in ph_text or "标语" in ph_text:
                await inp.fill("500+ free AI tools directory for creators")
                print("Tagline filled")
            elif "x.com" in ph_text or "twitter" in ph_text or "记载" in ph_text:
                await inp.fill("ferryman1980")
                print("Twitter filled")
            elif "github" in ph_text or "源代码" in ph_text or "repository" in ph_text:
                await inp.fill("https://github.com/ferryman1980/creatordir-tools")
                print("GitHub filled")
        except:
            pass
    
    # Fill textareas
    tas = await ph.query_selector_all("textarea")
    for ta in tas:
        ph_text = (await ta.get_attribute("placeholder") or "").lower()
        try:
            if "describe" in ph_text or "描述" in ph_text or "新颖" in ph_text:
                await ta.fill("A free directory of 500+ AI tools. 260+ comparison articles, 217 tool detail pages, search filters, open source.")
                print("Description filled")
            elif "comment" in ph_text or "评论" in ph_text or "motivate" in ph_text:
                await ta.fill("I built CreatorDir as a free resource for AI tools. 500+ tools with real comparisons!")
                print("Comment filled")
        except:
            pass
    
    await ph.wait_for_timeout(1000)
    
    # Check validation
    check = await ph.evaluate("""
        () => {
            const inputs = document.querySelectorAll("input, textarea");
            return Array.from(inputs).filter(i => i.value.length > 0).map(i => i.value.slice(0, 20));
        }
    """)
    print(f"Filled values: {len(check)} fields have values")
    for v in check:
        print(f"  '{v}'")
    
    # Verify what form says
    page_text = await ph.evaluate("document.body.innerText")
    if "需命名" in page_text or "标语" in page_text or "标签要求" in page_text:
        print("VALIDATION ERRORS still present")
    else:
        print("NO VALIDATION ERRORS!")
    
    # Check tags and submit buttons
    btns = await ph.evaluate("""
        () => Array.from(document.querySelectorAll("button")).map(b => b.textContent.trim()).filter(t => t.length > 0 && t.length < 35)
    """)
    print(f"Buttons: {btns}")
    
    await p.stop()

asyncio.run(main())
