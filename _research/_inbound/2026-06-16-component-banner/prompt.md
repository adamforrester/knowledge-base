You are researching the Banner (Alert) component for a senior design
systems practitioner at a digital agency. The output is a field-truth
study of how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a banner /
alert is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Banner is the SECOND Feedback brief — the PERSISTENT, in-flow counterpart
to Toast. It is the opposite of a Toast: where a Toast floats at a screen
edge, auto-dismisses, and never takes focus, a Banner sits IN the document
flow, stays until dismissed or until the triggering condition resolves,
and (unlike a Toast) can legitimately carry actions because it is
persistent and in the tab order. It STANDS ON one category substrate and
three component substrates:
- THE LIVE-REGION ANNOUNCEMENT PATTERN is INHERITED from Toast
  (components/toast.md), which established it for the Feedback category
  (role=status/polite vs role=alert/assertive). But Banner REFINES it with
  a sharp distinction (the headline accessibility point — see below): a
  banner present at page LOAD is NOT a live region. Don't re-derive the
  pattern — reference it and concentrate on the static-vs-dynamic refinement.
- THE ACTIONS + DISMISS CONTROLS inherit BUTTON (components/button.md) —
  unlike Toast, actions ARE legitimate here. Don't re-derive Button.
- THE SEVERITY ICON inherits ICON (components/icon.md) — info/success/
  warning/error/critical; decorative; color-not-sole-carrier.
- INLINE BODY LINKS inherit LINK (components/link.md).
It FORWARD-REFERENCES the siblings: Toast (the transient boundary — see
components/toast.md), Inline Message (the field/section-level boundary —
not yet briefed), and Dialog (the blocking boundary — see components/dialog.md).

THE DEFINING BANNER-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE PERSISTENT / IN-FLOW CONTRACT (the headline, the Toast opposite): a
  Banner is part of the document flow (not a floating overlay), remains
  visible until dismissed or the underlying condition resolves, and demands
  sustained cognitive attention. Resolve the contract and the contrast with
  Toast (transient, floating, auto-dismiss, no-focus-steal) and Dialog
  (blocking, focus-trapped).
- THE STATIC-vs-DYNAMIC LIVE-REGION REFINEMENT (the sharp accessibility
  point that separates it from Toast): a banner rendered in the DOM at page
  LOAD is NOT announced via role=alert — it is read in normal document
  order, so it needs no live region (and role=alert on a static banner is
  WRONG / causes double or mistimed announcement). A banner inserted
  DYNAMICALLY in response to a user action SHOULD be a live region —
  role=alert/assertive for errors, role=status/aria-live=polite for
  info/success. Resolve the rule precisely (static = reading order / maybe
  a region landmark; dynamic = live region) and the contrast with Toast
  (always dynamic, always a live region).
- THE PLACEMENT TAXONOMY — page-level / global banner (an app-wide system
  status / maintenance / announcement bar / cookie-consent at the very top,
  often spanning full width above the header or below it) vs contextual /
  section banner (scoped to a page region or card, explaining the state of
  that section) vs the boundary with an INLINE MESSAGE (field/section-level
  validation attached to a specific control). Resolve the levels and the
  banner-vs-inline-message line.
- SEVERITY / VARIANTS — info / success / warning / error / critical; the
  color-not-sole-carrier rule (severity icon + text, never colour alone);
  the genres (a system/status banner vs a promotional/announcement banner —
  some systems split these). Resolve the severity model.
- ACTIONS ARE LEGITIMATE (the Toast opposite) — because the banner is
  persistent and in the tab order, it can carry links/buttons (View, Retry,
  Update, Dismiss); resolve the action affordances and the contrast with
  Toast's action-reachability problem (a banner has none — the action is
  simply in the flow).
