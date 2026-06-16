# Breadcrumbs — field-truth study (Claude pass)

## 1. Framing
Breadcrumbs are a **secondary wayfinding aid**: a single-line trail showing the current page's position in a site/app hierarchy, rendered as a sequence of ancestor **Links** ending at the current page. The substrate is Link (each crumb is an `<a href>` to an ancestor URL — see link); Breadcrumbs add the *structure* (a labelled nav landmark + ordered list), the *current-page marking* (`aria-current="page"`), the *decorative separators*, and the *overflow/collapse* model. What it is: location breadcrumbs — "you are here in the tree." What it isn't: **primary navigation** (breadcrumbs supplement, never replace, the main nav), a **back button** (browser/OS history is linear and device-state-dependent; a breadcrumb is hierarchical and stable — §5), **Tabs** (peer views at the same level, not ancestors — see tabs), or a **Stepper/Wizard** (ordered steps in a linear flow, with completion state, not a hierarchy — see stepper). Two breadcrumb *types* exist in theory — **location** (where you are in the hierarchy; static, the common case) and **path/attribute** (the trail you actually clicked; rare, fragile) — the practice ships **location** breadcrumbs. Why systems disagree: the **last/current crumb** (link vs. static text), the **overflow/truncation** model, **separator** rendering, and whether the system **emits SEO structured data**.

## 2. Anatomy and parts
- **nav landmark** — `<nav aria-label="Breadcrumb">` (the APG pattern); the label distinguishes it from other `<nav>`s and is what a screen-reader landmark list shows.
- **ordered list** — `<ol>` of `<li>`; ordered because the crumbs have a meaningful sequence (root → … → current). The `<ol>`/`<li>` also gives screen readers "list, N items" + position.
- **crumb** — a **Link** (`<a href>`) to an ancestor (inherits link entirely — underline discipline, router `asChild`, link-vs-button).
- **current marker** — the final crumb, carrying `aria-current="page"`.
- **separator** — the `/`, `>`, or chevron between crumbs; **decorative, not DOM content** (CSS `::before`/`::after` or an `aria-hidden` element).
- **overflow/collapse affordance** — when the trail is too long: an ellipsis (`…`) crumb that reveals the collapsed middle ancestors (a Menu/disclosure — see menu).
- **home/root crumb** — optionally an icon (house) instead of the word "Home"; needs an accessible name either way.

