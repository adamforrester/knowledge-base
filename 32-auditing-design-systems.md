---
type: practice-area
title: Auditing Design Systems
description: Auditing as a discipline at agency scale — the eight-lane methodology, the productised audit engagement, reporting templates and the buy-in surface, continuous audit and drift detection in CI, and the audit ↔ Six Signs ↔ maturity diagnostic Discovery triad as the practice's highest-leverage productised offering.
tags: [extension, audit, discovery, governance, methodology, commercial]
timestamp: 2026-06-17
---

# 32 — Auditing Design Systems

> We run audits constantly. Inside Discovery, inside inherited engagements, inside the audit-and-reconnect pattern 00b names, inside the quarterly governance review 08 covers, inside every one of the seventeen-plus files where audit references show up as activities rather than as a discipline. What we have not done is articulate auditing as a methodology of its own — the eight surfaces it examines, the productised engagement that ships it as a sellable Discovery deliverable, the reporting template that holds the shape across engagements, the continuous-audit substrate that runs in CI between point-in-time audits, and the unified Discovery triad (audit + Six Signs + maturity) that is the strongest single artefact the practice can ship. This file is that articulation. It is also the practice's most-under-invested commercial surface; the IP exists in the senior practitioners' heads, and shipping it as a productised offering is the highest-leverage move available to the practice in 2026.

---

## Why auditing needs its own file

Audit references appear across at least seventeen files in this vault. 01 names audit activities at the engagement-architecture level. 08 covers the quarterly governance review with brand-alignment audit. 11 names the mobile-specific token audit. 12 covers Figma's native linting. 17 covers annotation-state auditing. 23 surfaces the under-tokenisation patterns audits typically expose. 25 covers the manual-walkthrough-when-Zeroheight-is-closed pattern. 31 names the WCAG-passes-audit-but-fails-real-users pattern. 00b names audit-first inherited engagements. 24 ships the Cascade Report as the cross-brand drift artefact. 30 covers the docs-platform freshness audit. The activity is everywhere; the discipline is nowhere.

What this file extends: every one of those references' audit dimension, plus the dual-agent research run on auditing-as-a-discipline (`_research/_inbound/2026-06-17-auditing-design-systems/`). What it does not replace: the activities themselves stay where they are — 08's quarterly governance review, 17's annotation-state audit, 24's Cascade Report all stay in their files. This file owns the methodology layer above them: the eight lanes, the productisation, the report template, the continuous-audit substrate, and the Discovery triad.

The practice's commercial-leverage gap, named explicitly in 09 §1.28: we run audits inside Discovery routinely; we do not sell standalone audit engagements as productised offerings, despite this being the most-asked-for entry-point engagement in the field. The audit's productisation is a 40–80-hour senior-practitioner investment that closes the practice's largest single sales-surface gap.

---

## 1. Why a DS audit is a DS-architecture concern, not a generic UX audit concern

A design system audit is a methodology in its own right, not a UX audit applied to a system, not an accessibility audit broadened in scope, not a front-end code audit narrowed to component code. The categorical difference is *what the audit reads*, not how rigorously it reads it.

A **UX audit** reads pages and screens. The unit of analysis is the user-facing surface; the methodology is heuristic against Nielsen's ten or some derivative; the evidence is screenshots and task walkthroughs; the findings are surface-specific and the recommendations are page-level fixes. Authority is the practitioner's reputation against the heuristic set.

