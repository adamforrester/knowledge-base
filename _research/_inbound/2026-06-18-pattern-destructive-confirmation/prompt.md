You are advising a senior design systems practitioner at a digital agency
who maintains a personal knowledge base of design-systems field-truth. The
knowledge base has a ~45-component catalogue and a PATTERNS layer above it.
Patterns carry a `tier` and a GOV.UK-style `goal` facet. Several patterns are
briefed: composition (Forms-as-a-system, View-state orchestration,
Data-collection recipes, Search orchestration) and layout-and-shell (App
shell).

This brief: **Destructive confirmation**. Tier: **`flow`**. Goal:
`help-user-act`. It is the FIRST `flow`-tier brief — a temporal interaction,
not a spatial recipe or a frame — so the spine BENDS the opposite way from
App shell: **Flow & states carries the weight, Decision rules are central,
and Layout is light** (a confirmation is a brief moment in time, not a
persistent structure). Lean into that shape.

The pattern: how a product guards an **irreversible or high-cost action** —
delete, remove, discard, overwrite, send, publish, deactivate. The central
and most contested question is NOT "how to style a confirm dialog" but
"**confirm or undo?**" — the field's strong default is that most actions
should be *undoable*, not *confirmed*, and that confirmation should be
reserved for the genuinely irreversible. The single most important boundary:
this brief does NOT re-derive the Dialog/Modal component (the shell, the
`alertdialog` role mechanics) or the Toast component (the undo surface) — it
owns the *flow*: confirm-vs-undo, the friction ladder, type-to-confirm, the
focus/labeling contract, and the copy. Assume Dialog, Toast, Button, Banner,
and Inline Message are briefed; cite the boundary, don't repeat them.

This is field-truth synthesis for someone who has shipped many destructive
flows. Explain the non-obvious — where leading systems and the UX literature
genuinely disagree, and the defensible default. Be opinionated and declarative.

=== WHAT TO SURVEY (the field) ===

Cite each with a version date; note the verification path for current claims.
- The undo-vs-confirm lineage — Aza Raskin ("never use a warning when you
  mean undo"), NN/g (confirmation dialogs, undo, error prevention, the
  confirmation-fatigue problem), the Gmail/optimistic-undo model.
- WAI-ARIA Authoring Practices — the `alertdialog` pattern, focus management,
  the never-autofocus-the-destructive-action contract.
- WCAG 2.2 — §3.3.4 (Error Prevention: legal/financial/data) and §3.3.6
  (Error Prevention: all) — the reversible/checked/confirmed requirement.
