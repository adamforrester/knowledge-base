# Synthesis — one source with many projections, or a hub? (the #876 run)

> Reconciles **two runs of the same brief** in `_research/_inbound/2026-08-21-source-of-truth-vs-hub/`
> — Claude (in-repo, 2026-08-21) and Gemini (2026-08-23). Path A: the two runs largely corroborate but
> **conflict on one point that should not be settled by majority**, and reconciling them is the
> deliverable. **Nothing here goes into a numbered file**: the decision has not been taken.
>
> **Filed 2026-08-21; reconciliation REBUILT 2026-08-23** against the real pair. The first version
> reconciled against a report of **unverified provenance** that was not established to be a run of this
> brief. Read `PROVENANCE.md` before citing anything here, and do not cite the superseded version.

---

## Read this first: the evidence is thin, and that is the finding

Before any conclusion, the state of the evidence, because it should not get lost behind the answer:

**Thin on the design-system side, dominated by vendor and agency content, with four solid pieces and
one strong analogue in a neighbouring discipline.**

The four solid pieces are one survey with real numbers (Sparkbox 2022, 219 respondents), two product
shutdowns as revealed preference (Specify, Backlight.dev), one first-party retrospective (Figma's own
internal library), and what Figma chose to *build*. The analogue is master data management, which has
had this exact argument for thirty years and named all four positions in it.

**One of those four needs an update after the second run, and it is a real one.** Claude's §3 cited
Code Connect (Apr 2024) as evidence Figma had *deliberately chosen* one-directional. That is still true
of Code Connect and **no longer true of Figma's posture overall**: `gemini.md` reports a **bidirectional
MCP server shipped Feb 2026**, pushing rendered browser UI back into Figma as editable layers. The
underlying finding survives — see the reconciliation — but the "even Figma won't try it" framing does
not, and should not be repeated.

**A second donor discipline arrived with the second run.** Gemini imports the same posture from machine
learning as *Human-in-the-Loop*, where Claude imported it from MDM as *consolidation with stewardship*.
Two neighbouring fields, one borrowed vocabulary, and **still nothing native to design systems** — which
is the finding, not the disagreement.

Everything else returned by search on "design system drift" was content marketing with no data.

**Neither posture wins on evidence.** The hub is **under-evidenced rather than disproven**;
single-source is **demonstrably fragile rather than disproven**. Anyone who reads this synthesis as a
verdict has read it wrong. What the evidence supports is narrower and more useful than a verdict —
see the trigger.

---

## Reconciling the two runs

The `#882` synthesis flagged that a single-agent run lacks the corroboration the dual-agent convention
exists to produce. **This run has it, as of 2026-08-23** — and getting there required withdrawing a
reconciliation published two days earlier against a source that could not be shown to answer this
brief. `PROVENANCE.md` carries that in full. The short version, because it changes what the agreements
below are worth: **"two independent runs agree" is a claim with a date, and before 2026-08-23 it was
not established.**

### Where they agree — corroborated, and now genuinely so

Four findings, reached by two models on different reasoning paths from the same brief:

1. **Do not build automated bidirectional sync.** Gemini: *"it must strictly avoid becoming an
   automated, bidirectional synchronization engine."*
2. **Tokens round-trip; components do not — lossy by construction, not by immaturity.** Gemini reaches
   this through paradigm mismatch (Figma Auto Layout's Hug/Fill/Fixed against CSS Grid, flexbox,
   container queries) where Claude reached it through information preservation. Same line, two
   derivations.
3. **The answer is one authoritative artifact accepting imports, with human-mediated reconciliation.**
4. **Conflict resolution needs a human for the residue.** Gemini adds the sharpest single sentence
   either run produced on *why*: an engineer's contrast fix, then a designer's sync from an older
   Figma file under last-write-wins, and **the accessibility fix is silently overwritten.** That is
   the failure mode with a name and a victim, and it is better than Claude's abstract version.

**A third derivation of (2) already sat in #876's own comment**, which neither run saw: Curtis draws
the line by *capability* — Figma "world-best-in-class" at naming/structure/styling/binding, limited at
composition/behavior/accessibility. **Three independent derivations of one boundary**, from
information-preservation, from paradigm mismatch, and from authoring capability. That is as close to
settled as this topic gets.

### The naming question: Claude's finding survives, and the conflict mostly dissolves

Claude's run concluded that the reconciliation *posture* **has no name in this field**, and that
adopting it means importing vocabulary — it proposed MDM's *consolidation style with stewardship*.