An **accessibility audit** reads against a standard. The unit of analysis is the conformance criterion (WCAG 2.2's 87 success criteria); the methodology is the W3C's WCAG-EM evaluation procedure; the evidence is per-criterion test results across a representative sample; the findings are stated as conformance failures with severity per criterion. Authority is the standard itself.

A **front-end code audit** reads codebases. The unit of analysis is the file, function, or module; the methodology is static analysis plus practitioner reading; the evidence is code excerpts and architectural diagrams; the findings are code-quality and performance concerns. Authority is professional engineering practice.

A **DS audit reads architecture, contracts, protocols, and the cross-surface drift signal.** The unit of analysis shifts depending on lane (the token tree, the component API, the contribution model, the adoption pattern); the methodology blends specification audit (against DTCG, ARIA APG, the system's own stated rules), heuristic audit (against the practitioner's accumulated pattern catalogue), and census audit (where tooling allows automated coverage scans). The evidence is multi-layered — token-tree extracts, component prop matrices, build-time scan output, contribution-velocity metrics, executive-stakeholder interviews. The findings are *architectural*. The audit's authority is methodological, evidential, and field-framed.

When an interface contains a usability flaw, a UX audit flags the page. A DS audit identifies whether the underlying component API forced the consumer to polyfill an interaction, thereby introducing the flaw systematically across every consuming application. **The DS audit evaluates the rules engine; adjacent audits evaluate the localised output.**

### How DS audits get miscategorised, and what it costs

The miscategorisation happens at three points and the costs at each are real. **At procurement,** the client's procurement function reads "design system audit" against the catalogue of audit-shaped engagements they have priced before — usually a UX audit ($15k–$40k) or an accessibility audit ($20k–$60k). The DS audit gets sized against those benchmarks and arrives at a budget that forces the engagement to skip lanes. The pre-engagement conversation has to re-anchor procurement: the price comparison that matters is not "what did your last UX audit cost" but "what will this audit's recommendations save you on the next eighteen months of system work." Audits that surface a token-tier consolidation opportunity routinely justify their cost ten times over against the redesign work the consolidation prevents.

**At kick-off,** the client team's expectation arrives as the heuristic walk-through. They expect the auditor to tour their Figma library and produce a list of fixes; the auditor opens with stakeholder interviews, requests build-pipeline access, asks for the token source-of-truth, and starts pulling component-coverage metrics. The team feels audited in a way they didn't authorise. The fix is a pre-audit framing document, sent before kick-off, that names the lanes in scope, the evidence the audit will collect, the access required, and the deliverables. With the framing in place, kick-off is a pre-flight check; without it, day one of the audit gets consumed by orientation.

**At delivery,** the client team reads the report against the heuristic-walkthrough expectation: a list of fixes. When the report opens with cross-lane patterns and architectural diagnostics, the team responds with "but what should we *fix*?" The architectural framing is the audit's diagnostic value; the team wants the punch list. The fix is the report's structure — executive summary first; per-lane findings second; cross-lane patterns third; recommendations as a separate section that *does* read as a punch list, organised in three priority bands.

The cost of these miscategorisations is real and quantifiable. Wrong scoping reduces audit depth. Wrong team mix produces the wrong evidence (a UX-led audit can't read the build pipeline; an engineering-led audit doesn't surface design-tool drift). Wrong output positions the audit as engineering housekeeping rather than commercial value. Wrong buy-in produces an audit that lives in a Notion page nobody refers to again.

### Why DS audits compound across engagements

A senior DS auditor's method improves with each engagement in ways a UX auditor's doesn't. DS audit findings cluster around a small number of architectural failure modes that recur across systems with surprising consistency, while UX audit findings are particular to each product's domain.

The recurring failure modes — the ones a senior auditor recognises in the first hour — include:

- **The literal-value-in-component-CSS pattern.** Components hard-code values the token system should supply. Visible at a glance once the auditor knows to look.
- **The semantic-tier-skip pattern.** Components consume primitive tokens directly, bypassing the semantic layer. Visible symptom is brittle theming; architectural cause is the absent semantic tier.
- **The "we have a token system but components don't use it" pattern.** Tokens exist in Figma, exist in Style Dictionary output, don't show up in production CSS because the dev team built parallel implementations.
- **The forked-component pattern.** Product teams forked the system's component because the API didn't accept their use case; the system team didn't accept the contribution; the fork now drifts. The canonical contribution-model failure.
- **The "every team claims to use the system, the build scan disagrees" pattern.** Self-reported adoption significantly higher than build-time scan reality.
- **The composite-typography-token-flattening pattern** (per 23). The system designed composite typography tokens; the build pipeline collapsed them to resolved values per platform; per-platform fidelity has degraded.
- **The contrast-pair-decay pattern** (per 31). The system documents WCAG contrast pairs at one theme; theming changes shipped without re-validating the contrast pairs; some pairs now fail.
- **The component-v1-API-still-shipping pattern.** Component API shifted across versions; consumers still pin to v1; the v3 API improvements aren't reaching production.

These patterns recur across systems built by different teams in different industries. The senior auditor's pattern catalogue is the practice's compounding intellectual asset; it is also a source of audit-finding bias the auditor has to manage. The discipline is to use the pattern catalogue as a *hypothesis generator* — what to look for first — not as a finding shortcut. **Our compounding asset in audit work is the audit method-IP**, not any specific audit's artefact.

### The audit's authority surface — three audiences, three standards

Audit findings have to defend themselves against three audiences with three different standards, and the senior auditor's report carries authority against all three.

**The client engineering lead** — who built the system. Findings need to be evidentially specific: file paths, line numbers, build-time scan output, specific commit SHAs. Vague findings lose to the engineering lead's specific knowledge; "the token at `components/button/background.brand` resolves to `#0066CC` in the Figma library and `#0070D2` in the Style Dictionary output; the discrepancy traces to commit a3f2c1b" wins.

**The client design lead** — who designed the system or inherited it. Findings need to be framed against intent — "the typography scale you stated as the intent in the foundational design document is implemented inconsistently here, here, and here, with these consequences for readers." Findings that read as taste lose to the design lead's authority over taste; findings that read as intent-vs-implementation hold.

**The executive** — who is paying for the audit. Findings need to be commercially framed — not "token-tier consolidation is recommended" but "the architectural change that prevents the next rebrand from costing six months of redesign." Findings that read as engineering detail lose the executive's attention; findings that read as commercial consequence hold it.

The audit's authority is methodological (the audit followed a stated method), evidential (each finding cites specific instances), and field-framed (industry consensus exists; the system diverges here). The senior auditor's report carries all three; the apprentice auditor's report carries one or two and gets pushed back proportionally.

---

## 2. Audit methodology — the eight audit lanes

The DS audit examines eight surfaces, each with its own methodology, evidence types, scoring rubric, and reporting shape. A comprehensive audit covers all eight; a focused audit names which lanes are in scope and which aren't, with the reasoning for each scope decision. The lanes interact — a finding in one lane is often the symptom of a cause in another — and the audit's diagnostic value lives in reading across lanes as much as in any single lane's depth.

| Lane | Key diagnostic focus | Primary evidence source |
|---|---|---|
| **Token** | Alias resolution, multi-mode orthogonality, dead tokens, literal-value detection, contrast-pair coverage, DTCG conformance | Style Dictionary build output, Tokens Studio graph engine, custom dependency-graph traversal |
| **Component** | API consistency, composition primitives, state-machine completeness, API drift, polyfill propagation | Component library repo, consumer-codebase AST scans, Storybook |
| **Accessibility** | WCAG 2.2 AA per component, four-engine × four-AT matrix, ARIA 1.3 APG conformance, focus management, user-preference media queries | Manual AT testing, axe-core CI, contrast-pair matrix |
| **Content** | Voice-and-tone consistency, error templates, empty-state copy, CTA verb taxonomy, ICU MessageFormat, AI-surface assistant tone | Documentation, hard-coded strings in consumer repos, AI-surface prompt walkthroughs |
| **Motion** | Three-tier motion tokens, choreography vocabulary, reduce-motion contract, performance budget, spring-parameter mapping | CSS transitions, Framer Motion configurations, native motion APIs |
| **Code** | Build pipeline health, CI quality gates, semver automation, test coverage, docs freshness, package-publish surface | CI/CD pipeline scripts, npm registry, GitHub Actions logs |
| **Governance** | Triage SLAs, contributor distribution, contribution-vs-participation, deprecation discipline, executive coalition | PR review logs, Jira/Linear cycle times, governance-body meeting notes |
| **Adoption** | Source-mix-overtime, per-team and per-component coverage, detached/forked counts | Build-time AST scans, Figma analytics, self-report-vs-reality interviews |

Eight lane summaries follow, each at the depth the productised audit demands.

### 2.1 Token audit

The token audit reads the system's token tree as architecture. The methodology examines tier coverage (primitive / semantic / component, or the collapsed shape that signals the audit's headline finding), alias resolution health (chain depth, integrity, theme-stability), multi-mode and multi-collection architecture (per 24's tokens-at-scale framing — when the brand axis warrants multi-collection vs. when mode warrants multi-mode), and theming-dimension orthogonality (mode + density + brand + contrast preference as separate axes vs. collapsed). The audit's most common headline finding lives here: dimensions that should be orthogonal have collapsed into a single "theme" axis, producing a combinatorial explosion of single tokens that becomes architecturally intractable past a portfolio's third or fourth brand.

Operational checks within the lane: dead-token detection (tokens defined that no consumer references — 1–5% is normal hygiene; 25%+ signals a system-team-vs-consumer disconnect), literal-value-in-component-CSS detection (the inarguable signal that the system is being actively bypassed), contrast-pair coverage and resolution across every theming dimension (cross-references the accessibility lane), DTCG conformance status (the 2025.10 Format Module's specifics — composite tokens via property-level-aliasing-with-`$ref` rather than `{alias}` notation), and cross-platform output integrity (Style Dictionary builds to web CSS / web JS / iOS Swift / Android Kotlin / Compose / Flutter / RN; the audit checks that each platform receives a faithful representation, with composite typography tokens a particularly common silent-flattening failure point).

Tooling. As of mid-2026, the lane is fragmented but powerful. Style Dictionary's CLI surfaces (`buildAllPlatforms`, `cleanPlatform`, the v4 resolver that exposes the dependency graph) give the audit programmatic access to the token tree. Tokens Studio's graph engine supports custom dependency-graph traversals — visually mapping the relationships between core brand colours and their downstream semantic applications. Knapsack, Supernova, and Backlight ship token-audit views with overlapping coverage. None unify the lane; the senior auditor assembles the picture from multiple tools plus custom scripts.

### 2.2 Component audit

The component audit reads components as APIs and behavioural contracts. The primary metric is coverage against the consumer's surface — for each component, how many products consume it, how many distinct screens reference it, how many distinct teams have consumed it. The matrix is the audit's most direct adoption signal; components with bimodal counts (high in some products, zero in others) signal team-level adoption gaps that the adoption lane will read in more depth.

API consistency across the library is audited next. Props that share semantics across components (`size`, `tone`, `disabled`, `loading`, `variant`, `as`, `asChild`) should have consistent typing, defaults, and behavioural contracts. The audit tabulates inconsistencies; the canonical failure is `size="small"` on Button and `size="sm"` on Input — same semantic, different naming, the cross-component composition surface fragments.

Composition primitives — Slot, AsChild, render-prop, polymorphic `as` — are the surface that lets consumers extend components without forking them. The audit examines coverage and consistency. Systems lacking composition primitives produce forking; the audit's finding is "consumers fork because the primitive surface forces it," with the forking evidence from the adoption lane cross-referenced.

State-machine completeness — focus, hover, active, disabled, error, loading, empty, selected, indeterminate — audited per component against the component's role. API drift across versions (additive / breaking / chaotic — the drift pattern signals the contribution model's health). Polyfill detection, where consumers wrap components in their own wrappers because the API is missing a prop — common polyfills are not always failures, but the catalogue tags each as legitimate, gap-driven, or fork-precursor. Detached and out-of-system component detection in Figma (detached-instance count via the API) and in code (imports that don't resolve to the system's package).

Tooling: the Figma API for detached-instance counts; Storybook's CSF plus custom tooling for the prop matrix; build-time scans against the consumer's codebase for the consumption metrics. The senior DS engineer's per-engagement scan-tooling work is what makes the census-mode lanes possible inside the audit's time budget.

### 2.3 Accessibility audit

The accessibility lane has the most-published methodology of the eight, anchored on the W3C's WCAG-EM (Evaluation Methodology) for conformance audits and the ARIA Authoring Practices Guide for composite-widget pattern conformance. We extend both for system-specific concerns.

**WCAG 2.2 conformance per component** (in force since October 2023; widely in procurement language by 2024–2025). Each component is audited against the relevant success criteria — text alternatives, contrast (1.4.3, 1.4.6, 1.4.11), keyboard accessibility (2.1.1, 2.1.2), focus management (2.4.3, 2.4.7, 2.4.11–13 — the new 2.2 focus-appearance and target-size criteria), name-role-value (4.1.2). The audit produces a per-component-per-criterion conformance grid.

**The four-engine × four-AT test matrix.** Real assistive-technology testing across the canonical browser × AT pairs — Chrome + JAWS (Windows), Firefox + NVDA (Windows), Safari + VoiceOver (macOS / iOS), Chrome + TalkBack (Android), plus increasingly Edge + Narrator (Windows). The matrix is real testing, not automated scanning; the auditor walks each component in each AT and notes the user experience. The matrix is the highest-authority accessibility evidence and the most labour-intensive; sample audits cover the most-used components (the consumer-surface analysis from the adoption lane tells the auditor which components warrant the matrix coverage). VoiceOver dominates mobile screen-reader use; JAWS leads on Windows enterprise; NVDA leads open-source Windows use — proportions vary by industry and per WebAIM's annual screen-reader survey, which is the verification path before quoting market-share figures in client artefacts.

**ARIA 1.3 composite-widget pattern conformance.** For composite widgets (combobox, listbox, menu, menubar, tablist, tree, grid, treegrid, dialog, alertdialog), conformance against the W3C APG's pattern. The audit reads the system's implementation against the APG and flags divergences; the divergences are sometimes legitimate (the APG pattern doesn't fit the use case; the system has shipped a different but accessible pattern) and sometimes failures (the divergence breaks AT navigation). The audit cites the APG section for each finding.

**Focus-management discipline.** Focus-trap-on-modal, roving-tabindex on composite widgets, restore-focus-on-close, skip-to-content link, focus-visible vs. focus indicators, the focus-appearance criterion (WCAG 2.2 SC 2.4.13). Tested manually across the AT matrix.

**Contrast pair coverage at every theming dimension.** Cross-references the token audit's findings into the accessibility lane. The audit confirms the token-level math with rendered-component testing; sometimes the math passes but the rendered component fails because the component's stacking context introduces transparency.

**User-preference media-query support.** `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`, `forced-colors`, `prefers-reduced-data`. The most-overlooked is `forced-colors` (Windows High Contrast Mode) — per 28's web-accessibility-implementation framing, components with custom colour schemes need explicit `forced-colors` handling or they break in HCM.

**EAA and Section 508 conformance.** For clients with regulatory exposure — European Accessibility Act (in force June 2025), Section 508 for US federal procurement, ADA Title III for US public-accommodation — the audit extends to the regulatory regime. The EAA imports WCAG 2.1 AA as baseline; Section 508 imports WCAG 2.0 AA via the Revised 508 Standards (2018); ADA Title III is litigation-anchored but courts have settled on WCAG 2.0/2.1 AA as the working standard. The audit's regulatory section is what client legal reads.

**The WCAG-passes-but-fails-real-users pattern** (per 31). Components that pass automated contrast checks against WCAG and fail real users — most common in dark-mode implementations where the literal contrast math works but perceptual contrast is inadequate. The audit's evidence is real-user testing or the auditor's perceptual-contrast read (APCA Lc as the working measure); the recommendation is APCA-as-quality-bar with WCAG-as-floor.

Tooling: axe-core (the canonical automated scanner; ships in axe DevTools, Storybook's a11y addon, Chromatic's a11y feature, Pa11y, Lighthouse) covers the automated portion. None of these substitute for real AT testing.

### 2.4 Content audit

Voice-and-tone consistency at the system level (Mailchimp / Polaris pattern), audited against the system's stated voice. Error-message templates, empty-state copy patterns, CTA verb taxonomies (the canonical example: "Submit" vs. "Save" vs. "Send" vs. "Continue" vs. "Done" vs. "OK" — same semantic role, multiple verbs, no apparent discipline). Per-component microcopy guidance (per 29's per-component template). ICU MessageFormat conformance for i18n-shipping systems (per 13). Assistant tone for AI surfaces (per 25 / 26 / 27) — refusal patterns, citation format, disclosure boilerplate, the LLM-surface microcopy that increasingly shapes the consumer experience.

Tooling is limited as of mid-2026. Acrolinx and Writer cover voice-and-tone validation against custom rules; Hemingway and Grammarly Business cover prose readability without modelling the system's voice. The lane runs largely manually. Our leverage is the audit's *checklist* — the centralised voice-and-tone matrix, the empty-state pattern, the verb taxonomy — which we ship as the recommendation deliverable.

### 2.5 Motion audit

Motion-as-foundation maturity is recent (per 18–21); systems built before 2022–2023 often don't have a motion lane to audit. When the lane exists, the audit examines three-tier motion-token coverage (duration / easing / composed), choreography vocabulary (entry / exit / transition / attention), the reduce-motion contract (`prefers-reduced-motion: reduce` handling, with the discipline of reducing duration and amplitude rather than removing motion entirely — motion-removal can break the user's understanding of state changes), the performance budget (INP-respecting, compositor-only animations), and cross-platform spring-parameter mapping where mobile is in scope.

