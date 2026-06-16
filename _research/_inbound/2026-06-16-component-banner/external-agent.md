# Banner (Alert) — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/banner.md`; version numbers and the static-vs-dynamic / conditional-mount AT specifics flagged unverified. The two passes converged almost completely — no substantive disagreement; the external pass is unusually sharp on the heading-level and conditional-live-region traps.*

---

Research Report: The Banner (Alert) Component in Enterprise Design Systems

## 1. Framing
The Banner (Alert / Section Message / Callout) is the primary vehicle for persistent, in-flow systemic communication — the antithesis of the transient Toast and the blocking Dialog. Where a Toast floats at the edge, auto-dismisses, and can't steal focus, a Banner is embedded in the document flow, alters layout, persists until dismissed/resolved, and sits in the tab order. Contract: sustained cognitive attention without aggressive interruption (no focus trap, no vanishing before a cognitively impaired user can read it). Industry consensus is fragmented largely due to misunderstanding the WAI-ARIA alert pattern. Critical divergence: a Banner rendered STATICALLY at page load vs one injected DYNAMICALLY post-hydration. A load-time banner sits in the visual reading order and needs no live-region wiring; forcing an alert role on it degrades the SR experience (duplicate/mistimed/dropped announcements). Dynamic banners rely on live regions to interrupt the a11y tree. Systems conflate the visual geometry of a persistent message with the semantic urgency of an a11y event.

## 2. Anatomy
Container substrate (block-level section/div; semantic bg+border; defensive padding/margin, no horizontal overflow). Severity icon (inherits Icon; strictly DECORATIVE — meaning carried by text + a11y tree; color/iconography not sole carriers; hidden from AT). Title/heading (concise, weighted; heading level must DYNAMICALLY align with the host document outline — hardcoding generic levels breaks the sequential heading structure). Body (context/consequence/resolution; max-width constrained for line length; inline Links inherited). Action affordances (Primary/secondary inherited Buttons, in the tab order — departure from Toast). Dismiss control (tertiary icon-only Button at logical end/top-right; min hit area + localized accessible label).

## 3. API
severity/tone/status drives visual state (Polaris migrated status->tone for communicative intent; MUI severity; Ant type; enums info/success/warning/error). Content injection diverges: sub-component architecture (MUI/Chakra nest title sub-components) vs flat string props (Ant/Polaris — simpler but restricts rich text; arbitrary nodes in a flat title compromise accessible-name if the title labels the region). Dismissibility: older systems auto-rendered a close from a callback; modern (Polaris v12+) require an explicit boolean + callback to enforce intent. Accessibility overrides: downgrade an error's assertive alert to a polite status or bypass the live region for static SSR banners (Radix Themes exposes an explicit accessibility mapping prop). Actions: React node slots vs structured action-object arrays (Atlassian SectionMessage parses {text, onClick} to conform to layout). Custom icon overrides / disable iconography.

## 4. States and variants
Severity spectrum: Info (blue/neutral; Primer adds a purple UPSELL variant separating promotional from system), Success (green/checkmark), Warning (yellow/orange), Error/Critical (red — Primer: critical = an error the user must resolve for the component to disappear). Dismissible vs persistent (system-critical e.g. failed payment must persist). Contrast: Carbon low-contrast (subtle fill — recommended default) vs high-contrast (inverted — emergencies); MUI filled/outlined/standard. Placement: page/global (full-width, no radius, dominates the shell) vs section (inherits parent radius/padding) vs inline (Spectrum InlineAlert strips vertical padding, bridges section banner and micro validation).

## 5. Usage guidance
Bounded by Toast / Dialog / Inline Message. Opinionated default: errors and actionable systemic feedback belong in a Banner, NOT a Toast — a Toast auto-dismisses and fails WCAG 2.2.3 (timing) for motor/cognitively impaired users who can't interact with vanishing targets; Banners give infinite time. Placement taxonomy: page-level global (maintenance, trial expiry, cookie consent — apex of the DOM); contextual section (a region's state — empty state, sync error); the Inline Message boundary (feedback attached to a single control). Banner blindness: over-use makes users tune out persistent blocks like ads; stacking displaces content below the fold. Strict dedupe + priority queue — show only the highest-severity banner; route secondary to a Notification Center or aggregate into one "multiple alerts" banner.

