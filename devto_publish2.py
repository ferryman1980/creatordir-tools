import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    devto = await ctx.new_page()
    await devto.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(3)
    print("URL:", devto.url)
    with open("D:\\项目\\工作区\\工作5\\promo_articles\\devto-building-240-ai-directory.md", "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    title = ""
    body_lines = []
    in_body = False
    for line in lines:
        if line.startswith("title: "):
            title = line.split(chr(34))[1]
        elif line.strip() == "---":
            in_body = not in_body
        elif not in_body:
            continue
        else:
            body_lines.append(line)
    body = "\n".join(body_lines)
    print("Title:", title)
    tf = await devto.query_selector("#article-form-title")
    if tf:
        await tf.fill(title)
        print("Title filled")
    bf = await devto.query_selector("#article_body_markdown")
    if bf:
        await bf.fill(body)
        print("Body filled")
    tagf = await devto.query_selector("#tag-input")
    if tagf:
        await tagf.fill("ai, productivity, webdev")
        print("Tags filled")
    await asyncio.sleep(2)
    result = await devto.evaluate("""() => {
        const btns = document.querySelectorAll("button");
        for (const btn of btns) {
            if (btn.textContent.trim() === "\\u53d1\\u5e03") {
                btn.dispatchEvent(new MouseEvent("click", {bubbles: true, cancelable: true}));
                return "Clicked publish";
            }
        }
        return "Not found";
    }""")
    print("Publish:", result)
    await asyncio.sleep(5)
    print("Final URL:", devto.url)
    await p.stop()
asyncio.run(main())