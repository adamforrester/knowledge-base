# Section — field-truth study (Claude pass)

## 1. Framing
A Section is the **semantic document region** — the fifth and final Layout brief, the one that **closes the Layout category**, and the **semantic counterpart to Card's visual surface**. Where Card is a styled *object* (chrome: background, border, radius, elevation), a Section is a *meaning-bearing region* of the document — a **landmark** + a **heading-level contract** — usually with **no chrome at all**. Card answers "this content is a bounded visual unit"; Section answers "this content is a named, navigable part of the page's structure."

Three things define it and are where systems diverge (and why many systems don't ship a "Section" at all — that's itself a finding):
- **The nameless-section / landmark contract (the headline + the a11y crux).** An HTML `<section>` is **only a landmark** (`role="region"`, navigable by AT landmark navigation) **when it has an accessible name** (an `aria-labelledby` pointing at its heading, or `aria-label`). A **nameless `<section>` is a generic container with zero landmark value** — the single most common Section misuse (wrapping everything in `<section>` for "semantics" that does nothing). A Section *earns* its landmark by having a name.
- **The heading-level contract + the document-outline-algorithm myth (the load-bearing point).** HTML5 *promised* sectioning elements would auto-compute heading levels (an `<h1>` inside a `<section>` rendering as an h2 in the outline) — but **no browser ever implemented it**, and it was **removed from the spec**. So heading levels are *not* automatic; a flat sea of `<h1>`s "fixed by the outline" is broken for assistive tech. The answer is manual level discipline (h1→h2→h3) and/or a **heading-level context** (a Section provides an auto-incrementing level to nested headings).
- **The genre split — semantic Section vs visual/layout "section".** The *semantic* Section (a landmark + heading-level context) vs the *visual* page band (a full-bleed background with a constrained, centered content column — the marketing-page section), which pairs with a **Container** (the max-width content primitive).

It stands on **Box** (inheriting the polymorphic `as`/`asChild` Slot — rendering `<section>`/`<article>`/`<aside>`/`<div>` — the spacing-token scale, the zero-runtime delivery, and the logical-property RTL — see box), **composes Stack** (the section header + body) and **hosts Grid/Card** (a grid of Cards — see stack, grid, card), and is the **semantic counterpart to Card** (the boundary Card already drew from its side — see card). What it *isn't*: a **Card** (a visual chrome surface — Section is about *meaning*, not chrome), a **Box** (a neutral *non-semantic* container — Box has no landmark/heading role), or a **default wrapper** (the sharp rule: **`<div>` is fine; don't reach for `<section>` by default** — most groupings carry no landmark value). Why systems disagree: whether to ship a `Section` at all (vs semantic HTML + a `Container` + a heading discipline), and how to model the heading-level context.

## 2. Anatomy and parts
- **the sectioning element** — the rendered tag (`<section>`/`<article>`/`<aside>`/`<div>` via `as`); the choice *is* the semantics (§ the sectioning-element decision). Default to `<div>` unless the region earns a landmark.
- **the section header** — the heading (the accessible name + the landmark label) + optional description + section-level actions (e.g., "Settings" / "Manage your account" / an Edit button). The header is what makes the region a *named* landmark.
- **the body** — the content: typically a **Stack** (header + content stacked) and/or a **Grid of Cards** (see stack, grid, card).
- **the (visual variant) full-bleed background + constrained content** — *optional*: a background color/image spanning the viewport edge-to-edge with a centered max-width content column inside (the marketing-page band — §11).
- **the (absence of) chrome by default** — a semantic Section has *no* background/border/elevation; it's pure document structure. Chrome means it's a **Card** (see card). The visual band is the one exception, and even there the chrome is the *background*, not a bounded surface.