## 6. Accessibility
Static-vs-dynamic is the sharp distinction. Static (at load): SR reads the DOM linearly top-to-bottom; the banner sits in reading order; applying an assertive alert / active live region is a critical anti-pattern (AT assumes live regions are empty containers for subsequent changes -> double announce / interrupt the page summary / ignore on init race). Use semantic HTML — ideally <section aria-labelledby> pointing to the title, a quiet discoverable landmark. Dynamic (injected on action/async): must be a live region to notify without shifting focus. Error/critical -> native alert role (implicitly assertive + atomic; interrupts the speech buffer). Info/success -> status role (implicitly polite; waits for the current sentence). Focus management: in-flow interactive elements have standard tab index; on dismissal, if focus rested on the dismiss button, node removal drops focus to body — disorienting; programmatically return focus to a logical surviving node (page heading / previous landmark / the trigger). WCAG 1.4.1 — colour not the sole carrier; the icon shape (triangle/circle/checkmark) is the semantic anchor for colour-blind users. Min target spacing/sizing.

## 7. Content guidelines
Scannable, objective, no filler. Heading: concise summary; Carbon prohibits trailing periods (SR reads rich title as one string; rogue punctuation causes unnatural pauses); front-load the issue ("Database connection failed", not "Warning!"). Body: never repeats the heading; explains the consequence (was data preserved?) + resolution; 1-2 sentences, else truncate + "View details" -> Dialog. Action labels: strong predictive verbs, 1-2 words ("Retry connection", "Update billing"). Dismiss accessible label localized + descriptive ("Dismiss error message", not bare "Close").

## 8. Motion
In-flow appearance/removal impacts surrounding layout (CLS risk + disorientation). Avoid aggressive entrances; prefer opacity. Animate height via CSS Grid template rows 0->1fr or a Collapse wrapper (MUI) to avoid render-thread thrash. Dismiss: not instantaneous — a 150-200ms height collapse + opacity fade lets the visual system track the shift. All transitions wrapped in prefers-reduced-motion; MUI overrides durations to 0ms when reduced motion is requested.

## 9. i18n
Icon position / text alignment / dismiss must mirror for RTL (Arabic/Hebrew). Hardcoded left/right margins/padding is a catastrophic anti-pattern; enforce CSS logical properties (margin-inline-start, padding-inline-end, border-inline-start). Text expansion: English->German/Russian +30-50%; never fixed heights (Flexbox/Grid grows vertically); actions wrap to a stacked row below the text when collisions occur (Primer actions layout) so touch targets aren't obscured.

## 10. Naming
Alert (MUI/Chakra/Ant/Bootstrap — common legacy, but a dangerous default: conflates the visual component with the ARIA alert role; <Alert severity="info"> invites assuming alert semantics when it should be a status region). Flash (legacy Rails / old Primer). Section Message / Message Bar (Atlassian / Fluent — descriptive but verbose). Callout (Radix Themes — but historically floating/tooltip). Inline Notification (Carbon — verbose). Opinionated default: Banner — divorces the visual in-flow geometry from the ARIA alert event; aligns with Polaris/Primer/Material 3; contrasts with the transient Toast. A Banner is the visual substrate; an alert is an invisible accessibility event.

## 11. Implementation notes
Conditional rendering of live regions is the most critical failure: mounting the alert-role container simultaneously with the error text (common in component frameworks) makes SRs — particularly macOS VoiceOver + Safari — fail to announce; the live-region container must be present in the a11y tree BEFORE the DOM mutation. Provide headless live-announcer wrappers decoupling the visual banner from hidden DOM nodes. Dismissal persistence: a dismissed global/section banner (privacy policy, maintenance) must persist across loads/navigations/remounts — accept a unique id, cross-reference localStorage/cookies in an init hook; ephemeral local state re-nags on refresh and erodes trust. Heading-level interpolation: injecting a hardcoded h2 into an h4-context card breaks the outline (Atlassian SectionMessage lints this via ESLint); accept a polymorphic prop / heading-level parameter.

