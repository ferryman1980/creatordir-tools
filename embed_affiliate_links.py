#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, glob
from bs4 import BeautifulSoup, NavigableString, Tag

TOOL_CONFIG = {
    "ChatGPT":    {"url": "https://chat.openai.com",                           "nofollow": True},
    "Claude":     {"url": "https://claude.ai",                                "nofollow": True},
    "Midjourney": {"url": "https://midjourney.com",                           "nofollow": True},
    "Canva":      {"url": "https://canva.com",                                "nofollow": True},
    "Grammarly":  {"url": "https://grammarly.com",                            "nofollow": True},
    "Semrush":    {"url": "https://semrush.com",                              "nofollow": True},
    "CapCut":     {"url": "https://capcut.com",                               "nofollow": True},
    "Jasper":     {"url": "https://jasper.ai",                                "nofollow": True},
    "Runway":     {"url": "https://runwayml.com",                             "nofollow": True},
    "Suno":       {"url": "https://suno.ai",                                  "nofollow": True},
    "Notion":     {"url": "https://notion.so",                                "nofollow": True},
    "Descript":   {"url": "https://descript.com",                             "nofollow": True},
    "ElevenLabs": {"url": "https://try.elevenlabs.io/ebksqtv6a5m6",           "nofollow": True},
    "Hostinger":  {"url": "https://www.hostinger.com?REFERRALCODE=ECA346010F8J", "nofollow": True},
}

TOOL_NAMES = sorted(TOOL_CONFIG.keys(), key=len, reverse=True)
TOOL_PATTERNS = {n: re.compile(re.escape(n), re.IGNORECASE) for n in TOOL_NAMES}

def _get_soup(node):
    while node.parent:
        node = node.parent
    return node

def _inside_a(node):
    p = node.parent
    while p:
        if isinstance(p, Tag) and p.name == "a":
            return True
        p = p.parent
    return False

def _replace(text_node, tname, url, nofollow):
    p = TOOL_PATTERNS[tname]
    orig = str(text_node)
    m = p.search(orig)
    if not m:
        return False
    s, e = m.start(), m.end()
    before, matched, after = orig[:s], orig[s:e], orig[e:]
    soup = _get_soup(text_node)
    a_tag = soup.new_tag("a", href=url, target="_blank")
    if nofollow:
        a_tag["rel"] = "nofollow"
    a_tag.string = matched
    nodes = []
    if before:
        nodes.append(NavigableString(before))
    nodes.append(a_tag)
    if after:
        nodes.append(NavigableString(after))
    parent = text_node.parent
    kids = list(parent.children)
    idx = kids.index(text_node)
    text_node.extract()
    for i, nd in enumerate(nodes):
        parent.insert(idx + i, nd)
    return True

def process(fp):
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("body") or soup
    mod = False
    added = 0
    tools = []
    for tn in TOOL_NAMES:
        pat = TOOL_PATTERNS[tn]
        url = TOOL_CONFIG[tn]["url"]
        nf = TOOL_CONFIG[tn]["nofollow"]
        for node in body.find_all(string=True):
            if node.parent.name in ("script", "style"):
                continue
            if _inside_a(node):
                continue
            if pat.search(str(node)):
                if _replace(node, tn, url, nf):
                    mod = True
                    added += 1
                    tools.append(tn)
                break
    if mod:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(str(soup))
    return mod, added, tools

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(base, "articles", "*.html")))
    print("=" * 50)
    print("  Embedding Affiliate Links into Articles")
    print("=" * 50)
    print("")
    print(f"Found {len(files)} HTML files to process")
    print("")
    tm, tl, ta = 0, 0, {}
    for i, fp in enumerate(files, 1):
        fn = os.path.basename(fp)
        mod, added, tools = process(fp)
        if mod:
            tm += 1
            tl += added
            for t in tools:
                ta[t] = ta.get(t, 0) + 1
            tstr = ", ".join(tools)
            print(f"  [+] File {i:3d}/{len(files)}: {fn}")
            print(f"      Links added: {added} ({tstr})")
        else:
            if i <= 3 or i >= len(files)-2:
                print(f"  [-] File {i:3d}/{len(files)}: {fn} (no changes)")
            elif i == 4:
                print(f"  [...] (skipping middle files for brevity)")
    print("")
    print("=" * 50)
    print("  FINAL SUMMARY")
    print("=" * 50)
    print(f"  Articles modified:  {tm} / {len(files)}")
    print(f"  Total links added:  {tl}")
    print("")
    print("  Per-tool breakdown:")
    for tn in TOOL_NAMES:
        c = ta.get(tn, 0)
        if c > 0:
            print(f"    {tn:20s} -> {c:3d} links")
        else:
            print(f"    {tn:20s} -> {c:3d} links (not found)")
    print("=" * 50)

if __name__ == "__main__":
    main()