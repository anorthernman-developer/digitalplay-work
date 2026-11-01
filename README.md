# digitalplay.work

Free, open, playful creative tools from the **Loose Parts Collective**. This repo is the hub: the website, the taxonomy that ties every section together, and the script that gathers each section's catalogue into one browsable list.

**Live site:** https://digitalplay-work.netlify.app (the digitalplay.work domain is still to be attached)

## What's in here

| Path | What it is |
|---|---|
| `site/` | The static website. No build step on the server, no framework, no tracking. |
| `taxonomy.json` | The ontology: 12 sections, their subcategories, six facets and the relationships between them. See [docs/taxonomy.md](docs/taxonomy.md). |
| `catalogue.schema.json` | JSON Schema every section's `catalogue.json` must match. |
| `scripts/aggregate.py` | Pulls each section catalogue (local checkout first, then GitHub) plus the Manifesto Machines catalogue into `site/data/tools.json`, and copies section tools into `site/play/`. |
| `scripts/build.py` | Runs the aggregator, then writes the HTML pages. |
| `data/music-summaries.json` | Plain one-line explanations, written for the hub, for music tools whose catalogue text names people or quotes sources. |
| `docs/launch-posts.md` | Draft launch posts for X and Substack Notes. Drafts only; nothing is posted automatically. |
| `docs/brand/` | The brand pack and a brand system prompt for anyone (or any tool) making things for the project. |
| `.github/ISSUE_TEMPLATE/` | The "Suggest a tool" form. |

## Sections

| Section | Repo | Status |
|---|---|---|
| Music | [manifesto-machines](https://github.com/anorthernman-developer/manifesto-machines) | Live, 81 instruments plus standalone apps |
| Art | [digitalplay-art](https://github.com/anorthernman-developer/digitalplay-art) | Live |
| Design | [digitalplay-design](https://github.com/anorthernman-developer/digitalplay-design) | Live |
| Coding | [digitalplay-coding](https://github.com/anorthernman-developer/digitalplay-coding) | Live |
| Writing | [digitalplay-writing](https://github.com/anorthernman-developer/digitalplay-writing) | Live |
| Moving Image, Games & Play, Performance, Photography & Image, Making, Nature & Science, Ideas | not yet | Coming soon; suggested first tools are in `taxonomy.json` |

## Build it

```sh
python3 scripts/build.py          # aggregate + write pages
python3 scripts/build.py --pages  # pages only, from the existing site/data/tools.json
python3 -m http.server -d site 8000
```

Python 3.8+ only. Section repos are read from sibling folders (`../digitalplay-art` or `../art`) if present, otherwise from GitHub.

## Deploy

The site is hosted on Netlify. `netlify.toml` publishes `site/` with strict security headers. Starter tools under `/play/` get a Content Security Policy that blocks every network request, so the "works offline, sends nothing" promise is enforced, not just claimed.

```sh
# scan for secrets first, every time
scripts/secret-scan.sh .
netlify deploy --prod --dir site
```

## The name

"Loose Parts Collective" comes from Simon Nicholson's 1971 theory of loose parts: places full of movable, open-ended bits invite more creativity than places where everything is fixed. Other names we considered, if it ever needs to change: **Open Play Collective**, **The Sandpit**, **Free Play Assembly**. The name appears in `taxonomy.json`, `scripts/build.py`, the licences and the brand pack.

## Rules for everything in this project

- No living artist's name or likeness in a tool name, branding or any AI prompt that imitates a named person.
- Influences appear only as short, factual "inspired by" lines.
- No copyrighted quotes, lyrics, scores, images or fonts without a licence. Fonts are SIL OFL and self-hosted.
- No personal data. No cookies, analytics or tracking.
- Never commit an API key. Visitors paste their own Gemini key and it stays in their browser.

## Licence

Code: MIT (`LICENSE`). Content: CC BY 4.0 (`LICENSE-CONTENT.md`). Fonts: SIL Open Font Licence 1.1 (`site/assets/fonts/OFL-*.txt`).
