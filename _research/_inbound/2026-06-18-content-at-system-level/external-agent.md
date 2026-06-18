# Content Considerations at the Design-System Level

## Why content-at-system-level is its own discipline

The operationalisation of content within a design system architecture requires a rigorous demarcation between per-component content guidance and system-level content architecture. Conflating these two layers routinely produces documentation sites that offer exhaustive microcopy instructions for individual components but entirely lack the overarching architectural constraints necessary to synthesise those components into a coherent brand voice. Per-component content guidance—which resides securely within the documentation page of a specific component (per 29 §14)—dictates execution constraints. It answers immediate, localised questions regarding character limits for a button label or the specific verb tense for a toast notification. In stark contrast, content-as-system-architecture establishes the immutable primitives, tokenised assets, and linguistic constraints that sit entirely above the component layer.

This distinction represents a critical commercial leverage point at the agency scale. An agency that ships component-specific documentation without a governing system-level architecture invariably produces fragmented, written-once microcopy. In such environments, as new components are introduced or bespoke layouts are assembled, they inherit no foundational voice constraints, leading to rapid brand degradation across digital surfaces. Conversely, shipping abstract content tokens without per-component consumption guidance leaves product teams with technical primitives they do not know how to apply. Both layers are strictly necessary, but their operational sequencing dictates that the system-level architecture must be established once per engagement to serve as the structural foundation. The per-component guidance then acts as the consumption layer, following the architecture rather than leading it.

The miscategorisation cost of treating content merely as a documentation appendix—the failure mode of "we'll write the microcopy guidelines page" per 04 §Failure modes—misses the architectural imperative entirely. High-maturity systems, such as those maintained by Atlassian or Shopify, do not treat content as an afterthought; they treat it as an infrastructural requirement. A practice that treats content as a token primitive without articulating the voice-and-tone constraint above the tokens ships primitives that fail to compose into a coherent brand voice. The empty-states pattern in Linear operates effectively because Linear possesses a highly opinionated, systemically enforced voice; applying identical primitives within a brand lacking strong voice constraints yields inconsistent output. Thus, the practice's discipline requires a strict hierarchy: the voice-and-tone constraint at the top, content tokens at the primitive layer, and per-component guidance as the consumption layer, with all three meticulously articulated.

Within the practice's existing vault, 04 names the UX Copywriter role and the content-guidelines deliverable but falls short of articulating the system-architecture layer beneath them. Document 29 §14 captures content per component, while 30 §Authored locates content guidance in the human-authored half of the pipeline. Document 03 identifies the microcopy seam at the component-library level, 25, 26, and 27 cover AI-surface content at the pattern level, 13 covers RTL and locale shape, and 23 covers typography (which carries voice). None of these documents currently articulate the system-level content architecture that sits above them. Closing this gap is essential for elevating the practice's deliverables from mere UI kits to comprehensive, enterprise-grade design systems.

## Voice-and-tone systematisation as a system artefact

The canonical field references for content strategy—notably the Mailchimp voice-and-tone matrix and Shopify Polaris's content guidelines—establish voice and tone not as an appendix of best practices, but as a rigid, system-level artefact applied uniformly across all product surfaces. At an architectural altitude, the distinction between the two is highly operational. "Voice" represents the brand's immutable character—the core attributes that remain identical whether the interface is delivering a celebratory success toast or a critical destructive-action confirmation. "Tone" constitutes the contextual adjustment of that voice, shifting the rhetorical posture based on the user's emotional state and the interface's functional requirement.

To operate this at an agency scale, the voice-and-tone matrix must be delivered as a structural system artefact. The matrix cross-tabulates the brand's core voice attributes across the horizontal axis against the system's defined interaction contexts along the vertical axis. The intersecting body cells prescribe exactly how the immutable voice expresses itself under varying contextual pressures, transforming abstract brand values into programmatic execution rules.

