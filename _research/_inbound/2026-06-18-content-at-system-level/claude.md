# Content at the system level — the architecture above the per-component microcopy layer

The practice's content material has lived almost entirely at the per-component layer for the full life of this knowledge base. 04 names content guidelines as a deliverable and the UX Copywriter as a 75-hour CareCentrix line item. 29 §14 captures content per component as one of the seventeen template fields. 30 §What is generated vs. authored locates content guidance in the authored half of the pipeline. 03 names the microcopy seam at the component-library altitude. 25 / 26 / 27 cover AI-surface content at the pattern level — refusal copy, citation conventions, assistant tone — but per-pattern, not as a system-coherent surface.

What none of this material articulates: the system-level content architecture that sits *above* the per-component layer. The voice-and-tone matrix as a system artefact rather than per-component microcopy guidance. Content tokens as a tokenised primitive analogous to design tokens. i18n content as system-level scope tied back to component content guidelines. AI-surface content as a content-system layer rather than per-25/26/27-pattern guidance. The UX Copywriter role's end-to-end ownership at engagement scale, with the 04 75-hour CareCentrix number justified against engagement variables. This file closes that gap.

A note on the slot decision before anything else. The synthesis path is **deepen 04, not a new file** — committed in 09 §1.31 and confirmed for this run. Content-as-system is one or two new H2 sections in 04 alongside the existing per-component architecture, plus targeted inline additions to 23 (typography composite tokens carrying voice in their `$description`) and 13 (content-token i18n discipline tied to component content guidelines). The reason: §1.31 is bounded scope per 09; content-as-system is a layer of documentation rather than a productisable extension topic. A new file (e.g., `35-content-systems.md`) would be over-commitment to content-as-practice-IP at this stage; the practice ships content as a documentation layer rather than as an independent productisation companion alongside 30 / 32 / 33 / 34. If subsequent engagements grow the AI-surface content material to its own commercial wedge, spinning out in a future revision is open; this run commits the 04 deepen.

A note on currency before anything else. Content tooling evolves slowly compared to MCP tooling (per 34) but faster than typography tokenisation fundamentals (per 23). Specific tooling claims about content-token vendor support, ICU authoring surfaces, LLM-based content review, and AI-surface content patterns below reflect mid-2026 platform state; verify against current docs before treating any specific tool name as load-bearing in client work. The architectural shape — voice-and-tone matrix as system artefact; content tokens as primitive; i18n as cross-cutting concern; AI-surface content as system-coherent layer; the UX Copywriter role as end-to-end content owner — is more durable than the tools attached to it.

---

## 1. Why content-at-system-level is its own discipline

### Per-component content vs. system-level content

The practice's existing content material treats content primarily as a *per-component* concern. 04 §Document intent ships content guidelines per component. 29 §14 captures content guidance as one of seventeen per-component template fields. 30 §Authored locates content guidance in the human-authored half of the pipeline alongside intent prose. 03's microcopy seam treats content as a per-component output. All correct, all load-bearing. None of it answers the question that determines whether the content layer survives: *what constraint does the per-component content satisfy, and how does the constraint get authored, governed, and propagated at system scale?*

The constraint is the brand voice plus the system's tone matrix; the propagation is content tokens; the cross-cutting concern is i18n; the AI-surface application is a coherent layer; the role that owns the whole thing end-to-end is the UX Copywriter. Per-component content guidance is the *consumption* of all five; per-component guidance does not produce them. The agency that ships per-component guidance without the system-level architecture above it produces docs sites with thorough microcopy guidance and no articulation of the brand-voice constraint the per-component guidance is meant to satisfy. The microcopy fragments by release; new components author content without inheriting the system's voice; the brand voice the client paid for fragments across the system the practice built.

### The fifth productisation companion (or not)

The pattern that 30 / 32 / 33 / 34 established is the productisation-companion shape: each productises a different facet of practice IP; each commits the workstation-vs-engagement-vs-portfolio billing distinction; each ships at least one synthesis-ready operational artefact. This file lands as a 04 deepen rather than a fifth productisation companion because the content-at-system layer is not yet at the productisation altitude the four companions occupy.

The reason: content-at-system is currently a *layer of documentation* rather than a *standalone billable engagement*. The voice-and-tone matrix ships as a deliverable inside Documentation; content tokens ship as a deliverable inside Foundations; the UX Copywriter is a role inside the team table; AI-surface content sits inside 25 / 26 / 27's pattern-level guidance. None of these is currently a separable engagement the practice sells as a productised line item.

If the practice's commercial direction over the next 24–36 months grows content-system engagements as separable offerings — content audits at portfolio scale (analogous to 32's productised audit but for the content layer); content-system standups at engagement scale (analogous to 33's brand-onboarding runbook but for content); AI-surface content packages at pattern-family scale — then spinning out a fifth productisation companion (e.g., `35-content-systems.md`) becomes the right move in a future revision. For now, the layer lives in 04. The deepen captures the architecture; the productisation-companion question stays open.

### Why this matters commercially

The agency that ships per-component content guidance without the system-level architecture under-delivers in three ways. The brand voice the client paid for fragments across releases. The content-token primitives the system would otherwise expose are absent — every product authoring against the system re-implements its own error templates, empty states, CTA verb taxonomies. The UX Copywriter's hours are a line item without justification — clients who push back on the 75-hour CareCentrix number get no answer; the role is at risk of being scoped out under budget pressure.

The agency that ships content-system architecture as part of Documentation (per the 04 deepen this file commits) closes all three. The voice-and-tone matrix is shipped *and* enforced — the matrix becomes the system prompt the AI assistant consumes, the review checklist every content-PR runs, the constraint per-component microcopy is authored against. The content-token primitives ship as part of Foundations alongside design tokens; products authoring against the system pull off the shelf. The UX Copywriter's hours scale against the three drivers (component count, content-surface complexity, content-token catalogue depth) that this file articulates; the CareCentrix 75 hours becomes one point on a defensible range from ~40 to ~250 hours.

### The miscategorisation costs to name

Two miscategorisations show up in agency proposals.

**Conflating system-level content with per-component content.** The practice that treats content as docs-appendix (the "we'll write the microcopy guidelines page" shape per 04 §Failure modes) misses content-as-system-architecture entirely. Content guidance that lives only on a docs page is functional debt — nobody reads it; per-component microcopy gets authored ad-hoc; the brand voice fragments. The fix: the voice-and-tone matrix ships as a system artefact; content tokens carry the system's microcopy as a tokenised primitive; per-component guidance follows the architecture rather than leading it.

**Treating content as token primitive without articulating the voice constraint above it.** The practice that ships content tokens (Linear-style empty-states; Stripe-style error templates) without articulating the voice-and-tone matrix above the tokens ships primitives that don't compose into coherent brand voice. Linear's empty-states pattern works *because* Linear has a strong, articulated voice (encouraging-not-perky; brief; system-aware); the same primitives in a brand without an articulated voice produce inconsistent output across the catalogue. The fix: the voice-and-tone matrix at the top; tokens at the primitive layer; per-component guidance as the consumption layer; all three articulated and all three governed together.

---

## 2. Voice-and-tone systematisation as a system artefact

### The matrix as the canonical artefact

The voice-and-tone matrix is the practice's most-undersold content artefact at system altitude. Mailchimp's *Voice and Tone* (`styleguide.mailchimp.com/voice-and-tone/`) is the canonical field reference; Shopify Polaris's *Voice and tone* (`polaris.shopify.com/content/voice-and-tone`) is the design-system-native reference; the Atlassian Design System's *Writing style* and IBM Carbon's *Content guidelines* both ship a matrix-shaped artefact. The shared shape: voice (the brand's immutable character) across the top of the matrix; tone (the contextual adjustment per situation) across the side; body cells specifying how the voice expresses in each tone context.

