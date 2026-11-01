# The digitalplay.work taxonomy

`taxonomy.json` is a small ontology for free, playful creative tools. It does three jobs: it tells the website how to group and filter tools, it tells contributors where a new tool belongs, and it keeps every section repo describing its tools in the same way.

## The shape of it

- **Sections** are the twelve trays. Each one is its own GitHub repo (Music lives in `manifesto-machines`).
- **Subcategories** sit inside a section. Every tool has exactly one.
- **Facets** cut across sections, so you can ask for "a first-go tool that takes my photos and gives me a PNG in five minutes" anywhere on the site.
- **Relationships** link a tool to the techniques it uses, the movement or era it comes from, what inspired it, and related tools.

## Sections

| Section | Status | Summary | Subcategories |
|---|---|---|---|
| Music | live | Instruments built from art manifestos, music theory, natural patterns and studio methods. Bring your own sounds. | Art manifestos as instruments, Composition and theory, Nature and philosophy, Generative and ambient, Found sound and production, Standalone apps |
| Art | live | Shapes, marks, colour and pattern. Push things about until a picture turns up. | Composition and collage, Pattern and symmetry, Drawing games, Colour and light, Print-style effects |
| Design | live | Grids, colour and type for posters, pages and things people actually read. | Layout and grids, Colour, Type and lettering, Pattern and surface, Information and maps |
| Coding | live | Code as a material for drawing, systems and toys. Small rules, big surprises. | Creative coding basics, Generative systems, Sound and code, Interactive toys |
| Writing | live | Words as loose parts: cut them up, constrain them, turn them into games. | Experimental writing, Interactive fiction, Poetry forms, Story games |
| Moving Image | coming soon | Animation, montage and stop motion from things you draw or film. | Animation, Editing and montage, Stop motion |
| Games and Play | coming soon | Make games, change rules and play with play itself. | Game design, Toys and play, Puzzles |
| Performance | coming soon | Prompts and scores for theatre, movement and live art. | Theatre and improvisation, Dance and movement, Live art |
| Photography and Image | coming soon | Camera play and darkroom-style effects on your own pictures. | Camera play, Darkroom effects, Image collage |
| Making | coming soon | Print, cut, fold and build: paper, textiles and tinkering. | Paper and card, Textiles, Building and tinkering |
| Nature and Science | coming soon | Patterns in leaves, weather, tides and numbers. | Natural patterns, Observation and recording, Maths and art |
| Ideas | coming soon | Tools for thinking sideways: prompts, constraints and reflection. | Creative thinking, Prompts and constraints, Reflection |

### Suggested first tools for the sections still to come

**Moving Image**
- Flipbook Studio: frame-by-frame drawing with onion skins, export a GIF
- Stop-Motion Booth: grab frames from your webcam and play them back
- Zoetrope: build a spinning optical toy strip and print it

**Games and Play**
- Board Game Forge: design a roll-and-move board and print it
- Rule Swap: take a classic game and change one rule at a time
- Tiny Platformer: draw a level and play it straight away

**Performance**
- Event Score Cards: write and shuffle one-line instructions for a performance
- Movement Dice: roll actions, levels and speeds for a short dance
- Shadow Theatre: cut-out puppets against a lit screen

**Photography and Image**
- Photogram Maker: lay objects on virtual blueprint paper
- Contact Sheet: shoot a roll of twelve and choose one
- Pinhole Simulator: see how aperture and distance change a picture

**Making**
- Paper Net Builder: design a 3D shape and print its net to fold
- Weave Planner: plan a woven pattern on a virtual loom
- Pop-Up Card Lab: simple pop-up mechanisms to cut and fold

**Nature and Science**
- Sky Diary: log the sky's colour each day and build a year-long strip
- Leaf Symmetry Lab: photograph leaves and compare their halves
- Sun Clock: make a sundial for your exact location

**Ideas**
- Prompt Deck: write your own deck of creative prompts and draw one a day
- Idea Collider: smash two random things together and see what you get
- Done List: a calm log of what you made this week

## Facets

### Skill level (`skillLevel`)

| id | Label | Meaning |
|---|---|---|
| `first-go` | First go | Open it and play. No experience needed. |
| `getting-going` | Getting going | A few ideas to pick up; rewards a second visit. |
| `deep-dive` | Deep dive | Lots of controls; give it an evening. |

### You bring (`input`)

| id | Label | Meaning |
|---|---|---|
| `your-sounds` | Your sounds |  |
| `your-images` | Your photos |  |
| `your-words` | Your words |  |
| `your-drawing` | Your drawing |  |
| `your-code` | Your code |  |
| `your-rules` | Your rules |  |
| `your-choices` | Your choices |  |

### You take away (`output`)

| id | Label | Meaning |
|---|---|---|
| `audio` | Live sound |  |
| `wav` | WAV recording |  |
| `image-png` | PNG image |  |
| `vector-svg` | SVG vector |  |
| `text` | Text |  |
| `css` | CSS |  |
| `json-preset` | Preset file |  |

### Movement or era (`era`)

| id | Label | Meaning |
|---|---|---|
| `ancient-traditional` | Ancient and traditional |  |
| `before-1900` | Before 1900 |  |
| `1900-1945` | 1900 to 1945 |  |
| `1946-1979` | 1946 to 1979 |  |
| `1980-today` | 1980 to today |  |

### Session length (`sessionLength`)

| id | Label | Meaning |
|---|---|---|
| `5-min` | 5 minutes |  |
| `15-min` | 15 minutes |  |
| `30-min-plus` | 30 minutes or more |  |

### AI (`ai`)

| id | Label | Meaning |
|---|---|---|
| `no-ai` | No AI | Everything runs in your browser. |
| `ai-optional` | AI optional | Works without AI. If you want, paste your own Gemini key; it stays in your browser. |

Multi-valued facets: `input` and `output` are lists. The rest take one value. In the browser, values inside one facet are combined with OR and different facets with AND.

## Relationships

- `inSection`: Every tool lives in exactly one section.
- `inSubcategory`: Every tool has exactly one subcategory inside its section.
- `usesTechnique`: Plain-English techniques a player practises, e.g. symmetry, loops, cut-up.
- `fromMovement`: The movement, tradition or era the idea comes from, stated factually.
- `inspiredBy`: Short factual lines naming a work, idea or tradition. Never a living person's likeness, voice or style imitation.
- `relatedTo`: Tools that share an idea or pair well, across any section.

## Adding a tool

1. Pick the section and one subcategory from the table above. If nothing fits, propose a new subcategory in your pull request.
2. Add an entry to that section repo's `catalogue.json`. It must validate against `catalogue.schema.json`.
3. Fill every facet honestly. "First go" means someone with no experience gets something nice within a minute.
4. Write `inspiredBy` as short factual lines: a technique, movement or historical source and a date. Never a tool that imitates a named living person.
5. Rebuild the hub with `python3 scripts/build.py`.

## Rules

- No living artist's name or likeness in a tool name, branding or AI prompt that imitates a named person.
- Influences appear only as short factual inspired-by lines.
- No copyrighted quotes, lyrics, scores, images or fonts without a licence.
- No personal data collected. Tools run in the browser and work offline.
- Visitor API keys are pasted by the visitor and stored only in their own browser.
