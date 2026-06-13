---
type: practice-area
title: Gaps and Open Questions
description: Practice gaps and unanswered questions across the corpus. Sourced inventory of what we don't yet have a POV on.
tags: [gaps, open-questions]
timestamp: 2026-06-10
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
- **Code Connect not defaulted.** Practice has IP; commercial proposals don't ship Code Connect bindings by default. By 2026 this should be standard.
- **Custom MCP server / registry not commercial.** Internal POV; not yet sold.
- **Engineering-onboarding artifact not produced.** Couldwell's `docs/decisions/`, `docs/onboarding/`, `docs/meeting-notes/` patterns; almost no client has them.
- **Headless vs. opinionated component architecture stance** undocumented.

### 1.8 Component-level accessibility annotations — CLOSED
- **Closed by 14-accessibility (architecture), 16-mobile-accessibility-implementation (framework depth across Flutter, Compose, SwiftUI/UIKit, React Native), and 17-accessibility-annotation-contract (the per-component annotation spec — name, role, state, value, focus, scaling, inversion, motion, gestures, live regions).**
- The remaining sliver — web implementation depth and the ARIA-specific annotation fields — is the new gap (see §1.16 below).

### 1.9 Motion as foundation
- Motion appears in token lists but the practice does not yet ship motion principles, motion audits, easing studies, or productive/expressive splits as foundational deliverables.
- Head's framework (principles → building blocks → choreography) is straightforward to adopt and would close the gap.
- **Closed (architectural layer) by 18-motion-foundations, 19-motion-implementation-web, 20-motion-implementation-mobile, and 21-motion-spec-and-handoff (May 2026).** Open gaps that remain are now downstream of the architectural treatment: cross-platform spring calibration as a practice deliverable (a starting mapping table is in 20 but the side-by-side reference videos are not yet a practice default); Pattern A vs. Pattern B tooling for the motion spec contract (a Figma-plugin or pipeline to emit machine-readable spec files does not yet exist as a turnkey product); the productive vs. expressive choice between parallel token sets and override-mode is not yet a practice default.

### 1.10 Documentation IA and templates
- Reference-site information architecture is named; not delivered as a deliverable.
- No standard practice template for the per-component doc page (purpose / when-to-use / avoid-when / props / states / accessibility / examples / do-don't / content / related / changelog).
- Tooling opinion is thin (Storybook / Supernova / Pattern Lab / Zeroheight / GitBook listed without trade-offs).
- Generated-from-data documentation not yet default; practice ships authored prose.

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

### 1.16 Web accessibility implementation depth
- 16-mobile-accessibility-implementation and 17-accessibility-annotation-contract are mobile-scoped. Web teams currently retrofit ARIA, `prefers-reduced-motion`, `prefers-contrast`, `forced-colors`, `inert`, `focus-visible`, ARIA APG keyboard interactions, and complex `aria-controls` relationships at PR review.
- The web equivalents of the annotation contract fields (name, role, state, value translate cleanly to ARIA; merging/traversal/dynamic-type/system-inversion have materially different mechanics).
- Next natural research run; explicitly flagged in 17.

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

### 3.2 Prism positioning
- VML library calls Prism alternately a "design system" and "an internal UI Kit and set of tools."
- The deck says DSes are *not* UI Kits — yet Prism is sometimes labeled one.
- **Working POV to develop:** Prism is properly described as a **white-label foundations + starter library** that accelerates the early stages of a bespoke client system, not a finished system. Document explicitly.

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

---

## How to use this file

This is a working document. Three suggested actions:

1. **Quarterly review.** Walk the file at quarterly practice-leadership meetings. Mark items closed (with the artifact that closed them), in-progress (with owner), or deferred (with rationale).
2. **Engagement scoping.** Cross-reference against active engagement scope. Items in Section 1.1, 1.4, 1.7, 1.10 are candidates for scope expansion in any current pitch.
3. **POV publishing.** Items in Section 1.12, 1.13, 4.10 are candidates for external thought-leadership publishing. The practice has the IP; publishing establishes claim.

The single most consequential closure: **Section 1.1 commercial scoping** plus **Section 4.2 pricing-after-handoff**. These together convert the practice from a build-engagement model to a build-and-operate model. Most other gaps are sub-claims of this one.

---

*This file is a synthesis across all 9 phase files plus the practice's source material plus the broader field. Items marked as field-level gaps (Section 5) draw on practitioner knowledge of the design systems field circa 2025–2026 beyond the source material reviewed for this knowledge base.*
