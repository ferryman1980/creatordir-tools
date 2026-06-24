import asyncio, json
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    
    pages = []
    for ctx in edge.contexts:
        pages.extend(ctx.pages)
    
    print(f"Total open pages: {len(pages)}")
    for i, pg in enumerate(pages):
        url = pg.url[:120]
        print(f"  [{i}] {url}")
        if "reddit" in url.lower():
            print("      >>> Reddit page found! Checking login state...")
            try:
                is_logged = await pg.evaluate("""() => {
                    const userMenu = document.querySelector('[data-testid=\"user-menu-button\"]');
                    const loginBtn = document.querySelector('[data-testid=\"login-button\"]');
                    const userIndicator = document.querySelector("faceplate-trackingmenu") || document.querySelector("#header-user-menu");
                    return {
                        hasUserMenu: !!userMenu,
                        hasLoginBtn: !!loginBtn,
                        hasUserIndicator: !!userIndicator,
                        url: window.location.href
                    }
                }""")
                print(f"      Login state: {json.dumps(is_logged, indent=4)}")
            except Exception as e:
                print(f"      Error: {e}")
    
    await p.stop()

asyncio.run(main())
