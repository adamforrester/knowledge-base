---
type: practice-area
title: Documentation
description: Docs strategy for two audiences (humans and machines). Storybook/MDX plus machine-readable metadata and registries from one source. Plus content as a system layer — voice-and-tone matrix, content tokens, i18n content depth, AI-surface content — and the UX Copywriter role at engagement scale.
tags: [phase, documentation, storybook, mcp, content, voice-and-tone]
timestamp: 2026-06-18
---

# 04 — Documentation

> The system's user manual for two distinct audiences: humans, and machines. Most published thinking still treats docs as a website for humans. The 2024+ practice ships docs as a parallel layer — human-readable Storybook/MDX *and* machine-readable metadata + registries — generated from the same source. Documentation is not the appendix; it is the system's surface.

---

## What this phase is, and why it matters

A component without documentation is a component that consumers will guess at. Guessing scales poorly. Documentation is the artifact that makes the system legible to the people (and now agents) who weren't in the room when decisions were made. It's also the artifact most likely to be deferred, under-resourced, and out of date — because shipping the component feels like the work, and writing about it feels like overhead.

Three reasons documentation deserves a phase, not a footnote:

1. **Intent does not survive otherwise.** A token, component, or pattern without a description of *why* and *when* will be misused within months. Couldwell's IKEA-without-instructions analogy still lands: the diagram doesn't tell you how to assemble it. (*Laying the Foundations*, 2019.)
2. **AI agents and code generators consume docs literally.** What humans can infer from brand context, agents cannot. Documentation that omits intent now produces wrong-component, wrong-token, off-brand outputs at scale. (Figma DS x AI, 2025; Wolosin, Jun 2025.)
3. **Documentation *is* training data.** Each tagged component, each token description, each `avoid_when` rule is a labeled data point that informs future AI selection — and, increasingly, future model fine-tuning. (Wolosin: *"Metadata isn't busywork. It's training data for the future of design."*)

Internal practice already names a dedicated UX Designer role to own documentation strategy across the engagement (CareCentrix 2026). The opportunity is to extend that role from "human docs strategist" to "human + machine docs strategist" and ship both layers as standard.

## What actually happens in this phase

Six clusters of work, run continuously through the engagement.

### 1. Documentation strategy and information architecture

