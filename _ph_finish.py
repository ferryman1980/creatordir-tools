import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    ph = None
    for tab in ctx.pages:
        if "/submission" in tab.url:
            ph = tab
            break
    if not ph:
        print("no ph tab")
        await p.stop()
        return
    
    await ph.bring_to_front()
    
    # Keep clicking next buttons until we find submit
    for attempt in range(10):
        await ph.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await ph.wait_for_timeout(500)
        
        btns = await ph.evaluate("""
            () => Array.from(document.querySelectorAll("button")).map(b => b.textContent.trim()).filter(t => t.length > 0 && t.length < 40)
        """)
        
        # Find first "next" or "submit" button
        clicked = False
        for btn_text in btns:
            if btn_text == "提交" or btn_text == "Submit" or btn_text == "Publish" or btn_text == "发布":
                # Click submit
                all_btns = await ph.query_selector_all("button")
                for btn in all_btns:
                    t = await btn.text_content()
                    if t == btn_text:
                        await btn.scroll_into_view_if_needed()
                        await ph.wait_for_timeout(500)
                        await btn.click()
                        print(f"SUBMIT CLICKED: {t}")
                        await ph.wait_for_timeout(5000)
                        print(f"After submit URL: {ph.url[:80]}")
                        clicked = True
                        break
                if clicked: break
            
            elif "下一步" in btn_text or "Next" in btn_text:
                all_btns = await ph.query_selector_all("button")
                for btn in all_btns:
                    t = await btn.text_content()
                    if t == btn_text:
                        await btn.scroll_into_view_if_needed()
                        await ph.wait_for_timeout(500)
                        await btn.click()
                        print(f"Next: {t}")
                        await ph.wait_for_timeout(2000)
                        clicked = True
                        break
                if clicked: break
        
        if not clicked:
            print(f"No more buttons to click. Current: {btns}")
            break
    
    print(f"\nFinal URL: {ph.url[:80]}")
    page_text = await ph.evaluate("document.body.innerText")
    if "等待" in page_text or "pending" in page_text.lower() or "submitted" in page_text.lower():
        print("SUBMISSION APPEARS SUCCESSFUL!")
    else:
        # Check for submit button one more time
        if "提交" in page_text or "Submit" in page_text:
            print("Submit button still visible - needs manual click")
        else:
            print("Page status: unknown")
            print(page_text[500:1000])
    
    await p.stop()

asyncio.run(main())
