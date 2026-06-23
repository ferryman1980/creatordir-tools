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
    # Read article
    with open("D:\\项目\\工作区\\工作5\\promo_articles\\best-free-ai-tools-small-business-2026.md", "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    title = lines[0].replace("# ", "").strip()
    body = "\n".join(lines[2:])
    print(f"Title: {title}")
    print(f"Body: {len(body)} chars")
    # Fill title
    tf = await devto.query_selector("#article-form-title")
    if tf:
        await tf.click()
        await tf.fill(title)
        print("Title filled OK")
    # Fill body
    bf = await devto.query_selector("#article_body_markdown")
    if bf:
        await bf.click()
        await bf.fill(body)
        print("Body filled OK")
    # Tags
    tagf = await devto.query_selector("#tag-input")
    if tagf:
        await tagf.click()
        await tagf.fill("ai, smallbusiness, productivity, 2026")
        print("Tags filled OK")
    await devto.wait_for_timeout(2000)
    # List buttons for publish
    btns = await devto.evaluate("""() => {
        const bs = document.querySelectorAll("button");
        return Array.from(bs).map(b => ({text: b.textContent.trim(), type: b.type, cls: (b.className || "").substring(0,40)}));
    }""")
    print("\nButtons:")
    for b in btns:
        print(f"  [{b['text']}]")
    await p.stop()

asyncio.run(main())
