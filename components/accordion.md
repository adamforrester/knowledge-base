---
okf_version: "0.1"
type: component-brief
title: Accordion
description: Tabs' vertical, multi-open cousin — progressive disclosure of stacked content sections. A field-truth study of the Disclosure-primitive decomposition (single collapsible + coordinated set), single-vs-multi-open (multi default), the heading + button[aria-expanded] + region pattern (each header its own tab stop, NOT tabs' roving), the native-<details>-first decision (the name attribute, ::details-content, calc-size), and the height-animation problem, with the practice's defaults.
tags: [components, navigation]
category: Navigation
status: stable
aliases: [disclosure, collapse, expander, details, expansion-panel]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Accordion

> Accordion is Tabs' vertical, multi-open cousin — and the boundary between them is the cleanest in the catalogue: Tabs show **one** panel at a time in a **horizontal** row via `tablist`/`tab`/`tabpanel` + roving tabindex; an Accordion is a **vertical** stack of expand/collapse sections that can show **zero, one, or many** at once via a completely different pattern — a heading wrapping a `<button aria-expanded>` that toggles a region, **not** a tablist. Tabs *swap* the view; Accordions *expand it inline*. Everything else follows from that: each header is its own tab stop (no roving), the open-set can be empty, and the hard problem is the one CSS spent a decade unable to solve — animating height to content. The platform has now solved it, which reshapes the whole implementation.

---

## 1. Framing

An Accordion is a **vertical stack of expand/collapse sections** for progressive disclosure — compressing long or supplementary content into scannable headers the user opens as needed (FAQs, settings groups, filter sidebars). What it *isn't*: **one-at-a-time horizontal panels** (→ Tabs — the cousin, §5), a **single** standalone collapsible (→ a Disclosure, the atomic primitive — §2), **multi-level hierarchical** data (→ Tree), a **sequence** (→ Stepper), or **routing**.

Why systems disagree: the **Disclosure-vs-Accordion decomposition** (one component or a primitive + a group), **single-open vs. multi-open**, the **native `<details>` vs. custom ARIA** decision (freshly reopened by platform features), and the perennial **height-animation problem**.

## 2. Anatomy and parts — the disclosure decomposition

A single expand/collapse section is a **Disclosure** (a header button + a region); an Accordion is a **DisclosureGroup** — a coordinated *set* of Disclosures. This parallels the catalogue's atomic-vs-set decompositions (checkbox/CheckboxGroup, the toggle-button/segmented pattern). **The practice ships `Disclosure` (the standalone collapsible — "Advanced settings", a single FAQ) + `Accordion`/`AccordionItem` (the coordinated set)** — React Aria's `Disclosure`/`DisclosureGroup` is the reference (Primer ships a standalone `Details` similarly).

Per-item parts (standardised across systems):

- **Heading wrapper** — a real `<hN>` (`<h3>` etc.) of the correct outline level, containing *only* the trigger; does not itself take focus.
- **Trigger button** — a native `<button aria-expanded aria-controls>` spanning 100% of the header (the whole-header hit target); holds the label + a rotating chevron (`aria-hidden`).
- **Region/panel** — the disclosed content (`role=region` + `aria-labelledby`→the button).
- **Divider**, and at the set level an optional **expand-all/collapse-all** control.

One group-level a11y detail (Carbon): wrapping the items in `<ul>`/`<li>` gives screen readers "item X of N" group-size context — useful for the *grouped* Accordion, but a *standalone* Disclosure must **not** be in a list.

## 3. Properties / API

(No form-field substrate to inherit — Accordion is a disclosure pattern, not a form control.)

- **`allowsMultipleExpanded` / `selectionMode`** — multi-open (the practice **default**) vs. single-open (exclusive). The headline prop. Multi-open is the default because exclusive mode actively frustrates the common "compare section A with section C" task; reserve single-open for severe vertical constraints or a wizard-like flow. (Base Web is the outlier, defaulting to exclusive — `accordion={true}`.)
- **`allowAllClosed` / `collapsible`** — may every section be closed? **Default yes.** Forcing one section always-open blurs the line with Tabs — if the UI needs one pane always visible, that's Tabs, not an Accordion.
- **`expandedKeys` / `defaultExpandedKeys` / `onExpandedChange`** — controlled/uncontrolled, an **iterable of keys** (key-based, not index — the tabs lesson). The array type elegantly serves *both* modes (exclusive just holds ≤1 key), so consumers don't fork state logic.
- per-item: `key`, `title`/header, `isDisabled`, default-expanded; **`headingLevel`** (default 3, overridable — §6).
- composition: `<Accordion><AccordionItem>` children (over a config array), associated by key.

