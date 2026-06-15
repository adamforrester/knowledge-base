# Combobox — field-truth study (Claude pass)

## 1. Framing

Combobox is the component the field openly calls the hardest widget in ARIA, and it earns the title by standing on *two* substrates at once: the Text Field form-field stack (label/helper/error, describedby — see text-field) **and** Select's overlay/listbox/positioning machinery (the `aria-activedescendant` focus contract, popover positioning, virtualization — see select). It re-derives neither; what is genuinely its own is the **destructive filter**.

What a Combobox *is*: a **text input that filters a listbox as the user types**. That one fact is the whole boundary. What it *isn't*: a Select (a *button* trigger with non-destructive type-ahead — see select §1, the boundary drawn from the other side), a plain Text Field, or a Search Field (a text-field specialisation that submits a query rather than resolving to a value from a set). The recurring confusion is the inverse of Select's: teams bolt a filter onto a listbox and ship an ARIA-broken "select", or add a dropdown to a search box and ship a combobox without the `role`/`aria-autocomplete` contract.

Why systems disagree:

- **Autocomplete model** — none / list / inline / both (the `aria-autocomplete` values). Inline completion (auto-filling and selecting the predicted remainder) is powerful and a known accessibility/UX trap.
- **Free-text vs. strict** — may the value be arbitrary text, or must it resolve to an option? This is the line between an autocomplete-over-a-known-set and a creatable/tags input.
- **Who owns the filter** — the component (built-in substring match) or the consumer (especially for async/remote).
- **Single vs. multi (token input)** — the multi-combobox is its own contested sub-pattern.

## 2. Anatomy and parts

Inherits the Text Field field row (label, helper, error, describedby) and Select's overlay (listbox, option, option-group, popover) — not repeated (see text-field §2, select §2). Combobox-specific:

- **Editable input** — the trigger is a real `<input role="combobox">`, not a button. Owns `aria-expanded`, `aria-controls`, `aria-autocomplete`, and `aria-activedescendant`.
- **Disclosure/trigger button** — an optional caret that opens the full list without typing (turning the combobox into a select-like browse); a real button, `aria-hidden` from the input's name.
- **Clear button** — resets the query/value, returns focus to the input.
- **Filtered listbox** — the same listbox, but its option set is a *function of the query*; carries the empty/no-results/loading states inside it.
- **Match highlight** — the matched substring emphasised within each option (presentation only, never the accessible name).
- **Token row** (multi) — selected values as removable chips, usually before or within the input.

## 3. Properties / API

Inherits the Text Field core and Select's option model (`options`/composed children, `value`, `loading`, `clearable`, `multiple`, size — see text-field §3, select §3). Combobox-specific:

