---
okf_version: "0.1"
type: pattern-brief
title: App shell
description: The persistent application frame every screen sits inside — the global header and its three zones, the primary navigation (top vs side vs hybrid), the content region, the responsive collapse across breakpoints, the landmark/skip-link skeleton, and the SPA route-change focus contract. The first layout-and-shell brief, so layout carries the weight and flow is light. Composes Side Navigation + Menu + Link + Avatar + the search slot; borders the Side Navigation component, the page templates that sit inside it, the Search orchestration pattern, Breadcrumb/Tabs, and the IA strategy.
tags: [patterns, app-shell, navigation, layout, accessibility, navigate]
tier: layout-and-shell
goal: navigate
status: stable
aliases: [App shell, application frame, global header, UI shell, page frame, navigation chrome, masthead]
last-audited: 2026-06-18
timestamp: 2026-06-18
---

# App shell

> Every screen in an application sits inside the same frame: a header across the top, a primary navigation down the side or along that header, a content region, and — underneath the visuals — a landmark skeleton and a skip link that decide whether the whole thing is navigable by keyboard and screen reader. The shell is the one surface a user never leaves; it isolates global persistence from local volatility. It is the substrate, not the page. This brief owns the frame — where navigation lives, what the header carries, how it collapses on a phone, and the single most-missed thing in single-page apps: what happens to focus when the content swaps. It defers the nav *control* to the Side Navigation component and the *pages* to the template briefs that sit inside it.

---

## Problem & context

The app shell is the most-seen, least-noticed surface in a product — present on every screen, so its mistakes compound on every screen. The recurring problem is a universal container that accommodates shallow marketing pages, deep master-detail views, and data-dense dashboards without forcing users to re-learn the navigation model at every juncture. The shell codifies the boundary between what **persists** across route changes and what is **ephemeral**.

Systems diverge from a single tension: maximising content real estate versus maximising navigation discoverability — enterprise tools expose dense omnipresent sidebars; consumer tools shed permanent nav for expansive content and off-canvas drawers. But the deeper reason the shell is hard now is architectural: the move from multi-page apps to SPAs/PWAs **broke native browser orientation**. A full reload used to reset scroll, update the document title, and alert screen readers to a context change for free. In an SPA the content swaps dynamically inside a persistent shell, so those native accessibility and history mechanics go inert unless the shell **actively reconstructs** them. The shell is therefore tasked not just with visual layout but with rebuilding the orientation contracts the browser used to handle.

The pattern applies to any **application** with persistent navigation across multiple destinations — a SaaS product, an admin console, a dashboard suite. It does **not** apply to a marketing site or a single document (lighter header, no persistent app nav), and it stops at the content region's edge: what fills the content area is a **page template** (master-detail, dashboard, settings), each its own brief. The right frame depends on IA shape and platform; the decisions below resolve by IA depth and platform rather than fashion.

## Composition

This brief defines a structural archetype, not a composition recipe. The shell assembles briefed components into fixed regions and dictates *where* they reside, *how* they scale, and *when* they hide/reveal — never their internal anatomy.

- **Side Navigation** (see side-navigation) — the primary nav control when nav is vertical; its items, sections, rail behaviour, and `aria-current` are the component's. The shell decides *whether* nav is a side nav and *where it sits in the frame*.
- **Menu** (see menu) — the account/avatar menu, the overflow, the workspace/product switcher dropdowns.
- **Link / Button** (see link, see button) — the logo/home anchor (route-to-home), header actions, the skip link, the global create/“+”.
- **Avatar** (see avatar) — the account entry point in the header.
- **The search slot** — a Search field that invokes the Search orchestration pattern (see patterns/search-orchestration); the shell owns the slot, not the search experience.
- **Badge** (see badge) — the notification/count indicator on the header bell.

**The delta this pattern adds** is the frame itself: the region model, the header's zone model, the responsive transformation, the landmark/skip-link skeleton, and the SPA route-change contract. Re-deriving the Side Navigation's internals inside the shell is a critical anti-pattern — the shell owns the *slot*, the component owns the *control*.

## Decision rules

The structural forks. Machine-resolvable where a real threshold exists; prose where genuinely contextual.

