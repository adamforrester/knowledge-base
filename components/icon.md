---
okf_version: "0.1"
type: component-brief
title: Icon
description: A primitive with two load-bearing decisions — is this glyph meaningful or decorative, and how is the set delivered. A field-truth study of the semantic-vs-decorative accessible-name matrix (decorative by default), the icon-only-button trap (the Icon is never the interactive element), the currentColor sizing-and-colour model, the inline-SVG-over-icon-font delivery call, and the set-as-versioned-API rename problem. A claude-only run, per the convergent-primitive rule.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [glyph, symbol, svg-icon]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Icon

> Icon is a primitive, but a more contested one than Divider — the field converges on the essentials and splits, quietly, on delivery and the sizing-and-colour model. Two decisions carry the whole component: is this glyph *meaningful* or *decorative* (which determines how, or whether, it reaches assistive tech), and how is the *set* delivered to the page (inline SVG, sprite, or font). Get those two right and the rest is tokens and taxonomy. The recurring failure isn't drawing the glyph — it's treating the Icon as a button, or naming it twice.

---

## 1. Framing

An icon is a small vector glyph standing in for a concept. What it *isn't*: a button (the most common and most damaging conflation — §5), an illustration (larger, narrative, its own component), or a logo. The two load-bearing questions are **semantics** — is the glyph meaningful (and so owed an accessible name) or decorative (and so owed silence) — and **delivery** — inline SVG vs. sprite vs. icon font, a genuine engineering trade with accessibility and bundle consequences (§11). Sizing and colour, which look like the substance of an icon system, are settled conventions by comparison: a token grid and `currentColor`. The single artefact that actually matters is the **set** — a named, versioned vocabulary of glyphs on a shared grid, governed like an API (§10).

## 2. Anatomy and parts