- **Reference-site IA.** Standard sections (per scoping doc and CareCentrix): Home / Getting Started / Guidelines (Accessibility, Color, Typography, Layout, Theme, Tokens) / Component Overview / Per-Component pages / Patterns / Support / Changelog.
- **Per-component minimum.** Name, short description, primary purpose, examples (design + code), do's & don'ts, accessibility rules, states (rest/hover/focus/disabled/error/loading), content guidelines, historical context (Couldwell's Adobe Portfolio cautionary tale: undocumented, lost the "why").
- **Cross-disciplinary collaborative naming.** Designers, engineers, PMs, and content strategists agree on what things are called *before* docs are written. (Mall, 90 Days Activity #25 — glossary as a Discovery deliverable, not an appendix.)
- **Tooling decision.** The standard menu (Storybook, Supernova, Pattern Lab, Zeroheight, GitBook, custom site) is well-known; the choice is rarely the leverage point. The leverage point is *consistency between design files, code, and docs* — the same name in all three places (Couldwell).

### 2. Document intent, not appearance

- **Explain the *why*.** Not "this is a button"; "use this component when the user must take an action that progresses the primary task." (CareCentrix 2026 + Figma DS x AI 2025.)
- **Color guidance includes purpose.** "Why these brand colors? When and why use X over Y?" (Couldwell.)
- **Tokens carry descriptions** (`$description`). The single highest-ROI single action for AI compatibility — and equally valuable to human juniors. (AI-Compatible Design Systems, Feb 2025.)
- **Components carry usage rules with explicit *avoid_when*.** Negative selection prevents more mistakes than positive examples alone. (Wolosin Jun 2025; AI-Compatible Design Systems Feb 2025.)

### 3. Layered documentation architecture (2024+ standard)

The practice's emerging stance — and the one that differentiates from legacy "docs site" thinking — is that documentation is **a parallel layer**, not a single artifact. Wolosin's four-tier metadata loop (Jun 2025) is the cleanest articulation:

| Tier | Location | Audience | Update mechanic |
|---|---|---|---|
| **1. Structured metadata** | `.ai.json` per component + registry | AI agents (via MCP) | Authored alongside component |
| **2. Embedded in design tool** | Figma component descriptions, variable names, variant labels | Designers in Figma | Updated in design |
| **3. Embedded in code** | TypeScript types, JSDoc, semantic prop naming | Developers in their IDE | Updated in code |
| **4. Cross-tool links** | Figma↔Storybook dev links; Code Connect | Both, switching contexts | Generated from ID joins |

The internal AI-Compatible doc maps these tiers to an explicit four-layer stack:

1. **Tokens with descriptions** (every token has `$description` in DTCG JSON).
2. **Component metadata** (`.ai.json` + registry).
3. **Agent instructions** (`AGENTS.md` / `CLAUDE.md`) — the practice's claim is that none of the public discourse names this artifact yet; this is a defensible POV differentiator.
4. **Figma pipeline** (variables → DTCG export → Style Dictionary → CSS custom properties; Code Connect; MCP).

### 4. Generated, not handwritten

The 2025+ standard: docs are generated from component definitions, not handwritten alongside them. Curtis's *Components as Data* (Sep 2025) makes the case explicit — when components are YAML/JSON definitions, the documentation site, the code, the Figma assets, and the AI registry all derive from the same source. This is what closes the gap between "documented" and "actually accurate."

The mechanism (drawn from Curtis + Wolosin + Mangialardi):

- Component data file (YAML/JSON) is the source.
- Storybook stories are generated from the data + variants.
- MDX prose pages are authored, but every parameter list, every default, every example state is generated.
- `.ai.json` is generated (with human-authored `when_to_use` / `avoid_when` / `business_context`).
- Code templates per framework are generated (or scaffolded).
- Figma component sets are generated (or rebuilt from data).
- A CI check fails the build if the component code changes but `.ai.json` doesn't. (AI-Compatible doc Ch.7 — *metadata freshness tracking*.)

Most clients will not arrive at this on day one. The practice's job is to set the architecture so that when the client is ready to add generation, the foundation supports it.

### 5. Layer hygiene and structure

A practical Figma-side discipline named in Figma DS x AI (2025): clean files parse better. No unnecessary groups or frames; consistent layer naming; component instances rather than detached copies; variants properly structured. AI agents (and humans new to a file) read the structure as signal — chaos in the file becomes chaos in the output.

### 6. Documentation as sales surface

The site is also a sales artifact for adoption. Couldwell's stance: *"The guidelines and decisions you make when designing a system are no good just in your head."* If consumers can't find, understand, and trust the documentation in three minutes, they will either build wrong or build their own. Both are adoption failures.

Tactics:

- Search-first IA. Most consumers arrive looking for one thing.
- Examples before specs. Show the working component, then explain the props.
- Right-and-wrong examples explicit. Do/don't side-by-side.
- States documented and visible (rest / hover / focus / disabled / loading / error / empty).
- Accessibility details inline (color contrast, keyboard nav, screen reader expectations) — not in a separate a11y page consumers won't visit. (Figma DS x AI, 2025.)
- Changelog and versioning visible. Adopters need to know what's stable, what's deprecated, what's coming.

## Content as a system layer

The practice's content material has lived almost entirely at the per-component layer for the full life of the corpus. The Cluster-1 Content guidelines bullet (per the CareCentrix 2026 standard) ships content per component; 29 §14 captures content as one of seventeen template fields; 30 §Authored locates content guidance in the human-authored half of the pipeline; 03 names the microcopy seam at the component-library level; 25 / 26 / 27 cover AI-surface content at the pattern level. None of this articulates the system-level content architecture *above* the per-component layer — the voice-and-tone matrix as a system artefact rather than per-component microcopy guidance; content tokens as a tokenised primitive analogous to design tokens; i18n content as system-level scope tied back to component content guidelines; AI-surface content as a content-system layer rather than per-25/26/27-pattern guidance. This section closes that gap.

The hierarchy this section commits: **voice-and-tone constraint at the top; content tokens at the primitive layer; per-component guidance as the consumption layer.** All three articulated; the architecture established once per engagement to serve as the structural foundation; per-component guidance follows the architecture rather than leading it. The agency that ships per-component content guidance without the system-level architecture produces fragmented microcopy that drifts release-by-release; the agency that ships content tokens without the voice-and-tone constraint above them ships primitives that fail to compose into coherent brand voice. Linear's empty-states pattern works *because* Linear has a strong, articulated voice; the same primitives in a brand without the voice constraint produce inconsistent output. All three layers are necessary; the system-level architecture is the practice's leverage at engagement scale.

### The voice-and-tone matrix as a system artefact

The voice-and-tone matrix is the practice's most-undersold content artefact at system altitude. Mailchimp's *Voice and Tone* (`styleguide.mailchimp.com/voice-and-tone/`) is the canonical field reference; Shopify Polaris's *Voice and tone* (`polaris.shopify.com/content/voice-and-tone`) is the design-system-native reference; the Atlassian Design System's *Writing style* and IBM Carbon's *Content guidelines* both ship matrix-shaped artefacts. The shared shape: **voice** (the brand's immutable character — the thing that doesn't change between a confirmation toast and a destructive-action dialog) across the top of the matrix; **tone** (the contextual adjustment per situation — confident in success, calm in error, direct in destructive-action) across the side; body cells specifying how voice expresses in each tone context.

The matrix's altitude is system-level — applied across every surface, not per-component. The brand's three-to-five voice attributes are the immutable column headers; the system's content contexts (success / error / destructive / empty / loading / disabled / read-only / informational; plus AI contexts per the AI-surface section below) are the tone row headers; the body cells specify how voice expresses in each context.

The matrix the practice ships at engagement scale follows the shape below. Voice attributes are brand-specific (the three columns are illustrative — Expert / Warm / Direct serves as a worked example; real engagements author against the client's brand). Tone contexts are system-specific.

| Tone context ↓ / Voice attribute → | Expert (clear, authoritative, precise) | Warm (empathetic, human, supportive) | Direct (unambiguous, efficient, plainspoken) |
|---|---|---|---|
| **Success / confirmation** | Validates the system state definitively ("Database synchronisation complete"). | Acknowledges the user's effort without exuberance or patronising. | States the outcome immediately, no filler ("Changes saved"). |
| **Error / network failure** | Diagnoses the cause precisely; never dead-ends. | Validates frustration; never blames the user; offers the next path. | Names the remediation step ("Check connection and retry"). |
| **Destructive action** | Names the technical scope of the deletion and any retention. | Calm, never alarming; confirms intent without inducing panic. | Stark, unmistakable verbs ("Delete permanently", not "Remove"). |
| **Empty state — first-use** | Explains the surface's capability and required inputs. | Encourages the first interaction; never patronising. | Single, clear imperative verb ("Start", "Create"). |
| **Empty state — no-results / filtered-out** | States the filter that excluded results; never abstract. | Brief; offers the next action (clear filters; broaden criteria). | Short; no metaphors. |
| **Loading / processing** | Specific where possible ("Searching 1,200 records…"). | Reassuring; acknowledges wait without anxiety. | Concise progress; "Loading…" only when no specifics available. |
| **Disabled / read-only** | States the constraint precisely; never the symptom. | Neutral; explains why if non-obvious. | Avoid passive voice. |
| **Informational** | Names what's true; avoids hedging. | Helpful, never lecturing. | Short sentences; one idea per callout. |
| **Assistant — proactive** (per AI-surface section) | Offers one thing; never overwhelms. | Warm but bounded. | No filler ("I can help with…"). |
| **Assistant — refusing** (per AI-surface section) | Names the constraint precisely; offers the alternative. | Acknowledges the request; never apologetic loops. | Direct; no hedging. |

The matrix is the artefact; the body cells are the system's voice expressing in each context. The matrix ships as part of the content-system deliverable; per-component content guidance per 29 §14 references the matrix's body cells rather than re-authoring them.

The matrix is only useful if it's enforceable. Three enforcement disciplines work — and the highest-leverage one is AI-prompt-mediated. **Matrix-as-AI-system-prompt** (the most aggressive discipline): the matrix becomes the system prompt the AI assistant consumes; per 25 §The architecture beneath; per 27's structured-output scaffolding — the assistant's outputs are constrained by the system prompt; the system prompt encodes the voice attributes plus the relevant tone-context body cells; the assistant's outputs inherit the brand voice without per-output authoring. Voice fragmentation across AI surfaces becomes structurally prevented. The matrix directly parameterises the LLM. **Pre-merge content review**: every PR with content changes runs the matrix's three or four voice questions before merge; the reviewer (typically the UX Copywriter per the next section) confirms the new content satisfies the matrix's voice attributes for the relevant tone context; ~5 minutes per content-bearing PR. **Token-mediated authoring** (per the content-tokens subsection below): when the system ships content tokens, components consuming the tokens inherit the matrix's voice rather than authoring per-component; the matrix's voice expresses *through the token catalogue*. Token-mediated authoring is the most durable enforcement because it removes the per-component authoring step entirely. Without enforcement, the matrix decays into a docs page nobody reads; per-component content drifts release-by-release; the brand voice fragments.

For multi-brand and white-label-for-resellers systems (per 24 / 33), the voice-and-tone matrix scales as a per-brand axis. Each brand's matrix is one of the per-reseller assets the engine generates per 33 §7. The Theme Schema's voice-tone parameter (per 33's brand-voice tone parameter at §3 / §5) is the for-resellers system's voice-axis input; the engine derives the per-brand content tokens from the voice parameter the way it derives the color tokens from the primary-color primitive.

Voice connects to typography at the token layer. Per 23 — typography is voice in type; the brand-voice-as-immutable-system-constraint framing in 23 covers the type-side voice; the matrix here covers the content-side voice; both express the same brand constraint at the system level. The link is operational at the typography composite-token layer — the composite typography token's `$description` field carries the voice intent (the practice's tokens-with-descriptions discipline applied to the content / voice axis). See 23 for the typography-side discipline.

### Content tokens / writing-tokens as a primitive

The field is starting to ship content tokens, mostly without naming them as such. **Linear's empty-states.** Each empty state across Linear's product surface carries a consistent encouraging-not-perky voice via what are effectively templated tokens — first-use, no-results, filtered-out — the voice is consistent because the primitives are shared. **Stripe's error-message taxonomy.** Errors carry codes (`card_declined`, `insufficient_funds`, `expired_card`); the codes map to user-facing message templates; the templates carry Stripe's voice (clear; never blaming; always offering the next action). **Polaris's content-pattern primitives.** Polaris ships pattern tokens for CTAs, error microcopy, loading messages — each with usage rules and parameter slots. **GOV.UK's component content patterns.** GOV.UK Design System ships content patterns for date input, names, addresses, error messages — each pattern carries the GOV.UK voice (concise; plain English; accessible reading level) as a tokenised template. **IBM Carbon's content guidance.** Carbon ships content-pattern guidance for empty states, error messages, notifications — less explicitly tokenised than Linear or Stripe but moving in the same direction.

The shared shape: content as a *named, reusable, composable resource* analogous to design tokens — primitives the consumer pulls off the shelf rather than authoring per-component. Every system already ships these implicitly through pattern guidance; making them explicit (named, versioned, governed, AI-readable) converts implicit IP into an operational primitive.

The line between content-as-token and content-as-prose is the same line as design-tokens-vs-component-styles: tokens carry *templated, system-level* content; prose carries *judgment*. **Tokenisable.** CTA verb taxonomies (the system's verbs — "Save", "Continue", "Submit", "Cancel", "Discard", "Discard changes" — with usage rules and tone-context mappings); error message templates per error category (network / validation / permission / destructive-confirm); empty-state copy patterns (first-use / no-results / filtered-out / system-empty / waiting-for-input); loading-state microcopy ("Loading…" / "Searching…" / "Saving…" / "Generating…"); confirmation patterns (success messages; toast copy; destructive-action confirmation); disabled-state explanations; loading skeletons' ARIA-live announcements; AI-surface refusal templates; disclosure boilerplate; citation copy templates. **Not tokenisable.** Long-form prose; marketing copy; brand-narrative content; per-component intent prose (the "when-to-use" and "avoid-when" guidance is per-component judgment, not a token); authored content in product surfaces (blog posts; help documentation; legal text — these live in CMS per the CMS-vs-content-tokens line below). The discipline is testable — if the content varies meaningfully per-instance based on the local situation (the specific error code; the specific empty-state context), it's tokenisable with parameter slots; if it varies meaningfully based on human judgment, it's prose.

The DTCG-shaped schema for content tokens is the practice's defensible POV. As of mid-2026, DTCG's 2025.10 Format Module covers design tokens (color, spacing, typography, motion, dimension) but **does not cover content tokens**. The closest precedent is i18n message catalogues (ICU MessageFormat per 13). The practice can lead by shipping a content-token schema shape as a custom DTCG `$extensions` extension; if and when the DTCG community ratifies a content-token spec, the practice migrates.

The schema's load-bearing properties:

| Schema property | Type | System function |
|---|---|---|
| `$type` | String | Declares the token type as `content` (or `message`). Signals to translation, build, and validation tools that the value requires linguistic processing rather than transformation as a design value. |
| `$value` | String | The source-locale ICU MessageFormat template (e.g., `"{count, plural, one {# item selected} other {# items selected}}"`). ICU-shaped from authoring time; pluralisation, gender, ordinal-aware via ICU selectors. |
| `$description` | String | The voice intent — references the relevant tone-context body cell from the voice-and-tone matrix above ("Used in error states. Voice: calm, never blaming. Tone: direct without alarm. Per voice-and-tone matrix §Error."). The contract between the matrix and the token; reviews against the matrix happen here. |
| `$extensions.<vendor>.parameters` | Object | The slot shape — each parameter has type and usage description; parameters are validated at runtime; AI clients consume the parameter shape via `.ai.json` integration per 30 and respect it during composition. |
| `$extensions.<vendor>.locale` | Object | The i18n axis — default locale; per-locale variants live in the localisation catalogue keyed by the token's name; ICU-conformance flag. |
| `$extensions.<vendor>.tone` | String | Ties the token back to the matrix — the tone-context name is the body-cell key the description references ("error", "destructive", "assistant-refusing"). |
| `$extensions.<vendor>.ai-readable` | Boolean | The `.ai.json` integration flag per 30 — when true, the token is consumed by AI clients via the per-component MCP surface; when false, the token is human-only. |

Cross-platform localisation flows naturally from this shape. The token's `$value` is the source-locale template; per-locale variants live in the i18n catalogue keyed by the token's name; the runtime resolves per the user's locale via ICU. Without content tokens, every component carries its own i18n integration; with content tokens, the integration happens at the token layer.

Where content lives — in the DS's content tokens or in the CMS's content models — is a procurement-grade decision. The practice's working position: **tokens for templated, system-level content; CMS for editorial, product-specific content.** The line is similar to design tokens vs. component-specific styles: tokens for system primitives; component-specific authoring for per-instance overrides. **Tokens.** "Save" / "Cancel" / "Discard changes" CTA verbs (every product uses them). Network-error templates. Empty-state copy patterns. AI-surface refusal templates. Disclosure boilerplate. **CMS.** Help documentation. Marketing copy. Blog posts. Legal text. Per-product feature names. Per-product onboarding copy. The boundary surfaces again at the i18n layer (per the next subsection) and again in the forthcoming §1.32 CMS work; the practice's discipline is to name the boundary at scoping.

Tooling reality and gaps. Tokens Studio doesn't ship content tokens as a first-class object (custom metadata via `$extensions` is the bridge investment); Style Dictionary's transforms don't cover content tokens natively (custom transforms required, ~8–16 hours per platform); Specify, Knapsack, Supernova, Backlight don't ship content tokens as a first-class object; ICU authoring tooling is thin — most CMSes don't author ICU; most translation vendors have varying ICU support (Lokalise, Crowdin, and Phrase support ICU; Smartling and TransPerfect have varying support; verify per vendor); ICU's parser-error mode is brittle (authors mistakenly using double curly braces instead of single braces produce parse failures). The practice's bet: native vendor support for content tokens lands in 2026–2027 alongside the AI-readiness commercial pressure; practitioners shipping content tokens today are wrapping ICU message catalogues with DTCG-shaped metadata as a bridge investment.

LLM-based content review tooling is emerging — LLMs can read the matrix above and review content-PR diffs against it (automated voice / tone consistency checking). As of mid-2026, this is custom work (senior practitioners script it via Claude API; no major DS-tooling vendor ships LLM content review natively); the practice's bet is that this lands in 2026–2027.

### i18n content depth at the system level

Per 13 — the practice covers RTL and locale shape at the architectural level. What this section adds is the content layer above 13: how component content guidelines tie back to i18n tooling; how content tokens (per the previous subsection) carry locale variants; how the UX Copywriter role coordinates with localisation vendors; how the voice-and-tone matrix handles per-locale tonal adjustments.

ICU MessageFormat at system scale integrates with content tokens — the token contains an ICU template; the runtime resolves via ICU per the user's locale. The system ships ICU-shaped templates, not hand-authored per-locale strings. Most engagements still ship hand-authored per-locale strings because the tooling for ICU authoring is thin; the practice's discipline at engagement scale is to author ICU-shaped templates from day one of the content-token catalogue; localisation vendors translate the ICU templates per locale (preserving ICU shape); the runtime resolves per locale.

Pluralisation at system scale illustrates the necessity. The English speaker's mental model — *one cat / two cats* — doesn't generalise. **Russian** has three plural categories (one / few / many); **Arabic** has six (zero / one / two / few / many / other); **Welsh** has six; **Polish** has four; **Japanese and Chinese** have one (no inflection by count); **Slovenian** has four. ICU expresses pluralisation via the `plural` selector with named CLDR cases (`zero`, `one`, `two`, `few`, `many`, `other`). Content tokens carrying ICU templates handle this natively; per-locale variants in the localisation catalogue carry locale-specific plural categories. Hand-authored per-locale strings break here — the English authoring "one item / N items" doesn't translate to Russian's three categories without re-authoring.

Gendered language. ICU's `select` selector handles gendered variants. **Spanish** has masculine / feminine; **German** has three genders; **Finnish** has none; **Hebrew** has masculine / feminine in second-person address. Content tokens at system scale declare the gendered variant axis as part of the token shape; per-locale catalogues carry the variants; the runtime resolves per the user's gender preference (or the application's known data about the user). The pattern that fails: gendered language treated as per-component; per-component microcopy authored without gender-axis support; the application produces grammatically incorrect output in gendered locales.

RTL content ordering. Per 13 — logical properties at the layout level. At the content level: bidirectional content embedding (Arabic-with-English-loanwords; Hebrew-with-numbers); the Unicode `<bdi>` element (bidirectional isolation) versus `<span dir="rtl">` directional override; the `unicode-bidi` CSS property's role. Content tokens at system scale carry directional metadata — the token's primary direction; the embedded-content directional handling. The discipline: prefer `<bdi>` over `<span dir="rtl">` to prevent cross-directional pollution between the directional run and surrounding content.

Localisation governance. The UX Copywriter (per the next H2 section) coordinates with localisation vendors on per-locale content. The system's content tokens are the source-of-truth; the localisation vendor consumes the source tokens and produces per-locale variants; the variants flow back into the content-token catalogue. Without content tokens, localisation is per-component string-by-string; with content tokens, localisation is catalogue-shaped. The vendor landscape: TransPerfect, Lionbridge (the large translation vendors); Smartling, Lokalise, Crowdin, Phrase (the modern localisation platforms). The content-token catalogue is portable across platform vendors via standard formats (JSON, XLIFF, TMX, Gettext); the practice's discipline is to keep the catalogue portable and treat the platform vendor as a workflow tool rather than a lock-in.

The line that connects to §1.32 (CMS platforms — forthcoming). Localised editorial content lives in the CMS; localised system content lives in the content-token catalogue. The boundary is the same as the content-token-vs-CMS line above — system-level vs. product-specific. When §1.32 deepens 10 with the headless / composable / MCP-for-CMS-components material, the boundary articulated here applies at the broader CMS surface (Sitecore, Contentful, Sanity, Strapi, Storyblok).

### Content for AI surfaces as a content-system layer

Per 25 / 26 / 27 — the practice ships AI-aware patterns (chat, streaming, citation, refusal, tool-call) and adaptive interfaces (Sentient Triangle scaffold, fourteen patterns, five-rung spectrum). The content half of these patterns — assistant tone, refusal copy patterns, disclosure boilerplate, citation format conventions, error / fallback / clarification / tool-call-confirm copy — is currently per-pattern in 25 / 26 / 27 but not articulated as a content-system layer. The voice-and-tone matrix above + the content tokens above + the UX Copywriter role below collectively own the AI-surface content layer at system scale.

**Assistant tone as voice-and-tone applied to AI surfaces.** The brand's voice constrains the assistant's outputs; the matrix's contexts include AI-surface contexts (assistant-proactive / assistant-reactive / assistant-uncertain / assistant-refusing / assistant-clarifying / assistant-handing-off-to-human). The matrix's body cells for AI contexts specify how the brand voice expresses in each AI context — and become the system prompt the assistant consumes (per 25 §The architecture beneath; per 27's structured-output scaffolding). **The matrix directly parameterises the LLM.** This is the highest-leverage AI-surface enforcement pattern; the matrix isn't a docs page, the matrix is in the assistant's runtime prompt; voice consistency across AI surfaces becomes structurally guaranteed.

**Refusal copy patterns.** Per 25 §Refusal patterns — the assistant refuses (out-of-scope; safety; capability; privacy). Each refusal category has a content-pattern shape — the refusal acknowledges the request, names the constraint, offers an alternative path. Content tokens at system level ship the refusal templates per refusal category; the templates carry the brand voice; per-pattern customisation fills the parameter slots. Without tokens, every product surface re-authors refusal copy and the brand voice fragments.

**Disclosure boilerplate.** Per 25 §Disclosure (EU AI Act Article 50 framing). Disclosure copy is system-level — the system ships the disclosure template; products consume the template; the legal team reviews the template once not per-product. Content tokens at system level ship the disclosure templates. Disclosure that drifts per-product is a compliance risk under EU AI Act Article 50; tokenised disclosure is structurally enforced.

**Citation format conventions.** Per 25 §Citation patterns — the assistant cites sources. Citation format (inline-link / footnote / sidebar / collapsible) is per-pattern; citation copy conventions (how to introduce a citation; how to handle partial-confidence citations; how to handle missing-source cases) is system-level. Content tokens carry the citation copy templates — confident citation ("{source} states {claim}"); partial-confidence citation ("{source} suggests {claim}, though context may matter"); missing-source case ("I don't have a source for this; treat as opinion").

**Streaming / partial-output / interruption content.** Per 25 — streaming responses produce partial outputs; users may interrupt; the system shows a partial state then a final state. The content for streaming UI (the "thinking…" / "generating…" / "almost done…" microcopy; the interruption confirmation; the resume-vs-restart prompt) is system-level. Content tokens carry the streaming-state templates; the family's body cells per the matrix carry the brand voice in streaming contexts (calm; never anxious; specific where possible; never apologetic).

**Tool-call confirmation.** Per 25 §Tool-call patterns + 27's structured output rendering — the assistant proposes a tool call; the user confirms. The confirmation copy ("This will send an email to {recipient}. Continue?") is system-shaped via tokens; the tool-call's specific parameters fill the parameter slots. The matrix's destructive-action body cell applies — direct without alarm; name the consequence; never bury the lede.

**Adaptive-UI content (the variability-by-design problem applied to content).** Per 26 / 27 — adaptive interfaces compose components per render via LLM. The components' content (the microcopy in each rendered component; the copy in adaptive empty-states / loading-states / refusal-states) is system-shaped — the LLM composes from the system's content tokens, not from ad-hoc strings. The variability-by-design problem (per 26's residual gap on purpose-built authoring tooling for variability) applies to content as well as visual: the designer specifies a *space* of possible content outputs and reviews the *distribution* of what the LLM produces. **Content tokens are the boundary the variability operates within** — the LLM composes within the token catalogue; the token catalogue carries the matrix's voice constraint; the matrix is enforced at composition time. The pattern that fails: the LLM composes free-form content that drifts from the matrix; the brand voice fragments; per-render variance is unbounded. The pattern that works: the LLM composes from tokens; the variance is bounded; the matrix is structurally enforced.

## The UX Copywriter role at engagement scale

The CareCentrix 2026 commercial standard (Our POV, below) names a UX Copywriter at 75 fixed hours integrated into component documentation. The role is named but not justified — the 75 hours is a CareCentrix-specific number; what justifies more or fewer hours; what the role owns end-to-end at system scale; how the role hands off to client product teams; how content guidelines get maintained after handoff — none of this is articulated. This section closes that gap.

The UX Copywriter is the practice's content-side analogue to the design technologist (per 00e) — a hybrid role that crosses content / design / engineering boundaries. Hiring signal: writing fluency at senior level (the role authors the system's voice; weak writing produces a weak system); design-system literacy (the role consumes 22 / 23 / 24's token discipline and produces a content-token catalogue against it); i18n awareness (the role coordinates with localisation vendors and authors ICU-shaped templates); AI-surface fluency (the role authors the system prompt's voice constraint and the AI-surface content templates per the section above). The role doesn't need to be a senior software engineer; the role does need to operate fluently with engineering counterparts on token-catalogue mechanics and AI system-prompt coordination.

### What the role owns end-to-end

Four ownership clusters:

- **Content architecture.** The voice-and-tone matrix; the content-token catalogue; the i18n content strategy; the AI-surface content layer. The role authors the matrix at engagement Discovery; ships the content-token catalogue alongside Foundations; coordinates the i18n strategy with the localisation vendor; ships the AI-surface content layer alongside whichever 25 / 26 / 27 patterns the engagement scopes.
- **Content production.** The system-level content (matrix, tokens, templates, AI-surface copy) per Cluster-2 above (Document intent). The role authors the system-level content directly; per-component content guidance per 29 §14 references the system-level content rather than re-authoring.
- **Content review.** Per-component content guidance review; pre-merge PR review for content changes (~5 minutes per content-bearing PR); release-readiness content audit per the matrix's enforcement disciplines (a quarterly drift audit at portfolio scale; the audit produces a remediation list for the next quarter).
- **Cross-functional coordination.** Localisation vendor coordination (~4–8 hours per locale beyond source — TransPerfect / Lionbridge / Smartling / Lokalise / Crowdin / Phrase); legal review for disclosure copy (~8–16 hours per major release for legal-review cycles under EU AI Act Article 50); brand-team review for voice-and-tone matrix evolution (~4–8 hours per quarter); AI-surface tone-prompt coordination with the engineering team that ships the prompt.

### The hour-justification model

The CareCentrix 75 hours is a Pattern 2 (Figma-only handoff per 00d) standard-complexity number. At engagement scale, the role's hours scale against three drivers:

- **Component count.** ~0.5–1 hour per component for the per-component content guidance per 29 §14 — primarily review and matrix-binding rather than authoring (the matrix and content tokens carry most of the per-component work).
- **Content-surface complexity.** AI surfaces add ~20–40 hours per AI pattern family (chat / streaming / refusal / citation / tool-call). Multi-locale adds ~30–60 hours per locale beyond the source (vendor coordination; ICU template authoring; per-locale tone review for tonal-adjustment locales — Japanese keigo, German Sie/du, etc.).
- **Content-token catalogue depth.** A deep catalogue (CTA / error / empty-state / loading / confirmation / disclosure / citation / refusal token families) adds ~40–80 hours; a thin catalogue (errors only) adds ~15–25 hours.

The CareCentrix 75 hours fits roughly **20–25 components, English-only, no AI surfaces, a thin token catalogue**. Other points on the range:

| Engagement shape | Hours |
|---|---|
| Pattern 1 (Product-support component build), 15 components, English-only, no AI surfaces, error tokens only | **~40–60 hrs** |
| Pattern 2 (Figma-only handoff), 20–25 components, English-only, no AI surfaces, thin catalogue (CareCentrix baseline) | **~75 hrs** |
| Pattern 2, 30 components, English-only, no AI surfaces, thin catalogue | **~80–100 hrs** |
| Pattern 2, 30 components, three locales (English + two others), no AI surfaces, standard catalogue | **~140–180 hrs** |
| Pattern 6 (white-label per 33), 50 components, English-only at launch, AI surfaces (chat + refusal + citation), deep catalogue | **~180–250 hrs** plus Run-phase retainer |

The practice's discipline: scope the role against the three drivers; quote a range (40–250 hours per Build) with the driver mix making the case for the chosen point in the range. The CareCentrix 75-hour line item becomes a defensible point on a scaled range rather than a number quoted without justification.

### When a system needs the role

Below ~10 components, the role doesn't pay back — the content guidance is thin enough for the senior visual designer or UX designer to author directly. Above ~10 components, content drift becomes visible by release; above ~20 components, content drift becomes a failure mode (per the Failure modes section below). At ~20+ components with multi-locale or AI-surface scope, the role's payback is strongest; below, it's optional.

The minimum viable scope for the role's inclusion: **~10 components plus any of multi-locale, AI surfaces, or recurring content-system maintenance (Run-phase retainer).** At less than that, content can be absorbed by the senior visual designer or UX designer; at more than that, content drift without the dedicated role becomes a release-cost.

### Handoff to client product teams

The role hands off three things at engagement end:

- **The voice-and-tone matrix as a governed artefact.** The client's content team owns evolution; the practice provides the matrix shape and the per-context body cells; the client extends per their content surface's needs over time.
- **The content-token catalogue as a maintained primitive.** The client's engineering team consumes; the client's content team authors token additions; the practice provides the schema shape, the initial catalogue, and the token-evolution discipline (semver-for-content-tokens analogous to 24's semver-for-design-tokens).
- **The per-component content guidance per 29 §14.** Consumed by the client's product teams; the practice provides the initial per-component guidance and the matrix-binding discipline; the client maintains as components evolve.

The handoff is incomplete without the governance contract — who reviews matrix changes; who approves token additions; who coordinates localisation. This is content's analogue to the 07 contribution-model handoff at the component layer. The practice's discipline: ship the governance contract alongside the content-system handoff; without it, the system the client paid for decays as soon as the practice leaves.

### The Run-phase parallel

Per 33 §5 — white-label-for-resellers ships a run-phase retainer with three SLAs (brand-onboarding / engine-availability / schema-coordination). Bespoke engagements with a content-system handoff can ship an analogous content-retainer with three commitments:

- **Matrix-evolution coordination.** Quarterly matrix review; new tone contexts added as the client's product surfaces grow; voice attributes maintained across the matrix's evolution.
- **Token-addition review.** New content tokens reviewed against the matrix; schema-shape conformance; voice / tone metadata complete; AI-readability flag set correctly.
- **Localisation coordination.** Per-locale variant review with the localisation vendor; ICU shape preserved; per-locale tone review for tonal-adjustment locales.

The retainer follows the same shape as 33 §5 but applied to the content layer — three discrete commitments, each with an explicit SLA, each with an hour estimate, all priced as a recurring monthly retainer (typically 8–24 hours/month depending on content-surface complexity). Content is one of the natural Run-phase retainer surfaces the practice has not yet articulated; this section adds it to the run-phase pricing landscape that 00d's run-phase pricing gap and 33 §5's for-resellers retainer also occupy.

### Connection to 00e team-and-discipline

The role's hiring signal, seniority calibration, and career path within the practice are open questions worth picking up in a future 00e revision. This section lands the role's *engagement-scale* discipline; the *practice-scale* discipline (how the practice hires, levels, and progresses Copywriters across engagements) belongs in 00e.

## Our POV

The CareCentrix 2026 commercial standard:

- **Dedicated UX Designer role** owns documentation strategy across the engagement. Defines structure and format of Figma component documentation; documents do/don't, states, accessibility notes; ensures docs are actionable for an engineering audience.
- **Usage documentation per component** (when/how to use, do/don't, annotated specs).
- **Design patterns documentation** (common workflows and interface patterns for internal tooling).
- **Content guidelines** (tone of voice, error message patterns, help text best practices).
- **UX Copywriter role** (75 hours scoped): integrates content guidelines into component documentation.
- **Accessibility standards documentation** (contrast ratios, type minimums, focus state specs).
- **Digital style guide in Figma** covering all foundational elements with usage doc.
- **Published Figma component library** ready for engineering consumption.

**Practice-distinctive POVs in this phase:**

- **Documentation is a named role, not a residue.** A dedicated UX Designer owning docs strategy across the engagement is rarer than it should be in consultancy practice. We sell this; we should sell it harder.
- **UX Copywriter for content standards.** A consistent dedicated role for tone, error messages, and help text — operationalized as hours, not aspirations. (CareCentrix 2026 introduced this; Thrive 2024 didn't.)
- **Accessibility integrated into component docs**, not as a separate chapter.
- **Token descriptions as a default deliverable.** Every token gets a description; the AI-Compatible doc names this as the highest-leverage move. We should make this default in commercial proposals (currently aspirational).
- **The four-layer AI documentation stack** (tokens with descriptions / `.ai.json` + registry / `AGENTS.md` + `CLAUDE.md` / Figma pipeline). The instruction-file layer (`AGENTS.md`/`CLAUDE.md`) is genuinely under-theorized in public DS discourse; the practice can claim it.
- **AI-aware patterns ship with their own documentation contract.** When the system also publishes consumer-facing AI patterns (chat input, streaming, citation, refusal, tool-call), the disclosure copy, refusal copy, citation behaviour, and approval workflow become docs deliverables in their own right — and they sit alongside legal/governance artefacts (PIA, Article 50 disclosure language) the docs site does not normally host. (See 25-ai-aware-patterns-and-conversational-ui.)
- **Component-prompt pairs as the emerging docs artefact for adaptive UI.** When components participate in LLM composition, the docs unit shifts from "component + props table" to *component + JSON schema + semantic prompt* — a bundled, machine-readable description of when and how the component should be used. No design tool authors this pairing as a first-class object yet; the prompt half is improvised in code or markdown. The practice can lead by shipping this layer as a default `.ai.json` extension. (See 26-adaptive-interfaces-foundations and 27-adaptive-interfaces-implementation.)
- **The accessibility annotation contract as `.ai.json` fields.** The per-component annotation in 17-accessibility-annotation-contract — name mechanism, role, state, ARIA relationships, focus-return target, `forced-colors` survival, APG keyboard pattern — maps 1:1 to fields in the component's `.ai.json` schema. This is what closes the gap between "the design system documents accessibility" and "the code-generation pipeline cannot produce a non-conformant component." A modal-dialog component flagged in `.ai.json` mandates `inert` scope and a focus-trap requirement; an input flagged with an error state mandates the `aria-invalid` and `aria-describedby` wiring. The schema is the contract. (See 28-web-accessibility-implementation §9 for the web annotation fields and 16-mobile-accessibility-implementation for the mobile counterparts.)

**Gaps in our current commercial Documentation standard, honestly named:**

- **The IA of the docs site itself is not a deliverable.** "Reference website v1" is named in scoping; the IA, search behavior, navigation patterns, and per-component template aren't. They should be — the site experience is the adoption experience.
- **Generated-from-data as commercial default — articulated by 30-generated-from-data-documentation (June 2026).** Curtis's *Components as Data* model is the architectural answer; the practice now ships a phased-adoption commercial framing (Phase 1 baseline generation, Phase 2 Code Connect and Figma sync, Phase 3 custom MCP server), the per-component hours redistribution (2–8 hours generated vs. 4–11 authored), the ~30-component break-even, the 5-question decision tree, the migration playbook off Notion / Confluence / GitBook / Zeroheight / hand-rolled. The residual gap is now in the next engagement: this is articulated; commercial proposals still need to itemise it as a Foundations-tier deliverable.
- **Machine-readable docs are aspirational, not contractual.** AI-Compatible doc covers `.ai.json` and registries; CareCentrix-style proposals don't yet ship them. This needs to flip — every component shipped should have a peer `.ai.json`.
- **Tooling opinion is thin.** Scoping doc lists Storybook / Supernova / Pattern Lab / Zeroheight / GitBook without trade-offs. Clients ask which to use; we should have a defensible recommendation framework rather than "depends."
- **Closed by 29-per-component-documentation-template (June 2026).** The practice now ships a 17-section template — header, summary, live example, purpose, when-to-use, avoid-when, anatomy, props/API, states, variants, examples, do/don't, accessibility, content guidelines, composition/related, changelog, conformance dossier — with conditional rendering per component-type, a CI freshness check, per-section minimum-prose rules, and a YAML version-zero schema the practice pulls off the shelf in week one of every engagement. The accessibility section maps 1:1 to the 17 / 28 annotation contract; the conformance dossier slot aggregates into the consuming product's ACR.
- **Glossary is not a default deliverable.** Mall's Activity #25 framing — glossary as a *negotiation* between disciplines, produced in Discovery — is missing from our commercial flow.
- **Documentation-as-training-data narrative is undeveloped.** Wolosin's framing ("metadata is training data") is a strong argument for fully-described documentation. We don't yet make this argument explicitly in pitches.

## External perspectives

### Validate

- **Couldwell's "document as you go"** — directly aligns with our practice's continuous-documentation stance.
- **Couldwell's "name in design = name in code = name in docs"** — exactly the discipline our practice insists on.
- **Curtis on documentation as a major-release track** — alongside Visual Style, UI Components, Tech Architecture. Validates docs as a first-class product surface, not an afterthought.
- **Curtis's documentation substeps** (template setup, examples, design guidelines, accessibility, code API, component explorer states, code usage examples, writing/editorial, images, prototype demos) — directly maps to a usable per-component doc template.
- **Figma DS x AI (2025)** on the "explain the why," "show right and wrong examples," "include accessibility details," "maintain layer hygiene" — directly validates the practice's documentation principles.
- **Wolosin (Jun 2025)** on the four-tier metadata loop — validates the practice's `.ai.json` + registry layer; extends with explicit cross-tool linking.

### Challenge

- **Frost on "docs site as historical artifact."** Frost (2016) treated the style-guide site as the primary documentation surface. By 2025, the docs site is one of four layers (per Wolosin). Practice should not lead with "we'll build a docs site" — should lead with the layered model.
- **Curtis on "Figma is one target among many."** If the design tool is downstream of component data, then Figma documentation (component descriptions, variant labels) is also generated. Practice should treat Figma metadata as derived from the source data, not as the source itself.
- **Idean's "make tools, not rules."** Pushes against doc-heavy systems. Documentation should serve practitioners, not regulate them. The discipline test: if a section of docs isn't used by a practitioner in three months, delete it (or move to archive).
- **Figma DS x AI's "AI as documentation consumer."** Pushes the practice to write docs that are simultaneously human-readable and machine-parseable. Specifically: avoid implicit context, write declaratively, structure consistently. This changes prose style.
- **Anderson's "DS as infrastructure"** (Nov 2024) — implies documentation is the infrastructure's *contract*, not its description. Contracts are versioned, machine-readable, and enforced. Documentation that doesn't behave like a contract is informational, not infrastructural.

### Extend

- **Wolosin's 4-tier metadata loop** is a clearer pedagogical frame than the practice's current 4-layer AI stack. Worth absorbing as a teaching frame for clients.
- **Curtis's component pipeline + documentation step** as a structural artifact in the project plan — explicit doc substeps per component, gated as part of release.
- **Mall's glossary-as-Discovery** (Activity #25) — adopt as standard Discovery deliverable.
- **Figma DS x AI's prompting-conventions artifact** — increasingly, design systems should ship a "how to prompt against this system" guide for client teams using AI tools. Practice does not yet do this.
- **Mangialardi's decision logs / ADRs** in the docs repo (`docs/decisions/`) — lightweight architecture decision records. Almost no client has them. Easy adoption win.
- **Couldwell's intent-documentation discipline for color** ("why these brand colors? when use X over Y?") generalizes to every foundation: every token, every component, every pattern documents *intent*, not just appearance.
- **Wolosin's "training data" framing** strengthens the ROI argument for full documentation: even if no AI agent reads it today, the data accumulates and pays off as soon as one does.

## Tensions and open questions

1. **Human vs. machine docs as a single artifact.** Our scoping doc says docs must be "an ongoing part of the design and build process, not an afterthought" — written for humans. Our AI-Compatible doc says human-only docs are now a *failure mode*. Working synthesis: docs are produced as a parallel layer, not one or the other. Generated-from-data architecture closes the loop — author once, generate both surfaces.
2. **Tooling choice.** Storybook is the engineering-side standard. Zeroheight, Supernova, Knapsack are the design-side options. The right answer is "the docs live where they're consumed and generate from one source." Practice should articulate a recommendation framework: codebases with strong dev culture → Storybook + MDX is sufficient; designer-heavy orgs → Zeroheight/Supernova on top; high-budget enterprise → Knapsack with Code Connect.
3. **How much prose is enough.** Idean's "make tools not rules" warns against doc-heavy systems. Couldwell argues for thorough documentation including intent. Both are right at different scales. Working principle: prose only when generation can't capture it. Anything that can be derived from data should be derived; anything that's irreducibly human (intent, when-to-use, anti-patterns, do/don't with reasoning) is prose.
4. **Versioning and changelog.** SemVer is well-established. The harder question is *what* gets versioned — every component, the whole library, the tokens separately? Curtis's library tiers suggest the answer: each tier (Core foundation, Core library, Shared library, Team library) has its own version cadence. The practice's commercial standard hasn't yet articulated this clearly.
5. **AGENTS.md / CLAUDE.md as a public-facing artifact.** The instruction file is unique IP — the practice claims it; external sources don't yet name it. As a stance for clients: ship it by default, document its purpose, treat its evolution as a release event.
6. **Documentation tooling lock-in.** Zeroheight, Supernova, Knapsack are SaaS; their hosted docs become a dependency. For regulated/on-prem clients (Penpot territory), self-hosted is required. Practice should have an opinion on portability.
7. **Documentation for whom.** Practice defaults to writing for designers consuming the system. The increasingly important audiences are (a) developers consuming components, (b) AI agents consuming metadata, (c) brand/marketing teams consuming guidelines, (d) executives evaluating the system. Each needs different surfaces. The 4-layer model addresses (a) and (b); (c) and (d) are usually under-served.

## Failure modes specific to this phase

- **Documentation deferred.** "We'll write the docs once components are built." Components ship; docs lag by weeks; consumers either build wrong or wait. Both damage adoption. (Couldwell.)
- **Tooling first, content later.** Six weeks spent picking Zeroheight vs. Supernova; one week spent writing actual content. The site is empty, then half-empty, then forgotten.
- **Documentation that doesn't explain intent.** Props tables and screenshots — no when-to-use, no avoid-when, no purpose statement. Consumers (and AI) can use the components but can't *choose* between them.
- **Tokens without descriptions.** Every token is a name and a value; no `$description`. AI agents fail silently; junior designers misuse silently.
- **Implicit context.** Documentation written for the team that built the system — references shared assumptions, abbreviations, internal lore. New consumers (and AI) can't follow it.
- **Stale documentation.** Components evolve; docs don't update. Trust erodes — once consumers find one wrong page, they trust nothing on the site.
- **Generic component pages.** Every component has the same template, but the template doesn't include the things this specific component actually needs (e.g., Form components need validation guidance; Toast needs auto-dismiss behavior; Modal needs focus-trap notes).
- **Accessibility as a separate chapter.** Color contrast, keyboard navigation, ARIA documented in a "/accessibility" page nobody reads. Should live inline with each component's docs.
- **No machine-readable layer.** Beautifully written docs that no agent can parse. By 2026, this is functional debt — the system is already older than its peers.
- **Glossary missing.** Six months in, "pattern," "template," and "page" mean different things to different teams; the system is three systems and no one noticed.
- **Documentation tooling as adoption substitute.** "We bought Zeroheight, so we have a docs strategy." Tooling without staffed authoring is empty.

---

*Provenance: The dedicated UX Designer documentation-strategy role, UX Copywriter content-standards role, accessibility integrated into component docs, and Figma-style-guide-with-usage standard are internal POV from CareCentrix 2026. The reference-site IA, per-component minimum, and tooling menu are from DS-Scoping (2026) and VML library (2024–2026). The four-layer AI documentation stack (tokens-with-descriptions / `.ai.json` + registry / `AGENTS.md`+`CLAUDE.md` / Figma pipeline) is internal POV from AI-Compatible Design Systems (Feb 2025). The instruction-file layer (`AGENTS.md`/`CLAUDE.md`) is a defensible POV differentiator — external sources do not yet name it. The four-tier metadata loop (structured metadata / Figma-native / React-native / cross-link) and "metadata is training data" framing are from Diana Wolosin (Indeed, Jun 2025). "Document as you go," "name match across design+code+docs," and the IKEA-without-instructions analogy are from Andrew Couldwell (Laying the Foundations, 2019). The component-pipeline documentation step and "Documentation Platform" as a major-release track are from Nathan Curtis (Operating Design Systems, Sep 2023), treated as near-internal-tier weight. "Components as Data" generates documentation is from Curtis (Sep 2025). "Explain the why," "show right and wrong examples," "include accessibility details inline," "maintain layer hygiene," and AI-as-documentation-consumer are from Figma DS x AI (2025). "Make tools, not rules" is from Idean (Hack the Design System, 2019). The glossary-as-Discovery activity is from Mall (90 Days, 2023). Decision logs / ADRs in the docs repo are from Mangialardi (Design Systems for Developers, 2021). The "DS as infrastructure / docs as contract" reframe is from Sam Anderson (Nov 2024).*
