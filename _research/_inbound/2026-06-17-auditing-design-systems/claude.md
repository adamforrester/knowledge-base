# Auditing design systems as a discipline — at agency scale

The design-systems field talks about audits constantly, audits things constantly, and has not articulated auditing as a discipline of its own. The audit-shaped artefacts are everywhere — Sparkbox's case studies, EightShapes' contribution-and-coverage-audit posts, UXPin's "62 shades of gray" framing that became the canonical buy-in story, Brad Frost's interface inventory chapter in *Atomic Design*, the InVision *Design Systems Handbook* audit pages, conference talks at Clarity and Config and Smashing where individual practitioners narrate the audit they ran most recently. What the field has not produced is a unified treatment of *the audit as a methodology*: what makes a DS audit categorically different from adjacent audit forms, what eight surfaces a comprehensive audit examines, how the audit becomes a productised commercial deliverable rather than a thing-the-senior-practitioner-does-inside-Discovery, what the report shape is that produces buy-in, how continuous auditing in CI complements the point-in-time audit, and how the audit fits with Six Signs and the maturity diagnostic in a unified Discovery triad.

This document treats auditing as a discipline. Six sections in order: why this is a DS-architecture concern (not a generic UX audit concern); the eight-lane methodology; audit-as-deliverable; reporting templates and buy-in tactics; continuous audit and drift detection; and the Discovery triad. The references section names the field's primary sources, with notes on which translate to agency contexts and which require translation.

A note on the agency-side angle. Most published audit content is written from in-house practitioner positions — the audit being run is the in-house team's diagnostic of their own system, often published as case study or retrospective. Agency-side audit work is structurally different: the auditor doesn't author the system, has limited time on the engagement, has to defend findings against the team that *did* author the system, and is operating against the commercial pressure of the audit being a sellable engagement of its own. The agency lens is what's missing from the field's audit literature; this document foregrounds it.

---

## 1. Why a DS audit is a DS-architecture concern, not a generic UX audit concern

### The audit as a stable, named methodology

A DS audit is a methodology in its own right, with its own evidence types, scoring rubrics, and reporting shape. It is not a UX audit applied to a system; it is not an accessibility audit broadened in scope; it is not a front-end code audit narrowed to component code. The categorical difference is in *what the audit reads*, not in how rigorously it reads it.

A **UX audit** reads pages and screens. The unit of analysis is the user-facing surface; the methodology is heuristic (Nielsen's ten or some derivative), the evidence is screenshots and task walkthroughs, the findings are surface-specific, the recommendations are page-level fixes. The audit's authority is the practitioner's pattern recognition against the heuristic set.

An **accessibility audit** reads against a standard. The unit of analysis is the conformance criterion (WCAG 2.2's 87 success criteria as of late 2023, or an equivalent regional standard); the methodology is conformance-evaluation per the W3C's WCAG-EM methodology; the evidence is per-criterion test results across a representative sample; the findings are stated as conformance failures with severity per criterion. The audit's authority is the standard itself.

A **front-end code audit** reads codebases. The unit of analysis is the file, function, or module; the methodology is static analysis plus practitioner reading; the evidence is code excerpts and architectural diagrams; the findings are code-quality concerns, security issues, performance problems, technical debt. The audit's authority is professional engineering practice.

A **DS audit reads architecture, contracts, protocols, and the cross-surface drift signal.** The unit of analysis shifts depending on lane (the token tree, the component API, the contribution model, the adoption pattern); the methodology blends specification audit (against DTCG, ARIA APG, the system's own stated rules), heuristic audit (against the practitioner's accumulated pattern catalogue), and census audit (where tooling allows automated coverage scans). The evidence is multi-layered — token-tree extracts, component prop matrices, build-time scan output, contribution-velocity metrics, executive-stakeholder interviews. The findings are *architectural*: the system's foundations are misshapen here, the components-as-contract is broken there, the governance protocol is failing in this specific way. The audit's authority is methodological (the audit followed a stated method), evidential (each finding cites specific instances), and field-framed (industry consensus exists; the system diverges here, with this consequence).

The categorical difference matters because DS audit findings *generalise* in ways UX audit findings don't. A senior DS practitioner who has run twenty audits has a method that compounds — the failure modes accumulate, the patterns become visible, the diagnostic accuracy increases. Each audit is faster than the last because the practitioner recognises the pattern in the first hour rather than constructing it across the week. UX audit findings are surface-specific and don't generalise the same way; the heuristics generalise, but the findings against them are particular to each product. The agency's compounding asset in audit work is *audit method-IP*, not any specific audit's artefact. This is the same dynamic that makes the agency-side DS practitioner's cross-engagement experience the practice's compounding asset (per the team-and-discipline literature); the audit is a particularly clean expression of that compounding because the methodology is articulable.

### How DS audits get miscategorised, and what it costs

The miscategorisation happens at three points in the engagement.

**At procurement.** The client's procurement function reads "design system audit" against the catalogue of audit-shaped engagements they have priced before. The closest comparable is usually a UX audit (priced as a heuristic walkthrough at $15k–$40k) or an accessibility audit (priced as a WCAG conformance evaluation at $20k–$60k). The DS audit gets sized against those benchmarks. The result: the engagement is under-budgeted for the architectural depth the methodology demands. A DS audit on a moderately mature multi-platform system that genuinely covers all eight lanes should be sized at $50k–$120k for a 5–10 day engagement; clients budgeting against the UX-audit anchor produce $30k SOWs that force the audit to skip lanes.

The pre-engagement conversation has to *re-anchor procurement*. The DS audit is not a UX audit on more screens; it is an architectural diagnostic of a multi-tier system. The price comparison that matters is not "what did your last UX audit cost" but "what will this audit's recommendations save you on the next 18 months of system work." Audits that surface a token-tier consolidation opportunity routinely justify their cost ten times over against the redesign work the consolidation prevents. The agency lead's discipline at procurement is to refuse the wrong anchor.

**At kick-off.** The client team's expectation arrives at the kick-off meeting as the heuristic walk-through. They expect the auditor to tour their Figma library, click around their staging site, and produce a list of "things to fix." When the auditor opens with stakeholder interviews, requests build-pipeline access, asks for the token source-of-truth file, and starts pulling component coverage metrics from their analytics, the team feels audited in a way they didn't authorise.

The fix is the pre-audit framing document, sent before kick-off, that names what the audit will examine and why. The framing document is the audit's contract with the client team — it states the eight lanes (or the subset in scope), the evidence the audit will collect, the access the audit needs, the interviews the audit will conduct, the deliverables the audit will produce. With the framing established, the kick-off becomes a pre-flight check rather than a renegotiation. Without it, the first day of the audit is consumed by orientation and the audit's depth is correspondingly reduced.

**At delivery.** The client team reads the audit report against the heuristic-walkthrough expectation: a list of fixes. When the report opens with cross-lane patterns and architectural diagnostics, the team responds with "but what should we *fix*?" The audit's diagnostic value lives in the architectural framing; the team wants the punch list. The fix is the report's structure (executive summary first; per-lane findings second; cross-lane patterns third; recommendations as a separate section that *does* read as a punch list, organised in three priority bands). The diagnostic and the punch list are both present; the report's structure ensures both audiences land on the artefact they need first.

The cost of these miscategorisations is real and quantifiable. Wrong scoping reduces the audit's depth (lanes get skipped). Wrong team mix produces the wrong evidence (a UX-led audit can't read the build pipeline; an engineering-led audit doesn't surface the design-tool drift). Wrong output positions the audit as engineering housekeeping rather than commercial value. Wrong buy-in produces an audit that lives in a Notion page nobody refers to again. The senior agency practitioner who has run the productised audit a dozen times has internalised the framing, the contract, and the report shape; the practice without the productised methodology re-discovers each of these per engagement.

### Why DS audits compound across engagements

A senior DS auditor's method improves with each engagement in ways a UX auditor's doesn't. The mechanism: DS audit findings cluster around a small number of *architectural failure modes* that recur across systems with surprising consistency, while UX audit findings are particular to each product's domain and visual language.

The recurring DS failure modes — the ones a senior auditor recognises in the first hour — include:

- **The literal-value-in-component-CSS pattern.** Components hard-code values the token system should supply. The pattern is visible at a glance once the auditor knows to look; finding it earlier in each subsequent engagement compounds the auditor's diagnostic speed.
- **The semantic-tier-skip pattern.** Components consume primitive tokens directly, bypassing the semantic layer. The visible symptom is brittle theming; the architectural cause is the absent semantic tier; the fix is a redesign of the token-tier consumption discipline.
- **The "we have a token system but components don't use it" pattern.** Tokens exist in Figma, exist in Style Dictionary output, and don't show up in production CSS because the dev team built parallel implementations. The audit's evidence is a build-time scan against the token catalogue; the gap is governance, not architecture.
- **The forked-component pattern.** Product teams forked the system's component because the API didn't accept their use case; the system team didn't accept the contribution; the fork now drifts. The pattern is the canonical contribution-model failure mode.
- **The "every team claims to use the system, the build scan disagrees" pattern.** Adoption claims are based on intent or self-report; actual usage is much lower. Visible in coverage scans against build artefacts.
- **The composite-typography-token-flattening pattern.** The system designed composite typography tokens; the build pipeline collapsed them to resolved values per platform; per-platform fidelity has degraded. Visible in cross-platform spot checks.
- **The contrast-pair-decay pattern.** The system documents WCAG contrast pairs at one theme; theming changes shipped without re-validating the contrast pairs; some pairs now fail. Visible in automated scans across every theming dimension.
- **The component-v1-API-still-shipping pattern.** The component's API shifted across versions; consumers still pin to v1; the v3 API improvements aren't reaching production. Visible in version-distribution scans.

These patterns recur across systems built by different teams, against different consumers, in different industries. The senior auditor's method is partly the methodology and partly the *pattern catalogue* — the accumulated recognition that lets the auditor look at a system for an hour and predict, with reasonable accuracy, which of these patterns the audit will surface. The pattern catalogue is the practice's compounding intellectual asset; it is also a source of audit-finding bias the auditor has to manage (a practitioner who sees the same patterns across engagements may pattern-match without verification, which produces findings that aren't backed by the specific system's evidence). The discipline is to use the pattern catalogue as a *hypothesis generator* — what to look for first — not as a finding shortcut.

UX audits don't compound the same way because UX failure modes are domain-specific. The checkout-abandonment failure mode in e-commerce doesn't generalise to the form-completion failure mode in fintech onboarding doesn't generalise to the navigation failure mode in publishing. The UX practitioner's expertise compounds, but each audit's findings remain particular. DS audit findings transfer because the underlying architecture is constant: every system has tokens, components, governance, adoption — the lanes are the same; the failure modes are the same; the diagnostic methodology is the same.

### The audit's authority surface

The audit's findings have to defend themselves against three audiences with three different standards.

**The client engineering lead** — who built the system, knows the codebase, has lived with the architectural decisions, and is professionally invested in their correctness. Findings against this audience need to be *evidentially specific*: file paths, line numbers, build-time scan output, specific commit SHAs. The auditor cannot say "the token system is inconsistent"; the auditor has to say "the token at `components/button/background.brand` resolves to `#0066CC` in the Figma library and `#0070D2` in the Style Dictionary output; the discrepancy traces to commit a3f2c1b in the design-tool round-trip." The evidence wins the argument; vague findings lose to the engineering lead's specific knowledge.

**The client design lead** — who designed the system or inherited it, understands the design intent, and is professionally invested in the system's craft. Findings against this audience need to be *framed against intent*: not "the typography scale is wrong" but "the typography scale you stated as the intent in the foundational design document is implemented inconsistently here, here, and here, with these consequences for readers." The auditor has to read the system's stated intent (which may live in a design document, a Notion page, a Slack thread, or only in the design lead's head) and frame findings as gaps between stated intent and implementation, not as the auditor's preferences against the design lead's choices. Findings that read as taste lose to the design lead's authority over taste; findings that read as intent-vs-implementation hold.

**The executive** — who is paying for the audit, has a commercial stake in the system, and is reading the report through a "what should I do about this" lens. Findings against this audience need to be *commercially framed*: not "token-tier consolidation is recommended" but "the architectural change that prevents the next rebrand from costing six months of redesign." The audit's findings have to translate into language the executive uses; the translation is the audit's commercial value. Findings that read as engineering detail lose the executive's attention; findings that read as commercial consequence hold it.

The audit's authority is not single-sourced. Methodology authority (the audit followed a stated method) anchors against the engineering lead's specifics. Evidential authority (each finding cites specific instances) defends against the design lead's intent. Commercial authority (each finding has its commercial framing) reaches the executive. The senior auditor's report carries all three; the apprentice auditor's report carries one or two and gets pushed back in proportion.

---

## 2. Audit methodology — the eight audit lanes

The DS audit examines eight surfaces, each with its own methodology, evidence types, scoring rubric, and reporting shape. A comprehensive audit covers all eight; a focused audit names which lanes are in scope and which aren't, with the reasoning for each scope decision. The lanes interact — a finding in one lane is often the symptom of a cause in another — and the audit's diagnostic value lives in reading across lanes as much as in any single lane's depth.

### 2.1 Token audit

The token audit reads the system's token tree as architecture. The methodology examines:

**Tier coverage.** The token tree's structure — primitive layer (raw values, the alphabet), semantic layer (role-named aliases, the words), component layer (component-specific composites, the sentences). Audits the tier separation: are all three present, or is the system collapsed (no semantic tier; no component tier; primitives consumed directly by components)? Audits the tier discipline: do components consume semantics, or do they reach for primitives? The discipline failure is the most common token-audit finding.

**Alias resolution health.** The chain from semantic to primitive — `button.background` → `color.brand.primary` → `color.blue.500` → `#0066CC`. Audits the chain's depth (deep chains are fragile; flat chains lose abstraction); audits the chain's integrity (broken aliases that resolve to undefined; circular aliases; aliases pointing to deprecated tokens that still exist for backward compatibility); audits the chain's *consistency* across themes (the alias chain should be stable across light/dark; the values change, the structure doesn't).

**Multi-mode and multi-collection architecture.** Per 24's tokens-at-scale framing — when does the system use multi-mode (one collection, multiple modes per token) vs. multi-collection (separate collections per dimension) for theming axes? Audits the architecture: the brand axis especially deserves multi-collection treatment; mode (light/dark) is the canonical multi-mode use case; density and contrast preference are typically multi-mode; mixing multi-mode-for-brand at portfolio scale is an architectural failure mode the audit should flag.

**Theming dimension orthogonality.** The system's theming dimensions — mode, density, brand, contrast preference, motion preference — should be orthogonal axes that compose independently. Audits whether the dimensions are actually independent or whether they have collapsed into a single "theme" axis. A common failure: brand and mode collapsed (one theme is "Brand A Light," another is "Brand B Dark"; the auditor can't independently switch brand without also switching mode). The audit surfaces the collapse; the recommendation is the dimensional split.

**Dead-token detection.** Tokens defined in the source-of-truth that no consumer references. Build-time scan of the codebase for token-name occurrences vs. the token catalogue produces the dead-token list. Audits the dead-token count (1–5% is normal hygiene; 10%+ is system-team-vs-consumer disconnect; 25%+ is a system that has accumulated tokens for hypothetical use). The dead-token list is also a deprecation candidate list; the audit's recommendation usually pairs the two.

**Literal-value-in-component-CSS detection.** Build-time scan of component CSS (or the equivalent in native platforms) for hex values, raw pixel values, or other literals the token system should supply. Audits the count, the distribution (which components, which value types), and the pattern (are the literals an oversight, or do they signal a token-tier gap?). The audit-finding language matters here — "literal values found" is a complaint; "the token tier is missing values these components need" is a diagnosis.

**Contrast-pair coverage and resolution.** Every WCAG-mandated contrast pair (text-on-background, large-text-on-background, non-text-UI-on-background, focus-indicator-on-background) audited across every theming dimension. Audits the coverage (is every pair tested) and the resolution (do the pairs pass at the threshold). A common failure: pairs validated at one theme only; theme variations ship without re-validation. The audit's evidence is a per-pair-per-theme matrix; the report includes the failures with severity per WCAG level.

**DTCG conformance status.** Per 22's token-architecture-extensions framing — does the token source conform to the DTCG Format Module (2025.10 as of mid-2026)? Audits the conformance: token types correctly declared, composite tokens use property-level-aliasing-via-`$ref` rather than `{alias}` notation, mode declarations conform, color-space declarations correct (`srgb`, `oklch`, `display-p3`, etc.). The DTCG conformance audit is a recent lane; pre-2024 systems often shipped pre-DTCG token shapes that need migration.

**Cross-platform output integrity.** Style Dictionary or equivalent build outputs to multiple platforms (web CSS, web JS, iOS Swift, Android Kotlin/XML, Compose, Flutter, RN). Audits that each platform receives a faithful representation: the alias structure preserved where the platform supports it, resolved values correct, naming conventions per-platform appropriate, missing or platform-specific tokens flagged. A common failure: the build silently flattens composite typography tokens on one platform and not another; cross-platform fidelity degrades without anyone noticing.

The token audit's tooling surface as of mid-2026: Style Dictionary's audit-surface support has grown (v4 and onward expose enough of the dependency graph to traverse programmatically; custom transforms and resolvers can produce the dead-token list and the literal-value scan). Tokens Studio's audit features (the Inspector and the design-tool-side audit views) cover the Figma-to-token-source seam. Knapsack and Supernova both ship token-audit views as part of their broader products. None of these unify the lane; the senior auditor assembles the picture from multiple tools plus custom scripts.

### 2.2 Component audit

The component audit reads components as APIs and contracts. The methodology examines:

**Coverage against the consumer's surface.** For each component in the system, the audit measures: how many products consume it, how many distinct screens or pages reference it, how many distinct teams have consumed it. The data comes from build-time scans against the consumer's codebase (web: ESTree-based scans for React component imports; native: source-text scans against component name patterns). The coverage matrix is the audit's most direct adoption signal — components with high count are the system's load-bearing pieces; components with zero count are dead code; components with bimodal counts (high in some products, zero in others) signal team-level adoption gaps.

**API consistency.** Across the component library, the audit reads the prop signatures for cross-component consistency. Props that share semantics across components (`size`, `tone`, `disabled`, `loading`, `variant`, `as`, `asChild`) should have consistent typing, consistent default values, and consistent behavioural contracts. The audit tabulates inconsistencies. A common failure: `size="small"` on Button and `size="sm"` on Input — same semantic, different naming, the cross-component composition surface fragments. The audit's evidence is a per-prop matrix across components; the report flags the inconsistencies with severity weighted by how many consumers depend on the inconsistent shape.

**Composition primitives.** The system's composition primitives — Slot, AsChild, render-prop, polymorphic `as` — are the surface that lets consumers extend components without forking them. The audit examines the primitive coverage (does the system ship a Slot pattern; do components support `asChild` polymorphism; what's the polymorphic-`as` surface) and the primitive consistency (do primitives behave identically across components). Systems without composition primitives produce forking; the audit's finding is "consumers fork because the primitive surface forces it," with the forking evidence from the adoption audit cross-referenced.

