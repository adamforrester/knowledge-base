---
okf_version: "0.1"
type: component-brief
title: Text Field
description: The component where accessibility, validation, and composition collide. A field-truth study of where the leading systems converge (placeholder-is-not-a-label, static top labels, read-only ≠ disabled, the aria-describedby chain, the polite character counter) and where they fracture (bundled-props vs. composed-slots, how far to split the typed-component family, who owns validation timing), with the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [text-input, input, textbox, formfield]
last-audited: 2026-06-14
timestamp: 2026-06-14
---

# Text Field

> Button is contested on its variant model; Text Field is contested on its anatomy. Where a button has one interactive element, a text field is a labelled control with up to four satellite text regions — label, helper, error, character count — each of which must be programmatically associated or it is invisible to assistive tech. The disagreements encode rival theories of where the field ends and the form begins, who owns validation, and how much of the typed-input family to split into separate components. If Button is the calibration brief for *intent vs. appearance*, Text Field is the calibration brief for *encapsulation boundary and accessibility wiring*.

---

## 1. Framing

The text field is the fundamental primitive of data capture — the conduit between human intent and machine state (external). Its conceptual simplicity hides the deepest *structural* disagreement in the catalogue: what actually constitutes the component. Is a text field the bare `<input>`, or does it encapsulate the input, its `<label>`, the container, the helper text, and the validation message inside one immutable boundary (external)? Every API divergence in §3 descends from where a system draws that line.

What a Text Field *is*, for this brief: a single-line control for free-form, non-enumerable text the system cannot offer as a fixed set — names, emails, search queries, SKUs, amounts (both agents). What it *isn't*: multi-line input (Textarea), a choice from a known set (Select / Radio / Combobox), a boolean (Checkbox / Switch), a date (Date Picker), or a rich-text editor. The boundary that recurs and bites is **text-field-versus-combobox**: the moment a suggestion list attaches, the component is in ARIA combobox territory with a different keyboard and ARIA contract — bolting autocomplete onto a plain text field is the single most common way teams ship a broken combobox (Claude).

Why systems disagree, beyond the encapsulation line:

- **Monolithic vs. composite.** Spectrum and Material 3 have historically bundled label, input, and validation into one component — rigid, consistent, accessible by construction, but hostile to bespoke layouts (a field inline in a sentence, a custom element between label and input) (external). Primer, Fluent, and Atlassian separate the input primitive from a `FormControl` / `Field` parent the consumer wires together — more flexible for horizontal and data-dense forms, but it lets a developer detach a label or forget an error message (external). The field is converging on a **hybrid**: a constrained monolithic `TextField` for the common vertical-form case, with the underlying primitives exposed for the edge cases (external; React Aria's `TextField` composing `Label`/`Input`/`Text`/`FieldError` is the reference). This is the practice's foundational call — see §3.
- **How far to split the typed family.** Does one component take a `type` prop, or does the family fracture into `TextField` / `NumberField` / `EmailField` / `SearchField`? (See §3 — the external pass argues for an aggressive split; we land in a defensible middle.)
- **Who owns validation** — and when it fires (§3, §6).
- **Placeholder semantics** — universally settled as an anti-pattern when used as a label, but not every API makes the right thing the easy thing.

Framework coupling adds a final axis. The external pass reports Polaris migrating from React components to framework-agnostic Web Components (`<s-text-field>`, Shadow DOM), while Shopify Hydrogen rejects opinionated wrappers entirely in favour of native `<input>` + React Router form actions — the same component, opposite postures, because governed admin dashboards and performance-obsessed storefronts want opposite things (external). We record the Polaris/Web-Components claim as **unverified** (same provenance gap as the Button brief; §11, §14).

## 2. Anatomy and parts

A production text field is a small multi-node structure, and the field has converged on roughly the same parts (both agents):

- **Root / container** — the outermost element; establishes the positioning context for floating labels or absolutely-positioned validation icons, and owns the layout flow of label, input, and messages (external).
- **Label** — the accessible name. Static text above the field (Carbon, Polaris, Spectrum, Primer) or a floating element that animates from the input line to the top on focus (Material 3). Required for every field; a visually-hidden label is the only acceptable "label-less" case, and even then it exists in the DOM (both agents).
- **Required / optional indicator** — asterisk or "(optional)" suffix; the field is split on which to mark (§7).
- **Input control** — the `<input>` itself; owns `type`, `value`, `placeholder`, `autocomplete`, `inputmode`. This is the accessibility target and the node a `ref` must reach (§11).
- **Leading / trailing adornment slots** — affixes inside or beside the field. Naming diverges sharply: `prefix`/`suffix` (Polaris, Spectrum), `leadingVisual`/`trailingVisual` (Primer), `startEnhancer`/`endEnhancer` (Base Web), `contentBefore`/`contentAfter` (Fluent) (external). **The load-bearing distinction is decorative vs. interactive**: a currency glyph or search icon is a *visual adornment* that must be `aria-hidden` and must not be the field's accessible name; a clear or password-reveal control is an *action* — a real `<button>` with its own `aria-label` and tab stop. Both agents independently warn that a generic "enhancer" slot invites consumers to drop clickable icons in without keyboard handling or ARIA — the recurring inaccessibility trap. Primer formalises the split (`leadingVisual`/`trailingVisual` for visuals, `TextInput.Action` for interactives) (external).
- **Helper / description text** — persistent guidance below the field, associated via `aria-describedby` (`helpText` Carbon, `caption` Primer, `description` Spectrum).
- **Error / validation message** — replaces or supplements helper text on error, associated via `aria-describedby` with the field marked `aria-invalid` (`invalidText` Carbon, `ValidationMessage` Primer).
- **Character counter** — optional; the live-region wiring is the hardest part (§6).

Two structural archetypes: **floating label** (label doubles as placeholder, animates up on focus/fill — Material's signature) vs. **static top-aligned label** (label always above). The field has largely moved *against* floating labels for accessibility and i18n reasons — the label collides with the placeholder, truncates under text expansion, and an empty field can read as filled. Material 3 still offers floating; Polaris, Carbon, Primer, and Spectrum default to static top labels (Claude, corroborated by external's motion treatment). **The practice default is the static top label.**

## 3. Properties / API

**The converged core** (both agents, near-universal across Polaris, Spectrum, Material 3, Carbon, Primer, Atlassian, Base Web):

- `value` / `defaultValue` — controlled and uncontrolled (universal).
- `onChange` (and `onBlur`, `onFocus`).
- `label` — string or node; required in practice.
- `placeholder` — example text only, never the label (universal in *existence*, contested in *discipline*).
- `helpText` / `description` — persistent guidance.
- `error` / `errorMessage` / `invalid` — error state + message.
- `disabled` and `readOnly` — distinct, and routinely confused (§4).
- `required` — plus the optional/required display convention (§7).
- `size` — three tiers (small / medium / large); Carbon maps these to 32 / 40 / 48px (external).
- `autoComplete` — the WHATWG token (`email`, `name`, `current-password`, `one-time-code`); an accessibility obligation, not a convenience (§6).
- `id` / `name` — wiring and form submission.

**The encapsulation decision — the load-bearing divergence.** The field splits between bundled props (`<TextField label helpText error>`, Polaris) and composed children (`<TextField>` wrapping `<Label>`/`<Input>`/`<Text slot="description">`/`<FieldError>`, React Aria/Spectrum). Bundled is terse but fixes the layout of the satellite regions; composed is verbose but hands the consumer layout control while the wiring is handled by context (Claude). Both agents land on the **hybrid**: ship `label`/`helpText`/`error` as props for the 90% vertical-form case, *and* expose the composed slots for the 10% that needs custom layout. The non-negotiable, regardless of surface, is that the wiring — `id` generation, `aria-describedby` chaining, `aria-invalid` — is handled internally and correctly (§6, §11). This is the practice's foundational call for the component.

**How far to split the typed family — where we diverge from the external pass.** The external agent argues the generic `type` multiplexer is being *deprecated entirely* in favour of discrete components (`TextField` / `NumberField` / `EmailField` / `URLField`), citing Polaris's `<s-text-field>`/`<s-number-field>`/`<s-email-field>` split and Spectrum's separate `NumberField`. The core insight is right but the conclusion overshoots. The practice's position is a **graduated split by behavioural distance**:

- **`NumberField` is genuinely a separate component.** It needs a different keyboard model (increment/decrement, spinbutton semantics), locale-aware decimal/grouping parsing, and wheel-scroll suppression so a scroll past the page doesn't mutate the value (both agents). `<input type="number">` is an outright trap — it accepts `e`/`+`/`-`, breaks on locale separators, and surprises with spinbutton AT semantics (Claude). Reach for `NumberField`, never `type="number"`.
- **`SearchField` and `PasswordField` are thin specialisations** — `SearchField` adds clear + `type="search"` + a search-submit affordance; `PasswordField` adds the reveal toggle. Worth their own names so the extra affordances and their accessible names are baked in.
- **`email` / `url` / `tel` stay as `type` + `inputmode` + `autocomplete` on the base `TextField`.** They need no different keyboard model and no different validation engine — only attributes that change the mobile keyboard and autofill. Spinning up separate components for them is matrix bloat without behavioural payoff. (Note: React Spectrum's `TextField` itself still carries a `type` prop for exactly these — the external pass overstated the breadth of the deprecation.)

**Validation ownership and timing.** Three field stances: (a) the field is purely presentational and renders the `error` it is handed, with a form library owning timing (Polaris, Primer); (b) the field integrates the native Constraint Validation API and can hook `<form>` validation / `:invalid` (React Aria/Spectrum, via `validationBehavior="native"`); (c) the field owns a `validate` prop. **The practice default is presentational by default** — the form library (React Hook Form, Formik, native Server Actions) owns timing — **with optional native-constraint integration** for teams that want it. Do not bake a validation *engine* into the field. The timing contract itself (validate on blur, re-validate on change *after* the first error, focus the first invalid field on submit, error summary for long forms) is in §6 (Claude).

**`clearable`.** Base Web ships a first-class `clearable` that injects a labelled clear button and handles `clearOnEscape`; Primer makes the consumer compose it (external). **We make `clearable` first-class** — the recurring trap is returning focus to the `<input>` after the clear button is pressed, which average implementations mishandle and strand focus (external). The clear control is a real labelled button that announces the cleared state.

**Native attribute pass-through.** Base Web and Primer rest-spread all native attributes onto the `<input>` (arbitrary `data-*`, `aria-*`); Spectrum abstracts the DOM and strips unknown attributes, exposing only a curated ARIA surface (external). The trade-off is escape-hatch flexibility vs. protecting the internal accessibility contract. We **spread to the input by default** (consumers need it for analytics, third-party form libs, and `ref`/anchoring — §11) while owning the a11y-critical attributes internally so a consumer cannot accidentally clobber them.

**Forms-era APIs.** React 19 / Server Actions pass a `FormData` object to a form `action`, superseding the synthetic-`onSubmit` paradigm; Spectrum's field already supports it (external). The field must emit a real `<input name>` so it works uncontrolled, in a native `<form>`, with `useFormStatus`, and with the Constraint Validation API. A field that only works controlled is a liability in 2026 form architectures (both agents).

## 4. States and variants

**Runtime states** — Text Field is the component where the *full* generic state set actually applies (unlike Button):

| State | Trigger | Contract |
| --- | --- | --- |
| rest | default | base tokens |
| hover | pointer over | subtle border/background shift; never the sole carrier |
| focus-visible | keyboard or click focus | `:focus-visible` ring, ≥3:1 vs. surroundings (WCAG 1.4.11, 2.4.13) — the field is a primary focus target |
| pressed | touch-down (mobile) | tactile feedback before the virtual keyboard animates up; largely a mobile concern (external — Material 3 Compose, Apple HIG) |
| disabled | author / app state | native `disabled` — removed from tab order, not submitted, silent to AT; exempt from contrast |
| read-only | author / app state | **distinct from disabled** — focusable, selectable/copyable, *submitted*, passes contrast (`readonly` attribute) |
| loading | async validation / value | spinner replaces an adornment without reflow; `aria-busy`; don't block typing unless intended (external — Primer `loading`/`loaderPosition`) |
| error | validation failure | `aria-invalid="true"` + `aria-describedby` → message; never colour-only; pair with an error icon |
| warning | soft validation | non-blocking caution (external — Carbon); *contested* — many systems collapse warning into helper/error, so treat as optional, not core |
| empty | no value | placeholder/label state; the reason floating labels are risky (empty must not read as filled) |

**read-only vs. disabled is the Text-Field-specific live edge** — the analogue of Button's disabled debate. `disabled` removes the field from the tab order and form submission and is silent to AT; `readOnly` keeps the value reachable, copyable, and submitted, and passes contrast. Blurring them strands data a screen-reader user cannot reach (both agents — Fluent and Carbon treat `readOnly` as a first-class distinct property). Use `readOnly` for values the user may need to read or copy but not edit (a generated API key); reserve `disabled` for fields irrelevant in the current state — and consider the focusable-inactive pattern (see Button §4, and 28) where the *reason* for disablement matters.

**Intentional variants** (author-chosen): `size` {small, medium, large} × density {comfortable, compact — Carbon adds a borderless "fluid" variant for fields flush against toolbars/grid cells (external)} × an appearance axis some systems expose (outline / underline / filled — Material's and Fluent's split). **The practice default is a single bordered (outline) style at three sizes**; filled and underline are theming choices, not API variants (both agents recommend limiting container variation and bulletproofing runtime states across sizes instead).

A frontier note: Carbon ships an **"AI Presence"** variant — a gradient + AI iconography signalling that content was AI-generated or that the field prompts an agent, doubling as an explainability-popover trigger (external). This is a single-system frontier pattern, not a practice default; we flag it as a signal for the four-layer AI stack (see 15-ai-in-ds and GLOSSARY) rather than adopting it, and revisit if it spreads.

## 5. Usage guidance

**Use** for free-form, non-enumerable single-line input — names, titles, SKUs, identifiers, short queries (both agents).

**Don't use** when the value comes from a known set (→ Select / Radio / Combobox), spans multiple lines or needs review of large blocks (→ Textarea), is numeric-formatted (→ NumberField — and for an approximate/relative numeric value, → Slider, optionally paired with NumberField for precision; see slider), is boolean (→ Checkbox / Switch), is a date (→ Date Picker, though a masked text input is a legitimate fallback), or needs suggestions (→ Combobox) (both agents).

**Decision frameworks rather than rules:**

- **Label always visible.** The only acceptable label-less field is search with a visually-hidden label and a search-icon affordance — and the label still exists in the DOM (both agents).
- **One input, one concept.** Don't pack "first last" or "MM/YY/CVC" into one field unless masking genuinely helps; multiple concepts → multiple fields (Claude).
- **Helper text is persistent guidance; error is a state.** Show the format hint in helper text *before* the user fails, not only in the error message (both agents).
- **Mark the minority.** If most fields are required, mark "(optional)"; if most are optional, mark required — consistently within a form (both agents).
- **Mobile: minimise text entry.** On Watch/TV-class devices, prefer selection, dictation, or button-driven gathering; when a field is necessary, set the right `inputmode`/`type` so the correct virtual keyboard appears (external — Apple HIG).
- **Inline-edit for dense data.** For editing discrete values in place rather than in a dedicated form, an inline-editable pattern (a static read view that swaps to an edit field on interaction) cuts the visual clutter of dozens of persistent borders (external — Atlassian `InlineEditableTextfield`).

## 6. Accessibility

The theory is in 14-accessibility, 17-accessibility-annotation-contract, and 28-web-accessibility-implementation; this is only what is Text-Field-specific.

- **Programmatic label association is the whole game.** `<label for=id>` or a wrapping `<label>`. `placeholder` is *not* a label — it disappears on input (failing SC 3.3.2), is typically styled below the 4.5:1 text-contrast floor (1.4.3), and is not a reliable accessible name (both agents). Use `aria-label`/`aria-labelledby` only when a visible `<label>` genuinely cannot be used, and treat that as an exception requiring review (external — Spectrum's governance).
- **The `aria-describedby` chain is the recurring wiring failure.** Helper text *and* error message both associate via `aria-describedby` (the field can reference multiple ids, announced in sequence on focus). On error, set `aria-invalid="true"` and ensure the error id is in the chain. Primer auto-generates the ids via React Context and stitches the chain so the consumer never hand-manages ids (external) — this is the pattern to copy (§11).
- **`autocomplete` is an accessibility obligation.** WCAG 2.2 **SC 1.3.5 Identify Input Purpose** requires the purpose of fields collecting user info to be programmatically determinable; the WHATWG `autocomplete` token is how you satisfy it (Claude). *This is the most Text-Field-specific SC and the external pass omitted it from its criteria list — a genuine gap; the prose is authoritative here.*
- **The character counter is the hardest a11y problem in the component.** A naive live-updating count machine-guns the screen reader on every keystroke ("100 remaining… 99… 98…"), rendering the field unusable (external). The established fix (GOV.UK and USWDS field research): the *visual* counter updates instantly but is `aria-hidden="true"`; a *separate* visually-hidden node with `aria-live="polite"` announces the count only when the user pauses typing (external). This bifurcated pattern is the practice default for any counted field.
- **Required.** Set `required`/`aria-required`; don't rely on the asterisk alone — it is a visual-only cue unless the label text or `aria-required` carries it (both agents).
- **Error timing.** Validate on blur, re-validate on input *after* the first error, announce politely, move focus to the first invalid field on submit, and surface an error summary for long forms (Claude; see 28).
- **High Contrast Mode.** In Windows HCM the field must adopt system colours — border matching button-text colour at rest, switching to button-border colour on hover/focus (external — Spectrum). Carbon enforces a 3:1 non-text contrast for the field boundary itself so the hit area is identifiable before focus (external).
- **Target size.** The input and any interactive affix (reveal / clear) meet the target-size minimum (SC 2.5.8), and those affixes carry accessible names (both agents).
- **WCAG SCs the field participates in:** 1.3.5 Identify Input Purpose, 1.3.1 Info and Relationships, 3.3.1 Error Identification, 3.3.2 Labels or Instructions, 3.3.3 Error Suggestion, 1.4.3 Contrast, 1.4.11 / 2.4.13 (focus and boundary contrast), 4.1.2 Name/Role/Value, 2.5.8 Target Size, and — for login/checkout fields specifically — 3.3.7 Redundant Entry and 3.3.8 Accessible Authentication (WCAG 2.2) (Claude; external supplied 1.3.1/1.4.3/3.3.1/3.3.2/4.1.2 and missed the 1.3.5 and 2.2-auth set).

## 7. Content guidelines

- **Label: noun or noun phrase, sentence case, concise** — "Email address," not "Enter your email address here." Carbon forbids trailing colons; keep labels ≤3 words to bound the i18n budget (external).
- **Placeholder: an example, never an instruction or the label** — "name@example.com." It vanishes on input, so nothing load-bearing lives there (both agents).
- **Helper text carries the format up front** — "Use 8+ characters," shown before failure, not only in the error (both agents).
- **Error message: say what is wrong AND how to fix it** (SC 3.3.3). "Enter a valid email address, e.g. name@example.com," not "Invalid input." Be specific, be human, don't blame the user — and pair it with an error icon so it is not colour-only (both agents).
- **Required / optional:** mark the minority, consistently (§5).
- **Empty state** for a field is just the placeholder/label; there is no separate empty UI (both agents). (See 04-documentation for the system-level content-guidelines layer.)

## 8. Motion and transition

State transitions — border colour on focus/error, the helper→error swap — are short token-driven changes, ~100–150ms, eased-out (both agents). The error appearance must not jank the layout: reserve space or animate height gently so the form does not jump (Claude). The **floating-label animation**, if used, is the one signature motion — label sliding from the input line to the top and shrinking as the value enters (external — Material 3). **Reduce-motion contract:** under `prefers-reduced-motion: reduce`, resolve label/indicator transitions to an instant position/colour change rather than a slide, keeping the state perceivable; an async-validation spinner is functional (carried by `aria-busy` / the live region), not decoration (both agents). (See 18-motion-foundations and 19-motion-implementation-web.)

## 9. Internationalization

- **Text expansion.** Labels, helper, and error text expand substantially in German, Russian, and others; never fix the field's label or message width — allow wrap, never truncate (an ellipsis hides the field's purpose) (both agents). Field *width* is content-driven — a postcode input is narrower than a street address; size to expected input, and for horizontal label layouts use a min-width safe zone or wrap (external — Primer `layout="horizontal"`).
- **RTL.** Mirror via logical properties (`padding-inline-start`, flex `gap`) so leading/trailing adornments swap sides automatically; systems on absolute physical positioning fail here (external). **But the input *content* direction can differ from the UI direction** — a Latin email or phone number typed into an Arabic UI. Set `dir="auto"` on the input (or rely on the Unicode bidi algorithm) so the value renders correctly regardless of UI direction (Claude). Currency/unit affixes follow locale placement (symbol before vs. after the number).
- **Locale input.** Numeric fields must respect locale decimal/grouping separators — a comma is a decimal point across much of Europe and a thousands separator in North America; parse locale-aware before sending to the backend (external — Carbon `NumberInput`). And **don't fire validation mid-IME-composition** — guard on `compositionstart`/`compositionend` so CJK input isn't validated on intermediate keystrokes (Claude). (See 13-internationalization-and-rtl.)

## 10. Naming

The component name splits along framework-era lines: **`TextField`** (Polaris, Spectrum, Material, Atlassian, Fluent) vs. `TextInput` (Carbon, Primer) vs. `Input` (Base Web) (both agents). **The practice default is `TextField`** for the composed, ready-to-deploy component (label + input + helper + error), reserving **`Input`** / **`TextInput`** for the bare headless primitive if we expose one.

Prop aliases consumers will reach for, with canonical mappings for codemod/search: `helperText`/`description` → `helpText`; `errorText`/`errorMessage`/`invalidText` → `error`; `leadingVisual`/`trailingVisual`/`startEnhancer`/`endEnhancer`/`contentBefore`/`contentAfter` → `prefix`/`suffix`; `readonly` → `readOnly`. The typed specialisations are their own components, not props: `NumberField`, `SearchField`, `PasswordField` (§3) — name them explicitly so consumers don't reach for `type="number"` on the base. Documentation search must alias `TextBox`, `Input`, and `FormField` to this page (external).

## 11. Implementation notes

- **Wire ids internally with `useId`.** The component generates stable ids to connect `label[for]`, `aria-describedby` (helper + error), and `aria-invalid` without the consumer hand-managing them — the most common real a11y failure in shipped fields is broken or duplicated ids in this chain (both agents; Primer's Context-driven auto-stitching is the reference, §6).
- **`forwardRef` to the `<input>`, not the wrapper.** A `ref` passed to the composite must pierce the structural `<div>` and land on the input node, or consumers can't programmatically focus on load or focus the first invalid field on submit (external — Primer, Spectrum). The ref-misroutes-to-wrapper bug is a recurring trap.
- **Controlled and uncontrolled both.** The React traps: a controlled `value` with no `onChange` (read-only by accident), and flipping `value` between a string and `undefined` (switching the input controlled↔uncontrolled mid-life). Default to uncontrolled with `defaultValue` for form-library ergonomics; support controlled for live formatting (Claude).
- **Emit a real `<input name>`** so the field works uncontrolled, in a native `<form>`, with `useFormStatus` / Server Actions, and with the Constraint Validation API (both agents, §3).
- **Don't use `type="number"`** for general numeric input — prefer `inputmode="numeric"`/`decimal` + formatting, or the dedicated `NumberField` (§3).
- **Separate adornment from action** in the slot API (§2) so consumers can't drop an unlabelled clickable icon into a "visual" slot.
- **Autofill styling.** Browser autofill applies UA styles (`:-webkit-autofill`) that fight token theming; handle the filled state explicitly or it looks broken (Claude).
- **Headless substrate, opinionated skin.** As with Button, the wiring (ids, describedby, invalid, focus) belongs in a headless primitive (React Aria's field hooks) with the visual surface themeable; ship the bundle for the common case and expose the composed slots for the rest (both agents).

*A cross-cutting unverified claim, identical in provenance to the Button brief:* the external pass reports Polaris migrating to framework-agnostic Web Components (`<s-text-field>`, Shadow DOM), with `2025-07` as the final React-API release, and notes the Shadow-DOM friction that React `onChange` doesn't bubble identically across the boundary (forcing raw `addEventListener('input')` or a bridge). The direction matches Shopify's stated trajectory but we have no `_source-text/` backing for the specific version/date, so we record it as a claim to verify before it hardens (§14).

## 12. Related and alternative components

- **Composes with:** Label, Helper/Description text, FieldError, Icon (prefix/suffix adornment), Button (clear / reveal action), Spinner (loading), Form (the composite owner), Tooltip (optional inline help — never the sole carrier of essential info).
- **Alternative to:** Textarea (multi-line — see textarea, which inherits this brief's substrate and diverges on the sizing model, the character counter, and the Enter-key contract), Select / Combobox (enumerable / suggested values — see select for the listbox sibling and the select-vs-combobox boundary), NumberField (numeric), SearchField (search + clear), Date Picker (dates), PasswordField (reveal), Checkbox / Switch (boolean).
- **Supersedes:** a bare `<input>` without label wiring; the placeholder-as-label pattern; `type="number"` for formatted numeric input.
- **Superseded by:** nothing for free-form single-line text; specific uses migrate to the typed siblings above.

(See 03-component-library for the system-level component model this brief sits under, and 29-per-component-documentation-template for the delivered docs page this brief feeds.)

## 13. Field POV evolution

Macro shifts over the last ~two years, both agents converging on direction:

1. **Floating labels out of favour.** Static top-aligned labels are now the assumed default for accessibility, i18n, and density; Material 3 retains floating as an option but it is no longer the field-wide norm.
2. **Placeholder-as-label is universally an anti-pattern** — settled, though legacy code persists.
3. **The typed family is splitting.** The old single polymorphic `<Input type>` is fracturing into discrete components (Spectrum's `NumberField`, Polaris's `<s-number-field>`) for tree-shaking and localised behaviour/a11y — we adopt this for `NumberField`/`SearchField`/`PasswordField` and hold the line at `type`+attributes for email/url/tel (§3).
4. **Accessibility wiring moved into Context.** Primer and Fluent auto-generate ids and stitch the `aria-describedby` chain via React Context, removing the highest-frequency manual-ARIA error class from the consumer (external).
5. **Validation-timing consensus** converging on validate-on-blur, re-validate-after-first-error, focus-first-invalid, error-summary-for-long-forms; and **`autocomplete` hardening into a 1.3.5 obligation**, with WCAG 2.2's auth SCs (3.3.7, 3.3.8) raising the bar on login/checkout fields specifically (Claude).
6. **Framework-agnostic delivery** (the unverified Polaris Web Components move, §11) and **AI-presence states** (Carbon's frontier variant, §4) are the two edges to watch — neither is a practice default yet.

## 14. Sources cited

Field-leader systems, conservative version dates (the external pass supplied more precise numbers — Primer v36.4.0, Carbon v1.109.0, Polaris 2025-07/2025-10, Fluent v9, Base Web v10 — held loosely and unverified; `last-audited` in frontmatter is the re-run trigger):

- Shopify Polaris — `TextField` (bundled label/helpText/error, prefix/suffix, clearable); the (unverified) Web Components split into `<s-text-field>`/`<s-number-field>`/`<s-email-field>` (Polaris, 2025).
- Adobe Spectrum / React Aria — `TextField`, `NumberField`, `SearchField`, the composed `Field` model, native Constraint Validation integration, React 19 `action`/`FormData` support, High Contrast Mode behaviour (Spectrum, 2024–2025).
- Google Material 3 — filled / outlined text fields, floating-label motion (Material 3, 2024).
- IBM Carbon — `TextInput`, size px mapping (32/40/48), fluid variant, warning state, locale-aware `NumberInput`, 3:1 boundary contrast, AI-presence variant (Carbon, 2024–2026).
- GitHub Primer — `TextInput` / `FormControl`, Context-driven `aria-describedby` stitching, `leadingVisual`/`trailingVisual` vs. `TextInput.Action`, `loading`/`loaderPosition`, `layout="horizontal"`, `forwardRef` to input (Primer, 2024–2025).
- Atlassian Design System — `Textfield` / `Field`, `InlineEditableTextfield` (Atlassian, 2024).
- Uber Base Web — `Input`, `startEnhancer`/`endEnhancer`, `clearable`/`clearOnEscape`, native attribute pass-through (Base Web, 2024).
- Microsoft Fluent UI (v9) — `contentBefore`/`contentAfter` slot polymorphism, first-class `readOnly`, required-asterisk convention (Fluent, 2024–2025).
- Shopify Hydrogen — native `<input>` + React Router form actions as the headless-storefront posture (Hydrogen, 2024).
- Apple Human Interface Guidelines — minimise text entry on Watch/TV, virtual-keyboard `type` selection (Apple HIG, 2024).
- GOV.UK Design System & USWDS — accessible character-counter research (the `aria-hidden` visual + polite-live-region bifurcation).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.3.5, 1.3.1, 3.3.1, 3.3.2, 3.3.3, 1.4.3, 1.4.11, 2.4.13, 4.1.2, 2.5.8, 3.3.7, 3.3.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: text-field
  name: TextField
  aliases: [text-input, input, textbox, formfield]
  category: form
  status: stable
description: >
  Single-line control for free-form, non-enumerable text. Composite of
  label + input + helper + error. Not multi-line (textarea), not a known
  set (select/combobox), not numeric-formatted (number-field), not
  suggestion-backed (combobox).
api:
  props:
    - name: label
      type: string | node
      required: true        # visually-hidden allowed, never absent
      description: Visible persistent label; never the placeholder.
    - name: value
      type: string
      required: false
      description: Controlled value; pair with onChange.
    - name: defaultValue
      type: string
      required: false
      description: Uncontrolled initial value (preferred for form libraries).
    - name: onChange
      type: function
      required: false
    - name: type
      type: enum
      values: [text, email, url, tel, search, password]
      default: text
      required: false
      description: Passthrough for attribute-only variants (mobile keyboard +
        autofill). NOT number — use number-field. search/password better
        served by their thin specialisations.
    - name: placeholder
      type: string
      required: false
      description: Example only; vanishes on input; never load-bearing.
    - name: helpText
      type: string | node
      required: false
      description: Persistent guidance; wired via aria-describedby.
    - name: error
      type: string | node
      required: false
      description: Error message; sets aria-invalid + describedby; say what
        and how to fix (SC 3.3.3); pair with icon, not colour-only.
    - name: required
      type: boolean
      default: false
      required: false
      description: Sets required/aria-required; mark the minority in a form.
    - name: disabled
      type: boolean
      default: false
      required: false
      description: Removes from tab order + submission; silent to AT; exempt
        from contrast.
    - name: readOnly
      type: boolean
      default: false
      required: false
      description: Focusable, copyable, SUBMITTED, passes contrast. Distinct
        from disabled.
    - name: autoComplete
      type: string (WHATWG token)
      required: false
      description: Satisfies SC 1.3.5 Identify Input Purpose.
    - name: inputMode
      type: enum
      values: [text, numeric, decimal, tel, email, url, search]
      required: false
    - name: prefix
      type: slot (adornment)
      required: false
      description: Static/decorative affix; aria-hidden if purely visual.
    - name: suffix
      type: slot (adornment | action)
      required: false
      description: May hold a labelled action (clear/reveal) — a real
        focusable button, not decoration.
    - name: clearable
      type: boolean
      default: false
      required: false
      description: Adds a labelled Clear button; announces cleared state;
        returns focus to the input.
    - name: loading
      type: boolean
      default: false
      required: false
      description: Async validation/value; spinner replaces an adornment
        without reflow; sets aria-busy.
    - name: size
      type: enum
      values: [small, medium, large]
      default: medium
      required: false
states:
  runtime: [rest, hover, focus-visible, pressed, disabled, read-only, loading, error, empty]
  optional: [warning]            # contested; many systems fold into helper/error
  notes:
    read-only-vs-disabled: "readOnly submits + is copyable + passes contrast; disabled does none and is silent to AT"
variants:
  size: [small, medium, large]
  density: [comfortable, compact, fluid]
  style: [outline]               # default; filled/underline are theming, not API
  frontier: [ai-presence]        # Carbon-only; not a practice default
accessibility:
  wcag-criteria: ["1.3.5", "1.3.1", "3.3.1", "3.3.2", "3.3.3", "1.4.3", "1.4.11", "2.4.13", "4.1.2", "2.5.8", "3.3.7", "3.3.8"]
  label-association: "native <label for>/wrapping; placeholder is NOT a label"
  aria-attributes:
    - aria-invalid        # on error
    - aria-describedby    # helper + error ids, auto-stitched
    - aria-required       # when not native required
    - aria-label          # only when no visible <label> possible
    - aria-live           # polite, on the visually-hidden char-counter node
    - aria-busy           # during loading
  keyboard-model:
    typing: native text editing
    tab: focuses input; interactive affixes are separate tab stops
    escape: clears value when clearable
  focus-behavior:
    focus-visible: required        # ring + boundary >=3:1 (1.4.11/2.4.13)
    error-focus: move-to-first-invalid-on-submit
    ref: forwardRef must reach the <input>, not the wrapper
  character-counter:
    visual: aria-hidden=true, updates instantly
    announced: separate visually-hidden node, aria-live=polite (speaks on pause)
content:
  label-pattern: "noun phrase, sentence case, <=3 words, no trailing colon; never the placeholder"
  placeholder-pattern: "example value only; nothing load-bearing"
  helper-pattern: "format/constraint shown before failure"
  error-pattern: "what is wrong AND how to fix (SC 3.3.3); icon + text, not colour-only; not 'Invalid input'"
  empty-pattern: "label + optional placeholder; no separate empty UI"
i18n:
  text-expansion: "no fixed label/message width; wrap, never truncate; field width content-driven"
  rtl: "mirror via logical properties; set dir=auto on input so content direction can differ from UI"
  locale: "locale-aware decimal/grouping parsing (number-field); guard validation during IME composition"
composition:
  composes-with: [label, helper-text, field-error, icon, button, spinner, form, tooltip]
  alternative-to: [textarea, select, combobox, number-field, search-field, date-picker, password-field, checkbox, switch]
  supersedes: ["bare input without label wiring", "placeholder-as-label", "type=number for formatted numeric"]
  superseded-by: null
notes:
  contested:
    - bundled-props vs composed-slots (ship both: props for 90%, slots for 10%)
    - how far to split the typed family (number-field separate; email/url/tel = type+attrs)
    - validation ownership/timing (presentational default; form lib owns timing)
    - floating vs static label (static default; floating is a Material option)
    - warning as a distinct state (optional; many systems fold it in)
  unverified:
    - polaris-web-components-migration (needs _source-text backing; shared with button brief)
    - external-supplied precise version numbers
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-14-component-text-field/` (14 June 2026). Both agents converged on the spine — the monolithic-vs-composite encapsulation tension resolving to a hybrid (bundled props + composed slots), placeholder-is-not-a-label, the static top-label default, read-only ≠ disabled as the component's live edge, the decorative-adornment vs. interactive-action slot split, the `aria-describedby` helper+error chain auto-wired via generated ids, the GOV.UK/USWDS polite-live-region character counter, first-class `clearable` with focus return, `NumberField` as a genuinely separate component, `TextField` as the naming default, logical-property RTL with no-fixed-width expansion and locale-aware number parsing, the ~100–150ms reduce-motion transition contract, and a real `<input name>` for Server-Actions/FormData. The practice's graduated typed-family split (NumberField/SearchField/PasswordField separate; email/url/tel as `type`+attributes) is the chosen middle between the external pass's argued full deprecation of the `type` multiplexer and a single polymorphic component. External-agent contributions: the Carbon size px mapping / fluid / warning / AI-presence variants, the Fluent `contentBefore`/`contentAfter` slot polymorphism, the Primer Context-driven id-stitching and `forwardRef`-to-input trap, the native-attribute pass-through vs. strict-ARIA divergence, the Windows High Contrast behaviour, the Atlassian inline-edit pattern, the Apple-HIG minimise-text-entry guidance, and the (unverified) Polaris Web Components migration. Claude-pass contributions: the text-field-vs-combobox boundary as the key adjacency trap, `autocomplete` as the SC 1.3.5 obligation and the WCAG 2.2 auth SCs (3.3.7/3.3.8) — both omitted by the external pass's criteria list, the validation-timing framework, the controlled/uncontrolled React traps, `dir="auto"` for content-vs-UI direction and the IME-composition validation guard, and the autofill-styling note. Version numbers are held conservatively per §14; the Polaris Web Components migration and external-supplied precise version numbers are flagged unverified pending `_source-text/` backing. The §15 schema is free-form per the catalogue design spec and will be formalised after ~5 briefs.*
