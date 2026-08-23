# Claude run — one source with many projections, or a hub? (2026-08-21)

Raw output. Every external claim was fetched during this run; URLs and dates inline. Nothing here is
authoritative until synthesised. Written **without sight of the Gemini run** — see
`gemini-NOT-CAPTURED.md`.

---

## Direct answer

**Plan to accept imports; do not plan to become a hub.** The evidence does not support building
bidirectional sync edges before you have a second author, and it does not support pretending a second
author will never arrive. The token layer is genuinely single-origin and should stay centralized —
nothing in the evidence argues otherwise, and the MDM literature would call that a correct
*transaction/centralized* style. The component layer is different in kind: it is authored, so the
moment a designer or engineer expresses intent elsewhere you have a multi-origin system whether or not
you built one. What the evidence supports is the **narrow middle**: one authoritative artifact that
can *ingest* proposals from other origins through a human-reviewed queue, with no automatic
write-back. That is a named pattern in master data management (*consolidation style with
stewardship*), it is roughly what Figma's own official mechanism does (*registry style* — link, don't
sync), and it is the only posture here with more than a few years of production evidence behind it.
The trigger is not a date; it is **the first time someone authors component intent outside the
definition and it survives more than one release cycle.** Before that, an import path is speculative
machinery. After that, its absence is how the definition goes stale.

**Evidence quality, stated up front because it changes the weight of everything below.** The
design-system-specific literature on this question is **thin and heavily vendor-authored**. Most
results for "design system drift" are agency content marketing with no data. The load-bearing evidence
is four things — one survey with real numbers, three product shutdowns as revealed preference, one
first-party retrospective, and a twenty-year-old literature in a neighbouring discipline that has
already had this argument. Those are separated from the marketing throughout.

---

## 1. What breaks in single-source systems when authorship is multi-origin

**The failure mode is not that the source goes wrong. It is that the source goes *quiet*, and a
shadow source accumulates in the artifact people actually touch.**

The strongest first-party account is **Figma's own internal design system**
(`figma.com/blog/figma-pattern-library/`, 21 Nov 2024, fetched 2026-08-21):

> "Detached instances ran rampant. Components that should have been consistent showed subtle but
> meaningful differences."

The fragmentation became *"impossible to ignore"* only when a launch forced an audit. The remedy was
not reconciliation — they **rebuilt from scratch**, five months, 680+ tokens and 22 component sets.

Two things there matter more than the headline. The drift was **invisible until a deadline made
someone look**. And the detached instance *is* the shadow source: a designer expressing intent the
library could not absorb, so they severed the link and kept working.

The clearest case of a *single-source generator* going stale is **Lona** — Airbnb's "define the system
in JSON, generate cross-platform UI code, Sketch files and other artifacts", the purest published
instance of the architecture under discussion. Now at `github.com/Lona/Lona` (fetched 2026-08-21),
**out of the `airbnb` org**, carrying:

> "Airbnb doesn't provide support for this project. The code and automated tests are not at the same
> degree of technical rigor as other Airbnb projects."

and conceding that of the planned React/Swift/Kotlin/RN targets, *"currently, the only target is React
Native, and it's extremely rough (not really usable)."* 7.5k stars; the generator half never landed.

**I want to be careful about what Lona proves.** It is **not** evidence that single-source fails
because of multi-origin authorship — it is evidence that the *generation* half is expensive and can
stall on its own. Conflating the two would be sloppy. What it establishes is that the most-cited
public instance of this architecture did not reach production.

Empirical numbers, from the **Sparkbox 2022 Design Systems Survey**
(`designsystemssurvey.sparkbox.com/2022/`, fetched 2026-08-21; 219 respondents, 183 maintainers,
fifth edition):

- **"Parity between design & code" is the third-highest challenge, 37%** of maintainers.
- **36% have no defined contribution process**; **33%** accept coded contributions; **37%** accept
  subscriber designs.
- **"Only 33% of maintainers are satisfied with their design system's current stance on accepting
  contributions."**
- Among systems the survey classes **successful**: **92% accepted coded contributions, 83% accepted
  design submissions** (160 respondents).

That last gap — 92% vs 33% — is the only quantitative signal found on either side, and it points away
from strict single-source. **Read it carefully**: "successful" is self-reported, causation is
unestablished, and mature systems plausibly accept more contributions *because* they are mature.

**Could not determine: the timescale.** No source measures the interval between "single source
established" and "shadow source emerges."

---

## 2. What a hub costs

