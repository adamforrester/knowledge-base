# Synthesis — the behaviour half of the vanilla projection (the #882 run)

> Reads the raw run in `_research/_inbound/2026-08-21-vanilla-behaviour-projection/`.
> Path A was used because this feeds a **decision the owner is taking with a developer partner**, and
> the synthesis itself is the deliverable. **Nothing here goes into a numbered file yet** — promotion
> happens after the decision, not before. Filed 2026-08-21.

---

## Read this first: the corroboration this convention exists to produce is missing

`_research/README.md` defines a run as one prompt against **two** agents, precisely so that
convergence can be treated as evidence. **This run has one agent.** No external pass exists, and no
prompt was supplied — the brief was reconstructed from prism3 `#882` and `docs/19` §3 (see
`prompt.md`).

The previous run on this topic (`2026-08-13-component-output-targets`) earned its conclusion by
**two independent agents reaching the same reversal**, and its synthesis said so explicitly. This one
has no such backing. Every claim below is single-pass. Where a claim additionally rests on a single
*source*, it is marked **[single-source]**.

What partly offsets this: the load-bearing findings are **measurements of published code and
documented Baseline status**, not judgements. Anyone can re-open the same URLs and check them. That
is a different kind of reliability from agreement between two agents, and it is the kind this run has.

---

## The bottom line

**Option 1 wins, and it is not the compromise it looks like — it is the native shape of both target
platforms.**

- **AEM Edge Delivery**: every block is a folder with a same-named `.css` and `.js`; the JS "is
  loaded as a module (ESM) and exports a default function that is executed as part of the block
  loading". Buildless, framework-free.
- **Drupal SDC**: a same-named `.js` beside the component auto-loads; `libraryOverrides` takes
  control when needed; `core/drupal` + `core/once` is the documented dependency idiom.

A class-based skin that ships **no** JS is the unusual artefact on both platforms. Option 1 does not
add a layer to these platforms; it fills a slot they already opened.

## The finding that should change how #882 is framed

**#882 has the difficulty ordered backwards.** It names *"`dialog`'s focus trap"* first, as the hard
case. Measured against Adobe's own published block collection and against Baseline:

| behaviour | platform | Adobe's own block |
|---|---|---|
| dialog / focus trap | **native** — `<dialog>` + `showModal()` gives focus, ESC, `inert`, top layer, `aria-modal`; Baseline **widely available since March 2022** | 71 lines, uses `showModal()` |
| accordion | **native** — `<details>`/`<summary>` | 23 lines, converts markup to `<details>` |
| **tabs** | **nothing native** | **47 lines, zero keyboard listeners** — no arrows, no Home/End, no roving tabindex |
| menu | nothing native | **no block exists** |
| select / listbox | `appearance: base-select` is **explicitly not Baseline** | no block exists |

**The hardest-sounding behaviour is free; the easy-sounding one is the gap — and Adobe's reference
implementation does not close it.** Their tabs block is a click handler with ARIA attributes on it.

Two consequences:

1. **The residue is smaller than #882 implies.** After `<dialog>`, `<details>` and invoker commands
   (Baseline newly available **2025-12-12**, giving declarative `show-modal` / `close` /
   `toggle-popover` on `<button>` with no JS), the genuine tranche-4 residue is: **tabs keyboard
   model, menu roving tabindex, combobox/listbox.** Three behaviours, not five.
2. **We would be beating Adobe's floor, not matching it.** That is the right call and worth stating
   as a cost rather than discovering later.

## On option 2 (web components) and option 3 (documented contract)

**Option 2 is not argued against here** — `19` §3 already ranks it 6 and this run found nothing to
disturb that.

**Option 3 has weak prior art and one disqualifying gap.** The ARIA APG already *is* an
implementation-agnostic behaviour contract, published per pattern with keyboard tables, and Adobe
Spectrum demonstrably runs one spec against two implementations **[single-source: search-derived,
individual pages not each fetched]**. But:

- **Nothing in the surveyed literature describes testing that an implementation conforms to a
  published behaviour contract.** The APG ships no conformance suite. The one machine-readable
  component-contract spec found — Design System Contracts, v1.0.1, built 2026-08-17
  **[single-source, no named production adopters]** — covers props, anatomy, tokens, slots and
  "declared events", and **does not cover keyboard interaction or focus management**.

So on current evidence a behaviour contract would be **prose that nothing verifies**. Given this
practice's standing position that an unchecked claim drifts, option 3 cannot stand alone. It can
stand *beside* option 1 — the contract being what the vanilla layer is written against and what a
future React target implements — which is a materially different proposal from #882's option 3.

