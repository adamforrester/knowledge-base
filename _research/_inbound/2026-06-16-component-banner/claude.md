# Banner (Alert) — field-truth study (Claude pass)

## 1. Framing
A Banner is a **persistent, in-flow message** that communicates an important state, error, or announcement and stays visible until dismissed or until the triggering condition resolves. It is the **opposite of a Toast**: where a Toast floats at a screen edge, auto-dismisses, and never takes focus, a Banner sits **in the document flow**, persists, demands sustained attention, and — crucially — **can legitimately carry actions** because it's persistent and in the tab order (the Toast action-reachability problem simply doesn't exist here). It is the second Feedback brief and **inherits the live-region announcement pattern Toast established** (role=status/polite vs role=alert/assertive — see toast), plus **Button** (actions + dismiss — see button), **Icon** (severity — see icon), and **Link** (inline body links — see link).

The one piece genuinely its own — the sharp accessibility refinement of Toast's pattern — is the **static-vs-dynamic live-region rule**: a banner **present in the DOM at page load** is read in normal document order and is **NOT a live region** (`role=alert` on a static banner is *wrong* — it causes double/mistimed announcements); only a banner **inserted dynamically** in response to an action should be a live region (alert/status). Toast is always dynamic, always a live region; Banner forks on insertion timing.

What it *isn't*: a **Toast** (transient, floating, auto-dismiss, no-focus-steal — see toast), an **Inline Message** (field/section validation attached to a specific control — see inline-message when briefed), or a **Dialog** (blocking, focus-trapped, must-act — see dialog). Why systems disagree: the static-vs-dynamic semantics, the placement taxonomy, dismissibility rules, and the Banner/Alert/`role=alert` naming overload.

## 2. Anatomy and parts
- **container** — a full-width (page) or contained (section) in-flow block, severity-styled.
- **severity icon** (inherits Icon) — info/success/warning/error/critical; decorative (`aria-hidden`); **color-not-sole-carrier** (§6).
- **title / heading** — an optional short heading (the essence).
- **body** — the message, which may contain **inline Links** (inherits Link) and short lists.
- **action(s)** (inherit Button) — optional links/buttons (View, Retry, Update) — legitimate here (§5).
- **dismiss / close** (inherits Button) — an optional icon "Dismiss" (§5/§6).

Placement levels: **page-level/global** (app-wide, full-width, top of page) / **contextual/section** (scoped to a region/card) / the **inline-message** boundary (field-level — out of scope).