### 2.6 Code audit

Build pipeline health, CI quality gates (visual-regression, automated-a11y, semver automation), per-component test coverage, docs platform freshness (per 29 / 30), package-publish surface (tree-shaking, peer dependencies, side effects), framework-specific integration health, and the implementation-vs-design-source faithfulness check (per 12 for the design-to-code seam). Tooling: GitHub's Actions surface plus Chromatic / Percy plus axe-core in CI plus the language-specific test runners. The senior DS engineer reads the CI configuration and the build pipeline; tooling automates the evidence collection.

### 2.7 Governance audit

Per 07's governance framing — request triage, SLAs, review-and-merge cadence, contribution-vs-participation distinction (Curtis: contributions are tangible, useful, federated, released; everything else is participation), the contribution scale (Fix → New Catalog), contributor distribution (the system team vs. designated ambassadors vs. ad-hoc contributors), deprecation discipline (does deprecation actually happen, on what timeline, with what consumer-migration support — the canonical failure is deprecation announcements without removal), major-release cadence, governance-body meeting cadence and decision quality, and the executive-coalition surface (a weakening coalition is a leading indicator of system-budget-cut and engagement-extension-rejection).

Tooling: limited automation. The audit is interview-led plus document-review (the contribution guide, meeting notes, release notes). The senior auditor's evidence is mostly conversational.

### 2.8 Adoption audit

High adoption numbers can mask vanity-metric calculation; the audit insists on a defensible coverage definition. Three industry definitions are in use (per 07's coverage framing and 08's measurement framework):

- **Morningstar's "% of pages applying system components."** Tracks the percentage of total application pages utilising system components. Most actionable single number for executive readouts.
- **Veriff's "components in use across all repos."** Most comprehensive for engineering-led organisations; engineering-heavy to compute.
- **Cristiano Rastelli's "source-mix-overtime"** (popularised at Badoo's Cosmos system; published as didoo). Calculates the percentage of nodes originating from the design system versus all nodes in a given project. Proportional approach prevents the data skew that pure instance counts produce; the practitioner standard for the most-faithful adoption read.

