# Pagination — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/pagination.md`; version numbers and the rel=prev/next current crawl state flagged unverified. The two passes converged almost completely — no substantive disagreement.*

---

Pagination Component Field-Truth Study and Architecture Report

## 1. Framing
Pagination is a severe stress test for routing polymorphism, focus management, semantic HTML, and accessibility. It is a Navigation-category brief composed of three established substrates: page-number items + the nav landmark inherit Link and Breadcrumbs; prev/next/load-more inherit Button; the page-size picker inherits Select. Building it requires orchestrating primitives, not reinventing interaction models.

The defining framing is the three-model framework: numbered (discrete page links), load-more (manual append), infinite scroll (intersection-observer append). Practice default: numbered is the strictly enforced standard for known/bounded/jumpable/bookmarkable sets (tables, admin, e-commerce search) — guarantees bookmarkable URLs, shareable views, and a sense of dataset volume/position. Load-more applies exclusively to chronological feeds/discovery where order matters but depth is open-ended — preserves vertical orientation and keeps loaded items in the DOM. Infinite scroll is a dangerous extreme: strands keyboard users, makes footers unreachable, destroys position sense, breaks history/scroll restoration; permissible only for casual visually-heavy mobile discovery feeds, and must degrade to a load-more button after a capped number of auto-appends. Field leaders diverge on how monolithic the numbered component is (Ant's all-inclusive table pager vs React Aria's refusal to ship a UI component) but converge on purpose: discrete, URL-driven wayfinding through large arrays.

## 2. Anatomy and parts
Outer container = nav landmark wrapper (<nav aria-label>, the Breadcrumbs contract). Layout = semantic <ul> (informs SR of count). Page items = <li> with interactive nodes swapping between <a> (URL apps) and <button> (SPA); active uses aria-current="page". Prev/next flank the items (inherit Button; icon-only chevrons or icon+text; disabled at boundaries). Truncation ellipsis = contested; practice default renders it inert (aria-hidden="true" span), not an interactive jump (ambiguous interaction). Enterprise: page-size Select + range/status text "Showing 1–10 of 200" + sometimes a page-jump input (Ant). Table provided: Landmark Wrapper (nav, Breadcrumbs), Layout List (ul/li), Page Item Active (a aria-current=page, Link), Page Item Inactive (a or button, Link/Button), Prev/Next (button, Button), Ellipsis (span aria-hidden, inert), Page-Size (select, Select), Range Text (span, Typography).

## 3. Properties / API
Controlled (page/current + onPageChange) and uncontrolled (defaultPage/defaultCurrent). Total span divergence: count/pageCount (total pages — MUI/Primer) vs total (raw items) + pageSize (Ant/enterprise; internally Math.ceil(total/pageSize)). Practice default: prefer count (pages) for the simple pager; require total+pageSize for the enterprise pager to auto-render "Showing M–N of T". Windowing: siblingCount (pages either side of active; default 1) + boundaryCount (pages locked to start/end; default 1). showFirstLast boolean for absolute jump buttons. renderItem slot (MUI) / hrefBuilder (Primer) / asChild (Radix) for polymorphic routing — the system never hardcodes routing. pageSizeOptions + onPageSizeChange for enterprise.

## 4. States and variants
Item states: rest/hover/focus/active/current. Current = reversed contrast or heavy underline + aria-current="page". Disabled manifests at boundaries: native disabled removes from tab order, creating a trap (rapid Next to last page drops focus to <body>); practice default uses aria-disabled="true" + pointer-events suppression + JS event prevention, preserving focus order. Macro variants: minimal prev/next pager (Polaris); compact/mobile (collapse to "Page 4 of 20" fraction + prev/next; Apple HIG dots for ≤10 peers); load-more (block button appends); infinite (intersection observer + spinner).

## 5. Usage guidance
Numbered for deterministic indexing/retrieval (search, catalogs, admin tables) — communicates volume + position, bookmarkable. Load-more for discovery/feeds — preserves order, keeps items in DOM, user agency over requests. Two numbered archetypes: Enterprise Table Pager (Carbon/Ant — page-size select + range readout + numbered links + quick-jump, locked to table bottom) and Simple Content Pager (Primer/Base Web — strips size selector + range text, pure truncation array). Placement: always bottom (top forces nav before content). Conditional unmount when content fits one page.

## 6. Accessibility
APG has NO formal pagination pattern; industry converged on a composite. Outer <nav> with aria-label ("Pagination") so SR users isolate it in the landmark rotor (else collides with primary nav). <ul>/<li> announces count. Current = aria-current="page"; active styling ≥3:1 background, ≥4.5:1 text. Ellipsis trap: exposed dots announce "dot dot dot"/"period period period"; practice default aria-hidden="true" (semantic list already implies gaps). Focus management on transition is the most-botched requirement: real <a> links reload + browser moves focus to top; SPA <button> mutations leave focus stranded at the bottom (content silently changes) — must move focus to top of results region or aria-live="polite" announce "Page 2 of 10 loaded". Load-more: move focus to first newly-loaded item, else keyboard users reverse-tab up through new content.

## 7. Content guidelines
Numeric links: visible integer; accessible name "Go to page 4"/"Page 4". Enterprise readout "Showing [Start]–[End] of [Total]" with en-dash (–) not hyphen; degrade to "Showing [Start]–[End]" if total unknown/expensive. Compact: "Page [Current] of [Total]" / "[Current] / [Total]" — also SR fallback. Page-size label "Items per page:"/"Rows per page:". Boundary controls strictly "Previous"/"Next" (not Prev/Back/Forward). Load-more "Load more items"/"Show more results", not "More".

