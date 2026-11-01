#!/usr/bin/env python3
"""Build the static site into site/. No dependencies beyond Python 3.8+.
  python3 scripts/build.py            aggregate catalogues, then write the pages
  python3 scripts/build.py --pages    write the pages from the existing site/data/tools.json
"""
import html, json, os, subprocess, sys, datetime
HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(HUB, 'site')
E = lambda s: html.escape(str(s), quote=True)
GH = 'https://github.com/anorthernman-developer'
HUB_REPO = GH + '/digitalplay-work'
X_URL = 'https://x.com/craig_stanley'
SUBSTACK_URL = 'https://anorthernman.substack.com'
BOOK_URL = 'https://www.amazon.co.uk/Digital-Play-Computer-language-Development/dp/3125013593'
COLOUR = {'#d9432b': 'tomato', '#f3b61f': 'sun', '#2a46c9': 'cobalt', '#2a7449': 'moss', '#7a3e8e': 'plum', '#11717a': 'teal'}
NAV = [('index.html', 'Home'), ('about.html', 'About'), ('project.html', 'The tools'), ('book.html', 'The book'),
       ('community.html', 'Community'), ('follow.html', 'Follow')]

MARK = ('<svg viewBox="0 0 40 40" aria-hidden="true" focusable="false"><circle cx="13" cy="13" r="9" fill="#d9432b"/>'
        '<rect x="22" y="5" width="13" height="13" fill="#2a46c9" transform="rotate(14 28.5 11.5)"/>'
        '<path d="M4 36 L13 21 L22 36 Z" fill="#f3b61f" stroke="#1f1d2b" stroke-width="1.5" stroke-linejoin="round"/>'
        '<path d="M24 36 V31 A6 6 0 0 1 36 31 V36 Z" fill="#2a7449"/></svg>')