## 3. Properties / API
- **`items` / `children`** — the crumbs. Two API shapes in the field: a **data-driven** `items` array (`{label, href}`) the component maps and auto-separates (Polaris-ish, Material), or **composed children** (`<Breadcrumbs><Breadcrumb href>…</Breadcrumb></Breadcrumbs>`, React Aria/Carbon) where the component injects separators between slots. The practice default mirrors the text-field encapsulation POV: **composed children for control, with a convenience `items` prop for the common data-driven case** (inherits link's `asChild` per crumb so each can be a router Link).
- **`separator`** — token/glyph or render-slot; default a chevron or slash (§7). Decorative regardless of how it's passed (§6, §11).
- **overflow controls** — `maxItems` (collapse threshold) + `itemsBeforeCollapse` / `itemsAfterCollapse` (how many head/tail crumbs to keep, MUI's vocabulary), or a boolean `showRoot` + automatic middle-collapse. The practice exposes a **collapse threshold + keep-first/keep-last counts**.
- **current-crumb handling** — whether the last child auto-gets `aria-current="page"` and renders as text vs. link (§4, §6). The component should mark the last crumb automatically.
- **router integration** — inherits link's `asChild`/`as` per crumb (§11).

## 4. States and variants
- **Crumb states** — inherit link: rest / hover / focus-visible / (visited rarely). The **current crumb** is the distinct state — visually de-emphasised or emphasised, `aria-current="page"`, and typically **non-interactive** (§6).
- **Variants:** **default** (full trail) / **collapsed/overflow** (middle crumbs behind a `…`) / **with-home-icon** (root as an icon) / **condensed/mobile** (often just a single "‹ Parent" back-up-one-level crumb). Size scales with the type ramp; breadcrumbs are usually one small text size.

## 5. Usage guidance
- **Use** when the site/app has a **deep (3+ level) hierarchy** the user navigates into (e-commerce categories, docs trees, file systems, nested settings) — breadcrumbs give the "where am I / climb back up" affordance.
- **Don't use** for: **flat sites** (no hierarchy to show), as **primary navigation** (they're a supplement), for **linear flows** (→ Stepper), for **peer views** (→ Tabs), or as a **substitute for a back button** (different mental model — hierarchy vs. history).
- **Decision frameworks:**
  - **Breadcrumb vs. back button:** breadcrumb = *hierarchy* (stable, structural, "up to parent"); back = *history* (linear, session-dependent, "previous page"). On mobile, a single "‹ Parent" crumb is hierarchical even though it looks like back — it goes *up*, not *back*.
  - **Breadcrumb vs. tabs vs. stepper:** ancestors → breadcrumb; peers at one level → tabs; ordered steps with progress → stepper.
  - **Current crumb interactive?** Default **non-interactive text** for the current page (a self-link is low-value), but **link + `aria-current="page"`** is acceptable and is what several systems ship (it keeps the trail visually uniform and gives a reload affordance). Resolve to one default (§6).

## 6. Accessibility
- **The landmark + list contract:** `<nav aria-label="Breadcrumb">` → `<ol>` → `<li>` → crumb Link. The `aria-label` (or `aria-labelledby`) is required so the landmark is distinguishable; "Breadcrumb" (singular) is the APG convention, and screen readers append "navigation," so don't include the word "navigation" in the label.
- **`aria-current` on the current crumb:** **`aria-current="page"`** is the APG value for the current page in a breadcrumb (NOT `aria-current="location"` — `location` is for "current within a container" like a visual highlight; `page` is the breadcrumb/nav-current idiom, matching link §6). This is the single most-confused breadcrumb a11y detail.
- **Decorative separators:** the `/`/`>`/chevron must be **inert to AT** — rendered via CSS `::before`/`::after` on the `<li>` (preferred) or as an `aria-hidden="true"` element. **Never** put the separator as text content of a list item or between crumbs in the DOM (it gets read, and inflates the list count). If it's an icon, it's `aria-hidden`.
- **Current crumb (link vs text):** if a Link, `aria-current="page"` is mandatory; if static text, it should still sit in the `<li>` and may carry `aria-current="page"` on the text element so AT announces "current page."
- **Overflow menu a11y:** the `…` affordance is a real `<button>` opening a Menu/disclosure of the collapsed crumbs (keyboard-operable, labelled e.g. "Show N more"); not a non-focusable glyph.
- **WCAG SCs:** 2.4.5 (multiple ways to locate a page — breadcrumbs are one of the two "ways"), 2.4.8 (location — breadcrumbs satisfy this AAA SC directly), 1.3.1 (info & relationships — the list/nav structure), 4.1.2 (name/role/value), plus all of link's SCs per crumb (1.4.1 underline/contrast, 2.4.4 link purpose).

## 7. Content guidelines
- **Concise crumb labels matching the page/section titles** — a crumb is the destination page's name; keep it short (the trail is one line). Don't restate the hierarchy in each label.
- **Truncation + tooltip** — if a single label is too long, truncate with ellipsis and expose the full text on hover/focus (title/tooltip), but prefer collapsing the *trail* over truncating *labels*.
- **The home label** — "Home" text, or a house icon with an accessible name ("Home"); the root crumb is the site/app root, not necessarily the literal homepage.
- **Don't include the current page as a clickable verb** — it's a location, not an action.

## 8. Motion and transition
Minimal. The only motion is the **overflow menu open/close** (a quick fade/scale, ~150ms — see menu/popover) and possibly a hover underline on crumbs (inherits link). No trail animation. Under `prefers-reduced-motion`, the overflow menu opens instantly. (See 18/19.)

## 9. Internationalization
- **RTL** — the trail order flips (root on the right), and the separator glyph flips: a `>`/chevron must mirror to `<` (use a logical/mirroring glyph or `transform` under `[dir=rtl]`); a `/` slash is direction-neutral but the *order* still flips. This is the headline i18n trap — handle separators with logical properties / CSS mirroring, not a hardcoded glyph.
- **Text expansion** — labels grow in German/Finnish; the collapse/truncation model must hold (favours trail-collapse over fixed-width labels).
- **Localised labels** — "Home," overflow "Show more," and the nav `aria-label` ("Breadcrumb") are all localised.

## 10. Naming
**`Breadcrumbs`** (the container, plural) + **`Breadcrumb`** or **`BreadcrumbItem`** (the crumb) is the dominant pairing (React Aria `Breadcrumbs`/`Breadcrumb`, Carbon `Breadcrumb`/`BreadcrumbItem`, MUI `Breadcrumbs`). The practice default: **`Breadcrumbs`** (container) / **`BreadcrumbItem`** (crumb, which *is* a Link via `asChild`). Aliases: `Breadcrumb` (singular as container, Polaris/Carbon vary), `BreadcrumbList`, `Crumb`, `BreadcrumbTrail`.

## 11. Implementation notes
- **Decorative separators via CSS, not DOM** — `li:not(:first-child)::before { content: "/"; }` (or a background/mask icon), so the separator never enters the accessibility tree or the list count. This is the cardinal breadcrumb implementation rule.
- **Overflow-collapse logic** — when crumb count exceeds the threshold, keep first (root) + last (current) [+ optional parent], replace the middle with a `…` button that opens a Menu of the hidden crumbs. Decide collapse by **count** (simple, deterministic) or **available width** (a ResizeObserver-driven "responsive" collapse — more correct, more complex). The practice default: **count-based with keep-first/keep-last**, width-based as an enhancement.
- **Router integration** — each crumb inherits link's `asChild`/`as` so it can be a framework router Link while emitting a real `<a href>` (see link §11). The component owns the `<nav>`/`<ol>`/`<li>`/separator/`aria-current`; the consumer owns routing.
- **SEO / structured data** — `schema.org` **`BreadcrumbList`** (JSON-LD) drives Google's breadcrumb rich-result. **The practice POV:** the design-system component **does not auto-emit JSON-LD** (it can't know canonical URLs/site structure, and SSR/duplication concerns belong to the app/SEO layer) — it ships the *accessible HTML* breadcrumb and **documents the JSON-LD pattern + offers an optional opt-in `structuredData` emitter** for teams that want it. Don't silently inject structured data; don't pretend it's the component's job by default.
- **Headless vs. opinionated** — React Aria provides headless `Breadcrumbs`/`useBreadcrumbs` (structure + a11y, no style); the practice skins a headless core rather than hand-rolling the landmark/list/`aria-current` wiring.