- Design systems — IBM Carbon (danger/destructive modal + button), Shopify
  Polaris (critical actions, destructive), Material 3 (dialogs, destructive),
  Atlassian, Adobe Spectrum, GitHub Primer (the "type-to-confirm" / "danger
  zone" pattern), GOV.UK. Where each draws the confirm-vs-undo line and how
  each handles button order/labeling.
- The platform button-order divergence (macOS vs Windows confirm/cancel
  order) and the field convention for the web.

=== WHAT TO RESOLVE (decision rules are central; flow carries the weight) ===

Make rules machine-resolvable (`IF condition → USE resolution`) wherever a
real threshold exists. Resolve at least:

1. **Confirm vs undo — the central fork.** When is an action undoable (→ do it
   + offer undo, no dialog) vs genuinely irreversible (→ confirm)? The
   deciding axes (reversibility, cost/blast-radius, frequency, recoverability
   via soft-delete). The confirmation-fatigue argument (over-confirming
   trains users to click through). The strong default toward undo.
2. **The friction ladder** — match friction to severity: no friction
   (reversible) → undo toast → simple confirm dialog → type-to-confirm →
   (rare) extra friction. The thresholds for each rung.
3. **The confirmation dialog** — `role="alertdialog"`; the focus contract
   (NEVER autofocus the destructive button — focus cancel/the safe option or
   the dialog container); Esc/backdrop-to-cancel; the title-as-question; the
   body (consequences, scope, irreversibility).
4. **Button labeling & placement** — action-specific verbs ("Delete 3 files",
   not "OK/Yes"); destructive styling (the danger button); the confirm/cancel
   order (and the macOS/Windows divergence); never default/autofocus to the
   destructive action; cancel as the safe escape.
5. **Type-to-confirm** — when warranted (very high blast-radius: delete repo/
   org/production/database); what the user types (the resource name); the
   a11y and copy of it; why it works (forces deliberate action).
6. **The undo model** — the optimistic-action + grace-period (soft delete)
   model; the undo affordance (Toast with Undo); the undo window length; what
   is and isn't undoable; the relationship to "deleted, recoverable for 30
   days".
7. **Bulk & scope** — confirming an action on N items; showing the count and
   exactly what's affected; the "this can't be undone" clarity at scale.
8. **When NOT to confirm** — reversible/low-cost/frequent actions; the cost of
   over-confirmation; substituting undo.

=== THE BOUNDARIES TO HOLD (state in a Related section) ===

- **vs the Dialog / Modal (component)** — the dialog shell and `alertdialog`
  role mechanics vs the destructive-confirmation flow that uses it.
- **vs the Toast (component)** — the undo surface vs the undo flow/model.
- **vs Save & unsaved-changes (pattern)** — the "discard changes?" guard is a
  sibling flow; name the overlap and the seam.
- **vs Forms-as-a-system (pattern)** — form submit/validation is not a
  destructive confirmation; don't conflate.
- **vs Inline Message / Banner (components)** — inline warnings vs the modal
  interruption; when an inline confirm beats a modal.

=== OUTPUT — follow this pattern-brief spine (bent for flow) ===

Structured markdown. ALWAYS sections appear; SCALES appear when they carry
weight — for this tier, **Flow & states is heavy; Layout is light**.
1. **Frontmatter** — YAML: type: pattern-brief, title, description, tags,
   tier: flow, goal: help-user-act, status, timestamp.
2. **`# Destructive confirmation` H1 + a one-paragraph blockquote** framing
   the problem and the boundary (the flow that guards an irreversible action,
   and the confirm-vs-undo question at its heart).
3. **Problem & context** — the recurring problem; confirmation fatigue; when
   it applies; why systems diverge.
4. **Composition** — the components the flow assembles as typed references
   (Dialog/alertdialog, Button, Toast, Banner, Inline Message). Don't
   re-derive them.
5. **Decision rules** — the forks above (1–8) as machine-resolvable rules.
   This is the analytical core.
6. **Flow & states** (HEAVY — the core of this brief) — the lifecycle: intent
   → (undo path: optimistic action → grace period → commit/undo) vs (confirm
   path: dialog → focus safe → confirm/cancel → execute → feedback); the
   state machine for both paths; the soft-delete/grace-period timeline.
7. **Accessibility orchestration** — `alertdialog` semantics, the focus
   contract (safe default, focus return), Esc, the undo-toast a11y (announce +
   reachable before it dismisses — the live-region + timing problem), keyboard.
8. **Content & copy** (near-ALWAYS here) — the title-as-specific-question, the
   consequence/scope/irreversibility body, the action-verb button label, the
   undo-toast copy, the type-to-confirm prompt. The copy IS much of the
   safety.
9. **Layout & structure** (LIGHT) — only what's needed: dialog sizing, button
   row, the toast position. Keep it short.
10. **Variants & responsive** (SCALES) — undo-toast vs simple-dialog vs
    type-to-confirm vs inline-confirm; bulk confirmation; mobile.
11. **Anti-patterns** — the recurring traps (confirming the reversible /
    confirmation fatigue, autofocusing the destructive button, "Are you sure?
    OK/Cancel" vague copy, no undo where undo was possible, undo toast that
    vanishes too fast or isn't announced, color-only danger, defaulting to
    destructive, type-to-confirm for trivial actions).
12. **Related patterns & components** — the five boundaries above, typed.
13. **Field POV evolution** (SCALES) — the shifts (confirm-everything →
    undo-first; the rise of type-to-confirm for high-blast-radius; soft-delete
    + grace period; the alertdialog focus reckoning).
14. **Reference instantiations** (SCALES) — where to look (the ARIA
    alertdialog pattern, Primer type-to-confirm/danger-zone, Gmail undo,
    Carbon danger modal).
15. **Sources cited** — with version dates; flag unsourced claims as
    unverified rather than inventing citations.
16. **Agent-consumable schema** — a fenced YAML block: identity (id, name,
    aliases, tier, goal, status), problem, composition (requires: [typed
    component ids]), decision_rules (as `{ if, use }`), flow (the heavy field
    for this tier — the two paths + grace-period timeline),
    accessibility_orchestration, content, layout, variants, anti_patterns,
    reference_instantiations, relations (composes / relates-to / boundary),
    notes (contested / unverified).

Synthesize; give frameworks where context (reversibility, blast radius,
frequency) decides, defaults where the field has converged. Date current-state
claims. Flag what you can't source.
