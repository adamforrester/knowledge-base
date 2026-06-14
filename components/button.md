---
okf_version: "0.1"
type: component-brief
title: Button
description: The most-shipped, least-agreed-upon component. A field-truth study of where the leading systems converge (native button, link-vs-button, three-tier size, delayed-spinner loading) and where they fracture (the variant-axis model, native disabled vs. focusable inactive), with the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [btn, cta]
last-audited: 2026-06-14
timestamp: 2026-06-14
---

# Button

> Every system has a Button; almost none agree on its API. The disagreements are not cosmetic — they encode rival theories of how a design system should expose intent versus appearance, where to draw the boundary of encapsulation, and how much of the platform's behaviour to re-implement versus inherit. This is the calibration brief for the catalogue: if the 15-section spine survives Button-the-meta-component, it survives anything.

---

## 1. Framing

Button is the fundamental unit of transactional intent, and consistently the most architecturally fractured component in any enterprise system (external). The friction has one root: the persistent conflation of how a button *looks* with what it *does* in the document. A Button is asked to be a synchronous form-submission trigger, an asynchronous action initiator with a pending state, a state-toggling primitive, and — too often — a navigator. That overburdening is what produces the polymorphic APIs where one component renders as `<button>`, `<a>`, or a router link depending on props (external).

What a Button *is*, for this brief, is the in-flow trigger for an action that happens *now*, in the current context: submit, save, confirm, delete, open a dialog, fire async work. What it *isn't*: navigation (that is a Link, even when it looks like a button), a binary toggle (Switch/Checkbox), or a persistent one-of-many selection (segmented control, ToggleButton). The single most consequential boundary in the whole component is **button-versus-link semantics** — `<button>` triggers an action and is operated with Space *and* Enter; `<a href>` navigates, is operated with Enter only, and exposes a URL to the context menu, middle-click, and the accessibility tree. Both agents converge completely on the rule and diverge entirely on how to *enforce* it through the API.

The deeper reason systems disagree is that **the hierarchy axis is overloaded**. "Primary" silently bundles *visual emphasis* (how loud) with *page rank* (the one action that matters most here) with, sometimes, *tone* (is this destructive?). Every divergence in §3 is a different attempt to unbundle those. Governance-heavy systems — Carbon, Material 3 — couple visual variant tightly to semantic rank and treat the Button as a locked black box (external). Utility-first systems — Base Web, Atlassian's underlying primitives — expose the internals and let consumers override subcomponents (external). Neither extreme is the practice's position: we want the accessible, correct behaviour baked in and the *visual* surface themeable, which is the headless-substrate-plus-opinionated-skin posture §11 lands on.

## 2. Anatomy and parts

A production Button is not a styled `<button>` tag with text inside — it is a small multi-node structure, and the field has converged on roughly the same parts (external):

- **Container / target** — the interactive element (`<button>`, or `<a>` when navigating). Owns the hit area, radius, background, border. This is the accessibility target.
- **Touch-target expansion** — the *optical* size and the *hit* size are deliberately decoupled. A visually compact button (say 28px tall) extends its clickable area outward — typically via a `::before` pseudo-element or absolute-positioned overlay — to satisfy ergonomic minimums without inflating the visual design (external). This reconciles the WCAG 2.5.8 floor (24×24 CSS px) with Apple's far larger 44×44pt target (Apple HIG, 2024) without forcing chunky "small" buttons.
- **Focus ring as its own concern** — the modern standard separates the focus indicator from the element border and gives it an `outline-offset` (≈2px) so an unbroken sliver of background sits between border and ring (external). This is what keeps a primary-coloured button's ring from blending into its own fill and failing WCAG 1.4.11 — a real failure Atlassian documents (external).
- **Layout container** — an `inline-flex` row that centres content and owns the gap between the leading slot, label, and trailing slot.
- **Leading / trailing visual slots** — and here the naming has *evolved*: the field is moving from `leadingIcon`/`trailingIcon` to **`leadingVisual`/`trailingVisual`**, because the slot routinely holds avatars, status dots, unread counters, and spinners, not just icons (external; Primer). We adopt the `*Visual` vocabulary.
- **Label** — wrapped in its own atomic span so truncation, wrap, and line-height are controllable independently of the flex row.
- **Pending slot** — where the spinner enters, either replacing the leading visual or overlaying the label (see §4 on width preservation).

