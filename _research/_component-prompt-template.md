# Component-brief research prompt template

Use this template for component-brief research runs. The same prompt goes to both agents (the external one and Claude in this repo) when running dual-agent. For claude-only runs, the same template is used; only the external-agent output is omitted.

This is a companion to `_prompt-template.md`. The original template targets ~3,000-word topic surveys that land in numbered files. This template targets per-component briefs that land at `components/<slug>.md`.

---

## When to use which template

- **`_prompt-template.md`** — topic-level research that lands in a numbered file. Practice-area surveys (accessibility, motion, tokens, AI patterns).
- **`_component-prompt-template.md`** — single-component briefs that land in `components/<slug>.md`. Field-truth studies of one component.

If unsure, ask: is the output a numbered file or a component brief? That answers it.

---

## When to deviate

The 15-section spine is the contract. Deviation is rare, and is recorded in the synthesis. Reasons that justify deviation:

- **Foundational primitive** — for `Box`, `Stack`, `Divider`, sections 4 (states/variants) and 8 (motion) collapse to one paragraph each. The spine still ships; the depth scales.
- **Non-web component** — for components with no web equivalent (Action Sheet, Bottom Sheet on mobile), section 11 (implementation notes) shifts to platform-specific frameworks; section 9 (i18n) becomes platform-locale concerns.

For everything else, follow the spine.

---

## The template

Copy from this section. Replace `{{double-braced}}` placeholders. Remove any `[guidance: ...]` comments before sending.

```
You are researching the {{Component Name}} component for a senior
design systems practitioner at a digital agency. The output is a
field-truth study of how the leading design systems handle this
component — what they converge on, where they diverge, and what
the practice's opinionated default should be when starting from
scratch.

This is not an introductory guide. Assume the reader knows what a
{{component}} is, knows what a design system is, and has shipped
multiple component libraries. Explain the non-obvious — the prop
choices field leaders disagree on, the accessibility decisions that
are still contested, the implementation traps that recur across
codebases.

Field-leader systems to survey (web, unless the component is
mobile-first):

- Shopify Polaris
- Adobe Spectrum
- Google Material 3
- IBM Carbon
- GitHub Primer
- Atlassian Design System
- Shopify Hydrogen (where it diverges from Polaris)
- Base Web (Uber)

Mobile reference (where the component has a mobile dimension):

- Apple Human Interface Guidelines
- Material 3 (Compose / mobile)
- Microsoft Fluent

Cite each system referenced with a version date — e.g., (Polaris
12.0, 2025), (Material 3, 2024), (Spectrum 2024.4). Currency
matters; section 14 of the brief is the auditable record.

Output structure — follow this 15-section spine:

1. Framing — what this component is, what it isn't, why systems
   disagree on it.
2. Anatomy and parts — structural model, named parts, slot
   vocabulary.
3. Properties / API — converged prop set across field leaders;
   divergences with reasoning.
4. States and variants — runtime states (rest / hover / focus-
   visible / pressed / disabled / loading / error / empty / read-
   only) vs. intentional variants (size / tone / density /
   emphasis); canonical matrix.
5. Usage guidance — when to use, when not to use, what to use
   instead.
6. Accessibility — component-specific concerns. The reader has
   read 14-accessibility, 17-accessibility-annotation-contract,
   and 28-web-accessibility-implementation; do not re-state the
   theory; identify what is specific to this component (ARIA
   pattern, keyboard model, focus contract, AT announcements,
   the WCAG SC the component participates in).
7. Content guidelines — labels, tone, error / empty / CTA copy
   patterns.
8. Motion and transition — entry / exit, state transitions,
   reduce-motion contract.
9. Internationalization — RTL behaviour, text expansion, locale
   concerns.
10. Naming — what the field calls it; the practice's default;
    aliases consumers will reach for.
11. Implementation notes — framework-specific gotchas, prop-vs-
    slot decisions, headless-vs-opinionated tension.
12. Related and alternative components — typed relationships
    (composes with / alternative to / supersedes / superseded by).
13. Field POV evolution — how the leading systems' position has
    changed; recent shifts worth flagging.
14. Sources cited — every system referenced, with version dates.
15. Agent-consumable schema — a fenced YAML block representing
    the brief's structured content as the practice's opinionated
    `.ai.json` shape for this component. Free-form YAML; the
    schema is the structured projection of sections 1–13. Cover:
    identity (id, name, aliases, category, status), API (props
    with type/default/required/deprecated/description),
    composition (composes-with, alternative-to, supersedes,
    superseded-by), accessibility (wcag-criteria, aria-attributes,
    keyboard-model, focus-behavior), states, variants, content
    (label-pattern, error-pattern, empty-pattern). The schema
    must not contradict any prose section above; if it does, the
    prose wins and the schema is wrong.

Output format: Structured markdown. Use H2 headings that match
the numbered spine above. Synthesize findings — do not list
sources mechanically. Where the field has consensus, state it
clearly; where decisions are context-dependent, provide decision
frameworks rather than declaring a winner. Where claims depend on
current platform state — feature names, version flags, ARIA
attributes that recently changed — date them and note the
verification path.

Depth: Expert audience. Do not explain {{the basic concept of
this component}} — explain {{the non-obvious application or the
implementation trade-off that field leaders still disagree on}}.
```

---

## Filing a completed run

Same convention as `_prompt-template.md`:

```
_research/_inbound/YYYY-MM-DD-component-<slug>/
  prompt.md           the prompt verbatim
  external-agent.md   raw output from the other agent (dual-agent only)
  claude.md           Claude's run of the same prompt
```

Slug convention: lowercase, hyphenated, prefixed with `component-`. Examples: `2026-07-01-component-button`, `2026-07-12-component-text-field`, `2026-07-20-component-toast`.

The presence of `external-agent.md` records that the run was dual-agent; its absence records that the run was claude-only. No frontmatter field encodes this — the folder is the audit.

After the brief lands at `components/<slug>.md`, the `_inbound/` folder stays in place as audit record. If a `_synthesis/` intermediate was used, move it to `_research/_archive/` after promotion.

---

## What this template does not include

- **House voice.** The vault's first-person plural enters at the synthesis step (when writing the brief), not at the agent step.
- **Vault-specific cross-references.** The agents do not see numbered files; the brief author adds the `(See 14-accessibility §3.)`-style cross-references during synthesis.
- **The §15 schema's final shape.** Free-form YAML for the first ~5 briefs. The shape stabilises through real use; only then is the schema formalised into `components/_schema.md`.
