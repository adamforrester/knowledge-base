---
okf_version: "0.1"
type: component-brief
title: Icon
description: A primitive with two load-bearing decisions — is this glyph meaningful or decorative, and how is the set delivered. A field-truth study of the decorative-by-default accessible-name matrix, the icon-only-button trap (the Icon is never the interactive element), the geometric/optical anatomy, the currentColor sizing-and-colour model, the delivery trade (inline-SVG default, legacy icon fonts dead, variable WOFF2 a legitimate modern path), and the set-as-versioned-API deprecation problem. Promoted to a dual-agent run.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [glyph, symbol, svg-icon]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Icon

> Icon is a primitive, but a more contested one than Divider — the field converges on the essentials and splits, genuinely, on delivery. Two decisions carry the whole component: is this glyph *meaningful* or *decorative* (which determines how, or whether, it reaches assistive tech), and how is the *set* delivered to the page (inline SVG, sprite, or — now again — a variable font). Get those two right and the rest is geometry and taxonomy. The recurring failure isn't drawing the glyph — it's treating the Icon as a button, naming it twice, or assuming the delivery question was settled when it has just reopened.

---

## 1. Framing

An icon is a small vector glyph standing in for a concept. What it *isn't*: a button (the most common and most damaging conflation — §5), an illustration (larger, narrative, its own component), or a logo. The contemporary icon is not a static imported asset but a strongly-typed, version-controlled DOM node that has to route itself correctly into the accessibility tree, scale against adjacent type without thrashing layout, and tree-shake out of the bundle when unused (external). Two questions carry it: **semantics** — is the glyph meaningful (and so owed an accessible name) or decorative (and so owed silence, §6) — and **delivery** — inline SVG vs. sprite vs. variable font, a real engineering trade with accessibility, bundle, and rendering-performance consequences (§11). The single artefact that actually matters is the **set** — a named, versioned vocabulary of glyphs on a shared grid, governed like an API (§10).

## 2. Anatomy and parts

