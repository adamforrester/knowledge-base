# Icon — field-truth study (Claude pass, claude-only run)

## 1. Framing
Icon is a primitive, but a more contested one than Divider: the field converges on the essentials and splits on delivery and the sizing/colour model. What it is: a small vector glyph rendering a concept. What it isn't: a button (the most common conflation — §5), an illustration (larger, narrative, its own component), or a logo. The two load-bearing decisions: **is this glyph meaningful or decorative** (its accessible-name treatment, §6), and **how is the set delivered** (inline SVG vs. sprite vs. font, §11). Everything else — sizing, colour — is a token/convention call.

## 2. Anatomy and parts
A single `<svg>` (the practice default delivery), with an optional accessible-name mechanism (`<title>` / `aria-label` + `role="img"`) or `aria-hidden`. The set itself is the real artefact: a named, versioned vocabulary of glyphs on a shared grid.

## 3. Properties / API
Converged: `name`/which-glyph (or per-glyph components — `<IconSearch/>`); `size` (token scale, not arbitrary px); `color`/`tone` (default `currentColor`); `label` (presence promotes to semantic, absence = decorative/aria-hidden); `decorative` boolean in some systems. Practice default: per-glyph components (best tree-shaking) OR a `name` prop on a single component backed by a sprite; `size` from the token scale; colour via `currentColor` by default with an optional `tone`; `label` optional — its presence is the semantic switch. Don't expose arbitrary width/height or stroke — bind to the grid and token scale.

