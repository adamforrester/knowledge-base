You are researching content considerations at the design-system level —
the practitioner-facing discipline of treating content as system
architecture (voice and tone systematised at brand level; content tokens
as a primitive analogous to design tokens; i18n content depth at system
scope; content for AI surfaces as a content-system layer; the UX
Copywriter role at engagement scale) — for a senior design systems
practitioner leading the practice at a global creative agency. The
output is a structured knowledge document whose load-bearing material
will land as a deepen pass on `04-documentation.md` (one or two new
H2 sections at system altitude alongside the existing per-component
content discipline) plus targeted inline additions to
`23-typography-tokenisation.md` (typography composite tokens carrying
voice in their `$description`) and `13-internationalization-and-rtl.md`
(content-token i18n discipline tied back to component content
guidelines). Synthesis path is **deepen 04, not a new file** — the
slot decision is committed in 09 §1.31 and confirmed for this run.

This run is the *content-as-system-architecture* half of the content
question. The per-component half — content guidance per component, the
17-section template's §14 Content guidelines slot, the AI-Compatible
doc's tone-as-token argument — is already covered by 04
(§Documentation strategy, §Document intent not appearance,
§Generated-not-handwritten), 29 §14 (Content guidelines as a per-
component template field), 30 §What is generated vs. authored (content
guidance as authored, not generated), 03 (the component library's
microcopy seam), and 26 §3 (assistant tone for adaptive surfaces).
What is *not* covered is the system-level architecture above the per-
component layer — the voice-and-tone matrix as a system artefact
rather than per-component guidance; content tokens as a tokenised
resource analogous to design tokens; i18n content tied to component
content guidelines; AI-surface content patterns as a content-system
layer rather than per-25/26/27-pattern guidance; the UX Copywriter
role's end-to-end ownership at engagement scale (the 04 75-hour
CareCentrix line item is named but not justified by client size or
content surface complexity). This run closes that gap.

This is not an introductory guide — assume the reader is the practice
lead, has read 04 / 13 / 23 / 25 / 26 / 27 / 29 / 30 / 31 / 32 / 33 in
the practice's vault, knows what a design token is (per 22 / 24), what
DTCG is (per 22 / 24), what a Theme Schema is (per 24 + 33), what
ICU MessageFormat is (per 13), what a `.ai.json` registry is (per 30),
what 25's chat / streaming / refusal / citation / tool-call patterns
are at the implementation layer, what 26 / 27's adaptive UI postures
and patterns are, what the per-component template's 17 sections
include (per 29), and what the CareCentrix 2026 commercial standard's
UX Copywriter 75-hour line item is (per 04 §Our POV). Don't explain
what voice-and-tone matrices are at the basic level (Mailchimp's
voice-and-tone is widely known), what microcopy is, what error states
are, what design tokens are, what ICU MessageFormat does at the basic
level, what the DTCG schema is — explain how the practice should
*operate* the content layer of a DS as a discipline at agency scale,
where content tokens are a defensible primitive vs. where they are
over-engineering, where the field's content tooling has known gaps
that practitioners work around, what the UX Copywriter role owns
end-to-end and how it staffs at engagement scale, and how this layer
relates to (but does not replace) the per-component content guidance
covered in 04 / 29 / 03.

Research scope — cover all of the following:

1. Why content-at-system-level is its own discipline

- The case that content-as-system-architecture is a *distinct
  discipline* from per-component content guidance. Per-component
  content lives in the docs page (29 §14); voice-and-tone-as-system-
  artefact, content-tokens, AI-surface content patterns, and the
  Copywriter role live above the per-component layer. Both are needed;
  conflating them produces docs sites with thorough per-component
  microcopy guidance and no articulation of the brand-voice constraint
  the per-component guidance is meant to satisfy.
