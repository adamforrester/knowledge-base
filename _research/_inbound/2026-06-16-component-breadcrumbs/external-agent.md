# Breadcrumbs — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/breadcrumbs.md`; version numbers and the Atlassian maxItems=8 default flagged unverified.*

---

Breadcrumbs: Field-Truth Component Report

## 1. Framing
The Breadcrumbs component operates as a secondary navigation mechanism designed to reveal the user's location within a hierarchical information architecture. While its visual presentation is ostensibly simple—a horizontally arranged sequence of text labels and separators—the Breadcrumbs component represents one of the most structurally contested patterns in modern enterprise design systems. The implementation of this component sits squarely at the intersection of complex accessible routing, responsive space constraints, semantic markup discipline, and machine-readable metadata for search engine optimization (SEO).

At a conceptual level, the contemporary practice has strictly converged on a location-based routing model over a path-based routing model. Path-based implementations—which dynamically generated crumbs reflecting the user's historical click path (e.g., Search Results > Category > Product)—have been universally deprecated across leading design systems. They duplicate native browser history functionality, disorient users navigating via direct links, and break the predictability of the site's permanent taxonomy. The modern Breadcrumb strictly mirrors the site's information architecture, providing a predictable escape hatch up the structural tree.

Despite this ontological consensus, the mechanical implementation exhibits significant divergence across the industry. Leading systems—including Adobe Spectrum (React Aria), IBM Carbon, GitHub Primer, Atlassian Design System, and Base Web—disagree sharply on fundamental architectural decisions. These disagreements manifest in the interactive nature of the current page indicator, the rendering methodology for visual separators, the mathematical overflow and truncation logic for deep hierarchies, and the integration of JSON-LD structured data.

Furthermore, mobile design paradigms introduce a severe contextual conflict. While web-centric systems rely on deep Breadcrumb trails to orient users in complex dashboards or vast e-commerce catalogs, mobile-first guidelines such as the Apple Human Interface Guidelines (HIG) and Google's Material 3 heavily favor single-level back buttons and flat Top App Bars. The traditional multi-node Breadcrumb is increasingly viewed as an anti-pattern on narrow viewports, forcing design system architects to build complex responsive state swaps into the component's core logic.

## 2. Anatomy and Parts
The structural anatomy of a Breadcrumbs component is rigorously governed by the W3C ARIA Authoring Practices Guide (APG). The standardized anatomy consists of: Navigation Landmark (<nav>) with a descriptive accessible name; List Container (<ol>); Crumb Node (<li>); Crumb Link (<a> or polymorphic <Link>) inheriting the system's baseline Link; Separator (decorative, hidden from the accessibility tree); Overflow Affordance (ellipsis ... opening a menu of collapsed nodes); Current Marker (final node — split between self-referential link and static text).

The Landmark and Ordered List Contract: React Aria and Primer enforce <nav aria-label="Breadcrumb">, establishing a discrete landmark. The <ol>/<li> structure announces total count and sequential position. A flat row of <span>/<div> violates WCAG 1.3.1.

Separator Architecture: separators must never be read by screen readers or inserted as independent list items. React Aria requires aria-hidden="true" on DOM-injected separators; modern systems prefer CSS pseudo-elements (li:not(:last-child)::after { content: '/'; }).

## 3. Properties / API
Two patterns: data-driven (items array) or composable declarative (JSX children). Props: children/items; maxItems (Atlassian default 8); itemsBeforeCollapse (default 1); itemsAfterCollapse (default 1 or 2); separator; overflow ('wrap' | 'menu' | 'menu-with-root', Primer, default 'wrap'); aria-label (default "Breadcrumb"); defaultExpanded (default false); onExpand callback.

Truncation/overflow: when array length exceeds maxItems, compute visual slices. maxItems={5}, itemsBeforeCollapse={1}, itemsAfterCollapse={2} on an 8-item array renders [Item 1] > [...] > [Item 7] > [Item 8]. Root + immediate parent/current stay visible.

