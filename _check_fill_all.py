
import asyncio, sys, re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def check_and_fill():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        
        # Get the newest pages (ignore old zhihu ones)
        all_pages = context.pages
        print(f"Total pages: {len(all_pages)}")
        
        for page in all_pages:
            try:
                url = page.url
                await page.wait_for_timeout(1000)
                html = await page.content()
                
                inputs = len(re.findall(r'<input[^>]*', html))
                textareas = len(re.findall(r'<textarea[^>]*', html, re.I))
                buttons = len(re.findall(r'<button[^>]*', html, re.I))
                forms_count = len(re.findall(r'<form[^>]*', html, re.I))
                
                title = ""
                try: title = await page.title()
                except: pass
                
                print(f"\n{page.url[:70]}")
                print(f"  Title: {title[:40]}")
                print(f"  Forms: {forms_count}, Inputs: {inputs}, Textareas: {textareas}, Buttons: {buttons}")
                
                # For pages with forms, try to find visible inputs
                if forms_count > 0 and inputs > 0:
                    visible = await page.evaluate("""
                        () => {
                            const els = document.querySelectorAll("input:not([type=hidden]):not([type=checkbox]):not([type=radio]), textarea");
                            return Array.from(els).filter(el => el.offsetParent !== null).map(el => ({
                                tag: el.tagName,
                                type: el.type,
                                name: el.name,
                                placeholder: el.placeholder,
                                id: el.id
                            }));
                        }
                    """)
                    if visible:
                        for v in visible:
                            print(f"    {v['tag']}: name={v['name'][:20]}, ph={v['placeholder'][:20]}")
                            
                            # Fill it!
                            combined = (v["name"] + " " + v["id"] + " " + v["placeholder"]).lower()
                            try:
                                handle = await page.query_selector(f"#{v['id']}, [name='{v['name']}'], input[placeholder='{v['placeholder']}']")
                                if not handle:
                                    handle = await page.query_selector(f"input:visible, textarea:visible")
                                
                                if handle:
                                    if "name" in combined or "title" in combined:
                                        await handle.fill("CreatorAI Tools")
                                        print(f"      FILLED: CreatorAI Tools")
                                    elif "url" in combined or "website" in combined or "link" in combined:
                                        await handle.fill("https://creatordir-tools.vercel.app")
                                        print(f"      FILLED: URL")
                                    elif "desc" in combined or "about" in combined:
                                        await handle.fill("Curated directory of 200+ AI tools for content creators")
                                        print(f"      FILLED: Description")
                                    elif "email" in combined:
                                        await handle.fill("346010735@qq.com")
                                        print(f"      FILLED: Email")
                            except Exception as e:
                                print(f"      Fill error: {str(e)[:30]}")
                    
                    # Find submit buttons  
                    submit_btns = await page.evaluate("""
                        () => {
                            const btns = Array.from(document.querySelectorAll("button, input[type=submit]"));
                            return btns.filter(b => b.offsetParent !== null)
                                .map(b => ({text: (b.innerText || b.value || "").trim().substring(0, 25)}));
                        }
                    """)
                    for sb in submit_btns:
                        if any(w in sb["text"].lower() for w in ["submit","add","list","send","create"]):
                            print(f"    SUBMIT: {sb['text']}")
                
            except Exception as e:
                print(f"  Error: {str(e)[:40]}")
        
        await browser.close()
        print("\n=== Done ===")

asyncio.run(check_and_fill())
