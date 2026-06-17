---
okf_version: "0.1"
type: component-brief
title: Combobox
description: The hardest widget in ARIA, and the first brief to stand on two substrates at once — the Text Field form-stack and Select's overlay/listbox machinery. A field-truth study of the defining destructive filter, the two-state model (inputValue vs. value), the autocomplete-mode and strict-vs-free-text decisions, async race-condition handling, the multi-select token-vs-checkbox split, and the ARIA 1.2 pattern, with the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [autocomplete, autosuggest, typeahead, searchable-select, filterable-select, combo-box]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Combobox

> If Select is contested on its platform, Combobox is contested on its *state*. It is the component the field openly calls the hardest widget in ARIA, and it earns the title by standing on two substrates at once — the Text Field form-stack (label, helper, error, the describedby chain) and Select's whole overlay/listbox/positioning machinery (the `aria-activedescendant` focus contract, the popover, virtualization). It re-derives neither. What is genuinely its own is one mechanic — an editable input that *destructively filters* the list as you type — and the volatile tension that mechanic creates between two values that every other control keeps as one: the **text in the field** and the **selected entity**. Combobox is the calibration brief for *the two-state reconciliation problem and standing on two inherited substrates*.

---

## 1. Framing

A Combobox is a **text input that destructively filters a listbox as the user types**, resolving to a value from a (often large or remote) set. That one mechanic is the whole boundary. What it *isn't*: a Select (a *button* trigger, non-destructive type-ahead, no editing — see select §1, the boundary drawn from the other side), a plain Text Field, a Search Field (which *submits a query* and routes, rather than resolving to a value in a form), or a Tags Input (which generates *arbitrary* tokens against no underlying vocabulary — §12).

The defining consequence of the editable trigger is that the component must hold **two states**: the `inputValue` (the raw, localized string in the field) and the `value` (the structured entity — usually an id or object — chosen from the list). A Select keeps these perfectly synchronized because its trigger can't be edited; a Combobox invites arbitrary text, so "what the user sees" and "what the system registers" can diverge at every keystroke. Reconciling them is the source of nearly every Combobox bug and nearly every field divergence (both agents converge hard on this as *the* framing).

Where systems disagree:

- **Strict vs. free-text** — must the value resolve to an option, or may it be arbitrary string? Spectrum gates it with `allowsCustomValue` (default off, reverts on blur); Atlassian/Base Web split it into a separate *creatable* component; Fluent uses a `freeform` flag.
- **Autocomplete model** — the `aria-autocomplete` values: `none` / `list` / `inline` / `both`. The field converges on `list`; `inline` (ghost-text completion) keeps resurfacing despite real a11y and cursor-management traps.
- **The multi-select architecture** — and this is two genuinely different components wearing one name (§4): a **token** model (Primer, Atlassian — selecting closes the list and drops a removable chip in the input) vs. a **checkbox/count** model (Carbon, Fluent — the list *stays open* with persistent checkboxes and the input is just a search facet).
- **Filter ownership** — built-in matcher vs. consumer/server-controlled.

## 2. Anatomy and parts

Inherits the Text Field field row (label, helper, error, describedby) and Select's overlay (popover, listbox, option, option-group) — not repeated (see text-field §2, select §2). The structure is a deliberate hybrid: a persistent **trigger group** in flow plus the inherited transient overlay. Combobox-specific parts (both agents):

- **Editable input** — a real `<input>` carrying `role="combobox"`, `aria-expanded`, `aria-controls`, `aria-autocomplete`, `aria-activedescendant`. The trigger is editable, which is the entire difference from Select.
- **Toggle button** — an optional caret to open the full list without typing (a select-like browse mode); a real button, `aria-hidden` from the input's name.
- **Clear button** — resets *both* `inputValue` and `value`; returns focus to the input.
- **Token group** (multi-token only) — removable chips inside or below the input; the input expands to wrap them.
- **Filtered listbox** — the inherited listbox, but its option set is a *function of the query*, and it carries the empty / no-results / loading states inside it.
- **Match highlight** — matched substring emphasised (`<mark>`/bold) within each option; presentation only, never the accessible name.
- **Empty-state slot, create/action item** (creatable), **loader** (inline in the trigger for input-loading, or at the list foot for pagination).

