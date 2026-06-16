# Pagination — field-truth study (Claude pass)

## 1. Framing
Pagination splits a large result set into navigable chunks and gives the user a way to move between them and a sense of *where they are* in the whole. It reuses more of the catalogue than any brief so far: the **page-number items inherit Link** and the **`nav[aria-label="Pagination"]` + list landmark contract Breadcrumbs established** (page items as Links + `aria-current="page"` — see link, breadcrumbs), the **prev/next/load-more controls inherit Button** (see button), and the **rows-per-page picker inherits Select** (see select). What's genuinely Pagination-specific — and what the field actually fights over — is the **three-model decision**, the **truncation/window algorithm**, the **link-vs-button** page-item rule, and the badly-under-specified **focus-on-page-change** problem.

**The defining framing is the three-model choice:**
- **Numbered pagination** (discrete page links 1 2 … N) — for **known/bounded, jumpable, bookmarkable** sets: search results, data tables, admin lists. The user can jump to page 7, deep-link to it, and sense the total.
- **Load-more** (a Button that appends the next chunk) — for **feeds where depth is open** but you want keyboard/footer access preserved and explicit user control.
- **Infinite scroll** (auto-load on scroll) — for **casual discovery feeds only**, and with serious accessibility costs (keyboard users stranded, the footer becomes permanently unreachable, focus loss, no sense of position/total, lost scroll position on back-nav).

What it *isn't*: **Tabs** (a fixed small set of peer views, not chunks of one ordered set), a **Stepper** (a linear flow with completion state — see breadcrumbs §boundaries), or a **Carousel** (paged *content*, not paged *results*). Why systems disagree: which of the three models is the default, the truncation algorithm, whether page items are links or buttons, the enterprise-table-pager vs. simple-content-pager split, and focus/announcement on page change.

## 2. Anatomy and parts
- **nav landmark + list** — `<nav aria-label="Pagination">` wrapping an `<ol>`/`<ul>` of items (the Breadcrumbs landmark contract reused; the label disambiguates it from other navs).
- **page-number item** — a **Link** (`<a href="?page=N">`) when the URL changes, or a Button in SPA mode (§3); the **current page** carries `aria-current="page"` and is typically non-interactive or visually distinct.
- **prev / next controls** — Buttons or Links ("‹"/"›" or "Previous"/"Next"); **disabled at the boundaries** (first page → prev disabled; last page → next disabled).
- **ellipsis / overflow indicator** — the "…" for collapsed page ranges; **inert by default** (a gap indicator, not a control — §6).
- **page-size / rows-per-page select** — a Select ("10 / 25 / 50 per page") — the enterprise-table pattern (§3, see select).
- **range / status text** — "Showing 1–10 of 200" / "Page 3 of 20" (a live-region-friendly summary, §6).
- **page-jump input** — a "Go to page [ ]" number field (Ant/Carbon enterprise pattern; optional).