**1. Top nav vs side nav vs hybrid** — the central frame fork.
- `IF the IA is broad and shallow (≲ ~5–7 top-level destinations, site/editorial, content-immersive)` → **horizontal top nav** in the header.
- `IF the IA is deep or wide (complex SaaS/enterprise, nested sections, user-configurable views, room to grow)` → **side nav** (vertical scales to more items and nesting; the field treats it as the app default — widescreen made vertical scroll effectively infinite while horizontal space stays constrained).
- `IF a multi-product suite or a deep app that also needs global search/actions/account` → **hybrid**: a global top header (logo, search, global actions, account, product switcher) **plus** a side nav for in-product destinations. The dominant enterprise shell (Atlassian, Carbon).

**2. The global header anatomy & zones** — a strict three-zone bar, kept rigid so muscle memory survives across apps.
- **Leading:** logo/home, the nav trigger (when collapsed), optionally a product/workspace switcher. (On macOS PWAs/Electron, this zone must also clear the native window controls — Spectrum.)
- **Center:** global **search** (the slot invoking the Search pattern); if there's no top nav, let the search field expand into the negative space for a larger target.
- **Trailing:** global **create/“+”**, **notifications** (bell + Badge), **help**, environment indicator, and the **account/avatar** menu — account last.
- `IF an environment is non-production or impersonated` → a persistent **environment banner** ("Staging," "Viewing as…").
- Header is **sticky** and shallow (one row).

**3. Side-nav states.**
- **Expanded** (icon + label) by default on wide viewports; **collapsed icon rail** (label on hover/flyout) for density or on toggle; **rail + flyout** for nested items.
- `IF nested/multi-level items` → an expandable tree or rail-with-flyout, not a deep always-open accordion that shoves content down.
- The collapse **toggle persists** the user's choice; the active item carries `aria-current="page"`; group with sections + labels. Persistent (pushes content) on desktop; **overlay** on mobile.

**4. Responsive collapse** — the shedding sequence (breakpoints are conventional, not normative).
- `IF wide` → side nav **persistent and expanded**.
- `IF tablet (≈ < 1024px)` → side nav **collapses to an icon rail** or a toggle; the header gains a hamburger in the leading zone.
- `IF mobile (≈ < 768px)` → the header sheds hard (logo → icon mark; search → a magnifying-glass icon opening a full-screen search modal; trailing utilities → an overflow, keeping avatar + notifications), and nav becomes a **hamburger drawer** (overlay + scrim) OR — `IF ≤ ~5 flat peer destinations` — a **bottom navigation bar** (thumb-zone ergonomics beat a multi-layer hamburger).
- `IF top nav overflows before the breakpoint` → the **Priority+** pattern: show as many items as fit, tuck the rest into a "More" dropdown.

**5. Landmark & skip-link structure** — the a11y the shell owns (detail in §7).

**6. The SPA route-change contract** — the single most-missed a11y issue (detail in §7).

**7. Scroll & persistence model.**
- Header **sticky**; side nav **fixed** (own scroll if long); the **content region is the scroll container**. Letting the global header scroll away is for immersive marketing pages only — an anti-pattern in functional apps.
- **Two grid models** (Carbon delineates): the **editorial model** centers content at a max-width (~1440px) for readable line length, growing margins on ultra-wide; the **high-density product model** uses full browser width, pinning the side nav left and expanding the grid for tables/dashboards. Choose by content type.

**8. Multi-product / workspace.**
- `IF multiple products` → a **product switcher** (waffle/grid) at the far edge of the top header (far-left or far-right), separated from local routing.
- `IF multiple orgs/workspaces` → a **workspace switcher** near the logo or at the side-nav top, distinct from the account menu (switching context ≠ managing your account).

## Layout & structure

The heavy section for this tier. The frame is a small set of regions inside a container that locks to the viewport (100vw/100vh):

- **Header (`banner`)** — full-width, sticky, shallow (~48–64px, one row). Three zones: leading (logo / switcher / nav trigger), center (search), trailing (create / notifications / help / environment / account). Sheds to essentials on mobile.
- **Primary navigation (`navigation`)** — side (vertical, scales deep) or top (horizontal, shallow). Side nav: fixed, own scroll, expanded/rail/drawer by breakpoint.
- **Main (`main`)** — the content region and scroll container; holds exactly one page template; editorial max-width-and-centered by default, full-bleed for the high-density product model.
- **Complementary (`complementary`)** — optional contextual/right panel (details, help, activity); not the primary nav.
- **Footer (`contentinfo`)** — minimal in apps (legal/version), fuller on sites.

