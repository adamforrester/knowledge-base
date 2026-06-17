You are researching auditing design systems as a discipline — methodology,
audit-as-deliverable, reporting templates, continuous-audit and drift-detection,
and the relationship between audit / Six Signs / maturity diagnostic in
Discovery — for a senior design systems practitioner leading the practice at a
global creative agency. The output is a structured knowledge document that
will be promoted to a numbered file in the practitioner's vault
(`32-auditing-design-systems.md`), positioned as an extension topic alongside
22 (token architecture extensions), 24 (tokens at scale), 26/27 (adaptive
interfaces), 30 (generated-from-data documentation), 31 (color systems).

The practice's existing audit content is fragmented across 17+ files. 01
Discovery names audit activities at the engagement-architecture level. 08
Ongoing Maintenance covers the quarterly governance review with brand-alignment
audit. 11 Mobile and Cross-Platform names the mobile-specific token audit. 12
Figma Practice covers Figma's native linting. 17 Accessibility Annotation
Contract covers annotation-state auditing. 23 Typography Tokenisation surfaces
the under-tokenisation patterns audits typically expose. 25 AI-Aware Patterns
covers the manual-walkthrough-when-Zeroheight-is-closed pattern. 31 Color
Systems names the WCAG-passes-audit-but-fails-real-users pattern. 00b Agency
Context names audit-first inherited engagements. The practice runs audits
constantly; auditing as a discipline of its own — methodology articulated,
deliverable productised, reporting templated, drift-detection automated, and
the Discovery triad (audit + Six Signs + maturity) unified — has not been
written. This file closes that gap.

This is not an introductory guide — assume the reader is the practice lead,
has read 01, 08, 23, 24, 30, 31 in the practice's vault, knows what a token
audit, component audit, and accessibility audit each individually look like,
knows the broader DS field's audit references (Curtis on contribution audits,
Brad Frost's *Atomic Design* audit chapter, UXPin's "62 shades of gray"
framing, Sparkbox's audit case studies, the EightShapes audit posts), and is
fluent in the standard audit vocabulary (heuristic vs. specification audit,
sample vs. census audit, point-in-time vs. continuous audit, governance audit,
drift, cascade analysis, dead-token detection). Don't explain what an audit
is, what WCAG conformance auditing means, what visual-regression testing is,
what a heuristic audit is, what a token audit examines — explain how the
practice should *operate* auditing as a unified discipline, where the field's
audit methods break down at agency scale, what the productisation of the audit
demands commercially and technically, what reporting shape produces buy-in
from non-DS executives, and what the relationship between audit /
Six Signs / maturity diagnostic actually is.

Research scope — cover all of the following:

1. Why this is a DS-architecture concern, not a generic UX audit concern

- The case that "design system audit" is a stable, named methodology — not a
  variant of UX audit, accessibility audit, or front-end code audit. What
  makes a DS audit categorically different from each of those adjacent
  audit forms (DS audits read tokens-as-architecture, components-as-contract,
  governance-as-protocol, and the cross-surface drift signal; adjacent audits
  read pages, screens, conformance against a standard, or codebases-as-code).
- How DS audits get miscategorised at agency scale and what that costs.
  Procurement reading the DS audit as a UX audit and budgeting accordingly;
  client teams expecting a heuristic walk-through and getting an architectural
  diagnostic; the agency lead defaulting to "we'll audit your components"
  when the system needs token-tier and governance-tier diagnostics. The
  miscategorisation costs are real (wrong scoping, wrong team mix, wrong
  output, wrong buy-in).
- Why DS audits compound across engagements and individual UX audits don't.
  A senior DS practitioner who has run twenty audits has a method that
  improves with each one — the failure modes accumulate, the patterns become
  visible, the diagnostic accuracy increases. UX audit findings are
  surface-specific and don't generalise the same way; DS audit findings
  generalise across surfaces because the underlying architecture is
  constant. The agency's compounding asset in audit work is the *audit
  method-IP*, not any specific audit's artefact.
- The audit's authority surface. A DS audit's findings have to be defensible
  against a client engineering lead who built the system, a client design
  lead who has lived with it, and an executive who is paying for the audit.
  The authority is methodological (the audit followed a stated
  methodology), evidential (the findings cite specific instances), and
  framed against the field (industry consensus exists; the system diverges
  here). Audits that read as opinion lose the room; audits that read as
  diagnosis hold it.

