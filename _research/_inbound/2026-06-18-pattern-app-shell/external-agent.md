# App shell — external-agent pass

*Second independent pass for the App shell pattern brief (first `layout-and-shell` tier). Captured as the dual-agent audit record. Synthesised with `claude.md` into `patterns/app-shell.md`.*

---

## App shell

The application shell is the persistent, omnipresent frame that surrounds, anchors, and orchestrates the user's primary content and tasks. It is the architectural substrate of the digital experience, bearing global orientation, system-level navigation, and structural consistency. The shell is not the journey itself, but the vessel through which all journeys are navigated. It isolates global persistence from local volatility.

### Problem and context

The landscape demands applications that feel cohesive and familiar regardless of IA complexity. The recurring problem: a universal structural container that accommodates shallow marketing pages, deep master-detail views, and data-dense dashboards without forcing users to re-learn navigation at every juncture. The shell codifies the boundary between what persists across route changes and what is ephemeral. Systems diverge from the tension between maximizing content real estate and maximizing navigation discoverability. Critically, the MPA→SPA/PWA shift broke native browser orientation: full reloads used to reset scroll, update the title, and alert screen readers; in SPAs content swaps inside a persistent shell, rendering native accessibility/history inert unless the shell actively reconstructs those contracts.

### Composition

A structural archetype, not a composition recipe. The shell assembles conceptual components into fixed regions — header, primary/secondary navigation, main content, the semantic landmark skeleton — and dictates where they reside, how they scale, and when they hide/reveal. Typed references: Side Navigation / Navigation Drawer; the Global Search Slot (invokes the search pattern); User Menu / Avatar (account, auth state, workspace switchers); Brand/Logo (route-to-home anchor); Skip-to-Content Link (visually hidden, keyboard-focusable). Boundary: the shell owns the slot, grid placement, and responsive collapse; components own their internal anatomy, active routing states, nested logic, and localized ARIA. Re-deriving Side Navigation internals inside the shell is a critical anti-pattern.

### Decision rules

- **Top nav** IF shallow hierarchy (<5 top-level) and content/editorial immersion. **Side nav** IF complex SaaS/enterprise with deep hierarchy or >5 destinations (left-aligned LTR). **Hybrid** IF navigating between distinct products while maintaining deep intra-product nav (global header for cross-product switching + local side nav).
- **Header zones:** Brand/Identity leading, Global Search center, System Utilities trailing.
- **Side-nav states:** collapsed icon rail expanding to a full drawer on hover (flyout) or explicit toggle when space is constrained.
- **Responsive collapse** (<1024px): collapse side nav into a temporary overlay drawer via a hamburger trigger in the header.
- **Mobile paradigm:** IF strictly task-oriented with 3–5 peer destinations → bottom navigation bar rather than a hamburger.
- **Contextual overflow:** IF top nav exceeds horizontal space → Priority+ (reveal as many as fit, tuck the rest into "More").
- **Scroll persistence:** fixed global header + fixed side nav; only the main content scrolls.
- **Multi-product switcher:** a waffle icon at the far-left or far-right of the global header, separated from local routing.

### Layout and structure (heavy)

**Region model:** container spans 100vw/100vh, locking the frame to the screen. Standard enterprise model: permanent global header fixed to top; below it, side nav (leading edge) + main content. **A genuine divergence on header/side-nav overlap:** IBM Carbon's UI Shell spans the header full width and places left/right panels strictly *below* it (header supremacy / brand umbrella); Material 3's expressive update often lets the navigation rail occupy the full leading-edge height with the top app bar adjacent within the content pane (ergonomic access over brand dominance). Defensible default for multi-product ecosystems: the full-width global header, physically capping the application.

**Header zone model:** leading (hamburger trigger when collapsed, brand mark, app title; on macOS Spectrum must accommodate the native traffic-light window controls, pushing brand inward); center (global search / command palette / brief top nav; if nav absent, search expands into the negative space for a larger target); trailing (notifications, help, environment indicators, multi-product switcher, avatar/account). Rigid separation supports cross-app muscle memory.