The Claude pass framed the press feedback as Material's named "state layer" (a tint overlay whose opacity encodes hover/pressed); most web systems express the same thing as background/shadow token shifts rather than a named node (Claude). Treat the state layer as a Material-ism, not a required part.

## 3. Properties / API

**The converged core** (both agents, near-universal across the field):

- an action handler (`onClick` / `onPress`);
- a label, as children (web) or a `label` string (some RN/mobile APIs);
- `disabled` (contested in *behaviour*, not in *existence* — see §4);
- a three-tier `size` — `small | medium | large`, medium default;
- a stretch-to-container flag (`fullWidth` / `block` / `isFullWidth` — universally present, universally named differently);
- `type` passing through to the HTML attribute. **The recurring trap: the platform default is `type="submit"`, so a Button inside a `<form>` with no explicit `type` submits the form.** We default the component to `type="button"` and require `submit` to be explicit (both agents; Primer does this).

**The variant-axis model — the load-bearing divergence.** The field splits between a single overloaded `variant`/`kind`/`appearance` enum and a multi-axis model. Both agents independently reject the single overloaded enum: it documents easily but explodes into bloat the moment design asks for a "danger-outlined" or "primary-ghost" button (external), and it forces page-rank and tone to ride the same prop (Claude). The practice's default is the **two-axis intent + appearance** model:

- **`intent`** — `primary | secondary | danger | ghost` — the semantic role and colour mapping.
- **`appearance`** — `solid | outline | plain` — the visual fill, decoupled so the matrix scales by addition, not multiplication.

This is the model shipping systems are closest to (Spectrum separates semantic `variant` from fill; Polaris separates `variant` hierarchy from `tone` — external). Two honest costs of choosing it. First, `intent` still bundles hierarchy (`primary`/`secondary`) with tone (`danger`), so it cannot cleanly express a *low-emphasis destructive* action — a quiet "Delete" in a table row — the way a fully orthogonal emphasis+tone split could (Claude). We accept that: the destructive action in a confirmation flow is rarely the quiet one, and the rare quiet-destructive case is served by `intent="danger" appearance="plain"`. Second, `ghost` (an intent) and `plain` (an appearance) overlap at the low-emphasis end. We treat `ghost` as the conventional alias for `intent="secondary" appearance="plain"` and flag the redundancy as a seam to resolve when the §15 schema is formalised (the spec mandates free-form YAML until the shape settles across ~5 briefs).

**Loading state naming.** `loading` (Polaris, Primer) versus `isPending` (Spectrum). We default to **`isPending`** (external): "loading" implies a server fetch, while "pending" accurately describes a UI halted on any promise — and it aligns with React's `useTransition`/`useFormStatus`/Server-Actions vocabulary the implementation will sit on (§11). Whichever name, the *behaviour* is the contract (§4), not the spelling.

**Polymorphism.** Three approaches exist: a single Button with `as`/`href` that swaps the element; Radix-style `asChild` prop-merging; or a separate `LinkButton`. Both agents land in the same place: **prefer a separate `LinkButton`**, and where polymorphism is unavoidable, infer the element from `href` (presence of `href` → render `<a>`) rather than carrying a fully generic `as` prop. The reason is concrete: generic polymorphic `forwardRef` typing bloats TypeScript compile times and degrades IDE responsiveness in large codebases (external), and an `as`-driven Button makes it trivially easy to ship an `<a>` with no `href` (a "button" that does nothing) or a `<button href>` (silently ignored) (Claude).

**Icon as prop vs. child.** Prefer the constrained **prop/slot** (`leadingVisual={<Icon/>}`) over arbitrary children for adornments — it is lintable and keeps the Button from taking a hard dependency on the icon library (external). Reserve children for the label.

