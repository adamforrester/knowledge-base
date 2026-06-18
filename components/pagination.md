---
okf_version: "0.1"
type: component-brief
title: Pagination
description: The most reuse-heavy Navigation brief — it inherits Link + the Breadcrumbs nav-landmark contract (page items + aria-current), Button (prev/next/load-more), and Select (rows-per-page), and invents almost nothing. A field-truth study of the three-model decision (numbered vs load-more vs infinite scroll), the truncation/window algorithm (siblingCount/boundaryCount + the inert ellipsis), the link-vs-button page-item rule (and the rel=prev/next SEO deprecation), the under-specified focus-on-page-change problem (load-more's focus-to-new-items rule), the enterprise-table-pager vs simple-content-pager archetypes, and the tabular-nums no-layout-shift discipline — with the practice's defaults.
tags: [components, navigation]
category: Navigation
status: stable
aliases: [pager, pagination-nav, page-controls, table-pagination]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Pagination

> Pagination splits a large result set into navigable chunks and tells the user *where they are* in the whole. It is the catalogue's most reuse-heavy brief: it invents almost nothing, standing instead on Link + the `nav[aria-label]` landmark contract Breadcrumbs established (page items are Links + `aria-current="page"`), on Button (prev/next/load-more), and on Select (rows-per-page). What's genuinely its own — and what the field actually fights over — is four things: the **three-model decision** (numbered vs. load-more vs. infinite scroll), the **truncation/window algorithm** (`siblingCount`/`boundaryCount` + an inert ellipsis), the **link-vs-button** page-item rule (URL-changing pages are real `<a href>`s, SPA-in-place pages are Buttons), and the badly-under-specified **focus-on-page-change** problem (where focus goes and what is announced after you turn the page — the part most systems get wrong, especially load-more, which must move focus to the first new item). Notably, WAI-ARIA APG has *no* dedicated pagination pattern: pagination simply *is* a labelled nav of links + `aria-current`, which is exactly why it inherits rather than invents.

---

## 1. Framing

Pagination chunks a bounded or open-ended result set and provides wayfinding between the chunks plus a sense of position in the total. It is a Navigation brief assembled from briefed substrates: the **page-number items + the nav landmark inherit Link and the Breadcrumbs contract** (see link, breadcrumbs), the **prev/next/load-more controls inherit Button** (see button), and the **rows-per-page picker inherits Select** (see select). Building pagination is orchestrating primitives, not inventing interaction models.

**The defining framing is the three-model decision:**
- **Numbered pagination** (discrete page links) — the strict default for **known/bounded, jumpable, bookmarkable** sets: search results, data tables, admin, e-commerce catalogues. It communicates the dataset's *volume* and the user's *exact position*, and lets them deep-link/bookmark/share a specific page.
- **Load-more** (a Button appending the next chunk) — for **chronological feeds and discovery** where order matters but depth is open-ended. Preserves keyboard access, footer reachability, scroll-back (prior items stay in the DOM), and user control over bandwidth. The safe default for feeds.
- **Infinite scroll** (auto-load on scroll via an intersection observer) — a dangerous extreme to restrict severely: it strands keyboard users in an ever-growing DOM, makes the **footer permanently unreachable**, destroys the sense of position/total, and breaks history + scroll-restoration on back-navigation. Permissible *only* for casual, visually-heavy discovery feeds (touch/mobile), and even then it must degrade to a load-more button after a capped number of auto-appends.

What it *isn't*: **Tabs** (a fixed small set of peer views, not chunks of one ordered set — see tabs), a **Stepper** (a linear flow with completion state — see breadcrumbs §boundaries), or a **Carousel** (paged *content*, not paged *results*). Why systems disagree: which model is default, how monolithic the numbered component is (Ant's all-in-one table pager vs. React Aria shipping *no* pagination UI at all), the truncation algorithm, link-vs-button, and focus/announcement on change.

## 2. Anatomy and parts