| Tone Context (System Situations) | Voice: Expert (Clear, authoritative, precise) | Voice: Warm (Empathetic, human, supportive) | Voice: Direct (Unambiguous, efficient, plainspoken) |
|---|---|---|---|
| **Success / Confirmation** | Validates the system state definitively (e.g., "Database synchronisation complete"). | Acknowledges the user's achievement without excessive exuberance or patronisation. | States the outcome immediately without filler (e.g., "Changes saved"). |
| **Error / Network Failure** | Diagnoses the root cause using precise terminology, avoiding dead-end states. | Validates frustration; avoids blaming the user; offers immediate support pathways. | Provides the exact remediation step immediately (e.g., "Check connection and retry"). |
| **Destructive Action** | Details the exact technical scope of the deletion and data retention policies. | Remains calm and reassuring, confirming intent safely without inducing panic. | Uses stark, unmistakable verbs (e.g., "Delete permanently", not "Remove"). |
| **Empty State (First-Use)** | Explains the functional capability of the empty surface and required inputs. | Encourages the first interaction warmly to reduce onboarding friction. | Provides a single, clear "Start" or "Create" imperative verb. |
| **Loading / Processing** | Indicates the specific backend operation occurring (e.g., "Encrypting payload..."). | Reassures the user that the system is actively working on their behalf. | Uses concise progressive indicators to manage time expectations. |

This matrix bridges directly into typography. As established in 23, typography choices inherently function as voice expressed in type—representing the type system's connotation vocabulary and operating as an immutable system constraint. Voice-in-content and voice-in-type carry the identical brand constraint at the system level. Therefore, typography composite tokens (per 23's DTCG composite-token shape) must carry voice intent programmatically within their `$description` fields. This practice unifies the visual and verbal axes under a single tokenised constraint, ensuring that the selection of a specific typographic scale aligns with the rhetorical posture of the content it renders.

For multi-brand or white-label-for-reseller architectures (per 24 and 33), the voice-and-tone matrix scales as a per-brand axis. Each brand's unique matrix is generated by the underlying engine as a distinct asset. The Theme Schema's voice-tone parameter acts as the input for the reseller system; the engine derives the necessary per-brand content tokens from this parameter exactly as it calculates semantic color tokens from a primary hex value.

However, the matrix remains an inert, rapidly decaying document unless paired with rigorous enforcement disciplines. The field frequently fails by shipping a matrix that product teams promptly ignore, leading to relentless content drift where voice fragments by release. Effective enforcement requires three specific operational mechanisms. First, pre-merge review checklists ensure every pull request containing interface text changes is evaluated against the core voice attributes. Second, AI-assistant tone parameters (per 25, 26, 27) format the matrix as the system prompt consumed by adaptive UI assistants, ensuring generative text strictly adheres to brand constraints. Third, content-token usage discipline mandates that when the system provides a specific `content/error/network-failure` token, consuming components inherit the pre-vetted voice of the matrix, programmatically overriding ad-hoc component authoring. The practice's discipline dictates that the matrix is shipped and enforced; the enforcement is what makes it system-shaped rather than docs-appendix-shaped.

## Content tokens / writing-tokens as a primitive

The most significant evolution in system-level content architecture is the deployment of content tokens—often termed writing tokens—as first-class primitives. Pioneered by high-maturity ecosystems such as Linear's empty-states patterns and Stripe's error-message taxonomies, content tokens encapsulate interface text as named, reusable, and composable resources. They function analogously to design tokens, allowing engineering teams to pull vetted, voice-aligned microcopy directly from the system registry rather than relying on manual authoring per component.

A rigorous architectural boundary must be drawn regarding what is tokenisable. Tokenisable content encompasses highly repetitive, templated microcopy parameterised with specific slots. This includes Call-to-Action (CTA) verb taxonomies with strict usage rules, error message templates categorised by fault type (network, validation, permission), empty-state patterns (first-use vs. filtered-out), loading microcopy, and standard confirmation patterns. Non-tokenisable content includes long-form prose, marketing narratives, brand-narrative content, and per-component intent prose. The fundamental dividing line is clear: tokens carry templated content with parameterised slots; prose carries judgment.