A single `<svg>` (the practice's default delivery), carrying *either* an accessible-name mechanism (`role="img"` + `aria-label`, or an SVG `<title>`) *or* `aria-hidden="true"` — never both, and the choice is the whole accessibility story (§6). Structurally there is nothing else; the real "anatomy" is the set the glyph is drawn from.

## 3. Properties / API

The converged surface: which glyph (a `name` prop on a single component, or per-glyph components like `<IconSearch/>`); `size` (from a token scale, not arbitrary pixels); colour (defaulting to `currentColor`, with an optional `tone`); and a `label` whose **presence is the semantic switch** — supplied, the icon is meaningful and named; omitted, it is decorative and hidden. **The practice ships per-glyph components** (the best tree-shaking) *or* a `name`-prop component backed by a sprite for very large sets; `size` from the token scale; `currentColor` by default with an optional `tone`; and the optional `label`. Width, height, and stroke are **bound to the grid and token scale, not exposed as props** — an icon system that lets every consumer set arbitrary dimensions has no grid.

## 4. States and variants

An icon has **no runtime states of its own** — it is not interactive, so hover/focus/pressed/disabled belong to whatever control wraps it. Variants are size (the 16/20/24 grid), a fill/weight axis where the set supports it (Material Symbols' `FILL`/`wght`/`GRAD`/`opsz`; SF Symbols' weights), and the meaningful/decorative split. Collapsed per the primitive-deviation rule.

## 5. Usage guidance

**Use** to reinforce meaning, speed scanning, or label an action *alongside* text where space allows.

**Don't** use an icon as the sole label for a meaningful action without giving the control an accessible name (§6); crowd a UI with icons that compete for attention; or invent one-off glyphs outside the set (the set is the discipline — an ad-hoc glyph is debt).

**The icon-only-button is the key trap, and it is everywhere.** An icon-only control is a **Button** (see button) with an `aria-label` and a proper hit target — the accessible name and the target size live on the *button*, and the Icon inside is `aria-hidden`. An Icon component is never itself the interactive element; the moment it appears to be, the design has put the affordance on the wrong node. (This is the inverse framing of Button's icon-only case — the two briefs meet here.)

## 6. Accessibility

The theory is in 14-accessibility; the Icon-specific decision is a three-way matrix, and almost every icon bug is picking the wrong cell:

- **Decorative** — an icon beside a visible text label, or pure ornament: `aria-hidden="true"`. The adjacent text already names the thing, and a named icon would double-announce ("Search, search"). **This is the default and the most common correct answer.**
- **Meaningful standalone** — an icon conveying information with no adjacent text: give it an accessible name via `role="img"` + `aria-label` (or an SVG `<title>`), so AT conveys the concept.
- **Inside an icon-only control** — the *control* carries the `aria-label`; the icon is `aria-hidden`. Name the control, never both (§5).

WCAG: **1.1.1 Non-text Content** (a meaningful icon needs a text alternative; a decorative one must be hidden), **1.4.11 Non-text Contrast** (a meaningful icon clears 3:1; decorative icons are exempt), **1.4.1 Use of Color** (an icon must not be the *sole* carrier of meaning that colour conveys). Target size (2.5.8) is the wrapping control's concern, not the glyph's.

## 7. Content guidelines

The "content" of an icon is its accessible name *when meaningful*: a concise noun or verb naming the concept or the action it triggers — "Search", "Delete" — matching what the icon depicts and the action it fires, not the glyph's internal asset name. A decorative icon has no content and takes no name.

## 8. Motion and transition

Static by default. Icons move only as part of a state transition they belong to — a chevron rotating on expand, a glyph cross-fading outlined→filled on activation, a spinner — and that motion is owned by the host component and honours reduce-motion there (see 18-motion-foundations, 19-motion-implementation-web). An Icon has no inherent motion.

## 9. Internationalization

**Directional icons must mirror in RTL** — back/forward arrows, send, undo/redo, list indentation, progress chevrons — via logical flipping (`transform: scaleX(-1)` or an RTL-specific glyph). **Non-directional icons must not mirror** (search, settings, a clock). Some glyphs are culturally loaded — a checkmark, a waste bin, hand gestures — and need locale review rather than blind reuse. The set should *mark which glyphs are directional* so consumers and the build don't have to guess. (See 13-internationalization-and-rtl.)

## 10. Naming

`Icon` is universal as the component name; the contested layer is the **set's identity and per-glyph taxonomy** — Material Symbols, GitHub Octicons, Apple SF Symbols, Carbon icons, Spectrum's Workflow and UI icon families. The practice ships a single **named, versioned icon set**, with per-glyph names as a stable vocabulary plus aliases (consumers reach for `trash` / `delete` / `bin` for the same glyph — alias them). The hard problem is **rename and deprecation**: when a glyph is renamed or retired, ship an alias map and a deprecation path with a codemod, never a silent break. The icon set is an API, and renames are breaking changes.

## 11. Implementation notes

- **Inline SVG (per-glyph components) is the practice default** — tree-shakeable so a screen ships only the glyphs it uses, styleable via `currentColor`, accessible, and request-free. The cost is bundle weight when a surface imports hundreds; that is the signal to consider a sprite.
- **SVG sprite** (`<use href="#icon">`) — one cached request, strong for very large sets used broadly, but harder to tree-shake, and cross-document `<use>` plus `currentColor` has historical quirks to verify.
- **Icon fonts are an anti-pattern now** — ligature/PUA glyphs render as tofu or a stray letter when the font fails to load, resist per-glyph and multi-tone colour, and are mis-announced by some assistive tech. Don't ship new icon fonts.
- **`currentColor` is the default colouring mechanism** — the glyph inherits text colour and so tracks its host control's states (hover, disabled, error) for free, which is why icon colour rarely needs to be a prop.
- **Size from the token scale (16/20/24) and align optically with text** — to cap-height/centre, not bounding box; the recurring polish bug is an icon sitting a pixel low beside its label.
- **Variable / optical-sizing axes** (Material Symbols' `FILL`/`wght`/`GRAD`/`opsz`, SF Symbols) are the frontier for sets that want icon weight to track adjacent type from one source — flag as emerging and verify tooling support before committing.

## 12. Related and alternative components

- **Composes with:** Button (icon-only and icon+text — the §5 boundary), Link, Text Field (prefix/suffix adornments — see text-field §2), Menu, Tag, and effectively every component with an affordance.
- **Alternative to:** Illustration (larger, narrative), Logo, and Emoji (which carry their own platform a11y semantics and shouldn't be used as UI icons).
- **Supersedes:** icon fonts; ad-hoc inline SVGs drawn outside the set.
- **Superseded by:** nothing.

(See 03-component-library for the system-level component model, and 29-per-component-documentation-template for the docs page this feeds. The Button brief's icon-only case and this brief's §5 are the same boundary from two sides.)

## 13. Field POV evolution

1. **Icon fonts → inline SVG** is essentially complete among field leaders; new fonts are no longer shipped.
2. **Variable / optical-sizing sets** (Material Symbols, SF Symbols) render weights, fills, and grades from one source, replacing multiple static cuts.
3. **The two-tone / variable-fill direction is growing** — outlined-vs-filled as a state pair (outlined at rest, filled when active) rather than two unrelated glyphs.
4. **Set-as-versioned-API discipline is hardening** — alias maps, deprecation paths, and rename codemods are becoming standard, treating the glyph vocabulary as a governed interface.

## 14. Sources cited

Conservative version dates (claude-only run; `last-audited` is the re-run trigger):

- Google Material Symbols — variable axes `FILL` / `wght` / `GRAD` / `opsz` (Material, 2024).
- Apple SF Symbols — weights, hierarchical / multicolor rendering (Apple HIG, 2024).
- GitHub Octicons — the 16/24 two-grid system (Octicons, 2024).
- IBM Carbon — icon library and sizing (Carbon, 2024).
- Adobe Spectrum — Workflow and UI icon families, sizing model (Spectrum, 2024).
- Shopify Polaris — `Icon` (`currentColor`, `tone`) (Polaris, 2024).
- Atlassian Design System, Uber Base Web — icon components (2024).
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
  button, not an illustration, not a logo.
api:
  delivery: "per-glyph inline-SVG components (tree-shakeable) | sprite via name prop for very large sets"
  props:
    - {name: name, type: string, required: false, description: which glyph (single-component+sprite); else per-glyph components}
    - {name: size, type: enum, values: [16, 20, 24], default: 20, required: false, description: token scale, not arbitrary px}
    - {name: color, type: token, default: currentColor, required: false}
    - {name: label, type: string, required: false, description: "presence => semantic (role=img/aria-label); absence => decorative aria-hidden"}
    - {name: decorative, type: boolean, default: true, required: false}
  tokens-not-props: [width, height, stroke]
states:
  runtime: []          # not interactive — states belong to the host control
variants:
  size: [16, 20, 24]
  fill: [outlined, filled]
  weight: [variable-where-supported]
accessibility:
  wcag-criteria: ["1.1.1", "1.4.1", "1.4.11", "2.5.8"]
  decorative: "aria-hidden=true — the DEFAULT, especially beside visible text"
  meaningful: "role=img + aria-label, or SVG <title>"
  in-control: "host control carries aria-label; icon aria-hidden — never name both"
  contrast: "meaningful >=3:1 (1.4.11); decorative exempt; never sole carrier of colour meaning (1.4.1)"
content:
  label-pattern: "concise noun/verb naming the concept/action (Search, Delete); decorative => none"
i18n:
  rtl: "directional glyphs mirror (back/forward/send/undo); non-directional do not; set marks directional glyphs; culturally-loaded glyphs need review"
implementation:
  - "inline SVG (currentColor, tree-shakeable) is the default"
  - "sprite for very large broadly-used sets; harder to tree-shake"
  - "icon fonts are an anti-pattern (tofu on load fail, no multi-tone, AT mis-reads)"
  - "optical alignment with text (cap-height), not bounding box"
  - "variable/optical-sizing axes (FILL/wght/GRAD/opsz) emerging — verify tooling"
composition:
  composes-with: [button, link, text-field, menu, tag]
  alternative-to: [illustration, logo, emoji]
  supersedes: ["icon fonts", "ad-hoc inline SVGs outside the set"]
  superseded-by: null
notes:
  contested:
    - "delivery — inline-SVG vs sprite (we default inline-SVG)"
    - "sizing model — px-grid vs em (we bind to the token grid)"
    - "the set-as-versioned-API rename/deprecation problem"
  trap: "icon-only-button — the Icon is never the interactive element; the wrapping Button is"
  evolution:
    - "icon fonts retired in favour of inline SVG"
    - "variable/optical-sizing sets; outlined-vs-filled as a state pair"
```

---

*Provenance: claude-only research run, `_research/_inbound/2026-06-15-component-icon/` (15 June 2026), sanctioned by the convergent-primitive rule (see `components/index.md`); the absence of `external-agent.md` records the single-pass run. Icon is the more contested of the two foundation primitives briefed this round — the field genuinely converges on the accessibility matrix and the inline-SVG-over-icon-font call, but splits on delivery (inline-SVG vs. sprite) and the sizing model, so this brief is a candidate for a dual-agent second pass if the delivery trade needs adversarial depth. The load-bearing calls: decorative-by-default accessible-name treatment (`aria-hidden` unless the glyph is meaningfully standalone), the icon-only-button trap (the Icon is never the interactive node — the wrapping Button is, the same boundary the Button brief draws from its side), and inline SVG as the default delivery with icon fonts named an anti-pattern. The states/variants and motion sections collapse per the primitive-deviation rule. The §15 schema is free-form per the catalogue design spec.*