- Where content-at-system sits relative to existing files. 04 names
  the UX Copywriter role and the content-guidelines deliverable but
  doesn't articulate the system-architecture layer beneath them. 29
  §14 captures content per component. 30 §Authored locates content
  guidance in the human-authored half of the pipeline. 03 names the
  microcopy seam at the component-library level. 25 / 26 / 27 cover
  AI-surface content at the pattern level. 13 covers RTL and locale
  shape. 23 covers typography (which carries voice). None of these
  articulates the system-level content architecture that sits *above*
  them — the voice-and-tone matrix as system artefact; content tokens
  as primitive; AI-surface copy as system-coherent surface; the
  Copywriter role's end-to-end ownership.
- Why this matters commercially. The agency that ships docs guidance
  per component without the system-level content architecture
  produces inconsistent microcopy across components — every component's
  content is written-once, never refactored against the system's
  voice; new components inherit no constraint; the brand voice
  fragments. The agency that ships content tokens without the per-
  component guidance ships primitives the consumer doesn't know how
  to apply. Both are needed. The system-level architecture is the
  practice's leverage — operationalise it once per engagement; the
  per-component guidance follows the architecture rather than
  leading it.
- The miscategorisation cost worth naming. The practice that treats
  content as docs-appendix (the "we'll write the microcopy guidelines
  page" failure mode per 04 §Failure modes) misses content-as-system-
  architecture entirely. The practice that treats content as token
  primitive without articulating the voice-and-tone constraint above
  the tokens ships tokens that don't compose into coherent brand
  voice (the Linear-empty-states pattern works because Linear has a
  strong voice; the same primitives in a brand without a strong
  voice produce inconsistent output). The practice's discipline:
  voice-and-tone constraint at the top; tokens at the primitive layer;
  per-component guidance as the consumption layer; all three articulated.

2. Voice-and-tone systematisation as a system artefact

- The case for the voice-and-tone matrix as a system artefact, not
  per-component content. The Mailchimp voice-and-tone matrix
  (`styleguide.mailchimp.com/voice-and-tone/`) and Shopify Polaris's
  content guidelines (`polaris.shopify.com/content`) are the canonical
  field references — both treat voice (the immutable brand
  characteristic) and tone (the contextual adjustment per situation)
  as a *system-level matrix* applied across every surface, not as
  per-component microcopy.
- The voice / tone distinction at system altitude. Voice is the
  brand's immutable character — the thing that doesn't change between
  a confirmation toast and a destructive-action dialog. Tone is the
  contextual adjustment — confident but not arrogant in a success
  state; clear and calm in an error state; matter-of-fact in a
  destructive-action confirmation. The matrix is the cross-tabulation
  — voice across the top (the brand's three-to-five voice attributes,
  e.g., "warm, expert, plainspoken, direct, never condescending");
  tone across the side (the system's content contexts, e.g.,
  success / error / destructive / empty / loading / disabled /
  read-only / informational); body cells specify how voice expresses
  in each context. The matrix is the practice's most-undersold
  content artefact at system altitude.
- How voice connects to typography. Per 23 — typography choices are
  voice in type ("brand voice as an immutable system constraint";
  the type system's connotation vocabulary; the monumental-display-
  plus-invisible-text asymmetric pattern). Voice-in-content and
  voice-in-type carry the same brand constraint at the system level;
  the matrix lives across both surfaces. Typography composite tokens
  per 23's DTCG composite-token shape can carry voice intent in
  their `$description` (the practice's tokens-with-descriptions
  discipline applied to the content / voice axis).
- The multi-brand voice question. Per 24 / 33 — multi-brand and
  white-label-for-resellers systems carry brand voice as a per-
  brand axis. Each brand's voice-and-tone matrix is one of the
  per-reseller assets the engine generates (per 33 §7). The Theme
  Schema's voice-tone parameter (per 33's brand-voice tone parameter
  for assistant copy at §3 / §5) is the for-resellers system's
  voice-axis input; the engine derives the per-brand content tokens
  from the voice parameter the way it derives the color tokens from
  the primary-color primitive.
