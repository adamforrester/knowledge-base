---
name: Promotion — research ready to land in a numbered file
about: A completed research run or synthesis draft waiting to be promoted into the vault
title: "Promote: "
labels: promotion
---

<!--
Use this when research exists but hasn't landed. Research that sits in
_research/ is not authoritative and is invisible to a reader of the vault —
this issue is what keeps it from going stale unnoticed.
-->

## The run

<!-- Path under _research/_inbound/ (and _synthesis/ if a Path-A draft exists). -->

## Sourcing

- [ ] Dual-agent (`prompt.md` + `external-agent.md` + `claude.md`) — reconcile per `_research/README.md`
- [ ] Single-sided (`claude.md` only) — state Path B and flag it in the provenance footer

## Target

<!-- Numbered file(s) and section. Note if it needs a new numbered file
(then: frontmatter + index.md hook + inline cross-refs per CLAUDE.md). -->

## Why it isn't already covered

<!-- The specific thing the vault is missing. Guards against re-promoting
something an adjacent file already says. -->

## On completion

- [ ] Promoted into the numbered file(s), house voice, citations in parens
- [ ] Inline cross-references added from related files
- [ ] `index.md` hook added/updated if the description changed materially
- [ ] `timestamp` bumped on every numbered file touched
- [ ] Path A only: synthesis moved to `_research/_archive/` (`_inbound/` stays put)
- [ ] `09-gaps-and-open-questions.md` updated if this closes a registered gap