**The header/side-nav overlap is a genuine field divergence.** IBM Carbon's UI Shell spans the header full width and places the nav panels strictly *below* it — header supremacy, a single brand umbrella capping the app. Material 3's expressive update often lets the navigation rail occupy the full leading-edge height with the top app bar adjacent *within* the content pane — ergonomic nav access over brand dominance. **The defensible default for multi-product ecosystems is the full-width global header** (it physically caps the application and gives the clearest structural boundary); the full-height rail is defensible for single-product, nav-first tools.

**The responsive model:** wide → header + persistent expanded side nav + (editorial) centered content; tablet → collapsed rail; mobile → essentials header + hamburger drawer *or* bottom nav + full-width content. One `main`, one `h1`, landmarks intact at every breakpoint. The sticky header must not eat the mobile viewport — keep it one shallow row, or scroll-link it to hide on scroll-down and reveal on scroll-up.

## Accessibility orchestration

The a11y the *frame* owns (the nav control's own ARIA is inherited from Side Navigation). This is the shell's signature responsibility.
- **Landmarks** — `banner` / `navigation` / `main` / optional `complementary` / `contentinfo`; exactly one `main`. **Label every `navigation`** when there's more than one (`aria-label="Primary"` / `"Product"` / `"Breadcrumb"`) — the W3C APG mandates it, or landmark-rotor tools become useless ("landmark soup").
- **The skip-link contract (WCAG 2.4.1)** — a "Skip to main content" link as the **first focusable element** in the DOM, visually hidden until focused; its `href` targets the `main` container's `id`, and **that target must carry `tabindex="-1"`** — without it, browsers may fail to move programmatic focus and the next Tab jumps back to the top, nullifying the skip link entirely.
- **`aria-current="page"`** on the active nav item; a single correct heading hierarchy (one `h1` per view, in `main`).
- **The SPA route-change contract** — the most destructive failure when missed. On client-side navigation the shell must: (1) update `document.title` on route resolution; (2) **move focus** into the new view — the prevailing standard is the incoming `<h1>` (given `tabindex="-1"`, focused via `.focus()`), or the `main` container if there's no unique heading; (3) **manage scroll manually** — set `history.scrollRestoration = 'manual'`, reset main scroll to top on forward navigation, restore from the router cache on back. Without this, screen-reader users never learn the view changed and focus is orphaned on unmounted nodes.
- **The mobile drawer** — a focus trap while open (keyboard can't reach the obscured background), Esc to close, focus returns to the trigger; the scrim is inert to AT.
- Keyboard order matches visual order through the frame.

## Flow & states

Light, by tier — the shell is mostly persistent. Its only stateful bits: the **side-nav expand/collapse** (toggle, persisted; animate width smoothly so the adjacent content doesn't jar-reflow), the **mobile drawer open/close** (slide-in over a scrim, focus trap, Esc, focus return), and the **route transition** (focus + scroll + announcement, per §7). No journey, no submission lifecycle — that's what makes this a `layout-and-shell` brief, not a `composition` one.

## Content & copy

- **Nav labels** short, noun-led, consistent with the destinations' page titles; no jargon.
- **Skip-link text** explicit and conventional ("Skip to main content") — not verbose ("Click here to skip navigation").
- **Nav `aria-label`s** avoid redundancy — "Primary," not "Primary navigation" (the role already announces "navigation").
- **Account/switcher labels** name what they switch ("Switch workspace"); the account menu is the person's name/email.
- **Environment banner** unambiguous ("Staging," "Sandbox," "Viewing as [user] — exit").
- **Icon-only header buttons** (hamburger "Open main menu," notifications, help) carry accessible labels.

## Variants & responsive

- **Top-nav shell** (marketing/e-commerce/portals; Priority+ overflow) vs **side-nav shell** (complex apps/dashboards; deep nesting, F-pattern scanning, configurable menus) vs **hybrid** (global header + product side nav — the enterprise default).
- **Marketing-site frame** (lighter header, no persistent app nav, fuller footer) vs **app frame**.
- **Multi-product shell** (product switcher + per-product side nav).
- **Breakpoint variants** — persistent expanded → rail → drawer/bottom-nav, per the responsive model.

## Anti-patterns

A hamburger menu on desktop where nav fits (hides the IA, raises interaction cost). No skip link (every keyboard user tabs the whole nav on every page). No SPA route-change focus management (the single most common SPA a11y failure — screen-reader users never learn the page changed). "Landmark soup" — nested/duplicated `nav`/`header` without unique labels, or two `main`s. Too many top-level destinations crammed into a horizontal bar. A non-persistent frame that reloads the chrome on every navigation (defeats the app-shell model). A sticky header tall enough to eat the mobile viewport (keep minimal or scroll-link it). Reflowing navigation that jumps as nested accordions open instead of animating height. Burying primary destinations in the account menu. A bottom nav with more than ~5 items.

## Related patterns & components

- **vs the Side Navigation (component)** (see side-navigation) — the nav control's own anatomy, item states, collapse mechanics, and ARIA vs the *frame that places it*. The shell decides whether nav is a side nav and where it sits; the component decides how the nav itself behaves. Re-deriving its internals in the shell is the boundary violation to avoid.
- **vs the page templates** — master-detail, dashboard, settings, error pages (sibling `layout-and-shell` briefs) **sit inside** the shell's `main`. The shell is the substrate; the template is the page. The shell persists; the template swaps.
- **vs Search orchestration (pattern)** (see patterns/search-orchestration) — the header's search field *invokes* that pattern; the shell owns the slot and its placement, not the search experience.
- **vs Breadcrumb / Tabs (components)** — secondary, in-content navigation that lives inside the page template within `main`, not part of the frame.
- **vs the navigation IA / information architecture** — *what* the destinations are and how they're grouped is a discovery/IA strategy concern (see 01-discovery-and-strategy); the shell is the structural vehicle, not the IA.
- **`composes`:** side-navigation, menu, link, button, avatar, badge.

## Field POV evolution

Top nav was the universal standard under low-resolution monitors (vertical space scarce). Widescreen displays flipped it: vertical scroll became effectively infinite while horizontal space stayed constrained, so enterprise apps pivoted to **side nav** for deeper hierarchies and F-pattern scanning without unwieldy mega-menus. The mobile era introduced the **hamburger** as an omnipresent lazy catch-all; an engagement-metrics backlash ("out of sight, out of mind") drove **bottom navigation** for mobile, restricting the hamburger to overflow or complex enterprise mobile. Most recently, the **SPA accessibility reckoning**: frameworks long prioritised seamless visual transitions at the expense of AT users who lost all context on client-side routing, and the mature standard now mandates manually reconstructing focus, live regions, and scroll restoration on route change — the reason this brief treats that as the shell's signature duty. Material 3 has since embraced fully **adaptive navigation** (bar → rail → drawer across breakpoints).

## Reference instantiations

Go look at: **IBM Carbon** UI Shell (distinct Header / Left / Right panels; full-width header capping; trailing-zone product switcher); **Atlassian** page layout (slot-based: Banner / TopNavigation / LeftSidebar / Main; resizable side nav / icon rail); **Material 3** adaptive navigation (the bar → rail → drawer matrix — the gold standard for adaptive shells); **Shopify Polaris** Frame (TopBar + Navigation around the merchant admin / App Bridge content); **GOV.UK** (strict top-nav; the global header separated from the Service navigation — the accessible-frame baseline); **Adobe Spectrum** / **Microsoft Fluent** (OS window-control handling and declarative area-based backbones); the **WAI-ARIA landmark regions** spec and the skip-link pattern.

## Sources cited

- WAI-ARIA Authoring Practices / ARIA landmark regions — banner/navigation/main/complementary/contentinfo, multiple-nav labelling, the skip-link pattern (WCAG 2.4.1 Bypass Blocks); the skip-target `tabindex="-1"` requirement (current; *verify*).
- SPA route-change focus management — the move-focus + `document.title` + `history.scrollRestoration='manual'` contract (a11y community / framework router guidance; *verify specific sources*).
- IBM Carbon — UI Shell, the editorial-vs-fluid grid models (v11, 2025; *verify*).
- Shopify Polaris — Frame, TopBar, Navigation, App Bridge (2024–25; *verify*).
- Atlassian Design System — page layout slots + navigation (2025; *verify*).
- Material 3 — adaptive navigation (drawer / rail / bar by window-size class); the expressive full-height-rail update (2024–25; *verify*).
- Adobe Spectrum (OS window controls), Microsoft Fluent (area-based layout), GOV.UK (service header) — shell/header patterns where documented (*verify*).
- Nielsen Norman Group — top vs side nav, the hamburger-menu research, mobile bottom nav, the Priority+ overflow pattern (*verify articles/dates*).
- The PWA "app shell" architecture model (shell-persists / content-swaps) (*secondary; verify*).

`notes.unverified`: the top-level-destination thresholds (~5–7 for a top bar; ~5 for bottom nav) and the breakpoints (~1024px tablet, ~768px mobile) are widely-used heuristics/conventions, not sourced constants — flag as such; the two passes proposed slightly different numbers (<5 vs ≲7 for top nav). The header-height band (~48–64px) is conventional, not normative. Which design systems ship a *named* app-shell pattern vs a Frame/Shell component is mixed (Carbon and Polaris clearest); verify before asserting convergence. Current version strings flagged.

## Agent-consumable schema

```yaml
identity:
  id: app-shell
  name: App shell
  aliases: [application frame, global header, UI shell, page frame, navigation chrome, masthead]
  tier: layout-and-shell
  goal: navigate
  status: stable
problem: >
  The persistent frame every screen sits inside — the global header and its
  zones, the primary navigation (top vs side vs hybrid), the content region,
  the responsive collapse, the landmark/skip-link skeleton, and the SPA
  route-change focus contract. Applies to apps with persistent multi-destination
  navigation; not to marketing sites or single documents. The page that fills
  the content region is a separate template brief.
composition:
  requires: [side-navigation, menu, link, button, avatar, badge]
  search_slot: search-orchestration
  delta: region model, header zone model, responsive transformation, landmark/skip-link skeleton, SPA route-change contract
decision_rules:
  nav_placement:
    - { if: "broad shallow IA (~5-7 top-level, site/editorial)", use: "horizontal top nav" }
    - { if: "deep/wide app IA (many destinations, nesting, room to grow)", use: "side nav" }
    - { if: "multi-product suite or deep app needing global search/actions/account", use: "hybrid: global top header + side nav" }
  header_zones:
    - { if: "always", use: "3 zones — leading (logo/switcher/nav-trigger), center (search slot), trailing (create/notifications/help/environment/account)" }
    - { if: "no top nav present", use: "expand the center search into the negative space" }
    - { if: "non-production or impersonated", use: "persistent environment banner" }
    - { if: "always", use: "sticky, shallow one row" }
  side_nav_states:
    - { if: "wide viewport", use: "expanded (icon+label), persistent (pushes content)" }
    - { if: "density or user toggle", use: "collapsed icon rail (label on hover/flyout)" }
    - { if: "nested items", use: "expandable tree or rail+flyout, not a deep always-open accordion" }
    - { if: "always", use: "persist collapse choice; aria-current=page on active; sectioned" }
  responsive_collapse:
    - { if: "wide", use: "persistent expanded side nav" }
    - { if: "tablet (~<1024px)", use: "collapsed icon rail / toggle + header hamburger" }
    - { if: "mobile (~<768px) + large/nested IA", use: "hamburger drawer (overlay + scrim); header sheds to essentials" }
    - { if: "mobile + <= ~5 flat peer destinations", use: "bottom navigation bar (no hamburger)" }
    - { if: "top nav overflows before breakpoint", use: "Priority+ (fit what you can, More dropdown)" }
  scroll_model:
    - { if: "always", use: "sticky header + fixed side nav + content is the scroll container; header never scrolls away in an app" }
    - { if: "reading/editorial content", use: "editorial grid: max-width ~1440 centered" }
    - { if: "data tables/dashboards", use: "high-density grid: full browser width" }
  multi_product:
    - { if: "multiple products", use: "product switcher (waffle) at far edge of top header" }
    - { if: "multiple orgs/workspaces", use: "workspace switcher near logo / side-nav top, distinct from account menu" }
layout: >
  Container 100vw/100vh. Regions: header(banner, sticky, ~48-64px, 3 zones) /
  primary nav(navigation, side or top) / main(content + scroll container, one
  page template, editorial max-width-centered or full-bleed high-density) /
  optional complementary / footer(contentinfo, minimal in apps). Header/side-nav
  overlap is contested: Carbon full-width header caps below (default for
  multi-product); Material allows a full-height nav rail with the top bar
  adjacent. Responsive: wide = header + persistent expanded side nav; tablet =
  rail; mobile = essentials header + drawer OR bottom nav + full-width. One
  main, one h1, landmarks intact at every breakpoint; sticky header must not eat
  the mobile viewport (minimal or scroll-linked hide/reveal).
accessibility_orchestration: >
  Landmarks (labelled navs when >1, one main); skip-to-content as first
  focusable -> main, and the main target MUST have tabindex=-1; aria-current=page
  on active item; single heading hierarchy; the SPA route-change contract
  (update document.title + move focus to new h1[tabindex=-1] or main + scroll:
  history.scrollRestoration='manual', reset on forward, restore on back);
  mobile drawer is a focus trap with Esc + focus return; keyboard order matches
  visual order. (Nav control's own ARIA is the Side Navigation component's.)
flow: [persistent (mostly), nav-expand-collapse (persisted, animated width), mobile-drawer-open-close (scrim + focus trap), route-transition (focus+scroll+announce)]
content: >
  Short noun-led nav labels matching page titles; explicit skip-link text
  ("Skip to main content"); non-redundant nav aria-labels ("Primary" not
  "Primary navigation"); switchers name what they switch (distinct from
  account); unambiguous environment-banner copy; accessible labels on icon-only
  header buttons ("Open main menu").
variants: [top-nav-shell, side-nav-shell, hybrid-shell, marketing-frame, multi-product-shell, breakpoint-variants]
anti_patterns:
  - hamburger on desktop where nav fits
  - no skip link (or skip target without tabindex=-1)
  - no SPA route-change focus management
  - landmark soup (duplicated/unlabelled navs, two mains)
  - too many top-level destinations in a horizontal bar
  - non-persistent frame that reloads chrome on navigation
  - sticky header tall enough to eat the mobile viewport
  - nav that reflows/jumps instead of animating height
  - burying primary destinations in the account menu
  - bottom nav with more than ~5 items
reference_instantiations:
  - { system: "IBM Carbon", look_at: "UI Shell (header + side nav, editorial vs fluid grid)" }
  - { system: "Atlassian", look_at: "page layout slots (Banner/TopNav/LeftSidebar/Main)" }
  - { system: "Material 3", look_at: "adaptive navigation (bar/rail/drawer by window size)" }
  - { system: "Shopify Polaris", look_at: "Frame / TopBar / Navigation" }
  - { system: "WAI-ARIA", look_at: "landmark regions + skip-link pattern" }
relations:
  composes: [side-navigation, menu, link, button, avatar, badge]
  relates-to: [search-orchestration, master-detail, dashboard, settings, breadcrumb, tabs]
  boundary: >
    The Side Navigation component is the nav control; this pattern is the frame
    that places it (don't re-derive its internals). The page templates
    (master-detail/dashboard/settings) sit inside the shell's main — the shell
    is the substrate, the template is the page; the shell persists, the template
    swaps. The header search slot invokes Search orchestration. Breadcrumb/Tabs
    are in-content nav. The IA strategy (what the destinations are) is a
    discovery concern, not the frame.
notes:
  contested: "header vs side-nav overlap (Carbon full-width header cap vs Material full-height rail); top vs side vs hybrid at mid-size IAs; hamburger vs bottom-nav on mobile; whether a footer belongs in an app shell"
  unverified: "the ~5-7 top-level and ~5 bottom-nav thresholds, the ~1024/768px breakpoints, and the ~48-64px header height are heuristics/conventions, not constants; which systems ship a NAMED app-shell pattern vs a Frame/Shell component (Carbon/Polaris clearest); version strings"
```
