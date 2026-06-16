---
okf_version: "0.1"
type: component-brief
title: Breadcrumbs
description: The first Navigation brief built directly on Link — a trail of ancestor Links ending at the current page, wrapped in the APG nav[aria-label]+ol/li landmark contract. A field-truth study of the structure contract, the contested current-crumb (text-with-aria-current=page vs interactive-link), the decorative-separator rule (CSS pseudo-element, never DOM content), the truncation/overflow collapse model (keep root + current, middle into an ellipsis menu), the mobile back-up-one-level swap, and the SEO BreadcrumbList structured-data question — with the practice's defaults.
tags: [components, navigation]
category: Navigation
status: stable
aliases: [breadcrumb, breadcrumb-trail, crumb]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Breadcrumbs

> Breadcrumbs are the first Navigation brief that stands directly on another component: a crumb *is* a Link (see link — the `<a href>` contract, the underline discipline, the `asChild` router polymorphism all inherit unchanged). What Breadcrumbs add is the **structure** (a labelled `<nav>` landmark wrapping an ordered list), the **current-page marking** (`aria-current="page"`), the **decorative separators** (CSS, never DOM content), and the **overflow/collapse** model for deep trails. The whole component is a *secondary* wayfinding aid — it shows where you are in the hierarchy and offers an escape hatch up the tree. It never replaces the primary nav, never tracks history (that's a back button), never sequences a flow (that's a Stepper), and never segments peers (that's Tabs). Modern practice has settled the big ontological question — breadcrumbs map the **permanent location hierarchy**, not the user's click path — and now disagrees only on the mechanics: the current crumb, the separator rendering, the overflow maths, and who emits the SEO structured data.

---

## 1. Framing

A Breadcrumb trail reveals the current page's position in a site/app's information architecture as a single line of ancestor Links ending at the current page. What it *isn't*: **primary navigation** (breadcrumbs supplement the global nav/sidebar; they are never the sole way to move — they participate in SC 2.4.5's "multiple ways"), a **back button** (history is linear and session-dependent; a breadcrumb is hierarchical and stable — §5), **Tabs** (peer views at the *same* level, not ancestors — see tabs), or a **Stepper/Wizard** (ordered steps with completion state in a linear flow — see stepper when briefed).

The settled ontology: breadcrumbs are **location-based**, mapping the permanent taxonomy (Home › Electronics › Audio › Headphones), **not path-based** (the historical click trail). Path/attribute breadcrumbs are a purged anti-pattern — they duplicate browser history, disorient users who arrive by deep link, and break the predictability of a stable tree. Both research passes converged on this without reservation.

Why systems still disagree, mechanically: the **current/last crumb** (interactive link vs. static text), the **separator** rendering (DOM element vs. CSS pseudo-element), the **overflow/truncation** maths for deep trails, the **mobile** swap, and whether the design system **emits JSON-LD structured data**.

## 2. Anatomy and parts

The structure is rigorously fixed by the WAI-ARIA APG breadcrumb pattern — the component is built from semantic primitives in a strict nesting:

- **`<nav aria-label="Breadcrumb">`** — the outermost element; a discrete navigation **landmark** that *must* carry an accessible name (§6). Without it a screen-reader landmark list announces only "navigation," indistinguishable from the global/footer/TOC navs on the same page.
- **`<ol>`** — an **ordered** list, because the crumbs are a meaningful sequence (root → … → current). The `<ol>`/`<li>` is what lets AT announce "list, N items" and the user's position within it; a flat row of `<span>`/`<div>` strips that and fails SC 1.3.1.
- **`<li>`** — the crumb wrapper.
- **crumb** — a **Link** (`<a href>` to an ancestor), inheriting link entirely (underline discipline, focus ring, `asChild` router polymorphism — see link).
- **separator** (`/`, `›`, chevron) — **decorative, never DOM content** and never its own list item; rendered via CSS `::before`/`::after` (preferred) or, if a physical element is unavoidable, `aria-hidden="true"` (§6, §11).
- **overflow affordance** — when the trail outruns its space: a real `<button>` (ellipsis `…`) with `aria-haspopup`/`aria-expanded`, opening a Menu of the collapsed middle crumbs (§6, see menu).
- **current marker** — the final crumb (the active page), `aria-current="page"`, by default non-interactive text (§4).
- **home/root crumb** — optionally a house icon instead of "Home"; either way it needs an accessible name (§7).

