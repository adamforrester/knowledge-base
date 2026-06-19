*Claude pass — one of two dual-agent inputs for the App shell pattern brief. The first `layout-and-shell` draft; the spine is bent — Layout & structure is heavy, Flow is light. To be synthesised with `external-agent.md` into `patterns/app-shell.md`.*

---

okf_version: "0.1"
type: pattern-brief
title: App shell
description: The persistent application frame every screen sits inside — the global header and its zones, the primary navigation (top vs side vs hybrid), the content region, the responsive collapse across breakpoints, the landmark/skip-link skeleton, and the SPA route-change focus contract. The first layout-and-shell brief, so layout carries the weight and flow is light. Composes Side Navigation + Menu + Link + Avatar + the search slot; borders the Side Navigation component, the page templates that sit inside it, the Search orchestration pattern, Breadcrumb/Tabs, and the IA strategy.
tags: [patterns, app-shell, navigation, layout, accessibility, navigate]
tier: layout-and-shell
goal: navigate
status: draft
aliases: [App shell, application frame, global header, UI shell, page frame, navigation chrome]
last-audited: 2026-06-18
timestamp: 2026-06-18

---

# App shell

> Every screen in an application sits inside the same frame: a header across the top, a primary navigation down the side or along that header, a content region, and — underneath the visuals — a landmark skeleton and a skip link that decide whether the whole thing is navigable by keyboard and screen reader. The shell is the one surface a user never leaves; it is the substrate, not the page. This brief owns the frame — where navigation lives, what the header carries, how it collapses on a phone, and the single most-missed thing in single-page apps: what happens to focus when the content swaps. It defers the nav *control* to the Side Navigation component and the *pages* to the template briefs that sit inside it.

---

## Problem & context

The app shell is the most-seen, least-noticed surface in a product — present on every screen, so its mistakes compound on every screen. The recurring problem is that teams treat the frame as scaffolding and under-think the three things that actually make it work: **where the primary navigation goes** (and how it survives a deep IA), **how the frame collapses** onto a phone without losing its destinations, and **what happens on client-side navigation** — because in a single-page app the page no longer reloads, so focus, scroll, and the screen-reader announcement that a reload used to provide for free must now be orchestrated by hand. Get the frame wrong and every task inside it inherits the cost: a keyboard user tabs through the whole nav on every route, a screen-reader user never learns the page changed, a phone user can't reach half the app.

The pattern applies to any **application** with persistent navigation across multiple destinations — a SaaS product, an admin console, a dashboard suite. It does **not** apply to a marketing site or a single-page document (which want a lighter header and no persistent app nav), and it stops at the content region's edge: what fills the content area is a **page template** (master-detail, dashboard, settings), each its own brief. Systems diverge because the right frame depends on IA shape and platform: a broad, shallow site wants horizontal top nav; a deep app with dozens of destinations wants a side nav; a multi-product suite wants both plus switchers. The decisions below resolve by IA depth and platform rather than by fashion.

## Composition

The shell assembles briefed components into a persistent frame and adds the region structure; it re-derives none of them.

- **Side Navigation** (see side-navigation) — the primary nav control when nav is vertical: its items, sections, collapse/rail behaviour, and `aria-current` are the component's; the shell decides *whether* nav is a side nav and *where it sits in the frame*.
- **Menu** (see menu) — the account/avatar menu, the overflow, the workspace/product switcher dropdowns.
- **Link / Button** (see link, see button) — the logo/home link, header actions, the skip link, the global create/“+”.
- **Avatar** (see avatar) — the account entry point in the header.
- **The search slot** — a Search field that invokes the Search orchestration pattern (see patterns/search-orchestration); the shell owns the slot, not the search experience.
- **Badge** (see badge) — the notification/count indicator on the header bell.

**The delta this pattern adds** is the frame itself: the region model (header / nav / main / optional complementary / footer), the header's zone model, the responsive transformation, the landmark/skip-link skeleton, and the SPA route-change contract — none of which any single component owns.

## Decision rules

The structural forks. Machine-resolvable where a real threshold exists; prose where it's genuinely contextual.