## 4. States and variants

**Runtime states** (system-set, not author-chosen):

| State | Trigger | Contract |
| --- | --- | --- |
| rest | default | base tokens |
| hover | pointer over | state-layer/background shift; never the sole carrier of meaning; absent on touch |
| focus-visible | keyboard focus | offset ring, `:focus-visible` not `:focus`, ≥3:1 (WCAG 1.4.11, 2.4.13) |
| pressed | pointer-down / Space-Enter | brief shade or `scale(0.98)` — guarded by reduce-motion (§8) |
| pending (loading) | async in flight | delay spinner, preserve width, keep focusable, suppress re-fire, announce busy |
| disabled / inactive | author or app state | **the contested decision — below** |

There is no **error**, **empty**, or **read-only** state on Button. Those belong to the field or form the button acts on, not to the button (both agents). The generic spine lists them; for Button they are correctly N/A.

**The disabled decision — the live edge of the whole component.** Native HTML `disabled` removes the element from the tab order and the accessibility tree: for a keyboard or screen-reader user the button ceases to exist. A user who completes a long form but misses one field cannot tab to the greyed submit to discover *why* it is blocked — an inaccessible dead end (external). Both agents converge on moving off native `disabled` for any button that is *relevant but currently unsatisfied*, toward a focusable pattern: `aria-disabled="true"` plus a suppressed handler, so the control stays reachable, can carry an explanatory tooltip or `aria-describedby`, and never silently swallows focus. Primer formalises this as a distinct **`inactive`** state — visually muted but semantically present, surfacing the blockage reason on focus/click (external). Spectrum's `pending` uses the same `aria-disabled`-not-`disabled` mechanism so focus is retained while async work runs (Claude). The practice's default: reserve native `disabled` for controls that are *fundamentally irrelevant to the current view*; use the focusable inactive pattern for everything blocked by satisfiable app state. (See 28-web-accessibility-implementation for the implementation; this is the component-specific application of it.) Note the standing tension — focusable `aria-disabled` is the accessibility-forward position but is *not* yet most systems' default mapping, so it is a per-engagement decision to make explicitly, not a silent default.

**The pending width trap.** Replacing "Submit request" with a centred spinner collapses the button's width and reflows the layout around it — a recurring, avoidable bug (external). Two fixes: replace the *leading visual* with the spinner and leave the label in place (Primer's approach, preserves width for free); or, for label-only buttons, measure and lock the width before swapping to the spinner. During pending, set `aria-disabled`, suppress the handler to prevent double-submit, and keep focus on the button (both agents).

**Intentional variants** (author-chosen): `intent` × `appearance` (§3) × `size {small, medium, large}` × width `{auto, full}`, with leading-visual / trailing-visual / icon-only / pending as orthogonal modifiers. The "one high-emphasis button per view" rule is near-universal (Material 3, Polaris, Carbon, Atlassian — both agents). Success- and warning-toned buttons are deliberately rare across the field; colour is a weak carrier for "this is the safe choice," so we do not ship a success intent by default and reach for it only with a non-colour reinforcement.

## 5. Usage guidance

**Use** for an immediate action in the current context: submit/save/reset a form, trigger a UI state change (open modal, toggle drawer, expand accordion), or fire async work (both agents).

**Do not use for navigation.** If the element takes the user to a new URL, it is a Link regardless of how it looks; when it must *look* like a button, use a `LinkButton` that emits a real `<a href>` (external). This is not pedantry — it is what preserves "open in new tab," middle-click, and the right-click menu, none of which a `<button>` can offer. Don't use a Button for a persistent binary (Switch / Checkbox) or one-of-many selection (segmented control / ToggleButton).

**Decision frameworks rather than rules:**

