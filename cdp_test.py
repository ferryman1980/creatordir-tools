import asyncio, json
import websockets

async def cdp_send(ws, cmd_id, method, params=None):
    msg = {"id": cmd_id, "method": method}
    if params:
        msg["params"] = params
    await ws.send(json.dumps(msg))
    async for msg in ws:
        data = json.loads(msg)
        if data.get("id") == cmd_id:
            return data.get("result", {})

async def main():
    cdp_url = "ws://127.0.0.1:9222/devtools/browser/3d547708-be2e-405e-a141-f0029cfacd1c"
    async with websockets.connect(cdp_url) as ws:
        print("CDP connected")
        result = await cdp_send(ws, 1, "Target.getTargets")
        targets = result.get("targetInfo", [])
        print(f"Targets: {len(targets)}")
        for t in targets:
            title = t.get("title", "?")[:40]
            url = t.get("url", "?")[:80]
            tid = t.get("targetId", "?")[:20]
            print(f"  {title} | {url}")
        
        # Check GitHub login
        for t in targets:
            if "github.com/login" in t.get("url", ""):
                print("\nGitHub login page detected - not logged in!")
                break
            elif "github.com" in t.get("url", ""):
                print(f"\nGitHub page found: {t.get('title','?')}")
                break
        else:
            # Navigate to GitHub
            print("\nNavigating to GitHub...")
            # Activate first target and navigate
            first_target = targets[0]
            print(f"First target: {first_target.get('title','?')[:40]}")

asyncio.run(main())
