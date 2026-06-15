# Tabs — field-truth study (Claude pass)

## 1. Framing
Tabs let a user switch among **mutually-exclusive panels of content in the same context**, showing one at a time. It is the first Navigation-category brief and does **not** inherit the form-field substrate (no label/helper/error). It shares mechanics with Segmented Control (a horizontal single-select row, roving tabindex, a sliding active indicator) but is defined by the one thing segmented controls lack: **it owns panels** (`role=tablist`/`tab`/`tabpanel`). What it is: in-page disclosure of parallel content sections (Details / Reviews / Specs). What it isn't: a **value/filter switch in place** (→ Segmented Control — segmented §5, the boundary from the other side), **site navigation that changes the URL/route** (→ a nav landmark with links + `aria-current`, NOT a tablist — the most-violated tabs boundary), a **sequential flow** (→ Stepper/Wizard), or **stacked expand/collapse** (→ Accordion, which is tabs' vertical/multi-open cousin). Why systems disagree: **manual vs. automatic activation**, **lazy panel mounting**, **overflow handling**, and the **routing boundary**.

## 2. Anatomy and parts
- **Tablist** (`role=tablist`) — the container of tabs; owns orientation + roving tabindex.
- **Tab** (`role=tab`) — the clickable label; `aria-selected`, `aria-controls`→panel, `tabindex` per roving model; may carry an icon, a count badge, or a close affordance.
- **Tabpanel** (`role=tabpanel`) — the content region; `aria-labelledby`→its tab, `tabindex=0` so it's focusable/scrollable.
- **Active indicator** — the underline/pill that marks (and often slides to) the selected tab (the segmented-pill mechanic).
- **Overflow affordance** — scroll buttons / swipe / a "more" menu when tabs exceed the width (§overflow).

