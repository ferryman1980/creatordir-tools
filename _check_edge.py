import urllib.request, json
try:
    data = urllib.request.urlopen('http://127.0.0.1:9222/json/version', timeout=5).read()
    print('Edge CDP OK')
    print(json.loads(data).get('Browser','unknown'))
except Exception as e:
    print(f'Edge CDP failed: {e}')
