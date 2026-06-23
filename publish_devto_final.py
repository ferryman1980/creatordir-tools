import asyncio
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    devto = None
    for pg in ctx.pages:
        if "dev.to" in pg.url:
            devto = pg
            break
    if not devto:
        print("Dev.to page not found")
        return
    await devto.bring_to_front()
    await devto.wait_for_timeout(2000)
    
    # Fill title
    tf = await devto.query_selector("#article-form-title")
    if tf:
        await tf.click()
        await tf.fill("Best Free AI Tools for Small Business Owners in 2026")
        print("Title filled")
    
    # Read and fill body
    with open("D:\\项目\\工作区\\工作5\\promo_articles\\best-free-ai-tools-small-business-2026.md", "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    body = "\n".join(lines[2:])
    bf = await devto.query_selector("#article_body_markdown")
    if bf:
        await bf.click()
        await bf.fill(body)
        print("Body filled")
    
    # Tags
    tagf = await devto.query_selector("#tag-input")
    if tagf:
        await tagf.click()
        await tagf.fill("ai, smallbusiness, productivity, 2026")
        print("Tags filled")
    
    await devto.wait_for_timeout(1000)
    
    # Click publish using dispatchEvent
    result = await devto.evaluate('''() => {
        const btns = document.querySelectorAll("button");
        for (const btn of btns) {
            if (btn.textContent.trim() === "\u53d1\u5e03") {
                btn.dispatchEvent(new MouseEvent("click", {bubbles: true, cancelable: true}));
                return "Clicked \u53d1\u5e03 button";
            }
        }
        return "Publish button not found";
    }''')
    print("Publish result:", result)
    
    await devto.wait_for_timeout(5000)
    print("Final URL:", devto.url)
    print("\nDone!")
    await p.stop()

asyncio.run(main())
