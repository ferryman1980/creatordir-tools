
import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=10000)
            page = browser.contexts[0].pages[0]
            
            # Go to PartnerStack direct signup
            await page.goto("https://app.partnerstack.com/auth/register", timeout=20000)
            await page.wait_for_timeout(3000)
            print(f"URL: {page.url[:80]}")
            print(f"Title: {(await page.title())[:60]}")
            
            # Check all visible elements
            info = await page.evaluate("""
                () => {
                    const els = document.querySelectorAll("input, button, a");
                    return Array.from(els).filter(el => el.offsetParent !== null).map(el => ({
                        tag: el.tagName,
                        type: el.type || "",
                        name: el.name || "",
                        id: el.id || "",
                        placeholder: el.placeholder || "",
                        text: (el.innerText || el.textContent || "").trim().substring(0, 30),
                        href: el.href || ""
                    }));
                }
            """)
            
            print(f"Visible elements: {len(info)}")
            for el in info:
                if el["tag"] == "INPUT" or (el["text"] and el["text"].length > 0):
                    print(f"  {el['tag']}: {el['type']} name={el['name'][:15]} ph={el['placeholder'][:15]} text={el['text'][:20]}")
                if el["href"] and ("signup" in el["href"] or "register" in el["href"]):
                    print(f"  LINK: {el['text']} -> {el['href'][:60]}")
            
            await browser.close()
        except Exception as e:
            print(f"Error: {str(e)[:80]}")

asyncio.run(main())
