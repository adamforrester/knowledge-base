# Destructive confirmation — external-agent pass

*Second independent pass for the Destructive confirmation pattern brief (first `flow`-tier brief). Captured as the dual-agent audit record. Synthesised with `claude.md` into `patterns/destructive-confirmation.md`.*

---

## Destructive confirmation

A destructive confirmation is the temporal flow designed to guard against the irreversible loss of user data, access, or system state. Its central function is not to render an overlay but to answer a question of interaction friction: should the system interrupt the user to confirm, or execute optimistically and offer a path to undo? By calibrating friction to the action's blast radius, the flow prevents catastrophic loss while mitigating the cognitive fatigue that renders routine warnings invisible. This brief defines the orchestration; it references but does not re-derive the Dialog/Modal, Toast, Button, Banner, or Inline Message components.

### Problem & context

Confirmation fatigue arises from habituation: when a system frequently interrupts routine workflows, the brain treats the interruption as a mechanical obstacle, not a semantic question, and the user clicks the primary action blindly — the warning fails precisely when most needed (the boy who cried wolf). Canonically articulated in Aza Raskin's 2007 axiom "Never use a warning when you mean undo": because users act on motor memory, a confirmation doesn't prevent the mistaken action; it only slows successful ones and creates false security. The superior paradigm, where feasible, is to let the action proceed with an optimistic undo. But pure undo isn't universally viable — legal/financial/compliance/cascading-architecture actions are genuinely irreversible (delete a production DB, revoke a root org, submit a tax return), and there the system must deploy escalating deliberate friction. The field converges on one philosophy: **friction must scale with irreversibility and cost.**

### Composition

No new primitives; orchestrates existing components through a temporal lifecycle. Dialog/Modal (alertdialog) — the interruption container, pessimistic path only, traps focus. Button (Danger/Destructive) — trigger + execution, red styling + action-verb label. Toast/Snackbar — transient undo affordance + success feedback, strict TTL. Banner/Inline Message — persistent in-context validation / permanent state change.

### Decision rules

**1. Confirm vs undo — central fork.** IF reversible AND soft-deleted → Undo (optimistic + Toast). IF high blast-radius OR hard-deleted OR legal/financial → Confirm (pessimistic + Dialog). IF high frequency AND low consequence → immediate execution (no confirm, no undo). Soft-delete architectures let the UI abstract a backend grace period as Undo. WCAG 2.2 §3.3.4/§3.3.6 mandate high-stakes submissions be reversible, checked, or confirmed.

**2. The friction ladder (5 levels).** L0 Trivial (high-freq, recoverable, negligible) → instant. L1 Recoverable (soft-delete) → optimistic + Undo toast. L2 Irreversible single-item → simple confirm dialog. L3 Catastrophic (massive blast radius, multi-user/system) → type-to-confirm dialog. L4 Critical (existential infra/finance) → MFA challenge or secondary-approver requirement.

**3. The confirmation dialog.** IF Confirm flow → `role="alertdialog"`. IF dialog opens → focus the Cancel/safe option (never autofocus destructive). IF backdrop/Esc → cancel + return focus to origin.

**4. Button labeling & placement.** Action-specific verbs ("Delete user", not "OK"). Button order: on web, place Cancel (secondary) left, Confirm (primary danger) right. Historical divergence (Windows affirmative-left, macOS affirmative-right); the dominant web convention (Material 3, Carbon) adopted right-aligned affirmative, aligning with LTR reading (the forward progression at the terminal point of the scan).

**5. Type-to-confirm.** IF catastrophic → require exact string match (user input == resource name) to enable Confirm. Forces a cognitive mode-switch that disrupts the motor loop; deliberate intent, not passive acknowledgment.

**6. The undo model.** Display Toast with explicit Undo; visibility 5000–10000ms; on Undo, revert UI immediately + send abort to backend queue. Optimistic update hides deletion latency; a background queue holds the command until the grace period expires.

**7. Bulk & scope.** IF item_count > 1 → exact count in the title ("Delete 14 files?"). IF cascading → enumerate downstream consequences in the body.

**8. When NOT to confirm.** IF save-draft / toggle / remove-from-view → execute without a dialog. IF error handling → inline validation, not modal interruption. Over-confirmation trains blind dismissal and destroys the pattern's efficacy.

