---
okf_version: "0.1"
type: component-brief
title: Side Navigation
description: The most composition-heavy brief and the one that closes the Navigation category — primary persistent wayfinding that inherits Link (items + nav landmark + aria-current), Drawer (the mobile form), Accordion/Disclosure (sub-sections), and Tooltip (rail labels). A field-truth study of the persistent-structure-vs-drawer decision and the responsive transform, the collapsed-rail-vs-expanded model, the multi-level Disclosure-not-role=menu sub-nav (and the Disclosure-Navigation-Hybrid + the side-nav-vs-tree boundary), the aria-current active-state contract, the tabbed-not-roving keyboard model, the SSR/FOUC cookie-not-localStorage state persistence, and the width-animation layout-thrashing trap — with the practice's defaults.
tags: [components, navigation]
category: Navigation
status: stable
aliases: [sidebar, side-nav, nav, nav-list, navigation, navigation-rail, navigation-drawer]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Side Navigation

> Side Navigation is an app's **primary persistent wayfinding** — a vertical column of navigation Links, pinned to the inline-start edge, present across route changes — and the most composition-heavy brief in the catalogue: it invents almost nothing, standing on **Link** (the items + the `nav[aria-label]` landmark + `aria-current="page"` contract), **Drawer** (its mobile/collapsed-overlay form), **Accordion/Disclosure** (collapsible sub-sections), and **Tooltip** (the collapsed-rail icon labels). It closes the Navigation category. The defining decision is **persistent structure vs. transient drawer + the responsive transform**: a side nav is a *persistent block in the layout grid* (reserving width, stable across routes) — not an overlay — and on narrow viewports it transforms into a modal Drawer behind a hamburger (the boundary Drawer set up from the other side). Three things are genuinely its own and recur as traps: the **collapsed-rail-vs-expanded** model (and the icon-only label requirement), the **multi-level Disclosure-not-`role=menu`** sub-nav (the nav-is-not-a-menu rule reaching nav in full — Ant's `role=menu`-for-nav is the documented anti-pattern), and the **SSR state-persistence / FOUC** problem (persist the collapse state in a cookie, not localStorage, or the page flashes on load).

---

## 1. Framing

Side Navigation establishes the **primary, persistent spatial contract** of an app — a dedicated column that dictates the layout boundaries for the main content and anchors the user's mental model across route changes. It inherits **Link** (items + nav landmark + active — see link, breadcrumbs), **Drawer** (the mobile form — see drawer), **Accordion/Disclosure** (sub-sections — see accordion), **Tooltip** (rail labels — see tooltip), and **Icon** (item icons).

**The defining decision is persistent-structure vs. transient-drawer + the responsive transform:** a side nav is a **persistent block in the CSS grid/flex shell** — it reserves width (a ~56–80px collapsed *rail* or a ~240–320px expanded *panel*), stays present across routes, and is *not* an overlay. The **Drawer** is its opposite: a transient overlay that escapes flow, traps focus, and is dismissed. On narrow viewports (typically <768px) the side nav **transforms into a modal Drawer behind a hamburger** — the same nav content, two presentations. Material 3 formalised this: the rail and the drawer are **responsive variants of one data structure**, not separate components (and it deprecated the rigid "Permanent Navigation Drawer" for the collapsible "Expanded Navigation Rail").

What it *isn't*: a **Drawer** (transient overlay; the side nav *is* a drawer on mobile — see drawer), a **Menu** (`role=menu` *commands*; this is *navigation links* — the nav-is-not-a-menu rule, see menu), **Tabs** (in-page panel switching, not cross-page routing — see tabs; never nest tabs as nav), **Breadcrumbs** (a secondary location *trail*, not primary nav — see breadcrumbs), or a **Tree** (`role=tree` for hierarchical *data*; site nav is nav+disclosure+links — §6). Why systems disagree: the rail-vs-expanded default, the API model (monolithic vs composable vs overrides), nesting depth, and Ant's `role=menu` overload.

