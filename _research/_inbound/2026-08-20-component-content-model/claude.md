# Claude run — what should a machine-readable content model for a UI component contain? (2026-08-20)

Raw output. Every URL opened **2026-08-20**. Quotations verbatim; schema fragments are pasted from the
source files, not composed.

**The headline finding reverses the brief's premise on one point.** The brief expects component schemas
mostly not to have solved content shape. **Drupal SDC has** — slots carry `minItems`, `maxItems` and an
`expected` component list, and props are full JSON Schema draft-04, so length constraints come free by
inheritance. AEM has not. That asymmetry, not the CMS comparison, is the thing that should drive the
design.

---

## 1. Drupal SDC — what `component.yml` actually expresses

Source of record: `core/assets/schemas/v1/metadata.schema.json` on the `11.x` branch —
`raw.githubusercontent.com/drupal/drupal/11.x/core/assets/schemas/v1/metadata.schema.json` (6,995 bytes).
Read as the schema file, which per the brief's rule outranks the prose docs.

Top-level properties: `$schema`, `name`, `description`, `status`, `noUi`, `props`, `slots`, `variants`,
`tags`, `libraryOverrides`, `thirdPartySettings`.

### props — full JSON Schema draft-04, plus two Drupal extensions

```json
"propDefinition": {
  "$ref": "http://json-schema.org/draft-04/schema#",
  "meta:enum": { "type": "object", "minItems": 1, "uniqueItems": true,
    "patternProperties": { "additionalProperties": false, "^[a-zA-Z0-9_-]*$": { "type": "string" } } },
  "x-translation-context": { "type": "string", "title": "Translation Context" }
}
```

**Which subset? None — it is the whole of draft-04 by `$ref`.** So `type`, `enum`, `default`, `required`,
`minLength`, `maxLength`, `pattern`, `minimum`/`maximum`, `minItems`/`maxItems` on arrays are all
available on a prop without Drupal defining any of them. The two additions are Drupal's own:
`meta:enum` (human labels for enum values) and `x-translation-context`.

### slots — and this is the part that reverses the premise

```json
"slotDefinition": {
  "type": "object", "additionalProperties": false,
  "patternProperties": { "^[a-zA-Z0-9_-]+$": { "type": "object", "properties": {
    "title": { "type": "string", "title": "Title" },
    "description": { "type": "string", "title": "Description" },
    "examples": { "type": "array", "items": { "type": "string" } },
    "expected": { "type": "array", "title": "Expected components",
      "description": "List of components / component tags that are expected to be put into this slot.",
      "items": { "type": "string", "title": "Expected component item",
                 "description": "A component ID or tag." } },
    "minItems": { "type": "integer", "minimum": 0, "title": "Minimum number of items",
      "description": "The minimum number of items a slot should accommodate" },
    "maxItems": { "type": "integer", "minimum": 1, "title": "Maximum number of items",
      "description": "The maximum number of items a slot should accommodate" }
  } } }
}
```

**So SDC expresses, natively:**

| Question | SDC answer |
|---|---|
| Cardinality | **Yes** — `minItems` / `maxItems` per slot |
| What may go in a slot | **Yes** — `expected`, a list of component IDs or tags |
| Length constraints | **Yes, on props** — `maxLength`/`minLength` inherited from draft-04 |
| Required vs optional | **Yes** — draft-04 `required` on props; slots are optional by construction |
| Enums + defaults | **Yes** — draft-04, plus `meta:enum` for labels |
| **Overflow behavior** | **No.** Zero occurrences of `overflow`, `truncat`, or any equivalent in the file |

**Docs-versus-source divergence, reported per the rules.** The official annotated walkthrough
(`drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml`,
accessed in an earlier pass and re-read for this one) documents slots as *"The key is the name of the
slot. In your template you will use `{% block body %}`"* and says of props *"If your component has
required properties, you list them here."* **It does not mention `minItems`, `maxItems` or `expected`
anywhere.** The schema is richer than the documentation that introduces it. Source wins; an author
reading only the docs would conclude SDC has no cardinality.

**One caveat I am flagging rather than smoothing:** the descriptions say a slot *"should accommodate"*
that many items — permissive language. Whether Drupal's render pipeline **enforces** min/max at render
time, or whether these are advisory hints for authoring UIs, is not answered by the schema file and I
did not verify it. See COULD NOT VERIFY.