def page(fname, title, desc, body, scripts=(), base=False):
    nav = ''.join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == fname else '', l) for h, l in NAV)
    full = title if fname == 'index.html' else '%s · digitalplay.work' % title
    js = ''.join('<script src="assets/js/%s" defer></script>' % s for s in scripts)
    doc = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
{'<base href="/">' if base else ''}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(full)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#f6f1e7">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/bricolage-grotesque-normal-400-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts.css">
<link rel="stylesheet" href="assets/css/site.css">
{js}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap">
<a class="brand" href="index.html">{MARK}<span class="vh">digitalplay.work home</span><b aria-hidden="true">digitalplay</b><span aria-hidden="true">.work</span></a>
<nav aria-label="Main"><ul class="nav">{nav}</ul></nav>
</div></header>
<main id="main" tabindex="-1">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<div>
<p class="label">Colophon</p>
<p>digitalplay.work is made by Craig Stanley and the Loose Parts Collective. The code is MIT, the words and pictures are CC BY 4.0, and the fonts are under the SIL Open Font Licence.</p>
<p>No cookies, no tracking, no accounts. <a href="privacy.html">Privacy</a> · <a href="credits.html">Licence and credits</a></p>
</div>
<div>
<p class="label">Elsewhere</p>
<p><a href="{HUB_REPO}">Source on GitHub</a> · <a href="{X_URL}">X</a> · <a href="{SUBSTACK_URL}">Substack</a></p>
</div>
</div></footer>
</body>
</html>
'''
    open(os.path.join(SITE, fname), 'w').write(doc)

def head(kicker, h1, lede, extra=''):
    return f'<div class="page-head"><div><p class="label">{kicker}</p><h1>{h1}</h1></div><div><p class="lede">{lede}</p>{extra}</div></div>'

# ---------- data
def load():
    tax = json.load(open(os.path.join(HUB, 'taxonomy.json')))
    tools = json.load(open(os.path.join(SITE, 'data', 'tools.json')))['tools']
    return tax, tools

def facet_label(tax, f, v):
    for x in tax['facets'][f]['values']:
        if x['id'] == v: return x['label']
    return v

# ---------- pages
HERO_SVG = '''<svg viewBox="0 0 500 400" aria-hidden="true" focusable="false">
<g class="part" transform="translate(120 120) rotate(0)"><circle r="70" fill="#d9432b"/></g>
<g class="part" transform="translate(330 110) rotate(18)"><rect x="-55" y="-55" width="110" height="110" fill="#2a46c9"/></g>
<g class="part" transform="translate(250 270) rotate(-8)"><path d="M-75 55 L0 -70 L75 55 Z" fill="#f3b61f" stroke="#1f1d2b" stroke-width="4" stroke-linejoin="round"/></g>
<g class="part" transform="translate(410 290) rotate(0)"><path d="M-55 50 V0 A55 55 0 0 1 55 0 V50 Z" fill="#2a7449"/></g>
<g class="part" transform="translate(95 300) rotate(-30)"><path d="M-50 0 A50 50 0 0 1 50 0 Z" fill="#7a3e8e"/></g>
<g class="part" transform="translate(205 70) rotate(0)"><circle r="30" fill="none" stroke="#11717a" stroke-width="14"/></g>
<g class="part" transform="translate(395 205) rotate(62)"><rect x="-70" y="-6" width="140" height="12" rx="6" fill="#1f1d2b"/></g>
<g class="part" transform="translate(60 205) rotate(90)"><path d="M0 0 H45 A45 45 0 0 1 0 45 Z" fill="#f3b61f" stroke="#1f1d2b" stroke-width="3"/></g>
</svg>'''

def home(tax, tools):
    counts = {}
    for t in tools: counts[t['section']] = counts.get(t['section'], 0) + 1
    tiles = []
    soon = [s for s in tax['sections'] if s['status'] != 'live']
    for s in tax['sections']:
        live = s['status'] == 'live'
        size = 'big' if s['id'] in ('music', 'art') else ('wide' if s is soon[-1] else '')
        c = 'c-' + COLOUR.get(s['colour'], 'tomato')
        if live:
            href = 'project.html#section=' + s['id']
            foot = '%d tool%s to play with' % (counts.get(s['id'], 0), '' if counts.get(s['id'], 0) == 1 else 's')
        else:
            href = 'community.html#' + s['id']
            foot = 'Coming soon · %d ideas lined up' % len(s.get('suggestedNext', []))
        tiles.append(f'<li class="tile {"live" if live else "soon"} {size} {c}"><span class="chip" aria-hidden="true"></span>'
                     f'<h3><a href="{href}">{E(s["name"])}</a></h3><p>{E(s["summary"])}</p><p class="label">{foot}</p></li>')
    body = f'''<section class="hero" aria-labelledby="hero-h"><div class="wrap">
<div>
<p class="label">Loose Parts Collective · free, open and yours to change</p>
<h1 id="hero-h">Creative tools to <em>play</em> with, made to be pulled apart.</h1>
<p class="lede">digitalplay.work is a free collection of small browser toys for music, art, design, code and words. Bring your own sounds, photos and sentences, push them about, and see what turns up. No sign-up, no feed, and most of them work offline.</p>
<p class="actions"><a class="btn btn-ink" href="project.html">Browse all {len(tools)} tools</a> <a class="btn" href="about.html">Why we’re doing this</a></p>
</div>
<figure class="table">{HERO_SVG}<figcaption class="label">Go on, drag a shape about.</figcaption></figure>
</div></section>
<section class="band" aria-labelledby="trays-h"><div class="wrap">
<div class="band-head"><h2 id="trays-h">Twelve trays of loose parts</h2><p>Five have tools in already. Seven are waiting for you to suggest what goes in them.</p></div>
<ul class="tray">{''.join(tiles)}</ul>
</div></section>
<section class="band" aria-labelledby="how-h"><div class="wrap">
<div class="band-head"><h2 id="how-h">How it works</h2><p>Every tool follows the same three habits.</p></div>
<ol class="steps">
<li><h3>Bring your own stuff</h3><p>Each tool starts with your material: a voice memo, a photo off your phone, a paragraph you wrote on the bus. The tool is the table; you bring the parts.</p></li>
<li><h3>Learn as you go</h3><p>Every tool has a LEARN panel that explains the idea behind it in plain words, where it came from, and a couple of things to try next.</p></li>
<li><h3>Keep it, share it, change it</h3><p>Save presets, export them as a file, and hand them to a mate. Every tool is a single HTML file under an open licence, so you can open it up and make it your own.</p></li>
</ol>
</div></section>
<section class="band" aria-labelledby="book-h"><div class="wrap">
<div class="prose"><div>
<h2 id="book-h">Where the name comes from</h2>
<p>“Digital play” is the title of a 2011 book by Kyle Mawer and Graham Stanley about using computer games in language teaching. Its big idea is simple: people learn well when they are playing, and a teacher can build real learning around real games. This site takes that idea out of the language classroom and into the creative arts. <a href="book.html">Read our summary of the book</a>.</p>
</div>
<aside class="aside"><h2>Put the phone down</h2><p>This isn’t another feed. Pick a tool, make something odd for fifteen minutes, then go and tell someone about it. <a href="about.html#socials">More on that</a>.</p></aside>
</div></div></section>'''
    page('index.html', 'digitalplay.work · free creative tools to play with', 'Free, open, playful browser tools for music, art, design, coding and writing, from the Loose Parts Collective.', body, ['table.js'])

def about(tax, tools):
    live = [s for s in tax['sections'] if s['status'] == 'live']
    body = head('About the project', 'Play first. Everything else follows.', 'digitalplay.work is a free, open collection of creative tools for people who would rather make something than scroll past it.') + f'''
