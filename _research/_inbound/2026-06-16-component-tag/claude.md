# Tag — field-truth study (Claude pass)

## 1. Framing
A Tag is the **interactive / removable token** — the active counterpart to Badge (the passive indicator). Where Badge *informs* and is `aria-hidden`-on-a-host or announces its own static text, a Tag is a focusable, operable thing: the user clicks it, toggles it, or removes it. The headline problem — exactly parallel to Badge — is that **"Tag" / "Chip" / "Token" name overlapping but distinct genres**, and the practice has to resolve the genre split and the naming morass before the API.

The canonical genre taxonomy is **Material 3's four chips**, plus a standalone metadata tag:
- **Assist chip** — acts like a button; a transient, contextual *smart action* ("Add to calendar", "Turn on flashlight"). It triggers an action, doesn't persist a state.
- **Filter chip** — a *toggle* in a multi-select set, carrying a selected/unselected state ("Weekend", "Under $50"). Borders Checkbox.
- **Input chip** — a user-entered, **removable token** in a field (email recipients, applied filters, free-text tags). The genre the multi-select Combobox composes. Borders the token field.
- **Suggestion chip** — a dynamically-generated prompt/recommendation; acts like a button/link ("Trending: …", a reply suggestion).
- **(Standalone) read-only / metadata tag** — an article category, a status label (sometimes a link). The closest to Badge — and the boundary case that makes the Badge-vs-Tag line load-bearing.

The naming morass: **Material / MUI / Carbon** call it **Chip**; **Ant / Polaris / Spectrum / Atlassian** call it **Tag**; **GitHub Primer** calls it **Token** (`Token` / `AvatarToken` / `IssueLabelToken`); **Fluent** ships `Tag` / `InteractionTag` + `TagGroup`. The same word ("Chip") is the umbrella in Material but a specific thing elsewhere.

The five genres collapse to **three interaction archetypes** — the real axis the API must serve: **action** (assist/suggestion → behaves like a **Button**), **selection** (filter = multi-select → borders **Checkbox**; choice = single-select → borders **Radio**), and **input/token** (removable tokens in a field → composed by the multi-select **Combobox**). What it *isn't*: a **Badge** (the passive, non-interactive, non-removable indicator — see badge; the boundary from Tag's side: if it has an `onClick`, an `×`/remove, or a selected state, it's a **Tag**), a true **Button** (an assist chip is button-*like* but lives in a chip set, low-commitment and often plural), or a **Checkbox/Radio** in a form (a filter chip is a *lightweight, inline* multi-select; a real form field with a label + validation is a checkbox group — §5). Why systems disagree: the genre model + naming, and the removable-tag accessibility pattern (still genuinely contested — §6).

## 2. Anatomy and parts
- **the tag body** — the container (filled or outlined surface, radius, padding); the primary hit target *when the whole tag is interactive* (action/filter/choice). Carries the label and the optional leading/trailing parts.
- **the leading icon / avatar / dot** — an optional adornment: an icon (inherits Icon — see icon), an avatar (a person token — Primer's `AvatarToken`), or a status dot. A *selected* filter/choice chip often swaps the leading slot for a **checkmark** (Material's selected state).
- **the label** — the short text. Truncates with ellipsis + full text on hover/`title` past a max-width (§7).
- **the trailing remove "×"** *(removable/input genre only)* — an **embedded icon button** with its *own* accessible name ("Remove [tag]") — a second interactive element inside the tag (inherits Button + Icon — see button, icon). This is the source of the accessibility complexity (§6): one tag = two operable things.
- **the selected indicator** *(filter/choice)* — a checkmark, a fill change, or an outline→filled transition; never color alone (§6).
- **the hit-target structure** — the load-bearing anatomical decision: is the **whole tag** clickable (action/filter) with the `×` a nested button, or is **only the `×`** interactive (a read-only token you can only remove)? This drives the role model (§6).