## 3. Properties / API

Two API shapes appear in the field: a **data-driven** `items` array (`{label, href}` objects the component maps and auto-separates — MUI, Material) and **composed children** (`<Breadcrumbs><BreadcrumbItem href>…</BreadcrumbItem></Breadcrumbs>` — React Aria, Carbon, Primer — the component injects separators between slots). Headless libraries support both. **The practice default mirrors the text-field encapsulation POV: composed `BreadcrumbItem` children for control, with a convenience `items` prop for the common data-driven case** — each crumb inherits link's `asChild` so it can render a framework-router Link (§11).

- **`items` / `children`** — the crumbs (typed `BreadcrumbItem` children, or a data array).
- **`maxItems`** — the count threshold that triggers middle-collapse (Atlassian defaults to 8). Above it, the trail collapses (§4).
- **`itemsBeforeCollapse`** — root crumbs kept before the ellipsis (default 1).
- **`itemsAfterCollapse`** — current/parent crumbs kept after the ellipsis (default 1–2).
- **`separator`** — token/glyph or render-slot; default a chevron (`›`) or slash (`/`). Decorative regardless of how it's passed (§6); **restrict overrides to system-approved glyphs/icons** to prevent layout breakage and rogue branding.
- **`overflow`** — Primer's `'wrap' | 'menu' | 'menu-with-root'`: wrap onto a second line, collapse into a menu, or collapse keeping the root visible. The practice exposes a collapse strategy in this spirit, defaulting to the menu form.
- **current-crumb handling** — the component auto-marks the **last** crumb `aria-current="page"` and renders it non-interactive by default (§4, §6); the consumer doesn't hand-wire it.
- **router integration** — inherits link's `asChild`/`as` per crumb (§11).

## 4. States and variants

Crumb interaction states **inherit Link** (rest / hover / focus-visible / active — see link). Breadcrumbs add macro-level structural states driven by depth and viewport.

**The current-crumb decision (the live fork).** The field splits two ways:

- **Static text + `aria-current="page"` (IBM Carbon, Base Web).** The current page is rendered as a non-interactive `<span>`/text inside the `<li>`, removed from the tab order, carrying `aria-current="page"`. Rationale: a crumb's entire contract is "navigate to an ancestor"; the current page is neither an ancestor nor a destination, so a self-referential link is a minor anti-pattern (it violates the anchor expectation, and `Cmd/Ctrl-R` already reloads).
- **Interactive link + `aria-current="page"` (React Aria, Primer).** Every crumb including the last is an `<a>`, visually de-emphasised (weight/colour, underline removed) and `aria-current="page"`. Rationale: a uniform focusable DOM tree and a uniform polymorphic API (every node is a Link).

**The practice default: non-interactive text carrying `aria-current="page"`, auto-derived by the component from last position.** The link-form's headline argument — API uniformity under polymorphic routing — doesn't actually force the link: the component still accepts a uniform `items`/children list and simply *renders* the final one as text, so the consumer's API stays uniform while the output stays semantically honest. Both forms are WCAG-conformant; this remains a genuinely contested decision (flagged in §15), and the link-form is a defensible house style for teams that prize a uniform node tree.

**Variants:** **default** (full trail) / **collapsed/overflow** (middle crumbs behind a `…` button → Menu, the trigger bound to `aria-expanded`) / **with-home-icon** (root as a house icon) / **condensed/mobile** (see §5 — typically a single "‹ Parent" back-up-one-level crumb). Breadcrumbs are usually one small text size; size tracks the type ramp.

## 5. Usage guidance

