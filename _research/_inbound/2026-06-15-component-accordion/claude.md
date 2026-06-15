# Accordion — field-truth study (Claude pass)

## 1. Framing
An Accordion is a **vertical stack of expand/collapse sections**, each a header that toggles a region of content — used to progressively disclose / compress long content into scannable headers. It is the vertical, often-multi-open cousin of Tabs (see tabs): where Tabs show **one** panel at a time in a horizontal row via the tablist/tab/tabpanel + roving-tabindex pattern, an Accordion can show **many (or zero)** sections at once and uses a **completely different ARIA pattern** — a heading wrapping a `<button aria-expanded aria-controls>` that toggles a region (NOT a tablist). What it is: disclosure of independent or loosely-related content sections (an FAQ, a settings group, a filter sidebar). What it isn't: **one-at-a-time horizontal panels** (→ Tabs), a **single** standalone collapsible (→ a Disclosure — the atomic primitive, §2), a **hierarchical tree** (→ Tree), or **routing**. Why systems disagree: the **Disclosure-vs-Accordion decomposition**, **single-open vs. multi-open**, **native `<details>` vs. custom ARIA**, and the **height-animation problem**.

## 2. Anatomy and parts — the disclosure decomposition
A single expand/collapse section is a **Disclosure** (a header button + a region); an **Accordion** is a *set* of disclosures with optional cross-coordination (single-open). This parallels the catalogue's atomic-vs-set decompositions (checkbox/segmented). The practice ships **`Disclosure`** (the standalone collapsible — "Show more", a single FAQ) **+ `Accordion`/`AccordionItem`** (the coordinated set). Per-item parts:
- **Heading wrapper** — a real `<h2>`/`<h3>` (correct outline level) containing only the trigger.
- **Trigger button** — `<button aria-expanded aria-controls>`; the whole header is the hit target; holds the label + a rotating chevron indicator.
- **Region/panel** — the collapsible content (`role=region` + `aria-labelledby`→the button, when there are few enough regions; or a plain container).
- optional **expand-all/collapse-all** control at the set level.

## 3. Properties / API
- **`allowMultiple` / `selectionMode`** — multi-open (default) vs. single-open (exclusive). The headline prop.
- **`expandedKeys` / `defaultExpandedKeys` / `onExpandedChange`** — controlled/uncontrolled open set (array; a single key for exclusive). Key-based, not index (the tabs lesson).
- **`allowAllClosed`** (or `collapsible`) — may every section be closed, or must one stay open? Default allow-all-closed for multi; for single-open, expose both.
- per-item: `key`, `title`/header, `isDisabled`, default-expanded.
- composition: `<Accordion><AccordionItem>` children (over a data array), associated by key.
- native passthrough where using `<details>`: the `name` attribute groups single-open `<details>` natively (§11).

## 4. States and variants
States (per item): collapsed / expanded (`aria-expanded`) / hover / focus-visible (ring on the header button) / disabled. Variants: **flush** (dividers only) vs. **contained/boxed** (each item a card); with-icon/indicator; expand-all affordance; nested (discouraged). No tone.

## 5. Usage guidance
- **Use** to compress long, scannable, independently-consumed content into headers the user opens as needed: FAQs, settings sections, filter groups, progressive detail.
- **Don't use** for: content the user needs **most/all of at once** (just show it — accordions add interaction cost and hide content from in-page scanning); **one-at-a-time horizontal** sections (→ Tabs); a **single** collapsible (→ Disclosure); **hierarchical** data (→ Tree); **sequential** steps (→ Stepper); **navigation/routing** (→ nav).
- **Decision frameworks:**
  - **Accordion vs. Tabs** — vertical, multi-open, content-compression (Accordion) vs. horizontal, one-at-a-time, peer-panel switching (Tabs). **Tabs commonly become accordions on mobile** (the responsive transform) — narrow viewports favour vertical stacking over a horizontal overflow row.
  - **Accordion vs. Disclosure** — a *set* vs. a *single* collapsible.
  - **Single vs. multi-open** — multi-open (independent) by default; single-open (exclusive) only when sections are genuinely mutually-exclusive views or vertical space is tight and you want at most one expanded.
