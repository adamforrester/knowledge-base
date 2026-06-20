*Claude pass — one of two dual-agent inputs for the Destructive confirmation pattern brief (first `flow`-tier brief). The spine is bent the opposite way from App shell — Flow & states is heavy, Decision rules are central, Layout is light. To be synthesised with `external-agent.md` into `patterns/destructive-confirmation.md`.*

---

okf_version: "0.1"
type: pattern-brief
title: Destructive confirmation
description: The flow that guards an irreversible or high-cost action — and the question at its heart, confirm vs undo. The undo-first default, the friction ladder (no friction → undo toast → confirm dialog → type-to-confirm), the alertdialog focus contract (never autofocus the destructive button), action-verb button labels, the soft-delete grace-period model, and the copy that carries the safety. The first flow-tier brief, so flow & states carries the weight and layout is light. Composes Dialog/alertdialog + Button + Toast + Banner + Inline Message; borders the Dialog component, the Toast component, Save & unsaved-changes, Forms-as-a-system, and inline warnings.
tags: [patterns, destructive, confirmation, undo, accessibility, help-user-act]
tier: flow
goal: help-user-act
status: draft
aliases: [Destructive confirmation, delete confirmation, are-you-sure, confirm-vs-undo, type-to-confirm, danger zone]
last-audited: 2026-06-18
timestamp: 2026-06-18

---

# Destructive confirmation

> Every product has actions that hurt to get wrong — delete, remove, discard, overwrite, send, publish. The reflex is to throw an "Are you sure?" in front of each one, and the reflex is mostly wrong. The field's hard-won lesson is that **most destructive actions should be undoable, not confirmed**: a confirmation that fires too often trains the user to click through it, so it protects nothing and slows everything. This brief owns the *flow* that guards a dangerous action — the confirm-vs-undo decision first, then the friction ladder, the focus and labeling contract, and the copy that actually carries the safety. It defers the dialog shell to the Dialog component and the undo surface to Toast, and resolves only the flow.

---

## Problem & context

The recurring problem is calibration: too little friction and users destroy things by accident; too much and you get **confirmation fatigue** — the dialog becomes muscle-memory noise, dismissed without reading, and the one time it mattered it didn't help. The deeper insight, and the thing teams most often miss, is that confirmation is usually the wrong tool: a modal *interrupts before* the action and demands a prediction ("will I regret this?"); **undo lets the action happen and offers a cheap reversal after** — which matches how people actually work (act, notice, correct). So the first question is never "what should the dialog say" but "**does this need a dialog at all, or does it need undo?**"

The pattern applies to any irreversible or high-cost action. It does **not** apply to reversible, low-cost, or frequent actions (those want undo or nothing) and it is **not** a form submit or a validation gate (Forms-as-a-system). Systems diverge because they weigh two costs differently — the cost of an accidental destruction vs the cost of friction on every action — and because reversibility is often an *engineering* choice (soft-delete makes "irreversible" reversible). The decisions below resolve by reversibility, blast radius, and frequency rather than by reflex.

## Composition

The flow assembles briefed components and adds the guard logic; it re-derives none of them.