### Flow & states (heavy)

**Path A — Undo (optimistic).** Intent (trigger) → Optimistic Execution (item vanishes; background countdown 5000–10000ms; data queued/TTL/inactive) → Feedback & Affordance (Toast renders with Undo; `aria-live="polite"` announces) → Resolution Fork (ignore → timer expires → exit animation → hard delete; OR Undo → abort signal → item reappears → success toast). Tightly controlled timeline (illustrative): T=0ms item unmounts; T=50ms toast renders + job queued; T=50–7000ms user has full agency; T=7000ms toast exit animation; T=7300ms toast unmounts + queue locks (no late abort); T=7500ms DB purge.

**Path B — Confirm (pessimistic).** Intent → Interruption (backdrop, underlying UI inert, `role="alertdialog"`, focus trapped) → Evaluation (focus to Cancel/safe; user reads consequence; if type-to-confirm, primary stays disabled until exact string match) → Resolution Fork (Cancel/backdrop/Esc → close + return focus to trigger, backend untouched; OR Confirm → proceed) → Processing (dialog stays open, destructive button shows progress + disabled to prevent duplicate submit, await server) → Feedback (dialog dismisses; since the trigger element may no longer exist in the DOM, focus moves to a logical anchor — top of the remaining list / page heading; optional informational success toast).

### Accessibility orchestration

`alertdialog` (not `dialog`) instructs SRs to treat it as a critical, time-sensitive alert. Focus contract: never default to destructive; focus Cancel (failsafe against rapid keyboard execution), or the container/first non-destructive element; trap focus (Tab cycles within); on dismissal return focus to the trigger, or a predetermined successor if it was destroyed. Use `aria-labelledby` (title) + `aria-describedby` (body consequence paragraph) so the SR announces the whole warning cohesively. **Undo-toast timing:** pause the Toast's expiration timer the moment it receives keyboard focus or hover, so SR/switch users retain control of the reversion window.

### Content & copy

Title = a specific question, never "Are you sure?"/"Warning" — `{Verb} + {Noun}?` ("Delete 3 files?", "Remove integration?"). Body declares facts (consequence, scope, irreversibility, cascade), doesn't ask permission: "This action cannot be undone. This will permanently delete the repository and remove access for 12 active collaborators." Buttons use action verbs; "Yes/No"/"OK/Cancel" prohibited in isolation — `[ Cancel ]` adjacent to `[ Delete repository ]`. Type-to-confirm prompt states exactly what to type. Undo toast brief: "File deleted. [Undo]."

### Layout & structure (light)

Dialogs narrow for readability (max ~400–480px), not full-screen on desktop. Button row bottom-right (LTR forward-momentum), destructive far-right, secondary to its left. Undo toast bottom-left or bottom-center, non-obstructive, not overlapping nav or the spatial area of the deleted item.

### Variants & responsive

Undo Toast (low, optimistic) / Simple Dialog (medium, pessimistic) / Type-to-Confirm (high, string-match-bound primary) / Inline Confirm (contextual — a dense data-table row converts to a confirmation state inline rather than breaking context with a modal). Mobile: center dialog often morphs to a Bottom Sheet (thumb reach); buttons stack vertically full-width; Cancel at the very bottom (closest to thumb) as the most accessible escape.

### Anti-patterns

Autofocusing the destructive button (rapid Enter executes before the warning is parsed). Confirmation fatigue (confirming reversible/low-stakes — crying wolf). Vague copy ("Are you sure?" + OK/Cancel). Refusing an optimistic Undo because the backend prefers synchronous calls (UX must dictate architecture, not vice versa). Undo toasts with timeouts too brief (2s) to reach. Color-only danger (fails WCAG contrast/color-blindness).

### Related patterns & components

vs Dialog/Modal (component): the visual shell + `<dialog>`, alertdialog role, z-index, focus mechanics are the component's; this brief defines when/how to deploy it destructively. vs Toast (component): the ephemeral surface vs the background-queue + optimistic state machine. vs Save & Unsaved Changes (pattern): a sibling guarding navigational data loss, not a direct delete command. vs Forms-as-a-system: validation/error is not destructive confirmation. vs Inline Message/Banner: persistent in-page warning for field-contextual destructive actions instead of a modal.

