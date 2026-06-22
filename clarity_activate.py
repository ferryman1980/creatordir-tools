import websocket, json, time

WS_URL = "ws://127.0.0.1:9222/devtools/browser/340155de-0932-401d-b1d0-e8953fbbd27a"
ws = websocket.create_connection(WS_URL, timeout=10)
ws.settimeout(15)

# Get and attach to Clarity
ws.send(json.dumps({"id": 1, "method": "Target.getTargets"}))
resp = json.loads(ws.recv())
pages = [t for t in resp["result"]["targetInfos"] if t["type"] == "page"]
clarity = [p for p in pages if "clarity" in p["url"].lower()][0]

ws.send(json.dumps({"id": 2, "method": "Target.attachToTarget", "params": {"targetId": clarity["targetId"], "flatten": True}}))
while True:
    r = json.loads(ws.recv())
    if r.get("id") == 2:
        sid = r["result"]["sessionId"]
        break

time.sleep(2)

# Try clicking "我安装了代码" button by finding it
ws.send(json.dumps({"id": 3, "method": "Runtime.evaluate", "params": {"expression": """
(function() {
    var btns = Array.from(document.querySelectorAll("button"));
    for (var b of btns) {
        if (b.textContent.includes("代码") || b.textContent.includes("installed") || b.textContent.includes("Code")) {
            b.click();
            return "Clicked: " + b.textContent.trim().substring(0, 30);
        }
    }
    return "No matching button";
})()
""", "returnByValue": True}, "sessionId": sid}))
time.sleep(3)

# Get the new page content
ws.send(json.dumps({"id": 4, "method": "Runtime.evaluate", "params": {"expression": "document.body.innerText.substring(0, 2000)", "returnByValue": True}, "sessionId": sid}))
for i in range(10):
    r = json.loads(ws.recv())
    if r.get("id") == 3:
        print("Click result:", r.get("result",{}).get("result",{}).get("value",""))
    if r.get("id") == 4:
        print("Page:", r.get("result",{}).get("result",{}).get("value","")[:1000])

# Also try clicking Dashboard sidebar link
ws.send(json.dumps({"id": 5, "method": "Runtime.evaluate", "params": {"expression": """
(function() {
    var links = Array.from(document.querySelectorAll("a"));
    for (var l of links) {
        if (l.textContent.includes("仪表板") || l.textContent.includes("Dashboard")) {
            l.click();
            return "Clicked dashboard";
        }
    }
    return "No dashboard link";
})()
""", "returnByValue": True}, "sessionId": sid}))
time.sleep(4)

ws.send(json.dumps({"id": 6, "method": "Runtime.evaluate", "params": {"expression": "window.location.href", "returnByValue": True}, "sessionId": sid}))
for i in range(10):
    r = json.loads(ws.recv())
    if r.get("id") == 5: print("Nav result:", r.get("result",{}).get("result",{}).get("value",""))
    if r.get("id") == 6: print("Current URL:", r.get("result",{}).get("result",{}).get("value",""))

ws.close()
