import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    for tab in ctx.pages:
        if "/posts/new" in tab.url:
            ph = tab
            break
    else:
        print("no tab")
        await p.stop()
        return
    
    await ph.bring_to_front()
    await ph.wait_for_timeout(1000)
    print("PH tab found")
    
    # Fill URL using native setter
    await ph.evaluate('''
        var inp = document.querySelector("input[placeholder*=\"www.\"], input[placeholder*=\"producthunt\"]");
        if (inp) {
            var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
            setter.call(inp, "https://creatordir-tools.vercel.app");
            inp.dispatchEvent(new Event("input", {bubbles:true}));
            inp.dispatchEvent(new Event("change", {bubbles:true}));
        }
    ''')
    print("URL filled")
    await ph.wait_for_timeout(1500)
    
    # Also check if there's an existing draft we need to deal with
    # Click Start
    await ph.evaluate('''
        var btns = document.querySelectorAll("button");
        for (var b of btns) {
            if (b.textContent.trim() === "开始" || b.textContent.trim() === "Start") {
                b.click();
                break;
            }
        }
    ''')
    print("Start clicked")
    await ph.wait_for_timeout(3000)
    
    # Check if full form appeared
    page_text = await ph.evaluate("document.body.innerText")
    print("After start:")
    print(page_text[:500])
    
    # If full form, fill fields
    if "发射名称" in page_text or "Launch name" in page_text:
        # Fill name
        await ph.evaluate('''
            var inputs = document.querySelectorAll("input");
            for (var i of inputs) {
                var ph = (i.placeholder || "").toLowerCase();
                if (ph.includes("name") || ph.includes("发射")) {
                    var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
                    setter.call(i, "CreatorDir - AI Tools Directory");
                    i.dispatchEvent(new Event("input", {bubbles:true}));
                    break;
                }
            }
        ''')
        print("Name filled")
        
        # Fill tagline
        await ph.evaluate('''
            var inputs = document.querySelectorAll("input");
            for (var i of inputs) {
                var ph = (i.placeholder || "").toLowerCase();
                if (ph.includes("tagline") || ph.includes("标语")) {
                    var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
                    setter.call(i, "500+ free AI tools directory for creators and developers");
                    i.dispatchEvent(new Event("input", {bubbles:true}));
                    break;
                }
            }
        ''')
        print("Tagline filled")
    
    await p.stop()

asyncio.run(main())
