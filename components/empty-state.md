---
okf_version: "0.1"
type: component-brief
title: Empty State
description: The fifth and final Feedback brief, which closes the Feedback category — the rendered content of a data container when there's nothing to show, turning absence into guidance. A field-truth study of the genre taxonomy (first-use/no-results/all-done/error/no-permission) that drives content + action, the loading/content/empty/error terminal-states machine, the genre->action mapping, the illustration question (decorative/aria-hidden, the over-illustration cost), the dynamic no-results status announcement (the lightest reuse of the Feedback live-region pattern) + focus-stays-in-search, the table-replacement methodology, the FOES trap, and content/tone by genre — with the practice's defaults.
tags: [components, feedback]
category: Feedback
status: stable
aliases: [empty, blankslate, illustrated-message, zero-state, no-results]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Empty State

> An Empty State is the **rendered content of a data container when there's nothing to show** — it turns an unacceptable blank container (a dead end) into an actionable, contextual waypoint. It is the fifth and final Feedback brief and **closes the Feedback category**. It inherits **Button** (the CTA), **Icon**/illustration (the visual), **Link** (secondary/inline links), and — its lightest touch — the **live-region pattern Toast established** (only for the *dynamic no-results announcement*, §6). It is **composed by the Data components** — an Empty State *is* the zero-state of a Table, List, Tree, search-results grid, or card. Two framings define it: the **genre taxonomy** (the *why* drives the content + action — first-use/onboarding, no-results, all-done, error, no-permission), and the **terminal-states machine** (a container goes `idle → loading → {content | empty | error | no-permission}`; an empty result is *expected*, an error is a *failure*). The defining accessibility nuance separates the **static rendered content** (not a live region) from the **dynamic no-results announcement** (the one live-region touch) — and the field's settled rule that **focus stays in the search field**, never yanked to the empty state.

---

## 1. Framing

An Empty State is one terminal state of a data container's lifecycle (`loading → {content | empty | error | no-permission}`). It inherits **Button** (CTA — see button), **Icon**/illustration (visual — see icon), **Link** (links — see link), and **lightly the live-region pattern from Toast** (the no-results announcement, §6). It's **composed by the Data hosts** (Table/List/Tree).

