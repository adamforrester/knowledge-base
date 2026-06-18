---
type: practice-area
title: Gaps and Open Questions
description: Practice gaps and unanswered questions across the corpus. Sourced inventory of what we don't yet have a POV on.
tags: [gaps, open-questions]
timestamp: 2026-06-16
---

# 09 — Gaps & Open Questions

> Where the practice's collective material — internal and external — is thin, dated, contested, or silent. Organized in four categories per brief, plus a fifth pass against the broader field for what's missing across all sources.

---

## 1. Known depth gaps

Areas where the collective source material is thin or silent. These are the highest-priority opportunities for the practice to develop original POV and productized offerings.

### 1.1 Pricing, commercial structuring, and SOW language
- **No pricing model after handoff.** CareCentrix prices Discovery / Foundations / Build only. No retainer, support tier, governance subscription, federated chargeback, or quarterly review tier. This is the largest single commercial gap. Three productizable offerings need pricing: Run-phase retainer, quarterly governance review, Ambassadors program.
- **No SOW templates with role hours per phase.** VML library's Section 7 ("Scoping & Team Building") reads as an unfinished outline ("Roadmap example, Backlog example w/ t-shirt sizing, Sprint Timeline, Request intake flow") — promised but not delivered. Every senior practitioner reinvents this for each pitch.
- **No t-shirt sizing examples.** Flagged as a desired output in the deck; not produced.
- **No sprint timeline examples** with realistic week-counts per phase. Only one concrete duration claim across all internal materials: Prism's "5 days vs. 6 weeks scoped."
- **No request-intake flow examples** despite being flagged as desired.
- **Pricing models for ongoing work** — retainer? Subscription? Federated chargeback? Per-component? No internal stance.

### 1.2 Maturity model and readiness diagnostic
- **No productized maturity assessment workshop.** The Six Signs framework is opportunity recognition, not maturity diagnosis. InVision's 5-level ladder (Nascent → Basic → Integrated → Distributed → Optimized) and Paavan's 0–4 scale are productizable as paid 1–2 day diagnostic engagements; the practice has not yet packaged either.
- **No org-readiness diagnostic.** Idean's Audrey Hacq names this clearly: *"If the maturity of the organization is low... the design system is not the main solution."* Practice should ask discovery questions that diagnose organizational readiness — and decline (or scope smaller) when the diagnostic is bad.

### 1.3 Multi-brand technical governance
- **Token architecture for multi-brand is under-articulated.** Internal materials handle multi-brand at the *theming* layer (T-Mobile/Metro, Ford/Lincoln) but the architectural decision — when one system with brand themes vs. parallel brand-specific systems vs. federated systems with shared roots — is not laid out as a decision tree.
- **Composition-based brand extension** is mentioned in the AI-Compatible doc as where brand actually lives, but the *architectural* implications (how composition patterns get registered, themed, validated) are not yet detailed.
- **The Multi-Brand Governance source (Apr 2025)** covers process governance well but skips technical governance entirely. Practice's combined POV is unique but undocumented coherently.
- **Largely closed by 24-tokens-at-scale (May 2026)** — multi-collection-not-multi-mode for brand, managed inheritance vs. fork governance, brand version pinning, the Theme Schema contract for white-label, blast-radius-weighted RACI, and the Generative Token pattern. The remaining gap is sub-bulleted as §1.20 below: the Generative Token / OKLCH-derived brand expansion pattern as a practice-default deliverable.