## 8. Motion and transition
Restraint — pagination is an index, users expect snappy response. Hover/active 100–150ms crossfade. Layout-shift trap: active page incrementing single→double→triple digit (9→10→100) shudders with proportional fonts; fix with font-variant-numeric: tabular-nums or fixed min-width accommodating three digits. Load-more: new items fade in with slight vertical translation (staggered) to signal downward expansion. Infinite: loading indicator at intersection boundary; respect prefers-reduced-motion (static "Loading...").

## 9. Internationalization
RTL: truncation array flips (page 1 far right, progressing left); prev/next chevrons mirror (Next on left, left-pointing); use logical properties / transform: scaleX(-1) via dir="rtl", not hardcoded SVG. Locale digits: run integers through Intl.NumberFormat (Persian/Eastern Arabic numerals). String expansion: "Showing M–N of T" expands up to 40% (German/Russian); flex + logical gap, no fixed text-node widths; interpolation order customizable.

## 10. Naming
Majority (MUI, Carbon, Primer, Ant, Atlassian) standardize on Pagination. A subset uses Pager (reserved for the minimal prev/next variant). Practice default: standardize on Pagination; variations as named exports/props/variants (Pagination.Minimal, Pagination.Table), not separate Pagination/Pager components. Load-more divorced from the namespace (a Button composition).

## 11. Implementation notes
Truncation algorithm (MUI usePagination): totalVisible = (boundaryCount*2) + (siblingCount*2) + 3 (current + two ellipses); if count <= threshold return 1..count, no ellipses. Else leftSiblingIndex = Math.max(currentPage - siblingCount, boundaryCount + 2), rightSiblingIndex = Math.min(currentPage + siblingCount, count - boundaryCount - 1); inject 'start-ellipsis'/'end-ellipsis' when siblings disconnect from boundaries. SEO: Google deprecated <link rel="prev/next"> in 2019; every paginated link must be a real <a> with resolvable href (?page=2). Button+onClick pagination is invisible to crawlers. Routing polymorphism via asChild/renderItem spreads a11y attrs + handlers + classes onto a user-provided router anchor. Headless: MUI usePagination returns the window array, leaving <nav>/<ul>/<li> rendering to the consumer.

## 12. Related and alternative components
Link (base interactive primitive for URL-changing pagination). Breadcrumbs (shares nav[aria-label]+ul landmark; both horizontal locational indicators). Button (prev/next/boundary + load-more). Select (enterprise row density). Table/Data Grid (primary host; couples state to sort/filter/cursor offset). Alternative: Virtualized Scrolling/windowing (React Aria useAsyncList — async fetch + DOM virtualization; performant for massive sets but severe a11y issues with absolute positioning, SR cursor tracking, breaks native Find-in-Page). A specialized alternative, not a wholesale replacement.

## 13. Field POV evolution
Repudiation of infinite scroll (mid-2010s panacea → a11y community demonstrated focus-trap/footer/keyboard costs → field retreated to load-more as ethically/architecturally superior). rel=prev/next deprecation (2019) forced polymorphic rendering adoption (decouple visual logic from routing so consumers pass crawlable <a>). Monolithic → headless hooks (usePagination exports the math engine; React Aria/Spectrum bypass a dedicated UI pager entirely, supplying useAsyncList).

## 14. Sources cited
MUI v5 (2026). IBM Carbon v11 (2026; Enterprise Table Pager vs Nav Pager separation). GitHub Primer React v36 (2026; reload-vs-append focus rules). Ant Design v5.19+ (2026; showSizeChanger/showQuickJumper). Shopify Polaris v12+ (2026; hasNext/hasPrevious). Base Web v13+ (2026; Numbered vs Overflow). Google Material 3 (2026; deprecates pagination in swipeable cards). React Aria/Spectrum v3 (2026; intentional absence of a pager UI, useAsyncList).

## 15. Agent-consumable schema

```yaml
identity:
  name: Pagination
  aliases: [Pager, Pagination Nav, Page Controls]
  category: Navigation
  description: A complex navigational list that allows users to traverse bounded datasets via sequential, numbered links or discrete boundary controls.

anatomy:
  wrapper: {element: nav, role: navigation, attributes: [aria-label]}
  layout: {element: ul}
  pageItem: {inherits: Link, attributes: ['aria-current="page" on active']}
  controls: {inherits: Button, elements: [Previous, Next, First, Last]}
  ellipsis: {element: span, attributes: ['aria-hidden="true"']}
  densityPicker: {inherits: Select, optional: true}

api:
  controlled: {page: number, onPageChange: function(event, page)}
  uncontrolled: {defaultPage: number}
  total: {count: number (total pages, preferred for simple), totalItems: number (enterprise), pageSize: number}
  windowing: {siblingCount: number (default 1), boundaryCount: number (default 1)}
  rendering: {renderItem: function | slot (polymorphic routing), showFirstLast: boolean}

states:
  active: [aria-current="page", visual highlight]
  disabledBoundary: [aria-disabled="true", pointer-events suppressed]
  mobileCollapse: Hides truncation array, falls back to fraction or dots.

accessibility:
  keyboard: Normal tab sequence; arrows do not navigate pages (Enter/Space activates items).
  focusManagement:
    spaMutations: Move focus to new content wrapper or announce via aria-live.
    loadMore: Move focus to first newly appended item.
    reload: Browser native (focus to top of document).
  semantics: No formal APG pattern. Requires nav > ul > li > a.

implementation:
  seo: Relies on true anchors/hrefs due to Google rel=prev/next deprecation.
  headless: Calculate truncation array via hooks (usePagination) before rendering DOM.
```
