import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    
    # Find PH tab, or create new one
    ph = None
    for tab in ctx.pages:
        if "/posts/new" in tab.url or "/submission" in tab.url:
            ph = tab
            break
    if not ph:
        ph = await ctx.new_page()
    
    # Go back to /posts/new to restart
    await ph.goto("https://www.producthunt.com/posts/new", wait_until="domcontentloaded", timeout=15000)
    await ph.wait_for_timeout(2000)
    print(f"PH: {await ph.title()}")
    
    # Fill URL using Playwright fill (triggers React events properly)
    inputs = await ph.query_selector_all("input")
    for inp in inputs:
        ph_text = await inp.get_attribute("placeholder") or ""
        if "www." in ph_text or "producthunt" in ph_text:
            await inp.fill("https://creatordir-tools.vercel.app")
            print("URL filled")
            break
    
    await ph.wait_for_timeout(1000)
    
    # Click Start
    btns = await ph.query_selector_all("button")
    for btn in btns:
        t = await btn.text_content()
        if t.strip() == "开始" or t.strip() == "Start":
            await btn.click()
            print("Start clicked")
            break
    
    await ph.wait_for_timeout(3000)
    print(f"Submission URL: {ph.url[:80]}")
    
    # Now we should be on /submission page - fill using Playwright fill
    # Find all inputs and fill by placeholder
    all_inputs = await ph.query_selector_all("input")
    for inp in all_inputs:
        ph_text = (await inp.get_attribute("placeholder") or "").lower()
        try:
            if "name" in ph_text or "发射名称" in ph_text:
                await inp.fill("CreatorDir - AI Tools Directory")
                print("Name filled")
            elif "tagline" in ph_text or "标语" in ph_text:
                await inp.fill("500+ free AI tools directory for creators, marketers and developers")
                print("Tagline filled")
            elif "x.com" in ph_text or "twitter" in ph_text or "记载" in ph_text:
                await inp.fill("ferryman1980")
                print("Twitter filled")
        except:
            pass
    
    # Fill textareas
    all_tas = await ph.query_selector_all("textarea")
    for ta in all_tas:
        ph_text = (await ta.get_attribute("placeholder") or "").lower()
        try:
            if "describe" in ph_text or "描述" in ph_text or "新颖" in ph_text:
                await ta.fill("A completely free directory of 500+ AI tools for content creation, marketing, video, design and productivity. Features 260+ in-depth comparison articles, 217 tool detail pages, and search with category filters across 16 categories. Open source on GitHub.")
                print("Description filled")
            elif "comment" in ph_text or "评论" in ph_text or "motivate" in ph_text:
                await ta.fill("I built CreatorDir as a completely free resource for anyone looking for the best AI tools. 500+ tools curated across 16 categories with real comparisons. Check it out!")
                print("Comment filled")
        except:
            pass
    
    await ph.wait_for_timeout(1000)
    
    # Check validation
    page_text = await ph.evaluate("document.body.innerText")
    if "需命名" in page_text or "标语是必需的" in page_text or "发射标签" in page_text:
        print("Validation errors still present - checking value state...")
        
        # Check what values actually made it
        check = await ph.evaluate("""
            () => {
                const inputs = document.querySelectorAll("input, textarea");
                return Array.from(inputs).filter(i => i.value.length > 0).map(i => ({
                    ph: (i.placeholder || "?").slice(0, 20),
                    val: i.value.slice(0, 40)
                }));
            }
        """)
        for c in check:
            print(f"  [{c['ph']}] = {c['val']}")
    
    # Try to select tags
    await ph.wait_for_timeout(1000)
    await ph.evaluate("window.scrollTo(0, 500)")
    await ph.wait_for_timeout(500)
    
    # Click on tag input
    tag_inputs = await ph.query_selector_all("input")
    for inp in tag_inputs:
        ph_text = (await inp.get_attribute("placeholder") or "").lower()
        if "tag" in ph_text or "标签" in ph_text:
            await inp.click()
            print("Clicked tag input")
            break
    
    await ph.wait_for_timeout(1500)
    
    # Click AI tag
    tags = await ph.query_selector_all("span, div, [role='option']")
    for tag in tags:
        t = await tag.text_content()
        if t.strip() == "AI":
            await tag.click()
            print("AI tag selected")
            break
    
    await ph.wait_for_timeout(500)
    
    for tag in tags:
        t = await tag.text_content()
        if t.strip() == "Productivity":
            await tag.click()
            print("Productivity tag selected")
            break
    
    # Upload screenshot
    file_input = await ph.query_selector("input[type='file']")
    if file_input:
        await file_input.set_input_files("D:\\项目\\工作区\\工作5\\ph_screenshot.png")
        print("Screenshot uploaded")
    
    print("\nForm ready for submit! Check validation.")
    
    await p.stop()

asyncio.run(main())
