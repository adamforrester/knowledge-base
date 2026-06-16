# Side Navigation — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/side-navigation.md`; version numbers and the inherited platform-state flagged unverified. The two passes converged almost completely — no substantive disagreement.*

---

Side Navigation: Architecture, Implementation, and Field-Truth Convergence

## 1. Framing
Side navigation is the structural terminus of the navigation taxonomy — the primary, persistent spatial contract of an app, commanding a dedicated geometric region and dictating layout boundaries for sibling content. Reaching it closes the navigation category. It is highly composite, standing on four substrates: Link (anchor + router polymorphism + aria-current="page" active boundary), Drawer (the transient modal overlay on restricted viewports), Accordion (in-place vertical disclosure for multi-level), Tooltip (accessible names when collapsed to an icon rail). The defining tension is persistent-structure vs transient-drawer: a side nav is a persistent block in the CSS Grid/Flexbox shell, scaling from a collapsed rail (56-80px) to an expanded panel (240-320px), stable across routes; a drawer is a transient overlay escaping flow, trapping focus. Modern architectures transform between these on viewport thresholds without layout thrashing or SSR hydration mismatches.

## 2. Anatomy and Parts
Macro (in a <nav>/<aside>, flex-shrink:0, full height): header (sticky top — branding/workspace switcher), scrollable content (overflow-y:auto, flex-grow:1, independent scroll, not window scroll), footer (sticky bottom — settings/profile/auth), resize rail (cursor:col-resize — drag width / toggle collapse; shadcn/Atlassian). Micro: Navigation Group (+ Group Header, optionally an accordion toggle) > Navigation Item [Leading Visual (icon/avatar, persists in rail) + Label + Trailing Visual (badge/count/chevron) + Active Indicator (border/fill/weight = aria-current=page)].

## 3. Properties / API
Three models. Monolithic (Polaris — a deep items JSON object; consistent but bundles router logic, brittle Next/React Router integration, precludes SSR optimisation). Composable slots (shadcn/Primer — <SidebarGroup>/<SidebarMenu>/<SidebarMenuItem>, asChild polymorphism applies DS classes to the consumer's router link without intercepting click; Primer refactored NavList to SSR-compatible slots removing deep-nesting limits). Overrides (Base Web — a data array + an overrides object injecting custom components at any node). Practice default: composable slots with polymorphic rendering.

## 4. States and Variants
Expanded (240-320px, labels+badges+chevrons visible, grid computes remaining width). Collapsed Rail (56-80px, mandatory mute: labels/badges/chevrons disappear, icons only; nested sub-menus pivot from in-place Accordion to floating Flyouts/Popovers; icons must trigger Tooltips on hover+focus). Modal Drawer (<768px, persistent grid abandoned, hidden behind a hamburger; elevated z-index, semi-transparent aria-hidden backdrop, focus trapped until dismissed via overlay click/close button/Escape). Material 3 Expressive deprecated the standard Navigation Drawer for the Expanded Navigation Rail — a rail and a drawer are responsive variants of the same hierarchical data structure.

## 5. Usage Guidance
Carbon: side nav mandatory past >5 top-level secondary items (top nav exhausts horizontal space -> overflow/truncation; side nav scales vertically). Supports up to three levels (Category > Sub-menu > Item); top nav struggles past one dropdown layer. Boundaries: never mix top and side primary nav — if side nav is primary, the top bar is global utilities only (search, notifications, account, workspace switcher); splitting routing fragments the mental model. Side nav = structural routing (changes URL + page context); Tabs = localised in-page panel switching (never nest tabs as nav); Breadcrumbs = where you are relative to root (auxiliary, never replaces side nav).

## 6. Accessibility
The most pervasive catastrophic error: blindly applying role="menu" to site nav (Ant Design wraps vertical nav in role="menu" + role="menuitem"). role="menu" is exclusively for desktop-app command menus (File/Edit/View) — it makes AT expect Tab to exit and arrow-key/roving-tabindex/activedescendant internal navigation, breaking the Tab-through-links expectation; the nav becomes inaccessible to standard keyboard traversal. Correct: the Disclosure Navigation pattern — a <nav> landmark with a unique aria-label (a page has multiple navs), an <ul> wrapper (announces item count/position), <a> links with aria-current="page" on the active one, and a <button aria-expanded aria-controls> for sub-section toggles (Space/Enter toggles the nested <ul>). Disclosure Navigation Hybrid: when a parent is both a routable link and a toggle, place a secondary <button> chevron adjacent to the link (Enter on the link navigates; Space/Enter on the chevron expands). Skip link: a visually-hidden <a href="#main-content"> positioned in the DOM immediately before the <nav>, revealed on focus, to bypass the nav. Tree boundary: role="tree"/treeitem (Up/Down between nodes, Left/Right collapse/expand) is for infinitely-deep hierarchical data (file systems); site nav uses <nav> + disclosure, not treeview.

## 7. Content Guidelines
Labels ruthlessly concise (1-3 words); long labels wrap (destroy vertical rhythm) or truncate (hide context) — Material: wrap to max 2 lines, then rewrite, don't dynamically shrink/truncate. Sentence casing (title case's jagged tracking slows scanning). Auxiliary data as trailing badges, subordinate to the label, hidden when collapsed to a rail. Icons: simple monochromatic vectors; Apple HIG 44x44pt touch targets (impacts mobile drawer); consistent icon usage per hierarchy level (mixing icon-led + text-only breaks the alignment axis).

