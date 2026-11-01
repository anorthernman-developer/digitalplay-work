#!/usr/bin/env python3
"""Merge every section catalogue plus the Manifesto Machines catalogue into site/data/tools.json,
copy section tools into site/play/<section>/, and copy taxonomy.json into site/data/.

Sources, in order of preference:
  1. sibling folders ../digitalplay-<section> or ../<section> (local checkouts)
  2. raw.githubusercontent.com/<owner>/digitalplay-<section>/main/...
Manifesto Machines is always read from GitHub (falls back to a local checkout), never modified.
Run: python3 scripts/aggregate.py
"""
import json, os, re, shutil, sys, urllib.request
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(HUB, 'site')
OWNER = 'anorthernman-developer'
RAW = 'https://raw.githubusercontent.com/%s/%s/main/%s'
MM_PAGES = 'https://%s.github.io/manifesto-machines/' % OWNER
LIVE_SECTIONS = ['art', 'design', 'coding', 'writing']
MM_SUB = {'art manifesto': 'Art manifestos as instruments', 'music theory': 'Composition and theory', 'nature/philosophy': 'Nature and philosophy',
          'generative systems': 'Generative and ambient', 'found-sound production': 'Found sound and production'}
STANDALONE = [  # linked only if the repo exists and the live URL answers 200
    {'repo': 'emotional-frameworks-live', 'title': 'Emotional Frameworks Live', 'from': '77'},
    {'repo': 'fifty-three-cells', 'title': 'Fifty-Three Cells', 'from': '79'},
]

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': 'digitalplay-aggregate'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def status(url):
    try:
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'digitalplay-aggregate'})
        with urllib.request.urlopen(req, timeout=15) as r: return r.status
    except Exception as e:
        return getattr(e, 'code', 0)

def local_dir(sec):
    for c in ['../digitalplay-%s' % sec, '../%s' % sec]:
        p = os.path.normpath(os.path.join(HUB, c))
        if os.path.exists(os.path.join(p, 'catalogue.json')): return p
    return None

def era_from_year(y):
    y = str(y)
    if 'BC' in y: return 'ancient-traditional'
    m = re.search(r'\d{4}', y)
    if not m: return 'ancient-traditional'
    n = int(m.group())
    return 'before-1900' if n < 1900 else '1900-1945' if n <= 1945 else '1946-1979' if n <= 1979 else '1980-today'

def short_year(y):
    return re.split(r'\s*[(;]', str(y))[0].strip()

def names_in(*fields):
    toks = set()
    for f in fields:
        for w in re.findall(r"[A-ZÀ-Ý][\w'’.-]{2,}", f or ''):
            toks.add(w.strip('.'))
    return toks - {'The', 'And', 'With', 'For', 'From', 'Manifesto', 'Music', 'Foundation', 'Long', 'Now', 'Strategies', 'Oblique', 'Ensemble'}

CAT = {'art manifesto': 'art manifesto', 'music theory': 'music theory', 'nature/philosophy': 'nature/philosophy',
       'generative systems': 'generative systems', 'eno': 'generative systems',
       'found-sound production': 'found-sound production', 'fred again..': 'found-sound production', 'fred': 'found-sound production'}
GENERIC = {'generative systems': 'Generative and ambient music', 'found-sound production': 'Found-sound production methods',
           'music theory': 'Music theory', 'nature/philosophy': 'Patterns in nature and philosophy', 'art manifesto': 'An art manifesto'}
QUOTES = re.compile(r"['‘’“”\"]")
WEAK_START = re.compile(r'^(He|She|They|His|Her|Their|It|Its|This|These|That|Those|There|In \d|On \d|Born|After|Before|When|Where)\b')
OVERRIDES_FILE = os.path.join(HUB, 'data', 'music-summaries.json')

def cat_of(t):
    c = (t.get('category') or '').strip().lower()
    return CAT.get(c, 'art manifesto' if 'manifesto' in c else c)

def has_name(s, names):
    return any(re.search(r'\b%s\b' % re.escape(n), s) for n in names)

def ok_sentence(s, names):
    if not s or not s[0].isupper() or QUOTES.search(s) or WEAK_START.search(s): return False
    if len(s.split()) < 7 or has_name(s, names): return False
    return True

def all_names(t):
    return names_in(t.get('author', ''), t.get('design_homage', ''), t.get('design_short', ''))

def clean_desc(t, overrides):
    """Hub-written summary if there is one; else the first idea sentence that names nobody and quotes nothing."""
    if t['number'] in overrides: return overrides[t['number']]['summary']
    names = all_names(t)
    for s in re.split(r'(?<=[a-z0-9)][.!?])\s+', t.get('idea', '').strip()):
        if ok_sentence(s, names): return s
    return None

def inspired_source(t, overrides):
    if t['number'] in overrides and overrides[t['number']].get('inspired'): return overrides[t['number']]['inspired']
    names = all_names(t)
    for src in (t.get('source_short', ''), t.get('source', '')):
        if src and not has_name(src, names) and not QUOTES.search(src) and cat_of(t) not in ('generative systems', 'found-sound production'):
            return src
    return GENERIC.get(cat_of(t), 'A published idea')

