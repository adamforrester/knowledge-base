---
okf_version: "0.1"
type: component-brief
title: Link
description: The navigation primitive — and the routing side of the boundary Tabs, Segmented Control, and Button all point at. A field-truth study of the href contract (the no-href / onClick-div anti-pattern), the link-vs-button boundary from the link side, the inline/standalone/quiet variants and the underline discipline, internal-vs-external + the new-tab/tabnabbing rules, aria-current for nav, and the framework-router polymorphism (asChild/Slot, always a real <a href>), with the practice's defaults.
tags: [components, navigation]
category: Navigation
status: stable
aliases: [text-link, anchor, hyperlink, link-button]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Link

> Link is the navigation primitive — and the place the catalogue's routing boundary finally lives. Button drew the link-vs-button line from the button side; Tabs and Segmented Control both ruled that *routing is a nav of links + `aria-current`, not a tablist*. Link is where that pattern is. The whole component rests on one non-negotiable contract — **a real `<a href>`** — because the `href` is what gives the browser the status-bar preview, the context menu, middle-click-for-new-tab, drag-to-bookmark, SEO, and the accessibility tree. An `<a>` with no `href`, or an `onClick` div styled as a link, throws all of that away. If it goes to a URL it's a Link; if it acts in place it's a Button — *regardless of how it looks*.

---

## 1. Framing

A Link navigates to a URL/destination (a page, a fragment, a document, an external origin), negotiating with the browser's routing, the OS window manager, and the accessibility tree. What it *isn't*: an **in-place action** (→ Button — `<button>`, Space *and* Enter, no URL; the core boundary, §5), a **link styled as a button** (→ LinkButton — still an `<a href>`, just wearing button tokens; button §10), or a **non-navigating affordance**.

The defining contract is the **`href`**: its presence is what makes the element a real link (status-bar preview, "open in new tab", middle-click, drag-to-bookmark, crawlable, announced as a link). So the two cardinal rules both passes converge on: **(1) if the interaction doesn't change the URL, it's a Button, not a Link; (2) even JS/SPA-routed navigation must still render a real `<a href>`** (the router intercepts the click; the href stays for fallback/middle-click/SEO). Why systems disagree: the **underline discipline**, **internal-vs-external/new-tab** handling, **`aria-current`** for nav links, and — most heavily — the **framework-router polymorphism**.

## 2. Anatomy and parts

A native **`<a href>`** with the **label text embedded directly inside it** (a `<span>`/`<div>` wrapper *outside* the anchor breaks the accessible-name computation), plus optional affordances:

- **External/new-tab icon** — a trailing "launch"/arrow-out glyph (+ visually-hidden "opens in new tab / external site"); it shares the text's colour token and baseline. *Standalone links may carry icons; inline links forgo them* (icons disrupt running-text rhythm — Carbon).
- **The underline** — the non-colour affordance (§6), engineered with `text-decoration-skip-ink: auto` + `text-underline-offset` so it clears descenders (the legacy `text-decoration: underline` struck through `g/j/p/q/y`); or a `border-bottom`/`box-shadow` for pixel control.
- **Visited treatment** — a colour shift for history wayfinding, but the browser quarantines `:visited` to a few colour properties (and `getComputedStyle` lies) for privacy (§4).
- **`aria-current` marker**, **download/file indicator**.

The design-system Link is **polymorphic** — it renders `<a>` by default but can *become* a router Link (§11).

## 3. Properties / API

- **`href`** — the destination; **required for a real link**. No `href` ⇒ not a link (§6).
- **`variant`** — `inline` (default) / `standalone` / `quiet` (subtle) / `inverse` (static colour over images/dark) — driving the underline behaviour (§4).
- **`target` / `rel`** — `target="_blank"` must auto-attach **`rel="noopener noreferrer"`** (security, §5).
- **`isExternal`** — renders the external indicator + visually-hidden warning + the rel.
- **`asChild` (or `as`)** — the router polymorphism: merge the Link's styling/a11y onto a framework router's Link while emitting one clean `<a href>` (§11). The most-debated API decision.
- **`aria-current`** — `page` (current page in nav) / `step` (wizard) / `location` (breadcrumb leaf) / `true` (generic) (§6).
- **No real `disabled`** — links don't natively disable; handle via the documented sequence (§4) or, better, don't render it as a link. (Primer note: the discrete `underline` prop is being deprecated in favour of deriving it from the variant.)

