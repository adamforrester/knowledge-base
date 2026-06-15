---
okf_version: "0.1"
type: component-brief
title: Select
description: The form component where accessibility ideals collide hardest with styling ambitions, and the first whose core is contested at the platform level. A field-truth study of the native-vs-custom decision (a framework, not a winner), the select-vs-combobox boundary, the multi-select models, the aria-activedescendant focus contract, and the platform shift — Popover API, CSS Anchor Positioning, and customizable-select — that is redrawing the whole component, with the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [dropdown, picker, listbox, select-panel, exposed-dropdown-menu]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Select

> Text Field is contested on its anatomy, Textarea on its physics; Select is contested on its *platform*. Like its form siblings it inherits the field substrate — label, helper, error, the describedby chain (see text-field) — but its core question is one no other form control faces: build on the native `<select>` or re-engineer the whole interaction as a custom ARIA listbox, and that single decision cascades into anatomy, accessibility, motion, and implementation. And it is the first brief written across a live platform inflection: the Popover API, CSS Anchor Positioning, and customizable-select are, right now, dissolving the trade-off the entire component was organised around. Select is the calibration brief for *the native-vs-custom decision and writing durably across a moving platform*.

---

## 1. Framing

A Select is a control for choosing one or several values from a **known, enumerable set the user does not type**. What it *isn't*: free-form text (Text Field/Textarea), a small mutually-exclusive set better shown inline (Radio/Segmented Control), a boolean (Switch/Checkbox), or — the load-bearing boundary — **a set the user filters by typing, which is a Combobox**. The select-vs-combobox confusion is the single most-confused adjacency in component libraries (both agents): a Select trigger is a *button*, and typing invokes non-destructive **type-ahead** (jump to the first match); a Combobox trigger is a *text input*, and typing **destructively filters** the list. The moment a field filters options as you type, you are in ARIA combobox territory with a different role and contract — the mirror of text-field's text-field-vs-combobox trap. The practice isolates the two into **separate components**, never a `searchable` flag bolted onto Select (both agents; IBM Carbon enforces the Dropdown-vs-Combobox split rigidly).

