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
        print("PH tab not found")
        await p.stop()
        return
    
    await ph.bring_to_front()
    
    # Fill all form fields using native setter + React events
    await ph.evaluate("""
        () => {
            const setNativeValue = (element, value) => {
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                const nativeTextareaValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLTextAreaElement.prototype, 'value'
                ).set;
                
                if (element.tagName === 'TEXTAREA' && nativeTextareaValueSetter) {
                    nativeTextareaValueSetter.call(element, value);
                } else if (nativeInputValueSetter) {
                    nativeInputValueSetter.call(element, value);
                }
                
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
            };
            
            const inputs = document.querySelectorAll('input, textarea');
            inputs.forEach(el => {
                const ph = (el.placeholder || '').toLowerCase();
                if (ph.includes('name') || ph.includes('名称')) {
                    setNativeValue(el, 'CreatorDir - AI Tools Directory');
                }
                if (ph.includes('tagline') || ph.includes('标语')) {
                    setNativeValue(el, '500+ curated AI tools for creators, marketers and developers');
                }
                if (ph.includes('twitter') || ph.includes('x.com') || ph.includes('记载')) {
                    setNativeValue(el, 'ferryman1980');
                }
                if (ph.includes('describe') || ph.includes('描述') || ph.includes('what')) {
                    setNativeValue(el, 'A free directory of 500+ AI tools for content creation, marketing, video, design and productivity. Features 260+ comparison articles, search with filters across 16 categories, and hand-picked affiliate deals. Open source on GitHub.');
                }
            });
            
            // Also set the launch tag area
            document.querySelectorAll('[contenteditable]').forEach(el => {
                const ph = (el.getAttribute('placeholder') || '').toLowerCase();
                if (ph.includes('comment') || ph.includes('评论')) {
                    el.textContent = 'I built CreatorDir as a free resource for anyone looking for the best AI tools. 500+ tools curated across 16 categories with real comparisons. Check it out!';
                }
            });
            
            return 'done';
        }
    """)
    print("Form filled via native setter")
    
    # Check filled values
    vals = await ph.evaluate("""
        () => {
            const inputs = document.querySelectorAll('input, textarea');
            return Array.from(inputs).filter(i => i.value && i.value.length > 3).map(i => ({
                ph: (i.placeholder || '?'),
                val: i.value.slice(0, 60)
            }));
        }
    """)
    for v in vals:
        print(f"  {v['ph'][:20]}: {v['val']}")
    
    # Now try to select tags
    # Click on the tag selection area
    await ph.evaluate("""
        () => {
            const all = document.querySelectorAll('span, div, button');
            for (const el of all) {
                if (el.textContent.includes('最多选择') || el.textContent.includes('launch tag') || el.textContent.includes('发射标签')) {
                    el.parentElement?.querySelector('button')?.click();
                    return;
                }
            }
        }
    """)
    print("Clicked tags area")
    
    await p.stop()

asyncio.run(main())