**State machine completeness.** Every component's variant matrix — focus, hover, active, disabled, error, loading, empty, selected, indeterminate — audited for completeness against the component's role. A button with no `loading` state is an obvious gap; a select with no `error` state is a gap; a component without a focus-visible state is an accessibility gap. The audit's evidence is the per-component state matrix; the report flags the missing states with severity weighted by the consumer's likely encounter rate.

**API drift.** The component's API across versions — v1 → v2 → v3 — audited for the drift's shape. Are the version transitions additive (new props added, old props deprecated with grace), breaking (props removed, semantics changed without migration), or chaotic (props added and removed without a clear discipline)? The drift pattern signals the contribution model's health — additive drift is mature, breaking drift signals weak governance, chaotic drift signals no governance.

**Polyfill detection.** Consumers wrapping components in their own wrappers because the API is missing a prop or behaviour. Build-time scan finds the wrapper components and pattern-matches against system component names; the wrappers are the polyfill evidence. Common polyfills: a "ProductButton" that's the system's Button plus the team's tracking instrumentation; a "FormField" that wraps the system's Input with the team's validation logic. The polyfills are not always failures — some are legitimate composition; some signal API gaps. The audit reads the polyfill catalogue and tags each as legitimate, gap-driven, or fork-precursor.

**Detached and out-of-system component detection.** In Figma, components that are detached from the library or built outside the library entirely. In code, components whose imports don't resolve to the system's package. Build-time scans on both surfaces produce the catalogue. The audit reads the catalogue for patterns: which teams produce the most out-of-system components, which surfaces accumulate them, which categories (form fields, navigation, data-density components) are most often re-implemented. The pattern points to the gap the system's coverage doesn't fill.

The component audit's tooling surface: Figma's API exposes the detached-instance count; Storybook's CSF + custom tooling can produce the per-component prop matrix; build-time scans require custom tooling against the consumer's codebase (the senior DS engineer typically builds these per-engagement, with the practice's scaffold accelerating each successive engagement). Visual-regression tooling (Chromatic, Percy, Playwright's snapshot mode) covers the state-completeness lane indirectly — uncovered states are unrendered, which surfaces in the regression suite's coverage report.

### 2.3 Accessibility audit

The accessibility lane has the most-published methodology of the eight. The W3C's WCAG-EM (Evaluation Methodology) is the canonical procedure for WCAG conformance audits; the ARIA Authoring Practices Guide is the canonical reference for composite-widget pattern conformance. The DS audit's accessibility lane uses WCAG-EM as its base methodology and extends it for system-specific concerns.

**WCAG 2.2 conformance per component.** As of WCAG 2.2 (October 2023, though uptake into procurement language continued through 2024–2025), each component is audited against the relevant success criteria — text alternatives, contrast (1.4.3, 1.4.6, 1.4.11), keyboard accessibility (2.1.1, 2.1.2), focus management (2.4.3, 2.4.7, 2.4.11, 2.4.12, 2.4.13 — the new 2.2 focus-appearance and target-size criteria), name-role-value (4.1.2). The audit produces a per-component-per-criterion conformance grid; the cells are PASS / FAIL / N/A / NEEDS REVIEW.

**The four-engine × four-AT test matrix.** Real assistive-technology testing across the canonical browser × AT pairs — Chrome + JAWS (Windows), Firefox + NVDA (Windows), Safari + VoiceOver (macOS / iOS), Chrome + TalkBack (Android). Plus, increasingly, Edge + Narrator (Windows), Firefox + Orca (Linux), and for keyboard-only users the standard browser/keyboard pair. The matrix is real testing, not automated scanning — the auditor walks each component in each AT and notes the user experience. The matrix is the highest-authority accessibility evidence and the most labour-intensive; sample audits cover the system's most-used components (the consumer-surface analysis from the adoption audit tells the auditor which components warrant the matrix coverage).