As of mid-2026, the Design Tokens Community Group (DTCG) specification covers design tokens such as colour, spacing, typography, and motion, but lacks a native, formalised schema for content tokens. The closest existing precedent is i18n message catalogues based on ICU MessageFormat, where keys map to templates with parameter slots, accommodating locale variants and pluralisation rules. The practice must lead by shipping a defensible, DTCG-shaped content-token schema that bridges this gap, rendering it ICU-compatible at the i18n axis and AI-readable via `.ai.json` (per 30).

### Speculative but Defensible DTCG-Shaped Content Token Schema

| Schema Property Path | Data Type | System Function and Description |
|---|---|---|
| `content.feedback.error.network_timeout.$type` | String | Declares the token type as `content` or `message`, signalling to translation and build tools that the value requires linguistic processing. |
| `content.feedback.error.network_timeout.$value` | String | Contains the core ICU MessageFormat template (e.g., `"{count, plural, one {Connection failed after # retry.} other {Connection failed after # retries.}}"`). |
| `content.feedback.error.network_timeout.$description` | String | Articulates the specific voice intent and usage constraint from the matrix, ensuring consumers understand the tone alignment. |
| `content.feedback.error.network_timeout.$extensions.i18n.locale` | Object | Houses the dictionary of localized `$value` overrides per target locale, enabling seamless runtime internationalisation resolution. |
| `content.feedback.error.network_timeout.$extensions.i18n.parameters` | Object | Documents the required shape and data types of the slots within the ICU template (e.g., `count: Integer`), generating type-safe TypeScript interfaces. |

This architecture heavily implicates cross-platform localisation. Content tokens carry localisation as a cross-cutting concern, reconciling with i18n tooling at runtime. The token's locale variants resolve via ICU, and parameters bind at render time. Without content tokens, every component carries its own fragmented i18n integration; with content tokens, the integration occurs purely at the token layer, isolating the complexity from the component API.

The boundary between where content lives—within the design system's content tokens or within the CMS's content models—is a procurement-grade decision that foreshadows the modern composable/headless coverage outlined in 09 §1.32. The practice's working position is definitive: tokens exist for templated, system-level content, while the CMS exists for editorial, product-specific content. This line mirrors the distinction between design tokens for system primitives and component-specific styles for per-instance overrides.

Tooling reality currently presents significant friction. As of mid-2026, Tokens Studio does not ship content tokens, Style Dictionary's transforms do not cover them natively (requiring custom transforms), and no major design-token vendor supports them as a first-class object. The practice's bet is that native vendor support will land in late 2026 to 2027, driven by AI-readiness commercial pressure. Practitioners shipping content tokens today are effectively wrapping ICU message catalogues with DTCG-shaped metadata as a highly necessary bridge investment.

## i18n content depth at the system level

While document 13 establishes the architectural foundation for RTL layouts and locale shape, it does not articulate how component content guidelines tie back to i18n tooling, nor how content tokens carry locale variants. Furthermore, it leaves unaddressed how the UX Copywriter orchestrates governance with localisation vendors or how the voice-and-tone matrix accommodates per-locale tonal adjustments—such as Japanese keigo levels, the German formal/informal Sie/du distinction, or RTL rhetorical conventions.

At system scale, the integration of ICU MessageFormat with content tokens is paramount. ICU handles pluralisation, gender, ordinals, and locale-aware selections natively. The design system ships ICU-shaped templates within the `$value` of the content token, which the runtime resolves per the user's locale. This is a radical departure from the standard industry practice of shipping hand-authored, per-locale static strings. Most engagements still rely on hand-authored strings because the tooling for ICU authoring remains thin—most CMSes, design system documentation platforms, and even certain translation vendors fail to natively support or validate ICU syntax, often resulting in parser errors when double curly braces are mistakenly used instead of single braces.

