# Button — field-truth study

## 1. Framing

Button is the most-shipped, least-agreed-upon component in any system. Every library has one; almost none agree on the prop model, and the disagreements are not cosmetic — they encode different theories of how a design system should expose intent versus appearance.

What a Button *is*, for the purpose of this brief, is the in-flow trigger for an action: it does something *now*, in the current context (submit, open, confirm, delete). What it *isn't*: navigation (that is a Link, even when it looks like a button), a binary toggle (Switch/Checkbox), or a persistent selection (segmented control, ToggleButton). The single most consequential boundary in the entire component is **button-versus-link semantics** — `<button>` triggers an action and is operated with Space and Enter; `<a href>` navigates, is operated with Enter only, and exposes a URL to the context menu, middle-click, and the accessibility tree. Field leaders converge completely on the rule (action → button, navigation → link) and diverge entirely on how to *enforce* it through the API.

Why systems disagree on Button:

- **Appearance versus intent.** Some systems name variants by visual weight (`primary`/`secondary`/`tertiary` — appearance), others by communicative role (`emphasis: bold/subtle`, `tone: critical/success` — intent). The split is philosophical: do you let the consumer pick a look, or pick a meaning and derive the look?
- **The hierarchy axis is overloaded.** "Primary" conflates *visual emphasis* (how loud) with *page rank* (the one action that matters most here). Newer systems are trying to split these into orthogonal axes; older ones bundle them.
- **The polymorphism problem.** A Button that can render as `<a>` is convenient and semantically dangerous. Whether to allow `as`/`href` on Button, or force a separate component, is unsettled.
- **Loading and disabled** are both "you can't use this right now" but have opposite accessibility consequences, and systems handle the difference unevenly.

## 2. Anatomy and parts

The converged structural model is a single interactive container wrapping an optional leading adornment, a required-or-optional label, and an optional trailing adornment, with an optional state overlay:

- **Container / target** — the `<button>` (or `<a>` styled as button) element. Owns the hit area, focus ring, background, border, radius. This is the accessibility target; minimum touch size lives here (WCAG 2.5.8, 24×24 CSS px minimum; 44×44 per Apple HIG; Material's 48×48 recommendation).
- **Leading icon / start slot** — decorative-by-default icon before the label.
- **Label** — the text. For an icon-only button this is *visually* absent but must still exist as an accessible name.
- **Trailing icon / end slot** — disclosure chevron, external-link indicator, dropdown caret.
- **Loading indicator** — spinner that typically *replaces* the leading icon or overlays the label while preserving the button's width to prevent layout shift.
- **Pressed/state layer** — Material's "state layer" is the explicit named part here (a tint overlay whose opacity encodes hover/focus/pressed). Most web systems express the same thing with background/box-shadow tokens rather than a named layer.

Slot vocabulary diverges: Polaris uses `icon`; Carbon uses `renderIcon` (a component reference, not a node); Spectrum and Primer use explicit `<Icon>`/leading-visual children; Material names `startIcon`/`endIcon` (MUI's implementation of M3) or icon slots in Compose. The deep divide is **icon-as-prop versus icon-as-child**: prop is constrained and easy to lint; child is flexible and easy to misuse (two icons, an image, arbitrary nodes).

## 3. Properties / API

**Converged across nearly every field leader:**

- An action/click handler (`onClick`/`onPress`).
- A label, supplied as children (web) or a `label`/`text` prop (some mobile/RN APIs).
- A disabled flag.
- A size scale (see §4).
- A variant/hierarchy axis (see §4 — this is where naming diverges).
- A "stretch to container width" flag — `fullWidth` (Primer, MUI), `block` (Carbon historically), `isFullWidth` (Spectrum). Universally present, universally named differently.
- An element-type escape hatch — `as`/`asChild`/`href`/`renderRoot`. Present in most, contested (see §11).
- A type passthrough — the HTML `type` (`button`/`submit`/`reset`). **The recurring trap: the platform default is `type="submit"`, so a Button inside a `<form>` with no explicit `type` submits the form.** Some systems (Primer) default their component to `type="button"` to neutralize this; others pass through and inherit the platform footgun.

**Divergences worth reasoning about:**

- **Loading state as prop.** Polaris `loading`, Carbon (via state), Primer `loading` + `loadingAnnouncement`, Spectrum `pending` (added 2024) with a built-in delay before the spinner appears. Atlassian `isLoading`. The divergence is whether the system owns the busy announcement and the anti-flicker delay, or leaves them to the consumer. Spectrum's `pending` is the most opinionated: it delays the spinner, keeps the label, sets `aria-disabled` rather than `disabled` so focus is retained, and announces busy.
- **Icon-only as a separate component versus a prop.** Primer ships `IconButton` as a distinct component (forces `aria-label`); Spectrum has `ActionButton`; Material has `IconButton`; Polaris encourages `Button` with `icon` and `accessibilityLabel`. Splitting the component lets you *require* the accessible name at the type level — the strongest argument for the split.
- **Tone/intent versus visual variant.** Polaris `tone="critical"` + `variant`; Spectrum `variant="accent|negative|primary|secondary"` + `style="fill|outline"` + `staticColor`; Carbon `kind="primary|secondary|tertiary|ghost|danger"`; Primer `variant="default|primary|danger|invisible"`; Atlassian `appearance="default|primary|subtle|warning|danger|link"`. Material 3 enumerates *five named button types* (elevated, filled, filled-tonal, outlined, text) rather than orthogonal axes — the most "appearance-first" model in the field.
- **`destructive`/`danger` as its own axis versus a tone value.** Most fold it into the variant/tone enum; a few (Spectrum `negative`) treat it as a semantic variant. Practice question: is "danger" an emphasis level or a tone? Treating it as tone (orthogonal to emphasis) lets you have a low-emphasis destructive action (subtle "Delete") — which the page-rank-coupled "danger variant" model can't express cleanly.

**The orthogonal-axis ideal** (where the field is trending, 2023–2025): separate **emphasis** (how visually loud: bold/default/subtle/plain) from **tone/intent** (neutral/critical/success/...) from **size** from **shape**. This composes cleanly (subtle + critical = quiet delete) but explodes the visual matrix and pushes work onto token theming. Spectrum and Polaris are closest to it; Material 3 is furthest from it.

## 4. States and variants

**Runtime states** (set by the system/user, not chosen at author time):

| State | Trigger | Notes / contested points |
|---|---|---|
| rest | default | — |
| hover | pointer over | not available on touch; never the sole carrier of meaning |
| focus-visible | keyboard focus | must use `:focus-visible`, not `:focus`, to avoid ring-on-click; ring must meet 3:1 (WCAG 1.4.11) and 2.4.13 focus-appearance (2.2) |
| pressed/active | pointer down / Space-Enter held | Material models this as a state-layer opacity |
| disabled | `disabled` prop | **the central contested decision** — see below |
| loading/pending | async in flight | retain width; announce busy; keep label or replace with spinner |
| error | not a button state | error belongs to the form/field, not the button — leaders agree the button has no `error` state; the empty/read-only states from the generic spine **do not apply** to Button |

**The disabled debate** is the single most contested accessibility decision in this component:

- Native `disabled` removes the element from the tab order and the accessibility tree's interaction affordances, gives no tooltip-on-hover, and announces nothing about *why* it's disabled. It is the simplest and the most user-hostile.
- `aria-disabled="true"` (plus suppressing the action handler) keeps the button focusable and discoverable, lets you attach an explanatory tooltip/`aria-describedby`, and is increasingly the recommended pattern for buttons whose disabled reason matters (form submit blocked by validation). Spectrum's `pending`, GOV.UK guidance, and a growing share of accessibility practitioners favor keeping critical actions focusable.
- Field state (2024–2025): most component *defaults* still map to native `disabled`; the more accessibility-forward systems expose or default to the focusable `aria-disabled` pattern for submit-style buttons. This is genuinely unsettled — flag it as a per-engagement decision, not a universal default.

**Intentional variants** (author-chosen):

- **Size** — converged on a 3-step scale (small/medium/large) as the default; some add xsmall (Spectrum) or micro (Polaris historically). Medium is the default everywhere.
- **Emphasis/hierarchy** — primary/secondary/tertiary or bold/default/subtle/plain. The "one primary per view" guidance is near-universal (Material, Polaris, Carbon, Atlassian all state it).
- **Tone/intent** — neutral/critical(danger)/success/warning. Critical is universal; success/warning buttons are rarer and several systems deliberately omit success-toned buttons (color isn't the right carrier for "this is the safe choice").
- **Width** — auto / full-width.
- **Shape** — most are rectangle-with-radius; Material 3 (2024–2025) introduced *shape morphing* (shape changes on press) and a `square`/`round` shape distinction, which is a Material-specific divergence.

**Canonical matrix** the practice can adopt: `emphasis {bold, subtle, plain} × tone {neutral, critical} × size {sm, md, lg} × width {auto, full}`, with icon-leading / icon-trailing / icon-only / loading as orthogonal modifiers. Everything else (success tone, elevated/tonal Material types, shape morph) is system-specific extension.

## 5. Usage guidance

- **Use** for an immediate action in the current context: submit, save, confirm, delete, open dialog, trigger async work.
- **Don't use** for navigation — use a Link (even if visually a button; see §6). Don't use for toggling a persistent on/off state — use Switch or a pressed ToggleButton (`aria-pressed`). Don't use a chain of equal-emphasis primary buttons — the field is unanimous that a view has at most one primary.
- **What to use instead:**
  - Navigation that looks like a button → Link styled as button (Primer `LinkButton`, Spectrum link, or `as="a"`).
  - Many low-emphasis inline actions → text/plain button or link-button.
  - Binary state → Switch (settings, immediate effect) or Checkbox (form, deferred submit).
  - One-of-many persistent selection → segmented control / ToggleButton group.
  - A menu trigger → button with `aria-haspopup` + `aria-expanded` (a MenuButton), not a bare button.
- **Decision framework, emphasis:** assign emphasis by the action's importance *to this view*, not its importance globally. Exactly one bold/primary; the destructive action is usually *not* the primary even on a delete screen (the primary is "Cancel"/"Keep", the destructive is secondary-critical) — though this is a content/safety call, not a hard rule.

## 6. Accessibility (Button-specific only)

Assuming 14 / 17 / 28 are read, the Button-specific contract:

- **ARIA role.** Use native `<button>` — it carries `role="button"`, focusability, and Space/Enter activation for free. `<div role="button">` is the canonical anti-pattern: it requires manually adding `tabindex="0"`, `keydown` handlers for *both* Enter and Space (and `keyup` for Space to match native, plus `preventDefault` on Space to stop page scroll), and still misses Windows High Contrast affordances. Only reach for it when forced by legacy constraints.
- **Keyboard model.** `<button>`: Enter activates on keydown, Space activates on keyup. `<a href>` styled as button: Enter only — Space scrolls. This asymmetry is *the* reason link-vs-button matters to AT users, and the reason a "button" with no real action should still be a `<button>` and a "button" that navigates should be a real link.
- **Accessible name.** Text content is the name. For icon-only: `aria-label` (or visually-hidden text) is mandatory — the highest-frequency real-world Button a11y failure. Prefer a separate IconButton component that requires the name at the type level. If a visible label and `aria-label` disagree, voice-control users who say the visible word can't activate it (WCAG 2.5.3 Label in Name) — keep `aria-label` a superset of the visible text.
- **Loading/busy announcement.** A spinner is invisible to AT unless announced. Set `aria-busy="true"` and/or a polite live-region message ("Saving…"). Keep the button focusable while loading (use `aria-disabled`, not `disabled`) so focus isn't lost and the busy state is discoverable. Primer's `loadingAnnouncement` and Spectrum's `pending` both formalize this.
- **Disabled discoverability.** See §4 — native `disabled` is silent and unfocusable; `aria-disabled` + suppressed handler keeps the *why* reachable. Never put a tooltip on a natively-disabled button (it can't receive hover/focus reliably).
- **Toggle buttons** use `aria-pressed` (true/false) — distinct from `aria-expanded` (for disclosure/menu triggers) and `aria-checked` (for switch role). Conflating these is a common AT bug.
- **WCAG SCs the button participates in:** 1.4.11 Non-text Contrast (focus ring, boundary 3:1), 2.4.7 Focus Visible, 2.4.13 Focus Appearance (2.2), 2.5.3 Label in Name, 2.5.5/2.5.8 Target Size, 4.1.2 Name/Role/Value, 1.4.13 (only if a tooltip is attached). Disabled-contrast is explicitly *exempt* from contrast minimums, which is exactly why silent-disabled hurts — it's allowed to be illegible.

## 7. Content guidelines

- **Verb-first, action-specific labels.** "Save changes", "Delete file" — not "OK", "Submit", "Yes". Field-unanimous (Polaris, Material, Atlassian, Carbon content guidance all say this).
- **Match the destructive verb to the consequence**; the confirm button in a delete dialog should say "Delete" (echoing the action), not "Confirm" — reduces mode errors.
- **Length.** Keep to 1–3 words where possible; the label drives min-width and the i18n expansion budget (§9). Sentence case is the modern default (Material moved away from ALL CAPS in M3; Polaris, Primer, Atlassian all sentence-case).
- **No "click here" / no device verbs** ("tap"/"click") — the label should read the same across input modalities.
- **Empty/error copy** don't apply to Button itself (no empty or error state, §4); error copy belongs to the field/form the button submits.
- **Icon-only buttons** still need a name that *is* the action ("Add to cart"), not the icon's appearance ("plus").

## 8. Motion and transition

- **State transitions** (hover/press) are short token-driven color/opacity/elevation changes — Material's state-layer opacity ramps; web systems' background/shadow transitions, typically 100–200ms, ease-out. These should run through motion *tokens*, not hard-coded.
- **Press feedback.** Material 3 uses ripple + (2024+) shape-morph on press; iOS uses a brief dim/scale; most web systems use a background/elevation shift only. Ripple is a Material signature and a divergence, not a default to copy.
- **Loading.** The spinner's appearance should be *delayed* (~ Spectrum-style threshold, e.g. a few hundred ms) so fast responses don't flicker a spinner. Preserve button width across the rest→loading transition (reserve label width) to avoid layout shift.
- **reduce-motion contract.** Under `prefers-reduced-motion: reduce`: drop ripple/shape-morph/scale; keep the *instantaneous* state color change (state must still be perceivable). The spinner is a functional indicator, not decoration — it may keep a reduced/none animation but the busy state must still be conveyed (the `aria-busy`/live-region path carries it regardless).

## 9. Internationalization

- **Text expansion.** German/Finnish/Russian can run 30–100% longer than English at short string lengths; buttons are *the* component where this bites because labels are short and authors set fixed widths. Don't fix button width to the English label; allow wrap or min-width with generous max. Polaris and Material both warn on this explicitly.
- **RTL.** Mirror the whole button: leading icon moves to the visual right, trailing/disclosure chevrons flip direction (a "next →" becomes "← التالي"). Use logical CSS properties (`padding-inline-start`, `margin-inline-end`) so leading/trailing slots mirror automatically. Directional icons (arrows, chevrons) must flip; non-directional icons (search, settings, brand glyphs) must *not* — this per-icon decision is the recurring RTL trap.
- **Loading spinners** generally do not flip direction by locale (spin direction is not semantic), though a few systems mirror them; not worth opinionating.
- **Locale.** Don't bake verb conjugation or interpolation into the component; the label is a passed-in string the consumer localizes.

## 10. Naming

- **Component name.** "Button" is universal. Icon-only: split opinion — `IconButton` (Primer, Material/MUI), `ActionButton` (Spectrum). Practice default: ship **Button** and a distinct **IconButton** (so the accessible name is required at the type level).
- **The variant-axis names are where the field fragments** (see §3): `variant` (Primer/MUI), `kind` (Carbon), `appearance` (Atlassian), `variant`+`style`+`staticColor` (Spectrum), named button types (Material). Practice default: **`emphasis`** (bold/subtle/plain) + **`tone`** (neutral/critical/...) as orthogonal axes, with `variant` accepted as a deprecated alias for migration.
- **Aliases consumers reach for:** `primary`/`secondary` (→ emphasis), `danger`/`destructive` (→ tone:critical), `cta`, `pill` (shape), `block` (→ fullWidth), `ghost`/`text`/`link`/`plain` (→ emphasis:plain or a LinkButton). Document the alias→canonical mapping so search/codemod can resolve them.

## 11. Implementation notes

- **`type` default.** In a form, default the component to `type="button"` unless `submit` is explicit, OR force the author to choose. The platform `submit` default is the most common real bug. (Primer defaults to `button`.)
- **Polymorphism — `as`/`asChild`/`href`.** Three approaches: (a) a single Button with `as`/`href` that swaps the element (convenient, risks shipping `<a>` with no href = a "button" that doesn't work, or `<button href>` = ignored); (b) Radix-style `asChild` that merges props onto a single child (powerful, sharp edges around prop merging and ref forwarding); (c) separate `Button` and `LinkButton` (Primer) — most explicit, most components. Recommendation: **separate LinkButton** for clarity; if you must polymorph, validate that `href` ⇒ renders `<a>` and that `<a>` paths drop button-only props (`type`, `disabled`→`aria-disabled`).
- **Icon as prop vs child.** Prop (`icon={IconSearch}`) is lintable and constrained; child (`<Button><Icon/>Label</Button>`) is flexible and abuse-prone. For a DS that wants enforceable consistency, prefer the **prop** for leading/trailing icons and reserve children for the label.
- **Headless vs opinionated.** React Aria (Adobe), Radix, Ark, and Base UI provide a headless `useButton`/`Button` that normalizes the cross-element behavior (press events across mouse/touch/keyboard/pointer, the `<a>`/`<button>`/`<div>` differences, focus-visible, disabled). React Aria's `usePress` deliberately *unifies* press across input types and fixes mobile 300ms/ghost-click and drag-cancel behavior — worth adopting under the hood even in an opinionated system. The tension: headless gives correct behavior + your styling but you own all visual tokens; fully-opinionated (Material/Polaris) gives batteries-included visuals but fights custom theming.
- **Forwarding `ref` and spreading rest props** to the underlying element is expected by consumers; failing to forward `ref` breaks tooltip/popover anchoring.
- **Loading width preservation:** render the label invisibly (visibility:hidden / opacity:0) under the spinner rather than removing it, to hold width.

## 12. Related and alternative components

- **Composes with:** Icon (leading/trailing), Spinner (loading), Tooltip (label for icon-only / disabled-reason — with the disabled-focus caveat), ButtonGroup (grouping/segmentation), Menu/Popover (as a MenuButton trigger via `aria-haspopup`/`aria-expanded`).
- **Alternative to:** Link (navigation vs action — the core boundary), IconButton (icon-only specialization), ToggleButton (`aria-pressed` persistent state), Switch (binary setting), Chip/Tag (removable/selectable token).
- **Supersedes:** legacy `<input type="button|submit">` and `<div role="button">` patterns; ALL-CAPS Material 2 button styling (M3 sentence case).
- **Superseded by:** nothing — Button is foundational. (Material 2's button taxonomy was *superseded by* M3's five-type model within the Material lineage.)

## 13. Field POV evolution

- **Sentence case over ALL CAPS.** Material 3 (2021→) abandoned the M2 uppercase button label; the field is now uniformly sentence/Title case.
- **Owned loading/pending state.** Spectrum added `pending` (2024) with built-in delay + focus retention + busy announcement; Primer formalized `loading` + `loadingAnnouncement`. The field is moving the busy-state responsibility *into* the component.
- **Disabled → focusable disabled.** Growing movement (accessibility practitioners, GOV.UK, Spectrum `pending` using `aria-disabled`) away from native `disabled` for critical actions toward focusable `aria-disabled` + suppressed handler + explained reason. Still not the default in most systems — the live edge.
- **Orthogonal axes over named variants.** Trend toward separating emphasis from tone from shape (Spectrum, Polaris) rather than one overloaded `variant` enum — though Material 3 went the *other* way with five discrete named button types, so the field is genuinely split here.
- **Material 3 expressive (2024–2025):** shape morphing on press, new shape/size matrix, refreshed button group behaviors — Material-specific, not a cross-field default.
- **Headless adoption underneath opinionated systems.** React Aria's `usePress` press-normalization is increasingly used as the behavioral substrate even where the visual layer is bespoke.

> Verification path for the dated claims above: Material 3 docs (m3.material.io, "Buttons" + "Expressive" update), Spectrum `pending`/Button changelog (spectrum.adobe.com), Primer Button/IconButton docs (primer.style), Polaris Button (polaris.shopify.com), React Aria `useButton`/`usePress` (react-spectrum.adobe.com). Re-confirm version dates at synthesis time.

## 14. Sources cited

- Shopify Polaris — Button (Polaris 12.x, 2024–2025).
- Adobe Spectrum — Button, incl. `pending` (Spectrum 2024.x); React Aria / React Spectrum `useButton`, `usePress` (2024–2025).
- Google Material 3 — Buttons; M3 Expressive shape/morph update (Material 3, 2024–2025; sentence-case change from M3, 2021).
- IBM Carbon — Button, `kind` model (Carbon v11, 2024).
- GitHub Primer — Button, IconButton, LinkButton, `type="button"` default, `loading`/`loadingAnnouncement` (Primer React, 2024–2025).
- Atlassian Design System — Button, `appearance` model (ADS, 2024).
- Shopify Hydrogen — uses Polaris/Hydrogen primitives; no material Button divergence from Polaris noted (2024).
- Base Web (Uber) — Button `kind`/`shape`/`size` (Base Web v13–14, 2023–2024).
- Apple Human Interface Guidelines — Buttons, 44pt target (HIG, 2024).
- Microsoft Fluent 2 — Button variants (Fluent 2, 2024).
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
  Not navigation (use Link), not persistent state (use Switch/ToggleButton).
api:
  props:
    - name: children
      type: ReactNode (label)
      required: true            # except when iconOnly/IconButton
      description: Visible label; verb-first, sentence case.
    - name: onClick
      type: function
      required: false
      description: Action handler. Suppressed when aria-disabled.
    - name: emphasis
      type: enum
      values: [bold, subtle, plain]
      default: subtle
      required: false
      description: Visual loudness, orthogonal to tone. One bold per view.
    - name: tone
      type: enum
      values: [neutral, critical, success]
      default: neutral
      required: false
      description: Communicative intent; color is never the sole carrier.
    - name: variant
      type: enum
      deprecated: true
      description: Legacy alias for emphasis+tone; map primary->bold,
        secondary->subtle, danger->tone:critical.
    - name: size
      type: enum
      values: [sm, md, lg]
      default: md
      required: false
    - name: fullWidth
      type: boolean
      default: false
      required: false
      description: Stretch to container; aliases block/isFullWidth.
    - name: type
      type: enum
      values: [button, submit, reset]
      default: button          # opinionated: neutralize platform submit default
      required: false
    - name: disabled
      type: boolean
      default: false
      required: false
      description: Prefer aria-disabled+suppressed handler for critical
        actions so the disabled reason stays focusable/announced.
    - name: loading
      type: boolean
      default: false
      required: false
      description: Delays spinner ~few hundred ms, retains width, keeps
        focus (aria-disabled not disabled), announces busy.
    - name: iconLeading
      type: IconComponent
      required: false
    - name: iconTrailing
      type: IconComponent
      required: false
    - name: as | href
      type: polymorph (string|element)
      required: false
      description: Discouraged; prefer separate LinkButton. href MUST
        render <a>; <a> path drops type/disabled.
composition:
  composes-with: [icon, spinner, tooltip, button-group, menu, popover]
  alternative-to: [link, icon-button, toggle-button, switch, chip]
  supersedes: ["input[type=button|submit]", "div[role=button]"]
  superseded-by: null
accessibility:
  wcag-criteria: ["1.4.11", "2.4.7", "2.4.13", "2.5.3", "2.5.5", "2.5.8", "4.1.2", "1.4.13"]
  role: button            # native <button>; avoid div[role=button]
  aria-attributes:
    - aria-label           # required for icon-only; superset of visible text
    - aria-disabled        # preferred over native disabled for critical actions
    - aria-busy            # during loading
    - aria-pressed         # only for toggle buttons
    - aria-haspopup        # only for menu-trigger buttons
    - aria-expanded        # only for disclosure/menu triggers
  keyboard-model:
    button: { enter: keydown-activate, space: keyup-activate }
    link-as-button: { enter: activate, space: scrolls }   # why button!=link
  focus-behavior:
    focus-visible: required   # :focus-visible, 3:1 ring, SC 2.4.13
    disabled-focus: retained-when-aria-disabled
    loading-focus: retained
states:
  runtime: [rest, hover, focus-visible, pressed, disabled, loading]
  not-applicable: [error, empty, read-only]   # belong to field/form, not button
variants:
  emphasis: [bold, subtle, plain]
  tone: [neutral, critical, success]
  size: [sm, md, lg]
  width: [auto, full]
  modifiers: [icon-leading, icon-trailing, icon-only, loading]
content:
  label-pattern: "verb-first, action-specific, sentence case, 1-3 words; no 'OK'/'click here'"
  error-pattern: null     # button has no error state
  empty-pattern: null     # button has no empty state
i18n:
  text-expansion: "no fixed width to English label; allow min-width + wrap"
  rtl: "mirror layout via logical props; flip directional icons only"
notes:
  contested:
    - disabled-vs-aria-disabled (live edge)
    - emphasis/tone orthogonal axes vs single variant enum (field split)
    - polymorphism (as/href) vs separate LinkButton
    - icon-as-prop vs icon-as-child
```