- **Dialog** (see dialog) — the confirmation surface, used in its `alertdialog` mode; the component owns the modal shell, focus trap, and Esc; this pattern decides *when* to summon it and *what its focus/labeling contract is*.
- **Button** (see button) — the destructive action button (danger styling) and the cancel/safe button; the labeling and order are this pattern's call.
- **Toast** (see toast) — the undo surface (action + "Undo"); the component owns the toast; this pattern owns the undo *model* (grace period, what's reversible).
- **Banner / Inline Message** (see banner, see inline-message) — the inline-confirm alternative and any persistent danger-zone warning, when a modal is the wrong interruption.
- **Text Field** (see text-field) — the type-to-confirm input for the highest-blast-radius actions.

**The delta this pattern adds** is the guard flow: the confirm-vs-undo decision, the friction ladder, the focus/labeling contract, the soft-delete grace-period model, and the copy — none of which any single component owns.

## Decision rules

The analytical core. Machine-resolvable where a real threshold exists.

**1. Confirm vs undo — the central fork.**
- `IF the action is reversible (or can be made reversible via soft-delete) AND not catastrophic` → **do it immediately and offer undo** (no dialog). The strong default.
- `IF the action is genuinely irreversible OR high blast-radius (bulk, shared/destructive-to-others, financial, legal)` → **confirm** before executing.
- `IF the action is frequent` → lean harder toward undo even if mildly destructive — a dialog on a frequent action *guarantees* click-through fatigue.
- The test, in order: **reversibility** (can I undo it?), **blast radius** (how much, whose, how recoverable?), **frequency** (how often?). Undo wins unless irreversibility or blast radius forces a confirm.

**2. The friction ladder** — match friction to severity; never more than the danger warrants.
- `reversible, low-cost` → **no friction** (just do it), or undo if a mistake is plausible.
- `reversible but noticeable` → **optimistic action + undo toast**.
- `irreversible, bounded` → **simple confirm dialog** (alertdialog).
- `irreversible, high blast-radius` → **type-to-confirm**.
- `(rare) catastrophic/system-level` → type-to-confirm + extra deliberate friction (re-auth, second factor).
- Every extra rung costs every user every time — climb only as far as the danger requires.

**3. The confirmation dialog.**
- Use `role="alertdialog"` (not a plain dialog) so AT announces it as a decision; the component supplies the focus trap and Esc.
- **NEVER autofocus the destructive button.** Focus the **cancel/safe** option (or the dialog/its heading) so a reflexive Enter/Space doesn't destroy. Esc and backdrop click cancel (the safe outcome).
- Title is the **specific question**; body states the **consequence, scope, and irreversibility**.

**4. Button labeling & placement.**
- **Action-specific verbs** — "Delete 3 files," "Discard draft," "Deactivate account" — never "OK/Yes/Confirm" (a label that doesn't say what happens isn't a safeguard).
- **Destructive styling** (the danger/red button) AND a text label — never color alone.
- **Cancel is the safe escape**, visually secondary; the destructive action is **never the default** and never autofocused.
- Button **order** is a real platform divergence (macOS puts the confirming action right; Windows left); pick one convention per product and hold it — the safety comes from labeling + focus + styling, not from order alone.

**5. Type-to-confirm** — the high-blast-radius rung.
- `IF the action destroys something large/shared/irrecoverable (delete a repo, an org, a production database, a workspace)` → require the user to **type the resource's name** to enable the destructive button.
- It works because it forces deliberate, non-reflexive action (you can't muscle-memory it) and re-states exactly what's being destroyed. Keep the prompt and input labeled and accessible; show the exact string to type.
- `IF the action is trivial` → do **not** use type-to-confirm (it's friction theatre; trains resentment).

**6. The undo model.**
- Prefer **optimistic execution + a grace period**: perform the action immediately (the user sees it done), but defer the irreversible commit behind a window — a **soft delete** recoverable for N seconds (toast Undo) or N days (a trash/restore).
- The **undo affordance** is a Toast with an Undo action; the window must be long enough to notice and reach (and announced — see a11y).
- `IF true undo is impossible` → fall back to confirm; `IF a 30-day restore exists` → say so in the copy and lean undo-first.

**7. Bulk & scope.**
- `IF acting on N items` → state the **count and exactly what's affected** ("Delete 3 projects and their 142 tasks? This can't be undone"); the bigger the scope, the higher the rung (bulk irreversible → type-to-confirm or the count typed).

**8. When NOT to confirm.**
- `IF reversible / low-cost / frequent` → don't confirm; use undo or nothing. Over-confirmation is itself a defect — it's the cause of the click-through reflex that makes the *necessary* confirmations fail.

## Flow & states

The heavy section for this tier. There are two paths; the decision rules choose which.

**The undo path (default for reversible):** *intent* (user triggers the action) → *optimistic execution* (the UI reflects it done immediately; the item is soft-deleted / staged) → *grace period* (an undo toast is shown; a timer runs — seconds for a toast, or a longer trash window) → **commit** (timer elapses / toast dismissed → the irreversible delete happens) **or** **undo** (user activates Undo → the action is reversed, the UI restored, focus returned). The key property: the user is never *blocked*; the safety is the reversal window, not a gate.

**The confirm path (for irreversible/high-blast):** *intent* → *dialog open* (alertdialog; focus moves to the safe/cancel option) → [*type-to-confirm sub-state* (destructive button disabled until the resource name matches)] → **confirm** (execute → success feedback) **or** **cancel** (Esc / backdrop / cancel → no-op, focus returns to the trigger). The action only happens after deliberate confirmation; there may be no undo after.

**The grace-period timeline** is the pattern's signature: optimistic now → reversible for a window → committed. Choosing the window length (toast seconds vs trash days) by recoverability cost is the core flow decision.

## Accessibility orchestration

The a11y the *flow* owns (the Dialog/Toast components own their own widget ARIA):
- **`role="alertdialog"`** for the confirm dialog so AT announces it as an alert demanding a decision; the dialog is labelled by its title and described by its body.
- **The focus contract** — focus moves into the dialog on open to the **safe/cancel** control (never the destructive one), and **returns to the triggering element** on close. The single most important a11y *and* safety property here.
- **The undo-toast timing problem** — an auto-dismissing toast is an a11y trap: the Undo must be **announced** (a polite live region) *and* **keyboard-reachable before it disappears**. Either give enough time + a focus path, or (better for critical undo) use a persistent affordance, not just an ephemeral toast. Don't hide a critical reversal behind a 4-second toast a screen-reader user can't reach.
- **Esc cancels**; the destructive action is never the default action of the form/dialog.

## Content & copy

The copy *is* much of the safety — near-ALWAYS load-bearing.
- **Title = the specific question** — "Delete this project?", not "Are you sure?" A vague title makes the user reconstruct what's happening at the worst moment.
- **Body = consequence + scope + reversibility** — what will happen, to what/whom, and whether it can be undone ("This permanently deletes the project and its 142 tasks. This can't be undone." / "You can restore it from Trash for 30 days.").
- **Button = the action verb** — "Delete," "Discard," "Remove 3 items" — matching the title's verb; never "OK/Yes."
- **Undo-toast copy** — confirm what happened + offer the reversal: "Project deleted. **Undo**."
- **Type-to-confirm prompt** — name exactly what to type ("Type **acme-prod** to confirm") and why.
- Never blame; never bury the irreversibility in a sentence the user won't read.

## Layout & structure

Light, by tier. The confirm dialog is a small centered modal (the Dialog component's small size), title + body + a right-aligned (or platform-conventional) button row with cancel secondary and the danger button distinct. The undo toast sits in the toast region (typically bottom or bottom-left) with the Undo action inline. Type-to-confirm adds a single labeled input above the button row. Nothing structural beyond that — this is a moment, not a layout.

## Variants & responsive

- **Undo toast** (reversible) vs **simple confirm dialog** (irreversible bounded) vs **type-to-confirm** (high blast-radius) vs **inline confirm** (a confirm rendered in place — e.g. a row's "Delete? · Confirm / Cancel" — when a modal is too heavy an interruption).
- **Bulk confirmation** — count + scope in the title/body; the rung rises with N.
- **Mobile** — the dialog is a centered sheet or bottom sheet; the undo toast must be reachable above the thumb area and not auto-dismiss before it's seen; type-to-confirm keyboards in.

## Anti-patterns

Confirming the reversible (the root cause of confirmation fatigue). Autofocusing the destructive button (a reflexive Enter destroys). "Are you sure? [OK] [Cancel]" — vague title, non-verb buttons. No undo where undo was possible (defaulting to a gate when a reversal would serve better). An undo toast that vanishes too fast or isn't announced/reachable by AT. Danger signalled by color alone. Defaulting/autofocusing to the destructive action. Type-to-confirm on trivial actions (friction theatre). Burying the irreversibility in prose. A double-confirm ("are you really sure?") — escalation that just trains click-through. Using a destructive confirmation for a non-destructive save (conflating with Forms-as-a-system).

## Related patterns & components

- **vs the Dialog / Modal (component)** (see dialog) — the dialog shell, the `alertdialog` role mechanics, the focus trap and Esc are the component's; this pattern decides *when* to summon a confirm dialog and *what its focus/labeling/copy contract is*.
- **vs the Toast (component)** (see toast) — Toast is the undo *surface*; this pattern owns the undo *model* (optimistic execution, the grace period, what's reversible, the timing/announcement contract).
- **vs Save & unsaved-changes (pattern)** — the "Discard changes?" guard is a sibling `flow`: same alertdialog + focus + verb-label machinery, but it guards *unsaved work on navigation* rather than an explicit destructive action. Shared mechanics, different trigger; cross-reference, don't merge.
- **vs Forms-as-a-system (pattern)** (see patterns/forms-as-a-system) — a form submit / validation gate is not a destructive confirmation; don't wrap normal submits in "are you sure."
- **vs Inline Message / Banner (components)** — an inline confirm or a persistent "danger zone" warning is the right tool when a modal interruption is disproportionate; the modal is for the moment of action, the banner for standing risk.
- **`composes`:** dialog, button, toast, banner, inline-message, text-field.

## Field POV evolution

The arc is **confirm-everything → undo-first**. Early software gated every destructive action with a warning dialog; Aza Raskin's "never use a warning when you mean undo" and the Gmail undo-send model reframed the default — let the action happen, make it reversible, and reserve interruption for the genuinely irreversible. In parallel, **type-to-confirm** rose (GitHub's "danger zone" popularised typing the repo name) as the calibrated friction for high-blast-radius actions, and **soft-delete + a grace period** (trash/restore for N days) made "irreversible" reversible for most data, pushing even more actions onto the undo path. The `alertdialog` **focus reckoning** — never autofocus destruction, focus the safe option — became the accepted a11y default over the same period. The throughline: friction moved from *uniform* (confirm all) to *calibrated* (match the rung to the danger).

## Reference instantiations

Go look at: the **WAI-ARIA APG `alertdialog` pattern** (the focus + role contract); **GitHub Primer** type-to-confirm and the "danger zone" (the high-blast-radius rung); **Gmail** undo-send (the optimistic + grace-period model); **IBM Carbon** danger modal + danger button; **Shopify Polaris** critical/destructive actions; **Material 3** dialogs (destructive). NN/g on confirmation dialogs, undo, and error prevention for the rationale.

## Sources cited

- Aza Raskin — "Never Use a Warning When you Mean Undo" (the undo-first thesis) (*secondary; widely cited*).
- Nielsen Norman Group — confirmation dialogs, undo, error prevention, confirmation fatigue (*verify articles/dates*).
- WAI-ARIA Authoring Practices Guide — the `alertdialog` pattern, focus management (current; *verify*).
- WCAG 2.2 — §3.3.4 (Error Prevention: legal/financial/data) and §3.3.6 (Error Prevention: all) — reversible/checked/confirmed (*verify*).
- GitHub Primer — type-to-confirm / "danger zone" pattern (*verify*).
- IBM Carbon — danger modal + danger button (v11, 2025; *verify*); Shopify Polaris — critical/destructive actions (2024–25; *verify*); Material 3 — dialogs (2024–25; *verify*); Atlassian, Adobe Spectrum, GOV.UK — destructive/confirm patterns where documented (*spotty; flag where absent*).
- Gmail — undo-send / optimistic-undo model (*secondary; product observation*).

`notes.unverified`: the undo-window lengths (toast seconds; trash ~30 days) are conventions, not constants — flag as such. The button-order convention is genuinely contested (macOS vs Windows vs web); the brief takes the position that labeling + focus + styling carry the safety, not order. Which design systems ship a *named* destructive-confirmation pattern vs only a danger button + dialog is mixed (Carbon, Polaris, Primer clearest); verify before asserting convergence. Current version strings flagged.

## Agent-consumable schema

```yaml
identity:
  id: destructive-confirmation
  name: Destructive confirmation
  aliases: [delete confirmation, are-you-sure, confirm-vs-undo, type-to-confirm, danger zone]
  tier: flow
  goal: help-user-act
  status: draft
problem: >
  Guard an irreversible or high-cost action without training click-through.
  The central question is confirm vs undo: most destructive actions should be
  undoable, not confirmed; confirmation is reserved for the genuinely
  irreversible/high-blast-radius. Applies to delete/remove/discard/overwrite/
  send/publish; NOT to reversible/frequent actions (use undo) or form submits.
composition:
  requires: [dialog, button, toast, banner, inline-message, text-field]
  delta: confirm-vs-undo decision, the friction ladder, focus/labeling contract, soft-delete grace-period model, the copy
decision_rules:
  confirm_vs_undo:
    - { if: "reversible (or soft-deletable) and not catastrophic", use: "execute immediately + undo toast (no dialog)" }
    - { if: "genuinely irreversible OR high blast-radius (bulk/shared/financial/legal)", use: "confirm before executing" }
    - { if: "frequent action", use: "lean to undo even if mildly destructive (a dialog guarantees click-through fatigue)" }
  friction_ladder:
    - { if: "reversible low-cost", use: "no friction (or undo if mistake plausible)" }
    - { if: "reversible but noticeable", use: "optimistic action + undo toast" }
    - { if: "irreversible bounded", use: "simple confirm dialog (alertdialog)" }
    - { if: "irreversible high blast-radius", use: "type-to-confirm" }
    - { if: "catastrophic/system-level", use: "type-to-confirm + extra friction (re-auth)" }
  dialog:
    - { if: "showing a confirm dialog", use: "role=alertdialog; focus the safe/cancel option (NEVER the destructive button); Esc/backdrop cancel" }
  buttons:
    - { if: "always", use: "action-specific verb labels (Delete 3 files), danger styling + text (not color alone), cancel secondary, destructive never default/autofocused" }
    - { if: "button order", use: "pick one convention per product (macOS/Windows diverge); safety is labeling+focus+styling, not order" }
  type_to_confirm:
    - { if: "destroys something large/shared/irrecoverable (repo/org/prod/db)", use: "require typing the resource name to enable the destructive button" }
    - { if: "trivial action", use: "do NOT use type-to-confirm (friction theatre)" }
  undo_model:
    - { if: "reversible", use: "optimistic execution + grace period (soft delete); Toast Undo; window long enough to notice + reach" }
    - { if: "30-day restore exists", use: "say so in copy and lean undo-first" }
    - { if: "true undo impossible", use: "fall back to confirm" }
  bulk:
    - { if: "acting on N items", use: "state count + exact scope; raise the rung with N" }
  when_not_to_confirm:
    - { if: "reversible/low-cost/frequent", use: "do not confirm; use undo or nothing (over-confirmation causes click-through)" }
flow: >
  Two paths. UNDO (default, reversible): intent -> optimistic execution
  (UI shows done, item soft-deleted) -> grace period (undo toast + timer) ->
  commit (timer elapses -> irreversible delete) OR undo (reverse + restore +
  focus return). User never blocked; safety is the reversal window. CONFIRM
  (irreversible/high-blast): intent -> alertdialog open (focus to safe/cancel)
  -> [type-to-confirm sub-state: destructive disabled until name matches] ->
  confirm (execute + success feedback) OR cancel (Esc/backdrop/cancel -> no-op,
  focus returns). Signature: the optimistic-now -> reversible-window ->
  committed timeline; window length (toast seconds vs trash days) chosen by
  recoverability cost.
accessibility_orchestration: >
  role=alertdialog (announced as a decision), labelled by title + described by
  body; focus moves to the safe/cancel control on open (NEVER the destructive
  button) and returns to the trigger on close; Esc cancels; the undo toast must
  be announced (polite live region) AND keyboard-reachable before it dismisses
  — don't hide a critical reversal behind an unreachable 4s toast (prefer a
  persistent affordance for critical undo).
content: >
  Title = specific question (Delete this project?, not Are you sure?); body =
  consequence + scope + reversibility (what, to whom, can it be undone / 30-day
  restore); button = the action verb matching the title (never OK/Yes); undo
  toast confirms + offers reversal (Project deleted. Undo.); type-to-confirm
  names exactly what to type. Copy carries the safety; never blame or bury the
  irreversibility.
layout: >
  Light. Confirm dialog = small centered modal (title + body + button row,
  cancel secondary, danger button distinct, platform-conventional order); undo
  toast in the toast region with inline Undo; type-to-confirm adds one labeled
  input above the button row. Mobile: centered/bottom sheet; toast reachable,
  no premature auto-dismiss.
variants: [undo-toast, simple-confirm-dialog, type-to-confirm, inline-confirm, bulk-confirmation]
anti_patterns:
  - confirming the reversible (confirmation fatigue)
  - autofocusing the destructive button
  - "Are you sure? OK/Cancel" vague title + non-verb buttons
  - no undo where undo was possible
  - undo toast that vanishes too fast or isn't announced/reachable
  - danger signalled by colour alone
  - defaulting/autofocusing to the destructive action
  - type-to-confirm on trivial actions (friction theatre)
  - burying the irreversibility in prose
  - double-confirm escalation (trains click-through)
  - using destructive confirmation for a non-destructive save
reference_instantiations:
  - { system: "WAI-ARIA APG", look_at: "alertdialog pattern (focus + role contract)" }
  - { system: "GitHub Primer", look_at: "type-to-confirm / danger zone" }
  - { system: "Gmail", look_at: "undo-send (optimistic + grace period)" }
  - { system: "IBM Carbon", look_at: "danger modal + danger button" }
  - { system: "Shopify Polaris", look_at: "critical/destructive actions" }
relations:
  composes: [dialog, button, toast, banner, inline-message, text-field]
  relates-to: [save-and-unsaved-changes, forms-as-a-system, view-state-orchestration, notification-orchestration]
  boundary: >
    The Dialog component owns the alertdialog shell/focus-trap/Esc; this pattern
    decides when to summon it and its labeling/copy contract. Toast owns the
    undo surface; this pattern owns the undo model (grace period). Save &
    unsaved-changes is a sibling flow (discard-changes guard) sharing the
    mechanics with a different trigger. A form submit is not a destructive
    confirmation. Inline Message/Banner are the inline/standing-risk
    alternatives to a modal interruption.
notes:
  contested: "button order (macOS vs Windows vs web — safety from labeling+focus+styling, not order); how high the undo-first default should reach into mildly-irreversible actions"
  unverified: "undo-window lengths (toast seconds; trash ~30 days) are conventions not constants; which systems ship a NAMED destructive-confirmation pattern vs a danger button + dialog (Carbon/Polaris/Primer clearest); version strings"
```
