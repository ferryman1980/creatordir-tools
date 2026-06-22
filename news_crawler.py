#!/usr/bin/env python3
# AI News Crawler - fetches from Reddit, HackerNews, RSS feeds
import os, json, requests, re, time, sys, io, html as htmlmod
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"D:\\项目\\工作区\\工作5"
os.chdir(BASE)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
LOG = os.path.join(BASE, "_news_crawl_log.txt")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + chr(10))

def clean(s): return htmlmod.unescape(re.sub(r'<[^>]+>', '', s)).strip()

log('='*50)
log('AI NEWS CRAWLER STARTED')
all_news = []
seen_urls = set()

log('--- Reddit r/artificial ---')
try:
    r = requests.get('https://www.reddit.com/r/artificial/hot.json?limit=15', headers={'User-Agent': UA+' (by /u/crawler)'}, timeout=15)
    if r.status_code == 200:
        for post in r.json()['data']['children']:
            data = post['data']
            title = data.get('title','')
            url = data.get('url','')
            if url and url not in seen_urls:
                seen_urls.add(url)
                permalink = 'https://www.reddit.com' + data.get('permalink','')
                all_news.append({
                    'title': title[:200],
                    'url': url,
                    'summary': (data.get('selftext','') or title)[:300],
                    'date': datetime.fromtimestamp(data.get('created_utc',0)).strftime('%b %d, %Y') if data.get('created_utc') else '','cat':'Industry','source':'Reddit r/artificial','source_url': permalink,'score': data.get('score',0)
                })
        log(f'  Got {len(r.json()["data"]["children"])} posts')
except Exception as e: log(f'  Reddit error: {e}')

log('--- Hacker News AI ---')
try:
    r = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=15)
    if r.status_code == 200:
        count = 0
        for sid in r.json()[:50]:
            try:
                ri = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json', headers={'User-Agent': UA}, timeout=10)
                if ri.status_code == 200:
                    item = ri.json()
                    title = item.get('title','')
                    url = item.get('url','')
                    if any(kw in title.lower() for kw in ['ai','gpt','chatgpt','llm','machine learning','deep learning','neural','openai','claude','gemini','copilot','llama','mistral','diffusion','transformer']):
                        if url and url not in seen_urls:
                            seen_urls.add(url)
                            hn_url = url or ('https://news.ycombinator.com/item?id=' + str(item.get('id','')))
                            all_news.append({
                                'title': title[:200],
                                'url': hn_url,
                                'summary': title[:300],
                                'date': datetime.fromtimestamp(item.get('time',0)).strftime('%b %d, %Y') if item.get('time') else '','cat':'Research','source':'Hacker News','source_url':hn_url,'score': item.get('score',0)
                            })
                            count += 1
            except: pass
            time.sleep(0.05)
        log(f'  {count} AI stories')
except Exception as e: log(f'  HN error: {e}')

log('--- TechCrunch AI RSS ---')
try:
    r = requests.get('https://techcrunch.com/category/artificial-intelligence/feed/', headers={'User-Agent': UA}, timeout=15)
    if r.status_code == 200:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(r.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'content': 'http://purl.org/rss/1.0/modules/content/'}
        # Handle both RSS and Atom
        items = root.findall('.//item') or root.findall('.//atom:entry', ns)
        count = 0
        for item in items[:12]:
            title = clean(item.findtext('title','') or '')
            link = (item.findtext('link','') or (item.find('link').get('href','') if item.find('link') is not None else ''))
            desc = clean(item.findtext('description','') or item.findtext('summary','') or '')
            pubdate = item.findtext('pubDate','') or item.findtext('published','') or ''
            if link and link not in seen_urls and title:
                seen_urls.add(link)
                try: d = datetime.strptime(pubdate[:25], '%a, %d %b %Y %H:%M:%S')
                except: d = datetime.now()
                all_news.append({'title':title[:200],'url':link,'summary':desc[:300],
                    'date':d.strftime('%b %d, %Y'),'cat':'Launches','source':'TechCrunch','source_url':link,'score':0})
                count += 1
        log(f'  {count} articles')
except Exception as e: log(f'  TC error: {e}')

log('--- VentureBeat AI RSS ---')
try:
    r = requests.get('https://venturebeat.com/category/ai/feed/', headers={'User-Agent': UA}, timeout=15)
    if r.status_code == 200:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(r.content)
        count = 0
        for item in root.findall('.//item')[:10]:
            title = clean(item.findtext('title','') or '')
            link = item.findtext('link','') or ''
            desc = clean(item.findtext('description','') or '')
            pubdate = item.findtext('pubDate','') or ''
            if link and link not in seen_urls and title:
                seen_urls.add(link)
                try: d = datetime.strptime(pubdate[:25], '%a, %d %b %Y %H:%M:%S')
                except: d = datetime.now()
                all_news.append({'title':title[:200],'url':link,'summary':desc[:300],'date':d.strftime('%b %d, %Y'),'cat':'Industry','source':'VentureBeat','source_url':link,'score':0})
                count += 1
        log(f'  {count} articles')
except Exception as e: log(f'  VB error: {e}')

log(f'Total news: {len(all_news)} items')
output = {'generated':datetime.now().isoformat(),'total':len(all_news),'data':all_news}
with open(os.path.join(BASE, 'data', 'ai_news.json'), 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
log('Saved to data/ai_news.json')
log('AI NEWS CRAWLER FINISHED')
log('='*50)
print(f'Done! {len(all_news)} news items crawled')