### Field POV evolution

"Confirm everything" (late-1990s–2005, synchronous `window.confirm()`, trained mass fatigue) → the Raskin Pivot (2007, "never use a warning when you mean undo") → Optimistic UIs (2010s, AJAX + Gmail's action+grace-period made Undo the gold standard for routine deletions) → the friction reckoning (2018–present, enterprise SaaS blast radius grew catastrophic; GitHub Primer's Danger Zone / type-to-confirm established extreme-consequence-requires-un-automatable-friction) → WCAG 2.2 (2023) formalized error prevention as legal necessity (§3.3.4/§3.3.6).

### Reference instantiations

WAI-ARIA APG (the canonical alertdialog: keyboard trapping, escape, aria-describedby). GitHub Primer (Danger Zone + type-to-confirm). IBM Carbon (Danger Modal: focus handling, prohibition on autofocusing destructive, button alignment). Shopify Polaris (consequence-driven, verb-first microcopy). GOV.UK (irreversible legal/tax transactions where Undo is impossible).

### Agent-consumable schema (external pass)

```yaml
identity:
  id: pattern-destructive-confirmation
  name: Destructive confirmation
  aliases: [delete confirmation, destructive flow, confirm or undo, danger zone]
  tier: flow
  goal: help-user-act
  status: active
problem: >
  Overuse of confirmation dialogs leads to confirmation fatigue, rendering warnings invisible
  to users operating on motor memory. The pattern resolves when to use optimistic execution
  with undo (recoverable actions) versus high-friction pessimistic confirmation (irreversible).
composition:
  requires: [component-dialog-alertdialog, component-button-danger, component-toast-undo, component-banner-inline]
decision_rules:
  - { if: "action_is_reversible AND data_is_soft_deleted", use: "Undo Flow (Toast)" }
  - { if: "action_is_irreversible OR action_is_legal_financial OR data_is_hard_deleted", use: "Confirm Flow (Dialog)" }
  - { if: "severity_is_catastrophic", use: "Type-to-Confirm Dialog" }
  - { if: "dialog_opens", use: "Set focus to Cancel/Safe option" }
  - { if: "evaluating_button_order", use: "Cancel left, Confirm/Danger right" }
flow:
  undo_path: [intent, optimistic_execution (UI instant + TTL queue), feedback (Toast + Undo), resolution (expire=commit OR undo=abort+revert)]
  confirm_path: [intent, interruption (alertdialog + focus trap), evaluation (focus safe, read consequences), resolution (cancel=dismiss OR confirm=execute), processing (loading + disabled), feedback (dismiss + focus to anchor)]
accessibility_orchestration:
  - 'container: role="alertdialog"'
  - "focus_entry: Cancel/Safe button to prevent accidental Enter deletion"
  - "focus_trap: Tab wraps within dialog bounds"
  - "semantics: aria-describedby links to consequence paragraph"
  - 'undo_toast: aria-live="polite", timer pauses on focus/hover'
content:
  title: "Specific Verb+Noun question (Delete 3 files?)"
  body: "Explicit facts re irreversibility + cascade; no permissive language"
  button: "Action verb matching the title; no generic OK/Yes"
layout:
  - "Constrain dialog width (~400-480px) for reading line length"
  - "Buttons bottom-right (web) or stacked vertically (mobile, Cancel bottom)"
variants: [undo-toast (low), simple-dialog (medium), type-to-confirm (high), inline-confirm (contextual)]
anti_patterns:
  - "Autofocusing the destructive button"
  - "Confirmation fatigue (confirming trivial/reversible)"
  - "Vague copy (Are you sure? OK)"
  - "Unreachable undo toasts (too-short timeouts)"
  - "Color-only danger indicators"
reference_instantiations: [ARIA APG alertdialog, GitHub Primer Danger Zone, IBM Carbon Danger Modal, Shopify Polaris Modal (Destructive)]
relations:
  composes: [Dialog, Button, Toast]
  boundary: [Save & unsaved changes, Forms-as-a-system, Inline Message]
notes: >
  Contested: Button order (Windows vs macOS). Web consensus aligns with macOS (Cancel left,
  Action right) for forward momentum, enforced by Carbon and Material.
```
