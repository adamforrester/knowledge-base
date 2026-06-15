---
okf_version: "0.1"
type: component-brief
title: Tabs
description: The first Navigation brief — in-page panel switching, and the component most often misused for routing. A field-truth study of the tablist/tab/tabpanel + roving-tabindex contract, the manual-vs-automatic activation decision (automatic default, manual when switching is expensive), the tabs-vs-routing boundary (route changes are nav links, not a tablist), the tabs-vs-segmented boundary (panels vs. value-in-place), the panel-mounting trilemma, and overflow handling, with the practice's defaults.
tags: [components, navigation]
category: Navigation
status: stable
aliases: [tab-list, tab-panel, tab-group, tab-bar]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Tabs

> Tabs is the first Navigation brief, and the component the field most consistently *misuses* — because a horizontal row of labels looks like navigation, teams reach for `role="tab"` to change routes, and ship a broken contract where the screen reader announces an in-place panel swap while the browser performs a page load. The whole brief turns on one rule with two boundaries: **tabs swap panels in place** — they are not routing (that's a nav of links), and they are not a value-in-place switch (that's a Segmented Control). It shares mechanics with Segmented Control (the roving-tabindex row, the sliding indicator) but is defined by the one thing a segmented control lacks: **it owns panels.** Does not inherit the form-field substrate — Tabs is a disclosure/navigation pattern, not a form control.

---

## 1. Framing

Tabs organize **parallel sections of related content in one context**, showing one panel at a time and hiding the rest (`role=tablist`/`tab`/`tabpanel`). What it *is*: in-page disclosure of peer content — a product page's Description / Specs / Reviews, a settings area's sections. What it *isn't*, and these boundaries are the brief's spine:

- **Not routing.** Tabs must swap panels in place without changing the URL or triggering a page load. If clicking changes the route, it is **navigation** — a `<nav>` of anchor links with `aria-current`, *not* a tablist (§5). This is the most-violated tabs boundary; the field is now bifurcating the component to enforce it (Primer's `UnderlineNav` for routing vs. `UnderlinePanels` for in-place tabs).
- **Not a value-in-place switch** (→ Segmented Control — see segmented-control). A segmented control filters/toggles a variable of the *current* view (form semantics, a styled radio group); Tabs reveal an *entirely different structural panel* with its own layout and data. Both share the horizontal roving-tabindex row and sliding indicator; the semantic payload is opposite.
- **Not a sequence** (→ Stepper/Wizard — lateral peer movement vs. a dependent ordered journey) or **stacked multi-open disclosure** (→ Accordion — tabs' vertical, often-mobile cousin).

Why systems disagree: **manual vs. automatic activation**, the **panel-mounting strategy**, **overflow handling**, and the routing boundary.

## 2. Anatomy and parts

Strictly governed by the ARIA roles, so the node tree is highly converged (both agents). Tabs **shares the roving-tabindex row and the sliding active-indicator with Segmented Control** (segmented-control §2) — noted, not re-derived. Parts:

- **`TabList`** (`role=tablist`) — the container of triggers; owns roving tabindex, orientation, and overflow behaviour.
- **`Tab`** (`role=tab`) — the trigger: a short label, optional leading icon, optional count badge, optional close affordance (closable variant); carries `aria-selected` + `aria-controls`.
- **Active indicator** — the underline or contained-pill that marks (and slides to) the selected tab.
- **Overflow affordance** — scroll buttons / a swipe-with-fade-mask / a "More" menu when tabs exceed the width (§overflow).
- **`TabPanels`** (optional wrapper, manages layout/transitions) → **`TabPanel`** (`role=tabpanel`) — the content region, `aria-labelledby`→its tab, `tabindex=0` so it's focusable/scrollable.

Compositional/headless exposure (`<Tabs><TabList><Tab/></TabList><TabPanel/></Tabs>`) is the field default over a config array, so consumers can wrap a tab in a tooltip or inject custom nodes without breaking the ARIA wiring (§13).

## 3. Properties / API

(No form-field substrate to inherit.) Converged + contested:

- **`selectedKey` / `defaultSelectedKey` / `onSelectionChange`** — controlled/uncontrolled active tab. **Key-based, not index-based** — both passes reject the index pattern: in a mutable/reorderable tab collection, an index causes catastrophic state-mismatch (wrong panel after a data mutation); a stable string key maps correctly regardless of order (React Aria's model).
- **`activationMode` / `keyboardActivation`** — `automatic` (default) | `manual` — the headline contested prop (§6).
- **`orientation`** — horizontal (default) | vertical (arrows swap to Up/Down).
- **`disabledKeys` / per-tab `isDisabled`** — for permission-gated views (with the disabled-active-tab focus trap to handle, §11).
- **panel mounting** — `forceMount`/`keepMounted` control over the mount trilemma (§11).
- per-tab: `key`, icon, badge, `isClosable`/`onClose` (the browser/editor-tab variant).
- composition: `<Tab>`/`<TabPanel>` children, associated by key — over a data array.

## 4. States and variants

States (per `Tab`): rest / hover / focus-visible (high-contrast ring marking the roving position — which can sit on a *different* tab than the selected one, so the ring and the indicator are distinct signals) / **selected** (`aria-selected`, indicator, heavier weight) / disabled (per-tab, excluded from the roving sequence). Panels: hidden vs. shown; `tabindex=0`.

**Variants:** **Line/underline** (the default, for primary page-level organization, flush against a divider) vs. **Contained/pill** (for nested/localized switching — the visual-weight hierarchy that prevents disorientation when tab sets stack; Material encodes it as `PrimaryTabRow`/`SecondaryTabRow`); **horizontal vs. vertical** (vertical for >~6 categories or doc-style nav); **scrollable / overflow-menu**; **with icon / count badge**; **closable + addable** (the editor-tab pattern, requiring careful focus management on close). The practice ships **line for primary, contained for nested**. No tone/emphasis.

## 5. Usage guidance

- **Use** to organize parallel, peer content sections in one context, viewed one at a time, where switching is cheap and the URL needn't change.
- **Don't use** for: a **route change** (→ a `<nav>` of links + `aria-current` — *the* boundary); a **value/filter/view switch of the current panel** (→ Segmented Control — see segmented-control); a **required sequence** (→ Stepper/Wizard); content meant for **side-by-side comparison** (show both); **many independent expandable sections** (→ Accordion, also better on narrow viewports); and **never nest beyond two levels** (primary + secondary max — deeper guarantees overload; switch to vertical or a tree).
- **Decision frameworks:**
  - **Tabs vs. Navigation (routing)** — *in-place panel swap vs. route change*. If the URL changes and it's a destination, it's navigation (links), not a tablist, however tab-like it looks. (Deep-linking to a tab without routing is still allowed — §11.)
  - **Tabs vs. Segmented Control** — *distinct panels vs. value-in-place*. Different structural schema/data → Tabs; re-filter/re-sort/re-visualize the current view → Segmented.
  - **Tabs vs. Accordion** — horizontal one-at-a-time (desktop) vs. vertical, possibly-multi-open, stacked (mobile-friendly).

## 6. Accessibility

The APG tabs pattern, which is rigorously specified:

- **Role contract:** `role=tablist` wraps `role=tab`s; each `Tab` has `aria-selected` (`true`/`false`, explicit on all) and `aria-controls`→its panel; each `role=tabpanel` has `aria-labelledby`→its tab and **`tabindex=0`** (so keyboard users reach the content without tabbing through every interactive element first). Bidirectional wiring keeps both the tab and the panel self-describing to AT.
- **Roving tabindex:** the tablist is one composite tab stop — the active tab is `tabindex=0`, the rest `-1`; **Tab** enters/exits the whole list, **arrows** move between tabs (Left/Right horizontal, Up/Down vertical), **Home/End** jump to first/last. (Shared with segmented-control; the difference is Tab-then-Tab moves into the *panel*.)
- **Manual vs. automatic activation — the headline call, resolved.** *Automatic* (selection-follows-focus): arrowing instantly selects the focused tab and swaps the panel — the APG default, fewer keystrokes. *Manual*: arrowing moves focus only; Enter/Space activates. **The practice defaults to automatic, and requires manual when a panel switch is expensive** — a network request, async data, a heavy render — because automatic makes a keyboard user arrowing past three tabs fire three expensive loads. This is the same expensive-side-effect logic as radio's selection-follows-focus (radio §6) and segmented's, made deterministic by the APG. Expose `activationMode`.
- **Routing is not a tablist** — `role=tab` on a route-changing link misrepresents it; use `<nav>` + links + `aria-current` (§5).
- **Panel focus** stays on the tab after activation (the user keeps arrowing); the panel is reachable via Tab. Count badges announce coherently ("Errors, 4 items", via visually-hidden text), and icon-only tabs need an `aria-label` + tooltip.
- **WCAG SCs:** 4.1.2 (tab/panel roles + selected), 2.1.1 (keyboard), 1.4.11/2.4.13 (focus ring + indicator contrast), 1.4.1 (selected conveyed by more than colour — the indicator + `aria-selected`), 2.4.3 (focus order).

## 7. Content guidelines

Short, **parallel noun** labels (1–2 words — "Overview", "Activity", "Settings"), never verbs ("View Details") which kill scannability and wrap awkwardly. **No multiline for horizontal tabs** — overflow (scroll/menu) instead of wrapping; the only exception is vertical tabs, which may wrap to two lines then truncate-with-tooltip. Icons must be universally legible or carry an `aria-label`+tooltip; count badges show quantity and announce as part of the label. The tablist needs an accessible name (`aria-label`) when context doesn't supply one. Past ~6–7 tabs, reconsider the IA (the overflow signal).

## 8. Motion and transition

The **active-indicator slide** is the signature motion (shared with the segmented pill): the underline/pill animates `translateX`+`width` to the target tab (~150–200ms), measured via `getBoundingClientRect` + a `ResizeObserver` (recompute on resize, late-font-load, RTL) — and increasingly delegated to **CSS Anchor Positioning / the View Transitions API**, retiring the JS measurement (§13). Panel transitions: a quick cross-fade or a 4–8px slide-up softens the swap (React Aria exposes `--tab-panel-width`/`-height` to animate dimension changes so a short panel replacing a tall one collapses smoothly rather than snapping); avoid sliding panels horizontally (implies a sequence tabs don't have). Under `prefers-reduced-motion: reduce`, snap the indicator and drop panel transitions. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

**RTL mirrors order and inverts the math:** tab order flows right-to-left, leading icons swap sides, and the indicator's `translateX` negates. **The keyboard remaps to logical direction** — in RTL, ArrowLeft advances to the logically-next tab and ArrowRight goes back (intercept `dir` in the roving handler). **Text expansion** (de/ru +150–200%) is the reason overflow handling is load-bearing and equal-width tabs are fragile; horizontal tabs can't wrap, so they must fall into scroll/overflow gracefully. Vertical tabs sidestep horizontal expansion. (See 13-internationalization-and-rtl.)

## 10. Naming

The converged compound naming mirrors the ARIA roles: **`Tabs`** (root/state) / **`TabList`** / **`Tab`** / **`TabPanels`** (optional wrapper) / **`TabPanel`** (React Aria, Radix, Chakra, Base Web). **The practice adopts this five-part naming**, and — critically — ships a **distinct component for the routing case** (a `TabNav`/nav-links pattern, after Primer's `UnderlineNav` vs. `UnderlinePanels` split) rather than overloading `Tabs` with `href` routing (§5). Aliases to map: `TabGroup`, `TabBar`, `UnderlinePanels`; and `Segmented`/`SegmentedControl` as the *mis-conflation* to disambiguate (see segmented-control).

## 11. Implementation notes

- **The panel-mounting trilemma is the contested implementation call:**
  - **Mount-all** (all panels in the DOM, inactive ones `hidden`) — enables browser Find-in-Page, SEO indexing, and correct printing, but loads every panel's content/effects upfront (heavy for data viz).
  - **Mount-on-activate (lazy)** — instant initial load, but switching away **unmounts and destroys** the panel's local state (a half-filled form, an expanded tree, an iframe) — the fatal trap.
  - **Keep-alive** — mount on first activation, then keep mounted-but-`hidden` (state preserved at a memory cost) — the enterprise compromise.
  - **The practice defaults to mount-on-activate, with keep-alive opt-in for stateful panels and mount-all (`forceMount`) opt-in for SEO/print.** Expose the choice.
- **Disabled-tab focus trap:** if the active tab becomes disabled by an async permission change, the roving engine must shift `tabindex=0` to the nearest viable sibling — otherwise the keyboard user is stranded in a focus black hole.
- **Deep-linking without routing:** bind `selectedKey` to a URL **hash or query param** (`?tab=billing`), parse it on mount into `defaultSelectedKey`, and update it via the History API **without** a routing event — satisfying shareable links *and* the in-place-swap contract. Genuine route changes → the nav-links component.
- **Indicator measurement** — measured/translated element + `ResizeObserver`, not a per-tab pseudo-element (shared with segmented-control §11); migrating to CSS Anchor Positioning.
- **Don't hand-roll** — React Aria `useTabList`/`useTab`/`useTabPanel`, Radix Tabs, Headless UI for the focus/keyboard/ARIA contract; skin it. Controlled `selectedKey` carries the controlled-without-`onChange` trap.

## 12. Related and alternative components

- **Composes with:** TabList/Tab/TabPanel (the parts), Icon (tab icons — see icon), Badge (count), Button/Icon (the close affordance on closable tabs), the overflow Menu.
- **Alternative to:** Segmented Control (value-in-place — see segmented-control), a nav of links (routing — the boundary; `aria-current`, not `role=tab`), Accordion (vertical/multi-open/mobile), Stepper/Wizard (sequential), Carousel (auto-advancing peer content).
- **Supersedes:** ad-hoc show/hide `<div>`s without the tablist ARIA; `role=tab` misused for routing (→ nav links).
- **Superseded by:** Accordion on narrow viewports; a nav landmark when it is really routing.

(The first Navigation brief; shares the roving-tabindex + sliding-indicator mechanics with segmented-control but owns panels — see segmented-control for the boundary from its side, button for the close affordance, icon/badge for tab adornments. 03-component-library; 29 for the docs template. Accordion and the routing `TabNav`/Link are the adjacent Navigation briefs to come.)

## 13. Field POV evolution

1. **Monolithic → headless/compositional.** Config-array "black-box" tabs (early Polaris, Bootstrap) gave way to exposed `TabList`/`Tab`/`TabPanel` parts (React Aria, Radix, Base Web), locking the ARIA wiring internally while handing rendering back to the consumer.
2. **The "routing tab" is being killed off** — strict systems (Primer) forcibly split route-changing nav (`UnderlineNav` + `aria-current`) from in-place tabs (`UnderlinePanels`); "if it changes the route, it isn't a tab."
3. **Lazy mounting is now an explicit, documented prop** rather than an implicit default; key-based selection standardised over index.
4. **The sliding indicator is migrating off JavaScript** — `getBoundingClientRect`/`ResizeObserver` giving way to CSS Anchor Positioning + the View Transitions API (verify support before relying on it).

## 14. Sources cited

Conservative dating (the external pass cited Spectrum/React Aria v3.49.0, Carbon v1.76.0/React 19, Primer v37, Polaris 13.0+ 2025/2026, Material 3 Primary/SecondaryTabRow, Fluent 2, Base Web Tabs-Motion, Apple HIG — held loosely; the CSS-Anchor-Positioning/View-Transitions indicator migration and the Polaris Web-Components claim are flagged unverified; `last-audited` is the re-run trigger):

- Adobe Spectrum / React Aria — `Tabs`/`TabList`/`Tab`/`TabPanels`, `useTabList`, key-based selection, `keyboardActivation`, `--tab-panel-*` vars (Spectrum, 2024–2025).
- GitHub Primer — the `UnderlineNav` (routing) vs. `UnderlinePanels` (in-place) split; the routing-isn't-a-tab rule (Primer, 2024–2025).
- IBM Carbon — `Tabs`/`TabList`/`TabPanel`, automatic vs. manual tablists, line/contained/dismissible, vertical wrap-to-two-lines (Carbon, 2025–2026).
- Google Material 3 — primary/secondary tab hierarchy (`PrimaryTabRow`/`SecondaryTabRow`), scrollable tabs, the two-level nesting cap (Material 3, 2024–2025).
- Uber Base Web — the `Tabs` "Tabs-Motion" sliding-indicator upgrade (Base Web, 2025–2026).
- Microsoft Fluent 2 — `TabList`/`Tab` (Fluent, 2024–2026).
- Shopify Polaris — `Tabs` (Polaris, 2025–2026).
- Atlassian Design System — `Tabs`/`TabList` (Atlassian, 2024–2025).
- Radix UI / Headless UI — `Tabs` / `Tab.Group`, `forceMount`/`keepMounted` (2024–2025).
- Apple Human Interface Guidelines — tab views vs. segmented controls (Apple HIG, 2023–2024).
- WAI-ARIA APG — Tabs pattern (manual/automatic activation, roving tabindex, the role/aria wiring).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 4.1.2, 2.1.1, 1.4.11, 2.4.13, 1.4.1, 2.4.3.

## 15. Agent-consumable schema

```yaml
identity:
  id: tabs
  name: Tabs
  aliases: [tab-list, tab-panel, tab-group, tab-bar]
  category: navigation
  status: stable
description: >
  In-page switching among mutually-exclusive PANELS of related content,
  one shown at a time (role=tablist/tab/tabpanel). NOT routing (route
  changes are a nav of links + aria-current, not a tablist), NOT a
  value-in-place switch (segmented-control), NOT a sequence (stepper) or
  stacked multi-open disclosure (accordion). First Navigation brief; does
  NOT inherit the form-field substrate.
anatomy:
  shares-mechanics-with: segmented-control   # roving-tabindex row + sliding active-indicator (not re-derived)
  parts:
    - {name: TabList, role: tablist, note: owns roving tabindex, orientation, overflow}
    - {name: Tab, role: tab, note: trigger; aria-selected + aria-controls; optional icon/badge/close}
    - {name: active-indicator, note: underline or contained pill; slides to the selected tab}
    - {name: overflow-affordance, note: scroll buttons / swipe+fade-mask / 'More' menu}
    - {name: TabPanels, note: optional wrapper for layout/transitions}
    - {name: TabPanel, role: tabpanel, note: aria-labelledby->tab, tabindex=0 (focusable/scrollable)}
  exposure: "compositional/headless (<Tabs><TabList><Tab/></TabList><TabPanel/>) over a config array"
api:
  props:
    - {name: selectedKey/defaultSelectedKey/onSelectionChange, type: string|number, description: "KEY-based not index-based (index mis-maps after a tab-collection mutation)"}
    - {name: activationMode/keyboardActivation, type: enum, values: [automatic, manual], default: automatic, description: "manual when a panel switch is expensive/async (§accessibility)"}
    - {name: orientation, type: enum, values: [horizontal, vertical], default: horizontal}
    - {name: disabledKeys / per-tab isDisabled, type: array/boolean, description: per-permission; handle the disabled-active-tab focus trap}
    - {name: mounting (forceMount/keepMounted), type: control, description: the mount trilemma (§implementation)}
    - {name: per-tab, type: "key, icon, badge, isClosable/onClose", description: closable = the editor-tab variant}
states:
  runtime: [rest, hover, focus-visible, selected, disabled]
  notes:
    focus-vs-selected: "the roving focus ring can sit on a DIFFERENT tab than the selected one (automatic mode aside) — distinct signals"
    panel: "hidden | shown; tabindex=0"
variants:
  style: [line-underline (primary/page-level, default), contained-pill (nested/localized)]
  orientation: [horizontal, vertical]
  overflow: [scroll, swipe-fade-mask, more-menu]
  content: [text, with-icon, with-count-badge]
  closable: [static, closable-addable]
  hierarchy: "line=primary, contained=secondary (Material PrimaryTabRow/SecondaryTabRow); max TWO nesting levels"
accessibility:
  pattern: "WAI-ARIA APG Tabs"
  wcag-criteria: ["4.1.2", "2.1.1", "1.4.11", "2.4.13", "1.4.1", "2.4.3"]
  roles: "tablist > tab (aria-selected true/false on all, aria-controls->panel) ; tabpanel (aria-labelledby->tab, tabindex=0)"
  keyboard-model:
    tab: "enters/exits the whole tablist; then Tab moves into the active panel"
    arrows: "between tabs (Left/Right horizontal, Up/Down vertical); roving tabindex (active=0, rest=-1)"
    home-end: "first/last tab"
    enter-space: "activates the focused tab in MANUAL mode"
  activation:
    practice-default: "automatic (selection-follows-focus)"
    manual-when: "panel switch is expensive — network/async/heavy render (else arrowing fires N expensive loads)"
  routing: "role=tab is NOT for route changes — use <nav> + links + aria-current; deep-linking to a tab via hash/query without a routing event is fine"
  panel-focus: "stays on the tab after activation; panel reachable via Tab"
  announcements: "count badge coherent ('Errors, 4 items'); icon-only tabs need aria-label + tooltip; tablist needs an accessible name"
content:
  label-pattern: "short parallel NOUNS (1-2 words); no verbs; NO multiline for horizontal (overflow instead); vertical may wrap-2-lines+truncate"
  icon: "universally legible or aria-label + tooltip"
  count: ">~6-7 tabs signals reconsidering the IA"
motion:
  active-indicator: "translateX+width slide ~150-200ms (segmented-pill mechanic); measured via getBoundingClientRect + ResizeObserver (resize/font-load/RTL); migrating to CSS Anchor Positioning / View Transitions"
  panel: "quick cross-fade or 4-8px slide-up; React Aria --tab-panel-width/height for dimension changes; avoid horizontal panel slide"
  reduce-motion: "snap the indicator + drop panel transitions"
i18n:
  rtl: "order flows right-to-left, icons swap sides, indicator translateX negates; keyboard remaps (ArrowLeft = logically-next in RTL)"
  expansion: "de/ru +150-200% -> overflow handling load-bearing; horizontal tabs can't wrap, must fall into scroll/menu; vertical sidesteps it"
implementation:
  - "panel mounting trilemma: mount-all (Find-in-Page/SEO/print, heavy) / mount-on-activate (instant load, DESTROYS panel state on switch) / keep-alive (mount-once then hidden, state preserved). PRACTICE: mount-on-activate default, keep-alive opt-in for stateful panels, forceMount opt-in for SEO/print"
  - "disabled-active-tab: shift tabindex=0 to nearest viable sibling or the keyboard user is trapped"
  - "deep-link via URL hash/query bound to selectedKey + History API (NO routing event) — shareable + in-place-swap contract"
  - "indicator = measured/translated element + ResizeObserver, not a pseudo-element; -> CSS Anchor Positioning"
  - "don't hand-roll — React Aria useTabList/useTab/useTabPanel, Radix, Headless UI; controlled-without-onChange trap"
composition:
  composes-with: [tab-list, tab, tab-panel, icon, badge, button, menu]
  alternative-to: [segmented-control, nav-links (routing), accordion, stepper-wizard, carousel]
  supersedes: ["show/hide divs without tablist ARIA", "role=tab misused for routing (-> nav links)"]
  superseded-by: ["accordion on narrow viewports", "a nav landmark when it's really routing"]
  routing-variant: "a distinct TabNav/nav-links component (Primer UnderlineNav model) — NOT Tabs with href"
notes:
  contested:
    - "manual vs automatic activation (automatic default; manual when expensive/async)"
    - "panel mounting trilemma (mount-on-activate default + keep-alive/forceMount opt-ins)"
    - "tabs-vs-routing (route changes are nav links, not a tablist) and tabs-vs-segmented (panels vs value-in-place)"
  shared-mechanics: "roving-tabindex row + sliding indicator with segmented-control"
  unverified:
    - "the CSS-Anchor-Positioning / View-Transitions indicator migration (verify browser support)"
    - "external-supplied 2025/2026 version numbers; Polaris Web-Components"
  evolution: "monolithic -> headless/compositional; routing-tab killed off (UnderlineNav vs UnderlinePanels); lazy-mount explicit; indicator migrating off JS"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-tabs/` (15 June 2026), the first Navigation-category brief. Both passes converged on the spine — tabs swap panels in place (the routing boundary: a route change is a `<nav>` of links + `aria-current`, NOT a tablist, with the field bifurcating via Primer's `UnderlineNav`/`UnderlinePanels` split), the tabs-vs-segmented boundary (distinct panels vs. value-in-place, closing segmented-control's open reference), the APG tablist/tab/tabpanel + roving-tabindex contract, manual-vs-automatic activation (automatic default, manual when switching is expensive/async — the same expensive-side-effect logic as radio §6), key-based over index-based selection, the panel-mounting trilemma (mount-all / mount-on-activate / keep-alive), the line-vs-contained primary/secondary hierarchy, the sliding-indicator mechanics shared with segmented-control, RTL order+indicator+arrow inversion, short-parallel-noun labels with no horizontal multiline, and the five-part `Tabs`/`TabList`/`Tab`/`TabPanels`/`TabPanel` naming with a distinct routing component. External-pass contributions folded in: the sharpened mount-strategy trilemma (Find-in-Page/SEO/print for mount-all; state-destruction for lazy; keep-alive as the compromise), the disabled-active-tab focus-black-hole trap, the deep-linking-via-hash-without-routing technique, the badge-announcement and Material primary/secondary-row detail, the Base Web Tabs-Motion and CSS-Anchor-Positioning/View-Transitions indicator migration, and the React Aria `--tab-panel-*` dimension vars. Claude-pass contributions: the framing as the first Navigation brief that does not inherit the form substrate, the explicit shared-mechanics-with-segmented-control tie, and the mount-on-activate-default resolution. The CSS-Anchor/View-Transitions migration and the 2025/2026 version numbers are flagged unverified. Conformant to `components/_schema.md`. Opens the Navigation category; Accordion and the routing nav/Link are the adjacent briefs to come.*