- **Don't hide critical/always-needed content** behind a collapsed header, and avoid nesting accordions (disorienting).

## 6. Accessibility
- **The pattern is heading + button + region, NOT tablist** (APG Accordion): each header is a `<button aria-expanded="true|false" aria-controls="panelId">` **wrapped in a heading element of the correct level** (`<h3><button>…</button></h3>`) so the document outline stays intact and screen-reader users can navigate by heading. The panel is the controlled region (`role=region` + `aria-labelledby` the button — though `role=region` on every panel can be verbose, so some systems reserve it; the button↔panel `aria-controls`/`aria-expanded` wiring is the non-negotiable part).
- **Each header is its own tab stop** — Tab moves between headers (and into open panels). This is **the key keyboard difference from Tabs**: an accordion does *not* use roving tabindex; every header is in the natural tab order. **Enter/Space** toggles. The APG offers **optional** Up/Down arrow movement between headers + Home/End — a nice-to-have, not required; if implemented, it must not trap or replace Tab.
- **Heading level is a real contract** — pick the level that fits the surrounding outline; don't hard-code `<h3>` if it breaks hierarchy (expose a `headingLevel` prop or `as`).
- **Expanded content is in the DOM and reachable**; collapsed content is `hidden` (removed from tab order and AT). On expand, optionally scroll the header into view if the panel pushes content.
- **WCAG SCs:** 4.1.2 (button + expanded state), 1.3.1 (heading structure), 2.1.1 (keyboard), 2.4.13/1.4.11 (focus + indicator contrast), 1.4.1 (indicator not colour-only).

## 7. Content guidelines
Header labels: concise, parallel, scannable noun phrases or questions (FAQ); they're the information scent for collapsed content, so they must telegraph what's inside. The **whole header is the click/tap target** (button spans the row, not just the chevron). Don't bury content the user always needs. Expand-all/collapse-all copy where the set is long.

## 8. Motion and transition
The signature motion is the **height expand/collapse**, and it's the hard part: animating `height: 0 → auto` isn't natively possible, so the field uses **`grid-template-rows: 0fr → 1fr`** (the modern CSS trick), **`interpolate-size: allow-keywords` + `calc-size(auto)`** (the newest platform feature — verify support), the **max-height hack** (brittle), or **JS-measured height**. The chevron rotates (~150–200ms). Under `prefers-reduced-motion: reduce`, snap open/closed (no height tween) — keep the state change instant. Native `<details>` historically couldn't animate; `::details-content` + `calc-size` now enable it (verify). (See 18/19.)

