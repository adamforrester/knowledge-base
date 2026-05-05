# Research prompt template

Use this template for dual-agent research runs. The same prompt goes to both agents (the external one and Claude in this repo). Saving the prompt verbatim alongside both outputs is what makes the synthesis step possible — see `README.md` for the broader workflow.

This template is informed by two completed runs (Figma practice, i18n/RTL). Update it as we learn from future runs; templates are tools, not contracts.

---

## When to deviate from the template

Most prompts should follow it. The shape is what makes outputs comparable. Deviate when:

- **The topic is genuinely small** — a focused question on one decision, not a broad practice survey. A 7-section template is overkill for "what's our position on detached components." Use a paragraph prompt instead.
- **The topic is meta** — research about our practice, not about a DS technique. The audience framing changes; the references section may not apply.

For everything else, fill the template, run both agents, save raw outputs, synthesise.

---

## The template

Copy from this section. Replace `{{double-braced}}` placeholders. Remove any `[guidance: ...]` comments before sending.

```
You are researching {{topic}} for a senior design systems practitioner
at a digital agency. The output is a structured knowledge document.
{{One-sentence framing hook: what gap does this fill, what context is
the practitioner bringing to it, what should the agent know about why
this is being researched. Optional but strongly encouraged for
under-covered topics; skip for topics with abundant existing
material.}}

[guidance: assume the reader knows the field. Add an explicit "this is
not an introductory guide" sentence if the topic has lots of 101-level
material that the agent might default to. Example: "This is not an
introductory guide — assume the reader knows X and knows what a design
system is."]

Research scope — cover all of the following:

[guidance: 5–7 numbered sections, parallel structure. Each section
gets 3–6 bullet sub-points. Use the numbered scope as the section
spine — both agents will follow it, and the synthesis will align off
it. If the topic risks being miscategorized as content/marketing/etc.,
make Section 1 the meta-framing: "Why this is a DS X concern, not a Y
concern."]

1. {{Section title}}

{{Bullet sub-point}}
{{Bullet sub-point}}
{{Bullet sub-point}}

2. {{Section title}}

{{Bullet sub-point}}
{{Bullet sub-point}}

[... continue through 5–7 sections]

Output format: Structured markdown. Use section headings that match
the numbered scope above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather
than declaring a winner. Flag areas where DS tools (Figma, Style
Dictionary, code pipelines, etc.) have known gaps that practitioners
work around. Where claims depend on current platform state — feature
names, version flags, percentage figures, browser support — date them
and note the verification path. Include a references section linking
to primary sources ({{topic-appropriate examples: e.g., Figma docs,
W3C specs, MDN, platform HIG, practitioner blogs, case studies}}).

Depth: Expert audience. Do not explain {{basic concept}} — explain
{{advanced application or non-obvious implication}}.
```

---

## Why each piece is there

**Audience boilerplate.** "Senior design systems practitioner at a digital agency" is the consistent reader across our runs. It sets depth and removes the agent's tendency to over-explain fundamentals.

**Framing hook.** The i18n run had one ("Most design system source material is silent on this topic — this research should fill that gap"); the Figma run didn't. The hook tells the agent what gap to fill, not just what to write about. For under-covered topics this is essential. For well-covered topics it can be skipped or used to specify our angle (e.g., "agency-side practice, not in-house product practice").

**The numbered-scope spine.** Both runs ended with highly comparable section structure because both prompts used 7 numbered scope sections. The agents followed the scope as the document's spine. **Don't break this** unless the topic genuinely doesn't decompose that way.

**Meta-framing as Section 1.** Optional but powerful when the topic risks miscategorization. The i18n run's Section 1 ("Why this is a DS architecture concern, not just a content concern") forced both agents to argue the framing before getting to mechanics. The synthesis inherited the framing for free.

**The "synthesize, don't list" instruction.** Without it, agents tend to organize by source rather than by topic. With it, both runs produced topic-organized prose with sources cited inline.

**The "trade-offs over winners" instruction.** This is what produces the texture in the output. Without it, agents pick a winner and lose the practitioner-relevant nuance. With it, we get explicit decision frameworks.

**The "tool gaps" instruction.** Tells the agent we want them to surface what the field works around, not just what it does. Both runs produced useful gap lists.

**The currency note** (new based on what we learned). Both runs had agents make confidently-dated claims about platform features ("Schema 2025 introduced X", "Composite Types — 2025 update"). Without an explicit currency instruction, neither agent flagged its own date confidence. The instruction tells the agent to mark claims that depend on current state — saves verification work in synthesis.

**The synthesis-friendly structure note** (new). "Use section headings that match the numbered scope above." Both runs happened to do this; explicit makes it consistent.

**The depth directive.** "Don't explain X — explain Y" keeps the agent at expert depth. The Figma prompt had this and it worked; the i18n prompt didn't and the agent occasionally drifted into 101-level explanation. Worth always including.

---

## Filing a completed run

```
_research/_inbound/YYYY-MM-DD-topic-slug/
  prompt.md           the prompt verbatim
  external-agent.md   raw output from the other agent, no edits
  claude.md           Claude's run of the same prompt
```

Slug convention: lowercase, hyphenated, no underscores, descriptive enough that it's clear which run it is six months from now. `2026-05-05-figma-best-practices` and `2026-05-05-i18n-rtl-l10n` are good examples.

After both raw outputs are saved, the synthesis goes to `_research/_synthesis/YYYY-MM-DD-topic-slug.md` (mirror the inbound slug). When the synthesis is promoted to a numbered file, move the synthesis to `_research/_archive/`.

See `README.md` for the full workflow narrative.

---

## Worked example: minimal prompt

For a small, focused question — not a full survey:

```
You are researching {{specific question}} for a senior design systems
practitioner at a digital agency. The output is a focused position
paper, not a survey. {{Why we're researching this — 1–2 sentences.}}

Cover:
- {{specific question dimension 1}}
- {{specific question dimension 2}}
- {{specific question dimension 3}}

Output format: Structured markdown. State a position with reasoning;
flag where the position depends on context. Cite primary sources
where the position is contested. Brief (1500–2500 words).

Depth: Expert audience.
```

Use this shape when the goal is "what should our practice's position be on X" rather than "what does the field know about X."

---

## What we don't put in the prompt

- **House voice.** The vault's first-person plural ("we", "our practice") enters at the synthesis step, not at the agent step. Pushing voice into the prompt would constrain the agents and make the two outputs more redundant.
- **Vault context (VML, agency commercial model, internal IP).** Agent outputs should be neutral expert documents; the vault's agency-specific framing is added during synthesis. Exceptions: research about our commercial model or our internal IP, where the context is the topic.
- **Specific format prescriptions** (table here, prose there). Let the agents choose their structure within the numbered scope; convergent structural choices are signal, divergent choices give the synthesis more material.