- **`inputValue` / `onInputValueChange`** — the *text in the field*, distinct from `value` (the *selected option*). The defining Combobox API fact: it has **two states** — the query string and the resolved selection — and conflating them is the single most common bug (the controlled-value trap, §11). React Aria models this split explicitly.
- **`aria-autocomplete` / `autocompleteMode`** — `none | list | inline | both`. The practice default is **`list`** (typing filters, no surprise text insertion); `inline`/`both` (auto-completing the remainder) is opt-in only, because auto-inserted-and-selected text fights deletion and confuses screen readers (§6).
- **`allowsCustomValue` (free-text) vs. strict** — strict (must resolve to an option) is the default for data integrity; free-text is opt-in and shades into the creatable/tags boundary (§12).
- **filtering** — a built-in default matcher (case- and diacritic-insensitive substring) with a `filter`/`onFilter` override; for **async**, the consumer owns filtering and the component just renders, debounces input, and surfaces loading/empty (§11).
- **`onInputChange` debounce + async contract** — minimum-query-length, debounce, **cancel stale requests** (race conditions are the classic async-combobox bug), and distinct loading / no-results / type-more / error states.
- **`menuTrigger`** — `input | focus | manual`: does the list open on focus, on first keystroke, or only via the caret? (Spectrum exposes exactly this.)
- **selection reconciliation** — on blur with strict mode, restore the last valid value (don't strand half-typed text as the value); on clear, reset both states.

## 4. States and variants

Inherits Text Field states and Select's expanded/option/loading-listbox states (see select §4). Combobox-specific:

| State | Combobox-specific contract |
| --- | --- |
| filtering | the open list reflects the current query; the active option resets sensibly as results change |
| no-results | "No results for '<query>'" inside the listbox — distinct from the empty (no-query) state |
| type-more / min-query | async with a minimum query length: "Type 2+ characters" before firing |
| loading | async fetch in flight: spinner in the listbox/input, `aria-busy`; don't clear the field |
| inline-completion (if enabled) | the predicted remainder is selected text the next keystroke replaces — must not block backspacing |

**Variants:** size/density inherited; the genuine Combobox axes are **autocomplete mode** (`none/list/inline/both`), **strict vs. free-text**, **single vs. multi (token)**, and **filtered vs. async**.

## 5. Usage guidance

- **Use** when the set is **large enough that scrolling/scanning is painful (~>15 options)**, or **remote/unbounded**, and the user can name what they want — country pickers, user/assignee search, tag selection, address autocomplete.
- **Don't use** for: a **small known set** (→ Select, or Radio if ≤~5), a value the user **doesn't type** (→ Select), a **search that submits a query** rather than resolving to a value (→ Search Field), or **commands** (→ Menu).
- **Decision frameworks:**
  - **Combobox vs. Select** is the filtering line: will the user type to narrow? Yes → Combobox. No → Select (see select §1, §5).
  - **Strict vs. free-text:** strict when the value must be a real entity (a user id); free-text when arbitrary input is valid (a tag, a free address line) — and free-text multi *is* a tags input (§12).
  - **`list` autocomplete by default;** reserve `inline`/`both` for high-confidence, low-ambiguity completions (a known command palette), never for open-ended search.
  - **Mobile:** the same input + listbox, but the listbox should expand to a full-screen/sheet surface (inherited from select §5); the OS keyboard is the input method, so set the right `inputmode`/`enterkeyhint`.

## 6. Accessibility

Inherits the Text Field substrate (label, describedby, error) and Select's `aria-activedescendant` focus contract — DOM focus stays on the **input**, the active option is tracked virtually (see select §6). Combobox-specific:

- **The ARIA 1.2 combobox pattern** (the current correct one; ARIA 1.0's was abandoned): `role="combobox"` on the **input** itself (not a wrapper), with `aria-expanded`, `aria-controls` → the listbox id, and **`aria-autocomplete`** (`list`/`inline`/`both`) declaring the behaviour. The popup is `role="listbox"`; options `role="option"`. This is the pattern that recently changed — verify against APG, and *do not* ship the deprecated 1.0 pattern (`role` on a wrapper) still found in old code.
- **`aria-activedescendant`, never moved DOM focus** — focus stays in the input so the user keeps typing while arrowing the list; moving focus into the listbox breaks typing (select §6, sharpened here because typing is the primary interaction).
- **Announce the result count and changes** — when filtering changes the list, a polite live region announces "N results" so a screen-reader user knows typing did something; silence reads as a broken field.
- **Inline completion is an a11y minefield** — auto-selected completion text must be deletable (backspace removes the suggestion, doesn't re-trigger it), and the autocompletion must be announced; this is why `list` is the safe default.
- **Keyboard model:** typing filters; Down/Up move the active option (Down opens if closed); Enter selects the active option; Escape first clears the query / closes, then clears the value; Tab commits (strict: to the active or last-valid; free-text: to the typed value); Home/End within the text. Backspace edits the query, never silently mutates the selection.
- **WCAG SCs:** the Text Field set (1.3.5, 3.3.1/2/3, 1.4.11, 4.1.2, 2.5.8) plus **4.1.3 Status Messages** (the results-count / loading live region) and **1.4.13** (the popup dismissible/hoverable, inherited from select). The whole pattern leans hardest on **4.1.2 Name/Role/Value**.

## 7. Content guidelines

- **Label/placeholder** inherited (label is a noun phrase; placeholder is an example like "Search countries", never the label).
- **Empty vs. no-results vs. type-more:** three distinct messages — nothing typed (show recents or top options, or nothing), "No results for 'X'", and "Type 2+ characters". Don't show "No results" before the user has typed the minimum.
- **Match highlight** aids scanning but is presentational; the option's accessible name stays the full label.
- **Free-text affordance:** if custom values are allowed, signal it ("Add '<query>'" as the create row).
- Error copy follows SC 3.3.3, delegated to the substrate.

## 8. Motion and transition

Inherits Select's listbox enter/exit (~100–150ms, faster exit, reduce-motion drops transform — see select §8). Combobox-specific: the list **re-renders on every keystroke**, so do *not* animate option insertion/removal during filtering — it lags behind typing and thrashes; the open/close transition animates, the filter update is instant. Match-highlight changes are instant, not transitioned.

## 9. Internationalization

Inherits Text Field i18n (logical-property RTL, expansion, IME) and Select's listbox mirroring (see select §9). Combobox-specific:

- **The filter matcher must normalize diacritics and case** (`Intl`/`localeCompare` with sensitivity) so typing "osterr" matches "Österreich" — the same point as Select's type-ahead, but load-bearing here because filtering *is* the interaction.
- **IME composition is critical** — for CJK input, do **not** filter on intermediate composition keystrokes; filter on `compositionend`, or the list thrashes mid-composition (text-field §9, sharpened).
- **Locale-aware sort/collation** of results; RTL mirrors the input, caret, and token row.

## 10. Naming

**`Combobox`** is the field and ARIA-spec default (Spectrum/React Aria, Fluent, the ARIA pattern itself), with `Autocomplete` (MUI), `ComboBox` (Carbon), and `Autosuggest` as the common aliases. **The practice default is `Combobox`** — it matches the ARIA role and the select sibling's naming logic. The multi/token variant is often a separately-named **`TagInput` / `TokenInput` / `MultiCombobox`** (§12). Aliases to map: `Autocomplete`, `Autosuggest`, `TypeAhead`, `SearchSelect`.

## 11. Implementation notes

- **Don't hand-roll** — use a headless primitive (React Aria `useComboBox`, Downshift, Radix) for the input/listbox/`activedescendant` contract; it is even more failure-prone than Select. Skin it.
- **The two-state model is the core trap.** `inputValue` (text) and `value` (selection) are distinct; a controlled combobox must manage both, reconcile them on selection/blur/clear, and not fight the user's typing. The classic bug: binding the input to `value` so selecting an option can't be re-edited, or so typing mutates the committed value.
- **Async race conditions** — debounce input, and **cancel or ignore stale responses** (AbortController / request-id guard) so an earlier slow query can't overwrite a later one. Surface min-query, loading, no-results, and error as distinct states.
- **Filtering ownership** — built-in matcher for local data; for remote, the component must *not* also filter the returned set (double-filtering hides server results). Make local-vs-async an explicit mode.
- **Inherited machinery** — positioning (Floating UI → CSS Anchor Positioning + Popover API), top-layer rendering, virtualization for long/remote lists, and the hidden form-mirror for submission all carry over from select §11.
- **Form value** — emit the resolved `value` (not the query) for native forms/Server Actions.

## 12. Related and alternative components

- **Composes with:** Text Field substrate, Listbox/Option/Popover (the surface), Icon (search/caret/clear), Tag/Token (multi), Spinner (async), Form.
- **Alternative to:** Select (no typing/filtering), Search Field (submits a query vs. resolves to a value), Menu (commands), Radio (tiny sets).
- **Supersedes:** a Select with a bolted-on filter that lacks the combobox ARIA; an autocomplete hand-rolled on a bare `<input>`.
- **Superseded by / specialises into:** **TagInput/TokenInput** (free-text multi), **Command palette** (combobox over actions), **address/predictive-search** patterns.

(See text-field and select for the two inherited substrates; 03-component-library; 29 for the docs template. Search Field, when briefed, draws the query-vs-value boundary from its side.)

## 13. Field POV evolution

1. **ARIA 1.0 → 1.2 combobox pattern** — the `role` moved onto the input and the dual-listbox hack was abandoned; shipped code still carries the old pattern, so this is an active correctness migration.
2. **The two-state (`inputValue` vs `value`) split** is now explicit in mature libraries (React Aria) rather than an implicit footgun.
3. **Async-first** — comboboxes are increasingly remote/predictive (search-as-you-type backends), pushing debounce/cancel/loading into the core contract.
4. **Platform shift inherited from select** — Popover API + CSS Anchor Positioning; and the emerging question of whether `appearance: base-select` ever extends to editable comboboxes (it currently doesn't — verify).
5. **Command-palette ubiquity** (⌘K) has made the combobox-over-actions pattern a first-class use, blurring combobox/menu.

## 14. Sources cited

(Conservative; reconcile with external pass.) Adobe Spectrum / React Aria `ComboBox` (`inputValue`/`menuTrigger`/`allowsCustomValue`, the two-state model) (2024–2025); IBM Carbon `ComboBox` / `FilterableMultiSelect` (2024); Shopify Polaris `Combobox` + `Autocomplete`, Hydrogen predictive search (2024); GitHub Primer autocomplete (2024); Atlassian `react-select` (async/creatable) (2024); Material 3 autocomplete/exposed-dropdown (2024); Microsoft Fluent `Combobox` (2024); Base Web combobox/creatable (2024); WAI-ARIA APG Combobox pattern (1.2); WCAG 2.2 (Oct 2023) — 1.3.5, 3.3.1/2/3, 1.4.11, 1.4.13, 2.4.13, 4.1.2, 4.1.3, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: combobox
  name: Combobox
  aliases: [autocomplete, autosuggest, typeahead, search-select, combo-box]
  category: form
  status: stable
description: >
  A text input that destructively FILTERS a listbox as the user types,
  resolving to a value from a (often large or remote) set. Stands on the
  text-field substrate AND select's overlay machinery. Not a Select
  (button trigger, no filtering), not a Search Field (submits a query),
  not a Menu (commands).
api:
  inherits: [text-field, select]   # field substrate + option model/overlay; only the delta below
  props:
    - {name: inputValue, type: string, required: false, description: "the TEXT in the field — distinct from value (the selection); manage both"}
    - {name: value, type: scalar | array, required: false, description: "the resolved selected option(s); array when multiple"}
    - {name: autocompleteMode, type: enum, values: [none, list, inline, both], default: list, description: "aria-autocomplete; list is the safe default; inline/both opt-in (a11y trap)"}
    - {name: allowsCustomValue, type: boolean, default: false, description: "free-text vs strict must-resolve-to-option; free-text multi = tags input"}
    - {name: filter, type: function, required: false, description: "matcher override; default case+diacritic-insensitive substring; OMIT for async (consumer/server filters)"}
    - {name: menuTrigger, type: enum, values: [input, focus, manual], default: input, description: "open on first keystroke / on focus / caret only"}
    - {name: loading, type: boolean, default: false, description: "async fetch in flight; aria-busy; don't clear the field"}
    - {name: multiple, type: boolean, default: false, description: "token/tag input; inherits select's multi summary"}
states:
  inherits: [text-field, select]   # rest, hover, focus-visible, disabled, read-only, loading, error, empty, expanded
  combobox-specific: [filtering, no-results, type-more-min-query, loading-listbox, inline-completion]
variants:
  size: [small, medium, large]
  autocomplete: [none, list, inline, both]
  resolution: [strict, free-text]
  selection: [single, multiple-token]
  source: [local-filtered, async-remote]
accessibility:
  inherits: [text-field, select]   # label/describedby/error; aria-activedescendant focus stays on the INPUT
  pattern: "WAI-ARIA 1.2 Combobox (role=combobox ON THE INPUT; NOT the deprecated 1.0 wrapper pattern)"
  wcag-criteria: ["1.3.5", "3.3.1", "3.3.2", "3.3.3", "1.4.11", "1.4.13", "2.4.13", "4.1.2", "4.1.3", "2.5.8"]
  aria-attributes:
    input: "role=combobox, aria-expanded, aria-controls, aria-autocomplete, aria-activedescendant"
    listbox: "role=listbox; options role=option"
    results: "polite live region announces result count + loading (4.1.3)"
  keyboard-model:
    type: filters the list
    move: ArrowDown/Up (Down opens if closed), Home/End in text
    select: Enter (active option)
    escape: clears query/closes, then clears value
    commit: Tab (strict -> active/last-valid; free-text -> typed value)
    backspace: edits query, never silently mutates the selection
  focus-behavior: "DOM focus stays on the input; active option via aria-activedescendant; inline-completion text must be deletable"
content:
  label-pattern: "noun phrase (shared with text-field); placeholder is an example ('Search countries'), not the label"
  empty-pattern: "three distinct states — empty/no-query (recents or nothing), 'No results for X', 'Type N+ characters'"
  highlight-pattern: "matched substring emphasised; presentational only — accessible name stays the full label"
  free-text-pattern: "if allowsCustomValue, signal a create row ('Add X')"
  error-pattern: "what + how to fix (SC 3.3.3); delegated to substrate"
motion:
  inherits: select   # listbox enter/exit, faster exit, reduce-motion drops transform
  combobox-specific: "do NOT animate option insert/remove during filtering (lags typing); open/close animates, filter update is instant"
i18n:
  inherits: [text-field, select]
  combobox-specific:
    - "filter matcher normalizes diacritics + case (osterr -> Österreich) — load-bearing since filtering IS the interaction"
    - "IME: filter on compositionend, never intermediate keystrokes (CJK thrash)"
    - "locale-aware result collation; RTL mirrors input/caret/token row"
implementation:
  - "don't hand-roll — headless primitive (React Aria useComboBox, Downshift, Radix); even more failure-prone than select"
  - "TWO-STATE model is the core trap: inputValue (text) vs value (selection); reconcile on select/blur/clear; don't fight typing"
  - "async: debounce + CANCEL stale responses (AbortController/request-id); distinct min-query/loading/no-results/error states"
  - "filtering ownership explicit: built-in matcher for local; for remote DON'T double-filter the returned set"
  - "inherits positioning (Floating UI -> CSS Anchor + Popover API), virtualization, hidden form-mirror from select"
  - "emit the resolved value (not the query) for native forms/Server Actions"
composition:
  composes-with: [text-field, listbox, option, popover, icon, tag, spinner, form]
  alternative-to: [select, search-field, menu, radio-group]
  supersedes: ["select with a bolted-on filter lacking combobox ARIA", "autocomplete hand-rolled on a bare <input>"]
  superseded-by: null
  specialises-into: [tag-input, token-input, command-palette, predictive-search]
notes:
  contested:
    - autocomplete mode (list default; inline/both opt-in)
    - strict vs free-text (strict default; free-text shades into tags input)
    - filter ownership (built-in local vs consumer/server async)
    - single vs multi-token, and the combobox-vs-tags-input boundary
  unverified:
    - "whether appearance:base-select ever extends to editable comboboxes (currently no — verify)"
  evolution: "ARIA 1.0 -> 1.2 pattern migration; explicit two-state model; async-first; command-palette ubiquity"
```
