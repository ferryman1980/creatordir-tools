import websocket, json, time

WS_URL = "ws://127.0.0.1:9222/devtools/browser/340155de-0932-401d-b1d0-e8953fbbd27a"
ws = websocket.create_connection(WS_URL, timeout=10)
ws.settimeout(5)

ws.send(json.dumps({"id": 1, "method": "Target.getTargets"}))

for i in range(5):
    try:
        r = json.loads(ws.recv())
        print("[%d] id=%s method=%s" % (i, r.get("id"), r.get("method","")[:30]))
        if r.get("id") == 1:
            pages = [t for t in r["result"]["targetInfos"] if t["type"] == "page"]
            for p in pages:
                print("  PAGE: %s %s" % (p["targetId"][:20], p["url"][:80]))
            break
    except:
        print("[%d] timeout" % i)
        break

ws.close()
