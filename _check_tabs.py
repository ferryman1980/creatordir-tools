from playwright.sync_api import sync_playwright
p = sync_playwright().start()
edge = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
ctx = edge.contexts[0]
for i, page in enumerate(ctx.pages):
    print('Tab %d: %s' % (i, page.url))
p.stop()