## 4. States and Variants
Crumbs inherit Link states (Rest/Hover/Focus-Visible/Active). The Current Page State is the most contested decision:
- Methodology A (Primer, React Aria): interactive <a> with aria-current="page", visually de-emphasised. Maintains uniform focusable DOM, simplifies polymorphic API, allows refresh-by-click.
- Methodology B (IBM Carbon, Base Web): non-interactive static text node, removed from tab sequence. A non-navigating link violates anchor expectations; Ctrl+R/Cmd+R makes self-link redundant.
Opinionated default: Methodology A (aria-current="page" link) increasingly preferred for net-new systems, driven by polymorphic routing (Next.js/React Router) simplifying the API.

Collapsed/Overflow: icon-only <button> with ellipsis, aria-expanded, opening Popover/Menu. Condensed/Mobile: Primer overflow="menu" forces collapse; iOS HIG/Android favour dropping the trail for a single "Back" chevron / Top App Bar. Below 768px hide all <li> except penultimate node.

## 5. Usage Guidance
Use for deep hierarchies (3+ levels). Don't use for flat architectures, linear flows (Stepper), or mobile native apps (HIG discourages). Breadcrumb vs Back Button: history vs taxonomy. Polaris Page back-arrow blurs this. Breadcrumb vs Tabs: peers vs parent-child. Strictly secondary wayfinding.

## 6. Accessibility
nav must have aria-label. aria-current accepts page/step/location/date/time/true; for breadcrumbs aria-current="page" is the strict standard (location reserved for broader environment indicators). Separators aria-hidden="true" if DOM elements. Overflow ellipsis is a <button> with aria-haspopup="menu", aria-expanded, descriptive aria-label ("Show path"). Menu follows APG, traps focus, Escape returns focus. Participates in WCAG 2.4.8 Location (AAA) and 1.3.1 (A).

## 7. Content Guidelines
Labels match page title, aliased if verbose ("Quarterly Financial Earnings Report Q3 2026" -> "Q3 2026"). Prefer whole-node menu collapse over per-label CSS truncation; if truncating, attach accessible Tooltip on hover and focus. Home/Root: house icon needs aria-label="Home"; icon+text needs aria-hidden on the svg.

## 8. Motion and Transition
Limited to overflow menu disclosure: 100ms opacity fade + 4px translate, scale 0.95->1.0. Respect prefers-reduced-motion: reduce (snap open).

## 9. Internationalization
RTL: trail reverses (root far right) via Flexbox + logical properties. Symmetrical / needs no mirroring; asymmetrical chevron > flips to < via transform: scaleX(-1) on dir="rtl" or swapped SVG. Text expansion 30-50% (German/Russian/Finnish); truncation logic must recalculate.

## 10. Naming
Parent: Breadcrumbs (plural standard); aliases Breadcrumb, Trail. Child: BreadcrumbItem / Breadcrumb.Item / Crumb. Naming the child singular Breadcrumb is an anti-pattern. Default: Breadcrumbs wrapping BreadcrumbItem.

## 11. Implementation Notes
Separators via CSS pseudo-elements/sibling combinator, not JSX mapping. Physical SVGs aria-hidden + focusable="false". Router integration via asChild polymorphic pattern (Radix) or as prop — agnostic of the consuming router. SEO/JSON-LD: the UI component should NOT emit JSON-LD — SSR frameworks generate metadata in the server <head> before render; client-side emission risks duplicate scripts, hydration mismatches, parse failure if JS fails, and de-indexing if hidden via display:none. Delegate to the application page-level/SEO layer.

## 12. Related and Alternative Components
Link (foundational primitive); Tabs (peer panels); Stepper/Progress Indicator (linear flows); Menu (overflow); Back Button (history-based, favoured on mobile by HIG/Material).

## 13. Field POV Evolution
Path-based -> location-based. Wrapping -> truncation (overflow menu). DOM clutter -> polymorphism (asChild). Separation of concerns: JSON-LD extracted from UI into SSR layer.