## 3. Properties / API
- **`count` / `total` + `pageSize`** — the total item/page count driving the range. (Or `pageCount` directly.)
- **`page` / `defaultPage` + `onPageChange`** — controlled/uncontrolled current page (1-indexed by convention).
- **`siblingCount` / `boundaryCount`** (MUI's vocabulary) — the window algorithm: `boundaryCount` pages pinned at each end (default 1 → always show first + last), `siblingCount` pages either side of the current page (default 1), ellipsis filling the gaps (§11).
- **`pageSize` + `pageSizeOptions` + `onPageSizeChange`** — the rows-per-page Select (changing it usually resets to page 1).
- **`showFirstButton` / `showLastButton`** — jump-to-first/last controls.
- **render-item / `renderItem`** (or `asChild` per item) — **the slot that decides Link vs Button** and lets a page item render a framework-router Link (inherits Link's `asChild`, §11).
- **`mode`** — numbered vs. load-more (a `hasMore` + `onLoadMore` + `loading` shape for the load-more archetype).
- Headless **`usePagination`** (MUI/React Aria-style) returns the computed item list (`{type: 'page'|'ellipsis'|'previous'|'next'|'first'|'last', page, selected, disabled}`) for full render control.

## 4. States and variants
- **Item states:** rest / hover / focus-visible / **current** (`aria-current="page"`, distinct style) / **disabled** (prev/next at boundaries; the inert ellipsis is not a state, it's a non-control).
- **Variants:**
  - **Numbered** (full truncated list) — the default for bounded sets.
  - **Load-more** (a single Button appending the next chunk) — feeds.
  - **Infinite scroll** (auto-load) — discovery feeds, with the a11y mitigations (§11).
  - **Simple prev/next** (just "‹ Previous / Next ›", optionally "Page 3 of 20") — content/article paging (Polaris-style).
  - **Full table pager** (page-size Select + range text + page-jump + prev/next + numbers) — the enterprise/Carbon archetype.
  - **Compact / mobile** — collapse to prev / "3 of 20" / next.

## 5. Usage guidance
- **The three-model framework (the headline decision):**
  - **Numbered** when the set is **bounded and the user benefits from jumping, deep-linking, or sensing the total** — search results, tables, admin. Bookmarkable and crawlable.
  - **Load-more** when depth is **open-ended but you must keep keyboard access, the footer reachable, and user control** — most "feed" cases. The safest default for content feeds.
  - **Infinite scroll** **only** for casual, endless discovery feeds where the footer is irrelevant and position doesn't matter (social timelines, image galleries) — and even then, provide a load-more fallback and a reachable footer. Never for search results, tables, or anything with a footer the user needs (checkout, settings, contact). It is an accessibility liability by default.
- **Enterprise-table pager vs. simple content pager** — a data table wants the **full pager** (page-size, range text, jump, numbers); an article/blog or a short list wants the **minimal prev/next** (numbers add noise). Match the archetype to the host.
- **Don't use Pagination for:** a small fixed set of peer views (→ Tabs), a linear flow (→ Stepper), or paged marketing content (→ Carousel).

## 6. Accessibility
- **Structure:** `<nav aria-label="Pagination">` + a list, page items as Links with **`aria-current="page"`** on the current page (the Breadcrumbs/Link nav contract reused). **WAI-ARIA APG has no dedicated pagination pattern** — pagination *is* a labelled nav of links + `aria-current`, which is why it inherits rather than invents.
- **The inert ellipsis** — the "…" gap indicator is **not interactive** and not announced as a control (a `<span aria-hidden="true">` or a list item with no actionable role); making it a focusable "jump" is a non-standard enhancement, not the default.
- **Disabled prev/next at boundaries** — prev on page 1 / next on the last page are disabled; use `aria-disabled` + non-actionable (or omit) rather than a focus trap; don't leave a dead-but-focusable control silently doing nothing.
- **Focus management on page change (the under-specified problem, and the part most systems get wrong):**
  - **Numbered (in-place/SPA update):** after activating a page, **keep focus on the activated control** (it persists if the control still exists) and **announce the change via a live region** ("Page 3 of 20" in an `aria-live="polite"` status) so a screen-reader user knows the content swapped. Moving focus to the top of the results region is the alternative when the activated control disappears.
  - **Load-more:** **move focus to the first newly-loaded item** (so keyboard users continue from where the new content begins instead of being dropped at the top or stranded on a button that may vanish) and announce "N more loaded."
  - **Full page navigation (real `?page=N` href):** the browser loads a new page; normal focus reset applies (consider focusing the results heading).
- **Icon-only prev/next** need accessible names ("Go to previous page" / "Go to next page"); page-number links benefit from "Go to page N" / "Page N, current page" names so they're meaningful out of context.
- **WCAG SCs:** 2.4.4 (link purpose — meaningful control names), 4.1.2 (name/role/value), 1.3.1 (the nav/list structure), 4.1.3 (status messages — the live-region announcement), 2.4.7 (focus visible), plus Link's and Button's inherited SCs.

## 7. Content guidelines
- **Page-number labels** are the numbers; give links a full accessible name ("Go to page 4", "Page 4, current page").
- **Range/status text** "Showing 1–10 of 200" (or "1–10 of 200 results") is the most useful orientation cue — prefer it over a bare "Page 3 of 20" for tables; localise the dash and order (§9).
- **Rows-per-page** label "Rows per page" / "Items per page"; keep the options sane (10/25/50/100).
- **Prev/Next** "Previous"/"Next" (or icon + visually-hidden name); avoid "<<"/">>" as the only label.
- **Load-more** "Load more" / "Show more results" (not "More") + optionally the remaining count ("Load 20 more").

## 8. Motion and transition
Minimal. Numbered pagination swaps content with no required animation (a brief cross-fade of the results region is optional; avoid a layout jump — reserve the pager's width). **Load-more appends** the next chunk below with a short fade-in of the new items (then focus moves into them, §6). Infinite scroll shows a loading spinner/skeleton at the foot of the list. Under `prefers-reduced-motion: reduce`, drop fades and snap. The pager itself must be **fixed-width / no-layout-shift** as the current page moves through the range (the truncation algorithm holds the width — §11). (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** flips the whole sequence (page 1 on the right) and **mirrors the prev/next chevrons** (prev points right); logical properties + the nav landmark handle layout, but the chevron glyphs must mirror (like Breadcrumbs' separator).
- **Number formatting** — page numbers and the "of 200" total should respect locale digit systems (Arabic-Indic, Devanagari) and grouping separators.
- **"M–N of T" string** — the dash, order, and word "of"/"results" are localised; don't concatenate ("Showing" + range + "of" + total) — use a single interpolated, translatable string with placeholders.
- **Text expansion** — "Rows per page", "Previous"/"Next", "Load more" expand; don't fix their widths. (See 13-internationalization-and-rtl.)

## 10. Naming
**`Pagination`** is the near-universal component name (MUI, Carbon, Polaris, Primer, Atlassian, Ant, Base Web); **`Pager`** is the older alias. Sub-parts: `PaginationItem` / `Pagination.Item`, prev/next, ellipsis. **The practice default: `Pagination`** (container) with a headless `usePagination` returning the item model, page items rendered as Links via a `renderItem`/`asChild` slot, and a `loadMore` mode (or a separate `LoadMore` control) for the feed archetype. Aliases: `Pager`, `PaginationNav`, `TablePagination` (the enterprise variant).

## 11. Implementation notes
- **The window/truncation algorithm** — compute the visible item list from `page`, `pageCount`, `siblingCount`, `boundaryCount`: always render `boundaryCount` pages at each end, `siblingCount` pages either side of `page`, and an **ellipsis where there's a gap > 1**. The classic output is `1 … 4 5 [6] 7 8 … 20`. Guard the edge cases (current near an end collapses one ellipsis; small counts show all pages with no ellipsis) and keep the rendered **width stable** so the control doesn't reflow as the user pages — reserve slots. A headless `usePagination` (MUI) is the clean way to ship this logic separately from rendering.
- **Link vs. button rendering** — page items that change the URL render a real **`<a href="?page=N">`** (bookmarkable, crawlable, middle-clickable — inherits Link + `asChild` for the framework router, see link); client-only SPA pagination that mutates state in place renders **Buttons**. The `renderItem`/`asChild` slot is what lets the same component do both. Don't ship `href="#"` + onClick.
- **SEO / `rel="prev"`/`"next"`** — **Google deprecated `rel=prev/next` as an indexing signal (2019)**; it's no longer required for crawl, though it remains valid HTML and some other agents use it. The real SEO lever is **crawlable `<a href>` page links** (not button/onClick pagination). (Current-platform-state — verify; flag unverified.)
- **Focus + live region** — wire an `aria-live="polite"` status node announcing "Page N of M" on change; manage focus per §6 (keep-on-control for numbered, **move-to-first-new-item for load-more** — the most-missed rule).
- **Infinite-scroll mitigations** — if infinite scroll is unavoidable: provide a **load-more button fallback**, keep the **footer reachable** (don't auto-load forever before it), preserve **scroll/position on back-navigation**, announce new content, and consider a "you've reached page N" anchor. Treat infinite scroll as an enhancement layered over a load-more/numbered base, not a replacement.
- **Headless vs. opinionated** — `usePagination` (MUI/React Aria-style) for the item model + a skinned render is the practice default; note that **some systems ship no Pagination component at all** (React Aria/Spectrum compose it from Link/Button) — a signal that pagination is "a labelled nav of links + a window algorithm," not a novel widget.

## 12. Related and alternative components
- **Stands on:** Link + the Breadcrumbs nav-landmark contract (page items + `aria-label` + `aria-current` — see link, breadcrumbs), Button (prev/next/load-more — see button), Select (rows-per-page — see select), Icon (chevrons — see icon).
- **Hosted by:** Table (the primary host of the enterprise pager — see table when briefed), List, search-results and gallery layouts.
- **Alternative to / boundary with:** Tabs (fixed peer views, not chunks of one set — see tabs), Stepper (linear flow with completion — see breadcrumbs boundary), Carousel (paged content, not paged results), and **infinite scroll** (the pattern pagination is the accessible alternative to).
- **Composes:** the load-more Button and the page-size Select are the reused controls; the page item is a Link.

(The most reuse-heavy brief so far — it invents almost nothing, standing on Link/Breadcrumbs (items + nav contract), Button (controls), and Select (page-size), and contributing the three-model decision, the window algorithm, and the focus-on-page-change rule. See link/breadcrumbs for the nav contract, button for the controls, select for the page-size picker, table for the primary host. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **`rel=prev/next` deprecated** as a Google indexing signal (2019) — crawlable `<a href>` page links, not the link-rel hints, are what matter now (current-platform-state — verify).
2. **Load-more over infinite scroll for accessibility** — the field has hardened against pure infinite scroll (footer-unreachable, keyboard-stranded, position-loss) and toward load-more or numbered as the accessible default, with infinite scroll reserved for casual feeds.
3. **Headless `usePagination`** converged — separating the window/truncation algorithm from rendering (MUI), so the same logic drives Link-based and Button-based pagers.
4. **The focus-to-new-items rule for load-more** gained recognition as the fix for the "click load-more, get dropped to the top / stranded" failure.
5. **Some systems ship no Pagination component** (React Aria) — reflecting that it's a composition of briefed primitives, not a novel widget.

## 14. Sources cited
(Conservative; reconcile with external.) **MUI** `Pagination`/`usePagination`/`TablePagination` (count, siblingCount, boundaryCount, the item model, renderItem) (2024–2026); **IBM Carbon** `Pagination` (page-size select, range text, page jump — the enterprise table pager) (2024–2026); **Shopify Polaris** `Pagination` (minimal prev/next) (2024–2026); **GitHub Primer** `Pagination` (truncation/margin/surround) (2024–2026); **Atlassian** `Pagination` (2024–2026); **Ant Design** `Pagination` (jumper, size-changer — the most complete) (2024–2026); **Base Web (Uber)** `Pagination` (2024); **Google Material 3** (no strong pagination pattern; table footer) (2024); **Adobe React Aria / Spectrum** — *no dedicated Pagination component* (composed from Link/Button) — itself a finding (2024–2026); **WAI-ARIA APG** — no formal pagination pattern (nav + links + `aria-current`); **Google Search Central** — `rel=prev/next` deprecation (2019). WCAG 2.2 (Oct 2023) — 2.4.4, 4.1.2, 1.3.1, 4.1.3, 2.4.7, plus Link/Button SCs.

## 15. Agent-consumable schema (conform to _schema.md in pagination.md)
identity(Pagination; aliases Pager/PaginationNav/TablePagination; navigation; stable)/description(splits a large result set into navigable chunks + conveys position; three models numbered|load-more|infinite; NOT tabs (peer views), NOT stepper (linear flow), NOT carousel (paged content); the accessible alternative to infinite scroll)/anatomy(nav[aria-label=Pagination]+list; page item=Link; current marker aria-current=page; prev/next controls (disabled at boundaries); inert ellipsis; page-size Select; range/status text 'Showing M–N of T'; optional page-jump input)/api(inherits: link+breadcrumbs (items + nav contract), button (controls), select (page-size); count/total+pageSize; page/defaultPage+onPageChange; siblingCount/boundaryCount window; pageSizeOptions/onPageSizeChange; showFirst/Last; renderItem/asChild = Link-vs-button slot; mode numbered|load-more (hasMore/onLoadMore/loading); headless usePagination returns item model)/states(item rest/hover/focus/current(aria-current=page)/disabled(prev-next at boundary); ellipsis is a non-control; variants numbered/load-more/infinite/simple-prev-next/full-table-pager/compact-mobile)/accessibility(nav[aria-label]+list, aria-current=page; APG has NO pagination pattern — it IS nav+links+aria-current; inert ellipsis (not a control); disabled prev/next at boundaries; FOCUS-ON-CHANGE — numbered: keep focus on control + live-region 'Page N of M'; load-more: MOVE FOCUS TO FIRST NEW ITEM + announce 'N more loaded'; icon-only controls need names 'Go to previous page'; SC 2.4.4/4.1.2/1.3.1/4.1.3/2.4.7)/content(numbers w/ full names 'Go to page N'; 'Showing M–N of T' range as the orientation cue; 'Rows per page' 10/25/50/100; Previous/Next not <<; 'Load more'+remaining count)/motion(minimal; numbered content swap optional cross-fade no layout jump; load-more append fade-in then focus into; infinite spinner/skeleton; reduce-motion snaps; pager FIXED-WIDTH no-shift)/i18n(RTL sequence flip + chevron mirror; locale digits + grouping; 'M–N of T' single interpolated translatable string not concatenation; text expansion on labels)/implementation(window algorithm from page/pageCount/siblingCount/boundaryCount + ellipsis-on-gap, stable width; Link href=?page=N (bookmarkable/crawlable, asChild router) vs Button for SPA, never href=# +onClick; rel=prev/next deprecated by Google 2019 — crawlable <a> is the lever; aria-live 'Page N of M' + focus mgmt (load-more focus-to-new-items is the most-missed); infinite-scroll mitigations: load-more fallback + reachable footer + restore scroll on back; headless usePagination, some systems ship NO Pagination (React Aria composes from Link/Button))/composition(stands-on link+breadcrumbs nav contract, button controls, select page-size, icon chevrons; hosted-by table/list/search-results; alternative-to tabs, stepper, carousel, infinite-scroll)/notes(contested: three-model default (numbered vs load-more vs infinite); ellipsis inert vs jump; link-vs-button page items; focus-on-change strategy. trap: pure infinite scroll (footer-unreachable, keyboard-stranded, position-loss); load-more dropping focus to top; ellipsis as a dead focusable control; layout shift as current page moves. inherited: Link <a href>+aria-current+asChild, the breadcrumbs nav landmark contract, Button controls, Select page-size. evolution: rel=prev/next deprecated; load-more over infinite for a11y; headless usePagination; focus-to-new-items rule; some systems ship no component. unverified: external 2026 version numbers; rel=prev/next current crawl state.)