**1. Top nav vs side nav vs hybrid** — the central frame fork.
- `IF the IA is broad and shallow (≲ ~7 top-level destinations, site-like, marketing-adjacent)` → **horizontal top nav** in the header.
- `IF the IA is deep or wide (an app with many destinations, nested sections, or room to grow)` → **side nav** (vertical scales to more items and nesting than a horizontal bar).
- `IF a multi-product suite or a deep app that also needs global actions/search/account` → **hybrid**: a global top header (logo, search, global actions, account, product switcher) **plus** a side nav for the in-product destinations. This is the dominant enterprise shell.
- Bias: apps trend side-nav or hybrid; sites trend top-nav.

**2. The global header anatomy & zones** — the header is a three-zone bar.
- **Left:** logo/home (links to the default route), optionally the nav trigger (mobile) and a product/workspace switcher.
- **Center (or left-of-right):** global **search** (the slot that invokes the Search pattern) — prominent if search is primary.
- **Right:** global **create/“+”**, **notifications** (bell + Badge), **help**, and the **account/avatar menu** — in roughly that order, account-last.
- `IF an environment is non-production or impersonated` → a persistent **environment banner**/indicator (staging, "viewing as…").
- Header is typically **sticky**; keep it shallow (one row) and shed non-essentials on mobile.

**3. Side-nav states.**
- **Expanded** (icon + label) is the default on wide viewports; **collapsed icon rail** (icon-only, label on hover/flyout) for density or when the user toggles it; **rail + flyout** for nested items.
- `IF the nav has nested/multi-level items` → an expandable tree or a rail-with-flyout, not a deep always-open accordion that pushes content down.
- The collapse **toggle persists** the user's choice (localStorage); the active item carries `aria-current="page"`; group with sections + labels.
- Persistent (pushes content) on desktop; **overlay** (over content, with scrim) on mobile.

**4. Responsive collapse** — the desktop → tablet → mobile transformation.
- `IF wide viewport` → side nav **persistent and expanded**.
- `IF medium viewport` → side nav **collapses to an icon rail** or a toggle.
- `IF narrow / mobile` → nav becomes a **hamburger-triggered drawer** (overlay + scrim), OR — `IF ≤ ~5 flat top-level destinations` — a **bottom navigation bar** (thumb-reachable, no hamburger). Bottom nav beats a hamburger for a small flat IA; a hamburger is right for a large/nested one.
- The header sheds to: logo, nav trigger, maybe search icon, account; everything else moves into menus.

**5. Landmark & skip-link structure** — the a11y the shell owns.
- One `banner` (header), `navigation` landmark(s), one `main`, optional `complementary`, one `contentinfo` (footer). **Label each `navigation`** (`aria-label="Primary"`, `"Breadcrumb"`) when there's more than one.
- A **skip-to-content link** as the first focusable element, jumping focus to `main` — non-negotiable, because the nav repeats on every page.
- Logical keyboard order: skip link → header → nav → main; a single, correct heading hierarchy (one `h1` per view, in `main`).

**6. The SPA route-change contract** — the single most-missed a11y issue.
- On client-side navigation the page doesn't reload, so the shell must: **move focus** to a sensible target (the `main`/`h1` of the new view, or a focusable container), **restore/reset scroll** (top for a new page; preserved for back), and **announce the change** (update the document `<title>` and/or a polite live region with the new page name).
- `IF the shell persists and only the content swaps` (the app-shell model) → this orchestration is mandatory; a server-rendered full reload gets it for free, an SPA does not.

**7. Scroll & persistence model.**
- Header **sticky** at top; side nav **fixed** (own scroll if long); the **content region is the scroll container**. Content has a **max-width and is centered** for readability on wide screens (full-bleed only for dashboards/tables that need it).
- The frame persists; only `main` swaps.

**8. Multi-product / workspace.**
- `IF multiple products` → a **product switcher** (a grid/menu) in the top-left header.
- `IF multiple orgs/workspaces` → a **workspace switcher**, usually top-left near the logo or at the side-nav top.
- Keep switchers distinct from the account menu (switching context ≠ managing your account).

## Layout & structure

The heavy section for this tier. The frame is a small set of regions:

- **Header (`banner`)** — full-width, sticky, shallow (one row, ~48–64px). Three zones: left (logo / switcher / nav trigger), center (search), right (create / notifications / help / account). Sheds to essentials on mobile.
- **Primary navigation (`navigation`)** — side (vertical, scales deep) or top (horizontal, shallow). Side nav: fixed, own scroll, expanded/rail/drawer by breakpoint.
- **Main (`main`)** — the content region and scroll container; holds exactly one page template; max-width + centered by default, full-bleed when the template demands it.
- **Complementary (`complementary`)** — optional contextual/right panel (details, help, activity); not the primary nav.
- **Footer (`contentinfo`)** — minimal in apps (legal/version), fuller on sites.

**The responsive model:** wide → header + persistent expanded side nav + centered content; medium → header + collapsed rail; narrow → header (essentials) + hamburger drawer *or* bottom nav + full-width content. One `main`, one `h1`, landmarks intact at every breakpoint. The header's stickiness must not eat the mobile viewport — keep it one shallow row.

## Accessibility orchestration

The a11y the *frame* owns (the nav control's own ARIA is inherited from Side Navigation):
- **Landmarks** — `banner` / `navigation` (labelled) / `main` / `complementary` / `contentinfo`, so AT users can jump between regions; exactly one `main`.
- **Skip link** — first focusable element, visible on focus, moves focus to `main`; the answer to "the nav repeats on every page."
- **`aria-current="page"`** on the active nav item; a single correct heading hierarchy.
- **The SPA route-change contract** (the shell's signature a11y duty) — move focus to the new view's `main`/heading, reset/restore scroll, and announce via `<title>` + a polite live region, because the reload that used to announce a page change no longer happens.
- **The mobile drawer** — a focus trap while open, Esc to close, focus returns to the trigger; the scrim is inert to AT.
- Keyboard order matches visual order through the frame.

## Flow & states

Light, by tier. The shell is mostly persistent; its only stateful bits: the **side-nav expand/collapse** (toggle, persisted), the **mobile drawer open/close** (with focus trap), and the **route transition** (focus + scroll + announcement, per the a11y contract). No journey, no submission lifecycle — that's what makes this a `layout-and-shell` brief, not a `composition` one.

## Content & copy

- **Nav labels** are short, noun-led, and consistent with the destinations' page titles; no jargon.
- **Skip-link text** is explicit ("Skip to main content").
- **Account/switcher labels** name what they switch ("Switch workspace," not just an avatar); the account menu is the person's name/email.
- **Environment banner** copy is unambiguous ("Staging environment," "Viewing as [user] — exit").
- **Notification/help** controls carry accessible labels (icon-only buttons need them).

## Variants & responsive

- **Top-nav shell** (broad/shallow, site-like) vs **side-nav shell** (deep app) vs **hybrid** (global header + product side nav — the enterprise default).
- **Marketing-site frame** (lighter header, no persistent app nav, fuller footer) vs **app frame**.
- **Multi-product shell** (product switcher + per-product side nav).
- **Breakpoint variants** — persistent expanded → rail → drawer/bottom-nav, as in the responsive model.

## Anti-patterns

A hamburger menu on desktop where there's room for visible nav (hides the IA for no reason). No skip link (every keyboard user tabs the whole nav on every page). No route-change focus management in an SPA (screen-reader users never learn the page changed — the single most common SPA a11y failure). Missing or duplicated landmarks (two `main`s, unlabelled multiple navs). Too many top-level destinations crammed into a horizontal bar (use a side nav). A non-persistent frame that reloads the chrome on every navigation (defeats the app-shell model). A sticky header so tall it eats the mobile viewport. Nav that reflows unpredictably between breakpoints. Burying primary destinations in an account menu. A bottom nav with more than ~5 items (overflow becomes unreachable).

## Related patterns & components

- **vs the Side Navigation (component)** (see side-navigation) — the nav control's own anatomy, item states, collapse mechanics, and ARIA vs the *frame that places it*. The shell decides whether nav is a side nav and where it sits; the component decides how the nav itself behaves.
- **vs the page templates** — master-detail, dashboard, settings, error pages (sibling `layout-and-shell` briefs) **sit inside** the shell's `main`. The shell is the substrate; the template is the page. The shell persists; the template swaps.
- **vs Search orchestration (pattern)** (see patterns/search-orchestration) — the header's search field *invokes* that pattern; the shell owns the slot and its placement, not the search experience.
- **vs Breadcrumb / Tabs (components)** — secondary, in-content navigation that lives inside `main`, not part of the frame.
- **vs the navigation IA / information architecture** — *what* the destinations are and how they're grouped is a discovery/IA strategy concern (see 01-discovery-and-strategy); the shell is the structural vehicle, not the IA.
- **`composes`:** side-navigation, menu, link, button, avatar, badge.

## Field POV evolution

Three arcs. **Top nav → side nav for apps**: as products grew deep IAs, the horizontal bar ran out of room and the side nav (which scales vertically and nests) became the app default, while sites kept top nav. **The hamburger backlash and bottom-nav rise**: NN/g and others showed the desktop hamburger hides navigation and lowers engagement; the field pulled primary nav back into view on desktop and adopted **bottom navigation** on mobile for small flat IAs (thumb-reachable, always visible) over the catch-all hamburger. And **the SPA focus-management reckoning**: as client-side routing became universal, the industry belatedly recognised that the free page-change announcement of a server reload was gone, and route-change focus + announcement became a known (if still under-implemented) requirement — the reason this brief treats it as the shell's signature a11y duty.

## Reference instantiations

Go look at: **IBM Carbon** UI Shell (header + side nav, the rail) ; **Shopify Polaris** Frame / TopBar / Navigation; **Atlassian** page layout + navigation system (the slots model); **Material 3** adaptive navigation (drawer vs rail vs bar by window size); the **WAI-ARIA landmark regions** spec and the skip-link pattern; **GOV.UK** service header / page template for the accessible-frame baseline.

## Sources cited

- WAI-ARIA Authoring Practices / ARIA landmark regions — banner/navigation/main/complementary/contentinfo, the skip-link pattern, multiple-nav labelling (current; *verify*).
- SPA route-change focus management guidance — the move-focus-on-navigation + announce contract (a11y community / GOV.UK; *verify specific sources*).
- IBM Carbon — UI Shell (header, side nav, rail) (v11, 2025; *verify*).
- Shopify Polaris — Frame, TopBar, Navigation (2024–25; *verify*).
- Atlassian Design System — page layout + navigation (2025; *verify*).
- Material 3 — adaptive navigation (drawer / rail / bar by window-size class) (2024–25; *verify*).
- Microsoft Fluent, Adobe Spectrum, GOV.UK — shell/header patterns where documented (*spotty; flag where absent*).
- Nielsen Norman Group — top vs side nav, the hamburger-menu research, mobile bottom nav (*verify articles/dates*).
- The PWA "app shell" architecture model (shell-persists / content-swaps) (*secondary; verify*).

`notes.unverified`: the top-level-destination thresholds (~7 for a top bar; ~5 for bottom nav) are widely-used heuristics, not sourced constants — flag as such. The header height band (~48–64px) is conventional, not normative. Which design systems ship a *named* app-shell pattern vs leave it to a Frame/Shell component is mixed (Carbon and Polaris are clearest); verify before asserting convergence. Current version strings flagged.

## Agent-consumable schema

```yaml
identity:
  id: app-shell
  name: App shell
  aliases: [application frame, global header, UI shell, page frame, navigation chrome]
  tier: layout-and-shell
  goal: navigate
  status: draft
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
    - { if: "broad shallow IA (<= ~7 top-level, site-like)", use: "horizontal top nav" }
    - { if: "deep/wide app IA (many destinations, nesting, room to grow)", use: "side nav" }
    - { if: "multi-product suite or deep app needing global search/actions/account", use: "hybrid: global top header + side nav" }
  header_zones:
    - { if: "always", use: "3 zones — left (logo/switcher/nav-trigger), center (search slot), right (create/notifications/help/account)" }
    - { if: "non-production or impersonated", use: "persistent environment banner/indicator" }
    - { if: "always", use: "sticky, shallow one row; shed non-essentials on mobile" }
  side_nav_states:
    - { if: "wide viewport", use: "expanded (icon+label), persistent (pushes content)" }
    - { if: "density or user toggle", use: "collapsed icon rail (label on hover/flyout)" }
    - { if: "nested items", use: "expandable tree or rail+flyout, not a deep always-open accordion" }
    - { if: "always", use: "persist collapse choice; aria-current=page on active; sectioned" }
  responsive_collapse:
    - { if: "wide", use: "persistent expanded side nav" }
    - { if: "medium", use: "collapsed icon rail / toggle" }
    - { if: "narrow + large/nested IA", use: "hamburger-triggered drawer (overlay + scrim)" }
    - { if: "narrow + <= ~5 flat destinations", use: "bottom navigation bar (no hamburger)" }
  landmarks_skip:
    - { if: "always", use: "banner/navigation(labelled)/main/complementary/contentinfo; one main; skip-to-content first focusable" }
  spa_route_change:
    - { if: "client-side navigation (shell persists, content swaps)", use: "move focus to new main/h1 + reset/restore scroll + announce via title + polite live region" }
  scroll_model:
    - { if: "always", use: "sticky header + fixed side nav + content is the scroll container; content max-width + centered (full-bleed only when the template needs it)" }
  multi_product:
    - { if: "multiple products", use: "product switcher in top-left header" }
    - { if: "multiple orgs/workspaces", use: "workspace switcher near logo / side-nav top, distinct from account menu" }
layout: >
  Regions: header(banner, sticky, ~48-64px, 3 zones) / primary nav(navigation,
  side or top) / main(content + scroll container, one page template, max-width
  centered) / optional complementary / footer(contentinfo, minimal in apps).
  Responsive: wide = header + persistent expanded side nav + centered content;
  medium = collapsed rail; narrow = essentials header + drawer OR bottom nav +
  full-width. One main, one h1, landmarks intact at every breakpoint.
accessibility_orchestration: >
  Landmarks (labelled navs, one main); skip-to-content as first focusable ->
  main; aria-current=page on active item; single heading hierarchy; the SPA
  route-change contract (focus to new view + scroll reset/restore + title/
  live-region announcement); mobile drawer is a focus trap with Esc + focus
  return; keyboard order matches visual order. (Nav control's own ARIA is the
  Side Navigation component's.)
flow: [persistent (mostly), nav-expand-collapse (persisted), mobile-drawer-open-close (focus trap), route-transition (focus+scroll+announce)]
content: >
  Short noun-led nav labels matching page titles; explicit skip-link text;
  switchers name what they switch (distinct from account); unambiguous
  environment-banner copy; accessible labels on icon-only header buttons.
variants: [top-nav-shell, side-nav-shell, hybrid-shell, marketing-frame, multi-product-shell, breakpoint-variants]
anti_patterns:
  - hamburger on desktop where nav fits
  - no skip link
  - no SPA route-change focus management
  - missing or duplicated landmarks (two mains, unlabelled navs)
  - too many top-level destinations in a horizontal bar
  - non-persistent frame that reloads chrome on navigation
  - sticky header tall enough to eat the mobile viewport
  - nav that reflows unpredictably between breakpoints
  - burying primary destinations in the account menu
  - bottom nav with more than ~5 items
reference_instantiations:
  - { system: "IBM Carbon", look_at: "UI Shell (header + side nav, rail)" }
  - { system: "Shopify Polaris", look_at: "Frame / TopBar / Navigation" }
  - { system: "Atlassian", look_at: "page layout + navigation slots" }
  - { system: "Material 3", look_at: "adaptive navigation (drawer/rail/bar by window size)" }
  - { system: "WAI-ARIA", look_at: "landmark regions + skip-link pattern" }
relations:
  composes: [side-navigation, menu, link, button, avatar, badge]
  relates-to: [search-orchestration, master-detail, dashboard, settings, breadcrumb, tabs]
  boundary: >
    The Side Navigation component is the nav control; this pattern is the frame
    that places it. The page templates (master-detail/dashboard/settings) sit
    inside the shell's main — the shell is the substrate, not the page. The
    header search slot invokes Search orchestration. Breadcrumb/Tabs are
    in-content nav. The IA strategy (what the destinations are) is a discovery
    concern, not the frame.
notes:
  contested: "top vs side vs hybrid at mid-size IAs; hamburger vs bottom-nav on mobile; whether the footer belongs in an app shell at all"
  unverified: "the ~7-top-level and ~5-bottom-nav thresholds and the ~48-64px header height are heuristics, not constants; which systems ship a NAMED app-shell pattern vs a Frame/Shell component (Carbon/Polaris clearest); version strings"
```