**The genre taxonomy (the headline — the *why* drives content + action):**
- **first-use / onboarding** — the system works but no data was ever created; **the highest-value state** (a feature's first impression), demanding a prominent **create** CTA.
- **no-results** — a user search/filter returned zero; needs immediate **adjust/clear** guidance.
- **user-cleared / all-done** — inbox-zero / task complete; a success state, often **no CTA**.
- **error / failure** — a *localized* container load failure (the empty-vs-error boundary); degrades to an error-flavored empty state to hold the layout, with a **retry**.
- **no-permission** — the data exists but the user lacks access; pivots to **request-access**.

What it *isn't*: a **loading** state (→ Skeleton/Progress, the *in-between* — see progress, skeleton; an empty result is *expected*, loading is transient), or a **system error** that warrants a persistent surface (→ Banner/Inline — see banner, inline-message; a 500 is a *failure*, not expected absence). Why systems disagree: the genre taxonomy, the illustration question, the empty-vs-error treatment, and the table-replacement methodology.

## 2. Anatomy and parts
A standardised vertical hierarchy (center-aligned for a void; left-aligned/inline for tight table rows; container queries scale padding/font in narrow bounds — Primer):
- **visual** — illustration or **Icon** (or none); **decorative** (`aria-hidden` — meaning is in the text, §6); the bespoke-illustration-cost trap (§5/§13).
- **heading** — a short, positive/neutral title; **the heading level must map to the document outline** (Atlassian's `headingLevel`, default 4 — §6/§11).
- **body / description** — lower-contrast text: *why* it's empty + *what to do*.
- **primary action** (inherits Button) — the genre-mapped CTA.
- **secondary action** — a tertiary Button or **Link** (docs / request access).
- **container** — the host region (full-page / in-card / in-row / in-section).

## 3. Properties / API
- **API paradigm — composable parts vs monolithic** (a genuine schism): **monolithic** (Polaris/Atlassian/Ant — `heading`/`description`/`image`/`primaryAction`/`secondaryAction` string-or-config props; rigorous tokens but **rigid** — the recurring trap is injecting rich HTML / a troubleshooting `<ul>` / multiple actions into a string `description`, prompting "unsquish"/margin-override requests) vs **composable** (Chakra — `EmptyState.Root`/`.Indicator`/`.Title`/`.Description`/`.Content`; inversion of control, slots arbitrary DOM without breaking tokens). **The practice default: composable parts** with a monolithic convenience wrapper for the common case.
- **`headingLevel`** (Atlassian, default 4) — the heading-outline injector (§6).
- **`as` / `asChild`** — polymorphic element (a `<div>` → semantic `<section>`).
- **`image` / `imageContained`** (Ant `image` — default vs `PRESENTED_IMAGE_SIMPLE`).
- **`size`** — sm/md/lg (compact in-row vs full-page padding/scale).
- genre is usually **content-driven** (heading/body/action), not a heavy variant enum.

## 4. States and variants
- **No intrinsic interactive states** — it's a layout wrapper; hover/focus/pressed belong to its composed Button/Link.
- **By genre (the primary axis):** **first-use** (high prominence, illustration, encouraging, primary create CTA) / **no-results** (compact, monochrome icon, clear-filters CTA) / **all-done** (restrained, success icon, often *no* CTA) / **error** (stripped-back utility, warning icon, retry CTA) / **no-permission** (lock icon, request-access CTA).
- **By visual:** illustrated / icon-only / text-only.
- **By placement/size:** full-page (max padding, large scale) / in-card / in-table-row (strip the description + illustration, text only) / in-section; compact vs full.

## 5. Usage guidance
- **Never leave a blank container** — absence without guidance is a dead end that fractures trust and momentum; implement an Empty State across every container that iterates data (Table/List/Tree).
- **The genre → action mapping (the core rule):**
  - **first-use** → a primary **create** CTA + encouraging copy; treat as **onboarding** (a localized, just-in-time alternative to intrusive modal tours).
  - **no-results** → **clear-filters / adjust / broaden** (secondary Button/Link — the user is exploring, not creating); help them recover.
  - **all-done** → often **no action** (or a gentle next step) — let the user enjoy completion.
  - **error** → **retry / reload** (a functional escape hatch).
  - **no-permission** → **request-access / contact-admin**.
- **The table-replacement methodology (the recurring trap):** when a Table is empty, rendering the column headers + pagination around an empty message creates cognitive load and makes AT announce empty table semantics first. Carbon: for a **first-use** empty table, **unmount the entire shell** (headers/pagination/footer) and replace it with the Empty State. But for a **transient no-results** (active filtering), **preserve the headers** (Polaris's point — hiding them disorients a user iterating filters). So: **full-replacement for first-use, inline-replacement for no-results.**
- **Don't use an Empty State for:** the **loading** in-between (→ Skeleton/Progress), or a **failure warranting a persistent error surface** (→ Banner/Inline — the error-flavored empty state is for *in-container* "couldn't load this list", not a page-level system error).

## 6. Accessibility
- **The static content is NOT a live region** — wrapping the empty-state visual in `aria-live`/`role=alert` is a disastrous anti-pattern (it spontaneously reads paragraphs + alt text + button labels the moment data vanishes, destroying spatial awareness). It's rendered content, read in document order.
- **The dynamic no-results announcement (the one live-region touch, reusing Toast's pattern):** when a search/filter *empties the results in response to a user action*, a **permanently-mounted, visually-hidden `role="status"` `aria-live="polite"` element** (decoupled from the empty-state DOM — the pre-existing-region rule) updates to announce the count — **"No results found" / "0 items"** — so a non-visual user gets parity with the visual appearance.
- **Focus stays in the search field (the settled rule)** — do **not** programmatically move focus to the empty state's heading/CTA when a query empties the results; moving focus steals agency, and the user needs to stay in the input to backspace/broaden. WAI-ARIA forbids the focus-steal; the status announcement covers the non-visual case.
- **The illustration is decorative** — `aria-hidden="true"` on inline SVGs, or `alt=""` + omit `title` on `<img>` (the heading/body already state the context — an informative `alt` is redundant audible clutter).
- **The heading in the outline** — interpolate the correct `<h*>` for the container's position (Atlassian's `headingLevel`, default 4); a hardcoded level breaks the rotor/document outline (the Banner/Inline-Message lesson).
- **The action is in the tab order** — a normal Button.
- **Color-not-sole-carrier** — the genre is conveyed by heading/body text, not colour.
- **WCAG SCs:** 4.1.3 (Status Messages — the dynamic no-results announcement), 1.3.1 / 2.4.6 (heading/structure in the outline), 1.1.1 (decorative illustration), 2.4.3 (focus order — *don't* steal focus), plus the action Button's SCs. (A static empty state mostly needs correct semantic structure + the decorative-image handling.)

## 7. Content guidelines
- **Heading — positive, active, propels forward** — "Start by adding a project" / "Your inbox is clear" / "No results for 'invoices'", never "No data" / "Nothing here" / a subtly hostile "You don't have any projects" / "Error". Don't shame the user (Intuit/NNG).
- **Body — the "Why + What" heuristic** — explain *why* it's empty (the condition) + *what to do* (the resolution). Carbon's error-condition mapping: **permissions** ("you lack access" + how to request) / **system fault** ("an external failure" + a status log/retry) / **configuration required** ("unconfigured" + the first step) / **unsupported action** ("invalid parameter" + the supported formats).
- **Action labels — imperative verbs matching the heading** — "Create project", "Clear filters", "Try again", "Request access"; never "OK"/"Click here"/"Submit".
- **Tone by genre** — **encouraging** (first-use = opportunity), **helpful** (no-results = recovery), **reassuring** (all-done), **no-blame** (error = "We couldn't load this", constructive over technical fault codes — NNG).
- **First-use is the highest-value copy** — it's onboarding; invest in it. (i18n: avoid abbreviations, keep sentences short for ~1.5× expansion — §9.)

## 8. Motion and transition
Restrained — the empty state appears when content is *removed* or *fails*, so aggressive motion (bouncing illustrations) exacerbates the broken-interface feeling. A minimal fast fade-in (~150–200ms) reduces layout-shift jarring while staying calm. **Implementation trap (Polaris-documented):** an illustration initialised `opacity: 0` and faded in via a JS-appended `--loaded` class **gets permanently stuck at zero opacity** when the load event doesn't fire during rapid client-side routing / unexpected remounts — leaving a blank gap. **Favor pure CSS `@keyframes` fade-ins over brittle JS class toggling.** Under `prefers-reduced-motion: reduce`, snap to full opacity instantly. No decorative illustration animation. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** — center-aligned layouts stay stable, but **horizontal/compact variants must use logical properties** (`margin-inline-start`/`end`, not `margin-left`) so the illustration mirrors to the correct side; the action row mirrors.
- **Text expansion** — descriptions expand up to ~1.5× (de/ru); the container (often a constrained card) must use **flexible flexbox** (no hardcoded heights) so multiline copy wraps without clipping the action button.
- **Illustration cultural neutrality** — human figures, hand gestures, culturally-specific clothing, and hyper-local metaphors fail to translate and can offend; lean to **abstract/geometric or systemic iconography**. Localise the heading/body/action; the no-results echo handles the user's query term. (See 13-internationalization-and-rtl.)

## 10. Naming
The field splits on framing: **`EmptyState`**/**`Empty State`** (Polaris, Atlassian, Chakra, Carbon — names the *state*, the consensus), **`Blankslate`** (Primer — the blank-canvas metaphor), **`IllustratedMessage`** (Spectrum — names the *form*, unifying empty/error/no-results under one component), **`Empty`** (Ant — terse). **The practice default: `EmptyState`** — it aligns with the terminal-state mental model of state-driven frameworks (React/Vue/Svelte) and is the consensus. Note Spectrum's insight: empty/error/no-results share a *form* (visual + message + action), so a system may implement one `IllustratedMessage`-style primitive and vary the content; the practice keeps `EmptyState` as the name and composes the error/no-results cases from it. Deprecate ambiguous aliases (`NoData`, `ZeroState`) for lexicon unity. Aliases to map: `Empty`, `Blankslate`, `IllustratedMessage`, `ZeroState`, `NoResults`.

## 11. Implementation notes
- **The terminal-state machine** — the host renders one of `idle/loading` (Skeleton/Progress) → `content | empty | error | no-permission`; the Empty State is the `empty` (+ optionally `error`/`no-permission`) branch.
- **The Flash of Empty State (FOES) trap** — a data array is `[]` *before* the fetch resolves, so a naive `data.length === 0` check **flashes the empty state for milliseconds** before the skeleton/data. Guard it: **`if (!isLoading && data.length === 0) return <EmptyState/>`** — never show empty *during* loading.
- **The no-results announcement + focus** — push the count to a pre-existing polite `role=status` region; **leave focus in the search field** (§6).
- **The decorative illustration + dark-mode trap** — `aria-hidden`/`alt=""`; and **SVGs must use `currentColor`** for fill/stroke so theme tokens recolour them (Ant's default multi-layer SVGs blow out white on dark — the documented fix is the token-hooked simple variant / `currentColor`).
- **Heading level** — interpolate the correct `<h*>` (`headingLevel` prop, default 4).
- **Composable parts** — slot illustration/heading/description/actions so one primitive composes first-use vs no-results vs error (and avoids constant minor releases to accept new edge-case props — tertiary buttons, legal disclaimers).
- **Container queries** — scale padding/font to the bounding box (Primer) so the same component works full-page and in a narrow card.
- **Don't hand-roll** — Polaris `EmptyState` / Primer `Blankslate` / Spectrum `IllustratedMessage` / Chakra `EmptyState`; skin them; wire the no-results announcement at the data-host layer.

## 12. Related and alternative components
- **Stands on:** Button (the CTA — see button), Icon/illustration (the visual — see icon), Link (secondary/inline links — see link), and **lightly the live-region pattern** from Toast (the dynamic no-results announcement — see toast).
- **Composed by:** Table / List / Tree / search-results / card — the data hosts whose zero-state *is* the empty state (see table/list/tree for the hosts).
- **Alternative to / boundary with:** **Skeleton / Progress** (the *loading* terminal state — the in-between; transition without a flash — see progress, skeleton), **Banner / Inline Message** (the *error/failure* terminal state — a persistent error surface vs an in-container error-flavored empty state — see banner, inline-message).

(The fifth and final Feedback brief — the zero-state content of a data container, anchored by the genre taxonomy and the loading/content/empty/error terminal-states machine; the live-region pattern's lightest touch. It **closes the Feedback category**. See button for the CTA, icon for the visual, link for the links, toast for the no-results live-region touch, progress/skeleton for the loading boundary, banner/inline-message for the error boundary, table/list/tree for the data hosts that compose it. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **From technical fallback to growth surface** — the empty state moved from a place to dump "404"/error codes to a recognised **user-acquisition and onboarding** surface (product-led growth); first-use especially is a feature's first impression.
2. **The genre taxonomy matured** — from a single generic "empty" to distinct genres (first-use/no-results/all-done/error/no-permission), each with its own content + action.
3. **Illustration restraint** — the flat-design era's massive bespoke-illustration libraries proved costly (maintenance, cross-platform consistency, cultural neutrality, dark-mode incompatibility); modern systems lean to monochrome systemic icons for all but high-value first-use screens.
4. **The composable-parts shift** — from rigid monolithic prop APIs to composable sub-components (Chakra) for flexibility.
5. **The accessibility consensus settled** — decouple the static visual rendering from the dynamic `role=status` announcement; don't steal focus; decorative illustrations `aria-hidden`.

## 14. Sources cited
(Conservative; the external pass cited Polaris v13.9.5, Spectrum IllustratedMessage v3.47.0, Primer Blankslate v38.26.0, Atlassian EmptyState v7.6.1, Ant Empty v6.4.4 — held loosely and flagged unverified.) **Shopify Polaris** `EmptyState` (illustration + heading + action; the opacity-load-class motion bug; the table header-during-filter debate) (2024–2026); **Adobe Spectrum** `IllustratedMessage` (the unified empty/error/no-results form; logical properties) (2024–2026); **GitHub Primer** `Blankslate` (container queries) (2024–2026); **Atlassian** `EmptyState` (`headingLevel` default 4) (2024–2026); **Ant Design** `Empty` (image/`PRESENTED_IMAGE_SIMPLE`, the dark-mode SVG trap) (2024–2026); **Chakra UI** `EmptyState` (Root/Indicator/Title/Description/Content parts) (2024–2026); **IBM Carbon** the empty-state / no-data pattern + the table-shell-replacement methodology + the Why+What error mapping (2024–2026); **Google Material 3** empty-state guidance (2024–2026); **Base Web (Uber)** (2024); **Intuit / Nielsen Norman Group** content heuristics (no-blame, constructive over technical); **WAI-ARIA APG** — no formal empty-state pattern (content + a `role=status` live region for dynamic no-results); the inherited Feedback live-region pattern (see toast). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.3, 1.3.1, 2.4.6, 1.1.1, 2.4.3.

## 15. Agent-consumable schema

```yaml
identity:
  id: empty-state
  name: Empty State
  aliases: [empty, blankslate, illustrated-message, zero-state, no-results]
  category: feedback
  status: stable
description: >
  The rendered content of a data container when there's nothing to show —
  turns absence into guidance. One terminal state of the
  loading->{content|empty|error|no-permission} container machine; the WHY
  (genre) drives content+action; composed BY the Data components (Table/List/
  Tree) as their zero-state. Closes the Feedback category. NOT a loading
  Skeleton/Progress (the in-between; empty is EXPECTED), NOT a Banner/Inline
  error (a system FAILURE vs expected absence).
anatomy:
  parts:
    - "visual: illustration or Icon (or none); DECORATIVE aria-hidden — meaning in the text; bespoke-illustration-cost trap"
    - "heading: short positive/neutral; heading level MAPS to the document outline (headingLevel, default 4)"
    - "body/description: lower-contrast; WHY it's empty + WHAT to do"
    - "primary action (inherits button; genre-mapped CTA)"
    - "secondary action (tertiary button / Link — docs/request-access)"
    - "container (center-aligned for a void; left/inline for tight rows; container queries scale padding/font)"
api:
  inherits: [button (CTA), icon (visual), link (links), toast (live-region pattern — no-results only)]
  paradigm: "composable parts (Chakra EmptyState.Root/.Indicator/.Title/.Description/.Content — practice default) vs monolithic (Polaris/Atlassian/Ant heading/description/image/action props — rigid, the rich-HTML-in-a-string-prop trap)"
  props:
    - {name: headingLevel, type: number, default: 4, description: "the heading-outline injector (Atlassian)"}
    - {name: as/asChild, type: "elementType/boolean", description: "polymorphic (div -> section)"}
    - {name: image/imageContained, type: "node", description: "Ant image vs PRESENTED_IMAGE_SIMPLE"}
    - {name: size, type: enum, values: [sm, md, lg], description: "compact in-row vs full-page"}
  genre: "usually content-driven (heading/body/action), not a heavy variant enum"
states:
  intrinsic: "none (layout wrapper; hover/focus/pressed belong to the composed Button/Link)"
  by-genre: "first-use (high prominence, illustration, create CTA, encouraging) / no-results (compact, mono icon, clear-filters CTA) / all-done (restrained, success icon, often NO CTA) / error (utility, warning icon, retry CTA) / no-permission (lock icon, request-access CTA)"
variants:
  visual: [illustrated, icon-only, text-only]
  placement: "full-page / in-card / in-table-row (strip description+illustration) / in-section; compact vs full"
accessibility:
  wcag-criteria: ["4.1.3", "1.3.1", "2.4.6", "1.1.1", "2.4.3"]
  not-a-live-region: "the static visual is NOT aria-live/role=alert (would spam paragraphs+alt+labels on data vanish); rendered content, read in order"
  no-results-announcement: "the ONE live-region touch — a permanently-mounted visually-hidden role=status aria-live=polite (decoupled from the empty-state DOM) updates to the count ('No results found') on a user-action emptying the results (reuses Toast)"
  focus: "STAYS in the search field on no-results — NEVER steal focus to the empty state (WAI-ARIA forbids it; the user needs to backspace/broaden)"
  illustration: "DECORATIVE — aria-hidden=true on SVG / alt='' + omit title on img (heading/body carry the meaning)"
  heading-outline: "interpolate the correct h* (headingLevel default 4); hardcoded level breaks the rotor/outline"
  color: "genre conveyed by text, not colour"
content:
  heading: "positive/active, propels forward ('Start by adding a project'/'Your inbox is clear'/'No results for X'); NEVER 'No data'/'Nothing here'/'Error'; no user-blame"
  body: "Why + What heuristic (the condition + the resolution); Carbon mapping — permissions/system-fault/config-required/unsupported-action each get explanation + resolution"
  actions: "imperative verbs matching the heading ('Create project'/'Clear filters'/'Try again'/'Request access'); never OK/Click here/Submit"
  tone: "encouraging (first-use=opportunity), helpful (no-results=recovery), reassuring (all-done), no-blame (error, constructive over fault codes — NNG); first-use is the highest-value copy (onboarding)"
motion:
  appearance: "minimal fade-in ~150-200ms (restrained — don't draw frantic attention to absence)"
  trap: "Polaris opacity:0 locked by a missing JS --loaded class on client routing -> blank gap; favor pure CSS @keyframes over JS class toggling"
  reduce-motion: "snap to full opacity instantly; no decorative illustration animation"
i18n:
  rtl: "center layouts stable; horizontal/compact MUST use logical properties (margin-inline-start/end) so the illustration mirrors"
  expansion: "descriptions ~1.5x (de/ru) — flexible flexbox, no hardcoded heights, wrap without clipping the CTA; avoid abbreviations"
  illustration: "cultural neutrality — avoid human figures/gestures/local metaphors; lean abstract/geometric/systemic icons"
implementation:
  - "terminal-state machine: host renders loading (Skeleton/Progress) -> content|empty|error|no-permission; Empty State is the empty (+optionally error/no-permission) branch"
  - "FLASH OF EMPTY STATE (FOES) trap: data array is [] before fetch resolves -> naive data.length===0 flashes the empty state; guard with if (!isLoading && data.length === 0) return <EmptyState/>"
  - "no-results: push count to a pre-existing polite role=status region; LEAVE FOCUS in the search field"
  - "decorative illustration aria-hidden/alt=''; SVGs use currentColor for dark-mode theme recolour (Ant multi-layer SVGs blow out white on dark -> token-hooked simple variant)"
  - "heading level interpolation (headingLevel, default 4)"
  - "table-replacement: full-replace the shell for first-use; preserve headers (inline-replace) for transient no-results"
  - "composable parts so one primitive composes first-use/no-results/error (avoids minor releases for edge-case props); container queries scale to the bounding box"
  - "don't hand-roll — Polaris EmptyState/Primer Blankslate/Spectrum IllustratedMessage/Chakra EmptyState; wire no-results at the data host"
composition:
  stands-on: [button (CTA), icon/illustration (visual), link (links), toast (live-region pattern — no-results only)]
  composed-by: [table, list, tree, search-results, card]
  alternative-to: [skeleton/progress (loading terminal state — in-between), banner/inline-message (error/failure terminal state — persistent error vs in-container error-flavored empty)]
notes:
  contested:
    - "the genre taxonomy (first-use/no-results/all-done/error/no-permission)"
    - "empty-vs-error treatment (error-flavored empty vs Banner/Inline)"
    - "the illustration question (illustrated vs icon vs text; bespoke cost)"
    - "table-replacement (full-replace shell vs preserve headers — first-use vs no-results compromise)"
    - "unified IllustratedMessage (one form) vs distinct EmptyState; composable vs monolithic API"
  trap:
    - "leaving a blank container (dead end)"
    - "FOES — showing empty during loading (guard with !isLoading)"
    - "the static visual as a live region (SR spam); stealing focus to the empty state on no-results"
    - "an informative alt on a decorative illustration; generic 'Empty'/'Nothing here'/'Error' heading"
    - "wrong/no action for the genre; over-illustration (cost + dark-mode blowout — use currentColor)"
    - "breaking the heading outline; opacity:0 locked by a missing JS load class"
  inherited: "Button CTA; Icon/illustration visual; Link links; Toast live-region pattern (no-results only — the lightest reuse)"
  role-in-family: "the fifth and final Feedback brief — the zero-state content; closes the Feedback category; the live-region pattern's lightest touch (only the dynamic no-results announcement)"
  evolution: "technical-fallback -> growth/onboarding surface; genre taxonomy matured; illustration restraint (monochrome icons over bespoke); composable-parts shift; a11y consensus (decouple static content from the dynamic status announcement, don't steal focus)"
  unverified:
    - "external 2026 version numbers"
    - "the no-results-announcement + focus AT specifics — verify against current screen readers"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-empty-state/` (16 June 2026), the fifth and final Feedback brief, which closes the Feedback category — the rendered content of a data container when there's nothing to show. It stands on Button (the CTA), Icon/illustration (the visual), Link (links), and lightly the live-region pattern Toast established (the dynamic no-results announcement only — the lightest reuse in the category), and is composed by the Data hosts (Table/List/Tree). The two passes converged almost completely — the genre taxonomy (first-use/no-results/all-done/error/no-permission, the *why* driving content + action), the loading/content/empty/error terminal-states machine (empty is *expected*, error is a *failure*), the genre→action mapping, the illustration-as-decorative rule, the static-content-is-not-a-live-region vs the dynamic no-results `role=status` announcement, the focus-stays-in-search rule, the heading-outline interpolation, content/tone-by-genre, and the never-leave-a-blank-container + first-use-as-onboarding POV. External-pass contributions folded in: the **Flash of Empty State (FOES)** trap (`if (!isLoading && data.length === 0)`), the **table-replacement methodology** (Carbon full-shell-replace for first-use vs preserve-headers for transient no-results — the Polaris debate), the **SVG dark-mode `currentColor`** trap (Ant's multi-layer-SVG blowout), Atlassian's concrete **`headingLevel`** prop (default 4), Primer's container-queries scaling, the Carbon Why+What error-condition mapping, the Polaris opacity-locked-by-missing-JS-load-class motion bug, the composable-vs-monolithic API schism + the rich-HTML-in-a-string-prop trap, and the illustration cultural-neutrality concern. Claude-pass contributions: the framing as the genre-taxonomy + terminal-states anchor, the lightest-live-region-touch observation, and the substrate map. The 2026 version numbers and the no-results-announcement AT specifics are flagged unverified. Conformant to `components/_schema.md`. The fifth and final Feedback brief — with Toast, Banner, Inline Message, Progress, and Empty State, the Feedback category is complete, the third category to close, and the live-region pattern has now been applied across all five (transient, persistent, field-associated, task-progress, and — here — its lightest no-results touch).*