## 2. Anatomy and parts
Macro (the three vertical zones + the rail), inside a `<nav>`/`<aside>` container (`flex-shrink:0`, full height):
- **header** — a sticky top zone (`position:sticky; top:0`): product/branding, a workspace/account switcher.
- **scrollable content** — the central track (`overflow-y:auto; flex-grow:1`) that scrolls *independently* of the window (don't hijack global scroll); holds the nav groups.
- **footer** — a sticky bottom zone: account/settings/docs/auth — persistent utilities.
- **resize rail** — an interactive edge (`cursor: col-resize`) for drag-to-resize / click-to-toggle (shadcn, Atlassian).

Micro (inside the content track):
- **Navigation Group** + an optional **Group Header** (a label, optionally an Accordion disclosure toggle for the section).
- **Navigation Item** — a **Link**: a **leading visual** (icon/avatar — *persists in the rail*), the **label**, a **trailing visual** (badge/count or a disclosure chevron), and the **active indicator** (a left border / background fill / weight — the visual form of `aria-current="page"`).

## 3. Properties / API
The field spans three API models: **monolithic** (a deep `items` JSON object — Polaris; consistent but router-locked and SSR-hostile), **composable slots** (`SidebarGroup`/`SidebarMenu`/`SidebarMenuItem` with `asChild` — shadcn/Primer; the modern default, no router lock-in), and **`overrides`** (a data array + per-node component injection — Base Web; flexible but less SSR-streamable). **The practice default is composable slots with polymorphic `asChild`.**

- **`items` / `children`** — the nav tree (data model `{label, href, icon, items?}` or composed `NavItem`/`NavGroup`); each item inherits Link's `asChild`.
- **`collapsed` / `defaultCollapsed` + `onCollapsedChange`** — the rail toggle; **persist across sessions via a cookie** (§11).
- **active/current** — the component marks the route-matching item `aria-current="page"`.
- **multi-level** — nested `items` + per-group expanded state, rendered as in-place disclosure (expanded) or a flyout Popover (collapsed rail).
- **`renderItem` / `asChild`** — the Link-vs-router slot.
- **mobile breakpoint / `as="drawer"`** — render as a modal Drawer below the breakpoint.
- (Leading edge: a **resizable** width + **drag-to-reorder** items — Atlassian's Pragmatic Drag and Drop.)

## 4. States and variants
- **Item states:** rest / hover / focus-visible / **active** (`aria-current="page"`, the "you are here" indicator — distinct from hover/focus) / disabled.
- **Component states (the three postures — responsive variants of one structure):**
  - **Expanded** (~240–320px) — icon + label + trailing visuals; the main content sits adjacent.
  - **Collapsed rail** (~56–80px) — **icon-only**: labels, badges, and chevrons disappear; nested items **pivot from in-place disclosure to flyout Popovers**; icons **must** carry Tooltips/accessible names (§6).
  - **Modal drawer** (<768px) — escapes the grid, elevated z-index, scrim, focus-trapped, hamburger-toggled (inherits Drawer).
- **Variants:** single-level vs multi-level; with-icons / with-badges; the section group; Material's navigation rail / drawer / bar taxonomy.

## 5. Usage guidance
- **Use Side Navigation** as **primary persistent wayfinding** for a **broad/deep IA** — dashboards, admin/SaaS, consoles, docs. Carbon's threshold: side nav is warranted past **~5 top-level items** (top nav exhausts horizontal space and forces overflow/truncation; side nav scales vertically). It gracefully supports a **shallow hierarchy** (a top-level category → one sub-level → item).
- **Don't use it for:** a **shallow/marketing site** (→ top nav / header bar), **in-page panel switching** (→ Tabs — never nest tabs as nav), a **location trail** (→ Breadcrumbs — secondary), a **transient panel** (→ Drawer — though the mobile side nav *is* a drawer), or **hierarchical data** (→ Tree — `role=tree`).
- **Decision frameworks:**
  - **Never mix top + side *primary* nav** — pick one routing backbone; if side nav is primary, the top bar is **global utilities only** (search, notifications, account, workspace switcher). Splitting routing across both fragments the mental model.
  - **Side nav vs. Tabs:** cross-page routing that changes the URL/context (side nav — links + `aria-current`) vs. in-page sibling-panel visibility (Tabs — `tablist`). The routing-is-not-a-tablist rule (see tabs).
  - **Rail vs. expanded:** expanded when labels aid scanning / there's room; collapse to a rail to reclaim space (rail icons **must** carry tooltips/labels). Persist the choice.
  - **Nesting depth is contested and should stay shallow** — Carbon caps at a **single** sub-level for clarity; ~three levels (category → sub-menu → item) is the practical ceiling; deeper is an IA smell (flatten, or use a sub-page).

## 6. Accessibility
- **The nav landmark + unique label:** `<nav aria-label="Primary">` — a *unique* name (a page has multiple navs: header, footer, breadcrumb) so a screen-reader landmark list distinguishes it. Items are a `<ul>`/`<li>` list of Links (the list conveys "item N of M").
- **`aria-current="page"`** on the active item (inherited Link — a visual `.active` class alone is insufficient). Multi-level: the active child is `aria-current="page"` and its ancestor group is expanded/indicated (the ancestor is not itself `aria-current`).
- **The Disclosure pattern for sub-sections, NOT `role=menu`** (the most catastrophic, most common error): `role=menu`/`menuitem` is for *desktop-app command menus* — it makes AT expect Tab to *exit* and arrow-keys to navigate (roving tabindex/`aria-activedescendant`), breaking the Tab-through-links expectation. **Ant Design defaults its vertical nav to `role=menu` — the documented anti-pattern.** The correct pattern: a `button[aria-expanded]` + `aria-controls` revealing a nested `<ul>` of Links (the Accordion mechanics).
- **The Disclosure Navigation Hybrid** — when a parent is *both* a routable landing page *and* an expand toggle, don't overload one element: render the **Link** (Enter navigates) + an **adjacent chevron `<button>`** (`aria-expanded`; Space/Enter expands the sub-menu). One element can't unambiguously be both.
- **The keyboard model is TABBED, not roving** — a side nav is a *list of links*; Tab moves through them in order. It is **not** a roving-tabindex widget (not a menu/menubar/tree). The collapse toggle and group headers are `button`s.
- **The collapsed-rail label requirement** — an icon-only rail item still needs an **accessible name** (visually-hidden label / `aria-label`) *and* a visible **Tooltip** on hover/focus (inherited Tooltip; the text labels left the DOM, so the icon alone is not a name).
- **The skip link** — a visually-hidden "Skip to content" Link placed in the DOM **immediately before** the `<nav>`, revealed on focus, so keyboard users bypass a long nav (a `<nav>` of dozens of links is a real traversal barrier).
- **`role=tree` only for a true data tree** — a file explorer / deep taxonomy is `role=tree` (arrow-key traversal); *site nav* is nav+disclosure+links. Don't reach for treeview for a nav.
- **WCAG SCs:** 4.1.2 (name/role/value — the landmark + `aria-current` + the toggle), 1.3.1 (list/landmark structure), 2.4.1 (bypass blocks — the skip link), 2.4.5 (multiple ways), 2.4.8 (location — the active state), 2.5.5/2.5.8 (44×44 touch targets, esp. the mobile drawer — Apple HIG 44pt), plus Link's SCs (2.4.4) and the rail Tooltip's 1.4.13.

## 7. Content guidelines
- **Ruthlessly concise labels** — one to three words, noun-led, matching the destination's page title; front-load the distinguishing word. Long labels destroy vertical rhythm (wrapping) or hide context (truncation); Material advises **wrap to max two lines, then rewrite** — don't dynamically shrink/truncate.
- **Sentence casing**, not title case — title case's jagged tracking slows scanning of dense lists.
- **Icon discipline** — icons aid recognition but **must pair with a label** (or a rail tooltip); keep icon usage consistent across a hierarchy level (mixing icon-led and text-only items breaks the alignment axis). Never icon-only without a name.
- **Trailing badges/counts** are subordinate, far-edge, concise ("3", "99+", "New") with an accessible name ("3 unread"); **hidden in the rail** (they'd collide with the icon).

## 8. Motion and transition
- **The collapse/expand transition is the most performance-sensitive motion in the layout.** Animating the container `width` forces a reflow every frame and **violently resizes the adjacent main content (layout thrashing)**. Mitigations: wrap labels in `white-space:nowrap; overflow:hidden` so they don't reflow as the column shrinks, **fade the label opacity out *before* the width reduces**, keep icons fixed, and drive the width via a CSS variable (`--sidebar-width`) ~150–200ms. **The mobile drawer must NOT animate `width`/`left`** — sit it off-canvas and animate **`transform: translateX(-100% → 0)`** (GPU compositor, 60fps, no reflow — inherits Drawer's slide).
- **Sub-item reveal** — in-place disclosure animates region height (inherits Accordion's `::details-content`/`calc-size` — see accordion); the collapsed-rail **flyout** is an origin-aware Popover (see popover).
- Under `prefers-reduced-motion: reduce`, snap the width/height and drop the slide. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** is a full structural inversion: the panel shifts to the **inline-end** edge (logical `inset-inline-start` mirrors), item anatomy reverses (icon trailing, badge/chevron leading), and the disclosure/collapse **chevrons mirror**; the mobile drawer slides from the mirrored edge. Use **CSS logical properties** (`margin-inline-start`, `inset-inline-*`) so it flips off `dir="rtl"` with no JS. Don't hardcode `left`/`margin-left`.
- **Text expansion** — labels expand +30–50% (de/ru); accommodate via a **user-resizable width** (the resize rail — Atlassian) or graceful two-line wrap, not truncation. (See 13-internationalization-and-rtl.)

## 10. Naming
The field is fragmented: **`Sidebar`** (Apple HIG, shadcn — but "sidebar" semantically connotes an auxiliary `<aside>` content panel, not the routing backbone), **`UI Shell` "Left Panel"** (Carbon — the layout-wrapper framing), **`Navigation Drawer` / `Navigation Rail`** (Material — naming by shape/state), **`NavList`** (Primer — the list primitive, detached from the layout container), **`Nav`** (Fluent), **`Menu`** (Ant — the overload). **The practice default: `Side Navigation`** — the most precise name (it describes position + purpose without binding to a width like "Rail" or a state like "Drawer") — composing **`NavItem`** (a Link) / **`NavGroup`** (a Disclosure of items) / the collapse toggle, with the mobile form delegated to **`Drawer`** and rail labels to **`Tooltip`**. Aliases to map: `Sidebar`, `SideNav`, `Nav`, `NavList`, `Navigation`, `NavigationRail`, `NavigationDrawer`.

## 11. Implementation notes
- **The persistent layout shell** — the side nav is a **column in the app's grid/flex shell** (`grid-template-columns: var(--sidebar-width) 1fr`), not a `position:fixed` overlay; collapsing animates the column width + reflows content.
- **State persistence + the SSR/FOUC trap (the headline implementation point):** the collapse state must persist across routes *and* sessions, so component-local state is insufficient (it resets on refresh). **`localStorage` is wrong for SSR** — the server can't read it, renders the *expanded* default, then the client hydrates, reads localStorage, and **snaps to collapsed — a jarring FOUC + layout shift.** The fix (shadcn): **store the preference in an HTTP cookie** (sent on every request → the server renders the correct width in the initial HTML, zero shift). Where cookies are barred (caching/privacy), inject a **blocking synchronous `<head>` script** that reads localStorage and sets `--sidebar-width` on `:root` *before* first paint.
- **The mobile-drawer transform** — below the breakpoint, render the *same nav content* as a modal **Drawer** behind a hamburger (inherits Drawer — focus-trap, scrim, the `translateX` slide; see drawer). Share the item model between the persistent and drawer renders.
- **The collapsed rail + flyout** — collapsed shows icons + tooltips; in-place disclosure sub-items become **flyout Popovers** anchored to the rail item (inherited Popover positioning + the no-native-detent/anchor caveats).
- **Sub-nav is Disclosure, not `role=menu`** — `button[aria-expanded]` + a region of Links (reuse Accordion's `<details>`/`::details-content` where it fits — see accordion); the Disclosure-Navigation-Hybrid for link-+-toggle parents (§6).
- **`aria-current` + router integration** — derive the active item from the current route, set `aria-current="page"`; each item renders the framework router's Link via **`asChild`** while emitting a real `<a href>` (SEO + middle-click; avoids the "history needs a DOM" errors of monolithic APIs — inherited Link).
- **Don't hand-roll** — shadcn `Sidebar` (Provider + CSS vars + `collapsible="icon"` + cookie SSR), Primer `NavList`, Carbon `SideNav`, or compose Link + Accordion + Drawer + Tooltip; skin them.

## 12. Related and alternative components
- **Stands on:** Link (items + the `nav[aria-label]` landmark + `aria-current` + `asChild` router — see link, breadcrumbs), Drawer (the mobile/collapsed-overlay form — see drawer), Accordion/Disclosure (collapsible sub-sections — see accordion), Tooltip (collapsed-rail icon labels — see tooltip), Icon (item icons — see icon), Popover (the rail flyout — see popover).
- **Alternative to / boundary with:** the **top nav / app header** (shallow/marketing or global-utilities-only vs deep-IA persistent side nav — not yet briefed), **Tabs** (in-page panel switching, not cross-page nav — see tabs), **Breadcrumbs** (a secondary location trail — see breadcrumbs), **Drawer** (transient overlay; the side nav *is* a drawer on mobile — see drawer), **Menu** (`role=menu` commands, not nav links — see menu; the nav-is-not-a-menu boundary), **Tree** (`role=tree` for hierarchical data, not site nav).

(The most composition-heavy brief and the one that closes the Navigation category — it invents almost nothing, standing on Link (items + nav contract + active), Drawer (mobile form), Accordion (sub-sections), and Tooltip (rail labels), and contributing the persistence + responsive transform, the rail-vs-expanded model, the multi-level Disclosure-not-`role=menu` sub-nav, and the SSR/FOUC cookie persistence. With Tabs, Accordion, Breadcrumbs, Link, Pagination, and Side Navigation, the Navigation category is complete. See link/breadcrumbs for the nav contract, drawer for the mobile form, accordion for the sub-sections, tooltip for the rail labels, menu for the nav-is-not-a-menu rule, tabs for the routing-is-not-a-tablist rule. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The fall of the Permanent Navigation Drawer** — Material 2's rigid always-expanded ~300px desktop drawer was deprecated in Material 3 for the **Expanded Navigation Rail**, cementing that all modern side navs must collapse to a space-saving rail.
2. **The nav-is-not-a-menu correction reached side nav** — the W3C APG campaign settled multi-level nav on the Disclosure pattern (Tab-through links, no roving), and `role=menu`-for-nav (Ant) is the flagged anti-pattern.
3. **Monolithic → composable** — config-driven `items` JSON (Polaris, router-locked, SSR-hostile) gave way to slot composition with `asChild` (shadcn/Primer — no router lock-in, SSR-streamable), with Base Web's `overrides` as a middle path.
4. **The SSR/FOUC cookie solution converged** — storing collapse state in a cookie (not localStorage) to render the correct width server-side, eliminating the hydration flash.
5. **The responsive side-nav ↔ drawer transform** and **`aria-current="page"`** standardised; the leading edge added **user-resizable width + drag-to-reorder** (Atlassian).

## 14. Sources cited
(Conservative; reconcile with external.) **Google Material 3** — navigation rail / drawer / bar; the Permanent-Drawer→Expanded-Rail deprecation (2024–2026); **IBM Carbon** — UI Shell `SideNav` ("Left Panel", the >5-items threshold, single-sub-level cap) (2024–2026); **GitHub Primer** — `NavList` (SSR slots + `aria-current`, the deep-nesting refactor) (2024–2026); **Shopify Polaris** — `Navigation` (the monolithic-API legacy friction) (2024–2026); **Atlassian** — side navigation (resizable 56→320px, Pragmatic Drag and Drop reorder) (2024–2026); **Microsoft Fluent** — `Nav` (2024–2026); **Ant Design** — `Menu` inline/vertical (the `role=menu`-for-nav anti-pattern — flagged) (2024–2026); **Base Web (Uber)** — Side Navigation (the `overrides` API) (2024); **shadcn/ui** — `Sidebar` (`SidebarProvider`, CSS-var layout, `collapsible="icon"`, cookie SSR persistence — the de facto reference) (2024–2026); **WAI-ARIA APG** — no formal side-nav pattern (nav landmark + list of Links + Disclosure; treeview only for a data tree); **Apple HIG** — sidebars / 44×44pt touch targets (2024–2026). WCAG 2.2 (Oct 2023) — 4.1.2, 1.3.1, 2.4.1, 2.4.5, 2.4.8, 2.5.5/2.5.8, 2.4.4, 1.4.13.

## 15. Agent-consumable schema

```yaml
identity:
  id: side-navigation
  name: Side Navigation
  aliases: [sidebar, side-nav, nav, nav-list, navigation, navigation-rail, navigation-drawer]
  category: navigation
  status: stable
description: >
  Primary PERSISTENT wayfinding — a vertical column of nav Links in the app
  shell (a grid/flex column reserving width, present across routes), the
  current item aria-current=page; transforms into a modal Drawer on mobile.
  The most composition-heavy brief. NOT a transient Drawer (it's the
  persistent structure), NOT a Menu (role=menu commands; nav-is-not-a-menu),
  NOT Tabs (in-page), NOT Breadcrumbs (secondary trail), NOT a Tree
  (role=tree for data).
anatomy:
  macro: "<nav>/<aside> (flex-shrink:0, full height) > header (sticky top: branding/switcher) + scrollable content (overflow-y:auto, independent scroll) + footer (sticky bottom: account/settings) + resize rail (drag-resize/click-toggle)"
  micro: "Navigation Group (+ optional Group Header / Accordion toggle) > Navigation Item = Link [leading visual (icon, persists in rail) + label + trailing visual (badge/chevron) + active indicator (= aria-current=page)]"
api:
  inherits: [link (items + nav landmark + aria-current + asChild router), drawer (mobile form), accordion (sub-sections), tooltip (rail labels), icon, popover (rail flyout)]
  models: "monolithic items-JSON (Polaris; router-locked, SSR-hostile) | composable slots + asChild (shadcn/Primer; PRACTICE DEFAULT) | overrides (Base Web)"
  props:
    - {name: items/children, type: "data model | NavItem/NavGroup", description: nav tree; each item inherits Link asChild}
    - {name: collapsed/defaultCollapsed, type: boolean}
    - {name: onCollapsedChange, type: function, description: "PERSIST via cookie (not localStorage) — §implementation"}
    - {name: active/current, type: route-derived, description: marks matching item aria-current=page}
    - {name: multi-level, type: "nested items + per-group expanded", description: in-place disclosure (expanded) / flyout Popover (rail)}
    - {name: renderItem/asChild, type: slot, description: Link-vs-router}
    - {name: mobile-breakpoint / as=drawer, type: "breakpoint", description: render as modal Drawer below it}
    - {name: resizable / reorderable, type: boolean, description: "leading edge — drag-resize width / drag-to-reorder (Atlassian)"}
states:
  item: [rest, hover, focus-visible, "active (aria-current=page, you-are-here indicator)", disabled]
  postures: "expanded (~240-320px, icon+label) | collapsed rail (~56-80px, ICON-ONLY + tooltip + flyout subitems) | modal drawer (<768px, escapes grid, scrim, focus-trap, hamburger) — responsive variants of ONE structure"
variants:
  axes: [single-level, multi-level, with-icons, with-badges, section-group, "Material rail/drawer/bar"]
accessibility:
  wcag-criteria: ["4.1.2", "1.3.1", "2.4.1", "2.4.5", "2.4.8", "2.5.5", "2.5.8", "2.4.4", "1.4.13"]
  landmark: "nav[aria-label] UNIQUE (page has header/footer/breadcrumb navs); ul/li list of Links ('item N of M')"
  active: "aria-current=page on active item (visual class alone insufficient); multi-level: active child current + ancestor expanded (ancestor not itself current)"
  disclosure-not-menu: "sub-sections = button[aria-expanded]+aria-controls + nested ul of Links (Accordion mechanics) — NOT role=menu (makes AT expect Tab-exits + arrow-nav; breaks Tab-through-links). Ant role=menu-for-nav = THE anti-pattern"
  hybrid: "link-AND-disclosure parent: render Link (Enter navigates) + adjacent chevron button (aria-expanded; Space/Enter expands) — one element can't be both"
  keyboard: "TABBED through links, NOT roving (not a menu/menubar/tree); toggle + group headers are buttons"
  rail-label: "icon-only rail item needs accessible name (visually-hidden/aria-label) + visible Tooltip (icon != name)"
  skip-link: "visually-hidden 'Skip to content' immediately before <nav>, revealed on focus (a long nav is a traversal barrier)"
  tree: "role=tree ONLY for a true data tree (file explorer); site nav is nav+disclosure+links"
content:
  labels: "1-3 words, noun-led, match page title; Material: wrap to max 2 lines then REWRITE (don't shrink/truncate)"
  casing: "sentence case (title case slows dense-list scanning)"
  icons: "must pair with a label/tooltip; consistent per hierarchy level; never icon-only without a name"
  badges: "subordinate, far-edge, concise + accessible name ('3 unread'); HIDDEN in the rail"
motion:
  collapse: "THE perf-sensitive motion — animating container WIDTH forces reflow + thrashes adjacent content; mitigate: white-space:nowrap labels, fade label opacity BEFORE width reduces, fixed icons, --sidebar-width var ~150-200ms"
  drawer: "NEVER animate width/left — off-canvas + transform: translateX(-100%->0) (GPU, 60fps, no reflow; inherits Drawer)"
  subitem: "in-place disclosure region height (inherits Accordion) / collapsed-rail flyout Popover (origin-aware)"
  reduce-motion: "snap width/height, drop slide"
i18n:
  rtl: "full inversion — panel to inline-end edge (logical inset-inline-start mirrors), item anatomy reverses (icon trailing, badge/chevron leading), chevrons mirror, drawer slides mirrored; CSS logical properties, no hardcoded left"
  expansion: "labels +30-50% — user-resizable width (resize rail) or 2-line wrap, not truncation"
implementation:
  - "PERSISTENT layout shell — a grid/flex column (grid-template-columns: var(--sidebar-width) 1fr) NOT position:fixed; collapse animates column width + reflows"
  - "STATE PERSISTENCE + SSR/FOUC TRAP: collapse state must survive route + session; localStorage is WRONG for SSR (server renders expanded default -> client hydrates -> snaps to collapsed = FOUC + layout shift); FIX = HTTP COOKIE (sent every request, server renders correct width), or a blocking <head> script setting --sidebar-width before first paint"
  - "mobile-drawer transform — same nav content as a modal Drawer behind a hamburger (shared item model; inherits Drawer focus-trap/scrim/translateX)"
  - "collapsed rail + flyout — icons+tooltips; in-place disclosure sub-items become flyout Popovers"
  - "sub-nav = Disclosure not role=menu (reuse Accordion <details>/::details-content); Disclosure-Navigation-Hybrid for link+toggle parents"
  - "aria-current + router asChild (real <a href> — SEO/middle-click; avoids monolithic-API 'history needs a DOM' errors)"
  - "don't hand-roll — shadcn Sidebar (Provider + CSS vars + collapsible=icon + cookie SSR) / Primer NavList / Carbon SideNav, or compose Link+Accordion+Drawer+Tooltip"
composition:
  stands-on: [link (items + nav contract + active + asChild), drawer (mobile form), accordion/disclosure (sub-sections), tooltip (rail labels), icon, popover (rail flyout)]
  alternative-to: [top-nav/app-header (shallow/marketing or global-utilities-only), tabs (in-page, not nav), breadcrumbs (secondary trail), drawer (transient; side nav IS a drawer on mobile), menu (role=menu commands; nav-is-not-a-menu), tree (role=tree data)]
  role-in-family: "the most composition-heavy brief — closes the Navigation category, inventing almost nothing"
notes:
  contested:
    - "rail-vs-expanded default"
    - "API model (monolithic vs composable-slots [practice default] vs overrides)"
    - "nesting depth (Carbon: 1 sub-level; ~3 levels practical ceiling; deeper is an IA smell)"
    - "Ant's role=menu-for-nav overload (anti-pattern)"
    - "side-nav vs top-nav for a given IA (never mix as primary)"
  trap:
    - "role=menu for site nav (nav-is-not-a-menu; breaks Tab-through)"
    - "roving tabindex on a list of links (it's tabbed)"
    - "localStorage collapse state in SSR -> FOUC/layout shift (use a cookie)"
    - "animating container width -> layout thrashing (transform for the drawer; fade labels for the rail)"
    - "icon-only rail without a name/tooltip; mixing icon-led + text-only items"
    - "role=tree for site nav (only for data trees); position:fixed instead of a layout column; hardcoded left (breaks RTL)"
    - "overloading one element as link AND disclosure (use the hybrid)"
  inherited: "Link items + nav landmark + aria-current + asChild; Drawer mobile form; Accordion sub-sections; Tooltip rail labels; Icon; Popover rail flyout"
  evolution: "Permanent Navigation Drawer deprecated -> Expanded Navigation Rail (Material 3); nav-is-not-a-menu reached side nav; monolithic -> composable slots (+ Base Web overrides); SSR/FOUC cookie solution; responsive side-nav<->drawer + aria-current standardised; resizable + drag-reorder (leading edge)"
  unverified:
    - "external-supplied 2026 version numbers"
    - "the inherited platform-state (accordion <details>/calc-size, drawer/popover anchor-positioning) — verify, shared across the family"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-side-navigation/` (16 June 2026), the most composition-heavy brief and the one that closes the Navigation category — primary persistent wayfinding standing on Link (items + the `nav[aria-label]` landmark + `aria-current`), Drawer (the mobile/collapsed-overlay form), Accordion/Disclosure (collapsible sub-sections), and Tooltip (the collapsed-rail icon labels). The two passes converged almost completely — the persistent-structure-vs-drawer decision and the responsive transform (a layout column on desktop → a modal drawer behind a hamburger on mobile; Material's rail/drawer as responsive variants of one structure, with the Permanent Drawer deprecated for the Expanded Rail), the collapsed-rail-vs-expanded model and the icon-only label requirement (rail items need an accessible name + a Tooltip; sub-items pivot to flyout Popovers), the multi-level Disclosure-not-`role=menu` sub-nav (the nav-is-not-a-menu correction reaching nav, Ant's `role=menu` overload the flagged anti-pattern) and the side-nav-vs-Tree boundary, the `aria-current="page"` active-state contract, the tabbed-not-roving keyboard model, the unique-labelled nav landmark + the skip link, and `Side Navigation` as the most precise name over Sidebar/Rail/Drawer. External-pass contributions folded in: the **SSR/FOUC state-persistence problem and the cookie-not-localStorage fix** (shadcn — render the correct width server-side; a blocking `<head>` script as the cookie-barred fallback), the **Disclosure Navigation Hybrid** (a link + an adjacent chevron-button for link-and-toggle parents), the **width-animation layout-thrashing trap** (transform-translateX for the drawer; fade labels before width for the rail), the three API models (monolithic / composable-slots / Base Web's `overrides`), the concrete widths (rail 56–80px / expanded 240–320px) and Carbon's >5-items threshold and single-sub-level cap, the never-mix-top-and-side rule, the resize rail + Pragmatic-Drag-and-Drop reorder, and the 44×44pt touch targets. Claude-pass contributions: the framing as the most composition-heavy, category-closing brief that invents almost nothing, the responsive-variants-of-one-structure framing, and the substrate map. The 2026 version numbers and the inherited platform-state (accordion `<details>`/`calc-size`, drawer/popover anchor-positioning) are flagged unverified. Conformant to `components/_schema.md`. With Tabs, Accordion, Breadcrumbs, Link, Pagination, and Side Navigation, the Navigation category is complete.*