## The sub-fork option 1 creates, which #882 does not mention

**Choosing option 1 reopens #252 at rank 2**, where `19` §3 currently says it does not reach: author
our own behaviours, or wrap an existing framework-agnostic engine.

And the wrap side may be empty. **Zag.js documents React, Vue 3, Solid and Svelte, and no vanilla
installation path.** Wrapping it from vanilla means writing and maintaining the adapter ourselves,
which is most of the cost of authoring with none of the control.

*A methodological note worth keeping, because it happened inside this run.* An earlier fetch of
Zag's GitHub README concluded vanilla **was** supported, inferring it from the line "The component
interactions are modelled in a framework agnostic way." The installation docs contradict it.
**"Framework-agnostic" in a README describes an architecture, not a supported target** — and a single
fetch of promotional prose produced a confident wrong answer that a second fetch caught. In a
single-agent run, that is the failure mode to watch for; it is the reason the two-agent convention
exists.

## The binding question, which is a separate decision

Three class-based systems, three different conventions for binding behaviour to markup:

| system | binds via |
|---|---|
| GOV.UK Frontend | `data-module` to initialise; **`govuk-js-*` classes** to target elements within; `govuk-*` classes for styling — three distinct hook kinds |
| USWDS | **the styling class itself** (`.usa-accordion__button[aria-controls]`) |
| Bootstrap 5 | `data-bs-toggle` and `data-bs-*` config, the documented *preferred* path |

**There is no field consensus.** For this practice the question is sharper than for any of them,
because the emitted class names are a versioned contract — so a hook chosen wrongly is a breaking
change to undo. Filed as its own issue rather than settled here.

GOV.UK's three-way split is the one to argue about first: it is the only surveyed system that treats
"what this element is styled as" and "what this element is to the script" as **different questions
with different names**, which is the same separation-of-concerns instinct that put tokens and
components in different tiers.

## Scale, for calibration

GOV.UK Frontend — the most rigorous progressive-enhancement system surveyed — ships roughly **ten**
JS-enhanced components across a catalogue several times that size, and every one works without JS.
**It publishes no modal/dialog at all** (backlog issue #30, *Not published*).

That is worth sitting with. The system most committed to this exact projection declined the component
#882 treats as the motivating hard case.

## What this run could not determine

Listed for the developer conversation, because knowing the open questions is what makes that meeting
efficient.

1. **Is Adobe's tabs keyboard gap deliberate or an oversight?** No published rationale. Changes
   whether their blocks are a floor to beat or a standard to match.
2. **What does authoring vs wrapping actually cost?** No published maintenance hours, defect rates or
   audit outcomes for a hand-authored vanilla behaviour layer, in any system surveyed.
3. **Does a vanilla behaviour layer stay vanilla?** No longitudinal evidence. GOV.UK's has held; one
   data point is not a trend.
4. **Can a behaviour contract be gated at all?** Nothing found describes conformance-testing an
   implementation against a published behaviour contract. This is the gap that decides whether option
   3 is real.
5. **When does `select` get platform relief?** Customizable select is not Baseline; no shipping date
   is published for the browsers that lack it. MDN additionally warns of framework hydration failures
   under SSR.
6. **Does Drupal SDC's auto-loaded JS re-initialise correctly** for a component rendered N times or
   after AJAX? `core/once` reads as a dependency you add, not a default, and the USWDS-on-Drupal issue
   queue shows this failing in practice — but no authoritative Drupal statement on SDC specifically
   was found.
7. **The APG's own normative status.** Commonly asserted to be non-normative; the About page fetch did
   not contain such a statement, so it is **unverified here** rather than confirmed.

## Recommendation to carry into the decision

**Option 1, native-element-first, with option 3's contract as a companion rather than an
alternative.** Concretely, the shape to test with the developer partner:

- Prefer the platform element wherever one exists — `<dialog>`, `<details>`, popover, invoker
  commands — and let the class skin style it. Adobe's accordion at 23 lines is the model.
- Author the residue — **tabs, menu, combobox/listbox** — as small vanilla modules, one per
  component, which is the file both platforms already expect.
- Write the behaviour contract anyway, in the def's `accessibility` block, because a future React or
  web-component target needs it and because #882 is right that retrofitting it after tranche 4 is an
  eighteen-file migration. **But do not count it as a deliverable until someone answers whether it can
  be checked.**

The residue is three behaviours. That is the number to take into the room.