- **Emphasis is local.** Assign `intent="primary"` by the action's importance *to this view*, not globally; exactly one per view/region (both agents).
- **Destructive pairing.** Never place a `danger` button without an adjacent neutral escape hatch ("Cancel" / "Keep") (external). On a delete confirmation the primary is usually the safe choice and the destructive action is the secondary-danger — a content/safety call, not a hard rule (Claude).
- **Placement.** Primary at the terminus of the reading flow (bottom-trailing for LTR; full-width on mobile) (external).

## 6. Accessibility

The reader has 14-accessibility, 17-accessibility-annotation-contract, and 28-web-accessibility-implementation for the theory; this is only what is Button-specific.

- **Use the native `<button>`.** It carries `role="button"`, focusability, and Space/Enter activation for free. `<div role="button">` is the canonical anti-pattern: it needs manual `tabindex="0"`, `keydown` handlers for *both* Enter and Space, `keyup` for Space to match native, and `preventDefault` on Space to stop the page scrolling — and still misses Windows High Contrast affordances (both agents). Inherit the browser's behaviour; do not re-implement it.
- **Keyboard model is the reason link≠button.** `<button>`: Enter on keydown, Space on keyup. `<a>` styled as a button: Enter only — Space scrolls. This asymmetry is exactly why a navigating "button" must be a real link and an acting "link" must be a real button (both agents).
- **Accessible name.** Text content is the name. Icon-only buttons have no visible text and so *must* carry an `aria-label` (or visually-hidden text) — the single highest-frequency Button a11y failure in the wild, announced as "button, unlabelled" otherwise (external). Enforce it at the type level via a distinct `IconButton`, and fail loudly (dev warning) when an icon-only Button has no name. If a visible label and `aria-label` disagree, voice-control users who speak the visible word cannot activate the control — keep the name a superset of the visible text (WCAG 2.5.3 Label in Name) (Claude).
- **Busy announcement.** A spinner is invisible to assistive tech. Announce pending via `aria-busy` and/or a polite live region ("Saving…"); Primer's `loadingAnnouncement` is the formalised version (both agents). Keep the button focusable through the pending state (§4) so the busy state is discoverable.
- **State attributes are distinct, not interchangeable.** `aria-pressed` for toggle buttons, `aria-expanded` (+`aria-haspopup`) for disclosure/menu triggers, `aria-checked` only for the switch role. Conflating them is a common AT bug (Claude).
- **WCAG SCs the button participates in:** 1.4.11 Non-text Contrast (the focus ring and boundary, 3:1), 2.4.7 Focus Visible, 2.4.13 Focus Appearance (2.2), 2.5.3 Label in Name, 2.5.5 / 2.5.8 Target Size, 4.1.2 Name/Role/Value, and 1.4.13 only if a tooltip is attached. Disabled controls are *exempt* from contrast minimums — which is precisely why a silently-disabled button can be illegible *and* unreachable, and why §4's focusable-inactive pattern matters. (The external pass listed 2.4.11 Focus Not Obscured in its schema; that is a real 2.2 SC but not the button's primary focus concern — the load-bearing pair is 2.4.7 and 2.4.13.)

## 7. Content guidelines

**Verb-first and specific** — "Save changes," "Delete file" — not "OK," "Submit," or "Yes" (both agents). "Submit" leaks database vocabulary; "Click here" fails link-purpose. **Match the destructive verb to the consequence**: the confirm button in a delete dialog says "Delete," echoing the action, not "Confirm" — it reduces mode errors. **Sentence case, no terminal punctuation**, ideally ≤3 words to bound the i18n expansion budget (§9); Material 3 abandoned the M2 all-caps label and the field is now uniformly sentence/Title case (both agents; Fluent 2, 2024). **Name the object on menu/split actions** — "New event," not "New" (external).

The **"Cancel" vs. "Close" vs. "OK"** contract (Fluent 2, 2024, via external): "Cancel" aborts an in-progress task and reverts; "Close" dismisses an informational or completed view; never make a user click "OK" to dismiss an *error* — "OK" implies agreement with the failure. Use "Close" or "Dismiss." Error, empty, and CTA copy patterns beyond this belong to the host field/form, not the button (§4). (See 04-documentation for the system-level content-guidelines layer.)