Pluralisation at system scale illustrates the necessity of this architecture. The English speaker's mental model of singular versus plural (one cat / two cats) fails to generalise. Russian utilises three plural categories based on numeric casing, Arabic utilises six, Welsh uses six, and Polish uses four. ICU expresses pluralisation via the `plural` selector with named CLDR cases (`zero`, `one`, `two`, `few`, `many`, `other`). Content tokens carrying ICU templates handle this complexity natively, ensuring grammatical accuracy without requiring conditional logic in the application code. Hand-authored per-locale strings fundamentally break under these constraints.

Gendered language presents identical challenges. ICU's `select` operator manages gendered variants (male / female / non-binary / other), but per-locale, the required variants differ drastically. Spanish demands masculine and feminine variations, German requires three grammatical genders, while Finnish lacks grammatical gender entirely. Content tokens at system scale declare the required gendered variant axis centrally, allowing per-locale catalogues to carry the appropriate overrides. Similarly, RTL content ordering requires more than logical properties at the layout level. Bidirectional content embedding—such as Arabic text containing English loanwords or Hebrew text interspersed with numbers—requires directional metadata within the content token. The token must articulate its primary directionality and dictate the usage of Unicode `<bdi>` (Bi-Directional Isolation) elements over simple `<span dir="rtl">` tags to prevent cross-directional text pollution.

The governance of this localised content relies on the UX Copywriter. This role coordinates with localisation vendors (such as TransPerfect, Smartling, Crowdin, or Lokalise) to process per-locale content. The system's content tokens serve as the absolute source-of-truth. The localisation vendor ingests the source tokens, produces the per-locale variants based on the ICU templates, and flows the variants back into the content-token catalogue's extensions. Without content tokens, localisation devolves into a per-component, string-by-string exercise; with them, localisation becomes a scalable, catalogue-shaped pipeline. This boundary perfectly aligns with the forthcoming CMS platforms section (§1.32), where localised editorial content resides in the CMS, while localised system content resides securely in the token catalogue.

## Content for AI surfaces as a content-system layer

As design systems expand to support adaptive interfaces and generative surfaces (per 25, 26, 27), the content half of these patterns must be explicitly articulated as a content-system layer. The voice-and-tone matrix, the content tokens, and the UX Copywriter role collectively own this layer at system scale. Relying on ad-hoc, per-pattern guidance for AI features results in highly disjointed user experiences and introduces severe brand risk.

Assistant tone is the direct application of the voice-and-tone matrix to AI surfaces. The brand's voice constrains the assistant's outputs, but the tone matrix's contexts must be expanded to include specific AI interaction postures: proactive assistant, reactive assistant, uncertain assistant, refusing assistant, clarifying assistant, and human-handoff. The matrix's body cells for these AI contexts specify exactly how the brand voice expresses itself, and crucially, these cells become the actual system prompt that the assistant consumes. The matrix directly parameterises the LLM.

Refusal copy patterns demand strict systematisation. When an assistant refuses a request due to out-of-scope boundaries, safety constraints, or capability limitations, the refusal must follow a precise content-pattern shape: it must acknowledge the user's request, name the specific constraint, and offer a viable alternative path. Content tokens at the system level ship these refusal templates, carrying the brand voice and allowing per-pattern customisation to fill the parameter slots. Without tokens, every product surface re-authors refusal copy, leading to fragmented brand voice and varying levels of user frustration.

Disclosure boilerplate is similarly system-level. Under regulatory frameworks like the EU AI Act Article 50, systems must disclose when users are interacting with AI. The system ships the disclosure template via content tokens; products consume the template, ensuring the legal team reviews the language once, not per-product. The practice's discipline establishes that disclosure is a system-level content primitive, never a subject for per-product authoring.

Citation format conventions and streaming states also fall under this architecture. While citation format (inline-link, footnote, sidebar) is a pattern-level visual decision, the citation copy conventions—how to introduce a citation, handle partial-confidence citations, or address missing sources—are system-level content decisions carried by tokens. Furthermore, streaming responses produce partial outputs where users may interrupt generation. The content for streaming UI (the "generating…" microcopy, the interruption confirmation, the resume-vs-restart prompt) must be system-level and tokenised. Tool-call confirmations operate identically: the confirmation copy is system-shaped via tokens, with the specific tool-call parameters filling the ICU slots.