## 14. Sources Cited
Adobe Spectrum / React Aria useBreadcrumbs, Breadcrumbs (v3.5.32 / v1-16-0, 2026). IBM Carbon Breadcrumb (v11/React, 2026). GitHub Primer Breadcrumbs (React Components, 2026). Atlassian Breadcrumbs (v16.1.1, 2026). Base Web (Uber) Breadcrumbs (v18.1.0, 2026). Shopify Polaris Page breadcrumb / Web Components (v12/13, 2026). Google Material 3 Web / Top App Bar (2026). Apple HIG Navigation / Page Controls (2026). W3C WAI-ARIA APG Breadcrumb Pattern (2026).

## 15. Agent-consumable schema

```yaml
identity:
  name: Breadcrumbs
  aliases:
  category: Navigation
  description: A secondary navigation system displaying the hierarchical path to the user's current location within the information architecture.

anatomy:
  - nav (landmark wrapper)
  - ol (ordered list container)
  - li (node wrapper)
  - a/span/Link (crumb interactive element)
  - separator (visual divider, strict preference for CSS pseudo-element)
  - overflowMenu (ellipsis trigger button + popover/menu)

api:
  items: { type: ReactNode | Array, description: Collection of BreadcrumbItem children or data objects. }
  maxItems: { type: number, default: 8, description: Threshold triggering middle-node collapse into an overflow menu. }
  itemsBeforeCollapse: { type: number, default: 1, description: Number of root nodes to preserve before the ellipsis. }
  itemsAfterCollapse: { type: number, default: 1, description: Number of current/parent nodes to preserve after the ellipsis. }
  separator: { type: ReactNode | string, default: "'/' or '>'", description: Override for the visual divider. }
  aria-label: { type: string, default: 'Breadcrumb', description: Essential landmark label required by APG. }

states:
  rest: Default static state.
  hover: Underline appears or color intensifies (inherits Link primitive).
  focus-visible: High contrast focus ring on the interactive node.
  active: Pressed state (inherits Link primitive).
  current: Final node; styling removes standard link affordances, carries aria-current.
  collapsed: Middle nodes hidden within the overflow menu, controlled by maxItems.

variants:
  default: Standard full-width location trail.
  with-home-icon: Root node text replaced by an icon requiring aria-label="Home".
  condensed: Mobile-viewport swap to a single back-chevron (system dependent).

accessibility:
  landmark: Must wrap in <nav aria-label="Breadcrumb"> to distinguish from global nav.
  list_semantics: Must use <ol> and <li> to denote sequential count to screen readers.
  current_marker: Interactive final node must strictly carry aria-current="page".
  separators: DOM-injected separators must carry aria-hidden="true".
  keyboard: Overflow ellipsis must be focusable, open via Enter/Space, and trap focus.

content:
  conciseness: Labels must be concise, aliasing verbose destination page titles.
  truncation: Avoid CSS text-overflow on individual nodes; prefer middle-node menu collapse.

motion:
  menu_disclosure: 100ms fade/translate on overflow menu open.
  reduce_motion: Bypass all transitions, instantly snap open for prefers-reduced-motion.

i18n:
  rtl_flip: Asymmetrical separators (>) must visually flip to (<) via CSS transform.
  expansion: Collapse threshold logic must recalculate safely against text expansion.

implementation:
  - Polymorphic routing (asChild or component prop) is strictly required to bypass full-page SPA reloads.
  - Separators should ideally be CSS pseudo-elements (::after) attached to <li> to bypass the ARIA tree entirely.
  - JSON-LD structured data emission should be delegated to the application framework's SEO metadata layer, not baked directly into the UI component DOM tree.

composition:
  inherits: Link (for base interactions and polymorphism), Menu/Popover (for overflow state).

notes:
  - "Path-based (browser history) breadcrumbs are a strict anti-pattern; use exclusively for location-based architecture."
  - "Apple HIG mandates native back-buttons over desktop-style breadcrumb trails for mobile viewports."
  - "The active crumb methodology remains split; Link + aria-current='page' is the modern polymorphic preference over static span text."
```