## 3. Properties / API
- **`selectedKey` / `defaultSelectedKey` / `onSelectionChange`** — the active tab (key-based, like a collection; React Aria's model). Controlled + uncontrolled.
- **`activationMode`** — `automatic` (default) | `manual` (§6) — the headline contested prop.
- **`orientation`** — horizontal (default) | vertical.
- **composition** — `<Tabs><TabList><Tab/></TabList><TabPanel/></Tabs>` (compound) is the field default over a data array, because panels are arbitrary JSX. Tab↔panel association is by key/order.
- **lazy mounting** — a `forceMount`/`keepMounted` or render-prop control over mount-all vs. mount-on-activate vs. keep-alive (§11).
- per-tab: `key`, `isDisabled`, icon/badge, `isClosable` (closable variant).
- `isClosable`/`onClose` + add affordance for the browser/editor-tab variant.

## 4. States and variants
States: rest / hover / focus-visible (ring on the tab) / **selected** (`aria-selected`, indicator) / disabled (per-tab). Panels: hidden vs. shown; focusable. Variants: **underline vs. contained** (the two visual styles); **horizontal vs. vertical**; **scrollable / overflow-menu** (many tabs); **with icon / count badge**; **closable + addable** (the editor-tab pattern). No tone/emphasis.

## 5. Usage guidance
- **Use** to organize parallel, peer content sections in one context where the user views one at a time and switching is cheap (a product page's Details/Reviews/Specs; a settings area's sections).
- **Don't use** for: a **value/filter/view switch that mutates the current panel in place** (→ Segmented Control — segmented §5); **navigation that changes the route/URL** (→ a `<nav>` of links + `aria-current`, not tabs); a **required sequence** (→ Stepper/Wizard); content the user needs to **compare side-by-side** (→ show both, not tabs); or **many independent expandable sections** (→ Accordion). Don't nest tabs within tabs (disorienting).
- **Decision frameworks:**
  - **Tabs vs. Segmented Control** = *panels vs. value-in-place*. If selecting swaps a whole content region with its own layout/data → Tabs; if it re-sorts/filters/re-visualizes the current view → Segmented.
  - **Tabs vs. Navigation (routing)** = *in-page disclosure vs. route change*. If the URL changes and it's a destination, it's navigation (links), not a tablist — even if it looks like tabs.
  - **Tabs vs. Accordion** = horizontal one-at-a-time (tabs) vs. vertical, possibly-multi-open, stacked (accordion); accordion is better on narrow/mobile.

## 6. Accessibility
- **The ARIA tabs pattern (APG):** `role=tablist` wraps `role=tab`s; each tab has `aria-selected` and `aria-controls`→its `role=tabpanel`; the panel has `aria-labelledby`→its tab and `tabindex=0` (so keyboard users can scroll/focus the content). The tablist is a **single tab stop** (roving tabindex: the selected tab is `tabindex=0`, the rest `-1`); **arrow keys** move between tabs (Left/Right horizontal; Up/Down vertical), **Home/End** to first/last; **Tab** from the tablist moves to the active panel.
- **Manual vs. automatic activation — the headline call.** *Automatic* (selection-follows-focus): arrowing to a tab immediately selects it and shows its panel — fast, fewer keystrokes, the APG default. *Manual*: arrowing only moves focus; Enter/Space activates. **The practice default is automatic**, with **manual required when panel switching is expensive or async** (a fetch, a heavy render) — the same expensive-side-effect logic as radio's selection-follows-focus and segmented's, made concrete by the APG's own guidance. Expose `activationMode`.
- **Routing tabs are not a tablist** — if activation changes the route, use a `<nav>` + links + `aria-current="page"`; `role=tab` on a link misrepresents it to AT (§5).
- **Panel focus management** — on activation, focus stays on the tab (the user arrows on); the panel is reachable via Tab. Don't move focus into the panel on selection unless the panel's first action warrants it.
- **WCAG SCs:** 4.1.2 (tab/panel roles + selected), 2.1.1 (keyboard), 1.4.11/2.4.13 (focus + indicator contrast), 1.4.1 (selected not colour-only — the indicator + `aria-selected`), 2.4.3 (focus order).

## 7. Content guidelines
Short, parallel **noun** labels (1–2 words: "Overview", "Activity", "Settings"), no verbs, **no multiline** (wrapping breaks the tablist), scannable. Icons optional and consistent (all-or-none, like segmented). Count badges show quantity ("Comments 12"). Avoid too many tabs (the overflow signal — reconsider the IA past ~6–7). The tablist should have an accessible name (`aria-label`) when its purpose isn't obvious from context.

## 8. Motion and transition
The **active indicator slides** between tabs (~150–200ms, the segmented-pill mechanic; measured, not pseudo-element). Panel transitions: a quick cross-fade is acceptable, but avoid sliding panels (janky, and it implies a spatial sequence tabs don't have). Under `prefers-reduced-motion: reduce`, snap the indicator and drop panel transitions. Lazy-mounted panels shouldn't animate layout on first mount. (See 18/19.)

## 9. Internationalization
**RTL flips tab order and indicator/arrow direction** (Left/Right arrows swap meaning, via logical layout). Labels expand (de/ru) — another reason scrollable/overflow handling matters and equal-width tabs are fragile. Vertical tabs sidestep horizontal expansion. (See 13.)

## 10. Naming
`Tabs` (the root) + `TabList` + `Tab` + `TabPanel(s)` is the converged compound naming (React Aria, Radix, Spectrum). Some systems: `TabNav` (routing variant — Primer separates `TabNav` for links from `UnderlineNav`/tabs), `Tab.Group/List/Panels` (Headless UI). **Practice default: `Tabs` / `TabList` / `Tab` / `TabPanel`**, with a **distinct `TabNav`/nav-links component for the routing case** (don't overload Tabs with routing). Aliases: `TabGroup`, `TabBar`, `Segmented`(mis-conflation — see segmented-control).

## 11. Implementation notes
- **Roving tabindex** on the tablist (selected tab `tabindex=0`, rest `-1`); arrow handler moves focus + the `0`; `aria-activedescendant` is the alternative but roving is the APG norm.
- **Panel mounting strategy is a real decision:** mount-all (simple, SEO/print-friendly, but heavy + all panels' effects run), mount-on-activate (light, but loses panel state on switch and re-runs effects), or keep-alive (mounted-but-hidden via `hidden`, preserving state at a memory cost). Expose the choice (`keepMounted`/`forceMount`); default to mount-on-activate with keep-alive opt-in for stateful panels.
- **Indicator measurement** — like the segmented pill, a measured/translated element (ResizeObserver, recompute on resize/RTL/label change), not a per-tab pseudo-element.
- **Deep-linking without routing** — tab state can live in a URL *query param* (`?tab=reviews`) read on mount, which is *not* the same as route-based navigation tabs; this keeps `role=tab` correct while allowing shareable state. Genuine route changes → the nav-links variant.
- **Don't hand-roll** — React Aria `useTabList`/`useTab`/`useTabPanel`, Radix Tabs, Headless UI for the focus/keyboard/ARIA contract; skin it.
- **Controlled `selectedKey`** with the controlled-without-onChange trap; key-based selection over index (stable across reorder).

## 12. Related and alternative components
- **Composes with:** TabList/Tab/TabPanel (the parts), Icon (tab icons), Badge (count), Button/Icon (close affordance on closable tabs), the overflow Menu.
- **Alternative to:** Segmented Control (value-in-place — see segmented-control), a nav of links (routing — the boundary), Accordion (vertical/multi-open), Stepper/Wizard (sequential), Carousel (auto-advancing peer content).
- **Supersedes:** ad-hoc show/hide `<div>`s without the tablist ARIA; `role=tab` misused for routing (→ nav links).
- **Superseded by:** Accordion on narrow viewports; a nav landmark when it's really routing.

(First Navigation brief; shares the roving-tabindex + sliding-indicator mechanics with segmented-control but owns panels. See segmented-control for the boundary from its side, button for the close-affordance, 03-component-library, 29 for the docs template.)

## 13. Field POV evolution
1. **Manual activation guidance hardened** — the APG's "manual when expensive/async" is now widely followed, not just automatic-everywhere.
2. **Routing tabs split out** as a distinct component (Primer's `TabNav`/`UnderlineNav` vs. `Tabs`) — the role=tab-isn't-for-routing rule landing in APIs.
3. **Lazy mounting** is now an explicit, documented prop rather than an implicit default.
4. **Key-based selection** (over index) standardised via collection APIs (React Aria).
5. Underline-style tabs dominant over heavy contained "folder" tabs; the sliding indicator is the norm.

## 14. Sources cited
(Conservative; reconcile with external.) Adobe Spectrum / React Aria `Tabs`/`TabList`/`Tab`/`TabPanels`, `useTabList`, activation modes (2024–2025); Material 3 tabs (primary/secondary, scrollable) (2024); IBM Carbon `Tabs` (contained/line, dismissable) (2024); Shopify Polaris `Tabs` (2024); GitHub Primer `UnderlineNav`/`TabNav` vs. tab panels (2024); Atlassian `Tabs` (2024); Base Web `Tabs` (2024); Headless UI `Tab.Group`; Radix `Tabs`; Apple HIG tab bars / Material Compose (2024); WAI-ARIA APG Tabs pattern (manual/automatic activation, roving tabindex); WCAG 2.2 (Oct 2023) — 4.1.2, 2.1.1, 1.4.11, 2.4.13, 1.4.1, 2.4.3.

## 15. Agent-consumable schema (conform to _schema.md in tabs.md)
identity/description/anatomy(tablist/tab/tabpanel/indicator/overflow)/api(selectedKey, activationMode automatic|manual, orientation, lazy mounting, closable)/states(rest/hover/focus/selected/disabled)/variants(underline|contained, horizontal|vertical, scrollable, closable, with-icon/badge)/accessibility(tablist/tab/tabpanel + roving tabindex + manual-vs-automatic + routing-is-not-a-tablist)/content(short parallel nouns, no multiline)/motion(indicator slide, panel cross-fade)/i18n(RTL order+arrows)/implementation(roving tabindex, mounting strategy, indicator measurement, deep-link via query param not routing)/composition(segmented-control alt, nav-links for routing, accordion)/notes(manual-vs-automatic; tabs-vs-routing; lazy-mounting; tabs-vs-segmented).
