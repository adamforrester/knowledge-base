---
okf_version: "0.1"
type: component-brief
title: Section
description: The semantic document region and the brief that closes the Layout category — a field-truth study of the nameless-section landmark contract (a nameless <section> maps to role=generic, not a landmark; name-or-downgrade), the heading-level contract + the document-outline-algorithm myth (it never shipped, removed 2022–2025; manual levels or the heading-level <H> context), the semantic-Section-vs-visual/Container genre split, the sectioning-element decision tree (section/article/aside/main/div — div is the default, don't over-section), the full-bleed-background/constrained-content CSS (the grid-breakout over the 100vw-scrollbar negative-margin hack), and the don't-over-landmark rule — standing on Box, the semantic counterpart to Card, with the practice's defaults.
tags: [components, layout]
category: Layout
status: stable
aliases: [Container, Region, PageLayout, Layout.Section, Panel, ContentBlock, Band]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Section

> A Section is the **semantic document region** — the fifth and final Layout brief, the one that **closes the Layout category**, and the **semantic counterpart to Card's visual surface**. Where Card is a styled *object* (chrome: background, border, radius, elevation), a Section is a *meaning-bearing region* of the document — a **landmark** + a **heading-level contract** — typically with **no chrome at all**. Card answers "this is a bounded visual unit"; Section answers "this is a named, navigable part of the page's structure." It stands on **Box** (inheriting the polymorphic `as`/`asChild` Slot — rendering `<section>`/`<article>`/`<aside>`/`<div>` — the spacing-token scale, the zero-runtime delivery, and the logical-property RTL — see box), **composes Stack** (the section header + body) and **hosts Grid/Card** (a grid of Cards — see stack, grid, card), and is the **semantic counterpart to Card** (the boundary Card already drew from its side — see card). Two often-misunderstood web-platform realities define it: the **nameless-section landmark contract** — a `<section>` *without an accessible name* maps to `role="generic"` (functionally a `<div>`), so it earns its `region` landmark only by being *named*; and the **document-outline-algorithm myth** — HTML5 promised sectioning elements would auto-compute heading levels, but **no browser implemented it** and it was **removed from the spec (final removals ~2022–May 2025)**, so heading levels are *not* automatic. What it *isn't*: a **Card** (a visual chrome surface — Section is about *meaning*, not chrome), a **Box** (a *non-semantic* container), or a **default wrapper** (the sharp rule: **`<div>` is fine; don't reach for `<section>` by default**). Why systems disagree — and why many don't ship a "Section" at all: the *visual* need is a **Container** (max-width), the *app-shell* need is a **PageLayout**, and the *semantics* are often hand-authored HTML + a heading discipline.

---

## 1. Framing
A Section is the definitive semantic boundary in the layout taxonomy — the close of the continuum Box → Stack → Grid → Card → Section. The industry's fragmentation here is driven by a historical conflation of **semantics** and **visual layout**: systems either ship purely-visual `Container`s and ignore the semantic contract, or over-engineer semantic wrappers that flood the accessibility tree with landmark noise. The practice draws strict boundaries.

Three things define it (and explain why many systems don't ship one):
- **The nameless-section / landmark contract (the headline + the a11y crux).** Per the HTML Accessibility API Mappings, a `<section>` *without an accessible name* is exposed as **`role="generic"`** — functionally identical to a `<div>`, zero landmark value. It earns `role="region"` (navigable by AT landmark navigation) **only with a name** (an `aria-labelledby` pointing at its heading, or `aria-label`). Wrapping everything in nameless `<section>`s — the single most common misuse — does *nothing* for AT.
- **The heading-level contract + the document-outline-algorithm myth.** HTML5 *promised* sectioning elements would auto-level headings (an `<h1>` nested in `<section>`s becoming an h2/h3 in the outline). **No browser ever implemented it; it was removed from the spec (~2022–May 2025).** So headings do *not* auto-level — a flat sea of `<h1>`s "fixed by the outline" is broken for AT. The answer: manual discipline and/or a **heading-level context** (§6/§11).
- **The genre split — semantic Section vs visual/Container.** The *semantic* Section (a landmark + heading-level context) vs the *visual* page band (a full-bleed background + a constrained content column), which pairs with a **Container** (the max-width primitive). The practice models these as *two* primitives.

What it *isn't*: a **Card** (visual chrome — see card), a **Box** (`role=generic`, no semantics — see box), or a **default wrapper** (`<div>` is the right default — don't over-section). Why systems disagree: whether to ship a `Section` at all, and how to model the heading-level context.

## 2. Anatomy and parts
Section's anatomy is structural — semantic nodes and layout boundaries, not pixels. No background/border/shadow by default (the contrast with Card):
- **the sectioning element (root)** — the rendered tag (`<section>`/`<article>`/`<aside>`/`<main>`/`<div>` via `as`); the choice *is* the semantics, and it carries the ARIA attributes for landmark synthesis. Default to `<div>` unless the region earns a landmark.
- **the section header (slot)** — the semantic anchor: a **heading** (the accessible name / landmark label), an optional **description**, and optional **section-level actions** ("View all", "Edit", "Manage" — aligned inline-end). The header is what makes the region a *named* landmark; it labels the region so a screen-reader user knows its purpose before entering.
- **the body (slot)** — the content: typically a **Stack** (linear flow of header + content) and/or a **Grid** of **Cards** (see stack, grid, card); agnostic to its children.
- **the (visual variant) full-bleed background** — *optional*: a surface treatment ignoring parent padding to span the viewport edge-to-edge (alternating bands, hero imagery).
- **the (visual variant) constrained content column** — *optional*: an inner boundary arresting horizontal expansion at an optimal reading width (~60–80 characters), preventing typography from over-extending on ultrawide displays.
- **the (absence of) chrome by default** — a semantic Section has no chrome; chrome means it's a **Card** (see card). The visual band's only "chrome" is the *background*, not a bounded surface.

## 3. Properties / API
The API enforces accessibility invariants while giving layout flexibility:
- **`as`** — the sectioning element: `section` / `article` / `aside` / `main` / `div` (inherited from Box's polymorphism). The most consequential prop — it *is* the semantics (§6); `main` is valid but **one per page** (§6).
- **`title`** (string | node) — the human-readable heading rendered in the header; the component **auto-generates a unique id and wires `aria-labelledby`** to the root, so the region is *named* without hand-wiring (§11).
- **`aria-label`** — an invisible accessible name; the fallback when the landmark is needed but `title` is omitted (no visible heading).
- **`headingLevel`** (1–6) — the explicit heading rank; **overrides** the auto-incrementing context when manual control is needed. Better default: the **context** (§11).
- **`variant`** — `plain` (default flow, no chrome) / `full-bleed` (viewport-spanning background + constrained inner track) (§4).
- **`maxWidth`** (token) — constrains the inner content column (mapped to width tokens `sm`/`md`/`lg` or a character measure `60ch`); often delegated to a separate **Container** (§10).
- **the header slot / `actions`** — `Section.Header` (heading + description + actions), or `title`/`description`/`actions` props for the simple case; actions render inline-end opposite the title.
- **`padding` / spacing** — inherited from Box; the block/inline spacing and the inter-section rhythm.
- **`asChild`** — inherited from Box (merge onto a consumer element).
- **what it withholds** — no chrome (that's Card), no interaction, and crucially it does **not force a landmark**: with no `title`/`aria-label` it **degrades to a `<div>`** (or warns) rather than emitting a nameless `<section>` (§6/§11).

## 4. States and variants
- **States: none.** Section is a structural/semantic wrapper — no hover/focus/active/disabled (inherits Box's statelessness).
- **Variants, on two axes:**
  - **Semantic (the accessibility tree):** **region** (a *named* `<section>` — the default for a distinct named area) / **independent** (`<article>` — self-contained, syndicatable: a post, comment, card) / **complementary** (`<aside>` — tangential; → `role=complementary` when named) / **generic** (`<div>` — no landmark; the common default, prevents landmark noise).
  - **Visual (the render tree):** **plain** (no chrome, natural flow — the default) / **full-bleed band** (background breaks out to the viewport edges, content stays centered + constrained) / **constrained** (a pure max-width wrapper, the Bootstrap/MUI `Container` behavior — width without background).
  - **with/without a header** (the header supplies the landmark name).

## 5. Usage guidance
The recurring systemic failure is **over-application of `<section>`** — equating "visual grouping" with "semantic section", flooding the landmark rotor with trivial nodes. The decision tree:
- **A visually bounded object in a flow (a widget, a product tile, a task)?** → **Card**. Cards are *objects*; Sections are the *environments* that contain them (see card).
- **A major navigable region with a thematic shift and a distinct heading (a screen-reader user would want to jump to it — "Billing history", "Security settings")?** → **Section** (named, `role=region`).
- **Just a layout wrapper for spacing/alignment/background?** → **Box/`<div>`**. Don't use `<section>` to apply padding or a background token (see box).
- **vs the specific landmarks** — `<main>` (one per page), `<nav>` (→ see side-navigation), `<aside>` (complementary), `<header>`/`<footer>` (banner/contentinfo): `<section>`/`region` is the *generic* labelled landmark for anything that isn't one of those.
- **The don't-over-landmark rule (the load-bearing one):** every named Section is appended to the landmark navigation list. A marketing page with twelve product benefits each wrapped in a named `<section>` creates **twelve landmarks** — severe landmark noise. The correct structure is **one** named `<section>` ("Product benefits") containing a **Grid of twelve generic `<div>`s/Cards**. (The inverse over-semantic trap, cf. Divider's decorative-by-default and Banner's static-vs-dynamic role.)
- **The visual-band / semantics decoupling** — when a full-bleed band visually alternates content but is *not* a thematic shift, render it `as="div"`: decouple the visual band from the landmark weight (§11).
- **The heading-level discipline** — every Section heading at the right level (h2 → h3, no skips); nesting deepens the level. Use the heading-level context so this is automatic (§11).

## 6. Accessibility
Section's reason to exist *is* accessibility semantics — two absolute platform truths, both frequently misunderstood:

- **The nameless-`<section>` rule.** Per HTML-AAM, a `<section>` does **not** auto-map to `region` — *without* an accessible name it's exposed as **`role="generic"`** (a `<div>`). To elevate it: an accessible name via **`aria-labelledby` → the header heading's id** (preferred: visible name = AT name) or **`aria-label`**. A strict Section **automates this** (generates the heading id, wires `aria-labelledby` from `title`); with no name it **degrades to a `<div>`** or throws a dev-time warning — never silently ships an empty, non-functional landmark.
- **The heading-level contract (the outline-algorithm reality).** The HTML5 Document Outline Algorithm — author all `<h1>`s, let the browser compute the rank by nesting depth — was **never implemented** (it disrupted screen-reader scanning, which relies on *absolute* heading ranks, and vendors rejected it) and was **removed from the standard (~2022–May 2025)**. So an `<h1>` nested in three `<section>`s is *still an h1* to AT; a flat sea of `<h1>`s fails **WCAG 1.3.1** and **2.4.6**. The practice's answer: **manual discipline** (h2 → h3, no skips, one `<h1>`/page) and/or a **heading-level context** — a Section is a *level provider* that increments the context depth; a nested `Heading`/`<H>` reads it and renders the mathematically-correct `<hN>` (the Heydon Pickering `<H>` / react-headings pattern). Moving a Section to a deeper nesting then recomputes its headings automatically, zero refactor (§11).
- **The one-`<h1>` / one-`<main>` rules** — one top-level `<h1>` (the page title; Section headings begin at `<h2>`), one `<main>` landmark; Sections nest below.
- **Landmark navigation** — beyond native AT landmark rotors, utilities like React Aria's **`useLandmark`** polyfill **F6 / Shift+F6** keyboard cycling between landmarks (`banner`/`main`/`region`/`contentinfo`) and restore focus predictably when landmarks mount/unmount in SPAs.
- **WCAG SCs:** **1.3.1** (info & relationships — the region/heading structure), **2.4.1** (bypass blocks — landmarks enable skipping), **2.4.6** (headings & labels — descriptive section headings), **2.4.10** (section headings — content organized into labelled sections), **4.1.2** (name/role/value — the region's accessible name). Section is the brief where a11y *is* the component.

## 7. Content guidelines
- **The section heading** — it's the **accessible name** of the landmark and the outline anchor; AT users pull up landmark/heading lists *out of visual context*, so make it **specific** ("Billing history", "Shipping preferences", "User roles" — not "Content", "Details", "More information"). A real heading at the right level.
- **The description** — optional supporting text under the heading; **not** part of the accessible name (the heading alone is).
- **Don't skip levels** — no h2 → h4 (a 1.3.1 failure); the `<H>` context increments by exactly one. **One `<h1>` per page** (the document title); Section headings begin at `<h2>`.
- **Don't wrap everything** — paragraphs/lists/form fields in the main flow don't need a Section unless they're a distinct, *titled* subdivision; reserve `<section>` for named navigable regions.

## 8. Motion and transition
- Section ships **no motion of its own** — a semantic/layout wrapper (like Box/Stack/Grid). But it's the structural anchor for scroll interactions:
- **Scroll-into-view (hash navigation)** — Sections are the targets of in-page anchor links (`#billing-section`); support a **`scroll-margin-top`** token so the section heading isn't occluded by a fixed/sticky app-shell header when scrolled to.
- **Scroll-snap** — in marketing/carousel layouts, Sections act as `scroll-snap-align: start` children of a `scroll-snap-type` parent (presentation-style band scrolling).
- **Reduce-motion** — any entrance/scroll animation on a visual Section must respect `prefers-reduced-motion: reduce` (resolve to zero duration, appear instantly, no layout shift); `scroll-behavior: smooth` only under the no-preference query. Section itself is motion-neutral.

## 9. Internationalization
- **RTL is inherited from Box** — padding/margin/border use **logical properties** (`padding-inline`, `margin-inline-start`), so the section header (title inline-start, actions inline-end) mirrors automatically under `dir="rtl"` (Arabic/Hebrew) with no JS (see box).
- **The full-bleed background is direction-agnostic** — because the breakout relies on **CSS Grid tracking** (not explicit left/right negative margins), the band stays correct regardless of reading direction (§11); only the *content layout* within the constrained column mirrors.
- **Translated landmark names** — the `title`/`aria-label` must hook into the i18n dictionary so the landmark name a screen-reader user hears matches their localized language, not a hardcoded English string.

## 10. Naming
- **The field set (and the key finding: many systems don't ship a "Section"):** **`Container`** (MUI, Chakra, Bootstrap — the *constrained max-width* content column, the most common shipped primitive; "visual/width" focus, ignoring semantics); **`PageLayout`** (GitHub Primer — `Header`/`Content`/`Pane`/`Footer` *landmark slots*, rejecting a generic Section for explicit app-shell regions; Atlassian — `Banner`/`TopNavigation`/`LeftSidebar`/`Main`); **`Layout` / `Layout.Section`** / **`s-section`** (Polaris — a card-like grouping with a heading, distinct from `s-box`); **`region`** (the ARIA role, not a component); **`Panel`** (an older alias, overlaps Card); the **`Grid`** (Carbon — semantic sectioning atop row/column). Plain semantic HTML + a heading discipline is what many "use" instead — the honest field state.
- **The practice's default — model two orthogonal primitives:** a **`Section`** for the *semantic region* (renders the right sectioning element, auto-wires the name→landmark from its header heading, provides the **heading-level context**) and a **`Container`** for the *constrained-width content column* (the max-width primitive). **Compose them** — `<Section><Container>…</Container></Section>` — so a full-bleed Section can hold a beautifully constrained inner track. Don't conflate them into one over-propped component: semantics (Section) and width-constraint (Container) are orthogonal. The app-shell landmark set is a **`PageLayout`** composed pattern (`main`/`nav`/`aside`/`header`/`footer`), not a generic Section.
- **Aliases to map:** Container, Region, PageLayout, Layout.Section, Panel, ContentBlock, Band.

## 11. Implementation notes
- **The `as` → sectioning element + the name→landmark wiring.** Render the `as` tag; if it's `<section>` (or `role="region"`), **auto-wire `aria-labelledby` to the header heading** — generate the id with **`useId()`** (not hand-typed, which is typo-brittle), render the heading with that id, point the section at it. With no `title`/`aria-label`, **render a `<div>`** (or warn). This "name-or-downgrade" logic is the component's core value:
  ```jsx
  const Section = ({ as: Comp = 'section', title, ariaLabel, children }) => {
    const id = useId();
    const headingId = title ? `${id}-heading` : undefined;
    return (
      <Comp aria-labelledby={headingId} aria-label={!title ? ariaLabel : undefined}>
        {title && <H id={headingId}>{title}</H>}
        {children}
      </Comp>
    );
  };
  ```
- **The heading-level context (over the dead outline algorithm).** A React **`LevelContext`** carrying the current level; a Section increments it (**capped at 6** to avoid invalid `<h7>` — `Math.min(level + 1, 6)`); a `Heading`/`<H>` reads the context and renders the correct `<hN>`. Nesting Sections deepens headings automatically and correctly — moving a Section into a deeper nesting recomputes its headings with **zero JSX refactor**. The top-level `<h1>` is the page title; Sections begin at `<h2>`.
- **The full-bleed-background / constrained-content CSS (and why grid-breakout beats negative margins).** The legacy `width: 100vw` + `margin-inline: calc(50% - 50vw)` hack **triggers a horizontal scrollbar on Windows** because `100vw` *includes* the scrollbar width. The modern **CSS Grid breakout** solves it mathematically with no scrollbar side-effect — a named-line track grid where children default to the constrained center track and full-bleed children opt into the edge track:
  ```css
  .section-breakout {
    display: grid;
    grid-template-columns:
      [full-start] minmax(var(--page-gutter), 1fr)
      [content-start] minmax(0, var(--max-content-width))
      [content-end] minmax(var(--page-gutter), 1fr) [full-end];
  }
  .section-breakout > *            { grid-column: content; }  /* constrained by default */
  .section-breakout > .full-bleed  { grid-column: full;    }  /* opts into the edges */
  ```
  The simpler **inner-container** pattern (a full-width Section wrapping a centered `Container` with `max-width` + `margin-inline: auto`) is the common default; the grid breakout is cleaner when *some* children bleed and others don't.
- **The don't-over-landmark lint** — a review/lint rule flagging nameless `<section>`s, excessive `role=region` count, and duplicate `<main>`s.
- **Inherit Box, don't re-derive** — the `as`/`asChild` Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL all come from Box (see box); Section adds the semantics + the heading-level context + the constrained-width concern.
- **Headless vs opinionated** — the name→landmark wiring and the heading-level context are the headless logic worth owning (pure a11y, no styling); spacing and max-width are theme. **Why a `Container` often suffices:** many systems' only *visual* need is the max-width column, with semantics hand-authored — so they ship `Container` and skip `Section`. The practice ships **both** because the heading-level context + name→landmark wiring are genuinely valuable and error-prone to hand-roll.

## 12. Related and alternative components
- **Stands on:** **Box** (the polymorphic `as`/`asChild` Slot rendering the sectioning element, the spacing-token scale, the zero-runtime delivery, the logical-property RTL — see box).
- **Composes / hosts:** **Stack** (the section header + body, linear flow — see stack) and **Grid/Card** (a grid of Card content units — see grid, card).
- **Semantic counterpart to:** **Card** (Card = a visual bounded object with chrome; Section = a semantic region, usually no chrome — the strict boundary, drawn from both sides; see card).
- **Landmark siblings:** **`main`** (the one main region), **`nav`** (navigation — see side-navigation), **`aside`** (complementary), **`header`/`footer`** (banner/contentinfo) — Section (`region`) is the *generic* labelled landmark; these are the *specific* ones, composed into a **PageLayout** app shell (relating to Grid's named-areas — see grid).
- **Relates to:** **Heading/Text** (the heading-level context drives the nested `<hN>`), and the **Container** / max-width primitive (the constrained-content companion the practice ships alongside).
- **Alternative to:** a plain semantic `<div>` (the right default when there's no landmark value), a **Container** (when only the width constraint is needed), and a **PageLayout** (for the full app-shell landmark set).

(The semantic document region — the landmark + heading-level counterpart to Card's visual surface, and the brief that **closes the Layout category**. It stands on Box, composes Stack, hosts Grid/Card, and is the semantic counterpart to Card. See box for the substrate, stack/grid/card for the content + the visual-object boundary, side-navigation for the nav landmark, heading for the heading-level context. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The document-outline-algorithm myth → its removal → manual levels → the heading-level context.** The early-HTML5 era (~2010–2015) saw `<section>`s populated with all-`<h1>`s on the assumption the browser would compute depth; when accessibility APIs exposed them as a flat list of `<h1>`s (destroying navigability), the field corrected violently to *manual* level mapping, and then to the **heading-level-context component** (`<H>` / react-headings) — building the failed algorithm in user-land, correctly. The algorithm was officially removed from the standard (~2022–May 2025).
2. **The `<section>`-needs-a-name landmark settling.** The W3C clarified (HTML-AAM) that a `<section>` requires an accessible name to graduate from `generic` to `region` — forcing mature systems to integrate automatic `aria-labelledby` wiring and ending the "wrap everything in `<section>`" no-op.
3. **Landmark navigation raising region correctness + the don't-over-landmark discipline.** As AT landmark navigation became widely used, correct (and *not over-used*) landmarks became a real navigation affordance; React Aria's **`useLandmark`** (F6/Shift+F6 + focus restoration) elevated the Section from a static tag to a programmatic navigation anchor.
4. **The full-bleed-background/constrained-content CSS pattern.** The CSS Grid breakout displaced the brittle `100vw` negative-margin hack (and its Windows scrollbar bug), finally decoupling the semantic document tree from the visual full-bleed requirement.
5. **Many systems ship Container/PageLayout, not Section.** The honest field state: the *visual* need is a `Container`, the *app-shell* need is a `PageLayout`, the *semantics* are often hand-authored HTML + a heading discipline — so a standalone "Section" is the exception. The practice ships `Section` (for the heading-level context + name→landmark value) *and* `Container`, deliberately. (Polaris's recent shift to framework-agnostic web components — `s-section`/`s-page` — is the same composional turn, flagged unverified.)

## 14. Sources cited
(Conservative; reconcile with external.) **W3C HTML & ARIA** — HTML-AAM (`<section>` → `role=generic` without an accessible name → `region` with one; ARIA 1.2/1.3 landmark roles); the **removal of the Document Outline Algorithm** from the HTML standard (~2022–May 2025); WCAG 2.2 — 1.3.1, 2.4.1, 2.4.6, 2.4.10, 4.1.2. **GitHub Primer** — `PageLayout` (`Header`/`Content`/`Pane`/`Footer` landmark regions; v37.x) (2024–2026); **Shopify Polaris** — `Layout`/`Layout.Section` → `s-section`/`s-page` (the React→web-component shift; v2025-10–v2026-04) (2024–2026); **Atlassian** — `PageLayout` (`Banner`/`TopNavigation`/`LeftSidebar`/`Main` landmark slots) (2024–2026); **MUI** — `Container` (the max-width primitive; no Section) (2024–2026); **Chakra UI** — `Container`; `as="section"` (2024–2026); **Bootstrap** — `Container` (the constrained-width lineage); **Adobe React Aria** — `useLandmark` (F6/Shift+F6 landmark navigation + SPA focus restoration; 2026) (2024–2026); **IBM Carbon** — the grid + semantic sectioning; **Google Material 3** — the layout regions; **Heading-level context** — react-headings, Heydon Pickering's `<H>` / heading-level-context pattern. WAI-ARIA — landmark roles (`region`/`complementary`/`main`/`banner`/`contentinfo`).

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
  category. NOT a Card (a visual surface), NOT a Box (role=generic, non-semantic),
  NOT a default wrapper (<div> is fine — don't reach for <section> by default).
  Stands on Box (the polymorphic as/asChild Slot rendering section/article/aside/div,
  the spacing scale, the styling delivery, the logical-property RTL); composes Stack
  and hosts Grid/Card. Two load-bearing platform truths: a nameless <section> maps to
  role=generic (NOT a landmark), and heading levels are NOT automatic (the outline
  algorithm never shipped, removed ~2022-2025).
anatomy:
  parts:
    - "the sectioning element (root): the rendered tag (section/article/aside/main/div via as) — the choice IS the semantics + carries the ARIA attrs; default to div unless the region earns a landmark"
    - "the section header (slot): the heading (the accessible name + landmark label) + optional description + optional section-level actions (inline-end) — makes the region a NAMED landmark"
    - "the body (slot): a Stack (linear flow) and/or a Grid of Cards"
    - "the (visual variant) full-bleed background: a surface ignoring parent padding to span the viewport edge-to-edge"
    - "the (visual variant) constrained content column: an inner max-width boundary (~60-80ch) preventing over-extension on ultrawide"
    - "the (absence of) chrome by default: no bg/border/shadow (chrome = a Card); the visual band's chrome is the background, not a bounded surface"
api:
  inherits:
    - box        # the as/asChild Slot (renders the sectioning element), the spacing-token scale, the zero-runtime delivery, the logical-property RTL
  composes: [stack]            # the section header + body
  hosts: [grid, card]          # a grid of Card content units
  props:
    - {name: as, type: "'section'|'article'|'aside'|'main'|'div'", default: section, required: false, description: "THE sectioning element — it IS the semantics; main is valid but ONE per page; default div unless the region earns a landmark"}
    - {name: title, type: "string | node", default: ~, required: false, description: "the heading rendered in the header; the component AUTO-GENERATES a unique id (useId) + wires aria-labelledby to the root — names the landmark without hand-wiring"}
    - {name: aria-label, type: string, default: ~, required: false, description: "an invisible accessible name; the fallback when the landmark is needed but title is omitted"}
    - {name: headingLevel, type: "1-6", default: "context-derived", required: false, description: "explicit heading rank; OVERRIDES the auto-incrementing context when manual control is needed (better default: the context)"}
    - {name: variant, type: "'plain' | 'full-bleed'", default: plain, required: false, description: "plain (no chrome, natural flow) / full-bleed (viewport-spanning background + constrained inner track)"}
    - {name: maxWidth, type: "token | measure", default: auto, required: false, description: "constrains the inner content column (sm/md/lg or 60ch); often delegated to a separate Container"}
    - {name: "header slot / actions", type: "slot | title/description/actions props", default: ~, required: false, description: "heading + description + section-level actions (inline-end); supplies the landmark name"}
    - {name: padding/spacing, type: "token-scale", default: ~, required: false, description: "inherited from Box; block/inline spacing + inter-section rhythm"}
    - {name: asChild, type: boolean, default: false, required: false, description: "inherited from Box — merge onto a consumer element"}
  withholds: "no chrome (that's Card), no interaction, and does NOT force a landmark — with no title/aria-label it DEGRADES to a <div> (name-or-downgrade), never a nameless <section>"
states:
  runtime: []   # NONE — a structural/semantic wrapper; inherits Box's statelessness
variants:
  semantic: [region, article, complementary, generic]   # named <section> / <article> / named <aside> / <div> (no landmark — the common default)
  visual: [plain, full-bleed-band, constrained]
  header: [with-header, headerless]
  rendered-element: [section, article, aside, main, div]
accessibility:
  inherits: [box (the element it renders via as is the semantics)]
  wcag-criteria: ["1.3.1", "2.4.1", "2.4.6", "2.4.10", "4.1.2"]
  nameless-section-rule: "per HTML-AAM a <section> WITHOUT an accessible name is exposed as role=GENERIC (a div), NOT a landmark; it earns role=region ONLY with a name (aria-labelledby -> its heading, or aria-label). A Section must NAME-or-DOWNGRADE: auto-wire the name from the header heading (useId), or render a <div> / dev-warn — never a silent empty landmark"
  landmark-model: "region (named <section> — the generic one) / main (one per page) / complementary (named <aside>) / banner (<header>) / contentinfo (<footer>) / navigation / search / form"
  dont-over-landmark: "every named Section is appended to the landmark list; 12 product benefits each in a named <section> = 12 landmarks = noise. CORRECT: ONE named <section> ('Product benefits') containing a Grid of 12 generic divs/Cards (the inverse over-semantic trap, cf. Divider/Banner)"
  heading-level-contract: "the HTML5 OUTLINE ALGORITHM (auto-leveling headings by nesting depth) was NEVER implemented (SRs rely on ABSOLUTE ranks; vendors rejected it) + was REMOVED from the standard (~2022-May 2025). Headings do NOT auto-level (an h1 in 3 nested sections is STILL an h1). Answer: manual discipline (h2->h3, no skips, one h1/page) AND/OR a heading-level CONTEXT (a Section increments the level for nested Heading/<H>)"
  landmark-navigation: "React Aria's useLandmark polyfills F6/Shift+F6 cycling between landmarks + restores focus when landmarks mount/unmount in SPAs"
  one-h1-one-main: "one top-level h1 (the page title; Sections begin at h2), one <main>; Sections nest below"
content:
  section-heading: "the ACCESSIBLE NAME of the landmark + the outline anchor; AT users see landmark/heading lists OUT of visual context -> SPECIFIC ('Billing history' not 'Content'/'Details'); a real heading at the right level"
  description: "optional supporting text under the heading; NOT part of the accessible name (the heading alone is)"
  hierarchy: "don't skip levels (h2->h4 fails 1.3.1); the <H> context increments by exactly one; one h1/page (Sections begin at h2)"
  dont-wrap-everything: "main-flow paragraphs/lists/fields don't need a Section unless a distinct TITLED subdivision; reserve <section> for named navigable regions"
motion:
  own: none   # a semantic/layout wrapper, ships no animation
  scroll-into-view: "Sections are hash-nav targets (#id); support a scroll-margin-top token so the heading isn't occluded by a fixed/sticky app-shell header"
  scroll-snap: "Sections as scroll-snap-align:start children of a scroll-snap-type parent (presentation-style band scrolling)"
  reduce-motion: "entrance/scroll animation must respect prefers-reduced-motion (zero duration, no layout shift); scroll-behavior:smooth only under no-preference; Section itself is motion-neutral"
i18n:
  rtl-inherited: "padding/margin/border use LOGICAL properties (padding-inline/margin-inline-start) so the header (title inline-start, actions inline-end) mirrors under dir=rtl with no JS; inherited from Box"
  full-bleed-direction-agnostic: "the breakout relies on CSS GRID TRACKING (not left/right negative margins) so the band stays correct regardless of reading direction; only the content layout mirrors"
  name-translated: "title/aria-label must hook into the i18n dictionary — the landmark name a SR user hears must match their localized language, not a hardcoded English string"
implementation:
  - "the as -> sectioning element + the name->landmark wiring: render the as tag; if <section>/role=region, AUTO-WIRE aria-labelledby to the header heading via a useId()-generated id (not hand-typed); NO title/aria-label -> render a <div> (or dev-warn). Name-or-downgrade is the component's core value"
  - "the heading-level CONTEXT (over the dead outline algorithm): a LevelContext carrying the current level; a Section increments it CAPPED at 6 (Math.min(level+1,6) — no invalid <h7>); a Heading/<H> reads it + renders the correct <hN>. Nesting deepens headings automatically; moving a Section recomputes with zero JSX refactor; top-level h1 = the page title, Sections begin at h2"
  - "the full-bleed CSS + WHY grid-breakout beats negative margins: the legacy width:100vw + margin-inline:calc(50%-50vw) TRIGGERS A HORIZONTAL SCROLLBAR on Windows (100vw includes the scrollbar). The GRID BREAKOUT (named-line track grid: [full-start] minmax(gutter,1fr) [content-start] minmax(0,max) [content-end] minmax(gutter,1fr) [full-end]; children grid-column:content by default, full-bleed children grid-column:full) solves it with no scrollbar side-effect. The inner-container (full-width Section wrapping a centered max-width Container) is the simpler common default"
  - "the don't-over-landmark lint: flag nameless <section>s, excessive role=region count, duplicate <main>s"
  - "inherit Box, don't re-derive: the as/asChild Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL; Section adds the semantics + the heading-level context + the constrained-width concern"
  - "headless vs opinionated: the name->landmark wiring + the heading-level context are the headless logic worth owning (pure a11y, no styling); spacing + max-width are theme. WHY A CONTAINER OFTEN SUFFICES: many systems' only visual need is the max-width column + hand-authored semantics, so they ship Container + skip Section; the practice ships BOTH (the heading-level context + name-wiring are valuable + error-prone to hand-roll)"
composition:
  stands-on: [box]
  composes: [stack]                        # the header + body
  hosts: [grid, card]                      # a grid of Card content units
  semantic-counterpart-to: [card]          # visual object (chrome) vs semantic region (meaning)
  landmark-siblings: [main, "nav (see side-navigation)", aside, header, footer]   # the specific landmarks; region is the generic one; composed into a PageLayout app shell
  relates-to: ["heading (the heading-level context)", "container (the max-width companion)"]
  alternative-to: ["a plain semantic <div> (the default when no landmark value)", container, "PageLayout (the app-shell landmark set)"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "ship a Section at all? — many systems ship Container (max-width) + PageLayout (app shell) + hand-authored semantics instead; the practice ships BOTH Section (for the heading-level context + name->landmark) and Container, deliberately"
    - "the heading level: manual discipline vs a heading-level CONTEXT (practice: the context — correct by construction)"
    - "semantic Section vs visual/Container — TWO orthogonal primitives composed <Section><Container> (practice) vs one over-propped component"
    - "Section vs PageLayout for the app-shell landmark regions (PageLayout = the composed pattern)"
  trap:
    - "the NAMELESS <section> (role=generic, no landmark value — the most common misuse; name-or-downgrade)"
    - "relying on the document OUTLINE ALGORITHM for heading levels (never shipped, removed ~2022-2025; headings don't auto-level)"
    - "over-landmarking (12 named sections = landmark noise); reaching for <section> by default instead of <div>"
    - "skipping heading levels (h2->h4); multiple h1s / multiple <main>s"
    - "the width:100vw + negative-margin full-bleed hack (horizontal scrollbar on Windows) — use the grid breakout"
    - "putting chrome on a Section (that's a Card); a vague heading naming a landmark a SR user can't use"
  inherited: "Box's as/asChild Slot, the spacing-token scale, the zero-runtime styling delivery, the logical-property RTL"
  role-in-family: "the semantic document region — the landmark + heading-level counterpart to Card's visual surface; the brief that CLOSES the Layout category; stands on Box, composes Stack, hosts Grid/Card, the semantic counterpart to Card"
  evolution:
    - "the document-outline-algorithm myth -> its removal (~2022-2025) -> manual heading levels -> the heading-level-context component (<H>/react-headings)"
    - "the <section>-needs-a-name landmark settling (HTML-AAM: generic without a name; name-or-downgrade + auto aria-labelledby)"
    - "landmark navigation raising region correctness + the don't-over-landmark discipline (React Aria useLandmark F6)"
    - "the CSS Grid breakout displacing the 100vw negative-margin full-bleed hack (+ its Windows scrollbar bug)"
    - "many systems shipping Container/PageLayout, not Section (Polaris s-section/s-page web-component shift)"
  unverified:
    - "external 2026 version numbers across the surveyed systems (Primer v37.x, Polaris v2025-10–v2026-04)"
    - "the exact removal date of the HTML5 outline algorithm (~2022–May 2025) — verify"
    - "the Polaris s-section/s-page web-component migration state + the react-headings library state"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-section/` (16 June 2026), the thirty-ninth brief and the **semantic document region** — the landmark + heading-level counterpart to Card's visual surface, and the brief that **closes the Layout category**. It stands on Box (the polymorphic `as`/`asChild` Slot rendering the sectioning element, the spacing scale, the zero-runtime delivery, the logical-property RTL), composes Stack and hosts Grid/Card, and is the semantic counterpart to Card (the boundary drawn from both sides). The two passes converged with no genuine fork — the nameless-section landmark contract, the heading-level/outline-algorithm myth, the semantic-Section-vs-visual/Container genre split, the sectioning-element decision tree, the full-bleed CSS, and the don't-over-landmark rule — and both land the same architecture: ship `Section` (for the heading-level context + the name→landmark wiring) **and** a separate `Container` (for width), composed `<Section><Container>`. The external pass sharpened with decisive concrete detail: the precise **HTML-AAM `role="generic"`** mapping for a nameless `<section>`, the **`useId()` + `Math.min(level+1, 6)`-capped** heading-level context implementation, the **`width:100vw` + negative-margin Windows-scrollbar bug** as the *why* behind the CSS-Grid named-line breakout, the **outline-algorithm removal dating (~2022–May 2025)**, `scroll-margin-top` for hash-nav occlusion, React Aria's **`useLandmark` F6/Shift+F6** navigation + SPA focus restoration, and the **Polaris `s-section`/`s-page` web-component shift**. Claude-pass contributions: the semantic-counterpart-to-Card framing, the Box-substrate inheritance map, the Section-vs-Card-vs-Box-vs-div decision tree, the don't-over-landmark / name-or-downgrade discipline, and the two-primitive (Section + Container) resolution. The 2026 version numbers, the outline-removal date, and the Polaris web-component state are flagged unverified. Conformant to `components/_schema.md`. **With Section, the Layout category is complete** — Box, Stack, Grid, Card, Section — the fifth category to close as a connected set (after Overlay, Navigation, Feedback, and the Foundations cluster), and the layout foundation the whole catalogue composes on.*
