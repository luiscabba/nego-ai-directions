# Nego AI · Glass Console Design System

Dark frosted glass on a deep teal-black ground. Teal stands for the agent, amber for the debtor, blue for information and review. Everything floats as glass panels over three slow-drifting colour glows.

Source of truth: `canvas/P5.dc.html` (app) and `canvas/PSystem.dc.html` (system sheet).

---

## 1. Colour

### Core tokens

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#0A1012` | Page ground |
| `--panel` | `#0F1A1C` | Solid fills inside rings (score ring centre) |
| `--ink` | `#E6F0EE` | Primary text |
| `--ink-2` | `#C3D2CF` | Secondary text, body copy in cards |
| `--mute` | `#9FB3AF` | Labels, metadata, inactive nav |
| `--faint` | `#6F827E` | Disabled, future steps, table headers |
| `--teal` | `#7FE3C0` | Agent, primary action, success, active state |
| `--teal-d` | `#3FB68B` | Gradient end of primary buttons |
| `--teal-ink` | `#06231A` | Text on teal fills |
| `--amber` | `#F2C287` | Debtor, warnings, open tickets, late moments |
| `--amber-2` | `#F2D3A8` | Body text on warm cards |
| `--blue` | `#A9C1FF` | Info, in progress, needs review |
| `--red` | `#F0705A` | Live recording, end call, danger |

### Glass surfaces

| Surface | Fill | Border |
|---|---|---|
| Glass | `rgba(255,255,255,.055)` | `rgba(255,255,255,.12)` |
| Glass hi (featured) | `rgba(255,255,255,.085)` | `rgba(127,227,192,.36)` |
| Glass warm (debtor) | `rgba(242,194,135,.07)` | `rgba(242,194,135,.24)` |
| Row | `rgba(255,255,255,.03)` | none; hover `.065` |
| Line | | `rgba(255,255,255,.07)` for dividers |

Glass recipe: `backdrop-filter: blur(28px) saturate(160%)`, inset top highlight `0 1px 0 rgba(255,255,255,.12)`, drop shadow `0 24px 60px rgba(0,0,0,.28)`.

### Background glows

Three radial blobs behind everything, drifting on 16 s and 20 s loops:
- Teal `rgba(38,160,128,.46)`, top left, 820 × 620
- Blue `rgba(46,86,170,.40)`, top right, 760 × 580
- Amber `rgba(214,140,50,.22)`, bottom centre, 640 × 520

### Colour rules

- Teal is always the agent, amber is always the debtor. Speaker rings, waveforms, transcript names and timeline segments follow this.
- Status colour carries meaning, never decoration. Do not use amber for anything that is not a warning or the debtor.
- Every status also has a text label; colour is never the only signal.

---

## 2. Type

| Role | Font | Size / weight | Notes |
|---|---|---|---|
| Display | Sora | 38 / 600 | Home hero title, letter-spacing −.02em |
| Heading (H1) | Sora | 30 / 600 | Page titles, letter-spacing −.02em |
| Card title (H2) | Sora | 15 / 600 | |
| Body | Sora | 14 / 400 | Lists, transcripts, line-height 1.55 |
| Small | Sora | 12 / 400 | Row subtitles |
| Label | JetBrains Mono | 11 / 400 | Uppercase, letter-spacing .08em, `--mute` |
| Numbers | JetBrains Mono or Sora | | Always `font-variant-numeric: tabular-nums` |
| Script prompt | Sora | 30 / 500 | Script reader, line-height 1.45 |
| Live line | Sora | 21 / 400 | Spoken line, unsaid words in `--faint` |

Mono is used for timestamps, scores, counts, clock, pills and labels. Sora for everything people read as sentences.

Phone: Display 28, H1 24, script prompt 21.

---

## 3. Shape and space

| Token | Value | Use |
|---|---|---|
| `--r-s` | 12px | Icon tiles, small chips |
| `--r-m` | 18px | Inner cards, KPI tiles, hint |
| `--r-l` | 24px | Main panels |
| `--r-p` | 999px | Buttons, pills, tabs, search |
| Rows | 14px | Table rows, required points |

Spacing: 18px grid gap and card gap, 24px card padding (30–34px on hero and script cards), 28px page gutter on desktop, 16px on phone.

Layout: 88px glass rail on the left, 12-column grid for content. Phone: rail becomes a bottom bar, grid stacks to one column.

---

## 4. Components

### Buttons
| Variant | Look | Use |
|---|---|---|
| Primary | Teal gradient `140deg #7FE3C0 → #3FB68B`, `--teal-ink` text, teal glow shadow | One per view: Start, Go live, Review, Approve |
| Secondary | `rgba(255,255,255,.07)` fill, `.15` border | Read, Replay, Solo |
| Ghost | No fill, `--mute` text | Tertiary links: Progress, Read script |
| Danger | `--red` fill, white text | End call only |