- **nav landmark + list** — `<nav aria-label="Pagination">` wrapping a `<ul>`/`<li>` (the Breadcrumbs landmark contract reused; the label disambiguates it from the primary nav in the landmark rotor, and the list tells AT the count of visible controls).
- **page-number item** — a **Link** (`<a href="?page=N">`) when the URL changes, or a Button in SPA mode (§3); the **current page** carries `aria-current="page"` and is visually reversed/emphasised.
- **prev / next controls** — Buttons or Links (chevrons or "Previous"/"Next"); **disabled at the boundaries** (page 1 → prev; last page → next).
- **first / last jump controls** — optional double-chevron "go to first/last" (structurally distinct from the boundary *numeric* links).
- **truncation ellipsis** — the "…" standing in for hidden page ranges; **inert by default** (`<span aria-hidden="true">` — a gap indicator, not a control; §6).
- **page-size / rows-per-page select** — a Select ("10 / 25 / 50 per page") — the enterprise pattern (§3, see select).
- **range / status text** — "Showing 1–10 of 200" (en-dash, not hyphen) — the deterministic orientation readout.
- **page-jump input** — a "Go to page [ ]" field (Ant/Carbon `showQuickJumper`; optional).

## 3. Properties / API

- **Controlled / uncontrolled** — `page` (or `current`) + `onPageChange`, or `defaultPage`. Support both (1-indexed by convention).
- **Defining the total span (a real field divergence):** `count`/`pageCount` (total *pages*, computed by the consumer — MUI/Primer) vs. `total` (total *items*) + `pageSize` (Ant/Carbon, which internally does `Math.ceil(total/pageSize)`). **The practice default: accept `count` (pages) for the simple content pager** (decouples UI from data logic), **but require `total` + `pageSize` for the enterprise pager** so it can compute and render "Showing M–N of T" without the consumer hand-building the string.
- **Window algorithm:** `siblingCount` (pages either side of current — default 1) + `boundaryCount` (pages pinned at each end — default 1), with an ellipsis filling gaps (§11).
- **`pageSize` + `pageSizeOptions` + `onPageSizeChange`** — the rows-per-page Select (changing it resets to page 1).
- **`showFirstButton` / `showLastButton`** — the first/last jump controls.
- **The render-item slot (the routing-polymorphism lever):** `renderItem` (MUI — intercept the generated item and map it to a framework router Link), `hrefBuilder` (Primer — generate the URL string for native anchors), or **`asChild`** (Radix-style). This is what decides **Link vs Button** per item and lets a page item *be* a router Link (inherits Link's `asChild`, §11).
- **`mode`** — numbered vs. load-more (`hasMore` + `onLoadMore` + `loading`).
- Headless **`usePagination`** (MUI-style) returns the computed item model (`{type: 'page'|'start-ellipsis'|'end-ellipsis'|'previous'|'next'|'first'|'last', page, selected, disabled}`) for full render control.

## 4. States and variants

- **Item states:** rest / hover / focus-visible / **current** (`aria-current="page"`, reversed contrast or structural underline — must hold ≥3:1 against background and ≥4.5:1 text) / **disabled** (prev/next at boundaries). The ellipsis is not a state — it's a non-control.
- **Boundary-disabled handling (the keyboard trap):** native `disabled` *removes the control from the tab order*, so a keyboard user rapidly activating "Next" who hits the last page has focus suddenly dropped to `<body>`. The practice default uses **`aria-disabled="true"` + `pointer-events: none` + JS event prevention**, keeping the control in the focus order so the user learns they've reached the end without losing context.
- **Variants:**
  - **Numbered** (full truncated array) — the default for bounded sets.
  - **Simple prev/next** (just "‹ Previous / Next ›", optionally "Page 3 of 20") — content/article paging (Polaris `hasNext`/`hasPrevious`).
  - **Full table pager** (page-size Select + range text + page-jump + numbers + prev/next) — the enterprise/Carbon/Ant archetype.
  - **Load-more** (a single block Button appending items) — feeds.
  - **Infinite scroll** (intersection observer + foot-of-list spinner) — restricted discovery feeds.
  - **Compact / mobile** — collapse the array to prev / "Page 4 of 20" (a fraction node) / next. (Apple HIG's dot page-controls are a mobile variant, but only for ≤10 peers — they break under deep sets.)

## 5. Usage guidance

- **The three-model framework (the headline decision):**
  - **Numbered** when the set is **bounded and the user benefits from jumping, deep-linking, or sensing the total** — search, tables, admin, catalogues. Bookmarkable and crawlable.
  - **Load-more** when depth is **open-ended but keyboard access, a reachable footer, and user control matter** — most feeds. The safe default for continuous content.
  - **Infinite scroll** **only** for casual endless discovery where the footer is irrelevant and position doesn't matter — and even then with a load-more fallback after capped auto-appends. **Never** for search results, tables, or anything with a footer the user needs (checkout, settings, contact). An accessibility liability by default.
- **Enterprise-table pager vs. simple content pager** — a data table wants the **full pager** (page-size, range text, jump, numbers); an article/blog/short list wants the **minimal prev/next** (numbers add database-style noise). Match the archetype to the host.
- **Placement & conditional render:** pagination sits at the **bottom** of the dataset (top placement forces the user past controls before they've seen content); and it **unmounts entirely when everything fits on one page** (don't render dead disabled controls).
- **Don't use Pagination for:** a small fixed set of peer views (→ Tabs), a linear flow (→ Stepper), or paged marketing content (→ Carousel).

## 6. Accessibility

**WAI-ARIA APG has no dedicated pagination pattern** — the field converged on a composite: a labelled nav of links + `aria-current`. Adhere to it rigidly.

- **Structure:** `<nav aria-label="Pagination">` (the label is mandatory — without it the component collides with the primary nav in the landmark rotor) + a `<ul>`/`<li>` list, page items as Links with **`aria-current="page"`** on the current page (the Breadcrumbs/Link contract reused).
- **The inert ellipsis** — exposed truncation dots get announced as "dot dot dot" / "period period period"; wrap the "…" in `aria-hidden="true"`. The semantic list already implies the gap, so the visual ellipsis is pure noise for AT.
- **Disabled prev/next** — `aria-disabled` + non-actionable, *not* native `disabled` (which drops focus to `<body>` at the boundary — §4).
- **Keyboard model — tabbed, NOT roving.** Unlike Tabs/Menu, pagination is **not** a single-tab-stop roving widget: every control sits in the normal tab order and **arrow keys do not move between pages** (Enter/Space activates the focused item). It's a row of independent links/buttons, navigated by Tab.
- **Focus management on page change (the under-specified problem, and the part most systems botch):**
  - **Real `<a href>` full navigation:** the browser loads a new document and resets focus to the top — handled natively (optionally focus the results heading).
  - **SPA in-place update (Buttons):** activating a page swaps the content but leaves focus stranded on the pager at the bottom; the user (and AT) never learns the content changed. Fix: **move focus to the top of the results region** *or* announce via an **`aria-live="polite"`** status ("Page 2 of 10 loaded").
  - **Load-more:** **move focus to the first newly-loaded item** + announce "N more loaded." Leaving focus on the button forces keyboard users to reverse-tab up through the new content — the most-missed rule.
- **Accessible names:** icon-only prev/next need "Go to previous/next page"; page links read better as "Go to page N" / "Page N, current page".
- **WCAG SCs:** 2.4.4 (link purpose — meaningful names), 4.1.2 (name/role/value), 1.3.1 (the nav/list structure), 4.1.3 (status messages — the live-region announcement), 2.4.7 (focus visible), 1.4.3/1.4.11 (current-page contrast), plus Link's and Button's inherited SCs.

## 7. Content guidelines

- **Page-number labels** are the integers; give links full accessible names ("Go to page 4", "Page 4, current page").
- **Range/status text** "Showing 1–10 of 200" with an **en-dash (–)**, the best orientation cue for tables; **degrade gracefully** when the total is unknown/expensive (cursor datasets) to "Showing 1–10" without a layout error.
- **Compact fallback** "Page 3 of 20" / "3 / 20" — also the screen-reader announcement string for live-region focus strategies.
- **Rows-per-page** label "Rows per page:" / "Items per page:" left of the Select; keep integer options (10/25/50/100) for scanning and lower translation overhead.
- **Prev/Next** strictly "Previous"/"Next" (not "Prev"/"Back"/"Forward" — align with browser-nav terminology).
- **Load-more** explicit: "Load more items" / "Show more results" (+ optional remaining count "Load 20 more"), never bare "More".

## 8. Motion and transition

Pagination is an index — users expect snappy, immediate response, so motion is minimal. Item hover/active uses the system's micro-interaction tokens (~100–150ms colour/opacity crossfade). **The headline motion defect is layout shift:** as the current page increments from single → double → triple digits ("9" → "10" → "100"), a proportional font makes the whole array shudder. Fix with **`font-variant-numeric: tabular-nums`** (and/or a min-width on page slots sized for three digits) so the pager is **fixed-width / no-shift**. For **load-more**, new items fade in with a slight vertical translate (staggered if possible) to signal the feed expanded downward (then focus moves into them, §6). Infinite scroll shows a foot-of-list spinner/skeleton. Under `prefers-reduced-motion: reduce`, drop fades and fall back to a static "Loading…". (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL** flips the whole sequence (page 1 on the right, progressing left) and **mirrors the prev/next chevrons** (Next points left); use logical properties + `transform: scaleX(-1)` under `[dir=rtl]` for the glyphs rather than hardcoded SVGs (the Breadcrumbs separator lesson).
- **Locale digits** — run page numbers and the total through **`Intl.NumberFormat`** so users see familiar numerals (Eastern Arabic, Devanagari, Persian) and grouping separators.
- **"M–N of T" string** — a single interpolated, translatable string with placeholders (never concatenation); the interpolation *order* must be customisable for grammatical variation, and it expands ~40% in de/ru — use flex + logical `gap`, no fixed text-node widths.
- **Text expansion** — "Rows per page", "Previous"/"Next", "Load more" all grow; don't fix their widths. (See 13-internationalization-and-rtl.)

## 10. Naming

**`Pagination`** is the near-universal name (MUI, Carbon, Primer, Ant, Atlassian, Base Web); **`Pager`** is an older alias, sometimes reserved for the minimal prev/next variant. **The practice default: `Pagination`** (container) with a headless `usePagination` returning the item model, page items rendered as Links via a `renderItem`/`asChild` slot, density variants as configuration (`Pagination.Table`/`Pagination.Minimal`) not separate components, and the **load-more mechanism kept out of the namespace** (it's a composition of a standard Button + focus management, not a pagination sub-part). Aliases to map: `Pager`, `PaginationNav`, `PageControls`, `TablePagination`.

## 11. Implementation notes

- **The window/truncation algorithm** — compute the visible item list from `page`, `pageCount`, `siblingCount`, `boundaryCount`. The MUI `usePagination` shape: if `pageCount <= (boundaryCount*2 + siblingCount*2 + 3)` (the +3 = current page + two possible ellipses) render `1..pageCount` with no ellipsis; otherwise compute `leftSiblingIndex = max(page - siblingCount, boundaryCount + 2)` and `rightSiblingIndex = min(page + siblingCount, pageCount - boundaryCount - 1)`, and inject a `start-ellipsis` / `end-ellipsis` where a boundary is disconnected from its sibling window. The classic output is `1 … 4 5 [6] 7 8 … 20`. Keep the rendered **width stable** (`tabular-nums` + reserved slots) so it doesn't reflow as the user pages. A headless hook is the clean way to ship this logic separately from rendering.
- **Link vs. button rendering** — page items that change the URL render a real **`<a href="?page=N">`** (bookmarkable, crawlable, middle-clickable — inherits Link + `asChild` for the framework router, see link); client-only SPA pagination that mutates state in place renders **Buttons**. The `renderItem`/`hrefBuilder`/`asChild` slot does both. Never `href="#"` + onClick.
- **SEO / `rel="prev"`/`"next"`** — **Google deprecated `rel=prev/next` as an indexing signal (2019)**; relationships are no longer inferred from `<head>` metadata, so **every paginated page must be a real crawlable `<a href>`** — pure `<button>`+onClick pagination is invisible to crawlers. (Current-platform-state — verify; flag unverified. The tag remains valid HTML and some non-Google agents still use it.)
- **Focus + live region** — wire an `aria-live="polite"` status announcing "Page N of M"; manage focus per §6 (keep-on-control/move-to-results for numbered SPA; **move-to-first-new-item for load-more**).
- **Infinite-scroll mitigations** — if unavoidable: a **load-more fallback** after capped auto-appends, a **reachable footer**, **scroll/position restoration on back-nav**, new-content announcements, and a "page N" anchor. Layer it over a load-more/numbered base, never as a replacement.
- **Headless vs. opinionated** — `usePagination` (item model) + a skinned render is the practice default. Note that **some systems ship no Pagination UI at all** — React Aria/Spectrum supply async-data + collection primitives (`useAsyncList`) and have you compose the DOM — confirming pagination is "a labelled nav of links + a window algorithm," not a novel widget.

## 12. Related and alternative components

- **Stands on:** Link + the Breadcrumbs nav-landmark contract (page items + `aria-label` + `aria-current` — see link, breadcrumbs), Button (prev/next/load-more — see button), Select (rows-per-page — see select), Icon (chevrons — see icon).
- **Hosted by:** Table / Data Grid (the primary host of the enterprise pager, coupling page state to sort/filter/offset — see table), List, search-results and gallery layouts.
- **Alternative to / boundary with:** Tabs (fixed peer views — see tabs), Stepper (linear flow with completion — see breadcrumbs boundary), Carousel (paged content, not results), **infinite scroll** (the pattern pagination is the accessible alternative to), and **virtualized/windowed scrolling** (`useAsyncList` + DOM virtualization — performant for massive sets but with its own a11y costs: absolute-positioning/SR-cursor tracking and broken native find-in-page; a specialised alternative, not a replacement).

(The most reuse-heavy brief so far — it invents almost nothing, standing on Link/Breadcrumbs (items + nav contract), Button (controls), and Select (page-size), and contributing the three-model decision, the window algorithm, the link-vs-button rule, and the focus-on-page-change discipline. See link/breadcrumbs for the nav contract, button for the controls, select for the page-size picker, table for the primary host. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **The repudiation of infinite scroll.** Hailed as frictionless engagement in the mid-2010s and bled into enterprise apps; the a11y community demonstrated the focus-trap/footer-unreachable/position-loss costs, and the field retreated to **load-more (or numbered) as the accessible default**, infinite scroll reserved for casual feeds.
2. **The `rel=prev/next` deprecation (Google, 2019)** forced a rewrite: state-only JS pagination stopped being crawled, accelerating **polymorphic rendering** (`asChild`/`renderItem`/`hrefBuilder`) so consumers pass real crawlable `<a>`s back into the pager.
3. **Monolithic → headless.** Truncation math is complex-but-universal while styling is subjective, so systems export the engine as a hook (`usePagination`) with the opinionated UI as one implementation — and some (React Aria) ship **no** UI component, only the data primitives.
4. **The focus-to-new-items rule for load-more** gained recognition as the fix for the "click load-more, get dropped to the top / stranded on the button" failure.

## 14. Sources cited

(Conservative; the external pass stamped MUI v5/v6, Carbon v11, Primer React v36, Ant v5.19+, Polaris v12+, Base Web v13+, React Aria v3 — all "2026 platform state"; held loosely and flagged unverified; `last-audited` is the re-run trigger.)

- **MUI** `Pagination`/`usePagination`/`TablePagination` (the `count`/`siblingCount`/`boundaryCount` truncation math, `renderItem`, the item model) (2024–2026).
- **IBM Carbon** `Pagination` (page-size Select, range text, page jump — the enterprise table pager; the table-pager-vs-nav-pager split) (2024–2026).
- **Ant Design** `Pagination` (`total`+`pageSize`, `showSizeChanger`, `showQuickJumper` — the most complete enterprise API) (2024–2026).
- **GitHub Primer** `Pagination` (`hrefBuilder`, margin/surround truncation, the reload-vs-append focus rules) (2024–2026).
- **Shopify Polaris** `Pagination` (minimal `hasNext`/`hasPrevious` URL pager) (2024–2026).
- **Atlassian** `Pagination`; **Base Web (Uber)** `Pagination` (Numbered vs Overflow) (2024–2026).
- **Adobe React Aria / Spectrum** — *no dedicated Pagination component* (`useAsyncList` + collections; compose from Link/Button) — itself a finding (2024–2026).
- **Google Material 3** (no strong pagination pattern; guidance against pagination inside swipeable cards) (2024–2026); **Apple HIG** — dot page controls (≤10) (2024–2026).
- **WAI-ARIA APG** — *no* formal pagination pattern (nav + links + `aria-current`); **Google Search Central** — `rel=prev/next` deprecation (2019). WCAG 2.2 (W3C Recommendation, Oct 2023) — 2.4.4, 4.1.2, 1.3.1, 4.1.3, 2.4.7, 1.4.3, 1.4.11, plus Link/Button SCs.

## 15. Agent-consumable schema

```yaml
identity:
  id: pagination
  name: Pagination
  aliases: [pager, pagination-nav, page-controls, table-pagination]
  category: navigation
  status: stable
description: >
  Splits a large result set into navigable chunks and conveys position in
  the whole. Three models: numbered (bounded/jumpable/bookmarkable — the
  default), load-more (open feeds — the safe feed default), infinite scroll
  (casual discovery only — an a11y liability). NOT tabs (peer views), NOT
  stepper (linear flow), NOT carousel (paged content); the accessible
  alternative to infinite scroll. APG has NO pagination pattern — it IS a
  labelled nav of links + aria-current, so it inherits rather than invents.
anatomy:
  parts:
    - "nav[aria-label='Pagination'] + ul/li (the Breadcrumbs landmark contract reused)"
    - "page item: Link (a href=?page=N) or Button (SPA); current = aria-current=page"
    - "prev/next controls: Button/Link, disabled at boundaries"
    - "first/last jump controls (optional double-chevron)"
    - "truncation ellipsis: <span aria-hidden=true> — INERT gap indicator, not a control"
    - "page-size Select ('10/25/50 per page')"
    - "range/status text 'Showing 1–10 of 200' (en-dash)"
    - "page-jump input (optional, Ant showQuickJumper)"
api:
  inherits:
    - "link + breadcrumbs (page items + nav[aria-label]+aria-current landmark contract)"
    - "button (prev/next/load-more controls)"
    - "select (rows-per-page picker)"
  props:
    - {name: page/current, type: number, description: "controlled active page (1-indexed)"}
    - {name: defaultPage, type: number, description: uncontrolled}
    - {name: onPageChange, type: function}
    - {name: count/pageCount, type: number, description: "TOTAL PAGES (MUI/Primer) — practice default for the simple pager"}
    - {name: total + pageSize, type: number, description: "TOTAL ITEMS + size (Ant/Carbon) — required for the enterprise pager to compute the 'M–N of T' range"}
    - {name: siblingCount, type: number, default: 1, description: pages either side of current}
    - {name: boundaryCount, type: number, default: 1, description: pages pinned at each end}
    - {name: pageSizeOptions + onPageSizeChange, type: "number[] / function", description: "rows-per-page Select; changing resets to page 1"}
    - {name: showFirstButton/showLastButton, type: boolean}
    - {name: renderItem/hrefBuilder/asChild, type: "function/slot", description: "THE Link-vs-button + router-polymorphism lever (inherits link asChild)"}
    - {name: mode, type: enum, values: [numbered, load-more], description: "load-more adds hasMore/onLoadMore/loading"}
  headless: "usePagination returns the item model {type: page|start-ellipsis|end-ellipsis|previous|next|first|last, page, selected, disabled}"
states:
  item: [rest, hover, focus-visible, "current (aria-current=page; ≥3:1 bg, ≥4.5:1 text)", "disabled (prev/next at boundary)"]
  ellipsis: "not a state — a non-control"
  boundary-disabled: "aria-disabled + pointer-events:none + JS prevent, NOT native disabled (which drops focus to <body> at the boundary)"
variants:
  numbered: "full truncated array — default for bounded sets"
  simple-prev-next: "just Previous/Next (+ optional 'Page N of M') — content/article paging (Polaris hasNext/hasPrevious)"
  full-table-pager: "page-size Select + range text + page-jump + numbers + prev/next — enterprise (Carbon/Ant)"
  load-more: "single block Button appending items — feeds"
  infinite-scroll: "intersection observer + foot-of-list spinner — restricted discovery feeds"
  compact-mobile: "collapse array to prev / 'Page N of M' / next (Apple HIG dots only for ≤10)"
accessibility:
  wcag-criteria: ["2.4.4", "4.1.2", "1.3.1", "4.1.3", "2.4.7", "1.4.3", "1.4.11"]
  no-apg-pattern: "APG has NO pagination pattern — composite: nav[aria-label] + ul/li + aria-current=page"
  landmark: "nav[aria-label='Pagination'] mandatory (else collides with primary nav in the rotor)"
  ellipsis: "INERT — aria-hidden=true (else 'dot dot dot'); the list already implies the gap"
  disabled: "aria-disabled NOT native disabled (focus-to-body trap at boundary)"
  keyboard: "TABBED, not roving — every control in normal tab order; arrows do NOT move between pages; Enter/Space activates"
  focus-on-change:
    real-href: "browser resets focus to top (native)"
    spa-buttons: "move focus to results region OR aria-live=polite 'Page N of M loaded' (else focus stranded on pager, content silently swaps)"
    load-more: "MOVE FOCUS TO FIRST NEW ITEM + announce 'N more loaded' (the most-missed rule)"
  names: "icon-only prev/next need 'Go to previous/next page'; links 'Go to page N' / 'Page N, current page'"
content:
  labels: "integers visible; full accessible names"
  range: "'Showing 1–10 of 200' (en-dash); degrade to 'Showing 1–10' when total unknown"
  compact: "'Page 3 of 20' / '3 / 20' — also the SR announcement string"
  page-size: "'Rows per page:' + integer options 10/25/50/100"
  controls: "'Previous'/'Next' (not Prev/Back/Forward); load-more 'Load more items'/'Show more results' (+ remaining count), never 'More'"
motion:
  minimal: "snappy; item hover/active ~100-150ms colour/opacity"
  layout-shift: "THE defect — digit-width jump (9->10->100); fix with font-variant-numeric: tabular-nums + reserved slot width (fixed-width, no-shift)"
  load-more: "new items fade-in + slight translate (signal downward growth), then focus moves in"
  infinite: "foot-of-list spinner/skeleton"
  reduce-motion: "drop fades; static 'Loading…'"
i18n:
  rtl: "sequence flips (page 1 right) + chevrons mirror (scaleX(-1) under [dir=rtl], not hardcoded SVG)"
  digits: "Intl.NumberFormat for locale numerals + grouping"
  range-string: "single interpolated translatable string (not concatenation); order customisable; ~40% expansion (flex + logical gap, no fixed text widths)"
  expansion: "labels grow — no fixed widths"
implementation:
  - "window algorithm: if pageCount <= boundaryCount*2 + siblingCount*2 + 3 render all; else leftSiblingIndex=max(page-siblingCount, boundaryCount+2), rightSiblingIndex=min(page+siblingCount, pageCount-boundaryCount-1), inject start/end-ellipsis on gaps; output 1 … 4 5 [6] 7 8 … 20; STABLE width (tabular-nums + reserved slots)"
  - "Link href=?page=N (bookmarkable/crawlable/middle-click, asChild router) vs Button for SPA-in-place; renderItem/hrefBuilder/asChild slot; NEVER href=# + onClick"
  - "SEO: rel=prev/next DEPRECATED by Google 2019 — every page must be a real crawlable <a href>; button+onClick is invisible to crawlers (verify; tag still valid HTML for non-Google agents)"
  - "aria-live=polite 'Page N of M' + focus mgmt (load-more focus-to-new-items is the most-missed)"
  - "infinite-scroll mitigations: load-more fallback after capped auto-appends + reachable footer + scroll/position restoration on back-nav; layer over a load-more/numbered base"
  - "headless usePagination (item model) + skinned render; some systems ship NO Pagination UI (React Aria useAsyncList composes from Link/Button)"
composition:
  stands-on: [link, breadcrumbs (nav landmark contract), button (controls), select (page-size), icon (chevrons)]
  hosted-by: [table/data-grid (enterprise pager), list, search-results, gallery]
  alternative-to: [tabs, stepper, carousel, infinite-scroll, "virtualized/windowed scrolling (useAsyncList — performant but a11y costs: SR-cursor tracking, broken find-in-page)"]
notes:
  contested:
    - "three-model default (numbered vs load-more vs infinite)"
    - "count (pages) vs total (items)+pageSize API"
    - "ellipsis inert (practice default) vs interactive jump"
    - "link vs button page items (URL change vs SPA)"
    - "focus-on-change strategy (keep-on-control vs move-to-results vs live-region)"
  trap:
    - "pure infinite scroll (footer-unreachable, keyboard-stranded, position/history loss)"
    - "load-more leaving focus on the button (drops keyboard users to reverse-tab)"
    - "native disabled on boundary prev/next (focus-to-body)"
    - "digit-width layout shift (needs tabular-nums)"
    - "button+onClick pagination invisible to crawlers"
    - "ellipsis exposed to AT ('dot dot dot')"
  inherited: "Link <a href>+aria-current+asChild + the Breadcrumbs nav landmark contract; Button controls; Select page-size"
  evolution: "infinite-scroll repudiated for load-more; rel=prev/next deprecated -> polymorphic crawlable links; monolithic -> headless usePagination (some ship no UI); focus-to-new-items rule"
  unverified:
    - "external-supplied 2026 version numbers (MUI v5/6, Carbon v11, Primer v36, Ant v5.19+, Polaris v12+, Base Web v13+, React Aria v3)"
    - "rel=prev/next current crawl state (Google 2019 deprecation — verify)"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-pagination/` (16 June 2026), the most reuse-heavy Navigation brief — it stands on Link + the Breadcrumbs nav-landmark contract (page items + `aria-current`), Button (prev/next/load-more), and Select (rows-per-page), inventing almost nothing. The two passes converged almost completely — the three-model decision (numbered for bounded/jumpable/bookmarkable sets, load-more as the safe feed default, infinite scroll restricted to casual discovery with a load-more fallback), the `siblingCount`/`boundaryCount` window algorithm with the inert `aria-hidden` ellipsis, the link-vs-button page-item rule via a `renderItem`/`asChild` slot, the `rel=prev/next` 2019 SEO deprecation (crawlable `<a href>` is now the only lever), the under-specified focus-on-page-change problem (keep-focus/live-region for numbered SPA, move-focus-to-first-new-item for load-more), the enterprise-table-pager vs simple-content-pager archetypes, the `aria-disabled`-not-native-`disabled` boundary handling, and `Pagination` as the naming default. External-pass contributions folded in: the `font-variant-numeric: tabular-nums` fix for the digit-width layout-shift defect, the MUI `usePagination` truncation formula (the `boundaryCount*2 + siblingCount*2 + 3` threshold and the sibling-index math), the `count`(pages)-vs-`total`(items)+`pageSize` API divergence, `Intl.NumberFormat` for locale digits, the graceful range-text degradation when the total is unknown, virtualized/windowed scrolling (`useAsyncList`) as the data-heavy alternative with its own a11y costs, and the placement-at-bottom + conditional-unmount rules. Claude-pass contributions: the framing as the most reuse-heavy brief, the explicit tabbed-not-roving keyboard note, and the no-APG-pattern observation as the reason it inherits rather than invents. The 2026 version numbers and the `rel=prev/next` current crawl state are flagged unverified. Conformant to `components/_schema.md`. Continues the Navigation category alongside Tabs, Accordion, Breadcrumbs, and Link.*
