import websocket, json, time

WS_URL = "ws://127.0.0.1:9222/devtools/browser/340155de-0932-401d-b1d0-e8953fbbd27a"
SUBMIT_TARGET = "C9D192BAE7C7F3E68A4FD134AD2A145A"

ws = websocket.create_connection(WS_URL, timeout=10,
    header={"Origin": "http://127.0.0.1:9222"})
ws.settimeout(10)

def cmd(method, params=None, session_id=None, timeout=15):
    mid = int(time.time() * 1000) % 100000
    c = {"id": mid, "method": method}
    if params: c["params"] = params
    if session_id: c["sessionId"] = session_id
    ws.send(json.dumps(c))
    end = time.time() + timeout
    while time.time() < end:
        r = json.loads(ws.recv())
        if r.get("id") == mid and "result" in r:
            return r["result"]
    raise TimeoutError(f"Command {method} timed out")

def eval_js(js, sid):
    r = cmd("Runtime.evaluate", {"expression": js, "returnByValue": True}, sid)
    return r.get("result", {}).get("value")

print("=== Futurepedia.io Submit Automation ===")

sid = cmd("Target.attachToTarget", {"targetId": SUBMIT_TARGET, "flatten": True})["sessionId"]
print(f"Session: {sid}")

# Navigate and wait
cmd("Page.navigate", {"url": "https://futurepedia.io/submit-tool"}, sid)
print("Navigated, waiting for page...")
time.sleep(5)

# Resume from debugger
try:
    cmd("Runtime.runIfWaitingForDebugger", {}, sid)
except:
    pass

title = eval_js("document.title", sid)
print(f"Title: {title}")

# Get all input fields
inputs = eval_js("""
(function(){
    var fields = {};
    document.querySelectorAll("input, textarea, select").forEach(function(el){
        var name = el.name || el.id || el.placeholder || "unknown";
        var type = el.type || el.tagName.toLowerCase();
        fields[name] = {type: type, placeholder: el.placeholder || ""};
    });
    return JSON.stringify(fields);
})()
""", sid)
print(f"Form fields: {inputs[:1000] if inputs else 'none'}")

ws.close()
print("Done!")

# Get all buttons and their text
btns = eval_js("""
(function(){
    var btns = [];
    document.querySelectorAll("button, a[href]").forEach(function(el){
        btns.push({
            text: (el.textContent || "").trim().substring(0, 50),
            href: el.href || "",
            tag: el.tagName
        });
    });
    return JSON.stringify(btns);
})()
""", sid)
print(f"Buttons: {btns[:2000] if btns else 'none'}")

# Get full visible text
text = eval_js("document.body.innerText.substring(0, 3000)", sid)
if text:
    print("\nPAGE TEXT:")
    print(text)
