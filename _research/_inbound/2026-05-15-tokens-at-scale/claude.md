# Tokens at Scale — Multi-brand Portfolios, Governance, Validation, Versioning, Tooling

> Synthesis run, 2026-05-15. WebSearch was unavailable for this run; tool-state claims below are flagged with verification paths and dated. The reader should re-verify Style Dictionary, Tokens Studio, Specify, Supernova, Knapsack, and Figma Variables positioning before quoting any of this externally.

This document picks up where the practice's settled positions end: three-tier taxonomy, DTCG procurement, Curtis's seven theming dimensions, surface-as-inheritance, and the Figma → DTCG → Style Dictionary pipeline are assumed. The concerns here are the ones that small systems hand-wave and large ones cannot — the operational layer that determines whether a multi-brand token system survives its second year.

---

## 1. Multi-brand portfolio token architecture

### The collection-and-mode architecture

Once a portfolio crosses three or four brands, the question stops being "how do we structure tokens" and becomes "what is the unit of substitution." The field-converged answer in 2026 is that **modes are the wrong axis for brand**. Modes are a switch on a single collection — one set of names, multiple resolutions of those names. That works beautifully for theme (light/dark/high-contrast) and density (compact/comfortable) where the *shape* of the system is identical across the axis. It does not work for brand, because brand variation is not just resolution — brands add tokens, retire tokens, change semantic structure, change typography stacks, change spacing rhythms. Trying to encode that as modes produces a collection where half the variables are `undefined` in half the modes, and where adding a new brand means editing every variable in the collection.

The architecture that holds up is **multiple collections, each with their own mode axis**:

- A **core primitives** collection — palette ramps, type ramps, spacing scale, radius scale, motion curves. Mode-less (or single-moded). Shared by every brand, owned by the central team, frozen except by RFC.
- A **theme** collection — modes are `light` / `dark` / optionally `hc-light` / `hc-dark`. Semantic tokens (`color.bg.surface`, `color.fg.default`, `color.border.subtle`) resolved against primitives. Shared across brands in the simple case, brand-overridden in the complex case.
- A **brand** collection per brand (or a single brand collection with brand-as-mode where brand variation is genuinely shape-identical — rare). Brand-specific semantic overrides, brand-specific component tokens, brand-specific font references.
- A **density** or **platform** collection where those axes are real and orthogonal to brand. Most portfolios should resist adding these until they are clearly needed; they are mode-multiplication accelerants (see §7).

The reason this layering matters more than the names is that **collections are the boundary of substitution**. A consumer can swap one collection without touching another. A brand collection can be replaced wholesale for a white-label deployment. A theme collection can be evolved (light-dark-only → adding high-contrast) without disturbing brand work. Modes inside a collection cannot be added or removed without touching every variable in that collection. Treating collections as the substitution unit and modes as the within-collection variation is the architectural primitive.

### Brand inheritance vs. brand isolation

The two extreme positions:

- **Inheritance**: every brand inherits semantic tokens from a shared theme collection. Brand collections contain only the deltas — typically brand color anchors, brand fonts, and a handful of component overrides. Pro: minimum maintenance cost per brand, portfolio-wide consistency cheap. Con: any cross-brand semantic change cascades to all brands; brand teams cannot move at their own velocity; some brands genuinely need shape differences the shared semantics cannot model.
- **Isolation**: every brand owns its full semantic layer, with only primitives shared. Pro: brand teams ship independently, brand divergence is expressible. Con: maintenance cost is `O(brands × semantics)`; portfolio consistency becomes social rather than structural; the "agency look" leaks back in as each brand drifts toward its own conventions.

The **convergent middle** is a tiered inheritance: primitives are isolated from brand (one shared source), theme is shared by default with brand-overrideable points (a brand can replace `color.bg.surface` for its own surface, but inherits if it does not), component tokens are brand-owned by default but reference the shared semantic layer. The right question to ask of each token is "if Brand A changes this, should Brand B see the change?" If yes, it lives shared; if no, it lives in the brand collection; if "sometimes," it lives shared with brand override allowed and a governance rule (§2) about when overrides are appropriate.

A useful test for whether a brand should fork the core or override it: count the number of points of divergence. Under ~15% divergence, override. Above ~40%, fork. In between, the architecture is fighting the brand — usually because the shared semantic layer was designed for one brand and other brands were grafted on later. The fix is to widen the shared semantic vocabulary so the "weird" brand becomes expressible without forking, not to keep stacking overrides.

### Naming at brand scale

The naive approach — `color-bg-primary-acme`, `color-bg-primary-globex` — is wrong, and it is wrong in a way that compounds. It pushes brand into the name, which means every consumer of the token knows about brand, which means every change to the brand list ripples through every consumer. The token name is part of the API; brand is not.

The field-converged answer is **mode-driven resolution**: one name (`color-bg-primary`), resolved differently per brand at build time (when generating brand-specific outputs) or per mode (when brand is a runtime axis, which it rarely should be for portfolios — one app, one brand). Consumers reference `color.bg.primary` and never know which brand is active. The build pipeline produces `tokens.acme.css`, `tokens.globex.css`, etc., each with the same names and different values.

The exception is **brand-specific tokens that have no semantic analogue** — a brand-mark color used only on the brand wordmark, a brand-specific accent that exists in only one brand. These can carry brand in the name (`color-brand-acme-mark`) because they are not portable by design. Mixing the two — name-encoded brand for portable tokens — is the problem.

### The cost asymmetry of adding a new brand

In a well-architected portfolio, adding a 13th brand is roughly:

1. Create a new brand collection with the brand's primitive anchors (color, type).
2. Override the semantic tokens that genuinely differ.
3. Add brand-specific tokens for brand-only artifacts.
4. Re-run the build matrix; verify contrast and validation gates pass for the new brand.
5. Ship.

This is days of work, not weeks. The portfolio-wide tests catch issues before they reach product teams.