### 1.4 ROI and measurement methodology
- **Defensible ROI calculator absent across the entire field.** UXPin's "hours × salary" framing (2017) and the practice's component-level math (Button 67.7%, Dynamic menu 81%) are the most rigorous public artifacts. Neither is a calculator a client can run themselves. **A practice with this case-study volume should be publishing its own.**
- **No standardized measurement framework as deliverable.** Curtis's six themes (Productivity / Coverage / Satisfaction / Consistency / Quality / Efficiency) is the right framework; not yet productized into a measurement methodology with dashboards, instruments, and reporting cadence.
- **Coverage definition not committed.** Three competing industry definitions (didoo, Morningstar, Veriff). Practice should pick (working synthesis: Morningstar's *% of pages applying system components*).
- **Pilot exit criteria not defined.** "Pilot validation with engineering" is named in milestones; what makes it succeed or fail is not.

### 1.5 Pilot methodology and Practice Pilot
- **Pilot scoring framework not in commercial deliverables.** Eight-factor scoring exists in scoping doc; not shipped as a Discovery artifact.
- **Practice Pilot offering missing.** Mall's pre-pilot rehearsal is rare and valuable; could be productized as a 3–5 day workshop.
- **Three-part MVP scoping not adopted.** InVision MVP's collection + user base + contribution plan is the right scope; commercial proposals scope only the collection.

### 1.6 Contribution model and Ambassadors program
- **Curtis's contribution criteria, scale, and onboarding are not in commercial deliverables.** 8-factor criteria, 6-step onboarding, contribution-vs-participation distinction, contribution scale (Fix → New Catalog) — all available IP but not packaged.
- **Ambassadors program not productized.** Couldwell's Guardians/Ambassadors/Lead pattern; Sprout Social's program; GOV.UK's working group. Could ship as a 4–6 week embedded coaching engagement.

### 1.7 Code-side delivery
- **Token build pipeline not in deliverables.** DTCG-compliant tokens named; Style Dictionary configuration, GitHub Actions distribution, custom transforms not shipped. **Partially closed by 24-tokens-at-scale (May 2026)** — Style Dictionary v4 as the build engine, validation in CI with errors-vs-warnings discipline, the Cascade Report artefact. The remaining gap is making these a default commercial deliverable rather than an internal stance.
- **CI quality gates not in scope.** Visual regression, accessibility CI, token drift detection — not standard scope. Field is silent broadly; practice could lead. **Partially closed by 24** — DTCG schema validation, alias resolution, matrix contrast validation across brand × theme × density, dead-token detection. Same remaining gap: default deliverable, not just stated stance.
- **Code Connect not defaulted.** Practice has IP; commercial proposals don't ship Code Connect bindings by default. By 2026 this should be standard. **Partially closed by 30-generated-from-data-documentation (June 2026)** — 30 §2 articulates Code Connect as part of the Phase-2 deliverable in the phased-adoption pipeline, with the Code Connect asymmetry between React (Baseline-grade) and iOS / Android / Flutter (materially less mature) honestly named; 30 §6 commits the practice to shipping Code Connect as part of the AI-readiness cluster. The residual is shipping it in the next proposal.
- **Custom MCP server / registry not commercial.** Internal POV; not yet sold. **Partially closed by 30** — 30 §2 names the MCP server as the Phase-3 deliverable (40–80 hours of engineering, the dominant single line item) and frames it as durable practice IP that compounds across the portfolio (build once, reuse). The residual is the same: ship it in the next proposal.
- **Engineering-onboarding artifact not produced.** Couldwell's `docs/decisions/`, `docs/onboarding/`, `docs/meeting-notes/` patterns; almost no client has them. **Partially closed by 30** — 30 §3 names "pipeline-itself documentation including engineering onboarding" as part of the Phase-1 line items, and the per-component file-structure ownership annotations (engineer owns `.tsx` / `.types.ts` / `.stories.tsx` / `.test.tsx`; UX Designer owns `.docs.mdx` and authored portions) substrate the engineering-onboarding artefact at the component level. ADRs at the system level (Mangialardi) remain a separate practice-IP slot the per-component template doesn't itself produce.
- **Headless vs. opinionated component architecture stance** undocumented.

### 1.8 Component-level accessibility annotations — CLOSED
- **Closed by 14-accessibility (architecture), 16-mobile-accessibility-implementation (framework depth across Flutter, Compose, SwiftUI/UIKit, React Native), and 17-accessibility-annotation-contract (the per-component annotation spec — name, role, state, value, focus, scaling, inversion, motion, gestures, live regions).**
- The remaining sliver — web implementation depth and the ARIA-specific annotation fields — was named §1.16 below and is now also closed (see §1.16).

### 1.9 Motion as foundation
- Motion appears in token lists but the practice does not yet ship motion principles, motion audits, easing studies, or productive/expressive splits as foundational deliverables.
- Head's framework (principles → building blocks → choreography) is straightforward to adopt and would close the gap.
- **Closed (architectural layer) by 18-motion-foundations, 19-motion-implementation-web, 20-motion-implementation-mobile, and 21-motion-spec-and-handoff (May 2026).** Open gaps that remain are now downstream of the architectural treatment: cross-platform spring calibration as a practice deliverable (a starting mapping table is in 20 but the side-by-side reference videos are not yet a practice default); Pattern A vs. Pattern B tooling for the motion spec contract (a Figma-plugin or pipeline to emit machine-readable spec files does not yet exist as a turnkey product); the productive vs. expressive choice between parallel token sets and override-mode is not yet a practice default.

### 1.10 Documentation IA and templates
- Reference-site information architecture is named; not delivered as a deliverable.
- **Per-component template gap closed by 29-per-component-documentation-template (June 2026).** The practice now ships a 17-section template (header / summary / live example / purpose / when-to-use / avoid-when / anatomy / props/API / states / variants / examples / do-don't / accessibility / content guidelines / composition-and-related / changelog / conformance dossier), with conditional rendering per component-type, a CI freshness check, per-section minimum-prose rules, and a YAML version-zero schema the practice pulls off the shelf in week one of every engagement. The MDX template, the `.ai.json` schema mapping, and the conformance-dossier aggregation pattern are practice IP.
- Tooling opinion has firmed up (29 §6 carries the decision framework: Storybook + MDX as engineering default; Zeroheight / Supernova / Knapsack as hosted alternatives by client shape; self-hosted as default for regulated and EAA-procurement clients).
- **Generated-from-data as commercial default articulated by 30-generated-from-data-documentation (June 2026).** The pipeline (source format choices, five generation targets, CI surface, single-source-of-truth file structure, the authoring seam), the upfront engineering investment (~50–80 hours Phase 1 only; ~108–216 hours full Phase 1+2+3), the per-component hours redistribution (2–8 hours generated vs. 4–11 authored, ~3–6 hours saved per component), the ~30-component break-even, the 5-question decision tree (3-of-5 = mandate generation), the two-phase migration playbook, the four-prerequisite cluster relationship to AI-readiness, and the phased adoption (clients land Phase 1 in initial proposal, Phase 2/3 in retainer) are now committed practice POV. The residual that remains is *shipping it* — the next engagement actually itemising the pipeline as a Foundations-tier line item rather than absorbing it as overhead.
- **Per-component field-truth gap closed by `components/` catalogue (June 2026).** The new authoritative tier ships ~40 per-component briefs across the seven categories. Each brief is a 15-section field-truth study (framing / anatomy / properties / states / usage / accessibility / content / motion / i18n / naming / implementation / related / POV evolution / sources / agent-consumable schema). The §15 schema is the seed an engagement instantiates into its component data file (per 30). Briefs are written through the existing `_research/` dual-agent workflow with a purpose-built prompt template at `_research/_component-prompt-template.md`. The catalogue is the upstream artefact 29's docs page is built from. Intake is engagement-driven; gap visibility lives in `components/index.md`.

### 1.11 Glossary
- Mall's Activity #25 framing (glossary as a *negotiation* between disciplines) is missing from the practice's commercial flow. Most engagements treat glossary as a docs appendix.

### 1.12 AI-readiness as commercial default
- Token descriptions are aspirational, not contractual. Should be a default Foundations deliverable, not an AI add-on.
- `.ai.json` is in the AI-Compatible doc but not the commercial proposal. Should ship with every component by 2027.
- AGENTS.md / CLAUDE.md is unique IP; the practice can claim this layer publicly.

### 1.13 Trust, governance, liability for AI-generated assets
Obello's Trend 2 is a full agenda the practice's POV does not engage:
- Indemnification language for AI outputs.
- Audit trails for brand-asset provenance.
- Permissioning models (who can prompt vs. publish).
- Brand-safety enforcement at output time.
- Auditability and reviewability.
This will become a procurement-grade requirement for regulated industries (healthcare, financial services, government) within 18 months.

### 1.14 Failure-mode register / risk catalog
- Internal materials are uniformly aspirational. No catalog of named failure modes from prior engagements (other than the high-level ones in `01–08`).
- A genuine practice asset would be: anonymized post-mortems of past engagements, common pitfalls, recovery patterns.

### 1.15 Education curriculum and certification
- Cross-disciplinary onboarding mentioned (HTML/CSS for designers, Figma for engineers, Git for designers). No curriculum, no certification path, no "DS literacy" frame productized.

### 1.16 Web accessibility implementation depth — CLOSED
- **Closed by 28-web-accessibility-implementation and the web extension to 17-accessibility-annotation-contract (June 2026).** Both files cover ARIA 1.3 (working draft, not Recommendation as of mid-2026), the user-preference media-query surface (`prefers-reduced-motion`, `prefers-contrast`, `forced-colors`, `prefers-reduced-transparency`, `prefers-color-scheme`), `inert`, `:focus-visible`, the popover API, `<dialog>` + `showModal()`, the APG keyboard model per composite-widget pattern, the four-engine × four-AT test matrix, and the cross-engine divergences that change implementation decisions (`aria-owns`, `aria-description`, `aria-errormessage`, JAWS table mode, VoiceOver `aria-current="page"`).
- The annotation contract now carries five web-only fields — landmark and heading structure, ARIA relationships (with `aria-owns` discouraged), `inert` regions and modal scope, `forced-colors` survival, APG keyboard model per Tier 2 composite — and the mobile-derived fields gained web implementation lines.
- The standing gap that remains is adaptive UI — when the surface is generated per render, annotation targets shift to the component primitives the LLM composes from, and verification shifts to in-pipeline accessibility scanning of rendered DOM. See 17 *"Adaptive UI — the standing gap"* and 27-adaptive-interfaces-implementation §6.2.

### 1.17 Annotation methodology as a Figma practice
- 17 sketches two patterns — Pattern A (annotation as a layer in Figma) and Pattern B (annotation as metadata in the component schema) — and states the practice's preference, but does not work the methodology in Figma at the level 12-figma-practice operates on for everything else.
- Concretely: how the annotation table lives in a component file, how it's kept current as the design evolves, who owns it, how it's reviewed alongside the visual spec.
- A natural extension to 12-figma-practice.

### 1.18 Compose Multiplatform's accessibility story on iOS
- Compose on iOS (via CMP) is newer than Compose on Android. 16-mobile-accessibility-implementation flags this as a tension: do not assume parity with native SwiftUI/UIKit for accessibility until validated.
- For projects considering CMP for iOS, accessibility should be a release-blocking validation. Practice should have a position before recommending CMP commercially.

### 1.19 The annotation contract as a sellable deliverable
- 17-accessibility-annotation-contract is practice IP — derived from cross-framework synthesis, prescriptive enough to ship to clients, not yet in any commercial proposal.
- Sits next to §1.12 (AI-readiness as commercial default): practice has the artefact, hasn't packaged it.
- Productizable as a Discovery output or a Foundations deliverable. By when?

### 1.20 The Generative Token / OKLCH-derived brand expansion pattern
- The pattern (5–10 primitives produce a brand's full semantic layer mechanically via OKLCH lightness adjustments and a standardised transform set) is the field's most-promising direction for portfolio engagements past five brands. Mature systems doing this (Adobe Spectrum's light/dark math, IBM Carbon's contrast-pinned palettes) report onboarding costs of ~10% per additional brand.
- **The practice does not yet ship the tooling** — the OKLCH transforms, the brand-primitive Theme Schema, the generation pipeline that emits a full semantic layer from a small primitive set. Building it the first time is a one-time investment per portfolio that amortises across the engagement and its successors.
- Surface in next portfolio engagement scoping. By end of 2026 should be a default for any portfolio past three brands. (See 24-tokens-at-scale.)

### 1.21 `text-box-trim` Baseline gap and the cross-platform cap-height alignment story
- Cap-height alignment as a system-level feature requires `text-box-trim` on web parity with iOS `leading-trim` and Compose `LineHeightStyle.Trim`.
- **As of May 2026, `text-box-trim` is Limited Availability, not Baseline.** Chrome 133+, Safari 18.2+, Edge 133+ ship it; Firefox has implemented but keeps it disabled by default through at least Firefox 149. Verified via caniuse.com / MDN.
- The cross-platform alignment-baseline story does not close until Firefox enables the property by default. Track Firefox releases through 2026; revisit this gap as Firefox progresses. (See 23-typography-tokenisation.)

### 1.22 Continuous density via computed tokens
- The emerging pattern (density as a parameter in a spacing formula rather than a switch between named discrete modes) is technically feasible with Tokens Studio math and Style Dictionary preprocessors.
- The practice has not yet committed to a use case that justifies the architectural overhead. Most agency clients can articulate two or three density tiers; few can articulate the use case for continuous density.
- Watch for the use case to surface; do not lead with the pattern. (See 22-token-architecture-extensions.)

### 1.23 React Native Dynamic Type bridge as a practice standard
- Without a native bridge module, RN typography stays at the developer-specified size regardless of iOS Dynamic Type. This is the largest accessibility gap in cross-platform mobile typography.
- Open-source bridge modules exist but none has emerged as the convergent answer. The practice should either commit to maintaining its own bridge for RN engagements or commit to a specific upstream module and document the dependency.
- Currently undecided. By end of 2026 the practice should have a stated default. (See 23-typography-tokenisation.)

### 1.24 Token-usage telemetry from production
- The "we don't know which tokens are actually used" problem is one of the more-frequently-named failure modes in the field at portfolio scale. No standard tool tracks runtime usage.
- Approaches that work in 2026: build-time scans of compiled CSS for web; Style Dictionary plugins emitting a usage manifest for native; product analytics with token tags for surfaces where the deeper telemetry matters.
- The practice has not yet shipped any of these as a default deliverable. Surface in portfolio engagements past two years' operation. (See 24-tokens-at-scale.)

### 1.25 Typography deepening — CLOSED
- **Closed by the June 2026 deepen pass on 23-typography-tokenisation.** Three new H2 sections landed inline: **Brand voice in type choices** (after §The shape of a typography token set, before §Modular scales) covering the connotation vocabulary's limits, voice as an immutable system constraint, brand-brief-to-token translation, the monumental-display-plus-invisible-text asymmetric pattern, the multi-brand unify-text-vary-display pattern, the commissioned / licensed / commodity asset matrix with named foundries, the "brand smell" framing, and the system-green-of-typography suppression zones; **Type pairing as a system** (after §Modular scales, before §Fluid type) covering the triad-with-rare-fourth shape, the contrast-of-personality-not-category discipline, the categorical-collapse / double-novelty / personality-conflict / brittle-balance failure modes, the primitive/composite/component pairing token architecture, multi-script fallbacks via DTCG modes, single-vs-two-variable-family decision logic around `opsz`, the `font-variation-settings`-overrides-every-axis gotcha, and the no-Radix-equivalent-for-pairing tooling gap; **Font loading and performance** (after §Variable fonts, before §Line-height) covering the per-role `font-display` matrix (`optional` body / `swap` display / `block` icons), `unicode-range` subsetting with the over-subsetting failure mode and CMS-injected-content blind spot, the `<link rel="preload">` discipline including the `crossorigin` requirement, variable-font byte economics with the 2–3-weight break-even and per-axis non-linear cost, CLS mitigation via metric-matched fallback declarations (Fontaine / Fontsource / Capsize), the self-hosted-as-2026-default position post the 2022 Munich ruling, and OpenType feature settings as authoring decisions with the `font-feature-settings`-overrides-siblings cascade gotcha and the `font-variant-*` preference. The lighter additions — **heading-semantics-vs-visual-scale** as a subsection of §The shape of a typography token set, and **vertical-rhythm-and-the-baseline-grid-where-this-stands** as a subsection of §Line-height — also landed. Provenance footer extended; failure-mode register and tensions-and-open-questions section extended. Three claims flagged for `_source-text/` backing before client-facing quotation: Munich Regional Court 2022 ruling specifics (§1.27a), HTTP Archive `wght`-axis utilisation figures (§1.27b), per-axis variable-font byte cost ranges (§1.27c) — track alongside the existing 2026-06-15 color follow-ups in §1.27.

### 1.26 Team-building / DS-team-as-discipline — CLOSED

**Closed by the 2026-06-16 dual-agent run on team-and-discipline.** The synthesis landed as `00e-team-and-discipline.md`, positioned as a 00-level cross-cutting file alongside 00 / 00b / 00d. Eight H2 sections cover the agency-vs-in-house structural framing, hiring and skill mix, the five-stage Part Timer → Allocated Individual → Dedicated Team → Embedded Multi-Team arc, the four-part agency-to-client handoff with three named failure modes, internal team rituals (daily/weekly/monthly with documentation-as-ritual), career paths (with a five-grade IC/Lead leveling table), distributed and global team patterns (paired-timezones, async-dominant, the always-on-senior trap), and DS-specific burnout patterns (everyone's-customer load, never-finished load, invisible-improvement load, capitalist-contradiction-of-contribution, agency-specific cold-start fatigue).

Both agents converged on every load-bearing claim — the structural difference between agency and in-house DS teams, the four-part handoff structure, the failure-mode catalogue, async-dominant global teams, the four primary burnout vectors. Two artefacts were lifted from the external pass: the in-house-vs-agency comparison table and the five-grade IC/Lead leveling table. The "capitalist contradiction of contribution" framing (Hupe, *Your Contribution Model is Doomed*) was an external-pass-only contribution and is integrated into 00e §8 as the explanatory frame for contribution-model burnout. Inline cross-references added from 00d (roles), 07 (governance), 08 (retainer shapes); 00e cross-refers to 04, 15, 29, 30 where the topics intersect.

**Four claims surfaced in 00e need `_source-text/` backing before they appear in client artefacts.** Logged as §1.26a–§1.26d residuals (next housekeeping pass):

- **§1.26a — Hupe's two essays (*Burn Baby Burnout*, *Your Contribution Model is Doomed*).** Verify the canonical URLs, capture the body text of *Your Contribution Model is Doomed* in particular (the "capitalist contradiction of contribution" framing in 00e §8 leans on it), confirm publication dates. The framing is load-bearing for the burnout cluster; it should not appear in a client artefact unsourced.
- **§1.26b — Sparkbox four-stage maturity model (Version One / Growing Adoption / Surviving Teenage Years / Evolving), Callahan, Sparkbox.** 00e §3 references this as a system-side companion to the team-side Part-Timer-arc. Verify the canonical Sparkbox post, capture the stage definitions verbatim, confirm the model is current (the post may be 2018-vintage and have been superseded).
- **§1.26c — The Hot Potato Process, Mall and Frost.** 00e §4 names it as the canonical articulation of the paired-contribution coaching pattern. Verify the canonical writeup location (Frost's blog, Mall's site, or a SuperFriendly artefact), capture the body text, confirm attribution.
- **§1.26d — Banfield 2024 Knapsack post on enterprise product infrastructure.** External agent cited it; confirm title, URL, and whether it adds anything beyond what 30-generated-from-data-documentation already covers. If yes, capture; if no, drop the reference.

### 1.27 Source-text backing for claims surfaced in 2026-06-15 dual-agent runs — CLOSED

### 1.27 Source-text backing for claims surfaced in 2026-06-15 dual-agent runs — CLOSED

**Closed by the 2026-06-15 source-text pass.** All seven primary-source flags landed; both watch items produced their first quarterly check. The §1.27a residual on CSS Color 4 §14.2 (which had remained open after the late-evening pass because WebFetch truncated the spec) closed on a follow-up firecrawl_scrape pass that returned the full document — the body-text capture is now complete and the inline 31 §1 line is corrected. New `_source-text/` files captured: `ext-css-color-4-gamut-mapping.txt`, `ext-apca-thresholds.txt`, `ext-dtcg-format-module.txt`, `ext-munich-google-fonts-ruling.txt`, `ext-web-almanac-fonts.txt`, `ext-variable-font-axis-byte-costs.txt`, `ext-style-dictionary-changelog.txt`. Inline corrections landed in 31 §1 (DTCG colorSpace enumeration confirmed and de-hedged), 31 §1 gamut-mapping (no single normative CSS default; three §14.2 sibling algorithms with implementation choice), 31 §3 (APCA Lc table tightened against the canonical font-size × weight matrix), 31 §3 (APCA verification path expanded with `readtech.org/ARC/`), 23 §DTCG composite typography tokens (property-level-aliasing-via-`$ref` rule named explicitly), and 23 §Self-hosted vs. third-party hosting (Munich ruling specifics tightened with case number, court chamber, legal basis, narrowness caveat).

**What landed:**
- **§1.27a — CSS Color 4 §14.2 algorithm attribution (CLOSED with substantive correction).** Initial 2026-06-15 capture via WebFetch was partial (TOC only); follow-up capture via firecrawl_scrape against the Editor's Draft (7 May 2026, Bikeshed generator stamp 2026-06-09) returned the full document and §14.2 / §14.2.1 body text was extracted verbatim. The substantive finding: **there is no single normative CSS default.** §14.2 reads, "Implementations may choose any of the three algorithms based on their quality and runtime efficiency tradeoffs, and must use their chosen algorithm wherever CSS mandates that gamut mapping be performed." The three siblings (`Binary Search Gamut Mapping with Local MINDE`, `EdgeSeeker Gamut Mapping`, `Ray Trace Gamut Mapping`) all "aim at constant-lightness, constant-hue chroma reduction in the OkLCh color space" under a relative colorimetric intent; lightness extrema are clamped before chroma reduction (L ≥ 1.0 → destination white, L ≤ 0.0 → destination black). §14.2.1 confirms Binary Search with Local MINDE uses ΔE_OK as its distance metric (1 JND in OkLCh = 0.02). The 31 §1 line was rewritten — previously it claimed a single CSS Color 4 default (chroma-reduction) and hedged on which §14.2 algorithm was normative; now it names the spec's frame faithfully (three siblings, implementation choice, common chroma-reduction frame) and notes that browser choice is a per-engine, per-version question tracked through WPT. The practice's prior framing was a factual inaccuracy, not just under-cited; the correction matters for any client artefact that quotes 31 §1's gamut-mapping fallback strategy.
- **§1.27b — APCA Lc threshold table (CLOSED).** Captured the canonical Bronze / Silver / Gold tier rules and the full font-size × weight × Lc lookup matrix from `readtech.org/ARC/tests/visual-readability-contrast/`. The 14px-at-400-weight figure that 31 §3 had cited as Lc 90+ is actually Lc 80–85 in the canonical matrix; corrected inline. Lc 30 floor for non-text UI is practitioner shorthand because Myndex's published Non-Text Contrast guideline is still a placeholder; this is now flagged in 31 §3.
- **§1.27c — DTCG colorSpace: `display-p3` (CLOSED).** The Color Module 2025.10 enumerates fourteen valid colorSpace values including `display-p3`, alongside `srgb`, `srgb-linear`, `oklch`, `oklab`, `rec2020`, and others. The field sits as a sub-field of `$value` next to `components`, `alpha`, and an optional `hex` fallback. 31 §1 line de-hedged.
- **§1.27d — Munich ruling Az. 3 O 17493/20 (CLOSED for current text; subsequent case law remains a watch).** Confirmed the case is Landgericht München I, third civil chamber, ruling dated 20 January 2022; €100 damages plus €250,000 per future violation threatened; legal basis was § 823 Abs. 1 BGB ("general right of personality / informational self-determination"); the ruling explicitly cited self-hosting as the remedy. Captured the narrowness caveats: single ruling, single defendant, court of first instance, not binding across other Landgerichte, no appellate refinement established in contemporaneous press. 23 §Self-hosted vs. third-party hosting tightened with the specifics.
- **§1.27e — HTTP Archive `wght`-axis utilisation (CLOSED with correction).** The ~60% figure that 23's external pass surfaced is not in the source. The Web Almanac 2024 fonts chapter reports 99% file-level wght-axis support and 75–78% page-level CSS use via `font-variation-settings`; the ~60% figure is treated as a non-landing external-pass approximation. 23's body text never quoted the figure (it was footer-only), so no inline correction is needed; the §1.27e flag closes.
- **§1.27f — Per-axis variable-font byte cost ranges (CLOSED with verification procedure preserved).** Per-axis byte costs are genuinely per-typeface; no canonical primary-source ranges exist because the cost depends on master count, hint table size, glyph-coverage compounding, and compression-friendliness. 23's existing hedging at line 528 ("These ranges are practitioner-observed; verify against the specific font binary via Wakamai Fondue") and the §Tensions item at line 847 are correct and load-bearing. The verification procedure (foundry binary → Wakamai Fondue → foundry's published metrics) is captured in `ext-variable-font-axis-byte-costs.txt` and stays as the practice's recommended method. No body-text correction needed.
- **Style Dictionary `color-mix()` watch (CHECKED, no change).** Current version 5.4.4 (mid-2026); no native `color-mix()` or relative-color-syntax preservation. 5.3.0 added DTCG 2025.10 structured-color transforms (oklch, oklab, color(display-p3 ...), lch) but these output static CSS, not preserved expressions. 31 §1's recommendation holds unchanged. Next quarterly check: 2026-09-15.
- **DTCG typography composite-type watch (CHECKED, with one inline upgrade).** The 2025.10 Format Module is current; the load-bearing 2025.10 mechanic is the property-level-aliasing-via-JSON-Pointer rule (sub-property references need `$ref`, not `{alias}`) — now landed inline in 23 §DTCG composite typography tokens. Multi-mode resolution and per-script family overrides remain uncaptured from the spec; the watch continues. Next quarterly check: 2026-09-15.

**What remains open:**
- Nothing. §1.27 is fully closed. The two watch items (§Style Dictionary `color-mix()` and §DTCG typography composite-type) continue on their 2026-09-15 quarterly cadence, but neither is a §1.27 follow-up — they're standing watches.

### 1.28 Auditing design systems as a discipline — CLOSED

**Closed by the 2026-06-17 dual-agent run on auditing-as-a-discipline.** The synthesis landed as `32-auditing-design-systems.md`, positioned as an extension topic alongside 22 / 24 / 26 / 27 / 30 / 31. Six H2 sections cover the agency-vs-generic-UX-audit framing (with the recurring eight-pattern failure-mode catalogue), the eight-lane methodology (token / component / accessibility / content / motion / code / governance / adoption with the heuristic-vs-specification-vs-census mode distinction and the cross-lane diagnostic example), the productised audit engagement (3-day / 5-day / 10-day shapes priced at $25–45k / $50–80k / $90–150k respectively, with the canonical 5-day day-by-day shape and the three-artefact deliverable surface), the reporting template with the four-tier severity model and the bell-shaped severity distribution discipline, the continuous audit and drift detection surface (eight CI lanes plus the AI-readability ninth aspirational lane, the drift dashboard's tripartite audience, the audit-the-audit discipline against five named silent-failure modes), and the Discovery triad with the unified Discovery + audit deliverable at $50–120k as the practice's highest-leverage productised offering.

Both agents converged on every load-bearing claim — the agency-vs-in-house structural framing, the eight-lane methodology with identical sub-points, the cross-lane diagnostic example (token bypass → API drift → consumer fork → contribution-model rejection — both arrived at the same canonical illustration independently), the four-tier severity model, the "62 shades of gray" buy-in framing, the eight CI lanes, the drift dashboard's tripartite audience, the Discovery triad. Convergence was unusually strong (~85%), which is signal that this is the practice's best-articulated topic to date; both reasoning paths landed at the same conclusions independently. Two artefacts lifted from the external pass: the eight-lane summary table at §2 and the four-tier severity-model table at §4. Specific attributions added from the external pass: Cristiano Rastelli (didoo) for the source-mix-overtime formula at Badoo's Cosmos system; Marcin Treder for the original "62 shades of gray" UXPin audit story.

Inline cross-references added from 32 to 00b / 00d / 00e / 01 / 04 / 07 / 08 / 23 / 24 / 28 / 29 / 30 / 31; the See also block in 32 names the relationships explicitly. Cross-references back from those files added where the topic was previously hand-waved.

**Four claims surfaced in 32 need `_source-text/` backing before they appear in client artefacts.** Logged as §1.28a–§1.28d residuals (next housekeeping pass; extends the §1.26a–§1.26d cluster from the team-and-discipline run; both can be closed in a single source-text pass):

- **§1.28a — Cristiano Rastelli (didoo) at Badoo's Cosmos system, the source-mix-overtime formula.** Verify the canonical writeup, capture the calculation specifics, confirm the attribution. Load-bearing for 32 §2.8's adoption-coverage definition. Likely sources: Rastelli's blog at didoo.net, his Medium articles, or the original Badoo design-system case study.
- **§1.28b — Marcin Treder at UXPin, "62 shades of gray."** Verify the original audit case study's specifics (which client, which year, which exact phrasing), confirm the attribution. The framing is load-bearing for 32 §4's buy-in tactic. Likely source: UXPin's blog or Treder's published writing on the audit.
- **§1.28c — Screen-reader market share figures.** WebAIM's annual screen-reader survey is the canonical reference; verify the most recent figures (proportions vary year-on-year). The four-engine × four-AT matrix justification in 32 §2.3 references VoiceOver-on-mobile, JAWS-on-Windows, NVDA-on-Windows market share without quantification; the external pass surfaced specific numbers (~70% / ~40% / ~30%) that need source-text backing before they go in client artefacts. Likely source: WebAIM's most recent Screen Reader User Survey at https://webaim.org/projects/screenreadersurvey/.
- **§1.28d — Supernova's "AI-ready design systems" positioning.** The external pass referenced this as the vendor framing pushing toward continuous validation as the prerequisite for AI-agent code generation. Verify Supernova's published framing if the AI-readability ninth lane in 32 §5 is referenced inline in client work. Likely source: Supernova's blog or product marketing materials.

### 1.29 MCPs as practitioner tooling for DS work — CLOSED

**Closed by the 2026-06-17 dual-agent run on MCPs as practitioner tooling.** The synthesis landed as `34-mcps-for-ds-practice.md`, positioned as an extension topic alongside 22 / 24 / 26 / 27 / 30 / 31 / 32. Seven H2 sections cover the two-layer architecture (workstation stack vs. custom DS MCP server with the payback-curve distinction and the cost-of-not-having day-to-day workflows table); the Figma-side MCPs (Dev Mode read / Console MCP write with the branch-only-writes governance discipline); the component-side Storybook MCP (with the generic-vs-opinionated framing against the custom DS MCP); the accessibility-scanner MCPs (with the 30–40% / 60–70% automated-vs-manual coverage split and the no-native-screen-reader-MCPs gap); the token-side MCPs (Style Dictionary + Tokens Studio + custom wrappers; vendor-native MCP not yet shipping); the web-research MCPs (with the §1.27a truncation-fallback pattern as the canonical worked example); and the seven-tool default workstation config (with the starting `mcp-config.json` schema and the runbook discipline).

Both agents converged at unusually high rate (~90%) — the highest convergence the practice has measured to date. Both arrived independently at the two-layer architecture, the same five day-to-day workflows in the same order, the same Figma-side split, the same a11y-coverage split, the same seven-tool default config. Three artefacts lifted from the external pass: the §1 workspace-overview ASCII diagram (rendered into vault prose-led style); the §6 truncation-fallback flowchart (kept as ASCII because the visual reinforces the §1.27a pattern); the §7 working `mcp-config.json` schema as the runbook starting point. From Claude's pass: the §1.27a worked example as the running thread; the five Figma-side gaps catalogue; the audit-the-audit discipline carryover from 32 §5 applied to the workstation stack itself; the cost-of-having-too-much failure mode.

Inline cross-references added from 34 to 12 / 13 / 14 / 15 / 24 / 28 / 29 / 30 / 32; the See also block names the relationships explicitly. Cross-references back from 15 (architecture-side companion → 34 workstation-stack companion) and 30 (productisation companion → 34 workstation-IP companion) added where the topic was previously hand-waved.

**Three claims surfaced in 34 need `_source-text/` backing before they appear in client artefacts.** Logged as §1.29a–§1.29c residuals (next housekeeping pass; extends the §1.26a–§1.26d + §1.28a–§1.28d cluster — all eleven follow-ups closeable in a single source-text pass):

- **§1.29a — axe-core's published 30–40% WCAG-coverage methodology.** Both agents asserted the 30–40% / 60–70% automated-vs-manual split; the figure is widely cited but not trivially verified against a single Deque source. Verify against Deque's current published methodology (likely at deque.com/axe or in published whitepapers) before quoting in client work. Load-bearing for 34 §4's boundary-of-automated-scanning framing.
- **§1.29b — Southleft Figma Console MCP repository.** External named `github.com/southleft/figma-console-mcp`; confirm the canonical repo URL, the Desktop Bridge plugin install path, the maintainer's published roadmap, and the licensing terms before treating the dependency as fixed in the runbook. Material for 34 §2 and §7.
- **§1.29c — Workstation-MCP speed-up empirical validation.** 34 §1's task-and-leverage table cites speed-up multipliers (2–4× / 6–10× / 2–3× / 20–40× / 3–4×) drawn from senior-practitioner observation rather than tracked benchmarks. The first three engagements where the workstation stack is shipped as a productised standardisation should track actual speed-up; the empirically-validated multipliers replace the observation-based ones in the next file revision.

### 1.30 White-label design systems as an engagement type — CLOSED

**Closed by the 2026-06-17 dual-agent run on white-label DS as an engagement type.** The synthesis landed as `33-white-label-systems.md`, positioned as an extension topic alongside 22 / 24 / 26 / 27 / 30 / 31 / 32 / 34 — the fourth productisation companion in the 30 / 32 / 34 pattern. Seven H2 sections cover white-label as a distinct engagement type with the architecture-vs-engagement-shape distinction (the multi-brand-vs-white-label conflation cost; the productisation-companion framing); the two white-label shapes (for-resellers vs. as-starter, each with field examples, architecture, and commercial shape; the conflation cost; the three decision questions; the hybrid case); the architecture decision tree (the five-primitive minimum input set with *visual collapse* as the floor failure mode; the reseller-count payback curve with engine + first-three-resellers totalling 600–1,090 hours; the five-question synthesis-ready decision tree; the build-vs-buy reality with vendor gaps in validation, onboarding pipeline, and per-reseller MCP); the headless-vs-opinionated split (the dogmatic visual-vs-behaviour table; why the split makes for-resellers commercially viable and legally defensible; the 2026 library landscape — Radix / React Aria / Ark UI / Headless UI with Reach UI flagged in-maintenance); the commercial shape (the synthesis-ready comparison table with nine dimensions; the Build SOW shape totalling 770–1,160 hours; the Run SOW with three SLAs; the three-tier brand-onboarding pricing model — $5k / $12k / $25k+; how for-resellers closes 00d's run-phase pricing gap; **Pattern 6 — White-label / reseller platform** added to 00d's pattern set); the Prism positioning closure (the technology-team-adoption gap as load-bearing; the Prism2 → Prism3 investment scoping at 450–750 hours; the right-answer-for-now and the client conversation the closure unlocks); and the team / governance / failure-modes / AI-readiness layer (the brand-onboarding runbook as practice IP; six named failure modes including *brand-validation drift*, *the engine outpaces the system*, *reseller customisation outpaces the architecture*, *brand-onboarding SLA missed*, *the kit-vs-bespoke divergence*, and *the "starter became a product"* with the **thin-bespoke** framing; the engine's per-reseller AI-readiness output set; per-reseller MCP as the 2026–2027 tactical opportunity).

Both agents converged at unusually high rate — **~95%, the highest the practice has measured to date** (exceeding §1.29's ~90% and §1.28's ~85%). Both arrived independently at the architecture-vs-engagement-shape distinction; the for-resellers vs. as-starter bifurcation; the five-primitive minimum input set; the five-question architecture decision tree with identical engine-vs-no-engine outcomes; the headless visual-vs-behaviour split with the same library landscape; the three-tier pricing model; the three retainer SLAs; the Pattern 6 addition to 00d; the Prism2-as-starter closure with the technology-team-adoption gap as the load-bearing constraint; the same six failure modes; and the per-reseller MCP framing. The convergence rate is itself signal that this is the practice's best-articulated topic to date; both reasoning paths landed at the same conclusions independently. Two artefacts lifted from the external pass: the architecture decision tree's table format at §3 and the comparison table format at §5. Specific attributions added from the external pass: Stripe Connect Embedded Components' Elements Appearance API specificity; IBM Carbon's `g10` / `g90` / `g100` programmatic theme-swap reference; "Adobe Spectrum 2" and "IBM Carbon v11" version specificity; the *visual collapse* failure-mode framing; WCAG 2.2 explicit version citation. From Claude's pass: the full Build-hours total with documentation/`.ai.json` (~770–1,160 hrs); per-tier profitability margins; the IP-transfer-at-handoff and 00d-Pattern-fit rows; the **thin-bespoke** framing; the *schema-extension request* governance discipline; shadcn/ui / ZURB Foundation / ChannelEngine / ShipStation as additional examples.

Inline cross-references added from 33 to 00b / 00d / 02 / 07 / 08 / 17 / 22 / 24 / 28 / 30 / 31 / 32 / 34; the See also block names the relationships explicitly. Cross-references back from 00b (Prism2 framing → 33 §6 closes the positioning), 00d (white-label kit commercial question → 33 §5 articulates the answer; Pattern 6 added), 02 §6 (white-label as Curtis's seventh theming dimension → 33 productises it as an engagement type), and 24 (Generative Token pattern → 33 §3 architecture decision tree applies the architecture to the engagement-shaping question) added where the topic was previously hand-waved or split across files. **§3.2 below also closes** by pointing to 33 §6 — Prism2 is properly described as white-label-as-starter; the technology-team-adoption gap is the load-bearing constraint that holds it there; a hypothetical Prism3 would need the engine + schema + pipeline layers Prism2 lacks.

**Three claims surfaced in 33 need `_source-text/` backing before they appear in client artefacts.** Logged as §1.30a–§1.30c residuals (next housekeeping pass; extends the §1.26a–§1.26d + §1.28a–§1.28d + §1.29a–§1.29c cluster — fourteen follow-ups closeable in a single source-text pass):

- **§1.30a — Adobe Spectrum / IBM Carbon "10% of first reseller" payback figure.** Both agents asserted the figure as the canonical reseller-payback shape; widely cited in the field but not trivially verified against a single Spectrum or Carbon primary source. Verify against Adobe Spectrum 2's brand-derivation documentation and IBM Carbon v11's contrast-pinned-palette documentation before quoting in client work. Load-bearing for 33 §3's payback-curve framing.
- **§1.30b — The five-reseller engine break-even point.** The break-even calculation is observation-grounded rather than empirically verified. The first ~3–5 reseller-platform engagements where the practice ships an engine should track actual per-reseller cost against the engine investment to refine the break-even point. Update 33 §3 in the next file revision once empirical data exists.
- **§1.30c — Brand-onboarding pricing tiers ($5k / $12k / $25k+).** The tier model is practitioner-observation calibrated, not market-research-validated. The first ~5–10 reseller-platform engagements where the practice ships a tiered onboarding fee should track actual margin against the tier. Refine the model once the data accumulates.

### 1.31 Content considerations at the system level — CLOSED

**Closed by the 2026-06-18 dual-agent run on content at the system level.** The synthesis landed as a deepen on `04-documentation.md` (two new H2 sections — *Content as a system layer* and *The UX Copywriter role at engagement scale* — sitting between Cluster-6 and Our POV; ~4,900 words added; 04 grew from 185 lines / ~3,500 words to 349 lines / ~8,400 words) plus targeted inline additions to `23-typography-tokenisation.md` (typography composite-token `$description` carries voice intent — extending the tokens-with-descriptions discipline at the typography / content boundary) and `13-internationalization-and-rtl.md` (ICU-shaped messages live in the system's content-token catalogue; the per-component i18n consumption follows the catalogue rather than authoring per-component). Slot decision committed in the prompt: deepen 04, not a new file; the fifth-productisation-companion question stays open for a future revision if AI-surface content material grows enough to justify it.

The two new 04 sections cover: content-as-system as its own discipline (the conflation cost; the hierarchy — voice-and-tone constraint at top, content tokens at primitive layer, per-component guidance as consumption layer); the voice-and-tone matrix as a system artefact (the cross-tabulation of voice attributes × tone contexts; the synthesis-ready matrix table with three illustrative voice columns and ten tone-context rows including AI rows; three enforcement disciplines — matrix-as-AI-system-prompt, pre-merge content review, token-mediated authoring); content tokens / writing-tokens as a primitive (field examples — Linear, Stripe, Polaris, GOV.UK, Carbon; the tokenisable / not-tokenisable line; the synthesis-ready DTCG-shaped content-token schema with `$type` / `$value` / `$description` / `$extensions.<vendor>.parameters` / `.locale` / `.tone` / `.ai-readable`; the content-tokens-vs-CMS authoring boundary foreshadowing §1.32); i18n content depth at system scale (ICU integration; pluralisation across Russian/Arabic/Welsh/Polish/Slovenian; gendered language across Spanish/German/Finnish/Hebrew; RTL content ordering with `<bdi>` discipline; localisation governance via the UX Copywriter); and content for AI surfaces (assistant tone as voice-and-tone applied to AI surfaces with the matrix-directly-parameterises-the-LLM framing; refusal / disclosure / citation / streaming / tool-call content tokens; the variability-by-design problem applied to content with content tokens as the boundary the LLM composes within).

The UX Copywriter section justifies the CareCentrix 75-hour line item against three drivers (component count; content-surface complexity; content-token catalogue depth) producing a defensible 40–250-hour range with five worked engagement points (Pattern 1 / Pattern 2 baseline / Pattern 2 expanded / Pattern 2 multi-locale / Pattern 6 with AI surfaces). Names ~10-component minimum-viable scope and ~20-component payback floor. Articulates the tripartite handoff (matrix as governed artefact + content-token catalogue as maintained primitive + per-component content guidance) and the Run-phase content-retainer analogous to 33 §5's for-resellers retainer (matrix-evolution / token-addition / localisation coordination as three commitments).

Both agents converged at unusually high rate — **~97%, the highest the practice has ever measured** (exceeding §1.30's ~95% and §1.29's ~90%). Both arrived independently at the seven-section spine; the same hierarchy (voice-and-tone constraint at top → tokens at primitive → per-component as consumption); the same pricing model (40–250 hours, three drivers with identical hour estimates); the same DTCG-shaped content-token schema with `$type` / `$value` / `$description` / `$extensions` shape; the same matrix structure (voice × tone with body cells); the same three enforcement disciplines (matrix-as-AI-system-prompt, pre-merge review, token-mediated authoring); the same vendor-landscape gaps (no DTCG content-token spec; Tokens Studio / Style Dictionary / Specify / Knapsack / Supernova all silent on content tokens; ICU authoring tooling thin); the same tripartite handoff with governance-contract requirement; the same Run-phase content-retainer parallel; the same 00e residual flag for the role's practice-scale hiring discipline; the same slot decision (deepen 04, not new file) with the productisation-companion-spinout flagged available for future revision.

Two artefacts adopted from the external pass: the content-token DTCG schema rendered as a property-path table (cleaner than Claude's JSON-literal); the matrix's three-voice-column header (Expert / Warm / Direct) with shorter body cells. Lifted from external specifically: the "matrix directly parameterises the LLM" framing for §5 enforcement; the ICU parser-error specificity (single vs. double curly braces); IBM Carbon's *Empty States Pattern* citation. Preserved from Claude's pass: the four illustrative engagement points at §6 (Pattern 1 / Pattern 2 / Pattern 6 / multi-locale Pattern 2) showing the hour-model in action; the matrix's full ten tone contexts including AI rows (assistant-proactive and assistant-refusing) — the AI rows are load-bearing for §5's matrix-as-system-prompt enforcement; the variability-by-design framing tied to 26's residual gap; the per-vendor ICU support specificity at §4 (Lokalise / Crowdin / Phrase support; Smartling / TransPerfect varying); the references-organised-by-section footer; the LLM-based content review tooling section.

Inline cross-references added from 04's new sections to 23 / 13 / 25 / 26 / 27 / 29 §14 / 30 / 24 / 33 / 03 / 00d / 00e / 07 / 08; cross-references back from 23 (typography composite-token `$description` → 04 §Content as a system layer's voice-and-tone matrix) and 13 (ICU-shaped messages → 04's content-token catalogue authoring layer) added inline. The 00d "75-hour line item" question now has a defensible answer in 04 §The UX Copywriter role at engagement scale's hour-justification model.

**Three claims surfaced in the run need empirical or source-text validation before they appear in client artefacts.** Logged as §1.31a–§1.31c residuals (next housekeeping pass; extends the §1.26a–§1.26d + §1.28a–§1.28d + §1.29a–§1.29c + §1.30a–§1.30c cluster — seventeen follow-ups closeable in a single source-text pass):

- **§1.31a — DTCG content-token spec status.** As of mid-2026, no canonical DTCG content-token spec exists; the practice's `$extensions`-based schema is bridge investment. Track DTCG community discussions quarterly; if and when a content-token spec lands, the practice migrates the bridge schema. Verification path: the DTCG GitHub repo at `github.com/design-tokens/community-group` plus the Format Module update log.
- **§1.31b — CareCentrix 75-hour vs. three-driver hour-model calibration.** The hour-justification model (40–250 hours per Build, scaled against component count + content-surface complexity + content-token catalogue depth) is observation-grounded against the CareCentrix 75-hour single data point. The first 5–10 engagements where the practice ships a content-system layer with full Copywriter scope should track actual hours against the three-driver model. Refine in next 04 revision once empirical data exists.
- **§1.31c — Voice-and-tone matrix as agency-cross-engagement standard.** The matrix is widely shipped at per-product scale (Mailchimp, Polaris, Atlassian, Carbon, GOV.UK) but not yet widely shipped as an *agency-cross-engagement* artefact. The practice can lead by shipping the matrix as a default Discovery deliverable across engagements; the bet is that this becomes table stakes at agency scale by 2027. Track adoption across the next ~5 engagements that ship a content-system layer; the bet validates if the matrix lands as default Discovery deliverable across all of them.

### 1.32 CMS platforms — modern composable / headless coverage (deepen on 10)

- 10-cms-and-platform-integration is AEM-and-Drupal-shaped (12 H2 sections, 321 lines, with AEM as the dominant treatment). Modern composable-content / API-first patterns are largely absent.
- Named gaps:
  - **Headless CMS coverage.** Sitecore (XM Cloud / OrderCloud / SaaS), Contentful, Sanity, Strapi, Storyblok — none meaningfully covered. For agency clients on Sitecore (a real cohort) the file currently provides little.
  - **WordPress as DS host.** Still a real engagement type; absent.
  - **The CMS-vs-DS authoring boundary.** Where component anatomy lives in CMS schema vs. system schema; how the two source-of-truth claims reconcile; how Code Connect or `.ai.json` schemas align with CMS content models. This is a procurement-grade decision that the practice ships against without an articulated POV.
  - **MCP / AI-readability for CMS-managed components.** A natural extension of 30 §MCP — when components are authored *and stored* in the CMS, the registry has to source from there too. Not articulated.
  - **Composable-content patterns.** The 2025–2026 movement toward content-as-data with explicit schemas (sometimes called "headless DS-as-content-source") changes the integration story. Not covered.
- **Likely path: deepen 10-cms-and-platform-integration with new H2 sections for headless / composable / MCP-for-CMS-components. Not a new file.** Queue behind §1.30 (white-label) and §1.31 (content); surface when an engagement requires it.

### 1.33 SEO, GEO, and agent-discoverability for DS docs sites — field-level

- See §5.21 below — promoted to the field-level gaps section because the gap is across the entire DS field, not specific to the practice's coverage shape.

---

## 2. Temporal gaps

Areas where all available thinking is older and may need revisiting in light of current tools and practices.

### 2.1 Tokens-and-Variables tooling
- All foundational books (Frost 2016, Couldwell 2019, Idean 2019) predate W3C DTCG, Figma Variables modes, Style Dictionary maturity, and Tokens Studio.
- Mall *90 Days* (2023), InVision MVP/Benchmarking (2020), and even Mangialardi (2021) predate Figma Variables shipping (mid-2023) and the DTCG draft consolidating (2024).
- Curtis *Design Tokens* (Nov 2024) is the most current source; even it is approaching 18 months old.
- **Implication:** Anything in source material older than Figma Variables (mid-2023) is treating Sass variables, JSON files, or Sketch libraries as the source of truth. Practice should explicitly disclaim this when citing older sources.
- **Largely closed by 22-token-architecture-extensions, 23-typography-tokenisation, and 24-tokens-at-scale (May 2026).** DTCG 2025.10 stable spec (28 October 2025) is now the version-of-record. Style Dictionary v4, Tokens Studio, Figma Variables composite types, Penpot, and Terrazzo all support the stable spec. The 18-months-old-Curtis problem is no longer the active gap; the active gaps are 1.20–1.24 above.

### 2.2 AI integration
- All foundational books predate the AI-as-DS-consumer era (post-Nov 2024 Anderson reframe).
- The internal AI-Compatible doc (Feb 2025) is the practice's most current AI POV; the AI cluster external sources (Figma DS x AI, Obello, AI Tools, Wolosin, Anderson) span Nov 2024–2026 and represent the active frontier.
- **Implication:** Any pre-2024 framing of "design systems" should be read with the assumption that AI-readiness is now a core requirement, not a forward POV.

### 2.3 Atomic design vocabulary vs. modern reality
- Frost (2016) is the source of "atom / molecule / organism / template / page" — but Frost's atoms are HTML elements, not tokens. The "subatomic = tokens" framing is a post-Frost overlay.
- Frost's chapter on tooling (Pattern Lab) is historical.
- Couldwell's Foundations Model (2019) is more current as practical taxonomy than Frost's chemistry, but pre-Variables.
- **Implication:** Practice's "Subatomic / Atomic / Molecule / Organism / Template" stack is a useful overlay we own — should not be attributed to Frost.

### 2.4 Component anatomy / props / API design
- Frost stops at "molecule / organism" as taxonomy.
- Couldwell discusses naming and structure but not props/API.
- The UIC series (Nov 2024) is the practice's only deep treatment of component anatomy and properties.
- Curtis's *Components as Data* (Sep 2025) is the most current external treatment.
- **Implication:** This is one of the few areas where the practice's IP is at or ahead of the public field. Worth defending and publishing.

### 2.5 Multi-brand and multi-mode theming
- All foundational books (2016–2019) predate the modes/themes era.
- Light/dark parity, density modes, brand themes as architectural decisions — none discussed in foundational material.
- Multi-Brand Governance (Apr 2025) is current but covers process, not technical theming.
- Curtis (Nov 2024) covers theming dimensions; aligns with internal stance.
- **Implication:** Modes and themes are recent enough that most clients (and many consultancies) treat them as advanced features. Practice should treat them as table stakes.

### 2.6 Sketch + Symbols + Sass tooling
- Couldwell's tooling chapter (2019) is mid-Sketch-era and treats Sass variables as the token primitive.
- Mangialardi (2021) is pre-Variables and uses Style Dictionary as the abstraction over Sass.
- **Implication:** Tooling guidance from 2016–2021 needs significant translation. The architectural logic survives; the implementation does not.

### 2.7 ROI methodology
- Sparkbox studies referenced by Mall (2023) are the most rigorous public ROI artifacts in the entire corpus.
- Most cited stats (40–50%, 4-months-to-minutes, 30%-a11y) trace to 2018–2020 case studies.
- **Implication:** ROI evidence is older than current AI-era productivity gains. Practice should refresh with post-2024 case-study data.

### 2.8 Idean / consultancy POV from 2019
- *Hack the Design System* (Idean, 2019) is the most direct peer-consultancy benchmark. Its case studies (ABB CommonUX, IBM Carbon, AT&T, Dell, Mozilla) are 5+ years old.
- **Implication:** Cite the patterns, not the snapshots.

---

## 3. POV gaps

Topics where internal documents take a position but it feels underdeveloped or untested against external thinking.

### 3.1 Centralized vs. cyclical at handoff
- Internal materials prefer Centralized with contribution. Curtis's stages (Solitary → Central → Federated) say cyclical/federated is the eventual destination.
- The practice's POV does not articulate the *expected evolution* — at what month does the client's system move from centralized-with-contribution to cyclical?
- Working synthesis to develop: handoff at Centralized with documented contribution path; expect cyclical evolution at month 9–12.

### 3.2 Prism positioning — CLOSED

**Closed by 33-white-label-systems §6 (June 2026).** Prism2 is properly described as a **white-label-as-starter foundation + starter library**, not a finished design system, and not a multi-tenant white-label-for-resellers platform. The closure rests on the two-shape framing per 33 §2 (white-label-for-resellers vs. white-label-as-starter): Prism2 ships a token foundation, a Figma component kit, and a coded counterpart in development; it accelerates the early stages of a bespoke client engagement; it does not ship a brand-generation engine, a Theme Schema contract, or a per-reseller onboarding pipeline. The features Prism2 ships position it as a *starter*; the features it does not ship position it as *not for-resellers*. The technology-team-adoption gap (per 00b) is the load-bearing constraint that holds Prism2 in the as-starter shape; a hypothetical Prism3 would need the engine + schema + pipeline layers Prism2 lacks (~450–750 hours of investment per 33 §6, plus standing technology-team capacity). The client conversation the closure unlocks: *"Prism2 is our white-label-as-starter foundation. It is not a multi-tenant reseller platform; if your business model requires dynamic multi-brand tenancy, that engagement is a different shape — Pattern 6 — and a different price."* The conflict closes because the framing is no longer ambiguous — Prism2 is one shape, the hypothetical Prism3 is the other shape, and the practice articulates both.

### 3.3 Documentation human-vs-machine reconciliation
- Scoping doc says docs must be human-first ("not an afterthought").
- AI-Compatible doc says human-only docs are now a *failure mode*.
- **Working POV to develop:** docs are a parallel layer (human + machine), generated from a single source. Practice should articulate the architecture explicitly.

### 3.4 "Selling DS" boundary
- Internal library is simultaneously the deck *about* selling DS and the deck *for* selling DS. The practice has not separated *what we believe* from *how we pitch*.
- **Working POV to develop:** what we believe is in this knowledge base; what we pitch is one or two layers thinner. Articulate both.

### 3.5 AI-readiness as commercial default
- Internal AI-Compatible doc treats AI-readiness as a parallel layer.
- External 2025–2026 consensus is that it's table stakes.
- Commercial proposals don't yet default to shipping the AI layer.
- **Working POV to develop:** by end of 2026, default every commercial engagement to ship tokens-with-descriptions, `.ai.json`, AGENTS.md, Code Connect. AI-readiness is no longer an add-on.

### 3.6 Engineering pipeline scope
- CareCentrix 2026 explicitly excludes front-end development. Defensible commercial position; also a real gap because tokens that don't reach engineers aren't tokens.
- **Working POV to develop:** scope a "design token pipeline" deliverable separately — not implementation, but the build pipeline that delivers tokens to engineers. Defensible middle path between full implementation and pure design library.

### 3.7 Centralized blind-spot mitigation
- Practice's deck recommends centralized while listing its weaknesses (no day-to-day product context, no influence on product designers).
- Recommendation and mitigation aren't always paired.
- **Working POV to develop:** every centralized recommendation ships with the explicit Ambassadors / Communities-of-Practice / Office Hours mitigation.

### 3.8 Composition over components for brand
- AI-Compatible doc names "composition is where brand lives" — strongest internal POV.
- UIC series teaches composition primitives.
- The two are not yet integrated into a unified composition-extension methodology.
- **Working POV to develop:** brand extension is a composition concern. The practice's composition primitives + 5-dimension brand-alignment rubric form the core of a defensible AI-era brand-extension service.

### 3.9 Two-thirds-people scoping
- InVision MVP (2020): a DS is collection + user base + contribution plan. Two-thirds is people.
- Practice scopes the collection.
- **Working POV to develop:** restructure commercial scoping to make the user base (1–3 sponsors + dev fanbase) and contribution plan first-class deliverables.

### 3.10 Borrow-don't-build for clients
- InVision MVP recommends starting from existing systems for the client's pilot; Prism does this internally.
- Practice does not always recommend borrowing as a starting move for clients.
- **Working POV to develop:** for clients without strong brand identity stakes (most B2B / internal-tools cases), recommend starting from Prism or Material as foundation; bespoke only when brand differentiation justifies it.

---

## 4. Open strategic questions

Things the practice should probably have a more developed answer to but doesn't yet.

1. **What is our minimum viable governance offering?** What can we credibly ship for a 12–16 week MVP engagement that a client team can actually run after we leave?
2. **What is our pricing model after handoff?** Retainer? Subscription? Federated chargeback? Quarterly review? All three?
3. **What is our maturity diagnostic offering?** Productize a "Where are you on the curve?" workshop using InVision's 5-level or Paavan's 0–4 ladder.
4. **What is our defensible ROI methodology?** Borrowed stats are the field standard. The practice's case-study volume could publish its own calculator. By when?
5. **What is our position on AI-generated UI?** AI-readiness is forward POV; should be commercial default by end of 2026. By when does every engagement ship an AI-readable layer by default?
6. **When do we recommend *not* starting a system?** The Six Signs recognize when one is needed. We don't have an articulated set of conditions under which we would advise a client to *wait*. (Hacq's "low-maturity org" caveat suggests this should exist.)
7. **What is our stance on single-tool dependency?** All AI-cluster sources are Figma-centric. Penpot for on-prem; Sketch holdouts; XD legacy clients. What is our cross-tool POV?
8. **How do we sell the engineering pipeline without selling implementation?** The token build pipeline is a discrete deliverable; not currently scoped or priced.
9. **What is our maintenance-readiness diagnostic in Discovery?** Currently absent. Should be a Discovery question: *Is the org committed to funding the system after handoff?*
10. **What is our public-IP strategy?** The UIC series, the 5-dimension brand-alignment rubric, the AGENTS.md/CLAUDE.md instruction-file layer, the practice's component metadata schema — all defensible POV differentiators not yet published. Should some be published to establish thought leadership? Which?
11. **Where does Prism go?** Prism's positioning conflict (DS vs. UI Kit) needs resolution. What's Prism's roadmap relative to client engagements? When does Prism2 become Prism3, and what does that mean for engagements built on Prism2?
12. **How do we staff the practice?** Curtis's 1:2 designer:dev, 50% capacity floor, three-leads structure is one model. What's our default? How does it scale across simultaneous engagements?
13. **What is our position on AI tooling for our own team?** Internal practice is presumably using Cursor, Claude, Figma Make. Is there a documented practice-internal AI tooling policy and proficiency standard?
14. **What is our deprecation default?** 6 months for major components, 3 months for tokens — working synthesis. Need to commit.
15. **What is our coverage definition?** Curtis names three; we should pick. (Working synthesis: Morningstar's *% of pages applying system components*.)

---

## 5. Field-level gaps (not addressed by any source material)

Per the brief's final-check instruction: areas significant to design systems consultancy clients that are absent or shallow across all source material — internal and external. These are gaps the practice could lead by addressing.

### 5.1 Internationalization, localization, RTL, and bidirectional layout
- This gap is now articulated. (See 13-internationalization-and-rtl.)
- Original gap framing: source material was English-language Western-context; specific concerns included bidirectional layout (Arabic, Hebrew), text expansion, CJK typography, date/time/number/currency formatting at the component level, ICU MessageFormat for pluralization. For multi-region clients (Ford's 5-region case study is the only internal example), this is a real procurement-grade requirement.

### 5.2 Data visualization and charting
- Not addressed by any source.
- Charts have their own foundations (color encoding accessibility, axis conventions, legend patterns, accessibility for screen readers, animation in transitions).
- For healthcare (CareCentrix), financial services (Thrive), and most B2B SaaS, data viz is a required deliverable. Practice should have a charting POV.
- **Partial close (color layer): 31-color-systems.md §7** lands the data-viz palette architecture — three palette types (categorical / sequential / diverging), the 8–12 categorical limit and table-fallback contract, OKLCH-derived sequential ramps for accurate perceptual ordering, and the **isolation rule that data-viz tokens must never alias UI tokens**. The non-color half of charting (axis conventions, legend patterns, AT announcements, transition animation) remains open.

### 5.3 Email and notification design
- Email has fundamentally different rendering constraints (table-based layout, limited CSS, dark-mode quirks per client). No source addresses email design within DS scope.
- Push notifications, SMS, in-app messaging similarly absent.

### 5.4 Voice and conversational interfaces
- Conversational UI design (chat, voice assistants, embedded AI) has its own patterns (turn-taking, error recovery, persona consistency, tone-of-voice systematization).
- Increasingly relevant in 2026 with AI-driven product surfaces.
- **Largely closed by 25-ai-aware-patterns-and-conversational-ui (May 2026)** — chat input / streaming response / message-thread / tool-call / citation / refusal / disclosure as published-pattern clusters, the production-grade triad (Cloudscape, Atlassian Rovo, Twilio Paste), Vercel AI Elements as the leading open primitive layer, and the architecture/governance contract underneath. **Further closed by 26-adaptive-interfaces-foundations and 27-adaptive-interfaces-implementation (June 2026)** — the broader pattern set chat sits inside (Sentient Triangle scaffold, four postures, fourteen experience patterns including bespoke UI / intelligent canvas / call-and-response), the personalization-vs-adaptation diagnostic, and the implementation reality (five-rung spectrum, variant logging, eval-driven QA). Voice as a first-class input mode (transcription, diarisation, interruption semantics) is partially addressed but remains the residual gap; tone-of-voice systematization for assistant copy across product surfaces is the other piece still un-codified.

### 5.5 Embedded, automotive, TV, and non-web platforms
- Mobile DS practice (iOS, Android, Flutter) is now articulated. (See 11-mobile-and-cross-platform.)
- Ford's in-vehicle work appears in the case study but the methodology isn't generalized.
- TV (10-foot UI), automotive (driver-distraction-aware design), embedded (constrained hardware), wearables (small surfaces), AR/VR — all platform-specific concerns still absent across sources.

### 5.6 Performance budgets at the component level
- Token compliance is measured. CSS bundle size, JS bundle size, render performance, animation jank, image weight per component — not addressed.
- For mobile-heavy or low-bandwidth clients, this is significant.

### 5.7 Privacy and PII handling baked into components
- Forms collecting PII, medical components, financial components have specific privacy requirements (data minimization, consent UI, secure input handling, accessibility for screen readers without leaking data).
- HIPAA-compliant healthcare design (CareCentrix) implies but doesn't articulate component-level privacy patterns.

### 5.8 Component-level analytics and instrumentation
- How does a Button know it's been clicked? Should the system include analytics instrumentation by default?
- For data-driven clients, instrumented components are how the system measures coverage and use; absent from all sources.

### 5.9 Hiring, role definitions, and career paths within DS practice
- Curtis names roles (lead, designer, developer, QA, PM, content). No source articulates job descriptions, leveling (junior → senior → staff → principal), career paths, or compensation benchmarks for DS practitioners.
- Practice clients ask "how do we hire for this?" Currently no productized answer.

### 5.10 DS team operating budget benchmarks
- "What does it cost to run a DS team for a year?" "How does that compare to peers?" No source provides benchmark data. Worth a survey or panel research project.

### 5.11 Legal, IP, and licensing
- Third-party fonts (commercial licensing for digital + brand use), icon licensing (open-source vs. proprietary), photography rights, AI-generated content provenance.
- Obello (2026) flags AI-output indemnification; otherwise silent. For regulated industries, this is procurement-grade.

### 5.12 Sustainability and environmental impact
- Performance and bundle size connect to energy use; image weight × audience × frequency = real CO2.
- Lighter components, fewer bytes, fewer round-trips → measurable impact.
- Increasingly a procurement consideration in EU and ESG-conscious clients.
- Not addressed by any source.

### 5.13 DS for AI-native products
- Most DS thinking assumes the consuming product is a deterministic UI.
- AI-native products (generative interfaces, conversational flows, ambient AI) have different composition rules — the system constrains what AI can do, not just what humans build.
- Anderson's "infrastructure" reframe gestures at this; Wolosin's metadata loop touches it; neither articulates DS-for-AI-products as a distinct practice area.
- **Partially closed by 25-ai-aware-patterns-and-conversational-ui (May 2026)** for the consumer-facing pattern surface (chat, citation, refusal, tool-call, approval workflows) and by 15-ai-in-ds for the operator-side architecture (components-as-data, MCP, structured metadata). **Largely closed by 26-adaptive-interfaces-foundations and 27-adaptive-interfaces-implementation (June 2026)** — the practice now commits to Sentient Design as strategic vocabulary (with attribution to Clark & Kindred), the Sentient Triangle and four-postures scaffold, the fourteen experience patterns (including the canvas trio: composition / document / interface), the five-rung engineering spectrum that locates production work in the middle (Rungs 3–4: slot-based generation and structured-output rendering), and the design-system implications (primitives over composed components, semantic component contracts, evals replace screen-by-screen QA, variant logging as infrastructure). The residual gap that remains is **purpose-built authoring tooling for variability** — no design tool currently lets a designer specify a *space* of possible outputs and review the *distribution* of what comes out (the academic "variability by design" problem); component-prompt pairs are the emerging artefact but not yet a first-class object in any design tool. Worth tracking and possibly worth productising as a Prism2 extension.

### 5.14 Cross-tool design-source migration
- Sketch → Figma migrations. Figma → Penpot. XD legacy. 
- Real client need; no source addresses methodology.

### 5.15 The DS-as-vendor-product market
- DS-as-a-service vendors (Knapsack, Supernova, Specify, Tokens Studio, Zeroheight) are increasingly commercial product layers between consultancies and clients.
- No source articulates how to evaluate them, how to integrate with them, when to recommend them, or how their pricing models affect total cost of ownership for clients.

### 5.16 DesignOps as a separate discipline
- Brand → DS → Product is the practice's layered model. DesignOps (tooling, process, hiring, measurement, vendor management for the design function) is adjacent but distinct.
- Often co-bought with DS engagements; not articulated as a discrete discipline.

### 5.17 Design systems for compliance-first products
- Healthcare (HIPAA), financial (PCI, SOX), accessibility-mandated (Section 508), GDPR, CCPA — each imposes design constraints that the system can encode.
- Internal materials touch healthcare via CareCentrix and accessibility via WCAG; the broader compliance-as-system-feature framing is absent.

### 5.18 The "ethics of systems" conversation
- Perez-Cruz raises this implicitly (*"Systems aren't neutral"*) but the operational implication — what does inclusive contribution to a DS look like, who gets veto, who gets praised — is largely absent.
- Increasingly relevant as AI consumers introduce their own bias surfaces.

### 5.19 Knowledge transfer and engagement-end protocols
- What does the practice ship to a client at the moment the engagement ends? A recorded walkthrough? A 30-day Q&A window? A Slack channel that stays open? An "office hours" handover?
- Most engagements treat handoff as a single moment; the engagement-end protocol is improvised. Productizing it would close a real gap.

### 5.20 Failure recovery patterns
- What happens if the system loses its champion? Loses funding? A consuming team forks the system? An audit shows low coverage?
- Practice has implicit experience; nothing documented.

### 5.21 SEO, GEO, and agent-discoverability for DS docs sites
- Absent across all source material. Grep across the corpus returns one false positive (§1.27a "search" in another sense) and a single line in 07 §Specialists negotiable (SEO as a partial role). 25 §A practical lesson names the Zeroheight-behind-anonymous-fetch pattern as making research-by-fetching impossible — that observation is *adjacent* to the gap but does not articulate it.
- The 2025–2026 layer the practice does not engage:
  - **`llms.txt` / `agents.txt`** — emerging convention for sites declaring what an LLM crawler should index, analogous to `robots.txt`. Whether DS docs sites should ship one, what it should contain (the `.ai.json` registry path? the conformance dossier index? component prose?), and how it interacts with hosted-platform constraints (Zeroheight, Supernova) is undefined practice-wide.
  - **Generative Engine Optimization (GEO).** How a DS docs site ranks in AI-generated answers (ChatGPT, Perplexity, Claude.ai-as-search, Gemini summary). The optimisations differ from traditional SEO — citation-friendliness, structured authoritative claims, machine-readable provenance — and connect directly to 30's `.ai.json` registry-served-via-MCP architecture, but the practice has not yet positioned its docs architecture as GEO-favourable explicitly.
  - **Schema.org / structured data.** Whether DS docs output JSON-LD, whether the `.ai.json` registry should align with schema.org typing, whether per-component pages should be marked up as `SoftwareApplication` or `TechArticle` — all open. Storybook's autodocs output is not currently schema.org-typed by default.
  - **Crawlability of DS docs for LLMs vs. for traditional search.** Hosted platforms (Zeroheight in particular) often gate content behind anonymous-fetch barriers that block LLM training and serving crawlers as well as research-by-fetching. The procurement implication — clients on closed platforms inadvertently disqualify themselves from being cited by AI assistants — is a real concern the practice should have a stance on.
- Connects to §1.13 (Trust, governance, liability for AI-generated assets) — this is a *consumer-facing* extension of that. Connects to §1.12 (AI-readiness as commercial default) and §4.10 (public-IP strategy).
- **Likely path: a new initiative, but not the highest priority — surface when a content-heavy or regulated-industry client asks the question.** Log the gap; do not lead with the topic.

---

## How to use this file

This is a working document. Three suggested actions:

1. **Quarterly review.** Walk the file at quarterly practice-leadership meetings. Mark items closed (with the artifact that closed them), in-progress (with owner), or deferred (with rationale).
2. **Engagement scoping.** Cross-reference against active engagement scope. Items in Section 1.1, 1.4, 1.7, 1.10 are candidates for scope expansion in any current pitch.
3. **POV publishing.** Items in Section 1.12, 1.13, 4.10 are candidates for external thought-leadership publishing. The practice has the IP; publishing establishes claim.

The single most consequential closure: **Section 1.1 commercial scoping** plus **Section 4.2 pricing-after-handoff**. These together convert the practice from a build-engagement model to a build-and-operate model. Most other gaps are sub-claims of this one.

---

*This file is a synthesis across all 9 phase files plus the practice's source material plus the broader field. Items marked as field-level gaps (Section 5) draw on practitioner knowledge of the design systems field circa 2025–2026 beyond the source material reviewed for this knowledge base.*
