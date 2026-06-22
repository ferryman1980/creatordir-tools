import asyncio, json, websockets

async def cdp_command(ws, method, params=None, session_id=None, timeout=30):
    msg_id = int(__import__("time").time() * 1000) % 100000
    cmd = {"id": msg_id, "method": method}
    if params: cmd["params"] = params
    if session_id: cmd["sessionId"] = session_id
    await ws.send(json.dumps(cmd))
    while True:
        resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=timeout))
        if resp.get("id") == msg_id and "result" in resp:
            return resp["result"]

async def main():
    async with websockets.connect("ws://127.0.0.1:9222/devtools/browser/cc06499e-afb5-4ebd-b581-4b44b182d62c") as ws:
        targets = (await cdp_command(ws, "Target.getTargets"))["targetInfos"]
        pages = [t for t in targets if t["type"] == "page"]
        tid = next(p["targetId"] for p in pages if "submit" in p["url"].lower())
        
        sid = (await cdp_command(ws, "Target.attachToTarget", {"targetId": tid, "flatten": True}))["sessionId"]
        print(f"SID: {sid}")
        
        # Resume from any debugger pause
        await cdp_command(ws, "Runtime.runIfWaitingForDebugger", {}, sid)
        print("Resumed")
        
        # Simple eval - no Page.enable needed
        result = await cdp_command(ws, "Runtime.evaluate", {
            "expression": "document.title + ' | ' + window.location.href",
            "returnByValue": True
        }, sid)
        print("Result:", result.get("result", {}).get("value", "N/A"))

asyncio.run(main())