Gemini supplies four names: **Human-in-the-Loop (HITL)**, **Drift Gate**, **Accuracy Harness**,
**Targeted Review Queue**, **Reconciliation Loop**. On its face that is a reversal.

**It is not, and Gemini's own §7 is why.** It concedes: *"While Human-in-the-Loop reconciliation is a
mathematically proven and widely adopted pattern in **machine learning, Intelligent Document
Processing (IDP), and general software engineering**, the exact percentage of enterprise design teams
that have successfully formalized this workflow specifically for design-to-code synchronization
remains unquantified."*

So the names are **imported from ML and general software**, and design-system adoption is unquantified
— which is Claude's finding restated with a different donor discipline. Note the internal tension:
§6 asserts *"In design system architecture, this pattern is also referred to as…"* while §7 concedes
design-system adoption is unmeasured. **§7 is the more careful sentence and should be the one carried.**

**Net: the two runs agree that the posture is real and that its vocabulary is borrowed. They disagree
only on where to borrow it from** — MDM (consolidation/stewardship/survivorship/golden record) or ML
(HITL/drift gate/review queue). Both are defensible; MDM's is older and specifically about *reconciling
multiple authoring origins for one record*, which is the exact shape here, while HITL is about *a human
approving machine output*, which is a near neighbour rather than the same thing. **Worth having both
vocabularies available and choosing deliberately rather than by whichever arrives first.**

### The one genuine conflict: what Lona demonstrates — UNRESOLVED, and not settled by majority

Gemini calls Lona *"the most prominent historical example of an abandoned bidirectional hub"*,
*"explicitly designed to treat the design system as a programmable hub."*

Claude classifies it as **the purest published instance of a single-source generator** — which is
*prism3's own architecture*, not a hub.

**Two external reports now say "hub" and Claude says "single-source generator". This is recorded as
unresolved rather than folded, for three reasons.**

**First, Gemini's own description of Lona is a description of a single-source generator.** In the same
paragraph that labels it a hub: *"It utilized a single structured data format (.component JSON files)
as the central hub to generate cross-platform UI code, Sketch files, and documentation."* One
structured source, unidirectional generation outward, **no sync edge named anywhere.** The
disagreement is about the *label applied*, not about the *mechanism described* — and on the mechanism
the two runs do not actually differ.

**Second, Gemini's diagnosis of why Lona failed is Claude's reading, not its own label's.** It says the
failure was *"the sheer technical complexity of maintaining bespoke compilers"* — the **generation
half**, exactly what Claude identified, and nothing to do with reconciling multiple origins.

**Third, there is a checkable factual error on the "hub" side.** Gemini states Lona's *"repositories
were archived."* Claude fetched the repository on 2026-08-21: **it is not archived** — 7.5k stars,
2,197 commits, publicly active, moved out of the `airbnb` org and carrying *"Airbnb doesn't provide
support for this project."* Disclaimed is not archived, and a report that reached for the stronger word
is a report to check twice on this example.

**What each reading implies, since that is what makes it worth resolving:**

| reading | what Lona is evidence of | direction for prism3 |
|---|---|---|
| hub (both external reports) | bidirectional sync collapses under maintenance cost | **reassuring** — argues *for* the current posture |
| single-source generator (Claude) | the *projection* half is expensive and can stall on its own | **uncomfortable** — a caution *about* the current posture |

**Claude's reading is held**, on the mechanism evidence above and on the principle that the
less comfortable reading of an ambiguous case should not lose to a head-count. But it is a genuine
open conflict and is labelled as one. **Anyone using Lona in an argument about prism3 should read its
README first**, which takes two minutes and settles it better than either report.

### Two claims in `gemini.md` that must not enter the synthesis

Recorded here because both are load-bearing-looking and neither is sourced.

**1. The four-phase drift timeline** (Initial Divergence 1–3 months → Artifact Stagnation 3–6 →
Shadow Source 6–12 → System Abandonment 1–2 years), introduced as *"remarkably consistent across
organizations."* **No citation is given for any phase or boundary.** Claude's run determined
explicitly that **no source measures this interval** — it is undetermined item #2. Gemini's §7 does not
list the timeline among what it could not determine, so the report asserts as fact something its own
methodology section does not defend.

**This is the second time a run on this question has asserted a drift timeline while conceding
elsewhere that none is measurable.** The pattern is worth naming: the timeline is the single most
useful thing a reader would want, which is exactly why it gets supplied without evidence. **It stays
out.**