For Adaptive-UI content, where interfaces are composed per render via an LLM, the variability-by-design problem applies equally to content as it does to visual layout. The designer specifies a space of possible content outputs and reviews the distribution of what the LLM produces. The LLM must compose its microcopy from the system's content tokens, not from ad-hoc generative strings. Content tokens form the boundary within which the LLM's variability operates, ensuring the adaptive interface remains on-brand regardless of its dynamic composition.

## The UX Copywriter role at engagement scale

The CareCentrix 2026 commercial standard names a UX Copywriter line item at 75 fixed hours, integrated into component documentation [cite: 04 §Our POV]. However, this role is currently named without justification regarding what drives those hours, what the role owns end-to-end at system scale, how handoff occurs, and how guidelines are maintained post-engagement. The UX Copywriter operates as a system-level architectural discipline, assuming end-to-end ownership of the content layer.

The role's end-to-end ownership encompasses four domains:

- **Content architecture**: Designing the voice-and-tone matrix, establishing the content-token catalogue, defining the i18n content strategy, and structuring the AI-surface content layer.
- **Content production**: Authoring the system-level content (the matrix, the tokens, the templates, and the AI-surface copy) as well as the per-component guidance.
- **Content review**: Conducting pre-merge PR reviews for any interface text changes, reviewing per-component content guidance, and performing release-readiness content audits.
- **Cross-functional coordination**: Synchronising with localisation vendors, executing legal reviews for AI disclosure copy, and aligning with brand teams on voice-and-tone evolution.

The 75-hour CareCentrix baseline fits roughly 20–25 components, operating in English-only, with no AI surfaces and a thin token catalogue (primarily errors). At engagement scale, the role's hours scale dynamically against three primary drivers:

- **Component count**: Allocating approximately 0.5–1 hour per component specifically for authoring the per-component content guidance.
- **Content-surface complexity**: AI surfaces drastically increase scope, adding ~20–40 hours per AI pattern family (chat, streaming, refusal, citation, tool-call). Multi-locale requirements add ~30–60 hours per locale beyond the source language for ICU parameterisation and vendor alignment.
- **Content-token catalogue depth**: A deep catalogue encompassing CTAs, errors, empty states, loading sequences, and confirmations adds ~40–80 hours. A thin catalogue focused solely on errors adds ~15–25 hours.

The practice's discipline dictates scoping the role against these three drivers, quoting a range (40–250 hours per Build phase) with the driver mix making the case for the chosen point in the range. Below ~10 components, the role rarely pays back; the guidance is thin enough for a senior UX or visual designer to author directly. Above ~10 components, content drift becomes visible by release, and above ~20 components, it becomes a systemic failure mode. At ~20+ components, the role pays back immensely; below it, it is over-engineering.

