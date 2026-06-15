---
okf_version: "0.1"
type: component-brief
title: Divider
description: The catalogue's thinnest component and its sharpest accessibility test — a one-pixel rule that is either a semantic thematic break or a decorative line, and getting that one bit wrong is the only real way to ship it broken. A field-truth study of the separator-role decision (decorative by default), the vertical-divider height trap, the inset model, and the divider-versus-spacing judgment. A claude-only run, per the convergent-primitive rule.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [separator, rule, hr]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Divider

> Divider is the first brief on a primitive, and the first to prove the catalogue's claim that depth scales to the component — most of the 15-section spine has little to say about a one-pixel rule, and that is correct, not a gap. The whole component reduces to a single load-bearing decision: is this line a *semantic* thematic break that assistive tech should announce, or a *decorative* mark it must ignore? Get that one bit right and everything else is tokens. The brief is short because the component is honest.

---

## 1. Framing

A divider is a thin rule separating groups of content. What it *isn't*: a border (that belongs to a container and travels with it), an outline (a focus affordance), or whitespace — and whitespace is frequently the *better* separator, which makes "should this even be a divider" the first real question (§5). The contested core is not the pixels — every system draws roughly the same hairline — but the **semantics**: a divider is either a genuine thematic break (`role="separator"` / native `<hr>`) or pure visual decoration (`aria-hidden`), and shipping the wrong one is the only way a divider is meaningfully broken (§6). Systems converge on the visual and split, quietly, on the default for that bit.

## 2. Anatomy and parts

A single element. The one structural elaboration is the **labelled divider** — a short label centred or inset within the rule (the "OR" seam in an auth form), which splits the line into two segments flanking the content. Vertical dividers add no parts but acquire a height-context dependency that horizontal ones don't have (§11).

## 3. Properties / API

The converged surface is small: `orientation` (horizontal default / vertical); an inset model (`none` / `inset` / `middle-inset`, after Material 3); a flag deciding semantics (`decorative`, or its inverse); and, for the labelled case, `label` + `labelPosition`. **The practice ships `orientation`, `inset`, `decorative`, and the optional `label`/`labelPosition` — and nothing else.** Thickness and colour are **token-driven, not props**: a divider is the hairline/border token's first and thinnest consumer, and exposing arbitrary thickness or colour invites every consumer to reinvent the hairline. Hold the line at tokens.

## 4. States and variants

A divider has **no runtime states** — it is not interactive, so there is no hover, focus, pressed, or disabled (the generic state set simply doesn't apply, the inverse of Text Field where it all does). Variants are the cartesian of orientation × inset × (plain / labelled). This section collapses by design, per the primitive-deviation rule in the prompt template.

## 5. Usage guidance

**Use** to separate content groups *when whitespace alone leaves the grouping ambiguous* — dense lists, toolbar segments, menu sections, a card's header-from-body seam.

**Don't use** between every item in a list (that is noise — increase the spacing instead), as a decorative flourish, or where a container border already establishes the boundary.

**The divider-versus-spacing judgment is the real guidance.** Reach for space first; add a line only when proximity and alignment can't carry the grouping on their own. A page dense with rules reads as busier and *less* structured than the same page using a consistent spacing scale. The labelled divider is the one exception that earns its line — a genuine either/or seam ("OR" between credential and social login), not ornament.

## 6. Accessibility

This is the whole component. The theory is in 14-accessibility; the Divider-specific decision:

- **Semantic divider** — when the line marks a true *thematic content break*, give it `role="separator"` (or use native `<hr>`, which carries the role for free), plus `aria-orientation` when vertical. The break is then programmatically present and AT can convey it (WCAG **1.3.1 Info and Relationships**).
- **Decorative divider** — when the line is purely visual (segmenting a toolbar, dressing a card), mark it `aria-hidden="true"` / `role="presentation"` so it doesn't litter the accessibility tree with meaningless "separator" announcements. **Default to decorative**, and promote to semantic only for genuine thematic breaks — the inverse default (semantic everywhere) is the more common real-world bug, machine-gunning screen-reader users with separators between every toolbar button.
- **Contrast.** A decorative divider carries no information and is held to no contrast minimum; a divider that genuinely communicates a boundary should clear 3:1 (1.4.11) or it isn't doing the job it claims to.
- (A `role="separator"` *can* be focusable and operable — a resizable split-pane handle — which is why the role exists at all, but that is a different, interactive component, out of scope for the static divider.)

## 7. Content guidelines

Only the labelled divider has copy: one or two words, set per the type scale ("OR", "Today"). It is not a heading — don't overload it with a sentence or a section title (that is a heading's job, and a heading already creates the semantic break).

## 8. Motion and transition

None of its own. A divider may ride along in a parent's expand/collapse, but it has no entrance, exit, or state transition, so the reduce-motion contract is a non-issue here. (See 18-motion-foundations for the system-level position.)

## 9. Internationalization

A horizontal full-bleed divider is direction-neutral. An **inset** divider must measure its inset from *logical* edges (`margin-inline-start`/`-end`) so the inset mirrors correctly in RTL rather than stranding on the wrong side. A labelled divider's label follows text direction. A vertical divider's *position within a row* mirrors with the row. (See 13-internationalization-and-rtl.)

## 10. Naming

`Divider` is the field default (Material 3, Spectrum, Carbon, Atlassian, Base Web); the native element and the ARIA role are both `separator`, and Radix names its component `Separator` (with a `decorative` prop — the reference API for the semantics bit). **The practice default is `Divider`** for the component, with `Separator` documented as the primary alias (it is what consumers reaching from Radix or ARIA will search) alongside `Rule` and `Hr`.

## 11. Implementation notes