**ARIA 1.3 composite-widget pattern conformance.** For composite widgets (combobox, listbox, menu, menubar, tablist, tree, grid, treegrid, dialog, alertdialog), conformance against the W3C ARIA Authoring Practices Guide's pattern. The APG's patterns include the role assignments, the ARIA attributes, the keyboard interactions, and the focus management. The audit reads the system's implementation against the APG and flags divergences; the divergences are sometimes legitimate (the APG pattern doesn't fit the use case; the system has shipped a different but accessible pattern) and sometimes failures (the divergence breaks AT navigation). The audit cites the APG section for each finding.

**Focus-management discipline.** The system's focus-management contracts: focus-trap-on-modal, roving-tabindex on composite widgets, restore-focus-on-close, skip-to-content link, focus-visible vs. focus indicators, the focus-appearance criterion (WCAG 2.2 SC 2.4.13). The audit reads each focus-management surface and tests it; the evidence is per-surface, per-AT.

**Contrast pair coverage at every theming dimension.** Cross-references the token audit's contrast-pair findings into the accessibility lane. The audit confirms the token-side measurements with rendered-component testing; sometimes the token-level math passes but the rendered component fails because the component's stacking context introduces transparency (the focus indicator at WCAG 3:1 against the background passes the math; the focus indicator behind a translucent overlay drops below 3:1 against the apparent background).

**User-preference media-query support.** `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`, `forced-colors`, `prefers-reduced-data`. The audit reads each component's response to each media query; the most-commonly-failing is `prefers-reduced-motion` (motion-as-foundation maturity is recent; the system may not have a reduce-motion contract). `forced-colors` (Windows High Contrast Mode) is the most-overlooked; per 28's web-accessibility-implementation framing, components with custom colour schemes need explicit `forced-colors` handling or they break in HCM.

**EAA and Section 508 conformance.** For clients with regulatory exposure — European Accessibility Act (in force June 2025) for EU market entrants, Section 508 for US federal procurement, ADA Title III for US public-accommodation websites — the audit extends to the regulatory regime. The EAA imports WCAG 2.1 Level AA as its baseline; Section 508 imports WCAG 2.0 Level AA via the Revised 508 Standards (2018); ADA Title III is litigation-anchored but courts have settled on WCAG 2.0/2.1 AA as the working standard. The audit's regulatory section names the regime, the standard, the conformance status, and the remediation effort; this section is what client legal reads.

**The WCAG-passes-but-fails-real-users pattern.** Per 31 §The contrast surface — components that pass automated contrast checks against WCAG and fail real users. The pattern is most common in dark-mode implementations where the literal contrast math works but the perceptual contrast is inadequate. The audit's evidence here is real-user testing or the auditor's perceptual-contrast read (APCA Lc as the working measure); the recommendation is APCA-as-quality-bar with WCAG-as-floor.

The accessibility lane's tooling surface: axe-core (the canonical automated accessibility scanner; ships in axe DevTools, Pa11y, Storybook's a11y addon, Chromatic's a11y testing, and many CI integrations) covers the automated-checks portion. Pa11y wraps axe-core for CI use. Lighthouse includes a reduced axe-core ruleset. None of these substitute for real AT testing; the senior auditor's discipline is to use the automated tools for coverage and the AT testing for depth. The tooling gap as of mid-2026: no vendor ships unified four-engine × four-AT testing as a service; the practice runs the matrix manually or with VM-based remote desktop services (BrowserStack, Sauce Labs) for the cross-OS coverage.

### 2.4 Content audit

The content audit reads the system's content surface as a layer of the design system. The methodology examines:

**Voice-and-tone consistency.** The system's stated voice (typically captured in a brand guidelines document or a writing principles page) audited against the components' actual microcopy — error messages, empty states, helper text, button labels, tooltip content, form validation messages. The audit reads a sample of components and surfaces the voice drift. A common failure: the system's stated voice is "warm and approachable"; the error-message voice across components is variously curt, formal, apologetic, or neutral. The drift comes from per-component decisions made in isolation; the audit's recommendation is a centralised voice-and-tone matrix (Mailchimp's pattern is the field's reference).

**Error-message templates.** The system's error-message patterns — what errors say, how they're structured, how they handle the four error categories (validation errors, system errors, permission errors, integration errors). The audit reads the error catalogue across components; the evidence is the per-error-type matrix; the recommendation is template consolidation where the audit finds drift.

**Empty-state copy patterns.** Empty states appear across many components (lists, tables, search results, dashboards) and produce per-component drift if not centralised. The audit reads the empty-state catalogue and surfaces the inconsistency; the recommendation is the empty-state pattern library Linear and others have shipped.

**CTA verb taxonomy.** The verbs used on action buttons across the system. A senior content auditor catalogues the verbs and tabulates frequency: "Submit" vs. "Save" vs. "Send" vs. "Continue" vs. "Done" vs. "OK" — the same semantic role, multiple verbs, no apparent discipline. The audit's recommendation is a centralised verb taxonomy that maps semantic roles (form completion, multi-step navigation, irreversible action, modal dismissal) to specific verbs.

**Per-component microcopy guidance.** The system's per-component documentation (per 29's per-component-template framing) should include content guidance — what the component's text should sound like, what's appropriate placeholder content, what's not. The audit reads the documentation surface for content guidance presence; the gap is common.

**ICU MessageFormat / pluralisation / gendered-language conformance.** For systems shipping in i18n contexts, the audit examines whether the system's content surface is structured for localisation. ICU MessageFormat support in error messages and helper text; pluralisation handled (not "1 items" vs. "1 item"); gendered language handled where the locale demands it; RTL content ordering preserved. The audit's evidence is the localisation-readiness sample across components; per 13's i18n-and-RTL framing.

**Assistant tone for AI surfaces.** Per 25's AI-aware-patterns framing — the assistant's tone, refusal patterns, citation format, disclosure boilerplate. The audit reads the AI-surface content as a system layer; the evidence is the assistant's behaviour across canonical prompts; the recommendation is the assistant-tone guidelines if the gap is open.

The content audit's tooling surface as of mid-2026: limited. Acrolinx and Writer cover voice-and-tone validation against custom rules but require investment in rule-set authoring. Hemingway and Grammarly Business cover prose readability but don't model the system's specific voice. The senior content auditor mostly runs the lane manually, with sample-based reading; the practice's leverage is the audit's *checklist* (the centralised voice-and-tone matrix, the empty-state pattern, the verb taxonomy) which the practice ships as the audit's recommendation deliverable.

### 2.5 Motion audit

Motion-as-foundation maturity is recent (per 18-21's motion-foundations-and-implementation framing); systems built before 2022–2023 often don't have a motion lane to audit. When the lane exists, the audit examines:

**Three-tier motion token coverage.** Duration tokens (instant, fast, normal, slow, deliberate); easing tokens (linear, ease-out, ease-in-out, the spring family); composed motion tokens (the "fade-in," "slide-up," "scale-in" composites that consume duration + easing + property bindings). Audits the tier coverage; many systems ship duration and easing without composing them, leaving the consumer to compose per-instance.

**Choreography vocabulary.** The system's named motion patterns — entry (component appears), exit (component disappears), transition (component shifts state), attention (component requests user's attention). Audits whether the vocabulary exists and whether components use it consistently. A common failure: each component invents its own motion behaviour because the choreography vocabulary is absent.

