You are advising a senior design systems practitioner at a digital agency
who maintains a personal knowledge base of design-systems field-truth. The
knowledge base has a ~45-component catalogue and a PATTERNS layer above it.
Patterns carry a `tier` and a GOV.UK-style `goal` facet. Several `composition`
patterns are briefed (Forms-as-a-system, View-state orchestration,
Data-collection recipes, Search orchestration).

This brief: **App shell / global header**. Tier: **`layout-and-shell`**.
Goal: `navigate`. It is the FIRST `layout-and-shell` brief — a structural
archetype, not a composition recipe — so the spine BENDS: **Layout &
structure carries the weight**, decision rules are more about structural forks
(nav placement, responsive collapse) than micro-logic, and Flow is light (an
app shell is mostly persistent, not a journey over time). Lean into that shape;
don't force a `composition`-style brief.

The app shell is **the persistent frame every other screen sits inside** — the
global header, the primary navigation, the content region, and the landmark/
skip-link skeleton. The single most important boundary: this brief does NOT
re-derive the Side Navigation component (the nav control's own anatomy/ARIA,
already briefed) or the page templates that sit *inside* the shell
(master-detail, dashboard, settings — separate `layout-and-shell` briefs). It
owns the FRAME: the header zones, the nav placement decision, the responsive
collapse, the landmark structure, and the SPA route-change focus contract.
Assume Side Navigation, Menu, Link, Avatar, and the Search orchestration
pattern are briefed; cite the boundary, don't repeat them.

This is field-truth synthesis for someone who has built many app shells.
Explain the non-obvious — where leading systems genuinely disagree, and the
defensible default. Be opinionated and declarative.

=== WHAT TO SURVEY (the field) ===

Cite each with a version date; note the verification path for current claims.
- WAI-ARIA Authoring Practices — landmark regions (banner / navigation / main
  / contentinfo / complementary), the skip-link contract, and the SPA
  route-change focus-management guidance. The accessibility spine.
- Design-system shells/frames — IBM Carbon (the UI Shell: header + side nav),
  Shopify Polaris (Frame / TopBar / Navigation), Atlassian (the page layout /
  navigation system, the "side navigation" + "banner" slots), Material 3
  (navigation drawer vs rail vs bar; the adaptive navigation guidance),
  Microsoft Fluent, Adobe Spectrum, GOV.UK (the service header / page
  template). Where each places nav and how each collapses.
- The PWA "app shell" architecture model (the shell-persists / content-swaps
  idea) and SPA routing reality (focus, scroll restoration, title/route
  announcement).
- Navigation-UX literature — NN/g (top vs side nav, the hamburger-menu
  debate, mega-menus), responsive-navigation patterns (priority+, bottom nav).

=== WHAT TO RESOLVE (the structural decisions are the deliverable) ===

Give the structural forks as machine-resolvable rules (`IF condition → USE
resolution`) where a real threshold exists, prose where it's genuinely
contextual. Resolve at least:

1. **Top nav vs side nav vs both** — the central frame fork. When horizontal
   top nav, when a side nav, when the hybrid (top bar + side nav)? The
   deciding axes (IA depth/breadth, app vs site, number of destinations,
   density). 
2. **The global header anatomy & zones** — what lives in the header and where:
   logo/home, primary nav or nav trigger, global search (invokes the Search
   pattern), global create/“+”, notifications, help, account/avatar menu,
   workspace/org/product switcher, environment indicator. The left/center/
   right zone model; sticky behaviour.
3. **Side-nav states** — expanded vs collapsed icon rail vs rail+flyout;
   persistent vs overlay; multi-level/nested nav; the collapse toggle and its
   persistence; sectioning/grouping; the active-item + `aria-current` model.
4. **Responsive collapse** — the desktop → tablet → mobile transformation:
   persistent side nav → collapsed rail/toggle → hamburger drawer or bottom
   nav. The breakpoint strategy; bottom-nav (≤~5 destinations) vs hamburger;
   what the header sheds on mobile.
5. **Landmark & skip-link structure** — the banner/navigation/main/contentinfo
   landmarks, the skip-to-content link, heading hierarchy, labelling multiple
   navs (`aria-label`), the keyboard order through the frame. The a11y the
   shell owns.