**Grid & scroll persistence — two models (Carbon delineates):** the *editorial model* centers the grid and caps main content to a max-width (e.g., 1440px) for readability, growing margins on ultra-wide; the *high-density product model* uses full browser width, pinning the side nav left and expanding the content grid (or adding columns) for data tables/dashboards. Persistence: header and side nav `position: fixed`/`sticky`; main content is an independent vertically-scrollable container. Letting the global header scroll away is reserved for immersive marketing pages — a severe anti-pattern in functional apps.

**Responsive transformation (shedding sequence):** at the tablet breakpoint (<1024px) persistent side nav collapses to a narrow icon rail or disappears behind a toggle; the header gains a hamburger in the leading zone. At the mobile breakpoint (<768px) the header sheds hard: logo → icon-only mark; global search → a magnifying-glass icon triggering a full-screen search modal; trailing utilities → a consolidated overflow, keeping only avatar + notifications. With 3–5 core destinations, the bottom navigation bar (thumb-zone ergonomics) beats a multi-layered hamburger drawer.

### Accessibility orchestration

**Landmarks:** header in `banner`/`<header>`, content in `main`/`<main>`, footer in `contentinfo`/`<footer>`. **Multiple navs:** the W3C APG mandates each `navigation` landmark get a unique accessible name via `aria-label` — top as `"Global"`/`"Primary"`, side as `"Secondary"`/`"Product"` — or landmark-rotor tools become useless.

**Skip-link contract (WCAG 2.4.1):** the "Skip to main content" link must be the very first focusable element in the DOM, visually hidden via clipping until focused. Its `href` targets the main container's `id`, and that container **must have `tabindex="-1"`** — without it, browsers may fail to move programmatic focus and the next Tab jumps back to the top, nullifying the skip link.

**SPA route-change contract (the single most destructive failure):** in MPAs a hard reload reset focus and announced the new `<title>`; in SPAs the router swaps `main` while the shell persists, so the browser doesn't reset focus and the screen reader stays silent (or focus is orphaned on an unmounted node). The three-part fix: (1) update `document.title` on route resolution; (2) move keyboard focus into the new view — the prevailing standard is the incoming `<h1>` (equipped with `tabindex="-1"`, focused via `.focus()`), or the main container if there's no unique heading; (3) manage scroll manually — `history.scrollRestoration = 'manual'`, reset main scroll to zero on forward navigation, restore via router cache on back.

### Flow and states (light)

Side-nav expand/collapse (smooth width animation, no jarring reflow). Mobile: the side nav becomes a modal drawer (slide-in over a scrim) with a strict focus trap — keyboard users cannot tab into the obscured background; focus cycles within the drawer until close/Escape, then returns to the hamburger trigger.

### Content and copy

