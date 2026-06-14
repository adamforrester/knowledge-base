# Text Field — field-truth study

## 1. Framing

Text Field is the component where accessibility, validation, and composition collide. Button is contested on its *variant model*; Text Field is contested on its *anatomy* — what counts as part of the field versus part of the form, who owns validation timing, and how the label/helper/error trio wires to the input for assistive tech. Where Button has one interactive element, Text Field has a labelled control with up to four satellite text regions (label, helper/description, error, character count), each of which must be programmatically associated or it is invisible to a screen reader.

What a Text Field *is*: a single-line control for free-form text the system cannot enumerate (names, emails, search queries, amounts). What it *isn't*: a multi-line input (Textarea), a choice from a known set (Select/Radio/Combobox), a boolean (Checkbox/Switch), or a rich-text editor. The boundary that recurs is **text-field-versus-combobox**: the moment you attach a suggestion list you are in ARIA combobox territory with a different keyboard and ARIA contract — bolting autocomplete onto a plain text field is the most common way systems ship a broken combobox.

Why systems disagree:

- **Where the field ends and the form begins.** Does the component own the label, the helper, the error, and the layout of all three — or is it a bare input that a separate `FormField`/`Field` wrapper composes? Spectrum and React Aria lean on a composed `TextField`/`Field` model; Polaris bundles `label`/`helpText`/`error` as props on one `TextField`; Carbon and Primer sit between. This is the deepest structural divergence.
- **Validation timing and ownership.** On-change, on-blur, on-submit, or hybrid? Does the field own validation or just render the error it's handed? The field is split and the UX literature is opinionated (validate on blur, re-validate on change *after* the first error).
- **Placeholder semantics.** Everyone now agrees placeholder-as-label is an anti-pattern; not everyone's API makes the right thing the easy thing.
- **Controlled vs uncontrolled** and the React-specific traps around it.

## 2. Anatomy and parts

The converged anatomy is a labelled control plus associated satellite regions:

- **Label** — visible, persistent, associated via `<label for>`/`htmlFor` or wrapping. Not the placeholder. Required for every field; a visually-hidden label is the only acceptable "no visible label" case, and even then it must exist.
- **Required/optional indicator** — asterisk or "(optional)" text. The field is split on which to mark (see §7).
- **Input control** — the `<input>` itself. Owns `type`, `value`, `placeholder`, `autocomplete`, `inputmode`.
- **Prefix / suffix (addons / adornments)** — inline affixes inside or adjacent to the field: currency symbol, unit, search icon, password-reveal toggle, clear button. Named `prefix`/`suffix` (Polaris, Spectrum), `leadingVisual`/`trailingVisual` or `leadingAddon`/`trailingAddon` elsewhere. The trap: an *interactive* affix (reveal, clear) is a button that must be in the tab order and labelled; a *decorative* affix (currency glyph) must not steal focus and must not be the field's accessible name.
- **Helper / description text** — persistent guidance below the field, associated via `aria-describedby`.
- **Error / validation message** — replaces or supplements helper text on error, associated via `aria-describedby` (and the field marked `aria-invalid`), announced politely.
- **Character counter** — optional; the live-region wiring is contested (announce remaining count politely, but not on every keystroke).