<div class="prose"><div>
<h2>What this is</h2>
<p>It’s a shelf of small, playful tools that run in your web browser. Each one takes a single creative idea, like cutting up a sentence, folding a drawing into a kaleidoscope or growing a pattern from a few rules, and turns it into something you can push about with your own material.</p>
<p>The tools are grouped into twelve sections, from Music and Art to Making and Nature &amp; Science. {len(live)} of them have tools in already. The rest are open for ideas, and you can <a href="community.html">suggest what goes in them</a>.</p>

<h2>Why “digital play”</h2>
<p>The name is borrowed, with love, from <a href="book.html">a book of the same name</a> about using computer games to teach languages. That book argues that play isn’t a break from learning, it’s one of the best ways to do it, and that what matters is what you do with the technology rather than how fancy it is. We think the same is true for making art, music and writing.</p>

<h2>Fun first, then the clever bit</h2>
<p>Every tool has to be fun within a minute of opening it. Only then does it show you the idea underneath: where the technique came from, why it works, and how to take it further. Innovation tends to turn up when people are messing about, so we make the messing about as easy as we can.</p>

<h2>Free, and staying free</h2>
<p>Everything here is given away. No accounts, no adverts, no paywall, no upsell. The code is under the MIT licence and the words and pictures are under Creative Commons Attribution 4.0, so you can copy a tool, change it, use it in a classroom or a workshop, and share it again. All we ask is a credit.</p>

<h2 id="socials">Get off the socials for a bit</h2>
<p>Scrolling is easy, and it’s designed to keep you scrolling. Making something, even something small and daft, uses a different part of your brain. You make choices, you get things wrong, you notice things. That’s the part we want to wake up. So there’s no feed here, no likes and no notifications. Open a tool, make something, close the tab.</p>

<h2>Why “Loose Parts Collective”</h2>
<p>In 1971 the architect Simon Nicholson wrote about the theory of loose parts: the idea that places full of movable, open-ended bits invite far more creativity than places where everything is fixed down. Each tool on this site is meant to be a tray of loose parts. The collective is anyone who plays with them, suggests one, or builds one.</p>

