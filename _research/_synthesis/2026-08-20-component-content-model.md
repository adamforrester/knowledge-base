# Synthesis — machine-readable component content model

> **Single-source.** Unlike its two sibling runs from the same day, this brief was run against one
> agent only (`claude.md`); there is no `external-agent.md` to reconcile against. Recorded here
> rather than left to be inferred from a missing file, because the dual-agent convention exists
> precisely so that convergence and divergence are visible, and a single run offers neither.
> Not authoritative; synthesis scratch.

---

## What the run establishes, and why it reverses the brief

The brief was written expecting component schemas mostly not to have solved content shape, and
expecting headless CMS models to be where the prior art lived. **The opposite is true, and the
evidence is a single line in Drupal's core schema:**

`propDefinition` is `{"$ref": "http://json-schema.org/draft-04/schema#"}`.

SDC did not design a content vocabulary. It **inherited** one — and with it `maxLength`, `enum`,
`default`, `required` and the entire draft-04 validator ecosystem. `slotDefinition` adds `minItems`,
`maxItems` and `expected` on top.

So the shape the brief proposed — prose `content` plus a typed `contentModel` sibling — is wrong at
the level of structure, not detail. The move is to **adopt draft-04 semantics rather than invent a
parallel field**, and carry only what draft-04 genuinely cannot hold.

## The finding that generalises beyond this topic

**Drupal's documentation is poorer than Drupal's schema.** The official annotated `component.yml`
walkthrough never mentions `minItems`, `maxItems` or `expected`. Read the docs and you would conclude
SDC has no cardinality at all.

This is the second time in one day that going to shipped source found what documentation could not —
the other being the Salesforce Lightning stylesheet count in the surface-context runs. Worth
promoting to a working practice: **when a documentation search comes back thin on a system that
plainly ships the capability, read the schema or the compiled output before recording a null.**

## The null result, established rather than assumed

Overflow behaviour — *what happens at 200 characters* — exists nowhere as schema data. Zero
constraint keywords across the 48KB Custom Elements Manifest schema, none in SDC's, none in Figma's
property vocabulary. It lives as CSS, as per-library props, and as prose for humans.

The run established this **by inspection rather than by failing to find things**, which is what makes
it usable. A search that returns nothing and an inspection that returns zero are different epistemic
objects, and only the second supports a claim.

## Where the run argues against its own proposal, and partly wins

Props plus slots genuinely answer cardinality and type. What they cannot answer is **design intent
versus hard limit**: `maxLength: 200` says *invalid at 201*, not *designed for 60, degrades to 200*.
That gap is real and is the only thing the proposal needs to carry.

The run's own strongest counter — that SDC already has a better schema, and two extension keywords on
the prop would inherit draft-04's tooling for free — follows Drupal's own precedent with
`x-translation-context`.

**One refinement this synthesis adds:** the two proposed keywords are not equally supported.
`x-target-length` rests on the Q6 reasoning above. `x-overflow` rests on nothing — it is the one
field the run's own null result shows has no prior art anywhere, and no component currently asks for
it. Ship the first; defer the second until a real component demonstrates the shape it wants.

## Flags

- **The decisive gap is unresolved and the run says so:** whether SDC's `minItems`/`maxItems` are
  enforced at render or merely advisory. The schema says a slot *"should accommodate"* that many. If
  advisory, real SDC components likely do not populate these keys, and "standardised" quietly becomes
  "specified and unused" — a much weaker reason to adopt. It does not block using the vocabulary; it
  changes how much weight the precedent carries.
- **Section 3 is a two-system comparison, not the four the brief asked for.** Contentful (HTTP 429),
  Strapi, Adobe Content Fragment Models and Storybook `argTypes` all went unverified.
- **AEM cannot express the test case.** Its only cardinality primitive is a boolean `multi`, so
  `max: 3` reaches SDC intact and reaches AEM as `multi: true`, destroying the number. Reported as a
  disagreement to serve separately rather than reconciled — which is right. Do not lower the schema
  to AEM's floor.
- **Correction to the brief:** Figma has five component property types, not the four the prompt
  stated — Slot was added. Unexamined consequence: we carry `slots` in the component schema and
  nobody has checked whether the Figma projection should be using it.

## Open

Whether a second agent should be run against this brief before anything is promoted. The two sibling
runs both produced material divergence, and on Drupal specifically the external agent contradicted
itself between its own two runs — so a second pass here is not ceremony.
