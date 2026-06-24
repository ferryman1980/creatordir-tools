import urllib.request, json, urllib.parse, time

# Token
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXFfbF9CSEhXX3RBamdlRjUyMzAifQ.eyJzdWIiOiJ0Ml8yaDN3MXNlZ3lhIiwiZXhwIjoxNzUzODMxNTI1LCJpYXQiOjE3NTM4MzA5MjUsImp0aSI6InQyXzJoM3cxM2FvcXp2Zy5zdGFnaW5nIn0.BV5y9rDODC00IYxxgQNM_H6A8gYHGj3tMNMVuSsyRrMRYRzYhp4zEN9vW5e3r5bCk3nxPwp0MxLbLG9-z8lQ_I-7vTOJ-RpJAfk_CoO2AM_JE2OKK5E5qMREPyTv_hgV6RzLdPqBFSQh7TwxjG6uMQPcO8CnJ7pdNkZBjsQpxG9lAcgXx3VjkIJ4fNWElgY2oNX2NpVQqT3wS1QY3CSmoMRfKPH0iW0bQ0L0-WfOZ0lxVW_ETtMnbSk11OLCCsd2xFsY96tFnQ1SnJ7Yz5CQiHwsNi5n5tmm-vZnrKwnZQZgDNpMhl4_8IYKrz4nZ02MGZ2wAB0D-GN7-4V91Mozzt5tuFQ"

# Check token
req = urllib.request.Request("https://oauth.reddit.com/api/v1/me", headers={"Authorization": "Bearer " + token})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    me = json.loads(resp.read())
    print("Token valid! User: " + me.get("name", "?"))
except Exception as e:
    print("Token invalid: " + str(e))
    exit()

# Test post
data = urllib.parse.urlencode({
    "api_type": "json", "kind": "self", "sr": "test",
    "title": "test_" + str(int(time.time())),
    "text": "test", "sendreplies": "false"
}).encode()

post_req = urllib.request.Request(
    "https://oauth.reddit.com/api/submit",
    data=data,
    headers={"Authorization": "Bearer " + token, "Content-Type": "application/x-www-form-urlencoded"}
)
try:
    post_resp = urllib.request.urlopen(post_req, timeout=10)
    result = json.loads(post_resp.read())
    errors = result.get("json", {}).get("errors", [])
    print("Rate limit: " + ("OK" if not errors else str(errors)))
except Exception as e:
    print("Test post failed: " + str(e))
    exit()

if errors:
    print("Rate limited, exiting")
    exit()

# Post to subreddits (without links)
for sr in ["SideProject", "SaaS", "microsaas", "webdev"]:
    post_data = urllib.parse.urlencode({
        "api_type": "json", "kind": "self", "sr": sr,
        "title": "What AI tools are you actually using daily in 2026?",
        "text": "I have been testing different AI tools for content creation, coding, and design. Would love to hear what tools people are actually finding useful. Personally using ChatGPT for brainstorming and Canva for design work. What about you?",
        "sendreplies": "true"
    }).encode()
    
    try:
        pr = urllib.request.Request(
            "https://oauth.reddit.com/api/submit",
            data=post_data,
            headers={"Authorization": "Bearer " + token, "Content-Type": "application/x-www-form-urlencoded"}
        )
        pr_resp = urllib.request.urlopen(pr, timeout=10)
        pr_result = json.loads(pr_resp.read())
        pr_errors = pr_result.get("json", {}).get("errors", [])
        if pr_errors:
            print("  [" + sr + "] " + str(pr_errors))
        else:
            url = pr_result.get("json", {}).get("data", {}).get("url", "?")
            print("  [" + sr + "] POSTED: " + url)
    except Exception as e:
        print("  [" + sr + "] ERROR: " + str(e))
    
    time.sleep(7)

print("\n=== ALL DONE ===")
