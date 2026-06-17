---
okf_version: "0.1"
type: component-brief
title: Badge
description: The small non-interactive indicator primitive — a field-truth study of the genre split (count overlay / presence dot / status pill) + the naming morass (Fluent/Primer's tripartite split vs MUI/Ant's one-Badge-overlay vs Polaris/Chakra's status-pill Badge), the Badge-vs-Tag boundary (non-interactive indicator vs interactive/removable token), the announcement contract (count in the HOST's accessible name not a floating number; the dot's text equivalent; the dynamic-count role=status live region; aria-hidden the visual), the wrapper-vs-sibling overlap model + circular-vs-rectangular positioning + the cutout stroke + the RTL flip, color-not-sole-carrier severity, and count handling (max-cap/zero) — with the practice's defaults.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [CounterBadge, PresenceBadge, NotificationBadge, Label, CounterLabel, StateLabel, Counter, Notification dot, Pill, Indicator, Status]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Badge

> A Badge is a **small, non-interactive indicator** that annotates a host or a piece of content with a tiny quantum of state. The headline problem is that **"Badge" names three structurally different components** — the **count** (a number overlaid on a host: a bell with "3"), the **dot** (a contentless attention/presence marker: unread, online), and the **status pill** (standalone inline state text: "Active"/"Draft"/"Beta"). The dividing line that resolves the genre split is the **accessibility contract**: the overlay genres (count/dot) are **`aria-hidden`, their meaning injected into the *host's* accessible name** ("Notifications, 3 unread"); the status pill is **content that announces its own text**. Those are opposite contracts — which is why the field's most modern systems (Fluent v9, Primer) split them into separate components rather than treating them as one component's variants. It inherits **Icon** (the optional severity icon + the icon-button host — see icon), the **color-not-sole-carrier severity model** from the Feedback family (info/success/warning/error/neutral as color + text, never hue alone — see banner, toast), and the **live-region announcement pattern** from Toast for a dynamically-changing count (see toast). What it **isn't**: a **Tag/Chip** (the interactive, removable token — Badge holds the boundary at *non-interactive, non-removable*; if it has an `×`, an `onClick`, or a selected state, it's a Tag — see tag) or a **Toast/Banner** (the feedback surfaces — Badge informs passively, it doesn't alert; see toast, banner).

---

## 1. Framing

A Badge is **structurally inert metadata** — it has no states of its own (no hover, focus, active, disabled), no role of its own when overlaid, and no removability. It annotates; the host (or a Tag) carries any interactivity. Beyond that floor, the term fractures into three genres serving different structural and communicative purposes:

- **The count badge** — a number absolute-positioned as an overlay on a host (an icon button, an avatar, a tab, a nav item), signalling a quantitative accumulation (unread notifications, cart items). Dimensionally constrained, capped at a max ("99+"), with rules governing the zero value.
- **The dot badge** — a contentless filled circle overlaid on a host, signalling a *qualitative binary* — either an event ("something new / unread") or an availability state ("online / away / busy" on an avatar). It strips all text to minimize noise; its meaning is carried by color + placement + a *hidden text equivalent*.
- **The status / label pill** — a standalone inline element holding a short text string (and optionally a leading icon) annotating the lifecycle state of an adjacent entity ("Paid", "Beta", "Active"). It sits in the normal document flow, not floating via absolute positioning.

The naming morass is the field's clearest signal of the split. **Fluent v9** is the cleanest taxonomy: `Badge` (status pill) / `CounterBadge` (count) / `PresenceBadge` (dot). **Primer** echoes it exactly: `Label` / `CounterLabel` / `StateLabel`. **MUI** and **Ant** keep `Badge` for the *overlay* (count + dot) and push the status pill to `Chip`/`Tag`/`Badge status`. **Polaris**, **Chakra**, **Spectrum**, **Carbon** appropriate `Badge` for the *status pill* and handle overlays separately. The same word points at the count overlay in one system and the status pill in the next.

Why systems disagree, and the resolving principle: the **accessibility contracts are opposite**. A count/dot overlay must be **`aria-hidden` with its meaning in the host's name** (a screen reader landing on a bell that just says "3" is meaningless); a status pill is **content that announces its own text** in flow. A single component cannot cleanly serve both contracts, which is what tips the most modern field leaders — and this brief — toward the **tripartite split** over a one-component-with-a-`variant` model (§10).

## 2. Anatomy and parts

A unified ontology, four atomic parts (which apply depends on genre):

- **the host substrate** *(overlay genres only)* — the anchor the badge is absolute-positioned over (`IconButton`, `Avatar`, `Tab`, nav item). Not part of the badge's own DOM in sibling layouts, but the badge's positioning math depends entirely on the host's bounding box and border-radius. In the wrapper model (MUI/Ant) the host is the badge's `children`.
- **the badge surface** — the visual container (background, padding, radius, the **cutout stroke**). A count surface scales horizontally from a circle (single digit) to a pill (multi-digit); a dot is locked to a fixed symmetrical dimension (≈6–12px per the density scale); an overlaid surface carries a thick **stroke/cutout matching the canvas color** to separate it from the host silhouette.
- **the typographic layer** — the number or short status text, mapped to the smallest type token (`caption`/`label-small`) at medium/semibold weight to stay legible against high-contrast semantic fills.
- **the optional leading icon** *(status + presence)* — a severity icon in a status pill (a check/warning/alert, so color isn't the sole carrier — §6), or a state glyph in a presence dot. Overlaid *count* badges rarely carry icons (no room atop an already icon-heavy host). Inherits Icon (see icon).

Conspicuously absent: **interactive targets**. No hover/focus/active, no focus ring, no cursor change native to the badge. Any perceived interactivity is inherited from the host or a parent container. The Badge is structurally inert.

## 3. Properties / API

| Concern | MUI | Ant | Fluent v9 | Practice default |
| --- | --- | --- | --- | --- |
| Payload | `badgeContent` | `count` / `text` | implicit child | `value` |
| Genre | `variant="standard\|dot"` | `dot` | split components | split components (+ `variant` on the overlay) |
| Max cap | `max` (99) | `overflowCount` (99) | `overflowCount` | `max` (99) |
| Zero | `showZero` | `showZero` | `showZero` | `showZero` (default false → hide) |
| Severity | `color` | `status` / `color` | `color` | `tone` / `severity` (semantic) |
| Overlap math | `overlap` | `offset` | — | `overlap="rectangular\|circular"` |
| Placement | `anchorOrigin` | `placement` | `position` | `anchorOrigin` (logical) |

**The defining architectural fork — the host relationship.** The overlay genres model the host two ways. The **wrapper / content-injection model** (MUI, Ant — `<Badge><IconButton/></Badge>`) lets the badge measure its children, apply `position: relative` to the wrapper and `position: absolute` to the surface, and own the logical positioning entirely — abstracting the CSS math away from the product developer. The **sibling model** (Primer's `<CounterLabel>` as a sibling) expects the parent flex/grid to position it manually. **The practice favors the wrapper model for overlay genres** — it slashes implementation errors and layout drift. (The inline status pill has no host and needs neither.)

**Zero handling** converges: a count of `0` doesn't warrant a high-contrast attention marker, so the badge **hides at zero by default**, with `showZero` the explicit opt-in to force "0" (typically dropping to a neutral fill). This keeps `count > 0 ? <Badge/> : null` ternaries out of product code.

**Severity is locked to semantic tones**, not arbitrary hex/`colorScheme="red"`. Polaris (`tone`) and Spectrum constrain to `critical`/`positive`/`warning`/`info`/`neutral`-style enums — enforcing contextual meaning, predictable theming, and accessible contrast (§6).

**The accessible-label wiring** is not a style prop but the load-bearing surface: the overlay badge does not announce itself; the **host's accessible name** carries the count/dot meaning (§6). A well-designed API exposes a way to compose the host's label (or documents the consumer's obligation to wire it).

## 4. States and variants

- **States:** effectively **none** of the badge's own — it's non-interactive, so no hover/focus/active/disabled. The runtime axis is **content change**: the **zero state** (`value === 0` → hidden by default; `showZero` forces "0" on a neutral fill, often via `transform: scale(0)`→`scale(1)` for a graceful exit), the **overflow state** (`value > max` → `{max}+`, e.g. "99+"; high-volume dashboards may raise `max` to 999), and the count **incrementing**. These are *content* changes announced via the host (§6), not interaction states.
- **Variants:**
  - **genre:** count / dot / status(pill).
  - **severity / tone** (status + count color): info / success / warning / error / neutral.
  - **placement:** overlaid (anchored to a host corner, with the **cutout stroke**) vs standalone/inline (status pill — solid/subtle fill, no stroke).
  - **size:** **small** (dense UIs / small hosts — often two-digit-max before overflow), **standard/medium** (the baseline, sized to overlay 40–48px touch targets), **large** (status pills beside h1/h2 headings).
  - **count edge states:** zero (hidden / shown), overflow (`{max}+`), dot-on-overflow (some systems collapse a too-large count to a dot).

## 5. Usage guidance

- **Count** — for a *pending action / unread accumulation / queue size* attached to the navigational vector that resolves it ("3" over an Inbox, "5" over a Cart). A passive prompt to action; the number must be **actionable** — if the exact value doesn't matter, prefer a dot.
- **Dot** — when the exact integer is unknown, expensive to compute, or irrelevant; it answers the boolean "is there new activity?". Lower visual weight than a count; the standard for **avatar presence** (online/offline — Avatar the host, not yet briefed).
- **Status pill** — inline beside data entities in tables/lists/headers to denote lifecycle state ("Pending"/"Authorized"/"Voided").
- **Don't use a Badge for:**
  - An **interactive/removable token** → a **Tag/Chip** (filter chips, removable selections). The boundary: a Badge has no `onClick`, no `×`, no selected state. (See tag — the boundary is now drawn from both sides.)
  - A **feedback announcement** → a **Toast** (transient) or **Banner** (persistent) — see toast, banner. Badges *inform passively*; they don't *alert*. Relying on a badge to report a just-failed submission is a pattern violation.
- **Decision frameworks:**
  - **Count vs dot:** does the exact number carry information the user will act on? Yes → count; no → dot.
  - **Overlaid vs standalone:** annotating an interactive host → overlay; describing an entity in content flow → status pill.
  - **The count-in-the-host rule (load-bearing):** a count badge must never be the sole descriptor on a blank canvas — a floating "4" is meaningless; "4" over a "Messages" tab is a complete thought. Its meaning belongs in the host's accessible name (§6).

## 6. Accessibility

**The announcement contract is the crux**, and the field-truth here is recent and decisive. The WAI-ARIA APG has **no formal badge pattern** — so practitioners historically fell back to attaching `aria-label` to the floating badge node, producing disjointed readouts. The APG task force resolved the ambiguity (Issue 2507): per Matt King, *"Including information conveyed by a badge in the accessible name is consistent with the purpose of an accessible name… [it] serves the user better than description or details."* The contract that follows:

- **The overlaid visual badge is `aria-hidden="true"`**, and the **host carries the composed accessible name**. A screen reader landing on a bell that just says "3" is meaningless, so the count is *described in context* on the host:
  - *Wrong:* `<button aria-label="Inbox"><div aria-label="3 unread">3</div></button>` → "Inbox, button" … later a detached "3 unread".
  - *Right:* `<button aria-label="Inbox, 3 unread messages"><div aria-hidden="true">3</div></button>`.
- **A dot needs a text equivalent** in the host's name (`aria-label="Notifications, new alerts available"` / `"Jane Doe, online"`); the dot itself is `aria-hidden`. Never describe the visual ("red dot" as a label is prohibited).
- **A dynamically-changing count uses a status live region.** When a count increments while the user is on the page (a WebSocket tick 3→4), announce via a visually-hidden **`role="status"` / `aria-live="polite"`** node ("You have 4 unread messages") — the same live-region pattern Toast established (see toast), reused here. Polite, not assertive (a count tick is not an interruption); don't steal focus.
- **The standalone status pill announces its own text** — it is *content*, so it is **not** `aria-hidden`; "Draft" is read in flow. (This is the opposite contract from the overlay genres — the reason they're different components.)
- **Color is never the sole carrier (WCAG 1.4.1).** A red status badge alone fails for protanopic/deuteranopic users — severity pairs **color + text** (and optionally a leading icon/shape), inheriting the Banner/Toast severity model (see banner, toast). "System Status: Error", not a bare red pill.
- **WCAG SCs:** **1.4.1** (use of color), **1.4.3** (contrast — the badge text/fill *and* the badge-against-host edge; a count pill on a busy host needs the separating cutout stroke), **4.1.2** (name/role/value — the host's name folds the count), **4.1.3** (status messages — the dynamic-count live region). The overlaid badge has **no role of its own** (it's `aria-hidden`); a static status pill is just text (don't invent `role="status"` for it).

## 7. Content guidelines

- **The count cap** — cap large counts ("99+"/"9+") so the surface stays small and the number scannable; the exact value above the cap rarely matters. Pick the cap to fit the surface (single-host bells "9+"; inboxes "99+").
- **Zero handling** — hide at zero by default; show "0" only when it's itself meaningful (a deliberate `showZero`). Never render an empty pill.
- **The status label** — one or two words max; a taxonomical descriptor, not a sentence. "Failed", not "The transaction failed to process"; "Draft", not "Saved as a draft". Consistent casing across the set.
- **The dot's hidden text** — clear, actionable phrasing of the qualitative state ("Unread", "Update available"), never a description of the UI.
- **No color-only** — the text must carry the severity; color reinforces, never replaces.
- **Don't overload** — one badge per host. Layering a presence dot *and* a count on one avatar creates visual clutter and conflicting announcements.

## 8. Motion and transition

- **Appearance** — entering from the hidden/zero state, a subtle `transform: scale(0)→scale(1)` spring, with **`transform-origin` anchored to the overlap corner** (scaling out from the host's top-trailing corner, not the badge's own center).
- **Incrementing** — don't flash/pop the whole surface; target only the typographic layer — slide the old number up and fade it, slide the new one in from below.
- **Dot pulse** — reserve pulsing/"breathing" for *critical, synchronous* alerts (a live incoming call); generic async notifications stay static. A constantly-pulsing dot is a distraction and an accessibility problem.
- **Reduce-motion** — `prefers-reduced-motion: reduce` resolves all scale/translate/pulse instantly to the final state. The cue is the number/dot/text, not the motion, so dropping animation loses nothing.

## 9. Internationalization

- **The RTL flip via logical properties.** A top-**trailing** overlay sits top-right in LTR and **top-left in RTL**. Legacy physical anchoring (`top: 0; right: 0; translate(50%, -50%)`) kept the badge on the right in RTL (or bled it off-viewport). The modern standard eradicates physical directional properties: `inset-block-start: 0; inset-inline-end: 0` — the engine maps `inline-end` to the right in LTR and the left in RTL automatically, repositioning to the top-leading corner with **no JS overrides, no RTL classes**.
- **Number formatting** — counts run through `Intl.NumberFormat` for locale digits/grouping (Eastern Arabic numerals, separators). The max-cap renders most grouping moot, but the localized digit *glyphs* are still required.
- **Status label expansion** — never hardcode pill width/height; rely on intrinsic `padding-inline`/`padding-block` so the container grows for longer translations (German/Russian run 30–50% longer) without clipping the state word.
- **Dot neutrality** — the dot is visually locale-neutral (no text); its **text equivalent** in the host name must be translated.

## 10. Naming

- **The field set:** Fluent v9 `Badge` / `CounterBadge` / `PresenceBadge`; Primer `Label` / `CounterLabel` / `StateLabel`; MUI/Ant `Badge` (= count/dot overlay; status → `Chip`/`Tag`); Polaris/Chakra/Spectrum `Badge` (= status pill); Carbon `Badge indicator` + `Tag` with a notification dot.
- **The practice's opinionated default — adopt the tripartite split** (Fluent/Primer), because the genres' accessibility contracts are opposite (§6) and the structural requirements of a count overlay vs an inline status pill are too divergent to share one clean API:
  - **`Badge`** — reserved for the **standalone, non-interactive status pill** (severity tone + optional icon + text).
  - **`CounterBadge`** (alias `NotificationBadge`) — the **numerical overlay** (wrapper model, max/showZero, `aria-hidden` + host-name wiring).
  - **`PresenceBadge`** — the **avatar presence/unread dot** overlay.
  - The two overlay components share the positioning substrate (wrapper, overlap math, RTL flip, the aria contract); a `variant: count | dot` on a single overlay component is the valid lighter-weight alternative (MUI/Ant) and is recorded as the contested call (notes).
- **The Badge-vs-Tag disambiguation (the load-bearing naming call):** **Badge = non-interactive, non-removable indicator**; **Tag/Chip = interactive/removable/selectable token**. If it has an `onClick`, an `×`/dismiss, or a selected state, it is a **Tag**, regardless of what a vendor library calls it. **"Pill"** describes a `border-radius` token, **not** a component — relegate it. (See tag — the boundary drawn from Tag's side.)
- **Aliases to map:** CounterBadge, PresenceBadge, NotificationBadge, Label, CounterLabel, StateLabel, Counter, Notification dot, Pill, Indicator, Status.

## 11. Implementation notes

- **The overlap positioning model — circular vs rectangular.** A flat offset behaves differently against the two host shapes. **Rectangular** (`overlap="rectangular"` — icon buttons, tabs): the badge sits at the corner via `transform: translate(50%, -50%)` (LTR). **Circular** (`overlap="circular"` — avatars): pushing to the true corner of a circle leaves an awkward floating gap, so the API applies a **trigonometric inset** (the 45° intersection with the circle's radius, ≈14.6% inward) so the badge hugs the curve.
- **Host clipping + the stacking context (a recurring trap).** A host with `overflow: hidden` (mandatory for a circular avatar masking its image) **clips** an absolute badge injected as its direct child — the avatar-presence-dot trap. The fix: the **wrapper** establishes a parent-level stacking context (`position: relative`, owns the `z-index`), so the absolute badge overflows the host's visual bounds without being clipped by the host's own `overflow`.
- **The cutout stroke** — an overlaid surface carries a thick border matching the canvas color, keeping the host silhouette clean and holding the 1.4.3 edge contrast on busy hosts.
- **The count-in-the-aria-label wiring** — the host gets the composed `aria-label`; the visual badge is `aria-hidden`. A headless overlay can't know the host's label, so the API supplies/composes it — in React often via `React.cloneElement` to intercept and concatenate the child's `aria-label`, or by documenting the consumer's obligation explicitly.
- **The dynamic-count live region** — one shared app-level polite `role="status"` region for count changes (the pre-existing-region discipline from the Feedback live-region pattern — see toast); debounce rapid increments so AT isn't flooded.
- **The max-cap / zero logic** — `count > max ? \`${max}+\` : count`; `count === 0 && !showZero ? render nothing`. Keep it in the component, not the consumer.
- **Headless vs opinionated** — the positioning/overlap math, the RTL logical properties, and the aria wiring are the substrate worth owning; the palette and shape are theme. **Ship opinionated** (MUI/Ant/Fluent) with a forced DOM structure and automated a11y wiring, exposing only semantic payload (`tone`/`max`/`showZero`) — a purely headless badge pushes the circular-overlap math and the logical-positioning onto every consumer and invites drift.

## 12. Related and alternative components

- **Stands on:** **Icon** (the optional severity icon in a status pill + the icon-button count host — see icon).
- **Inherits (patterns):** the **color-not-sole-carrier severity model** from the Feedback family (info/success/warning/error/neutral as color + text — see banner, toast); the **live-region announcement pattern** from Toast for the dynamic-count change (see toast).
- **Overlaid on (hosts):** Icon buttons, **Avatar** (the presence-dot host — not yet briefed; shares the circular-overlap trigonometry), **Tabs** (a count on a tab — see tabs), nav items (a count on a side-nav item — see side-navigation).
- **Boundary:** **Tag/Chip** — the interactive/removable/selectable token (Badge is the passive indicator; the strictest functional boundary in the system; see tag).
- **Not:** **Toast** (transient feedback — see toast), **Banner** (persistent feedback — see banner). Badge is a passive standing indicator, not an event.

(A Foundations indicator primitive. It stands on Icon and the Feedback severity + live-region patterns; it is overlaid on Icon buttons / Avatars / Tabs / nav items; its hard boundary is Tag (interactive/removable). See icon for the substrate, banner/toast for the inherited severity + live-region patterns, tabs/side-navigation for hosts, tag for the interactive/removable boundary, avatar when briefed for the presence host. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **The taxonomic maturation — one CSS class → the tripartite split.** Early frameworks (Bootstrap 3) shipped a single `.badge` class slapped onto anything needing rounding + color. The field has since proven the structural requirements of a count overlay vs a status pill are too divergent to share one API — Fluent v9 (`Badge`/`CounterBadge`/`PresenceBadge`) and Primer (`Label`/`CounterLabel`/`StateLabel`) hardened the split.
2. **The accessibility hardening — floating label → accessible-name-on-host.** It was once accepted to attach `aria-label` to the floating badge node; the APG task force resolution (Issue 2507, Matt King) pivoted the field to the *accessible-name-on-host* model, with the dynamic-count `role="status"` region as the newer refinement (4.1.3).
3. **The color-as-sole-carrier awakening.** Growing WCAG strictness killed the generic "green = good / red = bad" pill — status severity now mandates color + text (+ optional icon), aligned with the Feedback severity model.
4. **Logical-positioning standardization.** The end of legacy-browser support let systems move overlay positioning entirely to `inset-inline-start/end`, abandoning the fragile JS layout calculations and duplicate RTL stylesheets.
5. **The Badge-vs-Tag clarification.** Systems increasingly separate the passive indicator (Badge/Label) from the interactive/removable token (Tag/Chip), reversing the earlier tendency to pile dismiss/click behavior onto a "badge".

## 14. Sources cited

(Conservative; reconcile with external.) **Microsoft Fluent UI v9** — `Badge` / `CounterBadge` / `PresenceBadge` (the tripartite split; the cleanest modern taxonomy) (2024–2026); **GitHub Primer** — `Label` / `CounterLabel` / `StateLabel` (the independent mirror of the split; `CounterLabel` as a sibling) (2024–2026); **MUI** — `Badge` (the wrapper/content-injection overlay; `badgeContent`/`max`/`showZero`/`variant="dot"`/`overlap="circular|rectangular"`/`anchorOrigin`) (2024–2026); **Ant Design** — `Badge` (count/dot/status + `Ribbon` + standalone; `overflowCount`/`offset`) (2024–2026); **Shopify Polaris** — `Badge` (`tone`, progress; the semantic status indicator) (2024–2026); **Adobe Spectrum** — `Badge` (the label/status; locked semantic variants) (2024–2026); **IBM Carbon** — `Tag` with status + the notification dot; the three-digit-max + dot-vs-number UX rules (2024–2026); **Chakra UI** — `Badge` (the status label) (2024–2026); **Google Material 3** — `Badge` (small dot vs large number) (2024–2026); **Base Web (Uber)** — `Badge` (2024); **W3C WAI-ARIA APG** — no formal badge pattern; the accessible-name-on-host mandate + `role="status"` live region + `aria-hidden` visual, per the **APG task force Issue 2507 resolution (Matt King)**; **MDN Web Docs** — CSS logical properties (`inset-inline-end`) for the RTL flip. WCAG 2.2 (W3C Recommendation, Oct 2023) — 1.4.1, 1.4.3, 4.1.2, 4.1.3.

## 15. Agent-consumable schema

```yaml
identity:
  id: badge
  name: Badge
  aliases: [CounterBadge, PresenceBadge, NotificationBadge, Label, CounterLabel, StateLabel, Counter, Notification dot, Pill, Indicator, Status]
  category: foundations
  status: stable
description: >
  A small, non-interactive indicator annotating a host or content with a quantum of
  state, across three structurally distinct genres: COUNT (a number overlaid on a
  host), DOT (a contentless attention/presence marker), and STATUS PILL (standalone
  inline state text). The dividing line is the accessibility contract — the overlay
  genres are aria-hidden with their meaning in the HOST's accessible name; the status
  pill is content announcing its own text — which is why the modern field (Fluent v9,
  Primer) SPLITS them into separate components. Non-interactive and non-removable —
  the boundary with Tag/Chip (interactive/removable). NOT a Toast/Banner (the feedback
  surfaces — Badge informs passively, doesn't alert).
anatomy:
  parts:
    - "host substrate (overlay only): the anchor (IconButton/Avatar/Tab/nav item); the badge's positioning math depends on its bounding box + border-radius; the wrapper model passes it as children"
    - "badge surface: background/padding/radius + the CUTOUT STROKE (a canvas-color border separating an overlay from the host silhouette); count scales circle->pill; dot fixed ~6-12px"
    - "typographic layer: the number/status text, smallest type token (caption/label-small), medium/semibold for legibility on semantic fills"
    - "optional leading icon (status + presence): a severity/state glyph (color-not-sole-carrier); overlay COUNT rarely carries an icon (no room)"
    - "ABSENT: interactive targets — no hover/focus/active, no focus ring, no cursor; structurally inert; interactivity inherited from the host"
api:
  inherits:
    - icon              # optional severity icon + icon-button count host
    - banner/toast      # color-not-sole-carrier severity model (pattern)
    - toast             # live-region pattern for the dynamic-count announcement (pattern)
  host-model: "WRAPPER/content-injection (MUI/Ant — <Badge><IconButton/></Badge>; measures children, owns relative/absolute positioning) vs SIBLING (Primer — parent flex/grid positions). Practice favors WRAPPER for overlays"
  props:
    - {name: variant, type: "'count' | 'dot' | 'status'", default: count, required: false, description: "the genre (or split into Badge/CounterBadge/PresenceBadge components — see naming)"}
    - {name: value, type: "number | string", default: null, required: false, description: "the count (number) or status text; dot has none"}
    - {name: max, type: number, default: 99, required: false, description: "count cap; over it -> `{max}+`; raise to 999 for high-volume"}
    - {name: showZero, type: boolean, default: false, required: false, description: "render a zero count; default hides at zero"}
    - {name: tone/severity, type: "'info' | 'success' | 'warning' | 'error' | 'neutral'", default: neutral, required: false, description: "semantic palette; color + text/icon, never color alone; NOT arbitrary hex"}
    - {name: overlap, type: "'rectangular' | 'circular'", default: rectangular, required: false, description: "corner math vs the host shape (circular = trigonometric ~14.6% inset to hug the curve)"}
    - {name: anchorOrigin, type: "{ vertical: 'top'|'bottom', horizontal: 'left'|'right' }", default: "{ top, trailing }", required: false, description: "the overlay corner; LOGICAL (inset-inline-end) so RTL flips to top-leading"}
    - {name: placement, type: "'overlaid' | 'standalone'", default: overlaid, required: false, description: "anchored to a host vs inline (status pills are standalone)"}
    - {name: size, type: "'small' | 'medium' | 'large'", default: medium, required: false, description: "small (dense/small hosts, 2-digit max) / medium (40-48px hosts) / large (status pills by h1/h2)"}
    - {name: host-accessible-name, type: wiring, default: null, required: true, description: "NOT a style prop — the overlay count/dot meaning lives in the HOST's aria-label, not the badge; the API must supply/compose it (React.cloneElement to intercept the child's label)"}
states:
  runtime: []           # non-interactive; no hover/focus/active/disabled of its own; no role when overlaid
  content-change: [zero-hidden, zero-shown, overflow-cap, increment]   # announced via host/live-region, not interaction states
variants:
  genre: [count, dot, status]
  tone: [info, success, warning, error, neutral]
  placement: [overlaid, standalone]
  size: [small, medium, large]
  count-edge: [zero-hidden, zero-shown, overflow-cap, dot-on-overflow]
accessibility:
  inherits:
    - banner/toast      # color-not-sole-carrier severity
    - toast             # live-region announcement
  wcag-criteria: ["1.4.1", "1.4.3", "4.1.2", "4.1.3"]
  announcement-contract: "APG has NO formal badge pattern; task-force resolution (Issue 2507, Matt King): the badge's info belongs in the accessible NAME, not description/details"
  aria-attributes:
    overlaid-badge: "aria-hidden=true — the visual count/dot is hidden from AT (a bare floating '3' is meaningless)"
    host: "aria-label folds the count/dot ('Inbox, 3 unread messages' / 'Jane Doe, online')"
    dynamic-count: "visually-hidden role=status aria-live=polite announces the change; polite not assertive; don't steal focus"
    status-pill: "NOT aria-hidden — its text is content, read in flow (the OPPOSITE contract from overlays — why they're different components)"
  keyboard-model: none      # non-interactive, not focusable
  focus-behavior: none      # focus belongs to the host (icon button / tab / nav item)
  color-rule: "severity = color + text (+ optional icon); a bare red pill fails 1.4.1 for protanopia/deuteranopia"
content:
  count-pattern: "cap large counts ('99+'/'9+'); the exact value above the cap rarely matters; fit the surface"
  zero-pattern: "hide at zero by default; showZero only when '0' is itself meaningful; never an empty pill"
  status-pattern: "1-2 words max, a taxonomical descriptor not a sentence ('Failed' not 'The transaction failed'); consistent casing"
  dot-pattern: "every dot has an actionable text equivalent in the host's name ('Unread'/'Update available'); NEVER describe the UI ('red dot' prohibited)"
  trap: "don't overload — one badge per host; layering a dot + count on one avatar = clutter + conflicting announcements"
motion:
  enter: "scale(0)->scale(1) spring; transform-origin ANCHORED to the overlap corner (not the badge's center)"
  increment: "animate only the typographic layer (slide old number up + fade, new slides in from below); never flash the whole surface"
  dot-pulse: "reserve for critical/synchronous alerts (a live call); async notifications stay static"
  reduce-motion: "resolve all scale/translate/pulse instantly — the cue is the number/dot/text, not the motion"
i18n:
  rtl: "overlay anchor flips to top-leading via LOGICAL properties (inset-block-start/inset-inline-end) — engine maps inline-end to left in RTL; NO JS overrides/RTL classes (eradicates legacy top:0;right:0;translate)"
  number-formatting: "counts via Intl.NumberFormat (locale digit glyphs/grouping); the cap renders grouping mostly moot but localized digits still required"
  label-expansion: "never hardcode pill width/height; intrinsic padding-inline/block so translations (DE/RU +30-50%) grow without clipping the state word"
  dot-neutrality: "the dot is visually locale-neutral; its text equivalent (in the host name) must be translated"
implementation:
  overlap-positioning: "rectangular = translate(50%,-50%) at the corner; CIRCULAR = trigonometric ~14.6% inward inset (45deg x radius) to hug the curve, else an awkward floating gap"
  host-clipping: "a host with overflow:hidden (a circular avatar masking its image) CLIPS an absolute child badge (the avatar-presence-dot trap); fix: the WRAPPER establishes a parent stacking context (position:relative + z-index) so the badge overflows without being clipped"
  cutout-stroke: "an overlay surface carries a canvas-color border, keeping the host silhouette clean + holding the 1.4.3 edge contrast on busy hosts"
  aria-wiring: "host carries the composed aria-label; visual badge aria-hidden; a headless overlay can't know the host label so the API supplies it (React.cloneElement to intercept/concatenate the child's aria-label)"
  live-region: "one shared app-level polite role=status for dynamic counts (the pre-existing-region discipline); debounce rapid increments"
  count-logic: "count>max ? `${max}+` : count; count===0 && !showZero ? render nothing — in the component, not the consumer"
  headless-vs-opinionated: "positioning/overlap math + logical properties + aria wiring is the substrate; palette/shape is theme. Ship OPINIONATED (forced DOM + automated a11y, expose only tone/max/showZero) — a headless badge pushes the circular-overlap math onto every consumer + invites drift"
composition:
  stands-on: [icon]
  composes-with: [icon, avatar, tabs, side-navigation]   # the count/dot hosts
  alternative-to: [tag, toast, banner]                    # tag (interactive boundary), toast/banner (feedback surfaces)
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "the tripartite SPLIT (Badge=pill / CounterBadge=count / PresenceBadge=dot — Fluent/Primer; the practice default, because the a11y contracts are opposite) vs ONE Badge + variant axis (MUI/Ant — the valid lighter-weight alternative)"
    - "where the status pill lives — its own Badge (Polaris/Chakra/Spectrum) vs folded into Chip/Tag (MUI/Ant)"
    - "dot-on-overflow (collapse a too-large count to a dot) vs always-cap ('99+')"
    - "showZero default — the field hides at zero; show only when 0 is meaningful"
    - "wrapper/content-injection (MUI/Ant — practice default for overlays) vs sibling (Primer)"
  trap:
    - "the floating bare '3' — an SR reading the count in isolation; it must live in the host's accessible name (APG Issue 2507)"
    - "attaching aria-label to the floating badge node (the old anti-pattern) instead of the host name"
    - "host overflow:hidden clipping the overlay (the avatar-presence-dot trap) — needs the wrapper stacking context"
    - "circular-overlap floating gap (a rectangular offset on a circular host) — needs the trigonometric inset"
    - "color-as-sole-carrier severity (WCAG 1.4.1 failure)"
    - "overloading one host with multiple badges; using a badge to ALERT (-> Toast/Banner)"
  inherited:
    - "color-not-sole-carrier severity (banner/toast)"
    - "the live-region announcement pattern (toast)"
    - "Icon (the severity icon + the count host)"
  role-in-family: "a Foundations indicator primitive standing on Icon + the Feedback severity/live-region patterns; overlaid on Icon buttons/Avatars/Tabs/nav items; hard boundary with Tag (interactive/removable)"
  evolution:
    - "one CSS class (Bootstrap .badge) -> the tripartite split (Fluent v9 / Primer)"
    - "floating-label a11y -> accessible-name-on-host (APG Issue 2507, Matt King) + the dynamic-count role=status refinement"
    - "the color-not-sole-carrier hardening (killed the bare green/red pill)"
    - "logical-positioning standardization (inset-inline-end; abandoned JS layout calcs + duplicate RTL stylesheets)"
    - "the Badge-vs-Tag clarification (passive indicator vs interactive/removable token)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "the circular-overlap ~14.6% trigonometric constant — verify against the specific system's implementation"
    - "the APG Issue 2507 attribution/quote — verify against the live APG issue thread"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-badge/` (16 June 2026), the thirty-second brief and the next Foundations primitive. It stands on Icon (the severity icon + the icon-button host) and inherits the Feedback color-not-sole-carrier severity model (banner/toast) + the Toast live-region pattern (the dynamic-count announcement), and holds a hard boundary with Tag (the interactive/removable token; briefed immediately after, so the boundary is now drawn from both sides — see tag). The two passes converged on the substance — the genre split (count / dot / status pill), the naming morass (Fluent/Primer's tripartite split vs MUI/Ant's one-Badge-overlay-plus-Chip vs Polaris/Chakra/Spectrum's status-pill Badge), the announcement contract (count in the HOST's accessible name not a floating number; the dot's text equivalent; the dynamic-count role=status live region; aria-hidden the visual), color-not-sole-carrier severity, and count handling (max-cap/zero). The one genuine fork was the headline architecture: the Claude pass leaned one-Badge-with-a-variant-axis; the external pass argued the Fluent/Primer tripartite split — resolved decisively toward the SPLIT, on the principle the external pass sharpened: the overlay genres (aria-hidden, meaning on the host) and the status pill (announces its own text) have OPPOSITE accessibility contracts, which is what makes them different components rather than one component's variants. The external pass also supplied the decisive field detail — the wrapper/content-injection vs sibling host model (and the practice's wrapper default), the circular-vs-rectangular overlap math (the ~14.6% trigonometric inset to hug a circular host vs the rectangular 50% translate), the cutout/stroke separation, the overflow:hidden host-clipping trap + the wrapper stacking-context fix, the React.cloneElement aria-label interception, the incrementing-number motion (slide-and-fade the typographic layer, transform-origin on the overlap corner), and the authoritative a11y citation (the WAI-ARIA APG task-force resolution, Issue 2507 / Matt King: the badge's information belongs in the accessible NAME). Claude-pass contributions: the accessibility-contract-as-dividing-line framing, the substrate/inheritance map, the Badge-vs-Tag boundary discipline, and the count-in-the-host rule. The 2026 version numbers, the ~14.6% circular constant, and the APG Issue 2507 attribution are flagged unverified. Conformant to `components/_schema.md`.*
