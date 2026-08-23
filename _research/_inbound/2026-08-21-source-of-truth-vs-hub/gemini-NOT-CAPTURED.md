# Gemini run — NOT CAPTURED. Read this before trusting the synthesis's reconciliation.

A second independent run of `prompt.md` was performed by the owner using Gemini. **Its raw text was
not provided to the agent that wrote `claude.md` and the synthesis, and is therefore not in this
folder.** This file exists so that absence is visible rather than inferred from a missing filename.

## What this breaks

`_research/README.md` says raw outputs live here untouched *"so we can audit which agent contributed
which claim later, especially when they disagree."* **For this run that audit is not possible from
the repo alone.** The Gemini side of every claim below is recorded second-hand.

## What the reconciliation was actually done against

A **structured summary supplied by the owner**, naming: four points of agreement, two points of
conflict, and the claims unique to each side. The synthesis reconciles against that summary, not
against the Gemini text. Specifically, the following were relayed rather than read:

**Agreements** (relayed): do not build bidirectional sync; tokens round-trip and components do not,
lossy by construction; the answer is one authoritative artifact accepting imports with human-mediated
reconciliation; conflict resolution needs a human for the residue, never last-write-wins and never
pure auto-merge.

**Conflicts** (relayed): the status of "Design System Contracts" as a named, established pattern; and
what the Lona project demonstrates.

**Gemini-only claims** (relayed, unverified here): Airbnb `react-sketchapp`; the deprecation of
Salesforce's Theo; a Southleft A/B test scoring 69/100 unsupervised against 100/100 constrained.

## What a reader should do with that

1. **Treat every "the other run found…" statement in the synthesis as second-hand.** It is a fair
   summary from the person who ran it, and it is not a primary record.
2. **Treat the four agreements as corroborated but not independently verifiable from this repo.**
   Corroboration is the single most valuable thing two runs produce, and here it rests on a relay.
3. **Do not treat the Gemini-only claims as sourced.** None was checked. `react-sketchapp` and Theo
   are both real and both easy to verify; the Southleft A/B test is the one that most needs a primary
   URL before it is quoted anywhere.
4. **If the Gemini text is recoverable, add it here** and re-read the synthesis's §"Reconciling the
   two runs" against it. The two conflicts in particular deserve checking against the actual wording,
   because one of them (see the synthesis) appears on inspection to be a **scope confusion rather than
   a factual disagreement**, and that reading could be wrong if the summary compressed it.

## Why this was not treated as a blocker

The owner offered the full text on request. It was not requested, because the relayed summary was
specific enough to reconcile the two named conflicts and because the more useful output was a written
record of *how* the conflicts resolve. That was a judgment call and it is the reason this file exists:
the cost of it is exactly the audit gap described above.