## 4. States and variants

States: rest / hover (pointer cursor; standalone reveals its underline) / focus-visible (high-contrast ring; **`:focus-visible`, not `:focus`**, so a mouse click doesn't leave a persistent ring) / active (pressed) / **visited** / **current** (`aria-current`).

- **`:visited` is locked down** — after mid-2000s history-sniffing exploits, browsers restrict it to a handful of colour properties and `getComputedStyle` returns the *unvisited* colour to JS. Use it for content/docs links; usually omit for app/nav links.
- **No disabled state, properly** — a "disabled link" is a contradiction (if you can't go there, don't link it). When an enterprise app must show an unavailable nav slot, the documented sequence is: **remove `href`, set `aria-disabled="true"`, add `role="link"` (since dropping `href` strips link semantics), `pointer-events: none` + visual dim, optionally `tabindex="-1"`** — but prefer rendering plain text.

**Variants:**

- **Inline** — in running body text; **persistent underline at rest** (the affordance); no icons.
- **Standalone** — isolated (nav rails, footers, beside controls); underline may be **revealed on hover/focus** because placement supplies the interactivity cue; icons allowed.
- **Quiet/subtle** — muted colour, no underline; only where the macro-layout guarantees interactivity (footer lists, breadcrumbs, dense tables).
- **Inverse/static-colour** — forced white/black over imagery/dark backgrounds, ignoring theme tokens, for guaranteed contrast.
- **Navigation** — a link inside a `<nav>`, marking the current item with `aria-current` (§6).

## 5. Usage guidance

- **Use** a Link to go to a URL/destination — a page, an in-page anchor, a document/download, an external site.
- **Don't use** a Link for: an **in-place action** (submit, open a dialog, toggle, mutate state → Button); a **navigation that needs button weight** (→ LinkButton — still `<a href>`); or anything with **no real destination** (`#`, `javascript:void(0)`, onClick-only).
- **Decision frameworks:**
  - **Link vs. Button (from the link side):** does it change the URL/location? Link. Does it act in the current context? Button. **JS navigation still uses `<a href>`** — intercept the click for client-side routing, but never an `onClick` div/span.
  - **Inline vs. standalone vs. nav:** inline links are **underlined** in body text; standalone/quiet may drop the resting underline *because placement carries the cue*; nav links sit in a `<nav>` and mark the current item `aria-current="page"`.
  - **Internal vs. external / new tab:** same tab by default. Reserve `target="_blank"` for narrow cases — a supplementary doc opened mid-form (avoid data loss), continuous media, an OAuth portal — always with the external indicator + warning and `rel="noopener noreferrer"`. Gratuitous new tabs break the back button and user control.

## 6. Accessibility

- **`role=link` via a real `<a href>`.** The `href` is what makes it focusable, Enter-operable, and context-menu/middle-click capable. **The no-href anti-pattern** (`<a>` without `href`, `a[role=button]`, onClick div) removes it from the accessibility tree as a link and from the tab order; the fragile `href="#"` + `preventDefault` or `role=link` + `tabindex=0` fallbacks are last resorts — provide a resolvable URL at render.
- **Keyboard: Enter activates (NOT Space).** Space scrolls the page; this is the operational tell vs. Button (which takes both). Standard tab order.
- **The underline/contrast contract** (the most link-specific rule): an inline link distinguished from surrounding text by **colour alone fails SC 1.4.1**. The contrast-only workaround (link-vs-text ≥3:1 *and* text-vs-background ≥4.5:1) technically passes but cramps the palette and collapses in dark mode, so **the practice enforces the underline for inline links** and rejects the contrast-only route. Standalone/nav links are exempt only because placement supplies the cue.
- **`aria-current`** marks the current item: **`page`** in site nav, `step` in a wizard, `location` in a breadcrumb, `true` generic — so AT announces "current page, link, Dashboard". A visual `.active` class alone is insufficient. (This is the nav-routing signal — *not* `aria-selected`, which is Tabs.)
- **New-tab warning** — `target="_blank"` must be announced (visually-hidden "(opens in new tab)" or the external icon's accessible name) per the no-surprise-context-change rule (3.2.5); pair with `rel="noopener noreferrer"` (reverse-tabnabbing + referrer privacy).
- **Skip link** — a "Skip to main content" Link, first in the tab order, visually hidden (via clipping, not `display:none`) until focused, targeting the `<main>` landmark (`href="#main"`) — a required bypass-blocks pattern Link owns.
- **WCAG SCs:** 1.4.1 (not colour-only), 2.4.4 / 2.4.9 (link purpose from text / in context), 4.1.2 (role/name), 1.4.11 / 2.4.13 (focus + contrast), 2.4.1 (bypass blocks / skip link), 3.2.5 (no unexpected new context).

## 7. Content guidelines

**Descriptive link text that stands alone** — AT lists links stripped of context, so never "click here" / "read more" / "learn more" by themselves (SC 2.4.4/2.4.9); front-load the meaningful words and link the noun phrase, not a whole sentence. Where extreme space forces generic text, supply an **`aria-label`** ("Read more about the Q3 report"). **Never embed raw URLs** in body copy (screen readers read every character) — describe the destination, hide the URL in `href`. **File links** state format and size ("Annual report (PDF, 2 MB)"). Multiple "Read more" links on a page must be distinguishable (distinct text or `aria-label`).

## 8. Motion and transition

Minimal and functional: a ~150–200ms ease `text-decoration-color`/colour transition on hover/focus; standalone links may animate the underline in (inline links stay underlined at rest). A left-to-right underline grow via pseudo-element is fine if done with `transform`/`opacity` (no layout thrash). Under `prefers-reduced-motion: reduce`, drop translation/scale and keep an opacity/colour change (or snap). No layout motion. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

**RTL** relocates the external/new-tab icon to the leading edge and **mirrors it horizontally** (the arrow points top-left), via logical properties so `dir="rtl"` handles it automatically. **Text expansion** (de/ru +30–50%) means inline links must **wrap across lines without breaking the underline or splitting an attached icon from its word** — `white-space: nowrap` on inline links is an anti-pattern. `aria-current` and external-indicator text localise. (See 13-internationalization-and-rtl.)

## 10. Naming

**`Link`** is the near-universal default (Spectrum/React Aria, Material, Carbon, Base Web), with `TextLink`/`Anchor`/`Hyperlink` as legacy aliases. **The practice default is `Link`** (the navigation primitive), **`LinkButton`** for the link-styled-as-button (button §10), and the router integration via **`asChild`/`as`** rather than a separate component. Atlassian's distinct **`Anchor`** primitive (a raw clickable block — e.g. a whole-card link, non-textual) is a defensible separate concern for complex platforms; the practice keeps a unified `Link` and reaches for an `Anchor`/clickable-wrapper only for the non-textual block case. Aliases to map: `TextLink`, `Anchor`, `Hyperlink`.

## 11. Implementation notes

- **Always emit a real `<a href>`** — for progressive enhancement, middle/cmd-click, "copy link address", SEO, and the a11y tree. An `onClick`-navigation `<div>`/`<span>`, an `<a>` with no `href`, or `href="#"`/`javascript:void(0)` is the cardinal sin (the field has purged it via linters). This is the headline rule.
- **Router polymorphism — `asChild`/Slot is the converged answer.** The design system must integrate the app's client-side router (Next.js/React Router/TanStack `Link`) *without depending on any router*. The `asChild` (Radix Slot) pattern: the Link **doesn't render its own node** — it clones the framework-router child and merges its classes/refs/handlers, yielding one clean `<a>` that marries DS styling with SPA routing (avoiding the `<a><a>` nesting trap and the brittle `as`-prop typings). The **`AppProvider` context** alternative (Atlassian's `routerLinkComponent`) removes per-instance boilerplate but tightly couples the DS to the host router and needs complex internal typings — so the practice prefers **`asChild`** (with a global `RouterProvider`-style hook, React Aria's approach, as the other acceptable option).
- **`target="_blank"` ⇒ auto `rel="noopener noreferrer"`** (when `isExternal`/new-tab) — prevent reverse-tabnabbing (`window.opener`) and strip the referrer.
- **No-href handling** — render plain text or warn; never ship a non-functional `<a>`.
- **Skip link** — visually-hidden-until-focused, first focusable, `href="#main"`.
- **Don't hand-roll** — React Aria `useLink`/`Link` + `RouterProvider`, or Radix `Slot` for `asChild`; skin it.

## 12. Related and alternative components

- **Composes with:** Icon (external/new-tab/download/file indicator — see icon), the `<nav>` landmark, Breadcrumbs (a trail of links, the leaf marked `aria-current="location"` — see Breadcrumbs when briefed), Menu items (navigation menu items *are* links under the hood), the framework router's Link.
- **Alternative to:** Button (in-place action — see button; the core boundary), LinkButton (navigation with button weight — button §10), a routing nav (the tabs/segmented routing boundary — links + `aria-current`, not a tablist — see tabs, segmented-control).
- **Supersedes:** an `onClick`-navigation `<div>`/`<span>`; an `<a>` without `href` (or `href="#"`/`javascript:void(0)`); `a[role=button]` for navigation.
- **Superseded by:** Button when the affordance is an action, not navigation.

(The routing/`aria-current` counterpart to the tabs-vs-routing and segmented-vs-routing boundaries; closes the link-vs-button boundary from the link side. See button for that boundary + LinkButton, tabs and segmented-control for the routing rule, icon for the external indicator. 03-component-library; 29 for the docs template. Breadcrumbs and Menu are the adjacent Navigation briefs that build on Link.)

## 13. Field POV evolution

1. **The death of the `onClick`-div.** SPAs once bound `router.push()` to styled `<div>`/`<button>`s, wrecking accessibility and power-user behaviours (middle-click, copy-link); strict auditing and linters have purged it — *SPA navigation still requires a real anchor.*
2. **Polymorphic rendering converged on `asChild`/Slot** — over years of `forwardRef` gymnastics, HOCs, and context injection — cleanly separating DS styling from router prefetching without invalid DOM.
3. **`aria-current="page"`** standardised as the current-nav-item signal (distinct from Tabs' `aria-selected`).
4. **New-tab discipline tightened** — `rel="noopener"` is now default browser behaviour for `target="_blank"`, and the announce-the-new-tab expectation hardened.
5. **Web Components migration** (Polaris, late 2025–2026) — decoupling foundational primitives like Link from framework lifecycles (cross-brief, unverified).

## 14. Sources cited

Conservative dating (the external pass cited Carbon v11.109.0, Primer v38.26.0, React Aria v1.18.0, all 2026 — held loosely; the Polaris Web-Components migration is the same cross-brief unverified claim; `last-audited` is the re-run trigger):

- Adobe Spectrum / React Aria — `Link`, `useLink`, `RouterProvider` (global router integration), the "quiet" variant (Spectrum, 2024–2026).
- IBM Carbon — `Link` (inline/standalone, visited token, size, external icon), the standalone-may-use-icons / inline-forgo-icons rule (Carbon, 2024–2026).
- GitHub Primer — `Link`/`LinkButton`, the external indicator, the underline-prop deprecation toward variant-derived underline (Primer, 2024–2026).
- Atlassian Design System — `Link`/`LinkButton`, the `Anchor` primitive, the `AppProvider` `routerLinkComponent` context-injection pattern (Atlassian, 2024–2025).
- Shopify Polaris — `Link` (monochrome/external); the Web-Components migration (Polaris, 2024–2026).
- Uber Base Web — `StyledLink`, the link-vs-button gray-area guidance (Base Web, 2024).
- Google Material 3 — link contrast/colour requirements (Material 3, 2024).
- Radix UI — the `asChild`/`Slot` composition pattern; MDN — `rel`/`target` security, `:visited` privacy.
- WAI-ARIA APG — the Link pattern; skip-link / bypass-blocks; the disabled-link (`aria-disabled` + `pointer-events`) handling.
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.4.1, 2.4.4, 2.4.9, 4.1.2, 1.4.11, 2.4.13, 2.4.1, 3.2.5.

## 15. Agent-consumable schema

```yaml
identity:
  id: link
  name: Link
  aliases: [text-link, anchor, hyperlink, link-button]
  category: navigation
  status: stable
description: >
  The navigation primitive — a real <a href> that transits to a URL /
  fragment / external origin. The href contract is non-negotiable (it
  enables status-bar preview, context menu, middle-click, drag-bookmark,
  SEO, a11y tree). Not an in-place action (button), not a link styled as a
  button (link-button — still <a href>). The routing/aria-current side of
  the tabs-vs-routing and segmented-vs-routing boundaries.
anatomy:
  core: "native <a href> with the label embedded INSIDE the anchor (outer span/div wrapper breaks accessible-name)"
  parts: [label, external/new-tab-icon (+visually-hidden warning; standalone may use icons, inline forgoes them), underline (skip-ink:auto + underline-offset, or border-bottom/box-shadow), visited-treatment, aria-current-marker, download/file-indicator]
  polymorphic: "renders <a> by default; can BE a framework router Link via asChild/as (§implementation)"
api:
  props:
    - {name: href, type: string, required: true, description: "destination; NO href => not a real link"}
    - {name: variant, type: enum, values: [inline, standalone, quiet, inverse], default: inline, description: drives underline behaviour}
    - {name: target, type: enum, values: [_self, _blank, _parent, _top], default: _self}
    - {name: rel, type: string, description: "auto noopener noreferrer when target=_blank"}
    - {name: isExternal, type: boolean, default: false, description: external indicator + visually-hidden warning + rel}
    - {name: asChild/as, type: boolean/elementType, description: "router polymorphism — merge DS styling onto a framework router Link, emit one real <a> (§implementation)"}
    - {name: aria-current, type: enum, values: [page, step, location, true], description: current nav item (NOT aria-selected — that's tabs)}
  no-disabled: "links don't natively disable; if required: remove href + aria-disabled=true + role=link + pointer-events:none (+tabindex=-1) — but prefer rendering plain text"
states:
  runtime: [rest, hover, focus-visible, active, visited, current]
  notes:
    focus-visible: ":focus-visible not :focus (no persistent ring after mouse click)"
    visited: ":visited locked to a few colour properties + getComputedStyle lies (privacy); use for content/docs links, omit for app/nav"
variants:
  inline: "in running text; PERSISTENT underline at rest; no icons"
  standalone: "isolated; underline revealed on hover/focus (placement carries the cue); icons allowed"
  quiet: "muted, no underline; only where layout guarantees interactivity"
  inverse: "static white/black over imagery/dark, ignoring theme tokens"
  navigation: "in a <nav>; current item marked aria-current"
accessibility:
  wcag-criteria: ["1.4.1", "2.4.4", "2.4.9", "4.1.2", "1.4.11", "2.4.13", "2.4.1", "3.2.5"]
  semantics: "role=link via a REAL <a href>; the no-href anti-pattern (a w/o href, a[role=button], onClick div) is removed from the a11y tree + tab order"
  keyboard: "ENTER activates (NOT Space — Space scrolls; the tell vs button which takes both)"
  underline-contract: "inline link by colour ALONE fails 1.4.1 -> enforce the underline; contrast-only workaround (link-vs-text >=3:1 AND text-vs-bg >=4.5:1) rejected (cramps palette, fails dark mode)"
  aria-current: "page (site nav) / step (wizard) / location (breadcrumb) / true; a visual .active class alone is insufficient"
  new-tab: "target=_blank announced (visually-hidden 'opens in new tab' / external icon name) per 3.2.5; + rel=noopener noreferrer"
  skip-link: "first focusable, visually-hidden-until-focused (clip, not display:none), href=#main"
content:
  link-text: "descriptive + stands alone; NO 'click here'/'read more' bare (2.4.4/2.4.9); link the noun phrase; aria-label when space forces generic text"
  no-raw-urls: "never embed raw URLs in body (SR reads every char); hide in href"
  file-links: "state format + size ('Annual report (PDF, 2 MB)')"
motion:
  transition: "~150-200ms ease colour/underline on hover/focus; underline-grow via transform/opacity (no thrash)"
  reduce-motion: "drop translation/scale; opacity/colour only or snap"
i18n:
  rtl: "external icon to leading edge + mirrored horizontally (logical properties auto on dir=rtl)"
  expansion: "inline links wrap across lines without breaking underline or splitting icon-from-word; white-space:nowrap is an anti-pattern"
implementation:
  - "ALWAYS emit a real <a href> (progressive enhancement, middle/cmd-click, copy-link, SEO, a11y) — onClick div / no-href / href=# is the cardinal sin"
  - "router polymorphism: asChild/Slot (Radix) clones the framework-router child + merges styling -> one clean <a> (avoids <a><a> nesting + brittle as-prop typings); AppProvider context (Atlassian) is the boilerplate-light alternative but couples DS to the router; RouterProvider hook (React Aria) also acceptable — practice prefers asChild"
  - "target=_blank => auto rel=noopener noreferrer (reverse-tabnabbing + referrer privacy)"
  - "no-href: render plain text or warn; never a non-functional <a>"
  - "skip link: visually-hidden-until-focused, first focusable, href=#main"
  - "don't hand-roll — React Aria useLink/Link + RouterProvider, or Radix Slot for asChild"
composition:
  composes-with: [icon, nav-landmark, breadcrumbs, menu-item, framework-router-link]
  alternative-to: [button, link-button, routing-nav (links + aria-current, not a tablist)]
  supersedes: ["onClick-navigation div/span", "<a> without href / href=# / javascript:void(0)", "a[role=button] for navigation"]
  superseded-by: [button (when it's an action, not navigation)]
notes:
  contested:
    - "underline discipline (enforce for inline; reject contrast-only workaround)"
    - "router polymorphism (asChild/Slot preferred over context-injection / as-prop)"
    - "Anchor-for-non-textual-clickable-blocks as a separate concern (Atlassian) vs unified Link"
  boundary: "link-vs-button from the link side (URL change=link, in-place act=button; JS nav STILL uses <a href>); the routing-is-a-nav-of-links rule (tabs/segmented)"
  unverified:
    - "Polaris Web-Components migration (cross-brief claim; needs _source-text)"
    - "external-supplied 2026 version numbers; Atlassian AppProvider perf-at-scale claim"
  evolution: "onClick-div purged; asChild/Slot converged; aria-current=page standardised; new-tab rel=noopener default; Web-Components migration"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-link/` (16 June 2026), the routing/`aria-current` adjacent thread off Tabs and Segmented Control, and the link side of the Button link-vs-button boundary. Both passes converged on the spine — the `href` contract as non-negotiable (the no-href / `onClick`-div / `href="#"` anti-pattern), link-vs-button from the link side (Enter-not-Space, exposes a URL) with JS-navigation still emitting a real `<a href>`, the LinkButton, the inline/standalone/quiet variants and the underline discipline (colour-alone fails 1.4.1; the practice enforces the underline for inline and rejects the contrast-only workaround), internal-vs-external with the external indicator + `target="_blank"` ⇒ `rel="noopener noreferrer"` + new-tab warning (reverse-tabnabbing), `aria-current` (page/step/location/true) as the nav signal distinct from Tabs' `aria-selected`, the `:visited` privacy constraints, the framework-router polymorphism resolved to `asChild`/Slot (with `AppProvider` context and `RouterProvider` as alternatives), skip links, the no-true-disabled handling, descriptive link text, and `Link`/`LinkButton` naming. External-pass contributions folded in: the `:visited` history-sniffing background and the colour-only constraint, the `text-decoration-skip-ink`/`underline-offset` engineering, the inverse/static-colour variant, the Atlassian `AppProvider` context alternative and the `Anchor`-for-non-textual-blocks distinction, the standalone-icons / inline-no-icons rule, and the disabled-link sequence (`aria-disabled` + `role=link` + `pointer-events:none`). Claude-pass contributions: the framing as the routing counterpart the form/navigation boundaries kept opening, the Enter-not-Space tell, and the `asChild`-preferred resolution. The Polaris Web-Components migration, the 2026 version numbers, and the Atlassian context perf-at-scale note are flagged unverified. Conformant to `components/_schema.md`. Closes the routing thread; Breadcrumbs and Menu are the Navigation briefs that build on Link.*
