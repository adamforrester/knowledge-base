# Link — field-truth study (Claude pass)

## 1. Framing
A Link is the navigation primitive — an `<a href>` that takes the user to a URL/destination. It is the routing counterpart the catalogue keeps pointing at: Button drew the link-vs-button boundary from the button side (button §1), and Tabs/Segmented established that *routing is a nav of links + `aria-current`, not a tablist* — Link is where that lives. What it is: navigation to a URL (a page, a section, a document, an external site). What it isn't: an **action in place** (→ Button — `<button>`, Space+Enter, no URL; the core boundary, §5), a **link styled as a button** (→ LinkButton — still an `<a href>`, button §10), or a **non-navigating affordance**. The defining rule: **if it goes to a URL, it's a Link (`<a href>`); if it does something in the current context, it's a Button** — regardless of appearance. Why systems disagree: the **underline discipline**, **internal-vs-external/new-tab** handling, **`aria-current`** for nav links, and the **framework-router polymorphism**.

## 2. Anatomy and parts
A native **`<a href>`** (the non-negotiable core), a **label** (descriptive text — §7), and optional affordances: an **external/new-tab icon** (+ visually-hidden "opens in new tab/external"), a **visited** treatment, an **`aria-current`** marker (nav links), a **download/file-type** indicator. Inline links live in running text (underlined); standalone/nav links sit alone. The design-system Link is **polymorphic** — it renders `<a>` by default but can *be* a router Link (§11).

