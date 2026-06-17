---
okf_version: "0.1"
type: component-brief
title: Tag
description: The interactive/removable token — the active counterpart to Badge. A field-truth study of the genre split (Material's assist/filter/input/suggestion four chips + Carbon's read-only/dismissible/selectable/operational matrix) collapsing to three interaction archetypes (action/selection/input), the naming morass (Chip vs Tag vs Token), the Badge-vs-Tag boundary from Tag's side, the removable-tag-group GRID accessibility pattern (role=grid/row/gridcell + Delete/Backspace + the focus-management-after-removal contract, never drop to body) and why listbox is prohibited, the selection roles (listbox/radiogroup) + action=button, the remove/dismiss contract + the embedded-button target-size trap (2.5.8), the display:contents grid fix, the token-field composition with the multi-select Combobox + the Backspace-removes-last convention, and truncation/overflow (+N more) — with the practice's defaults.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [Chip, Token, AvatarToken, IssueLabelToken, InteractionTag, CheckableTag, Pill, Label, Keyword, Facet, Lozenge]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Tag

> A Tag is the **interactive / removable token** — the active counterpart to Badge (the passive indicator). Where a Badge *informs* (it's `aria-hidden`-on-a-host or announces its own static text), a Tag is focusable and operable: the user clicks it, toggles it, or removes it. The headline problem — exactly parallel to Badge — is that **"Tag" / "Chip" / "Token" name overlapping but distinct genres**, canonically Material 3's four chips (**assist**, **filter**, **input**, **suggestion**) plus the standalone read-only metadata tag, which collapse to **three interaction archetypes**: **action** (assist/suggestion → a **Button**), **selection** (filter = multi-select toggle → borders **Checkbox**; choice = single-select → borders **Radio**), and **input/token** (removable tokens in a field → composed by the multi-select **Combobox**). It stands on **Icon** (the leading adornment + the remove `×` glyph — see icon) and **Button** (the embedded remove control is an icon button with its own accessible name — see button), is **composed by the multi-select Combobox** (the token field renders Tags — see combobox), and inherits the **color-not-sole-carrier severity model** where a tag encodes status (see badge, banner). What it **isn't**: a **Badge** (the passive, non-interactive, non-removable indicator — the boundary from Tag's side: if it has an `onClick`, a remove `×`, or a selected state, it's a **Tag**; if it's a read-only count/dot/status, it's a Badge — see badge). The accessibility crux is the **removable-tag-group GRID pattern** (`role=grid`/`row`/`gridcell` + arrow-nav + Delete/Backspace + the focus-management-after-removal contract) — the settled answer to the *one tag = two interactive things* problem.

---

## 1. Framing
A Tag occupies a contested liminal space: a polymorphic token reconciling three interaction archetypes, which is exactly why systems disagree on how to model it. The defining boundary — drawn from Tag's side — is **interactivity and removability**. If a container purely encodes a count, a status, or a read-only categorization, it is a **Badge** (Atlassian's *Lozenge*). The moment the user can *do* something to it — dismiss it, toggle its selection, trigger its action, remove it from a field — it is a **Tag**.

The genre taxonomy stabilized around **Material 3's four chips**: **assist** (a transient contextual action — "Add to calendar" — acts like a localized Button), **filter** (a toggleable multi-select state — "Weekend", "Under $50" — borders Checkbox), **input** (a user-authored, **removable** token in a field — recipients, applied filters — the genre the Combobox composes), and **suggestion** (a dynamically-generated prompt/recommendation — acts like a button/link). **IBM Carbon** operationalizes the same split as a variant matrix — **read-only** (categorizing), **dismissible** (removal), **selectable** (toggling), **operational** (disclosing overflow via a popover). Both collapse to the three macro archetypes: **action / selection / input**.

The naming morass: **Material / MUI / Polaris** standardize on **Chip** (Material as the umbrella for all four genres); **Carbon / Ant / Chakra / Atlassian** converge on **Tag**; **GitHub Primer** uses **Token** (`Token` / `AvatarToken` / `IssueLabelToken`) to emphasize the data-payload role; **Fluent** splits by interactivity — a passive categorizer is a `Tag`, an interactive one is an `InteractionTag` (+ `TagGroup`). Why systems disagree: the genre model + naming, and the removable-tag accessibility pattern, which was genuinely unsettled until recently (§6).

