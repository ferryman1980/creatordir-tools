import asyncio, json, websockets, urllib.request

async def main():
    # Get page targets from HTTP endpoint
    resp = urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=5)
    pages = json.loads(resp.read())
    print(f"Pages: {len(pages)}")
    for p in pages:
        url = p.get("url", "?")[:80]
        title = p.get("title", "?")[:40]
        ws_url = p.get("webSocketDebuggerUrl", "")
        has_ws = "ws://" in ws_url
        print(f"  {title:40s} | {url} | WS:{has_ws}")
    
    if not pages:
        print("No pages!")
        return
    
    # Use the first page's websocket URL
    page_ws = pages[0].get("webSocketDebuggerUrl", "")
    if not page_ws:
        print("No WebSocket URL for first page")
        return
    
    print(f"\nConnecting to page WebSocket...")
    async with websockets.connect(page_ws) as ws:
        print("Connected to page")
        
        # Navigate to GitHub
        nav_msg = {
            "id": 1,
            "method": "Page.navigate",
            "params": {"url": "https://github.com/ferryman1980/creatordir-tools/"}
        }
        await ws.send(json.dumps(nav_msg))
        
        # Wait for response
        async for msg in ws:
            data = json.loads(msg)
            if data.get("id") == 1:
                print(f"Navigation: {data.get('result', {})}")
                break
        
        # Wait a bit for page to load
        await asyncio.sleep(3)
        
        # Get current URL
        eval_msg = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": "window.location.href"}
        }
        await ws.send(json.dumps(eval_msg))
        async for msg in ws:
            data = json.loads(msg)
            if data.get("id") == 2:
                url = data.get("result", {}).get("result", {}).get("value", "?")
                print(f"Current URL: {url}")
                break

asyncio.run(main())
