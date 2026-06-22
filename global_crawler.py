#!/usr/bin/env python3
# Global Multi-Source Crawler - runs every 30 min
import os, json, requests, re, time, sys, io
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"D:\\项目\\工作区\\工作5"
os.chdir(BASE)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
LOG = os.path.join(BASE, "_crawl_log.txt")
LOCK = os.path.join(BASE, "_crawl_running.lock")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}]  {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + chr(10))
if os.path.exists(LOCK):
    log('LOCK exists - exiting')
    sys.exit(0)

try:
    with open(LOCK, 'w') as f: f.write('1')
    log('='*50)
    log('GLOBAL CRAWLER STARTED')
    
    rf = os.path.join(BASE, '_crawl_round.json')
    if os.path.exists(rf):
        with open(rf) as f: state = json.load(f)
    else:
        state = {'round': 0}
    state['round'] += 1
    rnd = state['round']
    log(f'Crawl round #{rnd}')
    all_items = []

    # Source 1: Hugging Face Spaces
    log('--- HF Spaces ---')
    try:
        r = requests.get('https://huggingface.co/api/spaces?sort=likes&direction=-1&limit=15', headers={'User-Agent': UA}, timeout=15)
        if r.status_code == 200:
            for s in r.json():
                sid = s.get('id','')
                all_items.append({'source':'huggingface','id':sid,'name':sid.split('/')[-1] if '/' in sid else sid,'url':'https://huggingface.co/spaces/'+sid,'description':(s.get('sdk','')+' space')[:300],'stars':s.get('likes',0),'topics':[s.get('sdk',''),s.get('task',{}).get('id','')],'language':s.get('sdk','Python'),'updated':datetime.now().isoformat()[:10],'homepage':'https://huggingface.co/spaces/'+sid,'license':'Apache 2.0'})
            log(f'  {len(r.json())} spaces')
    except Exception as e: log(f'  HF error: {e}')

    # Source 2: Dev.to AI articles
    log('--- Dev.to AI ---')
    try:
        r = requests.get('https://dev.to/api/articles?tag=ai&per_page=15&top=1', headers={'User-Agent': UA}, timeout=15)
        if r.status_code == 200:
            for a in r.json():
                all_items.append({'source':'devto','id':str(a.get('id','')),'name':a.get('title','')[:100],'url':a.get('url',''),'description':(a.get('description','') or a.get('title',''))[:300],'stars':a.get('positive_reactions_count',0)*10,'topics':a.get('tags','').split(',') if a.get('tags') else [],'language':'Article','updated':(a.get('published_at','') or '')[:10],'homepage':a.get('url',''),'license':''})
            log(f'  {len(r.json())} articles')
    except Exception as e: log(f'  Dev.to error: {e}')

    # Source 3: Hacker News AI
    log('--- HN AI ---')
    try:
        r = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=15)
        if r.status_code == 200:
            count = 0
            for sid in r.json()[:30]:
                try:
                    ri = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json', headers={'User-Agent': UA}, timeout=10)
                    if ri.status_code == 200:
                        item = ri.json()
                        title = item.get('title','')
                        if any(kw in title.lower() for kw in ['ai','gpt','chatgpt','llm','machine learning','deep learning','neural','openai','claude','gemini','copilot']):
                            all_items.append({'source':'hackernews','id':str(item.get('id','')),'name':title[:100],'url':item.get('url','https://news.ycombinator.com/item?id='+str(item.get('id',''))),'description':title[:300],'stars':item.get('score',0),'topics':['AI','Tech'],'language':'Article','updated':datetime.fromtimestamp(item.get('time',0)).isoformat()[:10] if item.get('time') else '','homepage':item.get('url',''),'license':''})
                            count += 1
                except: pass
                time.sleep(0.05)
            log(f'  {count} AI stories')
    except Exception as e: log(f'  HN error: {e}')

    # Source 4: GitHub (every 2nd run)
    if rnd % 2 == 1:
        log('--- GitHub AI (every 2nd) ---')
        try:
            r = requests.get('https://api.github.com/search/repositories?q=ai+tool&sort=stars&order=desc&per_page=15', headers={'User-Agent': UA}, timeout=15)
            if r.status_code == 200:
                for item in r.json().get('items',[]):
                    all_items.append({'source':'github','id':str(item.get('id','')),'name':item.get('full_name',''),'url':item.get('html_url',''),'description':(item.get('description','') or '')[:300],'stars':item.get('stargazers_count',0),'topics':item.get('topics',[]),'language':item.get('language','N/A') or 'N/A','updated':(item.get('updated_at','') or '')[:10],'homepage':item.get('homepage','') or item.get('html_url',''),'license':item.get('license',{}).get('spdx_id','') if item.get('license') else ''})
                log(f'  {len(r.json().get("items",[]))} repos')
        except Exception as e: log(f'  GitHub error: {e}')

    # Save
    output = {'generated':datetime.now().isoformat(),'round':rnd,'total':len(all_items),'data':all_items}
    with open(os.path.join(BASE, 'data', 'global_crawl.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    log(f'Saved {len(all_items)} items to data/global_crawl.json')
    with open(rf, 'w') as f: json.dump(state, f)
    log('GLOBAL CRAWLER FINISHED')
    log('='*50)

finally:
    if os.path.exists(LOCK): os.remove(LOCK)

print('Done!')