## 9. Internationalization
RTL flips the chevron side (leading edge) and any directional indicator; header text expands (de/ru) — headers wrap or truncate-with-care (unlike tabs, accordion headers *can* wrap, since they're stacked). Inherits general i18n. (See 13.)

## 10. Naming
`Accordion` + `AccordionItem` (+ `AccordionTrigger`/`AccordionPanel` in compound APIs) is the field default (Radix, Spectrum, Carbon, Material). The single primitive is **`Disclosure`** (React Aria, Headless UI `Disclosure`) or `Details`. Practice default: **`Accordion`/`AccordionItem`** (the set) **+ `Disclosure`** (the single collapsible). Aliases: `Collapse`, `Expander`, `Details`, `ExpansionPanel` (old Material).

## 11. Implementation notes
- **Native `<details>`/`<summary>` vs. custom ARIA** — `<details>` gives expand/collapse, keyboard, and (with `name`) native single-open exclusivity for *free*, and is the right default for simple disclosures; custom ARIA is needed for animated height (until `calc-size` is universal), rich headers, controlled state, and precise styling. The native-vs-custom call parallels select §11 — prefer native where it suffices, custom when the requirements exceed it.
- **The height animation** (§8) — `grid-template-rows` is the current robust default; `interpolate-size`/`calc-size(auto)` is the emerging native path (verify).
- **Controlled `expandedKeys`** (key-based) with the controlled-without-onChange trap; single-open coordinates by closing others.
- **`<details name>`** natively makes a single-open accordion (exclusive) — the platform feature (verify support); great for the no-JS case.
- **Scroll-into-view + deep-linking** — optionally scroll an expanding header into view; a URL hash can open a section on mount (and `:target` even works with native `<details>`).
- **Don't hand-roll** the ARIA — React Aria `useDisclosure`/`Disclosure`, Radix Accordion, Headless UI; skin it.

## 12. Related and alternative components
- **Composes with:** Disclosure (the primitive), heading, Icon (chevron), Card/Section (the contained variant), an expand-all Button.
- **Alternative to:** Tabs (horizontal one-at-a-time — see tabs), Disclosure (single), Tree (hierarchical), Stepper (sequential).
- **Supersedes:** ad-hoc show/hide `<div>`s without `aria-expanded`/heading semantics; a tablist misused for vertical multi-open sections.
- **Superseded by:** Tabs on wide viewports when one-at-a-time peer panels fit better; just showing the content when it's all needed.

(Tabs' vertical cousin; the Disclosure/Accordion decomposition parallels the catalogue's atomic-vs-set patterns (checkbox/segmented). See tabs for the boundary from its side, 03-component-library, 29 for the docs template.)

## 13. Field POV evolution
1. The **CSS height-animation problem is finally being solved natively** — `grid-template-rows: 0fr/1fr` then `interpolate-size: allow-keywords` + `calc-size(auto)`, replacing max-height/JS hacks.
2. **Native `<details>` got real** — the `name` attribute (exclusive single-open accordions, no JS) and `::details-content`/animatable disclosure, narrowing where custom is needed (the select-like native resurgence).
3. **Disclosure split out** as a named primitive (React Aria) rather than folding single-collapsible into Accordion.
4. **Heading-wrapped triggers** affirmed as the correct pattern over bare buttons (outline integrity).

## 14. Sources cited
(Conservative; reconcile with external.) Adobe Spectrum / React Aria `Disclosure`/`DisclosureGroup`(Accordion), `useDisclosure` (2024–2025); Radix `Accordion` (`type=single|multiple`, `collapsible`) (2024); IBM Carbon `Accordion`/`AccordionItem` (2024); Shopify Polaris (Collapsible) (2024); GitHub Primer (2024); Atlassian (2024); Base Web `Accordion`/`Panel` (2024); Material (ExpansionPanel→) (2024); MDN/CSS WG — `<details name>`, `::details-content`, `interpolate-size`/`calc-size` (2024–2025); WAI-ARIA APG Accordion + Disclosure patterns; WCAG 2.2 (Oct 2023) — 4.1.2, 1.3.1, 2.1.1, 2.4.13, 1.4.11, 1.4.1.

## 15. Agent-consumable schema (conform to _schema.md in accordion.md)
identity/description/anatomy(Disclosure primitive + Accordion/AccordionItem set; heading+button+region)/api(allowMultiple|selectionMode, expandedKeys, allowAllClosed)/states(collapsed/expanded/hover/focus/disabled)/variants(flush|contained, with-icon, single|multi, nested)/accessibility(heading+button[aria-expanded]+region NOT tablist; each header own tab stop vs tabs' roving; APG optional arrows; heading-level contract)/content(scannable header labels, whole-header hit target)/motion(height grid-template-rows 0fr->1fr / calc-size; chevron; reduce-motion snap)/i18n(RTL chevron; headers may wrap)/implementation(native <details>+name vs custom; height animation; controlled expandedKeys; deep-link via :target)/composition(Disclosure primitive, Tabs alt, Tree)/notes(disclosure-vs-accordion decomposition; single-vs-multi-open; native-vs-custom; height-animation; accordion-vs-tabs + mobile transform).