---

## 2. AEM — Universal Editor / Edge Delivery component model

`aem.live/developer/component-model-definitions`. Three artifacts.

**Component definition** — what can be inserted:

```json
{
  "title": "Hero",
  "id": "hero",
  "plugins": { "xwalk": { "page": {
    "resourceType": "core/franklin/components/block/v1/block",
    "template": { "name": "Hero", "model": "hero" }
  } } }
}
```

**Component model** — the authorable fields:

```json
{
  "id": "hero",
  "fields": [
    { "component": "reference", "valueType": "string", "name": "image",
      "label": "Image", "multi": false }
  ]
}
```

Field `component` types referenced on the page: `reference`, `text-input`, `text-area`, `multiselect`,
`select`, `toggle`, `richtext`, `aem-content`, `container`.

**Component filters** — what a container accepts. Per Adobe's Universal Editor filtering documentation
(`experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/universal-editor/filtering`),
the structure is an allow-list keyed by container id:

```json
{ "id": "section", "components": [ "text", "image", "button", "title", "hero", "cards", "columns", "quote" ] }
```

### Answering the brief's own test case

> *"this block takes a heading, up to three cards, and an optional image"*

- **a heading** — a `text-input` field. Expressible.
- **an optional image** — a `reference` field, absent when unset. Expressible.
- **up to three cards** — **not expressible.** Filters carry an allow-list of component ids and **no counts**. The only cardinality primitive on a field is `"multi": false` — a **boolean**. AEM can say *"cards are allowed here"* and *"this field takes many"*. It cannot say *three*.

**No length constraints and no overflow behavior are documented on any field type.**

### The disagreement, reported rather than reconciled

| | Drupal SDC | AEM UE/EDS |
|---|---|---|
| Cardinality | `minItems` / `maxItems` (integers) | `multi` (boolean) |
| Allowed children | `expected` (per slot) | `components` (per filter, per container) |
| Length | draft-04 `maxLength` on props | not documented |
| Overflow | none | none |

**The projection cannot serve both from one number without loss.** `max: 3` projects to SDC exactly and
to AEM as `multi: true` — the "3" is destroyed. That loss should be recorded at the projection site, not
papered over.

---

## 3. What headless CMS models have that component schemas do not

**Sanity** — `sanity.io/docs/validation`. Chained rule builders, verbatim example from the page:

```ts
defineField({
  title: 'Title',
  name: 'title',
  type: 'string',
  validation: rule => rule.required().min(10).max(80)
})
```

`required()`, `min()`, `max()` on string length. **Nothing on overflow or truncation** — the page
carries no such concept. Array item-count validation is not covered on that page (see COULD NOT VERIFY).

**Contentful, Strapi, Adobe Content Fragment Models** — see COULD NOT VERIFY. I got a 429 from
Contentful and did not reach the other two, so I am making **no claims** about their validation
vocabularies rather than reciting what I believe them to be.

### What transfers and what does not — INFERRED

**Transfers:** `required`, min/max length, min/max item counts, enums, defaults. These are exactly the
draft-04 vocabulary SDC already inherits, which is the point: **the CMS world and the SDC schema have
converged on the same primitives**, so adopting them costs nothing in novelty.

**Does not transfer:** a CMS validates *content being authored* and can reject it. A component schema
describes *what a component can hold* and rejects nothing at render time. So a CMS `max(80)` is an
enforcement boundary, and the same number in a component definition is a **design intent** — which is
why the 60-versus-200 question needs two numbers, not one (§7).

---

## 4. Overflow — is there prior art at all?

**Searched hard. The honest answer: overflow exists as a CSS property and as a per-library component
prop. It does not exist as a field in any component definition schema I examined.**

Verified nulls, by direct inspection rather than by failing to find:

- **Drupal SDC metadata schema** — 0 occurrences of `overflow`, `truncat`, or any synonym.
- **Custom Elements Manifest schema** — 0 occurrences of `overflow`, `truncat`, `maxLength`, `minLength`, `maxItems`, `minItems` across all 48,735 bytes.
- **AEM field types** — no overflow among the documented `component` values.
- **Figma component properties** — documented as not supporting constraint mechanisms at all (§5).

What **does** exist, and is a different layer:

- **CSS**: `line-clamp`, and the `max-lines` / `block-ellipsis` longhands discussed in the CSS Overflow work (W3C www-style archive, *"Minutes Berlin F2F 2018-04-12 … [css-overflow]"*).
- **Component props in individual libraries**: e.g. `vue-clamp`'s `maxLines`.
- **Design-system *pattern* pages**: Carbon publishes an "Overflow content" pattern; SLDS publishes a "Line clamp" page. **These are guidance for humans, not machine-readable fields.**

**This is the significant finding the brief anticipated.** Nothing in the schema tier declares overflow.
Any `overflow` field in the proposal is therefore **novel**, with no prior art to copy and no projection
target that consumes it — which is an argument for keeping it very small, and for being honest that its
only consumer today would be our own documentation and Figma sample-content generation.

---

## 5. Adjacent schemas

**Custom Elements Manifest** — `raw.githubusercontent.com/webcomponents/custom-elements-manifest/main/schema.json`.
The complete `Slot` definition:

```json
"Slot": {
  "properties": {
    "deprecated": { "type": ["string","boolean"], "description": "Whether the slot is deprecated.\nIf the value is a string, it's the reason for the deprecation." },
    "description": { "type": "string", "description": "A markdown description." },
    "name": { "type": "string", "description": "The slot name, or the empty string for an unnamed slot." },
    "summary": { "type": "string", "description": "A markdown summary suitable for display in a listing." }
  },
  "required": ["name"], "type": "object"
}
```

**Four fields, three of them prose.** CEM describes a component for *documentation and tooling
discovery*; it deliberately omits every constraint. Zero constraint keywords in the whole file.

**Figma component properties** —
`help.figma.com/hc/en-us/articles/5579474826519-Explore-component-properties`. **Correction to the
brief's premise:** the vocabulary is **five** types, not four. Boolean, Instance swap, Text, Variant,
and **Slot** — the last described as *"a flexible area in a component where you can add, edit, and
rearrange content."*

The documented limits: no numeric constraints, no maximum length, no child counts, no overflow. One
explicit content limit is stated — *"Text component properties currently don't support rich text — such
as lists styles, superscript, and other type settings."*

**Storybook `argTypes`** — not verified in this run. See COULD NOT VERIFY.

---

## 6. The falsification question

### The case that `contentModel` is redundant — argued as strongly as I can

**On the platform that matters most, it demonstrably is.** SDC already carries `minItems`, `maxItems`,
`expected` on slots and the whole of JSON Schema draft-04 on props. If the definition simply authored
SDC-shaped props and slots, it would get cardinality, allowed-child types, length, enums, defaults and
required **for free, in the target platform's own vocabulary, with no translation layer and no
information loss on the richest target.** A parallel `contentModel` field would restate what `props`
and `slots` already say, in a second vocabulary, which then has to be kept in agreement with the first —
and a second statement of the same fact that nothing checks is drift with extra steps.

**The composition layer's question is mostly answerable from props + slots.** "Can this hold a heading
and an image?" is `slots.heading` and `props.image` existing. "How many cards?" is `slots.items.maxItems`.
Those are the two questions a page-composition layer actually asks most of the time, and both are
already expressible.

**And the field will be filled in badly.** Seventeen components authored against an under-specified
optional field produces seventeen different interpretations — which is the drift this project closes
vocabularies to prevent. An unfilled or wrongly-filled `contentModel` is worse than no field, because a
composition layer that reads it will trust it.

### The case against redundancy — what props + slots genuinely cannot say

1. **Design intent versus hard limit.** `maxLength: 200` says the string is invalid at 201. It does not say the component was *designed for 60* and *degrades* between 60 and 200. The brief's own question — *"can it hold 60, and what happens at 200"* — is two facts, and JSON Schema has vocabulary for exactly one of them. This is the strongest argument for the field and it is not answerable by any existing platform vocabulary.
2. **Overflow has no home anywhere** (§4). If it is to be data, it is a new field by necessity.
3. **AEM cannot hold the number.** Authoring SDC-shaped slots means the AEM projection silently degrades `maxItems: 3` to `multi: true`. A neutral field makes the loss explicit at the projection boundary instead of hiding it in a platform-specific source.
4. **Figma needs a number neither platform has.** To generate honest sample content, the Figma projection needs the *target* length — 60 — not the maximum. A component filled with 200 characters of lorem in the design kit misrepresents the design.

