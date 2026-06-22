import glob, os, json, urllib.request
articles = len(glob.glob('articles/*.html'))
print(f'Articles: {articles}')
if os.path.exists('submission_results.json'):
    with open('submission_results.json') as f:
        s = json.load(f)
        print(f'Submissions: {json.dumps(s, indent=2)[:500]}')
else:
    print('No submission_results.json')
try:
    r = urllib.request.urlopen('https://api.github.com/repos/ferryman1980/creatordir-tools/issues', timeout=10)
    issues = json.loads(r.read())
    print(f'GitHub Issues: {len(issues)}')
    for i in issues[:5]:
        print(f'#{i['number']}: {i['title'][:60]}')
except Exception as e:
    print(f'GitHub error: {e}')