2. Audit methodology — the eight audit lanes

- The eight surfaces a comprehensive DS audit examines. Each lane has its
  own methodology, evidence types, scoring rubric, and reporting shape.

  - **Token audit.** Primitive vs. semantic vs. component-tier coverage;
    alias resolution health; multi-mode/multi-collection architecture vs.
    flat token tree; theming dimension orthogonality (mode + density +
    brand + contrast preference as separate axes vs. collapsed); dead-token
    detection; literal-value-in-component-CSS detection (the "the system
    isn't being used here" signal); contrast-pair coverage and resolution;
    DTCG conformance status; cross-platform output integrity. Tooling:
    Style Dictionary or the equivalent build, Tokens Studio's audit
    surface, custom dependency-graph traversal where the system is
    sufficiently mature.
  - **Component audit.** Coverage against the consumer's surface
    (component-by-component visit count vs. consumed-instance count);
    API consistency (props that share semantics across components — `size`,
    `tone`, `disabled`, `loading`); composition-primitive availability
    (Slot, AsChild, render-prop); state machine completeness (every
    component's variants, focus, hover, active, disabled, error, loading,
    empty); API drift (component v1 API vs. component v3 API at the
    primitive level); polyfill detection (consumers wrapping components
    because the API is missing a prop); detached or out-of-system component
    detection.
  - **Accessibility audit.** WCAG 2.2 conformance per component; the
    four-engine × four-AT test matrix coverage; ARIA 1.3 composite-widget
    pattern conformance; focus-management discipline (focus-trap-on-modal,
    roving-tabindex, restore-focus-on-close); contrast pair coverage at
    every theming dimension; user-preference media-query support
    (prefers-reduced-motion, prefers-color-scheme, prefers-contrast,
    forced-colors); the EAA/Section 508 conformance regime where the
    client's regulatory exposure demands it; the WCAG-passes-but-fails-
    real-users pattern (real AT testing as the higher bar). The lane has
    the most-published methodology of the eight.
  - **Content audit.** Voice-and-tone consistency at the system level
    (Mailchimp / Polaris pattern); error-message templates; empty-state
    copy; CTA verb taxonomies; per-component microcopy guidance; ICU
    MessageFormat / pluralisation / gendered-language conformance for
    i18n-shipping systems; assistant tone for AI surfaces (See 25 / 26 /
    27 for the AI-content sub-surface).
  - **Motion audit.** Three-tier motion token coverage (duration, easing,
    composed); choreography vocabulary (entry, exit, transition,
    attention); reduce-motion contract; performance budget (INP-respecting,
    compositor-only animations); cross-platform spring-parameter mapping
    where mobile is in scope. Often the lane that is missing entirely —
    motion-as-foundation maturity is recent.
  - **Code audit.** The system's repository — build pipeline health, CI
    quality gates (visual-regression, automated-a11y, semver automation),
    test coverage at the component level, the docs platform's freshness,
    the package-publish surface; the component implementation against the
    design source; framework-specific integration health.
  - **Governance audit.** Contribution-model operation (request triage,
    SLAs, review-and-merge cadence); contributor distribution (the system
    team vs. product teams); the contribution-vs-participation distinction
    (Curtis); the contribution-criteria-and-scale operation; the
    deprecation discipline; the major-release cadence; the governance
    bodies' meeting cadence and decision quality; the executive-coalition
    surface.
  - **Adoption audit.** Coverage definition (Morningstar's % of pages
    using system components; Veriff's components-in-use across repos;
    didoo's proportion-sourced-from-system); per-team adoption rate;
    per-component usage distribution (the long-tail problem); detached/
    forked component count; the "we use the system" claim vs. the build-
    time scan reality.

- How the eight lanes interact. A token audit surfaces a primitive used
  directly in a component (skipping the semantic tier); the component audit
  confirms the API drift is the consequence; the adoption audit shows the
  product team has forked the component because the API drift was material;
  the governance audit shows the contribution model couldn't accept the
  contribution that would have closed the API gap. The audit's diagnostic
  value comes from reading across lanes, not from any one lane's depth.
- Heuristic vs. specification vs. census auditing. When to walk a sample of
  surfaces with a senior practitioner's eye (heuristic — fast, deep on the
  patterns the practitioner recognises, blind to what they don't),
  when to spec-check every surface against a stated rule set (specification
  — slower, exhaustive, generates a defensible artefact), when to scan
  every consumer (census — only feasible with tooling; expensive but the
  highest-authority output). Real audits are blends; the methodology has
  to state which is being used per lane.

3. Audit-as-deliverable — the productised audit engagement

- The audit as a sellable Discovery deliverable. The practice runs audits
  inside Discovery routinely but does not sell the standalone audit as a
  productised offering. This is the strongest commercial-leverage candidate
  in the practice's named gap stack. The shape: a 3–5 day diagnostic
  engagement; a small dedicated team (DS lead + senior DS designer +
  senior DS engineer; design technologist if the audit reaches the build-
  pipeline lane); a defined deliverable (the audit report + an executive
  read-out); a defined commercial range ($25k–$80k typical for an agency-
  scale engagement; varies with the system's surface area and the lanes
  in scope); a defined hand-off (the audit recommends next steps; the
  client decides whether to engage on those next steps with the agency or
  internally).
- The commercial rationale. Audits are the highest-asked-for entry-point
  engagement. Clients can authorise an audit's budget without the
  procurement weight of a full DS engagement; the audit produces the
  diagnostic that justifies the larger engagement; the agency that ships
  audits regularly produces a pipeline of larger engagements behind them.
  In-house teams cannot self-audit credibly (they are the system's
  authors); the audit is a service the agency uniquely supplies. The
  productisation is the practice's most under-invested sales surface.
- The pre-engagement — what the audit needs to know before it starts.
  The system's surface (web only / web + native / web + native + multi-
  brand); the system's age and maturity (greenfield / 1–3 years / 5+
  years); the system's authoring tools (Figma + Tokens Studio + Style
  Dictionary, or a non-standard chain); the team that maintains it
  (allocated individual / dedicated team / federated); the stakeholder
  surface (one product team / multi-product / enterprise); the executive
  surface (who funded the audit, what's at stake politically, what the
  audit is being measured against). The pre-audit discovery is a half-day
  to a day; without it, the audit's first day is consumed by orientation.