## 4. States and variants

States (per item, all mapping to the header `<button>`): collapsed / **expanded** (`aria-expanded`, `[data-expanded]`/native `[open]`) / hover / focus-visible (keyboard-only ring) / disabled (muted, removed from tab order, expansion locked). 

**Variants:** **flush** (full-width, separated only by internal dividers — sidebars, mobile) vs. **contained/boxed** (each item a bordered card — dashboards; the contained item is essentially a Card + a collapse toggle); with-icon/indicator; expand-all affordance. **Nested accordions are forbidden** — they fracture hierarchy and break keyboard navigation; multi-level disclosure is a **Tree**, not nested accordions. No tone/emphasis.

## 5. Usage guidance

- **Use** to compress long, scannable, independently-consumed sections into headers opened on demand: FAQs, settings groups, filter panels, progressive detail.
- **Don't use** for: content the user needs **most/all of at once** (just show it — accordions add interaction cost and hide content from in-page Find/scanning); **one-at-a-time horizontal** peer panels (→ Tabs); a **single** collapsible (→ Disclosure); **hierarchical** data (→ Tree); a **sequence** (→ Stepper); **navigation/routing** (→ nav).
- **Decision frameworks:**
  - **Accordion vs. Tabs** — vertical/multi-open/inline-expansion vs. horizontal/one-at-a-time/view-swap. **The responsive transform is the key tie:** horizontal Tabs commonly **become an Accordion on narrow viewports** (vertical stacking beats a horizontal overflow row on mobile). (See tabs §5.)
  - **Accordion vs. Disclosure** — a coordinated *set* vs. a *single* collapsible.
  - **Accordion vs. Tree** — one level deep with rich panels (Accordion) vs. multi-tier nested nodes with `role=tree`/`treeitem` (Tree); note the chevrons even differ (Accordion down-closed/up-open; Tree right-closed/down-open).
  - **Single vs. multi-open** — multi by default; single only for tight space or a linear flow.
- **Don't hide always-needed content** behind a collapsed header.

## 6. Accessibility

A high-risk component — done wrong it fails 2.1.1, 2.4.3, and 4.1.2 at once. The exact contract:

- **Heading + button + region, NOT tablist.** Each header is a native `<button aria-expanded="true|false" aria-controls="panelId">` **wrapped in an `<hN>` of the correct level**; the panel is `role=region` + `aria-labelledby`→the button. The heading wrapper keeps the title in the screen-reader rotor and preserves the document outline; the button (not the heading) carries the interactivity and state.
- **The heading-level outline is a real contract** — an Accordion dropped under an `<h2>` section needs `<h3>` headers; hard-coding the level breaks the outline and is a systemic WCAG failure. Expose a **`headingLevel`** prop (default 3) or an `as` polymorphic prop.
- **Each header is its own tab stop — the key keyboard difference from Tabs.** Tab moves between headers (and into open panels); **no roving tabindex** (the opposite of tabs §6). **Enter/Space** toggles; on expand, the next Tab moves into the panel's first focusable element. The APG's **Up/Down between headers + Home/End** is an *optional* power-user enhancement (Tab traversal alone satisfies 2.1.1); if added, it must not trap focus.
- **Collapsed content is `hidden`** (out of tab order and AT); expanded content is reachable. Optionally scroll the header into view on expand (§11).
- **WCAG SCs:** 4.1.2 (button + `aria-expanded`), 1.3.1 (heading structure), 2.1.1 (keyboard), 2.4.3 (focus order), 2.4.13/1.4.11 (focus + indicator contrast), 1.4.1 (indicator not colour-only).

## 7. Content guidelines

