You are researching the Tabs component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what tabs are,
knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Tabs is the FIRST brief in the Navigation category. It does NOT inherit
the form-field substrate (no label/helper/error wiring like the form
controls). It is adjacent to two already-briefed components, and you
should resolve those boundaries crisply rather than re-derive them:
- SEGMENTED CONTROL (components/segmented-control.md) drew the boundary
  from its side: a segmented control switches a VALUE/filter/view IN
  PLACE; Tabs switch entire PANELS (role=tablist/tab/tabpanel). Confirm
  and sharpen the tabs-vs-segmented boundary from the tabs side.
- the tabs share the horizontal single-select row, roving tabindex, and a
  sliding active-indicator with segmented control; note the shared
  mechanics, don't re-explain them from scratch.

THE DEFINING TABS-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE ARIA TABS PATTERN — role="tablist" / role="tab" / role="tabpanel",
  aria-selected, the tab→panel aria-controls and panel→tab
  aria-labelledby wiring, tabindex=0 on the panel (focusable/scrollable),
  roving tabindex on the tablist.
- MANUAL vs. AUTOMATIC ACTIVATION (the headline contested decision) —
  does arrow-key focus immediately switch the panel (automatic /
  selection-follows-focus) or just move focus, requiring Enter/Space to
  activate (manual)? The APG rule of thumb (automatic when panels are
  cheap/instant; manual when switching is expensive or panels load
  async). Resolve the practice's default and the rule for choosing.
- THE TABS-VS-NAVIGATION (ROUTING) BOUNDARY — in-page tabs (tablist,
  swap panels in place) vs. tabs that change the URL/route. role="tab" is
  WRONG for routing; route-changing "tabs" should be a nav landmark with
  links (and aria-current), not a tablist. This boundary is heavily
  violated; resolve it crisply (parallel to segmented control's
  no-routing rule).
- LAZY-LOADING / PANEL MOUNTING — mount-all vs. mount-on-activate vs.
  keep-alive (mounted-but-hidden); the state-preservation vs. performance
  tradeoff, and forced-mount for SEO/printing.
- OVERFLOW HANDLING — too many tabs: horizontal scroll, swipe, a "more"
  overflow menu, or wrap to multiple rows; the responsive contract.
- ORIENTATION — horizontal default vs. vertical (aria-orientation,
  arrows swap to Up/Down).
- VARIANTS — closable/addable tabs (the browser/editor-tab pattern),
  count badges / icons in tabs, the active indicator (underline/pill),
  and the contained-vs-underline visual styles.

Field-leader systems to survey (web): Shopify Polaris, Adobe Spectrum
(React Aria Tabs), Google Material 3, IBM Carbon, GitHub Primer,
Atlassian Design System, Base Web (Uber). Mobile reference where
relevant: Apple HIG (tab bars vs. in-page segmented), Material 3 (Compose
/ tabs), Microsoft Fluent.

Cite each system referenced with a version date — e.g., (Polaris 12.0,
2025), (Material 3, 2024), (Spectrum 2024.4). Currency matters; section
14 of the brief is the auditable record.

Output structure — follow this 15-section spine:

1. Framing — what this component is, what it isn't, why systems disagree.
2. Anatomy and parts — tablist, tab, tabpanel, indicator, overflow
   affordance; named parts, slot vocabulary.
3. Properties / API — converged prop set; divergences with reasoning
   (selectedKey/value, activation mode, orientation, lazy mounting).
4. States and variants — runtime states (rest / hover / focus-visible /
   selected / disabled) vs. intentional variants (underline / contained,
   horizontal / vertical, closable, with-icon/badge, scrollable);
   canonical matrix.
5. Usage guidance — when to use, when not to use, what to use instead
   (the tabs-vs-segmented and tabs-vs-navigation decisions).
6. Accessibility — component-specific concerns (the tablist/tab/tabpanel
   contract, roving tabindex, manual vs automatic activation, the panel
   focus/labelling wiring, the WCAG SC it participates in). The reader
   has read 14-accessibility, 17-accessibility-annotation-contract, and
   28-web-accessibility-implementation; do not re-state the theory.
7. Content guidelines — tab labels (short, parallel nouns), icon/badge
   use, the no-multiline rule.
8. Motion and transition — the active-indicator slide, panel
   enter/exit, the reduce-motion contract.
9. Internationalization — RTL (tab order + indicator + arrow direction),
   text expansion, scrollable-tabs behaviour.
10. Naming — Tabs / TabList / Tab / TabPanel; the practice's default;
    aliases.
11. Implementation notes — framework gotchas (controlled selectedKey,
    roving tabindex, panel mounting strategy, the indicator measurement,
    deep-linking tab state without routing), prop-vs-slot decisions,
    headless-vs-opinionated tension.
12. Related and alternative components — typed relationships (composes
    with / alternative to / supersedes / superseded by), incl. segmented
    control, the nav/routing alternative, accordion, and stepper/wizard.
13. Field POV evolution — recent shifts worth flagging.
14. Sources cited — every system referenced, with version dates.
15. Agent-consumable schema — a fenced YAML block following the locked
    key order and conventions in components/_schema.md (identity,
    description, [anatomy], api, states, variants, accessibility,
    content, [motion], [i18n], [implementation], composition, notes;
    flag unverified claims under notes.unverified). The schema must not
    contradict any prose section above; if it does, the prose wins.

Output format: Structured markdown. Use H2 headings that match the
numbered spine above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather than
declaring a winner. Where claims depend on current platform state — feature
names, version flags, ARIA attributes that recently changed — date them
and note the verification path.

Depth: Expert audience. Do not explain what tabs are or that they switch
panels — explain the manual-vs-automatic activation decision, the
tablist/tabpanel ARIA + roving-tabindex contract, the tabs-vs-navigation
(routing) boundary, the lazy-mounting tradeoff, and the overflow handling
that field leaders still disagree on.