- **Use** for a **deep (3+ level) hierarchy** the user navigates into and needs to climb back out of — e-commerce taxonomies, nested admin dashboards/ERP, deep documentation trees, file systems — where the global/secondary nav can't by itself say "where am I."
- **Don't use** for: **flat architectures** (1–2 levels — a back link or persistent nav suffices), **primary navigation** (breadcrumbs are a supplement), **linear flows** (→ Stepper/Progress Indicator — breadcrumbs are static structure, not chronological progress), or **peer content** (→ Tabs).
- **Decision frameworks:**
  - **Breadcrumb vs. back button:** breadcrumb = *hierarchy* (stable, structural, "up to parent"); back = *history* (linear, session-dependent, "previous page"). On mobile a single "‹ Parent" crumb is still hierarchical (it goes *up*, not *back*) even though it resembles a back chevron. (Polaris has historically blurred this — its `Page` back-arrow behaves like a single-level breadcrumb and can read as redundant beside real back navigation.)
  - **Breadcrumb vs. tabs vs. stepper:** ancestors → breadcrumb; peers at one level → tabs; ordered steps with progress → stepper. They sit on perpendicular axes of the IA; don't conflate them.
  - **Mobile is a contextual swap, not a shrink.** Full horizontal trails fail on narrow viewports, and Apple HIG / Material favour a back chevron or top app bar natively. Below the breakpoint, collapse to a single "‹ Parent" (penultimate-node) link via a container/media query rather than wrapping or horizontal scroll.

## 6. Accessibility

Breadcrumbs participate directly in **SC 2.4.8 Location (AAA)** and **1.3.1 Info & Relationships (A)**, plus all of Link's SCs per crumb.