6. **The SPA route-change contract** — what happens on client-side navigation:
   focus management (move focus to main/the h1?), scroll restoration, route
   announcement (title + live region), the shell-persists/content-swaps model.
   The single most-missed a11y issue in SPAs.
7. **Scroll & persistence model** — sticky header, fixed side nav, the content
   scroll region; content max-width/centering; what persists vs scrolls.
8. **Multi-product / workspace** — the product switcher, the org/workspace
   switcher, the environment banner (staging/impersonation); where they live.

=== THE BOUNDARIES TO HOLD (state in a Related section) ===

- **vs the Side Navigation (component)** — the nav control's own anatomy/ARIA
  vs the frame that places it.
- **vs the page templates** (master-detail, dashboard, settings — sibling
  `layout-and-shell` briefs) — they sit INSIDE the shell's content region;
  the shell is the substrate, not the page.
- **vs Search orchestration (pattern)** — the header's search field invokes
  that pattern; the shell owns the slot, not the search experience.
- **vs Breadcrumb / Tabs (components)** — secondary/in-content navigation, not
  the frame.
- **vs the navigation IA / information architecture** — the strategy of what
  the destinations *are* is a discovery/IA concern (numbered files), not the
  frame's structural job.

=== OUTPUT — follow this pattern-brief spine (bent for layout-and-shell) ===

Structured markdown. ALWAYS sections appear; SCALES appear when they carry
weight — for this tier, **Layout & structure is heavy; Flow is light**.
1. **Frontmatter** — YAML: type: pattern-brief, title, description, tags,
   tier: layout-and-shell, goal: navigate, status, timestamp.
2. **`# App shell` H1 + a one-paragraph blockquote** framing the problem and
   the boundary (the persistent frame, not the pages inside).
3. **Problem & context** — the recurring problem; when it applies; why
   systems diverge.
4. **Composition** — the components the frame assembles as typed references
   (Side Navigation, Menu, Link, Avatar, the search slot…) and how the regions
   fit. Don't re-derive them.
5. **Decision rules** — the structural forks (1–8 above) as machine-resolvable
   rules where possible.
6. **Layout & structure** (HEAVY — the core of this brief) — the region model
   (header / nav / main / optional complementary / footer), the zone model of
   the header, the grid/max-width, the scroll/persistence model, the
   responsive transformation across breakpoints.
7. **Accessibility orchestration** — the landmark structure, the skip link,
   multiple-nav labelling, `aria-current`, keyboard order, and (critically)
   the SPA route-change focus/announcement contract. The a11y the shell owns.
8. **Flow & states** (LIGHT) — only what's stateful: nav expand/collapse,
   the mobile drawer open/close, route transitions. Keep it short.
9. **Content & copy** (SCALES) — nav labels, the skip-link text, the
   account/switcher labels, the environment banner copy.
10. **Variants & responsive** (SCALES) — top-nav vs side-nav vs hybrid shells;
    the marketing-site vs app shell; the multi-product shell; the breakpoint
    variants.
11. **Anti-patterns** — the recurring traps (hamburger on desktop, no skip
    link, no route-change focus management, nav that reflows unpredictably,
    too many top-level destinations, a non-persistent frame that reloads,
    missing landmarks, sticky header that eats mobile viewport).
12. **Related patterns & components** — the five boundaries above, typed.
13. **Field POV evolution** (SCALES) — the shifts (top nav → side nav for
    apps; the hamburger backlash; bottom nav on mobile; the adaptive
    navigation rail; the SPA focus-management reckoning).
14. **Reference instantiations** (SCALES) — where to look (Carbon UI Shell,
    Polaris Frame, Material adaptive navigation, the ARIA landmark spec).
15. **Sources cited** — with version dates; flag unsourced claims as
    unverified rather than inventing citations.
16. **Agent-consumable schema** — a fenced YAML block: identity (id, name,
    aliases, tier, goal, status), problem, composition (requires: [typed
    component ids]), decision_rules (as `{ if, use }`), layout (the region +
    zone + responsive model — the heavy field for this tier),
    accessibility_orchestration, flow, content, variants, anti_patterns,
    reference_instantiations, relations (composes / relates-to / boundary),
    notes (contested / unverified).

Synthesize; give frameworks where context (IA depth, app vs site, platform)
decides, defaults where the field has converged. Date current-state claims.
Flag what you can't source.