## 8. Motion and Transition
The expand/collapse is the most performance-sensitive motion. Animating container width forces continuous reflow/layout recalculation every frame; if the nav is in a flex/grid alongside main content, the content resizes violently (layout thrashing). Mitigate: wrap text in white-space:nowrap + overflow:hidden so it doesn't wrap as the container shrinks; fade label opacity out slightly BEFORE the width reduction; icons stay fixed; drive width via CSS variables. The mobile drawer must NEVER animate width/left — sit it off-canvas and animate transform: translateX(-100% -> 0) (GPU composite layer, flawless 60fps, no document reflow).

## 9. Internationalization
RTL: complete structural inversion — panel shifts left->right edge; within items, icons move right, badges/chevrons left; disclosure chevrons mirror (point left when collapsed). Handle natively via CSS logical properties (margin-inline-start not margin-left) — flips off the computed dir attribute. String expansion: English->German/Russian +30-50%; handle via user-controlled resize rail (Atlassian) or graceful multi-line wrapping without breaking flex padding.

## 10. Naming
"Sidebar" (Apple HIG, shadcn) — generic, but connotes an auxiliary <aside> content panel, not the routing backbone. Carbon: "UI Shell Left Panel" (a layout wrapper for the whole app). Material: "Navigation Drawer" (transient overlay) vs "Navigation Rail" (permanent narrow track). Primer: NavList (detaches the <ul> from the layout container). Practice default: Side Navigation — most precise, describes position + purpose without binding to a width (Rail) or state (Drawer).

## 11. Implementation Notes
State persistence + hydration mismatch (the prominent hazard): the collapsed/expanded preference must persist across routes and sessions; component-local state resets on refresh. localStorage in SSR causes a hydration mismatch — the server renders without localStorage access (defaults to expanded), the client hydrates, reads localStorage, forces a DOM update, causing FOUC + a violent layout shift (expanded -> collapsed). The definitive fix (shadcn): store the preference in an HTTP cookie — sent on every request, the server reads it and renders correct width classes in the initial HTML, zero shift. Where cookies can't be used (caching/privacy): a blocking synchronous inline <script> in <head> reads localStorage and applies a CSS variable (--sidebar-width) to :root before the body paints. Router integration: items must generate real <a href> (SEO, middle-click) but SPA routers need their own link components; use the asChild composition pattern to apply DS padding/hover/active to the consumer's router link, bypassing the "Browser history needs a DOM" errors of monolithic APIs (Polaris). Atlassian integrated Pragmatic Drag and Drop for end-user item reordering (persisted sort order).

