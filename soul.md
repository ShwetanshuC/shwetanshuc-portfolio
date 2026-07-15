# SOUL.md — /web-development/ Design DNA

This document is the source of truth for the standalone `/web-development/` page.
It exists because the first two passes at this page kept drifting back toward
generic "AI startup" visual language — gradient pills, card-with-shadow grids,
chip-tag rows, centered-everything hero blocks. Every rule below is written
as a direct correction against that drift, anchored to six reference images
the client supplied. Read this before touching any CSS or template on this
page. If a change can't be traced to a rule here, it doesn't belong on the page.

---

## 0. The reference set, read literally

**Ref 1 — Arjun Rawal (personal site).**
A near-empty white canvas. Seven photographs scattered around the edges like
loose polaroids — each at a slightly different rotation (-4° to +4°), soft
drop shadow, no border, no card chrome around them, no grid alignment to
each other. Dead center: a name in a warm, soft-terminal serif, not bold,
not italic-for-effect — just quietly confident. Below it, an email in a
plain small sans. Below that, four monochrome icon glyphs in a single row,
touching nothing. Below that, three lowercase words — `reading` `projects`
`research` — as the *entire* navigation. No button anywhere. No visible nav
bar. No card ever touches another card. The whole page is negative space
with nine small elements placed in it.

**Ref 2 — TwoSet Violin (site footer).**
Pure black. Every interactive element is a **thin 1px white-stroke outline**
on transparent fill — never a filled/gradient button. Labels are small,
tracked, uppercase, or plain sentence case with no styling flourish. An
email field is a dark bordered rectangle sitting directly beside its
outlined submit button — same height, same corner radius, visually one
unit. A row of plain icon glyphs (no circles, no backgrounds behind them)
sits by itself with generous space above and below. Copyright is a single
small centered line. Nothing glows. Nothing has a shadow.

**Ref 3 — Hokusai, *The Great Wave*.**
Not a UI reference — a *motion and composition* reference. One dominant
organic curve, foam breaking into hundreds of small discrete dots at the
crest, small boats (small deliberate details) caught inside the sweep of
the larger form. The lesson: motion should read as one continuous curve
made of many small independent parts, not many separate small animations
competing for attention.

**Ref 4 — warm living room.**
Pure mood/color reference. Warm amber light sources (visible bulbs, not
ambient fill) pooling on specific surfaces, everything else falling to
near-black. Light is *directional and sourced*, never a flat glow wash.
This is the model for how amber is allowed to appear on the page: as a
single warm light hitting one thing, not a tint over everything.

**Ref 5 — Arkitektkontoret (architecture studio site).**
Off-white/cream field, a thin black hairline rule framing the entire
viewport like a picture mat. One large architectural photograph occupies
roughly a third of the width — nothing else competes with it. A small
caption sits beside it in a plain sans: `Skeilunden　2004` — project name
and year, nothing more, no card, no border around the caption. Top-left:
a bold grotesk wordmark. Top-right: two plain nav words, no button styling.
Bottom of the photo: a `+ Alle prosjekter` text link with a plus glyph,
not a button. A tiny hand-drawn leaf mark sits bottom-left as the only
illustrative flourish on the entire page. This is the model for how a
"showcase section" should look: one real asset, one small plain caption,
acres of surrounding whitespace, zero card chrome.

**Ref 6 — flagged as the failure case.**
The current `01 / Product & Inventory Sites` section: a browser-chrome
mockup with fake macOS traffic-light dots, a fabricated "yourbusiness.com"
inventory grid with invented product cards, pill-shaped tag chips with
visible borders (`Filterable catalog` `Staff admin panel` …), a large
ghost "01" numeral, box-shadow under the mockup. This entire pattern —
fake product screenshots, bordered pill chips, drop-shadowed card —
is the thing to delete, everywhere it appears on the page.

---

## 1. The one-sentence brief

**A near-empty black gallery wall with one warm light source, a few real
artifacts hung on hairline rules, and nothing that looks like it came out
of a component library.**