The matrix's altitude is system-level — applied across every surface, not per-component. A confirmation toast and a destructive-action dialog share the same voice; the tone shifts contextually. The brand's three-to-five voice attributes (e.g., "warm, expert, plainspoken, direct, never condescending") are the immutable column headers; the system's content contexts (success / error / destructive / empty / loading / disabled / read-only / informational; plus AI contexts per §5) are the tone row headers; the body cells specify how voice expresses in each context.

### The matrix shape (synthesis-ready artefact)

The matrix the practice ships at engagement scale follows the shape below. Voice attributes are brand-specific; tone contexts are system-specific. Example body cells use a generic "warm + expert + plainspoken" voice for illustration; in real engagements, the body cells are authored against the client's brand.

| Tone context ↓ / Voice attribute → | Warm | Expert | Plainspoken |
|---|---|---|---|
| **Success** (confirmation, completion) | Acknowledge the user's effort; never effusive. | State what's done, not what's achieved. | Use active voice; avoid "successfully". |
| **Error** (validation, network, permission) | Calm, never blaming the user. | Name the constraint precisely; no abstractions. | Plain words; avoid jargon (`HTTP 503` → "couldn't reach the server"). |
| **Destructive** (delete confirm, irreversible) | Direct without alarm. | Name the consequence; never bury the lede. | "Delete account" not "Proceed with account removal". |
| **Empty** (first-use, no-results, filtered-out) | Inviting; never patronising. | Offer the next action; never just describe absence. | Short; no metaphors. |
| **Loading** (in-progress, streaming) | Patient; acknowledge wait. | Specific where possible ("Searching 1,200 records…"). | "Loading…" only when no specifics available. |
| **Disabled / read-only** | Neutral; explain why if non-obvious. | State the constraint, not the symptom. | Avoid passive voice. |
| **Informational** (callouts, hints) | Helpful, never lecturing. | Name what's true; avoid hedging. | Short sentences; one idea per callout. |
| **Assistant — proactive** (per §5) | Warm but bounded. | Offer one thing; never overwhelm. | No filler; no "I can help with…". |
| **Assistant — refusing** (per §5) | Acknowledge the request. | Name the constraint; offer the alternative. | No apologetic loops. |

The matrix is the artefact; the body cells are the system's voice expressing in each context. The matrix ships as part of the content-system deliverable; the per-component content guidance per 29 §14 references the matrix's body cells rather than re-authoring them.

### Voice-and-tone as the system prompt for AI surfaces

The matrix is only useful if it's enforceable. The cleanest enforcement at scale: the matrix becomes the system prompt the AI assistant consumes. Per 25 §The architecture beneath; per 27's structured-output scaffolding — the assistant's outputs are constrained by the system prompt; the system prompt encodes the matrix's voice attributes and the relevant tone-context body cells; the assistant's outputs inherit the brand voice without per-output authoring.

This is the most aggressive enforcement pattern and the one the practice should default to for AI-surface-bearing engagements. The matrix doesn't sit on a docs page nobody reads; the matrix sits in the assistant's runtime prompt, applied to every output. Voice fragmentation across AI surfaces becomes structurally prevented.

For non-AI surfaces, three lighter-weight enforcement disciplines work:

- **Pre-merge content review.** Every PR with content changes runs the matrix's three or four voice questions before merge. The reviewer (typically the UX Copywriter per §6) confirms the new content satisfies the matrix's voice attributes for the relevant tone context. The discipline catches drift before it lands; the cost is roughly 5 minutes per content-bearing PR.
- **Quarterly voice audit.** Per 32 §5's continuous-audit framing applied to content. The UX Copywriter samples 30–50 content surfaces across the system; the audit produces a drift report; the report becomes the next quarter's content-evolution priority list. The pattern that fails: voice audits that produce reports nobody reads because the audit isn't tied to a remediation cadence.
- **Token-mediated authoring.** Per §3 — when the system ships content tokens, components consuming the tokens inherit the matrix's voice rather than authoring per-component. Token-mediated authoring is the most durable enforcement because it removes the per-component authoring step entirely; the matrix's voice expresses *through the token catalogue*, not through ad-hoc per-component microcopy.

### How voice connects to typography (the 23 link)

Per 23 — typography is voice in type. The brand-voice-as-immutable-system-constraint framing in 23 §The shape of a typography token set covers the type-side voice; this section covers the content-side voice; both express the same brand constraint at the system level. The matrix lives across both surfaces — the type system's connotation vocabulary (per 23) and the content system's voice attributes (per this section) are coherent because both express the same brand voice.

The link is operational at the typography composite-token layer per 23 §DTCG composite typography tokens. The composite typography token's `$description` field carries the voice intent — the practice's tokens-with-descriptions discipline applied to the content / voice axis. A composite typography token for `text/body/error` carries:

```json
{
  "$type": "typography",
  "$value": { "fontFamily": "{family.body}", "fontSize": "{size.body}", "lineHeight": "{lh.body}", "fontWeight": "{weight.regular}" },
  "$description": "Used in error states. Voice: calm, never blaming. Tone: direct without alarm. Per voice-and-tone matrix §Error."
}
```

This is the inline addition this file's run lands in 23 — extending 23's brand-voice framing into the tokens-with-descriptions discipline at the typography / content boundary. The token is design-side; the description carries the content-side constraint; both flow from the same matrix.

### The multi-brand voice question (the 24 / 33 link)