**The strongest evidence is commercial mortality, and it is one-sided.** Two products built
specifically to be the reconciliation layer shut down within six months of each other:

- **Specify** — a design-token hub centralizing tokens from Figma, Tokens Studio and JSON. **Sunset
  15 November 2025** (`alternativeto.net/software/specify/about/`, fetched 2026-08-21).
- **Backlight.dev** (divRIOTS) — design-system development environment spanning design and code.
  **Shut down 1 June 2025.**

**No primary post-mortem was reachable for either.** Dates come from secondary aggregators. One search
summary attributed Specify's closure to failing to *"create a sustainable business"*; that was not
verifiable against a primary source, so **the reason is unestablished while the dates are reliable.**

Business failure ≠ architectural failure. A hub can be sound and unviable. What the shutdowns
establish is narrower: **the market did not sustain a dedicated hub, twice, in one year.**

Internal cost, from Sparkbox: **staffing shows the largest gap in the survey between priority (13%)
and challenge (35%)**. Adding N sync edges to a team already understaffed for one artifact is the
risk.

**A structural argument, labelled as reasoning not evidence.** A single source with N projections is N
one-way transforms. A hub with N round-tripping origins is **2N**, each lossy in its own way, plus a
reconciliation policy per disagreeing pair. Curtis names four edges for two origins.

**Curtis does not claim the hub is finished.** He describes prototype-to-specs extraction as *"early
days"* and reconciliation as needing *"more work"*
(`nathanacurtis.substack.com/p/spec-driven-ui-component-development`, 14 Aug 2026, fetched
2026-08-21). **Anyone citing that article as evidence the hub works in production is citing a design,
not a result.**

---

## 3. The round-trip problem

**There is a principled line, and it is not where most tools draw it: values round-trip, structure
does not.**

Tokens round-trip because a token is a *name bound to a value* — flat, orderless, conflict-detectable.
Two origins editing one token produce a one-line diff.

Components fail because a component is *structure plus behavior plus composition*. Round-tripping
needs the transform to be information-preserving both ways and it is not: Figma has no expression for
a keyboard model, a focus trap, an ARIA relationship or a conditional slot; a code implementation has
no expression for a variant matrix or an auto-layout constraint. Each direction discards what the
other cannot hold. **Lossy by construction, not by immaturity.**

**The most telling evidence is what Figma itself built.** Code Connect
(`figma.com/blog/introducing-code-connect/`, 16 Apr 2024, fetched 2026-08-21) is **one-directional,
design-to-code, and a *mapping* rather than a sync** — *"developers see your actual design system code
instead of auto-generated CSS."* It generates nothing and writes back nothing. The article contains no
mention of round-trip or bidirectional sync. The company with the most to gain from bidirectional
component sync shipped a link table.

In MDM vocabulary (§6), **Code Connect is registry style**: identify the correspondence, let each side
keep authorship, never write back.

**Succeeds:** tokens/values; one-way generation of design artifacts *from* code.
**Reliably fails:** behavior, keyboard/focus semantics, composition and slotting, layout intent. No
counterexample found — no product demonstrating durable bidirectional component sync at production
scale.

---

## 4. Conflict resolution

**Design systems have almost no literature here. Master data management has thirty years of it, and
its conclusion is that the automatic part is the easy part.**

No design-system source describing a real production conflict-resolution policy was found. **That
absence is the finding for question 4.**

MDM names the mechanisms: **survivorship rules** (declared per-field precedence), **golden record**
(the reconciled result, distinct from any origin's copy), **data stewardship** (a named human role
owning exceptions, with a **review queue** for what rules cannot decide), **trust scores** (per-source,
per-attribute weighting).

The load-bearing lesson: **every production MDM style keeps a human in the loop for the residue.**
Automatic merge handles volume; a steward handles disagreements. Nobody ships pure last-write-wins;
nobody ships pure auto-merge. The queue is the design, not a failure of it.

**Could not determine:** whether any design-system team has implemented survivorship rules or a
stewardship queue under any name. No instance found.

---

## 5. The documentation question

**Both origins are right about different halves, and the disagreement is really about which parts of
a component have their truth in code.**

Curtis's position is narrower than it is usually quoted as: *"prop tables and 'how to use' React, iOS
and Android originate more appropriately from coded implementations."* Prop tables and per-platform
usage — not all documentation.