Skip link: "Skip to main content" (avoid verbose "Click here to skip navigation"). Primary nav aria-label: "Global"/"Primary" (don't append "navigation" — the role already announces it). Hamburger: "Open main menu". Environment banner: "Staging"/"Sandbox" (unambiguous, persistent, prevents accidental production actions).

### Variants and responsive

Top-Nav shell (marketing/e-commerce/portals; Priority+ overflow). Side-Nav shell (complex apps/dashboards; deep nesting, F-pattern scanning, user-configurable menus). Hybrid shell (top global header for cross-product + side nav for the current app — Atlassian, Carbon). Bottom-nav variant for consumer mobile with limited peer destinations.

### Anti-patterns

Desktop hamburger (hides nav, raises interaction cost where space allows). Missing skip link (manual tabbing through dozens of nav links each route). Silent SPA transition (no focus/title management). Landmark soup (nested nav/header without unique aria-labels). Viewport-eating sticky header on mobile (must be minimal or scroll-linked to hide on scroll-down, reveal on scroll-up). Reflowing navigations (nested accordions jumping instead of animating height).

### Related patterns and components

Side Navigation component (shell dictates width/responsiveness/grid; component owns internal anatomy, `aria-current`, nested logic). Page Templates (master-detail, dashboards, settings — inside the main content region). Search Orchestration (header provides the slot; the pattern owns predictive typing, overlay, filtering). Breadcrumbs/Tabs (in-page secondary nav, inside the template). Navigation IA (the strategy of what destinations exist — a content/discovery discipline, not the frame).

### Field POV evolution

Top nav (low-res monitors, vertical-space scarcity) → side nav as widescreen made vertical scroll effectively infinite and horizontal space the constraint (deeper hierarchies, F-pattern, no unwieldy mega-menus). The mobile era's hamburger became an omnipresent lazy solution; an engagement-metrics backlash ("out of sight, out of mind") drove bottom navigation for mobile, restricting hamburgers to overflow/complex enterprise mobile. Most recently, the SPA accessibility reckoning: frameworks long prioritized seamless visual transitions at the expense of AT users; the mature standard now mandates manually reconstructing focus, live regions, and scroll restoration on route change. Material 3 embraced fully adaptive navigation (bar → rail → drawer across breakpoints). (Verification state: June 2026.)

### Reference instantiations

IBM Carbon (UI Shell: distinct Header/Left/Right panels; full-width header caps everything; trailing-zone product switcher). Atlassian (slot-based Page Layout: Banner, TopNavigation, LeftSidebar, Main; resizable side nav / icon rail). Material Design 3 (the adaptive bar→rail→drawer matrix — the gold standard for consumer-facing adaptive shells). Shopify Polaris (Frame wraps the merchant admin; separates persistent TopBar + Navigation from App Bridge iframe content). GOV.UK (strict top-nav; separates the global GOV.UK header from the Service navigation). Adobe Spectrum (OS-level window controls in the header for PWA/Electron). Microsoft Fluent (declarative area-based structural backbones handling hamburger/panel collapse without custom JS).

### Agent-consumable schema (external pass)

```yaml
id: app-shell
name: App shell
aliases: [global header, frame, ui shell, application layout, masthead]
tier: layout-and-shell
goal: navigate
status: stable
problem: >
  SPAs and complex platforms require a persistent, predictable architectural frame to house global navigation,
  orientation markers, and system utilities. Without a standardized shell, users lose spatial bearing during deep
  navigation, and SPAs fail to announce routing changes to assistive technologies.
composition:
  requires: [global-header, side-navigation-component, skip-to-content-link, user-avatar-menu]
  optional: [search-orchestration, multi-product-switcher]
decision_rules:
  - { if: "shallow hierarchy (<5 destinations), immersive content", use: "horizontal top navigation" }
  - { if: "complex data-dense tool with deep hierarchy", use: "persistent side navigation" }
  - { if: "multiple separate products", use: "hybrid: global header cross-product switch + side nav local routing" }
  - { if: "horizontal space cannot fit all top-nav items", use: "Priority+ overflow into a More dropdown" }
  - { if: "mobile (<768px) and 3-5 core destinations", use: "bottom navigation bar rather than hamburger" }
layout:
  region_model: "100vw/100vh locked grid. Header spans top, side nav spans left, main scrolls."
  zone_model: { leading: "identity, brand, nav triggers", center: "global routing, search", trailing: "utilities, notifications, profile, switchers" }
  responsive_transformation: "Desktop (side nav) -> Tablet (icon rail/toggle) -> Mobile (bottom nav or hamburger modal drawer)"
  persistence: "header + side nav fixed; main scrolls independently"
accessibility_orchestration:
  landmarks: "banner / navigation / main"
  multiple_nav_labels: "unique aria-labels (Primary vs Secondary)"
  skip_link: "first focusable node; target has tabindex=-1"
  spa_route_contract:
    focus_management: "shift focus to incoming <h1> (tabindex=-1) or main container"
    title_announcement: "update document.title every route resolution"
    scroll_restoration: "history.scrollRestoration='manual' to prevent layout jumping"
flow:
  - { trigger: "collapse toggle", action: "expanded list -> icon rail" }
  - { trigger: "mobile hamburger", action: "modal overlay drawer + scrim + focus trap" }
content:
  skip_link: "Skip to main content"
  aria_labels: "avoid redundancy; 'Primary' not 'Primary navigation'"
variants: [top_nav_shell, side_nav_shell, hybrid_shell]
anti_patterns:
  - "desktop hamburger hiding primary nav"
  - "no focus move on SPA route change"
  - "orphaned/redundant ARIA landmarks"
  - "sticky headers eating mobile viewport"
relations:
  composes: [header, navigation-rail, skip-link]
  boundary: [side-navigation-component, page-templates, search-orchestration, breadcrumb]
notes:
  contested: "header vs side-nav overlap (Carbon full-width header; Material allows side nav to reach top edge)"
```