**2. The $25,000 per engineer per year "copy-paste tax"**, attributed in §2 to *"analysts tracking
post-merger integration and multi-platform synchronization"* — **unnamed**. Gemini's own §7 then calls
it *"the anecdotal metric of a $25,000 'copy-paste tax'."* **Presented as an analyst figure in §2,
conceded as anecdotal in §7.** It stays out as a number; the qualitative claim it decorates —
reconciliation labour is real and hidden — survives on its own.

### Genuinely new in `gemini.md`, and worth carrying

**Figma shipped a bidirectional MCP server (Feb 2026)** integrating with Claude Code and GitHub
Copilot, able to *"query live Figma component hierarchies, generate code, and subsequently push
rendered browser UI back into Figma as fully editable vector layers."* **This is a material update to
Claude's §3**, which cited Code Connect (Apr 2024) as evidence Figma had deliberately chosen
one-directional. That was true of Code Connect and is **no longer true of Figma's posture overall.**

The finding survives the update, and Gemini is the one who says why: the MCP round-trip *"strips the
logic and corrupts the structural constraints, resulting in a visual artifact that looks correct but
is fundamentally broken under the hood."* **A round-trip existing is not a round-trip working**, and
Gemini's own §7 flags that there are *"no multi-year postmortems"* and that current reports are
*"heavily influenced by vendor marketing."* Carry the caveat with the capability.

**`token-reconciler-mcp`** (attributed to humano-ai, glama.ai, Aug 2026) is the most decision-relevant
new artifact: it computes a **drift report** rather than merging, compares colours **perceptually via
OKLab** so `#FFFFFF` and `rgb(255,255,255)` are not flagged while two adjacent greys are, and pairs
text/background against **WCAG 2.2 AA and the APCA draft** so *a pairing that passes in Figma and fails
on the shipped site is surfaced explicitly.* Its default `mostRecentWins` resolver is described in its
own docs as *"deliberately simple"* and *"dumb."*

**Verification status: the named tool could not be confirmed.** A search on 2026-08-23 did not surface
`token-reconciler-mcp` or humano-ai. Adjacent tools in the same category do exist and were found —
Dembrandt (token extraction and drift tracking over snapshots), designlang (CI drift bot, WCAG
contrast remediation), `design-token-bridge-mcp` (cross-platform token translation with a
`validate_contrast` tool). **So the category is corroborated and the specific tool is not.** Treat the
*design* — perceptual comparison plus accessibility pairing plus a report rather than a merge — as the
citable idea, and get a primary URL before naming the tool anywhere downstream.

### Claims appearing in only one run

**Claude only** (each fetched, URLs in `claude.md`): Sparkbox 2022 survey numbers; Specify sunset
15 Nov 2025 and Backlight.dev shutdown 1 Jun 2025; the MDM four-style taxonomy; Figma's Nov 2024
internal rebuild; Code Connect's one-directionality; Storybook autodocs limitations.

**Gemini only** (not independently verified here): the Airbnb DLS retrospective attributed to
Wichrowska and Kim at React Conf 2020 plus a Jan 2026 Medium analysis; Glovo's Pintxo cross-platform
drift; Tokens Studio and Webstudio's "Theirs"/"Ours"/"Merge" precedence rules; the Cairn Framework's
`cairn scan`; Figma's bidirectional MCP; `token-reconciler-mcp`.

The Airbnb DLS account is the one most worth verifying, because it is the only *named-company account
of the single-source failure mode* either run produced beyond Figma's own, and Claude's Lona reading
means Lona no longer plays that role.


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

Carried forward in full, because the undetermined list is the part most likely to be dropped when
someone summarises this later. Items 1–8 are Claude's; 9–12 are added by the second run, and **items 2
and 10 are the pair to watch — both runs concede the interval is unmeasured, and one of them supplied a
four-phase timeline anyway.**

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
9. **Long-term viability of the Feb 2026 bidirectional MCP.** `gemini.md`'s own §7: *"no multi-year
   postmortems available"*, and current reports *"heavily influenced by vendor marketing."* Whether it
   goes the way of Lona's compilers is unknowable today.
10. **The drift timeline — still unmeasured, and now asserted anyway.** `gemini.md` gives four phases
    (1–3 months → 1–2 years) as *"remarkably consistent across organizations"* with **no citation**,
    and does not list it in its own §7. It is excluded from this synthesis. See the reconciliation.
11. **The cost of running a hub, in money.** `gemini.md`'s $25,000/engineer/year is attributed to
    unnamed *"analysts"* in §2 and called *"anecdotal"* in its own §7. Excluded as a figure.
12. **Whether `token-reconciler-mcp` exists as described.** The named tool could not be confirmed on
    2026-08-23; adjacent tools in the same category were found. The *design* is citable; the tool needs
    a primary URL first.

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