## 3. Properties / API
- **`as`** — the sectioning element: `section` / `article` / `aside` / `div` (inherited from Box's polymorphism). The most consequential prop — it *is* the semantics (§6).
- **the accessible name** — `aria-labelledby` (pointing at the header heading's id, the preferred form) or `aria-label` (when there's no visible heading). Without one, a `<section>` is *not* a landmark (§6). A well-designed Section auto-wires `aria-labelledby` to its header heading.
- **`headingLevel` / the heading-level context** — the level for the section's heading (or, better, an auto-incrementing **context** so nested Sections deepen the level automatically — §11). The load-bearing API for correct headings.
- **the header slot** — `Section.Header` (heading + description + actions), or `title`/`description`/`actions` props for the simple case.
- **the visual variant** — `fullBleed` / `background` (the edge-to-edge band) + **`maxWidth`** (the constrained content column) — or a separate **`Container`** primitive the Section wraps (§10).
- **`padding` / spacing** — the section's block spacing (from the spacing scale); the rhythm between sections.
- **`asChild`** — inherited from Box (merge onto a consumer element).
- **what it withholds** — no chrome (that's Card), no interaction (it's a container), and crucially it does *not* force a landmark — a Section without a name renders a plain element, by design.

## 4. States and variants
- **States: none.** Section is a semantic/layout container — no interaction states (inherits Box's statelessness).
- **Variants:**
  - **semantic:** `region` (a named `<section>`) / `article` (self-contained) / `complementary` (`<aside>`) / **generic** (a `<div>` — no landmark, the common default).
  - **visual:** plain (no chrome — the default) / **full-bleed band** (background spans the viewport) / **constrained** (a max-width content column).
  - **with/without a header** (the header is what supplies the landmark name).
  - **the rendered element:** `section` / `article` / `aside` / `div`.

## 5. Usage guidance
- **Use a Section (as a named landmark) for:** a *major, navigable* part of the page that benefits from AT landmark navigation and a heading — a distinct content area a screen-reader user would want to jump to ("Search results", "Account settings", "Related articles"). The signal: it has a heading *and* it's significant enough to be a navigation target.
- **Don't reach for `<section>` by default (the sharp rule):** most groupings are **`<div>`s** — a `<section>` without a name does nothing for AT and a page littered with nameless sections is just `<div>`s with extra characters. **`<div>` is the right default**; promote to `<section>`/`role=region` only when the region earns a *name* and a *landmark*.
- **Section vs the alternatives:**
  - **vs Card** — Card is a *visual* bounded object (chrome); Section is a *semantic* region (meaning, usually no chrome). A page *region* is a Section; a content *unit* with a surface is a Card (a Section often contains a Grid of Cards — see card).
  - **vs Box/Stack** — Box/Stack are neutral, non-semantic layout; reach for them when there's no landmark/heading meaning. A Section adds *document semantics* on top.
  - **vs `main`/`nav`/`aside`/`header`/`footer`** — those are the *specific* landmarks (one `<main>` per page; `<nav>` → see side-navigation; `<aside>` for tangential; `<header>`/`<footer>` for banner/contentinfo). `<section>`/`region` is the *generic* labelled landmark for anything that isn't one of those.
- **The don't-over-landmark rule** — too many landmarks is noise: it defeats landmark navigation (the inverse over-semantic trap, cf. Divider's decorative-by-default and Banner's static-vs-dynamic role). Reserve landmarks for genuinely distinct, navigable regions; a typical page has a handful, not dozens.
- **The heading-level discipline** — every Section heading sits at the right level (h1 → h2 → h3, no skips); nesting a Section deepens the level. Use the heading-level context so this is automatic (§11).
- **The visual-section / Container case** — for marketing/landing bands (full-bleed background, constrained content), the Section (or a `Container`) handles the width constraint; the *semantics* still follow the same rules (a hero band is often just a `<div>`/`<section>` with a heading).

## 6. Accessibility
Section's whole reason to exist is accessibility semantics — and it has two load-bearing contracts.

- **The nameless-`<section>`-is-not-a-landmark rule.** A `<section>` exposes `role="region"` **only when it has an accessible name** — `aria-labelledby` referencing its heading's id (preferred: visible name = AT name), or `aria-label` (when there's no visible heading). **Without a name, `<section>` is a generic container** — no landmark, no AT navigation value. So a Section component must either *require/auto-wire a name* (from its header heading) or *render a plain `<div>`* when there's none — never emit a nameless `<section>` and pretend it's semantic.
- **The landmark model + don't-over-landmark.** The landmark roles: **`region`** (a named `<section>` — the generic one), **`main`** (the one main content region, one per page), **`complementary`** (`<aside>` — tangential), **`banner`** (`<header>` at the top level), **`contentinfo`** (`<footer>` at the top level), plus `navigation`/`search`/`form`. Landmarks let AT users jump between regions — but *too many* destroys that value (landmark noise). Reserve them for genuinely distinct, navigable areas.
- **The heading-level contract (the outline-algorithm reality).** The HTML5 document outline algorithm — which would have auto-leveled headings inside sectioning elements — **was never implemented by any browser and was removed from the spec**. So: headings do **not** auto-level; an `<h1>` inside three nested `<section>`s is *still an h1* to AT. The practice's answer: **manual level discipline** (h1 → h2 → h3, no skipped levels, one `<h1>` per page) and/or a **heading-level context** — a Section provides an incrementing level so a nested Heading/`<H>` renders the correct `<hN>` automatically (the react-headings / Heydon Pickering `<H>` pattern — §11). This is the single most-botched a11y aspect of sectioning.
- **The one-`<h1>` / one-`<main>` rules** — one top-level `<h1>` (the page title), one `<main>` landmark; Sections nest *below* those.
- **WCAG SCs:** **1.3.1** (info & relationships — the region/heading structure), **2.4.1** (bypass blocks — landmarks enable skipping), **2.4.6** (headings & labels — descriptive section headings), **2.4.10** (section headings — content is organized into labelled sections), **4.1.2** (name/role/value — the region's accessible name). Section is the brief where a11y *is* the component; there's almost nothing else to it.

## 7. Content guidelines
- **The section heading** — it's the **accessible name** of the landmark and the anchor of the outline; make it **specific** ("Billing history", not "Section") and a real heading at the right level. A landmark named by a vague heading is a landmark a screen-reader user can't use.
- **The description** — optional supporting text under the heading; not part of the accessible name (which is the heading alone).
- **The heading hierarchy** — don't skip levels (h2 → h4 is a 1.3.1 failure); nest levels with the structure. One `<h1>` per page.
- **Don't wrap everything in `<section>`** — the content rule mirroring the usage rule: a `<section>` per visual grouping, with no heading, is noise; reserve it for named, navigable regions.

## 8. Motion and transition
- Section ships **no motion of its own** — it's a semantic/layout container (like Box/Stack/Grid).
- **As a composition** — scroll-into-view and **scroll-snap** sections (full-page-band scrolling) are a *layout pattern* applied to Sections, not a Section feature; and in-page anchor navigation (`#section-id` jump links) targets Sections. The consumer adds these.
- **Reduce-motion** — any scroll-snap/scroll-behavior animation must respect `prefers-reduced-motion: reduce` (use `scroll-behavior: smooth` only under the no-preference query); Section itself is motion-neutral.

## 9. Internationalization
- **RTL is inherited from Box** — the section header layout (heading + actions), the padding, and any directional spacing use logical properties and mirror under `dir="rtl"` with no JS (the section actions flip to the leading edge — see box).
- **The heading/landmark name is translated** — `aria-label`/the heading text localizes; the landmark name a screen-reader user hears must be the translated heading, not a hardcoded English string.
- **The full-bleed background is direction-agnostic** (an edge-to-edge band has no side); only the *content layout* within the constrained column mirrors.

## 10. Naming
- **The field set (and the key finding: many systems don't ship a "Section"):** **`Container`** (MUI, Chakra, Bootstrap — the *constrained max-width* content column, the most common shipped primitive); **`PageLayout`** (GitHub Primer — `Header`/`Content`/`Pane`/`Footer` landmark regions; Atlassian — `Banner`/`TopNavigation`/`LeftSidebar`/`Main` slots); **`Layout` / `Layout.Section`** (Polaris — the page grouping); **`region`** (the ARIA role, not a component); **`Panel`** (an older alias, overlaps Card). Plain semantic HTML + a heading discipline is what many systems "use" instead of a Section component — that's the honest field state.
- **The practice's default — model two things:** a **`Section`** for the *semantic region* (renders the right sectioning element, auto-wires the name→landmark from its header heading, and provides the **heading-level context**), and a **`Container`** for the *constrained-width content column* (the max-width primitive). They compose (a full-bleed `Section` wraps a `Container`). Don't conflate them into one over-propped component — semantics (Section) and width-constraint (Container) are orthogonal concerns. The app-shell landmark regions are a **`PageLayout`** composed pattern (main/nav/aside/header/footer), not a generic Section.
- **Aliases to map:** Container, Region, PageLayout, Layout.Section, Panel, ContentBlock, Band.

## 11. Implementation notes
- **The `as` → sectioning element + the name→landmark wiring.** Render the `as` tag; if it's `<section>` (or `role="region"`), **auto-wire `aria-labelledby` to the header heading's id** (generate the id, point the section at it) — so the region is *named* without the consumer hand-wiring. If there's no header/name, **render a `<div>`** (don't emit a nameless `<section>`). This "name-or-downgrade" logic is the component's core value.
- **The heading-level context (over the dead outline algorithm).** Provide a React **context carrying the current heading level**; a Section *increments* it for its children; a `Heading`/`<H>` component reads the context and renders the correct `<hN>` (the react-headings / Heydon Pickering `<H>` pattern). So nesting Sections deepens headings *automatically and correctly* — the practical replacement for the outline algorithm that never shipped. The top-level `<h1>` is the page title; everything nests below.
- **The full-bleed-background / constrained-content CSS.** Two settled patterns: **(a) the grid breakout** — a page grid `grid-template-columns: minmax(1rem, 1fr) minmax(0, var(--content-max)) minmax(1rem, 1fr)` where content sits in the middle track and a full-bleed child spans `grid-column: 1 / -1` with its background edge-to-edge; **(b) the inner-container** — a full-width Section (background spans `100%`) wrapping a centered `Container` (`max-width` + `margin-inline: auto`) for the content. The inner-container pattern is simpler and the common default; the grid breakout is cleaner when *some* children bleed and others don't.
- **The don't-over-landmark lint** — a review/lint rule flagging nameless `<section>`s, excessive `role=region` count, and duplicate `<main>`s.
- **Inherit Box, don't re-derive** — the `as`/`asChild` Slot, the spacing-token scale, the zero-runtime delivery, and the logical-property RTL all come from Box (see box); Section adds the semantics + the heading-level context + the constrained-width concern.
- **Headless vs opinionated** — the name→landmark wiring and the heading-level context are the headless logic worth owning (they're pure semantics/a11y, no styling); the spacing and the max-width are theme. **Why a `Container` often suffices:** for many systems the only *visual* need is the max-width column, and the *semantics* are handled by hand-authored `<section>`/`<main>` + a heading discipline — so they ship `Container` and skip `Section`. The practice ships both because the heading-level context + name→landmark wiring are genuinely valuable and error-prone to hand-roll.

## 12. Related and alternative components
- **Stands on:** **Box** (the polymorphic `as`/`asChild` Slot — rendering the sectioning element — the spacing-token scale, the zero-runtime delivery, the logical-property RTL — see box).
- **Composes / hosts:** **Stack** (the section header + body content — see stack) and **Grid/Card** (a grid of Card content units — see grid, card).
- **Semantic counterpart to:** **Card** (Card = a visual bounded object with chrome; Section = a semantic region, usually no chrome — the boundary drawn from both sides; see card).
- **Landmark siblings:** **`main`** (the one main region), **`nav`** (navigation — see side-navigation), **`aside`** (complementary), **`header`/`footer`** (banner/contentinfo) — Section (`region`) is the *generic* labelled landmark; these are the *specific* ones, composed into a **PageLayout** app shell (relating to Grid's named-areas — see grid).
- **Relates to:** **Heading/Text** (the heading-level context drives the nested `<hN>`), and the **Container** / max-width primitive (the constrained-content alternative the practice ships alongside).
- **Alternative to:** a plain semantic `<div>` (the right default when there's no landmark value), a **Container** (when only the width constraint is needed, not the semantics), and a **PageLayout** (for the full app-shell landmark set).

(The semantic document region — the landmark + heading-level counterpart to Card's visual surface, and the brief that closes the Layout category. It stands on Box (the polymorphic sectioning element + the scale + the RTL), composes Stack and hosts Grid/Card, and is the semantic counterpart to Card. See box for the substrate, stack/grid/card for the content + the visual-object boundary, side-navigation for the nav landmark, heading for the heading-level context. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The document-outline-algorithm myth → its removal → manual levels → the heading-level context.** HTML5 promised auto-leveled headings inside sectioning elements; browsers never implemented it; the spec removed it. The field moved to *manual* heading-level discipline and then to the **heading-level-context component** (`<H>` / react-headings) — making nested headings correct by construction.
2. **The `<section>`-needs-a-name landmark settling.** The recognition that a nameless `<section>` is *not* a landmark (and that wrapping everything in `<section>` is a no-op) hardened into the name-or-downgrade rule.
3. **Landmark navigation raising region correctness.** As AT landmark navigation became widely used, correct (and *not over-used*) landmarks went from nice-to-have to a real navigation affordance — and the don't-over-landmark discipline followed.
4. **The full-bleed-background/constrained-content CSS pattern.** The grid-breakout and inner-container patterns settled the long-awkward "full-width background, centered content" marketing-layout problem.
5. **Many systems ship Container/PageLayout, not Section.** The honest field state: the *visual* need (max-width column) is a `Container`, the *app-shell* need is a `PageLayout`, and the *semantics* are often hand-authored HTML + a heading discipline — so a standalone "Section" component is the exception, not the rule. The practice ships `Section` (for the heading-level context + name→landmark value) deliberately, not by default.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- GitHub Primer — `PageLayout` (`Header`/`Content`/`Pane`/`Footer` landmark regions).
- Shopify Polaris — `Page` + `Layout` + `Layout.Section`; `BlockStack`.
- Atlassian — `PageLayout` (`Banner`/`TopNavigation`/`LeftSidebar`/`Main` landmark slots).
- MUI — `Container` (the max-width constrained content; no Section).
- Chakra UI — `Container`; `as="section"`.
- Bootstrap — `Container` (the constrained-width lineage).
- Adobe Spectrum / React Aria — the landmark utilities (`useLandmark`, landmark navigation); the `View`.
- IBM Carbon — the grid + semantic sectioning.
- Google Material 3 — the layout regions.
- Heading-level context — react-headings; Heydon Pickering's `<H>` / heading-level-context pattern; the abandoned HTML5 document outline algorithm.
- WAI-ARIA — landmark roles (`region`/`complementary`/`main`/`banner`/`contentinfo`); the `<section>`-needs-a-name rule; the heading-outline reality.
- WCAG 2.2 — 1.3.1, 2.4.1, 2.4.6, 2.4.10, 4.1.2.

## 15. Agent-consumable schema
```yaml
identity:
  id: section
  name: Section
  aliases: [Container, Region, PageLayout, Layout.Section, Panel, ContentBlock, Band]
  category: layout
  status: stable
description: >
  The semantic document REGION — a landmark + a heading-level contract, the SEMANTIC
  counterpart to Card's VISUAL surface (Card = a styled chrome object; Section = a
  meaning-bearing region, usually NO chrome) — and the brief that CLOSES the Layout
  category. NOT a Card (a visual surface), NOT a Box (a neutral NON-semantic container),
  NOT a default wrapper (<div> is fine — don't reach for <section> by default). Stands
  on Box (the polymorphic as/asChild Slot rendering section/article/aside/div, the
  spacing scale, the styling delivery, the logical-property RTL); composes Stack (the
  header+body) and hosts Grid/Card. The two load-bearing contracts: a nameless <section>
  is NOT a landmark, and heading levels are NOT automatic (the outline algorithm never
  shipped).
anatomy:
  parts:
    - "the sectioning element: the rendered tag (section/article/aside/div via as) — the choice IS the semantics; default to div unless the region earns a landmark"
    - "the section header: the heading (the accessible name + landmark label) + optional description + section-level actions — what makes the region a NAMED landmark"
    - "the body: a Stack (header + content) and/or a Grid of Cards"
    - "the (visual variant) full-bleed background + constrained content: optional — a background spanning the viewport + a centered max-width content column (the marketing band)"
    - "the (absence of) chrome by default: a semantic Section has NO bg/border/elevation (chrome = a Card); the visual band's chrome is the background, not a bounded surface"
api:
  inherits:
    - box        # the as/asChild Slot (renders the sectioning element), the spacing-token scale, the zero-runtime delivery, the logical-property RTL
  composes: [stack]            # the section header + body
  hosts: [grid, card]          # a grid of Card content units
  props:
    - {name: as, type: "'section'|'article'|'aside'|'div'", default: div, required: false, description: "THE sectioning element — it IS the semantics; default div unless the region earns a landmark"}
    - {name: accessible-name, type: "aria-labelledby | aria-label", default: ~, required: false, description: "aria-labelledby -> the header heading id (preferred; visible name = AT name) or aria-label; WITHOUT it a <section> is NOT a landmark"}
    - {name: headingLevel / heading-level-context, type: "number | context", default: "auto (context)", required: false, description: "the heading level; BETTER an auto-incrementing context so nested Sections deepen the level automatically (the <H>/react-headings pattern) — the replacement for the dead outline algorithm"}
    - {name: "header slot (Section.Header)", type: "slot | title/description/actions props", default: ~, required: false, description: "heading + description + section-level actions; supplies the landmark name"}
    - {name: "visual variant (fullBleed/background + maxWidth/Container)", type: "boolean + token", default: plain, required: false, description: "the edge-to-edge band + the constrained content column (or a separate Container the Section wraps)"}
    - {name: padding/spacing, type: "token-scale", default: ~, required: false, description: "the section's block spacing / inter-section rhythm"}
    - {name: asChild, type: boolean, default: false, required: false, description: "inherited from Box — merge onto a consumer element"}
  withholds: "no chrome (that's Card), no interaction, and does NOT force a landmark — a nameless Section renders a plain element by design"
states:
  runtime: []   # NONE — a semantic/layout container; inherits Box's statelessness
variants:
  semantic: [region, article, complementary, generic]   # named <section> / <article> / <aside> / <div> (no landmark — the common default)
  visual: [plain, full-bleed-band, constrained]
  header: [with-header, headerless]
  rendered-element: [section, article, aside, div]
accessibility:
  inherits: [box (the element it renders via as is the semantics)]
  wcag-criteria: ["1.3.1", "2.4.1", "2.4.6", "2.4.10", "4.1.2"]
  nameless-section-rule: "a <section> exposes role=region ONLY with an accessible name (aria-labelledby -> its heading, or aria-label); WITHOUT a name it's a GENERIC container, no landmark (the most common misuse). A Section must NAME-or-DOWNGRADE: auto-wire the name from its header heading, or render a plain <div>"
  landmark-model: "region (named <section> — the generic one) / main (one per page) / complementary (<aside>) / banner (<header>) / contentinfo (<footer>) / navigation / search / form"
  dont-over-landmark: "too many landmarks = noise that defeats landmark navigation (the inverse over-semantic trap, cf. Divider/Banner); reserve for genuinely distinct navigable regions — a handful per page, not dozens"
  heading-level-contract: "the HTML5 document OUTLINE ALGORITHM (auto-leveling headings in sectioning elements) was NEVER implemented + was REMOVED from the spec — so headings do NOT auto-level (an h1 in 3 nested sections is STILL an h1 to AT). Answer: manual discipline (h1->h2->h3, no skips, one h1/page) AND/OR a heading-level CONTEXT (a Section increments the level for nested Heading/<H>)"
  one-h1-one-main: "one top-level h1 (the page title), one <main>; Sections nest below"
content:
  section-heading: "the ACCESSIBLE NAME of the landmark + the outline anchor — SPECIFIC ('Billing history' not 'Section'), a real heading at the right level"
  description: "optional supporting text under the heading; NOT part of the accessible name (the heading alone is)"
  hierarchy: "don't skip levels (h2->h4 fails 1.3.1); nest levels with the structure; one h1/page"
  dont-wrap-everything: "a <section> per visual grouping with no heading is noise; reserve for named navigable regions (<div> is the default)"
motion:
  own: none   # a semantic/layout container, ships no animation
  composition: "scroll-into-view / scroll-snap sections + in-page anchor (#id) jump links are LAYOUT PATTERNS applied to Sections, not Section features; the consumer adds them"
  reduce-motion: "any scroll-snap/scroll-behavior:smooth must respect prefers-reduced-motion; Section itself is motion-neutral"
i18n:
  rtl-inherited: "the section header (heading + actions), padding, and directional spacing use logical properties + mirror under dir=rtl with no JS (actions flip to the leading edge); inherited from Box"
  name-translated: "the aria-label/heading text localizes — the landmark name a SR user hears must be the translated heading, not a hardcoded English string"
  full-bleed-direction-agnostic: "an edge-to-edge band has no side; only the content layout within the constrained column mirrors"
implementation:
  - "the as -> sectioning element + the name->landmark wiring: render the as tag; if <section>/role=region, AUTO-WIRE aria-labelledby to the header heading's id (generate it, point the section at it) so the region is named without hand-wiring; NO header/name -> render a <div> (never a nameless <section>). This name-or-downgrade logic is the component's core value"
  - "the heading-level CONTEXT (over the dead outline algorithm): a React context carrying the current level; a Section increments it for children; a Heading/<H> reads it + renders the correct <hN> (react-headings / Heydon Pickering <H>). Nesting Sections deepens headings automatically + correctly; the top-level h1 is the page title"
  - "the full-bleed-background/constrained-content CSS: (a) the GRID BREAKOUT — a page grid minmax(1rem,1fr) minmax(0,var(--content-max)) minmax(1rem,1fr), content in the middle track, a full-bleed child spans grid-column:1/-1; (b) the INNER-CONTAINER — a full-width Section wrapping a centered Container (max-width + margin-inline:auto). Inner-container is simpler/common; grid-breakout when SOME children bleed"
  - "the don't-over-landmark lint: flag nameless <section>s, excessive role=region count, duplicate <main>s"
  - "inherit Box, don't re-derive: the as/asChild Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL; Section adds the semantics + the heading-level context + the constrained-width concern"
  - "headless vs opinionated: the name->landmark wiring + the heading-level context are the headless logic worth owning (pure a11y, no styling); spacing + max-width are theme. WHY A CONTAINER OFTEN SUFFICES: many systems' only visual need is the max-width column + hand-authored semantics, so they ship Container + skip Section; the practice ships both because the heading-level context + name-wiring are valuable + error-prone to hand-roll"
composition:
  stands-on: [box]
  composes: [stack]                        # the header + body
  hosts: [grid, card]                      # a grid of Card content units
  semantic-counterpart-to: [card]          # visual object (chrome) vs semantic region (meaning)
  landmark-siblings: [main, "nav (see side-navigation)", aside, header, footer]   # the specific landmarks; region is the generic one; composed into a PageLayout app shell
  relates-to: ["heading (the heading-level context)", "container (the max-width alternative)"]
  alternative-to: ["a plain semantic <div> (the default when no landmark value)", container, "PageLayout (the app-shell landmark set)"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "ship a Section at all? — many systems ship Container (max-width) + PageLayout (app shell) + hand-authored semantics instead; the practice ships Section for the heading-level context + name->landmark value, deliberately not by default"
    - "the heading level: manual discipline vs a heading-level CONTEXT (practice: the context — correct by construction)"
    - "semantic Section vs visual/Container — model as TWO primitives (Section for semantics + Container for width — practice) vs one over-propped component"
    - "Section vs PageLayout for the app-shell landmark regions (PageLayout = the composed pattern)"
  trap:
    - "the NAMELESS <section> (no landmark value — the most common misuse; name-or-downgrade)"
    - "relying on the document OUTLINE ALGORITHM for heading levels (it never shipped; headings don't auto-level)"
    - "over-landmarking (too many region/section = landmark noise); reaching for <section> by default instead of <div>"
    - "skipping heading levels (h2->h4); multiple h1s / multiple <main>s"
    - "putting chrome on a Section (that's a Card); a vague heading naming a landmark a SR user can't use"
  inherited: "Box's as/asChild Slot, the spacing-token scale, the zero-runtime styling delivery, the logical-property RTL"
  role-in-family: "the semantic document region — the landmark + heading-level counterpart to Card's visual surface; the brief that CLOSES the Layout category; stands on Box, composes Stack, hosts Grid/Card, the semantic counterpart to Card"
  evolution:
    - "the document-outline-algorithm myth -> its removal -> manual heading levels -> the heading-level-context component (<H>/react-headings)"
    - "the <section>-needs-a-name landmark settling (name-or-downgrade)"
    - "landmark navigation raising region correctness + the don't-over-landmark discipline"
    - "the full-bleed-background/constrained-content CSS pattern (grid-breakout / inner-container)"
    - "many systems shipping Container/PageLayout, not Section (the honest field state)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "per-system Container/PageLayout/Section coverage + the heading-level-context library state (react-headings etc.)"
    - "the exact removal date of the HTML5 outline algorithm from the spec — verify"
```