def music_tools():
    try:
        mm = json.loads(fetch(RAW % (OWNER, 'manifesto-machines', 'catalogue.json')))
        src = 'github'
    except Exception:
        mm = json.load(open('/workspace/manifesto-machines/catalogue.json')); src = 'local'
    overrides = json.load(open(OVERRIDES_FILE)) if os.path.exists(OVERRIDES_FILE) else {}
    out, missing = [], []
    for t in mm:
        summary = clean_desc(t, overrides)
        if not summary:
            missing.append(t['number']); summary = 'A playable instrument from Manifesto Machines.'
        out.append({
            'id': 'music/' + t['file'].split('/')[-1].replace('.html', ''),
            'section': 'music', 'num': t['number'], 'title': t['title'],
            'summary': summary,
            'subcategory': MM_SUB.get(cat_of(t), 'Music'),
            'inspired': '%s (%s)' % (inspired_source(t, overrides), short_year(t.get('year', ''))),
            'skillLevel': 'deep-dive' if t.get('deep') else 'first-go',
            'input': ['your-sounds'], 'output': ['audio', 'wav'],
            'sessionLength': '30-min-plus' if t.get('deep') else '15-min',
            'ai': 'ai-optional' if t.get('gemini') else 'no-ai',
            'era': era_from_year(t.get('year', '')),
            'try': MM_PAGES + t['file'],
            'repo': 'https://github.com/%s/manifesto-machines/blob/main/%s' % (OWNER, t['file']),
            'techniques': [],
        })
    print('music: %d tools from %s' % (len(out), src))
    if missing: print('  no clean summary for: ' + ', '.join(missing) + ' (add them to data/music-summaries.json)')
    for s in STANDALONE:
        try:
            meta = json.loads(fetch('https://api.github.com/repos/%s/%s' % (OWNER, s['repo'])))
        except Exception:
            print('  standalone %s: repo not found, skipped' % s['repo']); continue
        live = meta.get('homepage') or ''
        if not live or status(live) != 200:
            print('  standalone %s: live URL not answering, skipped' % s['repo']); continue
        out.append({'id': 'music/' + s['repo'], 'section': 'music', 'num': 'app', 'title': s['title'],
                    'summary': re.sub(r'\s*Stand-?alone.*$', '', meta.get('description') or '').strip() or s['title'],
                    'subcategory': 'Standalone apps', 'inspired': 'Standalone live edition of Manifesto Machines tool %s' % s['from'],
                    'skillLevel': 'getting-going', 'input': ['your-sounds'], 'output': ['audio'], 'sessionLength': '30-min-plus', 'ai': 'no-ai',
                    'era': '1980-today' if s['from'] == '77' else '1946-1979', 'try': live, 'repo': meta['html_url'], 'techniques': []})
        print('  standalone %s: linked %s' % (s['repo'], live))
    return out

def section_tools(sec):
    d = local_dir(sec); repo = 'digitalplay-' + sec
    cat = json.load(open(os.path.join(d, 'catalogue.json'))) if d else json.loads(fetch(RAW % (OWNER, repo, 'catalogue.json')))
    dest = os.path.join(SITE, 'play', sec); os.makedirs(dest, exist_ok=True)
    out = []
    for t in cat['tools']:
        fn = t['file'].split('/')[-1]
        if d: shutil.copy(os.path.join(d, t['file']), os.path.join(dest, fn))
        else: open(os.path.join(dest, fn), 'wb').write(fetch(RAW % (OWNER, repo, t['file'])))
        out.append({'id': '%s/%s' % (sec, t['slug']), 'section': sec, 'num': t['num'], 'title': t['title'], 'summary': t['summary'], 'whatYouDo': t.get('whatYouDo', ''),
                    'subcategory': t['subcategory'], 'inspired': '; '.join(t.get('inspiredBy', [])), 'skillLevel': t['skillLevel'], 'input': t['input'], 'output': t['output'],
                    'sessionLength': t['sessionLength'], 'ai': t['ai'], 'era': t['era'], 'try': 'play/%s/%s' % (sec, fn),
                    'repo': 'https://github.com/%s/%s/blob/main/%s' % (OWNER, repo, t['file']), 'techniques': t.get('techniques', [])})
    print('%s: %d tools from %s' % (sec, len(out), d or 'github'))
    return out

def main():
    tax = json.load(open(os.path.join(HUB, 'taxonomy.json')))
    tools = music_tools()
    for sec in LIVE_SECTIONS: tools += section_tools(sec)
    os.makedirs(os.path.join(SITE, 'data'), exist_ok=True)
    json.dump({'generated': __import__('datetime').date.today().isoformat(), 'count': len(tools), 'tools': tools}, open(os.path.join(SITE, 'data', 'tools.json'), 'w'), ensure_ascii=False, indent=1)
    shutil.copy(os.path.join(HUB, 'taxonomy.json'), os.path.join(SITE, 'data', 'taxonomy.json'))
    print('total: %d tools' % len(tools))

if __name__ == '__main__': main()
