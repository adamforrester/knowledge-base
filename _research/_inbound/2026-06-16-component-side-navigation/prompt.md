You are researching the Side Navigation component for a senior design
systems practitioner at a digital agency. The output is a field-truth
study of how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what side
navigation is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Side Navigation is the most composition-heavy Navigation brief, and it
CLOSES the Navigation category. It STANDS ON four briefed substrates:
- THE ITEMS + NAV LANDMARK + ACTIVE STATE inherit LINK and the
  Breadcrumbs/Pagination nav contract (components/link.md,
  components/breadcrumbs.md): a <nav aria-label> wrapping lists of Links,
  the current item marked aria-current="page". Don't re-derive Link's
  <a href> contract or asChild router polymorphism — reference them as
  inherited.
- THE MOBILE / COLLAPSED-OVERLAY FORM inherits DRAWER
  (components/drawer.md): on narrow viewports the persistent side nav
  transforms into a MODAL DRAWER behind a hamburger. Don't re-derive the
  drawer; draw the side-nav-vs-drawer boundary (persistent structure vs
  transient overlay) explicitly.
- THE COLLAPSIBLE SUB-SECTIONS inherit ACCORDION / DISCLOSURE
  (components/accordion.md): multi-level nav expands sub-items via the
  heading+button[aria-expanded]+region disclosure pattern — NOT role=menu
  (the nav-is-not-a-menu rule from components/menu.md applies in full).
- THE COLLAPSED-RAIL ICON LABELS inherit TOOLTIP
  (components/tooltip.md): an icon-only collapsed rail needs each item's
  label exposed (tooltip + accessible name).
And item icons inherit ICON (components/icon.md).

THE DEFINING SIDE-NAVIGATION-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE PERSISTENT-STRUCTURE vs DRAWER decision + THE RESPONSIVE TRANSFORM
  (the headline): a side nav is a PERSISTENT part of the page layout (in
  the grid/flex shell, present across route changes) — NOT a transient
  overlay. On narrow viewports it transforms into a modal Drawer behind a
  hamburger toggle. Resolve the persistent-vs-transient boundary and the
  desktop->mobile transform (and the relationship to Material's navigation
  rail / navigation drawer / navigation bar taxonomy and Carbon's UI
  Shell).
- THE COLLAPSED-RAIL vs EXPANDED model (the defining interaction): the
  expanded nav (icon + label) collapsing to an icon-only RAIL (the
  toggle, state persistence across sessions, the collapsed-item label
  requirement via Tooltip, hover/flyout reveal of labels and sub-items).
  Resolve the rail-vs-expanded default and the collapse affordance.
- MULTI-LEVEL / NESTED STRUCTURE — single-level vs nested nav; sub-items
  expanded IN PLACE via the Accordion/Disclosure pattern (button
  [aria-expanded] + region) vs a FLYOUT (a Popover when collapsed to a
  rail); the hard rule that this is NOT role=menu (disclosure + links —
  the nav-is-not-a-menu correction); the side-nav-vs-Tree boundary (a true
  hierarchical data tree is role=tree; site nav is nav+disclosure+links).
- THE ACTIVE-STATE CONTRACT — aria-current="page" on the current item
  (inherited from Link), the visual "you are here" indicator, and the
  multi-level case (the active child + its expanded/highlighted ancestor);
  active-vs-hover-vs-focus distinction.