Well-founded: the API genuinely does live in code. But **docs-generated-from-code are demonstrably
lossy**, documented in the tooling's own tracker. Storybook autodocs uses static source analysis; the
field's own summary is that *"it generally does a decent job, it just needs a little help with the last
ten percent."* Concretely: `@defaultValue` tags *"are stripped out and then ignored"*, leaving the
Default column empty; `Readonly`-wrapped props lost descriptions after the react-docgen migration
(`github.com/storybookjs/storybook/issues/26593`); aliased imports are followed unreliably.

So: **code-generated docs are accurate about what exists and silent or wrong about what was
intended.** A default, a deprecation, a "why", an accessibility obligation are all intent, and static
analysis cannot recover intent never written as syntax.

The symmetric failure of spec-generated docs is §1's: the spec describes a component nobody verified
against the shipped one, and drifts silently because docs are checked least.

**The split the evidence supports:** generate the *reference* (props, types, signatures) from code,
where it is definitionally true. Generate the *contract* (what it is for, when not to use it, what
accessibility obligations it carries, which token roles it binds) from the definition, because that is
intent. Not a compromise — each source used where it is authoritative.

**Could not determine:** any measurement of documentation drift rates under either regime.

---

## 6. The middle path

**The pattern described — one authoritative artifact accepting imports with human reconciliation — is
master data management's *consolidation style*, and its taxonomy has four positions that map cleanly.**

Sources: `profisee.com/blog/master-data-management-implementation-styles/`,
`stibosystems.com/blog/4-common-master-data-management-implementation-styles`,
`semarchy.com/blog/mdm-implementation/` — all vendor-authored, but the taxonomy is stable across all
of them and predates all of them. Fetched 2026-08-21.

| MDM style | Who authors | Writes back? | Design-system equivalent |
|---|---|---|---|
| **Registry** | origins only; hub links | **no** | Figma Code Connect |
| **Consolidation** | hub is system of record; imports flow in | **no** | **the middle path** |
| **Coexistence** | hub *and* origins; bidirectional | **yes** | Curtis's four-edge hub |
| **Transaction / Centralized** | hub only | distributes outward | prism3 today |

Two findings bear directly.

**The direction of travel is the opposite of the one proposed.** The recommended progression is to
*start* at consolidation and work *up* to coexistence or centralized as governance maturity allows —
coexistence *"increases complexity and costs"*, centralized *"requires major changes to existing IT
infrastructure."* prism3 is already at the most controlled end; moving to coexistence is the expensive
move in that taxonomy, not the natural next step.

**Registry style barely exists in practice.** One vendor practitioner: *"I never saw a registry
implementation style in the wild — not one."* The most elegant-on-a-diagram option is the one nobody
runs — a direct caution about picking an architecture because the diagram is clean, which cuts both
ways here.

**Tradeoffs of consolidation-with-stewardship:** one unambiguously authoritative artifact, so no read
precedence needed; a real path for intent expressed elsewhere, so the definition stops going stale;
paid for with **latency and a queue** — an import is a proposal, someone must act, and if nobody does
the queue becomes the shadow source in a new location. MDM's answer to that last risk is that
stewardship must be a **named role**, not a rota.

**One name looked for and not found:** an established design-systems term for this posture. It has no
name in this field; adopting it means importing the vocabulary.

---

## What could not be determined

1. **Why Specify and Backlight actually shut down.** Dates solid; no primary cause statement reachable.
2. **How long single-source takes to go stale.** Unmeasured anywhere.
3. **Whether any design-system team runs a documented conflict-resolution policy.** None found; §4 is
   imported wholesale from another discipline.
4. **Whether Curtis's hub works.** Being built now, by its author, key edges *"early days."* No
   independent production account.
5. **Documentation drift rates** under either regime. No study found.
6. **Whether the Sparkbox contribution correlation is causal.** Large gap, self-reported success,
   maturity is an obvious confound.
7. **Whether anyone has built consolidation-style ingestion for a design system.** Well-established in
   data management; no design-system instance found.
8. **The counterfactual.** Nobody publishes *"we stayed single-source and it was fine."* Survivorship
   bias runs hard: retrospectives get written about rebuilds, not about systems that quietly worked.

**Honest summary of the evidence base:** thin on the design-system side, dominated by vendor and
agency content, with four solid pieces (one survey, two shutdowns, one first-party retrospective) and
one strong analogue in a neighbouring discipline. **The hub posture is under-evidenced rather than
disproven; single-source is demonstrably fragile rather than disproven.** Neither wins on evidence.
What the evidence does support: the expensive part is never the transform — it is the reconciliation
policy and the person who runs it, and that cost lands the moment there is a second author, not the
moment the second edge is built.