- **The landmark + list contract:** `<nav aria-label="Breadcrumb">` → `<ol>` → `<li>` → crumb Link. The `aria-label` (singular "Breadcrumb"; AT appends "navigation," so don't include the word) is the only thing that distinguishes this landmark from the global/sidebar/footer/TOC navs on a complex page. The `<ol>`/`<li>` announces count and position.
- **`aria-current` on the current crumb: `page`, not `location`.** `aria-current="page"` is the APG breadcrumb value — the current crumb *is* the current page. `location` is reserved for a current position *within a container/environment* (a visual highlight), not document-level nav, and is the most-confused breadcrumb a11y detail. Whether the current crumb is text or a link (§4), it carries `aria-current="page"` so AT announces "current page."
- **Decorative separators are inert to AT.** Render via CSS `::before`/`::after` on the `<li>` (preferred — never enters the a11y tree or inflates the list count), or if a physical `<svg>`/icon element is unavoidable, mark it `aria-hidden="true"` + `focusable="false"`. A separator as text content of a list item makes AT halt to read "slash" / "right angle bracket" between every crumb — severe, recurring noise.
- **Overflow-menu a11y:** the `…` is a real `<button>` with `aria-haspopup="menu"` + a dynamic `aria-expanded`, and a descriptive accessible name overriding the ellipsis ("Show path" / "More breadcrumbs" / "Show N more"). The menu follows the APG Menu pattern — arrow-key navigation between collapsed links, `Escape` closes and returns focus to the trigger.
- **WCAG SCs:** **2.4.8** (Location — breadcrumbs satisfy it directly), **2.4.5** (Multiple Ways — breadcrumbs are one of the required "ways"), **1.3.1** (the nav/list structure), **4.1.2** (name/role/value), plus link's per-crumb set (1.4.1 underline/contrast, 2.4.4 link purpose).

## 7. Content guidelines

- **Concise crumb labels that match the destination's page title (`<h1>`)** so the user trusts the choice; keep them short — the trail is one line. Don't restate the hierarchy in each label.
- **Trail-collapse over label-truncation.** When space runs out, collapse a whole node into the overflow menu rather than CSS-truncating a single label (per-label truncation forces the user to guess the destination). If a single dynamic string *must* be truncated (e.g. a user-uploaded filename), attach an accessible **Tooltip** exposing the full text on hover *and* keyboard focus.
- **The home/root crumb** is the app/site root (dashboard or homepage), labelled "Home" or a house icon. Icon-only ⇒ the `<a>` needs `aria-label="Home"`. Icon **and** text ("🏠 Home") ⇒ mark the `<svg>` `aria-hidden="true"` so AT doesn't announce "Home, Home, link."
- **The current page is a location, not a verb** — never phrase it as an action.

## 8. Motion and transition

Minimal — breadcrumbs are a static utility. The only motion is the **overflow menu** open/close: a fast ~100–150ms opacity fade with a slight (~4px) translate / 0.95→1.0 scale (see menu/popover). Latency or bouncy easing on a wayfinding utility creates friction. Crumb hover may animate an underline (inherits link). Under `prefers-reduced-motion: reduce`, the menu snaps open with no transition. No trail animation. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL flips both order and glyph.** The trail reverses (root on the right, flowing left) — achieved cleanly with Flexbox + logical properties (`margin-inline-start`). A symmetrical `/` needs no mirroring, but an **asymmetrical chevron (`›`) must flip to point left (`‹`)** — via `transform: scaleX(-1)` bound to `[dir=rtl]` or a swapped SVG asset. This is the headline i18n trap: handle separators with logical/mirroring CSS, not a hardcoded glyph.
- **Text expansion** (de/ru/fi +30–50%) means a five-crumb English trail may fit only three before overflowing; the collapse logic (count threshold or a `ResizeObserver` width measure) must recalculate safely and never force multi-line wrapping.
- **Localised strings** — "Home," the overflow "Show more," and the nav `aria-label` ("Breadcrumb") all localise. (See 13-internationalization-and-rtl.)

## 10. Naming

**`Breadcrumbs`** (plural container) wrapping **`BreadcrumbItem`** (the crumb, which *is* a Link via `asChild`) is the dominant pairing (React Aria `Breadcrumbs`/`Breadcrumb`, Carbon `Breadcrumb`/`BreadcrumbItem`, MUI `Breadcrumbs`); modern React favours dot-notation (`Breadcrumbs.Item`) to keep imports tidy. **The practice default: `Breadcrumbs` / `BreadcrumbItem`.** Naming the child singular `Breadcrumb` is an anti-pattern — it muddies whether an import is the wrapper or a node. Aliases to map: `Breadcrumb`, `BreadcrumbList`, `Crumb`, `BreadcrumbTrail`.

## 11. Implementation notes

- **Separators via CSS, not the DOM** — `li:not(:last-child)::after { content: '/'; pointer-events: none; user-select: none; }` (or a `background`/`mask` SVG), so the separator never pollutes the virtual DOM, the a11y tree, or the list count. The cardinal breadcrumb implementation rule. If multi-colour styling forces a physical `<svg>`, hide it (`aria-hidden="true"` + `focusable="false"`).
- **Overflow-collapse logic** — above `maxItems`, keep `itemsBeforeCollapse` root crumbs + `itemsAfterCollapse` current/parent crumbs, route the middle slice into a `…` button + Menu. Collapse by **count** (deterministic, simple — the practice default) or by **available width** (a `ResizeObserver`-driven responsive collapse — more correct, more complex; offer as an enhancement). The invariant: root (Home) and current always stay visible.
- **Router integration** — each crumb inherits link's `asChild`/Slot so it renders a framework-router Link (Next.js/React Router/TanStack) while emitting a real `<a href>`; the design system owns the `<nav>`/`<ol>`/`<li>`/separator/`aria-current` and stays router-agnostic (see link §11).
- **SEO / structured data — the component does *not* emit JSON-LD.** `schema.org` `BreadcrumbList` (an array of `ListItem`s, each with `@id`/`name`/`position`) drives Google's breadcrumb rich-result, but baking the `<script type="application/ld+json">` into the visual component is wrong on three counts: in SSR frameworks (Next.js/Nuxt) SEO metadata is generated in the server `<head>`/metadata API before the component tree renders (duplicate scripts, hydration mismatch); a client-rendered script is unparseable if JS fails; and a breadcrumb hidden on mobile via `display:none` can carry its JSON-LD into a hidden subtree and risk de-indexing the path. **The practice ships accessible, semantic HTML and delegates JSON-LD to the app's page-level/SEO layer — documenting the pattern and offering an optional opt-in emitter, never a silent default.**
- **Headless vs. opinionated** — React Aria provides headless `Breadcrumbs`/`useBreadcrumbs` (the landmark/list/`aria-current` wiring, no style); the practice skins that rather than hand-rolling the contract.

## 12. Related and alternative components

- **Composes with:** Link (each crumb — the substrate; see link), the `<nav>` landmark, Icon (home icon, separator chevron, overflow ellipsis — see icon), Menu (the overflow/collapse popover, with focus management — see menu), the page header/title (breadcrumbs commonly sit above the `<h1>`).
- **Alternative to:** Tabs (peer views, not ancestors — see tabs), Stepper/Progress Indicator (linear ordered flow — see stepper when briefed), a back button (history, not hierarchy; favoured natively on mobile — Apple HIG, Material), the primary nav (breadcrumbs supplement it).
- **Supersedes:** a `<div>` of slash-separated `<a>`s with the separator as text content (the recurring anti-pattern — fails the list count and reads the slash); path/history-based breadcrumbs.
- **Superseded by:** Tabs/Stepper when the relationship is peer/linear rather than hierarchical; nothing within the wayfinding-hierarchy lane.

(The first Navigation brief built directly on another component — a trail of Links + `aria-current="page"` inside the APG nav/ol/li landmark. Closes the "where am I in the hierarchy" lane against Tabs (peers) and Stepper (linear). See link for the crumb substrate and the `asChild` router polymorphism, tabs and segmented-control for the routing-vs-tablist rule, icon for the separator/home glyphs, 03-component-library; 29 for the docs template. Menu is the adjacent Navigation brief the overflow affordance will lean on.)

## 13. Field POV evolution

1. **Path-based → location-based.** Breadcrumbs as a visual echo of browser history disoriented deep-link arrivals and broke the site's mental model; the field has fully standardised on the permanent location hierarchy.
2. **`<nav aria-label>` + `<ol>`/`<li>` standardised** as the APG structure — the bare `<div>` of links is now a clear anti-pattern.
3. **Wrapping → truncation.** Letting a long trail wrap to a second line (destroying vertical rhythm) gave way to strict single-line layout with a calculated overflow menu for the middle nodes, plus the mobile single-parent "back-up" swap.
4. **Decorative-separator discipline hardened** — separators moved out of the DOM into CSS pseudo-elements / `aria-hidden`, so they stop polluting the list count and AT output.
5. **`aria-current="page"`** settled as the current-crumb signal (over `location` and over nothing), aligning with Link's nav-current idiom.
6. **Separation of concerns on SEO** — JSON-LD `BreadcrumbList` is increasingly treated as an app/SSR-metadata concern (opt-in), not a default component side effect.

## 14. Sources cited

Conservative dating (the external pass cited React Aria v3.5.32, Atlassian v16.1.1, Base Web v18.1.0, Carbon v11, Primer, Polaris v12/13 — all stamped "2026"; held loosely and flagged unverified; `last-audited` is the re-run trigger):

- WAI-ARIA APG — the **Breadcrumb pattern** (`nav[aria-label="Breadcrumb"]` + `ol`/`li` + `aria-current="page"`, decorative separators) (APG, 2024–2026).
- Adobe Spectrum / React Aria — `Breadcrumbs`/`Breadcrumb` + `useBreadcrumbs` (headless landmark/list/`aria-current`; the interactive-current-crumb form) (2024–2026).
- IBM Carbon — `Breadcrumb`/`BreadcrumbItem`, the **static-text current crumb**, the overflow menu (2024–2026).
- GitHub Primer — `Breadcrumbs`, the interactive-current-crumb form, the `overflow` `wrap`/`menu`/`menu-with-root` strategies (2024–2026).
- Atlassian Design System — `Breadcrumbs`, `maxItems`/`itemsBeforeCollapse`/`itemsAfterCollapse`, `defaultExpanded`/`onExpand` (2024–2026).
- Uber Base Web — `Breadcrumbs`, the static-text current crumb (2024–2026).
- Shopify Polaris — the `Page` `breadcrumb`/back-action model (and its back-button blur) (2024–2026).
- Google Material 3 / Apple HIG — the mobile back-chevron / top-app-bar preference over desktop breadcrumb trails (2024–2026).
- MUI — `Breadcrumbs` (`maxItems`/`itemsBeforeCollapse`/`itemsAfterCollapse`, collapse) (2024–2026).
- schema.org `BreadcrumbList` + Google Search Central breadcrumb structured-data docs.
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 2.4.8, 2.4.5, 1.3.1, 4.1.2, plus Link's set (1.4.1, 2.4.4).

## 15. Agent-consumable schema

```yaml
identity:
  id: breadcrumbs
  name: Breadcrumbs
  aliases: [breadcrumb, breadcrumb-trail, crumb, breadcrumb-list]
  category: navigation
  status: stable
description: >
  A secondary wayfinding trail showing the current page's location in the
  IA — a set of ancestor Links inside a nav[aria-label]+ol/li landmark,
  ending at the current page (aria-current=page). Location-based (the
  permanent taxonomy), NOT path-based (click history — an anti-pattern).
  Not primary nav, not a back button (history), not Tabs (peers), not a
  Stepper (linear flow). Each crumb inherits Link.
anatomy:
  structure: "nav[aria-label='Breadcrumb'] > ol > li > crumb(Link)"
  parts:
    - "nav landmark (REQUIRES accessible name — else 'navigation' is ambiguous)"
    - "ol (ordered — announces count + position; flat span/div fails 1.3.1)"
    - "li (crumb wrapper)"
    - "crumb = Link (a href to an ancestor; inherits link)"
    - "separator (DECORATIVE — CSS ::before/::after preferred, else aria-hidden; never DOM content / never a list item)"
    - "overflow affordance (real <button> ellipsis + aria-haspopup/aria-expanded -> Menu of collapsed crumbs)"
    - "current marker (final crumb; aria-current=page; non-interactive text by default)"
    - "home/root crumb (house icon or 'Home'; needs accessible name)"
api:
  inherits: link   # per crumb — <a href> contract, underline discipline, asChild router polymorphism
  shape: "composed BreadcrumbItem children (practice default) + convenience items[] data array"
  props:
    - {name: items/children, type: "BreadcrumbItem[] | {label,href}[]", description: the crumbs}
    - {name: maxItems, type: number, default: 8, description: count threshold that triggers middle-collapse}
    - {name: itemsBeforeCollapse, type: number, default: 1, description: root crumbs kept before the ellipsis}
    - {name: itemsAfterCollapse, type: number, default: "1–2", description: current/parent crumbs kept after the ellipsis}
    - {name: separator, type: "ReactNode | string", default: "'›' or '/'", description: "decorative; restrict overrides to approved glyphs"}
    - {name: overflow, type: enum, values: [wrap, menu, menu-with-root], default: menu, description: "Primer-style responsive strategy"}
    - {name: current-crumb, type: auto, description: "component auto-marks LAST crumb aria-current=page + renders non-interactive (consumer doesn't hand-wire)"}
    - {name: asChild/as, type: "boolean/elementType", description: "router polymorphism per crumb (inherits link)"}
states:
  inherits: link   # rest / hover / focus-visible / active, per crumb
  runtime:
    - "current: final crumb; aria-current=page; NON-INTERACTIVE TEXT by default (practice) — interactive-link form is the contested alternative"
    - "collapsed/overflow: middle crumbs behind a … button (aria-expanded) -> Menu"
variants:
  default: "full single-line trail"
  collapsed: "middle crumbs in an overflow menu (maxItems exceeded)"
  with-home-icon: "root = house icon (needs aria-label='Home')"
  condensed/mobile: "below breakpoint, swap to a single '‹ Parent' back-up-one-level link (container/media query)"
accessibility:
  wcag-criteria: ["2.4.8", "2.4.5", "1.3.1", "4.1.2", "1.4.1", "2.4.4"]   # last two via inherited Link
  landmark: "nav[aria-label='Breadcrumb'] (singular; AT appends 'navigation') — the only way to disambiguate from other navs"
  list-semantics: "ol/li announces count + position; flat span/div fails 1.3.1"
  current-marker: "aria-current=PAGE — NOT location (location = within-container highlight, not document nav); the most-confused detail"
  separators: "inert to AT — CSS ::before/::after (preferred) or aria-hidden+focusable=false; never text content (else 'slash' read between every crumb)"
  overflow-menu: "real <button> + aria-haspopup=menu + aria-expanded + descriptive name ('Show N more'); APG Menu — arrow-key, Escape returns focus to trigger"
content:
  labels: "concise, match the destination <h1>; don't restate the hierarchy"
  truncation: "trail-collapse (whole node into menu) over per-label CSS truncation; if a dynamic label must truncate, Tooltip on hover AND focus"
  home: "'Home' or house icon; icon-only => aria-label='Home'; icon+text => svg aria-hidden (avoid 'Home, Home')"
  current: "a location, not a verb"
motion:
  menu: "~100–150ms opacity fade + ~4px translate / 0.95->1.0 on overflow open"
  reduce-motion: "snap open, no transition"
  none: "no trail animation; crumb hover underline inherits link"
i18n:
  inherits: link
  rtl: "order flips (root right) via flex + logical props; asymmetrical chevron › must mirror to ‹ (scaleX(-1) on [dir=rtl] or swapped SVG); '/' is neutral"
  expansion: "de/ru/fi +30–50% — collapse logic must recalculate safely; never force multi-line wrap"
  localise: "'Home', overflow 'Show more', nav aria-label 'Breadcrumb'"
implementation:
  - "separators via CSS ::after (pointer-events/user-select:none), NOT the DOM — never touches the a11y tree or list count; physical svg => aria-hidden+focusable=false"
  - "overflow: above maxItems keep itemsBeforeCollapse root + itemsAfterCollapse current/parent, middle slice -> … button + Menu; count-based default, width-based (ResizeObserver) as enhancement; root + current always visible"
  - "router-agnostic: each crumb inherits link's asChild/Slot -> framework-router Link emitting a real <a href>; DS owns nav/ol/li/separator/aria-current"
  - "JSON-LD BreadcrumbList: component does NOT emit it — delegate to the app SSR/metadata layer (avoid duplicate scripts, hydration mismatch, hidden-subtree de-index); document + optional opt-in emitter, never silent default"
  - "skin headless useBreadcrumbs rather than hand-rolling the landmark/list/aria-current contract"
composition:
  composes-with: [link, nav-landmark, icon, menu, page-header]
  alternative-to: [tabs, stepper, back-button, primary-nav]
  supersedes: ["div-of-slash-separated-anchors (separator as text content)", "path/history-based breadcrumbs"]
  superseded-by: [tabs (peers), stepper (linear flow)]
notes:
  contested:
    - "current crumb: non-interactive TEXT + aria-current=page (practice default; Carbon/Base Web) vs interactive LINK + aria-current=page (React Aria/Primer — uniform node tree)"
    - "overflow collapse: count-based (default) vs width-based ResizeObserver"
    - "JSON-LD ownership: app/SSR layer (practice) vs component-emitted"
    - "mobile: collapse-to-menu vs swap-to-single-parent-back-link"
  inherited: "all of link per crumb — <a href> contract, underline discipline, asChild router polymorphism, Enter-not-Space, the no-href anti-pattern"
  trap:
    - "aria-current=location instead of page on the current crumb"
    - "separator as DOM/list-item content (read by AT, inflates the count)"
    - "flat div/span instead of ol/li (loses count + position, fails 1.3.1)"
  evolution: "path->location standardised; nav+ol/li standardised; wrap->truncation; separators DOM->CSS; aria-current=page settled; JSON-LD -> app layer"
  unverified:
    - "external-supplied 2026 version numbers (React Aria 3.5.32, Atlassian 16.1.1, Base Web 18.1.0, etc.) — held loosely"
    - "Atlassian maxItems default of 8 (external claim; needs _source-text)"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-breadcrumbs/` (16 June 2026), the first Navigation brief built directly on Link (see link). Both passes converged on the spine — the location-vs-path settlement, the APG `nav[aria-label]`+`ol`/`li` landmark contract, the decorative-separator rule (CSS pseudo-element, never DOM content), `aria-current="page"` (not `location`) on the current crumb, the `maxItems`/`itemsBeforeCollapse`/`itemsAfterCollapse` overflow-collapse model keeping root + current, the JSON-LD-as-app-concern position (the component ships semantic HTML, never a silent default), the `asChild` router polymorphism inherited per crumb, the mobile back-up-one-level swap, and `Breadcrumbs`/`BreadcrumbItem` naming. The one genuine fork was the current-crumb treatment: the external pass leaned interactive-link (React Aria/Primer) on an API-uniformity argument; the practice defaults to non-interactive text + `aria-current="page"` (Carbon/Base Web), since the component can auto-render the last crumb as text while keeping a uniform `items`/children API — the link-form's main argument doesn't hold, and both are WCAG-conformant, so it's flagged contested. External-pass contributions folded in: the Primer `overflow` `wrap`/`menu`/`menu-with-root` strategies, the Atlassian `maxItems`/`defaultExpanded`/`onExpand` surface, the three concrete JSON-LD failure modes (duplicate scripts, hydration mismatch, hidden-subtree de-indexing), the overflow-menu `aria-haspopup`/`aria-expanded` + focus-return detail, the RTL chevron-mirror mechanics, and the Polaris back-button blur. Claude-pass contributions: the framing as the first brief standing on another component, the trail-collapse-over-label-truncation rule, the auto-derived current crumb, and the count-vs-width collapse framing. The 2026 version numbers and the Atlassian `maxItems=8` default are flagged unverified. Conformant to `components/_schema.md`. Closes the wayfinding-hierarchy lane; Menu is the adjacent Navigation brief the overflow affordance leans on.*