**INFERRED conclusion:** the redundancy argument wins on cardinality and type, and loses on
**length-with-intent** and **overflow**. That should shape the proposal: do not restate what props and
slots already say. Add only what they cannot.

---

## 7. Synthesis — the proposed schema

Minimal by design: one map, six keys, most optional. **It deliberately does not restate cardinality that
`props`/`slots` already carry when the def is authored SDC-shaped** — it carries the two things nothing
else can hold, plus the minimum context needed to project them.

```ts
/** What each named content region can hold. Keyed by slot/prop name already declared elsewhere. */
type ContentModel = Record<string, {
  /** What kind of thing goes here. Decides the projection target. */
  kind: 'text' | 'richtext' | 'media' | 'component' | 'action';

  /** Item counts. Omit for single-value regions. Projects to SDC minItems/maxItems;
   *  to AEM as `multi: (max ?? 1) > 1` — the exact number is LOST there, by design. */
  min?: number;
  max?: number;

  /** Component ids permitted here. Projects to SDC `expected` and to an AEM filter entry. */
  accepts?: string[];

  /** THE 60-VS-200 FIELD, and the reason this type exists.
   *  `target` is what the component was designed to hold — the number the Figma projection
   *  generates sample content at, and the number a composition layer plans against.
   *  `max` is where it breaks. Both are counts of characters. */
  length?: { target: number; max?: number };

  /** What happens past `length.target`. NO PRIOR ART — see §4. Consumed today only by our own
   *  docs and the Figma projection; no delivery platform accepts it. */
  overflow?: 'wrap' | 'clamp' | 'truncate' | 'scroll';
  /** Line count when overflow is 'clamp'. */
  clampLines?: number;
}>;
```

### Worked example — a card with a heading, body, optional image, up to two actions

```ts
contentModel: {
  heading: {
    kind: 'text',
    length: { target: 60, max: 120 },
    overflow: 'clamp',
    clampLines: 2,
  },
  body: {
    kind: 'text',
    length: { target: 160, max: 320 },
    overflow: 'clamp',
    clampLines: 3,
  },
  media: {
    kind: 'media',
    max: 1,                       // optional: absent when unset
  },
  actions: {
    kind: 'action',
    min: 0,
    max: 2,
    accepts: ['button', 'link'],
  },
}
```

**How each field projects:**

| Field | SDC | AEM | Figma |
|---|---|---|---|
| `kind: text` | prop, `type: string` | `text-input` field | **Text property** |
| `kind: component` + `accepts` | slot + `expected` | filter `components` entry | **Slot property** |
| `min` / `max` | `minItems` / `maxItems` | `multi: true` — **number lost** | not expressible — **lost** |
| `length.max` | prop `maxLength` | not expressible | not expressible |
| `length.target` | not expressible | not expressible | **sample-content length** |
| `overflow` | not expressible | not expressible | not expressible |

**Three of six fields have no platform consumer.** That is stated rather than hidden, and it is the
honest cost of the proposal.

---

## VERIFIED

All accessed 2026-08-20.

- SDC `propDefinition` is `{"$ref": "http://json-schema.org/draft-04/schema#"}` plus `meta:enum` and `x-translation-context` — drupal/drupal `11.x` `core/assets/schemas/v1/metadata.schema.json`
- SDC `slotDefinition` carries `title`, `description`, `examples`, `expected`, `minItems`, `maxItems`, with the descriptions quoted above — same file
- SDC schema contains no overflow/truncation vocabulary — same file, tested by direct string search
- SDC top-level keys: `$schema`, `name`, `description`, `status`, `noUi`, `props`, `slots`, `variants`, `tags`, `libraryOverrides`, `thirdPartySettings` — same file
- AEM component definition, model and field-type list, with the `hero` examples quoted — aem.live/developer/component-model-definitions
- AEM model field carries `multi` as its only cardinality primitive — same page
- AEM filter shape `{ "id": "section", "components": [...] }` — Adobe Universal Editor filtering documentation
- Sanity `rule.required().min(10).max(80)` on a string field — sanity.io/docs/validation
- Custom Elements Manifest `Slot` has exactly `deprecated`, `description`, `name`, `summary`, `required: ["name"]`; zero constraint keywords in the 48,735-byte schema — webcomponents/custom-elements-manifest `schema.json`
- Figma component properties are **five** types — Boolean, Instance swap, Text, Variant, **Slot** — with no documented numeric, length, count or overflow constraint; and *"Text component properties currently don't support rich text…"* — help.figma.com 5579474826519
- CSS `line-clamp` and the `max-lines`/`block-ellipsis` longhands are discussed in W3C CSS Overflow minutes (www-style archive, Berlin F2F 2018-04-12)

