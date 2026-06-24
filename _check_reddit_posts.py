import asyncio, json
from playwright.async_api import async_playwright

async def main():
    p = await async_playwright().start()
    edge = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    
    page = await edge.contexts[0].new_page()
    
    # Get token
    cookies = await page.context.cookies()
    token_v2 = None
    for c in cookies:
        if c.get("name") == "token_v2":
            token_v2 = c.get("value")
            break
    print(f"Token: {token_v2[:50] if token_v2 else 'NONE'}...")
    
    # Check if we already posted in webdev by checking user's posts
    result = await page.evaluate(f"""
        async () => {{
            try {{
                // Get my username first
                const meResp = await fetch("https://oauth.reddit.com/api/v1/me", {{
                    headers: {{ "Authorization": "Bearer {token_v2}" }}
                }});
                const me = await meResp.json();
                const username = me.name;
                
                // Get my submitted posts
                const postsResp = await fetch("https://oauth.reddit.com/user/" + username + "/submitted?limit=5", {{
                    headers: {{ "Authorization": "Bearer {token_v2}" }}
                }});
                const posts = await postsResp.json();
                
                let result = "Username: " + username + "\\n";
                if (posts.data && posts.data.children) {{
                    for (const child of posts.data.children) {{
                        const post = child.data;
                        result += `Sub: ${{post.subreddit}} | Title: ${{post.title.slice(0,60)}} | URL: ${{post.url}} | Created: ${{new Date(post.created_utc*1000).toISOString()}}\\n`;
                    }}
                }}
                return result;
            }} catch(e) {{
                return "Error: " + e.toString();
            }}
        }}
    """)
    
    print("\\n=== My Recent Posts ===")
    print(result)
    
    await page.close()
    await p.stop()

asyncio.run(main())
