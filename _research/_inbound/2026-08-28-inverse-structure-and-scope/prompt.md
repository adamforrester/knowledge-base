# Brief — inverse/emphasis token structure and scope, plus Figma binding-panel mechanics

Run date: 2026-08-28. Single focused run, primary sources.

## Framing

We've decided to name-encode inverse as a bounded set. This pass **informs** two open
questions; it does not decide them:

- **PLACEMENT** — where the "inverse" marker sits in the path.
- **SCOPE** — which roles/components actually get an inverse treatment. This feeds our
  trim; our candidate set may be too narrow.

"It varies / no clear pattern" is a valid and useful finding. Do not manufacture a
consensus.

## Part 1 — Structure

For Carbon, Material 3, Primer, Polaris, Fluent, Atlassian (whichever ship inspectable
tokens): how is an inverse / on-emphasis token structured in the path?

- prefix group (`inverse/*`), nested per-role (`background/inverse/*`), suffix
  (`*-inverse` / `*.inverse`), or a flat distinct name (`text-inverse`)?
- is the structure CONSISTENT within the system, or mixed (ours had `on-inverse` vs
  `inverse`)?
- quote the actual token name from source.

Deliver a system × placement table.

## Part 2 — Scope

- which ROLES get an inverse variant — just surfaces + text (background/text/border), or
  the full set including interactive fill states?
- which COMPONENTS consume inverse? Bounded (tooltip, snackbar, banner, …) or broad?
- compare against our candidate set — button, icon button, social button, progress
  indicator, snackbar, tooltip. Is the field's set narrower, wider, or differently shaped?
  Name specific components each system gives an inverse/emphasis treatment.

Deliver a system × scope table.

## Part 3 — The Figma variable picker (Figma docs / help, primary source)

- how does the picker surface a slash-nested path — collapsible folders?
- does it have search, and does search match substrings across the full path (so
  "inverse" filters regardless of placement)?
- how are variables sorted within a folder (confirm alphabetical)?
- any feature that scopes the picker to relevant variables so placement matters less?

These are mechanics questions; verify, don't reason.

## Part 4 — Agents

Any documented evidence or reasoning on how token PATH STRUCTURE affects programmatic /
LLM consumption (predictability of "the inverse of X")? This is likely thin — if there's
no real source, SAY SO and reason from first principles, labeled as reasoning, not
evidence. Do not invent a citation.

## Output

A run under `_research/_inbound/`. The two tables, the Figma-panel facts, an honest agent
note. Flag what belongs in `31-color-systems.md`; open a promotion issue; do not edit the
numbered file. Recommendation allowed but must state which criteria it loses on. Post a
short summary to prism3 — taxonomy issue number to be supplied, or noted as pending.