- The day-by-day shape of a 5-day audit engagement. Day 1: orientation,
  stakeholder interviews (3–6 named individuals at 30–45 min each), pre-
  scan setup. Day 2: token-and-foundation audit; component sample audit
  (15–25 components depending on system size). Day 3: accessibility and
  content audit; code audit (where in scope); governance interviews.
  Day 4: adoption audit and the cross-lane synthesis; reporting draft.
  Day 5: report finalisation and the executive read-out (60–90 minutes).
  Variants for shorter (3-day for greenfield) and longer (10-day for
  enterprise multi-brand) engagements.
- The team mix and roles. The DS lead drives the engagement and the
  executive read-out. The senior DS designer owns the design-side lanes
  (token, component, accessibility-design, content, motion-design). The
  senior DS engineer owns the engineering-side lanes (code, build pipeline,
  CI, accessibility-implementation). The design technologist (where
  staffed) owns the cross-tooling sweep (Tokens Studio audit surface,
  Storybook health, Code Connect coverage, Figma Variables conformance).
  The senior accessibility specialist (fractional) augments the a11y lane
  for regulated-industry audits.
- The audit's deliverable surface. Three artefacts. The full audit report
  (50–200 pages depending on system surface; lane-by-lane methodology
  + findings + severity + recommendations; appendix with evidence). The
  executive summary (10–20 pages; the headline diagnostic, the top 5–10
  findings with their commercial framing, the recommended next steps).
  The audit dashboard or scorecard (single-page or one-screen; a per-lane
  health score, a per-finding severity, the headline recommendations
  ranked). The artefacts are companion-pieces; the executive surfaces the
  summary, the practitioners read the report, the dashboard is the artefact
  that travels (Slack, slide deck, exec readout).

4. Audit reporting templates and the buy-in surface

