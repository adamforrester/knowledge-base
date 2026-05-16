You are researching tokens-at-scale concerns for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our practice ships W3C DTCG-compliant token sets, runs the Figma → DTCG → Style Dictionary → platforms pipeline, and has well-established positions on token taxonomy, theming dimensions (Curtis's seven), surface-as-inheritance, naming, and the three-tier architecture. What our existing materials are thin on is the *operational* layer that becomes load-bearing once token systems pass a certain scale: multi-brand portfolios (the agency norm — clients with 5–20+ brands rolled into one system), token validation and CI gates (preventing bad tokens from shipping), and token versioning / migration (the change-management problem). These are concerns that small systems can hand-wave and large systems cannot. Our agency clients are increasingly the latter.

Specifically not in scope: re-deriving the three-tier taxonomy, the DTCG procurement-grade argument, the theming-from-day-one position, or basic Style Dictionary usage. Those are settled.

This is not an introductory tokens guide — assume the reader has shipped tokens to production, has used Tokens Studio and Style Dictionary, knows what DTCG is, knows what Figma Variables modes do, and has run into the limits of small-system token approaches. Explain tokens at scale at the level a senior DS lead needs to architect a multi-brand portfolio engagement and to operate it for years afterward.

Research scope — cover all of the following. Use these as the section spine of the output.

1. Multi-brand portfolio token architecture

   - The collection-and-mode architecture for 5+ brands sharing a core system. What lives in the shared collection, what lives in brand-specific collections, where modes are the right tool and where they aren't.
   - Brand inheritance vs. brand isolation — the two extreme positions and the convergent middle. When a brand should fork the core and when it should override it.
   - Naming conventions at brand scale — `color-bg-primary-brand-x` vs. mode-driven resolution. The trade-off and the field-converged answer.
   - The cost asymmetry — adding a new brand to a well-architected system vs. a poorly-architected one. Specific examples of cost drivers.
   - White-label and reseller scenarios — when the brand list is unknown at architecture time and the system has to accept arbitrary brand inputs.
   - The Figma library structure that supports this at scale — multiple foundation libraries vs. one foundation library with brand-overlay collections. Cross-reference our 12-figma-practice file's library architecture treatment.

2. Token governance at scale

   - Who can change which tokens — RACI at the token layer (primitives are central-team-owned, semantics are negotiable, component tokens are often delegated).
   - The change-review process for token edits — what gates exist between a designer changing a Figma variable and that change reaching production.
   - The deprecation cycle for tokens — how a renamed semantic token is communicated, how a deleted primitive is removed safely, the migration window.
   - Cross-brand token changes — when a primitive change cascades to 12 brands and the governance pattern that prevents breakage.
   - The relationship to our 07-governance-and-adoption file's contribution-flow patterns at the token-specific layer.

3. Token validation and linting

   - DTCG schema validation — the JSON-schema-style validation pass that catches structurally invalid tokens before they ship. What tools do this today (Token Forge, Tokens Studio's validation, custom validators).
   - Contrast validation in CI — calculating WCAG contrast ratios between pair tokens at build time and failing the build on contrast violations. Cross-reference 14-accessibility's pair-tokens treatment.
   - Dead-token detection — finding tokens that no component references, finding components that hardcode values instead of using tokens, finding tokens that reference deleted primitives.
   - Naming-convention linting — `color-bg-primary` matches the convention, `colorBgPrimary` doesn't. Where the system enforces vs. recommends.
   - Token-relationship validation — primitive tokens should not be consumed directly by components, semantic tokens should not have hardcoded values, composite tokens should reference primitives or semantics only.
   - The CI pipeline integration story — pre-commit hooks, GitHub Actions, the failure mode when validation gates block legitimate work.

4. Versioning and migration

   - Semver applied to design tokens — what's a major / minor / patch change. The breaking-change rules.
   - Renaming a semantic token — the deprecation-window pattern. How both old and new names ship simultaneously through one or more releases.
   - Codemods for token migrations — automated find-and-replace across consumer codebases. What's mature, what's not.
   - The changelog story — how token changes appear in a release note that consumers can act on.
   - Token-version-pinning vs. token-following-latest at the consumer level — when a product should pin a token version and when it should track.
   - The migration of a token-system upgrade — moving from a one-tier to three-tier architecture mid-engagement, moving from custom JSON to DTCG, moving from Figma Variables to Tokens Studio (or vice versa).

5. The tools landscape at scale

   - Tokens Studio — its enterprise position in 2026, the value relative to native Figma Variables now that Figma has shipped composite types and modes.
   - Style Dictionary — the current 4.x state, transform/format extension patterns, multi-brand output strategies.
   - Specify — the platform's enterprise positioning, the gap it fills relative to Style Dictionary.
   - Supernova as a token platform (not just a documentation platform).
   - Token Forge, Knapsack, and other enterprise platforms — what they do, where they fit, when they're worth the cost.
   - The AI-native token tools emerging in 2025–2026 — what's real, what's vapour.
   - The Figma Variables roadmap — what's coming that materially changes the tool landscape.
   - The "build vs. buy" decision at the token-pipeline layer — when a custom Style-Dictionary-based pipeline is the right answer and when a managed platform is.

6. Documentation as a deliverable at scale

   - Token documentation beyond DTCG `$description` — usage examples, do/don't pairs, contrast-pair validation displayed inline, deprecation history, the rendered-token visual reference.
   - Generated documentation vs. authored documentation for tokens — what's automatable.
   - The relationship to our 04-documentation file's broader documentation strategy.
   - Living token documentation that updates from the DTCG source vs. static documentation that drifts.
   - Token documentation for AI agents — the descriptions that make tokens correctly selected by AI-generated code.

7. Failure modes specific to scale

   - The mode-multiplication explosion — when 4 themes × 3 brands × 2 densities = 24 modes per collection.
   - The token-as-bottleneck pattern — where every change to a primitive requires central-team review and the queue grows past usefulness.
   - Cross-brand drift — brands forking their semantic tokens for valid reasons, then the brands appearing inconsistent across the portfolio.
   - The deprecated-token long tail — tokens that should have been removed years ago but are kept because one product still references them.
   - The validation-fatigue pattern — too many lint rules, every PR fails CI, engineers learn to ignore the warnings.
   - The "we don't know which tokens are used" problem at the portfolio level.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where the field has clear consensus (semver for tokens, validation in CI, multi-collection over multi-mode for brand axes), state it; where decisions are context-dependent (Tokens Studio vs. native Variables, build vs. buy, brand inheritance vs. isolation), give a decision framework. Flag tooling state — versions, vendor pricing, enterprise positioning — and date claims with the verification path. Include a references section linking to primary sources (Style Dictionary docs, Tokens Studio docs, Specify docs, Supernova docs, primary practitioner writing on token systems at scale — Nathan Curtis, Brad Frost, Jeremy Lawson, others at this depth).

Depth: Expert audience. Do not explain what a token is, what modes are, or what semantic naming means. Explain the architecture, governance, validation, versioning, and tooling decisions a senior DS architect needs at the enterprise multi-brand scale where small-system approaches stop working.