## 12. Related and Alternative Components
Top Navigation (header) — horizontal global bar; primary routing only if <5 top-level items and no deep sub-menus; often paired with side nav as a global utility belt. Tabs — in-page panel visibility toggle, lower in the hierarchy, never for site routing. Breadcrumbs — secondary trail of hierarchical depth relative to root; contextualises position within the side nav, doesn't replace it. Tree View — keyboard-intensive widget for deep hierarchical datasets, arrow-key traversal, independent of routing.

## 13. Field POV Evolution
The fall of the Permanent Drawer — Material 2's rigid always-expanded ~300px desktop drawer was deprecated in Material 3 Expressive for the Expanded Navigation Rail (300px persistent width on medium screens is hostile to content density); all modern side navs must gracefully collapse. The accessibility correction — early React/Vue blindly applied role="menu"; W3C APG campaigns corrected this to the Disclosure Navigation pattern (Tab through links, no hijacked focus managers). Monolithic -> slot composition — config-driven JSON (Polaris, friction with React Router + full-stack frameworks) gave way to primitive structural nodes (shadcn/Primer) empowering arbitrary layouts, server components, granular data fetching.

## 14. Field Systems Evaluated
Material 3 (Expressive — Drawer/Rail relationship, deprecating permanent drawers). IBM Carbon (UI Shell "Left Panel"; >5-items threshold; restricts nesting to a single sub-menu tier). GitHub Primer (NavList — SSR-compatible slots, resolved layout shifting + deep nesting). Shopify Polaris (monolithic Navigation — JSON API friction with React Router). Atlassian (resizable 56->320px; Pragmatic Drag and Drop reorder). Ant Design (problematic default role="menu"/role="menuitem" — an active anti-pattern). Base Web (the overrides API). shadcn/ui (SidebarProvider context, CSS-variable layout math, collapsible="icon" rail, cookie SSR persistence). Apple HIG (44x44pt touch targets).

## 15. Agent-Consumable Schema

```yaml
component: side_navigation
description: A persistent, composition-heavy layout primitive providing the primary routing backbone. Transforms from an expanded panel to a collapsed rail or modal drawer based on viewport constraints.
inherits:
  - link (routing, active state, aria-current)
  - drawer (mobile overlay)
  - accordion/disclosure (nested sub-menus)
  - tooltip (rail icon labels)
accessibility:
  landmark: <nav aria-label="Primary Navigation">
  pattern: Disclosure Navigation (NOT role="menu")
  keyboard: Tab/Shift+Tab (traverse links), Enter/Space (activate link or toggle disclosure), Esc (close drawer or flyout)
anatomy:
  Provider: Manages expanded/collapsed state and cookie/localStorage sync.
  Sidebar: The primary layout container (flex or grid).
  Header: Sticky top region (branding).
  Content: Scrollable track.
  Group: Semantic grouping section.
  MenuItem: <li> wrapper.
  MenuButton: Polymorphic slot (asChild) wrapping native framework links.
  Rail: Resize or toggle interactive handle.
api_architecture: composable_slots
states:
  - expanded: Full width (e.g., 256px - 320px), text and trailing visuals visible.
  - collapsed_rail: Minimized width (e.g., 56px - 80px), icons only, tooltips required.
  - mobile_drawer: Transient overlay invoked via header hamburger button.
implementation_rules:
  - Do not use role="menu" or role="menuitem" for primary site routing.
  - Prevent FOUC by hydrating collapsed/expanded state via HTTP cookies or blocking head scripts.
  - Avoid width animations on the main container; use CSS transforms or max-width transitions to prevent layout thrashing.
  - Require a visually hidden skip-to-content link immediately preceding the <nav> element.
```