- The audit report shape that produces buy-in. A senior practitioner can
  hand-write an audit report; the practice's productised audit needs a
  template that holds the shape across engagements without anchoring on
  the senior's voice. The template's elements:

  - **Executive summary** — the audit's headline diagnostic, in two
    paragraphs and a list. The 5–10 top findings with their *commercial*
    framing (each finding answers "so what?" in language the executive
    uses). The recommended next steps (in three priority bands: now /
    next / later).
  - **Methodology statement** — what the audit examined (per-lane
    scope), what evidence was collected, what wasn't examined and why,
    what assumptions the audit makes about the system's surface and
    consumer base.
  - **Per-lane findings** — for each lane in scope: a one-paragraph
    health summary, the top findings (each finding has a title, a
    description, an evidence section citing specific instances, a
    severity, an estimated effort to remediate, a recommended owner).
    The lane's health score (a structured rubric, not a vibe).
  - **Cross-lane patterns** — the audit's diagnostic value lives here.
    Findings that are visible only across lanes; the architectural
    failure modes that compound across multiple lanes; the patterns the
    practice recognises from prior engagements.
  - **Recommendations** — the audit's "now / next / later" framing.
    Each recommendation has a defined scope, a recommended team mix,
    a rough effort estimate, a commercial framing, and a named
    relationship to the findings. The practice's audit report is the
    bridge to the next engagement; the recommendations are the bridge's
    explicit form.
  - **Appendix** — methodology details (the rubric per lane); the raw
    evidence (component-by-component findings, token audit output, the
    per-page coverage scan); the interview log (who was talked to, when,
    what surfaced).

- The severity model. Most audits use a four-tier severity (Critical /
  High / Medium / Low) with stated definitions; the practice should
  commit to a single rubric and apply it consistently. Critical: blocks
  release, blocks accessibility conformance, blocks brand integrity,
  blocks regulated-industry compliance. High: significant consumer-
  visible issue, governance failure, or architectural decision that will
  break under the next major change. Medium: quality concern, drift, or
  failure mode that will compound. Low: minor inconsistency, naming
  issue, polish item.
