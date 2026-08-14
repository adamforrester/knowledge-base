---
okf_version: "0.1"
type: component-brief
title: Text
description: The typographic primitive, and the one component whose contested core is a single decoupling — the semantic level a screen reader navigates by, versus the visual size a designer picks. A field-truth study of the one-component-plus-`as` model against the Heading/Text split, the heading-order trap the decoupling exists to make fixable, the tokens that must travel as a composite rather than as props, and the one axis a design tool provably cannot carry.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [typography, heading, paragraph, type, prose, title]
last-audited: 2026-08-14
timestamp: 2026-08-14
---

# Text

> Every system has a type ramp. Far fewer have a **component** that carries it, and the ones that do split on a question that looks cosmetic and is not: does a piece of text's *meaning* live in the component you reach for, or in a prop? `Heading` and `Text` as two components encode the semantic level in the component's identity. `Text` with an `as` prop makes it a value. The field is genuinely divided, and the tiebreaker is not taste — it is that **an `<h2>` sometimes has to look small**, and a system that cannot express that produces a document outline built out of font sizes. Get the decoupling right and the rest is the ramp.

---

## 1. Framing

Text is the primitive that renders a string at a step of the type ramp. What it *isn't*: a heading — heading is a *role* it can take, not a different component; a layout element — it sets no spacing of its own and a system that lets it is one where margins collapse unpredictably; a rich-text renderer — a component that accepts arbitrary markup and styles it is a different, larger problem (prose/typography-reset containers, out of scope); and it is not the type tokens themselves, which exist and are consumable without it.

The reason the component exists at all is composition. A card's title, a banner's message, a dialog's heading and a list's item copy are the same typographic decision made four times, and made four times by hand they drift. Text is where the ramp stops being a set of values and becomes a thing people place.

The contested core is **whether the semantic element and the visual style are one axis or two.** Everything else in this brief is settled in the field.

## 2. Anatomy and parts

One text node, which makes this a genuinely flat primitive. Three structural elaborations carry real weight:

- **The type composite.** A step of the ramp is never one value — it is family, size, line-height, letter-spacing and (usually) weight, and they are only correct together. This is why §3 holds the line at tokens: exposing `lineHeight` as a prop lets a consumer pair a 32px size with a 16px leading, which is a broken step of a ramp that the ramp itself would never produce.
- **Truncation.** Single-line ellipsis and multi-line `line-clamp` change the box model — a clamped element needs a constrained inline size to clamp against, so the parent is implicated. The truncated string also disappears from the visual layer while staying in the accessibility tree, which is usually right and occasionally a surprise.
- **The visually-hidden variant.** Text that exists only for assistive technology (`clip-path` inset, not `display:none`, which removes it from the tree entirely). Most systems ship it here rather than as its own component, and that is the right home — it is a rendering mode of text.

The box's height is font-metric dependent: the half-leading above and below a line is part of the font, not the CSS, which is why two families at the same size and line-height do not occupy the same box. See §11 on `text-box-trim`.

## 3. Properties / API

The converged surface, and the one contested pair first:

**`as` and `size` are two axes, and the practice ships them as two.** `as` selects the rendered element and therefore the semantics (`h1`–`h6`, `p`, `span`, `div`, `label`, `strong`). `size` (or `variant`) selects the step of the ramp. Polaris is the reference API here and states the reasoning plainly — the element you need and the style you want are independent choices, and a system that fuses them forces you to break one to get the other.