<h2>Who’s behind it</h2>
<p>digitalplay.work was started by Craig Stanley in 2026, building on <a href="project.html#section=music">Manifesto Machines</a>, a set of more than eighty free music instruments. It’s an arts project, not a business. If you’d like to help, the <a href="community.html">community page</a> explains how.</p>
</div>
<aside class="aside"><h2>At a glance</h2><dl>
<dt>Tools so far</dt><dd>{len(tools)}</dd>
<dt>Sections</dt><dd>12, with {len(live)} open</dd>
<dt>Cost</dt><dd>Nothing, ever</dd>
<dt>Tracking</dt><dd>None. <a href="privacy.html">Privacy</a></dd>
<dt>Licences</dt><dd>MIT for code, CC BY 4.0 for content</dd>
</dl></aside>
</div>'''
    page('about.html', 'About the project', 'Why digitalplay.work exists: digital play, fun before cleverness, giving things away, and getting off the socials for a bit.', '<div class="page"><div class="wrap">' + body + '</div></div>')

def project(tax, tools):
    secs = {s['id']: s for s in tax['sections']}
    counts = {}
    for t in tools: counts[t['section']] = counts.get(t['section'], 0) + 1
    tabs = ['<li><button type="button" data-sec="all" aria-pressed="true">All sections</button></li>']
    for s in tax['sections']:
        if s['status'] == 'live':
            tabs.append('<li><button type="button" data-sec="%s" aria-pressed="false">%s <span aria-hidden="true">(%d)</span><span class="vh">, %d tools</span></button></li>' % (s['id'], E(s['name']), counts.get(s['id'], 0), counts.get(s['id'], 0)))
        else:
            tabs.append('<li><button type="button" data-sec="%s" disabled>%s <span class="vh">(coming soon)</span></button></li>' % (s['id'], E(s['name'])))
    order = ['skillLevel', 'input', 'output', 'era', 'sessionLength', 'ai']
    sets = []
    for f in order:
        used = set()
        for t in tools:
            v = t[f]; used.update(v if isinstance(v, list) else [v])
        opts = ''.join('<label><input type="checkbox" name="%s" value="%s"> <span>%s</span><span class="count" aria-hidden="true"></span></label>' % (f, v['id'], E(v['label'])) for v in tax['facets'][f]['values'] if v['id'] in used)
        sets.append('<fieldset><legend>%s</legend>%s</fieldset>' % (E(tax['facets'][f]['label']), opts))
    cards = []
    for t in tools:
        s = secs[t['section']]
        c = 'c-' + COLOUR.get(s['colour'], 'tomato')
        attrs = ' '.join('data-%s="%s"' % (k, E(' '.join(t[f]) if isinstance(t[f], list) else t[f])) for k, f in
                         [('skill-level', 'skillLevel'), ('input', 'input'), ('output', 'output'), ('era', 'era'), ('session-length', 'sessionLength'), ('ai', 'ai')])
        terms = ' '.join([t['subcategory']] + t.get('techniques', []))
        tags = '<li>%s</li><li>%s</li>' % (E(facet_label(tax, 'skillLevel', t['skillLevel'])), E(facet_label(tax, 'sessionLength', t['sessionLength'])))
        tags += ''.join('<li>%s</li>' % E(facet_label(tax, 'input', v)) for v in t['input'])
        if t['ai'] == 'ai-optional': tags += '<li class="ai">AI optional</li>'
        num = '' if t['num'] == 'app' else ' · %s' % E(t['num'])
        what = '<p>%s</p>' % E(t['whatYouDo']) if t.get('whatYouDo') else ''
        cards.append(f'''<li class="card {c}" data-section="{t['section']}" {attrs} data-terms="{E(terms)}">
<div class="meta"><span class="label">{E(s['name'])}{num}</span></div>
<h3>{E(t['title'])}</h3>
<p class="sub">{E(t["subcategory"])}</p>
<p>{E(t['summary'])}</p>{what}
<p class="insp">Inspired by {E(t['inspired'])}</p>
<ul class="tags" aria-label="Facets">{tags}</ul>
<p class="links"><a href="{E(t['try'])}">Try it<span class="vh">: {E(t['title'])}</span></a> <a href="{E(t['repo'])}">Source<span class="vh"> for {E(t['title'])}</span></a></p>
</li>''')
    body = head('The project and the repo', 'Every tool, in one place.', 'Search by name or idea, then narrow it down by what you bring, what you take away and how long you’ve got. The whole thing is built from one open taxonomy.',
                '<p class="small">Each section lives in its own GitHub repo. This hub pulls their catalogues together. Read <a href="%s/blob/main/docs/taxonomy.md">how the taxonomy works</a> or grab <a href="data/taxonomy.json">taxonomy.json</a> and <a href="data/tools.json">tools.json</a>.</p>' % HUB_REPO) + f'''
