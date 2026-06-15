# Divider — field-truth study (Claude pass, claude-only run)

## 1. Framing
A divider is the catalogue's thinnest component and its sharpest accessibility test: a one-pixel rule that is either *semantic* (a real thematic break AT should announce) or *decorative* (a visual line AT must ignore), and getting that one bit wrong is the only real way to ship a broken divider. What it is: a thin rule separating content groups. What it isn't: a border (belongs to a container), an outline, or whitespace (often the better separator — §5). The contested core is the role decision (§6), not the pixels.

## 2. Anatomy and parts
Single element. Optional: a **label slot** (centred or inset text breaking the rule — the "OR" divider), which turns the line into two segments flanking content. Vertical dividers add a height-context dependency (§11).

## 3. Properties / API
Converged: `orientation` (horizontal default / vertical); `variant`/`inset` (full-bleed / inset / middle-inset); a `decorative` (or inverse `semantic`) flag deciding role vs. aria-hidden; optional `children`/`label` + `labelPosition` for the labelled divider; thickness/tone via tokens, not props. The practice default: `orientation`, `inset`, and `decorative` props; thickness and colour are token-driven, not API. Don't expose arbitrary thickness/colour — a divider is the hairline token's first consumer.

## 4. States and variants
No runtime states (no hover/focus/disabled — it isn't interactive). Variants: orientation × inset × (plain / labelled). Collapsed per primitive rule.

## 5. Usage guidance
Use to separate content groups *when whitespace alone is insufficient* — dense lists, toolbar segments, menu sections. Don't use: between every item (noise — increase spacing instead), as a decorative flourish, or where a container border already does the job. **Divider-vs-spacing is the key judgment:** reach for space first; add a line only when grouping is ambiguous without it. The labelled divider is for a genuine "either/or" seam (auth forms), not decoration.

## 6. Accessibility
The whole game. A divider that marks a **thematic content break** is semantic: `role="separator"` (or native `<hr>`), with `aria-orientation` when vertical. A divider that is **purely visual** (segmenting a toolbar, decorating a card) must be `aria-hidden="true"` / `role="presentation"` so it doesn't pollute the AT tree with meaningless "separator" announcements. Default to decorative; promote to semantic only for true thematic breaks. A `role="separator"` can also be *focusable and operable* (a resizable split-pane handle) — out of scope for the static divider but the reason the role exists. WCAG: 1.3.1 Info and Relationships (the semantic break must be programmatically present); a decorative divider must meet no contrast minimum (non-informational), but a divider carrying meaning should clear 3:1 (1.4.11) or it isn't doing its job.

## 7. Content guidelines
Only the labelled divider has copy: short, one or two words, uppercase or sentence case per type scale — "OR", "Today". Not a heading; don't overload it.

## 8. Motion and transition
None by default. A divider may participate in a parent's expand/collapse but has no motion of its own; reduce-motion is a non-issue.

## 9. Internationalization
Horizontal dividers are direction-neutral; an *inset* divider must measure the inset from logical edges (`margin-inline-start`) so it mirrors in RTL. A labelled divider's label follows text direction. Vertical dividers are orientation-neutral but their position in a row mirrors with the row.

## 10. Naming
`Divider` (Material, Spectrum, Carbon, Atlassian, Base Web) is the default; Polaris/Primer have used `Divider`/`Separator?` and CSS `<hr>`. Practice default: **`Divider`**. Aliases: `Separator` (Radix's name — and the ARIA role), `Rule`, `Hr`.

## 11. Implementation notes
Prefer native `<hr>` for the semantic horizontal case — it carries `role="separator"` for free and styles fine with `border` reset. For decorative, a `<div aria-hidden>` is fine. **The vertical-divider trap:** a vertical divider has no intrinsic height — it collapses to zero unless the flex/grid parent stretches it (`align-self: stretch`) or it's given an explicit height. This is the single recurring divider bug. Use a 1px logical-size rule (`block-size`/`inline-size`) and let the parent provide the cross-axis extent. Thickness from a hairline token; beware sub-pixel rendering on HiDPI (use `1px`, not scaled units, or transform-scale tricks).

## 12. Related and alternative components
Composes with: List, Menu, Card, Stack (the `divider`-between-items prop), Toolbar. Alternative to: whitespace/spacing tokens (the non-component separator), a container Border. Supersedes: ad-hoc `<hr>` without token styling. Superseded by: nothing.

## 13. Field POV evolution
Stable component; the only real movement is (1) the decorative-by-default consensus hardening (systems increasingly ship dividers `aria-hidden` and make `role="separator"` opt-in), and (2) Stack/Flex components absorbing the common case via a `divider`/`separator`-between prop, so a standalone Divider is reached for less often.

## 14. Sources cited
Material 3 Divider (full-width/inset/middle-inset) (2024); Spectrum Divider (size S/M/L weight) (2024); Carbon (CSS/contextual) (2024); Atlassian, Base Web Divider (2024); Polaris/Primer (`<hr>`/Divider) (2024); Radix `Separator` (decorative prop, the reference API) (2024); WAI-ARIA `separator` role; WCAG 2.2 (Oct 2023) — 1.3.1, 1.4.11.

## 15. Agent-consumable schema
```yaml
identity: {id: divider, name: Divider, aliases: [separator, rule, hr], category: foundations, status: stable}
description: >
  Thin rule separating content groups. Semantic (role=separator/<hr>) for
  thematic breaks, decorative (aria-hidden) otherwise — default decorative.
  Not a border, not an outline; prefer whitespace where it suffices.
api:
  props:
    - {name: orientation, type: enum, values: [horizontal, vertical], default: horizontal}
    - {name: inset, type: enum, values: [none, inset, middle-inset], default: none}
    - {name: decorative, type: boolean, default: true, description: aria-hidden when true; role=separator when false}
    - {name: label, type: node, required: false, description: labelled-divider content (OR-rule)}
    - {name: labelPosition, type: enum, values: [start, center, end], default: center}
  tokens-not-props: [thickness, color]   # hairline token, not API
states: {runtime: [], note: not interactive}
variants: {orientation: [horizontal, vertical], inset: [none, inset, middle-inset], content: [plain, labelled]}
accessibility:
  wcag-criteria: ["1.3.1", "1.4.11"]
  semantic: "role=separator (+ aria-orientation if vertical) | native <hr>"
  decorative: "aria-hidden=true / role=presentation — the default"
  contrast: "decorative: none required; meaningful: >=3:1 (1.4.11)"
content: {label-pattern: "1-2 words (OR/Today); not a heading", empty-pattern: "n/a"}
composition:
  composes-with: [list, menu, card, stack, toolbar]
  alternative-to: [spacing-token, border]
  supersedes: ["ad-hoc <hr> without token styling"]
  superseded-by: null
i18n: {rtl: "inset measured from logical edges (margin-inline-start); label follows text direction"}
implementation:
  - "prefer native <hr> for the semantic horizontal case"
  - "vertical divider has NO intrinsic height — parent must stretch it (align-self: stretch) or set explicit block-size"
  - "1px via logical size; watch HiDPI sub-pixel rendering"
notes: {contested: [decorative-vs-semantic default — we default decorative, divider-vs-spacing judgment]}
```