The audit picks one definition (we recommend Morningstar as default; provide alternatives by client context per 08's working synthesis), measures against it, and reports the trend over time. The number alone is incomplete; the trend matters more (rising / plateaued / declining).

Per-team adoption rate (the disaggregation that surfaces the bimodal pattern — Team A at 80%, Team B at 15% — and points the recommendation at team-level resistance vs. team-level support absence). Per-component usage distribution (the long-tail problem; a small number of components account for the majority of usage; the long tail is read for components that should be used more vs. components that shouldn't exist). Detached and forked component count (cross-references the component audit's findings; each fork is a per-team duplication of the system's work, with the cumulative cost framed commercially). The "we use the system" claim vs. the build-time scan reality — the gap is the adoption audit's most useful single finding because it surfaces the perception gap that prevents the system team from getting the resources it needs.

Tooling: build-time scans require custom tooling against the consumer's codebase. The senior DS engineer's per-engagement scaffold accelerates each successive engagement.

### Heuristic vs. specification vs. census auditing

The audit's methodology statement names which mode is in use per lane. Treating modes homogeneously leads to budget overruns or under-evidenced findings.

- **Heuristic auditing.** A senior practitioner walks a sample of surfaces against their pattern catalogue. Fast, deep on the patterns the practitioner recognises, blind to what they don't. Best for: the audit's first pass; the lanes where the failure modes are well-catalogued (component, content, governance); the senior-practitioner read of the system's overall architectural shape.
- **Specification auditing.** Spec-checking every (or every-in-scope) surface against a stated rule set. Slower, exhaustive within scope, generates a defensible artefact. Best for: WCAG conformance audits (rule set is the W3C standard); DTCG conformance audits (rule set is the spec); contribution-model audits against a stated protocol.
- **Census auditing.** Scanning every consumer at the build-time level via custom tooling. Expensive to set up, the highest-authority output. Best for: adoption-coverage measurement; literal-value detection; dead-token detection; per-component usage distribution.

Real audits are blends. A typical mid-2026 mid-engagement audit blends: heuristic for the first-pass component sweep + content + governance + executive-stakeholder readings; specification for accessibility (WCAG) + DTCG token conformance + ARIA APG composite-widget patterns; census for token-coverage + component-coverage + dead-tokens + literal-value detection. The blend is what produces both the architectural diagnosis and the defensible evidence.

### How the lanes interact

The audit's diagnostic value lives in cross-lane reading. A worked example, the canonical illustration both research passes converged on independently:

The token audit surfaces a primitive `color.blue.500` consumed directly by `Button` (skipping the semantic tier). The component audit confirms the API drift — `Button` has accumulated a `tone` prop that takes literal colour values instead of semantic role names. The adoption audit shows the product team has forked `Button` because the API drift made it impossible to support their brand variant cleanly. The governance audit shows the contribution model rejected the product team's contribution that would have closed the API gap, because the system team felt the contribution didn't fit the system's intent.

Each individual finding is a partial diagnosis. The architectural read is: the token-tier discipline lapsed (token audit), the lapse propagated into the component API (component audit), the consumer's response to the broken API was to fork (adoption audit), and the contribution model's rejection of the consumer's solution sealed the fork's permanence (governance audit). The recommendation isn't "fix the token tier" or "redesign the Button API" or "accept the contribution"; the recommendation is the architectural restoration that addresses all four lanes simultaneously, with the sequencing that makes the restoration possible.

Audits that report lane-by-lane and stop there miss the architectural diagnosis. Audits that read across lanes and report architectural patterns produce the diagnostic value the senior auditor's experience earns. Our report template (per §4) reserves the cross-lane patterns section as a distinct part of the report for exactly this reason.

---

## 3. Audit-as-deliverable — the productised audit engagement

We run audits inside Discovery routinely. The productised audit — a standalone, sellable engagement with a defined shape and price — is a different artefact, and the practice's strongest single entry-point opportunity into any DS-mature client. The under-investment is structural; closing it is the single highest-leverage commercial move we can make.

### The commercial rationale

Three properties make the productised audit a uniquely strong commercial offering.

**Audits are the highest-asked-for entry-point engagement.** Clients with mature-enough internal product organisations to have a system in production know they need outside diagnosis. They can articulate the request ("we want an audit of our design system") more easily than they can articulate the request for a multi-month redesign. The procurement weight of an audit (small, time-boxed, defined deliverable) is dramatically lower than the procurement weight of a multi-month engagement; the audit can be authorised at a vice-president's discretion in many organisations, where a six-month engagement requires C-level approval.

**The audit produces the diagnostic that justifies the next engagement.** A well-shaped audit's recommendations include the next engagement's scope. The audit names the architectural work the system needs; the recommendations propose how that work gets done; the executive readout introduces us as the natural partner for the recommended work. Conversion from audit to follow-on, when the audit is well-shaped and the follow-on is well-pitched, runs around 40–60% within six to twelve months — substantially higher than cold-start RFP conversion.

**In-house teams cannot self-audit credibly.** The team that authored the system has the most detailed knowledge of its construction and the worst position to read it as a whole. The senior in-house practitioner can audit components and tokens; they cannot audit the system's *architectural premises* against a frame outside the team's own. The agency auditor's outside-frame is the audit's distinctive value; the in-house equivalent would require hiring a senior outside practitioner to audit, which is what an agency engagement is. The audit is a service we uniquely supply.

The under-investment is structural. Most agency DS practices are organised around delivery work; the audit's productisation requires investment that doesn't directly serve any single engagement (methodology authoring, report template, build-time scan tooling scaffold, senior-practitioner training in the audit's shape). The investment is small (40–80 hours of senior time) but the practice has to authorise it as a sales investment, not as billable engagement work.

### The pre-engagement

A useful audit begins before the audit's first day. The pre-audit half-day to one-day sets the audit's scope and prevents day one from being consumed by orientation.

The pre-engagement maps: the system's surface (web only / web + native / web + native + multi-brand / multi-platform with custom integrations); the system's age and maturity (greenfield / 1–3 years / 5+ years); the system's authoring tools (Figma + Tokens Studio + Style Dictionary is the canonical 2026 stack; deviations shape what the audit can scan); the team that maintains it (allocated individual / dedicated team / federated — per 00e §3 the agency-side practitioner-count arc); the stakeholder surface (one product team / multi-product / enterprise); and **the executive surface** — who funded the audit, what's at stake politically, what the audit is being measured against. An audit funded against a "we're considering replacing the system" frame is shaped differently than one funded against "we want to scale to a new acquisition." The pre-audit discovery includes a 30-minute conversation with the executive sponsor; without it, the executive readout is vibes-based.

### The day-by-day shape of a 5-day audit

The 5-day shape is the canonical productised offering. Variants for 3-day (greenfield, single-platform, single-brand) and 10-day (enterprise, multi-platform, multi-brand) extend the shape proportionally.

**Day 1 — Orientation and stakeholder interviews.** Kick-off (60 minutes); access provisioning (Figma, codebase, build pipeline, analytics); pre-scan setup (the build-time scan tooling deployed; results stream in by mid-day). Three to six stakeholder interviews at 30–45 minutes each: the client DS lead, one or two product-team designers and engineers (consumers), the executive sponsor (the funder), a recent contributor from outside the system team (the federation signal), the most-recent escalation contact (where the system most recently failed or was contested).

**Day 2 — Foundation and component sweep.** Token audit in the morning: dependency-graph traversal, dead-token scan, literal-value scan, contrast-pair coverage matrix, DTCG conformance read, cross-platform output integrity check. Component sample audit in the afternoon: 15–25 components depending on system size, biased toward the most-consumed (per the adoption data partially available by mid-day), the most-recently-shipped (the system's current direction), the most-contested (the recent escalation references), plus 2–3 random (anti-bias).

**Day 3 — Specialised lanes and governance.** Accessibility audit in the morning — WCAG conformance grid for the sampled components; the four-engine × four-AT testing for the most-consumed (typically 5–10 components); ARIA APG conformance read for composite widgets; focus-management testing; user-preference media-query testing. Content audit in the early afternoon. Code audit in the late afternoon (where in scope) — build pipeline, CI gates, test coverage, semver pattern, docs freshness. Governance interviews — the contribution-model lead, the deprecation lead, the governance-body chair.

**Day 4 — Adoption audit and cross-lane synthesis.** Adoption audit in the morning: the build-time scan results matured (the scan completes overnight typically); per-team adoption-rate disaggregation; per-component usage distribution; detached/forked count; the self-report-vs-reality gap from the stakeholder interviews. Cross-lane synthesis in the afternoon — the senior auditor reads across all eight lanes' evidence and identifies the architectural patterns. The patterns become the headline diagnostic. Reporting draft begins.

**Day 5 — Report finalisation and the executive readout.** Report finalisation in the morning. Executive readout in the afternoon (60–90 minutes) — the audit lead presents the headline diagnostic, walks through the top 5–10 findings with their commercial framing, and proposes the recommended next steps.

The 5-day shape is intense. Senior auditors run two to three of these in a quarter and treat each as a substantial sustained-attention engagement. The model that works pairs the senior auditor with mid-level practitioners — the senior owns the synthesis and the readout; the mid-level owns the evidence collection and the per-lane findings; the lane-by-lane work parallelises across the team while the senior moves through stakeholder interviews and pattern reading.

### Team mix and roles

The 5-day audit's typical team mix is three to four people; the 10-day enterprise audit extends to five.

- **DS lead / audit lead.** Drives the engagement, runs stakeholder interviews, owns cross-lane synthesis, presents the executive readout. The senior practitioner with the deepest pattern catalogue. The lead's billable rate is the audit's largest single line item; the most senior available practitioner is the right call.
- **Senior DS designer.** Owns the design-side lanes — token (with the engineer's tooling support), component, accessibility-design, content, motion-design.
- **Senior DS engineer.** Owns the engineering-side lanes — code, build pipeline, CI gates, accessibility-implementation (real AT testing infrastructure, automated scanning), build-time scan tooling deployment. The engineer's tooling work is what makes the census-mode lanes possible inside the time budget.
- **Design technologist (where staffed).** The cross-tooling sweep — Tokens Studio audit surface, Storybook health, Code Connect coverage, Figma Variables conformance, the design-tool-to-code seam. Most useful where the tooling stack is non-canonical or where the seam is the audit's likely failure point.
- **Senior accessibility specialist (fractional).** Augments the a11y lane for regulated-industry audits — financial services under EAA exposure, US federal procurement under Section 508, healthcare under ADA Title III. Day 3 mostly; the report's regulatory section.

### Pricing and commercial range

Agency-scale productised audits price as of mid-2026:

- **3-day audit (greenfield, single-platform, single-brand).** $25k–$45k. Limited scope; team of two; deliverable is the executive summary and the dashboard plus a focused report (15–40 pages).
- **5-day audit (canonical mid-engagement).** $50k–$80k. Full scope; team of three; full deliverable surface.
- **10-day audit (enterprise, multi-platform, multi-brand).** $90k–$150k. Extended scope; team of four to five; full deliverable surface plus per-platform-and-per-brand sections.

Pricing varies materially by region and agency tier. The signal that matters more than absolute level is the audit's *position relative to follow-on engagement size* — an audit priced at 5–15% of the expected follow-on is in the right ratio. Lower than that, and the audit doesn't recover its sales-investment cost; higher than that, and the audit becomes a barrier to the follow-on.

The commercial discipline at sale: **the audit is sold *with* a clearly named follow-on path.** Not "audit, then we'll see"; rather, "audit (here's the shape and the deliverable), and based on the audit's findings, the recommended next engagement is in this range and shape." The conditional nature is honest (the findings might recommend a smaller follow-on, or no follow-on); the named pathway is what makes the commercial logic work.

### The deliverable surface

Three artefacts, each with a distinct audience.

**The full audit report (50–200 pages).** The complete document — lane-by-lane methodology, per-lane findings with severity / evidence / recommendations, the cross-lane patterns section, the recommendations organised in three priority bands, the appendix with raw evidence (token-audit output, per-component findings, per-page coverage scan, interview log). Audience: the practitioner — the client DS lead and the senior practitioners who will execute against the recommendations. The report is a working document; it survives the engagement as the reference for the system's next year.

**The executive summary (10–20 pages).** The headline diagnostic in two paragraphs and a list. The top 5–10 findings with their commercial framing. The recommended next steps in three priority bands (now / next / later). Audience: the executive sponsor; the practitioner reads it as the report's introduction. The summary is what travels in slide decks, in Slack threads, in the client's executive readouts. Most executives read only the summary; the audit's commercial framing has to land here.

**The audit dashboard (single-page or one-screen).** The per-lane health score (a structured rubric, not a vibe), the per-finding severity distribution (Critical / High / Medium / Low counts), the headline recommendations ranked. Audience: everyone — the executive who wants the at-a-glance, the practitioner who wants the priority signal, the next-engagement scoping conversation that needs an artefact to point at. The dashboard travels to LinkedIn posts, conference talks, our own case-study library.

The three artefacts are companion-pieces. The senior auditor authors the executive summary and the dashboard; the rest of the audit team contributes the per-lane sections of the full report.

---

## 4. Audit reporting templates and the buy-in surface

The audit report is the engagement's lasting artefact. The senior practitioner can hand-write a strong report once; the productised audit needs a *template* that holds the shape across engagements without anchoring on the senior's voice. The template is the practice's intellectual asset; each engagement's report is a particularisation of it.

### The template

Six sections, in order.

**Executive summary (10–20 pages).** Opens the report. The audit's headline diagnostic in two paragraphs. The top 5–10 findings with their commercial framing — each finding answers "so what?" in language the executive uses (speed to market, risk mitigation, developer velocity, resource utilisation). The recommended next steps in three priority bands. The summary is self-contained; an executive who reads only the summary should land on the audit's full diagnostic and recommendations.

**Methodology statement.** What the audit examined (per-lane scope), what evidence was collected, what wasn't examined and why, what assumptions the audit makes about the system's surface and consumer base. The statement is the audit's authority anchor against the engineering lead's specifics; it reads as professional and verifiable. The common failure is methodology statements written as defensive boilerplate (full of caveats and limitations); the discipline is to write methodology statements that read as confidence-grounded specificity.

**Per-lane findings.** For each lane in scope: a one-paragraph health summary; the lane's health score (a structured rubric — see below); the top findings, each with a title / description / evidence section citing specific instances / severity / estimated effort / recommended owner. The structure is consistent across lanes; the consistency is what makes the report navigable. A reader looking for "what did the audit find about adoption" should find the same shape they found in the token section.

**Cross-lane patterns.** The audit's diagnostic value lives here. Findings visible only across lanes; architectural failure modes that compound across multiple lanes; the patterns the practice recognises from prior engagements. Each pattern has a title (the architectural diagnosis), the constituent findings (which per-lane findings combine), the consequence (what happens if the pattern persists), and the recommendation (what the architectural restoration looks like).

**Recommendations.** The audit's "now / next / later" framing. Each recommendation has a defined scope (what the work covers), a recommended team mix (who does it), a rough effort estimate (in weeks or months), a commercial framing (why this matters in the executive's language), and a named relationship to the findings (which findings the recommendation addresses). The recommendations section is the bridge to the next engagement; the recommendations' phrasing is what holds the bridge.

**Appendix.** Methodology details (the rubric per lane); raw evidence (component-by-component findings, token audit output, the per-page coverage scan); the interview log. The appendix's audience is the practitioner who will execute against the recommendations; the depth here is what makes the report a reference document beyond the engagement's end.

### The severity model

A four-tier severity, applied consistently across the lane findings.

| Severity | Definition and impact threshold | Remediation priority |
|---|---|---|
| **Critical** | Blocks release; blocks accessibility conformance (legal risk); breaks brand integrity; blocks regulated-industry compliance | Immediate / blocker. Current sprint. |
| **High** | Significant consumer-visible issue; governance failure; architectural decision that will break under the next major change | High priority. Next release cycle. |
| **Medium** | Quality concern; technical or visual drift; localised failure mode that will compound over time | Backlog prioritisation. Standard maintenance. |
| **Low** | Minor inconsistency; naming convention violation; polish item without operational impact | Technical debt log. Opportunistic. |

The discipline that produces credible severity grades is to *state the rubric explicitly* in the methodology statement and *test each finding against the rubric* before assigning severity. The most common failure is severity-grade inflation — every finding gets graded High or Critical because the auditor wants to convey urgency. Inflation costs the report its authority; an executive looking at 47 Critical findings concludes either that the system is irreparable or that the auditor is exaggerating, and either conclusion damages the engagement.

A useful discipline: **target a roughly bell-shaped severity distribution.** A typical mid-engagement audit produces 2–8 Critical findings, 10–25 High findings, 30–60 Medium findings, and as many Low findings as are worth recording. The bell-shape is itself a credibility signal; reports that depart from it should justify the departure in the methodology statement.

### The "62 shades of gray" framing

The audit's strongest single buy-in tactic is *quantifying the visible consequence of the inconsistency.* The canonical reference is UXPin's audit story, attributed to Marcin Treder, that surfaced "62 shades of gray" in a single product's interface — a finding that required no expert-level interpretation, generated executive-level recognition, and carried the audit's authority into the budget conversation.

The technique generalises. Count the literal values the system has accumulated for any single semantic role, and report the count as the headline finding. Number of distinct grey hex values. Number of distinct button heights. Number of distinct heading sizes. Number of distinct error-message phrasings. Number of distinct loading-state implementations. The phrasing is concrete enough that the executive can recite it back unaltered. "Our system has 62 shades of gray" survives meeting transcripts, slide decks, and Slack threads in a way that "the system's colour-tier discipline has lapsed" doesn't.

The audit report should generate at least one such finding per engagement. The senior auditor's discipline is to *look for the finding actively* during the audit, not to settle for whatever surfaces; the count is rarely the highest-severity finding, but it's almost always the highest-traction finding.

The pattern extends to *quantifying variance against intent.* How many "primary" buttons (the brand says one; the system has shipped four). How many "blue" colours (the brand says one shade; the system has eleven distinct blues across surfaces). How many "loading" states (the system has nineteen distinct loading-state implementations across components). The variance against intent is the finding's grip; the executive recognises the gap between the brand's stated identity and the system's accumulated reality.

A second buy-in tactic that complements the first: **the cost framing.** Each finding's severity is paired with an effort estimate; the executive reads cost-of-fix against cost-of-not-fixing. The audit's most-recommended finding is the one where cost-of-fix is small and cost-of-not-fixing compounds. The senior auditor identifies these "high-leverage" findings explicitly in the executive summary; they become the audit's strongest commercial argument for the follow-on engagement.

### The recommendations format

Every recommendation has a *commercial framing* the audit lead has explicitly written. The framing translates engineering or design language into commercial consequence.

| Engineering language | Commercial framing |
|---|---|
| "Token tier consolidation" | "The architectural change that prevents the next rebrand from costing six months of redesign" |
| "Component API standardisation" | "The discipline that lets new product teams adopt the system in two weeks instead of six" |
| "Contribution-model overhaul" | "The change that turns the design system from a bottleneck into the company's leverage point on every product release" |

The framing is not marketing — it's translation. The recommendation's content is the same; the language reaches a different audience. The audit lead authors each recommendation's framing during the report's writing; the translation is the audit's commercial work.

A second discipline: every recommendation is *scoped against a possible follow-on engagement.* Not "do this work somehow"; rather "this work, in this shape, with this team, in this duration, against this commercial range." The scoping is honest — the audit's recommendations are our natural follow-on; the conditional sales path is named explicitly — and the scoping is what makes the recommendation actionable. An executive reading a vague recommendation can't act; an executive reading a scoped recommendation can authorise the next engagement.

### Common reporting failure modes

Six reporting patterns recur as failures across agencies.

- **The "everything is Critical" report.** Severity-grade inflation; the report loses authority. Fix: enforce the rubric; aim for the bell-shaped distribution.
- **The "we found 500 things" report.** The executive can't act; the recommendations are buried in detail. Fix: the executive summary's top-5–10 discipline; the appendix carries the long tail; the report's main body is the architectural diagnosis.
- **The "deep on one lane, silent on others" report.** The audit reads as a sales pitch for the lane the agency wants to scope. Fix: the methodology statement names the lane scope explicitly; the report's per-lane structure is consistent across lanes; the recommendations span lanes proportionally.
- **The "no executive summary" report.** The executive reads the first 5 pages and stops. Fix: the executive summary is a required template section; the senior auditor authors it.
- **The "vague recommendations" report.** "Modernise the token system" doesn't survive procurement scrutiny. Fix: every recommendation is scoped; every scope is procurement-actionable.
- **The "we said this last time" re-audit report.** When the audit is a re-audit, the report has to read the *delta* — what's changed, what's been addressed, what's regressed, what's newly surfaced. Reports that re-state the prior audit's findings without acknowledging the elapsed work read as bureaucratic; reports that explicitly track delta read as professional and buyer-respecting.

---

## 5. Continuous audit and drift detection — auditing in CI, not just at engagement start

The point-in-time audit is the practice's productised diagnostic. The continuous audit is the operational discipline that runs in the system's CI pipeline and prevents the system from accumulating the architectural debt the next point-in-time audit would surface. The two are complements, not substitutes; we ship both as distinct offerings, and the productised audit's recommendations almost always include "stand up the continuous-audit pipeline" as a first-priority follow-on.

### What runs in CI

A mature continuous-audit pipeline ships eight surfaces in the system's CI, with a ninth aspirational surface emerging as of mid-2026:

- **Visual regression at the component level.** Chromatic, Percy, Playwright with snapshot comparison. Each component PR runs a visual diff; unexpected diffs require explicit acknowledgment. Catches state-completeness regressions, theme-application regressions, layout regressions, font-loading regressions.
- **Visual regression at the token level.** On every primitive change, CI renders the system's component set against the token tree; the visual diff flags downstream effects. Per 24's cross-brand-drift framing — at portfolio scale this is the mechanism that surfaces brand drift from one team's "small primitive change" propagating across the brand portfolio.
- **Automated accessibility scanning.** axe-core or Pa11y running against every component story. Catches missing ARIA roles, contrast-pair regressions on automated cases, heading-hierarchy issues, label-association issues. Doesn't substitute for the four-engine × four-AT testing the productised audit performs; catches the easy wins.
- **The Cascade Report** (per 24 §3). On primitive changes, CI generates the per-brand and per-component impact report. The artefact is the conversation-starter for the governance review.
- **Dead-token detection.** Build-time scan for tokens no consumer references; the scan output is appended to every release. The dead-token list is the deprecation candidate list.
- **Literal-value-in-component-CSS detection.** Build-time scan for component-level CSS that hard-codes a value the token system should supply. Each occurrence is flagged; the team's PR review treats new occurrences as contribution-model failures.
- **Component coverage scan.** Build-time scan for component-instance counts, component-version-in-use, and detached/forked instances. Feeds the adoption audit; published to the drift dashboard.
- **Contrast-pair validation.** On theme or token changes, validate every WCAG-mandated contrast pair across every theming dimension. PR is blocked on regressions to existing pairs; new pairs are flagged for review. Per 31's color-systems framing — this is what continuous validation prevents the contrast-pair-decay pattern from happening.
- **Storybook-and-docs freshness check.** On component or API changes, validate that the component's Storybook story and docs page were updated in the same PR (or a paired follow-up within a stated SLA). Per 04 / 29 / 30 for the documentation surface; the freshness check is the discipline that prevents the docs-vs-source drift.
- **AI-readability validation (aspirational, mid-2026).** Per 25 / 26 / 27 / 30 — the components-as-data structure validated for AI-agent consumption. Validation runs against a canonical prompt set ("how would an AI agent describe how to use this component") and flags regressions in machine-readability. Supernova's "AI-ready design systems" positioning points at this; the tooling is custom and varies per practice as of mid-2026.

### The drift dashboard

The CI signals aggregate into a single artefact: the drift dashboard. Audience is tripartite.

- **The DS team.** The dashboard is the team's operational signal — what's drifting, where regressions are landing, where coverage is decaying. The team reads the dashboard at the start of each sprint and at the end of each release.
- **The executive coalition.** The dashboard is the sponsorship signal — the system's health number, refreshed on every release, presented at quarterly executive readouts. The executive doesn't need the per-lane detail; they need the trend (rising / plateaued / falling) and the headline.
- **The audit-engagement client.** The dashboard is the artefact the productised audit refreshes. An audit engagement that begins against an existing drift dashboard starts at hour one with the lane evidence largely available; the audit's value shifts from evidence collection to architectural synthesis.

The dashboard's shape: a single page or single screen, per-lane health score, lane-level trend (week-over-week, month-over-month), top recent findings, open-issue count. The aesthetic is the same discipline as a financial or operations dashboard — clarity, consistency, signal-over-noise.

The practice that ships the drift dashboard as a default deliverable on every engagement past Stage 2 (per 00e §3's practitioner-count arc) has the audit's work mostly done before the audit engagement starts. The dashboard is also the most-leverageable artefact for the post-handoff retainer relationship — the retainer pays for the dashboard's maintenance and the quarterly governance review that reads it.

### The governance review's relationship to continuous audit

The quarterly governance review (per 08) is the human surface above the continuous-audit signal. The review reads the dashboard, decides what to escalate, decides what to deprecate, decides what to recommend.

Without the continuous-audit substrate, the quarterly review is vibes-based — the team's read of how the system is doing, with whatever evidence happens to be at hand. The vibes-based review's discipline depends entirely on the senior practitioner running it; a strong senior produces strong reviews, a weak senior produces drift.

With the substrate, the review is signal-driven — the dashboard's data anchors the conversation, the per-lane trends are visible, the recent regressions are traceable. The substrate-driven review compounds the system team's effective seniority; it lets a mid-level practitioner run a credible review by reading the dashboard with the senior's prior coaching.

### The tooling reality in 2026

The continuous-audit surface is not unified. We assemble it from multiple tools.

- **Visual regression.** Chromatic (the most-used as of mid-2026 in the Storybook-centric workflow); Percy (BrowserStack-owned; mature but losing share to Chromatic); Playwright with snapshot comparison (open-source; the choice for non-Storybook workflows).
- **Automated accessibility.** axe-core (the canonical scanner; ships in axe DevTools, Storybook's a11y addon, Chromatic's a11y feature, Pa11y, Lighthouse); Pa11y (CI wrapper); Lighthouse (a reduced ruleset).
- **Token surface.** Style Dictionary's audit features (v4 and onward); Tokens Studio's audit features (the Inspector, the design-tool-side audit); custom dependency-graph traversal where the system has matured beyond off-the-shelf tooling.
- **Coverage scanning.** Custom build-time scans (the senior DS engineer's per-engagement work); the practice's compounding scaffold accelerates each successive engagement.
- **Drift dashboards.** Custom (most common; built on the practice's preferred dashboard surface — Notion, Linear, Looker, Grafana, or a custom internal dashboard); Knapsack and Supernova ship dashboard features with partial coverage; Backlight (Workleap-owned as of 2024) ships limited surfaces.
- **Unified vendor offerings.** Knapsack, Supernova, and Backlight are the closest as of mid-2026, with overlapping feature sets and gaps. None covers the full continuous-audit surface; choosing one as the platform should expect to fill gaps with custom tooling.

Our leverage is the *integration discipline* — the senior DS engineer who can stand up the integrated surface in 40–80 hours is the highest-leverage practitioner on the team for engagements past Stage 2. The integration is not a one-time cost; it requires ongoing maintenance as the underlying tools evolve. The practice that treats the integration as a one-time deliverable produces a pipeline that decays; the practice that treats it as a maintained artefact produces a pipeline that compounds.

### Where continuous audit fails silently

Five failure modes are routine and worth naming.

- **Tooling drift.** The audit scripts haven't been run against the latest tooling release; the scripts produce false negatives because the tooling has changed.
- **Coverage drift.** New components don't get their Storybook stories, so visual-regression coverage decays; the system grows but coverage shrinks proportionally.
- **Threshold drift.** Contrast-pair validation thresholds were set against WCAG 2.1 and haven't been updated to 2.2; the validation runs but doesn't catch 2.2-only criteria.
- **Naming drift.** Tokens were renamed (or aliases were re-routed); the dead-token scan didn't update its catalogue; tokens flagged as "dead" are actually live under their new name.
- **Acknowledgment drift.** Visual-regression diffs require explicit acknowledgment; over time, reviewers acknowledge changes without genuinely reviewing them. The signal degrades because the human review degrades.

The **"audit-the-audit" discipline** — quarterly review of the continuous-audit pipeline itself — is rarely articulated in the field's literature and routinely needed. Our productised audit's recommendations almost always include the audit-the-audit cadence as a first-priority operational hygiene item; the practice that ships the audit-the-audit cadence as a retainer offering produces the most reliable continuous-audit substrate across engagements.

---

## 6. The Discovery triad — audit, Six Signs, maturity diagnostic

The three Discovery diagnostics — **Six Signs** (the recognition diagnostic: is this a system rather than a UI kit?), **maturity diagnostic** (the trajectory diagnostic: where on the curve), **audit** (the current-state diagnostic: what's the system's actual health) — form a triad we ship piecemeal but should ship as a unified Discovery deliverable. The three reinforce each other in ways the field's audit literature mostly doesn't articulate.

### Six Signs as the qualifier

Six Signs (or our equivalent recognition criteria — variously named across practices as the "DS recognition test," the "system vs. UI kit diagnostic") answers the qualifier question: *is what we're auditing actually a system, or a UI kit being called a system?*

The recognition criteria converge on roughly six signs:

- **Tokens-as-architecture.** Multi-tier token tree consumed by both design and code as source-of-truth across surfaces. Not: "we have some named colours in Figma."
- **Components-as-contract.** Components have stated APIs; APIs are consistent across components; APIs ship behavioural contracts (focus, keyboard, AT semantics, motion). Not: "we have Figma components and React components that look like each other."
- **Governance-as-protocol.** Stated contribution model; the model operates (velocity metrics show contribution happening); deprecation discipline is real (items have been deprecated and removed). Not: "we have a Slack channel where people ask about the design system."
- **AT-as-stakeholder.** Accessibility shipped as a system contract, not as a per-component conformance afterthought. Token tree includes contrast pairs; components ship ARIA semantics; the system runs real AT testing. Not: "we ran axe-core once."
- **Multi-surface coverage.** More than one surface — multiple platforms, multiple brands, multiple product teams. Architectural decisions reflect the multi-surface reality. Not: "we have a Figma library for one product."
- **Intentional cross-engagement compounding.** Decisions made with the next year's surface area in mind, not just the current sprint's. Architectural choices reflect long-horizon thinking. Not: "we shipped what the current product needed."

Six Signs answers binary in practice — either the system has the architectural foundations or it has the appearance of a system without them. The diagnostic's value is the binary clarity; "you have a UI kit being called a design system" is a useful diagnosis even when the team rejects it, because the diagnosis names what the next engagement has to address.

If the answer is "UI kit," the audit's shape changes. The diagnostic isn't "here's the state of the system you have"; it's "here's what's missing to make this a system." The audit becomes a roadmap-to-system rather than a state-of-system report. The lanes still apply, but the lane findings are framed against the absence of the foundation rather than the operation of it. The recommendation is the foundation work, sequenced and scoped against the team's commitment.

### The maturity diagnostic as the trajectory

The maturity diagnostic answers: *given that this is a system, where on the maturity curve is it, and what's the next stage's challenge?* The reference frame we use is Sparkbox's four-stage model:

- **Version One.** The system exists. Foundations partially in place; component coverage small; governance informal; adoption starting.
- **Growing Adoption.** The system has consumers; coverage growing; contribution model starting to operate; the system is becoming load-bearing.
- **Surviving Teenage Years.** The system has accumulated technical debt; governance is contested; adoption is plateauing; the system is at risk of being replaced.
- **Evolving.** The system has survived the teenage years; governance is mature; adoption is widespread; the system is the organisation's load-bearing infrastructure.

(Sparkbox's canonical writeup is the verification path; the model's specifics may have evolved since first publication.)

Other frames exist (Curtis's stages model; the InVision *Design Systems Handbook*'s four-stage frame; the field's various "DS maturity" assessments). We pick a frame and apply it consistently; the frame's specific shape matters less than the consistency.

The agency-side variant of the curve (per 00e §3): Stage 0 (no DS practitioner) → Stage 1 (Part Timer) → Stage 2 (Allocated Individual) → Stage 3 (Dedicated Team) → Stage 4 (Embedded Multi-Team). At our scale the team's stage is the system's surrogate; the agency's maturity diagnostic reads the team and the system together.

The maturity diagnostic calibrates the audit's expectations. A Version One system audited against an Evolving system's standards is unfairly judged — the foundations aren't expected yet; the audit's findings should focus on the next stage's challenge. An Evolving system audited against a Version One's standards is under-ambitious — architectural debt has compounded; the audit should be pressing harder on governance and deprecation. Without calibration, the audit's findings are out-of-context.

### The audit as the current-state diagnostic

The audit's eight-lane methodology (per §2) reads the system's current state. *Given that this is a system (Six Signs), at this stage of maturity, here's the actual health.*

The audit's finding-shape depends on the prior diagnostics. A Version One system's audit emphasises foundation work — the token tier, the initial component library, the early governance. An Evolving system's audit emphasises drift and accumulated debt — the literal-value-in-component-CSS findings, the contribution-model fatigue, the dead tokens, the API drift. Same lane methodology; different finding-shapes against different stages.

Recommendations are also stage-calibrated. A Version One system's recommendations are foundation-building; an Evolving system's recommendations are debt-paydown and architectural-restoration. The commercial framing reflects the stage — Version One audits' follow-on engagements are foundation-build engagements; Evolving systems' follow-on engagements are restoration or successor-system engagements.

### How the three reinforce each other

The triad's reinforcement runs in both directions.

**Forward.** Six Signs shapes the audit's lane priorities — a system without a token tier doesn't audit alias resolution; a system without governance doesn't audit contribution-model operation. The maturity diagnostic shapes the audit's expectations — greenfield systems aren't audited for federated-contribution health. The audit produces stage-calibrated findings.

**Backward.** The audit's findings refine the maturity diagnostic. A system claims to be Evolving; the audit shows the contribution model isn't operating, the dead-token count is at 30%, per-team adoption is below 25% — the system is actually still in Surviving Teenage Years (or has regressed there). The audit's evidence corrects the self-perception; the corrected diagnostic feeds the next engagement's commercial framing.

**Cross-cutting.** The audit's findings sometimes surface a Six Signs gap. A system that claims systemhood but whose audit shows literal values consumed without semantic-tier mediation, contributions handled by ad-hoc Slack, accessibility handled by automated scanning only, and adoption tracked by self-report — the audit's diagnosis is "this is a UI kit being called a system." The Six Signs result was wrong; the audit corrects it. The recommendation is foundation work, framed against the team's likely resistance to the diagnosis.

The three diagnostics are read together; the Discovery report integrates them. The integrated read is the audit's most-leverageable single artefact.

### The unified Discovery deliverable

We ship one Discovery report that integrates Six Signs, maturity, and audit into a single read.

**Opening section: the system's framing.** Six Signs result; maturity diagnostic; the audit's headline diagnostic. Five to eight pages; reads as the report's frame.

**Middle section: the audit's body.** The eight-lane findings (per §2); the cross-lane patterns (per §4); the per-lane health scores. The bulk of the report (40–150 pages depending on system surface area).

**Closing section: the next-engagement recommendation.** Recommendations calibrated against the maturity stage; the engagement's shape (Discovery + foundation work for Version One; foundation work + adoption support for Growing Adoption; debt paydown + governance overhaul for Surviving Teenage Years; succession planning + new-platform expansion for Evolving). Five to ten pages; reads as the bridge to the follow-on.

The unified report is our highest-leverage Discovery artefact. It is also the artefact most agencies don't ship, because the three diagnostics are typically run by different practitioners on different timelines and the integration is treated as an after-the-fact pulling-together rather than a designed-as-one deliverable. Our commercial and intellectual leverage is to design the unified deliverable as one product.

### The commercial framing of the unified deliverable

A productised Discovery + audit engagement (5–10 days, $50k–$120k typical) is the strongest single sellable artefact we can ship. Three properties drive its commercial leverage.

**It produces the diagnostic that justifies the next engagement.** The recommendations section names the follow-on engagement's shape, scope, and commercial range. The executive who reads the Discovery report can authorise the next engagement against the report's recommendations.

**It carries the executive surface that the larger engagement requires.** The Discovery engagement builds the executive coalition. The 5–10 day engagement includes 60–90 minutes of executive readout; the readout is our introduction to the executive sponsorship surface. Multi-month follow-on engagements that begin with the executive coalition already in place run substantially smoother than engagements that have to build the coalition from scratch.

**It positions us as the practice that *thinks* about systems rather than just builds them.** The Discovery report's diagnostic depth — Six Signs + maturity + audit, integrated and stage-calibrated — is intellectual work. Agencies that ship this work signal a level of practice maturity that delivery-only agencies can't match. The signal is our competitive positioning at the next RFP; the signal compounds across engagements.

The under-investment is structural and worth naming explicitly. Most agencies treat Discovery as a low-margin lead-in to higher-margin delivery; the Discovery engagement is priced cheaply, run quickly, delivered without the polish the productised version would receive. The result is a Discovery output that doesn't carry its commercial value into the follow-on. The practice that invests in Discovery's productisation — that makes the Discovery engagement a premium, polished, intellectually-rigorous deliverable — converts at higher rates and at higher follow-on engagement values than the practice that under-invests. The investment is small (methodology authoring, report template, integration discipline, senior-practitioner training); the return is the practice's pipeline of larger engagements behind every Discovery.

We have the IP. The under-investment is a strategic gap, not a capability gap. Closing it is the highest-leverage commercial move available to the practice in the audit territory.

---

## See also

- 00b — Agency Context (audit-first inherited engagements; the engagement patterns that produce audit-shaped Discovery work)
- 00d — Commercial Model (the productised audit's pricing and the unpriced run-phase retainer the audit's recommendations flow into)
- 00e — Team and Discipline (the practitioner-count arc as the maturity-curve agency variant; the senior-practitioner team mix the productised audit demands)
- 01 — Discovery and Strategy (audit activities at the engagement-architecture level; Six Signs as the qualifier)
- 04 — Documentation (the documentation-freshness lane in the code audit; the team-voice question audit findings often surface)
- 07 — Governance and Adoption (the governance audit's contribution-model lane; the contribution-vs-participation distinction)
- 08 — Ongoing Maintenance (the quarterly governance review as the human surface above the continuous-audit signal; the retainer shapes the audit's recommendations populate)
- 23 — Typography Tokenisation (the under-tokenisation patterns the typography audit surfaces)
- 24 — Tokens at Scale (the Cascade Report; the cross-brand drift the visual-regression-at-the-token-level lane catches; the multi-collection-not-multi-mode architecture the token audit reads)
- 28 — Web Accessibility Implementation (the four-engine × four-AT testing matrix; the user-preference media-query surface; the ARIA APG composite-widget pattern conformance)
- 29 — Per-Component Documentation Template (the per-component documentation surface the docs-freshness check validates)
- 30 — Generated-from-Data Documentation (the docs-platform freshness; the AI-readability validation as the ninth aspirational continuous-audit lane)
- 31 — Color Systems (the contrast-pair-decay pattern; the WCAG-passes-but-fails-real-users pattern; the contrast-pair coverage lane)

---

## Provenance

This file synthesises a 2026-06-17 dual-agent run on auditing-as-a-discipline (`_research/_inbound/2026-06-17-auditing-design-systems/`). Both agents converged on the agency-vs-in-house structural framing, the eight-lane methodology with the same lane definitions and sub-points, the heuristic-vs-specification-vs-census mode distinction, the cross-lane diagnostic example (token bypass → API drift → consumer fork → contribution-model rejection — both passes arrived at the same canonical illustration independently), the audit-as-deliverable productisation with the same 5-day shape and three-artefact deliverable surface, the six-section reporting template with the same four-tier severity model, the "62 shades of gray" buy-in framing, the five named reporting failure modes, the eight continuous-audit CI lanes plus the "drift dashboard" tripartite audience, the four-failure-mode "audit-the-audit" discipline, and the Discovery triad of Six Signs + maturity + audit as the practice's highest-leverage productised deliverable.

Two artefacts lifted from the external pass: the eight-lane summary table at §2 (Audit Lane / Key Diagnostic Focus / Primary Evidence Source) as a synthesis-ready reference, and the four-tier severity-model table at §4. Specific attributions added from the external pass: Cristiano Rastelli (didoo) for the source-mix-overtime formula at Badoo's Cosmos system in §2.8; Marcin Treder for the original "62 shades of gray" UXPin audit story in §4. From Claude's pass: the eight-pattern recurring-failure-mode catalogue in §1, the bell-shaped severity distribution discipline in §4 (target 2–8 Critical / 10–25 High / 30–60 Medium), the sixth "we said this last time" re-audit failure mode, the fifth "acknowledgment drift" continuous-audit silent-failure mode, the AI-readability validation as the ninth aspirational continuous-audit lane in §5, the stratified pricing across 3-day / 5-day / 10-day shapes in §3, the 40–60% audit-to-follow-on conversion rate, the 5–15% audit-to-follow-on pricing-ratio rule, and the cross-references back to 00e's practitioner-count arc.

Two reconciliations: Sparkbox's maturity-stage names landed as the canonical "Version One / Growing Adoption / Surviving Teenage Years / Evolving" pending source-text verification; the audit-engagement pricing carries Claude's stratification across three engagement lengths in §3 with external's unified $50–120k range integrated into §6 as the Discovery + audit shape.

Several claims stand to gain `_source-text/` backing before they appear in client artefacts; flagged in 09 §1.28a–§1.28d as the next housekeeping pass:

- **§1.28a — Cristiano Rastelli (didoo) at Badoo's Cosmos system.** Verify the source-mix-overtime formula's canonical writeup, capture the calculation specifics, confirm the attribution. Load-bearing for §2.8's adoption-coverage definition.
- **§1.28b — Marcin Treder at UXPin, "62 shades of gray."** Verify the original audit case study's specifics (which client, which year, which exact phrasing), confirm the attribution. The framing is load-bearing for §4's buy-in tactic.
- **§1.28c — Screen-reader market share.** WebAIM's annual screen-reader survey is the canonical reference; verify the most recent figures (the proportions vary year-on-year). The four-engine × four-AT matrix justification in §2.3 leans on this.
- **§1.28d — Supernova's "AI-ready design systems" positioning.** Verify Supernova's published framing if the AI-readability ninth lane in §5 is referenced inline in client work.

These extend the §1.26a–§1.26d cluster from the team-and-discipline run; both can be closed in a single source-text housekeeping pass.