- The "62 shades of gray" framing (UXPin's audit-buy-in pattern). The
  audit's strongest single buy-in tactic is *quantifying the visible
  consequence of the inconsistency*. UXPin's audit famously surfaced "62
  shades of gray" in a single product's interface — a finding that
  required no expert-level interpretation, generated executive-level
  recognition, and carried the audit's authority into the budget
  conversation. The practice's audit reports should *generate at least
  one such finding*: a finding whose phrasing is so concrete that the
  executive can recite it back unaltered. Tactics: count the literal
  values the system has accumulated for any single semantic role
  (number of distinct grey hex values; number of distinct button heights;
  number of distinct heading sizes); count the variance against the
  intent (how many "primary" buttons, how many "blue" colours).
- The recommendations format. Every recommendation has a *commercial
  framing* the audit lead has explicitly written. "Token tier
  consolidation" reads as engineering housekeeping; "the architectural
  change that prevents the next rebrand from costing six months of
  redesign" reads as commercial value. The audit report is the bridge
  to the next engagement; the recommendations' phrasing is what holds
  the bridge.
- Common reporting failure modes. The "everything is critical" report
  (severity-grade inflation; the report loses authority). The "we found
  500 things" report (the executive can't act; the recommendations
  are buried). The "deep on one lane, silent on others" report (the
  audit reads as a sales pitch for the lane the agency wants to scope).
  The "no executive summary" report (the executive reads the first 5
  pages and stops). The "vague recommendations" report ("modernise the
  token system") that doesn't survive procurement scrutiny.

5. Continuous audit and drift detection — auditing in CI, not just at
   engagement start

- The shift from point-in-time audit to continuous audit. The
  point-in-time audit is the practice's productised diagnostic; the
  continuous audit is the operational discipline that prevents the
  system from needing the next point-in-time diagnostic. The two are
  complements, not substitutes. The practice should ship both as
  distinct offerings.
- The continuous-audit surface — what runs in CI:

  - **Visual regression at the component level.** Chromatic, Percy,
    Playwright with snapshot comparison, or the equivalent. Each
    component PR runs a visual diff; unexpected diffs require
    explicit acknowledgment.
  - **Visual regression at the token level.** Render the system's
    component set against the token tree on every primitive change;
    visual diff flags downstream effects. (See 24 §Cross-brand drift
    for the multi-brand application.)
  - **Automated accessibility scanning.** axe-core, Pa11y, or the
    equivalent against every component story. Catches conformance
    regressions at PR time. Doesn't replace real AT testing; does
    catch the easy wins.
  - **The Cascade Report** (per 24 §3). On primitive changes, CI
    generates the per-brand and per-component impact report. The
    artefact is the conversation-starter for the governance review.
  - **Dead token detection.** Build-time scan of the codebase for
    tokens that no consumer references; flagged for deprecation
    review.
  - **Literal-value-in-component-CSS detection.** Build-time scan for
    component-level CSS that hard-codes a value the token system
    should supply. Flagged as a contribution-model failure.
  - **Component coverage scan.** Build-time scan of the consumer's
    code for component-instance counts, component-version-in-use,
    and detached / forked component instances. Feeds the adoption
    audit.
  - **Contrast-pair validation.** On theme or token changes, validate
    every WCAG-mandated contrast pair across every theming dimension.
    Block the PR on regressions.
  - **Storybook-and-docs freshness check.** On component or API
    changes, validate that the component's Storybook story and docs
    page were updated in the same PR. (See 04 / 29 / 30 for the
    documentation surface.)

- The "drift dashboard" as the continuous-audit artefact. A single
  surface that aggregates the CI signals into a per-system health
  score, refreshed on every release. The dashboard's audience is the
  DS team itself (operational signal), the executive coalition
  (sponsorship signal), and the audit-engagement client (the artefact
  the productised audit refreshes). The practice that ships the drift
  dashboard as a default deliverable on every engagement past Stage 2
  has the audit's work mostly done before the audit engagement starts.
- The governance review's relationship to continuous audit. The
  quarterly governance review (per 08 §The quarterly governance
  review) is the human surface above the continuous-audit signal. The
  review reads the dashboard, decides what to escalate, decides what
  to deprecate, decides what to recommend to the executive coalition.
  Without the continuous-audit substrate, the quarterly review is
  vibes-based; with it, the review is signal-driven.
- The tooling reality in 2026. The continuous-audit surface is not
  unified — the practice assembles it from Chromatic + axe-core +
  Storybook + Style Dictionary's audit surface + Tokens Studio's
  audit surface + custom CI scripts + a custom dashboard. No vendor
  ships the unified drift surface; Knapsack and Supernova are the
  closest, with partial coverage. The practice's leverage is the
  *integration discipline* — the senior DS engineer who can stand up
  the integrated surface in 40–80 hours is the highest-leverage
  practitioner on the team for engagements past Stage 2.
- Where continuous audit fails silently. Tooling drift (the audit
  scripts haven't been run against the latest tooling release).
  Coverage drift (new components don't get their Storybook stories,
  so the visual-regression coverage decays). Threshold drift (the
  contrast-pair validation thresholds were set against WCAG 2.1 and
  haven't been updated to 2.2). Naming drift (tokens were renamed and
  the dead-token scan didn't update). The discipline of *auditing the
  audit* — quarterly review of the continuous-audit pipeline itself —
  is rarely articulated and routinely needed.

6. The audit ↔ Six Signs ↔ maturity diagnostic relationship — the
   Discovery triad

- The three Discovery diagnostics — Six Signs (recognition: is this a
  system rather than a UI kit?), maturity diagnostic (where on the
  curve: greenfield / growing / surviving teenage years / evolving),
  audit (current state: what's the system's actual health) — form a
  *triad* that the practice ships piecemeal but should ship as a
  unified Discovery deliverable.
- Six Signs as the qualifier. Curtis's framing (or the practice's
  equivalent recognition criteria — tokens-as-architecture, components-
  as-contract, governance-as-protocol, AT-as-stakeholder, multi-
  surface coverage, intentional cross-engagement compounding). Six
  Signs answers: *is what we're auditing actually a system, or a UI
  kit being called a system?* If the answer is "UI kit," the audit's
  shape is different — the diagnostic is "to become a system, here's
  what's missing"; the audit becomes a roadmap-to-system rather than
  a state-of-system report.
- The maturity diagnostic as the trajectory. The system's stage on
  the curve (greenfield through evolving — Sparkbox's four-stage
  model is a useful reference frame, with the agency-side variant
  per 09 §1.26 / 00e). The maturity diagnostic answers: *given where
  this system is on the curve, what's reasonable to expect, and
  what's the next stage's challenge?* A greenfield system audited
  against an evolving system's standards is unfairly judged; an
  evolving system audited against a greenfield's standards under-
  ambitious. The maturity diagnostic calibrates the audit's
  expectations.
- The audit as the current-state diagnostic. The point-in-time read
  of what the system actually is — the eight-lane methodology output.
  The audit answers: *given that this is a system (Six Signs) at
  this stage of maturity (diagnostic), here's the current state of
  health.*
- How the three reinforce each other. The Six Signs read shapes the
  audit's lane priorities (a system without a token tier doesn't
  audit the alias resolution; a system without governance doesn't
  audit the contribution model's operation). The maturity diagnostic
  shapes the audit's expectations (a greenfield system isn't audited
  for federated-contribution health). The audit's findings refine
  the maturity diagnostic (the system claims to be evolving, but the
  audit shows it's still growing — surfaces the gap between self-
  perception and actual stage). The three are read together; the
  Discovery report integrates them into one diagnostic.
- The unified Discovery deliverable. The practice should ship one
  Discovery report that integrates Six Signs (qualifier), maturity
  (trajectory), and audit (current state) into a single read. The
  report's shape: an opening section frames the system (Six Signs +
  maturity), the body presents the audit (the eight-lane findings),
  the closing section recommends the next engagement (calibrated
  against maturity stage). The unified report is the practice's
  highest-leverage Discovery artefact and is currently produced
  piecemeal.