<div id="browser" class="browser">
<div class="filters" role="group" aria-labelledby="filters-h">
<h2 id="filters-h" class="label">Filter</h2>
{''.join(sets)}
<button type="button" class="linkbtn" data-clear>Clear all filters</button>
</div>
<div>
<form class="search" role="search"><label><span class="label">Search the tools</span><input id="q" type="search" autocomplete="off" spellcheck="false" placeholder="Try “loops”, “colour” or “rules”"></label></form>
<ul class="sec-tabs" aria-label="Section">{''.join(tabs)}</ul>
<p id="status" class="status" role="status" aria-live="polite">Showing all {len(tools)} tools</p>
<div id="empty" class="empty" hidden><p>Nothing matches that. Try fewer filters, or <a href="community.html">suggest a tool</a> that would.</p><button type="button" class="linkbtn" data-clear>Clear all filters</button></div>
<ul class="cards">{''.join(cards)}</ul>
</div></div>'''
    page('project.html', 'The project and the repo', 'Search and filter every digitalplay.work tool by section, skill level, what you bring, what you take away, era, time and AI.', '<div class="page"><div class="wrap">' + body + '</div></div>', ['browser.js'])

def book(tax, tools):
    body = head('Digital Play, the book', 'The book behind the name.', 'A short summary, in our own words, of the book that gave this project its name. It isn’t a substitute for reading it.') + f'''
<div class="prose"><div>
<h2>What it is</h2>
<p><cite>Digital Play: Computer games and language aims</cite> is a practical book for language teachers, written by Kyle Mawer and Graham Stanley and published in 2011 by Delta Publishing as part of the Delta Teacher Development Series. It won the British Council’s 2012 ELTon award for innovation in teacher resources. It sets out to show teachers that the games their learners already love can be the centre of a lesson, not a reward at the end of it.</p>

<h2>How it is put together</h2>
<p>The book comes in three parts.</p>
<ul class="ticks">
<li><strong>The ideas.</strong> The first part explains why games and language learning fit together, what makes a game worth using, and what the teacher’s job becomes when the computer is involved.</li>
<li><strong>The activities.</strong> The middle and biggest part is a bank of practical classroom activities, arranged by how much technology you have, from none at all, through one computer and a projector, to a room full of machines or a class with phones.</li>
<li><strong>Taking it further.</strong> The last part is about the teacher’s own development: fitting games into a course, finding and judging new ones, and sharing what works with colleagues.</li>
</ul>

<h2>The main ideas, as we understand them</h2>
<ul class="ticks">
<li><strong>Play is serious.</strong> People of all ages learn by playing, and a game that holds someone’s attention is doing a lot of the teacher’s work already.</li>
<li><strong>Use real games.</strong> Ordinary, popular games, played for their own sake, often make better lessons than software made specially to teach. The learning comes from the tasks the teacher builds around them.</li>
<li><strong>Talk around the screen.</strong> Games naturally create gaps in information, with one person knowing what another needs. That gives learners a real reason to speak, ask, explain and write.</li>
<li><strong>Meaning before form.</strong> Get people communicating first, then look at the language they needed and used.</li>
<li><strong>Before, during and after.</strong> Much of the value is in what happens around the game: predicting, planning and instructing beforehand, then describing, retelling and reflecting afterwards.</li>
<li><strong>The teacher as guide.</strong> Learners may know the games better than the teacher. That’s fine; the teacher brings the language and the structure, and the learners bring the expertise in the game.</li>
<li><strong>Any kit will do.</strong> You don’t need a computer suite. One screen and a good idea can be enough. What you do with the technology matters much more than what you have.</li>
<li><strong>Share what works.</strong> Teachers get further when they collect, tag and swap game-based ideas and materials with each other.</li>
</ul>

