---
okf_version: "0.1"
type: pattern-brief
title: Destructive confirmation
description: The flow that guards an irreversible or high-cost action — and the question at its heart, confirm vs undo. The undo-first default, the five-rung friction ladder (no friction → undo toast → confirm dialog → type-to-confirm → MFA/approver), the alertdialog focus contract (never autofocus the destructive button), action-verb labels, the soft-delete grace-period model and its timeline, and the copy that carries the safety. The first flow-tier brief, so flow & states carries the weight and layout is light. Composes Dialog/alertdialog + Button + Toast + Banner + Inline Message; borders the Dialog component, the Toast component, Save & unsaved-changes, Forms-as-a-system, and inline warnings.
tags: [patterns, destructive, confirmation, undo, accessibility, help-user-act]
tier: flow
goal: help-user-act
status: stable
aliases: [Destructive confirmation, delete confirmation, are-you-sure, confirm-vs-undo, type-to-confirm, danger zone]
last-audited: 2026-06-18
timestamp: 2026-06-18
---

# Destructive confirmation

> Every product has actions that hurt to get wrong — delete, remove, discard, overwrite, send, publish. The reflex is to throw an "Are you sure?" in front of each one, and the reflex is mostly wrong. The field's hard-won lesson is that **most destructive actions should be undoable, not confirmed**: a confirmation that fires too often becomes motor-memory noise, dismissed without reading, so it protects nothing and the one time it mattered, it failed. This brief owns the *flow* that guards a dangerous action — the confirm-vs-undo decision first, then the friction ladder, the focus and labeling contract, and the copy that actually carries the safety. It defers the dialog shell to the Dialog component and the undo surface to Toast, and resolves only the flow.

---

## Problem & context

The recurring problem is calibration: too little friction and users destroy things by accident; too much and you get **confirmation fatigue** — the brain treats the interruption as a mechanical obstacle, not a semantic question, and clicks the primary action blind, so the warning fails precisely when it matters (the boy who cried wolf). The deeper insight, canonically Aza Raskin's ("never use a warning when you mean undo," 2007), is that because people act on motor memory, a confirmation can't reliably prevent the *mistaken* action — it only slows the *successful* ones and manufactures false security. A modal *interrupts before* and demands a prediction ("will I regret this?"); **undo lets the action happen and offers a cheap reversal after** — which matches how people actually work: act, notice, correct. So the first question is never "what should the dialog say" but "**does this need a dialog at all, or does it need undo?**"

But pure undo isn't universally viable. Where an action is genuinely irreversible — legal, financial, compliance, cascading-architecture (delete a production database, revoke a root org, submit a tax return) — the frontend can't reverse it, and the system must deploy *escalating deliberate friction* to break the motor loop. Note that reversibility is often an **engineering** choice: soft-delete makes "irreversible" reversible for most data. The pattern applies to any irreversible or high-cost action; it does **not** apply to reversible, low-cost, or frequent actions (use undo or nothing), and it is **not** a form submit or validation gate. The field converges on one philosophy — **friction scales with irreversibility and cost** — and diverges only on the implementation. The decisions below resolve by reversibility, blast radius, and frequency rather than by reflex.

## Composition

The flow assembles briefed components and adds the guard logic; it re-derives none of them.

