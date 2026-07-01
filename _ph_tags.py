import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    ph = None
    for tab in ctx.pages:
        if "/posts/new" in tab.url:
            ph = tab
            break
    if not ph:
        print("PH not found")
        await p.stop()
        return
    
    await ph.bring_to_front()
    
    # Click on the tags input to open selector
    await ph.evaluate("""
        () => {
            const inputs = document.querySelectorAll('input');
            for (const i of inputs) {
                if (i.placeholder && i.placeholder.includes('选择启动') || i.placeholder.includes('launch tag')) {
                    i.click();
                    i.focus();
                    return;
                }
            }
            // Try clicking on the tag area container
            const all = document.querySelectorAll('div, span');
            for (const el of all) {
                if (el.textContent.includes('选择启动标签') || el.textContent.includes('launch tags')) {
                    el.click();
                    return;
                }
            }
        }
    """)
    print("Tags area clicked")
    
    # Fill first comment
    await ph.evaluate("""
        () => {
            const all = document.querySelectorAll('[contenteditable], textarea');
            for (const el of all) {
                const ph = (el.getAttribute('placeholder') || '').toLowerCase();
                if (ph.includes('comment') || ph.includes('评论')) {
                    el.textContent = 'I built CreatorDir as a completely free directory of 500+ AI tools. Every tool is curated and tested - from AI writing assistants to video generators. Check it out and let me know what you think!';
                    el.dispatchEvent(new Event('input', {bubbles:true}));
                    return;
                }
            }
        }
    """)
    print("Comment filled")
    
    # Check if we can see tag options now
    await ph.wait_for_timeout(2000)
    page_text = await ph.evaluate("document.body.innerText")
    if "AI" in page_text:
        # Click AI tag
        await ph.evaluate("""
            () => {
                const all = document.querySelectorAll('span, div');
                for (const el of all) {
                    const t = el.textContent.trim();
                    if (t === 'AI' || t === 'Artificial Intelligence' || t === '人工智能') {
                        el.click();
                        return 'AI clicked';
                    }
                }
                return 'AI not found';
            }
        """)
        print("AI tag clicked")
        await ph.wait_for_timeout(1000)
        
        # Click Productivity  
        await ph.evaluate("""
            () => {
                const all = document.querySelectorAll('span, div');
                for (const el of all) {
                    const t = el.textContent.trim();
                    if (t === 'Productivity' || t === '生产力' || t === 'Developer Tools') {
                        el.click();
                        return 'clicked';
                    }
                }
                return 'not found';
            }
        """)
        print("Productivity tag clicked")
    
    print("\nPH form ready for final review")
    await p.stop()

asyncio.run(main())