## 4. States and variants
No runtime states of its own (it's not interactive — interactive states belong to the wrapping control). Variants: size (16/20/24 grid), weight/fill where the set supports it (Material Symbols' fill/weight/grade/optical-size axes; SF Symbols' weights), and the semantic/decorative split. Collapsed per primitive rule.

## 5. Usage guidance
Use to reinforce meaning, aid scanning, or label an action *alongside* (not instead of) text where space allows. Don't: use an icon as the sole label for a critical action without an accessible name (§6); overload a UI with icons that compete; or invent one-off glyphs outside the set (the set is the discipline). **The icon-only-button is the key trap:** an icon-only control is a *Button* with an `aria-label` and a proper hit target — the accessible name and target size live on the button, and the Icon inside is `aria-hidden`. An Icon component is never itself the interactive element.

## 6. Accessibility
The decision matrix:
- **Decorative** (an icon beside a visible text label, or pure ornament): `aria-hidden="true"`. The adjacent text already names the thing; a named icon would double-announce. This is the default and the most common correct answer.
- **Meaningful standalone** (an icon conveying info with no adjacent text): give it an accessible name — `role="img"` + `aria-label`, or an SVG `<title>` — so AT conveys the concept.
- **Inside an interactive control with no visible text** (icon-only button/link): the *control* carries `aria-label`; the icon is `aria-hidden`. Don't name both.
WCAG: 1.1.1 Non-text Content (a meaningful icon needs a text alternative; a decorative one needs to be hidden); 1.4.11 Non-text Contrast (a meaningful icon must clear 3:1; decorative icons are exempt); 1.4.1 Use of Color (an icon must not be the *sole* carrier of meaning colour conveys). Target size (2.5.8) is the wrapping control's concern, not the glyph's.

## 7. Content guidelines
The "content" of an icon is its accessible name when meaningful: a concise noun/verb naming the concept or action ("Search", "Delete"), matching what the icon depicts and the action it triggers — not the glyph's internal name. Decorative icons have no content.

## 8. Motion and transition
Static by default. Icons animate only as part of a state transition they belong to (a chevron rotating on expand, a spinner) — that motion is owned by the host component and honours reduce-motion there. An Icon has no inherent motion.

## 9. Internationalization
**Directional icons must mirror in RTL** — back/forward arrows, list bullets, send, undo/redo, indentation — via logical flipping (`transform: scaleX(-1)` or RTL-specific glyphs). Non-directional icons (search, settings) must *not* mirror. Some glyphs are culturally loaded (a checkmark, a trash can, hand gestures) and need locale review. The set should mark which glyphs are directional.

## 10. Naming
`Icon` is universal as the component; the contested layer is the **set's name and the per-glyph taxonomy** — Material Symbols, GitHub Octicons, Apple SF Symbols, Carbon icons, Spectrum Workflow/UI icons. Practice default: a single named, versioned icon set; per-glyph names are a stable vocabulary with aliases (consumers reach for `trash`/`delete`/`bin` — alias them). The hard problem is **rename/deprecation**: when a glyph changes name or is removed, ship an alias map and a deprecation path, never a silent break — the icon set is an API.

## 11. Implementation notes
- **Inline SVG (per-glyph React components) is the practice default** — tree-shakeable (ship only used glyphs), stylable via `currentColor`, accessible, no extra request. The cost is bundle weight if a screen imports hundreds.
- **SVG sprite** (`<use href="#icon">`) — one cached request, good for large sets used broadly, but harder to tree-shake and `currentColor`/cross-document `<use>` has historical quirks.
- **Icon fonts are an anti-pattern now** — ligature/PUA glyphs fail when the font doesn't load (showing tofu or a random letter), resist per-glyph colour, are read incorrectly by some AT, and can't do multi-tone. Don't ship new icon fonts.
- **`currentColor`** is the default colouring mechanism — the icon inherits text colour, so it tracks the surrounding control's states for free.
- **Size with the token scale** (16/20/24) and align optically with adjacent text (cap-height/centre alignment, not bounding-box) — the recurring polish bug is an icon that sits a pixel low next to its label.
- **Optical sizing / variable icon fonts** (Material Symbols' `FILL`/`wght`/`GRAD`/`opsz` axes, SF Symbols) are the frontier for sets that want weight to track adjacent type — flag as emerging.

## 12. Related and alternative components
Composes with: Button (icon-only and icon+text), Link, Text Field (adornments), Menu, Tag, every component with an affordance. Alternative to: Illustration (larger/narrative), Logo, Emoji (which carry their own a11y semantics). Supersedes: icon fonts; inline ad-hoc SVGs without the set. Superseded by: nothing.

## 13. Field POV evolution
1. **Icon fonts → inline SVG** is essentially complete among field leaders.
2. **Variable/optical-sizing icon sets** (Material Symbols, SF Symbols) let one source render weights/fills/grades, replacing multiple static cuts.
3. **The two-tone/duotone and variable-fill direction** is growing (filled vs. outlined as a state pair — e.g. an outlined icon at rest, filled when active).
4. **The set-as-versioned-API discipline** is hardening — alias maps, deprecation paths, and codemods for renames.

## 14. Sources cited
Material Symbols (variable: FILL/wght/GRAD/opsz) (2024); Apple SF Symbols (weights, hierarchical/multicolor) (2024); GitHub Octicons (16/24 two-grid system) (2024); IBM Carbon icons (2024); Adobe Spectrum (Workflow / UI icons, sizing) (2024); Shopify Polaris Icon (currentColor, tone) (2024); Atlassian, Base Web icons (2024); WCAG 2.2 (Oct 2023) — 1.1.1, 1.4.1, 1.4.11, 2.5.8.

## 15. Agent-consumable schema
```yaml
identity: {id: icon, name: Icon, aliases: [glyph, symbol, svg-icon], category: foundations, status: stable}
description: >
  Small vector glyph rendering a concept. Decorative (aria-hidden) by
  default; meaningful standalone gets an accessible name; inside an
  icon-only control the CONTROL is named and the icon is hidden. Not a
  button, not an illustration, not a logo.
api:
  delivery: "per-glyph inline-SVG components (tree-shakeable) | sprite via name prop"
  props:
    - {name: name, type: string, description: which glyph (if single-component+sprite); else per-glyph components}
    - {name: size, type: enum, values: [16, 20, 24], default: 20, description: token scale, not arbitrary px}
    - {name: color, type: token, default: currentColor}
    - {name: label, type: string, required: false, description: presence => semantic (role=img/aria-label); absence => decorative aria-hidden}
    - {name: decorative, type: boolean, default: true}
  tokens-not-props: [width, height, stroke]
states: {runtime: [], note: not interactive — states belong to the host control}
variants: {size: [16, 20, 24], fill: [outlined, filled], weight: [variable-where-supported]}
accessibility:
  wcag-criteria: ["1.1.1", "1.4.1", "1.4.11", "2.5.8"]
  decorative: "aria-hidden=true — the default (esp. beside visible text)"
  meaningful: "role=img + aria-label, or SVG <title>"
  in-control: "host control carries aria-label; icon aria-hidden (never name both)"
  contrast: "meaningful icon >=3:1 (1.4.11); decorative exempt; never sole carrier of colour meaning (1.4.1)"
content: {label-pattern: "concise noun/verb naming the concept/action (Search, Delete); decorative => none"}
i18n: {rtl: "directional glyphs mirror (back/forward/send/undo); non-directional do not; set marks directional glyphs; culturally-loaded glyphs need review"}
implementation:
  - "inline SVG (currentColor, tree-shakeable) is the default"
  - "sprite for very large broadly-used sets; harder to tree-shake"
  - "icon fonts are an anti-pattern (tofu on load fail, no multi-tone, AT mis-reads)"
  - "optical alignment with text (cap-height), not bounding box"
  - "variable/optical-sizing axes (FILL/wght/GRAD/opsz) emerging"
composition:
  composes-with: [button, link, text-field, menu, tag]
  alternative-to: [illustration, logo, emoji]
  supersedes: ["icon fonts", "ad-hoc inline SVGs outside the set"]
  superseded-by: null
notes:
  contested: [delivery (inline-SVG vs sprite), sizing model (px-grid vs em), the set-as-versioned-API rename problem]
  trap: "icon-only-button — the Icon is never the interactive element; the wrapping Button is"
```