- **Dialog** (see dialog) — the interruption container, used in its `alertdialog` mode for the *pessimistic* (confirm) path; the component owns the modal shell, focus trap, and Esc; this pattern decides *when* to summon it and *what its focus/labeling contract is*.
- **Button** (see button) — the destructive action button (danger styling) and the cancel/safe button; the labeling and order are this pattern's call.
- **Toast** (see toast) — the *optimistic* (undo) surface (action + "Undo"); the component owns the toast; this pattern owns the undo *model* (the background queue, grace period, what's reversible).
- **Banner / Inline Message** (see banner, see inline-message) — the inline-confirm alternative and any persistent "danger zone" warning, when a modal interruption is disproportionate.
- **Text Field** (see text-field) — the type-to-confirm input for the highest-blast-radius actions.

**The delta this pattern adds** is the guard flow: the confirm-vs-undo decision, the friction ladder, the focus/labeling contract, the soft-delete grace-period model and its timeline, and the copy — none of which any single component owns.

## Decision rules

The analytical core. Machine-resolvable where a real threshold exists.

**1. Confirm vs undo — the central fork.** The default bias is strongly toward undo.
- `IF reversible (or soft-deletable) AND not catastrophic` → **execute immediately + undo toast** (no dialog).
- `IF genuinely irreversible OR high blast-radius (bulk, shared/destructive-to-others, financial, legal, hard-delete)` → **confirm before executing**.
- `IF frequent AND low-consequence` → **immediate execution, no confirm and no undo** (a dialog here only manufactures fatigue).
- The test, in order: **reversibility** → **blast radius** → **frequency**. Undo wins unless irreversibility or blast radius forces a confirm. (WCAG 2.2 §3.3.4/§3.3.6 set the legal floor: high-stakes submissions must be reversible, checked, or confirmed.)

**2. The friction ladder** — match friction to severity; never more than the danger warrants. Every rung costs every user every time.
- **L0 Trivial** (frequent, recoverable, negligible) → instant, no friction.
- **L1 Recoverable** (soft-delete) → optimistic action + **undo toast**.
- **L2 Irreversible, single-item** → **simple confirm dialog** (alertdialog).
- **L3 Catastrophic** (massive blast radius, multi-user/system) → **type-to-confirm dialog**.
- **L4 Critical** (existential infra/finance) → **MFA challenge or a secondary-approver requirement**.

**3. The confirmation dialog.**
- Use `role="alertdialog"` (not a plain dialog) so AT announces a critical decision; the component supplies the focus trap and Esc.
- **NEVER autofocus the destructive button.** Focus the **cancel/safe** option (or the dialog/its heading) so a reflexive Enter/Space can't destroy. Esc and backdrop click cancel (the safe outcome) and return focus to the trigger.
- Title is the **specific question**; body states the **consequence, scope, and irreversibility**.

**4. Button labeling & placement.**
- **Action-specific verbs** — "Delete 3 files," "Discard draft," "Deactivate account" — never "OK/Yes/Confirm." A label that doesn't say what happens isn't a safeguard.
- **Destructive styling** (the danger button) AND a text label — never color alone.
- **Order:** the web default is **cancel left, destructive action right** (Material 3, Carbon — right-aligned affirmative matching LTR forward-momentum); this resolves the historical Windows-affirmative-left / macOS-affirmative-right divergence for the web. *But order is the weakest signal* — the safety comes from the **verb label + focus on the safe option + danger styling + never being the autofocused default**, not from which side the button sits. Pick the convention and hold it; don't rely on it.

**5. Type-to-confirm** — the L3 rung.
- `IF the action destroys something large/shared/irrecoverable (delete a repo, an org, a production database, a workspace)` → require the user to **type the resource's exact name** to enable the destructive button.
- It works because it forces a cognitive mode-switch that disrupts the automatic motor loop — deliberate intent, not passive acknowledgment — and re-states exactly what's being destroyed. Keep the prompt and input labeled; show the exact string to type.
- `IF trivial` → do **not** use it (friction theatre that trains resentment).

**6. The undo model.**
- Prefer **optimistic execution + a grace period**: perform the action immediately in the UI (the user sees it done), but defer the irreversible commit behind a window — a **soft delete** held in a background queue with a TTL, recoverable via the toast's Undo (seconds) or a trash/restore (days).
- The undo **toast** visibility is ≈**5–10s** (a convention, not a constant), and on Undo the UI reverts immediately and an abort signal is sent to the queue.
- `IF true undo is impossible` → fall back to confirm; `IF a longer restore window exists (e.g. 30-day trash)` → say so in the copy and lean undo-first.

**7. Bulk & scope.**
- `IF acting on N items` → state the **exact count in the title** ("Delete 14 files?") and **enumerate cascading consequences** in the body ("…and their 142 tasks"); the bigger the scope, the higher the rung.

**8. When NOT to confirm.**
- `IF reversible / low-cost / frequent (save draft, toggle, remove-from-view)` → don't confirm; use undo or nothing. `IF it's input error` → inline validation, not a modal. Over-confirmation is itself the defect — it's the cause of the click-through reflex that makes the *necessary* confirmations fail.

## Flow & states

The heavy section for this tier. Two paths; the decision rules choose which.

**Path A — the undo path (default, reversible).** *Intent* (user triggers the action) → *optimistic execution* (the UI reflects it done immediately — the row collapses, the item vanishes; architecturally it's soft-deleted into a background queue with a TTL, a countdown begins) → *feedback & affordance* (an undo Toast renders with a single Undo action; a polite live region announces it so AT users know reversal is possible without losing their place) → **resolution fork**: ignore → timer expires → toast exits → the hard delete commits; **or** Undo → an abort signal cancels the queued job → the item reappears (optimistic revert) → a success toast confirms restoration. The user is never *blocked*; the safety is the reversal window, not a gate.

An *illustrative* timeline (the orchestration must avoid race conditions): T=0 item unmounts; T≈50ms toast renders + job enters the queue; T=50ms–~7s the user has full agency elsewhere while the toast persists; T≈7s toast begins exit; T≈7.3s toast unmounts + the queue **locks** the job (no late abort); T≈7.5s the database purge runs. (Exact values are a convention.)

**Path B — the confirm path (irreversible/high-blast).** *Intent* → *interruption* (backdrop renders, underlying UI inert, `role="alertdialog"`, focus trapped) → *evaluation* (focus on the **safe/cancel** option; user reads the consequence; if type-to-confirm, the destructive button stays **disabled until the typed string matches**) → **resolution fork**: Cancel / Esc / backdrop → close, no-op, focus returns to the trigger; **or** Confirm → *processing* (the dialog stays open, the destructive button shows a progress state and is disabled to prevent a double-submit, awaiting the server) → *feedback* (dialog dismisses; because the triggering element is often now gone from the DOM, focus moves to a **logical anchor** — the top of the remaining list or the page heading; an optional informational success toast). The action only happens after deliberate confirmation; there may be no undo after.

The **grace-period timeline** (optimistic now → reversible window → committed) is the pattern's signature, and choosing the window by recoverability cost (toast seconds vs trash days) is the core flow decision.

## Accessibility orchestration

The a11y the *flow* owns (the Dialog/Toast components own their own widget ARIA):
- **`role="alertdialog"`** (not `dialog`) so AT treats it as a critical, time-sensitive decision; labelled by its title (`aria-labelledby`) and **described by its body** (`aria-describedby` → the consequence paragraph) so the whole warning is announced cohesively, not discovered piecemeal.
- **The focus contract** — focus moves into the dialog on open to the **safe/cancel** control (never the destructive one), is trapped while open, and **returns to the trigger** on close (or a predetermined successor if the trigger was destroyed). The single most important a11y *and* safety property here.
- **The undo-toast timing problem** — an auto-dismissing toast is an a11y trap: the Undo must be **announced** (polite live region) *and* reachable before it vanishes. **Pause the toast's expiration timer the moment it receives keyboard focus or hover**, so screen-reader and switch users keep control of the reversion window; for genuinely critical undo, prefer a persistent affordance over an ephemeral toast.
- **Esc cancels**; the destructive action is never the default action of the dialog.

## Content & copy

The copy *is* much of the safety — near-ALWAYS load-bearing.
- **Title = the specific question** — `{Verb} + {Noun}?` ("Delete 3 files?", "Remove integration?"), never "Are you sure?" or "Warning." A vague title makes the user reconstruct what's happening at the worst moment.
- **Body declares facts, doesn't ask permission** — consequence + scope + irreversibility + cascade: "This action cannot be undone. This will permanently delete the repository and remove access for 12 active collaborators."
- **Button = the action verb** matching the title — `[ Cancel ]` adjacent to `[ Delete repository ]`; never "Yes/No/OK" in isolation.
- **Type-to-confirm prompt** names exactly what to type ("Type **acme-prod** to confirm").
- **Undo-toast copy** is brief — confirm + remedy: "File deleted. **Undo**."
- Never blame; never bury the irreversibility in a sentence the user won't read.

## Layout & structure

Light, by tier — this is a moment, not a structure. The confirm dialog is a **narrow centered modal** (~400–480px, for a readable line length; never full-screen on desktop), title + body + a button row aligned bottom-right (LTR forward-momentum) with cancel secondary and the danger button distinct on the far right. The undo toast sits in the toast region (bottom-left or bottom-center), non-obstructive, not overlapping nav or the spot the deleted item vacated. Type-to-confirm adds one labeled input above the button row. **Mobile:** the dialog often morphs to a **bottom sheet** (thumb reach); buttons stack vertically full-width with **Cancel at the very bottom** (closest to the thumb) as the most accessible escape.

## Variants & responsive

- **Undo toast** (L1, reversible) vs **simple confirm dialog** (L2, irreversible bounded) vs **type-to-confirm** (L3, high blast-radius, primary bound to a string match) vs **inline confirm** (a confirm rendered in place — a dense table row converting to a "Delete? · Confirm / Cancel" state — when a modal would break context).
- **Bulk confirmation** — count + scope in the title/body; the rung rises with N.
- **Mobile** — bottom sheet, vertically stacked full-width buttons, cancel closest to thumb; the undo toast must be reachable and not auto-dismiss before it's seen.

## Anti-patterns

Confirming the reversible (the root cause of confirmation fatigue). Autofocusing the destructive button (a reflexive Enter destroys). "Are you sure? [OK] [Cancel]" — vague title, non-verb buttons. No undo where undo was possible (a gate where a reversal would serve better) — including refusing optimistic undo because the backend prefers synchronous calls (UX dictates architecture, not vice versa). An undo toast that vanishes too fast (2s) or isn't announced/reachable by AT. Danger signalled by color alone. Defaulting/autofocusing to the destructive action. Type-to-confirm on trivial actions (friction theatre). Burying the irreversibility in prose. Double-confirm escalation ("are you really sure?") that just trains click-through. Using a destructive confirmation for a non-destructive save (conflating with Forms-as-a-system).

## Related patterns & components

- **vs the Dialog / Modal (component)** (see dialog) — the dialog shell, the `alertdialog` role mechanics, the focus trap and Esc are the component's; this pattern decides *when* to summon a confirm dialog and *what its focus/labeling/copy contract is*.
- **vs the Toast (component)** (see toast) — Toast is the undo *surface*; this pattern owns the undo *model* (optimistic execution, the background queue, the grace period, what's reversible, the timing/announcement contract).
- **vs Save & unsaved-changes (pattern)** — the "Discard changes?" guard is a sibling `flow`: the same alertdialog + focus + verb-label machinery, but it guards *unsaved work on navigation* rather than an explicit destructive command. Shared mechanics, different trigger; cross-reference, don't merge.
- **vs Forms-as-a-system (pattern)** (see patterns/forms-as-a-system) — a form submit / validation gate is not a destructive confirmation; don't wrap normal submits in "are you sure."
- **vs Inline Message / Banner (components)** — an inline confirm or a standing "danger zone" warning is the right tool when a modal interruption is disproportionate; the modal is for the moment of action, the banner for standing risk.
- **`composes`:** dialog, button, toast, banner, inline-message, text-field.

## Field POV evolution

The arc is **confirm-everything → undo-first → calibrated friction**. The late-1990s–2005 era gated every action with synchronous `window.confirm()`, training a generation into fatigue. The 2007 **Raskin pivot** ("never use a warning when you mean undo") reframed the default: forgive the inevitable slip with a reversal rather than predict it with a warning. Through the 2010s, **optimistic UIs** (AJAX, Gmail's undo-send) made the action+grace-period model the gold standard for routine deletions. From ~2018 a **friction reckoning** followed as enterprise SaaS blast radius grew catastrophic — GitHub's "danger zone" and **type-to-confirm** established that extreme consequence needs extreme, un-automatable friction — while **soft-delete + grace period** pushed even more actions onto the undo path. WCAG 2.2 (2023) then formalised error prevention as a compliance necessity (§3.3.4/§3.3.6). The throughline: friction moved from *uniform* to *calibrated* — match the rung to the danger.

## Reference instantiations

Go look at: the **WAI-ARIA APG `alertdialog` pattern** (the focus + role + aria-describedby contract); **GitHub Primer** type-to-confirm and the "danger zone" (the high-blast-radius rung); **Gmail** undo-send (the optimistic + grace-period model); **IBM Carbon** danger modal + danger button (focus handling, the no-autofocus-destructive rule, button alignment); **Shopify Polaris** critical/destructive actions (verb-first consequence copy); **GOV.UK** for irreversible legal/tax transactions where undo is impossible. NN/g on confirmation dialogs, undo, and error prevention for the rationale.

## Sources cited

- Aza Raskin — "Never Use a Warning When you Mean Undo" (2007; the undo-first thesis) (*secondary; widely cited*).
- Nielsen Norman Group — confirmation dialogs, undo, error prevention, confirmation fatigue (*verify articles/dates*).
- WAI-ARIA Authoring Practices Guide — the `alertdialog` pattern, focus management, `aria-describedby` (current; *verify*).
- WCAG 2.2 — §3.3.4 (Error Prevention: legal/financial/data) and §3.3.6 (Error Prevention: all) (*verify*).
- GitHub Primer — type-to-confirm / "danger zone" pattern (*verify*).
- IBM Carbon — danger modal + danger button, button alignment (v11, 2025; *verify*); Shopify Polaris — critical/destructive actions + microcopy (2024–25; *verify*); Material 3 — dialogs, the affirmative-right button convention (2024–25; *verify*); Atlassian, Adobe Spectrum, GOV.UK — destructive/confirm patterns where documented (*spotty; flag where absent*).
- Gmail — undo-send / optimistic-undo model (*secondary; product observation*).

`notes.unverified`: the undo-window lengths (toast ~5–10s; trash ~30 days) and the dialog-width band (~400–480px) are conventions, not constants — flag as such, and the grace-period millisecond timeline is illustrative. Button order is genuinely contested (Windows vs macOS vs web): both passes land on cancel-left/action-right as the web default (Material/Carbon), but the brief holds that the safety comes from label + focus + styling, not order. Which design systems ship a *named* destructive-confirmation pattern vs only a danger button + dialog is mixed (Carbon, Polaris, Primer clearest); verify before asserting convergence. Current version strings flagged.

## Agent-consumable schema

```yaml
identity:
  id: destructive-confirmation
  name: Destructive confirmation
  aliases: [delete confirmation, are-you-sure, confirm-vs-undo, type-to-confirm, danger zone]
  tier: flow
  goal: help-user-act
  status: stable
problem: >
  Guard an irreversible or high-cost action without training click-through.
  The central question is confirm vs undo: most destructive actions should be
  undoable, not confirmed; confirmation is reserved for the genuinely
  irreversible/high-blast-radius. Applies to delete/remove/discard/overwrite/
  send/publish; NOT to reversible/frequent actions (use undo) or form submits.
composition:
  requires: [dialog, button, toast, banner, inline-message, text-field]
  delta: confirm-vs-undo decision, the friction ladder, focus/labeling contract, soft-delete grace-period model + timeline, the copy
decision_rules:
  confirm_vs_undo:
    - { if: "reversible (or soft-deletable) and not catastrophic", use: "execute immediately + undo toast (no dialog)" }
    - { if: "genuinely irreversible OR high blast-radius (bulk/shared/financial/legal/hard-delete)", use: "confirm before executing" }
    - { if: "frequent and low-consequence", use: "immediate execution, no confirm and no undo" }
  friction_ladder:
    - { level: "L0 trivial (frequent, recoverable, negligible)", use: "instant, no friction" }
    - { level: "L1 recoverable (soft-delete)", use: "optimistic action + undo toast" }
    - { level: "L2 irreversible single-item", use: "simple confirm dialog (alertdialog)" }
    - { level: "L3 catastrophic (massive blast radius)", use: "type-to-confirm dialog" }
    - { level: "L4 critical (existential infra/finance)", use: "MFA challenge or secondary-approver" }
  dialog:
    - { if: "showing a confirm dialog", use: "role=alertdialog; focus the safe/cancel option (NEVER the destructive button); Esc/backdrop cancel + return focus" }
  buttons:
    - { if: "always", use: "action-specific verb labels (Delete 3 files), danger styling + text (not colour alone), cancel secondary, destructive never default/autofocused" }
    - { if: "button order", use: "web default cancel-left/action-right (Material/Carbon); but safety is label+focus+styling, not order" }
  type_to_confirm:
    - { if: "destroys something large/shared/irrecoverable (repo/org/prod/db)", use: "require typing the exact resource name to enable the destructive button" }
    - { if: "trivial action", use: "do NOT use type-to-confirm (friction theatre)" }
  undo_model:
    - { if: "reversible", use: "optimistic execution + grace period (soft delete, TTL queue); Toast Undo ~5-10s; revert UI + abort signal on Undo" }
    - { if: "longer restore window exists (e.g. 30-day trash)", use: "say so in copy and lean undo-first" }
    - { if: "true undo impossible", use: "fall back to confirm" }
  bulk:
    - { if: "acting on N items", use: "exact count in title + enumerate cascade in body; raise the rung with N" }
  when_not_to_confirm:
    - { if: "reversible/low-cost/frequent (save draft, toggle, remove-from-view)", use: "do not confirm; undo or nothing" }
    - { if: "input error", use: "inline validation, not a modal" }
flow: >
  Two paths. UNDO (default, reversible): intent -> optimistic execution (UI
  shows done; item soft-deleted into a TTL queue; countdown) -> feedback (undo
  toast + polite live-region announce) -> resolution (timer expires -> commit
  hard delete; OR Undo -> abort signal + revert + success toast). User never
  blocked. Illustrative timeline: T0 unmount; T~50ms toast+queue; T~7s exit;
  T~7.3s unmount + queue locks (no late abort); T~7.5s purge. CONFIRM
  (irreversible/high-blast): intent -> interruption (alertdialog + focus trap)
  -> evaluation (focus safe/cancel; type-to-confirm keeps destructive disabled
  until string matches) -> resolution (cancel/Esc/backdrop -> no-op + focus
  return; OR confirm -> processing (button loading + disabled, await server) ->
  feedback (dismiss + focus to logical anchor since trigger may be gone)).
  Signature: optimistic-now -> reversible-window -> committed; window length
  (toast seconds vs trash days) chosen by recoverability cost.
accessibility_orchestration: >
  role=alertdialog (announced as a critical decision), aria-labelledby (title) +
  aria-describedby (consequence body); focus moves to the safe/cancel control on
  open (NEVER the destructive button), trapped while open, returns to the trigger
  (or a successor) on close; Esc cancels; the undo toast is announced (polite
  live region) AND its timer pauses on focus/hover so it stays reachable — prefer
  a persistent affordance for critical undo.
content: >
  Title = specific {Verb}+{Noun}? question (Delete 3 files?, not Are you sure?);
  body declares facts (consequence + scope + irreversibility + cascade), no
  permissive language; button = the action verb matching the title (never
  OK/Yes); type-to-confirm names exactly what to type; undo toast brief
  (File deleted. Undo.). Copy carries the safety; never blame or bury the
  irreversibility.
layout: >
  Light. Confirm dialog = narrow centered modal (~400-480px, never full-screen
  desktop); button row bottom-right, cancel secondary, danger button far-right
  distinct; undo toast bottom-left/center, non-obstructive. Type-to-confirm adds
  one labeled input above the buttons. Mobile: bottom sheet, vertically stacked
  full-width buttons, Cancel at the very bottom (thumb-closest); toast reachable,
  no premature auto-dismiss.
variants: [undo-toast (L1), simple-confirm-dialog (L2), type-to-confirm (L3), inline-confirm (contextual), bulk-confirmation]
anti_patterns:
  - confirming the reversible (confirmation fatigue)
  - autofocusing the destructive button
  - "Are you sure? OK/Cancel" vague title + non-verb buttons
  - no undo where undo was possible (incl. refusing optimistic undo for backend convenience)
  - undo toast that vanishes too fast or isn't announced/reachable
  - danger signalled by colour alone
  - defaulting/autofocusing to the destructive action
  - type-to-confirm on trivial actions (friction theatre)
  - burying the irreversibility in prose
  - double-confirm escalation (trains click-through)
  - using destructive confirmation for a non-destructive save
reference_instantiations:
  - { system: "WAI-ARIA APG", look_at: "alertdialog pattern (focus + role + aria-describedby)" }
  - { system: "GitHub Primer", look_at: "type-to-confirm / danger zone" }
  - { system: "Gmail", look_at: "undo-send (optimistic + grace period)" }
  - { system: "IBM Carbon", look_at: "danger modal + danger button, button alignment" }
  - { system: "Shopify Polaris", look_at: "critical/destructive actions + verb-first copy" }
relations:
  composes: [dialog, button, toast, banner, inline-message, text-field]
  relates-to: [save-and-unsaved-changes, forms-as-a-system, view-state-orchestration, notification-orchestration]
  boundary: >
    The Dialog component owns the alertdialog shell/focus-trap/Esc; this pattern
    decides when to summon it and its labeling/copy contract. Toast owns the undo
    surface; this pattern owns the undo model (queue + grace period). Save &
    unsaved-changes is a sibling flow (discard-changes guard) sharing the
    mechanics with a different trigger. A form submit is not a destructive
    confirmation. Inline Message/Banner are the inline/standing-risk alternatives
    to a modal interruption.
notes:
  contested: "button order (Windows vs macOS vs web — both passes land cancel-left/action-right as the web default, but safety is label+focus+styling, not order); how far the undo-first default should reach into mildly-irreversible actions"
  unverified: "undo-window lengths (toast ~5-10s; trash ~30 days), the ~400-480px dialog width, and the grace-period ms timeline are conventions/illustrative, not constants; which systems ship a NAMED destructive-confirmation pattern vs a danger button + dialog (Carbon/Polaris/Primer clearest); version strings"
```