Header labels: concise, parallel, scannable noun phrases (or questions, for FAQ) — they're the information scent for collapsed content, so they must telegraph what's inside; no trailing colons (Apple HIG). The **whole header is the hit target** (the `<button>` is `width:100%`, flex, padded), meeting 44/48px. Headers **wrap rather than truncate** under long/translated text (unlike tabs, accordion headers stack and can wrap) — use `min-height`, not fixed height, and keep the label clear of the chevron (Carbon's responsive right-margin rule is one concrete approach). Expand-all/collapse-all controls (right-aligned, above the group) for long sets.

## 8. Motion and transition

The signature motion is the **height expand/collapse**, historically the most notorious trap in UI: you can't natively animate `height: 0 → auto`, so the field used the **`grid-template-rows: 0fr → 1fr`** trick, the brittle **`max-height` hack** (bad easing — the browser times to the fake max), or **JS-measured height** (a `ResizeObserver` writing a pixel custom property — smooth but with layout-thrash and jank). **As of 2025–2026 the platform solves it natively:** `interpolate-size: allow-keywords` (opting into keyword interpolation) and **`calc-size(auto)`** enable pure-CSS eased height transitions with zero JS — *verify browser support before relying on it*; `grid-template-rows` remains the robust fallback. The chevron rotates 180° (~150–200ms). Under `prefers-reduced-motion: reduce`, **snap open/closed** (force `transition-duration` to ~0) — animating large text blocks vertically is a vestibular trigger. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

**RTL** moves the chevron to the leading (left) edge and right-aligns the text — achieved with flexbox `justify-content: space-between` + logical properties so `dir="rtl"` inverts automatically, no JS. Header **text expansion** (de/ru +30–50%) **wraps** rather than truncates (fluid `min-height`, never `text-overflow: ellipsis` except extreme edge cases), and must not overlap the chevron. (See 13-internationalization-and-rtl.)

## 10. Naming

The field converges on **`Accordion` + `AccordionItem`** for the public set (Carbon, Atlassian, Material), with the single primitive named **`Disclosure`** (React Aria, the ARIA pattern name) or `Details`; Base Web uses `Accordion`/`Panel`. **The practice default: `Accordion`/`AccordionItem`** (the set — the names designers and engineers reach for) **+ `Disclosure`** (the exposed standalone primitive and the headless `useDisclosure` hook). Aliases to map: `Collapse`, `Expander`, `Details`, `ExpansionPanel` (legacy Material), `Collapsible` (legacy Polaris).

## 11. Implementation notes

- **Native `<details>`/`<summary>` first — the decision the platform just changed.** `<details>` gives expand/collapse, keyboard, and focus for free; the **`name` attribute** natively groups a set into an **exclusive (single-open) accordion with zero JS**; and **`::details-content` + `transition-behavior: allow-discrete` + `calc-size(auto)`** now animate the native panel (the historic blocker). So the practice **leans native-`<details>`-first** for the underlying DOM — with **custom ARIA (React Aria/Radix) as the path for controlled `expandedKeys` state in React, complex orchestration, and legacy browser support**, rather than the reverse. (The native-vs-custom call parallels select §11; flag the `name`/`::details-content`/`calc-size` support as current-platform-state to verify.)
- **The height animation** (§8) — `interpolate-size`/`calc-size` native (verify) over `grid-template-rows: 0fr/1fr` (robust fallback) over the dead `max-height` hack.
- **Controlled `expandedKeys`** (key-based, iterable) with the controlled-without-`onChange` trap; single-open coordinates by closing siblings.
- **Scroll-into-view on expand** — on `onExpandedChange`, `requestAnimationFrame` then `scrollIntoView({block:'nearest'})` so a tall panel doesn't push the header off-screen.
- **Deep-linking** — read `location.hash` on mount and seed `defaultExpandedKeys`; `:target` even opens native `<details>` without JS.
- **Don't hand-roll the ARIA** — React Aria `Disclosure`/`useDisclosure`, Radix Accordion (`type=single|multiple`, `collapsible`), Headless UI; skin it.

## 12. Related and alternative components

- **Composes with:** Disclosure (the primitive), heading, Icon (chevron — see icon), Card/Section (the contained variant), an expand-all Button.
- **Alternative to:** Tabs (horizontal one-at-a-time — see tabs), Disclosure (single), Tree (hierarchical), Stepper (sequential), an expandable Table row (disclosure inside the table matrix — see Table when briefed).
- **Supersedes:** ad-hoc show/hide `<div>`s without `aria-expanded`/heading semantics; a tablist misused for vertical multi-open sections.
- **Superseded by:** Tabs on wide viewports when one-at-a-time peer panels fit better; just showing the content when it's all needed.

(Tabs' vertical cousin — see tabs for the boundary from its side; the Disclosure/Accordion decomposition parallels the catalogue's atomic-vs-set patterns (checkbox, segmented-control). 03-component-library; 29 for the docs template. Tree and the routing nav/Link are the adjacent Navigation briefs to come.)

## 13. Field POV evolution

1. **The height-animation problem is finally solved natively** — `grid-template-rows: 0fr/1fr`, then `interpolate-size: allow-keywords` + `calc-size(auto)` + `::details-content`, retiring the `max-height` hack and JS measurement.
2. **Native `<details>` got real** — the **`name` attribute** (exclusive single-open, no JS) and animatable disclosure narrow where custom ARIA is needed (the select-like native resurgence), shifting the practitioner's job from re-implementing behaviour to wrapping/tokenising native primitives.
3. **Disclosure split out** as a named primitive (React Aria) rather than folding the single-collapsible into Accordion.
4. **Heading-wrapped triggers** affirmed as correct over bare buttons (outline integrity).
5. **The list-primitive trend** — Material 3 *abandoned* its "Expansion Panel", folding expand/collapse into "Expressive Lists"; a signal toward composable list primitives over monolithic accordion components.

## 14. Sources cited

Conservative dating (the external pass cited React Aria v3.49.0, Carbon v1.109.0, Polaris v11+, Base Web, Primer, Material 3 Expressive Lists, Apple HIG, and the CSS WG specs — held loosely; the `calc-size`/`interpolate-size`/`<details name>`/`::details-content` platform features are flagged unverified as current-platform-state; `last-audited` is the re-run trigger):

- Adobe Spectrum / React Aria — `Disclosure` / `DisclosureGroup`, `useDisclosure`, `allowsMultipleExpanded`, `expandedKeys`, the JS height-measurement legacy (Spectrum, 2024–2025).
- IBM Carbon — `Accordion`/`AccordionItem`, `isFlush`, `<ul>/<li>` group wrapping, `aria-level`/heading-level handling, the responsive right-margin rule (Carbon, 2024–2026).
- Uber Base Web — `Accordion`/`Panel`, the `accordion` (exclusive-default) boolean, the APG-optional arrow-key pattern, the accordion-vs-tree demarcation (Base Web, 2024).
- GitHub Primer — `Details`/`useDetails`, the `as`-prop heading polymorphism (Primer, 2024–2025).
- Atlassian Design System — `Accordion`, Open-all/Close-all controls (Atlassian, 2024).
- Shopify Polaris — `Collapsible` / `Details` (Polaris, 2024).
- Google Material 3 — the move from Expansion Panel to Expressive Lists expand/collapse (Material 3, 2024–2025).
- Apple Human Interface Guidelines — `DisclosureGroup` (SwiftUI), label punctuation guidance (Apple HIG, 2024).
- W3C / WAI-ARIA APG — Accordion and Disclosure patterns; CSS Working Group / MDN — `<details name>`, `::details-content`, `interpolate-size`/`calc-size()`, `transition-behavior: allow-discrete` (2024–2026).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 4.1.2, 1.3.1, 2.1.1, 2.4.3, 2.4.13, 1.4.11, 1.4.1.

## 15. Agent-consumable schema

```yaml
identity:
  id: accordion
  name: Accordion
  aliases: [disclosure, collapse, expander, details, expansion-panel]
  category: navigation
  status: stable
description: >
  A vertical stack of expand/collapse sections for progressive disclosure
  (zero, one, or many open). Tabs' vertical multi-open cousin — heading +
  button[aria-expanded] + region, NOT tablist. Decomposes into Disclosure
  (single collapsible) + Accordion/AccordionItem (coordinated set). Not
  Tabs (horizontal one-at-a-time), not a single Disclosure, not a Tree
  (hierarchical), not routing.
anatomy:
  decomposition:
    primitive: "Disclosure (single collapsible) — exposed standalone + useDisclosure hook"
    set: "Accordion / AccordionItem (DisclosureGroup — coordinated set)"
    parallels: "the atomic-vs-set decompositions in checkbox / segmented-control"
  parts: [heading-wrapper (<hN>, holds only the trigger), trigger-button (<button aria-expanded aria-controls>, whole-header hit target), label, indicator (chevron, aria-hidden), region (role=region + aria-labelledby), divider, group-level expand-all/collapse-all]
  group-context: "Carbon <ul>/<li> wrapping gives 'item X of N'; a STANDALONE Disclosure must NOT be in a list"
api:
  props:
    - {name: allowsMultipleExpanded/selectionMode, type: boolean/enum, default: "multi-open", description: "multi (default — exclusive frustrates compare-A-with-C) vs single-open (tight space / wizard). Base Web outlier defaults exclusive"}
    - {name: allowAllClosed/collapsible, type: boolean, default: true, description: "may all sections close? yes — forcing one open blurs into Tabs (use Tabs then)"}
    - {name: expandedKeys/defaultExpandedKeys/onExpandedChange, type: iterable<key>, description: "controlled/uncontrolled, KEY-based not index; array serves both modes (exclusive holds <=1)"}
    - {name: headingLevel, type: integer, default: 3, description: "or an 'as' prop — must fit the host outline; hardcoding breaks WCAG 1.3.1"}
    - {name: per-item, type: "key, title, isDisabled, defaultExpanded"}
  composition: "<Accordion><AccordionItem> children, associated by key"
states:
  runtime: [collapsed, expanded, hover, focus-visible, disabled]
  notes: "expanded maps to aria-expanded / [data-expanded] / native [open]; collapsed content is hidden (out of tab order + AT)"
variants:
  style: [flush (dividers only — sidebars/mobile), contained (bordered card per item — dashboards)]
  content: [with-icon-indicator]
  selection: [multi-open (default), single-open]
  forbidden: [nested-accordions]   # -> Tree for multi-level
accessibility:
  pattern: "WAI-ARIA APG Accordion — heading + button[aria-expanded][aria-controls] + region[aria-labelledby]; NOT tablist"
  wcag-criteria: ["4.1.2", "1.3.1", "2.1.1", "2.4.3", "2.4.13", "1.4.11", "1.4.1"]
  heading-contract: "button wrapped in <hN> of the correct outline level (headingLevel prop, default 3); button carries interactivity+state, heading preserves the outline/rotor"
  keyboard-model:
    tab: "EACH header is its own tab stop — NO roving tabindex (the key difference from tabs); then Tab moves into the open panel"
    enter-space: "toggles the focused header"
    arrows: "APG-OPTIONAL — Up/Down between headers + Home/End; Tab traversal alone satisfies 2.1.1"
  indicator: "not colour-only (1.4.1); chevron aria-hidden"
content:
  label-pattern: "concise parallel noun phrases / questions; telegraph the hidden content; no trailing colons"
  hit-target: "whole header is the button (width:100%, flex, padded); 44/48px"
  overflow: "headers WRAP not truncate (min-height, no ellipsis); keep clear of the chevron (Carbon responsive right-margin)"
  bulk: "expand-all/collapse-all (right-aligned, above the set) for long groups"
motion:
  height: "the historic trap (can't animate height:0->auto). NATIVE NOW: interpolate-size: allow-keywords + calc-size(auto) (+ ::details-content / transition-behavior: allow-discrete) — verify support; FALLBACK grid-template-rows 0fr->1fr; DEAD: max-height hack / JS measurement"
  chevron: "180deg rotate ~150-200ms"
  reduce-motion: "snap open/closed (transition-duration ~0) — vertical text animation is a vestibular trigger"
i18n:
  rtl: "chevron to leading (left) edge, text right-aligned; flexbox space-between + logical properties auto-invert on dir=rtl (no JS)"
  expansion: "headers wrap (min-height), never ellipsis-truncate; must not overlap the chevron"
implementation:
  - "NATIVE <details>/<summary> FIRST: free expand/collapse+keyboard+focus; name attribute = exclusive single-open with ZERO JS; ::details-content + transition-behavior: allow-discrete + calc-size animate the native panel (verify support)"
  - "custom ARIA (React Aria/Radix) for controlled expandedKeys in React, complex orchestration, legacy support — the fallback, not the default"
  - "height: interpolate-size/calc-size native (verify) > grid-template-rows fallback > dead max-height hack"
  - "controlled expandedKeys key-based; single-open closes siblings; controlled-without-onChange trap"
  - "scroll-into-view on expand (rAF + scrollIntoView block:nearest); deep-link via location.hash -> defaultExpandedKeys (:target works for native <details>)"
  - "don't hand-roll the ARIA — React Aria Disclosure/useDisclosure, Radix (type=single|multiple, collapsible), Headless UI"
composition:
  composes-with: [disclosure, heading, icon, card, section, button]
  decomposition-relationship: "Disclosure (single) composes into Accordion (set); the contained variant is a Card + collapse toggle"
  alternative-to: [tabs, disclosure, tree, stepper, expandable-table-row]
  supersedes: ["show/hide divs without aria-expanded/heading semantics", "tablist misused for vertical multi-open sections"]
  superseded-by: ["tabs on wide viewports for one-at-a-time peer panels", "just showing content when it's all needed"]
notes:
  contested:
    - "Disclosure-vs-Accordion decomposition (ship both: primitive + set)"
    - "single-open vs multi-open (multi default; Base Web defaults exclusive)"
    - "native <details> vs custom ARIA (native-first now, given name/calc-size/::details-content; custom for controlled state + legacy)"
  boundary: "accordion-vs-tabs (vertical multi-open inline-expand vs horizontal one-at-a-time view-swap); the mobile tabs->accordion transform"
  unverified:
    - "the calc-size / interpolate-size / <details name> / ::details-content platform features (verify browser support)"
    - "external-supplied 2025/2026 version numbers"
  evolution: "height-animation solved natively; native <details> name+animation resurgence; Disclosure split out; Material dropped Expansion Panel for Expressive Lists"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-accordion/` (15 June 2026), the second Navigation-category brief and Tabs' vertical cousin. Both passes converged on the spine — the accordion-vs-tabs boundary (vertical multi-open inline-expansion + heading/button/region vs. horizontal one-at-a-time view-swap + tablist/roving-tabindex), the Disclosure/DisclosureGroup decomposition (a single collapsible primitive + the coordinated set, paralleling the catalogue's atomic-vs-set patterns), multi-open as the default with single-open + allow-all-closed opt-ins (force-one-open → use Tabs), the heading-wrapped-`button[aria-expanded]` + region pattern with each header its own tab stop (NOT tabs' roving tabindex) and the APG-optional arrow keys, the heading-level outline contract (a `headingLevel`/`as` prop), the height-animation problem and its native resolution (`grid-template-rows: 0fr/1fr` → `interpolate-size`/`calc-size`), chevron rotation + reduce-motion snap, flush-vs-contained variants, the nested-accordion prohibition (→ Tree), expand-all/collapse-all, scroll-into-view, hash deep-linking, the whole-header hit target, and `Accordion`/`AccordionItem` + `Disclosure` naming. The external pass pushed the **native-`<details>`-first** position harder (given the `name` attribute for zero-JS exclusivity, `::details-content` + `transition-behavior: allow-discrete`, and `calc-size`/`interpolate-size` for animation) — adopted, with custom ARIA reframed as the path for controlled `expandedKeys` state and legacy support rather than the default; it also contributed the Carbon `<ul>/<li>` group-context and responsive right-margin rules, the Tree-vs-Accordion chevron-direction contrast, the scroll-into-view/`rAF` technique, and the Material-dropped-Expansion-Panel/Expressive-Lists evolution. Claude-pass contributions: the framing as Tabs' cousin with the mobile tabs→accordion transform as the key tie, the explicit Disclosure-primitive decomposition parallel, and the native-where-it-suffices/custom-for-controlled-state reconciliation. The `calc-size`/`interpolate-size`/`<details name>`/`::details-content` platform features and the 2025/2026 version numbers are flagged unverified. Conformant to `components/_schema.md`. Second Navigation brief; Tree and the routing nav/Link are the adjacent threads remaining.*