## 8. Motion and transition

State transitions (background, border, shadow) should run fast — ~100–150ms, eased-out — through motion *tokens*, not hard-coded values; slow button transitions make the whole app feel sluggish (external). A definite **press state** matters: without it a button feels broken, so a subtle `scale(0.98)` or shadow drop on `:active` gives tactile confirmation (Apple HIG, 2024, via external). **Delay the pending spinner** by a few hundred ms so fast responses don't flicker one, and preserve width across the transition (§4) (Claude). Material 3 Expressive's shape-morphing on press (pill→squarer corners) is visually engaging but introduces reflow and CSS cost; we eschew dimensional morphing for stable geometry (both agents — flagged Material-specific). **Reduce-motion contract:** under `prefers-reduced-motion: reduce`, resolve scale/translate to `transform: none` and drop ripple/morph, keeping the *instantaneous* colour change so the state stays perceivable; the spinner is functional, not decoration, and the `aria-busy`/live-region path carries the busy state regardless. (See 18-motion-foundations and 19-motion-implementation-web; mobile in 20-motion-implementation-mobile, handoff in 21-motion-spec-and-handoff.)

## 9. Internationalization

**Text expansion is where i18n bites Button hardest** — labels are short, and a concise English verb can expand substantially in German, Finnish, or Russian (external cites up to ~300% at the extreme short-string end; we hold the exact figure loosely). Never fix the button to its English width; use `min-width` plus generous padding and allow wrap. When space is genuinely constrained, **wrap to a second line rather than truncate** — an ellipsis hides the action and forces a guess (external). **RTL:** mirror the whole button via logical properties (`padding-inline`, `margin-inline`, flex `gap`) so leading/trailing slots flip automatically; flip *directional* icons (back/forward chevrons) but never non-directional ones (search, settings) — and never media-transport icons (play, fast-forward), whose left-to-right meaning is global (both agents; Material 3, 2024). Expose this per-icon (`autoMirror`) rather than a blanket `scaleX(-1)` on every visual slot (external). The label is a passed-in string the consumer localises; don't bake conjugation or interpolation into the component. (See 13-internationalization-and-rtl.)

## 10. Naming

The component is universally **Button**. Icon-only splits between a distinct `IconButton` (Primer, Material) and `ActionButton` (Spectrum); we ship a distinct **`IconButton`** so the accessible name is required at the type level (§6). Navigation-styled-as-button is **`LinkButton`** (§3, §5).

The practice's prop nomenclature: **`intent`** `{primary, secondary, danger, ghost}` + **`appearance`** `{solid, outline, plain}` + **`size`** `{small, medium, large}` + **`isPending`** + **`isInactive`** (focusable disabled) + **`isDisabled`** (native, reserved). Aliases consumers will reach for, with their canonical mapping for codemod/search: `primary`/`secondary` → `intent`; `danger`/`destructive` → `intent="danger"`; `ghost`/`text`/`link`/`tertiary` → low-emphasis (`appearance="plain"`); `block` → `fullWidth`; `loading` → `isPending`; `variant`/`kind` → the old single-axis enum, decomposed into `intent`+`appearance`. Teams also wrap hot combinations (`<DangerOutlineButton>` = `intent="danger" appearance="outline"`) for ergonomics; the primitive underneath is unchanged.

## 11. Implementation notes