Per 24 / 33 — multi-brand and white-label-for-resellers systems carry brand voice as a per-brand axis. Each brand's voice-and-tone matrix is one of the per-reseller assets the engine generates per 33 §7. The Theme Schema's voice-tone parameter (per 33's brand-voice tone parameter for assistant copy at §3 / §5) is the for-resellers system's voice-axis input; the engine derives the per-brand content tokens from the voice parameter the way it derives the color tokens from the primary-color primitive.

The shape this implies: the for-resellers Theme Schema names a voice-tone primitive alongside the five visual primitives per 33 §3 (primary color + neutral hue + typeface + radius + density). The voice-tone primitive is a structured input — three to five voice attributes named explicitly; per-tone-context guidance authored at minimum for success / error / destructive / empty (the load-bearing tone contexts). The engine generates the per-brand content tokens (per §3 below) by substituting the per-brand voice attributes into the system's content-token templates.

This is the multi-brand application of the matrix discipline. The practice's bet: white-label-for-resellers engagements that ship a content-system layer alongside the visual system are differentiated from those that ship visual-only platforms. The voice-axis Theme Schema input is the content-system's leverage at portfolio scale.

### The practitioner-side gap

The matrix is well-known as a surface but rarely shipped as a *system artefact* in DS engagements. Most engagements ship one of two failure modes:

- **Per-component content guidance without the matrix.** The CareCentrix-shape failure: each component's docs page has a Content guidelines section; the sections are authored per component without inheriting from a shared matrix; the brand voice fragments across components by release.
- **A matrix without enforcement.** The Mailchimp-via-influence shape: the practice ships a matrix as a docs-page deliverable; the matrix isn't tied to per-component review, AI-surface system prompts, or token-mediated authoring; the matrix becomes a static document; per-component content drift continues.

The practice's discipline closes both. The matrix ships as a system artefact *and* enforces through one or more of the three enforcement disciplines (AI system prompt; pre-merge review; token-mediated authoring). The enforcement is what makes the matrix system-shaped rather than docs-appendix-shaped.

---

## 3. Content tokens / writing-tokens as a primitive

### The case for content tokens

The field is starting to ship content tokens, mostly without naming them as such. The pattern is visible in:

- **Linear's empty-states.** Each empty state across Linear's product surface carries a consistent encouraging-not-perky voice via what are effectively templated tokens — first-use ("Welcome to Cycles. Set your first cycle to start tracking your team's velocity."), no-results ("Nothing matches your filter. Try removing some constraints."), filtered-out ("All issues are filtered out. Clear filters to see them."). The voice is consistent because the primitives are shared.
- **Stripe's error-message taxonomy.** Errors carry codes (`card_declined`, `insufficient_funds`, `expired_card`); the codes map to user-facing message templates; the templates carry Stripe's voice (clear, never blaming the user, always offering the next action). The taxonomy is shipped as part of the Stripe API documentation and consumed by every product integrating Stripe.
- **Polaris's content-pattern primitives.** Polaris ships pattern tokens for CTAs, error microcopy, loading messages — each with usage rules and parameter slots. The patterns are documented at the system level; per-product surfaces consume them.
- **GOV.UK's component content patterns.** GOV.UK Design System ships content patterns for date input, names, addresses, error messages — each pattern carries the GOV.UK voice (concise, plain English, accessible reading level) as a tokenised template.
- **IBM Carbon's content guidance.** Carbon ships content-pattern guidance for empty states, error messages, notifications — less explicitly tokenised than Linear or Stripe but moving in the same direction.

The shared shape: content as a *named, reusable, composable resource* analogous to design tokens — primitives the consumer pulls off the shelf rather than authoring per-component. The practice's case for shipping content tokens explicitly: every system already ships these implicitly through pattern guidance; making them explicit (named, versioned, governed, AI-readable) converts implicit IP into an operational primitive.

### What's tokenisable vs. what isn't

The line between content-as-token and content-as-prose is the same line as design-tokens-vs-component-styles: tokens carry *templated, system-level* content; prose carries *judgment*.

**Tokenisable.** CTA verb taxonomies (the system's verbs — "Save", "Continue", "Submit", "Cancel", "Discard", "Discard changes" — with usage rules and tone-context mappings); error message templates (per error category — network / validation / permission / destructive-confirm); empty-state copy patterns (per empty-state category — first-use / no-results / filtered-out / system-empty / waiting-for-input); loading-state microcopy ("Loading…" / "Searching…" / "Saving…" / "Generating…" / "Almost done…"); confirmation patterns (success messages; toast copy; destructive-action confirmation lines); disabled-state explanations ("This action requires admin permissions."); loading skeletons' ARIA-live announcements; AI-surface refusal templates and disclosure boilerplate per §5.

**Not tokenisable.** Long-form prose; marketing copy; brand-narrative content; per-component intent prose (the "when-to-use" and "avoid-when" guidance is per-component judgment, not a token); authored content in product surfaces (blog posts; help documentation; legal text — these live in CMS per §4's content-tokens-vs-CMS line).

The discipline: tokens carry templated content with parameterised slots; prose carries judgment. The line is testable — if the content varies meaningfully per-instance based on the local situation (the specific error code; the specific empty-state context; the specific destructive-action target), it's tokenisable with parameter slots. If the content varies meaningfully per-instance based on human judgment about the situation (the specific framing for an error; the specific tone for an explanation), it's prose.

### The DTCG-shaped schema for content tokens (synthesis-ready artefact)

DTCG's 2025.10 Format Module covers design tokens (color, spacing, typography, motion, dimension) but *does not cover content tokens*. As of mid-2026, the field has no canonical content-token spec. The closest precedent is i18n message catalogues (ICU MessageFormat per 13) — keys map to templates with parameter slots; locale variants per key; pluralisation rules.

The practice can lead by shipping a content-token schema shape as a defensible POV. The shape, sketched:

```json
{
  "$type": "content",
  "$value": "Couldn't reach {service}. Try again or check your connection.",
  "$description": "Used in network-error states. Voice: calm, never blaming the user. Tone: direct, offers next action. Per voice-and-tone matrix §Error.",
  "$extensions": {
    "vendor": {
      "parameters": {
        "service": { "type": "string", "description": "The service that couldn't be reached, lowercase noun phrase." }
      },
      "locale": {
        "default": "en-US",
        "icu": true
      },
      "tone": "error",
      "ai-readable": true
    }
  }
}
```

The shape's load-bearing properties:

- **`$value` is the source-locale ICU template.** ICU-shaped from authoring time; pluralisation, gender, ordinal-aware via ICU selectors.
- **`$description` carries the voice intent.** Per the matrix's relevant tone-context body cell; the description is the contract between the matrix and the token; reviews against the matrix happen here.
- **`$extensions.<vendor>.parameters`** declares the slot shape. Each parameter has type and usage description; parameters are validated at runtime; the AI client (per `.ai.json` integration) reads the parameter shape and respects it during composition.
- **`$extensions.<vendor>.locale`** declares the i18n axis. Default locale; ICU-conformant flag; per-locale variants live in the localisation catalogue (per §4) keyed by the token's name.
- **`$extensions.<vendor>.tone`** ties the token back to the voice-and-tone matrix per §2 — the tone-context name is the body-cell key the description references.
- **`$extensions.<vendor>.ai-readable`** is the practice's `.ai.json` integration flag per 30 — when true, the token is consumed by AI clients via the per-component MCP surface; when false, the token is human-only.

This schema shape is the practice's defensible content-token POV. As of mid-2026, no DTCG content-token spec exists; the practice's discipline ships this shape as a custom DTCG `$extensions` extension; if and when the DTCG community ratifies a content-token spec, the practice migrates. The bet: a DTCG content-token spec lands in 2026–2027 alongside the AI-readiness commercial pressure; the practice's bridge investment migrates without significant rework.

### Cross-platform localisation angle

Content tokens carry localisation as a cross-cutting concern. The token's `$value` is the source-locale template; per-locale variants live in the i18n catalogue (per §4) keyed by the token's name; the runtime resolves per the user's locale via ICU.

Without content tokens, every component carries its own i18n integration — the component imports message catalogues directly, manages locale state, formats strings inline. With content tokens, the integration happens at the token layer — components consume the token's resolved value; the token resolves locale-aware via the runtime; the component is locale-agnostic.

This is the shape ICU-aware modern frameworks (FormatJS, LinguiJS, react-intl) already encourage at the message-catalogue layer. The content-token shape this section commits is the DTCG-aligned version of the same pattern, with the addition of voice-intent metadata (`$description`), tone-context binding (`$extensions.<vendor>.tone`), and AI-readability (`$extensions.<vendor>.ai-readable`).

### The CMS-vs-content-tokens authoring boundary

Where content lives — in the DS's content tokens or in the CMS's content models — is a procurement-grade decision. The practice's working position: tokens for *templated, system-level* content; CMS for *editorial, product-specific* content. The line is similar to design tokens vs. component-specific styles: tokens for system primitives; component-specific authoring for per-instance overrides.

Examples that fall on each side:

- **Tokens.** "Save" / "Cancel" / "Discard changes" CTA verbs (system-level, every product uses them). Network-error templates. Empty-state copy patterns. AI-surface refusal templates. Disclosure boilerplate.
- **CMS.** Help documentation. Marketing copy. Blog posts. Legal text (terms / privacy). Per-product feature names. Per-product onboarding copy (where the brand has multiple products with different onboarding stories).

The boundary surfaces in §4 (i18n) and again in §1.32's forthcoming CMS work. The practice's discipline: name the boundary at scoping; the content-token catalogue carries system-level content; the CMS carries product-specific content; the two coexist and reference each other (the CMS content can reference content-token templates for consistent microcopy; the content-tokens reference CMS-managed content via parameter slots when needed).

### Tooling reality and gaps

As of mid-2026, the content-token tooling landscape is thin.

- **Tokens Studio** doesn't ship content tokens as a first-class object. The practice's bridge investment: custom Tokens Studio metadata via `$extensions` carries content-token data alongside design tokens; Tokens Studio's plugin surface consumes the metadata via custom plugins.
- **Style Dictionary's transforms** don't cover content tokens natively. Custom transforms required to emit per-platform content-token output (web JSON, iOS Swift, Android Kotlin); the practice's bridge investment is roughly 8–16 hours of custom transform work per platform.
- **Specify, Knapsack, Supernova, Backlight** don't ship content tokens as a first-class object. Their token catalogues are design-token-shaped; content tokens are absent or implemented as ad-hoc string fields without voice / tone / parameter / i18n metadata.
- **ICU authoring tooling is thin.** Most CMSes don't author ICU; most translation vendors don't author ICU; most DS documentation doesn't author ICU. The practitioner-side gap: senior practitioners who want ICU-shaped content tokens write them by hand in the source-of-truth repo, then ship them through translation vendors that may not preserve ICU shape correctly. Lokalise, Crowdin, and Phrase support ICU; Smartling and TransPerfect have varying support; verify per vendor before treating as fixed.
- **LLM-based content review tooling is emerging.** LLMs can read the matrix per §2 and review content-PR diffs against it — automated voice / tone consistency checking. As of mid-2026, this is custom work (the practice's senior practitioners script it via Claude API; no major DS-tooling vendor ships LLM content review natively); the practice's bet is that this lands in 2026–2027.

The practice's bet on the broader landscape: native vendor support for content tokens lands in 2026–2027 alongside the AI-readiness commercial pressure; practitioners shipping content tokens today are wrapping ICU message catalogues with DTCG-shaped metadata as a bridge investment.

---

## 4. i18n content depth at the system level

### The case for i18n content as system-architectural concern

Per 13 — the practice covers RTL and locale shape at the architectural level (logical properties, text expansion, multi-script typography, locale-aware tokens, RTL component mirroring). What's not covered: how component content guidelines tie back to i18n tooling; how content tokens (per §3) carry locale variants; how the UX Copywriter role coordinates with localisation vendors; how voice-and-tone (per §2) handles per-locale tonal adjustments.

13 is the architectural foundation for i18n; this section adds the content layer above it. The link this run lands as an inline addition to 13: a pointer to 04's new system-level content section as the content-token authoring layer; the practice's i18n content discipline ties back to the content-token catalogue.

### ICU MessageFormat at system scale

Per 13 — ICU covers pluralisation, gender, ordinals, locale-aware select. At system scale, ICU integrates with content tokens (per §3) — the token contains an ICU template; the runtime resolves via ICU per the user's locale. The system ships ICU-shaped templates, not hand-authored per-locale strings.

Most engagements still ship hand-authored per-locale strings because the tooling for ICU authoring is thin. The practice's discipline at engagement scale: author ICU-shaped templates from day one of the content-token catalogue; localisation vendors translate the ICU templates per locale (preserving ICU shape); the runtime resolves per locale. This is the shape modern frameworks (FormatJS, LinguiJS, react-intl) already encourage; the content-token catalogue is the system-level wrapper that makes the discipline visible across engagements.

### Pluralisation at system scale

The English speaker's mental model — one cat / two cats — doesn't generalise. Russian has three plural categories (1 / few / many); Arabic has six (zero / one / two / few / many / other); Welsh has six; Polish has four; Japanese and Chinese have one (no inflection by count); Slovenian has four. ICU expresses pluralisation via the `plural` selector with named cases (`one`, `few`, `many`, `other`).

A content-token carrying a pluralisable template:

```json
{
  "$type": "content",
  "$value": "{count, plural, one {# item selected} other {# items selected}}",
  "$description": "Used in selection-state announcements. Voice: matter-of-fact. Tone: informational.",
  "$extensions": {
    "vendor": {
      "parameters": {
        "count": { "type": "number", "description": "The selection count, must be non-negative integer." }
      },
      "locale": { "default": "en-US", "icu": true },
      "tone": "informational"
    }
  }
}
```

Per-locale variants in the localisation catalogue carry locale-specific plural categories. Russian has three cases; the per-locale variant carries `{count, plural, one {…} few {…} many {…} other {…}}`. Arabic has six. The catalogue carries the variants; the runtime resolves.

Hand-authored per-locale strings break here — the English authoring "one item / N items" doesn't translate to Russian's three categories without re-authoring. Content tokens with ICU templates handle this natively.

### Gendered language

ICU's `select` selector handles gendered variants (male / female / non-binary; or per-locale gender systems). Per locale, the gendered variants differ — Spanish has masculine / feminine; German has three genders; Finnish has none; Hebrew has masculine / feminine in second-person address forms. Content tokens at system scale declare the gendered variant axis; per-locale catalogues carry the variants.

The practitioner-side discipline: gendered language is a system-level concern in locales where it matters; the content-token catalogue declares the gendered variant axis as part of the token shape; the localisation vendor produces the per-locale variants; the runtime resolves per the user's gender preference (or the application's known data about the user). The pattern that fails: gendered language is treated as per-component; per-component microcopy gets authored without gender-axis support; the application produces grammatically incorrect output in gendered locales.

### RTL content ordering

Per 13 — logical properties at the layout level. At the content level: bidirectional content embedding (Arabic-with-English-loanwords; Hebrew-with-numbers; mixed-LTR-and-RTL within a single string); the Unicode `<bdi>` element (bidirectional isolation); the `<span dir="rtl">` directional override; the `unicode-bidi` CSS property's role.

Content tokens at system scale carry directional metadata — the token's primary direction; the embedded-content directional handling. A content token in an RTL locale variant may be authored RTL but contain LTR substrings (English brand names, numbers, technical terms); the token's metadata declares how the RTL context handles the embedded LTR substrings. The runtime renders with the appropriate `dir` attributes and Unicode bidirectional isolates.

### Localisation governance

The UX Copywriter (per §6) coordinates with localisation vendors on per-locale content. The system's content tokens are the source-of-truth; the localisation vendor consumes the source tokens and produces per-locale variants; the variants flow back into the content-token catalogue. Without content tokens, localisation is per-component string-by-string; with content tokens, localisation is catalogue-shaped.

The vendor landscape: TransPerfect, Lionbridge (the large translation vendors); Smartling, Lokalise, Crowdin, Phrase, Memsource (the modern localisation platforms). The platform vendors integrate with translation vendors at varying depths; the content-token catalogue is portable across platform vendors via standard formats (JSON, XLIFF, TMX, Gettext); the practice's discipline is to keep the catalogue in a portable format and treat the platform vendor as a workflow tool rather than a lock-in.

### The line that connects to §1.32 (CMS platforms — forthcoming)

Localised editorial content lives in the CMS; localised system content lives in the content-token catalogue. The boundary is the same as the content-token-vs-CMS line per §3 — system-level vs. product-specific.

The CMS-vs-content-tokens line surfaces in 09 §1.32 (CMS platforms — modern composable / headless coverage) as one of the named sub-gaps: the CMS-vs-DS authoring boundary. This section foreshadows §1.32 — the boundary is articulable at the content layer; §1.32 will deepen 10 with the broader CMS architectural framing alongside the headless / composable / MCP-for-CMS-components material. The link this section lands: when §1.32 deepens 10, it picks up the content-token-vs-CMS-managed-content line from this section and applies it across the broader CMS surface (Sitecore, Contentful, Sanity, Strapi, Storyblok).

---

## 5. Content for AI surfaces as a content-system layer

### The case for AI-surface content as system architecture

Per 25 / 26 / 27 — the practice ships AI-aware patterns (chat, streaming, citation, refusal, tool-call) and adaptive interfaces (Sentient Triangle scaffold, fourteen patterns, five-rung spectrum). The content half of these patterns — assistant tone, refusal copy patterns, disclosure boilerplate, citation format conventions, error / fallback / clarification / tool-call-confirm copy — is currently per-pattern in 25 / 26 / 27 but not articulated as a content-system layer.

The voice-and-tone matrix per §2 + the content tokens per §3 + the UX Copywriter role per §6 collectively own the AI-surface content layer at system scale. This section pulls the content material out of 25 / 26 / 27 into the content-system altitude.

### Assistant tone as voice-and-tone applied to AI surfaces

The brand's voice (per §2) constrains the assistant's outputs; the tone matrix's contexts include AI-surface contexts (assistant-proactive / assistant-reactive / assistant-uncertain / assistant-refusing / assistant-clarifying / assistant-handing-off-to-human). The matrix's body cells for AI contexts specify how the brand voice expresses in each AI context — and become the system prompt the assistant consumes (per 25 §The architecture beneath; per 27's structured-output scaffolding).

The AI rows of the matrix per §2 illustrate the shape: assistant-proactive carries "warm but bounded; offer one thing; never overwhelm"; assistant-refusing carries "acknowledge the request; name the constraint; offer the alternative; no apologetic loops". The assistant's system prompt encodes the voice attributes plus the relevant AI tone-context body cells; the assistant's outputs inherit the brand voice.

This is the highest-leverage AI-surface enforcement pattern. The matrix isn't a docs page; the matrix is in the assistant's runtime prompt; voice consistency across AI surfaces becomes structurally guaranteed.

### Refusal copy patterns

Per 25 §Refusal patterns — the assistant refuses (out-of-scope; safety; capability; privacy). Each refusal category has a content-pattern shape — the refusal acknowledges the request, names the constraint, offers an alternative path. Without content tokens, every product surface re-authors refusal copy and the brand voice fragments.

Content tokens at system level ship the refusal templates per refusal category. The shape:

```json
{
  "$type": "content",
  "$value": "I can't {action} — {reason}. {alternative}",
  "$description": "Used in assistant refusal states. Voice: acknowledges request, names constraint, offers alternative. Per voice-and-tone matrix §Assistant — refusing.",
  "$extensions": {
    "vendor": {
      "parameters": {
        "action": { "type": "string", "description": "The action the user requested, in lowercase verb phrase." },
        "reason": { "type": "string", "description": "The constraint that prevents the action, plain language." },
        "alternative": { "type": "string", "description": "The alternative path, starting with an action verb if possible." }
      },
      "tone": "assistant-refusing",
      "ai-readable": true
    }
  }
}
```

Per refusal category, the template's voice constraint is the same; the parameter slots fill per-instance. The brand's voice is consistent across refusal types because the template carries the matrix's voice constraint; products consume the template rather than authoring per-product refusal copy.

### Disclosure boilerplate

Per 25 §Disclosure (EU AI Act Article 50 framing). Disclosure copy is system-level — the system ships the disclosure template; products consume the template; the legal team reviews the template once not per-product. Content tokens at system level ship the disclosure templates.

The practice's discipline: disclosure is a system-level content primitive, not per-product authoring. The legal-review cost is paid once at the system level; per-product disclosure is the template + per-product parameter values; the brand's voice expresses through the template; the legal constraint expresses through the template's structure. Disclosure that drifts per-product is a compliance risk under EU AI Act Article 50; tokenised disclosure is structurally enforced.

### Citation format conventions

Per 25 §Citation patterns — the assistant cites sources. Citation format (inline-link / footnote / sidebar / collapsible) is per-pattern; citation copy conventions (how to introduce a citation; how to handle partial-confidence citations; how to handle missing-source cases) is system-level. Content tokens carry the citation copy templates.

Three citation tone-contexts that surface as token-shapes:

- **Confident citation.** "{source} states {claim}." Voice: direct, attributing.
- **Partial-confidence citation.** "{source} suggests {claim}, though context may matter." Voice: appropriately hedged.
- **Missing-source case.** "I don't have a source for this; treat as opinion." Voice: honest, not defensive.

The templates ship in the content-token catalogue; the assistant's system prompt references them; the assistant's outputs inherit the citation conventions.

### Streaming / partial-output / interruption content

Per 25 — streaming responses produce partial outputs; users may interrupt; the system shows a partial state then a final state. The content for streaming UI (the "thinking…" / "generating…" / "almost done…" microcopy; the interruption confirmation copy; the resume-vs-restart prompt) is system-level. Content tokens carry the streaming-state templates.

The streaming-state microcopy is a token family; the family's body cells per the matrix carry the brand voice in streaming contexts — calm, never anxious; specific where possible; never apologetic. Components consuming the streaming-state primitives (chat surfaces, search, generation flows) inherit the family's voice constraint.

### Tool-call confirmation

Per 25 §Tool-call patterns + 27's structured output rendering — the assistant proposes a tool call; the user confirms. The confirmation copy ("This will send an email to {recipient}. Continue?") is system-shaped; the tool-call's specific parameters fill the parameter slots. Content tokens carry the confirmation templates.

The confirmation copy's voice constraint is critical — the matrix's destructive-action body cell applies (direct without alarm; name the consequence; never bury the lede). The token-mediated authoring ensures every tool-call confirmation carries the same voice constraint; per-tool-call authoring fragments the brand voice.

### Adaptive-UI content (the variability-by-design problem applied to content)

Per 26 / 27 — adaptive interfaces compose components per render via LLM. The components' content (the microcopy in each rendered component; the copy in adaptive empty-states / loading-states / refusal-states) is system-shaped — the LLM composes from the system's content tokens, not from ad-hoc strings.

The variability-by-design problem (per 26's residual gap on purpose-built authoring tooling for variability) applies to content as well as visual: the designer specifies a *space* of possible content outputs and reviews the *distribution* of what the LLM produces. Content tokens are the boundary the variability operates within — the LLM composes within the token catalogue; the token catalogue's voice constraint expresses through every composition; the variability is bounded by the matrix.

This is the practice's most-aggressive AI-surface content discipline. The LLM doesn't author free-form content; the LLM composes from the token catalogue; the token catalogue carries the matrix's voice constraint; the matrix is enforced at composition time. The pattern that fails: the LLM composes free-form content that drifts from the matrix; the brand voice fragments; per-render variance is unbounded. The pattern that works: the LLM composes from tokens; the variance is bounded; the matrix is structurally enforced.

---

## 6. The UX Copywriter role at engagement scale

### The case for the UX Copywriter as a system-level role

Per 04 §Our POV — the CareCentrix 2026 commercial standard names a UX Copywriter at 75 fixed hours integrated into component documentation. The role is named but not justified — the 75 hours is a CareCentrix-specific number; what justifies more or fewer hours; what the role owns end-to-end at system scale; how the role hands off to client product teams; how content guidelines get maintained after handoff — none of this is articulated.

The UX Copywriter is the practice's content-side analogue to the design technologist (per 00e) — a hybrid role that crosses content / design / engineering boundaries. The role's hiring signal is writing fluency + design-system literacy + i18n awareness + AI-surface fluency; the role's seniority calibration is similar to the design technologist's (typically senior or lead level for engagements with substantial content surface).

### What the role owns end-to-end at system scale

Four ownership clusters:

**Content architecture.** The voice-and-tone matrix per §2; the content-token catalogue per §3; the i18n content strategy per §4; the AI-surface content layer per §5. The role authors the matrix at engagement Discovery; ships the content-token catalogue alongside Foundations; coordinates the i18n strategy with the localisation vendor; ships the AI-surface content layer alongside whichever 25 / 26 / 27 patterns the engagement scopes.

**Content production.** The system-level content (matrix, tokens, templates, AI-surface copy) per 04 §Document intent. The role authors the system-level content directly; per-component content guidance per 29 §14 references the system-level content rather than re-authoring.

**Content review.** Per-component content guidance review; pre-merge PR review for content changes; release-readiness content audit per §2's enforcement disciplines. The role is the gating reviewer for content-bearing changes; the review cost is roughly 5 minutes per content-bearing PR, scaling with PR volume.

**Cross-functional coordination.** Localisation vendor coordination per §4 (typically 4–8 hours per locale beyond source); legal review for disclosure copy per §5 (typically 8–16 hours per major release for legal-review cycles); brand-team review for voice-and-tone matrix evolution (typically 4–8 hours per quarter for matrix-evolution coordination); AI-surface tone-prompt coordination (the matrix becomes the system prompt; the role coordinates with the engineering team that ships the prompt).

### The hour-justification model

The CareCentrix 75 hours is a Pattern 2 (Figma-only handoff per 00d) standard-complexity number. At engagement scale, the role's hours scale with three drivers:

- **Component count.** ~0.5–1 hour per component for the per-component content guidance per 29 §14 — primarily review and matrix-binding rather than authoring (because the matrix and content tokens carry most of the per-component work).
- **Content-surface complexity.** AI surfaces add ~20–40 hours per AI pattern family — chat / streaming / refusal / citation / tool-call. Multi-locale adds ~30–60 hours per locale beyond the source — localisation vendor coordination, ICU template authoring, per-locale tone review.
- **Content-token catalogue depth.** A deep catalogue with CTA / error / empty-state / loading / confirmation / disclosure / citation / refusal token families adds ~40–80 hours; a thin catalogue with errors only adds ~15–25 hours.

The CareCentrix 75 hours fits roughly **20–25 components, English-only, no AI surfaces, a thin token catalogue** — a Pattern 2 standard-complexity engagement. Other points on the range:

- **Pattern 2, 30 components, English-only, no AI surfaces, thin token catalogue.** ~80–100 hours.
- **Pattern 2, 30 components, three locales (English + two others), no AI surfaces, standard token catalogue.** ~140–180 hours.
- **Pattern 6 (white-label per 33), 50 components, English-only at launch, AI surfaces (chat + refusal + citation), deep token catalogue.** ~180–250 hours, plus ongoing engagement-scale Run-phase retainer for matrix evolution and per-reseller voice coordination.
- **Pattern 1 (Product-support component build per 00d), 15 components, English-only, no AI surfaces, error tokens only.** ~40–60 hours.

The practice's discipline: scope the role against the three drivers; quote a range (40–250 hours per Build) with the driver mix making the case for the chosen point in the range. The CareCentrix 75-hour line item becomes a defensible point on a scaled range rather than a number quoted without justification.

### When a system needs the role at all

Below ~10 components, the role doesn't pay back — the content guidance is thin enough for the senior visual designer or UX designer to author directly. Above ~10 components, content drift becomes visible by release; above ~20 components, content drift becomes a failure mode (per 04 §Stale documentation). At ~20+ components with multi-locale or AI-surface scope, the role's payback is strongest; below, it's optional.

The minimum viable scope for the role's inclusion: **~10 components plus any of multi-locale, AI surfaces, or recurring content-system maintenance (Run-phase retainer)**. At less than that, content can be absorbed by the senior visual designer or UX designer's hours; at more than that, content drift without the dedicated role becomes a release-cost.

### Handoff to client product teams

The role hands off three things at engagement end:

- **The voice-and-tone matrix as a governed artefact.** The client's content team owns evolution; the practice provides the matrix shape and the per-context body cells; the client extends per their content surface's needs over time.
- **The content-token catalogue as a maintained primitive.** The client's engineering team consumes; the client's content team authors token additions; the practice provides the schema shape (per §3), the initial catalogue, and the token-evolution discipline (semver-for-content-tokens analogous to 24's semver-for-design-tokens).
- **The per-component content guidance per 29 §14.** Consumed by the client's product teams; the practice provides the initial per-component guidance and the matrix-binding discipline; the client maintains as components evolve.

The handoff is incomplete without the governance contract — who reviews matrix changes; who approves token additions; who coordinates localisation. This is content's analogue to the 07 contribution-model handoff at the component layer. The practice's discipline: ship the governance contract alongside the content-system handoff; without it, the system the client paid for decays as soon as the practice leaves.

### The Run-phase parallel

Per 33 §5 — white-label-for-resellers ships a run-phase retainer with three SLAs (brand-onboarding / engine-availability / schema-coordination). Bespoke engagements with a content-system handoff can ship an analogous content-retainer with three commitments:

- **Matrix-evolution coordination.** Quarterly matrix review; new tone contexts added as the client's product surfaces grow; voice attributes maintained across the matrix's evolution.
- **Token-addition review.** New content tokens reviewed against the matrix; schema-shape conformance; voice / tone metadata complete; AI-readability flag set correctly.
- **Localisation coordination.** Per-locale variant review with the localisation vendor; ICU shape preserved; per-locale tone review for tonal-adjustment locales (Japanese keigo, German Sie/du, etc.).

The retainer follows the same shape as 33 §5 but applied to the content layer — three discrete commitments, each with an explicit SLA, each with an hour estimate, all priced as a recurring monthly retainer (typically 8–24 hours/month depending on content-surface complexity). Content is one of the natural Run-phase retainer surfaces the practice has not yet articulated; this section adds it to the run-phase pricing landscape that 00d's run-phase pricing gap and 33 §5's for-resellers retainer also occupy.

### Connection to 00e team-and-discipline

The UX Copywriter is the content-side analogue to 00e's design-technologist archetype — a hybrid role that crosses content / design / engineering boundaries. The role's hiring signal isn't yet articulated in 00e; this section surfaces it as a 00e residual.

The hiring signal: writing fluency at senior level (the role authors the system's voice; weak writing produces a weak system); design-system literacy (the role consumes 22 / 23 / 24's token discipline and produces a content-token catalogue against it); i18n awareness (the role coordinates with localisation vendors and authors ICU-shaped templates); AI-surface fluency (the role authors the system prompt's voice constraint and the AI-surface content templates per §5). The role doesn't need to be a senior software engineer; the role does need to operate fluently with engineering counterparts on token-catalogue mechanics and AI system-prompt coordination.

The 00e residual flag: the role's hiring signal, the role's seniority calibration, and the role's career path within the practice are open questions worth picking up in a future 00e revision. This section lands the role's *engagement-scale* discipline; the *practice-scale* discipline (how the practice hires, levels, and progresses Copywriters across engagements) belongs in 00e.

---

## 7. Integration — deepen 04, plus targeted additions to 23 and 13

### The slot decision committed in this run

The synthesis path is **deepen 04, not a new file.** The reason: §1.31 is bounded scope per 09; the content-at-system layer is one or two H2 sections in 04 alongside the existing 04 architecture, plus targeted inline additions to 23 and 13. A new file (e.g., `35-content-systems.md`) is over-commitment to content-as-practice-IP at this stage; the practice ships content as a layer of documentation rather than as an independent productisation companion.

The fifth-productisation-companion question stays open. If subsequent engagements grow content-system engagements as separable offerings (content audits at portfolio scale; content-system standups at engagement scale; AI-surface content packages at pattern-family scale), spinning out in a future revision is the right move. For now, the architecture lives in 04.

### What lands in 04

Two new H2 sections in 04, sitting between 04's existing Cluster-6 (Documentation as sales surface, lines 83–95) and the Our-POV section (line 96):

**Content as a system layer.** Covers §§1–5 above — the case for content-at-system as a discipline; the voice-and-tone matrix as system artefact (with the matrix shape table from §2); content tokens as a primitive (with the content-token DTCG-shaped schema from §3); i18n content depth at system scale (with the ICU-and-content-tokens framing from §4); AI-surface content as a content-system layer (with the per-pattern token shapes from §5). The section is the load-bearing addition; it carries the architecture above per-component content guidance.

**The UX Copywriter role at engagement scale.** Covers §6 — what the role owns end-to-end (four ownership clusters); the hour-justification model with the three drivers and four illustrative engagement points; when the system needs the role; the handoff and the Run-phase retainer parallel; the 00e residual flag for the role's practice-scale hiring discipline.

The two sections together add roughly 2,500–3,500 words to 04, taking it from ~3,500 words to ~6,000–7,000 words. Manageable; sits under the 09 §1.31 "bounded scope" framing.

### What lands in 23

One inline addition to 23 §The shape of a typography token set or §DTCG composite typography tokens (precise placement to be decided at integration time): the typography composite token's `$description` field carries voice intent — extending 23's brand-voice-as-system-constraint discipline into a tokens-with-descriptions discipline at the typography / content boundary.

The addition's body, sketched:

> *Composite typography tokens carry voice intent in their `$description` field. The typography token for `text/body/error` ships the type spec in `$value` (font family, size, line height, weight) and the voice constraint in `$description` ("Used in error states. Voice: calm, never blaming. Tone: direct without alarm. Per voice-and-tone matrix §Error."). The description binds the typography-side voice (per 23's brand-voice-as-immutable-system-constraint framing) to the content-side voice (per 04's voice-and-tone matrix at system level). Both flow from the same matrix; the typography token is the design-side expression, the content token is the content-side expression, both share the same voice intent in their descriptions. (See 04 §Content as a system layer.)*

### What lands in 13

One inline addition to 13's existing message-format coverage: a pointer to 04's new system-level content section as the content-token authoring layer.

The addition's body, sketched:

> *ICU-shaped messages live in the system's content-token catalogue per 04 §Content as a system layer — the content tokens carry ICU templates in `$value`, locale variants in `$extensions.<vendor>.locale`, and parameter shapes in `$extensions.<vendor>.parameters`. The localisation vendor consumes the source-locale templates and produces per-locale variants; the runtime resolves per the user's locale via ICU. Without content tokens, every component carries its own i18n integration; with content tokens, the integration happens at the token layer. (See 04 §Content as a system layer for the content-token catalogue authoring discipline; per-component i18n consumption follows the catalogue.)*

### See also block in the new 04 sections

- **23 — Typography Tokenisation** (typography-as-voice; composite-token `$description` carrying voice intent at the typography / content boundary).
- **13 — Internationalization and RTL** (i18n architectural foundation; content-tokens layer above 13's locale shape).
- **25 — AI-Aware Patterns and Conversational UI** (AI-surface patterns whose content half this section pulls into the system layer).
- **26 — Adaptive Interfaces - Foundations** (adaptive UI content; variability-by-design problem applied to content).
- **27 — Adaptive Interfaces - Implementation** (structured-output content scaffolding; LLM-mediated content composition bounded by the token catalogue).
- **29 — Per-Component Documentation Template** (the per-component template's §14 Content guidelines field, which references the system-level matrix and tokens rather than authoring per-component).
- **30 — Generated-from-Data Documentation** (content guidance located in the authored half of the pipeline; the matrix and the token catalogue ship as authored deliverables).
- **24 — Tokens at Scale** (multi-brand voice as per-brand axis; the Theme Schema's voice-tone primitive).
- **33 — White-Label Systems** (the for-resellers Theme Schema's voice-tone parameter; the engine generates per-brand content tokens from the voice axis the way it generates per-brand visual tokens from the color axis).
- **03 — Component Library** (the component-library microcopy seam consumes the content-token catalogue rather than authoring per-component microcopy).
- **00d — Commercial Model** (the UX Copywriter 75-hour line item is one point on a defensible 40–250-hour range scaled against the three drivers).
- **00e — Team and Discipline** (Copywriter as 00e residual — the role's practice-scale hiring signal, seniority calibration, and career path remain open for a future 00e revision).
- **07 — Governance and Adoption** (the content-side governance contract at handoff is content's analogue to the component-layer contribution model).
- **08 — Ongoing Maintenance** (the Run-phase content retainer is one of the practice's productisable post-Build offerings analogous to 33 §5's for-resellers retainer).

### The open residual

If the AI-surface content material per §5 grows in subsequent engagements — particularly if the variability-by-design problem applied to content (per §5's adaptive-UI content section) becomes load-bearing for adaptive engagements — spinning out a content-systems file as the fifth productisation companion becomes the right move in a future revision. This run commits the 04 deepen; the productisation-companion question stays open.

---

## References

The content-at-system literature is mature at the per-product level (Mailchimp, Polaris, GOV.UK, Atlassian, Carbon all ship voice-and-tone material) but thin at the cross-product / cross-engagement / agency-scale level. References below organised by section.

### Voice-and-tone matrix references (per §2)

- **Mailchimp's Voice and Tone** — `styleguide.mailchimp.com/voice-and-tone/`. The canonical field reference for voice / tone matrices; introduced the two-axis (voice column / tone row) shape that the practice adopts.
- **Shopify Polaris's Voice and tone** — `polaris.shopify.com/content/voice-and-tone`. Design-system-native voice-and-tone material; ships pattern-level guidance alongside the matrix.
- **Atlassian Design System's Writing style** — `atlassian.design/content/voice-and-tone`. Content guidelines integrated into the design-system docs; useful reference for the matrix-as-system-artefact discipline.
- **IBM Carbon's Content guidelines** — `carbondesignsystem.com/guidelines/content/overview/`. Carbon's content material; less explicitly matrix-shaped than Mailchimp / Polaris but covers similar ground at system altitude.
- **GOV.UK style guide** — `gov.uk/guidance/style-guide`. Public-sector content reference; load-bearing for accessibility and reading-level discipline.

### Content tokens / writing-tokens references (per §3)

- **Linear's empty-states pattern** — `linear.app` (content visible across the product). Practitioner-observed content-token shape; not formally documented but consistently applied.
- **Stripe's error-message taxonomy** — `docs.stripe.com/error-codes`. Error codes mapped to user-facing message templates; the canonical example of content tokens in the field.
- **Polaris content patterns** — `polaris.shopify.com/patterns`. Pattern tokens for CTAs, error microcopy, loading messages; covered with usage rules at system altitude.
- **GOV.UK Design System content patterns** — `design-system.service.gov.uk/patterns/`. Content patterns for date input, names, addresses, error messages; tokenised templates with usage rules.
- **DTCG Format Module 2025.10** — `tr.designtokens.org/format/`. Current spec; does not cover content tokens. The practice's content-token shape per §3 is a custom DTCG `$extensions` extension pending a future content-token spec.
- **ICU MessageFormat documentation** — `unicode-org.github.io/icu/userguide/format_parse/messages/`. The canonical message-format reference; underpins content tokens' i18n axis.

### i18n content references (per §4)

- **ICU MessageFormat** — `unicode-org.github.io/icu/userguide/format_parse/messages/`. As above.
- **Lokalise** — `lokalise.com`. Localisation platform with ICU support; common practitioner choice.
- **Crowdin** — `crowdin.com`. Localisation platform with ICU support; common practitioner choice.
- **Smartling** — `smartling.com`. Localisation platform with varying ICU support; verify per project.
- **Phrase** — `phrase.com`. Localisation platform with ICU support; growing practitioner adoption.
- **Memsource (now Phrase TMS)** — `phrase.com/products/tms/`. Localisation platform; common at enterprise scale.
- **Unicode CLDR Plural Rules** — `cldr.unicode.org/index/cldr-spec/plural-rules`. Per-locale plural categorisation reference.
- **Unicode Bidirectional Algorithm** — `unicode.org/reports/tr9/`. The canonical RTL handling reference; underpins 13's RTL coverage and this section's content-direction handling.

### AI-surface content references (per §5)

- **EU AI Act Article 50** — `artificialintelligenceact.eu/article/50/`. Disclosure requirements; load-bearing for §5's disclosure boilerplate framing.
- **OpenAI's content guidelines for assistants** — varies; verify against current OpenAI documentation. Useful reference for refusal patterns at API scale.
- **Anthropic's Constitutional AI material** — `anthropic.com`. Reference for the assistant-tone-as-system-prompt pattern.
- **The Vercel AI SDK and AI Elements documentation** — `sdk.vercel.ai`. Practitioner-level AI-surface content patterns at the implementation layer; ships content templates alongside component primitives.

### UX Copywriter role references (per §6)

- **Andy Welfle and Michael Metts, *Writing is Designing*** (Rosenfeld Media, 2020). The canonical UX writing book at practitioner depth.
- **Torrey Podmajersky, *Strategic Writing for UX*** (O'Reilly, 2019). Strategic-level UX writing material; useful for the role's seniority-calibration discussion.
- **Erika Hall's writing on content strategy** — `mulestrong.com/blog/`. Cross-discipline content-strategy material that intersects DS work.
- **Nicole Fenton and Kate Kiefer Lee, *Nicely Said*** (New Riders, 2014). Foundational UX writing material; predates DS era but architecturally durable.
- **John Saito's writing** — `medium.com/@jsaito`. Practitioner-level UX writing material at Dropbox, Lyft, Google.

### Verification notes

- All "as of mid-2026" claims about content-token vendor support, ICU authoring tooling, LLM-based content review tooling, and AI-surface content patterns reflect mid-2026 platform state. Verify against current docs before treating any specific claim as load-bearing in client work.
- The DTCG content-token spec is the practice's bet for 2026–2027; track DTCG community discussions quarterly. The practice's bridge schema per §3 is custom DTCG `$extensions` and migrates if and when a canonical content-token spec lands.
- Native vendor support for content tokens from Specify / Knapsack / Supernova / Backlight / Tokens Studio is the practice's bet for 2026–2027; track quarterly.
- The CareCentrix 75-hour UX Copywriter line item is a single data point at one engagement complexity. The hour-justification model per §6 is observation-grounded against the three drivers; the first 5–10 engagements where the practice ships a content-system layer with full Copywriter scope should track actual hours against the three-driver model. Refine in next file revision once empirical data exists.
- The voice-and-tone matrix as system-level artefact is widely shipped at per-product scale (Mailchimp, Polaris, Atlassian, Carbon, GOV.UK); it is not yet widely shipped as an *agency-cross-engagement* artefact. The practice can lead by shipping the matrix as a default Discovery deliverable across engagements; the bet is that this becomes table stakes at agency scale by 2027.
- Content tokens are the practice's most aggressive content-system commitment. The bet is that the field shifts to tokenised content over the next 24 months under AI-readiness commercial pressure; the practice's bridge schema migrates to whichever spec wins.