- **Prefer native `<hr>` for the semantic horizontal case** — it carries `role="separator"` for free and styles cleanly with a `border` reset. For the decorative case, a `<div aria-hidden="true">` is fine.
- **The vertical-divider height trap is the one recurring divider bug.** A vertical divider has *no intrinsic height* — it collapses to zero unless the flex/grid parent stretches it (`align-self: stretch`) or it is given an explicit cross-axis extent. Size it with logical properties (`block-size`/`inline-size`) and let the parent provide the height; don't hard-code a pixel height that breaks when the row's content grows.
- **Render at `1px` and watch HiDPI sub-pixel rounding** — scaled units can vanish or double on fractional device-pixel ratios; pull thickness from the hairline token rather than computing it.

## 12. Related and alternative components

- **Composes with:** List, Menu, Card, Toolbar, and **Stack** — whose `divider`-between-items prop is increasingly where the common case lives, so the standalone Divider is reached for less (§13).
- **Alternative to:** a spacing token (the non-component separator, and usually the first thing to try — §5) and a container Border.
- **Supersedes:** an ad-hoc `<hr>` styled inline without the hairline token.
- **Superseded by:** nothing.

(See 03-component-library for the system-level component model, and 29-per-component-documentation-template for the docs page this feeds. The Stack brief, when written, should reference this for its `divider`-between contract.)

## 13. Field POV evolution

A stable component with only two real movements: (1) the **decorative-by-default consensus is hardening** — systems increasingly ship dividers `aria-hidden` and make `role="separator"` the opt-in, recognising that most rules in a UI are visual segmentation, not thematic breaks; and (2) **layout primitives are absorbing the common case** — Stack/Flex components expose a `divider`/`separator`-between prop, so a free-standing Divider element is needed less often than it once was.

## 14. Sources cited

Conservative version dates (claude-only run; `last-audited` is the re-run trigger):

- Google Material 3 — Divider (full-width / inset / middle-inset) (Material 3, 2024).
- Adobe Spectrum — Divider (size S/M/L weight) (Spectrum, 2024).
- IBM Carbon — divider/contextual rules (Carbon, 2024).
- Atlassian Design System, Uber Base Web — Divider (2024).
- Shopify Polaris, GitHub Primer — `<hr>` / Divider usage (2024).
- Radix UI — `Separator` with the `decorative` prop (the reference API for the semantics split) (Radix, 2024).
- WAI-ARIA — the `separator` role (focusable/operable and static forms).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.3.1, 1.4.11.

## 15. Agent-consumable schema

```yaml
identity:
  id: divider
  name: Divider
  aliases: [separator, rule, hr]
  category: foundations
  status: stable
description: >
  Thin rule separating content groups. Semantic (role=separator / native
  <hr>) for genuine thematic breaks, decorative (aria-hidden) otherwise —
  default decorative. Not a border, not an outline; prefer whitespace
  where it suffices.
api:
  props:
    - {name: orientation, type: enum, values: [horizontal, vertical], default: horizontal, required: false}
    - {name: inset, type: enum, values: [none, inset, middle-inset], default: none, required: false}
    - {name: decorative, type: boolean, default: true, required: false, description: aria-hidden when true; role=separator when false}
    - {name: label, type: node, required: false, description: labelled-divider content (the OR-rule)}
    - {name: labelPosition, type: enum, values: [start, center, end], default: center, required: false}
  tokens-not-props: [thickness, color]   # the hairline token, never API
states:
  runtime: []          # not interactive — no hover/focus/pressed/disabled
variants:
  orientation: [horizontal, vertical]
  inset: [none, inset, middle-inset]
  content: [plain, labelled]
accessibility:
  wcag-criteria: ["1.3.1", "1.4.11"]
  semantic: "role=separator (+ aria-orientation when vertical) | native <hr>"
  decorative: "aria-hidden=true / role=presentation — the DEFAULT"
  contrast: "decorative: none required; meaningful: >=3:1 (1.4.11)"
content:
  label-pattern: "1-2 words (OR / Today); not a heading"
  empty-pattern: "n/a"
composition:
  composes-with: [list, menu, card, stack, toolbar]
  alternative-to: [spacing-token, border]
  supersedes: ["ad-hoc <hr> styled inline without the hairline token"]
  superseded-by: null
i18n:
  rtl: "inset measured from logical edges (margin-inline-start) so it mirrors; label follows text direction"
implementation:
  - "prefer native <hr> for the semantic horizontal case (role for free)"
  - "vertical divider has NO intrinsic height — parent must stretch it (align-self: stretch) or set explicit block-size"
  - "render at 1px via logical size; watch HiDPI sub-pixel rounding; thickness from the hairline token"
notes:
  contested:
    - "decorative-vs-semantic default — we default decorative"
    - "divider-vs-spacing — try whitespace first; a line only when grouping is ambiguous"
  evolution:
    - "decorative-by-default hardening; role=separator increasingly opt-in"
    - "Stack/Flex divider-between prop absorbing the common case"
```

---

*Provenance: claude-only research run, `_research/_inbound/2026-06-15-component-divider/` (15 June 2026) — the catalogue's first claude-only brief, sanctioned by the convergent-primitive rule (see `components/index.md`). The absence of `external-agent.md` in the folder records the single-pass run. The brief deliberately collapses the states/variants and motion sections per the primitive-deviation rule in the prompt template — a one-pixel non-interactive rule has no runtime states and no motion, and saying so plainly is the point. The load-bearing call is the decorative-by-default semantics (`aria-hidden` unless the line is a true thematic break), against the more common real-world bug of `role="separator"` everywhere. The §15 schema is free-form per the catalogue design spec.*