- **`type` default** — default the component to `type="button"`; require `submit` explicitly (§3). The platform's `submit` default is the most common real Button bug (both agents).
- **Headless substrate, opinionated skin.** The field is moving the *behaviour* into headless primitives — Atlassian's `Pressable`, and React Aria's `useButton`/`usePress` — which normalise press across mouse/touch/keyboard/pointer, fix mobile ghost-clicks and drag-cancel, and unify the `<button>`/`<a>`/`<div>` differences (both agents). We build on a headless press primitive and own the visual tokens, rather than either re-implementing press by hand or adopting a fully-styled black box.
- **Reject arbitrary overrides.** Base Web's `overrides` prop (target/replace internal nodes) is powerful for white-label work but breaks encapsulation (external). Prefer strict token mapping plus headless composition over an open override surface on the core Button.
- **Forms and Server Actions.** Buttons increasingly invoke React 19 / Next App Router / Remix Server Actions from inside a `<form action>`. Integrate with `useFormStatus` so `isPending` toggles automatically while the action is in flight, and stay agnostic enough to accept submission from wrapper contexts like Hydrogen's `CartForm` without fighting native form behaviour (external).
- **Prop-vs-slot** — adornments via the `leadingVisual`/`trailingVisual` slot, label via children (§3); don't pass complex JSX into string props, and don't make Button import the icon library (external).
- **Forward `ref` and spread rest props** to the underlying element — consumers depend on it for tooltip/popover anchoring (Claude).

*A note on one cross-cutting claim:* the external pass reports that Polaris has migrated from a monolithic React library to framework-agnostic Web Components (Shadow DOM, `:host` CSS custom properties for theming), dated to late 2025. The direction is plausible and matches Shopify's stated trajectory, but we have no `_source-text/` backing for the specific version/date, so we record it as a claim to verify before it hardens into the practice's POV rather than asserting it. If true, it reinforces the headless-substrate posture: behaviour and theming surface survive framework churn.

## 12. Related and alternative components