- DISMISSIBILITY — dismissible (an X / close) vs persistent (stays until
  the condition resolves); the rule that a system-critical banner should
  NOT be dismissible (or its dismissal must persist so it doesn't re-nag);
  the focus-on-dismiss question (where focus goes when a banner is removed).
- THE NAMING OVERLOAD — Banner / Alert / Callout / Notification /
  MessageBar / SectionMessage / InlineAlert / Flash; the component "Alert"
  vs the ARIA role=alert vs alertdialog confusion; resolve the practice's
  default name and disambiguate it from role=alert.
- BANNER BLINDNESS / STACKING — the don't-stack-many-banners discipline,
  banner blindness (users tune out persistent banners), priority/dedupe,
  and the relationship to a notification center.

Field-leader systems to survey (web): Shopify Polaris (Banner — the
canonical persistent banner, tone + page/inline placement), GitHub Primer
(Flash / Banner), Atlassian (SectionMessage — the section/inline banner),
IBM Carbon (Notification — inline + actionable variants), Adobe Spectrum
(InlineAlert), Microsoft Fluent (MessageBar), Google Material 3 (Banner),
MUI (Alert + AlertTitle), Ant Design (Alert), Bootstrap (Alert — the
legacy reference), Radix Themes (Callout), Chakra (Alert). WAI-ARIA APG
(the Alert pattern role=alert + the live-region semantics; the
static-vs-dynamic distinction; the landmark/region question). Mobile
reference where relevant: Apple HIG, Material 3. Cite each with a version
date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Toast live-region pattern, the
Button actions/dismiss, the Icon severity, and the Link inline links; flag
unverified claims under notes.unverified).

1. Framing — what it is (a persistent in-flow message) and what it isn't
   (a transient Toast / a field Inline Message / a blocking Dialog); the
   persistent + static-vs-dynamic-live-region realities up front; why
   systems disagree.
2. Anatomy and parts — the severity icon, the title/heading, the body
   (with inline links), the action(s), the dismiss/close; the container +
   the placement levels.
3. Properties / API — severity/tone/status, title + children, dismissible
   + onDismiss, actions/primaryAction, the role/aria-live wiring (static vs
   dynamic), placement (page/section/inline), icon override.
4. States and variants — info/success/warning/error/critical; dismissible
   vs persistent; page/global vs contextual/section vs inline; with-action
   / with-title / with-list; system vs promotional.
5. Usage guidance — Banner (persistent, important, in-context) vs Toast
   (transient confirmation) vs Inline Message (field/section validation)
   vs Dialog (must-act, blocking); the errors-and-actions-go-here rule
   (the Toast handoff); the don't-stack / banner-blindness discipline.
6. Accessibility — the static-vs-dynamic live-region rule (no live region
   at load; role=alert/status only when inserted dynamically), role=alert
   vs role=status vs region landmark, the color-not-sole-carrier rule,
   the dismiss + focus-on-dismiss, the actions in the tab order, WCAG SCs.
7. Content guidelines — the heading + body, action labels, severity tone,
   the dismiss; concise + scannable; don't over-banner.
8. Motion and transition — minimal (in-flow appearance + layout-shift
   consideration), the dismiss collapse, reduce-motion.
9. Internationalization — RTL (icon + action + dismiss side flip via
   logical properties), text expansion (banners hold more text — wrap), the
   full-width page banner.
10. Naming — Banner / Alert / Callout / Notification / MessageBar /
    SectionMessage / InlineAlert / Flash; the practice's default; the
    role=alert disambiguation; aliases.
11. Implementation notes — the static-vs-dynamic live-region wiring (the
    key trap), dismissal persistence (don't re-nag), the page-level vs
    section placement, actions in the flow, layout-shift on insert/dismiss,
    headless vs opinionated.
12. Related and alternative components — typed relationships (Toast
    transient boundary + the inherited live-region pattern, Inline Message
    boundary, Dialog blocking boundary, Button actions/dismiss, Icon
    severity, Link inline links, the Notification Center).
13. Field POV evolution — recent shifts (the static-vs-dynamic live-region
    clarification, errors-move-from-toast-to-banner, the Alert/role=alert
    disambiguation, banner-blindness awareness).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a banner is — explain the
persistent/in-flow contract (the Toast opposite), the static-vs-dynamic
live-region rule (a banner at load is NOT role=alert; only a
dynamically-inserted one is — the sharp refinement of Toast's pattern), the
placement taxonomy (page/global vs section vs the inline-message boundary),
the severity + color-not-sole-carrier model, the legitimacy of actions
(the Toast opposite), the dismissibility + don't-re-nag rules, and the
Banner-vs-Alert-vs-role=alert naming overload that field leaders still
diverge on.