At engagement end, the role executes a tripartite handoff to the client product teams: the voice-and-tone matrix as a governed artefact (owned by the client's content team), the content-token catalogue as a maintained primitive (consumed by engineering, authored by content), and the per-component content guidance. This handoff is fundamentally incomplete without a governance contract defining who reviews matrix changes, approves token additions, and coordinates localisation. This is content's analogue to the contribution-model handoff at the component layer.

Bespoke engagements with a content-system handoff can ship a run-phase retainer analogous to the white-label-for-resellers SLAs described in 33 §5. This content-retainer covers matrix-evolution coordination, token-addition review, and localisation coordination. Content is one of the natural Run-phase retainer surfaces the practice has not yet fully articulated. The UX Copywriter is the content-side analogue to the design-technologist archetype outlined in 00e—a hybrid role crossing content, design, and engineering boundaries, requiring writing fluency, design-system literacy, i18n awareness, and AI-surface fluency.

## Integration — deepen 04, plus targeted additions to 23 and 13

The synthesis path for this research is to deepen 04, not a new file. The content-at-system layer represents bounded scope (per 09 §1.31) that fits as one or two H2 sections in 04 alongside the existing architecture, which already handles the per-component half cleanly. Creating a new file (e.g., `35-content-systems.md`) would represent an over-commitment to content-as-practice-IP at this stage. The practice ships content as a layer of documentation rather than as an independent productisation companion.

### What lands in 04

Two new H2 sections will be injected into `04-documentation.md`, sitting between the existing Cluster-6 Documentation-as-sales-surface and the Our-POV section:

- **Content as a system layer**: This section will cover the voice-and-tone matrix as an artefact, the DTCG-shaped content tokens, i18n content depth via ICU, and AI-surface content patterns.
- **The UX Copywriter role at engagement scale**: This section will detail end-to-end ownership, the hour-justification scaling model (40–250 hours), the governance handoff, and the Run-phase retainer parallel.

### What lands in 23

One targeted inline addition will be made to `23-typography-tokenisation.md` (under `The shape of a typography token set` or `DTCG composite typography tokens`):

The typography composite-token's `$description` field carries voice intent. This extends the discipline of treating brand-voice as an immutable system constraint into a tokens-with-descriptions discipline that seamlessly crosses the typography and content boundary.

### What lands in 13

One targeted inline addition will be made to `13-internationalization-and-rtl.md` (expanding existing message-format coverage):

The content-token i18n discipline ties directly back to component content guidelines via ICU MessageFormat. The addition will point to the new system-level content section in 04 as the definitive content-token authoring and governance layer.

### Cross-references ("See also" block)

The new sections in 04 will include a rigorous cross-reference block pointing to:

- 23: Typography-as-voice.
- 13: i18n content and ICU MessageFormat.
- 25 / 26 / 27: AI-surface content, streaming states, and adaptive UI bounds.
- 29 §14: Per-component content.
- 30: Content residing in the authored half of the pipeline.
- 24 / 33: Multi-brand and white-label voice-and-tone as Theme Schema input.
- 03: The component-library microcopy seam.
- 00d: The 75-hour line item justified via the scoping matrix.
- 00e: The UX Copywriter as a hybrid discipline residual.

(Note on open residuals: While the AI-surface content material generated in this run is dense, the practice's discipline dictates landing it as a 04 deepen first. If AI-surface content material grows significantly in subsequent client engagements, it remains a candidate for spinning out into its own dedicated slot alongside 25/26/27 in a future revision.)

## References

- Mailchimp Content Style Guide, *Voice and Tone*. Available at: `styleguide.mailchimp.com/voice-and-tone/`.
- Shopify Polaris, *Content Guidelines*. Available at: `polaris.shopify.com/content`.
- Atlassian Design System, *Voice and Tone Principles*. Available at: `atlassian.design/content/voice-tone`.
- Stripe API Reference, *Error Codes and Error Handling*. Available at: `docs.stripe.com/error-codes`.
- Linear, *Empty States and Microcopy Patterns* (Industry Observation).
- IBM Carbon Design System, *Empty States Pattern*. Available at: `carbondesignsystem.com/patterns/empty-states-pattern/`.
- GOV.UK Design System, *Style Guide and Content Integration*. Available at: `design-system.service.gov.uk`.
- Unicode ICU User Guide, *MessageFormat*. Available at: `unicode-org.github.io/icu/userguide/format_parse/messages/`.
- Lokalise, Crowdin, and Smartling Documentation on ICU and Translation Pipelines.
- Metts, M. J., & Welfle, A. (2020). *Writing Is Designing: Words and the User Experience*. Rosenfeld Media.
- Podmajersky, T. (2019). *Strategic Writing for UX: Drive Engagement, Conversion, and Retention with Every Word*. O'Reilly Media.
- Hall, E. (2013). *Just Enough Research* / Mule Design Publications on Conversational Design.
- Curtis, N. (EightShapes). *Component Design Guidelines and Naming Tokens in Design Systems*.