## 12. Related and alternative components
- **Composes with:** Link (each crumb — the substrate; see link), the `<nav>` landmark, Icon (home icon, separator chevron, overflow ellipsis — see icon), Menu (the overflow/collapse popover — see menu), Page header / Page title (breadcrumbs commonly sit above the H1).
- **Alternative to:** Tabs (peer views, not ancestors — see tabs), Stepper (linear ordered flow — see stepper), a back button (history, not hierarchy), the primary nav (breadcrumbs supplement it).
- **Supersedes:** a hand-rolled `<div>` of slash-separated `<a>`s with the separator as text content (the recurring anti-pattern — breaks the list count + reads the slash).
- **Superseded by:** Tabs/Stepper when the relationship is peer/linear rather than hierarchical; nothing within the wayfinding-hierarchy lane.

(The first brief built directly on Link — a trail of Links + `aria-current="page"` + the nav/ol/li landmark. Closes the "where am I in the hierarchy" wayfinding lane against tabs (peers) and stepper (linear). See link for the crumb substrate, tabs/segmented-control for the routing-vs-tablist rule, 03-component-library, 29 for the docs template.)

## 13. Field POV evolution
1. **`<nav aria-label> + <ol>/<li>` standardised** as the APG breadcrumb structure — the bare `<div>` of links is now a clear anti-pattern.
2. **`aria-current="page"`** settled as the current-crumb signal (over `location` and over nothing), aligning with link's nav-current idiom.
3. **Decorative-separator discipline hardened** — separators moved out of the DOM into CSS pseudo-elements / `aria-hidden`, so they stop polluting the list count and AT output.
4. **Collapse/overflow became the expected deep-trail behaviour** (ellipsis menu keeping root + current), and the **mobile single-parent "back-up" crumb** emerged as the small-screen convention.
5. **Structured-data ownership clarified** — JSON-LD `BreadcrumbList` is increasingly treated as an app/SEO-layer concern (opt-in), not a default component side effect.