## 3. Properties / API
- **`severity` / `tone` / `status`** — info / success / warning / error / critical (+ neutral); maps to icon + styling + (when dynamic) the live-region politeness.
- **`title` + `children`** — heading + body content (slotting inline Links/lists).
- **`dismissible` + `onDismiss`** — show a close control; **persist the dismissal** (don't re-nag — §11).
- **`action` / `primaryAction` / `secondaryAction`** — the action Buttons (label + onClick, or a Link).
- **role / `aria-live` wiring** — the static-vs-dynamic switch: nothing at load; `role=alert` (dynamic error) / `role=status` (dynamic info) on dynamic insert (§6).
- **placement** — page/global vs section/contextual (where it renders + full-width vs contained).
- **`icon`** — override/hide the severity icon.

## 4. States and variants
- **States:** shown / dismissed (removed); a banner has no interactive states beyond its actions/dismiss.
- **Variants:**
  - **severity:** info / success / warning / error / critical (+ neutral).
  - **dismissible vs persistent** (persistent for system-critical — §5).
  - **placement:** page/global (full-width announcement/system bar) / contextual/section (scoped).
  - **content:** with-title / with-action / with-list / icon-only-leading.
  - **genre:** system/status banner vs promotional/announcement banner (some systems split; cookie-consent/maintenance/announcement bars are the global genre).

## 5. Usage guidance
- **Use a Banner** for a **persistent, important, in-context message** the user should see and may need to act on: a system status/outage, a maintenance notice, a page-level error or warning, a feature announcement, a consent/cookie bar, the result of a process that must remain visible. It stays until resolved/dismissed.
- **Don't use a Banner for:**
  - A **brief, transient confirmation** ("Saved") → a **Toast** (see toast).
  - **Field/form validation** attached to a control → an **Inline Message** (`aria-describedby` — see text-field, inline-message).
  - A **blocking decision** that must be resolved before continuing → a **Dialog** (see dialog).
- **Decision frameworks:**
  - **Banner vs. Toast:** persistent + in-flow + may-carry-actions (Banner) vs. transient + floating + auto-dismiss + non-actionable (Toast). **Errors and actionable feedback that Toast hands off live here** — a Banner is where the "no-error-toasts" POV routes errors (persistent, reachable actions).
  - **Banner vs. Inline Message:** page/section-scoped, general (Banner) vs. attached to a specific field/control, validation (Inline Message).
  - **Page vs. section banner:** app-wide system state → page-level/global (full-width, top); a region/card's state → contextual/section.
  - **Don't over-banner:** stacking many persistent banners causes **banner blindness** (users tune them out); limit to the genuinely important, dedupe, and prioritise; route low-priority status to a notification center.

## 6. Accessibility
- **The static-vs-dynamic live-region rule (the sharp point, and the refinement of Toast's pattern):**
  - **Static (present at page load):** the banner is **read in normal document order** — it needs **no live region**, and **`role=alert` on a static banner is wrong** (AT may announce it out of turn, or double-announce). Optionally expose it as a **`region` landmark** (with an accessible name) if it's a significant standing area.
  - **Dynamic (inserted in response to an action):** it **should be a live region** — **`role="alert"`** (assertive) for errors/critical, **`role="status"` / `aria-live="polite"`** for info/success — so AT announces the new content without moving focus. (The same politeness model as Toast, but Toast is *always* dynamic.)
- **Actions are in the tab order** — because the banner is persistent and in-flow, its links/buttons are reachable by normal Tab (no hotkey/landmark gymnastics — the Toast action-reachability problem doesn't exist here).
- **Dismiss + focus-on-dismiss** — the close is a labelled "Dismiss"/"Close" Button; **manage focus on dismissal** (when the banner is removed, move focus to a sensible nearby element / the element that logically follows, not let it drop to `<body>`).
- **Color-not-sole-carrier** — severity is conveyed by **icon + text** (and often a heading word), never colour alone (SC 1.4.1).
- **Don't overuse `role=alert`** — reserve assertive for genuinely urgent dynamic errors; a wall of `role=alert` banners is announcement chaos.
- **WCAG SCs:** 4.1.3 (Status Messages — the dynamic live region, the headline), 1.4.1 (colour not alone), 1.3.1 (info & relationships — the structure/landmark), 2.4.3 (focus order — focus-on-dismiss), 1.4.3/1.4.11 (severity contrast), plus the action/dismiss Buttons' and inline Links' SCs.

## 7. Content guidelines
- **Heading + body** — a short heading carrying the essence (when used) + a concise body; state what happened and what (if anything) to do.
- **Action labels** — clear verbs ("Retry", "Update now", "View details"); keep to one or two.
- **Severity tone** — match the message to the severity (don't dress an error as info, or cry-wolf with critical); the icon + heading set the tone so the body can stay factual.
- **Dismiss** — a labelled close; don't make a system-critical banner dismissible (or persist the dismissal).
- **Concise & scannable; don't over-banner** — every persistent banner competes for attention; the more there are, the less each is seen.

## 8. Motion and transition
Minimal — a Banner is in-flow, so its appearance/removal **shifts layout**; animate the **insert/dismiss** with a height/opacity collapse (~150–200ms) to soften the reflow, and **reserve space / anchor scroll** so a banner appearing above content doesn't jump what the user is reading (especially a dynamically-inserted page banner). The dismiss collapses the banner's height then removes it. Under `prefers-reduced-motion: reduce`, snap (no collapse animation). No decorative motion. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** — the severity icon, action(s), and dismiss flip edges via logical properties (`padding-inline`, `margin-inline-start`); the full-width page banner is direction-neutral in placement but mirrors its internal layout.
- **Text expansion** — banners hold *more* text than toasts (+30–50% expansion); they must **wrap gracefully** (multi-line is fine here, unlike a toast) without truncating, and the action row wraps below the text on narrow widths.
- **Localised** heading, body, action labels. (See 13-internationalization-and-rtl.)

## 10. Naming
A heavily overloaded space: **`Banner`** (Polaris, Material 3 — the persistent in-flow message), **`Alert`** (MUI, Ant, Bootstrap, Chakra — the same thing, but *the name collides with the ARIA `role=alert`*), **`Callout`** (Radix Themes — the inline note/highlight), **`Notification`** (Carbon — inline variant), **`MessageBar`** (Fluent), **`SectionMessage`** (Atlassian — the section-scoped banner), **`InlineAlert`** (Spectrum), **`Flash`** (Primer). **The practice default: `Banner`** for the persistent in-flow message (avoiding the `Alert`/`role=alert` collision), with **`severity`**/`tone` for the variant, **page vs. section** as a placement prop, and the field-level case routed to **Inline Message**. Critically, **disambiguate the component name from `role=alert`** — the component is `Banner`; `role=alert` is an ARIA semantic applied *only* when the banner is dynamic + urgent. Aliases to map: `Alert`, `Callout`, `Notification`, `MessageBar`, `SectionMessage`, `InlineAlert`, `Flash`.

## 11. Implementation notes
- **The static-vs-dynamic live-region wiring (the key trap):** decide by insertion timing. Rendered at load → **no live region** (reading order; optionally a `region` landmark). Inserted on an action → wrap/assign **`role=alert`** (error) or **`role=status`** (info) so it's announced. A blanket `role=alert` on every banner (the common mistake) double-announces static ones and over-interrupts. (If you must reuse one element, only attach the live role when it's dynamically shown.)
- **Dismissal persistence (don't re-nag)** — persist a dismissal (localStorage/cookie/user-pref/server flag) keyed to the banner's identity + version, so a dismissed announcement/consent banner doesn't reappear on every navigation; a *system-critical* banner is either non-dismissible or re-shows only while the condition holds.
- **Page vs. section placement** — the page/global banner is a full-width block at the app shell top (above/below the header); the section banner renders inside the relevant region/card. Page banners that insert dynamically should **reserve space / anchor scroll** to avoid shifting content under the user (the layout-shift consideration).
- **Actions in the flow** — the action buttons/links are real, in-tab-order controls (no portal/hotkey machinery); a banner with a primary + dismiss is the common shape.
- **Focus on dismiss** — move focus sensibly when removing a banner (§6).
- **Don't hand-roll the semantics** — most systems ship `Alert`/`Banner` with the severity + icon + dismiss; the value-add is getting the **static-vs-dynamic live-region** right, which most libraries leave to the consumer (a frequent a11y bug).

## 12. Related and alternative components
- **Stands on:** the **live-region announcement pattern** inherited from Toast (the Feedback-category substrate — see toast), Button (actions + dismiss — see button), Icon (severity — see icon), Link (inline body links — see link).
- **Alternative to / boundary with:** **Toast** (transient, floating, auto-dismiss, non-actionable — the persistent/in-flow opposite; errors and actions hand off *to* the Banner — see toast), **Inline Message** (field/section validation attached to a control — see inline-message when briefed), **Dialog** (blocking, focus-trapped, must-act — see dialog), a **Notification Center** (a persistent log; low-priority status routes there instead of stacking banners).
- **Refines for the category:** the static-vs-dynamic live-region distinction that the live-region pattern (Toast established) needs once a feedback surface can be present at load.

(The second Feedback brief — the persistent, in-flow, actionable counterpart to Toast, refining the inherited live-region pattern with the static-vs-dynamic rule. See toast for the transient boundary + the inherited live-region pattern, dialog for the blocking boundary, inline-message when briefed for the field-level boundary, button/icon/link for the parts. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The static-vs-dynamic live-region clarification** — a11y practice hardened the rule that a banner present at load is *not* `role=alert` (reading order), only a dynamically-inserted one is — correcting the widespread "every Alert is `role=alert`" bug.
2. **Errors moved from Toast to Banner** — as the no-error-toasts POV spread (Polaris/Primer), the persistent Banner became the documented home for errors and actionable feedback (the Toast handoff).
3. **The `Alert`/`role=alert` disambiguation** — systems increasingly name the component `Banner` (or document the distinction) to stop conflating the component with the ARIA role.
4. **Banner-blindness awareness** — the don't-stack/dedupe/notification-center discipline emerged as persistent banners proliferated.
5. **Dismissal persistence** standardised (cookie/pref-keyed) so announcement/consent banners don't re-nag.

## 14. Sources cited
(Conservative; reconcile with external.) **Shopify Polaris** `Banner` (tone, page/inline placement — the canonical persistent banner) (2024–2026); **GitHub Primer** `Flash`/`Banner` (2024–2026); **Atlassian** `SectionMessage` (the section-scoped banner) (2024–2026); **IBM Carbon** Notification (inline + actionable) (2024–2026); **Adobe Spectrum** `InlineAlert` (2024–2026); **Microsoft Fluent** `MessageBar` (2024–2026); **Google Material 3** Banner (2024–2026); **MUI** `Alert`/`AlertTitle` (2024–2026); **Ant Design** `Alert` (2024–2026); **Bootstrap** `Alert` (the legacy reference) (2024–2026); **Radix Themes** `Callout` (2024–2026); **Chakra** `Alert` (2024–2026); **WAI-ARIA APG** — the Alert pattern (`role=alert` + live-region semantics; the static-vs-dynamic distinction; the region landmark); the inherited Feedback live-region pattern (see toast). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.3, 1.4.1, 1.3.1, 2.4.3, 1.4.3, 1.4.11.

## 15. Agent-consumable schema (conform to _schema.md in banner.md)
identity(Banner; aliases Alert/Callout/Notification/MessageBar/SectionMessage/InlineAlert/Flash; feedback; stable)/description(a PERSISTENT IN-FLOW message communicating an important state/error/announcement; stays until dismissed or the condition resolves; the Toast opposite (persistent vs transient) and CAN carry actions (persistent + in tab order); NOT a Toast (transient/floating/auto-dismiss), NOT an Inline Message (field/section validation), NOT a Dialog (blocking); the documented home for errors + actionable feedback that Toast hands off)/anatomy(container (full-width page / contained section, severity-styled); severity icon (inherits icon; aria-hidden; color-not-sole-carrier); optional title/heading; body (inline Links inherit link, short lists); action(s) (inherit button — legitimate here); dismiss/close (inherits button); placement levels page-global / contextual-section / inline-message boundary)/api(inherits: toast (live-region pattern), button (actions + dismiss), icon (severity), link (inline links); severity/tone/status info|success|warning|error|critical(+neutral); title + children; dismissible + onDismiss (PERSIST dismissal); action/primaryAction/secondaryAction; role/aria-live wiring (STATIC vs DYNAMIC switch); placement page|section; icon override/hide)/states(shown/dismissed; no interactive states beyond actions/dismiss; variants severity info|success|warning|error|critical(+neutral), dismissible vs persistent (persistent for critical), placement page-global vs contextual-section, content with-title/with-action/with-list, genre system/status vs promotional/announcement)/accessibility(THE STATIC-vs-DYNAMIC LIVE-REGION RULE — present at LOAD = read in document order, NO live region (role=alert on a static banner is WRONG, double/mistimed announce; optionally a region landmark); inserted DYNAMICALLY = live region role=alert/assertive (errors) or role=status/aria-live=polite (info/success); Toast is always dynamic, Banner forks on timing; actions in the TAB ORDER (no Toast reachability problem); dismiss = labelled Button + manage focus-on-dismiss (don't drop to body); color-not-sole-carrier (icon+text, 1.4.1); don't overuse role=alert; SC 4.1.3/1.4.1/1.3.1/2.4.3/1.4.3/1.4.11)/content(heading carrying the essence + concise body (what happened + what to do); action labels clear verbs (1-2); match tone to severity (no cry-wolf); labelled dismiss, critical not dismissible; concise + scannable, don't over-banner)/motion(minimal, IN-FLOW so appearance/removal shifts layout — animate insert/dismiss height/opacity collapse ~150-200ms + reserve space/anchor scroll so a page banner doesn't jump content; reduce-motion snaps)/i18n(RTL icon/action/dismiss edges flip via logical properties; text expansion — banners hold more text, WRAP gracefully (multi-line OK, unlike toast), action row wraps below on narrow; localise heading/body/actions)/implementation(static-vs-dynamic live-region wiring is THE trap — load=no live region (maybe region landmark), action-insert=role=alert/status; blanket role=alert double-announces static + over-interrupts; dismissal PERSISTENCE keyed to identity+version (don't re-nag; critical non-dismissible or re-show only while condition holds); page=full-width app-shell-top block vs section=inside the region; dynamic page banners RESERVE SPACE/anchor scroll (layout shift); actions are real in-tab-order controls (no portal/hotkey); focus-on-dismiss; value-add is getting static-vs-dynamic right (libs leave it to the consumer))/composition(stands-on toast (inherited live-region pattern — Feedback substrate), button (actions+dismiss), icon (severity), link (inline links); alternative-to toast (transient/floating/non-actionable opposite — errors+actions hand off here), inline-message (field/section validation), dialog (blocking), notification-center (persistent log — low-priority status routes there); REFINES the live-region pattern with the static-vs-dynamic rule)/notes(contested: the static-vs-dynamic live-region semantics (most-botched); Banner vs Alert naming (+ the role=alert collision); dismissibility of critical banners; page-vs-section-vs-inline taxonomy; system vs promotional genres. trap: role=alert on a static at-load banner (double/mistimed announce); blanket live region on every banner; banner blindness from stacking; non-persisted dismissal that re-nags; layout shift on dynamic insert; colour-only severity. inherited: Toast's live-region pattern; Button actions+dismiss; Icon severity; Link inline links. role-in-family: the second Feedback brief — the persistent, in-flow, actionable counterpart to Toast; refines the live-region pattern with static-vs-dynamic. evolution: static-vs-dynamic live-region clarified; errors moved Toast->Banner; Alert/role=alert disambiguation; banner-blindness awareness; dismissal persistence. unverified: external 2026 version numbers; the static-vs-dynamic AT behaviour specifics — verify against current screen readers.)