## 12. Related and alternative components
Toast (transient boundary, the inverse — inherits the same live-region injection but is transient/overlay/auto-dismiss/no-focus-trap/no-critical-actions; upgrade to Banner if intervention or reading time is needed). Dialog (blocking boundary / escalation — a critical banner's resolution requiring extensive input invokes a modal Dialog). Inline Message (micro field boundary — stripped of fills/borders, adjacent to inputs). A Banner is a compositional wrapper inheriting Icon, Button, Link.

## 13. Field POV evolution
Historically over-indexed on Toasts for all feedback -> chaotic interfaces where errors vanished. Massive course correction migrating interactive/error states from transient Toasts into persistent in-flow Banners, driven by WCAG 2.1/2.2 enforcement penalizing timed error resolution. Semantic disambiguation of Alert-the-role vs Alert-the-component drove renames (GitHub Flash->Banner). Banner-blindness awareness -> visual de-escalation (low-contrast defaults — Carbon; systemic dedup). Banners shifting from loud megaphones to respectful integrated status indicators.

## 14. Sources cited
Shopify Polaris v12.0.0+ (Banner, status->tone, strict dismissibility). GitHub Primer (Banner from Flash, landmark a11y, actions wrap, upsell). IBM Carbon v11/v12 (Notification, inline vs toast split, low/high contrast, actionable focus sentinels). Atlassian v8.13.0+ (SectionMessage, ESLint heading-level lint, object-array actions). Microsoft Fluent 2 React v9 (MessageBar, politeness->aria-live). MUI v5 (Alert, severities, filled/outlined, sub-components). Adobe Spectrum v3.29.0+ (InlineAlert, logical properties). Ant Design v5/v6.4+ (Alert). Radix Themes v3.2.0+ (Callout, role-bypass mapping). Chakra v2/v3 (Alert). WAI-ARIA APG (Alert Pattern — assertive live regions, static-vs-dynamic, interruption timing).

## 15. Agent-consumable schema

```yaml
identity:
  name: Banner
  aliases: [Alert, Callout, SectionMessage, MessageBar, InlineNotification, Flash]
  category: Feedback
  description: A persistent, in-flow messaging component for important system states/errors/prompts requiring sustained cognitive attention without blocking the workflow or trapping focus.
anatomy:
  root_container: section/div boundary managing layout displacement
  severity_icon: decorative inline-start icon (aria-hidden=true)
  title: concise summary requiring dynamic context-aware heading-level mapping
  body: contextual text (consequence + resolution)
  actions: inherited Buttons in the logical tab order
  dismiss_control: tertiary icon button with localized accessible label
api:
  tone_severity: {type: enum, values: [info, success, warning, error, critical, neutral]}
  title: {type: node_or_string, note: node injection must preserve accessible naming}
  children: {type: node}
  dismissible: {type: boolean, note: explicit flag enabling the dismiss control}
  onDismiss: {type: function, note: local removal or state-persistence logic}
  actions: {type: node_or_array}
  roleOverride: {type: string, note: bypass default ARIA live regions for static SSR}
  placement: {type: enum, values: [global, section, inline]}
states_and_variants:
  severities: [Information, Success, Warning, Error]
  behavioral: persistent (critical) vs dismissible (informational)
  contrast: low-contrast (subtle) vs high-contrast (inverted)
  layouts: full-width global vs border-radius-constrained section
accessibility:
  static_render: semantic landmark (section aria-labelledby); NO live regions at load (prevents duplicate announcements)
  dynamic_render: role=alert (assertive errors) or role=status (polite info)
  focus_management: tab order flows through internal actions; return focus to a logical surviving node on dismiss
  contrast_mandate: colour not sole carrier; severity icons required; text/bg passes 1.4.3
content:
  - titles objective, no trailing punctuation (SR parsing)
  - action labels predictive verbs, 1-2 words
  - body focuses on consequence + resolution, not title repetition
implementation:
  traps:
    - live-region container must exist in the DOM before text injection (avoid conditional-render of the root)
    - global-banner dismissal must map to localStorage/cookies (no re-nag on refresh)
  motion: Grid-row animation or opacity fades, wrapped in prefers-reduced-motion
  i18n: RTL logical properties; layout flexibility for ~50% text expansion
composition:
  inherits: [Icon (severity), Button (actions + dismiss), Link (inline navigation)]
  forward_references: [Toast (transient boundary), Dialog (blocking boundary), Inline Message (field-level boundary)]
notes:
  opinionated_default: systemic errors requiring user action MUST use Banners, never transient Toasts
  banner_blindness: deduplicate; don't stack multiple global banners; low-contrast defaults
```