## 3. Properties / API
- **`label` / children** — the text content.
- **`variant` / genre** — assist / filter / input / suggestion (Material), or the archetype model action / selection / input. Most libraries expose this as a mix of booleans (`clickable`, `onDelete`) rather than one enum (MUI: a `Chip` is clickable if `onClick`, deletable if `onDelete`).
- **`selected` / `aria-selected`** *(filter/choice)* — the toggle state; `CheckableTag` (Ant) is the explicit selectable variant.
- **`onRemove` / `onDelete` / `closable`** — the remove handler + whether the `×` renders (MUI `onDelete`, Ant `closable`/`onClose`, Chakra `TagCloseButton`). Presence of the handler is what makes a tag removable.
- **`onClick`** — the action handler (assist/suggestion/filter body).
- **`disabled`** — non-operable; still announced (§6).
- **`leadingIcon` / `avatar` / `icon`** — the leading adornment.
- **`size`** — small / medium (the common pair; some add large).
- **`tone` / `color` / `variant=filled|outlined`** — the visual weight + the semantic tone where a tag encodes status (inherits the Badge/Banner color-not-sole-carrier rule — §6).
- **`removable`** — whether the remove affordance exists.
- **the remove button's accessible-name wiring** — not a styling prop but load-bearing: the embedded `×` needs its own name composed from the tag's label ("Remove Marketing"), not a bare "Remove" or "×" (§6).
- **the group:** `TagGroup` / `ChipSet` / token-field — the container that owns the selection model (single/multi), the keyboard navigation, and the focus-management-after-removal (§6/§11). The group is where the real API lives; a lone tag is half the story.

