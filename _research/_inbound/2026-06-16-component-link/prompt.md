You are researching the Link component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a link is,
knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Link is a Navigation-category brief and the routing counterpart to two
already-briefed components — resolve those boundaries rather than
re-derive them:
- BUTTON (components/button.md) drew the link-vs-button boundary from the
  button side: <a href> NAVIGATES (Enter only, exposes a URL to
  middle-click / new-tab / the context menu / the a11y tree), <button>
  ACTS (Space + Enter, no URL). Close this boundary from the LINK side,
  and cover the LinkButton (a link styled as a button) that the Button
  brief named.
- TABS and SEGMENTED CONTROL both established the rule that ROUTING (a
  URL/route change) is a nav of LINKS with aria-current, NOT a tablist /
  segmented control. Link is where that routing pattern lives. Cover the
  in-a-nav-landmark navigation-link case and the aria-current contract.

THE DEFINING LINK-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE LINK-VS-BUTTON BOUNDARY from the link side, and the
  link-with-no-href anti-pattern (a without href, or a[role=button], is
  not a real link — not focusable/operable as a link); the
  "JS-navigation still uses <a href>" rule.
- INLINE vs. STANDALONE vs. NAVIGATION link — an inline link in running
  text, a standalone CTA-style link, and a link inside a <nav> landmark;
  how the underline discipline and aria-current differ across the three.
- THE UNDERLINE DISCIPLINE — underline as the non-colour affordance for
  inline links (colour alone fails WCAG 1.4.1); when underline may be
  dropped (standalone/nav links with other affordances) and the
  contrast contract (link vs. surrounding text >=3:1 AND text >=4.5:1).
- INTERNAL vs. EXTERNAL links — the external-link indicator (icon + a
  visually-hidden "opens in new tab/external"), target=_blank with
  rel="noopener noreferrer" (tabnabbing/security), and the
  warn-before-opening-a-new-context accessibility rule.
- aria-current — the values (page / step / location / true) and which to
  use for the current nav item; visited state (:visited) and its privacy
  constraints.
- THE FRAMEWORK-ROUTER POLYMORPHISM — the design-system Link must render
  a real <a href> for progressive enhancement / middle-click / SEO, yet
  also wrap a client-side router's Link (Next.js, React Router, TanStack)
  for SPA navigation. Resolve the asChild / render-prop / as-prop
  polymorphism pattern and why a plain onClick-navigation div is wrong.
- SKIP LINKS (skip-to-content), download links, and disabled-link
  handling (links can't truly be disabled).

Field-leader systems to survey (web): Shopify Polaris, Adobe Spectrum
(React Aria Link), Google Material 3, IBM Carbon, GitHub Primer,
Atlassian Design System, Base Web (Uber). Mobile reference where relevant:
Apple HIG, Material 3. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; flag unverified claims under notes.unverified).

1. Framing — what it is, what it isn't, why systems disagree.
2. Anatomy and parts — the <a>, label, optional external/new-tab icon,
   visited/current affordances.
3. Properties / API — href, target/rel, the polymorphic as/asChild for
   router integration, variant (inline/standalone/quiet), external.
4. States and variants — rest / hover / focus-visible / active / visited
   / current; inline vs. standalone vs. nav; quiet/subtle.
5. Usage guidance — when to use vs. Button / LinkButton; internal vs.
   external; new-tab discipline.
6. Accessibility — link role/semantics, the no-href anti-pattern, the
   underline/contrast contract, aria-current, new-tab warning, skip
   links, the WCAG SC it participates in.
7. Content guidelines — descriptive link text (no "click here"/"read
   more"), the link-text-in-context rule, external/file indicators.
8. Motion and transition — hover/focus underline transition,
   reduce-motion.
9. Internationalization — RTL (icon side, direction), text expansion,
   the in-running-text wrapping.
10. Naming — Link / TextLink / Anchor; the practice's default; aliases
    incl. LinkButton.
11. Implementation notes — the router polymorphism (asChild), real <a
    href> always, target/rel security, the no-href trap, skip-link
    implementation, headless-vs-opinionated.
12. Related and alternative components — typed relationships (Button,
    LinkButton, the nav landmark, Breadcrumbs, Menu item, Tabs routing
    boundary).
13. Field POV evolution — recent shifts (framework-router asChild
    convergence, the death of onClick-div navigation).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a link is — explain the
link-vs-button boundary from the link side, the inline/standalone/nav
distinction and the underline discipline, the internal/external and
new-tab contract, aria-current, and the framework-router polymorphism
that field leaders still disagree on.
