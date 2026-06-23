import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = edge.contexts[0]
    pg = ctx.pages[0]
    await pg.goto("https://www.reddit.com/register/", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(5)
    
    # Try to find any input elements including shadow DOM
    html = await pg.content()
    # Check if email input exists
    email_input = await pg.locator('input[name="email"]').count()
    print(f"Email inputs by name: {email_input}")
    
    by_type = await pg.locator('input[type="email"]').count()
    print(f"Email inputs by type: {by_type}")
    
    all_inputs = await pg.locator('input').count()
    print(f"Total inputs: {all_inputs}")
    
    # Try to get the full page HTML for inputs
    input_info = await pg.evaluate("""() => {
        const inputs = document.querySelectorAll("input");
        return Array.from(inputs).map(i => ({
            type: i.type,
            name: i.name,
            id: i.id,
            placeholder: i.placeholder,
            outerHTML: i.outerHTML.substring(0,200)
        }));
    }""")
    print("\nAll input elements:")
    for inp in input_info:
        print(f"  type={inp['type']} name={inp['name']} id={inp['id']} ph={inp['placeholder']}")
        print(f"  HTML: {inp['outerHTML']}")
    
    await p.stop()

asyncio.run(main())