Sizes: default 12/20 padding 14px text; `sm` 8/14 at 13px; `lg` 15/30 at 16px.
States: hover brightens; focus `2px solid --teal` outline, 3px offset; pressed `scale(.96)`.

### Status pills
Mono 11px, pill shape, a 6px dot in the same colour before the text.
`ok` teal (Passed, Closed) · `amb` amber (Ticket, Ticket open, Late) · `info` blue (In progress, Needs review) · `bad` red (Live, dot blinks) · neutral grey (New, None).

### Filter chips
Outline pill with a mono count. Active: teal tint fill and teal border.

### Segmented tabs
Glass pill container, 4px padding. Active tab: `rgba(255,255,255,.13)` with inner highlight. Used for Summary/Transcript, Duo/Solo, Agent/Team lead, Approve/Redo.

### Search
42px glass pill with a search icon; border turns teal on focus. Max 320px on desktop, full width on phone.

### Table
Mono uppercase header row in `--faint` over a divider. Rows are separate rounded tiles (14px) on `.03` fill, `.065` on hover. Selected or needs-attention row: teal tint plus 1px teal inset ring. Phone hides middle columns.

### Required point
Row with a 20px circle: empty (todo, faint text), teal ring with halo (now), filled teal with check (met, shows the timestamp).

### Speaker ring
Round avatar. Speaking: layered glow `0 0 0 6px / 14px` rings plus 50px blur in the speaker's colour. Listening: no glow, label in `--faint`.

### Waveform
32 bars, 4px wide, animating height. Colour follows whoever is speaking.

### AI hint
Gradient card (teal to blue tint), teal border and soft teal glow, spark icon tile, mono eyebrow "AI hint · <trigger>", 16px suggested line. Appears during the call when a cue is detected and leaves once acted on.

### Scoring pipeline
Four steps: Recording saved, Transcribing, Analyzing, Scoring. Each row: icon tile, name, detail, progress bar, percentage. Waiting at 45% opacity; running gets a teal border and tinted icon; done turns the icon solid teal with a check.

### Playback bar
Round play button, mono clock, scrubber made of speaker segments (teal agent, amber debtor), white playhead with glow, moment markers below (teal met, amber late). Clicking a key moment or flagged item seeks to it; the transcript highlights the current line.

### Score ring
Conic gradient in teal over `.08` track, panel-coloured centre, large tabular number, "/ 100" label.

### Debtor rating
Five star buttons (amber when on) plus tag chips (Realistic, Pushed back, Followed brief). Duo sessions only.

### Toast
Bottom centre pill, dark glass with teal border, teal check circle, slides up, auto-dismisses after 3.2 s.

### KPI tile
Mono label, 28px value, 12px delta line (teal for good, amber for watch).

### Icons
One set, 24px grid, 1.75 stroke, round caps and joins. Filled only for play, pause and star. Set: home, books, mic, chart, users, review, search, play, pause, check, spark, doc, arrow, lock, star, replay, rec, text, scan, gauge.

---

## 5. Motion

| Name | Spec | Use |
|---|---|---|
| Ease | `cubic-bezier(.16,1,.3,1)` | Default for everything |
| Enter | 0.6s, from `translateY(14px)`, blur 6px, opacity 0 | Every screen change |
| Slide | 0.4s, from `translateY(8px)` | List rows, staggered 40–50ms |
| Grow / Rise | 0.8–0.9s scale from 0 | Meters (from left), bars (from bottom) |
| Pop | 0.5s, 0.6 → 1.06 → 1 | Pills and buttons that appear |
| Countdown | 0.8s per number, ring stroke draws, number scales 1.5 → 1 with blur | 3, 2, 1, Live |
| Hint | 0.55s, rise 12px and scale .98 → 1 | AI hint arrival |
| Halo | 1.4s pulse | Waiting avatar in the lobby |
| Blink | 1s steps | Live dot |

`prefers-reduced-motion` turns all animation off.

---

## 6. Screens

**Agent:** Home (coaching ticket hero, last 6 scores, KPIs, practice queue) · Playbooks (bank list, filter chips, search, scripts table) · Script reader (step rail, prompt, debtor cue, scored point) · Role play hub (lobbies, Duo/Solo, new session) · Lobby · Countdown · Live (speaker stage, live line, AI hint, required points) · Scoring · Results (score ring, criteria, playback, key moments or transcript, metrics, AI coaching, debtor rating) · Progress (weekly trend, skills, history).

**Team lead:** Team (KPIs, filter chips, search, agent table with last-6 sparkline) · Session review (playback, synced transcript, AI score, flagged moments, Approve or Redo).

Coaching loop: QA AI flag → agent practice → AI score → TL review → ticket closed, with status updated on both sides.

---

## 7. Content rules

- Sample names and banks only (Amihan, Harbor, Lakbay, Bayanihan Demo Bank). No real client data.
- Public material shows low or medium breach examples only, never critical or compliance-risk cases.
- Debtor and agent lines stay in Taglish as spoken; UI chrome is English.
- Headers plainly name what is on the screen.
- No em dashes in UI copy.
