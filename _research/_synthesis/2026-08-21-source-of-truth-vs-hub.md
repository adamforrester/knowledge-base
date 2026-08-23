# Synthesis — one source with many projections, or a hub? (the #876 run)

> Reconciles two independent runs of `_research/_inbound/2026-08-21-source-of-truth-vs-hub/prompt.md`
> — Claude (in-repo) and Gemini (run separately by the owner). Path A was used because the two runs
> **conflict on two points**, and reconciling them is the deliverable. **Nothing here goes into a
> numbered file**: the decision has not been taken, and this feeds it. Filed 2026-08-21.

---

## Read this first: the evidence is thin, and that is the finding

Before any conclusion, the state of the evidence, because it should not get lost behind the answer:

**Thin on the design-system side, dominated by vendor and agency content, with four solid pieces and
one strong analogue in a neighbouring discipline.**

The four solid pieces are one survey with real numbers (Sparkbox 2022, 219 respondents), two product
shutdowns as revealed preference (Specify, Backlight.dev), one first-party retrospective (Figma's own
internal library), and what Figma chose to *build* (Code Connect's deliberate one-directionality). The
analogue is master data management, which has had this exact argument for thirty years and named all
four positions in it.

Everything else returned by search on "design system drift" was content marketing with no data.

**Neither posture wins on evidence.** The hub is **under-evidenced rather than disproven**;
single-source is **demonstrably fragile rather than disproven**. Anyone who reads this synthesis as a
verdict has read it wrong. What the evidence supports is narrower and more useful than a verdict —
see the trigger.

---

## Reconciling the two runs — the most valuable part of this write-up

The `#882` synthesis flagged that a single-agent run lacks the corroboration the dual-agent convention
exists to produce. **This run has it**, and the corroboration is worth more than either run alone.

**Caveat that must travel with everything in this section:** the Gemini raw text was not available to
the agent writing this. Reconciliation was done against a **structured summary supplied by the owner**.
See `gemini-NOT-CAPTURED.md` for exactly what that breaks.

### Where they agree — treat as corroborated

Four findings, reached independently by two models on different reasoning paths:

1. **Do not build bidirectional sync.**
2. **Tokens round-trip; components do not — and it is lossy by construction, not by immaturity.**
3. **The answer is one authoritative artifact accepting imports, with human-mediated reconciliation.**
4. **Conflict resolution needs a human for the residue. Never last-write-wins, never pure auto-merge.**

That both runs land on (2) and (3) *by different routes* is the strongest single result here. The
Claude run derived the round-trip line from information-preservation (Figma cannot express a keyboard
model; code cannot express a variant matrix) and the reconciliation posture from MDM's taxonomy.
Whatever route Gemini took, it arrived at the same two places.

**And a third derivation of the same line already exists in prism3's own issue tracker**, which
neither run saw. #876's own comment records Curtis drawing the line by *capability*: Figma is
*"utterly world-best-in-class … in essential naming, structure, styling, binding"* but has
*"limitations in expressiveness, particularly from a configuration and composition, behavior and
accessibility perspective."* His generated specs are `api`/`variants`/`examples`; his authored ones are
`accessibility`/`behavior`/`configurations`/`layout`/`motion`.

**That is the same line as finding (2), drawn from the opposite direction.** The round-trip argument
says *structure survives translation and behavior does not*; Curtis's capability argument says *Figma
authors structure well and behavior badly*. Three independent derivations of one boundary is as close
to a settled result as this topic has.

### Where they conflict — and why the readings differ

#### Conflict 1: "Design System Contracts" as a named, established pattern

**The other run** presents it as established 2026 practice: a named framework (`ds-contracts-poc`,
Southleft / Christine Vallaure), a "three-way differ", and an A/B test scoring **69/100 unsupervised
versus 100/100 constrained**.

**This run** found the same artifact and classified it as **weak**: `ds-contracts-spec.pages.dev`,
v1.0.1, page built 2026-08-17, GitHub org `southleft`, specifying *"props and their legal values,
anatomy, token bindings, slot constraints, accessibility semantics, declared events"* — with **no named
production adopters**, its evidence being compatibility scoring against 101 components from 8
third-party libraries.

**On inspection this is substantially a scope confusion, not a factual disagreement, and that matters
more than which run was "right".** Two different things are being named:

| | what it names | is it established? |
|---|---|---|
| Design System Contracts | a **component contract schema** — props, anatomy, tokens, slots | new, one org, no named adopters |
| the thing this run said has no name | the **multi-origin reconciliation posture** — who may author, what gets imported, who arbitrates | genuinely unnamed in this field |

This run's claim was *"an established design-systems term for this **posture**"* — not "nobody has
written a component schema." Both statements survive. **A component contract schema is not a
reconciliation architecture**, and conflating them is easy because both get called "contracts".

Where the runs do genuinely differ is on **status**, and here this run's reading holds: a v1.0.1 spec
from a single organisation with no named production adopters is not established practice, however
good the idea. **The A/B test is one vendor testing its own framework** — the direction of the result
is unsurprising and the effect size (69 → 100, a perfect score) is suspiciously clean. It is not
independent evidence. That does not make it wrong; it makes it unciteable as proof.

**Net:** the disagreement mostly dissolves. Design System Contracts is real, relevant, and worth
watching for the *component schema* question. It is not evidence that the reconciliation posture has a
name or a track record.

#### Conflict 2: what Lona demonstrates

**The other run** cites Airbnb's Lona as hub-failure evidence.

**This run** classifies it as **the purest published instance of a single-source generator** — define
the system in JSON, generate cross-platform UI code and design files — which is *prism3's own
architecture*, not a hub.

**The readings point the evidence in opposite directions, so this needs stating plainly rather than
being left as emphasis.** If Lona is hub-failure evidence, it argues *for* prism3's current posture. If
Lona is single-source-generator evidence, it is a caution *about* prism3's current posture. Those are
not compatible.

This run's reading is the more careful one, and the reason is a distinction it made explicitly:

> "It is **not** evidence that single-source fails because of multi-origin authorship — it is evidence
> that the *generation* half is expensive and can stall independently. Conflating the two would be
> sloppy."

Lona had no sync edges and no second origin. It generated from JSON. What failed was the **generator**:
of the planned React/Swift/Kotlin/React-Native targets, its own README concedes *"currently, the only
target is React Native, and it's extremely rough (not really usable)."* It is now outside the `airbnb`
org with *"Airbnb doesn't provide support for this project"* on it.

**So Lona is a caution about the cost of the projection half, addressed to prism3, not a point against
hubs.** Read correctly it is the *less* comfortable finding — which is a reason to be suspicious of the
comfortable reading rather than a reason to prefer it.

### Claims appearing in only one run — single-source, both directions

**This run only** (each fetched, URLs in `claude.md`): Sparkbox 2022 survey numbers; Specify sunset
15 Nov 2025 and Backlight.dev shutdown 1 Jun 2025; the MDM four-style taxonomy; Figma's Nov 2024
internal rebuild; Code Connect's one-directionality; Storybook autodocs limitations.

**Other run only** (relayed, **not verified here**): Airbnb `react-sketchapp`; the deprecation of
Salesforce's Theo; the Southleft A/B test.

`react-sketchapp` and Theo are both real and both cheap to verify; neither was checked in this run and
neither should be quoted without a URL. The A/B test is the one that most needs a primary source
before it appears anywhere downstream.

---

## The bottom line

**Accept imports; do not become a hub.**

The token layer is genuinely single-origin and should stay centralized — MDM would call that a correct
*transaction/centralized* style and nothing in either run argues otherwise. The component layer is
different in kind: a def is *authored*, so the moment a designer or engineer expresses intent
elsewhere the system is multi-origin whether or not the architecture admits it.

What both runs support is the **narrow middle**: one authoritative artifact that *ingests* proposals
from other origins through a human-reviewed queue, with **no automatic write-back**. In MDM that is
**consolidation style with stewardship**. Its tradeoff is stated rather than hidden: you pay in
**latency and a queue**, and if nobody works the queue it becomes the shadow source in a new location.
MDM's answer to that risk is that stewardship must be a **named role**, not a rota.

## The trigger — the actionable part, and it is not hypothetical

**Not a date. The first time someone authors component intent outside the definition and it survives
more than one release cycle.**

**That condition is being created right now by a decision already taken.** The #882 run concluded that
the vanilla projection ships a small behaviour layer for the three components with no native element —
**tabs, menu, combobox/listbox**. Roving tabindex, focus management and ARIA state transitions are
*component intent*, they will live in hand-written JS, and **no `ComponentDef` field can hold them**.
The def has an `accessibility` block of prose; it has nothing that expresses a keyboard model.

So the second origin is not a future designer changing something in Figma. It is **the behaviour layer
prism3 is about to write itself**, and it arrives with Arc 4 — which is exactly where #876 says the
decision must be taken *"before the code leg exists."*

**One asymmetry worth naming, from #876 itself:** TokenPress is already a Figma→specs edge **for
tokens**. So the pattern is not foreign to the system — it exists, it runs, and it exists precisely at
the tier where finding (2) says round-tripping works. That is a first-party instance of the boundary
both runs found, and it is the cheapest place to test any further edge.

## The correction to #876's own framing

#876 was filed from Curtis's article. **His piece describes prototype-to-specs extraction as "early
days" and reconciliation across surfaces as needing "more work."**

So anyone citing that article as evidence the hub posture *works in production* is **citing a design,
not a result.** That is a correction to the issue's framing, not a criticism of the source — Curtis is
transparent about what is unfinished, and the article is the best available articulation of the
posture. It is simply not evidence of outcome, and #876 leans on it as though it were.

## What neither run could determine

Carried forward from `claude.md` in full, because the undetermined list is the part most likely to be
dropped when someone summarises this later.

1. **Why Specify and Backlight actually shut down.** Dates solid; no primary cause statement reachable.
   Business failure is not architectural failure and the two cannot be separated here.
2. **How long single-source takes to go stale.** Unmeasured anywhere. Figma's account implies years.
3. **Whether any design-system team runs a documented conflict-resolution policy.** None found. The
   whole conflict-resolution answer is imported from another discipline.
4. **Whether Curtis's hub works.** Being built now, by its author, key edges "early days".
5. **Documentation drift rates** under either regime. No study.
6. **Whether the Sparkbox contribution correlation is causal.** 92% vs 33% is a large gap; "successful"
   is self-reported and maturity is an obvious confound.
7. **Whether anyone has built consolidation-style ingestion for a design system.** No instance found.
8. **The counterfactual — and this is the one to keep.** **Nobody publishes "we stayed single-source
   and it was fine."** Retrospectives get written about rebuilds, not about systems that quietly
   worked. Survivorship bias runs hard through every account in §1, including Figma's, and it means
   the failure literature systematically overstates how often single-source fails. **If this synthesis
   gets compressed to one line by someone downstream, this is the item that will be lost, and losing
   it inverts the reading.**

## What to do next

1. **Do not build any edge yet.** The decision this synthesis supports is a *posture*, not
   construction.
2. **Watch the trigger.** It is arriving with Arc 4's behaviour layer, not with a hypothetical
   designer. Filed as its own issue rather than left here.
3. **Answer the smaller question first.** #876's own comment already reframes this more tractably than
   "one source or many": *which surface is the best authoring interface for which kind of intent, and
   what does transcribing between them cost?* That is answerable from evidence — prism3 hand-authors
   `button.ts`'s 9,006-byte `anatomy` block, and `docs/32` records that it was derived by reading a
   Figma prototype and transcribed by hand. **The transcription cost is real and already being paid,
   silently, once per def.** Measuring it on one def costs one def.
