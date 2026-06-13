---
type: practice-area
title: Tokens at Scale
description: Operational layer for enterprise multi-brand token systems. Multi-collection-not-multi-mode, Generative Token pattern, blast-radius-weighted RACI, the Cascade Report, semver-for-tokens, build-vs-buy.
tags: [extension, tokens, scale, multi-brand, governance, semver]
timestamp: 2026-05-16
---

# 24 — Tokens at Scale

> Small token systems can hand-wave governance, validation, and versioning. Large ones cannot — and our agency clients are increasingly the latter, with multi-brand portfolios that hold five to twenty brands and engagements that need to survive years of post-launch change. This file is the operational layer for token systems at that scale: multi-brand collection architecture, governance weighted by blast radius, validation that the system can run against itself in CI, semver applied honestly to a visual API, and the tools landscape at the enterprise tier. Where 22 is the spec-and-architecture layer, this file is the operations layer on top of it.

---

## What "at scale" actually means

A single-product token system can live with informal governance, manual review, and ad-hoc deprecation. **The point at which "at scale" becomes a different problem is roughly when any one of three thresholds is crossed:**

- The system serves three or more brands sharing a foundation tier.
- The system has more than one consuming codebase that pins a token version.
- The team that maintains the tokens is structurally separate from the teams that consume them.

Past any one of these thresholds, the failure modes of small-system token work — drift, manual migration, validation by review only, undocumented overrides — become structural. They cannot be solved with more discipline; they need architecture. This file is what that architecture looks like.

The positions in this file build on 22 (DTCG 2025.10 mechanics, computed-tokens-at-authoring discipline, the mode-multiplication-as-collection-decomposition pattern) and on 12-figma-practice (Variables, modes, scoping, the cross-file alias risk). Read both first.

---

## Multi-brand portfolio architecture

### Collections, not modes, for brand

The single most-load-bearing architectural decision in a multi-brand system: **brand is a collection axis, not a mode axis.** Modes work for theme (Light / Dark), density (Compact / Comfortable), and maybe contrast (Standard / High). Modes fail for brand because brand axes multiply rather than compose. Three brands × two themes × two densities is twelve modes on a single collection; with five brands the same matrix is twenty modes on a single collection, which is unusable in Figma and incoherent in code.

The convergent pattern (it has been called the "12-practice model" in some recent agency writing, building on the architecture 12-figma-practice already names at a smaller scale):

- **A single Global Foundations collection.** Read-only for brand teams. Holds cross-brand primitives — neutral spacing scales, timing functions, base neutral palettes, target-size floors, anything that should not vary by brand. This is the shared core.
- **A Brand Semantic collection per brand.** Each brand's collection aliases the Global Foundations primitives to brand-specific intents. The collection does not hold *new* values; it holds *aliases* that express how this brand's semantics map to the shared primitives. Modes within a brand's collection are for that brand's themes (Light / Dark) and density.
- **A Components layer that consumes brand semantics through a swap.** Components reference a generic "Blueprint" library; when Brand X is the rendering target, the Blueprint library is swapped for Brand X's Semantic library. The component code is written once; the brand-specific expression rides on top.

This is the architecture that makes the cost of adding the Nth brand sublinear. **A well-architected portfolio's tenth brand should cost roughly 10% of the first; a poorly-architected one's tenth brand costs more than the first** because every per-brand override has to be re-derived across the now-fragmented system.

### Brand inheritance vs. brand isolation — managed inheritance as the middle

Two extremes neither of which is correct:

- **Total inheritance.** Every brand is a strict subset of the core. Maximum consistency, zero brand autonomy. Brands with genuinely unique UI requirements (luxury brands needing larger radii, technical brands needing tighter density) are forced into compromise that visibly degrades them.
- **Brand isolation.** Each brand is a silo, with no shared foundation. Maximum brand autonomy, zero portfolio efficiency. Every change has to be made twenty times.

The middle is **managed inheritance.** Brands inherit the Standard Semantic layer by default. If a brand's requirements fall within ~80% of the core, the brand uses the core semantics unchanged. Where the brand's requirements diverge, the brand forks specific token sets — but the fork is governed:

- **Cosmetic deviations** (color, border radius, font family) → theme override at the Brand Semantic collection.
- **Functional deviations** (new layout logic, new component anatomy, density profiles the core doesn't have) → candidate for a new semantic pattern *in the core*, which other brands can then adopt or not.

The governance rule prevents the forks from accumulating into de facto silos. A brand can override the value of `color/bg/primary` without permission; a brand that wants to introduce a new token category goes through review at the core.

### Naming is intent-based, not brand-bound

A common failure pattern at the multi-brand scale: encoding the brand name in the token itself. `color-bg-primary-brand-alpha`. This produces tokens that cannot be referenced by shared components — every consumer has to know which brand it is rendering for and import the right token name. Components fragment by brand.

**The convergent pattern is mode-driven resolution with brand-neutral names.** The token is `color/bg/primary`. The value resolves at build time (Style Dictionary) or runtime (CSS custom properties + brand attribute) based on which brand is the rendering target. The same component code references the same token name and gets the right brand's value automatically.

The naming taxonomy that survives the multi-brand scale: `[category]/[property]/[concept]/[state]`. For example, `color/text/on-action/hover`. This shape carries semantic clarity across twenty brands because the intent is invariant even when the value isn't.

### White-label and reseller scenarios

The hardest portfolio scenario is the one where the brand list is unknown at architecture time — white-label products that ship to dozens or hundreds of resellers, each of whom supplies their own brand inputs. Hardcoding brand values is impossible; even Brand Semantic collections do not scale to "an arbitrary number of unknown future brands."

The architectural pattern is **contract-driven interoperability.** The DS defines a Theme Schema: a JSON contract that specifies exactly which values a brand must provide (primary color, logo URI, font stack, brand radius, brand density). A Theme Resolver — typically a custom Style Dictionary transform or a runtime CSS-variable injection step — injects the brand-supplied values into the global semantic framework.

This shifts the agency's role from "designing each brand" to "architecting a brand-generation engine." Resellers supply the minimum brand-defining values; the system generates the rest. The economic shape of this engagement is different — recurring brand-onboarding revenue rather than per-brand design effort — and the practice should flag it explicitly when scoping white-label work.

### The Generative Token pattern

A related and more aggressive extension: deriving a brand's entire semantic layer from a small set of primitives via standardised computation. The pattern names a brand by five to ten core primitives — a primary color, a neutral hue, a typeface, a radius, a density step — and computes the rest of the semantic layer mechanically. Tints from the primary are derived via OKLCH lightness adjustments (rather than hand-picked); accent semantics map by formula; density-aware spacing tokens generate from the brand's chosen density step.

Mature systems doing this (Adobe Spectrum's light/dark math, IBM Carbon's contrast-pinned palettes) report onboarding costs for an additional brand of roughly 10% of the first brand's cost.

**Practice position:** the Generative Token pattern is the field's most-promising direction for multi-brand at scale, and the practice does not yet ship it as a default. The investment to build the computation set is meaningful but one-time per portfolio. **Treat as a known pattern that warrants investment in the next portfolio engagement** (also flagged in 09 as a gap between what the field has moved to and what our commercial proposals currently default to).

---

## Governance at scale

Governance weight should track blast radius. The principle is mechanical: the larger the consequence of a change, the more friction the change passes through. **A primitive change cascades to every brand and every consuming codebase; a semantic change cascades to every component in one brand; a component-token change cascades to one component.** Each layer needs governance proportional to its cascade.

### RACI by token tier

| Token tier | Responsible | Accountable | Cascade |
|---|---|---|---|
| Primitive (spacing scales, neutral palettes, timing) | Central DS team | DS lead | Portfolio-wide; affects every brand. |
| Semantic (`color/bg/primary`, `font-size/body`) | Brand lead / DS liaison | Head of brand | One brand; every component using that semantic. |
| Component (`btn/padding/inline`, `card/border-radius`) | Product team designers | Product lead | One component in one brand. |

The right RACI by tier makes governance enforceable without bureaucracy. A product designer can change a component token without central-team approval; a brand lead can change a brand semantic without portfolio-wide review; a primitive change passes through the central team and an impact review. The friction matches the consequence.

This extends 07-governance-and-adoption's contribution-flow patterns into the token-specific layer. Where 07 names the contribution process at the component layer (the rule-of-three promotion, the contribution review), this file names it at the token layer (the blast-radius-weighted RACI, the cascade report).

### The change-review process

The gate between a Figma variable edit and a production deployment is the **Token Pull Request**. A change to a Figma variable triggers a background sync to a Git repository (Tokens Studio, Supernova, or a custom pipeline); the PR is the artefact that gates production.

Every Token PR passes three gates:

1. **Technical validation.** Automated CI checks the JSON against the DTCG schema, runs alias resolution, runs contrast validation. Structural and accessibility failures block the build. (See the Validation section below.)
2. **Design review.** Peer review by another designer confirms the token name follows the taxonomy, the aliasing logic is correct (semantic tokens reference primitives, not literals), and the change does not duplicate or conflict with existing tokens.
3. **Impact analysis.** For primitive changes specifically, CI generates a **Cascade Report** showing every brand and every component affected by the change. This is the single artefact that prevents "we didn't realise this would change Brand Q" failures.

The Cascade Report is the practice's most-undersold operational artefact. Generating it requires the token system to maintain a dependency graph (which tokens reference which, which components reference which tokens, which brands resolve to which primitives). Style Dictionary v4's resolver exposes enough information to generate it; Tokens Studio's API supports a Figma-side equivalent. The practice should ship the Cascade Report as a default deliverable on portfolio engagements past three brands.

### Deprecation as a window, not a switch

Tokens are an API. Renaming or removing a token is a breaking change for every consumer. **Tokens at scale are never deleted; they are sunset through a window.**

The deprecation pattern that has converged across the field:

- **Release N.** The new token is introduced. The old token is marked `$deprecated` (in `$extensions.<vendor>.deprecated` until the spec adds the property — see 22). The new and old tokens coexist; the new token is the alias target the documentation points to.
- **Release N+1.** The old token is aliased to the new token at the build layer. Consumers using the old token name continue to get correct values but receive a console warning (web) or compile warning (native) flagging the deprecation.
- **Release N+2.** The old token is removed from the documentation but remains in the code. Tooling can still resolve it; new code cannot find it via discovery.
- **Major release.** The old token is hard-deleted. By this point, codemod tooling should have migrated any remaining consumers.

This is the window. The duration of each step is engagement-dependent (a portfolio with fast-moving consumer codebases can compress to weeks; a portfolio with slow enterprise consumers needs quarters). The shape is the same: introduce → coexist → warn → remove. **Compressing the window because "no one uses the old token anymore" is the single most common cause of unanticipated breakage** at portfolio scale, because the people who maintain the system are not the people who consume it, and "no one uses it" is reliably wrong.

### Brand version pinning

A primitive change can break a sensitive brand even when the change is correct for the rest of the portfolio. Adjusting a base neutral palette can fail contrast for one brand whose semantic tokens push the contrast pair to a margin. The portfolio cannot wait on the slowest brand to upgrade; the slowest brand cannot accept a change that breaks its WCAG conformance.

**Brand Version Pinning** is the convergent solution. Most brands track the latest Global Foundations release; a brand can opt to pin its semantic layer to a specific Foundations version while it reviews the change. The pinning is explicit (it shows up in the brand's `package.json` or equivalent token-version manifest); the brand has a stated unpin date; the central team can see which brands are pinned and to which versions.

This is "federated computational governance" applied to tokens — local autonomy within global constraints. The pattern borrows from data mesh architectures and lands cleanly in the token domain because tokens have the same shape problem (one source of truth, many consumers with different cadences).

### Cross-brand drift

The failure mode that brand version pinning exists to prevent in one direction is the same failure mode that managed inheritance exists to prevent in the other: **brands fork specific values for legitimate reasons, and then the cumulative drift across the portfolio becomes invisible to anyone reviewing one brand at a time.**

The architectural fix is visual regression testing at the token layer. Style Dictionary or a documentation platform renders each brand's component set; visual diffs flag where brands have drifted from the core logic. The diff is the conversation-starter; the governance question — should this brand re-converge or should the core absorb the variant — is for the design lead to answer.

---

## Validation as executable architecture

Validation is the mechanism by which the architecture you've described in 22 and earlier in this file becomes executable. **The system can run against itself in CI; bad tokens fail the build.** This is the load-bearing operational capability at scale.

### What gets validated

| Check | Tool | Severity |
|---|---|---|
| DTCG schema compliance (`$value` / `$type` / `$description` / `$extensions` shape) | JSON Schema validator (`ajv`); Style Dictionary v4 native; Token Forge | Error — blocks build |
| Alias resolution (no broken references, no cycles) | Style Dictionary v4 native; custom resolver | Error — blocks build |
| Contrast validation (every pair token meets WCAG / APCA threshold across every brand × theme × density) | `colorjs.io`; `apca-w3`; custom CI step | Error — blocks build |
| Relationship rules (primitives not consumed directly by components; semantics don't hold literal values; composites reference primitives or semantics only) | Custom linter | Warning by default; can be promoted to error |
| Naming-convention conformance (matches `[category]/[property]/[concept]/[state]`) | Custom linter | Warning |
| Dead-token detection (tokens with no component references; tokens referencing deleted primitives) | Token-usage scanner | Warning |

### The errors-vs-warnings discipline

The single most-important governance decision in token validation: **only structural and accessibility failures are blocking errors; naming, dead-token, and relationship-rule failures are warnings.** This is the anti-fatigue position.

The trap is over-blocking. A CI pipeline that fails every PR for a minor naming convention violation produces engineers who learn to ignore the warnings and copy-paste the override flag into their config. The validation infrastructure that was supposed to enforce quality becomes a discoverable workaround.

The correct partition:

- **Always block (Errors):** DTCG schema, broken aliases, contrast failures, type mismatches against `$type` allowlist. These are correctness failures; the system cannot ship them.
- **Surface but allow (Warnings):** Naming convention drift, dead tokens, relationship-rule violations (primitive consumed directly, semantic with literal value). These are quality concerns; they require human judgement to triage; over-blocking them defeats their purpose.

Warnings should be reported in the PR, accumulated in a dashboard, and reviewed by the central team periodically. They should not stop the build. **The system's job is to make quality visible, not to make it mandatory at every layer.**

### Contrast validation across the matrix

The single check with the highest leverage at portfolio scale: contrast validation across the *full* brand × theme × density matrix. A change to `color/bg/primary` in Brand B for Dark mode at Compact density must pass contrast against every text token that pairs with it. Manual review cannot reliably catch matrix violations at twenty brands; CI must.

This extends 14-accessibility's pair-tokens architecture into the validation pipeline. Pair tokens are the *encoding*; matrix contrast validation is the *enforcement*. Together they make accessibility-by-default mechanical rather than aspirational.

The practice should default to validating both WCAG 2.x and APCA in CI:

- **WCAG 2.x** is the regulatory standard. Procurement and conformance claims (ACR / VPAT) reference WCAG 2.x.
- **APCA** is the perceptually-correct successor. It catches real readability failures that WCAG 2.x passes (light text on dark saturated colors, certain hue pairs at borderline contrast).

Run both. Block on WCAG failures (regulatory floor); surface APCA failures as warnings to the design lead (readability quality).

---

## Versioning and migration

Tokens are a visual API. Semantic versioning applies — with adapted rules that account for the fact that breaking changes can be visual, not just structural.

### Semver for tokens, honestly

The adapted semver rules:

| Bump | What it covers |
|---|---|
| **Major (X.0.0)** | Token renamed or deleted. Token whose `$value` change breaks a contrast pair (visual breakage that affects compliance). Token whose `$type` changed. Structural changes to the token file. |
| **Minor (0.X.0)** | New tokens added. New brand added. New mode added to an existing collection. |
| **Patch (0.0.X)** | Value change that does not affect contrast pairs or structure. A typographic adjustment. A small color tweak. Documentation-only changes. |

The non-obvious rule is the contrast-pair one. **A `$value` change that breaks contrast in any brand × theme × density combination is a major bump, even when the token's shape is unchanged.** The reason: consumers pinning to a minor version expect not to receive a regression that fails their accessibility conformance claim. Treating contrast-breaking value changes as major bumps preserves that expectation.

This rule is the most novel position in our practice's token-versioning POV and the most important one to commit to explicitly in client materials.

### Codemods

Manual migration across twenty consumer codebases is an operational failure. Renames and signature changes ship with codemods — automated transformation scripts (typically `jscodeshift` for web, `swift-syntax` for iOS, `kotlin-compiler-plugin` for Android) that parse the consumer's source and apply the migration mechanically.

The practice's commercial proposal for any portfolio engagement past three brands should include codemod authorship as a default deliverable for any breaking token change. This is the single most under-sold piece of token operations in our pitches today.

### Pinning vs. tracking

Consumers in production should pin to a minor version of the token package. Tracking `latest` is correct for marketing-tier surfaces (fast iteration, brand currency matters); pinning is correct for product-tier surfaces (accessibility conformance, predictable releases).

The release-note artefact for any token change should include:

- The semver bump and the reason.
- A visual diff showing the component-level impact across every brand the change touches.
- The codemod (if any) and instructions to run it.
- The pin-vs-track recommendation for this release.

This is the changelog as an executable migration plan, not as a list of hex changes.

---

## The tools landscape at scale

The 2026 landscape stabilises into three categories. **None of them does everything; the practice composes from them.**

### Authoring tools

- **Figma Variables.** The default authoring surface for tokens in 2026. Composite types and the Resolver Module's coming mode treatment continue to mature. The native variable system is sufficient for most engagements up to mid-complexity.
- **Tokens Studio.** Still the right tool past Figma Variables' limits — math expressions, multi-collection inheritance, deeper composite-type handling. The position the tool's vendor has carved out is "advanced management suite," and it holds in 2026. Tokens Studio is the right choice when the system needs math at authoring time, when the brand portfolio exceeds Figma's mode caps, or when the team needs DTCG-compliant export with full fidelity.
- **Penpot.** The open-source alternative to Figma, with first-class DTCG support and (notably) no proprietary tier between the authoring surface and the export format. Worth tracking; not yet a default.

### Build pipelines

- **Style Dictionary v4.** The load-bearing engine in our practice's stack. Native DTCG 2025.10 support, async transforms, idiomatic per-platform output, brand-aware composite type handling. The right answer for any portfolio engagement where the client takes code ownership.
- **Terrazzo.** A reference implementation of the DTCG spec; worth tracking for clients who want a thin, spec-conformant build with minimal opinion.
- **Custom pipelines.** Still appropriate where the client has proprietary platform requirements (embedded systems, in-house design language with no off-the-shelf transform).

### Token operations platforms

- **Supernova.** Has moved beyond documentation into a Token Operations Platform — automated code delivery (Figma change → PR to multiple repositories), versioning, governance dashboards. The right answer for clients in operate-mode retainers where the agency manages the ongoing pipeline.
- **Specify.** Similar positioning to Supernova; emphasises the Enterprise Data Layer (source of truth that feeds Style Dictionary and other downstream tools).
- **Knapsack.** Documentation-and-governance platform with token operations features. Useful when the engagement includes a substantial documentation deliverable.
- **AI-native token tools** are emerging through 2025–2026 (Token AI, prompt-driven token generation, AI-assisted contrast validation). The category is real but pre-stable; flag in client conversations as a watch-list, not a recommendation.

### Build vs. buy

The decision rule: **build with Style Dictionary v4 when the client owns the resulting code; buy a platform (Supernova / Specify / Knapsack) when the agency runs the ongoing operation as a retainer.**

The build path is right for handover engagements. Style Dictionary gives the client a maintainable, debuggable pipeline that their engineering team can own; the agency hands it over and steps back. The buy path is right for operate-mode engagements where the agency is the ongoing operator; managed platforms provide the UI and automation that make the operation cost-effective at scale.

Hybrid is common — Style Dictionary as the build core, Supernova or Knapsack for documentation and governance UI. The hybrid is fine when the build core is the source of truth and the platform is the consumer.

---

## Documentation as a deliverable at scale

Static documentation sites drift. Token documentation at scale must be generated from the DTCG source and re-rendered on every build. Hand-authored prose is appropriate for judgement-call content (usage guidelines, do-don't patterns, deprecation rationale); the catalog of tokens, values, contrast pairs, and usage examples is machine-generated.

### What good token documentation contains

Beyond the `$description` field:

- **Rendered usage examples** showing the token in situ across every brand × theme × density combination.
- **Contrast pass/fail matrix.** A live-rendered table showing which foreground/background combinations pass at the WCAG and APCA thresholds for each brand. This is the design lead's daily working artefact.
- **Deprecation history.** Visible inline at each deprecated token, with the migration target and the codemod link.
- **Provenance.** Where the token came from (primitive value, alias chain, computation source) and where it goes (which components consume it).
- **AI-agent metadata.** Token descriptions formatted for AI coding agents — "Use `color/bg/primary` for the background of call-to-action buttons. Do not use for general surface backgrounds." Hyper-specific use and not-use language.

The AI-agent description is the highest-ROI single addition to token documentation. AI agents reach for tokens by name and description; specific, exclusionary descriptions ("do not use for X") produce system-compliant generated code; vague descriptions produce drift.

### Living documentation, not static

The documentation is rebuilt from the token source on every release. Static documentation that "describes the system" drifts the moment the token source changes; living documentation cannot drift because there is only one source.

This is the same components-as-data argument that 15-ai-in-ds names for components, applied to tokens. The token JSON is the source of truth; documentation, code, Figma assets, and AI-agent context are all generated artefacts. The practice's commercial proposals for portfolio engagements should make this explicit — the deliverable is the data layer plus the generation pipeline, not a documentation site.

---

## Failure modes specific to scale

- **Brand encoded in token names** (`color-bg-primary-brand-alpha` instead of `color/bg/primary` resolved by brand mode). Components fragment by brand; reuse collapses; the cost asymmetry breaks.
- **Mode multiplication on a single collection.** Three brands × two themes × two densities on one collection = twelve modes. Decompose to one mode dimension per collection.
- **Central-team approval required for every token change.** The queue grows past usefulness; product teams route around the system. Federate — product teams own component tokens, brand teams own semantics, central team owns primitives.
- **Cross-brand drift accumulating invisibly.** Brands fork legitimate values; no one reviewing one brand at a time sees the portfolio-wide pattern. Visual regression testing at the token layer surfaces it.
- **Deprecation window compressed because "no one uses the old token."** This is reliably wrong; people who maintain the system are not people who consume it. Hold the window; trust the codemod.
- **Validation fatigue from over-blocking PRs.** Naming convention failures stop the build; engineers paper over with override flags. Block only on errors (structural, contrast); surface warnings to a dashboard.
- **Deprecated-token long tail.** Tokens deprecated five releases ago still present in the codebase because one product never upgraded. Telemetry on token usage in production + firm end-of-life dates on old versions.
- **No visibility on which tokens are actually used.** Style Dictionary builds the system from the source; nothing tracks runtime usage. The fix is token-usage telemetry from production (web: a build-time scan of compiled CSS; native: a Style Dictionary plugin that emits a usage manifest).
- **Build-or-buy decision made on cost rather than engagement shape.** Buying a platform for a handover engagement leaves the client with a vendor dependency they can't maintain; building a custom pipeline for an operate-mode retainer absorbs agency hours that should be billable as design work. Match the tool to the engagement shape.

---

## Tensions and open questions

1. **Generative Token pattern as a practice default.** The OKLCH-derived brand expansion pattern (5–10 primitives produce the rest of the semantic layer mechanically) is the field's most-promising direction for portfolio engagements past five brands. The practice does not yet ship it as a default. The build cost is real but one-time per portfolio; the per-brand efficiency is large. The case for adopting it is strong; the obstacle is that no current commercial proposal includes the tooling investment. **Surface in next portfolio engagement scoping; treat as a known pattern we will need to build the first time and amortise across the engagement and its successors.** (Also opened as a gap in 09.)

2. **APCA as the procurement-grade contrast standard.** WCAG 2.x is the regulatory floor; APCA is the perceptually-correct successor that catches real readability failures WCAG passes. The field is mid-transition. The practice should validate against both, block on WCAG, and warn on APCA. The conversation with clients about APCA-as-the-better-readability-measure is one the practice should be having more often.

3. **Token operations platforms vs. Style Dictionary as the long-term direction.** Supernova and Specify are absorbing operations work (Figma → PR pipelines, governance dashboards, telemetry) that previously required custom tooling. The trade-off is platform lock-in vs. custom-pipeline maintenance burden. The practice's current default of "build with Style Dictionary for handover engagements, buy a platform for operate engagements" is correct for the current state of the field; whether it survives the platforms' continued evolution is a watch-list item.

4. **`$deprecated` as a spec-level property.** Practitioners encode it in `$extensions.<vendor>.deprecated`. A spec-level property would simplify validation and codemod tooling. Watch the DTCG community group's 2026 drafts.

5. **The token-usage telemetry gap.** No standard for tracking which tokens consumers actually use in production. The "we don't know which tokens are used" problem is one of the more frequently-named failure modes in the field but has not yet produced a convergent tool. The practice should track this as an emerging requirement on portfolio engagements past two years' operation.

6. **AI-agent-generated tokens.** AI agents producing token definitions (rather than just consuming them) is a 2026 emerging pattern — prompt-driven brand expansion, AI-assisted contrast tuning, AI-generated semantic naming. The pattern is too immature to commit to but should be in scope for any portfolio engagement starting mid-2026 or later. Flag as a watch-list capability.

---

## See also

- **22-token-architecture-extensions** — the DTCG mechanics, computed-token discipline, and density encoding that this file's operations layer assumes.
- **12-figma-practice** — the Figma-side mechanics (Variables, modes, scoping, library architecture). The multi-collection-for-brand pattern in this file extends 12's one-dimension-per-collection treatment.
- **07-governance-and-adoption** — the contribution-flow patterns this file's blast-radius-weighted RACI specialises into the token layer.
- **14-accessibility** — pair tokens for contrast; this file's matrix contrast validation is the CI enforcement that makes pair tokens executable.
- **04-documentation** — the broader documentation strategy this file's living-token-documentation pattern fits into.
- **15-ai-in-ds** — components-as-data and the AI-agent-readable description discipline; this file applies the same argument to tokens.
- **09-gaps-and-open-questions** — where the Generative Token pattern is opened as a known-pattern-we-don't-yet-ship gap.

---

*Provenance: Multi-collection-over-multi-mode for brand axis, managed inheritance as the middle, the Theme Schema contract for white-label, the Generative Token pattern with OKLCH-derived brand expansion, blast-radius-weighted RACI, the Cascade Report as a CI artefact, brand version pinning as federated computational governance, the validation errors-vs-warnings discipline, the WCAG-blocks-APCA-warns contrast pattern, the contrast-pair-breakage as a major-bump semver rule, the deprecation window pattern, the build-vs-buy engagement-shape decision rule, and the token-operations-platform vs. Style Dictionary asymmetry are synthesised from the dual-agent research outputs in `_research/_inbound/2026-05-15-tokens-at-scale/` (May 2026). The "12-practice model" naming for the multi-brand library architecture is from one of those outputs. Style Dictionary v4 (late 2024), Supernova, Specify, Knapsack, Penpot, and Terrazzo positioning are from each tool's published documentation as of May 2026. The federated-computational-governance framing borrows from data mesh architecture writing (Zhamak Dehghani, 2019–2024). The blast-radius governance principle is internal POV. Tokens-as-API and semver-for-tokens are aligned with practitioner writing from Nathan Curtis (EightShapes, *Design Tokens* Nov 2024) and Robin Rendle. The AI-agent-readable description discipline is aligned with 15-ai-in-ds.*
