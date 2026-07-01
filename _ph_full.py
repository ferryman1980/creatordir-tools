import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    ph = None
    for tab in ctx.pages:
        if "producthunt.com/posts/new" in tab.url:
            ph = tab
            break
    if not ph:
        ph = await ctx.new_page()
        await ph.goto("https://www.producthunt.com/posts/new", wait_until="domcontentloaded", timeout=20000)
    
    await ph.bring_to_front()
    await ph.wait_for_timeout(2000)
    print(f"PH: {await ph.title()} | {ph.url[:80]}")
    
    page_text = await ph.evaluate("document.body.innerText")
    if "Cloudflare" in page_text or "正在" in page_text[:20]:
        print("Cloudflare blocking - waiting for manual bypass")
        await p.stop()
        return
    
    # Step 1: Fill URL and click Start
    native_setter = """
        const setVal = (el, val) => {
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            setter.call(el, val);
            el.dispatchEvent(new Event('input', {bubbles:true}));
            el.dispatchEvent(new Event('change', {bubbles:true}));
        };
    """
    
    # Fill URL
    await ph.evaluate(native_setter + """
        const inputs = document.querySelectorAll('input');
        for (const i of inputs) {
            if (i.type === 'text' && i.placeholder && (i.placeholder.includes('www.') || i.placeholder.includes('producthunt'))) {
                setVal(i, 'https://creatordir-tools.vercel.app');
                break;
            }
        }
    """)
    print("URL filled")
    await ph.wait_for_timeout(1000)
    
    # Click Start button
    await ph.evaluate("""
        const btns = document.querySelectorAll('button');
        for (const b of btns) {
            if (b.textContent.trim() === '开始' || b.textContent.trim() === 'Start') {
                b.click();
                return;
            }
        }
    """)
    print("Start clicked")
    await ph.wait_for_timeout(3000)
    
    # Check if we're on the full form
    new_text = await ph.evaluate("document.body.innerText")
    if "发射名称" in new_text or "Launch name" in new_text.lower() or "进行中" in new_text:
        # We're on the full form!
        print("Full form loaded!")
        
        # Fill Name
        await ph.evaluate(native_setter + """
            const inputs = document.querySelectorAll('input');
            for (const i of inputs) {
                const ph = (i.placeholder || '').toLowerCase();
                if (ph.includes('name') || ph.includes('发射')) {
                    setVal(i, 'CreatorDir - AI Tools Directory');
                    break;
                }
            }
        """)
        print("Name filled")
        await ph.wait_for_timeout(500)
        
        # Fill Tagline
        await ph.evaluate(native_setter + """
            const inputs = document.querySelectorAll('input');
            for (const i of inputs) {
                const ph = (i.placeholder || '').toLowerCase();
                if (ph.includes('tagline') || ph.includes('标语')) {
                    setVal(i, '500+ free AI tools directory for creators, marketers and developers');
                    break;
                }
            }
        """)
        print("Tagline filled")
        await ph.wait_for_timeout(500)
        
        # Fill Twitter
        await ph.evaluate(native_setter + """
            const inputs = document.querySelectorAll('input');
            for (const i of inputs) {
                const ph = (i.placeholder || '').toLowerCase();
                if (ph.includes('@launch') || ph.includes('twitter') || ph.includes('x.com') || ph.includes('记载')) {
                    setVal(i, 'ferryman1980');
                    break;
                }
            }
        """)
        print("Twitter filled")
        await ph.wait_for_timeout(500)
        
        # Fill Description
        await ph.evaluate("""
            const textareas = document.querySelectorAll('textarea');
            for (const ta of textareas) {
                const ph = (ta.placeholder || '').toLowerCase();
                if (ph.includes('describe') || ph.includes('描述') || ph.includes('新颖') || ph.includes('unique')) {
                    const setter = Object.getOwnPropertyDescriptor(
                        window.HTMLTextAreaElement.prototype, 'value'
                    ).set;
                    setter.call(ta, 'A completely free directory of 500+ AI tools for content creation, marketing, video production, design, and productivity. Features 260+ in-depth comparison articles, 217 tool detail pages, and search with category filters. Open source on GitHub. Every tool is curated and tested.');
                    ta.dispatchEvent(new Event('input', {bubbles:true}));
                    ta.dispatchEvent(new Event('change', {bubbles:true}));
                    break;
                }
            }
        """)
        print("Description filled")
        
        # Fill comment
        await ph.evaluate("""
            const all = document.querySelectorAll('[contenteditable], textarea');
            for (const el of all) {
                const ph = (el.getAttribute('placeholder') || '').toLowerCase();
                if (ph.includes('comment') || ph.includes('评论') || ph.includes('motivate')) {
                    if (el.tagName === 'TEXTAREA') {
                        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                        setter.call(el, 'I built CreatorDir as a free resource for anyone looking for the best AI tools. 500+ tools curated across 16 categories with real comparisons. Check it out and let me know what you think!');
                        el.dispatchEvent(new Event('input', {bubbles:true}));
                    } else {
                        el.textContent = 'I built CreatorDir as a free resource for anyone looking for the best AI tools. 500+ tools curated across 16 categories with real comparisons. Check it out!';
                    }
                    break;
                }
            }
        """)
        print("Comment filled")
        
        # Try to select tags
        await ph.evaluate("""
            const inputs = document.querySelectorAll('input');
            for (const i of inputs) {
                const ph = (i.placeholder || '').toLowerCase();
                if (ph.includes('tag') || ph.includes('标签')) {
                    i.click();
                    i.focus();
                    break;
                }
            }
        """)
        await ph.wait_for_timeout(1500)
        print("Tags area focused")
        
        # Click AI tag
        await ph.evaluate("""
            const all = document.querySelectorAll('span, div, button, [role="option"]');
            for (const el of all) {
                const t = el.textContent.trim();
                if (t === 'AI' || t === '人工智能') {
                    el.click();
                    return;
                }
            }
        """)
        print("AI tag clicked")
        await ph.wait_for_timeout(500)
        
        # Click Productivity
        await ph.evaluate("""
            const all = document.querySelectorAll('span, div, button, [role="option"]');
            for (const el of all) {
                const t = el.textContent.trim();
                if (t === 'Productivity' || t === '生产力') {
                    el.click();
                    return;
                }
            }
        """)
        print("Productivity tag clicked")
        await ph.wait_for_timeout(500)
        
        # Click Developer Tools
        await ph.evaluate("""
            const all = document.querySelectorAll('span, div, button, [role="option"]');
            for (const el of all) {
                const t = el.textContent.trim();
                if (t === 'Developer Tools' || t === '开发工具') {
                    el.click();
                    return;
                }
            }
        """)
        print("Developer Tools tag clicked")
        
        print("\n=== ALL FORM FIELDS FILLED ===")
    else:
        print(f"Form not advanced: {new_text[:200]}")
    
    await p.stop()

asyncio.run(main())