In a poorly-architected portfolio — brand encoded in names, shared semantics with hardcoded values, no validation gates — adding a 13th brand is:

1. Find every reference to existing brand names across all consumers (`color-bg-primary-acme` is in hundreds of components).
2. Decide which references are brand-portable and which are not, by reading code.
3. Patch the consumer codebases to make them brand-aware (or worse, add `if (brand === 'acme')` branches).
4. Re-test every component on the new brand because no validation pipeline exists.

This is weeks per brand, scales linearly with portfolio size, and produces compounding tech debt. The cost asymmetry is the single best argument for investing in architecture at brand 3 or 4, before the cost curve catches up.

### White-label and reseller scenarios

The hardest portfolio shape is the **unknown brand list** — a SaaS product white-labeled for an indeterminate number of resellers, each with their own brand inputs. The architecture has to accept arbitrary brand inputs at deploy time and produce a working build without manual intervention.

The pattern that works is **brand-as-input**, not brand-as-collection. The shared system defines a contract: "to add a brand, supply these N primitive values (color anchors, font family, logo asset) and optionally these M semantic overrides." A code path or build script consumes the brand input file and produces a brand-specific output. Modes are not used for brand; collections are produced dynamically. The contract is the API.

The implication is that **the semantic layer must be expressible entirely as functions of the brand input**. Hardcoded semantic values, brand-encoded names, or any architecture that requires hand-edits per brand collapses immediately at white-label scale. This is the strongest forcing function the practice has for getting the architecture right — the work done to support white-label cleans up the rest of the portfolio.

### Figma library structure

See `12-figma-practice.md` for the broader treatment; the portfolio-scale specifics:

- **One foundation library per portfolio** holding primitive variables and (usually) shared semantic variables. All brand libraries depend on this one. Updating the foundation cascades to all brand libraries via library subscription, which is both the strength and the risk (see §2 governance).
- **One brand library per brand**, each subscribing to the foundation. Brand libraries contain brand-specific variables and brand-specific component instances. Designers working on Brand A enable Foundation + Brand A libraries in their files; the brand-specific variables shadow or extend the shared ones.
- **Resist multiple foundation libraries**. The temptation when the portfolio gets large is to split the foundation by domain (color foundation, typography foundation, motion foundation). This produces a brittle dependency graph in Figma — when a designer wants to change one variable they have to know which foundation owns it. One foundation, organized internally by collection, is the practical answer until the foundation is genuinely too large to load (Figma's variable performance has been the limiting factor in some accounts; verify current state via Figma's release notes and your own performance testing — Figma Variables performance characteristics have been changing release-by-release through 2025–26).

The library architecture in Figma should mirror the build-pipeline architecture. If the build emits per-brand outputs from a shared primitive set + per-brand overrides, the Figma libraries should do the same. Misalignment between Figma library structure and pipeline structure is the most common source of "the designs don't match the build" complaints at portfolio scale.

---

## 2. Token governance at scale

Token governance is a special case of contribution governance (`07-governance-and-adoption.md`) but with two properties that make it more constrained: tokens are atoms, and atoms have transitive dependencies. A primitive change touches every semantic that references it, every component token that references those semantics, every component that consumes those component tokens, and every consumer of every component. The blast radius of a token edit is larger than the blast radius of a component edit, and that is what governance has to manage.

### RACI at the token layer

A workable allocation for a portfolio of 5–20 brands:

- **Primitives** — central team owned (R/A). Changes require an RFC, semver-major bump, and a migration window. Brand teams are consulted (C) but cannot change primitives unilaterally. Adding a new primitive (extending a ramp, adding a curve) is lower-stakes than editing one; treat as minor unless it replaces an existing primitive.
- **Shared semantics** — central team owned, brand teams contribute via PR. Brand teams can propose new semantics ("we need `color.bg.surface.inverse`"); central team approves and adds. Editing the resolution of an existing semantic is breaking (see §4).
- **Brand semantics (overrides)** — brand team owned. Brand teams change their own overrides without central approval. Central team retains the right to flag overrides that drift the brand from the portfolio (a brand consistently overriding `color.fg.default` to something off-system is a signal, not a violation).
- **Component tokens** — owned by the component owner (often central, sometimes federated). At scale, federated component ownership is common; component tokens follow the component.

The principle is that **the further from the leaves, the more centralized the ownership**. Primitives are leaves; consumers are roots. Edits at the leaves affect roots; edits at roots affect only themselves. Governance weight should track blast radius.

### Change-review process for token edits

The end-to-end path from a designer editing a Figma variable to that change reaching production:

1. **Designer edits in a Figma branch** (or in a Tokens Studio working set). Not in main.
2. **Export to DTCG JSON**, either via Tokens Studio's export, Figma Variables REST API + adapter, or a managed platform's sync. The JSON lands in a pull request against the token repo.
3. **CI validates the PR**: DTCG schema validation, naming-convention lint, contrast pair check, dead-token check, relationship validation (see §3). Validation failures block the PR.
4. **Human review** by a token reviewer (central team for primitives/shared semantics; brand team lead for brand collections; component owner for component tokens). The reviewer reads the diff against the existing token set, not just the JSON.
5. **Semver bump** is assigned (major/minor/patch — see §4) and recorded in the PR.
6. **Merge** triggers a build. Style Dictionary (or equivalent) produces platform outputs and a release artifact. The release notes include the token diff with semver bump and any required migrations.
7. **Consumers** pick up the release on their own cadence (pinning vs. following — see §4).

The Figma → JSON sync step is the most failure-prone in 2026. Designers expect Figma changes to "just appear" in the system; the governance gate intentionally interposes a PR. Practices that try to make Figma the source of truth without the PR step end up with no governance at all — every variable edit is a production change. The PR is the gate, even if the *origin* of the edit is Figma.

### Deprecation cycle for tokens

Tokens cannot be deleted as if they were lines of code. Their consumers are not in one repository.

The pattern that works is **rename, don't delete**:

1. **Announce** the deprecation in the release notes and (where the system supports it) emit a build-time warning when the deprecated token is consumed.
2. **Ship both names simultaneously** through one to three minor releases. Both `color.fg.default` (old) and `color.text.primary` (new) resolve to the same value. The DTCG `$deprecated` field (where supported) and a `$description` note flag the old one.
3. **Provide a codemod** that rewrites consumer references from old to new (§4).
4. **Remove the old name** in the next major release, after a public migration window of ~3 months for active portfolios, longer for slow-moving ones.

For deleting a primitive (not renaming — actually removing): the primitive must first have no semantic referencing it. Audit, point semantics at a replacement primitive, ship a release, then remove the primitive in the next major. The two-step is necessary because primitive references in consumers are rare but possible (especially in older codebases), and the audit cannot guarantee the leaves are clean unless the references are removed first.

### Cross-brand token changes

A primitive change that cascades to 12 brands is the highest-risk operation in a portfolio token system. Two patterns mitigate:

- **Brand-by-brand rollout**: the primitive change ships in a release, but brand collections pin to the previous primitive version until validated. Brand teams update on their own schedule. This requires the build pipeline to support per-brand primitive pinning — most portfolio systems don't support this until they hit the first painful cross-brand change and add it.
- **Portfolio-wide test gate**: the primitive change must pass contrast, validation, and (ideally) visual-regression tests for every brand before merge. The CI matrix runs `brands × themes × densities`, and a failure on any cell blocks the merge. This is the right answer for systems that ship primitives infrequently; it is too slow for systems where primitive churn is constant (which is itself a smell — primitives shouldn't churn).

The governance pattern that connects them: **primitives change rarely, on a predictable cadence, with portfolio-wide testing**. Brand semantics change frequently, with brand-scope testing. Component tokens change continuously, with component-scope testing. The cadence-by-tier model maps neatly onto the architecture-by-tier model and lets the slow gates apply to the slow-changing layers.

### Connection to the contribution flow

The `07-governance-and-adoption.md` patterns — federated contribution, central review for shared assets, contribution levels (consume / contribute / co-own) — apply at the token layer with a single adjustment: **token contributions are reviewed against the portfolio, not just the system**. A brand team proposing a new semantic must be reviewed against the question "does this make sense for the other 11 brands, or is it brand-specific?" because the answer determines which collection it lands in. Token review is a cross-portfolio function in a way component review usually is not.

---

## 3. Token validation and linting

The contract is: no token reaches a consumer build without having passed every validation gate the system defines. Validation is the place where governance becomes mechanical — if it isn't automated, it isn't enforced.

### DTCG schema validation

A structurally invalid token (missing `$type`, malformed `$value`, illegal reference) should fail the build at the earliest point — ideally in pre-commit, certainly in PR CI. JSON Schema validation against the DTCG draft schema is the baseline. Several tools do this in 2026, with varying coverage:

- **Style Dictionary 4.x** (verify current minor at `https://styledictionary.com/` and `https://github.com/amzn/style-dictionary` — Style Dictionary 4 shipped in 2024 with first-class DTCG support; later 4.x minors have tightened DTCG conformance and validation hooks. Verify state at run time.) validates token shape on parse, but its validation is more lenient than a strict DTCG schema pass — it accepts non-DTCG shapes for legacy reasons. For strict DTCG, layer a JSON Schema validator (Ajv) on top before handing to Style Dictionary.
- **Tokens Studio** (verify at `https://tokens.studio/` and the Figma plugin release notes; as of late 2025 Tokens Studio's standalone DTCG export was maturing alongside their hosted platform). Tokens Studio's own validation catches malformed exports but does not enforce the full DTCG draft surface.
- **Token Forge** and similar smaller validators (verify positioning; this segment has been churning) — these provide stricter DTCG schema validation and are typically run in CI alongside Style Dictionary, not instead of it.
- **Custom validators** built on Ajv + the DTCG draft schema are the answer when no off-the-shelf tool tracks the draft closely enough. The DTCG draft is still moving in 2026; a custom validator pinned to a specific draft version is the most defensible position for procurement-grade systems.

The validation should run at three points: pre-commit (fast, schema-only), PR CI (full suite), and release-tag (final gate). Pre-commit catches typos; PR CI catches everything else; release-tag is the belt-and-braces for security.

### Contrast validation in CI

Pair tokens (foreground/background pairs declared as related in the token set — see `14-accessibility.md`) make automated contrast validation possible. The validator iterates declared pairs, computes WCAG 2 contrast ratios (and optionally APCA), checks against thresholds (AA / AAA / non-text), and fails the build on violations.

The non-trivial parts:

- **Threshold per pair, not per system**. Body text needs AA (4.5:1), large headings need 3:1, non-text UI elements need 3:1, AAA is opt-in. The pair declaration carries its threshold so the validator knows what to check.
- **Brand × theme × density matrix**. A pair that passes in light mode may fail in dark mode; a pair that passes in Brand A may fail in Brand B. The validator runs the matrix and reports per-cell failures, not just per-pair.
- **Override resolution**. When a brand overrides a semantic token, the contrast computation must use the brand's resolved value, not the shared default. This requires the validator to understand the collection-and-mode resolution model, not just the flat token list.
- **APCA experimentation, WCAG 2 enforcement**. APCA (the perceptual contrast algorithm proposed for WCAG 3) is more accurate but not yet a conformance basis. Most enterprise systems report both and enforce WCAG 2. Reassess when WCAG 3 stabilizes; verify state at `https://www.w3.org/TR/wcag-3.0/` and `https://git.apcacontrast.com/`.

When a contrast pair fails CI, the failure message must explain *which pair, which brand, which mode, what ratio, what threshold*. Generic "contrast failure" output is useless at portfolio scale. Good failure messages are the difference between contrast validation being enforced and being disabled the first time it blocks legitimate work.

### Dead-token detection

Three related problems live under this header:

- **Unreferenced tokens** — defined in the token set, not consumed anywhere. The detector needs the set of consumer references (CSS variables in product code, Figma variable usages in libraries, MDX references in docs) and the set of defined tokens. The diff is the dead set. The detector should distinguish "unreferenced anywhere" (delete) from "unreferenced by code but referenced in Figma" (likely live, used by designers) from "unreferenced in current brand build but defined in another brand's collection" (intentional).
- **Hardcoded values in consumers** — components that use `#fff` or `16px` instead of a token reference. Stylelint with a project-specific rule, or a custom AST visitor, catches these in code. The cross-portfolio version checks every consumer codebase against the token set and produces a hardcoded-value report. This is the strongest signal of token-system adoption health.
- **Dangling references** — tokens that reference primitives that have been deleted or renamed. Style Dictionary catches the build-time version; the static check catches it before build. Should fail CI hard — a dangling reference is a build break waiting to happen.

The dead-token report should be **a regular output, not a gate**. Gating on dead tokens means a token defined in advance of a feature can't ship until the feature ships — which inverts the desired sequence. Report dead tokens, review periodically, remove on schedule.

### Naming-convention linting

Once the convention is decided (kebab-case, namespaced, structured `category.subcategory.role.modifier` — the practice's existing position), enforcement is a regex pass on token names plus a structural check against the namespace tree. Tools:

- A custom lint script in Node with the convention encoded.
- Style Dictionary's `name` transformation includes validation hooks, but is more useful for output than input.
- Tokens Studio's plugin can warn on convention violations in the Figma UI, but cannot enforce — enforcement is a CI concern.

The lint should distinguish **enforce** (convention violations block PR) from **warn** (style suggestions). Casing, namespace shape, and reserved-word collisions are enforced. Subjective name choices (`color.fg.primary` vs. `color.text.primary`) are reviewed by humans, not linted — linters cannot encode taste.

### Token-relationship validation

The architectural constraints from §1 — primitives are not consumed directly, semantics don't have hardcoded values, composite tokens reference primitives or semantics only — are enforceable as static checks:

- **Primitives consumed by components**: walk consumer references; any reference to `color.palette.blue.500` from a component is a violation (should go through a semantic). The check has false positives in transitional periods (system mid-migration); allowlists per-token are pragmatic.
- **Semantics with hardcoded values**: walk the token tree; any semantic whose `$value` is a literal rather than a `{reference}` is a violation. Exceptions for tokens that genuinely have no primitive (a brand-specific one-off color) need explicit annotation.
- **Composite tokens**: typography, shadow, border composites should reference primitives or semantics in their parts, not literals. Same check as above, applied per-part.

These checks make the three-tier architecture executable. Without them, the architecture is aspirational — drift is invisible until it has happened.

### CI pipeline integration

The shape that works:

1. **Pre-commit hook** (Husky + lint-staged or equivalent): schema validation, naming lint. Fast, ~seconds. Optional bypass with `--no-verify` for emergencies.
2. **PR CI** (GitHub Actions, GitLab CI, etc.): full validation suite — schema, contrast matrix, relationship validation, dead-token report (informational), build dry-run. Required for merge.
3. **Release CI**: full validation + visual regression on the consumer reference app + changelog generation + semver bump verification. Cuts the release tag.
4. **Consumer CI**: when a consumer pulls a new token version, their CI should run their visual regression suite against the new tokens before the dependency update lands. This is the consumer's responsibility, not the token system's, but the token system should make it easy (publish a `tokens-only` build, document the test pattern).

**The failure mode** to plan for: validation gates that block legitimate work. The mitigation is layered — pre-commit for fast feedback, PR CI with clear failure messages, an explicit override path (label-based or approver-based) for the small number of cases where a validation rule is wrong rather than the change being wrong. Without the override path, validation fatigue (§7) is guaranteed.

---

## 4. Versioning and migration

Tokens are an API. APIs have versions. Token versioning at scale is semver applied to a token set, with the breaking-change rules adapted to the token domain.

### Semver applied to tokens

The breaking-change rules that hold up in practice:

- **Major (1.0.0 → 2.0.0)**: any change that requires consumer code changes to remain working. Renaming a token. Removing a token. Changing the type of a token (`color` to `gradient`). Changing the resolution semantics (a semantic that previously meant "background of surface" now means "background of card"). Removing a mode or collection. Adding a required brand input (white-label scenarios).
- **Minor (1.0.0 → 1.1.0)**: any additive change that does not break existing consumers. Adding a new token. Adding a new mode. Adding a new brand collection. Tightening a contrast pair (the pair existed and met the previous threshold; the threshold change does not break the pair).
- **Patch (1.0.0 → 1.0.1)**: any change that is invisible to consumers in shape. Documentation updates. Internal refactors of token references that produce identical resolved values. Bug fixes where a token's resolved value was wrong (e.g., a typo in a hex code).

Three nuances:

- **Value changes are usually minor, sometimes major**. Changing `color.bg.surface` from `#fff` to `#fafafa` is technically a value change consumers will see. It is not a breaking API change (the name still works, the type is the same). Semver guidance treats this as minor with a callout in release notes. The exception: value changes that move a contrast pair out of conformance are breaking (the consumer's accessibility commitments now fail). Treat them as major even though the API shape is unchanged.
- **Tier transitions are major**. Moving a token from `primitive` to `semantic`, or vice versa, changes the contract for consumers who care about tier (which is most of them, for relationship validation).
- **Brand additions are minor, brand removals are major**. Adding a brand collection is additive. Removing a brand collection breaks any consumer that depended on that brand's outputs.

### Renaming a semantic token

The deprecation-window pattern in detail:

1. **Release N**: introduce the new name. The new name is the canonical reference; the old name is an alias resolving to the same value, marked `$deprecated: "Use color.text.primary"` in the DTCG metadata. Both ship.
2. **Release N+1** (next minor): the old name continues to ship; the build emits warnings when consumers reference it. Codemod is published.
3. **Release N+M** (next major, ≥3 months later): the old name is removed. The release notes call out the removal explicitly, with the codemod as the migration path.

The window length is portfolio-dependent. Fast-moving consumer products can handle a 6-week window. Heavy enterprise consumers may need 6 months. The system's policy should be explicit and uniform — "deprecations live for at least one major cycle, minimum 3 months" — so consumers can plan upgrades.

### Codemods for token migrations

A codemod for token renames is largely solved at the level of CSS variables and JS/TS token imports:

- For CSS variables: a regex replacement is usually safe (`--color-fg-default` → `--color-text-primary`), with caveats for names that are substrings of other names. Use word boundaries or a more structured replacement (PostCSS plugin with a token map) for safety.
- For JS/TS: jscodeshift or ts-morph with a transformer that targets import specifiers and member-expression chains. The token map is the input; the transformer applies it.
- For Tailwind / utility frameworks: the transformer must understand the framework's class-name shape (`bg-surface` → `bg-background`), which usually means a framework-specific codemod.
- For Figma: there is no codemod equivalent. Designers re-bind variables manually, or Tokens Studio's bulk operations re-bind. This is the weakest link in the migration story and the most frequent cause of "the design moved but the build didn't" or vice versa.

Maturity in 2026: token-rename codemods for CSS and JS are commodity (multiple npm packages exist; the practice should maintain its own or fork one to integrate with its naming conventions). Type-change and tier-change codemods are more bespoke — there is no general-purpose tool. AI-assisted codemod generation is appearing (frameworks that ingest a token diff and emit a transformer); verify current state of the AI codemod ecosystem at run time as it is moving quickly.

### The changelog story

A consumer reading a release note needs three things, in order:

1. **The breaking-change list** — what they must change to upgrade. With codemod commands where they exist.
2. **The deprecation list** — what they should change soon. With the deadline (next major release).
3. **The additive list** — new tokens, new brands, new modes — what they can now use.

Generated from the token diff. Style Dictionary 4.x and similar tooling can produce a structural diff; the human-readable changelog is layered on top with the semver bump assigned per change. Conventional Commits + a changelog generator is the field-standard approach; the token-specific addition is the codemod commands inline.

### Version pinning vs. tracking

For consumer products: **pin in production, track in development**. Pinning to an exact version means upgrades are explicit (the consumer chooses when to absorb the change); tracking means upgrades land on every build (risky if any release is breaking).

The practical pattern is to pin to a minor version range (`^1.4.0`) for production — minor and patch updates are absorbed, major updates require explicit consumer action. The token system's semver discipline must be tight enough that consumers can trust the range pin. The first time a "minor" release breaks a consumer, trust is gone and every consumer pins to exact versions, which kills the upgrade cadence and produces the deprecated-token long tail (§7).

Some consumers — regulated products, ones with their own release cycles — pin exact and upgrade quarterly. The token system should publish an "LTS-ish" track if a critical mass of consumers does this, where each major release is supported for ≥12 months with security/contrast fixes backported.

### Migrating the token system itself

Mid-engagement upgrades happen. The patterns:

- **One-tier → three-tier**: introduce semantics in parallel with primitives. Components migrate to semantics one at a time. The system runs three-tier-curious for a release or two, then primitives stop being consumed directly via lint enforcement.
- **Custom JSON → DTCG**: write a one-shot converter (most custom JSON shapes are mechanically translatable). Run both shapes in parallel for one release while consumers verify. Cut over.
- **Figma Variables ↔ Tokens Studio**: this is harder than either direction implies. Tokens Studio supports more token types and richer references than Figma Variables (composite typography, complex math) but is a plugin layer; Figma Variables is native but more constrained. Migration in either direction requires a mapping spec for the cases the two tools handle differently. As of mid-2026, the gap has narrowed but not closed (verify at Tokens Studio release notes and Figma's variables release notes); composite typography and certain math expressions still differ. Practical pattern: run both for a release, generate the same DTCG export from each, diff the output, resolve the diffs case-by-case.

The meta-rule: token system migrations are best done one axis at a time. Migrating taxonomy *and* tooling *and* naming convention in one release is the failure mode. Pick one, run it through deprecation windows, then the next.

---

## 5. The tools landscape at scale

> Tool positioning, versions, pricing, and roadmap items below are dated and require re-verification. The landscape moves quarterly. Verification paths are noted per tool.

### Tokens Studio

Verify at `https://tokens.studio/` and `https://github.com/tokens-studio` (May 2026).

Tokens Studio's enterprise position in 2026 is **the bridge layer between Figma and DTCG when Figma Variables doesn't carry enough information**. Figma Variables in 2026 supports modes, references, and a limited set of types (color, number, string, boolean) plus some composite types that have shipped iteratively (verify what's GA vs. beta at the Figma release notes). Tokens Studio supports:

- Composite typography (font family + weight + size + line height + tracking, as a single token, referencing primitives).
- Math expressions in references (`{spacing.base} * 2`).
- Token-level metadata richer than Figma's native variable description.
- DTCG export with broader type coverage than Figma's native export.
- Multi-set composition (themes as composable token sets, not just modes).

The trade-off: Tokens Studio is a plugin, not native. Designers must run it; it has its own UI; it can drift from Figma if the sync isn't disciplined. The hosted platform (Tokens Studio Pro / Sync, verify branding) addresses sync discipline but adds cost.

The decision rule: if the system needs composite typography, math, or multi-set composition, Tokens Studio is the answer through at least 2026. If the system can express its tokens entirely as native Figma Variables (the simple case — color, basic semantics, a small set of modes), native Variables + a custom DTCG export adapter is sometimes the cleaner answer, because fewer tools means fewer integration seams. The gap narrows annually; revisit per engagement.

### Style Dictionary

Verify at `https://styledictionary.com/` and `https://github.com/amzn/style-dictionary` (May 2026).

Style Dictionary 4 (shipped 2024) is the field-standard transform/format engine and has remained so through 4.x. The key 4.x additions for portfolio scale:

- First-class DTCG token support (4.0+).
- Async/ESM-native build pipeline.
- Custom parsers and pre-processors as proper extension points (not monkey-patches).
- Improved reference resolution and error reporting.

The transform/format extension pattern for multi-brand:

- **One pipeline, many outputs**. The build runs once over the unified token set; per-brand and per-platform outputs are produced by parameterized output configurations.
- **Pre-processors** for token-set composition (foundation + brand-A → brand-A-resolved tokens). Run before the transform stage.
- **Custom formats** for any platform-specific output the built-in formats don't cover (iOS asset catalogs, Android resource flavors, Tailwind config). Maintain these in a shared `@portfolio/style-dictionary-formats` package so brand pipelines don't fork format logic.
- **Filter functions** for slicing outputs (one platform's tokens only, one tier's tokens only).

Style Dictionary remains the right answer for the **build pipeline** in a custom-pipeline portfolio. Where managed platforms compete is on the *authoring* and *governance* layers, not the build itself; many platforms emit Style Dictionary configs as their hand-off to the consumer's build.

### Specify

Verify at `https://specifyapp.com/` (May 2026).

Specify's enterprise positioning is **the token platform that sits between design tools and code without requiring a custom Style Dictionary pipeline**. It ingests from Figma, manages the token set as a hosted source of truth, and emits to consumer platforms. The gap it fills relative to raw Style Dictionary is the *authoring and sync* layer — the parts that require glue code in a custom pipeline are productized.

Where it works: portfolios where the design team is the primary authoring surface, where the engineering team wants a managed sync, and where the price tag clears the budget. Where it doesn't: portfolios with heavy custom transforms, regulated environments that require self-hosted pipelines, or portfolios where Style Dictionary expertise is in-house and the custom pipeline is already mature.

Pricing and enterprise tiers shift; verify current state. As a heuristic, Specify (and Supernova at the token-platform tier) prices at roughly the cost of one mid-level FTE per year for an enterprise contract, which is the break-even budget vs. building the same with internal effort.

### Supernova as a token platform

Verify at `https://supernova.io/` (May 2026).

Supernova began as a documentation platform and has expanded into token management. Its enterprise pitch in 2026 is **end-to-end** — tokens, components, documentation, code generation — under one roof. The token-platform piece overlaps with Specify and Tokens Studio's hosted offering. Supernova's strength is the docs integration (token changes auto-update docs); its weakness is depth in any individual layer compared to specialists.

The decision against Style Dictionary + Specify + custom docs is the integration tax — Supernova in one workflow is one vendor, one contract, one model. Against the practice's preference for procurement-grade DTCG + best-of-breed tools, Supernova is a viable answer for clients who want one platform and are willing to trade depth for cohesion. Treat as a viable shortlist entry, not a default.

### Token Forge, Knapsack, and other enterprise platforms

Verify Knapsack at `https://knapsack.cloud/`; Token Forge positioning at its current repo/site (May 2026; this segment is volatile).

- **Knapsack** is more a design system platform than a token tool — components, docs, tokens, governance, all in one. The token features are integrated rather than best-in-class. Worth considering when the brief is "platform for the whole DS practice" rather than "token pipeline."
- **Token Forge** and similar smaller tools fill validation, schema enforcement, or specific gaps (CI integration, contrast validation) more deeply than the all-in-one platforms. Often used alongside Style Dictionary rather than instead of it.

The "worth the cost" calculus: a managed platform is worth it when it removes 6+ months of internal engineering work *and* the client doesn't have the in-house capability to maintain a custom pipeline. For agency-built systems that hand off to an in-house team, a custom pipeline is often the right answer because it leaves the client with code they own. For agency-built systems that the agency operates indefinitely, a managed platform is often the right answer because it reduces the maintenance load on the agency.

### AI-native token tools (2025–2026)

The segment is real but young. Genuine functionality landing in 2026:

- **AI-assisted token naming and generation** — propose a token taxonomy from a Figma file, propose names for tokens that don't yet have them, generate codemods from token diffs.
- **AI-assisted contrast remediation** — propose alternative values that meet contrast thresholds while staying close to the brand.
- **AI-assisted documentation** — generate `$description` text, usage examples, do/don't pairs from token metadata + component usage.

Vapour:

- "AI generates your whole design system" — at the token layer, not without significant supervision; the outputs need taxonomic review.
- "AI decides theming" — the choices that make a theme work are subjective; AI proposes, designers decide.

The practical position for 2026: integrate AI as an authoring assistant (in the docs layer, the naming layer, the codemod layer), not as a decision-maker. Tools that present AI as an autonomous token system architect are oversold; tools that present AI as a productivity accelerator on specific tasks are credible.

### Figma Variables roadmap

Verify at `https://help.figma.com/` release notes and the Figma roadmap (May 2026). Items that have been signaled or shipped in 2025–26 that materially change the tool landscape:

- **More composite types** (typography, shadow, border as first-class Variable types). Each addition narrows the gap with Tokens Studio.
- **Improved library performance** for portfolios with many variables and many subscribing files. Performance has been the limiting factor at large scales.
- **REST API maturation** for Variables. Read/write parity that makes Figma a programmable source of truth without plugin layers.
- **Better mode management** — copying modes across collections, mode templates, mode inheritance — addresses the mode-multiplication pain point (§7).

Roadmap items routinely slip; the gap with Tokens Studio narrows but doesn't close on any predictable schedule. The decision should be re-made per engagement on current state.

### Build vs. buy at the token-pipeline layer

A decision framework:

| Factor | Lean Build (Style Dictionary + custom) | Lean Buy (Specify / Supernova / Knapsack) |
|---|---|---|
| In-house DS engineering capacity | High | Low |
| Client retains pipeline ownership | Required | Acceptable to license |
| Custom transforms / unusual platforms | Many | Few |
| Procurement / regulatory constraints | Self-hosted preferred | SaaS acceptable |
| Engagement model | Agency builds, hands off | Agency builds and operates |
| Portfolio scale | 1–10 brands | 10+ brands, white-label scenarios |
| Authoring surface | Engineering-led | Design-led |
| Time-to-first-output | Months acceptable | Weeks required |

Most VML engagements weight toward build for handover-style deliveries (the client wants code they own) and toward buy for operate-style retainers (the agency wants to reduce its maintenance load). Hybrid is common — Style Dictionary as the build, a managed platform for authoring/governance UI, both feeding the same DTCG source.

---

## 6. Documentation as a deliverable at scale

Per `04-documentation.md`, the practice's position is that documentation is a build target, not a write-up. At the token layer, this becomes especially load-bearing because the volume of tokens, the variability across brands, and the rate of change all exceed what a hand-written docs site can sustain.

### Beyond DTCG `$description`

The `$description` field carries the canonical one-line meaning of a token. It is not enough. Token documentation at scale needs:

- **Usage examples** — components that legitimately use this token, rendered. The cardinality of (token × component × brand) is high; generated examples beat curated ones.
- **Do/don't pairs** — explicit anti-patterns, especially for tokens that are commonly misused (using a primitive directly, using a brand-specific token in a portable component).
- **Contrast pair validation displayed inline** — for foreground/background tokens, the docs render the actual contrast ratio against declared pairs and flag failures. This is the same data as the CI validator, surfaced visually.
- **Deprecation history** — what this token used to be called, when it was renamed, what it will be renamed to, when it will be removed. The deprecation timeline lives on the token's docs page.
- **Rendered visual reference** — a color swatch, a spacing block, a typography sample. Generated from the resolved value, per brand and per mode.
- **Reference graph** — what this token references (its dependencies) and what references it (its dependents). Critical for impact analysis when a token is being changed.

### Generated vs. authored

The split:

- **Generated**: rendered visual reference, contrast pair validation, deprecation history (from semver + `$deprecated`), reference graph, usage examples (from component-token static analysis), per-brand resolution table.
- **Authored**: the *meaning* of the token (what is `color.bg.surface` *for*), do/don't pairs (judgement, not extractable from data), the migration narrative when a token is replaced (why, not just when).

Authored documentation should be sparse and high-quality. Generated documentation carries the volume. The MDX (or equivalent) page for a token is mostly slots that pull from generated sources; the authored prose is two or three sentences and a do/don't.

### Living vs. static

Living documentation is the only viable shape at portfolio scale. Static documentation drifts within one release. The shape:

1. DTCG source is the truth.
2. A docs build runs alongside the token build. Same source.
3. Each token page is generated from the token's metadata + the build-time facts (resolved value per brand × mode, contrast pairs, references).
4. Authored content (description, do/don't, migration prose) lives in the token's MDX or in a sidecar file keyed to the token name.
5. The docs site is rebuilt on every token release, with the changelog as a first-class navigation surface.

When designers ask "why doesn't the docs site show the new token I added in Figma?" the answer is always "because it isn't in DTCG yet." That answer is acceptable; the answer "because nobody updated the docs site" is not.

### Token documentation for AI agents

AI-generated code that uses tokens correctly depends on the token's documentation being machine-legible. The fields that matter:

- **The `$description`** — the canonical meaning, written for an LLM as much as a designer. "Background color for the primary surface — cards, panels, the body of dialogs" beats "primary background."
- **Usage tags** — structured metadata (`usage: ["surface", "card", "panel"]`) that an LLM can match against intent.
- **Anti-patterns** — explicit "do not use for text foregrounds" markers that prevent the LLM from selecting the token for incompatible contexts.
- **Tier** — primitive / semantic / component, so the LLM (or a tool the LLM calls) can enforce the relationship rules.
- **Brand portability** — whether the token is portable across brands or brand-specific, so brand-agnostic code generation knows what to avoid.

The practice's existing `.ai.json`-style metadata pattern (per `15-ai-in-ds.md`, GLOSSARY entries) applies at the token layer with the same shape — machine-readable sidecars next to DTCG, generated where possible, hand-authored where judgement is needed.

---

## 7. Failure modes specific to scale

### Mode-multiplication explosion

`4 themes × 3 brands × 2 densities = 24 modes per collection`, multiplied across collections, multiplied across editing surfaces. Every variable in the collection must define a value in every mode. The collection becomes unmaintainable; designers refuse to edit it; the mode axis quietly becomes "we only really update light/dark and the others drift."

The fix is architectural, not procedural: **move brand and density out of modes and into separate collections** (§1). Modes should be reserved for axes that are genuinely orthogonal and shape-identical (light/dark, optionally density when density is a true within-brand axis). Brand is not orthogonal to anything; it gets its own collection. This is the single highest-leverage architectural decision at portfolio scale.

The secondary fix is **mode templates** (a feature on Figma's roadmap, verify state) — being able to declare "all modes in this collection must include these N variables with these defaults" so adding a mode doesn't require touching every variable. Until that ships, mode hygiene is a manual chore that compounds.

### Token-as-bottleneck

When every primitive change requires central-team review and the central team is two people, the queue grows past usefulness. Brand teams start working around the system — local overrides in product code, parallel "shadow" token sets — and within a year the central tokens are nominal.

The mitigation is the RACI from §2: primitives are slow on purpose, but semantics are negotiable, and brand-collection edits are brand-team-owned. If brand teams are blocked on primitives more than monthly, the primitive set is wrong — either too small (it should be extended), or too leaky (semantics that should encapsulate the primitive aren't doing their job). Treat bottleneck symptoms as architectural signals, not staffing problems.

### Cross-brand drift

Brand A overrides `color.bg.surface` to be slightly warmer for valid reasons. Brand B overrides it to be slightly cooler. Brand C inherits the shared default. Six months later, the three brands look meaningfully different at the surface level, and product owners notice.

The drift is often legitimate (the brands *are* different). The system's job is not to prevent it but to **make it visible**. A portfolio-wide token-override report — "Brand A overrides 23 semantic tokens, Brand B overrides 47, Brand C overrides 4" — is a governance signal. Brands with high override counts are either (a) under-served by the shared semantic vocabulary (the system should grow more semantics) or (b) genuinely divergent (the system should accept the override but examine whether it should remain in the portfolio under the same shared foundation).

The fix to the *consistency* problem is not removing overrides; it is choosing which overrides are sanctioned and which are drift. The portfolio governance review (quarterly) is where this happens.

### Deprecated-token long tail

A token deprecated in 2023 is still referenced by one product team in 2026 because they never upgraded. The token can't be removed. The token set carries forward indefinitely. Multiplied across decades of deprecations, the system bloats.

Two mitigations:

- **Hard removal deadline** in the deprecation policy. Tokens are not removed when they are deprecated, but they *are* removed N major releases later, regardless of remaining consumers. Consumers who haven't migrated get a build break, which is the forcing function that the soft deprecation didn't provide. The policy must be explicit and the calendar predictable.
- **Per-consumer adoption tracking** — the token system knows which consumers consume which tokens (via registries, import tracking, or self-report). When a consumer is the last holdout on a deprecated token, the governance conversation is pointed: "you have until release X to migrate or you lose tokens you depend on." This shifts the deprecated-token cost from the system to the laggard, which is the correct allocation.

The deprecated-token long tail is also where AI codemods earn their value — if migration cost is near-zero, consumers have no excuse for not upgrading.

### Validation fatigue

Twenty lint rules, every PR fails CI, engineers learn to override with `--no-verify` or to copy-paste failing tokens past the gate. The system is enforced on paper; in practice it isn't.

The mitigation is rule curation, not rule maximization:

- **Tier rules into error and warning**. Errors block. Warnings inform. Most rules should be warnings; the ones that block are the ones that produce actual breakage (dangling references, schema violations, contrast failures with no override).
- **Make failure messages excellent**. "Token contrast failed" is useless. "Token pair `color.fg.default` over `color.bg.surface` in Brand B / dark mode resolves to ratio 3.8:1, fails AA threshold 4.5:1 (declared for body text). Fix in `tokens/brand-b/colors.json` line 47, or downgrade the pair to large-text-only" is actionable.
- **Allow declared overrides**, scoped per-token, with an expiry date. A token with `$override: "intentional, expires 2026-09-01"` opts out of a specific lint for a specific reason. Reviewed in PR; visible in reports; auto-expires.
- **Measure the fatigue**. If the same override appears on most PRs, the rule is wrong. Remove or relax it. Validation is a tool; if it isn't fit, sharpen it or set it aside.

### "We don't know which tokens are used"

At portfolio scale, the question "is this token still used?" has no easy answer. Consumers are many, in different repos, on different versions, sometimes in compiled bundles where the references aren't traceable.

The infrastructure that makes the question answerable:

- **A token registry** the consumers publish to — at build time, each consumer publishes the list of tokens it references. The registry aggregates per token, per consumer, per version.
- **Static analysis** against consumer codebases the system can reach. The reference report is the input; the gap (consumers that haven't published) is itself a signal.
- **Telemetry** in the rendered application — at runtime, what tokens are actually resolved on real users' pages. This is the strongest signal but the hardest to get; most portfolios stop at static analysis.

The registry is the highest-leverage piece. Without it, deprecation decisions are guesses; with it, deprecation has the data backing it needs and the deprecated-token long tail shrinks because tokens with zero consumers in the registry can be removed safely.

---

## References

Primary sources to verify against current state. URLs current as of May 2026; verify availability before quoting.

- **DTCG (Design Tokens Community Group)** — `https://www.designtokens.org/` and the draft spec at `https://tr.designtokens.org/format/`. Schema authority.
- **Style Dictionary** — `https://styledictionary.com/`, GitHub `https://github.com/amzn/style-dictionary`. Build engine.
- **Tokens Studio** — `https://tokens.studio/`, Figma plugin and hosted platform.
- **Specify** — `https://specifyapp.com/`. Token platform.
- **Supernova** — `https://supernova.io/`. Design system platform with token features.
- **Knapsack** — `https://knapsack.cloud/`. Design system platform.
- **Figma Variables** — `https://help.figma.com/hc/en-us/sections/14397166203671-Variables`. Native Figma token primitives, modes, roadmap.
- **WCAG 2.2** — `https://www.w3.org/TR/WCAG22/`. Contrast thresholds for CI validation.
- **WCAG 3 / APCA** — `https://www.w3.org/TR/wcag-3.0/`, `https://git.apcacontrast.com/`. Future contrast model.

Practitioner writing — verify these author pages or canonical posts before citing:

- **Nathan Curtis (EightShapes)** — `https://medium.com/eightshapes-llc`. Token taxonomy, naming, theming dimensions; the practice's canonical references.
- **Brad Frost** — `https://bradfrost.com/blog/`. Design system shape, governance, scale.
- **Jeremy Lawson** — practitioner writing on Figma Variables and token migration; verify current canonical posts.
- **Robin Cannon, Lukas Oppermann, Louis Chenais, others in the DTCG orbit** — schema-level writing on DTCG and token tooling.

Internal cross-references:

- `02-design-foundations.md` — taxonomy, theming, pipeline base.
- `04-documentation.md` — documentation strategy (this document extends to tokens).
- `07-governance-and-adoption.md` — contribution flow (this document extends to the token layer).
- `12-figma-practice.md` — Figma library architecture at the foundation layer.
- `14-accessibility.md` — pair tokens for contrast validation in CI.
- `15-ai-in-ds.md` — AI-readable token metadata; AI codemods.

All tool-state claims in this document are dated May 2026 and should be re-verified before being used in client materials. The token tooling landscape moves quarterly; positions stated as current may be six months stale by the time this document is read.
