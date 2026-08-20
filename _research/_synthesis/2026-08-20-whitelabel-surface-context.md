# Synthesis — surface context in white-label and owned-code systems

> Reconciles `claude.md` (Claude, in-repo) and `external-agent.md` (Gemini), both run 2026-08-20
> against the same brief. This is the follow-up run to `2026-08-20-surface-context-modeling`, which
> surveyed only first-party systems — every one of which controls its own surfaces, which we do not.
> Not authoritative; synthesis scratch.

---

## The finding neither earlier run could source

**Telefónica Mística deprecated its inverse variant** *(external only)*:

> *"ThemeVariant: deprecated inverse variant (replaced by brand) and added new negative variant"*

Both earlier runs listed "any public record of regret over a variant axis" under COULD NOT VERIFY.
This is it, and it comes from the closest category to our own — a genuine multi-brand system.

**Read it precisely, though.** This is not variant → cascade. It is one variant becoming two, inside
a mechanism (`ThemeVariant`, a React context) that was already a cascade. Mística changed its
*vocabulary*, not its architecture. What it actually evidences is that **"inverse" was the wrong
concept** — a more useful claim than the one the external run draws from it.

The corroborating detail is the more valuable half: an inverse surface in the Blau brand required
*"entirely different accessible text tokens"* from the same surface in Movistar, *"necessitating
unique token resolutions rather than generic inversion."* **In a multi-brand system, inversion is
authored, not computed.** We reproduced this independently against our own generated brands — see
the sibling synthesis, where 33% of inverse tokens diverge from their dark-mode counterparts, in the
same places, in all four brands.

---

## Where the runs diverge

**Salesforce Lightning, again.** The external run: COULD NOT VERIFY. The in-repo run counted the
shipped stylesheet — 455 global `--slds-g-*` hooks with 11 carrying inverse (2.4%), 476 component
`--slds-c-*` hooks with 21 (4.4%), spanning exactly three components: avatar, badge, button *(Claude
only)*. Both runs conclude the two-mechanism pattern is an **adaptation rather than a defect**, and
they arrive there by different routes: the external run by argument (a cascade recolours; some
components must *redraw*), the in-repo run by showing the two layers do different jobs and neither is
derivable from the other.

**The in-repo run corrects itself, and the correction matters.** Its earlier pass called the
`:not(.slds-button--neutral)` carve-out a "hand-maintained exclusion list." It is one component
across ten selectors — not a list, and the maintenance argument built on it was overstated. The
replacement finding is better: *the container rule reaches past its own boundary to restyle
descendant links, which is what forced the carve-out.* **A container that publishes context and
paints only itself needs no exclusion at all.** That is a design rule; the original was a complaint.

**Drupal.** The external run here states that SDC authors *"explicitly pass the variant down to the
component via form fields"* — which contradicts its own earlier run's claim that Drupal is
standardising on the cascade, a claim sourced to an open core issue. The later statement is better
sourced. With the in-repo run's *"SDC has no documented implicit-context mechanism at all"*, two of
three passes now agree: **the platforms diverge.** EDS is a container cascade; SDC is an explicit
prop.

---

## The strongest evidence against the cascade, which is in the in-repo run

Adobe's own guidance on the mechanism we would depend on: *"it is recommended to avoid it, until it
is really necessary."* And Drupal's equivalent is not core at all — it is the contributed
`layout_builder_styles`. Consumption is undocumented on both *(both agents, independently)*.

So the container-publishes-context mechanism is **discouraged on one platform and non-core on the
other**. We have not established the scope of *"it"* in Adobe's sentence, and that matters before
treating it as a blocker.

Even at its strongest reading it does not reverse the recommendation, because the alternative is
worse: a variant axis is not discouraged for a document author, it is unavailable. This is the
discouraged option against the impossible one.

---

## What transfers directly

**Enforcement for client-authored components is a solved problem twice over** *(external only)*.
Panda's `strictTokens: true` fails the build on any raw value; StyleX's `@stylexjs/eslint-plugin`
prevents hardcoded hex values statically. Both are precedents for the conformance checker a
white-label kit needs.

And the counterpoint matters as much: on **AEM, conformance is left entirely to inspection** — no
compiler, no shipped lint rule. On our primary platform we would have to bring our own.

**Radix ships `appearance="inherit"`** *(Claude only)* — a published precedent for the
cascade-prop-defaulting-to-inherit shape.

---

## Reliability flags on `external-agent.md`

- **Marriott's "140+ Design Tokens; 192+ Color Token Values" is sourced to a personal portfolio
  site**, as is the quote about hotel associates and eye strain. Neither is Marriott. Do not quote
  the figure.
- **shadcn/ui: COULD NOT VERIFY — for the second time across two runs.** For a library this well
  documented that is a search failure, not an absence, and it leaves the owned-code section thinner
  than it should be.
- **The report ends with a stray "For medical advice or diagnosis, consult a professional."** A model
  artefact, left in place per the no-editing rule, and a reminder to read a raw output end to end
  before quoting from it.
- The in-repo run states its own weakness plainly and it is real: **one of seven multi-brand systems
  sourced.** Volkswagen, Marriott/IHG, Mercado Libre, Zeta, ING and Santander went unreached, and it
  declined to backfill with blog posts. The external run covers several of those but at markedly
  lower source quality — Supernova's and Cieden's marketing pages rather than the systems' own
  documentation. **Breadth and reliability are inversely distributed across these two runs**, which
  is the single most important thing to hold when reading them together.

---

## Where both runs land

Cascade to publish context; the disagreement is only about whether a second, per-component mechanism
ships alongside it. The in-repo run argues its own counter-argument well: **that is two mechanisms,
and reducing to one is why the question was asked.** SLDS's own usage — three of roughly forty
components — suggests most never need the second.

The sequencing that follows: ship the cascade alone, and add a declared per-component response only
when a component demonstrably cannot recolour its way there.
