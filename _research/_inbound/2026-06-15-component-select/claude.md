# Select — field-truth study (Claude pass)

## 1. Framing

Select is the component where the field's accessibility ideals collide hardest with its styling ambitions. Like Textarea, it inherits the Text Field substrate (label/helper/error, the describedby chain, read-only-vs-disabled — see text-field); unlike Textarea, its *core* is contested at the platform level: **native `<select>` vs. a custom ARIA-listbox**. That one decision cascades into every other section.

What a Select *is*: a control for choosing one (or several) values from a **known, enumerable set the user does not type**. What it *isn't*: free-form text (Text Field/Textarea), a small mutually-exclusive set better shown inline (Radio/Segmented Control), a boolean (Checkbox/Switch), or — the load-bearing boundary — **a set the user filters by typing, which is a Combobox**. The select-vs-combobox confusion is the single most common adjacency error: the moment a text input filters the options, you are in ARIA combobox territory with a different role, keyboard model, and announcement contract. Bolting a filter field onto a listbox without changing the ARIA is how teams ship a broken combobox (the mirror of text-field's text-field-vs-combobox trap).

Why systems disagree:

- **Native vs. custom is a genuine trade, not a settled win.** Native `<select>` is accessible by construction, gets the OS picker free on mobile (the single best mobile select UX), and is keyboard-complete — but is nearly unstylable (the option list especially) and can't hold rich option content (icons, descriptions, two-line options). A custom listbox styles fully and holds rich content — but you now own the entire focus/keyboard/announcement contract, and most custom selects ship subtly broken. The field has *not* converged; it has converged on a *decision framework* (§5).
- **How much to split the family.** Single-select listbox, multi-select, and the searchable variant (combobox) — one component with props, or separate components?
- **The positioning model** — Floating UI / Popper today, migrating toward the CSS Anchor Positioning + Popover API.

## 2. Anatomy and parts

Inherits the Text Field field-row anatomy (label, required indicator, helper, error, describedby wiring) — not repeated. Select-specific parts:

- **Trigger** — the button-like control showing the current value (or placeholder) and a disclosure caret. For native, this *is* the `<select>`; for custom, it's a `<button>` with `aria-haspopup="listbox"`/`aria-expanded`. The accessible name comes from the associated label, not the placeholder.
- **Value display** — the selected option's label rendered in the trigger; for multi-select, a count summary ("3 selected") or token/tag row.
- **Listbox popover** — the floating surface (`role="listbox"`), positioned against the trigger, with collision handling and scroll.
- **Option** (`role="option"`) — owns `aria-selected`, may carry a leading icon, a description line, or a trailing checkmark/checkbox.
- **Option group** (`role="group"` + `optgroup`/labelled heading) — sectioning with a non-selectable group label.
- **Placeholder / empty state** — the no-selection state in the trigger, and the no-options/loading state inside the listbox.
- **Multi-select extras** — per-option checkboxes, a select-all, a clear, and the token row.

## 3. Properties / API

Inherits the Text Field core (`label`, `value`/`defaultValue`, `onChange`, `helpText`, `error`, `disabled`, `readOnly`, `required`, `name`, `id`, `size`) — see text-field §3. Select-specific:

- **`options` (data) vs. `<Option>` children (composition)** — the field splits between a data-driven `options={[{label, value}]}` prop and composed `<Select.Option>` children. Data-driven is terse and serializable (good for the `.ai.json` story); composition holds rich option content cleanly. The practice ships **both**: `options` for the common flat case, composed children for icons/descriptions/groups.
- **`value`/`onChange` typing** — single-select is a scalar; multi-select is an array. Keep them distinct rather than overloading one prop with mode-dependent types.
- **`multiple`** — the single-vs-multi switch. Multi-select needs a selection-summary model (count vs. tokens) and a `select-all`.
- **`placeholder`** — the no-selection prompt. Subtle trap (native): a placeholder `<option value="">` must be present-but-disabled-after-selection, and it is *not* the label.
- **`native`** — the practice exposes the native-vs-custom choice as an explicit prop (or two components, §10), defaulting to native on touch and custom on pointer where rich content is needed (§5).
- **`searchable`** — the boundary prop: setting it makes the component a **Combobox**, not a styled Select. The practice does *not* bolt a `searchable` onto Select; it routes to the Combobox component (§12).
- **`loading`** — async option loading; the listbox shows a spinner/skeleton, not an empty state.
- **`clearable`** — a labelled clear affordance, returning focus to the trigger (the same focus-return discipline as text-field's clearable).

## 4. States and variants

Inherits Text Field runtime states (rest/hover/focus-visible/disabled/read-only/loading/error/empty — see text-field §4). Select-specific:

| State | Select-specific contract |
| --- | --- |
| expanded | trigger `aria-expanded="true"`; listbox open, active option tracked via `aria-activedescendant` (or roving focus) |
| empty (no selection) | placeholder shown in trigger; distinct from the empty *listbox* (no options) state |
| loading | listbox shows spinner/skeleton; trigger may show `aria-busy` |
| read-only | renders the value, not interactive; for native, `disabled` is the only lever — so a custom control is needed for a true submitted-but-not-editable select |
| error | `aria-invalid` on the trigger; the describedby chain carries the message |

**Intentional variants:** `size` and density carry over; the single bordered/outline style is the default. The Select-specific variant axis is **single vs. multi** (and the multi summary style: count vs. tokens).

## 5. Usage guidance

- **Use** for choosing from a known, enumerable set the user doesn't type — country, status, category, assignee from a fixed roster.
- **Don't use** for: ≤~5 mutually-exclusive options where the choices fit inline (→ Radio / Segmented Control — a select hides options behind a click), a set the user filters by typing (→ Combobox), boolean (→ Switch/Checkbox), or very large/remote sets needing search (→ Combobox with async).
- **Native-vs-custom decision framework:**
  - **Native `<select>` when:** mobile/touch is primary (the OS picker is unbeatable), options are plain text, and you don't need rich content. Default to native.
  - **Custom listbox when:** options need icons/descriptions/two-line content, multi-select with tokens is required, or the trigger needs bespoke styling the platform can't deliver — *and* you accept ownership of the full a11y contract.
- **Multi-select model:** tokens/tags when selections are few and identity matters; a count summary ("3 selected") when many; always offer select-all/clear for long lists.
- **Mobile:** prefer native; if custom, the listbox should become a full-screen or bottom-sheet picker, not a cramped popover.

## 6. Accessibility

Shared substrate (label association, describedby, error wiring, focus contrast) is in text-field §6. Select-specific:

- **Native `<select>` is the accessibility baseline** — role, keyboard, typeahead, and AT announcements are free and correct. Every custom listbox is measured against it.
- **The custom-listbox ARIA contract** (APG Listbox pattern): trigger `role="button"` (or `combobox` if it's actually searchable) with `aria-haspopup="listbox"`, `aria-expanded`, `aria-controls`; listbox `role="listbox"` with `aria-multiselectable` when multi; options `role="option"` with `aria-selected`. Track the active option with **`aria-activedescendant`** (focus stays on the trigger/input) — the more robust pattern than roving tabindex for selects.
- **Keyboard model:** Enter/Space/Down opens; Up/Down move the active option; Home/End jump; typeahead selects by typed prefix; Enter/Space selects; Escape closes and returns focus to the trigger; Tab closes and commits. Type-to-select is expected, not optional.
- **Focus return** — on close, focus must return to the trigger; on select in single mode, close and return; the focus-lost-to-body bug is the most common custom-select failure.
- **Announcements:** the selected value and the listbox's option count/position should be announced; multi-select selection changes announced politely.
- **WCAG SCs:** the Text Field set (1.3.5 where the select collects identifiable info, 3.3.1/3.3.2/3.3.3, 1.4.11/2.4.13, 4.1.2) plus **4.1.2 Name/Role/Value** doing heavy lifting on the custom roles, and 2.5.8 target size on the trigger and options.

## 7. Content guidelines

- **Label:** noun phrase, sentence case (shared with text-field).
- **Placeholder option:** "Select a country" — a prompt, not the label, and not a real value.
- **Option labels:** parallel, concise, scannable; sort meaningfully (alphabetical, frequency, or logical) — not by data-insertion order.
- **Empty listbox copy:** "No options" / "No matches" (the latter only in combobox); **loading** is a spinner, not empty copy.
- **Multi-select summary:** "3 selected" or tokens; error copy follows SC 3.3.3.

## 8. Motion and transition

The listbox entry/exit is the signature motion — a short (~100–150ms) fade+scale or slide from the trigger edge, origin-anchored to the trigger. Honor `prefers-reduced-motion` by dropping the transform and keeping an instant or opacity-only change. Don't animate option list height on filter (combobox) — it lags. State transitions follow text-field's token-driven timing.

## 9. Internationalization

Inherits text-field i18n (logical-property RTL, expansion, IME). Select-specific: the caret and any leading option icons mirror in RTL; option label text expansion can blow out the trigger width — truncate the *trigger* value with a tooltip/title, never the options in the list; sort order is locale-aware (collation differs by language); and the native picker localizes for free (an argument for native in heavily-localized products).

## 10. Naming

`Select` is near-universal (Polaris, Spectrum, Carbon, Base Web, Atlassian); Material calls the custom one a "menu"/exposed dropdown; some systems split `Select` (native) from `Listbox`/`Combobox` (custom). Practice default: **`Select`** for the component (native or custom behind one API or a `native` prop), reserving **`Combobox`** for the searchable sibling and **`Listbox`** for a bare headless primitive if exposed. Aliases: `Dropdown`, `Picker`, `MenuSelect`.

## 11. Implementation notes

- **Don't reinvent the listbox** — use a headless primitive (React Aria `useSelect`/`useListBox`, Downshift, Radix Select) for the focus/keyboard/ARIA contract; skin it. Hand-rolled selects are the highest-bug-density form control.
- **Positioning:** Floating UI today (collision flip/shift, `size` middleware to cap listbox height to the viewport); migrating toward CSS Anchor Positioning + the Popover API (`popover` attr for top-layer rendering, no z-index wars) — flag as emerging, verify support.
- **Top-layer rendering** avoids `overflow: hidden`/z-index clipping — render the listbox in the top layer (Popover API) or a portal.
- **Long lists:** virtualize beyond a few hundred options, but virtualization fights `aria-activedescendant` (the active option must be in the DOM) and typeahead — or, better, if the list is long enough to need virtualization, it probably wants **search → Combobox**.
- **Native styling:** `appearance: none` + custom caret gets you a styled *trigger* but not styled *options* — the hard wall that pushes teams to custom.
- **Forms:** emit a real value for native `<form>`/Server Actions; a custom listbox needs a hidden `<input>`/`<select>` mirror to participate in form submission.

## 12. Related and alternative components

- **Composes with:** Label, Helper/FieldError, Option, OptionGroup, Icon (option/trigger), Checkbox (multi-select options), Tag/Token (multi summary), Popover/Listbox (the surface), Form.
- **Alternative to:** Combobox (searchable/typeahead), Radio/Segmented Control (small inline sets), Menu (actions, not value selection — the select-vs-menu boundary: a menu performs commands, a select sets a form value), Switch/Checkbox (boolean), Autocomplete.
- **Supersedes:** a bare unstyled `<select>` without label wiring; a Menu misused to pick a form value.
- **Superseded by:** Combobox when the set grows large enough to need filtering.

(See text-field and textarea for the shared substrate, 03-component-library for the model, 29 for the docs template.)

## 13. Field POV evolution

1. **Native-first resurgence on mobile** — the OS picker's UX has pulled systems back toward native `<select>` where content allows.
2. **The Popover API + CSS Anchor Positioning** are reshaping the positioning/top-layer story, retiring portal+z-index hacks.
3. **`selectmenu`/customizable-select** (the long-promised stylable native select, `appearance: base-select`) is the edge to watch — it would collapse the native-vs-custom trade entirely; verify spec/support status before relying on it.
4. **The select-vs-combobox split is hardening** — searchable is increasingly its own component, not a Select prop.
5. **Multi-select tokenization** converging on the tag-row + count-summary hybrid.

## 14. Sources cited

(Conservative; reconcile with external pass.) Polaris `Select` (native-leaning) (2024–2025); Spectrum/React Aria `Select`/`Picker`, `ListBox`, `ComboBox`, `useSelect` (2024–2025); Material 3 exposed dropdown menu (2024); Carbon `Select`/`Dropdown`/`MultiSelect` (2024); Primer `Select`/`SelectPanel`, `ActionMenu` boundary (2024); Atlassian `Select` (react-select lineage) (2024); Base Web `Select` (2024); Fluent `Dropdown`/`Combobox` (2024); Apple HIG pickers / Material Compose (2024); WAI-ARIA APG Listbox & Combobox patterns; WCAG 2.2 (Oct 2023) — 1.3.5, 3.3.1/2/3, 1.4.11, 2.4.13, 4.1.2, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: select
  name: Select
  aliases: [dropdown, picker, menu-select, listbox]
  category: form
  status: stable
description: >
  Control for choosing one or several values from a known, enumerable
  set the user does NOT type. Native <select> or custom ARIA listbox.
  Not free-form (text-field), not filtered-by-typing (combobox), not a
  small inline set (radio/segmented), not commands (menu).
api:
  inherits: text-field   # label, value/defaultValue, onChange, helpText, error, disabled, readOnly, required, name, id, size, clearable
  props:
    - name: options
      type: array<{label,value,disabled?,icon?,description?,group?}>
      required: false
      description: Data-driven options (flat case). Alternative to composed <Option> children.
    - name: multiple
      type: boolean
      default: false
      description: Multi-select; value becomes an array; needs summary model + select-all.
    - name: native
      type: boolean
      description: Native <select> vs custom listbox. Default native on touch / plain text.
    - name: placeholder
      type: string
      description: No-selection prompt; not the label, not a real value.
    - name: loading
      type: boolean
      default: false
      description: Async options; listbox shows spinner, not empty copy.
    - name: searchable
      type: boolean
      deprecated: true
      description: DO NOT use — searchable = Combobox, a separate component.
composition:
  composes-with: [label, helper-text, field-error, option, option-group, icon, checkbox, tag, popover, form]
  alternative-to: [combobox, radio, segmented-control, menu, switch, checkbox]
  supersedes: ["bare unstyled <select> without label wiring", "menu misused to set a form value"]
  superseded-by: ["combobox when the set needs filtering"]
accessibility:
  inherits: text-field
  pattern: "APG Listbox (custom) | native <select> baseline"
  wcag-criteria: ["1.3.5", "3.3.1", "3.3.2", "3.3.3", "1.4.11", "2.4.13", "4.1.2", "2.5.8"]
  aria-attributes:
    - aria-haspopup=listbox
    - aria-expanded
    - aria-controls
    - role=listbox
    - role=option / aria-selected
    - aria-multiselectable   # multi
    - aria-activedescendant  # active option; focus stays on trigger
    - aria-invalid
  keyboard-model:
    open: Enter/Space/ArrowDown
    move: ArrowUp/Down, Home/End, typeahead-by-prefix
    select: Enter/Space
    close: Escape (return focus to trigger), Tab (commit)
  focus-behavior:
    active-option: aria-activedescendant (not roving)
    on-close: focus returns to trigger
states:
  inherits: text-field   # rest, hover, focus-visible, disabled, read-only, loading, error, empty
  select-specific: [expanded, no-selection, empty-listbox, loading-listbox]
variants:
  size: [small, medium, large]
  selection: [single, multiple]
  multi-summary: [count, tokens]
  rendering: [native, custom]
content:
  label-pattern: "noun phrase, sentence case (shared with text-field)"
  placeholder-pattern: "'Select a X' prompt; not the label, not a value"
  option-pattern: "parallel, concise; sorted meaningfully + locale-aware, not insertion order"
  empty-pattern: "'No options'; loading is a spinner not empty copy"
  error-pattern: "what + how to fix (SC 3.3.3); aria-invalid on trigger"
notes:
  contested:
    - native vs custom (decision framework, not a winner)
    - options-data vs composed-children (ship both)
    - select vs combobox (searchable routes to combobox)
  emerging:
    - "Popover API + CSS Anchor Positioning retiring portal/z-index"
    - "customizable-select (appearance: base-select) could collapse the native-vs-custom trade — verify support"
```