<h2>From language aims to creative arts</h2>
<p>The book is about language teaching. digitalplay.work borrows its spirit and points it at making things: music, art, design, code, writing and the rest. The same habits carry over. Start with something genuinely playful. Bring your own material to it. Talk about what you made and how. Share it so someone else can build on it. Each tool’s LEARN panel is our version of the conversation around the screen.</p>
<p class="note">This page is a summary written in our own words. It contains no text, activities or images from the book. To read the real thing, buy a copy.</p>
</div>
<aside class="aside"><h2>The book</h2><dl>
<dt>Title</dt><dd><cite>Digital Play: Computer games and language aims</cite></dd>
<dt>Authors</dt><dd>Kyle Mawer and Graham Stanley</dd>
<dt>Series</dt><dd>Delta Teacher Development Series</dd>
<dt>Publisher</dt><dd>Delta Publishing, 2011</dd>
<dt>ISBN</dt><dd>978-1-905085-55-2</dd>
</dl>
<p><a class="btn btn-sun" href="{BOOK_URL}">Buy it on Amazon UK</a></p>
<p class="small">Not an affiliate link. We don’t earn anything from it.</p>
</aside>
</div>'''
    page('book.html', 'Digital Play, the book', 'A summary in our own words of Digital Play: Computer games and language aims by Kyle Mawer and Graham Stanley, and how this site extends its idea to the creative arts.', '<div class="page"><div class="wrap">' + body + '</div></div>')

def community(tax, tools):
    items = []
    for s in tax['sections']:
        sn = s.get('suggestedNext') or []
        if not sn: continue
        state = 'open now' if s['status'] == 'live' else 'coming soon'
        items.append('<li id="%s"><h3>%s</h3><p class="label">%s</p><ul>%s</ul></li>' % (s['id'], E(s['name']), state, ''.join('<li>%s</li>' % E(x) for x in sn)))
    body = head('Community', 'Suggest a tool. Build one. Swap ideas.', 'The collective is whoever turns up. Here’s how to join in without handing over anything you don’t want to.') + f'''
<div class="channels">
<div class="channel"><h2>Suggest a tool</h2><p>Got an idea for something playful? Open a suggestion on GitHub. There’s a short form that asks what it would do, what you’d bring to it and what you’d take away.</p>
<p><a class="btn btn-sun" href="{HUB_REPO}/issues/new?template=suggest-a-tool.yml">Suggest a tool on GitHub</a></p></div>
<div class="channel"><h2>Talk it through</h2><p>Not sure it’s a tool yet? Start a conversation in GitHub Discussions, show something you made, or ask how one of the tools works.</p>
<p><a class="btn" href="{HUB_REPO}/discussions">Open Discussions</a></p></div>
</div>
<div class="prose"><div>
<h2>Already on the list</h2>
<p>These are the ideas we’d like to build next, section by section. If one of them sounds like yours, say so in Discussions and help shape it.</p>
</div>
<aside class="aside"><h2>House rules</h2><ul class="ticks small">
<li>Ideas, techniques and movements, yes. Copying a named living artist’s style or identity, no.</li>
<li>Only share material that’s yours or openly licensed.</li>
<li>GitHub is public. Don’t post personal details, yours or anyone else’s.</li>
<li>Be kind. Beginners are the point.</li>
</ul></aside></div>
<ul class="sugg">{''.join(items)}</ul>
<div class="band"><div class="prose"><div>
<h2>Building a tool yourself</h2>
<p>Every section repo has a CONTRIBUTING guide. In short: one HTML file, no external requests, your own inputs, a LEARN panel, presets you can export as JSON, and a short factual “inspired by” line. Fork the repo for the section, add your tool, and open a pull request.</p>
<p>Section repos: <a href="{GH}/digitalplay-art">Art</a> · <a href="{GH}/digitalplay-design">Design</a> · <a href="{GH}/digitalplay-coding">Coding</a> · <a href="{GH}/digitalplay-writing">Writing</a> · <a href="{GH}/manifesto-machines">Music</a></p>
<p class="small">GitHub is run by GitHub, Inc. and has its own privacy policy. This site doesn’t collect anything itself; see <a href="privacy.html">privacy</a>.</p>
</div></div></div>'''
    page('community.html', 'Community', 'Suggest a tool, talk about ideas and contribute to digitalplay.work through GitHub. No sign-up on this site.', '<div class="page"><div class="wrap">' + body + '</div></div>')

def follow(tax, tools):
    body = head('Follow along', 'New tools, as they land.', 'There’s no mailing list on this site. Follow on X or subscribe on Substack, whichever you already use.') + f'''
