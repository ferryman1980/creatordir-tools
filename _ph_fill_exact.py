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
        print("no tab")
        await p.stop()
        return
    
    await ph.bring_to_front()
    
    # 1. Fill Name
    await ph.fill('input[name="name"]', "CreatorDir - AI Tools Directory")
    print("Name filled")
    
    # 2. Fill Twitter
    await ph.fill('input[name="productTwitterHandle"]', "ferryman1980")
    print("Twitter filled")
    
    # 3. Fill Comment
    await ph.fill('textarea[name="commentBody"]', "I built CreatorDir as a completely free resource for anyone looking for the best AI tools. 500+ tools curated across 16 categories with real comparisons. Check it out!")
    print("Comment filled")
    
    # 4. Add GitHub link via additionalLinks
    # First click "+ 添加更多链接" button
    try:
        add_link_btn = await ph.query_selector('button:has-text("添加更多链接")')
        if add_link_btn:
            await add_link_btn.click()
            print("Add link clicked")
            await ph.wait_for_timeout(1000)
            # Fill GitHub URL
            github_inputs = await ph.query_selector_all('input[placeholder="https://"]')
            for gi in github_inputs:
                await gi.fill("https://github.com/ferryman1980/creatordir-tools")
                print("GitHub link added")
                break
    except:
        print("Add link not needed")
    
    # 5. Select tags - click tag input
    tag_input = await ph.query_selector('input[name="topics"]')
    if tag_input:
        await tag_input.click()
        print("Tag input clicked")
        await ph.wait_for_timeout(1500)
        
        # Click AI tag
        all_spans = await ph.query_selector_all("span, div")
        for span in all_spans:
            t = await span.text_content()
            if t.strip() == "AI":
                await span.click()
                print("AI tag selected")
                break
        
        await ph.wait_for_timeout(500)
        
        # Click Productivity tag
        for span in await ph.query_selector_all("span, div"):
            t = await span.text_content()
            if t.strip() == "Productivity":
                await span.click()
                print("Productivity tag selected")
                break
    
    await ph.wait_for_timeout(500)
    
    # Check validation
    page_text = await ph.evaluate("document.body.innerText")
    if "需命名" in page_text:
        print("WARN: Name still required")
    if "标语" in page_text and "必需" in page_text:
        print("WARN: Tagline still required")
    if "标签要求" in page_text:
        print("WARN: Tags still required")
    if "源代码" in page_text or "GitHub" in page_text or "repository" in page_text.lower():
        print("WARN: GitHub link required")
    
    # Check current values
    vals = await ph.evaluate("""
        () => {
            const inputs = document.querySelectorAll("input, textarea");
            return Array.from(inputs).filter(i => i.value.length > 0 && i.name.length > 0).map(i => i.name + "=" + i.value.slice(0, 30));
        }
    """)
    print(f"\nCurrent values: {vals}")
    
    # Check for validation errors in buttons
    btns = await ph.evaluate("""
        () => Array.from(document.querySelectorAll("button")).map(b => b.textContent.trim()).filter(t => t.length > 0 && t.length < 40 && !t.includes("LLMs") && !t.includes("Productivity") && !t.includes("Marketing") && !t.includes("Design") && !t.includes("Social") && !t.includes("Finance") && !t.includes("AI") && !t.includes("Engineering"))
    """)
    print(f"Action buttons: {btns}")
    
    await p.stop()

asyncio.run(main())
