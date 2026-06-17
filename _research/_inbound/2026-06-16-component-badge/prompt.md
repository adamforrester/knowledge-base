You are researching the Badge component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a badge is,
knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Badge is a small Foundations indicator primitive. It STANDS ON one
component substrate and one category pattern, and boundaries with Tag:
- THE OPTIONAL LEADING ICON (status badges) + the COUNT-OVERLAY HOST inherit
  ICON (components/icon.md). Don't re-derive Icon.
- THE SEVERITY / COLOR-NOT-SOLE-CARRIER pattern is shared with the Feedback
  severity model (Banner/Toast — components/banner.md, components/toast.md):
  info/success/warning/error/neutral conveyed by color + text/icon, never
  color alone. Reference it; don't re-derive.
- THE DYNAMIC-COUNT ANNOUNCEMENT lightly reuses the LIVE-REGION PATTERN from
  TOAST (components/toast.md): a count that changes (notifications
  incrementing) announces via a status live region.
It FORWARD-REFERENCES Tag (the interactive/removable token — not yet
briefed; draw the Badge-vs-Tag boundary) and Avatar (the presence-dot host
— not yet briefed), and is OVERLAID ON Icon buttons / Avatars / Tabs /
nav items (the count/dot host).

THE DEFINING BADGE-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE GENRE SPLIT + THE NAMING MORASS (the headline): "Badge" means
  different things across systems. Resolve the three genres — (1) the COUNT
  badge (a number overlaid on a host: a notification count "3"/"99+");
  (2) the DOT badge (a small dot, no number: unread/"something new"/an
  avatar presence dot); (3) the STATUS / LABEL badge (a small pill with
  text indicating state: "Active"/"Draft"/"Beta"/"New", usually standalone
  inline, not overlaid). And the naming morass: Fluent splits Badge
  (status) / CounterBadge (count) / PresenceBadge (dot); MUI/Ant Badge =
  the count/dot overlay; Polaris/Chakra Badge / Primer Label = the status
  pill. Resolve the practice's genre model + naming, and the BADGE-vs-TAG
  boundary (Badge = a NON-INTERACTIVE, non-removable indicator; Tag/Chip =
  an interactive/removable token).
- THE ANNOUNCEMENT CONTRACT (the accessibility crux): a count/dot badge is
  NOT a standalone focusable element — its meaning must be conveyed through
  the HOST'S accessible name ("Notifications, 3 unread"), NOT a floating
  "3" the screen reader reads in isolation. Resolve: the visual badge is
  aria-hidden while the host's aria-label carries the count; a DOT needs a
  text equivalent ("unread"); a DYNAMICALLY-changing count uses a status
  live region (role=status) to announce the change; and the standalone
  status pill announces its text.
- PLACEMENT / OVERLAP relative to the host — the count/dot overlaid at the
  top-trailing corner of an icon/avatar (the offset, the host clipping/
  overflow, the RTL flip to top-leading); vs the status pill inline (in a
  table cell, beside a title). Resolve the overlap-positioning model.
- COLOR-AS-SOLE-CARRIER (the WCAG 1.4.1 failure): the status badge's
  severity (info/success/warning/error/neutral) must pair color with text
  (and optionally an icon/shape) — a red badge alone fails for color-blind
  users. Resolve the severity model + the never-color-alone rule.
- COUNT HANDLING — the max-cap ("99+"/"9+"), the zero-handling
  (hide-at-zero vs show-zero vs the showZero prop), the dot-when-overflow
  or dot-when-no-count, the standalone-vs-overlay count.
- SIZING — small/large; the dot vs the count-pill vs the status-pill
  dimensions; the host-relative sizing.

Field-leader systems to survey (web): Microsoft Fluent (Badge /
CounterBadge / PresenceBadge — the clean tripartite split), MUI (Badge —
the count/dot overlay on a child, badgeContent/max/showZero/variant=dot/
overlap/anchorOrigin), Ant Design (Badge — count/dot/status + Ribbon +
standalone), Shopify Polaris (Badge — tone/progress, the status indicator),
GitHub Primer (Label / CounterLabel / StateLabel — the split), Adobe
Spectrum (Badge — the label/status), IBM Carbon (Tag with status + the
notification dot), Chakra UI (Badge — the status label), Google Material 3
(Badge — small dot vs large number), Base Web (Uber) (Badge). WAI-ARIA APG
(no formal badge pattern — the accessible-name-on-host + status live region
+ aria-hidden visual). Mobile reference where relevant. Cite each with a
version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Icon substrate, the color-not-
sole-carrier severity pattern, and the Toast live-region pattern (dynamic
count); flag unverified claims under notes.unverified).

1. Framing — what it is (the count/dot/status indicator) and what it isn't
   (an interactive/removable Tag); the genre split + the naming morass +
   the announcement contract up front; why systems disagree.
2. Anatomy and parts — the badge surface (count/dot/pill), the optional
   icon, the text, the host-overlap anchor; the (no) interactivity.
3. Properties / API — content (count/text), max, showZero, variant
   (dot/count/status), tone/severity, overlap/anchorOrigin (overlay),
   standalone vs overlaid, the accessible-label wiring.
4. States and variants — count / dot / status(label); the severity tones;
   overlaid vs standalone/inline; sizes; the zero/overflow states.
5. Usage guidance — Badge (non-interactive count/dot/status indicator) vs
   Tag/Chip (interactive/removable token) vs Toast/Banner (the feedback
   surfaces); when count vs dot vs status; the count-in-the-host-name rule.
6. Accessibility — the announcement contract (count in the host's
   accessible name, NOT a floating number; the dot's text equivalent; the
   dynamic-count status live region; aria-hidden the visual), color-not-
   sole-carrier, the standalone status announcement, WCAG SCs.
7. Content guidelines — the count cap, the status label (short, clear),
   the dot's hidden text, no-color-only, don't-overload.
8. Motion and transition — minimal (the count appearing/incrementing, the
   dot pulse), reduce-motion.
9. Internationalization — RTL (the overlay flips to top-leading, the
   number formatting via Intl), the status label expansion, dot neutrality.
10. Naming — Badge / CounterBadge / PresenceBadge / Label / CounterLabel /
    StateLabel / Status / Tag; the practice's default; the Badge-vs-Tag
    disambiguation; aliases.
11. Implementation notes — the host-overlap positioning + RTL flip + host
    clipping, the count-in-the-aria-label wiring + the dynamic-count live
    region, the max-cap/zero logic, the aria-hidden visual, headless vs
    opinionated.
12. Related and alternative components — typed relationships (Icon
    substrate + the count-overlay hosts (Icon button/Avatar/Tab/nav), the
    color-not-sole-carrier severity pattern (Banner/Toast), the Toast
    live-region (dynamic count), Tag the interactive/removable boundary,
    Avatar the presence-dot host).
13. Field POV evolution — recent shifts (the Badge/CounterBadge/Presence
    tripartite split, the count-in-the-host-name a11y settling, the
    color-not-sole-carrier hardening, the Badge-vs-Tag clarification).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a badge is — explain the genre
split (count/dot/status) + the naming morass + the Badge-vs-Tag boundary,
the announcement contract (the count belongs in the host's accessible name,
not a floating number; the dot's text equivalent; the dynamic-count live
region; aria-hidden the visual), the placement/overlap model + RTL flip,
the color-as-sole-carrier failure + the severity model, and the count
handling (max-cap/zero) that field leaders still diverge on.