<div class="channels">
<div class="channel"><h2>X</h2><p>Short posts when a new tool goes live, plus the odd thing someone made with one.</p><p><a class="btn btn-ink" href="{X_URL}">@craig_stanley on X</a></p></div>
<div class="channel"><h2>Substack</h2><p>Notes on each new tool and the idea behind it, plus a longer write-up now and then. Subscribe there if you want it by email.</p><p><a class="btn btn-sun" href="{SUBSTACK_URL}">Read on Substack</a></p></div>
</div>
<div class="prose"><div>
<h2>How the posts get made</h2>
<p>We schedule posts with Buffer, a tool for queuing social posts. A person writes and checks every one. Nothing is posted automatically.</p>
<ol class="flow">
<li><div><h3>A tool goes live</h3><p>A new tool is merged into one of the section repos and appears on <a href="project.html">the tools page</a>.</p></div></li>
<li><div><h3>A draft gets written</h3><p>A short, plain post is drafted in the hub repo, in <a href="{HUB_REPO}/blob/main/docs/launch-posts.md">docs/launch-posts.md</a>, so anyone can see what’s coming.</p></div></li>
<li><div><h3>Craig reads it and queues it</h3><p>Craig edits the draft and queues it in Buffer himself, for X and as a Substack Note.</p></div></li>
<li><div><h3>It goes out, and that’s it</h3><p>No bots replying, no tracking links. If you want to talk about a tool, come to <a href="community.html">Discussions</a>.</p></div></li>
</ol>
</div>
<aside class="aside"><h2>About your data</h2><p class="small">X, Substack and Buffer are separate services with their own privacy policies. This site sets no cookies and doesn’t embed their widgets, so nothing loads from them until you click through.</p></aside>
</div>'''
    page('follow.html', 'Follow along', 'Follow digitalplay.work on X and Substack, and see how launch posts are written and scheduled.', '<div class="page"><div class="wrap">' + body + '</div></div>')

def privacy(tax, tools):
    body = head('Privacy', 'We don’t want your data.', 'Short version: no cookies, no analytics, no tracking, no accounts. The longer version is below.') + '''
<div class="prose"><div>
<h2>This website</h2>
<ul class="ticks">
<li>No cookies, no analytics, no advertising and no tracking pixels.</li>
<li>No forms. We don’t collect names, email addresses or anything else.</li>
<li>Fonts, scripts and styles are all served from this site, so visiting doesn’t send anything to Google or anyone else.</li>
<li>The site is hosted on Netlify. Like any web host, Netlify handles technical information such as your IP address in order to deliver pages and keep the service secure. We don’t use it to identify or profile anyone.</li>
</ul>
<h2>The tools</h2>
<ul class="ticks">
<li>The tools run in your browser. Your sounds, photos and words stay on your device and aren’t uploaded anywhere.</li>
<li>Presets you save are kept in your browser’s local storage. You can export them as a file, and clearing your browser’s site data removes them.</li>
<li>The starter tools in Art, Design, Coding and Writing make no network requests at all once they’ve loaded.</li>
</ul>
<h2 id="gemini">AI and your own Gemini key</h2>
<p>A few music tools have an optional AI feature. If you choose to use it, you paste in your own Google Gemini API key.</p>
<ul class="ticks">
<li>Your key is stored only in your own browser’s local storage on that device. It isn’t sent to us, and we never see it.</li>
<li>When you press an AI button, the tool sends your request straight from your browser to Google’s Gemini API using your key. Google’s terms and privacy policy apply to that request.</li>
<li>Every tool works without AI. Leave the key box empty and nothing is ever sent.</li>
<li>To remove a key, use the tool’s clear button if it has one, or clear this site’s data in your browser settings.</li>
<li>Don’t paste a key on a shared or public computer.</li>
</ul>
<h2>Other sites we link to</h2>
<p>We link to GitHub, X, Substack and Amazon. They’re separate services with their own policies, and nothing from them loads on this site until you follow a link.</p>
<h2>Questions</h2>
<p>Ask in <a href="https://github.com/anorthernman-developer/digitalplay-work/discussions">GitHub Discussions</a>, but please don’t post personal details there because it’s public.</p>
</div>
<aside class="aside"><h2>In one line</h2><p>Your stuff stays on your device, and so does your key.</p><dl><dt>Last updated</dt><dd>''' + datetime.date.today().strftime('%-d %B %Y') + '''</dd></dl></aside>
</div>'''
    page('privacy.html', 'Privacy', 'digitalplay.work sets no cookies, runs no analytics and collects no personal data. Any Gemini key you paste stays in your own browser.', '<div class="page"><div class="wrap">' + body + '</div></div>')

def credits(tax, tools):
    insp = sorted({t['inspired'] for t in tools if t['section'] != 'music'})
    body = head('Licence and credits', 'Take it, change it, credit it.', 'Everything here is free to reuse under open licences. Here’s what applies to what, and who we owe thanks to.') + f'''