- Enforcement disciplines. The voice-and-tone matrix is only useful
  if it's enforceable. Three disciplines that work: review checklists
  (every PR with content changes runs the matrix's three or four
  voice questions before merge); AI-assistant tone parameters per
  25 / 26 / 27 (the matrix becomes the system prompt the assistant
  consumes — the brand voice constrains the assistant's outputs);
  content-token usage discipline (per §3 below — when the system
  ships a `content/error/network-failure` token, components using it
  inherit the matrix's voice rather than authoring per-component).
  The pattern that fails: the matrix exists as a docs page nobody
  reads; per-component content drift over time; voice fragments by
  release.
- Practitioner-side gap to name. The matrix is well-known as a
  surface but rarely shipped as a *system artefact* in DS engagements.
  Most engagements either ship per-component content guidance
  without the matrix (CareCentrix-shape) or ship a matrix without
  enforcing it through the per-component pipeline. The practice's
  discipline: the matrix is shipped *and* enforced; the enforcement
  is what makes it system-shaped rather than docs-appendix-shaped.

3. Content tokens / writing-tokens as a primitive

- The case for content tokens. The field is starting to ship them
  — Linear's empty-states pattern (each empty state carries a
  consistent "encouraging-not-perky" voice via tokenised templates);
  Stripe's error-message taxonomy (errors carry codes that map to
  templates; the templates carry the system's voice); Polaris's
  content-pattern primitives (Polaris ships pattern tokens for
  CTAs, error microcopy, loading messages). The shared shape:
  content as a *named, reusable, composable resource* analogous
  to design tokens — primitives the consumer pulls off the shelf
  rather than authoring per-component.
- What's tokenisable vs. what isn't. **Tokenisable.** CTA verb
  taxonomies (the system's verbs — "Save", "Continue", "Submit",
  "Cancel", "Discard" — with usage rules); error message templates
  (per error category — network / validation / permission /
  destructive-confirm); empty-state copy patterns (per empty-state
  category — first-use / no-results / filtered-out / system-empty);
  loading-state microcopy ("Loading…" vs. "Searching…" vs.
  "Saving…"); confirmation patterns (success messages; toast copy;
  destructive-action confirm). **Not tokenisable.** Long-form prose;
  marketing copy; brand-narrative content; per-component intent
  prose (the "when-to-use" guidance is per-component judgment, not
  a token). The line: tokens carry *templated* content with
  parameterised slots; prose carries *judgment*.
- The DTCG-shaped schema for content tokens. Does the field have
  one? As of mid-2026, no — DTCG covers design tokens (color,
  spacing, typography, motion, dimension) but not content tokens.
  The closest precedent is i18n message catalogues (ICU
  MessageFormat per 13) — keys map to templates with parameter
  slots; locale variants per key; pluralisation rules. Content
  tokens at system level can shape the same way: a `$value`
  containing the template string; a `$description` containing the
  voice intent; `$extensions.<vendor>.locale` carrying per-locale
  variants; `$extensions.<vendor>.parameters` describing the slot
  shape. The practice can lead by shipping a content-token schema
  shape as a defensible POV — DTCG-shaped, ICU-compatible at the
  i18n axis, AI-readable via `.ai.json` per 30. (Surface a
  speculative-but-grounded schema sketch in the file.)
- Cross-platform localisation angle. Content tokens carry
  localisation as a cross-cutting concern; per 13 — RTL string
  ordering, locale-specific date / number / currency formatting,
  pluralisation rules. Content tokens at system level reconcile
  with i18n tooling at runtime — the token's locale variants
  resolve via ICU; the parameters bind at render time. Without
  content tokens, every component carries its own i18n integration;
  with content tokens, the integration happens at the token layer.
- The CMS-vs-content-tokens authoring boundary. Where content
  lives — in the DS's content tokens or in the CMS's content
  models — is a procurement-grade decision. Per 09 §1.32 (CMS
  platforms — modern composable / headless coverage) — the
  CMS-vs-DS authoring boundary is a forthcoming gap; this section
  foreshadows it. The practice's working position: tokens for
  *templated, system-level* content; CMS for *editorial,
  product-specific* content. The line is similar to design
  tokens vs. component-specific styles: tokens for system
  primitives; component-specific for per-instance overrides.
- Tooling reality and gaps. Tokens Studio doesn't ship content
  tokens; Style Dictionary's transforms don't cover content tokens
  natively (custom transforms required); no major design-token
  vendor ships content tokens as a first-class object as of
  mid-2026. The practice's bet: native vendor support lands in
  2026–2027 alongside the AI-readiness commercial pressure;
  practitioners shipping content tokens today are wrapping ICU
  message catalogues with DTCG-shaped metadata as a bridge
  investment.

4. i18n content depth at the system level

- The case for i18n content as system-architectural concern. Per
  13 — the practice covers RTL and locale shape at the architectural
  level. What's not covered: how component content guidelines tie
  back to i18n tooling; how content tokens (per §3) carry locale
  variants; how the UX Copywriter role coordinates with localisation
  vendors; how voice-and-tone (per §2) handles per-locale tonal
  adjustments (Japanese keigo levels; German formal/informal Sie/du;
  RTL rhetorical conventions). 13 is the architectural foundation;
  this section adds the content layer above it.
- ICU MessageFormat at system scale. Per 13 — ICU covers
  pluralisation, gender, ordinals, locale-aware select. At system
  scale, ICU integrates with content tokens (per §3) — the token
  contains an ICU template; the runtime resolves via ICU per the
  user's locale. The system ships ICU-shaped templates, not
  hand-authored per-locale strings. Most engagements still ship
  hand-authored per-locale strings because the tooling for ICU
  authoring is thin (most CMSes don't author ICU; most DS
  documentation doesn't author ICU; most translation vendors
  don't author ICU).
- Pluralisation at system scale. The English speaker's mental model
  (one cat / two cats) doesn't generalise. Russian has three plural
  categories; Arabic has six; Welsh has six; Polish has four. ICU
  expresses pluralisation via the `plural` selector with named
  cases (`one`, `few`, `many`, `other`). Content tokens carrying
  ICU templates handle this natively; hand-authored per-locale
  strings break.
- Gendered language. ICU's `select` selector handles gendered
  variants (male / female / non-binary). Per locale, the gendered
  variants differ — Spanish has masculine / feminine; German has
  three genders; Finnish has none. Content tokens at system scale
  declare the gendered variant axis; per-locale catalogues carry
  the variants.
- RTL content ordering. Per 13 — logical properties at the layout
  level. At the content level: bidirectional content embedding
  (Arabic-with-English-loanwords; Hebrew-with-numbers); the
  Unicode `<bdi>` element vs. `<span dir="rtl">`; the
  `unicode-bidi` CSS property's role. Content tokens at system
  scale carry directional metadata (the token's primary direction;
  the embedded-content directional handling).
- Localisation governance. The UX Copywriter (per §6) coordinates
  with localisation vendors (TransPerfect, Lionbridge, Smartling,
  Crowdin, Lokalise) on per-locale content. The system's content
  tokens are the source-of-truth; the localisation vendor
  consumes the source tokens and produces per-locale variants;
  the variants flow back into the content-token catalogue. Without
  content tokens, localisation is per-component string-by-string;
  with content tokens, localisation is catalogue-shaped.
- The line that connects to §1.32 (CMS platforms — forthcoming).
  Localised editorial content lives in the CMS; localised system
  content lives in the content-token catalogue. The boundary
  is the same as the content-token-vs-CMS line per §3 — system-
  level vs. product-specific. Foreshadow §1.32 here.

5. Content for AI surfaces as a content-system layer

- The case for AI-surface content as system architecture. Per
  25 / 26 / 27 — the practice ships AI-aware patterns (chat,
  streaming, citation, refusal, tool-call) and adaptive interfaces
  (Sentient Triangle scaffold, fourteen patterns, five-rung
  spectrum). The content half of these patterns — assistant tone,
  refusal copy patterns, disclosure boilerplate, citation format
  conventions, error / fallback / clarification / tool-call-confirm
  copy — is currently per-pattern in 25 / 26 / 27 but not
  articulated as a content-system layer. The voice-and-tone matrix
  per §2 + the content tokens per §3 + the UX Copywriter role per
  §6 collectively own the AI-surface content layer at system scale.
- Assistant tone as voice-and-tone applied to AI surfaces. The
  brand's voice (per §2) constrains the assistant's outputs; the
  tone matrix's contexts include AI-surface contexts (assistant-
  proactive / assistant-reactive / assistant-uncertain / assistant-
  refusing / assistant-clarifying / assistant-handing-off-to-
  human). The matrix's body cells for AI contexts specify how the
  brand voice expresses in each AI context — and become the
  system prompt the assistant consumes (per 25 §The architecture
  beneath; per 27's structured-output scaffolding).
- Refusal copy patterns. Per 25 §Refusal patterns — the assistant
  refuses (out-of-scope; safety; capability; privacy). Each refusal
  category has a content-pattern shape — the refusal acknowledges
  the request, names the constraint, offers an alternative path.
  Content tokens at system level ship the refusal templates; the
  templates carry the brand voice; the per-pattern customisation
  fills the parameter slots. Without tokens, every product surfaces
  re-authors refusal copy and the brand voice fragments.
- Disclosure boilerplate. Per 25 §Disclosure (EU AI Act Article 50
  framing). Disclosure copy is system-level — the system ships
  the disclosure template; products consume the template; the
  legal team reviews the template once not per-product. Content
  tokens at system level ship the disclosure templates. The
  practice's discipline: disclosure is a system-level content
  primitive, not per-product authoring.
- Citation format conventions. Per 25 §Citation patterns — the
  assistant cites sources. Citation format (inline-link / footnote
  / sidebar / collapsible) is per-pattern; citation copy
  conventions (how to introduce a citation; how to handle
  partial-confidence citations; how to handle missing-source
  cases) is system-level. Content tokens carry the citation copy
  templates.
- Streaming / partial-output / interruption content. Per 25 —
  streaming responses produce partial outputs; users may interrupt;
  the system shows a partial state then a final state. The content
  for streaming UI (the "thinking…" / "generating…" / "almost
  done…" microcopy; the interruption confirmation copy; the
  resume-vs-restart prompt) is system-level. Content tokens carry
  the streaming-state templates.
- Tool-call confirmation. Per 25 §Tool-call patterns + 27's
  structured output rendering — the assistant proposes a tool
  call; the user confirms. The confirmation copy ("This will send
  an email to <recipient>. Continue?") is system-shaped; the
  tool-call's specific parameters fill the parameter slots. Content
  tokens carry the confirmation templates.
- Adaptive-UI content. Per 26 / 27 — adaptive interfaces compose
  components per render via LLM. The components' content (the
  microcopy in each rendered component; the copy in adaptive
  empty-states / loading-states / refusal-states) is system-shaped
  — the LLM composes from the system's content tokens, not from
  ad-hoc strings. The variability-by-design problem (per 26's
  residual gap on purpose-built authoring tooling for variability)
  applies to content as well as visual: the designer specifies a
  *space* of possible content outputs and reviews the *distribution*
  of what the LLM produces. Content tokens are the boundary the
  variability operates within.

6. The UX Copywriter role at engagement scale

- The case for the UX Copywriter as a system-level role. Per 04
  §Our POV — the CareCentrix 2026 commercial standard names a
  UX Copywriter at 75 fixed hours integrated into component
  documentation. The role is named but not justified — the 75
  hours is a CareCentrix-specific number; what justifies more
  or fewer hours; what the role owns end-to-end at system scale;
  how the role hands off to client product teams; how content
  guidelines get maintained after handoff — none of this is
  articulated.
- What the role owns end-to-end at system scale. **Content
  architecture.** The voice-and-tone matrix (§2); the content-
  token catalogue (§3); the i18n content strategy (§4); the
  AI-surface content layer (§5). **Content production.** The
  system-level content (matrix, tokens, templates, AI-surface
  copy) per 04 §Document intent. **Content review.** Per-component
  content guidance review; pre-merge PR review for content changes;
  release-readiness content audit. **Cross-functional coordination.**
  Localisation vendor coordination per §4; legal review for
  disclosure copy per §5; brand-team review for voice-and-tone
  matrix evolution. **Documentation.** The content-guidelines
  surface in the docs site; the content-token catalogue
  documentation; the per-component content guidance per 29 §14.
- The hour-justification model. The CareCentrix 75 hours is a
  Pattern 2 (Figma-only handoff per 00d) standard-complexity
  number. At engagement scale, the role's hours scale with three
  drivers: **component count** (~0.5–1 hour per component for
  the per-component content guidance); **content-surface
  complexity** (AI surfaces add ~20–40 hours per AI pattern
  family — chat / streaming / refusal / citation / tool-call;
  multi-locale adds ~30–60 hours per locale beyond the source);
  **content-token catalogue depth** (a deep catalogue with
  CTA / error / empty-state / loading / confirmation token
  families adds ~40–80 hours; a thin catalogue with errors
  only adds ~15–25 hours). The CareCentrix 75 hours fits roughly
  20–25 components, English-only, no AI surfaces, a thin token
  catalogue. The practice's discipline: scope the role against
  the three drivers; quote a range (40–250 hours per Build) with
  the driver mix making the case for the chosen point in the
  range.
- When a system needs the role at all. Below ~10 components, the
  role doesn't pay back — the content guidance is thin enough
  for the senior visual designer or UX designer to author
  directly. Above ~10 components, content drift becomes visible
  by release; above ~20 components, content drift becomes a
  failure mode (per 04 §Stale documentation). At ~20+ components,
  the role pays back; below, it's over-engineering.
- Handoff to client product teams. The role hands off three
  things at engagement end: the voice-and-tone matrix as a
  governed artefact (the client's content team owns evolution);
  the content-token catalogue as a maintained primitive (the
  client's engineering team consumes; the client's content
  team authors token additions); the per-component content
  guidance per 29 §14 (consumed by the client's product teams).
  The handoff is incomplete without the governance contract —
  who reviews matrix changes; who approves token additions;
  who coordinates localisation. This is content's analogue to
  the 07 contribution-model handoff at the component layer.
- The Run-phase parallel. Per 33 §5 — white-label-for-resellers
  ships a run-phase retainer with three SLAs. Bespoke
  engagements with a content-system handoff can ship an
  analogous content-retainer (matrix-evolution coordination;
  token-addition review; localisation coordination); the same
  retainer-shape as 33 §5 but applied to the content layer.
  Content is one of the natural Run-phase retainer surfaces
  the practice has not yet articulated.
- Connection to 00e team-and-discipline. The UX Copywriter is
  the content-side analogue to 00e's design-technologist
  archetype — a hybrid role that crosses content / design /
  engineering boundaries. The hiring signal (writing fluency
  + design-system literacy + i18n awareness + AI-surface
  fluency) is not yet articulated in 00e; this section
  surfaces it as a 00e residual.

7. Integration — deepen 04, plus targeted additions to 23 and 13

- The slot decision committed in this prompt. The synthesis
  path is **deepen 04, not a new file.** The reason: §1.31 is
  bounded scope per 09; the content-at-system layer is one or
  two H2 sections in 04 alongside the existing 04 architecture
  (which already covers the per-component half cleanly). A new
  file (e.g., `35-content-systems.md`) is over-commitment to
  content-as-practice-IP at this stage; the practice ships
  content as a layer of documentation rather than as an
  independent productisation companion.
- What lands in 04. Two new H2 sections: **Content as a system
  layer** (covering §§1–5 above — the voice-and-tone matrix,
  content tokens, i18n content depth, AI-surface content) and
  **The UX Copywriter role at engagement scale** (covering §6).
  The new sections sit between 04's existing Cluster-6
  Documentation-as-sales-surface and the Our-POV section.
- What lands in 23. The typography composite-token's
  `$description` field carries voice intent — extending 23's
  brand-voice-as-system-constraint discipline into a
  tokens-with-descriptions discipline that crosses the typography
  / content boundary. One inline addition to 23's §The shape of
  a typography token set or §DTCG composite typography tokens.
- What lands in 13. The content-token i18n discipline ties back
  to component content guidelines via ICU MessageFormat. One
  inline addition to 13's existing message-format coverage,
  pointing at the new 04 system-level content section as the
  content-token authoring layer.
- See also block in the new 04 sections. Cross-references to 23
  (typography-as-voice); 13 (i18n content); 25 / 26 / 27 (AI-
  surface content); 29 §14 (per-component content); 30 (content
  in the authored half of the pipeline); 24 / 33 (multi-brand /
  white-label voice-and-tone-as-Theme-Schema-input); 03
  (component-library microcopy seam); 00d (75-hour line item
  justified); 00e (Copywriter as 00e residual).
- The open residual. Some material in this run may surface as
  candidate for spinning out as a new file (e.g., if the run
  produces enough on the AI-surface content layer to justify
  its own slot alongside 25 / 26 / 27). The practice's discipline
  is to land the run as a 04 deepen first; if the AI-surface
  content material grows in subsequent engagements, spin out
  in a future revision. This run commits 04 deepen.

Output format: Structured markdown. Use H2 section headings that match
the seven-section spine above. Synthesize findings — do not list
sources mechanically. Where the field has consensus, state it clearly;
where decisions are context-dependent, provide decision frameworks
rather than declaring a winner. Two synthesis-ready artefacts must
ship: the voice-and-tone matrix shape (per §2 — voice attributes
across the top, tone contexts down the side, body cells specifying
expression) as a sketch the practice carries into scoping; the
content-token DTCG-shaped schema (per §3 — `$value` carrying ICU
template, `$description` carrying voice intent, `$extensions.<vendor>`
carrying locale and parameter shape) as a defensible POV. Flag where
content tooling has known gaps (no DTCG content-token spec; no
major-vendor content-token surface; ICU authoring tooling thin; the
variability-by-design problem applied to content). Where claims
depend on current state — vendor positioning, ICU tooling support,
LLM-based content review tooling — date them and note the
verification path. Include a references section linking to primary
sources (Mailchimp's voice-and-tone matrix at
`styleguide.mailchimp.com/voice-and-tone/`; Shopify Polaris content
guidelines at `polaris.shopify.com/content`; Linear's empty-states
and microcopy patterns; Stripe's error-message taxonomy and copy
guidelines; ICU MessageFormat documentation at
`unicode-org.github.io/icu/userguide/format_parse/messages/`; the
Lokalise / Crowdin / Smartling / Phrase localisation-platform
documentation; the practitioner writing on UX writing in DS work —
Andy Welfle and Michael Metts' *Writing is Designing*, Torrey
Podmajersky's *Strategic Writing for UX*, Erika Hall's writing
where it intersects DS, the practice-grade writing on DS content
work in the EightShapes catalogue if it exists, the GOV.UK style
guide as a public-sector reference, the Atlassian Design System's
content guidelines, IBM Carbon's content guidelines).

Depth: Expert audience. Do not explain what voice-and-tone is at the
basic level, what microcopy is, what design tokens are, what ICU
MessageFormat does at the basic level, what DTCG is, what `.ai.json`
is, what the per-component template is — explain how the practice
operates the content-at-system layer as a discipline at agency scale,
where content tokens are a defensible primitive vs. where they are
over-engineering, where the field's content tooling has known gaps,
what the UX Copywriter role owns end-to-end and how it staffs at
engagement scale, and how this layer relates to (but does not
replace) the per-component content guidance covered in 04 / 29 / 03.