- **Composes with:** Icon (leading/trailing visual), Spinner (pending), Tooltip (icon-only name / inactive-reason — with the don't-tooltip-a-natively-disabled-button caveat), ButtonGroup (grouping, radius collapsing, hierarchy validation), Menu/Popover (as a MenuButton trigger via `aria-haspopup`/`aria-expanded`).
- **Alternative to:** Link (navigation vs. action — the core boundary), IconButton (icon-only specialisation), LinkButton (navigation that looks like a button), ToggleButton (`aria-pressed` persistent state), SplitButton (default action + adjacent menu of related actions — the primary action is never duplicated inside the menu; Fluent 2, 2024), Switch (binary setting), Chip/Tag (removable/selectable token).
- **Supersedes:** `<input type="button|submit">`, `<div role="button">`, and Material 2's all-caps button styling.
- **Superseded by:** nothing — Button is foundational. (Within the Material lineage, M2's button taxonomy was superseded by M3's typed model.)

(See 03-component-library for the system-level component model this brief sits under, and 29-per-component-documentation-template for the delivered docs page this brief feeds.)

## 13. Field POV evolution

Three macro shifts in the last ~two years, both agents converging on the direction:

1. **Off native `disabled`, toward focusable inactive.** Accessibility-forward systems (Primer's `inactive`, Spectrum's `pending` via `aria-disabled`) keep blocked-but-relevant controls reachable and explained. Still not the field-wide default — the live edge (§4).
2. **Behaviour into headless primitives.** `Pressable` (Atlassian) and React Aria's `usePress` are increasingly the substrate beneath even bespoke visual layers (§11).
3. **Framework-agnostic delivery.** A retreat from React-coupled, CSS-in-JS systems toward Web Components + CSS variables, to outlast JS-framework churn — the (unverified, §11) Polaris Web Components move is the headline example.

Smaller, settled shifts: sentence case over all-caps (Material 3 from 2021); the component owning its own loading/pending state, anti-flicker delay, and busy announcement (Spectrum `pending`, Primer `loading`/`loadingAnnouncement`); and the slot vocabulary moving from `*Icon` to `*Visual` (Primer). The genuine remaining split is the variant-axis model itself — Material 3 went *toward* discrete named button types while Spectrum/Polaris went *toward* separated axes; we side with the separated-axis camp (§3).

## 14. Sources cited

Field-leader systems, conservative version dates (the external pass supplied more precise version numbers — Polaris 13.9.5, Spectrum 3.0.0, Carbon 1.109.0, Primer React 36.0 — which we have not independently verified and so hold loosely; `last-audited` in frontmatter is the re-run trigger):

- Shopify Polaris — Button; `tone`/`variant` split; the (unverified) Web Components migration (Polaris, 2025).
- Adobe Spectrum — Button; `isPending` with delay + focus retention; React Aria `useButton`/`usePress` (Spectrum, 2024).
- Google Material 3 — Buttons; typed button set; sentence-case from M3 (2021); Material 3 Expressive shape-morph (Material 3 / Material 3 Expressive, 2024–2025).
- IBM Carbon — Button, `kind` model (Carbon, 2024).
- GitHub Primer — Button, IconButton, LinkButton; `type="button"` default; `inactive`; `loading`/`loadingAnnouncement`; `leadingVisual`/`trailingVisual` (Primer, 2024).
- Atlassian Design System — Button; `appearance`; `Pressable` primitive; the focus-ring-on-primary 1.4.11 failure (Atlassian Design System, 2024).
- Shopify Hydrogen — `CartForm` async-submission wrapper context (Shopify Hydrogen, 2024).
- Base Web (Uber) — `overrides` internal-node model (Base Web, 2024).
- Apple Human Interface Guidelines — 44×44pt target; press-state emphasis (Apple HIG, 2024).
- Microsoft Fluent 2 — sentence case; Cancel/Close/OK contract; SplitButton (Fluent 2, 2024).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.4.11, 2.4.7, 2.4.13, 2.5.3, 2.5.5, 2.5.8, 4.1.2, 1.4.13.

## 15. Agent-consumable schema

```yaml
identity:
  id: button
  name: Button
  aliases: [btn, cta]
  category: form
  status: stable
description: >
  In-flow trigger for an immediate action in the current context.
  Not navigation (use link/link-button), not persistent state
  (use switch/toggle-button).
api:
  props:
    - name: children
      type: ReactNode (label)
      required: true        # except icon-only / icon-button
      description: Visible label; verb-first, sentence case, <=3 words.
    - name: onClick
      type: function
      required: false
      description: Action handler. Suppressed while isPending / isInactive.
    - name: intent
      type: enum
      values: [primary, secondary, danger, ghost]
      default: secondary
      required: false
      description: Semantic role + colour. One primary per view. ghost is
        the conventional alias for secondary + appearance:plain (overlap
        to resolve at schema formalisation).
    - name: appearance
      type: enum
      values: [solid, outline, plain]
      default: solid
      required: false
      description: Visual fill, decoupled from intent to prevent matrix
        explosion.
    - name: size
      type: enum
      values: [small, medium, large]
      default: medium
      required: false
    - name: fullWidth
      type: boolean
      default: false
      required: false
      description: Stretch to container; aliases block / isFullWidth.
    - name: type
      type: enum
      values: [button, submit, reset]
      default: button       # opinionated: neutralise platform submit default
      required: false
    - name: isPending
      type: boolean
      default: false
      required: false
      description: Delays spinner, preserves width, keeps focus
        (aria-disabled not native disabled), suppresses re-fire, announces
        busy. Preferred name over `loading`.
    - name: isInactive
      type: boolean
      default: false
      required: false
      description: Focusable disabled — visually muted, retains tab order,
        surfaces blockage reason. Use for relevant-but-unsatisfied controls.
    - name: isDisabled
      type: boolean
      default: false
      required: false
      description: Native disabled. Reserve for controls irrelevant to the
        current view; removes from tab order + a11y tree.
    - name: leadingVisual
      type: slot
      required: false
      description: Icon / avatar / counter / spinner before the label.
    - name: trailingVisual
      type: slot
      required: false
      description: Icon / caret / indicator after the label.
    - name: href
      type: string
      required: false
      description: Discouraged on Button — prefer link-button. If present
        MUST render <a>; <a> path drops type/disabled.
    - name: aria-label
      type: string
      required: false
      description: Required when no visible label (icon-only); must be a
        superset of any visible text (SC 2.5.3).
composition:
  composes-with: [icon, spinner, tooltip, button-group, menu, popover]
  alternative-to: [link, link-button, icon-button, toggle-button, split-button, switch, chip]
  supersedes: ["input[type=button|submit]", "div[role=button]"]
  superseded-by: null
accessibility:
  wcag-criteria: ["1.4.11", "2.4.7", "2.4.13", "2.5.3", "2.5.5", "2.5.8", "4.1.2", "1.4.13"]
  role: button            # native <button>; never div[role=button]
  aria-attributes:
    - aria-label          # icon-only; superset of visible text
    - aria-disabled       # focusable inactive + pending (preferred over native disabled)
    - aria-busy           # during isPending
    - aria-pressed        # toggle buttons only
    - aria-haspopup       # menu-trigger buttons only
    - aria-expanded       # disclosure / menu triggers only
  keyboard-model:
    button: { enter: keydown-activate, space: keyup-activate }
    link-as-button: { enter: activate, space: scrolls }   # why button != link
  focus-behavior:
    focus-visible: required        # :focus-visible, offset ring, >=3:1, SC 2.4.13
    ring: offset-from-border       # avoid blend with own fill (SC 1.4.11)
    disabled-focus: retained-when-aria-disabled
    pending-focus: retained
states:
  runtime: [rest, hover, focus-visible, pressed, pending, inactive, disabled]
  not-applicable: [error, empty, read-only]   # belong to field/form, not button
variants:
  intent: [primary, secondary, danger, ghost]
  appearance: [solid, outline, plain]
  size: [small, medium, large]
  width: [auto, full]
  modifiers: [leading-visual, trailing-visual, icon-only, pending]
content:
  label-pattern: "verb-first, action-specific, sentence case, <=3 words; no 'OK'/'Submit'/'click here'"
  error-pattern: null     # button has no error state; error belongs to the form/field
  empty-pattern: null     # button has no empty state
  dialog-copy: "Cancel = abort+revert; Close/Dismiss = dismiss info/error; never OK on an error"
i18n:
  text-expansion: "no fixed width to English label; min-width + padding; wrap, never truncate"
  rtl: "mirror via logical props; flip directional icons only; never media-transport icons"
notes:
  contested:
    - native-disabled vs focusable-inactive (live edge; per-engagement decision)
    - intent bundles hierarchy+tone, cannot cleanly express low-emphasis-destructive
    - ghost (intent) vs plain (appearance) overlap — resolve at formalisation
    - polymorphism: infer-from-href + separate link-button over generic `as`
  unverified:
    - polaris-web-components-migration (needs _source-text backing)
    - external-supplied precise version numbers
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-14-component-button/` (14 June 2026). Both agents converged on the spine — native `<button>` over `div[role=button]`, link-vs-button as the core boundary, three-tier size, `type="button"` default, the delayed-spinner / width-preserving / focus-retaining / busy-announcing pending contract, the move off native `disabled` toward a focusable inactive state, verb-first sentence-case labels, mirror-directional-icons-only RTL with no-fixed-width expansion, the reduce-motion transform:none contract, and headless press primitives as the behavioural substrate. The two-axis `intent` + `appearance` model (over a single overloaded `variant` enum and over the fully-orthogonal emphasis+tone alternative) is the practice's chosen default among options both agents surfaced — the trade-off (no clean low-emphasis-destructive; ghost/plain overlap) is recorded in §3. The `leadingVisual`/`trailingVisual` vocabulary, `isPending` over `loading`, Primer's named `inactive` state, the SplitButton/`Pressable`/`overrides` field detail, the Fluent Cancel/Close/OK contract, and the touch-target-expansion and focus-ring-separation anatomy are external-agent contributions; the `aria-pressed`/`aria-expanded`/`aria-checked` distinction, SC 2.5.3 Label in Name, the destructive-as-secondary nuance, and the state-layer-as-Material-ism framing are Claude-pass contributions. Version numbers are held conservatively per §14; the Polaris Web Components migration and the external-supplied precise version numbers are flagged unverified and need `_source-text/` backing before they harden. This is the catalogue's calibration brief; the §15 schema is free-form per the design spec and will be formalised after ~5 briefs.*