## INFERRED

- The SDC-versus-AEM comparison table, and the claim that `max: 3` cannot survive projection to AEM — reasoning from `multi` being boolean.
- That CMS validation and component-schema constraint are **different acts** (enforcement vs design intent), and therefore that the 60/200 question needs two numbers.
- That the redundancy argument wins on cardinality/type and loses on length-with-intent and overflow — my adjudication of §6.
- The projection table in §7, except the Figma Slot/Text rows which follow directly from the five documented property types.
- That `length.target` is the number Figma sample content should be generated at. Nobody documents this; it is my inference from Figma having no constraint vocabulary but needing *some* content length.

## COULD NOT VERIFY

Specific about what was attempted.

- **Whether SDC's `minItems`/`maxItems` are ENFORCED at render or advisory.** The schema descriptions say a slot *"should accommodate"* that many. I did not find the render-pipeline behavior and did not test it. **This materially affects how much weight to put on §1** — if advisory, SDC's cardinality is documentation too.
- **Contentful field validations.** `contentful.com/developers/docs/concepts/data-model/` returned **HTTP 429**. No claims made about Contentful.
- **Strapi** and **Adobe Content Fragment Models** — not reached in this run. No claims made. §3 is therefore a two-system comparison (Sanity + the SDC/draft-04 baseline), not the four-system comparison the brief asked for.
- **Sanity array item-count validation.** The validation page did not cover it; I did not confirm whether `min()`/`max()` apply to arrays.
- **Storybook `argTypes`.** Not fetched. No claims made about what it captures or omits.
- **AEM `component-filters.json` in a real repository.** Probed five plausible paths in `adobe/aem-boilerplate` (`component-models.json`, `component-definition.json`, `component-filters.json` at root; `models/_section.json`; `blocks/cards/_cards.json`) — **all 404**. The filter shape quoted in §2 comes from Adobe's documentation, not from a file I opened. Adobe's docs say the per-block JSON files are compiled into the root files, which likely explains the absence, but I did not confirm the source layout.
- **Any component definition schema that declares overflow.** Searched; found only CSS properties, per-library props, and human-facing pattern pages. Reported in §4 as a null result.

---

## The strongest argument that this field should not exist at all

**Drupal SDC already has the schema, and it is better than the one proposed here.**

`minItems`, `maxItems`, `expected`, plus the entire JSON Schema draft-04 vocabulary on props — that is a
mature, standardised, externally-maintained content model, and it is the native format of the primary
delivery platform. A `contentModel` field is a **second, weaker, home-grown vocabulary describing the
same facts**, which must then be kept in agreement with the first by hand.

The project's own history is the argument: it closes vocabularies precisely because a second statement
of the same fact drifts from the first. `contentModel` *is* a second statement. Author SDC-shaped props
and slots, project *down* to AEM's poorer model, accept the documented loss, and the only thing left
unexpressed is `length.target` and `overflow` — two fields, which could live as extension keywords on
the prop (`x-target-length`, `x-overflow`) exactly as Drupal itself does with `x-translation-context`.
**That is a two-keyword change instead of a new schema, and it inherits draft-04's tooling for free.**

I think that argument is strong enough that it should be tested before the field is built.

## Deliberately excluded from the proposal, and why

- **Rich-text feature lists** (which marks are permitted). Real, but it belongs to the editor configuration, and Figma cannot represent rich text at all — it says so explicitly.
- **Per-breakpoint content variation.** A heading's comfortable length differs at 320px and 1440px. Excluded because it multiplies every entry by the breakpoint count and no platform consumes it.
- **i18n expansion factors.** German runs ~35% longer than English; `length.target` should arguably be a range per locale. Excluded as premature — but it is the most likely first regret.
- **Validation regex / format.** Draft-04 already has `pattern` and `format`; restating them here would be exactly the redundancy §6 warns about.
- **Accessible-name derivation** (which region supplies the component's name). Genuinely missing from every schema surveyed, and a real gap — but it is an accessibility concern, not a content-shape one, and folding it in would blur the field's purpose.
