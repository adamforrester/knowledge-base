---
okf_version: "0.1"
type: component-brief
title: Banner (Alert)
description: The second Feedback brief — the persistent, in-flow, actionable counterpart to Toast, which inherits the live-region announcement pattern Toast established but refines it with the static-vs-dynamic rule. A field-truth study of the persistent/in-flow contract (the Toast opposite), the static-vs-dynamic live-region refinement (a banner at load is NOT role=alert), the placement taxonomy (page/global vs contextual/section vs the inline-message boundary), the severity + color-not-sole-carrier model, the dynamic heading-level mapping trap, the legitimacy of actions, dismissibility + don't-re-nag, the layout-shift/CLS consideration, and the Banner-vs-Alert-vs-role=alert naming overload — with the practice's defaults.
tags: [components, feedback]
category: Feedback
status: stable
aliases: [alert, callout, section-message, message-bar, inline-notification, inline-alert, flash]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Banner (Alert)

> A Banner is a **persistent, in-flow message** that communicates an important system state, error, or announcement and stays until dismissed or until the triggering condition resolves. It is the architectural **antithesis of a Toast**: where a Toast floats at the viewport edge, auto-dismisses, and is forbidden from taking focus, a Banner is embedded in the document flow, alters the page layout, persists, and sits in the sequential tab order — so, unlike a Toast, it can **legitimately carry actions** (the Toast action-reachability problem simply doesn't exist here). Its contract is *sustained cognitive attention without aggressive interruption*. It is the second Feedback brief and **inherits the live-region announcement pattern Toast established**, plus Button (actions + dismiss), Icon (severity), and Link (inline body links). The one piece genuinely its own — and the most-mishandled point in the component — is the **static-vs-dynamic live-region refinement**: a banner *present at page load* is read in normal document order and is **NOT** a live region (`role=alert` on a static banner is an active anti-pattern — it double-announces, mistimes, or drops); only a banner *inserted dynamically* in response to an action is a live region. Toast is always dynamic; Banner forks on insertion timing. The field is fragmented precisely because it conflates the *visual geometry* of a persistent message with the *semantic urgency* of an accessibility event.

---

## 1. Framing

A Banner sits **in the document flow**, communicates a persistent state/error/announcement, and stays until dismissed or resolved. It inherits the **live-region pattern from Toast** (role=status/polite vs role=alert/assertive — see toast), **Button** (actions + dismiss — see button), **Icon** (severity — see icon), and **Link** (inline body links — see link).

**The two realities that define it:**
- **Persistent + in-flow** — it alters layout, persists, and (unlike Toast) carries reachable actions in the tab order. The Toast opposite.
- **The static-vs-dynamic live-region split** — *present at load* = read in document order, **no** live region (`role=alert` here is wrong); *dynamically inserted* = a live region (alert for errors, status for info). The sharp refinement of Toast's always-dynamic pattern.

What it *isn't*: a **Toast** (transient, floating, auto-dismiss, non-actionable — see toast), an **Inline Message** (field-level validation attached to a specific control, stripped of heavy fill/border — see inline-message), or a **Dialog** (blocking, focus-trapped, must-act — see dialog). Why systems disagree: the static-vs-dynamic semantics, the placement taxonomy, contrast/dismissibility, and the Banner/Alert/`role=alert` naming overload.

## 2. Anatomy and parts
- **container** — a block-level in-flow element (full-width page or contained section), severity-styled (background + border tone); calculates padding/margin defensively so it displaces content without horizontal overflow.
- **severity icon** (inherits Icon) — visually reinforces tone; **decorative** (`aria-hidden`) — meaning lives in the text + the icon *shape* (color-not-sole-carrier — §6).
- **title / heading** — concise, prominently weighted; **the heading level must map dynamically to the host document's outline** (hardcoding `<h2>` breaks the page heading sequence — §6/§11).
- **body** — the message (context + consequence + resolution); width-constrained for readable line lengths; may hold **inline Links** (inherits Link) and short lists.
- **action(s)** (inherit Button) — primary/secondary resolution affordances, in the tab order (legitimate here — §5).
- **dismiss control** (inherits Button — icon-only) — at the logical end/top-trailing; needs a min hit target + a localized, descriptive accessible label ("Dismiss error message", not bare "Close").

Placement levels: **page/global** (full-width, app-shell top) / **contextual/section** (inside a region/card, inheriting its radius/padding) / the **inline** boundary (Spectrum's `InlineAlert` strips vertical padding to sit under a form aggregation — the bridge to Inline Message).

## 3. Properties / API
- **`severity` / `tone` / `status`** — info / success / warning / error / critical (+ neutral). (Polaris migrated `status`→`tone` to signal communicative *intent* over binary state; MUI uses `severity`, Ant `type`.)
- **`title` + `children`** — heading + body. Compound (`Callout.Root`/`Callout.Text` — Radix; `AlertTitle` — MUI/Chakra) vs flat string props (Ant/Polaris); **passing arbitrary nodes into a flat `title` can break the accessible-name calculation** if the title also labels the region.
- **`dismissible` (explicit boolean) + `onDismiss`** — modern systems (Polaris v12+) require an **explicit `dismissible` flag** alongside the callback (a callback alone silently rendering a close button is the deprecated ambiguous behaviour); **persist the dismissal** (§11).
- **`action` / `primaryAction` / `secondaryAction`** — node slots (pass Buttons) **or** a structured **action-object array** (Atlassian — guarantees layout conformance).
- **role / `aria-live` override** — the static-vs-dynamic switch; Radix exposes an explicit accessibility-mapping prop to force/bypass the live role (§6/§11).
- **placement** — global / section / inline.
- **`icon`** — override the SVG or disable the severity icon (denser layouts).
- **heading-level** — a polymorphic/`as`/level prop so the title interpolates the correct `<h*>` for its DOM context (§11).

## 4. States and variants
- **States:** shown / dismissed (removed). No interactive states beyond actions/dismiss.
- **Variants:**
  - **severity:** info / success / warning / error / critical (+ neutral); Primer adds an **upsell/promotional** variant (purple) separating marketing from system status.
  - **dismissible vs persistent** — system-critical (e.g. failed payment) is **persistent** (removing it would hide a blocking restriction).
  - **contrast:** **low-contrast** (subtle fill — the recommended default) vs **high-contrast** (inverted, reserved for emergencies) — Carbon; MUI's **filled / outlined / standard** modulate the same visual weight.
  - **placement:** page/global (full-width, no radius) / contextual/section (radius + padding from parent) / inline (stripped padding).
  - **content:** with-title / with-action / with-list / icon-less.
  - **genre:** system/status vs promotional/announcement (cookie-consent, maintenance, announcement bars are the global genre).

## 5. Usage guidance
- **Use a Banner** for a **persistent, important, in-context message** the user should see and may need to act on: a system outage/maintenance notice, a page-level error/warning, a feature announcement, a consent bar, the result of a process that must stay visible. It grants the user *infinite time* to comprehend and act.
- **Don't use a Banner for:**
  - A brief, transient confirmation ("Saved") → a **Toast** (see toast).
  - Field/form validation attached to a control → an **Inline Message** (a big banner overpowers the input — see inline-message).
  - A blocking decision that must be resolved before continuing → a **Dialog** (see dialog).
- **Decision frameworks:**
  - **The opinionated default — errors and actionable systemic feedback belong in a Banner, not a Toast.** A timed, vanishing Toast fails WCAG timing (2.2.1 Timing Adjustable / the no-timing family) for motor- and cognitively-impaired users who can't interact with a disappearing target; a Banner stays in the flow. **This is where Toast's no-error-toasts POV hands errors and actions off.**
  - **Banner vs. Toast:** persistent + in-flow + actionable (Banner) vs. transient + floating + auto-dismiss + non-actionable (Toast).
  - **Page vs. section vs. inline:** app-wide state → page/global (full-width, top of DOM); a region's state → contextual/section; a single control's validation → Inline Message.
  - **Don't over-banner (banner blindness):** users tune out stacked persistent blocks like ads, and aggressive stacking pushes the workspace below the fold. **Show only the highest-severity banner; dedupe; prioritise; route low-priority status to a Notification Center** or aggregate into one "multiple alerts" banner.

## 6. Accessibility
- **The static-vs-dynamic live-region rule (the sharp point, the refinement of Toast's pattern, the most-mishandled detail):**
  - **Static (present at page load):** the screen reader reads the DOM linearly top-to-bottom, so the banner is encountered **in document order** — it needs **no live region**. **Applying `role=alert`/an active live region to a static banner is a critical anti-pattern** (AT assumes live regions are empty containers for *subsequent* changes, so it double-announces, interrupts the page summary, or drops the node on an init race). Instead use semantic HTML — ideally a **`<section>` with `aria-labelledby`** pointing to the title, a quiet discoverable **landmark region**.
  - **Dynamic (inserted on an action/async event):** it **must** be a live region so AT is notified without a focus shift — **`role="alert"`** (implicitly assertive + atomic; interrupts) for errors/critical, **`role="status"` / `aria-live="polite"`** (waits for a pause) for info/success. (Same politeness model as Toast — but Toast is *always* dynamic.)
- **Actions are in the tab order** — because the banner is in-flow, its links/buttons are reachable by normal Tab (no hotkey/landmark machinery — the Toast reachability problem doesn't exist).
- **Focus on dismiss (a real hurdle):** when the user activates the dismiss button and the banner unmounts, focus resting on that button **drops to `<body>`** — disorienting. Programmatically **return focus to a logical surviving node** (the page heading, the previous landmark, or the element that triggered the banner).
- **Dynamic heading-level mapping** — the title's `<h*>` must match the document outline; a hardcoded level breaks rotor navigation (§11).
- **Color-not-sole-carrier (1.4.1)** — severity is conveyed by **icon shape + text** (triangle/circle/checkmark), not colour alone — the icon is the semantic anchor for colour-blind users, not decoration-for-its-own-sake.
- **Don't overuse `role=alert`** — reserve assertive for genuinely urgent dynamic errors.
- **WCAG SCs:** 4.1.3 (Status Messages — the dynamic live region, the headline), 1.4.1 (colour not alone), 1.3.1 (info & relationships — the structure/landmark/heading), 2.4.3 (focus order — focus-on-dismiss), 1.4.3/1.4.11 (severity + text contrast), 2.5.5/2.5.8 (dismiss hit target), plus the action/dismiss Buttons' and inline Links' SCs.

## 7. Content guidelines
- **Heading: concise, objective, front-loads the issue** — "Database connection failed" / "Subscription expired", never generic "Warning!"/"Error". **No trailing period** (AT reads a rich title as one continuous string; rogue punctuation causes unnatural pauses — Carbon).
- **Body: never repeats the heading** — it states the *consequence* (was data preserved?) and the *resolution*. Cap at one–two short sentences; if it needs a paragraph, truncate + a "View details" link that opens a Dialog.
- **Action labels: predictive active verbs, 1–2 words** — "Retry connection", "Update billing", not "Click here"/"OK".
- **Dismiss label** localized + descriptive ("Dismiss error message").
- **Match tone to severity** (no cry-wolf) and **don't over-banner** — every persistent banner competes for attention.

## 8. Motion and transition
Minimal — a Banner is in-flow, so its appearance/removal **shifts layout** (a Cumulative Layout Shift / CLS concern and a cognitive-disorientation risk if abrupt). Prefer an **opacity fade** for appearance; if animating height, use a **CSS Grid-rows `0fr`→`1fr`** transition (or a dedicated Collapse wrapper — MUI) to avoid render thrash. **Dismiss collapses the height (~150–200ms) + fades** so content below doesn't teleport upward and force the user to re-track. Dynamic page banners should **reserve space / anchor scroll** so they don't jump what the user is reading. Under `prefers-reduced-motion: reduce`, appear/disappear **instantly** (MUI zeroes its durations). No decorative motion. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** — the severity icon, actions, and dismiss flip edges via **CSS logical properties** (`margin-inline-start`, `padding-inline-end`, `border-inline-start`); hardcoded `left`/`right` is the catastrophic anti-pattern (the layout engine mirrors automatically off `dir`).
- **Text expansion** — banners hold *more* text than toasts (+30–50%); **never fixed height** — use Flexbox/Grid that grows vertically, **wrap gracefully** (multi-line is fine here), and the **action row wraps to a stacked configuration below the text** when translations cause collisions (Primer's actions-layout) so touch targets aren't obscured. (See 13-internationalization-and-rtl.)

## 10. Naming
A heavily overloaded space: **`Alert`** (MUI, Ant, Bootstrap, Chakra — the common legacy name, but it **collides with the ARIA `role=alert`**: `<Alert severity="info">` invites a developer to assume it *is* an alert role when it should be a status region — a direct cause of degraded a11y); **`Banner`** (Polaris, Material 3, and Primer's migration from `Flash`); **`Callout`** (Radix Themes — but historically a floating/tooltip term); **`Notification`**/**`InlineNotification`** (Carbon — verbose); **`MessageBar`** (Fluent); **`SectionMessage`** (Atlassian — placement-descriptive but verbose); **`InlineAlert`** (Spectrum); **`Flash`** (Primer legacy, Rails convention). **The practice default: `Banner`** — it cleanly divorces the visual in-flow geometry from the `role=alert` accessibility event, aligns with the modern systems, and contrasts with the transient Toast. **Disambiguate at the foundational level: a Banner is the visual structural substrate; `alert` is an invisible accessibility event applied *only* when the banner is dynamic + urgent.** Aliases to map: `Alert`, `Callout`, `SectionMessage`, `MessageBar`, `InlineNotification`, `InlineAlert`, `Flash`.

## 11. Implementation notes
- **The static-vs-dynamic live-region wiring (the key trap):** decide by insertion timing — at load → **no** live region (a `<section aria-labelledby>` landmark); on an action → `role=alert` (error) / `role=status` (info). A blanket `role=alert` on every banner double-announces static ones and over-interrupts.
- **The conditional-live-region trap (shared root cause with Toast):** if the `role=alert` *container* is conditionally mounted **simultaneously** with the error text (the common React anti-pattern), AT — notably **VoiceOver+Safari** — fails to announce it; the live region must exist in the accessibility tree **before** the mutation. Provide a **headless live-announcer** that decouples the visual banner from a persistent hidden announce node (the same utility the Toaster uses — see toast §11).
- **Dynamic heading-level mapping** — accept a polymorphic/`as`/level prop so the title renders the correct `<h*>` for its DOM context; a hardcoded `<h2>` in an h4-context card breaks the outline (Atlassian lints this with an ESLint rule).
- **Dismissal persistence (don't re-nag)** — key the dismissal to a unique id + version, checked against localStorage/cookie/user-pref in an init hook, so a dismissed announcement/consent banner doesn't reappear on refresh/navigation; a system-critical banner is non-dismissible or re-shows only while the condition holds.
- **Page vs. section placement + layout shift** — the page/global banner is a full-width app-shell-top block; the section banner renders in the region; dynamic page banners **reserve space / anchor scroll** (the CLS/scroll-jump fix).
- **Focus on dismiss** — return focus to a logical surviving node (§6).
- **Don't hand-roll the semantics** — most systems ship the severity + icon + dismiss; the value-add (which libraries routinely leave to the consumer, a frequent a11y bug) is getting the **static-vs-dynamic live region** and the **heading-level mapping** right.

## 12. Related and alternative components
- **Stands on:** the **live-region announcement pattern** inherited from Toast (the Feedback-category substrate — see toast), Button (actions + dismiss — see button), Icon (severity — see icon), Link (inline body links — see link).
- **Alternative to / boundary with:** **Toast** (transient, floating, auto-dismiss, non-actionable — the persistent/in-flow opposite; **errors and actions hand off *to* the Banner** — see toast), **Inline Message** (field-level validation attached to a control, stripped of fill/border — see inline-message), **Dialog** (blocking, focus-trapped, must-act; a critical Banner's action may *escalate into* a Dialog — see dialog), a **Notification Center** (a persistent log; low-priority status routes there instead of stacking banners).
- **Refines for the category:** the **static-vs-dynamic live-region distinction** the inherited pattern needs once a feedback surface can be present at load (Toast couldn't — it's always dynamic).

(The second Feedback brief — the persistent, in-flow, actionable counterpart to Toast, refining the inherited live-region pattern with the static-vs-dynamic rule and being the documented home for the errors and actions Toast hands off. See toast for the transient boundary + the inherited live-region pattern, dialog for the blocking boundary + the escalation, inline-message for the field-level boundary, button/icon/link for the parts. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The static-vs-dynamic live-region clarification** — a11y practice hardened the rule that a banner present at load is *not* `role=alert` (reading order), only a dynamically-inserted one is — correcting the widespread "every Alert is `role=alert`" bug.
2. **The course-correction of errors and actions from Toast to Banner** — driven by WCAG 2.1/2.2 timing enforcement, interactive/error feedback migrated out of transient toasts into persistent in-flow banners.
3. **The `Alert`→`Banner` rename / disambiguation** (GitHub `Flash`→`Banner`, Polaris `status`→`tone`) — systems renamed and restructured to stop conflating the component with the ARIA role.
4. **Banner-blindness awareness + visual de-escalation** — low-contrast defaults (Carbon), deduplication/priority queues, and routing to a Notification Center, treating banners as respectful status indicators not megaphones.
5. **Dismissal persistence** standardised (id+version keyed to storage) so announcement/consent banners don't re-nag.

## 14. Sources cited
(Conservative; the external pass cited Polaris v12+, Atlassian v8.13+, Fluent 2 React v9, MUI v5, Spectrum v3.29+, Ant v5/6.4+, Radix Themes v3.2+, Chakra v2/3, Carbon v11/12 — held loosely and flagged unverified.) **Shopify Polaris** `Banner` (`status`→`tone`, the explicit-`dismissible` requirement, page/inline placement) (2024–2026); **GitHub Primer** `Banner` (from `Flash`; landmark-region a11y, the actions-layout wrap, the upsell variant) (2024–2026); **Atlassian** `SectionMessage` (object-array actions, the ESLint heading-level lint) (2024–2026); **IBM Carbon** Notification (inline + actionable, low/high contrast, no-period titles) (2024–2026); **Adobe Spectrum** `InlineAlert` (the padding-stripped inline variant) (2024–2026); **Microsoft Fluent 2** `MessageBar` (politeness→aria-live mapping) (2024–2026); **Google Material 3** Banner (2024–2026); **MUI** `Alert`/`AlertTitle` (severity, filled/outlined/standard, Collapse, reduced-motion zeroing) (2024–2026); **Ant Design** `Alert` (2024–2026); **Bootstrap** `Alert` (legacy reference) (2024–2026); **Radix Themes** `Callout` (compound, the role-bypass accessibility prop) (2024–2026); **Chakra** `Alert` (2024–2026); **WAI-ARIA APG** — the Alert pattern (`role=alert` live-region semantics, the static-vs-dynamic distinction, the region landmark); the inherited Feedback live-region pattern (see toast). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.3, 1.4.1, 1.3.1, 2.4.3, 1.4.3, 1.4.11, 2.5.5, plus the timing family (2.2.1) for the errors-not-in-toasts rationale.

## 15. Agent-consumable schema

```yaml
identity:
  id: banner
  name: Banner
  aliases: [alert, callout, section-message, message-bar, inline-notification, inline-alert, flash]
  category: feedback
  status: stable
description: >
  A PERSISTENT IN-FLOW message communicating an important state/error/
  announcement; stays until dismissed or the condition resolves; the Toast
  opposite (persistent vs transient) and CAN carry actions (in-flow + in the
  tab order). The documented home for the errors + actionable feedback Toast
  hands off. NOT a Toast (transient/floating/auto-dismiss), NOT an Inline
  Message (field validation), NOT a Dialog (blocking).
anatomy:
  parts:
    - "container (block-level in-flow, full-width page / contained section, severity-styled; defensive padding/margin)"
    - "severity icon (inherits icon; DECORATIVE aria-hidden; meaning in text + icon SHAPE — color-not-sole-carrier)"
    - "title/heading (concise; heading level MAPS DYNAMICALLY to the document outline)"
    - "body (context+consequence+resolution; width-constrained; inline Links inherit link + short lists)"
    - "action(s) (inherit button; in the tab order — legitimate here)"
    - "dismiss (inherits button, icon-only; min hit target + localized descriptive label)"
  placement: "page/global (full-width, shell top) | contextual/section (region/card radius+padding) | inline (Spectrum InlineAlert, padding-stripped — bridges Inline Message)"
api:
  inherits: [toast (live-region pattern), button (actions + dismiss), icon (severity), link (inline links)]
  props:
    - {name: severity/tone/status, type: enum, values: [info, success, warning, error, critical, neutral], description: "Polaris status->tone; MUI severity; Ant type"}
    - {name: title + children, type: "node/string + node", description: "compound (Callout.Text/AlertTitle) vs flat string; arbitrary node in flat title can break accessible-name"}
    - {name: dismissible, type: boolean, description: "EXPLICIT flag (Polaris v12+) — callback alone silently rendering a close is deprecated"}
    - {name: onDismiss, type: function, description: "PERSIST the dismissal (id+version -> storage)"}
    - {name: action/primaryAction/secondaryAction, type: "node slot | action-object array (Atlassian)"}
    - {name: role/aria-live override, type: string, description: "force/bypass the live role (Radix accessibility-mapping prop) — the static-vs-dynamic switch"}
    - {name: placement, type: enum, values: [global, section, inline]}
    - {name: icon, type: "node | false", description: override/disable severity icon}
    - {name: heading-level/as, type: "string/number", description: "polymorphic so the title interpolates the correct h* for its DOM context"}
states:
  runtime: [shown, dismissed]
variants:
  severity: [info, success, warning, error, critical, neutral, "upsell/promotional (Primer)"]
  dismissibility: "dismissible vs persistent (critical = persistent)"
  contrast: "low-contrast (subtle fill — default) vs high-contrast (inverted, emergencies) — Carbon; MUI filled/outlined/standard"
  placement: [page-global, contextual-section, inline]
  content: [with-title, with-action, with-list, icon-less]
  genre: "system/status vs promotional/announcement (cookie-consent/maintenance/announcement bars)"
accessibility:
  wcag-criteria: ["4.1.3", "1.4.1", "1.3.1", "2.4.3", "1.4.3", "1.4.11", "2.5.5"]
  static-vs-dynamic: "PRESENT AT LOAD = read in document order, NO live region (role=alert on a static banner is an ANTI-PATTERN — double/mistimed/dropped announce; use <section aria-labelledby> landmark). INSERTED DYNAMICALLY = live region: role=alert (assertive+atomic, errors) / role=status+aria-live=polite (info/success). Toast is always dynamic; Banner forks on timing."
  actions: "in the TAB ORDER (in-flow) — no Toast reachability problem"
  focus-on-dismiss: "banner unmount drops focus to <body> — return focus to a logical surviving node (page heading / prev landmark / trigger)"
  heading-level: "title h* MUST map to the document outline (hardcoded level breaks rotor nav)"
  color: "severity = icon SHAPE + text, not colour alone (1.4.1); icon is the semantic anchor for colour-blind users"
  no-overuse: "reserve assertive role=alert for genuinely urgent dynamic errors"
content:
  heading: "concise, objective, front-loads the issue ('Database connection failed'); NO trailing period (AT parses title as one string)"
  body: "never repeats heading; states consequence + resolution; 1-2 sentences, else truncate + 'View details' -> Dialog"
  actions: "predictive active verbs, 1-2 words ('Retry connection')"
  dismiss: "localized descriptive label ('Dismiss error message')"
  discipline: "match tone to severity (no cry-wolf); don't over-banner"
motion:
  in-flow: "appearance/removal shifts layout (CLS + disorientation risk); prefer opacity fade; height via Grid-rows 0fr->1fr or a Collapse wrapper (no thrash)"
  dismiss: "collapse height ~150-200ms + fade so content below doesn't teleport up"
  layout-shift: "dynamic page banners reserve space / anchor scroll"
  reduce-motion: "appear/disappear instantly (MUI zeroes durations)"
i18n:
  rtl: "icon/actions/dismiss flip via CSS logical properties (margin-inline-start, padding-inline-end, border-inline-start); hardcoded left/right is the anti-pattern"
  expansion: "+30-50% — NEVER fixed height (flex/grid grows); wrap (multi-line OK); action row wraps to a stacked row below the text on collision (Primer)"
implementation:
  - "static-vs-dynamic live-region wiring (the key trap) — load=no live region (<section aria-labelledby> landmark), action-insert=role=alert/status; blanket role=alert double-announces static"
  - "CONDITIONAL-LIVE-REGION trap (shared with Toast) — mounting the role=alert container simultaneously with the text fails to announce (VoiceOver+Safari); the region must exist before the mutation -> headless live-announcer decoupling the visual banner from a persistent hidden node"
  - "dynamic heading-level mapping — polymorphic/as/level prop for the correct h* (Atlassian ESLint-lints hardcoded levels)"
  - "dismissal PERSISTENCE keyed to id+version -> localStorage/cookie/pref in an init hook (don't re-nag; critical non-dismissible or re-show only while condition holds)"
  - "page (full-width shell-top) vs section (in the region); dynamic page banners RESERVE SPACE/anchor scroll (CLS/scroll-jump)"
  - "focus-on-dismiss -> logical surviving node"
  - "value-add libs leave to the consumer: getting static-vs-dynamic + heading-level right"
composition:
  stands-on: [toast (inherited live-region pattern — Feedback substrate), button (actions + dismiss), icon (severity), link (inline links)]
  alternative-to: [toast (transient/floating/non-actionable opposite — errors + actions hand off HERE), inline-message (field validation, padding-stripped), dialog (blocking; a critical banner's action can escalate to a Dialog), notification-center (persistent log — low-priority status)]
  refines: "the live-region pattern with the static-vs-dynamic rule (needed once a feedback surface can be present at load; Toast is always dynamic)"
notes:
  contested:
    - "static-vs-dynamic live-region semantics (most-botched)"
    - "Banner vs Alert naming (+ the role=alert collision — practice picks Banner)"
    - "dismissibility of critical banners"
    - "page-vs-section-vs-inline taxonomy + the inline-message boundary"
    - "system vs promotional genres; low vs high contrast default (practice: low)"
  trap:
    - "role=alert on a static at-load banner (double/mistimed/dropped announce)"
    - "conditional-mount of the live-region container simultaneously with text (VoiceOver+Safari silence)"
    - "hardcoded heading level breaking the document outline"
    - "banner blindness from stacking; non-persisted dismissal that re-nags"
    - "layout shift / CLS on dynamic insert; colour-only severity; focus drop on dismiss"
  inherited: "Toast's live-region pattern; Button actions+dismiss; Icon severity; Link inline links"
  role-in-family: "the second Feedback brief — the persistent, in-flow, actionable counterpart to Toast; the home for the errors+actions Toast hands off; refines the live-region pattern with static-vs-dynamic"
  evolution: "static-vs-dynamic live-region clarified; errors+actions moved Toast->Banner (WCAG timing); Alert->Banner rename/disambiguation (Primer Flash->Banner, Polaris status->tone); banner-blindness + visual de-escalation (low-contrast default); dismissal persistence"
  unverified:
    - "external 2026 version numbers"
    - "the static-vs-dynamic + conditional-mount AT behaviour specifics — verify against current screen readers"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-banner/` (16 June 2026), the second Feedback brief — the persistent, in-flow, actionable counterpart to Toast, inheriting the live-region announcement pattern Toast established and refining it with the static-vs-dynamic rule. It stands on Button (actions + dismiss), Icon (severity), and Link (inline body links). The two passes converged almost completely — the persistent/in-flow contract (the Toast opposite), the static-vs-dynamic live-region refinement (a banner present at load is read in document order and is NOT `role=alert` — that's an anti-pattern; only a dynamically-inserted one is a live region; alert/assertive for errors, status/polite for info), the placement taxonomy (page/global vs contextual/section vs the inline-message boundary), the severity + color-not-sole-carrier model (the icon shape as the semantic anchor), the legitimacy of actions (the Toast reachability problem doesn't exist in-flow), the dismissibility + don't-re-nag rules + focus-on-dismiss, the errors-and-actions-hand-off-from-Toast POV, the banner-blindness discipline, and `Banner` over `Alert` to avoid the `role=alert` collision. External-pass contributions folded in: the **dynamic heading-level mapping** trap (a hardcoded `<h2>` in an h4-context card breaks the outline — Atlassian ESLint-lints it; needs a polymorphic level prop), the **conditional-rendering-of-the-live-region** trap (shared root cause with Toast — VoiceOver+Safari silence when the region mounts with its content; a headless live-announcer decouples it), Polaris's `status`→`tone` migration + the explicit `dismissible` boolean, the contrast variants (Carbon low/high, MUI filled/outlined/standard — low-contrast default), Primer's upsell/promotional variant + actions-layout wrap, the CLS + Grid-rows `0fr`→`1fr` motion + MUI's reduced-motion zeroing, the no-period-titles parsing rule, Spectrum's padding-stripped inline variant, and the object-array-vs-slot actions API. Claude-pass contributions: the framing as the live-region-pattern-refiner and the errors/actions handoff home, the static-vs-dynamic as the sharp refinement of Toast's always-dynamic pattern, and the substrate map. The 2026 version numbers and the static-vs-dynamic / conditional-mount AT specifics are flagged unverified. Conformant to `components/_schema.md`. The second Feedback brief; Inline Message and Progress remain, reusing the live-region pattern Toast established and Banner refined. **The in-region-vs-toast-vs-global-banner routing decision at view scale lives in the `view-state-orchestration` pattern** — this brief owns the Banner's persistent-in-flow contract, severity model, and dismissibility rules; the pattern owns *when* an in-region Banner is the right surface for a recoverable error (vs. replacing the region; vs. routing to a Toast; vs. a global banner for system-wide context). (`see view-state-orchestration`.)*