<div class="prose"><div>
<h2>Licences</h2>
<ul class="ticks">
<li><strong>Code</strong> (HTML, CSS, JavaScript and scripts): MIT Licence. Copyright © 2026 Craig Stanley and Loose Parts Collective contributors.</li>
<li><strong>Content</strong> (words, taxonomy, catalogues, pictures): Creative Commons Attribution 4.0 International (CC BY 4.0). Credit “digitalplay.work, Loose Parts Collective” with a link.</li>
<li><strong>Fonts</strong>: Bricolage Grotesque, Atkinson Hyperlegible and JetBrains Mono, all under the SIL Open Font Licence 1.1, served from this site.</li>
<li><strong>Music tools</strong>: each one carries its own licence and credits in <a href="{GH}/manifesto-machines">the Manifesto Machines repo</a>.</li>
</ul>
<h2>The book</h2>
<p>The name and the spirit of the project come from <cite>Digital Play: Computer games and language aims</cite> by Kyle Mawer and Graham Stanley (Delta Publishing, 2011). Our <a href="book.html">summary page</a> is written in our own words.</p>
<h2>Ideas we built on</h2>
<p>The starter tools are built on old, openly shared ideas. Each one says what inspired it:</p>
<ul class="ticks small">{''.join('<li>%s</li>' % E(i) for i in insp)}</ul>
<p>Simon Nicholson’s theory of loose parts (1971) gave the collective its name.</p>
<h2>Accessibility</h2>
<p>We aim for WCAG 2.2 level AA: readable contrast, keyboard access to every control, visible focus and respect for reduced-motion settings. If something gets in your way, <a href="{HUB_REPO}/issues/new?template=suggest-a-tool.yml">tell us on GitHub</a>.</p>
</div>
<aside class="aside"><h2>Source</h2><p><a href="{HUB_REPO}">digitalplay-work on GitHub</a> holds this site, the taxonomy and the build script.</p></aside>
</div>'''
    page('credits.html', 'Licence and credits', 'Licences for digitalplay.work code, content and fonts, and credits for the ideas behind the tools.', '<div class="page"><div class="wrap">' + body + '</div></div>')

def notfound(tax, tools):
    body = head('404', 'That part’s gone missing.', 'Loose parts do wander off. Try the tools page, or head back to the start.', '<p><a class="btn btn-ink" href="/project.html">Browse the tools</a></p>')
    page('404.html', 'Page not found', 'This page could not be found.', '<div class="page"><div class="wrap">' + body + '</div></div>', base=True)

def main():
    if '--pages' not in sys.argv:
        subprocess.check_call([sys.executable, os.path.join(HUB, 'scripts', 'aggregate.py')])
    tax, tools = load()
    for fn in (home, about, project, book, community, follow, privacy, credits, notfound): fn(tax, tools)
    open(os.path.join(SITE, 'favicon.svg'), 'w').write(MARK.replace(' aria-hidden="true" focusable="false"', ' xmlns="http://www.w3.org/2000/svg"'))
    print('pages written to', SITE)

if __name__ == '__main__': main()