Beyond the pair: `weight` (constrained to the ramp's weights, not a free number), `tone` (a semantic ink enum, never a colour value — the same argument Icon makes), `align` (logical: `start`/`end`/`center`, never `left`/`right` — §9), `truncate` / `lineClamp`, and `visuallyHidden`.

**Tokens, not props:** family, line-height, letter-spacing. They travel with the `size` rung as a composite (§2) and exposing them individually is how a ramp stops being a ramp. Colour is a **constrained enum**, not a token pass-through and not a raw value — `tone: subdued` resolves centrally so contrast is enforced in one place rather than per call site.

**No spacing props.** Margin on a text primitive is the single most common way a system's spacing scale gets bypassed, because it looks harmless. Spacing belongs to the layout primitive that contains it.

## 4. States and variants

**No runtime states.** Text is not interactive — no hover, focus, pressed or disabled. (Text *inside* an interactive control inherits that control's state through the cascade, which is the whole reason `tone` defaults to inherit-like behavior; the text primitive itself has no state of its own.)

Variants are the cartesian of the ramp: `size` × `weight` × `tone`, plus the boolean-ish `truncate` and `visuallyHidden`. The `size` ladder is the system's own, and it is the one place this brief declines to name a default vocabulary — a ramp is a foundation-level decision (see 23-typography-tokenisation) and a component brief that hard-coded one would be specifying the foundation from the wrong end.

## 5. Usage guidance

**Use** for every piece of standalone copy the system renders — headings, body, captions, labels that are not a form control's `<label>`. Consistency is the entire return: the ramp applied by a component is applied the same way everywhere, and applied by hand it is not.

**Don't use** to fake a heading. A large, bold `<span>` that reads as a section title and carries no heading semantics is invisible to the ~30% of screen-reader users who navigate primarily by heading, and it is the most common real-world defect this component exists to prevent (§6).

**Don't nest it in itself** to compose a style. Nested text primitives produce inheritance the ramp did not design and cascade bugs that are hard to see.

**Don't reach for it to set spacing.** If the answer to "how do I get 16px below this heading" is a prop on Text, the layout primitive is missing.

## 6. Accessibility

The decoupling in §3 exists for this section, and it is the whole component.

- **Heading semantics and order (WCAG 1.3.1).** Headings must form a correct outline — `h1` through `h6`, no skipped levels, one `h1` per view. **This is only achievable if the semantic level is independent of the visual size,** because real designs routinely need an `h3` that looks larger than an adjacent `h2`, or an `h2` set small in a dense panel. A fused `Heading level={n}` API forces the author to pick the level that *looks* right, and the outline degrades quietly. The decoupled API makes the correct answer expressible; nothing makes it automatic (§13).
- **Never convey a heading by appearance alone.** Size and weight are not programmatically determinable structure. This is the `1.3.1` failure, not a style preference.
- **Resize text to 200% without loss (1.4.4)** and **text spacing overrides (1.4.12)**. Both are properties of the ramp and its units rather than of this component, but the component is where they become testable — a ramp in `px` with fixed-height containers fails both, and the failure surfaces the first time someone sets a step at a size the container was drawn around.
- **Contrast (1.4.3 / 1.4.6).** `tone` resolving to a fixed enum is what makes this enforceable centrally. A `color` prop taking arbitrary values moves the contrast contract to every call site, where it is not checked.
- **Visually-hidden text uses the clip pattern, never `display:none`.** `display:none` and `visibility:hidden` remove the node from the accessibility tree, which is the opposite of the intent.
- **Truncated text stays in the accessibility tree.** An ellipsis is a visual truncation; the full string is still announced. If the full string genuinely should not be announced, truncate the data, not the display.

(See 14-accessibility for the theory and 28-web-accessibility-implementation for the implementation surface.)

## 7. Content guidelines

Sentence case for headings is the field default and the more legible choice; title case is a brand decision, not a system one. Headings take no terminal period. Keep headings short enough to survive a narrow viewport without wrapping to three lines — the ramp's largest steps are the ones that break first. Body copy sets its own measure: **45–75 characters per line** is the durable typographic guidance, and it belongs to the container's inline size rather than to this component, which is worth stating because it is the one place people look for it and it is not here.

## 8. Motion and transition

None of its own. Text may ride a parent's transition. A system that animates type size or weight on a text primitive is doing something the ramp did not intend and should justify it per component, not per primitive. (See 18-motion-foundations.)

## 9. Internationalization

More consequential here than in almost any other primitive, and three of these are silent failures:

- **`text-align` must be logical.** `start`/`end`, never `left`/`right`. A hard-coded `left` strands every RTL layout.
- **Letter-spacing must not be applied to Arabic and other joining scripts.** Tracking breaks the cursive joins between letters and renders the text as disconnected forms — legible to a machine, wrong to a reader. A ramp that applies tracking globally needs a script-scoped exception.
- **Line-height set for Latin will clip tall scripts.** Thai, Devanagari, and Vietnamese diacritics all exceed the Latin ascender/descender box. A ramp tuned against Latin alone produces clipped glyphs the first time content is localized.
- **CJK has no true italic**, and synthesized oblique is widely considered a defect rather than a fallback. An emphasis style that assumes italic needs an alternative for those scripts.
- **Text expands on translation** — commonly 30% into German, more for short strings. A heading sized to fit its container in English is a heading that wraps in five other locales.

(See 13-internationalization-and-rtl and 23-typography-tokenisation.)

## 10. Naming

`Text` is the field default for the primitive (Polaris, Chakra, Radix Themes, Spectrum, Material Compose). `Heading` appears as a sibling component in about half the surveyed systems. Base Web takes the third path — per-style components (`HeadingLarge`, `ParagraphMedium`) — which multiplies the API surface by the length of the ramp and is the approach with the fewest recent adopters.

**The practice default is a single `Text` component with `as` and `size`.** `Heading` is documented as an alias and may ship as a thin convenience wrapper that defaults `as` to a heading element — a convenience is fine; a second source of truth for the ramp is not. `Title`, `Paragraph`, `Type` and `Typography` are documented aliases; consumers arriving from Ant will search `Typography.Title`.

## 11. Implementation notes

- **A design tool cannot carry the semantic axis, and this is worth planning for rather than discovering.** A text node in a design file has a *text style* and nothing else — there is no `h2` in a Figma layer. So a design-side kit can express `size`, `weight` and `tone` faithfully and cannot express `as` at all. The semantic level is therefore code-only, and it has to be supplied at implementation time from the document's structure rather than read off the design. Systems that assume the kit and the code library are the same component surface get bitten here specifically.
- **Do not ship per-style components.** `HeadingLarge` / `BodySmall` as distinct exports means every ramp change is an API change, and the ramp is the thing most likely to be re-tuned per brand.
- **`text-box-trim` / `text-box-edge` is the emerging fix for half-leading**, letting a text box be measured from cap-height and baseline rather than from the font's line box. It removes the perennial "the designer's spacing does not match the built spacing" argument, which is not a rendering bug but a disagreement about what the box is. Support is recent enough to need a fallback; see §13.
- **Truncation needs a constrained parent.** `line-clamp` without a bounded inline size silently does nothing, which reads as the prop being broken.
- **A `p` cannot contain a `div`.** An `as` prop that admits both makes invalid nesting reachable through valid-looking props; validate the combination or document the constraint.

## 12. Related and alternative components

- **Composes with:** Card, Banner, Dialog, List, Table, Empty State, Tooltip, Form — effectively every component with copy in it, which is what makes it substrate rather than a catalogue entry.
- **Alternative to:** raw type tokens applied by hand (correct for one-offs inside another component's internals; wrong as a system-wide pattern), and a prose/typography-reset container for long-form authored content, which is a different component solving a different problem.
- **Supersedes:** ad-hoc styled `<span>`/`<div>` with hand-applied type values, and per-style component families.
- **Superseded by:** nothing.

(See 03-component-library for the system-level model, 23-typography-tokenisation for the ramp this renders, and 29-per-component-documentation-template for the docs page.)

## 13. Field POV evolution

Three movements, one of them recent:

1. **The split is narrowing toward one component plus `as`.** The systems that shipped `Heading`/`Text` separately increasingly expose a semantic-element escape hatch on both, which converges on the same API from the other direction.
2. **Heading order is moving from documentation to enforcement.** Lint rules and automated checks for skipped levels are increasingly standard, which matters because the decoupled API makes correct order *expressible* and does nothing to make it *likely* — the decoupling is necessary and not sufficient, and the enforcement layer is what closes it.
3. **`text-box-trim` is the first genuine change to the primitive's box model in years** (§11). Where it lands, the long-running "design spacing versus built spacing" disagreement resolves rather than being negotiated per component.

## 14. Sources cited

Conservative version dates (claude-only run, per the convergent-primitive rule; `last-audited` is the re-run trigger):

- Shopify Polaris — `Text` with `as` + `variant`; the decoupling is stated as the design rationale (Polaris, 2024–25).
- Radix Themes — `Text` / `Heading` with `as` (Radix, 2024–25).
- Chakra UI — `Text` / `Heading` (2024).
- Adobe Spectrum — `Heading` / `Text` / `Content` (Spectrum, 2024).
- Uber Base Web — per-style typography components (`HeadingLarge`, `ParagraphMedium`) (2024).
- Ant Design — `Typography.Text` / `.Title` / `.Paragraph` (2024).
- Google Material 3 — type scale + `Text` with `style` (Compose) (2024).
- IBM Carbon — type as tokens/classes, no text component (2024).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.3.1, 1.4.3, 1.4.4, 1.4.6, 1.4.12.
- CSS Inline Layout Level 3 — `text-box-trim` / `text-box-edge`.

## 15. Agent-consumable schema

```yaml
identity:
  id: text
  name: Text
  aliases: [typography, heading, paragraph, type, prose, title]
  category: foundations
  status: stable
description: >
  The typographic primitive: renders a string at a step of the type ramp.
  Semantic element (`as`) and visual step (`size`) are INDEPENDENT axes —
  that decoupling is what makes a correct heading outline expressible when
  an h2 has to look small. Not a heading (a role it takes), not a layout
  element (no spacing props), not a rich-text renderer.
anatomy:
  node: single text node
  type-composite: "family + size + line-height + letter-spacing travel together as one ramp step; never exposed individually"
  elaborations: [truncation (needs a constrained parent), visually-hidden mode (clip pattern)]
  box: "height is font-metric dependent (half-leading); see text-box-trim"
api:
  props:
    - {name: as, type: enum, values: [h1, h2, h3, h4, h5, h6, p, span, div, label, strong], default: p, required: false, description: "SEMANTICS. Independent of size. Code-only — a design tool cannot carry this axis."}
    - {name: size, type: enum, values: "the system's ramp", required: false, description: "VISUAL step. Independent of as."}
    - {name: weight, type: enum, values: "the ramp's weights", required: false, description: constrained to the ramp, never a free number}
    - {name: tone, type: enum, values: [default, subdued, brand, success, warning, danger, info, inherit], default: inherit, required: false, description: "semantic ink; REJECTS raw colour so contrast is enforced centrally"}
    - {name: align, type: enum, values: [start, center, end], required: false, description: "LOGICAL only — never left/right"}
    - {name: truncate, type: boolean, default: false, required: false}
    - {name: lineClamp, type: number, required: false, description: needs a constrained inline size on the parent}
    - {name: visuallyHidden, type: boolean, default: false, required: false, description: clip pattern, never display:none}
  tokens-not-props: [family, line-height, letter-spacing]
  deliberately-absent: [margin, padding, color]   # spacing belongs to the layout primitive; colour to `tone`
states:
  runtime: []          # not interactive; text inside a control inherits that control's state via the cascade
variants:
  size: "the system's ramp (a foundations decision — see 23)"
  weight: "the ramp's weights"
  tone: [default, subdued, brand, success, warning, danger, info, inherit]
  mode: [normal, truncated, clamped, visually-hidden]
accessibility:
  wcag-criteria: ["1.3.1", "1.4.3", "1.4.4", "1.4.6", "1.4.12"]
  heading-order: "h1-h6, no skipped levels, one h1 per view — only EXPRESSIBLE because `as` is independent of `size`"
  never: "convey heading level by size/weight alone (1.3.1 failure, not a style preference)"
  visually-hidden: "clip-path inset — display:none/visibility:hidden remove the node from the tree"
  truncation: "ellipsis is visual only; the full string stays in the accessibility tree"
content:
  label-pattern: "sentence case headings; no terminal period; short enough to survive a narrow viewport"
  measure: "45-75 characters per line — belongs to the CONTAINER's inline size, not to this component"
  empty-pattern: "render nothing rather than an empty node"
i18n:
  rtl: "text-align must be logical (start/end); a hard-coded left strands every RTL layout"
  letter-spacing: "must NOT apply to Arabic and other joining scripts — tracking breaks cursive joins"
  line-height: "a ramp tuned on Latin clips Thai, Devanagari and Vietnamese diacritics"
  cjk: "no true italic; synthesized oblique is a defect, not a fallback"
  expansion: "~30% into German for short strings; a heading sized to fit in English wraps elsewhere"
implementation:
  - "A DESIGN TOOL CANNOT CARRY `as` — a design text node has a style and no semantic level, so the semantic axis is code-only and supplied from document structure at implementation time"
  - "do not ship per-style components (HeadingLarge/BodySmall) — every ramp change becomes an API change"
  - "text-box-trim / text-box-edge is the emerging fix for half-leading; needs a fallback"
  - "line-clamp without a bounded inline size silently does nothing"
  - "a <p> cannot contain a <div> — validate the `as` + children combination or document the constraint"
composition:
  composes-with: [card, banner, dialog, list, table, empty-state, tooltip, form]
  alternative-to: [raw type tokens applied by hand, prose/typography-reset container]
  supersedes: ["ad-hoc styled span/div with hand-applied type values", "per-style component families"]
  superseded-by: null
notes:
  contested:
    - "one component + `as` vs a Heading/Text split — we ship one component; Heading may be a thin convenience wrapper, never a second source of truth for the ramp"
    - "the size vocabulary is deliberately NOT named here — a ramp is a foundations decision (23), and specifying it from a component brief is the wrong end"
  evolution:
    - "the Heading/Text split is narrowing toward one component + an `as` escape hatch"
    - "heading order moving from documentation to lint enforcement — the decoupling is necessary, not sufficient"
    - "text-box-trim is the first real change to the primitive's box model in years"
  unverified:
    - "the ~30% figure for screen-reader users navigating primarily by heading is widely cited in practitioner material and is not backed by a source in _source-text/ — treat as directional"
```

---

*Provenance: claude-only research run, 14 August 2026, sanctioned by the convergent-primitive rule (see `components/index.md`) — the field converges on everything except the one axis question in §3, which is documented as a live split rather than flattened. Written to close a gap found from the downstream direction: the Prism3 MVP catalogue (`Prism3/docs/40`) named `text` as a required dependency of Card, Banner, Dialog and List with no brief behind it, which inverts the catalogue's pipeline. The load-bearing call is the `as`/`size` decoupling and its §6 justification — the heading-order argument is what makes it an accessibility decision rather than an API preference. §11's first bullet is the finding most likely to be useful downstream and least likely to be in any vendor's documentation: the semantic axis is structurally uncarryable by a design tool, which makes it code-only in the sense `Prism3/docs/28` uses the term. The §15 schema conforms to `_schema.md`.*
