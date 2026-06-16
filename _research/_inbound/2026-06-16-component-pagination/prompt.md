You are researching the Pagination component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what
pagination is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Pagination is a Navigation-category brief that STANDS ON three already-
briefed substrates:
- THE PAGE-NUMBER ITEMS + NAV LANDMARK inherit LINK and the Breadcrumbs
  pattern (components/link.md, components/breadcrumbs.md): a
  <nav aria-label="Pagination"> wrapping a list, page items as Links when
  they change the URL (?page=2) with aria-current="page" on the current
  page. Don't re-derive Link's <a href> contract, the underline
  discipline, or the asChild router polymorphism — reference them as
  inherited. Reuse the nav[aria-label]+list landmark contract Breadcrumbs
  established.
- THE PREV / NEXT / LOAD-MORE CONTROLS inherit BUTTON
  (components/button.md): prev/next are controls disabled at the
  boundaries; load-more is a Button. Don't re-derive Button; note the
  link-vs-button decision (URL-changing page items are Links; SPA
  pagination that doesn't change the URL uses Buttons).
- THE PAGE-SIZE / ROWS-PER-PAGE PICKER inherits SELECT
  (components/select.md). Don't re-derive Select.

THE DEFINING PAGINATION-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE THREE-MODEL DECISION (the defining framing): numbered pagination
  (discrete page links) vs. load-more (a button that appends) vs. infinite
  scroll (auto-load on scroll). Resolve the framework for when each
  applies — numbered for known/bounded, jumpable, bookmarkable result
  sets (search results, tables, admin); load-more for feeds where order
  matters but depth is open; infinite scroll for casual discovery feeds
  ONLY, with its serious accessibility costs (keyboard users stranded, the
  footer becomes unreachable, focus loss, no sense of position). State the
  practice's default and the boundaries.
- THE TRUNCATION / WINDOW ALGORITHM for numbered pagination — the
  1 … 4 5 [6] 7 8 … 20 pattern: always show first + last (boundaryCount),
  a window of siblings around the current page (siblingCount), and an
  ELLIPSIS for the gap. Resolve whether the ellipsis is inert (a gap
  indicator, the practice default) or an interactive jump; the
  fixed-width / no-layout-shift requirement; the mobile collapse (prev /
  current-of-total / next).
- LINK vs BUTTON for page items — URL-changing, bookmarkable, crawlable
  pagination uses Links (real ?page=N hrefs, inherits Link + asChild);
  client-only/SPA pagination that mutates state in place uses Buttons.
  Resolve the rule and the SEO/crawlability dimension (rel=prev/next is
  deprecated by Google — note the current state).
- FOCUS MANAGEMENT ON PAGE CHANGE (the under-specified a11y problem):
  after activating a page link / prev / next / load-more, WHERE does focus
  go and WHAT is announced? Resolve: numbered — keep focus on the
  activated control or move to the results region + announce "Page N of M"
  via a live region; load-more — move focus to the first newly-loaded item
  (so keyboard users aren't dropped to the top) and announce "N more
  loaded"; the disabled-prev/next-at-boundary focus trap.
- THE ENTERPRISE TABLE PAGER vs THE SIMPLE CONTENT PAGER — the dense
  table pattern (page-size Select + "Showing 1–10 of 200" range/status
  text + page input/jump + prev/next, Carbon-style) vs. the minimal
  prev/next content pager (Polaris-style). Resolve the two archetypes and
  what each needs.
- ACCESSIBILITY — nav[aria-label="Pagination"] + list, aria-current="page"
  on the current page, the inert ellipsis, disabled-at-boundary prev/next,
  the live-region announcement, accessible names for icon-only prev/next
  ("Go to previous page"), and the note that WAI-ARIA APG has no formal
  pagination pattern (it is nav + links + aria-current).
- CONTENT — "Page X of Y", the "Showing M–N of T" range text, rows-per-
  page label, prev/next labels, the load-more label.

Field-leader systems to survey (web): MUI (Pagination — count,
siblingCount, boundaryCount, the ellipsis, usePagination), IBM Carbon
(Pagination — page-size select + range text + page jump, the enterprise
table pattern), Shopify Polaris (minimal prev/next Pagination), GitHub
Primer (Pagination — truncation), Atlassian Design System (Pagination),
Ant Design (the most complete pagination — jumper, size-changer),
Base Web (Uber) (Pagination), Google Material 3. Note where a system has
NO dedicated Pagination component (e.g. React Aria / Spectrum builds it
from Link/Button) — that absence is itself a finding. WAI-ARIA APG (the
no-formal-pattern note). Mobile reference where relevant: Apple HIG (page
controls / dots), Material 3. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for Link/Breadcrumbs (page items + nav
contract), Button (controls), and Select (page-size); flag unverified
claims under notes.unverified).

1. Framing — what it is, what it isn't; the three-model decision up front;
   why systems disagree.
2. Anatomy and parts — nav landmark + list, page-number item (Link),
   current marker, prev/next controls, ellipsis/overflow indicator,
   page-size select, range/status text, page-jump input.
3. Properties / API — count/total, page/defaultPage (controlled),
   onPageChange, siblingCount/boundaryCount, pageSize +
   pageSizeOptions/onPageSizeChange, showFirstLast, the render-item slot
   (Link vs button), load-more vs numbered mode.
4. States and variants — item states (rest/hover/focus/current/disabled);
   numbered vs. load-more vs. infinite; simple-prev/next vs. full table
   pager; compact/mobile.
5. Usage guidance — the three-model framework (numbered / load-more /
   infinite) and when each; the enterprise-table vs. content-pager
   archetypes; the boundaries.
6. Accessibility — nav[aria-label]+list, aria-current=page, inert
   ellipsis, disabled prev/next, focus management on page change, the
   live-region announcement, icon-only control names, the no-APG-pattern
   note, WCAG SCs.
7. Content guidelines — page-number labels, "Showing M–N of T", "Page X of
   Y", rows-per-page, prev/next + load-more labels.
8. Motion and transition — minimal; the content swap / load-more append;
   reduce-motion; infinite-scroll loading indicator.
9. Internationalization — RTL (prev/next + sequence flip, chevron mirror),
   number formatting/locale digits, "M–N of T" string order, text
   expansion.
10. Naming — Pagination / Pager; item names; the practice's default;
    aliases.
11. Implementation notes — the window/truncation algorithm, Link-vs-button
    rendering (inherits asChild), the rel=prev/next deprecation + SEO,
    focus management + live region, load-more focus-to-new-items, the
    infinite-scroll accessibility mitigations (a load-more fallback,
    reachable footer), headless (usePagination) vs opinionated.
12. Related and alternative components — typed relationships (Link +
    Breadcrumbs nav contract, Button controls, Select page-size, Table as
    the primary host, Tabs/Stepper boundaries, the infinite-scroll
    pattern).
13. Field POV evolution — recent shifts (rel=prev/next deprecation,
    load-more-over-infinite-scroll for a11y, headless usePagination).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what pagination is — explain the
numbered/load-more/infinite three-model decision, the truncation/window
(siblingCount/boundaryCount + inert ellipsis) algorithm, the link-vs-button
page-item rule (and the rel=prev/next/SEO state), the focus-management-on-
page-change problem (and load-more's focus-to-new-items rule), and the
enterprise-table-pager vs simple-content-pager archetypes that field
leaders diverge on.