## 4. States and variants
- **States:** **default / hover / focus / active** (it's interactive — unlike Badge), **selected / unselected** (filter/choice), **disabled**, plus the transient **removing** (the dismiss animation). The remove `×` has its *own* hover/focus state nested inside.
- **Variants:**
  - **genre / archetype:** assist / filter / input / suggestion (→ action / selection / input).
  - **selection:** selected vs unselected (filter = multi; choice = single).
  - **removable** vs static/read-only.
  - **clickable/action** vs display-only.
  - **tone:** neutral + the semantic palette (info/success/warning/error) where a tag encodes status.
  - **fill:** filled vs outlined.
  - **size:** small / medium (/ large).
  - **adornment:** leading icon / avatar / dot / none; trailing remove / none.

## 5. Usage guidance
- **Use a Tag (interactive/removable token) for:**
  - **Applied filters / facets** the user can see and remove (input chips in a search bar) — the canonical case.
  - **A lightweight inline multi-select** (filter chips) where a full checkbox group would be heavy and the options are few and scannable.
  - **Free-text / entity tokens** entered into a field (recipients, labels, keywords) — composed by the multi-select Combobox (see combobox).
  - **Contextual smart actions** (assist/suggestion chips) — low-commitment, plural, contextual.
- **Don't use a Tag for:**
  - A **passive indicator** (a count, a status pill you can't act on) → a **Badge** (see badge). The boundary: no `onClick`, no `×`, no selected state ⇒ Badge.
  - A **primary action** → a **Button** (see button). An assist chip is for *secondary, contextual, plural* actions, not the page's main CTA.
  - A **structured form choice with a label + validation** → a **Checkbox/Radio group** (see checkbox, radio). Filter chips are inline and lightweight; a real form field is not a chip set.
  - A **single binary setting** → a **Switch/Checkbox**, not a lone filter chip.
- **Decision frameworks:**
  - **Filter chips vs a checkbox group:** few, scannable, inline, immediate-effect, space-constrained (mobile) → chips; many options, grouped, labelled, part of a form submission → checkboxes. (Chips trade the explicit form semantics for compactness.)
  - **Assist chip vs Button:** is it the primary action, or one of several contextual suggestions? Primary → Button; contextual/plural/transient → assist chip.
  - **The Badge-vs-Tag test (from Tag's side):** can the user *do* something to it (click/toggle/remove)? Yes → Tag; no → Badge.

## 6. Accessibility
**The crux is the removable tag group, and the field has a modern settled answer: the GRID pattern.** A removable tag is *two* interactive things — the tag body and the embedded remove `×` — and a flat list of tags-with-buttons produces a focus mess (every tag = two tab stops; removing one drops focus to `<body>`). React Aria / Spectrum's **`TagGroup` implements the removable group as a `role="grid"`**: each tag is a **`row`**, the tag content and the remove button are **`gridcell`s**, arrow keys navigate *between* tags (a single tab stop into the group, then roving), and **Delete/Backspace on a focused tag removes it**. This is the reference implementation other systems are converging toward.

- **Focus management after removal (the load-bearing rule, the classic bug):** when a tag is removed, move focus to the **next** tag; if it was the last, the **previous**; if it was the only one, the **group container** (or the associated input). **Never drop focus to `<body>`** — that's the recurring failure. (WCAG 2.4.3 Focus Order.)
- **The remove button's accessible name** — the embedded `×` needs its *own* name composed from the label: `aria-label="Remove Marketing"`, not a bare "Remove", "Close", or "×". (4.1.2.)
- **The selection genres take different roles, not the grid:**
  - **Filter chips (multi-select)** → a `listbox` with `aria-multiselectable` and `option`s (`aria-selected`), or a group of `button[aria-pressed]` toggles. (The Toggle Button group model — see toggle-button.)
  - **Choice chips (single-select)** → a `radiogroup` of `radio`s (the Radio keyboard model — single tab stop, arrow to move + select — see radio).
  - **Assist / suggestion chips** → plain **`button`s** (see button). No selected state.
- **The whole-tag-vs-× hit target** — an *input* chip whose body is non-interactive (you can only remove it) shouldn't be a button; only the `×` is operable (inside the grid, the row is navigable, the remove cell is the action). An *action/filter* chip's whole body is the operable target with the `×` nested.
- **Backspace-removes-last-token** — in a token *input* field, Backspace at an empty caret removes the last token (a strong convention — but pair it with the visible group's Delete/Backspace, and don't make it the *only* way to remove).
- **Color-not-sole-carrier** — where a tag encodes status/category by color, pair color with text (and optionally an icon), inheriting the Badge/Banner severity rule (see badge, banner). A color-only tag set fails 1.4.1.
- **Target size** — the embedded `×` inside a small tag is the recurring 2.5.5/2.5.8 trap: the remove button's touch target must reach the minimum (24×24 CSS px for 2.5.8 AA; 44×44 for 2.5.5 AAA) even though the tag is small — via padding/hit-slop, not a bigger glyph.
- **WCAG SCs:** **2.1.1** (keyboard — operate + remove), **2.4.3** (focus order — the after-removal contract), **2.5.5 / 2.5.8** (target size — the `×`), **1.4.1** (color not sole carrier), **4.1.2** (name/role/value — the remove button's name, the selected state).

## 7. Content guidelines
- **Short labels** — one to three words; a tag is a token, not a sentence. Truncate past a max-width with an ellipsis and the full text in a `title`/tooltip.
- **The remove button's name** — "Remove [label]" ("Remove Marketing"), composed from the tag, never a bare "Remove"/"×".
- **Casing** — sentence case (or match the data, e.g. user-entered tags preserve the user's casing); consistent across the set.
- **Don't overload** — a tag carries one token of meaning; don't pack a label + count + status + two icons into one chip.
- **The Tag-vs-Badge content distinction** — a Tag's content is usually *user/data-driven and actionable* (a filter, a recipient, a category you can remove); a Badge's is *system-driven and passive* (a count, a status). If the content is something the user added or can act on, it's a Tag.

## 8. Motion and transition
- **Remove / dismiss** — the tag collapses out (scale/opacity + width collapse) and the **group reflows** to close the gap; keep it fast (~150ms) so removal feels immediate. The reflow is the costlier part — animate `transform`, not layout, where possible.
- **Add** — a new token animates in (scale/fade) as it's entered; subtle.
- **Selected transition** — the filter/choice chip's fill/checkmark transition is brief; the checkmark may slide the label.
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops the collapse/reflow animation to an instant remove (the state change is the information, not the motion).

## 9. Internationalization
- **RTL** — the remove `×` flips to the **leading (inline-start) edge** and the leading icon/avatar to the trailing; anchor via logical properties (`padding-inline`, `inset-inline`) so it mirrors off `dir="rtl"` with no JS.
- **Label expansion + truncation** — translated labels run longer; the max-width + ellipsis must hold, and the `title`/tooltip carries the full text. Don't hardcode tag widths.
- **Token-field wrapping** — a token field of tags wraps to multiple lines (or scrolls); the wrap must respect the RTL flow direction.

## 10. Naming
- **The field set:** Material / MUI / Carbon `Chip`; Ant / Polaris / Spectrum / Atlassian `Tag`; GitHub Primer `Token` (`Token` / `AvatarToken` / `IssueLabelToken`); Fluent `Tag` / `InteractionTag` + `TagGroup`; Chakra `Tag` (+ `TagCloseButton` / `TagLeftIcon`).
- **The practice's default — `Tag`** as the component name (over `Chip`, which Material overloads as the umbrella, and over `Token`, which reads as Primer-specific), with **`TagGroup`** as the container that owns the selection model + the grid keyboard pattern + focus-management-after-removal. Expose the genres via the **interaction archetype** rather than four lookalike components: a `Tag` that is *removable* (`onRemove`), *selectable* (`selected` in a `TagGroup` with a selection mode), or *actionable* (`onClick`) — the booleans/handlers compose, mirroring MUI's `clickable`/`onDelete` model but with the group owning selection. Material's assist/filter/input/suggestion names are useful *documentation* genres mapped onto this.
- **The Badge-vs-Tag + Chip-vs-Tag disambiguation:** **Tag = interactive/removable token; Badge = passive indicator** (the boundary drawn from Badge's side — see badge). **"Chip"** is an accepted alias but ambiguous (Material's umbrella); **"Token"** is the token-field framing; **"Pill"** is a `border-radius` aesthetic, not a component.
- **Aliases to map:** Chip, Token, AvatarToken, IssueLabelToken, InteractionTag, Pill, Label, Keyword, Facet.

## 11. Implementation notes
- **The grid-pattern removable group (the substrate worth owning).** Implement `TagGroup` as `role="grid"` (single tab stop in, roving focus across rows), each tag a `row` with content + remove `gridcell`s; Left/Right (Up/Down for wrapped) arrow between tags, Delete/Backspace removes the focused tag. This is React Aria's reference shape; don't hand-roll a flat list of buttons.
- **The focus-management-after-removal algorithm** — on remove: focus the next tag → else the previous → else the group/input. Capture the index before removal; after the list updates, resolve the new focus target (a `useEffect`/post-render focus call, since the removed node is gone). The single most-missed Tag detail.
- **The embedded-button target-size trap** — the `×` inside a small tag must hit 24×24 (2.5.8) / ideally 44×44 (2.5.5) via hit-slop padding/pseudo-element expansion, not by enlarging the visible glyph (which would unbalance the tag). A recurring audit failure.
- **The whole-tag-vs-× click handling** — when the whole tag is clickable *and* has a remove `×`, stop the `×`'s click from bubbling to the tag's `onClick` (clicking remove shouldn't also fire the tag action). The nested-interactive (button-in-a-button) HTML-validity problem: a clickable tag can't be a `<button>` containing a remove `<button>` — use the grid pattern (row + cells) or a non-button clickable container with two real buttons inside.
- **Backspace-removes-last-token** — in a token input, Backspace at an empty caret removes the last token and (optionally) puts its text back into the input for editing; guard against removing on every keypress.
- **Truncation + overflow** — per-tag `max-width` + ellipsis + `title`; the group's **"+N more"** collapse (a popover/expander of the remaining tags) or wrap-vs-scroll, decided by the container (a search bar wraps; a single-line cell collapses to "+3").
- **The token-field composition with Combobox** — the multi-select Combobox renders its value as a `TagGroup` of input chips inside the field; the combobox owns the input + listbox, the tag group owns the token display + removal (see combobox). Keep the two concerns separate.
- **Headless vs opinionated** — the grid keyboard pattern, focus-management, and the selection model are the headless substrate worth owning (React Aria/Spectrum); the fill/tone/shape is theme. Ship the *group* logic, theme the *tag*.

## 12. Related and alternative components
- **Stands on:** **Icon** (the leading icon + the remove `×` glyph — see icon) and **Button** (the embedded remove control is an icon button with its own accessible name — see button).
- **Composed by:** the multi-select **Combobox** (the token-input field renders Tags as input chips — see combobox; closes the "token-vs-checkbox multi-select split" that brief named).
- **Borders (selection):** **Checkbox** (the filter chip = lightweight inline multi-select — see checkbox) and **Radio** (the choice chip = single-select — see radio); **Toggle Button** (the `aria-pressed` filter-toggle alternative — see toggle-button).
- **Boundary:** **Badge** — the passive, non-interactive indicator (the Tag-vs-Badge line, drawn from Badge's side — see badge).
- **Inherits (pattern):** the **color-not-sole-carrier severity model** (Badge/Banner — where a tag encodes status by color — see badge, banner).
- **Alternative to:** a **Button** (for a true/primary action), a **Checkbox/Radio group** (for a structured form choice).

## 13. Field POV evolution
1. **Material's four-chip taxonomy settling.** Material 3 hardened the assist/filter/input/suggestion split, giving the field a shared genre vocabulary over the older single "Chip" blob — the same maturation Badge's tripartite split shows.
2. **The removable-tag-group GRID pattern hardening.** React Aria / Spectrum's `TagGroup`-as-`grid` (row/gridcell, arrow-nav, Delete/Backspace, focus-management-after-removal) emerged as the settled accessibility answer to the two-interactive-things problem, displacing ad-hoc flat-list-of-buttons implementations.
3. **Target-size raising the remove-button bar.** WCAG 2.2's 2.5.8 (Target Size Minimum, 24×24) made the tiny embedded `×` an explicit conformance issue, forcing hit-slop discipline.
4. **The Badge-vs-Tag clarification.** The field increasingly separates the passive indicator (Badge/Label) from the interactive/removable token (Tag/Chip), reversing the older tendency to conflate them.
5. **Naming hasn't converged** — Chip (Material/MUI/Carbon) vs Tag (Ant/Polaris/Spectrum) vs Token (Primer) persists; the practice picks `Tag` + `TagGroup` and treats the rest as aliases.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- Google Material 3 — `Chip` (the canonical assist / filter / input / suggestion four).
- MUI — `Chip` (filled/outlined, `clickable`, `onDelete`, `avatar`/`icon`).
- Ant Design — `Tag` (`closable`/`onClose`, `CheckableTag`, presets/status).
- Shopify Polaris — `Tag` (removable, disabled, clickable forms).
- GitHub Primer — `Token` / `AvatarToken` / `IssueLabelToken` (the Token family + remove button).
- Microsoft Fluent — `Tag` / `InteractionTag` + `TagGroup` (dismissible).
- Adobe Spectrum / React Aria — `TagGroup` (the grid pattern; removable; the focus-management-after-removal reference).
- IBM Carbon — `Tag` (read-only / dismissible / selectable / operational / filter).
- Chakra UI — `Tag` (+ `TagCloseButton` / `TagLeftIcon`).
- Base Web (Uber) — `Tag`.
- Atlassian — `Tag` (removable / linked).
- WAI-ARIA APG — no formal tag/chip pattern; the **grid pattern** for a removable token list; **listbox**/**radiogroup** for selection chips; **button** for action chips.
- WCAG 2.2 — 2.1.1, 2.4.3, 2.5.5, 2.5.8, 1.4.1, 4.1.2.

## 15. Agent-consumable schema
```yaml
identity:
  id: tag
  name: Tag
  aliases: [Chip, Token, AvatarToken, IssueLabelToken, InteractionTag, Pill, Label, Keyword, Facet]
  category: foundations
  status: stable
description: >
  The interactive/removable token — the active counterpart to Badge (the passive
  indicator). Spans three interaction archetypes: ACTION (assist/suggestion chips —
  behave like a Button), SELECTION (filter = multi-select toggle, borders Checkbox;
  choice = single-select, borders Radio), and INPUT/TOKEN (removable tokens in a
  field, composed by the multi-select Combobox). Material's four chips
  (assist/filter/input/suggestion) + the standalone read-only metadata tag. NOT a
  Badge (passive, non-interactive, non-removable — the boundary: onClick/×/selected
  ⇒ Tag), NOT a primary Button, NOT a structured-form Checkbox/Radio. Naming morass:
  Chip (Material/MUI/Carbon) vs Tag (Ant/Polaris/Spectrum) vs Token (Primer).
anatomy:
  parts:
    - "tag body (filled/outlined surface; the hit target when the whole tag is interactive)"
    - "leading icon/avatar/dot (inherits Icon; a selected filter/choice chip swaps it for a checkmark)"
    - "label (short; truncates with ellipsis + full text on hover/title)"
    - "trailing remove × (removable/input only): an EMBEDDED icon button with its OWN accessible name 'Remove [label]' (inherits Button + Icon) — one tag = two operable things"
    - "selected indicator (filter/choice): checkmark / fill / outline->filled; never color alone"
    - "hit-target structure: whole-tag clickable (action/filter) with × nested, vs only-the-× (read-only removable token)"
api:
  inherits:
    - icon              # leading icon + the remove × glyph
    - button            # the embedded remove control is an icon button
    - combobox          # composed-by: the multi-select token field renders Tags
    - badge/banner      # color-not-sole-carrier severity (where a tag encodes status)
  props:
    - {name: label, type: "string | node", default: ~, required: true, description: "the token text"}
    - {name: variant/genre, type: "'assist' | 'filter' | 'input' | 'suggestion'", default: input, required: false, description: "the genre; maps to the action/selection/input archetype (often expressed as clickable/onDelete booleans, not one enum)"}
    - {name: selected, type: boolean, default: false, required: false, description: "filter/choice toggle state (aria-selected); Ant CheckableTag"}
    - {name: onRemove/onDelete, type: function, default: ~, required: false, description: "the remove handler; its presence renders the × and makes the tag removable (MUI onDelete, Ant closable/onClose)"}
    - {name: onClick, type: function, default: ~, required: false, description: "the action handler (assist/suggestion/filter body)"}
    - {name: disabled, type: boolean, default: false, required: false, description: "non-operable; still announced"}
    - {name: leadingIcon/avatar, type: node, default: ~, required: false, description: "leading adornment (icon/avatar/dot)"}
    - {name: size, type: "'small' | 'medium' | 'large'", default: medium, required: false}
    - {name: tone/color, type: "'neutral' | 'info' | 'success' | 'warning' | 'error'", default: neutral, required: false, description: "semantic tone where a tag encodes status; color + text never color alone"}
    - {name: fill, type: "'filled' | 'outlined'", default: filled, required: false}
    - {name: removable, type: boolean, default: false, required: false}
    - {name: remove-accessible-name, type: wiring, default: ~, required: true, description: "the embedded × needs its OWN name composed from the label ('Remove Marketing'), not a bare 'Remove'/'×'"}
  group: "TagGroup/ChipSet/token-field — owns the selection model (single/multi), the grid keyboard nav, and focus-management-after-removal. The real API lives on the GROUP"
states:
  runtime: [default, hover, focus, active, selected, unselected, disabled, removing]   # interactive — unlike Badge; the × has its own nested hover/focus
variants:
  genre: [assist, filter, input, suggestion, read-only]
  archetype: [action, selection, input]
  selection: [selected, unselected]        # filter=multi, choice=single
  removable: [removable, static]
  tone: [neutral, info, success, warning, error]
  fill: [filled, outlined]
  size: [small, medium, large]
  adornment: [leading-icon, avatar, dot, none]
accessibility:
  inherits: [badge/banner (color-not-sole-carrier)]
  wcag-criteria: ["2.1.1", "2.4.3", "2.5.5", "2.5.8", "1.4.1", "4.1.2"]
  removable-group-GRID: "the settled pattern (React Aria/Spectrum TagGroup): role=grid, each tag a row, content + remove are gridcells; single tab stop in + roving arrow nav between tags; Delete/Backspace on a focused tag removes it"
  focus-after-removal: "move focus to the NEXT tag -> else the PREVIOUS -> else the group/input; NEVER drop to <body> (the classic bug; WCAG 2.4.3)"
  selection-roles:
    filter-multi: "listbox aria-multiselectable + options (aria-selected), or button[aria-pressed] toggles"
    choice-single: "radiogroup of radios (the Radio keyboard model)"
    action: "plain buttons (assist/suggestion; no selected state)"
  remove-button-name: "the × has its own aria-label='Remove [label]', not 'Remove'/'Close'/'×' (4.1.2)"
  hit-target: "whole-tag operable (action/filter) with × nested, vs only-the-× (read-only removable)"
  backspace-removes-last: "in a token input, Backspace at an empty caret removes the last token; not the ONLY removal path"
  target-size: "the embedded × must hit 24x24 (2.5.8 AA) / 44x44 (2.5.5 AAA) via hit-slop padding, NOT a bigger glyph (the recurring trap)"
content:
  label: "1-3 words; truncate past max-width with ellipsis + full text in title/tooltip"
  remove-name: "'Remove [label]', never bare 'Remove'/'×'"
  casing: "sentence case (or preserve user-entered casing); consistent across the set"
  trap: "don't overload — one token of meaning per tag (not label+count+status+two icons)"
  tag-vs-badge: "Tag content is user/data-driven + actionable (a removable filter/recipient/category); Badge is system-driven + passive (a count/status)"
motion:
  remove: "the tag collapses out (scale/opacity + width) + the GROUP REFLOWS to close the gap (~150ms; animate transform not layout)"
  add: "a new token scales/fades in"
  selected: "brief fill/checkmark transition"
  reduce-motion: "drop the collapse/reflow to an instant remove (the state change is the information, not the motion)"
i18n:
  rtl: "the remove × flips to the leading (inline-start) edge + the leading icon to trailing; logical properties (padding-inline/inset-inline), no JS"
  label-expansion: "translated labels run longer; max-width + ellipsis holds + title carries the full text; don't hardcode widths"
  token-field-wrap: "a token field wraps to multiple lines (or scrolls), respecting the RTL flow direction"
implementation:
  - "the GRID-pattern removable group (React Aria reference): role=grid, single tab stop + roving focus across rows, content + remove gridcells, arrow-nav + Delete/Backspace; don't hand-roll a flat list of buttons"
  - "focus-management-after-removal: capture the index before removal; after the list updates, focus next->previous->group/input (post-render focus call, the removed node is gone). The single most-missed detail"
  - "embedded-button target-size: the × hits 24x24/44x44 via hit-slop padding/pseudo-element, NOT a bigger glyph"
  - "whole-tag-vs-×: stop the ×'s click bubbling to the tag's onClick; a clickable tag CAN'T be a <button> containing a remove <button> (nested-interactive invalid) — use the grid (row + cells) or a non-button container with two real buttons"
  - "Backspace-removes-last-token in a token input (optionally restoring the text for editing); guard against removing every keypress"
  - "truncation + overflow: per-tag max-width + ellipsis + title; the group's '+N more' collapse (popover) or wrap-vs-scroll, decided by the container"
  - "token-field composition: the multi-select Combobox renders its value as a TagGroup of input chips; combobox owns input+listbox, tag group owns token display+removal (keep separate)"
  - "headless vs opinionated: ship the GROUP logic (grid keyboard, focus-mgmt, selection model) headless; theme the TAG (fill/tone/shape)"
composition:
  stands-on: [icon, button]
  composed-by: [combobox]                  # the multi-select token field
  borders: [checkbox, radio, toggle-button]   # filter=multi / choice=single / pressed-toggle
  alternative-to: [button, checkbox, radio]   # true action / structured form choice
  boundary: [badge]                        # the passive indicator (the Tag-vs-Badge line)
  inherits-pattern: [badge, banner]        # color-not-sole-carrier severity
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "one Tag + archetype booleans (onClick/onDelete/selected) vs separate components per genre (Material's four chips; Primer's Token/AvatarToken/IssueLabelToken) — the practice picks one Tag + a TagGroup that owns selection"
    - "filter chips as listbox(option/aria-selected) vs button[aria-pressed] toggles"
    - "naming: Chip (Material/MUI/Carbon) vs Tag (Ant/Polaris/Spectrum) vs Token (Primer) — unconverged"
    - "whole-tag clickable vs only-the-× per genre"
  trap:
    - "dropping focus to <body> after removing a tag (the focus-management-after-removal failure)"
    - "the embedded × failing target size (2.5.8/2.5.5) inside a small tag"
    - "nested-interactive: a clickable <button> tag containing a remove <button> (invalid HTML) — use the grid pattern"
    - "the ×'s click bubbling to the tag's onClick (remove also fires the action)"
    - "a bare 'Remove'/'×' accessible name instead of 'Remove [label]'"
    - "color-as-sole-carrier for status tags (1.4.1)"
    - "using a Tag for a passive indicator (-> Badge) or a primary action (-> Button) or a structured form choice (-> Checkbox/Radio)"
  inherited:
    - "Icon + Button substrates"
    - "color-not-sole-carrier severity (badge/banner)"
    - "composed by the multi-select Combobox token field"
  role-in-family: "the interactive/removable token — the active counterpart to Badge; stands on Icon+Button, composed by the multi-select Combobox, borders Checkbox/Radio, hard boundary with Badge"
  evolution:
    - "Material's four-chip taxonomy settling (assist/filter/input/suggestion)"
    - "the removable-tag-group GRID pattern hardening (React Aria/Spectrum TagGroup — grid/row/gridcell + Delete/Backspace + focus-mgmt-after-removal)"
    - "WCAG 2.2 target-size (2.5.8) raising the remove-button bar"
    - "the Badge-vs-Tag clarification (passive indicator vs interactive/removable token)"
    - "naming unconverged (Chip vs Tag vs Token)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "the React Aria TagGroup grid-pattern role details — verify against the current Spectrum/APG implementation"
```