- The commercial framing of the unified deliverable. A productised
  Discovery + audit engagement (5–10 days, $50k–$120k typical) is the
  strongest single sellable artefact the practice can ship. It
  produces the diagnostic the next engagement is scoped against, it
  carries the executive surface that the larger engagement requires,
  and it positions the agency as the practice that *thinks* about
  systems rather than just builds them. The productisation is
  underweighted; the practice has the IP.

Output format: Structured markdown. Use section headings that match the
numbered scope above. Synthesize findings — do not list sources mechanically.
Where the field has consensus, state it clearly; where decisions are
context-dependent, provide decision frameworks rather than declaring a winner.
Flag where DS audit tooling (Chromatic, Percy, Playwright, axe-core, Pa11y,
Style Dictionary's audit surface, Tokens Studio's audit surface, Knapsack,
Supernova, Backlight, custom build-time scans) has known gaps that
practitioners work around. Flag where the field's audit literature
(EightShapes, Sparkbox, UXPin, Brad Frost, Curtis, the InVision Design
Systems Handbook, conference talks at Clarity / Config / Smashing) breaks down
at agency scale. Where claims depend on current state — tooling versions,
practice patterns at named agencies, named individuals, named conferences,
WCAG version applicability — date them and note the verification path.
Include a references section linking to primary sources (Curtis's EightShapes
catalogue including audit-relevant posts; Brad Frost's *Atomic Design* audit
chapter and his blog audit references; UXPin's audit case studies and the
"62 shades of gray" framing; Sparkbox's audit case studies; the Knapsack
blog's audit-tooling content; the Supernova audit-surface documentation;
axe-core / Pa11y / Chromatic / Percy / Playwright documentation; Style
Dictionary's audit-surface documentation; Tokens Studio's audit surface;
the WCAG 2.2 conformance-evaluation methodology; the W3C ARIA Authoring
Practices Guide for the AT-test methodology; conference talks where the
agency-side audit is a topic).

Depth: Expert audience. Do not explain what an audit is, what WCAG
conformance auditing means, what visual-regression testing is, what a
heuristic audit is, what dead-token detection is, what a component audit
examines — explain how the practice operates auditing as a unified
discipline at agency scale, where the field's audit methods break down
in agency contexts, what productising the audit requires commercially and
technically, what reporting shape produces buy-in, and what the Discovery
triad (audit + Six Signs + maturity diagnostic) actually is when shipped
as one deliverable.