## 2. Anatomy and parts
A fully-featured removable Tag has up to five slots in a tightly constrained 24–32px height, demanding precise flex orchestration:
- **the substrate (container)** — the bounding box: radius, fill, padding, the stateful visual shifts (hover/focus/active), and the focus-ring projection. The primary hit target *when the whole tag is interactive*.
- **the leading affordance (optional)** — an icon, avatar (Primer's `AvatarToken`), or status dot for at-a-glance categorization (inherits Icon — see icon).
- **the label (core substance)** — the short text descriptor; truncates with ellipsis + full text on hover/`title` (§7).
- **the selected indicator (stateful)** — typically an animated checkmark that replaces or precedes the leading slot when a filter/choice tag toggles active; never color alone (§6).
- **the trailing affordance (action)** — the remove `×`, functionally an **embedded icon button** with its *own* accessible name ("Remove [label]") inheriting Button + Icon (see button, icon). The source of the accessibility complexity: one tag = two operable things.
- **the hit-target structure** — the load-bearing anatomical decision. A **dual-action** tag (click the body to select *and* click the `×` to remove) makes the body and the `×` two distinct focusable DOM elements, requiring event-propagation management so the `×` click doesn't also fire the body's `onClick`. A **removal-only** tag (the Combobox-token default) should **merge the hit targets** — the whole substrate is the remove action, which immediately resolves the target-size constraint (no surgical click on a 16px glyph). Chakra exposes this via the `TagCloseButton` compound part.

## 3. Properties / API
The API exposes a real ideological divide: rigid boolean-driven monolithic APIs (developer speed) vs composable nested-component APIs (flexibility + accessibility).

- **`label` / children** (`ReactNode`, required) — the text; accepting a node (not a strict string) allows localized formatting and custom truncation.
- **`onClick` / `onAction`** — triggers the action archetype (assist/suggestion); wires the body as a button.
- **`onRemove` / `onDelete`** — instantiates the `×`. **The API divergence:** MUI uses **callback-detection** — the `×` renders *iff* `onDelete` is supplied (elegant: a tag can't *look* removable without the logic to remove). Polaris / Spectrum / **React Aria decouple** the visual `removable`/`isRemovable` boolean from the handler — necessary for controlled/uncontrolled state machines and the case where a tag is also a navigational link (`href`) but removal runs through a higher-order manager. The practice leans toward callback-detection for the common case, decoupled where the group owns removal state.
- **`selected` / `defaultSelected`** — the filter/choice toggle. Ant isolates this in a separate `<CheckableTag>` to keep the state machine off the core component.
- **`leadingIcon` / `avatar`** — the leading slot (Primer splits `AvatarToken` out).
- **`disabled` vs `readOnly`** — *distinct*: `disabled` strips interactivity **and dims contrast**; `readOnly` **preserves full visual weight** but rejects interaction (immutable legacy filters, audit logs, finalized documents). (Spectrum warns against disabling a whole `TagGroup` — if nothing in it is operable, **hide the group** rather than dimming it all.)
- **`size`** — sm / md / lg (vertical footprint + type scale).
- **`tone` / `color` / `variant=filled|outlined|subtle`** — visual weight + the semantic tone where a tag encodes status (color + text, never color alone — §6).
- **the remove button's accessible-name wiring** — not a style prop but load-bearing: the `×` needs its own name composed from the label ("Remove Marketing"), not a bare "Remove"/"×" (§6).
- **the group:** `TagGroup` / `ChipSet` / token-field — owns the selection model (single/multi), the grid keyboard nav, the overflow algorithm, and focus-management-after-removal. **The real API lives on the group**; a lone tag is half the story.

## 4. States and variants
- **States:** **rest** (label/background must hold ≥3:1 against the app background), **hover**, **focus-visible** (the ring wraps the whole container for action/selection tags; for split-target removable tags it illuminates *only* the `×` when the remove action has keyboard focus), **active/pressed**, **selected** (filter/choice — a high-contrast fill + checkmark), **disabled** (low contrast, no pointer events), **read-only** (full contrast, no interaction — distinct from disabled), and the transient **removing**.
- **Variants:**
  - **genre / archetype:** assist / filter / input / suggestion (→ action / selection / input); Carbon's read-only / dismissible / selectable / operational matrix.
  - **selection:** selected vs unselected (filter = multi; choice = single).
  - **removable** vs static/read-only; **clickable/action** vs display-only.
  - **tone:** neutral + the semantic palette (info/success/warning/error) for status-encoding tags.
  - **fill:** filled / outlined / subtle.
  - **size:** sm / md / lg.
  - **adornment:** leading icon / avatar / dot / none; trailing remove / none.

## 5. Usage guidance
- **Use a Tag (interactive/removable token) for:** applied filters/facets the user can see and remove (input chips in a search bar — the canonical case); a lightweight inline multi-select (filter chips) where a checkbox group would be heavy; free-text/entity tokens entered into a field (recipients, labels — composed by the Combobox); contextual smart actions (assist/suggestion chips).
- **Don't use a Tag for:**
  - A **passive indicator** (a count, a status you can't act on) → a **Badge** (see badge). The test: no `onClick`, no `×`, no selected state ⇒ Badge.
  - A **primary / page-level action** → a **Button** (see button). An assist chip is for *transient, localized, plural* actions inline with content ("Reply: Sounds good"), never the page's main CTA ("Submit"/"Save").
  - A **static, exhaustive, vertical list of boolean choices** → a **Checkbox** group (see checkbox). Filter chips are for *horizontal, space-constrained, reflowing, dynamically-subsetted* options.
  - **Keyboard text entry** → Tags don't handle text input; they're the rendered tokens a multi-select **Combobox** produces (see combobox).
- **Decision frameworks:**
  - **Filter chips vs a checkbox group:** few, scannable, horizontal, inline, immediate-effect, space-constrained → chips; many, grouped, labelled, part of a form submission → checkboxes.
  - **Assist chip vs Button:** primary/page-level → Button; contextual/plural/transient/inline → assist chip.
  - **The Badge-vs-Tag test (from Tag's side):** can the user act on it (click/toggle/remove)? Yes → Tag; no → Badge.
- **Reflow vs overflow (the group's two settled patterns):** **Reflow** — the group wraps indefinitely to new lines, pushing content down (when seeing all tags matters). **Menu/overflow** — the group stays single-line, terminating in a computed **"+N more"** operational tag that opens a popover of the rest (constrained spaces: table cells, compact headers).

## 6. Accessibility
**The crux, and the field now has a settled answer.** The WAI-ARIA APG defines no formal tag/chip pattern; the component maps to existing ARIA paradigms **by interaction archetype**.

**The removable tag group is a GRID — not a listbox.** For years engineers forced removable token lists into `role="listbox"`; this is a hard violation, because ARIA **prohibits interactive elements (the embedded `×` button) inside a `role="option"`**. The settled reference implementation (Adobe React Aria / Spectrum `TagGroup`) renders the removable group as a **grid**:
- the container is **`role="grid"`**; each tag is a **`role="row"`**; the tag body/label is a **`gridcell`** and the remove button sits in an adjacent **`gridcell`** in the same row.
- a **single tab stop** enters the group, then **Left/Right arrows** rove between tags (Up/Down for wrapped rows), and **Delete/Backspace on a focused tag removes it** — no drilling into the inner button via extra tab stops.

**Focus management after removal (the load-bearing rule, the classic bug).** A removed node without programmatic intervention drops focus to `<body>`, dumping the screen-reader user at the top of the document. The settled contract: on remove, focus the **next** tag → else the **previous** → else the **group container / Combobox input / a designated fallback**. **Never `<body>`.** (Atlassian explicitly mandates this focus-return contract.)

**The selection genres take different roles** (no embedded remove, so no grid):
- **filter (multi-select)** → `listbox` + `aria-multiselectable`, or an array of `role="checkbox"`, or native `<button>` + `aria-pressed`.
- **choice (single-select)** → a `radiogroup` (the Radio "1 of X" keyboard model — see radio).
- **assist / suggestion (action)** → plain native `<button>` (or `role="button"` + Enter/Space — see button).

**The remove button's accessible name** — context-aware, interpolating the label: `aria-label="Remove Marketing"`, not a bare "Remove"/"Close"/"×" (a generic SVG with no name fails 1.1.1). The DRY alternative: `aria-label="Remove"` + `aria-labelledby` referencing the tag's text-node id.

**Target size (the embedded-`×` trap, WCAG 2.5.8).** A 16px `×` dropped into a 24–32px tag mathematically fails the 24×24 CSS-px minimum. The fix isolates the `×` in a real `<button>` and expands its footprint with **internal transparent padding** to 24×24 (ideally 44×44 for 2.5.5 AAA) — **padding on the button, not margin** (margin doesn't grow the hit area), and without enlarging the visible glyph.

**Color-not-sole-carrier** — a status-encoding tag pairs color with text (and optionally a leading icon), inheriting the Badge/Banner severity rule (see badge, banner); a color-only tag set fails 1.4.1.

**WCAG SCs:** **2.1.1** (keyboard — operate + remove), **2.4.3** (focus order — the after-removal contract), **2.5.5 / 2.5.8** (target size — the `×`), **1.4.1** (color not sole carrier), **1.1.1 / 4.1.2** (the remove button's name, the selected state).

## 7. Content guidelines
- **Brevity** — a single word where possible; two-to-three short words only for a specific entity (a full name, an email, a complex category). A tag is a token, not a sentence.
- **Casing** — sentence case is the standard (avoid all-caps shouting and all-lowercase informality); or preserve user-entered casing; consistent across the set.
- **The remove button's name** — "Remove [label]", composed from the tag, never a bare "Remove"/"×".
- **Truncation** — past the systemic `max-width`, force `text-overflow: ellipsis` + `overflow: hidden` + `white-space: nowrap`, **always paired** with a native `title` or a portal tooltip revealing the full string on hover/focus, so no data is permanently obscured. (Tags are the most common site of component-level truncation in enterprise UI.)
- **The Tag-vs-Badge content distinction** — don't inject systemic status language ("Failed", "Processing") into an interactive Tag; reserve that vocabulary for read-only Badges. A Tag's content is user/data-driven and actionable (a removable filter/recipient/category); a Badge's is system-driven and passive.

## 8. Motion and transition
- **Remove / dismiss** — snapping a tag out of the DOM creates a jarring layout shift; the preferred exit is dual-phase: a rapid **opacity fade** (the action executed) then a **height/width/margin collapse**, so sibling tags glide into the freed space — often via **FLIP** (First-Last-Invert-Play) to hold 60fps.
- **Add** — a subtle scale-up (90%→100%) + fade-in draws the eye to the new token.
- **Selected** — a rapid background cross-fade + a micro-scale-in of the checkmark.
- **Reduce-motion** — gate all scale/translate/collapse behind `prefers-reduced-motion: reduce`, falling back to instant opacity shifts (the state change is the information, not the motion).

## 9. Internationalization
- **Anatomical flipping (RTL)** — the leading icon/avatar moves to the right edge, the label aligns right, the remove `×` moves to the left (inline-start) edge — achieved with flex defaults + **CSS logical properties** (`padding-inline-start`, `margin-inline-end`), never hardcoded physical directions, so it mirrors off `dir="rtl"` with no JS.
- **Label expansion** — German/Russian/Romance translations run 30–50% longer; the container must never have a fixed physical width — intrinsic content sizing up to an engineered `max-width`, then the truncation rules (§7).
- **Token-field wrapping** — tags expanding within a Combobox field must wrap to multiple lines without fracturing the gap spacing between tokens and the text cursor, respecting the RTL flow direction.

## 10. Naming
- **The field set:** Material / MUI / Polaris `Chip`; Carbon / Ant / Chakra / Atlassian `Tag`; GitHub Primer `Token` (`Token` / `AvatarToken` / `IssueLabelToken`); Fluent `Tag` (passive) / `InteractionTag` (interactive) + `TagGroup`; Chakra's compound `Tag` / `TagLabel` / `TagCloseButton`.
- **The practice's default — `Tag`** as the primary component identifier. "Tag" communicates categorization/metadata/filtering and aligns with database/CMS terminology, without Material "Chip"'s proprietary overtones. **`TagGroup`** is the container owning selection, the grid keyboard pattern, overflow, and focus-management-after-removal. Expose the genres via the **interaction archetype** (a `Tag` that is *removable* via `onRemove`, *selectable* via `selected` within a `TagGroup`'s selection mode, or *actionable* via `onClick`) rather than four lookalike components; Material's assist/filter/input/suggestion are useful *documentation* genres mapped onto this.
- **Aliases / disambiguation:** **`Token`** is the systemic alias when a Tag is composed inside a Combobox/MultiSelect (a typed-then-tokenized payload). **`Pill`** is an outdated *visual* descriptor (the `border-radius: 9999px` aesthetic) — naming a component after a current shape is an anti-pattern that breaks when the radius changes; **deprecate it**. **`Badge`** is aggressively disambiguated as the passive, non-interactive sibling (see badge). Other aliases to map: `CheckableTag`, `InteractionTag`, `AvatarToken`, `IssueLabelToken`, `Lozenge`, `Label`, `Keyword`, `Facet`.

## 11. Implementation notes
- **The grid DOM + the `display: contents` fix (the non-obvious one).** The grid pattern's rigid `row`/`gridcell` wrappers fight CSS `flex-wrap` — semantic rows refuse to break inline, breaking the visual layout. React Aria's late-2023 resolution: apply **`display: contents`** to the `role="row"` / `role="gridcell"` wrappers, removing them from the CSS box tree so the visual tag elements participate directly in the outer `TagGroup`'s flex/grid layout — flawless horizontal wrapping while preserving the exact multi-tiered DOM the screen-reader API needs.
- **The focus-management-after-removal algorithm** — capture the index before removal; after the list updates (the removed node is gone), focus next → previous → group/input in a post-render focus call. The single most-missed Tag detail.
- **The target-size padding trap** — apply `padding` to the interactive `<button>` housing the `×` to expand the hit surface to 24×24 (the SVG stays optically small); **never `margin`** (it doesn't grow the clickable area). A recurring 2.5.8 audit failure.
- **The whole-tag-vs-`×` click handling** — when the body is clickable *and* removable, stop the `×`'s click bubbling to the body's `onClick`. The HTML-validity constraint: a clickable tag **can't** be a `<button>` containing a remove `<button>` (nested interactives are invalid) — use the grid (row + cells) or a non-button clickable container with two real buttons inside.
- **Field composition with the Combobox** — the multi-select Combobox renders its value array as a `TagGroup` of input chips inside the field; the combobox owns the input + listbox, the tag group owns the token display + removal. **The Backspace convention:** at an empty caret, Backspace **highlights/focuses the last token**; a second Backspace deletes it (guard against deleting on every keypress). This needs a focus manager that roves between the text-input cursor and the adjacent tag elements (precise `ref` management + synthetic-event interception).
- **Overflow "+N more" needs JS, not CSS** — a `ResizeObserver` measures the container's available width against the accumulated tag widths, slices the overflow, and appends a computed **"+N" operational tag** wired to a Popover of the hidden items (Fluent's overflow-tag pattern). The slice fluctuates with async web-font loading — flagged below.
- **Headless vs opinionated** — ship the **group** logic headless (the grid keyboard pattern, focus-management, selection model, overflow); theme the **tag** (fill/tone/shape). The field is moving toward Combobox + TagGroup + Tag coordinating via Context, away from monolithic `TagInput`/`TextInputWithTokens` files (Primer deprecated `TextInputWithTokens` for accessibility reasons).

## 12. Related and alternative components
- **Stands on:** **Icon** (the leading adornment + the remove `×` glyph — see icon) and **Button** (the embedded remove control is an icon button with its own accessible name — see button).
- **Composed by:** the multi-select **Combobox** (the token-input field renders Tags as input chips — see combobox; the Tag is the visual manifestation of the Combobox's selected-value array, closing the "token-vs-checkbox multi-select split" that brief named).
- **Borders (selection):** **Checkbox** (the filter chip = lightweight inline multi-select — see checkbox), **Radio** (the choice chip = single-select — see radio), **Toggle Button** (the `aria-pressed` filter-toggle alternative — see toggle-button).
- **Boundary:** **Badge** (Atlassian's *Lozenge*) — the passive, non-interactive indicator; the moment a status/count gains a remove/toggle/click affordance it morphs into a Tag (the Tag-vs-Badge line — see badge).
- **Inherits (pattern):** the **color-not-sole-carrier severity model** (where a tag encodes status — see badge, banner).
- **Alternative to:** a **Button** (a true/primary action), a **Checkbox/Radio** group (a structured form choice).

(A Foundations primitive — the interactive/removable token, the active counterpart to Badge. It stands on Icon + Button, is composed by the multi-select Combobox, borders Checkbox/Radio/Toggle Button, and holds the hard boundary with Badge. See icon/button for the substrates, combobox for the token-field composer, checkbox/radio for the selection borders, badge for the passive-indicator boundary, banner for the inherited severity pattern. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The taxonomy settling.** The old badge/pill/label/tag confusion largely resolved through Material 3's four-chip archetype taxonomy — the field now recognizes that *visual shape* (rounded corners) doesn't define the component, the *interaction archetype* does.
2. **The accessibility hardening — the GRID pattern.** React Aria / Spectrum's `role="grid"` removable-token pattern (formalized against the APG layout-grid guidance) deprecated the legacy inaccessible `listbox` implementations and `div`-soup + `tabindex` hacks, and the `display: contents` fix (late 2023) made it layout-compatible.
3. **Target-size elevation.** WCAG 2.2's 2.5.8 (24×24) forced a re-engineering of embedded remove-icon hit areas, ending the over-compact tags of the 2010s.
4. **The Badge-vs-Tag clarification.** The field separated the passive indicator (Badge/Lozenge) from the interactive token (Tag/Chip/InteractionTag) — Fluent's `Tag`/`InteractionTag` split is the clearest naming expression.
5. **The decline of monolithic inputs.** Systems moved away from massive `TagInput`/`TextInputWithTokens` components (Primer deprecated `TextInputWithTokens` over accessibility) toward headless, compositional Combobox + TagGroup + Tag coordinating via Context. (Polaris's recent move to `<s-chip>`/`<s-clickable-chip>`, 2025-10, is the same compositional turn — flagged unverified.)

## 14. Sources cited
(Conservative; reconcile with external.) **Google Material 3** — `Chip` (the canonical assist/filter/input/suggestion four; 88dp widths / 48×48 hit targets) (2024–2026); **Adobe React Aria / Spectrum** — `TagGroup`/`Tag` (the `role="grid"` pattern, the focus-management-after-removal algorithm, the `display: contents` grid fix; React Aria ~3.49) (2023–2026); **MUI** — `Chip` (the `onDelete` callback-detection API; filled/outlined; `clickable`) (2024–2026); **IBM Carbon** — `Tag` (the read-only / dismissible / selectable / operational matrix; v11) (2024–2026); **Microsoft Fluent UI v9** — `Tag` / `InteractionTag` + `TagGroup` (the interactivity-based split; the "+N" overflow tag) (2024–2026); **GitHub Primer** — `Token` / `AvatarToken` / `IssueLabelToken` (the data-payload nomenclature; deprecated `TextInputWithTokens` for accessibility) (2024–2026); **Ant Design** — `Tag` / `CheckableTag` (the selection state machine isolated in a distinct component; presets/status; v5) (2024–2026); **Shopify Polaris** — `Chip` / `Clickable Chip` (`<s-chip>`/`<s-clickable-chip>`, the recent deprecation of the legacy `Tag`; `removable` boolean; 2025-10) (2025–2026); **Atlassian Design** — `Tag` (the mandated focus-return contract — never drop to `<body>`); **Chakra UI** — `Tag` / `TagLabel` / `TagCloseButton` (the compound-component slot API) (2024–2026); **Base Web (Uber)** — `Tag` (2024); **WAI-ARIA APG** — no formal tag/chip pattern; the **layout-grid** structure for a removable token / message-recipient list; `listbox`/`radiogroup` for selection; `button` for action. WCAG 2.2 (W3C Recommendation, Oct 2023) — 2.1.1, 2.4.3, 2.5.5, 2.5.8, 1.4.1, 1.1.1, 4.1.2.

## 15. Agent-consumable schema

```yaml
identity:
  id: tag
  name: Tag
  aliases: [Chip, Token, AvatarToken, IssueLabelToken, InteractionTag, CheckableTag, Pill, Label, Keyword, Facet, Lozenge]
  category: foundations
  status: stable
description: >
  The interactive/removable token — the active counterpart to Badge (the passive
  indicator). Spans three interaction archetypes: ACTION (assist/suggestion chips —
  behave like a Button), SELECTION (filter = multi-select toggle, borders Checkbox;
  choice = single-select, borders Radio), and INPUT/TOKEN (removable tokens in a
  field, composed by the multi-select Combobox). Material's four chips
  (assist/filter/input/suggestion) + Carbon's read-only/dismissible/selectable/
  operational matrix + the standalone read-only metadata tag. NOT a Badge (passive,
  non-interactive — the boundary: onClick/×/selected ⇒ Tag), NOT a primary Button,
  NOT a structured-form Checkbox/Radio. Naming morass: Chip (Material/MUI/Polaris) vs
  Tag (Carbon/Ant/Chakra/Atlassian) vs Token (Primer); Fluent splits Tag/InteractionTag.
anatomy:
  parts:
    - "substrate/container: radius/fill/padding + stateful shifts + focus ring; the hit target when the whole tag is interactive"
    - "leading affordance (optional): icon/avatar/dot (inherits Icon); swaps to a checkmark when a filter/choice tag is selected"
    - "label: short text; truncates with ellipsis + full text on hover/title"
    - "trailing affordance: the remove × — an EMBEDDED icon button with its OWN accessible name 'Remove [label]' (inherits Button + Icon); one tag = two operable things"
    - "selected indicator (filter/choice): checkmark / fill / outline->filled; never color alone"
    - "hit-target structure: dual-action (body select + × remove = two focusable elements, stop × bubbling) vs removal-only (merge targets — the whole substrate removes, resolving target size — the Combobox-token default)"
api:
  inherits:
    - icon              # leading adornment + the remove × glyph
    - button            # the embedded remove control is an icon button
    - combobox          # composed-by: the multi-select token field renders Tags
    - badge/banner      # color-not-sole-carrier severity (where a tag encodes status)
  props:
    - {name: label, type: ReactNode, default: ~, required: true, description: "the token text; node (not strict string) for localized formatting/truncation"}
    - {name: onClick/onAction, type: function, default: ~, required: false, description: "the action archetype (assist/suggestion); wires the body as a button"}
    - {name: onRemove/onDelete, type: function, default: ~, required: false, description: "instantiates the ×. MUI: callback-DETECTION (× renders iff onDelete present). Polaris/Spectrum/React Aria: DECOUPLE removable boolean from the handler (controlled state / link tags)"}
    - {name: selected/defaultSelected, type: boolean, default: false, required: false, description: "filter/choice toggle (aria-selected); Ant isolates it in <CheckableTag>"}
    - {name: leadingIcon/avatar, type: ReactNode, default: ~, required: false, description: "leading slot (Primer splits AvatarToken)"}
    - {name: disabled, type: boolean, default: false, required: false, description: "strips interactivity AND dims contrast"}
    - {name: readOnly, type: boolean, default: false, required: false, description: "DISTINCT from disabled — preserves full visual weight but rejects interaction (immutable filters/audit logs)"}
    - {name: size, type: "'sm' | 'md' | 'lg'", default: md, required: false}
    - {name: tone/color, type: "'neutral' | 'info' | 'success' | 'warning' | 'error'", default: neutral, required: false, description: "semantic tone where a tag encodes status; color + text never color alone"}
    - {name: variant/fill, type: "'filled' | 'outlined' | 'subtle'", default: filled, required: false}
    - {name: remove-accessible-name, type: wiring, default: ~, required: true, description: "the × needs its OWN name composed from the label ('Remove Marketing'), not a bare 'Remove'/'×'"}
  group: "TagGroup/ChipSet/token-field — owns the selection model (single/multi), the grid keyboard nav, the overflow algorithm, and focus-management-after-removal. THE REAL API LIVES ON THE GROUP"
states:
  runtime: [rest, hover, focus-visible, active, selected, unselected, disabled, read-only, removing]
  focus-ring: "wraps the whole container (action/selection); for split-target removable tags, illuminates ONLY the × when the remove action has keyboard focus"
  contrast: "rest label/background >= 3:1 against the app background"
variants:
  genre: [assist, filter, input, suggestion, read-only]
  carbon-matrix: [read-only, dismissible, selectable, operational]
  archetype: [action, selection, input]
  selection: [selected, unselected]        # filter=multi, choice=single
  removable: [removable, static]
  tone: [neutral, info, success, warning, error]
  fill: [filled, outlined, subtle]
  size: [sm, md, lg]
  adornment: [leading-icon, avatar, dot, none]
accessibility:
  inherits: [badge/banner (color-not-sole-carrier)]
  wcag-criteria: ["2.1.1", "2.4.3", "2.5.5", "2.5.8", "1.4.1", "1.1.1", "4.1.2"]
  no-formal-pattern: "APG defines no tag/chip pattern; map to existing ARIA paradigms BY ARCHETYPE"
  removable-group-GRID: "role=grid (container), role=row (each tag), gridcell (label + a separate gridcell for the remove button); single tab stop in + Left/Right arrow rove between tags; Delete/Backspace on a focused tag removes it"
  why-not-listbox: "ARIA PROHIBITS interactive elements (the × button) inside role=option — so a removable token list CAN'T be a listbox; the grid is the settled fix (React Aria/Spectrum)"
  focus-after-removal: "move focus to the NEXT tag -> else the PREVIOUS -> else the group/Combobox-input/fallback; NEVER drop to <body> (the classic bug; WCAG 2.4.3; Atlassian mandates it)"
  selection-roles:
    filter-multi: "listbox aria-multiselectable + options, OR role=checkbox array, OR native button[aria-pressed]"
    choice-single: "radiogroup of radios (the Radio '1 of X' model)"
    action: "native button / role=button + Enter+Space"
  remove-button-name: "context-aware, interpolating the label ('Remove Marketing'); a bare SVG fails 1.1.1; DRY alt = aria-label='Remove' + aria-labelledby -> the tag text-node id"
  target-size: "the embedded × must hit 24x24 (2.5.8 AA) / 44x44 (2.5.5 AAA) via internal PADDING on the button (not margin — margin doesn't grow the hit area), glyph stays optically small"
content:
  label: "1 word ideal; 2-3 short words only for a specific entity (name/email/category); a token not a sentence"
  casing: "sentence case (or preserve user-entered); consistent across the set"
  remove-name: "'Remove [label]', never bare 'Remove'/'×'"
  truncation: "past max-width: ellipsis + overflow:hidden + nowrap, ALWAYS paired with title/portal-tooltip revealing the full string (the most common enterprise truncation site)"
  tag-vs-badge: "don't put systemic status language ('Failed'/'Processing') in an interactive Tag — that's Badge vocabulary; Tag content is user/data-driven + actionable"
motion:
  remove: "dual-phase exit — rapid opacity fade then height/width/margin collapse so siblings glide in (FLIP for 60fps)"
  add: "scale-up 90%->100% + fade-in"
  selected: "background cross-fade + checkmark micro-scale-in"
  reduce-motion: "gate all scale/translate/collapse behind prefers-reduced-motion -> instant opacity shifts"
i18n:
  rtl: "anatomical slots mirror — leading icon/avatar to the right, label right-aligned, remove × to the left (inline-start) — via flex defaults + logical properties (padding-inline-start/margin-inline-end), no JS"
  label-expansion: "DE/RU/Romance +30-50%; never a fixed physical width — intrinsic sizing to an engineered max-width then truncate"
  token-field-wrap: "tags wrap to multiple lines in a Combobox field without fracturing the gap to the text cursor; respect the RTL flow"
implementation:
  - "the display:contents grid fix (React Aria, late 2023): apply display:contents to the role=row/gridcell wrappers so they leave the CSS box tree — the visual tags participate in the outer TagGroup flex/grid (flawless wrap) while preserving the multi-tiered DOM the SR API needs"
  - "focus-management-after-removal: capture the index pre-removal; post-render (the node is gone) focus next->previous->group/input. The single most-missed detail"
  - "target-size padding trap: padding on the <button> housing the × expands the hit area to 24x24; NEVER margin (doesn't grow the clickable area)"
  - "whole-tag-vs-×: stop the ×'s click bubbling to the body's onClick; a clickable tag CAN'T be a <button> containing a remove <button> (nested-interactive invalid) — use the grid (row + cells) or a non-button container with two real buttons"
  - "Combobox field composition: the multi-select Combobox renders its value array as a TagGroup of input chips; combobox owns input+listbox, tag group owns token display+removal. Backspace at an empty caret highlights the last token; a 2nd Backspace deletes it (guard per-keypress). Focus rovers between the input cursor and adjacent tags"
  - "overflow '+N more' needs JS not CSS: a ResizeObserver measures available vs accumulated tag widths, slices the overflow, appends a computed +N operational tag wired to a Popover of the hidden items (Fluent). The slice fluctuates with async web-font load"
  - "headless vs opinionated: ship the GROUP logic headless (grid keyboard, focus-mgmt, selection, overflow); theme the TAG (fill/tone/shape). Combobox + TagGroup + Tag coordinate via Context — away from monolithic TagInput/TextInputWithTokens (Primer deprecated the latter for a11y)"
composition:
  stands-on: [icon, button]
  composed-by: [combobox]                  # the multi-select token field
  borders: [checkbox, radio, toggle-button]   # filter=multi / choice=single / pressed-toggle
  alternative-to: [button, checkbox, radio]   # true/primary action / structured form choice
  boundary: [badge]                        # the passive indicator (the Tag-vs-Badge line; Atlassian's Lozenge)
  inherits-pattern: [badge, banner]        # color-not-sole-carrier severity
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "one Tag + archetype booleans (onClick/onRemove/selected) + a TagGroup owning selection (the practice default) vs separate components per genre (Material's four chips; Primer's Token/AvatarToken/IssueLabelToken)"
    - "onDelete callback-DETECTION (MUI — × renders iff handler present) vs DECOUPLED removable-boolean + handler (Polaris/Spectrum/React Aria)"
    - "filter chips as listbox(option/aria-selected) vs role=checkbox vs button[aria-pressed]"
    - "naming: Chip (Material/MUI/Polaris) vs Tag (Carbon/Ant/Chakra/Atlassian) vs Token (Primer) — unconverged; Fluent's Tag/InteractionTag split"
    - "whole-tag clickable vs only-the-× per genre"
  trap:
    - "forcing a removable token list into role=listbox (ARIA prohibits interactive elements in role=option) — must be the grid pattern"
    - "dropping focus to <body> after removing a tag (the focus-management-after-removal failure)"
    - "the embedded × failing target size (2.5.8/2.5.5) — padding on the button, not margin"
    - "nested-interactive: a clickable <button> tag containing a remove <button> (invalid HTML)"
    - "the ×'s click bubbling to the body's onClick (remove also fires the action)"
    - "a bare 'Remove'/'×' accessible name instead of 'Remove [label]'"
    - "color-as-sole-carrier for status tags (1.4.1); putting status vocabulary in an interactive Tag (-> Badge)"
    - "disabling a whole TagGroup (Spectrum: HIDE the group instead); using a Tag for a passive indicator (-> Badge) / primary action (-> Button) / structured form choice (-> Checkbox/Radio)"
  inherited:
    - "Icon + Button substrates"
    - "color-not-sole-carrier severity (badge/banner)"
    - "composed by the multi-select Combobox token field"
  role-in-family: "the interactive/removable token — the active counterpart to Badge; stands on Icon+Button, composed by the multi-select Combobox, borders Checkbox/Radio/Toggle-Button, hard boundary with Badge (Atlassian's Lozenge)"
  evolution:
    - "Material's four-chip taxonomy settling (shape doesn't define it, the interaction archetype does)"
    - "the removable-token GRID pattern hardening (React Aria/Spectrum) + the display:contents layout fix, deprecating listbox/div-soup implementations"
    - "WCAG 2.2 target-size (2.5.8) raising the remove-button bar, ending the over-compact 2010s tags"
    - "the Badge-vs-Tag clarification (Fluent's Tag/InteractionTag split)"
    - "the decline of monolithic TagInput/TextInputWithTokens -> headless Combobox+TagGroup+Tag via Context (Primer deprecated TextInputWithTokens for a11y; Polaris -> s-chip/s-clickable-chip 2025-10)"
  unverified:
    - "external 2026 version numbers across the surveyed systems (React Aria ~3.49, Carbon v11, Ant v5, Polaris 2025-10)"
    - "the React Aria TagGroup grid-pattern role details + the display:contents date — verify against the current Spectrum/APG implementation"
    - "Polaris's deprecation of Tag for s-chip/s-clickable-chip — verify against the current Polaris release"
    - "the +N overflow algorithm's ResizeObserver behaviour fluctuates with async web-font loading"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-tag/` (16 June 2026), the thirty-third brief and the active counterpart to Badge (the thirty-second). It stands on Icon + Button (the leading adornment + the embedded remove control), is composed by the multi-select Combobox (the token field renders Tags — closing the "token-vs-checkbox multi-select split" that brief named), borders Checkbox/Radio/Toggle Button (the selection archetypes), and inherits the color-not-sole-carrier severity model (Badge/Banner) — and it resolves the Badge-vs-Tag boundary from Tag's side (interactive/removable ⇒ Tag; passive ⇒ Badge). The two passes converged strongly — the genre split (Material's assist/filter/input/suggestion four + Carbon's read-only/dismissible/selectable/operational matrix) collapsing to three interaction archetypes (action/selection/input), the naming morass (Chip vs Tag vs Token; Fluent's Tag/InteractionTag split) resolving to `Tag` + `TagGroup`, the removable-tag-group GRID accessibility pattern (`role=grid`/`row`/`gridcell` + Delete/Backspace + the focus-management-after-removal contract, never drop to `<body>`), the selection roles (listbox/radiogroup) + action=button, the remove/dismiss contract + the embedded-button target-size trap, and the token-field composition with the Combobox. The external pass supplied the decisive field detail — *why* listbox is prohibited (ARIA forbids interactive elements inside `role=option`), the **`display: contents` grid fix** (React Aria, late 2023 — semantic grid rows leaving the CSS box tree so the tags wrap in the outer flex layout), the `readOnly`-vs-`disabled` distinction, the `onDelete` callback-detection (MUI) vs decoupled-`removable`-boolean (Polaris/Spectrum/React Aria) API divergence, the FLIP reflow animation, the ResizeObserver reality of "+N more", Carbon's variant matrix, Spectrum's hide-don't-disable-the-whole-group rule, and the recent compositional turn (Primer deprecating `TextInputWithTokens`, Polaris moving to `<s-chip>`/`<s-clickable-chip>`). Claude-pass contributions: the three-archetype framing, the substrate/inheritance map, the Badge-vs-Tag test from Tag's side, the dual-action-vs-removal-only hit-target decision, and the filter-chips-vs-checkboxes call. The 2026 version numbers, the `display: contents` date, the Polaris deprecation, and the ResizeObserver/web-font interaction are flagged unverified. Conformant to `components/_schema.md`. With Tag briefed, the Badge-vs-Tag boundary is now drawn from both sides.*