Two structural models: **floating label** (label sits as placeholder, animates up on focus/fill — Material's signature) versus **static top-aligned label** (label always above the field). The field has largely converged *against* floating labels for accessibility and i18n reasons (label collides with placeholder, truncates under text expansion, and the empty-state reads as filled) — Material 3 still offers them; Polaris, Carbon, Primer, Spectrum default to static top labels.

## 3. Properties / API

**Converged core** (near-universal):

- `value` / `defaultValue` (controlled / uncontrolled).
- `onChange` (and `onBlur`, `onFocus`).
- `label` — string or node; required in practice.
- `type` — passthrough to the HTML input type (`text | email | url | tel | password | search | number`), with real semantic consequences for mobile keyboards and autofill.
- `placeholder` — example text only, never the label.
- `helpText` / `description` — persistent guidance.
- `error` / `errorMessage` / `invalid` — error state + message.
- `disabled` and `readOnly` — distinct (see §4).
- `required` — and the optional/required display convention.
- `autoComplete` — the WHATWG token (`email`, `name`, `current-password`, `one-time-code`, etc.).
- `id`/`name` — wiring and form submission.

**Divergences worth reasoning about:**

- **Bundled-props vs composed-children.** Polaris `<TextField label="" helpText="" error="">` bundles everything as props — terse, but the layout of label/helper/error is fixed and customising it means fighting the component. React Aria / Spectrum expose `<TextField>` composing `<Label>`, `<Input>`, `<Text slot="description">`, `<FieldError>` — verbose, but the consumer controls layout and the wiring is handled by context. The practice decision: bundle the common case as props *and* allow a composed escape hatch. Most consumers want `label`/`helpText`/`error` props; power users want the slots.
- **Validation ownership.** Three stances: (a) field is purely presentational, renders the `error` it's handed (Polaris, Primer — form library owns timing); (b) field integrates with native Constraint Validation API and surfaces `validationBehavior="native"` (React Aria/Spectrum — can hook `<form>` validation and `:invalid`); (c) field owns a `validate` prop. The practice default: presentational error rendering by default (the form library — React Hook Form, Formik, native Server Actions — owns timing), with optional native-constraint integration. Don't bake a validation engine into the field.
- **`prefix`/`suffix` as node vs structured addon.** A node slot is flexible but lets consumers drop interactive controls in without the field knowing they need tab-order/labelling. Some systems (Carbon) distinguish a passive prefix from an active "inline action." Recommendation: separate *adornment* (decorative/static, `aria-hidden` if purely visual) from *action* (a real labelled button slot).
- **Number input.** `<input type="number">` is a recurring trap: scroll-wheel changes values, `e`/`+`/`-` are accepted, locale decimal separators break, and screen-reader spinbutton semantics surprise. The field is moving toward `type="text" inputmode="numeric"` + formatting (React Aria's `NumberField` is a separate component for exactly this). Flag: prefer a dedicated NumberField over `type="number"` on TextField.
- **`clearable`** — a built-in clear button (common on search). Convenient; must be a labelled button ("Clear"), focusable, and announce the cleared state.

## 4. States and variants

**Runtime states** — Text Field is the component where the *full* generic state set actually applies (unlike Button):

| State | Notes / contract |
| --- | --- |
| rest | base |
| hover | subtle border shift; not sole carrier |
| focus-visible | `:focus-visible` ring, ≥3:1 (1.4.11, 2.4.13); the field is a primary focus target |
| disabled | native `disabled` — removed from tab order, not submitted, not validated; exempt from contrast |
| read-only | **distinct from disabled** — focusable, selectable/copyable, *submitted* with the form, `readonly` attribute; the most-confused TextField distinction |
| loading | async validation / async value (e.g. checking username) — spinner in suffix, `aria-busy`, don't block typing unless intended |
| error | `aria-invalid="true"` + `aria-describedby` → error message; not colour-only |
| empty | the placeholder/empty-label state — and the reason floating labels are risky (empty must not read as filled) |

**disabled vs read-only vs inactive** is to Text Field what the disabled debate is to Button: `disabled` removes from tab order and form submission and is silent to AT; `readOnly` keeps the value reachable, copyable, and submitted. Use `readOnly` for values the user may need to read/copy but not edit (a generated API key); reserve `disabled` for fields irrelevant in the current state — and consider the focusable pattern where the disabled reason matters.

**Intentional variants:** `size` (small/medium/large — medium default), density (compact/comfortable for data-dense forms), and a visual style axis some systems expose (outline vs filled vs underline — Material's filled/outlined; most others ship a single bordered style). The practice default is a single bordered style at three sizes; filled/underline are theming choices, not API variants.

## 5. Usage guidance

- **Use** for free-form, non-enumerable single-line input.
- **Don't use** when the value comes from a known set (→ Select/Radio/Combobox), spans multiple lines (→ Textarea), is boolean (→ Checkbox/Switch), is a date (→ Date Picker — though a masked text input is a legitimate fallback), or needs suggestions (→ Combobox).
- **Decision frameworks:**
  - **Label always visible.** The only acceptable label-less field is search with a visually-hidden label and a search icon affordance — and even then the label exists in the DOM.
  - **One input, one concept.** Don't pack "first last" or "MM/YY/CVC" into one field unless masking genuinely helps; multiple concepts → multiple fields.
  - **Helper text is persistent guidance, error is a state.** Don't put format hints only in the error; show them in helper text *before* the user fails.
  - **Optional vs required marking:** mark the minority. If most fields are required, mark "(optional)"; if most are optional, mark required. Be consistent within a form.

## 6. Accessibility

Theory is in 14 / 17 / 28; the Text-Field-specific contract:

- **Programmatic label association is the whole game.** `<label for=id>` or wrapping `<label>`. `placeholder` is *not* a label (disappears on input, fails 1.4.3 contrast as typically styled, and is not a reliable accessible name). `aria-label`/`aria-labelledby` only when a visible `<label>` genuinely can't be used.
- **Description and error wiring.** Helper text and error message associate via `aria-describedby` (the field can reference multiple ids). On error, set `aria-invalid="true"` and ensure the error id is in `aria-describedby`. The error message should be in a live region (or rendered such that the describedby update is announced) — but avoid announcing on every keystroke.
- **`autocomplete` is an accessibility feature, not just convenience** — WCAG 2.2 SC 1.3.5 Identify Input Purpose requires programmatically-determinable purpose for fields collecting user info; the WHATWG `autocomplete` token is how you satisfy it. This is a TextField-specific SC most components don't touch.
- **Required.** `required` + `aria-required` if not using native; don't rely on the asterisk alone (it's a visual-only cue unless the label text or `aria-required` carries it).
- **Error announcement timing** — validate on blur, re-validate on input after first error; announce the error politely; move focus to the first invalid field on submit (and to an error summary for long forms — see 28/the form pattern).
- **Touch target & spacing** — the input and any interactive affix (reveal/clear) meet target-size minimums (2.5.8); the reveal/clear buttons need accessible names.
- **WCAG SCs the field participates in:** 1.3.5 Identify Input Purpose, 3.3.1 Error Identification, 3.3.2 Labels or Instructions, 3.3.3 Error Suggestion, 1.4.11/2.4.13 (focus/border contrast), 4.1.2, 2.5.8, and 3.3.7 Redundant Entry / 3.3.8 Accessible Authentication (2.2) for login/repeat-entry fields.

## 7. Content guidelines

- **Label: noun or noun phrase, concise, sentence case.** "Email address," not "Enter your email address here."
- **Placeholder: an example, not an instruction or the label.** "name@example.com" — and accept that it vanishes on input, so nothing load-bearing lives there.
- **Helper text: the format/constraint up front.** "Use 8+ characters" shown before failure, not only in the error.
- **Error message: say what's wrong AND how to fix it** (3.3.3 Error Suggestion). "Enter a valid email address (e.g. name@example.com)," not "Invalid input." Be specific and human; don't blame.
- **Required/optional:** mark the minority consistently (§5).
- **Empty state** for a field is just the placeholder/label; there's no separate empty pattern beyond that.

## 8. Motion and transition

- **State transitions** (border colour on focus/error, helper→error swap) are short token-driven changes, ~100–150ms. The error appearance should not jank the layout — reserve space or animate height gently so the form doesn't jump.
- **Floating-label animation** (if used) is the one signature motion; under reduce-motion it should resolve to an instant position change, not a slide.
- **reduce-motion:** drop any non-essential transition; keep the instant colour/border state change (state must stay perceivable). Async-validation spinner is functional (announce via `aria-busy`), not decorative.

## 9. Internationalization

- **Labels and helper/error text expand** — never fix the field's label or message width; allow wrap. Field width is content-driven (an input for a postcode is narrower than one for a street address) — size to expected input, not to a uniform grid, and don't let i18n expansion truncate the label.
- **RTL:** the input mirrors — text alignment follows direction, prefix/suffix swap sides via logical properties. But **input *content* direction can differ from UI direction** (a phone number or Latin email typed into an Arabic UI) — set `dir="auto"` on the input or rely on the Unicode bidi algorithm so the value renders correctly regardless of UI direction. Currency/unit affixes follow locale placement (symbol before vs after the number).
- **Locale input concerns:** decimal/grouping separators (the number trap, §3), date/phone formats (prefer locale-aware components or masks), and IME composition — don't fire validation mid-composition (the `compositionstart`/`compositionend` events matter for CJK input).

## 10. Naming

- **Component name** splits: `TextField` (Spectrum, Material, MUI), `TextInput` (Carbon, Primer historically, Polaris uses `TextField`), `Input` (Base Web, shadcn). Practice default: **`TextField`** as the labelled composite (label + input + helper + error), with **`Input`** reserved for the bare control if we ship a headless one.
- **Prop aliases consumers reach for:** `helpText`/`helperText`/`description` → one canonical (`helpText`); `error`/`errorText`/`invalid`/`errorMessage` → canonical (`error` for message, `invalid` boolean if needed); `prefix`/`suffix` vs `leading*`/`trailing*`; `clearable`; `readOnly`/`readonly`. Document the mapping.
- Specializations are their own components, not props: `NumberField`, `SearchField`, `PasswordField` (or a `type`+`clearable`/reveal composition) — name the contested ones explicitly so consumers don't reach for `type="number"` on the base.

## 11. Implementation notes

- **Controlled vs uncontrolled.** Support both; the React trap is a controlled input with `value` but no `onChange` (read-only-by-accident) or value/`undefined` flips that switch the input between controlled and uncontrolled mid-life. Default to uncontrolled with `defaultValue` for form-library ergonomics; support controlled for live formatting.
- **`id` generation and wiring.** The component must generate stable ids (React `useId`) to wire `label[for]`, `aria-describedby` (helper + error), and `aria-errormessage`/`aria-invalid` without the consumer hand-managing ids. Getting this wiring wrong is the most common real a11y failure in shipped fields.
- **Native form & Server Actions.** Emit a real `<input name>` so the field works in an uncontrolled `<form>`, with `useFormStatus`/Server Actions, and with the Constraint Validation API. A field that only works controlled is a liability in 2026 form architectures.
- **Don't use `type="number"`** for general numeric input (§3); prefer `inputmode="numeric"`/`decimal` + formatting or a dedicated NumberField.
- **Composition vs bundle (the headless tension).** React Aria / Radix expose the wiring as hooks/primitives and let you own markup; Polaris/Carbon bundle. Ship the bundle for the 90% case, expose the composed slots for the 10%. The wiring (ids, aria-describedby, invalid) is the part that must be correct regardless.
- **Autofill styling.** Browser autofill applies UA styles (`:-webkit-autofill`) that fight token theming; handle it explicitly or the filled state looks broken.

## 12. Related and alternative components

- **Composes with:** Label, Helper/Description text, FieldError, Icon (prefix/suffix), Button (clear/reveal action), Form (the composite owner), Tooltip (optional inline help — not as the only carrier of essential info).
- **Alternative to:** Textarea (multi-line), Select/Combobox (enumerable / suggested values), NumberField (numeric), SearchField (search + clear), Date Picker (dates), PasswordField (reveal), Checkbox/Switch (boolean).
- **Supersedes:** bare `<input>` without label wiring; the placeholder-as-label pattern; `type="number"` for formatted numeric input.
- **Superseded by:** nothing for free-form single-line text; specific uses migrate to the specialized siblings above.

## 13. Field POV evolution

- **Floating labels out of favour.** The field has largely moved to static top-aligned labels for accessibility, i18n, and density reasons; Material 3 retains floating as an option but it is no longer the assumed default elsewhere.
- **Placeholder-as-label is now universally an anti-pattern** — settled, but legacy code persists.
- **Validation timing consensus** converging on "validate on blur, re-validate on change after first error, focus first invalid on submit, error summary for long forms."
- **`type="number"` retreat** toward `inputmode` + dedicated NumberField.
- **`autocomplete` as a 1.3.5 obligation** (WCAG 2.2) and 2.2's new auth-related SCs (3.3.7 Redundant Entry, 3.3.8 Accessible Authentication) raising the bar on login/checkout fields specifically.
- **Composition/headless** (React Aria, Radix, Base UI, shadcn) shifting the field from a bundled black box toward a wired-but-unstyled primitive with an opinionated skin on top.

> Verification path: React Aria TextField/NumberField/SearchField (react-spectrum.adobe.com), Polaris TextField (polaris.shopify.com), Carbon TextInput (carbondesignsystem.com), Primer TextInput/FormControl (primer.style), Material 3 text fields (m3.material.io), WCAG 2.2 SC 1.3.5/3.3.x (w3.org/TR/WCAG22). Re-confirm versions at synthesis.

## 14. Sources cited

- Adobe Spectrum / React Aria — TextField, NumberField, SearchField, Field composition, native Constraint Validation integration (2024–2025).
- Shopify Polaris — TextField (bundled label/helpText/error, prefix/suffix, clearable) (2024–2025).
- IBM Carbon — TextInput, passive vs active prefix (2024).
- GitHub Primer — TextInput / FormControl wiring (2024).
- Google Material 3 — filled/outlined text fields, floating labels (2024).
- Atlassian Design System — Textfield / Form field (2024).
- Base Web (Uber) — Input + overrides (2024).
- Apple HIG / Microsoft Fluent 2 — text field labelling, mobile keyboards (2024).
- WCAG 2.2 (W3C, Oct 2023) — SC 1.3.5, 3.3.1, 3.3.2, 3.3.3, 3.3.7, 3.3.8, 1.4.11, 2.4.13, 2.5.8, 4.1.2.

## 15. Agent-consumable schema

```yaml
identity:
  id: text-field
  name: TextField
  aliases: [text-input, input]
  category: form
  status: stable
description: >
  Single-line control for free-form, non-enumerable text. Composite of
  label + input + helper + error. Not multi-line (textarea), not a known
  set (select/combobox), not numeric-formatted (number-field).
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
      description: Uncontrolled initial value (preferred for form libs).
    - name: onChange
      type: function
      required: false
    - name: type
      type: enum
      values: [text, email, url, tel, password, search]
      default: text
      required: false
      description: Passthrough; drives mobile keyboard + autofill. Use a
        dedicated number-field instead of type=number.
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
        and how to fix (SC 3.3.3).
    - name: required
      type: boolean
      default: false
      required: false
      description: Sets required/aria-required; mark the minority in a form.
    - name: disabled
      type: boolean
      default: false
      required: false
      description: Removes from tab order + submission; silent to AT.
    - name: readOnly
      type: boolean
      default: false
      required: false
      description: Focusable, copyable, SUBMITTED; distinct from disabled.
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
      description: May hold a labelled action (clear/reveal) — that is a
        real focusable button, not decoration.
    - name: clearable
      type: boolean
      default: false
      required: false
      description: Adds a labelled Clear button; announces cleared state.
    - name: size
      type: enum
      values: [small, medium, large]
      default: medium
      required: false
composition:
  composes-with: [label, helper-text, field-error, icon, button, form, tooltip]
  alternative-to: [textarea, select, combobox, number-field, search-field, date-picker, password-field, checkbox, switch]
  supersedes: ["bare input without label wiring", "placeholder-as-label", "type=number for formatted numeric"]
  superseded-by: null
accessibility:
  wcag-criteria: ["1.3.5", "3.3.1", "3.3.2", "3.3.3", "3.3.7", "3.3.8", "1.4.11", "2.4.13", "2.5.8", "4.1.2"]
  aria-attributes:
    - aria-invalid        # on error
    - aria-describedby    # helper + error ids
    - aria-required       # when not native required
    - aria-label          # only when no visible <label> possible
  label-association: "native <label for>/wrapping; placeholder is NOT a label"
  keyboard-model:
    typing: native text editing
    tab: focuses input; interactive affixes are separate tab stops
  focus-behavior:
    focus-visible: required        # ring + border >=3:1 (1.4.11/2.4.13)
    error-focus: move-to-first-invalid-on-submit
states:
  runtime: [rest, hover, focus-visible, disabled, read-only, loading, error, empty]
  notes:
    read-only-vs-disabled: "readOnly submits + is copyable; disabled does neither and is silent to AT"
variants:
  size: [small, medium, large]
  density: [comfortable, compact]
  style: [bordered]               # filled/underline are theming, not API
content:
  label-pattern: "noun phrase, sentence case, concise; never the placeholder"
  placeholder-pattern: "example value only; nothing load-bearing"
  helper-pattern: "format/constraint shown before failure"
  error-pattern: "what is wrong AND how to fix (SC 3.3.3); not colour-only; not 'Invalid input'"
  empty-pattern: "label + optional placeholder; no separate empty UI"
notes:
  contested:
    - bundled-props vs composed-children (ship both: props for 90%, slots for 10%)
    - validation ownership/timing (default presentational; form lib owns timing)
    - floating vs static label (static default; floating is a Material option)
    - type=number trap -> prefer inputmode + number-field
    - prefix/suffix: adornment vs action distinction
```