- THE NAV LANDMARK + KEYBOARD MODEL — <nav aria-label="..."> (a unique
  label to distinguish it from the global header nav, breadcrumb nav,
  footer nav); the keyboard model is TABBED through links (NOT a roving
  tabindex widget — it's a list of links, not a menu/menubar/tree); the
  collapse toggle is a button[aria-expanded]; the skip-link relationship.
- ITEM ANATOMY — icon + label, the active indicator, an optional
  badge/count, nested group headers, collapsible section headers, the
  rail tooltip; the nav header (logo/product) and footer (account/settings
  pinned at the bottom).
- THE SIDE-NAV vs TOP-NAV vs TABS vs BREADCRUMBS boundaries — primary
  persistent wayfinding (side nav) vs the global header bar vs in-page
  panel switching (Tabs — not navigation) vs the location trail
  (Breadcrumbs, a secondary aid). Side nav as PRIMARY navigation.

Field-leader systems to survey (web): Google Material 3 (navigation rail /
navigation drawer / navigation bar — the responsive taxonomy), IBM Carbon
(UI Shell — SideNav, rail vs expanded), GitHub Primer (NavList — the
canonical side-nav list with sub-items + aria-current), Shopify Polaris
(Navigation), Atlassian Design System (side navigation / the navigation
system), Microsoft Fluent (Nav), Ant Design (Menu in inline/vertical mode
— note Ant overloads "Menu" for navigation, which the Menu brief flags as
the nav-is-not-a-role=menu anti-pattern; report it), Base Web (Uber) (Side
Navigation), shadcn/ui (Sidebar — the collapsible-rail reference). WAI-ARIA
APG (no formal side-navigation pattern — it is the nav landmark + a list
of links + the Disclosure pattern for sub-sections; treeview ONLY for a
true data tree). Mobile reference where relevant: Apple HIG (sidebars /
tab bars), Material 3 (navigation rail/bar). Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for Link (items + nav contract + active),
Drawer (mobile form), Accordion (sub-sections), Tooltip (rail labels);
flag unverified claims under notes.unverified).

1. Framing — what it is (persistent primary wayfinding) and what it isn't
   (a transient Drawer / a Menu / Tabs / Breadcrumbs / a data Tree); the
   persistent-vs-drawer + responsive-transform decision up front; why
   systems disagree.
2. Anatomy and parts — the nav landmark, the header (logo), the item
   (icon + label + active indicator + optional badge), the collapsible
   group/section, the collapse/expand toggle (rail), the footer
   (account/settings), the rail tooltip.
3. Properties / API — items/children (or a data model), collapsed/expanded
   + onCollapsedChange, the active/current item, multi-level (nested items
   + expanded state), the render-item slot (Link/asChild router), the
   mobile-drawer breakpoint.
4. States and variants — item states (rest/hover/focus/active=current/
   disabled); expanded vs collapsed rail; single vs multi-level;
   persistent vs the mobile drawer; with-icons / with-badges; the section
   group.
5. Usage guidance — side nav (primary persistent wayfinding, deep/broad
   IA) vs top nav (shallow/marketing) vs Tabs (in-page) vs Breadcrumbs
   (location trail) vs Drawer (transient); when a rail vs full; the
   boundaries + the responsive transforms.
6. Accessibility — nav[aria-label] (unique), aria-current=page, the
   Disclosure pattern for sub-sections (NOT role=menu), the tabbed (not
   roving) keyboard model, the collapse-toggle aria-expanded, the
   collapsed-rail tooltip/label requirement, the skip-link relationship,
   the tree-only-for-data-tree note, WCAG SCs.
7. Content guidelines — concise item labels, the icon discipline, section
   grouping, the active label, the collapsed-rail label, badge content.
8. Motion and transition — the collapse/expand width animation, the
   flyout/sub-item reveal, the mobile-drawer slide (inherits Drawer),
   reduce-motion.
9. Internationalization — RTL (the nav flips to the inline-end edge via
   logical properties, chevrons mirror), text expansion (labels), the
   rail width.
10. Naming — Side Navigation / Sidebar / Nav / Navigation Rail / NavList /
    SideNav; the practice's default; aliases.
11. Implementation notes — the persistent layout shell (grid/flex) vs the
    mobile-drawer transform, the collapsed-rail + flyout, the
    Disclosure-not-role=menu sub-nav, aria-current wiring + router
    integration (asChild), state persistence, headless vs opinionated.
12. Related and alternative components — typed relationships (Link items +
    nav contract, Drawer mobile form, Accordion/Disclosure sub-sections,
    Tooltip rail labels, Icon, the top-nav/app-header boundary, Tabs and
    Breadcrumbs boundaries, Tree).
13. Field POV evolution — recent shifts (the collapsible-rail/sidebar
    pattern, the nav-is-not-a-menu correction reaching side nav, the
    responsive side-nav<->drawer transform, aria-current standardisation).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what side navigation is — explain
the persistent-structure-vs-drawer decision + the responsive transform,
the collapsed-rail-vs-expanded model (and the collapsed-item label
requirement), the multi-level Disclosure-not-role=menu sub-nav (and the
side-nav-vs-tree boundary), the aria-current active-state contract, the
tabbed-not-roving keyboard model, and the side-nav-vs-top-nav-vs-tabs-vs-
breadcrumbs boundaries that field leaders still diverge on.
