You are researching the ToggleButton component for a senior design
systems practitioner at a digital agency. Field-truth study; the practice
is establishing an opinionated default.

This is a claude-only run for a largely convergent component that stands
on two already-briefed components: it inherits the BUTTON substrate
(components/button.md — native <button>, intent/appearance/size, the
press model, icon-only requiring an accessible name) and the
aria-pressed-vs-role-switch-vs-role-checkbox distinction already resolved
in the BUTTON (§6) and SWITCH (§6) briefs. Do not re-derive those.

Concentrate on what is ToggleButton-specific:
- it is a Button that carries a PERSISTENT binary pressed state
  (role=button + aria-pressed=true/false) — an action/mode that stays on,
  not a one-shot action (Button), not a system setting (Switch,
  role=switch), not a staged form value (Checkbox, role=checkbox)
- the setting-vs-action/mode boundary with Switch, and the visual
  divergence (a toggle button looks like a pressed button; a switch is a
  track+thumb); when each is correct
- the transient :active "pressed" vs the persistent aria-pressed
  "selected" state — the naming/visual trap
- the accessible-name-stays-constant + aria-pressed pattern vs the
  label-flips ("Mute"->"Unmute") pattern, and which the practice picks
- standalone toggle (Bold in a toolbar) vs in a group (ToggleButtonGroup
  / Segmented Control) — the atomic/group decomposition that connects to
  the selection-control decomposition and to the forthcoming Segmented
  Control brief
- keyboard (Space AND Enter, since it's a button — unlike switch's Space)
- typical uses: toolbar formatting (Bold/Italic), mute/pin/favourite,
  filter toggles, view toggles

Survey: Adobe Spectrum (ToggleButton), Material 3 (icon/toggle buttons),
Microsoft Fluent (ToggleButton), MUI (ToggleButton/ToggleButtonGroup),
GitHub Primer, Atlassian, Base Web, Apple HIG. Cite with version dates.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for button and the shared substrate;
flag unverified under notes.unverified). Expert audience; explain the
persistent-state contract, the aria-pressed-vs-switch boundary, the
constant-name+aria-pressed pattern, and the standalone-vs-group
decomposition.