A single `<svg>` (the practice's default delivery), carrying *either* an accessible-name mechanism (`role="img"` + `aria-label`, or an SVG `<title>`) *or* `aria-hidden="true"` — never both, and that choice is the whole accessibility story (§6). But the structural substance of an icon is **geometric governance**, where the field converges hard (external):

- **The grid.** Icons are drawn on a square, base-4/base-8 artboard so vector points land on the hardware pixel grid and strokes don't blur between pixels. The field standardises on a small fixed set — 16 / 20 / 24 (Carbon adds 32; Atlassian 12/16; Polaris 20) — and *prohibits arbitrary sizes*. Off-grid scaling is the first thing an icon system must forbid.
- **Stroke harmony.** Stroke weight is a constant tuned to the type alongside it — Atlassian's 1.5px icon stroke matches its 1.5px typeface stroke (the "squint test"); Material's baseline is a 2dp stroke. A glyph whose weight fights the adjacent text reads as foreign.
- **Optical alignment, not bounding-box alignment.** A glyph's bounding box is rarely its visual centre of mass, so inline icons need an optical baseline shift — Material Symbols shifts the glyph down ~11.5% of the text size to align its centre with the x-height. The recurring polish bug is an icon sitting a pixel low beside its label.

The "anatomy" most people picture (the paths) matters less than this governance; the set's value is consistency of grid, stroke, and optical centre across every glyph.

## 3. Properties / API

The converged surface — and the field is migrating toward **deliberately constrained, declarative** APIs that make the accessible, on-grid path the only easy one (the "pit of success", external):

- **which glyph** — a `name`/`icon` prop typed to the set's vocabulary (string literals, not free strings), or per-glyph components (`<IconSearch/>`).
- **`size`** — **enumerated** (`sm`/`md`/`lg`), mapping to the fixed pixel grid, *not* arbitrary integers — so the glyph snaps to the grid and can't be scaled off it.
- **colour / `tone`** — defaults to **`currentColor`** (inherit), with an optional **semantic token** (`critical`, `subdued`, `success`) — and the API should **reject raw hex** so contrast is enforced centrally (external — Polaris's `tone`, Atlassian's auto-colouring).
- **`label`** — the **sole accessibility gateway**: its presence makes the icon meaningful and named; its absence makes it decorative and hidden (§6). Primer's Octicon and Carbon both key the entire ARIA decision off this one prop.

Width, height, and stroke are **bound to the grid and token scale, not exposed** — an icon system that lets every consumer set arbitrary dimensions has no grid. (The practice ships per-glyph components for tree-shaking, *or* a `name`-prop component over a sprite/font for very large sets — §11.)

## 4. States and variants

An icon has **no runtime states of its own** — it is not interactive, so hover/focus/pressed/disabled belong to whatever control wraps it; the architectural goal is to restyle without DOM repaints or redundant asset fetches (external). The real axes are colour-state and the fill/weight variant, and the field splits on *how* to express multi-tone:

- **`currentColor` inheritance** — the standard: the glyph inherits the cascading `color`, so it tracks its host control's `:hover`/`:disabled`/error states instantly, no JS reconciliation (external).
- **Semantic-token colour** — Polaris-style explicit `tone`, insulating an error glyph from a rogue cascade turning it invisible (external).
- **Multi-tone / hierarchical** — the frontier. SF Symbols ships four rendering modes (**Monochrome / Hierarchical** — one tint, opacity varied by layer depth / **Palette** — independent colours per layer / **Multicolor** — intrinsic semantic colours); Carbon does two-tone from a single node via `[data-icon-path="inner-path"]` CSS selectors; Material does it via variable-font axes (below) (external).
- **Variable-font axes** — Material Symbols exposes `wght` / `FILL` / `GRAD` / `opsz` as continuous axes in one file: outlined→filled is `FILL: 0→1` via `font-variation-settings`, and `GRAD` optically thickens a glyph *without* widening it (vital for keeping weight legible on dark backgrounds) (external).

Variants therefore are: size (the grid), fill/weight (outlined↔filled, where the set supports it), and the colour-expression model. The meaningful/decorative split is the semantic axis, not a visual variant.

## 5. Usage guidance

**Use** to reinforce meaning, speed scanning, or label an action *alongside* text where space allows. The field is firm that **few icons are universally understood** — an icon beside a visible label is a wayfinding anchor for returning users, not a replacement for the words (external — Atlassian).

**Don't** use an icon as the sole label for a meaningful action without giving the control an accessible name (§6); crowd a UI with competing icons (it dilutes the genuinely semantic ones); or invent one-off glyphs outside the set (the set is the discipline — an ad-hoc glyph is debt).

**The icon-only-button is the key trap, and it is everywhere.** An icon-only control is a **Button** (see button) with an `aria-label` and a proper hit target — the accessible name and the target size live on the *button*, and the Icon inside is `aria-hidden`. An Icon component is never itself the interactive element; the moment it appears to be, the affordance is on the wrong node. The field formalises the separation (Salesforce's distinct `lightning-button-icon`; Base Web's `isIconButton`) precisely because the glyph lacks focus management, keyboard listeners, and — decisively — a touch target (§6). This is the inverse framing of Button's icon-only case; the two briefs meet here.

## 6. Accessibility

The theory is in 14-accessibility; the Icon-specific decision is a three-way matrix, and almost every icon bug is picking the wrong cell (both agents):

| Case | Visible text? | Developer action | Resulting DOM | AT behaviour |
| --- | --- | --- | --- | --- |
| **Decorative** | yes (text beside it), or ornament | omit `label` | `aria-hidden="true"` | silently bypassed |
| **Meaningful standalone** | no | `label="Status"` | `role="img"` + `aria-label` | "Status, image" |
| **Inside an icon-only control** | no | label on the *wrapper* | `<svg aria-hidden>` inside a labelled `<button>` | reads the wrapper, ignores the svg |

- **Decorative is the default and the most common correct answer.** A named icon beside its own text double-announces — "Email, Email" — which is real navigational friction; the decorative glyph must be *forcefully* hidden (external). Carbon and Primer both default to `aria-hidden` and key the override entirely off the presence of `label`.
- **`role="img"` is mandatory for a meaningful standalone icon** — without it many screen readers ignore the `aria-label` on a raw `<svg>` and leave the user on an unannounced stop (external).
- **The icon-only-button is an accessibility contract, not just architecture.** The *wrapper* `<button>` carries the `aria-label` (or sr-only text); the inner `<svg>` is `aria-hidden`. Reversing it — labelling the glyph, silencing the button — causes ghost focus rings and unpredictable AT behaviour (external). And the **touch target lives on the wrapper**: a 16–20px glyph cannot itself be the target, so the button supplies padding to the **44×44px** (WCAG/Apple; 48 on Android) minimum while the glyph stays visually tight (external).
- **Contrast:** a meaningful icon must clear **3:1** non-text contrast (1.4.11; Primer enforces it on its colour scales); a decorative icon is exempt. An icon must never be the *sole* carrier of meaning that colour conveys (1.4.1).
- **WCAG SCs:** **1.1.1 Non-text Content** (meaningful → text alternative; decorative → hidden), **1.4.1 Use of Color**, **1.4.11 Non-text Contrast**, and **2.5.8 Target Size** — the last being the *wrapping control's* concern, not the glyph's.

## 7. Content guidelines

The "content" of an icon is its accessible name *when meaningful*: a concise noun or verb naming the concept or the action it triggers — "Search", "Delete" — matching what the icon depicts and the action it fires, not the glyph's internal asset name. A decorative icon has no content and takes no name. The glyph's *design* has content rules too (external): rely on **globally established metaphors**, not local idioms; keep metaphors **minimal and additive** because complex ones turn to mud at 16px (Spectrum); and avoid depicting **physical hardware** (bezels, devices) that dates the moment the device does — the floppy-disk "save" glyph endures precisely because its meaning has transcended the obsolete object (Apple HIG).

## 8. Motion and transition

Static by default. Icons move only as part of a state transition they belong to — a chevron rotating on expand, a glyph cross-fading outlined→filled on activation, a spinner — and that motion is owned by the host component and honours reduce-motion there (see 18-motion-foundations, 19-motion-implementation-web). Two implementation realities (external): morphing SVG *paths* (hamburger→close by recomputing coordinates) needs heavy JS interpolation and is best avoided on the main thread; whereas a **variable-font** icon animates `font-variation-settings` (e.g. `FILL: 0→1`) with a plain CSS transition, hardware-accelerated by the text engine and free of DOM reflow — a genuine motion advantage of the variable-font delivery (§11). An Icon has no inherent motion of its own.

## 9. Internationalization

**Directional icons must mirror in RTL** — back/forward arrows, play, send, undo/redo, list indentation, alignment, reading-direction indicators — via logical flipping (`transform: scaleX(-1)` when `dir="rtl"`). **Non-directional icons must not mirror** — a clock stays a clock; a magnifying glass, a logo, a car keep their orientation. The robust pattern is **per-glyph metadata** — an `isMirroredInRTL` flag on each glyph so the component automates the transform and individual developers don't make subjective (often wrong) calls across the codebase (both agents). Some glyphs are culturally loaded — a checkmark, a waste bin, hand gestures — and need locale review rather than blind reuse. (See 13-internationalization-and-rtl.)

## 10. Naming

`Icon` is universal as the component name; the contested layer is the **set's identity and per-glyph taxonomy** — Material Symbols, GitHub Octicons, Apple SF Symbols, Carbon icons, Spectrum's Workflow and UI families. Two taxonomy styles (external): **literal** names the geometry (`magnifying-glass`, `chevron-right`), **semantic** names the function (`search`, `next`) — and semantic breaks down at scale when one glyph serves many actions. The field's resolution, which the practice adopts: **literal names for the immutable primitive tokens, semantic names at an alias layer on top.**

The hard problem is **deprecation and rename**, and it is a breaking change because a missing glyph fails silently (compile error, or worse, an invisible gap in production). The mature pattern is an **alias-token architecture**: the raw SVGs are immutable global tokens; the system exports alias tokens (e.g. `icon-primary-action`) pointing at them, so changing a metaphor is a central remap with zero downstream edits (external). For genuine removal, Atlassian's approach is the gold standard: **version-pin the legacy set** behind a deprecated entry point (`@atlaskit/icon/glyph`) while the new set lands in a new one (`/core`), *and* ship an **ESLint/AST auto-fixer** that rewrites consumers' import paths and component calls on upgrade (external). The icon set is an API; renames need codemods, not changelogs. Aliases to map in docs search: `glyph`, `symbol`, `svg-icon`, plus per-glyph synonyms (`trash`/`delete`/`bin`).

## 11. Implementation notes

Delivery is the genuinely contested decision, and the second pass reopened it: **legacy icon fonts are dead, but the *font* delivery model is not** (external).

- **Inline SVG (per-glyph components) is the practice default** — tree-shakeable (ship only used glyphs), styleable via `currentColor`, accessible, request-free, no FOUC. It is what Polaris, Atlassian, Spectrum, and Primer ship. Its cost is **DOM bloat**: every glyph injects its full path set into the document, and a dense dashboard with hundreds of icons inflates the node count, layout cost, and hydration time — to the point that Google's own measurements have font glyphs rendering materially faster than inline SVG in high-frame-rate tests (external, *verify the specific figure*).
- **Legacy icon fonts are an anti-pattern — don't ship new ones.** PUA/ligature glyphs render as tofu or a stray letter on load failure, force whole-library downloads, resist per-glyph/multi-tone colour, are mis-announced by AT, and shatter when a dyslexic user overrides fonts (external).
- **Variable WOFF2 fonts are a legitimate modern path — the real reopening.** A variable font encodes *infinite* weight/fill/optical-size permutations in one compact, cached payload with a minimal DOM footprint; matching that with inline SVG means exporting dozens of files per glyph and destroying the tree-shaking win (external — Material Symbols). **The practice's decision rule:** for a **locked, fixed-stroke** design language, ship **tree-shaken inline SVG** (the safest, most resilient default); for a system that genuinely needs **multi-axis / optical-sizing / dynamic-weight** glyphs, a **variable WOFF2 font** is the better engineering path. The choice follows the design language, not fashion.
- **SVG sprite** (`<use href="#icon">`) is the middle ground — one cached document, less DOM bloat than inline, but harder to tree-shake and with cross-document/`currentColor` quirks to verify.
- **Optical alignment with text** (cap-height/x-height, not bounding box) and the grid-snapping enum sizes (§2, §3) are the non-negotiable polish.

(The field's through-line, §13: the delivery answer is downstream of the *real* invariant — whatever the mechanism, the DOM presented to AT must be semantic, declarative, and correctly labelled.)

## 12. Related and alternative components

- **Composes with:** Button (icon-only and icon+text — the §5 boundary), Link, Text Field (prefix/suffix adornments — see text-field §2), Select (option/trigger visuals — see select), Menu, Avatar (an icon is the standard image-load *fallback*, promoted to `role="img"` with a generic label — external), Badge/Tag (a 12–16px icon paired with condensed status text — see Tag/Badge when briefed).
- **Alternative to:** Illustration (larger, narrative), Logo, Thumbnail (a preview *image* of content/product, not an interface metaphor — external), and Emoji (which carries its own platform a11y semantics and shouldn't be a UI icon).
- **Supersedes:** legacy icon fonts; ad-hoc inline SVGs drawn outside the set.
- **Superseded by:** nothing.

(See 03-component-library for the system-level component model, and 29-per-component-documentation-template for the docs page this feeds. The Button brief's icon-only case and this brief's §5 are the same boundary from two sides.)

## 13. Field POV evolution

The external pass frames the history as a pendulum between **network** and **rendering** optimisation, and the practice adopts it:

1. **HTTP/1.1 era** — connection limits favoured CSS sprites and legacy icon fonts to minimise requests.
2. **HTTP/2 era** — multiplexing dissolved the request bottleneck, and the field pivoted hard to tree-shaken **inline SVG** to cure the accessibility and FOUC failures of font hacks.
3. **Density era (now)** — inline-SVG **DOM bloat** has become the new bottleneck as interfaces grow denser and design languages demand parametric interpolation (optical sizing, responsive weight, smooth micro-motion), pulling the field toward a **hybrid**: variable WOFF2 fonts (Material) for parametric flexibility and a small DOM footprint, alongside ever-better AST tree-shaking for SVG (Atlassian, GitHub).

Secondary movements: **multi-tone/variable-fill** as a state pair (outlined↔filled) rather than two unrelated glyphs; and the **set-as-versioned-API discipline** hardening into alias maps, deprecation entry points, and rename codemods. The consensus: the delivery mechanism is secondary to the strict, declarative, correctly-labelled accessible API surface.

## 14. Sources cited

Conservative dating (the external pass supplied precise, largely 2026-stamped versions — Carbon React v1.109.0, Octicons v18.2.0, Atlassian Icon v22.19.0, Base Web v18.1.0 — held loosely and unverified; `last-audited` in frontmatter is the re-run trigger):

- Google Material Symbols — variable axes `wght`/`FILL`/`GRAD`/`opsz`, the ~11.5% optical baseline shift, the variable-font-vs-SVG delivery argument (Material, 2024–2026).
- Apple SF Symbols / HIG — the four rendering modes (Monochrome/Hierarchical/Palette/Multicolor), stroke-weight consistency, the no-physical-hardware metaphor rule (Apple HIG, 2024).
- GitHub Primer / Octicons — the `aria-label`-inferred decorative/semantic smart component, 3:1 contrast enforcement, two-grid (16/24) sizing (Primer, 2024–2026).
- IBM Carbon — 16px artboard + enumerated sizes, `aria-hidden`-by-default, two-tone via `[data-icon-path]` selectors (Carbon, 2024–2026).
- Atlassian Design System — 1.5px stroke "squint test", `glyph`/`size`/`label` constrained API, the alias-token architecture and the `/glyph`→`/core` + ESLint/AST deprecation migration (Atlassian, 2024–2026).
- Adobe Spectrum — Workflow/UI icon families, metaphor-legibility-at-16px guidance, `<sp-icon>` Web Component delivery (Spectrum, 2024–2026).
- Shopify Polaris — `Icon` (`source`, `tone`, `accessibilityLabel`), 20px viewBox, rem-global/em-inline sizing (Polaris, 2024–2026).
- Uber Base Web — `Icon` overrides, `isIconButton`, the Avatar image-fallback-to-icon pattern (Base Web, 2024).
- Salesforce Lightning — distinct `lightning-button-icon` formalising the icon-vs-icon-button separation (2024).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.1.1, 1.4.1, 1.4.11, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: icon
  name: Icon
  aliases: [glyph, symbol, svg-icon]
  category: foundations
  status: stable
description: >
  Small vector glyph rendering a concept. Decorative (aria-hidden) by
  default; meaningful standalone gets an accessible name; inside an
  icon-only control the CONTROL is named and the icon is hidden. Not a
  button, not an illustration, not a logo, not a thumbnail.
anatomy:
  grid: "square base-4/8 artboard; fixed sizes 16/20/24 (+32); arbitrary scaling forbidden"
  stroke: "constant weight tuned to the typeface (Atlassian 1.5px squint test; Material 2dp)"
  optical: "baseline shift (~11.5% down, Material) to align glyph centre to x-height — not bounding box"
api:
  delivery: "per-glyph inline-SVG components (tree-shakeable) | name-prop over sprite/variable-font for large or multi-axis sets"
  philosophy: "pit of success — the easy path is the accessible, on-grid one"
  props:
    - {name: name, type: string (typed to set vocabulary), required: false, description: which glyph; or per-glyph components}
    - {name: size, type: enum, values: [sm, md, lg, xl], default: md, required: false, description: enumerated, snaps to the pixel grid — NOT arbitrary integers}
    - {name: tone, type: enum/token, default: inherit (currentColor), required: false, description: semantic token; REJECT raw hex so contrast is enforced centrally}
    - {name: label, type: string, required: false, description: "the SOLE a11y gateway — present => meaningful (role=img + aria-label); absent => decorative (aria-hidden)"}
  tokens-not-props: [width, height, stroke]
states:
  runtime: []          # not interactive — states belong to the host control
  colour-model: [currentColor-inherit, semantic-token]
  multitone: [monochrome, hierarchical, palette, multicolor]   # SF Symbols modes; Carbon [data-icon-path]; Material axes
variants:
  size: [16, 20, 24]
  fill: [outlined, filled]      # Material FILL axis 0->1 via font-variation-settings
  weight: [variable-where-supported]  # wght / GRAD (optical thicken without widening)
accessibility:
  wcag-criteria: ["1.1.1", "1.4.1", "1.4.11", "2.5.8"]
  matrix:
    decorative: "text beside it / ornament -> omit label -> aria-hidden=true (the DEFAULT)"
    meaningful: "standalone -> label -> role=img + aria-label (role=img MANDATORY or AT ignores the label)"
    in-control: "wrapper button carries aria-label; icon aria-hidden — never name both"
  contrast: "meaningful >=3:1 (1.4.11); decorative exempt; never sole carrier of colour meaning (1.4.1)"
  touch-target: "44x44px (48 Android) on the WRAPPER, not the glyph (2.5.8)"
content:
  label-pattern: "concise noun/verb naming the concept/action (Search, Delete); decorative => none"
  metaphor-rules: "global metaphors not local idioms; minimal/additive (mud at 16px); no physical-hardware depictions"
i18n:
  rtl: "directional glyphs mirror (scaleX(-1)); non-directional do not; per-glyph isMirroredInRTL metadata automates it; culturally-loaded glyphs need review"
motion:
  default: none
  variable-font: "animate font-variation-settings (FILL 0->1) via CSS transition — hardware-accelerated, no reflow"
  svg-path-morph: "heavy JS interpolation — avoid on the main thread"
implementation:
  default: "tree-shaken inline SVG for a locked fixed-stroke design language (safest, most resilient)"
  variable-font: "variable WOFF2 for multi-axis / optical-sizing / dynamic-weight systems (one compact payload, minimal DOM, infinite axes)"
  sprite: "<use href> middle ground — cached, less DOM bloat, harder to tree-shake / currentColor quirks"
  anti-pattern: "legacy ligature/PUA icon fonts (tofu on load fail, whole-library download, no multi-tone, AT mis-reads, breaks on font override)"
  tradeoff: "inline-SVG DOM bloat is the new bottleneck in dense UIs (Google: font glyphs render materially faster in some tests — verify figure)"
composition:
  composes-with: [button, link, text-field, select, menu, avatar, badge, tag]
  alternative-to: [illustration, logo, thumbnail, emoji]
  supersedes: ["legacy icon fonts", "ad-hoc inline SVGs outside the set"]
  superseded-by: null
notes:
  contested:
    - "delivery — inline-SVG (default for fixed-stroke) vs variable WOFF2 (multi-axis) vs sprite; legacy fonts dead"
    - "sizing model — px-grid vs em (we bind to the grid; em on the outer container inline with text)"
    - "literal vs semantic taxonomy (literal tokens + semantic alias layer); the rename/deprecation codemod problem"
  trap: "icon-only-button — the Icon is never the interactive element; the wrapping Button is (name + 44px target on the wrapper)"
  evolution: "HTTP/1.1 sprites+fonts -> HTTP/2 inline SVG -> density-era hybrid (variable fonts + AST tree-shaking)"
  unverified: "external-supplied 2026 version numbers; the 'font glyphs ~5x faster than inline SVG' figure"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-icon/` (15 June 2026) — **promoted from claude-only to dual-agent** at the practitioner's request; the original solo brief flagged the delivery trade as the spot most likely to benefit from an adversarial pass, and it did. Both agents converged on the load-bearing calls — decorative-by-default accessible-name routing keyed off a single `label` prop (with `role="img"` mandatory for meaningful standalone glyphs), the icon-only-button trap (the Icon is never the interactive node — name and 44px target live on the wrapping Button), `currentColor` colouring, grid-snapped enum sizes over arbitrary integers, per-glyph `isMirroredInRTL` metadata, and the set-as-versioned-API discipline. The external pass materially sharpened the brief: the geometric/optical anatomy (base-4/8 grid, stroke-to-typeface harmony, the ~11.5% optical baseline shift), the SF Symbols four rendering modes and Material's `wght`/`FILL`/`GRAD`/`opsz` variable axes, the constrained "pit of success" API (reject raw hex, enumerated sizes), the metaphor content rules (no physical hardware; the floppy-disk endurance), the alias-token + `/glyph`→`/core` + ESLint/AST deprecation migration, and — the decision the second pass most changed — the **delivery position**: the solo brief's blanket "icon fonts are an anti-pattern" was refined to *legacy ligature/PUA fonts are dead, but variable WOFF2 fonts are a legitimate modern path*, with the practice landing on a design-language-dependent rule (inline SVG for fixed-stroke systems, variable WOFF2 for multi-axis/optical-sizing systems) rather than a flat ban. Claude-pass contributions retained: the decorative-default emphasis against the role=separator-everywhere failure mode's icon analogue, the Button-brief boundary tie, and the token-not-prop discipline on dimensions. The external pass's 2026 version numbers and the "font glyphs ~5× faster than inline SVG" figure are flagged unverified pending `_source-text/` backing. The §15 schema is free-form per the catalogue design spec.*