**The defining tension is native vs. custom, and it is a genuine trade, not a settled win** (both agents). Native `<select>` is accessible by construction, keyboard-complete, payload-free, and — decisively — delegates to the OS picker on mobile (the iOS wheel, the Android sheet), the best mobile select UX there is. But it cannot hold rich option content (avatars, secondary text, status) and resists styling, especially the option list. A custom ARIA listbox styles fully and holds rich content — but you now own the entire focus/keyboard/announcement contract, and most custom selects ship subtly broken (the external pass's Phase 1 "Styling Era" is precisely the record of that industry-wide regression).

What makes this brief unusual is that the trade is **actively dissolving**. The external pass frames a three-phase pendulum: a *Styling Era* (~2015–2020, custom `<div>` listboxes, accessibility regressions), an *Accessibility Era* (~2020–2024, headless libraries — React Aria, Radix — codifying ARIA 1.2 correctly but at heavy JS cost), and a *Platform Era* (2025–present) in which the **HTML Popover API, CSS Anchor Positioning, and the experimental `appearance: base-select`** let a *native* `<select>` accept rich DOM in `<option>` and expose the `::picker(select)` pseudo-element for full styling — collapsing the native-vs-custom trade entirely. This is real and directional, but it is **current-platform-state dependent**: the specifics (Chromium-only `base-select`, the version flags, the claimed bundle savings) must be verified before they harden, and the practice records them as the trajectory to design *toward*, not a shipped default (§11, §13).

## 2. Anatomy and parts

Inherits the Text Field field-row anatomy (label, required indicator, helper, error, the describedby wiring) — not repeated (see text-field §2). What is Select-specific is the **split anatomy**: a persistent trigger in document flow plus a transient overlay that must escape it (both agents):

- **Trigger** — for native, the `<select>` itself; for custom, a `<button>` (or, per ARIA 1.2, a `role="combobox"` element) carrying `aria-haspopup="listbox"`, `aria-expanded`, `aria-controls`. The accessible name comes from the associated label, never the placeholder. *Divergence worth noting:* Material 3's `ExposedDropdownMenuBox` uses a **read-only text field as the visual trigger** for parity with inputs (external) — visually clever, but a read-only-text-input-that-isn't-editable is an AT-clarity risk; prefer a button-semantics trigger.
- **Value display** — the selected label (or, for multi, a token row or count summary) inside the trigger.
- **Caret / disclosure icon** — the chevron; commonly rotates on open (§8).
- **Listbox overlay** (`role="listbox"`) — mounts in the **top layer** (Popover API) or, in older builds, a React portal, to avoid `overflow`/z-index clipping.
- **Option** (`role="option"`, `aria-selected`) — may carry leading visuals (icon/avatar), a description line, trailing metadata, and a selection indicator (checkmark / bold / background).
- **Option group** (`optgroup` / `role="group"` + label) — non-interactive sectioning.
- **Selection indicator, placeholder/empty, and multi-select extras** — per-option checkboxes, select-all, clear, the token row.

**The overlay mutates on mobile.** A narrow viewport should turn the popover listbox into a **tray / bottom sheet** for touch ergonomics (external — Spectrum's `sp-tray`); and Fluent exposes an `inlinePopup` to render the listbox inline rather than in a portal, working around an iOS VoiceOver bug where `aria-activedescendant` mapping is lost across a portalled overlay (external — a concrete, citable a11y trap, §6).

## 3. Properties / API

Inherits the Text Field core (`label`, `value`/`defaultValue`, `onChange`, `helpText`, `error`, `disabled`, `readOnly`, `required`, `name`, `id`, `size`, `clearable`) — see text-field §3. Select-specific:

**Data-driven vs. composed — the encapsulation divergence, Select's version of text-field's bundled-vs-composed question.** Two philosophies (external):

- **Data-driven** (`options={[{label, value, disabled, icon}]}`) — Base Web and Atlassian (the latter wrapping `react-select`). Terse, serializable (good for the `.ai.json` story), and — decisively — it gives the component the full item count up front, which is what virtualization needs to compute scroll heights before mounting (external).
- **Composed children** (`<Select.Option>`, `<Select.Group>`) — Spectrum/React Aria, Fluent. Natural JSX, clean for rich option content and interleaved dividers/groups, at the cost of the parent having to traverse the element tree to extract values/labels before render (external).

**The practice ships the hybrid** — consistent with the text-field call: an `options` array for the common flat case, *and* composed `<Option>`/`<Group>` children for rich content. (The external pass proposes `options` + an `itemRenderer` callback as the hybrid; composed children are the cleaner shape and match the catalogue's existing hybrid, with `itemRenderer` available as the data-driven escape hatch for teams that want it.) Keep single-select `value` a **scalar** and multi-select `value` an **array** — Base Web's always-array normalization buys signature consistency at the cost of a surprising single-select type, and the practice prefers the honest types.

Other Select-specific props:

- **`multiple`** — the single/multi switch. It *changes the keyboard contract* (Space toggles an option and keeps the listbox open, rather than selecting-and-closing) and needs a summary model (§4, §5).
- **`native`** — the practice exposes the native-vs-custom choice explicitly (a prop, or two components — §10), defaulting to native on touch / plain-text and custom where rich content is needed (§5). Architect the API so a native `<select>` can be dropped in under the hood as `base-select` lands (§11).
- **`placeholder`** — the no-selection prompt; not the label, not a real value. (Native trap: a placeholder `<option value="">` must be present-but-not-reselectable.)
- **`loading`** — async options: a trigger spinner (replacing the caret) and/or a listbox skeleton — not an empty state (both agents).
- **`searchable`** — *not a Select prop.* Routes to Combobox (§1, §12).

Two frontier props worth recording, neither a practice default: Carbon's **AI-inferred-option label** (a visual marker that a default selection was algorithmically suggested and wants verification — the same AI-presence signal as text-field §4), and Hydrogen's **URL-driven value** (its `VariantSelector` writes the selection to URL search params for shareable, indexable, progressively-enhanced variant links rather than local state — a genuinely useful pattern for e-commerce, external).

## 4. States and variants

Select doubles the form-field state matrix — it must keep the persistent trigger and the transient overlay in sync (external). Inherits the Text Field states (see text-field §4); Select-specific:

| State | Select-specific contract |
| --- | --- |
| expanded / open | trigger `aria-expanded="true"`; caret rotates; the trigger's border-radius may flatten on the seam with the listbox |
| option hover | a pointer over an option updates the *visual highlight only* — it must not mutate the value or fire selection (external) |
| selected | the option matching the value: checkmark / bold / high-contrast background (never colour alone) |
| loading | trigger spinner (replacing the caret) and/or listbox skeleton; not empty copy |
| empty — no selection | placeholder in the trigger |
| empty — no results | only in filtered/creatable selects: an explicit "No results" node in the listbox |
| read-only | renders the value, not interactive — note that native `<select>` has no `readonly`, only `disabled`, so a true submitted-but-not-editable select requires the custom path or a hidden mirror (§11) |

**Intentional variants:** `size` and density carry over (high-density matters for enterprise dashboards with long lists — external); single bordered/outline default. The Select-specific axes are **single vs. multi** (and the multi summary: tokens vs. count), and the **creatable / editable** variant — allowing a typed value not in the list, appending and selecting it (Atlassian/Base Web Creatable). Creatable deliberately blurs toward Combobox; treat it as a Combobox-adjacent mode, documented as such, not a casual Select toggle.

## 5. Usage guidance

- **Use** for choosing from a known, enumerable set the user doesn't type — and the field's converged sweet spot is **~5–15 options** that are familiar enough not to need upfront comparison (months, countries, status) and where vertical space is constrained (external).
- **Don't use** for: **≤~4–5 mutually-exclusive options** that should be exposed for one-tap choice (→ Radio Group; Material 3 pushes Connected Button Groups / Segmented Control for the rapid-toggle case — external); **>~15 options without search**, where scroll fatigue sets in (→ Combobox); **a set the user filters by typing** (→ Combobox); or **binary/on-off** (→ Switch/Checkbox).
- **Native-vs-custom decision framework** (the core call):
  - **Native `<select>` when** mobile/touch is primary (the OS picker is unbeatable), options are plain text, and rich content isn't needed. *Default to native.*
  - **Custom listbox when** options need icons/descriptions/two-line content, multi-select with tokens is required, or the trigger needs bespoke styling the platform can't yet deliver — *and* you accept ownership of the full a11y contract. As `base-select` matures, this branch shrinks (§11, §13).
- **Multi-select model:** **tokens/tags** when selections are few and identity matters (accepting that tokens wrap or truncate and complicate trigger height); a **count summary** ("3 selected") when many, or on mobile, to keep the trigger stable (external favours count for layout integrity). Inside the listbox, multi-select options **must render leading checkboxes** — a background highlight alone is an a11y failure (external).
- **Mobile:** prefer native; if custom, the listbox becomes a full-screen or bottom-sheet picker, not a cramped popover (§2).

## 6. Accessibility

The shared substrate (label association, describedby, error wiring, focus contrast) is in text-field §6. Select-specific — and the custom path is among the hardest a11y contracts in the catalogue (both agents):

- **Native `<select>` is the accessibility baseline** — role, keyboard, type-ahead, and AT announcements are correct for free; every custom listbox is measured against it, and most fall short. This is itself a strong argument for native.
- **The custom-listbox ARIA contract** (W3C APG Listbox): the trigger carries `aria-haspopup="listbox"` + `aria-expanded` + `aria-controls`, with `role="button"` *or* — per ARIA 1.2, for a control that opens a listbox — `role="combobox"` (the field is mid-migration on this; both are defensible, and the brief flags it as live). The overlay is `role="listbox"` (`aria-multiselectable` when multi); options are `role="option"` with `aria-selected`.
- **The focus contract is the make-or-break decision: DOM focus stays on the trigger.** Moving real focus into the overlay creates an inescapable trap; instead track the active option with **`aria-activedescendant`**, updating the referenced id as arrows move, so AT announces each option as if focused while the keyboard never leaves the trigger (both agents). This is the single most-cited custom-select failure when done wrong.
- **The portalled-overlay AT bug is real and citable:** when the listbox renders in a portal far from the trigger, iOS VoiceOver can lose the `aria-activedescendant` mapping — Fluent's `inlinePopup` (render inline, not portalled) is the documented mitigation (external). The Popover API top-layer model (§11) is the more durable fix.
- **Keyboard model:** Space/Enter or Down opens; Up/Down move the active option (and open if closed); Home/End jump; **type-ahead** selects by typed prefix with a ~500ms buffer-clear timeout; Enter/Space selects (in multi, Space toggles and keeps open, Enter commits/closes); Escape closes and returns visual focus to the trigger; Tab commits and closes. Type-ahead is expected, not optional.
- **Focus return** on close to the trigger; the focus-lost-to-`<body>` bug is the second most common custom-select failure.
- **WCAG SCs:** the Text Field set (1.3.5, 3.3.1/2/3, 1.4.11/2.4.13, 4.1.2 — doing heavy lifting on the custom roles, 2.5.8 on the trigger and options) **plus, specific to the overlay:** **1.4.13 Content on Hover or Focus** (the listbox must be Escape-dismissible and hoverable without collapsing) and **2.1.1 Keyboard** (the entire interaction, including scrolling overflowed options, operable without a pointer) (external supplied 1.4.13 / 2.1.1 / 4.1.2; the substrate set carries the rest).

## 7. Content guidelines

- **Label:** concise noun phrase, sentence case (shared with text-field) — reinforced here because the trigger's density tempts label-as-placeholder.
- **Placeholder:** the null state, plainly ("Country"), not an instruction ("Select a country from the list…"), and omittable when the label suffices (external; Base Web defaults to "Select…").
- **The optional-selection / "None" decision:** prefer a persistent **Clear** affordance on the trigger over a "None" option buried in the list (external) — the same first-class `clearable` with focus-return as text-field.
- **Options:** parallel, concise, sorted **meaningfully and locale-aware** (alphabetical/frequency/logical), not by data-insertion order; **never truncate option text with an ellipsis** — the listbox should size to the longest option or wrap, because a truncated option forces the user to guess hidden data (external).
- **Empty-listbox copy:** "No results" (filtered only); **loading is a spinner/skeleton, not empty copy.** Error copy follows SC 3.3.3 and is delegated to the substrate.

## 8. Motion and transition

The listbox entry/exit is the signature motion: a fast (~100–150ms) opacity fade plus a small vertical translate (e.g. `translateY(-4px)→0`), origin-anchored to the trigger, with the **exit faster than the entry** (~75ms, fade without translate) so dismissal feels instant (external). The platform shift reaches motion too: the Popover API + `@starting-style` let the `display: none → block` transition be authored in **pure CSS**, retiring the JS mount/unmount choreography that animation libraries existed to manage (external). Under `prefers-reduced-motion: reduce`, drop translation/scale and keep an accelerated opacity fade (~50ms) — React Spectrum now ships pre-calculated CSS variables for exactly this (external). The caret rotation on open follows the same reduce-motion rule. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

Inherits the Text Field i18n contract (logical-property RTL, expansion, IME — see text-field §9). Select-specific:

- **RTL mirrors the whole structure:** the caret moves to the leading (left) edge, text aligns right, and leading option visuals (flags, avatars) swap sides (external) — via logical properties so it's automatic.
- **The listbox must not be locked to the trigger width** — 30–50% expansion in German/Russian needs the overlay to grow its `min-width` to fit translated options (up to a viewport-bound max) rather than wrap or truncate (external; reinforces the no-truncation rule, §7).
- **Type-ahead must normalize diacritics:** typing "o" should match "Österreich" so users on non-localized keyboards can navigate (external) — fold Unicode normalization into the type-ahead matcher.
- **Locale-aware sort** (collation differs by language), and the **native picker localizes for free** — an argument for native in heavily-localized products. (See 13-internationalization-and-rtl.)

## 10. Naming

The field fragments: **`Select`** (Polaris, Atlassian, Base Web) vs. **`Picker`** (Spectrum) vs. **`Dropdown`/`Exposed Dropdown Menu`** (Carbon, Fluent, Material) vs. **`SelectPanel`** (Primer) (both agents). **The practice default is `Select`** — it maps cleanly to the native `<select>`, the clearest mental model for engineers (and the right anchor as the implementation moves toward native, §11). Reserve **`Combobox`** for the searchable sibling and **`Listbox`** for a bare headless primitive if exposed. Aliases to map in docs search: `Dropdown`, `Picker`, `Listbox`, `SelectPanel`, `ExposedDropdownMenu`, and `Combobox` *(flagged as the common mis-conflation, not a true alias — §1)*.

## 11. Implementation notes

The component is mid-transformation; the practice's call is to **build durably across the platform shift** rather than over-invest in soon-obsolete custom machinery.

- **Don't hand-roll the listbox** — for the custom path use a headless primitive (React Aria `useSelect`/`useListBox`, Downshift, Radix Select) for the focus/keyboard/ARIA contract; skin it. Hand-rolled selects are the highest-bug-density form control.
- **Positioning is moving off JavaScript.** The decade of Popper.js / Floating UI (recomputing coordinates on every scroll/resize, main-thread cost, detached popovers) is being replaced by **CSS Anchor Positioning** (`anchor-name` / `position-anchor` / `anchor()`) plus the **Popover API** top layer — positioning on the browser's layout engine, no portals, no z-index wars (external). *Verify support per target matrix* (the external pass cites Chrome 125 for anchor positioning; treat the version as a check, not a given) and keep a Floating-UI fallback until support is broad.
- **Customizable-select is the call to design toward.** `appearance: base-select` lets a native `<select>` accept rich DOM inside `<option>` and exposes `::picker(select)` for full styling — potentially deleting the entire custom listbox (the external pass cites ~29kB react-select / ~24kB Radix savings; treat the figures and the Chromium-only, behind-a-flag status as **unverified — verify before relying**). **Architect the API now so a native `<select>` can be dropped in under the hood** as support solidifies across Safari and Firefox.
- **Long lists:** virtualize beyond a few hundred options (render only the visible window; React Aria's `Virtualizer` is the reference) — but virtualization fights `aria-activedescendant` (the active option must be in the DOM) and type-ahead, and a list long enough to need it usually wants **search → Combobox**. (Hydrogen's 2,000-variant `VariantSelector` patch is the cautionary tale — external.)
- **Forms:** native `<select>` participates for free; a custom listbox needs a **hidden `<select>`/`<input>` mirror** to submit in a native `<form>` / Server Action (and to give the otherwise-readOnly-less custom control a submitted value, §4).

## 12. Related and alternative components

- **Composes with:** Label, Helper/FieldError, Option, OptionGroup, Icon (option/trigger visuals — see icon), Checkbox (multi-select options), Tag/Token (multi summary — see Tag when briefed), Popover/Listbox (the surface), Button (the trigger), Form.
- **Alternative to:** Combobox (searchable/typeahead — the §1 boundary; see combobox, which inherits this brief's overlay machinery and adds the destructive filter), Radio Group / Segmented Control / Connected Button Group (small sets exposed for one-tap), Checkbox Group (multi-select of a few items — see checkbox), Menu (commands, not value-setting — the select-vs-menu line: a menu *performs an action*, a select *sets a form value*), Switch/Checkbox (boolean).
- **Supersedes:** a bare unstyled native `<select>` without label wiring; a Menu misused to pick a form value.
- **Superseded by:** Combobox when the set grows large enough to need filtering.

(See text-field and textarea for the shared substrate this brief stands on, 03-component-library for the component model, and 29-per-component-documentation-template for the docs page this feeds. Combobox, when briefed, should back-reference this for the boundary; the Popover/Overlay and Menu briefs will share the overlay/positioning machinery covered here.)

## 13. Field POV evolution

The external pass's three-phase pendulum is the through-line, and the practice adopts it as the framing:

1. **Styling Era (~2015–2020)** — custom `<div>` listboxes to escape the unstylable native element, at the cost of industry-wide accessibility regressions.
2. **Accessibility Era (~2020–2024)** — headless libraries (React Aria, Radix) codify the ARIA 1.2 listbox/combobox patterns correctly, but heavy: JS positioning (Floating UI) and focus management dominate the payload.
3. **Platform Era (2025–present)** — the web platform absorbs the functionality: **Popover API, CSS Anchor Positioning, `appearance: base-select`** let native `<select>` carry custom styling and rich content, collapsing the native-vs-custom trade. A telling signal: Primer's ViewComponents reportedly entering maintenance mode as the platform overtakes the in-house effort (external — directional, unverified).

Secondary movements: **native-first resurgence on mobile** (the OS picker's UX pulling systems back to native); the **select-vs-combobox split hardening** into separate components; **multi-select tokenization** settling on the token-row + count-summary hybrid; and **AI-inferred-selection** markers appearing at the frontier (Carbon — §3), not yet a default.

## 14. Sources cited

Conservative dating (the external pass supplied aggressive, precise, largely 2026-stamped versions — Atlassian v16.10.0, Base Web v16.0.0, Primer v0.51.5, Fluent v8.125.6, Spectrum/React Aria v3.45.0, Polaris/Hydrogen v13.3.0 — held loosely and unverified; `last-audited` in frontmatter is the re-run trigger):

- Shopify Polaris — `Select` (native-leaning); Hydrogen `VariantSelector` (URL-driven state, 2,000-variant patch) (Polaris/Hydrogen, 2024–2026).
- Adobe Spectrum / React Aria — `Picker`, `ListBox`, `useSelect`, the `sp-tray` mobile mutation, `Virtualizer`, disclosure-animation CSS variables (Spectrum, 2024–2025).
- Google Material 3 — Exposed Dropdown Menu / `ExposedDropdownMenuBox` (read-only-text-field trigger), Connected Button Groups over segmented (Material 3, 2024–2026).
- IBM Carbon — `Dropdown` vs. `Combo box` dichotomy, `MultiSelect`, AI-explainability option labels (Carbon, 2024–2026).
- GitHub Primer — `SelectPanel`, anchored overlay, ViewComponents maintenance-mode signal (Primer, 2024–2026).
- Atlassian Design System — `Select` (react-select wrapper), Async/Creatable, `no-html-select` lint rule (Atlassian, 2024–2026).
- Uber Base Web — `Select` (data-driven, always-array value, Creatable, tag group) (Base Web, 2024–2026).
- Microsoft Fluent — `Dropdown`/`Combobox`, `inlinePopup` for the iOS VoiceOver `aria-activedescendant` bug (Fluent, 2024–2026).
- Apple HIG / Material 3 Compose — native pickers, mobile bottom-sheet (2024).
- W3C / WAI-ARIA APG — Listbox & Combobox patterns; CSS Working Group / MDN — CSS Anchor Positioning, the Popover API, `@starting-style`, the experimental `appearance: base-select` (2025–2026).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.3.5, 3.3.1, 3.3.2, 3.3.3, 1.4.11, 1.4.13, 2.4.13, 2.1.1, 4.1.2, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: select
  name: Select
  aliases: [dropdown, picker, listbox, select-panel, exposed-dropdown-menu]
  category: form
  status: stable
description: >
  Control for choosing one or several values from a known, enumerable set
  the user does NOT type. Native <select> or custom ARIA listbox — a
  decision framework, not a winner, and one the platform (Popover API,
  CSS Anchor Positioning, appearance:base-select) is actively collapsing.
  Not free-form (text-field), not filtered-by-typing (combobox), not a
  small inline set (radio/segmented), not commands (menu).
api:
  inherits: text-field   # label, value/defaultValue, onChange, helpText, error, disabled, readOnly, required, name, id, size, clearable + the bundled/composed hybrid + internal aria wiring
  data-model: "hybrid — options array (flat, virtualization-friendly) AND composed <Option>/<Group> children (rich content); itemRenderer as the data-driven escape hatch"
  props:
    - name: options
      type: array<{label,value,disabled?,icon?,description?,group?}>
      required: false
      description: Data-driven options (flat case). Gives item count up front for virtualization.
    - name: multiple
      type: boolean
      default: false
      description: Multi-select; value becomes an array; CHANGES keyboard contract (Space toggles + keeps open); needs summary model + leading checkboxes + select-all.
    - name: native
      type: boolean
      description: Native <select> vs custom listbox. Default native on touch / plain text. Architect so native can be dropped in as appearance:base-select lands.
    - name: placeholder
      type: string
      description: No-selection prompt; not the label, not a real value.
    - name: loading
      type: boolean
      default: false
      description: Async options; trigger spinner / listbox skeleton, not empty copy.
    - name: searchable
      type: boolean
      deprecated: true
      description: DO NOT use — searchable = Combobox, a separate component.
  frontier-not-default:
    - "AI-inferred-option label (Carbon) — marks an algorithmically suggested selection for verification"
    - "URL-driven value (Hydrogen VariantSelector) — selection in URL params for shareable/indexable links"
states:
  inherits: text-field   # rest, hover, focus-visible, disabled, read-only, loading, error, empty
  select-specific: [expanded, option-hover-highlight-only, selected, loading-listbox, no-selection, no-results]
  note: "native <select> has no readonly — only disabled; true read-only needs custom path or hidden mirror"
variants:
  size: [small, medium, large]
  density: [comfortable, compact]
  selection: [single, multiple]
  multi-summary: [count, tokens]
  rendering: [native, custom]
  mode: [creatable]      # blurs toward combobox; document as such
accessibility:
  inherits: text-field
  pattern: "native <select> baseline | APG Listbox (custom)"
  wcag-criteria: ["1.3.5", "3.3.1", "3.3.2", "3.3.3", "1.4.11", "1.4.13", "2.4.13", "2.1.1", "4.1.2", "2.5.8"]
  aria-attributes:
    trigger: "role=button | role=combobox (ARIA 1.2), aria-haspopup=listbox, aria-expanded, aria-controls"
    listbox: "role=listbox, aria-multiselectable (multi)"
    option: "role=option, aria-selected"
    active: "aria-activedescendant (focus STAYS on trigger — never move DOM focus into the overlay)"
    invalid: "aria-invalid on trigger"
  keyboard-model:
    open: Space/Enter/ArrowDown
    move: ArrowUp/Down, Home/End, type-ahead-by-prefix (~500ms buffer)
    select: Enter/Space (multi: Space toggles + keeps open, Enter commits)
    close: Escape (return focus to trigger), Tab (commit)
  focus-behavior:
    active-option: aria-activedescendant (not roving)
    on-close: focus returns to trigger
    portal-bug: "iOS VoiceOver loses activedescendant across a portal — inlinePopup / top-layer Popover mitigates"
content:
  label-pattern: "concise noun phrase, sentence case (shared with text-field)"
  placeholder-pattern: "plain null state ('Country'), not an instruction; omittable; never the label"
  option-pattern: "parallel, concise; sorted meaningfully + locale-aware; NEVER ellipsis-truncated (size to longest or wrap)"
  empty-pattern: "'No results' (filtered only); loading is a spinner/skeleton, not empty copy"
  clear-pattern: "persistent Clear affordance on the trigger over a 'None' option in the list"
  error-pattern: "what + how to fix (SC 3.3.3); aria-invalid on trigger; delegated to substrate"
motion:
  enter: "~100-150ms opacity + translateY(-4px)->0, anchored to trigger"
  exit: "~75ms, faster, fade without translate"
  reduce-motion: "drop translate/scale; accelerated opacity fade (~50ms)"
  platform: "Popover API + @starting-style enable pure-CSS enter/exit (retiring JS mount choreography)"
i18n:
  inherits: text-field
  select-specific:
    - "RTL mirrors caret (leading edge), text alignment, leading option visuals — via logical properties"
    - "listbox not locked to trigger width — grows min-width for expansion (German/Russian) up to viewport"
    - "type-ahead normalizes diacritics (o -> Österreich)"
    - "locale-aware option sort; native picker localizes for free"
implementation:
  - "don't hand-roll — headless primitive (React Aria useSelect, Downshift, Radix) for the contract; skin it"
  - "positioning moving off JS (Floating UI) to CSS Anchor Positioning + Popover API top layer — verify support, keep fallback"
  - "design toward appearance:base-select (rich DOM in <option>, ::picker styling) — architect so native drops in under the hood (UNVERIFIED — Chromium-only/flagged; verify)"
  - "virtualize long lists (React Aria Virtualizer) but it fights activedescendant + type-ahead — long list usually wants Combobox"
  - "custom listbox needs a hidden <select>/<input> mirror for native form/Server-Action submission"
composition:
  composes-with: [label, helper-text, field-error, option, option-group, icon, checkbox, tag, popover, listbox, button, form]
  alternative-to: [combobox, radio-group, segmented-control, checkbox-group, menu, switch, checkbox]
  supersedes: ["bare unstyled <select> without label wiring", "menu misused to set a form value"]
  superseded-by: ["combobox when the set needs filtering (>~15 options or typed filtering)"]
notes:
  contested:
    - native vs custom (decision framework, not a winner — and actively collapsing)
    - data-driven vs composed-children (ship both; composed cleaner than itemRenderer)
    - single-select scalar vs always-array value (we prefer honest scalar)
    - trigger role=button vs role=combobox (ARIA 1.2; live migration)
    - select vs combobox (searchable routes to combobox)
  unverified:
    - "appearance:base-select status + bundle-savings figures (~29kB react-select / ~24kB Radix)"
    - "Chrome 125 anchor-positioning version flag; Primer ViewComponents maintenance-mode signal"
    - "external-supplied 2026 version numbers"
  evolution: "Styling Era -> Accessibility Era -> Platform Era (the through-line)"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-select/` (15 June 2026). Both agents converged on the spine — native-vs-custom as the load-bearing decision framework (not a winner), the select-vs-combobox boundary drawn at destructive-filtering (Combobox) vs. non-destructive type-ahead (Select) with searchable routed to a separate component, the data-driven-vs-composed API tension resolving to a hybrid, the `aria-activedescendant` focus contract (DOM focus stays on the trigger), the multi-select token-vs-count summary with mandatory leading checkboxes, the ~5–15-option usage band, the listbox entry/exit motion with a faster exit, RTL mirroring of the whole structure, `Select` as the naming default, and the long-list-wants-Combobox conclusion. The brief leans on text-field/textarea for the shared form substrate (inherited, not re-derived) — Select's third such brief. External-agent contributions: the three-phase Styling/Accessibility/Platform evolution as the framing through-line, the Popover API + CSS Anchor Positioning + `appearance: base-select` platform shift and its motion (`@starting-style`) and bundle consequences, the Fluent `inlinePopup` iOS-VoiceOver `aria-activedescendant` bug, the Spectrum `sp-tray` mobile mutation, the Material `ExposedDropdownMenuBox` read-only-text-field trigger, the Hydrogen URL-driven `VariantSelector`, the Carbon AI-explainability labels, the Atlassian react-select/Creatable lineage, the diacritic-normalizing type-ahead, the no-ellipsis option rule, and the virtualization/2,000-variant cautionary tale. Claude-pass contributions: the select-vs-menu boundary (a menu performs an action, a select sets a value), the honest scalar-vs-array value position against Base Web's always-array, the hidden-mirror-for-form-submission and native-has-no-readonly notes, and the consistency of the hybrid API with the text-field encapsulation call. The external pass's aggressive 2026 version numbers, the `appearance: base-select` status and bundle figures, the Chrome 125 flag, and the Primer-maintenance-mode signal are all flagged **unverified** pending `_source-text/` backing — the same provenance discipline as the Button and Text Field briefs. The §15 schema is free-form per the catalogue design spec and will be formalised after ~5 briefs.*
