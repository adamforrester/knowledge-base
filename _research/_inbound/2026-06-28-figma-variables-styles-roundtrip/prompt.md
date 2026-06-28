You are researching **Figma Variables vs. Figma Styles, and the code → Figma
round-trip** for a senior design systems practitioner at a digital agency. The
output is a structured knowledge document.

This fills a specific blind spot in our existing Figma coverage. Our practice
notes already handle Figma Variables well at the practice level (collection
tiers, modes, mode-multiplication, scoping as governance, the Variables-vs-
Tokens-Studio trade-off, composite-type maturity in DTCG). What they do **not**
cover is the harder, more technical seam that a token-*generation* engine hits
when it tries to push generated tokens back into Figma: that **typography and
shadows are Figma _Styles_, a different object class from Variables**, that
several token types have no Figma home at all, and that writing variables back
into Figma is gated and lossy in specific, citable ways. We are building an
engine that generates a complete token layer (colour, dimension, typography,
shadow, motion) and will eventually need to emit it *into* Figma — so we need
the real mechanics, not the practice-level summary.

This is not an introductory guide — assume the reader knows what design tokens,
Figma Variables, modes, collections, and DTCG are, and knows the Figma→code
export direction. Explain the non-obvious implications for a code→Figma writer,
not the basics.

Research scope — cover all of the following. Verify every load-bearing claim
against **current** primary documentation (developers.figma.com Plugin API +
REST API; help.figma.com; the DTCG spec; tool docs for Tokens Studio / Style
Dictionary / Supernova). Today is 2026-06-28; date anything version- or
plan-dependent and give its verification path.

1. **Why this is a Variables-vs-Styles problem, not a naming problem.**

   - The Figma variable type ceiling: the exact `resolvedType` set and the
     absence of any composite/array/dimension-with-unit/expression type.
   - That a "dimension" is a unitless FLOAT and a typography/shadow "token" is
     not expressible as a single variable at all.
   - Why this forces composite design tokens out to either Figma Styles or a
     third-party layer.

2. **The variable model in detail.**

   - The full `VariableScope` enum, enumerated, and which scopes are valid for
     which `resolvedType`.
   - Scoping semantics (UI-picker filter only — does NOT prevent programmatic
     binding), `codeSyntax` (WEB/ANDROID/iOS), and known limits.
   - Collections, modes, per-plan mode caps and the hard platform caps
     (modes/variables per collection), one-mode-dimension-per-collection.

3. **Figma Styles as a distinct object class.**

   - The four style types (Paint, Text, Effect, Grid) and that they are stored
     and created separately from variables.
   - Which style sub-properties can bind to variables today (text font
     properties; effect colour and which effect numerics) and which remain
     literal-only.
   - The concrete consequence: a DTCG composite `typography`/`shadow` decomposes
     to atomic variables + a Style that binds them; `transition`/`duration`/
     `easing`/`spring` have no Figma variable OR style home (motion lives in
     prototype settings, not tokens).

4. **Writing tokens back into Figma (code → Figma).**

   - REST Variables API read/write endpoints and the **plan gate** (is write —
     or read — Enterprise-only?). This is the single most important constraint;
     be definitive and cite it.
   - The POST payload model (collections/modes/variables/values, tempId, action
     verbs) and the 4MB request limit.
   - The Plugin API write path as the any-plan alternative, and the interactive
     vs headless/CI trade-off.
   - Whether styles can be CREATED via REST or only via the Plugin API.

5. **Idempotent re-import: update-in-place vs build-from-scratch.**

   - How `VariableID`s work; matching existing variables by name to update in
     place (preserving IDs so component bindings + aliases survive) vs creating
     fresh (new IDs, broken bindings).
   - What the REST POST API supports for updating existing entities by id.
   - Strategies tools use to make re-import idempotent.

6. **The export/import JSON shape and the ecosystem.**

   - The official REST `variables/local` response schema (colour as RGBA float
     object; alias as `{type:"VARIABLE_ALIAS", id}`; `valuesByMode`, `scopes`,
     `codeSyntax`, `variableCollections`).
   - De-facto community export/import plugin JSON conventions (slash-delimited
     names, mode-keyed values) and how close they are to a `variables[]` +
     `$collection`/`$mode` shape.
   - How Tokens Studio, Style Dictionary, Supernova, and Figma's own import
     handle code→Figma, and where each is lossy.

7. **What a code→Figma writer must therefore produce.**

   - Beyond a `variables[]` array: the "style manifest" needed to recreate
     typography/shadow Styles and bind them to atomic variables.
   - An honest taxonomy of each token category → its Figma disposition
     (1:1 variable / style-part atom / no Figma home).

Output format: Structured markdown with section headings matching the numbered
scope above. Synthesize findings — do not list sources mechanically. Where the
field has consensus, state it; where decisions are context-dependent, give a
decision framework rather than declaring a winner. Flag every place a DS tool
(Figma, Style Dictionary, Tokens Studio, code pipeline) has a known gap that
practitioners work around. Where a claim depends on current platform state —
feature names, plan gates, version flags, numeric caps — date it and note the
verification path. Include a references section linking to primary sources
(Figma Plugin API, Figma REST API, Figma Help, W3C DTCG, tool docs).

Depth: Expert audience. Do not explain what a variable, mode, or token is —
explain the round-trip mechanics, the plan gates, and the decomposition a
composite token must undergo to survive a code→Figma write.