**The practice ships the composition disciplined:** input and toggle as distinct slots sharing a grouped wrapper, so a consumer can swap the plain input for a tokenized one or inject leading visuals (avatars) without touching the popover/filter logic (external — Primer's `Autocomplete.Input as={TextInputWithTokens}` is the reference for keeping token anatomy out of the core).

## 3. Properties / API

Inherits the Text Field core and Select's option model (`options`/composed children, `loading`, `clearable`, `multiple`, `size`, `disabled`, `readOnly`, `placeholder` — see text-field §3, select §3). Combobox-specific:

- **`inputValue` / `onInputValueChange` vs. `value` / `onChange` — the defining two-state API.** The text and the selection are *separate* controlled (or uncontrolled) bindings. This is the API expression of §1's framing, and conflating them is the single most common bug (§11). React Aria models the split explicitly; the practice adopts it.
- **`allowsCustomValue` (free-text) vs. strict.** Strict is the default (data hygiene): on blur, an unmatched `inputValue` reverts to the last valid selection, or clears if none. Free-text is opt-in. **And the practice separates two intents the field often conflates** (external): `allowsCustomValue` means "this form field accepts arbitrary text, the list is just suggestions" (a "Job Title"); *creating a new entity in a backend* is a different workflow served by an explicit `onCreate`/action-item render, not the same flag. Free-text *multi* is a Tags Input (§12).
- **`autocompleteMode` / `aria-autocomplete`** — `none | list | inline | both`. **Default `list`.** `inline`/`both` (auto-inserting and selecting the predicted remainder) are opt-in only — they trigger cursor-jump bugs, fight mobile autocorrect, and risk accidental submission of the *prediction* rather than the typed query (§6).
- **`menuTrigger`** — `input | focus | manual`. **Default `input`** (open on first keystroke); `focus` (open on focus) is right for a prominent isolated search field but is visual noise in a dense form; `manual` opens only via the caret/arrows (Spectrum's three modes).
- **filtering / `filterFn`** — a built-in **case- and diacritic-insensitive substring** matcher by default, with an override. **The hybrid rule both agents reach:** if the consumer supplies a controlled `items` array driven by `onInputChange` (the async case), the component **disables its internal filter and yields entirely** — double-filtering hides server results. Make local-vs-async an explicit mode.
- **async contract** — the practice keeps the Combobox a **pure presentation layer**: it exposes `loading` (render spinners) and `onLoadMore` (an intersection-observer hook at the list foot for infinite pagination), and pushes fetching/caching/cancellation to the consumer's data layer (React Query/SWR) — *not* a baked-in `loadOptions`. (Atlassian's `AsyncSelect`/`loadOptions` is the monolithic alternative; the practice rejects it for the headless-presentation model.)

## 4. States and variants

Inherits the Text Field states and Select's expanded/option-hover/loading-listbox states (see select §4). The Combobox runs the input state machine and the listbox state machine *simultaneously*, which is why the matrix is the catalogue's densest. Combobox-specific:

| State | Combobox-specific contract |
| --- | --- |
| typing — match found | list open + filtered; surviving options show **match highlight** so the user sees *why* they survived |
| typing — no match | the list **must not disappear** — it renders the empty-state slot echoing the query ("No results for 'X'"), confirming the filter ran |
| loading — input | debounced async fetch in flight while typing: spinner replaces the trailing caret/clear; `aria-busy`; **don't clear the field** |
| loading — pagination | list open, scrolled to the foot: spinner *below* the last option as more items append (distinct from input-loading — external) |
| type-more / min-query | async with a minimum query length: "Type 2+ characters" before firing |
| blur reconciliation | **the most fragile transition** — unmatched `inputValue` reverts to the last valid value (strict) or persists (free-text); never silently strands half-typed text as the value |

**Variants:** size/density inherited. The genuine Combobox axes: **autocomplete mode** (`none/list/inline/both`), **strict vs. free-text**, **source** (local-filtered vs. async-remote), and the **multi-select architecture** — which the field splits into two structurally different models the practice supports as distinct (external):

- **Token** (Primer/Atlassian) — selecting closes the list and drops a removable chip in the input, which grows to wrap. Best for **sparse tagging** (three assignees on a ticket).
- **Checkbox / count** (Carbon/Fluent) — the list **stays open** with persistent per-option checkboxes; the input shows a count summary ("3 selected") and acts as a search facet. Best for **dense analytical filtering** (fifteen overlapping regions on a dashboard).

The cognitive models differ, so the practice ships both rather than forcing one — `selectionMode: single | multiple-token | multiple-checkbox`.

## 5. Usage guidance

- **Use** when the set is **large enough that scanning is hostile (~>15 options)** or **remote/unbounded**, and the user can name what they want — country/user/assignee pickers, tag selection, address autocomplete.
- **Don't use** for: a **small known set** (→ Select, or Radio if ≤~5 — filtering is friction when the target is visually scannable); a value the user **doesn't type** (→ Select); a **search that submits a query and routes** (→ Search Field); arbitrary tokens against no vocabulary (→ Tags Input); or **commands** (→ Menu).
- **Decision frameworks:**
  - **Combobox vs. Select is the filtering line** — will the user type to narrow? Yes → Combobox; no → Select (select §1, §5).
  - **Combobox vs. Predictive Search is the output** — a Combobox *sets a form value*; predictive search (Hydrogen) *emits a link and routes away*. Never embed predictive-search-routing in a data-entry form, and never use a value-setting combobox for global navigation (external).
  - **Strict vs. free-text** — strict when the value must be a real entity (a user id); free-text when arbitrary input is valid (a city not yet in the taxonomy).
  - **Token vs. checkbox multi** — sparse tagging → token; dense batch filtering → checkbox/count (§4).
  - **Mobile:** the floating popover competes with the software keyboard, so the listbox should become a **full-screen or bottom-sheet search view**, not a cramped popover — Apple HIG explicitly prefers a full-screen table + pinned search bar for large mobile datasets (external; inherits select §5).

## 6. Accessibility

Inherits the Text Field substrate (label, describedby, error) and Select's focus contract (see select §6). Combobox-specific, and it leans harder on `4.1.2` than any other component:

- **The ARIA 1.2 combobox pattern — `role="combobox"` on the `<input>` itself**, with `aria-expanded`, `aria-controls` → the listbox id, and **`aria-autocomplete`** declaring the behaviour. **Do not ship the deprecated ARIA 1.0 pattern** (`role` on a wrapper `<div>` + `aria-owns` to bridge to a detached listbox) — it caused widespread screen-reader parsing failures and is obsolete; legacy code still carries it, so this is an active correctness check against the APG (both agents).
- **DOM focus never leaves the input** — unlike Select, where activation can move real focus into the listbox, a Combobox *must not*, or typing breaks. The active option is tracked with **`aria-activedescendant`** updated as arrows move; the screen reader announces it as if focused while keystrokes stay in the input (both agents — sharpened from select because typing *is* the primary interaction).
- **A polite live region announces the result count** ("7 options available", "No options available") so a screen-reader user knows the filter ran; silence reads as broken (**SC 4.1.3 Status Messages**).
- **`inline`/`both` autocomplete is an a11y minefield** — auto-inserted completion text must be deletable (backspace removes it, doesn't re-trigger), must be announced, and must not cause Enter to submit the *prediction* instead of the query. This is why `list` is the enforced default.
- **Keyboard model:** typing filters; Down/Up move the active option (Down opens if closed); Enter selects the active option; Escape clears the query/closes, then clears the value; Tab commits (strict → active/last-valid; free-text → typed value); Backspace edits the query and never silently mutates the selection.
- **Mobile/portal AT bug** (inherited from select §6): VoiceOver can lose `aria-activedescendant` across a portalled listbox — Fluent's `inlinePopup` (render the list inline, adjacent to the input) is the documented escape hatch; the top-layer Popover model is the more durable fix.
- **WCAG SCs:** the Text Field set (1.3.5, 3.3.1/2/3, 1.4.11, 2.4.13, 2.5.8) plus **4.1.3 Status Messages** (the results-count/loading live region), **1.4.13** (popup dismissible/hoverable, inherited), and **4.1.2 Name/Role/Value** carrying the combobox role contract.

## 7. Content guidelines

- **Placeholder signals the mechanic, not the identity** — "Search countries…" / "Type to filter…", not the static "Country" (which implies plain text entry). Still never the label (inherited). In free-text mode the placeholder can hint that custom entries are allowed (external — Fluent).
- **Three distinct empty messages, not one:** nothing typed (show recents/top options, or nothing), **no-results** ("No results for '<query>'" — echo the query to confirm the filter ran), and **type-more** ("Type 2+ characters"). Don't show "No results" before the minimum query.
- **Match highlight** aids scanning but is presentational; the option's accessible name stays the full label.
- **Creatable action copy is command-oriented** — "Add '<query>'" / "Create '<query>'" — so the user knows they're expanding the taxonomy, not selecting.
- Error copy follows SC 3.3.3, delegated to the substrate.

## 8. Motion and transition

Inherits Select's listbox enter/exit (~100–150ms fade + small translate, faster exit, reduce-motion drops the transform — see select §8). The Combobox-specific rule is a **prohibition**: do **not** animate option insertion/removal/reorder *during filtering*. The query mutates the list several times a second as the user types at speed; animating item height or position thrashes layout and makes the target impossible to track with the eye. The open/close transition animates; the **filter update snaps instantly**. If the popover's bounding box must resize, a hardware-accelerated `scaleY` on the wrapper is acceptable, but the contents stay un-animated. Match-highlight changes are instant.

## 9. Internationalization

Inherits Text Field i18n (logical-property RTL, expansion, IME) and Select's listbox mirroring (see select §9). Combobox-specific, and the filter engine is where it bites:

- **The default matcher must normalize, never naive-compare** — case-fold *and* strip diacritics (decompose `NFD`, remove combining marks) so "cafe" matches "café" and "munchen" matches "München". This is load-bearing here because **filtering *is* the interaction** (both agents; the external pass specifies the `normalize("NFD")` + combining-marks-strip pipeline).
- **IME composition is critical** — for CJK input, filter on `compositionend`, never on intermediate composition keystrokes, or the list thrashes mid-composition (sharpened from text-field §9).
- **RTL** mirrors the trigger group: the caret moves to the leading (left) edge; the clear button stays adjacent to the text's active alignment; option visuals swap sides.
- **Text expansion** in the listbox — don't clip; wrap or ellipsis-with-tooltip; the popover grows its `min-width` (inherits select §9).

## 10. Naming

The field is badly fragmented (external's table): **`Combobox`** (W3C/ARIA, Spectrum/React Aria, Fluent, Base Web) vs. **`Autocomplete`** (Primer, MUI) vs. **`Combo box` / `MultiSelect`** split (Carbon) vs. **`Select isSearchable`** (Atlassian/react-select bundles it into Select) vs. **`ExposedDropdownMenu`** (Material, naming the visual not the semantics). **The practice default is `Combobox`** — it matches the W3C canonical name and the `role`, eliminating dissonance between docs and the DOM, and aligns with the Select sibling's naming logic. The free-text-multi variant is often separately named **`TagInput` / `TokenInput`** (§12). Aliases to map in docs search and JSDoc: `Autocomplete`, `Autosuggest`, `Typeahead`, `SearchableSelect`, `FilterableSelect`.

## 11. Implementation notes

Inherits Select's overlay machinery (positioning via Floating UI → CSS Anchor Positioning + Popover API, top-layer rendering, virtualization, the hidden form-mirror for submission — see select §11; that machinery is now formalised in popover, of which the Combobox listbox is a `role=listbox` specialisation). The Combobox-specific traps, all of which recur across codebases (both agents):

- **Don't hand-roll** — use a headless primitive (React Aria `useComboBox`, Downshift, Radix/Base UI) for the input/listbox/`activedescendant`/keyboard contract; it is even more failure-prone than Select. Ship an opinionated styled `Combobox` for the 90% case *and* expose `Combobox.Root`/`.Input`/`.Popover` for the 10% (a data-table cell, a nav bar).
- **The two-state cursor-jump trap is the signature bug.** A fully controlled `inputValue` wired to slow React state can drop keystrokes and fling the caret to the end: the native input updates instantly, but a batched/delayed state commit overwrites it with stale text. The fix: the component maintains a **localized, synchronous source of truth** for the input (an uncontrolled ref / `useSyncExternalStore`) and only accepts an incoming `inputValue` that genuinely differs — breaking the destructive loop and preserving caret position. Never bind the input directly to the committed `value`.
- **Async race conditions** — debounce input (~300ms, per Hydrogen's predictive search) and **cancel stale requests with `AbortController`** (or a request-id guard) so a slow earlier query can't overwrite a fast later one. Surface min-query / input-loading / pagination-loading / no-results / error as distinct states.
- **Filter ownership is explicit** — built-in matcher for local data; for remote, the component must **not** re-filter the server's returned set (double-filtering hides results).
- **Virtualize long/remote lists** (the external pass triggers as low as ~50 items; the inherited select guidance is "beyond a few hundred" — either way, render only the visible window + overscan). Virtualization breaks browser Find-in-Page, which is an accepted trade because the input *is* the search. Note virtualization fights `aria-activedescendant` (the active option must be in the DOM).
- **Form value** — emit the resolved `value` (not the query string) for native forms/Server Actions.

## 12. Related and alternative components

- **Composes with:** Text Field substrate, Listbox/Option/Popover (the inherited surface), Icon (search/caret/clear — see icon), Tag/Token (the multi-select token field renders Tags — see tag), Spinner (async), Virtualizer, Form.
- **Alternative to:** Select (no typing/filtering — the §1 boundary), Search Field (submits a query and routes vs. resolves to a value), Tags Input (arbitrary tokens, no vocabulary), Menu (commands), Radio (tiny sets).
- **Supersedes:** the legacy standalone Typeahead (absorbed into the ARIA 1.2 combobox); a Select with a bolted-on filter lacking the combobox ARIA; an autocomplete hand-rolled on a bare `<input>`; the native `<datalist>` (§13).
- **Superseded by / specialises into:** **TagInput/TokenInput** (free-text multi), **Command palette** (combobox over actions — ⌘K), **predictive/address search** (combobox-shaped but routing).

(See text-field and select for the two inherited substrates this brief stands on; 03-component-library for the model; 29 for the docs template. Search Field, when briefed, draws the query-vs-value boundary from its side; Tags Input, when briefed, draws the vocabulary boundary.)

## 13. Field POV evolution

1. **ARIA 1.0 → 1.2 migration** — `role="combobox"` moved off the wrapper onto the `<input>`, and the `aria-owns`-bridged dual-listbox hack was abandoned; shipped code still carries the old pattern, so this is an active correctness migration (both agents).
2. **The death of native `<datalist>`** — unstyleable, behaviorally inconsistent across engines, and unable to render rich option content (avatars, two-line options), it has been universally abandoned for custom JS comboboxes (external).
3. **The explicit two-state model** (`inputValue` vs `value`) is now first-class in mature libraries (React Aria) rather than an implicit footgun.
4. **Async-first** — comboboxes are increasingly remote/predictive (search-as-you-type backends), pushing debounce/cancel/loading/pagination into the core contract.
5. **Headless state-machine extraction** — the field moved off monolithic `react-select` toward decoupled hooks (`useComboBox`) and headless primitives (Base UI/Radix), because extracting the state machine from the rendering layer is the only path to bespoke styling at scale (external).
6. **Command-palette ubiquity** (⌘K) has made combobox-over-actions a first-class use, blurring combobox/menu; and the platform shift inherited from select (Popover API + CSS Anchor Positioning) reaches comboboxes too — though whether `appearance: base-select` ever extends to *editable* comboboxes is unresolved (currently no — verify).

## 14. Sources cited

Conservative dating (the external pass stamped nearly every system 2026 — Spectrum/React Aria, Atlassian/react-select, Base Web/Base UI, Primer, Material 3/Compose, Carbon, Fluent 2, Polaris, Hydrogen, Radix, Apple HIG — held loosely and unverified; `last-audited` in frontmatter is the re-run trigger):

- Adobe Spectrum / React Aria — `ComboBox` (`inputValue`/`menuTrigger`/`allowsCustomValue`/`defaultFilter`, the explicit two-state model, `useComboBox`) (Spectrum, 2024–2025).
- IBM Carbon — `ComboBox` (single/custom) vs. `FilterableMultiSelect` (open-list persistent checkboxes) — the Dropdown/Combo box split (Carbon, 2024–2026).
- GitHub Primer — `Autocomplete`, the `Autocomplete.Input as={TextInputWithTokens}` token composition, internal `filterFn` (Primer, 2024–2026).
- Atlassian Design System — `react-select` (`isSearchable`, `AsyncSelect`/`loadOptions`, `CreatableSelect`) (Atlassian, 2024–2026).
- Microsoft Fluent 2 — `Combobox` (`freeform`, `inlinePopup` for iOS VoiceOver) (Fluent, 2024–2026).
- Shopify Polaris / Hydrogen — `Combobox` + `Autocomplete`; Hydrogen Predictive Search (300ms debounce, routing output) (Polaris/Hydrogen, 2024–2026).
- Uber Base Web / Base UI — `Combobox`/creatable, the `Overrides` headless slot API (Base Web, 2024–2026).
- Google Material 3 / Compose — `ExposedDropdownMenu` (Material, 2024–2026).
- Radix UI — headless combobox primitives (Radix, 2024–2026).
- Apple Human Interface Guidelines — full-screen table + pinned search bar over a combobox on mobile (Apple HIG, 2024).
- W3C / WAI-ARIA APG — the Combobox pattern (1.2), the deprecated 1.0 `aria-owns` model; `@tanstack/react-virtual` (virtualization reference).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.3.5, 3.3.1, 3.3.2, 3.3.3, 1.4.11, 1.4.13, 2.4.13, 4.1.2, 4.1.3, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: combobox
  name: Combobox
  aliases: [autocomplete, autosuggest, typeahead, searchable-select, filterable-select, combo-box]
  category: form
  status: stable
description: >
  A text input that destructively FILTERS a listbox as the user types,
  resolving to a value from a (often large or remote) set. Holds TWO
  states — inputValue (the text) and value (the selection). Stands on the
  text-field substrate AND select's overlay machinery. Not a Select
  (button trigger, no filtering), not a Search Field (submits a query +
  routes), not a Tags Input (arbitrary tokens, no vocabulary), not a Menu.
api:
  inherits: [text-field, select]   # field substrate + option model/overlay; only the delta below
  props:
    - {name: inputValue, type: string, required: false, description: "the TEXT in the field — a SEPARATE controlled binding from value; manage both"}
    - {name: value, type: scalar | array, required: false, description: "the resolved selected entity (id/object); array when multiple"}
    - {name: allowsCustomValue, type: boolean, default: false, description: "free-text vs strict (revert/clear on blur if unmatched). Distinct from onCreate (adding a backend entity). Free-text multi = tags input."}
    - {name: autocompleteMode, type: enum, values: [none, list, inline, both], default: list, description: "aria-autocomplete; list is the enforced default; inline/both opt-in (cursor-jump + a11y trap)"}
    - {name: menuTrigger, type: enum, values: [input, focus, manual], default: input, description: "open on first keystroke / on focus (prominent search only) / caret+arrows only"}
    - {name: filterFn, type: function, required: false, description: "override; default case+diacritic-insensitive substring; DISABLED when consumer supplies controlled items via onInputChange (no double-filter)"}
    - {name: loading, type: boolean, default: false, description: "async fetch in flight; spinner; aria-busy; don't clear the field"}
    - {name: onLoadMore, type: function, required: false, description: "intersection-observer at list foot for infinite pagination; component stays a pure presentation layer (no baked-in loadOptions)"}
    - {name: multiple, type: boolean, default: false, description: "see variants.selectionMode — token vs checkbox are different architectures"}
states:
  inherits: [text-field, select]   # rest, hover, focus-visible, disabled, read-only, loading, error, empty, expanded
  combobox-specific: [typing-match, typing-no-match, loading-input, loading-pagination, type-more-min-query, blur-reconciliation]
  note: "runs the input state machine and the listbox state machine simultaneously — the densest matrix in the catalogue"
variants:
  size: [small, medium, large]
  density: [comfortable, compact]
  autocomplete: [none, list, inline, both]
  resolution: [strict, free-text]
  source: [local-filtered, async-remote]
  selectionMode: [single, multiple-token, multiple-checkbox]   # token closes list + chip (sparse tagging); checkbox keeps list open + count (dense filtering)
accessibility:
  inherits: [text-field, select]   # label/describedby/error; aria-activedescendant focus stays on the INPUT
  pattern: "WAI-ARIA 1.2 Combobox (role=combobox ON THE INPUT; NOT the deprecated 1.0 wrapper + aria-owns)"
  wcag-criteria: ["1.3.5", "3.3.1", "3.3.2", "3.3.3", "1.4.11", "1.4.13", "2.4.13", "4.1.2", "4.1.3", "2.5.8"]
  aria-attributes:
    input: "role=combobox, aria-expanded, aria-controls, aria-autocomplete, aria-activedescendant"
    listbox: "role=listbox; options role=option, aria-selected"
    results: "visually-hidden aria-live=polite announces result count + loading (4.1.3)"
  keyboard-model:
    type: filters the list
    move: ArrowDown/Up (Down opens if closed), Home/End in text
    select: Enter (active option)
    escape: clears query/closes, then clears value
    commit: Tab (strict -> active/last-valid; free-text -> typed value)
    backspace: edits query, never silently mutates the selection
  focus-behavior: "DOM focus PERMANENTLY on the input; active option via aria-activedescendant; inline-completion text must be deletable + announced"
  mobile: "portalled listbox can drop activedescendant in iOS VoiceOver — inlinePopup / top-layer Popover mitigates (inherited from select)"
content:
  label-pattern: "noun phrase (shared with text-field)"
  placeholder-pattern: "signals the mechanic ('Search countries…' / 'Type to filter…'), not the static identity; never the label"
  empty-pattern: "THREE distinct states — empty/no-query (recents or nothing), 'No results for X' (echo the query), 'Type N+ characters'"
  highlight-pattern: "matched substring emphasised; presentational only — accessible name stays the full label"
  create-pattern: "command-oriented if creatable ('Add X' / 'Create X')"
  error-pattern: "what + how to fix (SC 3.3.3); delegated to substrate"
motion:
  inherits: select   # listbox enter/exit (~100-150ms, faster exit, reduce-motion drops transform)
  combobox-specific: "PROHIBIT animating option insert/remove/reorder during filtering (layout thrash, untrackable); open/close animates, filter update SNAPS; popover box may scaleY, contents stay static"
i18n:
  inherits: [text-field, select]
  combobox-specific:
    - "filter matcher MUST normalize: case-fold + strip diacritics (NFD decompose + remove combining marks) — café matches 'cafe' — load-bearing since filtering IS the interaction"
    - "IME: filter on compositionend, never intermediate keystrokes (CJK thrash)"
    - "RTL mirrors trigger group: caret to leading edge, clear button adjacent to active text alignment"
implementation:
  - "don't hand-roll — headless primitive (React Aria useComboBox, Downshift, Radix/Base UI); ship opinionated styled + expose Root/Input/Popover slots"
  - "TWO-STATE cursor-jump trap: keep a localized synchronous input source (uncontrolled ref / useSyncExternalStore); accept incoming inputValue only if it differs; never bind input to the committed value"
  - "async: debounce (~300ms) + AbortController cancel stale responses; distinct min-query/input-loading/pagination-loading/no-results/error states"
  - "filter ownership explicit: built-in for local; for remote DON'T re-filter the server's returned set"
  - "virtualize long/remote lists (breaks Find-in-Page — accepted; fights activedescendant — active option must be in DOM); inherits positioning + hidden form-mirror from select"
  - "emit the resolved value (not the query) for native forms/Server Actions"
composition:
  composes-with: [text-field, listbox, option, popover, icon, tag, spinner, virtualizer, form]
  alternative-to: [select, search-field, tags-input, menu, radio-group]
  supersedes: ["legacy standalone typeahead", "select with a bolted-on filter lacking combobox ARIA", "autocomplete hand-rolled on a bare <input>", "native <datalist>"]
  superseded-by: null
  specialises-into: [tag-input, token-input, command-palette, predictive-search]
notes:
  contested:
    - autocomplete mode (list default; inline/both opt-in)
    - strict vs free-text (strict default; free-text-multi = tags input; allowsCustomValue distinct from create-entity)
    - filter ownership (built-in local vs consumer/server async)
    - multi architecture: token (closes list, sparse tagging) vs checkbox/count (keeps list open, dense filtering) — ship both
  unverified:
    - "whether appearance:base-select ever extends to editable comboboxes (currently no — verify)"
    - "external-supplied 2026 version numbers; the ~50-item virtualization threshold and engine-dependent perf figures"
  evolution: "ARIA 1.0 -> 1.2 migration; death of native <datalist>; explicit two-state model; async-first; headless extraction; command-palette ubiquity"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-combobox/` (15 June 2026). Strong convergence on the spine — the destructive filter as the defining mechanic and the select-vs-combobox boundary, the two-state (`inputValue` vs `value`) reconciliation as the core tension, `allowsCustomValue` strict-vs-free-text (and free-text-multi = tags input), `aria-autocomplete=list` as the enforced default with `inline`/`both` as opt-in traps, `menuTrigger=input` default, the built-in-local-vs-yield-to-consumer filter rule (no double-filtering), async debounce + `AbortController` cancellation, the ARIA 1.2 pattern (role on the input, not the deprecated 1.0 wrapper + `aria-owns`), `aria-activedescendant` with DOM focus locked to the input, the polite results-count live region, virtualization, diacritic+case normalization, and the combobox-vs-select / -search-field / -tags-input boundaries. This is the first brief to stand on TWO substrates (text-field + select), expressed through the schema's `inherits:` field. External-agent contributions: the two distinct multi-select architectures (token-closes-list / sparse tagging vs. checkbox-keeps-list-open / dense filtering, mapped to Primer-Atlassian vs. Carbon-Fluent) as the sharpest single addition, the controlled-value cursor-jump mechanism and its `useSyncExternalStore`/localized-ref fix, the input-loading vs. pagination-loading split, the death of native `<datalist>` as an evolution point, the NFD normalization pipeline, the Hydrogen 300ms-debounce and predictive-search-routing boundary, the Apple-HIG full-screen-mobile guidance, the Fluent `inlinePopup` iOS bug, and the fragmented naming table. Claude-pass contributions: the `onCreate`-distinct-from-`allowsCustomValue` intent split, the pure-presentation async stance (`loading`/`onLoadMore` over a baked-in `loadOptions`), the inheritance framing against text-field/select, and the IME-on-`compositionend` filter guard. The external pass's 2026 version numbers, the ~50-item virtualization threshold, and the engine-dependent performance figures are flagged unverified pending `_source-text/` backing. Conformant to `components/_schema.md` (locked key order; `inherits:` per section; `notes.unverified`). The §15 schema is the structured projection of the prose.*