---

## 2. Anti-patterns — banned outright, no exceptions

- Filled gradient buttons (amber→orange or otherwise). Buttons are text or
  a 1px hairline outline. Never a filled shape as the primary CTA.
- Chip/pill tag lists with visible borders around each word
  (`⟨Filterable catalog⟩ ⟨Staff admin panel⟩ …`). If a list of features is
  needed, it's plain text separated by a middle dot (`·`), matching Ref 5's
  caption style.
- Fabricated browser-chrome mockups (fake traffic-light dots, invented
  product grids, made-up URLs). If there's no real screenshot, the section
  runs on typography and whitespace alone — it does not invent a screenshot
  to fill the space. Only genuine artifacts belong on the page: the
  before/after drag sliders (real client sites) are the *only* acceptable
  "proof" widget.
- Cards with `box-shadow` used as the default container for anything
  (testimonials, process steps, showcase content). Hairline 1px dividers
  replace card edges everywhere.
- Centered-everything layout rhythm. Every section in a row centered is
  the single strongest "generated" tell — see Ref 1 and Ref 5, both of
  which are asymmetric (content left, art right, or vice versa; numbers
  and captions left-anchored, not centered).
- More than two typefaces. See §3.
- Glow/blur drop-shadows on text or buttons as a decorative default. Glow
  is reserved for the hero dot-title only, and only because it's a literal
  light source (Ref 4's rule: light is sourced, not washed).
- Icon-in-a-circle or icon-in-a-filled-square treatments. Icons stand
  alone on the background, exactly as in Ref 1 and Ref 2.
- A section that doesn't move at all on scroll or hover. Static blocks of
  text stacked with zero motion is the second-strongest "generated" tell
  once the chip/card issues are fixed. See §5.

---

## 3. Typography

Two typefaces, each with exactly one job. Never a third.

**Identity face — `Fraunces`** (Google Fonts, variable, soft-terminal serif
with genuine warmth — the closest legally-available match to Ref 1's
name-mark and close in spirit to Ref 5's confident wordmark treatment).
Used *only* for:
  - The corner nav ("Personal Brand" / "Contact")
  - The hero eyebrow-adjacent short identity text, if any
  - Section numerals/captions in the architecture-caption style (§6.4)
  - Pull-quote testimonial text
  - Never for paragraphs of body copy — it's a display/caption face, not
    a reading face.

**Body/utility face — `Inter`**. Used for everything else: paragraph copy,
button labels, form fields, the hero subhead. Weight does the work of
hierarchy (400 body, 500–600 emphasis) — never a third face for "emphasis."

**Rule of thumb:** if a piece of text is *naming* something (a person, a
project, a section), it can be Fraunces. If it's *explaining* something,
it's Inter.

---

## 4. Color

```
--wf-black        #030303   canvas
--wf-panel        #0a0a0a   only for the rare full-bleed section shift
--wf-line         rgba(255,255,255,.10)   hairline dividers
--wf-line-soft    rgba(255,255,255,.06)   section-boundary hairlines
--wf-text         #f2f0ed   primary text (warm off-white, not pure #fff)
--wf-text-muted   rgba(242,240,237,.55)
--wf-text-faint   rgba(242,240,237,.32)   ghost numerals, captions
--wf-amber        #ff9c4d   the one warm light — buttons-on-hover, the
                              dot title, a single underline, never a fill
```

Amber appears in exactly three places on the whole page: the dot-orbit
title, hover states on text links/outlines, and the single accent word in
a section title (`em`). It never becomes a background fill, a card border
at rest, or a chip background. If in doubt, cut the amber.

---

## 5. Motion

Ref 3's lesson, operationalized: one continuous, physically-motivated
curve per moment, built from many small parts — not a dozen unrelated
`fade-in` timers firing at once.

**Hero entrance (the big moment):**
1. On load, the dot shader starts in a *scattered* state
   (`u_spreading` high, ~1.0, dots wandering wide inside their cells) and
   *no* mask applied yet — a loose amber haze, not the title shape.
2. Over ~1.8s (`cubic-bezier(0.16,1,0.3,1)`), `u_spreading` eases down to
   its resting value (~0.4) while the text mask fades/wipes in — the dots
   visibly *settle* into the letterforms rather than snapping to them.
   This is the literal "title animated out of dots" the client asked for,
   built from a parameter the real shader exposes rather than a fake
   per-dot tween.
3. Once settled, the dots keep drifting forever at low `speed` — idle
   motion never fully stops on this page, matching a light source that's
   always live (Ref 4).
4. The hero content (eyebrow, subhead, CTAs) is on its own gentler
   stagger, offset to *finish after* the dots settle, not compete with them.

**Cursor parallax:** the hero content shifts a few px opposite the cursor
(subtle, ≤12px range, spring-damped) — the one "designer portfolio" tell
that's currently completely absent from the page.

**Scroll:** sections reveal with translateY + slight blur-to-sharp
(not just opacity), staggered by ~90ms per child. Hairline dividers grow
from 0 → 100% width as they enter view rather than appearing instantly —
a divider drawing itself reads as considered in a way an instant line
never does.

**Hover:** any photographic/screenshot element (the before/after slider
cards) gets a small rotation + lift on hover, echoing Ref 1's
scattered-polaroid physicality — nothing in this design is perfectly
axis-aligned and static under a cursor.

**Reduced motion:** every effect above degrades to its settled end-state
instantly. No exceptions, no partial motion left running.

---

## 6. Layout grammar

### 6.1 Corner identity, not a navbar
Two elements, fixed top corners, Fraunces italic-leaning weight:
- Top-left: `Personal Brand` → home. Text only, no border, no pill.
- Top-right: `Contact` → contact page. **Plain text, not a button** —
  same visual weight as the left link, distinguished only by being on
  the right, exactly as Ref 1 gives its nav zero chrome and Ref 2 never
  puts a border around a text-only label.

### 6.2 Hero
Asymmetry is allowed here to break (Ref 1's hero *is* centered — it's the
one place centering is earned, because it's a single dominant identity
mark on an otherwise empty field). Everything below the hero moves to
asymmetric layout.

### 6.3 Showcase sections (the three site-type sections)
No mockup. No card. Structure, left-anchored:
```
01 — Inventory & Catalog          ← Fraunces, small, tracked, faint
Product & Inventory Sites         ← Fraunces, large, warm off-white
Filterable catalogs, inventory    ← Inter, muted, max ~60ch
management, real-time pricing...

Filterable catalog · Staff admin panel · Real-time pricing · AWS hosted
                                   ← Inter, faint, plain text, dot-separated
```
A thin hairline rule sits above the numeral, animating in on scroll
(§5). No image, no mockup, no chip borders. The section is allowed to be
*mostly empty* — that emptiness is the design, not a placeholder for a
missing asset.

### 6.4 Transformation section (before/after)
The only section allowed a "proof" widget, because it's real (a live
drag-comparison of an actual site rebuild). Cards lose their panel
background/box-shadow in favor of a single hairline border. Labels
(`Before` / `After`) are plain small caption text, not colored pill tags.

### 6.5 Process, testimonials, CTA
Process: plain numbered list, hairline rule under each step, no bordered
box. Testimonials: a single large Fraunces pull-quote, centered, no card,
no avatar circle — rotate through multiple quotes if more than one exists
rather than a card grid. CTA: unchanged in spirit — Fraunces heading,
Inter subtext, one outline button.

### 6.6 Footer
Match Ref 2's spare dark footer: one line, small, centered or split
between a copyright and a plain `Contact` text link. No icon row unless
real social links exist for this context (they don't, on this page —
omit rather than invent).

---

## 7. When something doesn't have a rule here

Ask: *would this survive on Ref 1 or Ref 5's page?* If it needs a card,
a shadow, a gradient, or a chip border to make sense, the answer is no —
find the version of it that's just typography, whitespace, and a hairline
rule instead.