## 14. Sources cited
(Conservative; reconcile with external.) WAI-ARIA APG **Breadcrumb pattern** (`nav[aria-label="Breadcrumb"]` + `ol`/`li` + `aria-current="page"`); Adobe Spectrum / **React Aria `Breadcrumbs`/`Breadcrumb`** + `useBreadcrumbs` (2024–2025); IBM **Carbon `Breadcrumb`/`BreadcrumbItem`** (overflow menu) (2024); **MUI `Breadcrumbs`** (`maxItems`/`itemsBeforeCollapse`/`itemsAfterCollapse`, collapse) (2024); Shopify **Polaris `Breadcrumbs`** (single back-action model) (2024); **Material 3** breadcrumbs (2024); GitHub **Primer `Breadcrumbs`** (2024); **Atlassian `Breadcrumbs`** (collapse after N) (2024); **Base Web (Uber) `Breadcrumbs`** (2024); **schema.org `BreadcrumbList`** + Google Search Central breadcrumb structured-data docs; WCAG 2.2 (Oct 2023) — 2.4.5, 2.4.8, 1.3.1, 4.1.2, plus link's SCs.

## 15. Agent-consumable schema (conform to _schema.md in breadcrumbs.md)
identity(Breadcrumbs/BreadcrumbItem; aliases Breadcrumb, BreadcrumbList, Crumb; navigation; stable)/description(secondary wayfinding trail of ancestor Links + current page; not primary nav, not back, not tabs/stepper)/api(inherits: link per crumb; items[] or composed children; separator (decorative); maxItems/itemsBeforeCollapse/itemsAfterCollapse overflow; auto aria-current=page on last; asChild router per crumb)/states(inherits link rest/hover/focus per crumb; current crumb = aria-current=page, typically non-interactive; collapsed/overflow; with-home-icon; condensed/mobile-back)/variants(default/collapsed/with-home-icon/condensed)/accessibility(nav[aria-label=Breadcrumb] + ol/li; aria-current=PAGE not location; decorative separators aria-hidden/CSS never DOM content; overflow = real button+menu; SC 2.4.5/2.4.8/1.3.1/4.1.2 + link SCs)/content(concise labels matching titles; trail-collapse over label-truncation; Home text-or-icon w/ accessible name; current page not a verb)/motion(only overflow menu ~150ms; reduce-motion instant)/i18n(RTL order flip + separator glyph mirror via logical props; text expansion favours collapse; localise Home/Show more/aria-label)/implementation(separators via CSS ::before not DOM; count-based collapse keep-first/keep-last, width-based as enhancement; router asChild per crumb; JSON-LD BreadcrumbList = opt-in not default; skin headless useBreadcrumbs)/composition(Link substrate, nav landmark, Icon, Menu overflow; alt Tabs/Stepper/back; supersedes div-of-slash-links)/notes(contested: current crumb link-vs-text; overflow count-vs-width; JSON-LD ownership; aria-current page-vs-location confusion. inherited: all of link per crumb.)
