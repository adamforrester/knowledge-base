# Research intake — what should a machine-readable "content model" for a UI component contain?

> Brief supplied 2026-08-20, feeding a schema design decision in the Prism3 engine repo. Reproduced
> here so both agents receive identical input. Findings report; the proposed schema is one section.

---

**The problem.** A component definition today carries copy guidance as free prose —
`content: { labelPattern?, errorPattern?, emptyPattern? }` — which is useful to a writer and
**structurally incapable** of answering the question a page-level composition needs to ask:
*"Can this component hold a 60-character heading and an image — and what happens at 200 characters?"*
Cardinality, type, constraint and overflow cannot live in a string. The proposal is a typed sibling
field, `contentModel`, carrying exactly those. Its shape is undecided.

**Forcing constraint:** ~17 more components are about to be authored. Deciding the shape now is small;
deciding it afterwards means revising every component and every downstream projection.

**Three consumers, wanting different things:** a page-composition layer ("blocks") that needs to know
what a component can hold before placing content; the delivery platforms, whose own component
definitions the projection must generate; and an AI agent that needs the constraints without reading
the implementation.

**Delivery platforms:** Drupal Single Directory Components and Adobe AEM Edge Delivery Services /
Universal Editor. Both server-render HTML.

**The questions.**

1. **Drupal SDC — what does `component.yml` actually express?** The closest prior art and the most important question. Document the `props` schema (which JSON Schema subset?), `slots`, required vs optional, enums, defaults. Then the critical part: **does it express cardinality, length constraints, or overflow behavior at all?** If not, say so explicitly and show what authors do instead. Quote the schema definition.
2. **AEM — what does the Universal Editor / Edge Delivery component model express?** The component definition JSON, the block/section content model, how a block declares what content it accepts. How would an author describe "this block takes a heading, up to three cards, and an optional image"? Quote the actual model format.
3. **What do headless CMS content models have that component schemas do not?** Compare Sanity, Contentful, Strapi and Adobe Content Fragment Models on field types, cardinality, length constraints, validation rules, required/optional. Name what transfers and what does not.
4. **Overflow — is there prior art at all?** Does anything declare overflow behavior (truncate / ellipsis / wrap / scroll / clamp-to-N-lines) as **data** rather than leaving it to CSS? Search hard; if the answer is genuinely "nothing does this," report it plainly rather than stretching a weak example.
5. **Adjacent schemas.** Custom Elements Manifest, Storybook `argTypes`, Figma component properties. What does each capture about content and what does it deliberately omit? Figma matters because any content model must survive projection into its small fixed property vocabulary.
6. **The falsification question.** A plausible answer is that `contentModel` is **redundant** — that typed `props` plus named `slots` already answer everything a composition layer needs. Argue that case as strongly as possible, then argue against it. What specifically can a composition layer *not* learn from props + slots alone?
7. **Synthesis.** Propose a minimal `contentModel` — the smallest set of fields that satisfies what SDC and AEM require, answers the 60-vs-200 question, and survives projection into Figma. Prefer fewer fields with clear semantics over a comprehensive model nobody fills in correctly.

**Output:** structured by question; every claim with a URL, access date, and direct quotation where
load-bearing; schema examples real, not composed. Then **VERIFIED** / **INFERRED** / **COULD NOT
VERIFY**, the last being specific and as valuable as the others. Finish with the proposed schema as a
concrete type with one worked example (a card with heading, body, optional image, up to two actions),
the strongest argument that the field should not exist at all, and what is deliberately excluded.

**Rules:** do not invent citations, schema fields or format examples. Where the two platforms disagree,
report the disagreement rather than reconciling it. Where documentation and source code differ, source
code wins; cite both. Prefer primary sources.