## 3. Properties / API
- **`href`** — the destination; **a Link without `href` is not a link** (§6). Required for the navigating case.
- **`target` / `rel`** — `target="_blank"` opens a new tab and must carry `rel="noopener noreferrer"` (security/tabnabbing) + a warning affordance (§6).
- **the router polymorphism** — `as` / `asChild` / a render-prop so the Link can render the framework router's Link (Next/React Router/TanStack) while still emitting a real `<a href>` (§11). The load-bearing API decision.
- **`variant`** — inline (underlined, in text) / standalone (CTA-style) / quiet-subtle (de-emphasised); **`isExternal`** (renders the external indicator + rel); `download`.
- `aria-current` (nav links — §6); no `disabled` (links don't truly disable — §4).

## 4. States and variants
States: rest / hover / focus-visible (ring) / active (pressed) / **visited** (`:visited` — privacy-restricted styling, usable for content links, often omitted for app/nav links) / **current** (`aria-current` nav item). Variants: **inline** (underlined, inherits text color-ish but distinct, in body copy) / **standalone** (a lone link, may carry an icon) / **navigation** (in a `<nav>`, with `aria-current`) / **quiet/subtle** (lower-emphasis). **No disabled** — a "disabled link" is either rendered as plain text (no `href`) or marked `aria-disabled` + `href` removed; better to not render it as a link.

## 5. Usage guidance
- **Use** a Link to navigate to a URL/destination: a page, an anchor within the page, a document/download, an external site.
- **Don't use** a Link for: an **in-place action** (submit, open a dialog, toggle, mutate state → Button); a **navigation that should look like a button** (→ LinkButton — still `<a href>`); or anything with **no real destination** (a `#`/`javascript:`/onClick-only "link" is the anti-pattern, §6).
- **Decision frameworks:**
  - **Link vs. Button (the core boundary, from the link side):** does it change the URL/location? Link. Does it act in the current context? Button. *JS-driven navigation still uses `<a href>`* (intercept the click for client-side routing, but emit the real href) — never an `onClick` div/span.
  - **Inline vs. standalone vs. nav:** inline links (in running text) are **underlined** (the affordance); standalone CTAs and nav links may drop the underline *if* another affordance (placement, icon, container) carries it; nav links sit in a `<nav>` and mark the current item with `aria-current="page"`.
  - **Internal vs. external / new tab:** open in the same tab by default; only `target="_blank"` when the context genuinely warrants it, always with the external/new-tab indicator + warning and `rel="noopener noreferrer"`. Don't force new tabs gratuitously (it breaks the back button and user control).

## 6. Accessibility
- **`role=link` via a real `<a href>`** — the `href` is what makes it a focusable, Enter-operable, context-menu-exposing link. **`<a>` without `href` is the recurring anti-pattern**: it's not focusable or operable as a link; and `a[role=button]` / onClick-div "links" lose URL semantics, middle-click, and new-tab. Reach for `<a href>` for navigation, `<button>` for actions — never blur them.
- **Keyboard:** **Enter** activates a link (NOT Space — Space scrolls; this is the operational difference from Button, which takes both). Standard tab order.
- **The underline/contrast contract** (the most link-specific a11y rule): an inline link distinguished from surrounding text by **colour alone fails SC 1.4.1** — it needs a non-colour cue (underline is the default). Where colour is relied on, link-vs-text contrast must be **≥3:1** *and* the link text must meet **≥4.5:1** against the background. Underlining inline links is the safe default.
- **`aria-current`** marks the current item in a set: **`page`** for the current page in nav, `step`/`location`/`true` for other contexts. This is how routing nav (the tabs/segmented boundary) signals "you are here" — not `aria-selected` (that's tabs).
- **New-tab warning** — `target="_blank"` must be announced (a visually-hidden "(opens in new tab)" or the external icon with an accessible name), per the no-surprise-context-change expectation; pair with `rel="noopener noreferrer"`.
- **Skip links** — a "Skip to main content" link, first in the tab order, visually hidden until focused, targeting the main landmark — a required a11y pattern Link owns.
- **WCAG SCs:** 1.4.1 (not colour-only), 2.4.4/2.4.9 (link purpose from text/context), 4.1.2 (role/name), 1.4.11/2.4.13 (focus + contrast), 2.4.1 (skip link / bypass blocks), 3.2.5 (no unexpected new-tab without warning).

## 7. Content guidelines
**Descriptive link text** — the text must convey the destination *out of context* (screen readers list links by text): never "click here", "read more", "learn more" alone (SC 2.4.4/2.4.9). Front-load the meaningful words. Don't wrap a whole sentence in a link; link the noun phrase. **External/file indicators** in the text or as a trailing icon ("Annual report (PDF, 2 MB)"). Multiple "Read more" links on a page must differ (or carry distinct `aria-label`s) so they're distinguishable in the links list.

## 8. Motion and transition
Minimal: a quick underline/colour transition on hover/focus (~100ms). The underline may animate in on hover for standalone links (but inline links stay underlined at rest). Under `prefers-reduced-motion`, keep it instant/opacity-only. No layout motion. (See 18/19.)

## 9. Internationalization
RTL: the external/new-tab icon moves to the leading edge (logical properties); link direction follows text direction. Link text expands like any string and wraps in running text (links can break across lines — ensure the focus ring/underline handles wrapped links). `aria-current` and external-indicator text are localised. (See 13.)

## 10. Naming
**`Link`** is near-universal (Spectrum/React Aria, Material, Carbon, Base Web); some systems use `TextLink` (to distinguish from nav/router links) or `Anchor`. **The practice default: `Link`** (the navigation primitive), with **`LinkButton`** as the named link-styled-as-button (button §10), and the framework-router integration via `as`/`asChild` rather than a separate component. Aliases: `TextLink`, `Anchor`, `Hyperlink`, `A`.

## 11. Implementation notes
- **Always emit a real `<a href>`** — for progressive enhancement, middle-click/cmd-click new-tab, "copy link", SEO, and the accessibility tree. An `onClick`-navigation `<div>`/`<span>` (or `<a>` with no `href`) is the cardinal sin — it breaks all of the above. This is the headline implementation rule.
- **Router polymorphism (`asChild`/`as`)** — the design-system Link must integrate with the app's client-side router (Next.js `Link`, React Router/TanStack `Link`) *without* the design system depending on any router. The pattern: an **`asChild`** (Radix-style — render the child, merging props onto it) or a polymorphic **`as`** prop, so the consumer passes their router's Link and the design system applies styling/behaviour to the rendered `<a>`. The router intercepts the click for SPA navigation but the real `href` remains for fallback/middle-click. (React Aria's `RouterProvider` is another approach — a global router hook.)
- **`target="_blank"` ⇒ `rel="noopener noreferrer"`** automatically when `isExternal`/new-tab (security: prevent `window.opener` tabnabbing; `noreferrer` optionally).
- **No-href handling** — if a Link renders without `href`, either render plain text or warn; don't ship a non-functional `<a>`.
- **Skip link** — visually-hidden-until-focused, first focusable element, `href="#main"`.
- **Don't hand-roll** — React Aria `useLink`/`Link`, Radix `asChild` on a Slot; skin it.

## 12. Related and alternative components
- **Composes with:** Icon (external/new-tab/download indicator — see icon), the `<nav>` landmark, Breadcrumbs (a trail of links — see Breadcrumbs when briefed), Menu items (which may be links), the framework router's Link.
- **Alternative to:** Button (in-place action — see button; the core boundary), LinkButton (navigation that looks like a button — button §10), a routing nav (the tabs/segmented boundary — links + `aria-current`, not a tablist — see tabs, segmented-control).
- **Supersedes:** an `onClick`-navigation `<div>`/`<span>`; an `<a>` with no `href` (or `href="#"`/`javascript:void(0)`); `a[role=button]` for navigation.
- **Superseded by:** Button when the affordance is an action, not navigation.

(The routing/`aria-current` counterpart to the tabs-vs-routing and segmented-vs-routing boundaries; closes the link-vs-button boundary from the link side. See button for the boundary and LinkButton, tabs/segmented-control for the routing rule, 03-component-library, 29 for the docs template.)

## 13. Field POV evolution
1. **The `asChild`/router-polymorphism pattern converged** — design-system Links integrate with framework routers via `asChild`/`as`/RouterProvider rather than baking in a router or forcing onClick navigation.
2. **The death of `onClick`-div navigation** — strict a11y practice and SSR/SEO needs killed the "navigation without a real href" pattern.
3. **`aria-current="page"`** standardised as the current-nav-item signal (distinct from `aria-selected` for tabs).
4. **New-tab discipline tightened** — `rel="noopener"` now default browser behaviour for `target=_blank`, and the announce-new-tab expectation hardened.

## 14. Sources cited
(Conservative; reconcile with external.) Adobe Spectrum / React Aria `Link`, `useLink`, `RouterProvider` (2024–2025); GitHub Primer `Link` (inline/standalone, `muted`) (2024); IBM Carbon `Link` (inline, visited, size, external icon) (2024); Material 3 links (2024); Shopify Polaris `Link` (monochrome/external) (2024); Atlassian `Link`/`LinkButton` (2024); Base Web `StyledLink` (2024); Radix `Slot`/`asChild`; WAI-ARIA APG link pattern; MDN `rel`/`target` security; WCAG 2.2 (Oct 2023) — 1.4.1, 2.4.4, 2.4.9, 2.4.1, 4.1.2, 1.4.11, 2.4.13, 3.2.5.

## 15. Agent-consumable schema (conform to _schema.md in link.md)
identity/description/anatomy(<a href> + label + external/new-tab icon + visited/current affordances; polymorphic to a router Link)/api(href, target/rel, as/asChild router polymorphism, variant inline|standalone|quiet, isExternal, download; NO disabled)/states(rest/hover/focus/active/visited/current; inline|standalone|nav|quiet)/accessibility(real <a href> = role=link; Enter not Space; the no-href anti-pattern; underline/contrast 1.4.1 + 3:1/4.5:1; aria-current=page; new-tab warning + rel=noopener; skip links)/content(descriptive link text, no 'click here', external/file indicators)/motion(underline/colour hover ~100ms)/i18n(RTL icon side; wraps in running text)/implementation(ALWAYS real <a href>; asChild/as router polymorphism; target=_blank=>rel=noopener noreferrer; no onClick-div; skip-link)/composition(Button alt, LinkButton, nav landmark, Breadcrumbs)/notes(link-vs-button from the link side; underline discipline; router polymorphism; the onClick-div anti-pattern; aria-current vs aria-selected).