**Reduce-motion contract.** `prefers-reduced-motion: reduce` handling across the system. Audits whether components respect the preference and whether the reduced-motion fallback is acceptable (some systems implement reduce-motion as motion-removal, which can break the user's understanding of state changes; the discipline is to reduce duration and amplitude rather than remove motion entirely).

**Performance budget.** INP-respecting motion (animations don't block input handling); compositor-only animations (transform and opacity, not layout-triggering properties); the 200ms INP threshold for "good" Core Web Vitals. Audits the performance budget against the system's motion implementations; the evidence is performance profiling against canonical interactions.

**Cross-platform spring-parameter mapping.** For systems shipping mobile, the audit examines how spring parameters map across platforms (web's `linear()` springs, iOS's spring API, Compose's `spring()`, Flutter's `SpringDescription`, RN's Animated.spring). The mapping is non-trivial because the underlying physics models differ; per 19/20's motion-implementation framing.

The motion audit's tooling surface: Framer Motion's tools cover the web side; the native platforms each have their own profiling tools; cross-platform unified motion tooling doesn't exist. The senior motion auditor reads the implementations and runs the platforms manually.

### 2.6 Code audit

The code audit reads the system's repository as software. The methodology examines:

**Build pipeline health.** The system's build — token build (Style Dictionary or equivalent), component build (Vite, Rollup, esbuild, or equivalent), docs build (Storybook, the docs platform), package publish (npm, internal registry). The audit reads each stage for correctness, performance, and reliability. A common failure: the build succeeds but produces stale output because a cache layer isn't invalidating; the consumers download a published package whose content diverges from the source.

**CI quality gates.** The system's CI pipeline — what runs on PR, what runs on main, what runs on release. The audit examines the gates: visual-regression (Chromatic / Percy / Playwright), automated accessibility (axe-core / Pa11y), unit tests, type-checking (TypeScript), linting (ESLint / Stylelint), build verification, semantic-version automation. The audit reads each gate for presence, configuration, and signal-to-noise ratio (gates that produce too many false positives get ignored; gates that produce false negatives let regressions through).

**Test coverage at the component level.** Per-component unit-test coverage, integration-test coverage, visual-regression coverage, accessibility-test coverage. The audit produces the per-component coverage matrix; the gaps are the components most likely to ship regressions.

**Semantic-version automation.** The system's release pipeline — does the version bump correspond to the change's nature (semver-as-contract: patch for fixes, minor for additive, major for breaking)? Audits the version history against the changelog; the failure mode is version-bump-by-vibe (every release is a minor; major bumps are rare; the version doesn't encode the breaking-change signal consumers need).

**Docs platform freshness.** Per 29/30's documentation framing — does the docs surface stay current with the source, or does it drift? The audit reads the docs surface for freshness signals (last-updated dates, broken links, examples that no longer compile, screenshots that no longer match the component). The drift is the leading indicator of the docs-vs-source discipline.

**Package publish surface.** What gets published, how, when, with what stability guarantee. The audit reads the package's published shape (exported APIs, types, peer dependencies, side effects, tree-shaking compatibility) for consumer-facing correctness.

**Component implementation against design source.** The implementation faithfulness — the design specifies a 12px gap, the implementation ships an 8px gap; the design specifies a focus indicator with these colours, the implementation ships those colours. Per 12's Figma-practice framing for the design-to-code seam. The audit's evidence is per-component side-by-side comparison.

**Framework-specific integration health.** For systems shipping cross-framework (React + Vue, or React + Web Components, or React + native mobile bindings), the audit examines whether each framework integration receives faithful component shape. Common failure: the React integration is the source-of-truth and the secondary framework integrations lag in completeness.

The code audit's tooling surface: GitHub's Actions surface plus the visual-regression tools (Chromatic, Percy) plus axe-core in CI plus the language-specific test runners (Jest, Vitest, Playwright). Coverage tooling (Istanbul, c8) for the unit-test lane. The senior DS engineer reads the CI configuration and the build pipeline; tooling automates the evidence collection.

### 2.7 Governance audit

The governance audit reads the system's contribution-and-governance protocol. The methodology examines:

**Contribution-model operation.** Per 07's governance framing — request triage, SLAs, review-and-merge cadence, contribution-vs-participation distinction (Curtis), the contribution scale (Fix → New Catalog). The audit reads the contribution-model artefacts (the contribution guide, the request template, the review checklist) and the operational data (the velocity metrics, the SLA adherence, the contributor distribution). A common failure: the contribution guide is well-written and the operational data shows nobody contributes; the model exists on paper but doesn't operate. The audit's evidence is the per-quarter contribution velocity and the contributor distribution; the recommendation reads the gap between model and operation.

**Contributor distribution.** Who contributes — the system team, designated ambassadors at consuming product teams, ad-hoc contributors, or only the system team. The audit tabulates contributors by source over the last four quarters; the distribution signals the contribution model's reach. A 90%-system-team distribution signals federation isn't happening; a 50%-system / 50%-product-teams distribution signals healthy hybrid contribution; a 20%-system / 80%-product-teams distribution may signal under-reviewed contribution that's at risk of system-team-as-bottleneck or system-as-anything-goes.

**Contribution-vs-participation distinction.** Curtis is precise: contributions are tangible, useful, federated, released; everything else is participation. The audit reads the system's claims of contribution against the strict definition; common failure is over-claiming participation as contribution. The audit's recommendation is the strict-definition adoption as a measurement discipline.

**Deprecation discipline.** The system's deprecation discipline — does deprecation actually happen, on what timeline, with what consumer-migration support? Audits the deprecation history (have items been deprecated; how many; on what timeline) and the active deprecations (what's currently deprecated; what's the migration path; what's the removal date). A common failure: deprecation announcements without removal — items deprecated three years ago that still ship.

**Major-release cadence.** How often the system ships major releases; what's in the major; how the major is communicated to consumers. The audit reads the version history and the release notes for cadence and quality. Healthy systems ship major releases every 12–24 months with clear migration paths; struggling systems either never ship majors (every change is minor or patch) or ship majors chaotically without migration support.

**Governance bodies' meeting cadence and decision quality.** If the system has formal governance bodies (a steering committee, a contribution review board, an ambassadors group), the audit reads their meeting cadence (do they meet on schedule), their decision artefacts (do meetings produce written decisions), and their decision quality (do the decisions get implemented). The audit's interview surface includes the governance bodies' chairs.

**Executive-coalition surface.** Who at the client sponsors the system, what they've committed to, when they last engaged. The audit's evidence is the stakeholder map plus the most-recent executive readout. A weakening coalition is a leading indicator of system-budget-cut and engagement-extension-rejection; the audit surfaces the signal early.

The governance audit's tooling surface: limited automation. The audit is interview-led plus document-review (the contribution guide, the meeting notes, the release notes). Backlight, Knapsack, and similar platforms ship limited contribution-tracking surfaces. The senior auditor's evidence is mostly conversational.

### 2.8 Adoption audit

The adoption audit reads the system's actual consumption. The methodology examines:

**Coverage definition and measurement.** Per 07 §The coverage definition — three industry definitions exist (Morningstar's % of pages applying system components; Veriff's components-in-use across all repos; didoo's proportion-sourced-from-system). The audit names which definition is in use, measures against it, and reports the result. A typical Coverage Number: 40–70% for mature in-house systems; 20–50% for agency-built systems past handoff; below 20% signals the system isn't being adopted. The number alone is incomplete; the trend matters more (is coverage growing, plateaued, or declining).

**Per-team adoption rate.** The coverage number disaggregated by consuming product team. The disaggregation surfaces the bimodal pattern — Team A is at 80% coverage, Team B is at 15%. The pattern signals either team-level resistance (Team B doesn't believe in the system) or team-level support absence (Team B can't get help when they try to adopt). The audit's recommendation depends on the cause; the interviews differentiate.

**Per-component usage distribution.** The coverage number disaggregated by component. The distribution is almost always long-tailed — a small number of components account for the majority of usage (Button, Input, Card, the navigation primitives); a long tail of components has minimal usage. The long tail isn't necessarily a failure (some components are inherently low-frequency — a multi-step wizard, a complex data-table); the audit reads the long tail for components that *should* be used more (the recommendation is awareness or adoption support) and components that *shouldn't* exist (the recommendation is deprecation).

**Detached and forked component count.** Cross-references the component audit's detached/forked findings into the adoption lane. The forking pattern is a leading indicator of system-team-vs-consumer disconnect; the audit's adoption section frames the count commercially (each fork is a per-team duplication of the system's work; the cumulative cost across teams is the system's failed-leverage cost).

**The "we use the system" claim vs. the build-time scan reality.** Most clients' self-reported adoption is significantly higher than the build-time scan reveals. The audit measures both — the interview-collected self-report and the build-time scan reality — and reports the gap. The gap is the adoption audit's most useful single finding; it surfaces the perception gap that prevents the system team from getting the resources it needs (the executive thinks the system is succeeding because the team is reporting success; the actual build artefacts show otherwise).

The adoption audit's tooling surface: build-time scans require custom tooling against the consumer's codebase. The senior DS engineer typically writes these per-engagement; the practice's leverage is the scaffold that makes each successive engagement faster. Knapsack, Supernova, and Backlight ship adoption-measurement features with varying coverage; none are unified.

### How the eight lanes interact

The audit's diagnostic value lives in the cross-lane reading. A worked example.

The token audit surfaces a primitive `color.blue.500` consumed directly by `Button` (skipping the semantic tier). The component audit confirms the API drift — `Button` has accumulated a `tone` prop that takes literal colour values instead of semantic role names. The adoption audit shows the product team has forked `Button` because the API drift made it impossible to support their brand variant cleanly. The governance audit shows the contribution model rejected the product team's contribution that would have closed the API gap, because the system team felt the contribution didn't fit the system's intent.

Each individual finding is a partial diagnosis. The architectural read is: the system's token-tier discipline lapsed (token audit), the lapse propagated into the component API (component audit), the consumer's response to the broken API was to fork (adoption audit), and the contribution model's rejection of the consumer's solution sealed the fork's permanence (governance audit). The recommendation isn't "fix the token tier" or "redesign the Button API" or "accept the contribution"; the recommendation is the architectural restoration that addresses all four lanes simultaneously, with the sequencing that makes the restoration possible (re-establish the token tier first; redesign the API against the semantic tier; communicate the redesign as a deprecation of the literal-value API; reopen the contribution conversation with a clearer protocol).

Audits that read lane-by-lane and report lane-by-lane miss the architectural diagnosis. Audits that read across lanes and report architectural patterns produce the diagnostic value the senior auditor's experience earns. The practice's report template (per §4) reserves the cross-lane patterns section as a distinct part of the report for exactly this reason.

### Heuristic vs. specification vs. census auditing

Three audit modes operate at different cost-and-authority points; real audits blend them per lane.

**Heuristic auditing.** A senior practitioner walks a sample of surfaces and reads against their accumulated pattern catalogue. Fast (a senior practitioner can heuristic-audit a system's component library in a day), deep on the patterns the practitioner recognises, blind to what they don't. The authority is the practitioner's reputation and demonstrated method. Best for: the first pass of an audit, where the goal is hypothesis generation; the lanes where the failure modes are well-catalogued (component audit, content audit); the senior-practitioner read of the system's overall architectural shape.

**Specification auditing.** Spec-checking every (or every-in-scope) surface against a stated rule set. Slower (specification-auditing a token tree at scale takes days); exhaustive within scope; generates a defensible artefact. The authority is the rule set itself. Best for: WCAG conformance audits (the rule set is the W3C standard); DTCG conformance audits (the rule set is the spec); contribution-model audits against a stated protocol (the rule set is the system's own contribution guide).

**Census auditing.** Scanning every consumer at the build-time level. Only feasible with tooling; expensive to set up (custom tooling against the consumer's codebase); the highest-authority output (it's not a sample, it's the truth). Best for: adoption-coverage measurement; literal-value-in-component-CSS detection; dead-token detection; per-component usage distribution.

The audit's methodology statement names which mode is in use per lane. A typical mid-2026 mid-engagement audit blends: heuristic for the component library's first pass + content + governance + executive-stakeholder readings; specification for accessibility (WCAG) + DTCG token conformance + ARIA APG composite-widget patterns; census for token-coverage + component-coverage + dead-tokens + literal-value detection. The blend is what produces both the architectural diagnosis (heuristic lays the hypothesis; specification anchors the conformance findings) and the defensible evidence (census produces the numbers the executive's procurement function can verify).

---

## 3. Audit-as-deliverable — the productised audit engagement

The senior agency practitioner runs audits inside Discovery routinely. The practice's productised audit — a standalone, sellable engagement with a defined shape and price — is a different artefact, and the field's strongest entry-point opportunity for any agency that wants to lead on DS work.

### The commercial rationale

Three properties make the productised audit a uniquely strong commercial offering.

**Audits are the highest-asked-for entry-point engagement.** Clients with mature-enough internal product organisations to have a system in production know they need outside diagnosis. They can articulate the request ("we want an audit of our design system") more easily than they can articulate the request for a multi-month redesign engagement. The procurement weight of an audit (small, time-boxed, defined deliverable) is dramatically lower than the procurement weight of a multi-month engagement; the audit can be authorised at a vice-president's discretion in many organisations, where a six-month engagement requires C-level approval.

**The audit produces the diagnostic that justifies the next engagement.** A well-shaped audit's recommendations include the next engagement's scope. The audit names the architectural work the system needs; the recommendations propose how that work gets done; the executive readout introduces the practice as the natural partner for the recommended work. The conversion rate from audit-engagement to follow-on engagement, when the audit is well-shaped and the follow-on is well-pitched, runs substantially higher than the conversion rate from cold-start RFP. Specific numbers vary by agency and by industry; agencies that run productised audits as part of their pipeline strategy commonly report 40–60% of audits converting to follow-on within 6–12 months.

**In-house teams cannot self-audit credibly.** The team that authored the system has the most detailed knowledge of its construction and the worst position to read it as a whole. The senior in-house practitioner can audit components and tokens; they cannot audit the system's *architectural premises* against a frame outside the team's own. The agency auditor's outside-frame is the audit's distinctive value; the in-house equivalent would require hiring a senior outside practitioner to audit, which is what an agency engagement is. The audit is a service the agency uniquely supplies.

The under-investment is structural. Most agency DS practices are organised around delivery work (the engagement that builds, runs, hands off the system). The audit's productisation requires investment that doesn't directly serve any single engagement: the methodology authoring, the report template, the build-time scan tooling scaffold, the senior-practitioner training in the audit's shape. The investment is small (40–80 hours of senior time to author the productised methodology; another 40–80 hours per engagement to run the audit) but the practice has to authorise it as a sales investment, not as billable engagement work.

### The pre-engagement — what the audit needs to know before it starts

A useful audit begins before the audit's first day. The pre-audit half-day to one-day sets the audit's scope and prevents the first day from being consumed by orientation.

**The system's surface.** Web only / web + native / web + native + multi-brand / multi-platform with custom integrations. The surface determines which lanes are in scope, how deep each lane goes, and which specialists the audit team needs. A web-only single-brand system needs a 3-person team for 5 days; a multi-platform multi-brand system needs a 5-person team for 10 days.

**The system's age and maturity.** Greenfield (under one year, in active foundation work) / 1–3 years (growing — has consumers, has shipped multiple versions, faces the first round of hard governance questions) / 5+ years (evolving — has accumulated technical debt, faces deprecation pressure, has competing successor systems). The age shapes the audit's expectations and the maturity diagnostic's framing (per §6).

**The system's authoring tools.** Figma + Tokens Studio + Style Dictionary is the canonical 2026 stack; deviations from it (Sketch + a custom token pipeline; Figma + a custom build with no Tokens Studio; an internally-developed authoring tool) shape what the audit can scan and what manual reading the audit demands.

**The team that maintains it.** Allocated individual / dedicated team / federated. The team's shape determines who the auditor interviews and which lane's evidence is most accessible. A federated system's governance audit is the audit's hardest lane (multiple teams, multiple decision points, distributed evidence); an allocated-individual system's governance lane is brief but the burnout-and-bus-factor finding is often the audit's headline.

**The stakeholder surface.** One product team / multi-product / enterprise. The stakeholder count shapes the interview surface and the executive readout.

**The executive surface.** Who funded the audit, what's at stake politically, what the audit is being measured against. The audit's commercial framing depends on the executive's frame; an audit funded against a "we're considering replacing the system" frame is shaped differently than an audit funded against a "we want to scale the system to a new acquisition" frame. The pre-audit discovery includes a 30-minute conversation with the executive sponsor; without it, the audit's executive readout is vibes-based.

### The day-by-day shape of a 5-day audit engagement

The 5-day shape is the canonical productised offering. Variants for 3-day (greenfield, single-platform, single-brand) and 10-day (enterprise, multi-platform, multi-brand) extend the shape proportionally.

**Day 1 — Orientation and stakeholder interviews.**

- Morning: kick-off with the client team (60 minutes); access provisioning (Figma access, codebase access, build-pipeline access, analytics access); pre-scan setup (the build-time scan tooling deployed against the codebase; results begin streaming in by mid-day).
- Afternoon: 3–6 stakeholder interviews at 30–45 minutes each. The interview list typically includes: the client DS lead (the system's primary author or maintainer); 1–2 product team designers and 1–2 product team engineers (the consumers); the executive sponsor (the funder); a recent contributor from outside the system team (the federation signal); the most-recent escalation contact (where the system most recently failed or was contested).

**Day 2 — Token-and-foundation audit; component sample audit.**

- Morning: token audit. The dependency-graph traversal, the dead-token scan, the literal-value scan, the contrast-pair coverage matrix, the DTCG conformance read, the cross-platform output integrity check. Heuristic + specification + census blend. Evidence collected: the token-audit findings document.
- Afternoon: component sample audit. 15–25 components depending on system size. The selection biases toward: the most-consumed components (per the adoption audit's coverage data, which by mid-day is partially available), the most-recently-shipped components (the system's current direction signal), the most-contested components (the recent escalation contact's references), and 2–3 random components (anti-bias). Per-component: API consistency, state-completeness, polyfill detection, design-source-faithfulness. Evidence: the per-component-audit findings document.

**Day 3 — Accessibility and content audit; code audit; governance interviews.**

- Morning: accessibility audit. The WCAG conformance grid for the sampled components; the four-engine × four-AT testing for the most-consumed components (typically 5–10); the ARIA APG conformance read for composite widgets; the focus-management testing; the user-preference media-query testing. Evidence: the per-component accessibility findings.
- Afternoon, first half: content audit. Voice-and-tone reading across the sampled components; the error-message catalogue; the empty-state catalogue; the verb-taxonomy survey; the i18n-readiness sample. Evidence: the content-audit findings.
- Afternoon, second half: code audit (where in scope) — build pipeline, CI gates, test coverage, semantic-version pattern, docs freshness; governance interviews — the contribution-model lead, the deprecation lead, the governance-body chair.

**Day 4 — Adoption audit and cross-lane synthesis; reporting draft.**

- Morning: adoption audit. The build-time scan results matured (the scan completes overnight typically); the per-team adoption rate disaggregation; the per-component usage distribution; the detached/forked count; the self-report-vs-reality gap analysis from the stakeholder interviews. Evidence: the adoption-audit findings.
- Afternoon: cross-lane synthesis. The senior auditor reads across all eight lanes' evidence and identifies the architectural patterns. The patterns become the audit's headline diagnostic. The reporting draft begins — executive summary first (the headline diagnostic and the top 5–10 findings); per-lane findings second (the lane-organised evidence); cross-lane patterns third; recommendations fourth.

**Day 5 — Report finalisation and the executive readout.**

- Morning: report finalisation. The full report (the per-lane sections completed; the appendix with raw evidence assembled; the methodology statement); the executive summary (10–20 pages); the audit dashboard or scorecard (single-page).
- Afternoon: the executive readout (60–90 minutes). The audit lead presents the headline diagnostic, walks through the top 5–10 findings with their commercial framing, and proposes the recommended next steps. Q&A, then the engagement formally ends.

The 5-day shape is intense; senior auditors run two to three of these in a quarter and treat each as a substantial sustained-attention engagement. The engagement model that works pairs senior auditors with mid-level practitioners on the audit team — the senior owns the synthesis and the readout; the mid-level owns the evidence collection and the per-lane findings; the lane-by-lane work parallelises across the team while the senior moves through stakeholder interviews and pattern reading.

### The team mix and roles

The 5-day audit's typical team mix is three to four people; the 10-day enterprise audit extends to five.

- **DS lead / audit lead.** Drives the engagement, runs the stakeholder interviews, owns the cross-lane synthesis, presents the executive readout. The senior practitioner with the deepest pattern catalogue. The lead's billable rate is the audit's largest single line item; the practice has to staff this role with the most senior available practitioner.
- **Senior DS designer.** Owns the design-side lanes — token audit (with the engineer's tooling support), component audit, accessibility audit's design-side (ARIA semantics, focus indicators, contrast at the component level), content audit, motion audit's design-side. Two-thirds the lead's billable rate but the larger share of the lane-evidence-collection work.
- **Senior DS engineer.** Owns the engineering-side lanes — code audit, build pipeline, CI gates, accessibility audit's implementation-side (real AT testing infrastructure, automated scanning), the build-time scan tooling deployment. The engineer's tooling work is what makes the census-audit lanes possible inside the engagement's time budget.
- **Design technologist (where staffed).** The cross-tooling sweep — Tokens Studio audit surface, Storybook health, Code Connect coverage, Figma Variables conformance, the design-tool-to-code seam audit. Most useful on engagements where the tooling stack is non-canonical or where the seam is the audit's likely failure point.
- **Senior accessibility specialist (fractional, where the regulatory exposure demands it).** Augments the a11y lane for regulated-industry audits — financial services under EAA exposure, US federal procurement under Section 508, healthcare under ADA Title III. Day 3 mostly; the report's regulatory section.

### The audit's deliverable surface

Three artefacts, each with a distinct audience.

**The full audit report (50–200 pages).** The complete document. Lane-by-lane methodology statements; per-lane findings with severity, evidence, and recommendations; the cross-lane patterns section; the recommendations section organised in three priority bands; the appendix with raw evidence (token-audit output, component-by-component findings, per-page coverage scan, interview log). The full report's audience is the practitioner — the client DS lead and the senior practitioners who will execute against the recommendations. The report is a working document; it survives the engagement as the reference for the system's next year of work.

**The executive summary (10–20 pages).** The audit's headline diagnostic in two paragraphs and a list. The top 5–10 findings with their commercial framing — each finding answers "so what?" in language the executive uses. The recommended next steps, in three priority bands (now / next / later). The executive summary's audience is the executive sponsor; the practitioner reads it as the report's introduction. The summary is what travels in slide decks, in Slack threads, in the client's executive readouts. Most executives read only the summary; the audit's commercial framing has to land here.

**The audit dashboard or scorecard (single-page).** The per-lane health score (a structured rubric: each lane scored 1–5 against a stated rubric; the aggregate score is the system's overall health number); the per-finding severity (Critical / High / Medium / Low counts); the headline recommendations ranked. The dashboard's audience is everyone — the executive who wants the at-a-glance number, the practitioner who wants the priority signal, the next-engagement scoping conversation that needs the artefact to point at. The dashboard is the artefact that travels to LinkedIn posts, to conference talks, to the agency's case-study library.

The three artefacts are companion-pieces. The senior auditor authors the executive summary and the dashboard; the rest of the audit team contributes the per-lane sections of the full report. The artefacts ship in the same package; the executive readout walks through the dashboard, hits the top findings from the executive summary, and points to the full report for depth.

### Pricing and commercial range

As of mid-2026, agency-scale productised audit engagements price in the range:

- **3-day audit (greenfield, single-platform, single-brand).** $25k–$45k. Limited scope; team of two; deliverable is the executive summary and the dashboard plus a focused report (15–40 pages).
- **5-day audit (canonical mid-engagement shape).** $50k–$80k. Full scope; team of three; full deliverable surface.
- **10-day audit (enterprise, multi-platform, multi-brand).** $90k–$150k. Extended scope across all lanes; team of four to five; full deliverable surface plus per-platform-and-per-brand sections.

The pricing varies materially by agency tier and by region. Top-tier agencies in major markets (London, New York, San Francisco, Tokyo) price at the upper end; regional agencies and emerging-market practices price at the lower end. The pricing signal that matters more than absolute level is the audit's *position relative to follow-on engagement size* — an audit priced at 5–15% of the expected follow-on engagement is in the right ratio. Lower than that, and the audit doesn't recover its sales-investment cost; higher than that, and the audit becomes a barrier to the follow-on.

The commercial discipline at sale: the audit is sold *with* a clearly named follow-on path. The pitch isn't "audit, then we'll see"; the pitch is "audit (here's the shape and the deliverable), and based on the audit's findings, the recommended next engagement is in this range and shape." The conditional nature is honest (the audit's findings might recommend a smaller follow-on, or no follow-on); the named pathway is what makes the audit's commercial logic work.

---

## 4. Audit reporting templates and the buy-in surface

The audit report is the engagement's lasting artefact. The senior practitioner can hand-write a strong report once; the practice's productised audit needs a *template* that holds the shape across engagements without anchoring on the senior's voice. The template is the practice's intellectual asset; each engagement's report is a particularisation of it.

### The report template

The template's elements, in order:

**Executive summary (10–20 pages).** Opens the report. The audit's headline diagnostic in two paragraphs — what the audit found at the architectural level. The top 5–10 findings with their commercial framing. The recommended next steps in three priority bands. The summary is self-contained — an executive who reads only the summary should land on the audit's full diagnostic and recommendations.

**Methodology statement.** What the audit examined (per-lane scope), what evidence was collected, what wasn't examined and why, what assumptions the audit makes about the system's surface and consumer base. The methodology statement is the audit's authority anchor against the engineering lead's specifics; it should read as professional and verifiable. A common failure: methodology statements written as defensive boilerplate (full of caveats and limitations); the discipline is to write methodology statements that read as confidence-grounded specificity.

**Per-lane findings.** For each lane in scope:

- A one-paragraph health summary (the lane's overall state).
- The lane's health score (a structured rubric — see below).
- The top findings (each finding has a title, a description, an evidence section citing specific instances, a severity, an estimated effort to remediate, a recommended owner).

The per-lane structure is consistent across lanes; the consistency is what makes the report navigable. A reader looking for "what did the audit find about adoption" should be able to flip to the adoption section and find the same structure they found in the token section.

**Cross-lane patterns.** The audit's diagnostic value lives here. Findings that are visible only across lanes; the architectural failure modes that compound across multiple lanes; the patterns the practice recognises from prior engagements. Each cross-lane pattern has a title (the architectural diagnosis), the constituent findings (which per-lane findings combine to surface it), the consequence (what happens if the pattern persists), and the recommendation (what the architectural restoration looks like).

**Recommendations.** The audit's "now / next / later" framing. Each recommendation has:

- A defined scope (what the recommended work covers).
- A recommended team mix (who does the work).
- A rough effort estimate (in weeks or months).
- A commercial framing (why this matters in the executive's language).
- A named relationship to the findings (which findings the recommendation addresses).

The recommendations section is the bridge to the next engagement; the recommendations' phrasing is what holds the bridge.

**Appendix.** Methodology details (the rubric per lane); the raw evidence (component-by-component findings, token audit output, the per-page coverage scan); the interview log (who was talked to, when, what surfaced). The appendix's audience is the practitioner who will execute against the recommendations; the depth here is what makes the report a reference document beyond the engagement's end.

### The severity model

Most audits use a four-tier severity (Critical / High / Medium / Low). The practice's discipline is to commit to one rubric, state it in the methodology section, and apply it consistently across findings.

- **Critical.** Blocks release, blocks accessibility conformance, blocks brand integrity, blocks regulated-industry compliance. Critical findings have to be addressed before the next major release; in regulated-industry contexts, before the next deployment.
- **High.** Significant consumer-visible issue, governance failure, or architectural decision that will break under the next major change. High findings should be addressed in the current quarter; deferring them creates compounding risk.
- **Medium.** Quality concern, drift, or failure mode that will compound over time. Medium findings should be addressed in the current half-year; the architectural cost of deferring is real but bounded.
- **Low.** Minor inconsistency, naming issue, polish item. Low findings can be addressed opportunistically; the architectural cost is small.

The discipline that produces credible severity grades is to *state the rubric explicitly* in the methodology statement and to *test each finding against the rubric* before assigning the severity. The most common failure is severity-grade inflation — every finding gets graded High or Critical because the auditor wants to convey urgency. Inflation costs the report its authority; an executive looking at 47 Critical findings concludes either that the system is irreparable or that the auditor is exaggerating, and either conclusion damages the engagement.

A useful discipline: target a roughly bell-shaped severity distribution. A typical mid-engagement audit produces 2–8 Critical findings, 10–25 High findings, 30–60 Medium findings, and as many Low findings as are worth recording. The bell-shape is itself a credibility signal; reports that depart from it should justify the departure in the methodology statement.

### The "62 shades of gray" framing

The audit's strongest single buy-in tactic is *quantifying the visible consequence of the inconsistency*. UXPin's audit famously surfaced "62 shades of gray" in a single product's interface — a finding that required no expert-level interpretation, generated executive-level recognition, and carried the audit's authority into the budget conversation. The story has become a canonical reference because the framing technique works.

The technique: count the literal values the system has accumulated for any single semantic role, and report the count as the headline finding. Examples:

- Number of distinct grey hex values used across the product (UXPin's original).
- Number of distinct button heights across the component library.
- Number of distinct heading sizes used across the marketing surface.
- Number of distinct error-message phrasings used across the form components.
- Number of distinct loading-state implementations used across data-fetching components.

The phrasing is concrete enough that the executive can recite it back unaltered. "Our system has 62 shades of gray" survives meeting transcripts, slide decks, and Slack threads in a way that "the system's color tier discipline has lapsed" doesn't. The audit report should generate at least one such finding per engagement. The senior auditor's discipline is to look for the finding actively during the audit, not to settle for whatever surfaces; the count is rarely the highest-severity finding, but it's almost always the highest-traction finding.

The "shades of gray" pattern generalises: count the literal values the system has accumulated against the intent. How many "primary" buttons (the brand says one; the system has shipped four). How many "blue" colours (the brand says one shade; the system has 11 distinct blues across surfaces). How many "loading" states (the system has 19 distinct loading-state implementations across components). The variance against intent is the finding's grip; the executive recognises the gap between the brand's stated identity and the system's accumulated reality.

A second buy-in tactic that complements the first: **the cost framing.** Each finding's severity is paired with an effort estimate (in weeks or months); the executive reads the cost-of-fix against the cost-of-not-fixing. The audit's most-recommended finding is the one where the cost-of-fix is small and the cost-of-not-fixing compounds. The senior auditor identifies these "high-leverage" findings explicitly in the executive summary; they become the audit's strongest commercial argument for the follow-on engagement.

### The recommendations format

Every recommendation has a *commercial framing* the audit lead has explicitly written. The framing translates engineering or design language into commercial consequence.

Engineering language: "Token tier consolidation."
Commercial framing: "The architectural change that prevents the next rebrand from costing six months of redesign."

Engineering language: "Component API standardisation."
Commercial framing: "The discipline that lets new product teams adopt the system in two weeks instead of six."

Engineering language: "Contribution-model overhaul."
Commercial framing: "The change that turns the design system from a bottleneck into the company's leverage point on every product release."

The framing is not marketing — it's translation. The recommendation's content is the same; the language reaches a different audience. The audit lead's discipline is to author each recommendation's framing during the report's writing, not to delegate the framing to the practitioner who wrote the technical recommendation. The translation is the audit's commercial work.

A second discipline: every recommendation is *scoped against a possible follow-on engagement*. The recommendation isn't "do this work somehow"; the recommendation is "this work, in this shape, with this team, in this duration, against this commercial range." The scoping is honest (the audit's recommendations are the agency's natural follow-on; the conditional sales path is named explicitly), and the scoping is what makes the recommendation actionable. An executive reading a vague recommendation can't act; an executive reading a scoped recommendation can authorise the next engagement.

### Common reporting failure modes

Five reporting patterns recur as failures across agencies:

**The "everything is Critical" report.** Severity-grade inflation; the report loses authority. Fix: enforce the rubric; aim for the bell-shaped severity distribution.

**The "we found 500 things" report.** The executive can't act; the recommendations are buried in detail. Fix: the executive summary's top 5–10 findings discipline; the appendix carries the long tail; the report's main body is the architectural diagnosis, not the long-tail findings.

**The "deep on one lane, silent on others" report.** The audit reads as a sales pitch for the lane the agency wants to scope as the follow-on. Fix: the methodology statement explicitly names the lane scope; the report's per-lane structure is consistent across lanes; the recommendations span lanes proportionally.

**The "no executive summary" report.** The executive reads the first 5 pages and stops; the audit's diagnostic doesn't reach them. Fix: the executive summary is a required section of the template; the senior auditor authors it.

**The "vague recommendations" report.** Recommendations that don't survive procurement scrutiny — "modernise the token system" — produce no follow-on. Fix: every recommendation is scoped; every scope is procurement-actionable.

A sixth failure worth naming: **the "we said this last time" report.** When the audit is a re-audit (the practice has audited the system before; this is the next quarterly or annual round), the report has to read the *delta* — what's changed, what's been addressed, what's regressed, what's newly surfaced. Reports that re-state the prior audit's findings without acknowledging the elapsed work read as bureaucratic; reports that explicitly track delta read as professional and buyer-respecting. The delta-reading is its own discipline and worth a section of the methodology statement.

---

## 5. Continuous audit and drift detection — auditing in CI, not just at engagement start

The point-in-time audit is the practice's productised diagnostic. The continuous audit is the operational discipline that runs in the system's CI pipeline and prevents the system from accumulating the architectural debt that the next point-in-time audit would surface. The two are complements, not substitutes; the practice should ship both as distinct offerings, and the productised point-in-time audit's recommendations almost always include "stand up the continuous-audit pipeline" as a first-priority follow-on.

### What runs in CI

A mature continuous-audit pipeline ships eight surfaces in the system's CI:

**Visual regression at the component level.** Chromatic, Percy, Playwright with snapshot comparison, or the equivalent. Each component PR runs a visual diff against the baseline; unexpected diffs require explicit acknowledgment from the reviewer. Catches: state-completeness regressions, theme-application regressions, layout regressions from CSS changes, font-loading regressions.

**Visual regression at the token level.** Renders the system's component set against the token tree on every primitive change; the visual diff flags downstream effects across components that consume the changed primitive. Per 24 §Cross-brand drift — at portfolio scale, the visual regression at the token level is the mechanism that surfaces brand drift from one team's "small primitive change" propagating across the brand portfolio.

**Automated accessibility scanning.** axe-core or Pa11y running against every component story. Catches: missing ARIA roles, contrast-pair regressions on automated cases, heading-hierarchy issues, label-association issues, the long tail of accessibility patterns axe-core covers. The discipline: automated scanning catches the easy wins; it does not substitute for the four-engine × four-AT testing that the productised audit performs.

**The Cascade Report (per 24 §3).** On primitive changes, CI generates the per-brand and per-component impact report. The artefact is the conversation-starter for the governance review (see below). At portfolio scale, the Cascade Report is the highest-leverage single CI artefact.

**Dead-token detection.** Build-time scan of the codebase for tokens that no consumer references; the scan output is appended to every release. The dead-token list is the deprecation candidate list; the governance review reads it quarterly and decides what gets formally deprecated.

**Literal-value-in-component-CSS detection.** Build-time scan for component-level CSS (or the equivalent on native platforms) that hard-codes a value the token system should supply. Each occurrence is flagged; the team's PR review process treats new occurrences as contribution-model failures (the contribution should have used a token; if no token exists, the contribution should have proposed one).

**Component coverage scan.** Build-time scan of the consumer's code for component-instance counts, component-version-in-use, and detached or forked component instances. Feeds the adoption audit and the per-team adoption-rate disaggregation. The scan output is published to the drift dashboard (see below).

**Contrast-pair validation.** On theme or token changes, the system validates every WCAG-mandated contrast pair across every theming dimension. The PR is blocked on regressions to existing pairs; new pairs are flagged for review. Per 31's color-systems framing — the contrast-pair-decay pattern is what continuous validation prevents.

**Storybook-and-docs freshness check.** On component or API changes, the CI validates that the component's Storybook story and docs page were updated in the same PR (or in a paired follow-up PR within a stated SLA). The freshness check is the discipline that prevents the docs-vs-source drift the docs platform's freshness audit (per §2.6) measures.

A ninth surface, increasingly common as of mid-2026: **AI-readability validation.** Per 25 / 26 / 27 / 30's AI-readiness framing — the components-as-data structure (the per-component metadata, the descriptions, the prop semantics) validated for AI-agent consumption. The validation runs against a canonical prompt set ("how would an AI agent describe how to use this component") and flags regressions in machine-readability. As of mid-2026 this is more aspirational than universal; the tooling is custom and varies per practice.

### The drift dashboard

The continuous-audit signals aggregate into a single artefact: the drift dashboard. The dashboard's audience is three:

- **The DS team itself.** The dashboard is the team's operational signal — what's drifting, where regressions are landing, where coverage is decaying. The team reads the dashboard at the start of each sprint and at the end of each release.
- **The executive coalition.** The dashboard is the sponsorship signal — the system's health number, refreshed on every release, presented at quarterly executive readouts. The executive doesn't need the per-lane detail; they need the trend (the health score is rising, plateaued, or falling) and the headline (the most-recent regression that warrants attention).
- **The audit-engagement client.** The dashboard is the artefact the productised audit refreshes. An audit engagement that begins against an existing drift dashboard starts the audit at hour one with the lane evidence largely available; the audit's value shifts from evidence collection to architectural synthesis.

The dashboard's shape: a single page (or a single screen if it's a software dashboard) with a per-lane health score, the lane-level trend (week-over-week, month-over-month), the top recent findings, and the open-issue count. The aesthetic is the same discipline as a financial dashboard or an operations dashboard — clarity, consistency, signal-over-noise.

The practice that ships the drift dashboard as a default deliverable on every engagement past Stage 2 (per 00e's practitioner-count arc) has the audit's work mostly done before the audit engagement starts. The dashboard is also the most-leverageable artefact for the post-handoff retainer relationship — the retainer pays for the dashboard's maintenance and the quarterly governance review that reads it.

### The governance review's relationship to continuous audit

The quarterly governance review (per 08 §The quarterly governance review) is the human surface above the continuous-audit signal. The review reads the dashboard, decides what to escalate to the executive coalition, decides what to deprecate, decides what to recommend.

Without the continuous-audit substrate, the quarterly governance review is vibes-based — the team's read of how the system is doing, with whatever evidence happens to be at hand. The vibes-based review's discipline depends entirely on the senior practitioner running it; a strong senior produces strong reviews, a weak senior produces drift.

With the continuous-audit substrate, the review is signal-driven — the dashboard's data anchors the conversation, the per-lane trends are visible, the recent regressions are traceable. The review's discipline depends on the dashboard's quality, not on the senior's heroics. The substrate-driven review compounds the system team's effective seniority; it lets a mid-level practitioner run a credible review by reading the dashboard with the senior's prior coaching.

The recommended cadence: the quarterly review (60–90 minutes, per 08); a monthly drift dashboard refresh (asynchronous); a weekly engineering-led check-in on the CI pipeline's health (the audit-the-audit work, see below). The cadences are not free — the team has to budget for them — but the alternative (the system drifts; the next point-in-time audit is more expensive because the system has accumulated more debt) is more expensive in the aggregate.

### The tooling reality in 2026

The continuous-audit surface is not unified. The practice assembles it from multiple tools:

- **Visual regression.** Chromatic (the most-used as of mid-2026; ships Storybook integration and CI hooks); Percy (BrowserStack-owned; mature but losing share to Chromatic on the Storybook-centric workflow); Playwright with snapshot comparison (open-source; requires more configuration; the choice for non-Storybook workflows).
- **Automated accessibility.** axe-core (the canonical scanner; ships in axe DevTools, Storybook's a11y addon, Chromatic's a11y feature, Pa11y, Lighthouse); Pa11y (CI wrapper around axe-core); Lighthouse (a reduced axe-core ruleset for general web auditing).
- **Token surface.** Style Dictionary's audit features (v4 and onward); Tokens Studio's audit features (the Inspector, the design-tool-side audit); custom dependency-graph traversal where the system has matured beyond off-the-shelf tooling.
- **Coverage scanning.** Custom build-time scans (the senior DS engineer's per-engagement work); the practice's compounding scaffold accelerates each successive engagement.
- **Drift dashboards.** Custom (most common; built on the practice's preferred dashboard surface — Notion, Linear, Looker, Grafana, or a custom internal dashboard); Knapsack and Supernova ship dashboard features with partial coverage; Backlight ships limited dashboard surfaces.
- **Unified vendor offerings.** Knapsack, Supernova, and Backlight are the closest as of mid-2026, with overlapping feature sets and gaps. None covers the full continuous-audit surface; the practice choosing one of these as the platform should expect to fill gaps with custom tooling.

The practice's leverage is the *integration discipline* — the senior DS engineer who can stand up the integrated surface in 40–80 hours is the highest-leverage practitioner on the team for engagements past Stage 2. The integration is not a one-time cost; it requires ongoing maintenance as the underlying tools evolve. The practice that treats the integration as a one-time deliverable produces a pipeline that decays; the practice that treats it as a maintained artefact produces a pipeline that compounds.

### Where continuous audit fails silently

Five failure modes are routine and worth naming:

**Tooling drift.** The audit scripts haven't been run against the latest tooling release; the scripts produce false negatives because the tooling has changed. Fix: quarterly review of the audit pipeline itself; the "audit-the-audit" discipline.

**Coverage drift.** New components don't get their Storybook stories, so the visual-regression coverage decays; the system grows but the coverage shrinks proportionally. Fix: the merge-gate discipline that requires Storybook stories on every component PR.

**Threshold drift.** The contrast-pair validation thresholds were set against WCAG 2.1 and haven't been updated to 2.2; the validation runs but doesn't catch 2.2-only criteria. Fix: the threshold-review discipline as part of the audit-the-audit work.

**Naming drift.** Tokens were renamed (or aliases were re-routed); the dead-token scan didn't update its catalogue; tokens now flagged as "dead" are actually live under their new name. Fix: the catalogue-refresh discipline tied to the system's release cadence.

**Acknowledgment drift.** Visual-regression diffs require explicit acknowledgment from the reviewer; over time, reviewers acknowledge changes without genuinely reviewing them ("LGTM" on every diff). The signal degrades because the human review degrades. Fix: the periodic spot-check on acknowledgment quality; the discipline of acknowledgment-as-decision rather than acknowledgment-as-formality.

The "audit-the-audit" discipline — quarterly review of the continuous-audit pipeline itself — is rarely articulated in the field's literature and routinely needed in practice. The practice's productised audit's recommendations almost always include the audit-the-audit discipline as a first-priority operational hygiene item; the practice that ships the audit-the-audit cadence as a retainer offering produces the most reliable continuous-audit substrate across engagements.

---

## 6. The audit ↔ Six Signs ↔ maturity diagnostic relationship — the Discovery triad

The three Discovery diagnostics — Six Signs (the recognition diagnostic: is this a system rather than a UI kit?), maturity diagnostic (the trajectory diagnostic: where on the curve), audit (the current-state diagnostic: what's the system's actual health) — form a triad that the practice ships piecemeal but should ship as a unified Discovery deliverable. The three reinforce each other in ways the field's audit literature mostly doesn't articulate.

### Six Signs as the qualifier

Six Signs (or the practice's equivalent recognition criteria, which various practices have variously named — the "DS recognition test," the "system vs. UI kit diagnostic," the "DS-not-DS check") answers the qualifier question: *is what we're auditing actually a system, or a UI kit being called a system?*

The recognition criteria converge across practices on roughly these signs:

- **Tokens-as-architecture.** The system has a multi-tier token tree (primitive / semantic / component); the tree is consumed by both design and code; the tree is the source-of-truth across surfaces. Not: "we have some named colours in Figma."
- **Components-as-contract.** The system's components have stated APIs; the APIs are consistent across components; the APIs ship behavioural contracts (focus, keyboard, AT semantics, motion). Not: "we have Figma components and React components that look like each other."
- **Governance-as-protocol.** The system has a stated contribution model; the model operates (the velocity metrics show contribution happening); the deprecation discipline is real (items have been deprecated and removed). Not: "we have a Slack channel where people ask about the design system."
- **AT-as-stakeholder.** Accessibility is shipped as a system contract, not as a per-component conformance afterthought. The token tree includes contrast pairs; the components ship ARIA semantics; the system runs real AT testing. Not: "we ran axe-core once."
- **Multi-surface coverage.** The system covers more than one surface — multiple platforms, multiple brands, multiple product teams. The architectural decisions reflect the multi-surface reality. Not: "we have a Figma library for one product."
- **Intentional cross-engagement compounding.** The system's decisions are made with the next year's surface area in mind, not just the current sprint's. The architectural choices reflect long-horizon thinking. Not: "we shipped what the current product needed."

Six Signs answers: *is this a system?* The answer is binary in practice — either the system has the architectural foundations or it has the appearance of a system without the foundations. The diagnostic's value is the binary clarity; "you have a UI kit being called a design system" is a useful diagnosis even when the team rejects it, because the diagnosis names what the next engagement has to address.

If the Six Signs answer is "UI kit," the audit's shape changes. The diagnostic isn't "here's the state of the system you have"; it's "here's what's missing to make this a system." The audit becomes a roadmap-to-system rather than a state-of-system report. The lanes still apply (token, component, accessibility, content, motion, code, governance, adoption), but the lane findings are framed against the absence of the foundation rather than the operation of it. The recommendation is the foundation work, sequenced and scoped against the team's commitment.

### The maturity diagnostic as the trajectory

The maturity diagnostic answers: *given that this is a system, where on the maturity curve is it, and what's the next stage's challenge?*

Sparkbox's four-stage model is a useful reference frame:

- **Version One.** The system exists. Foundations are partially in place; component coverage is small; governance is informal; adoption is starting.
- **Growing Adoption.** The system has consumers; coverage is growing; the contribution model is starting to operate; the system is becoming load-bearing.
- **Surviving Teenage Years.** The system has accumulated technical debt; governance is contested; adoption is plateauing; the system is at risk of being replaced.
- **Evolving.** The system has survived the teenage years; governance is mature; adoption is widespread; the system is the organisation's load-bearing infrastructure.

Other maturity-curve frames exist (the InVision *Design Systems Handbook*'s four-stage frame; Curtis's stages model; the field's various "DS maturity" assessments). The practice should pick a frame and use it consistently; the frame's specific shape matters less than the consistency of application.

The agency-side variant of the curve (per 00e §3): Stage 0 (no DS practitioner) → Stage 1 (Part Timer) → Stage 2 (Allocated Individual) → Stage 3 (Dedicated Team) → Stage 4 (Embedded Multi-Team). The agency's maturity diagnostic reads the team's stage as the system's surrogate, since at agency scale the team's stage is the constraint on the system's growth.

The maturity diagnostic calibrates the audit's expectations. A greenfield (Version One) system audited against an evolving system's standards is unfairly judged — the foundations aren't expected yet; the audit's findings should focus on the next stage's challenge. An evolving system audited against a greenfield's standards is under-ambitious — the architectural debt has compounded; the audit should be pressing harder on governance and deprecation. The diagnostic's value is the calibration; without it, the audit's findings are out-of-context.

### The audit as the current-state diagnostic

The audit's eight-lane methodology (per §2) reads the system's current state. Given that this is a system (Six Signs), at this stage of maturity (diagnostic), here's the actual health.

The audit's finding-shape depends on the prior diagnostics. A Version One system's audit emphasises foundation work — the token tier, the initial component library, the early governance. An Evolving system's audit emphasises drift and accumulated debt — the literal-value-in-component-CSS findings, the contribution-model fatigue, the dead tokens, the API drift. The same lane methodology produces different finding-shapes against different stages.

The audit's recommendations are also stage-calibrated. A Version One system's recommendations are foundation-building; an Evolving system's recommendations are debt-paydown and architectural-restoration. The audit's commercial framing reflects the stage — Version One audits' follow-on engagements are foundation-build engagements; Evolving systems' follow-on engagements are restoration or successor-system engagements.

### How the three reinforce each other

The triad's reinforcement runs in both directions.

**Forward.** Six Signs shapes the audit's lane priorities — a system without a token tier doesn't audit alias resolution; a system without governance doesn't audit contribution-model operation. The maturity diagnostic shapes the audit's expectations — greenfield systems aren't audited for federated-contribution health. The audit then produces stage-calibrated findings.

**Backward.** The audit's findings refine the maturity diagnostic. A system claims to be Evolving; the audit's findings show the contribution model isn't operating, the dead-token count is at 30%, the per-team adoption is below 25% — the system is actually still in Surviving Teenage Years (or has regressed there). The audit's evidence corrects the self-perception; the corrected diagnostic feeds the next engagement's commercial framing.

**Cross-cutting.** The audit's findings sometimes surface a Six Signs gap. A system that claims systemhood but whose audit shows literal values consumed without semantic-tier mediation, contributions handled by ad-hoc Slack, accessibility handled by automated scanning only, and adoption tracked by self-report — the audit's diagnosis is "this is a UI kit being called a system." The Six Signs result was wrong; the audit corrects it. The recommendation is foundation work, framed against the team's likely resistance to the diagnosis.

The three diagnostics are read together; the Discovery report integrates them. The integrated read is the audit's most-leverageable single artefact, and one most agencies don't ship.

### The unified Discovery deliverable

The practice should ship one Discovery report that integrates Six Signs, maturity, and audit into a single read. The report's shape:

**Opening section: the system's framing.** Six Signs result (is this a system, with the recognition criteria's evaluation); maturity diagnostic (the curve stage, with the diagnostic's evaluation); the executive summary of the audit's headline diagnostic. The opening is 5–8 pages and reads as the report's frame.

**Middle section: the audit's body.** The eight-lane findings (per §2); the cross-lane patterns (per §4); the per-lane health scores. The middle is the bulk of the report (40–150 pages depending on system surface area).

**Closing section: the next-engagement recommendation.** The audit's recommendations calibrated against the maturity stage; the engagement's shape (Discovery + foundation work for Version One; foundation work + adoption support for Growing Adoption; debt paydown + governance overhaul for Surviving Teenage Years; succession planning + new-platform expansion for Evolving). The closing is 5–10 pages and reads as the bridge to the follow-on.

The unified report is the practice's highest-leverage Discovery artefact. It is also the artefact most agencies don't ship, because the three diagnostics are typically run by different practitioners on different timelines and the integration is treated as an after-the-fact pulling-together rather than a designed-as-one deliverable. The practice's commercial and intellectual leverage is to design the unified deliverable as one product.

### The commercial framing of the unified deliverable

A productised Discovery + audit engagement (5–10 days, $50k–$120k typical) is the strongest single sellable artefact the practice can ship. Three properties drive its commercial leverage:

- **It produces the diagnostic that justifies the next engagement.** The recommendations section names the follow-on engagement's shape, scope, and commercial range. The executive who reads the Discovery report can authorise the next engagement against the report's recommendations.
- **It carries the executive surface that the larger engagement requires.** The Discovery engagement builds the executive coalition. The 5–10 day engagement includes 60–90 minutes of executive readout; the readout is the practice's introduction to the executive sponsorship surface. Multi-month follow-on engagements that begin with the executive coalition already in place run substantially smoother than engagements that have to build the coalition from scratch.
- **It positions the agency as the practice that *thinks* about systems rather than just builds them.** The Discovery report's diagnostic depth — Six Signs + maturity + audit, integrated and stage-calibrated — is intellectual work. Agencies that ship this work signal a level of practice maturity that delivery-only agencies can't match. The signal is the agency's competitive positioning at the next RFP; the signal compounds across engagements.

The under-investment is structural and worth naming explicitly. Most agencies treat Discovery as a low-margin lead-in to the higher-margin delivery work; the Discovery engagement is priced cheaply, run quickly, and delivered without the polish the productised version would receive. The result is a Discovery output that doesn't carry its commercial value into the follow-on. The practice that invests in Discovery's productisation — that makes the Discovery engagement a premium, polished, intellectually-rigorous deliverable — converts at higher rates and at higher follow-on engagement values than the practice that under-invests. The investment is small (the methodology authoring, the report template, the integration discipline, the senior-practitioner training); the return is the practice's pipeline of larger engagements behind every Discovery.

The practice has the IP to ship the productised Discovery and audit. The under-investment is a strategic gap, not a capability gap. Closing it is the highest-leverage commercial move the practice can make in the audit territory.

---

## References

The DS-audit literature is fragmented; primary sources cluster across practitioner blogs, conference talks, and platform documentation. The references below are organised by the section they primarily support, with notes on which translate to agency contexts.

### Primary field references — DS-audit methodology

- **Brad Frost, *Atomic Design* (2013, online), Chapter 5 on Interface Inventory.** The canonical introduction to the audit-as-component-inventory pattern. The interface inventory is the heuristic ancestor of the modern DS audit. https://atomicdesign.bradfrost.com/chapter-5/
- **Brad Frost, "Interface Inventory" blog post and follow-ups.** The practice that became the interface inventory's common form. https://bradfrost.com/blog/post/interface-inventory/
- **Nathan Curtis, EightShapes catalogue.** Multiple posts cover audit-relevant patterns — *Recognizing Patterns*, *Pattern Library Audit*, *Coverage Numbers in a Design System*, and the broader contribution-model writing that audits read against. https://medium.com/@nathanacurtis
- **Nathan Curtis, *Coverage Numbers in a Design System* (EightShapes, 2020 with revisions).** The canonical articulation of the three coverage definitions (Morningstar, Veriff, didoo). https://medium.com/eightshapes-llc/measuring-design-system-coverage-90e0d5f97375
- **Sparkbox audit case studies.** Sparkbox publishes Practitioner-style writeups of their DS audits; the case studies are the field's strongest agency-side audit reference. https://sparkbox.com/foundry
- **Ben Callahan / Sparkbox, *Design System Maturity Model*.** The four-stage model (Version One / Growing Adoption / Surviving Teenage Years / Evolving). https://sparkbox.com/foundry/design_system_maturity_model
- **InVision Design Systems Handbook (2017, online).** Slightly dated but foundational. The handbook's audit chapters address the inventory pattern and the maturity assessment. https://www.designbetter.co/design-systems-handbook
- **The Design Systems Podcast.** Multiple episodes feature audit-focused practitioner conversations. https://thedesignsystem.guide/podcast
- **Design Systems Conference (Clarity).** Multiple talks across 2018–2025 address the audit; the agency-side audit talks are scattered through the back catalogue. https://www.clarityconf.com/

### Audit-as-deliverable productisation

- **UXPin, "62 shades of gray" framing.** The canonical buy-in story; the original case study in UXPin's content library. The phrasing has become a field reference; the original case is rarely cited but frequently invoked. https://www.uxpin.com/ (search the content library for the audit case)
- **Sparkbox and Knapsack on the audit-as-engagement-shape.** Sparkbox and Knapsack both publish audit-engagement framing as part of their commercial offering descriptions. https://sparkbox.com/foundry; https://www.knapsack.cloud/blog
- **Dan Mall on Discovery engagements.** Mall's writing on the Discovery shape (and the Hot Potato process for the contribution-coaching arc that the audit's recommendations often initiate). https://danmall.com/

### Reporting templates and buy-in

- **The "62 shades of gray" framing (above).** The buy-in tactic's canonical reference.
- **Brad Frost on the audit's report shape.** Frost's blog includes practitioner-shaped writing on how audits get written and what's worth including. https://bradfrost.com/

### Continuous audit and drift detection

- **Chromatic's Visual Testing documentation.** The most-used visual-regression tool in the Storybook-centric workflow as of mid-2026. https://www.chromatic.com/docs/
- **Percy (BrowserStack) documentation.** The visual-regression tool with the longest history in the space; competitive with Chromatic on non-Storybook workflows. https://www.browserstack.com/docs/percy
- **Playwright documentation, Snapshot Comparison.** The open-source alternative for visual regression; chosen for non-Storybook workflows. https://playwright.dev/docs/test-snapshots
- **axe-core documentation (Deque).** The canonical automated accessibility scanner; ships in many integrations. https://github.com/dequelabs/axe-core
- **Pa11y documentation.** CI-friendly wrapper around axe-core. https://pa11y.org/
- **Lighthouse documentation (Google).** General web auditing with a reduced axe-core ruleset. https://developer.chrome.com/docs/lighthouse/
- **Style Dictionary v4+ documentation, audit features.** The dependency-graph traversal and the build-time scan surfaces. https://styledictionary.com/
- **Tokens Studio documentation, Inspector and audit features.** The design-tool-side audit surface. https://tokens.studio/
- **Knapsack documentation, drift dashboard features.** The unified drift surface; partial coverage of the continuous-audit lanes. https://www.knapsack.cloud/
- **Supernova documentation, audit and dashboard features.** The competitor to Knapsack on the unified drift surface. https://www.supernova.io/
- **Backlight documentation (Workleap-owned as of 2024).** The third unified-platform option; limited drift dashboard. https://backlight.dev/

### Accessibility — methodology references

- **W3C WCAG 2.2.** The conformance standard. https://www.w3.org/TR/WCAG22/
- **W3C WCAG-EM (Evaluation Methodology) 1.0.** The canonical conformance-evaluation procedure. https://www.w3.org/TR/WCAG-EM/
- **W3C ARIA Authoring Practices Guide (APG).** The composite-widget pattern reference. https://www.w3.org/WAI/ARIA/apg/
- **WCAG-EM Report Tool.** The W3C's tool for producing WCAG-conformance evaluation reports. https://www.w3.org/WAI/eval/report-tool/

### Regulatory references — for the regulated-industry audit

- **European Accessibility Act (Directive (EU) 2019/882), in force 28 June 2025.** EU-market accessibility regulation; imports WCAG 2.1 AA as baseline. https://eur-lex.europa.eu/eli/dir/2019/882/oj
- **US Section 508 Revised Standards (2018).** US federal procurement accessibility. Imports WCAG 2.0 AA. https://www.section508.gov/manage/laws-and-policies/
- **Americans with Disabilities Act (ADA) Title III.** US public-accommodation accessibility; courts have settled on WCAG 2.0/2.1 AA as the working standard. Litigation-anchored. https://www.ada.gov/

### Maturity and Discovery diagnostics

- **Sparkbox four-stage maturity model (above).**
- **InVision Design Systems Handbook's maturity framing (above).**
- **Curtis on stages — *Solitary, Centralized, Federated, Cyclical*.** EightShapes; the team-side maturity frame. https://medium.com/eightshapes-llc/team-models-for-scaling-a-design-system-2cf9d03be6a0
- **The agency-side practitioner-count arc (per the practice's 00e file).** Stage 0 through Stage 4 (Embedded Multi-Team) as the agency variant.

### Conferences and community

- **Clarity Conference back catalogue.** Multiple audit-focused talks. https://www.clarityconf.com/
- **Config (Figma).** Audit-relevant talks scattered through the catalogue.
- **Smashing Conference.** Practitioner-level talks including audit work. https://smashingconf.com/
- **Into Design Systems.** Newsletter and conference; audit topics surface regularly. https://www.intodesignsystems.com/

### Verification notes

- All "as of mid-2026" claims about tooling versions and audit-surface coverage should be re-checked against the current state. The vendor landscape is evolving rapidly; Knapsack, Supernova, and Backlight in particular are actively shipping new features.
- The DTCG Format Module is at version 2025.10 as of mid-2026; the conformance audit's specifics should be re-checked against the current spec at https://tr.designtokens.org/format/
- WCAG 2.2 has been the working standard since October 2023; WCAG 3.0 is in working-draft status as of mid-2026 and not yet a procurement standard. The audit's a11y lane should track WCAG 3.0's evolution as it approaches Recommendation status.
- The "62 shades of gray" attribution to UXPin is widely circulated; the original case study's specifics (which client, which year, which exact phrasing) deserve primary-source verification before the framing appears in client artefacts.
- The Sparkbox four-stage maturity model post may be 2018-vintage; verify the current canonical Sparkbox writeup before treating the model's specifics as load-bearing.
- Pricing ranges for productised audit engagements ($25k–$45k for 3-day; $50k–$80k for 5-day; $90k–$150k for 10-day) reflect mid-2026 industry observation and vary materially by region and agency tier. Verify against current proposals and recent engagements before treating as load-bearing in client conversations.
