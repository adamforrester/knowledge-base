You are researching the Tag component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a tag/chip
is, knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Tag is the INTERACTIVE / REMOVABLE TOKEN — the active counterpart to Badge
(the passive indicator). It STANDS ON two component substrates and
boundaries hard with Badge:
- THE LEADING ICON/AVATAR + THE REMOVE/DISMISS "×" AFFORDANCE inherit ICON
  (components/icon.md) and BUTTON (components/button.md — the embedded
  remove control is an icon button with its own accessible name "Remove
  [tag]"). Don't re-derive Icon or Button.
- THE BADGE BOUNDARY (the headline disambiguation, already drawn from
  Badge's side — components/badge.md): Badge = a NON-INTERACTIVE,
  non-removable indicator (count/dot/status); Tag/Chip = an INTERACTIVE,
  removable/selectable token. Resolve it from Tag's side and don't
  re-derive Badge.
It is COMPOSED BY the multi-select Combobox (the token-input field renders
Tags — components/combobox.md, which already named "the token-vs-checkbox
multi-select split"), and its selection genres border Checkbox (multi-
select filter) and Radio (single-select choice) (components/checkbox.md,
components/radio.md).

THE DEFINING TAG-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE GENRE SPLIT + THE NAMING MORASS (the headline, parallel to Badge):
  "Tag"/"Chip"/"Token" name overlapping but distinct things. Resolve the
  genres — Material 3's canonical FOUR chips: (1) ASSIST chip (acts like a
  button — a transient smart action, e.g. "Add to calendar"); (2) FILTER
  chip (a toggle/selected state in a multi-select set — "Weekend",
  "Under $50"); (3) INPUT chip (a user-entered, REMOVABLE token in a field
  — recipients, applied filters, free-text tags); (4) SUGGESTION chip (a
  dynamically-generated prompt/recommendation, acts like a button/link).
  Plus the standalone read-only/metadata Tag (an article category, a
  status label that's a link). And the naming morass: Material/MUI/Carbon =
  Chip; Ant/Polaris/Spectrum/Atlassian = Tag; GitHub Primer = Token
  (Token/AvatarToken/IssueLabelToken); Fluent = Tag/InteractionTag +
  TagGroup. Resolve the practice's genre model + naming, and the BADGE-vs-
  TAG boundary from Tag's side (interactive/removable = Tag; passive = Badge).
- THE THREE INTERACTION ARCHETYPES the genres collapse to (the real axis):
  (a) ACTION (assist/suggestion → behaves like a Button — see button);
  (b) SELECTION (filter = multi-select toggle → borders Checkbox; choice =
  single-select → borders Radio — see checkbox, radio); (c) INPUT/TOKEN
  (removable tokens in a field → composed by multi-select Combobox — see
  combobox). Resolve how one Tag component (or a family) serves all three
  without becoming an over-propped blob.
- THE ACCESSIBILITY MODEL (the crux, and genuinely contested): a removable
  tag is TWO interactive things — the tag body AND the embedded remove "×"
  button. Resolve the modern settled pattern: the REMOVABLE TAG GROUP as a
  GRID (React Aria / Spectrum TagGroup — role=grid, each tag a row, the
  remove a gridcell; arrow-key navigation between tags + Delete/Backspace
  to remove + the focus-management-after-removal contract: move focus to
  the next tag, then previous, then the container — never drop focus to
  <body>). Contrast the SELECTION genres' roles (filter chips =
  listbox/multi-select or button[aria-pressed]; choice chips = radiogroup;
  action chips = button). Resolve the remove affordance's accessible name
  ("Remove [tag]"), the whole-tag-vs-just-the-× hit target, and the
  Backspace-in-the-input-removes-the-last-token convention.
- THE REMOVE / DISMISS CONTRACT — the embedded icon button (inherits
  Button/Icon), its 44px touch target inside a small tag, the focus return
  after removal, the keyboard (Delete/Backspace on the focused tag), and
  the "is the whole tag clickable or only the ×" decision per genre.
- TRUNCATION / OVERFLOW — long tag text (max-width + ellipsis + the full
  text in a tooltip/title), and the TAG-GROUP overflow ("+3 more" / a
  popover of the rest / wrap-vs-scroll) in a token field.
- SIZING + ANATOMY — small/medium/large; the leading icon/avatar/dot, the
  label, the trailing remove ×; filled-vs-outlined; the color/tone model
  (and color-not-sole-carrier for status-style tags, inheriting the
  Badge/Banner severity rule where a tag encodes meaning).

Field-leader systems to survey (web): Google Material 3 (Chip — the
canonical assist/filter/input/suggestion four), MUI (Chip —
filled/outlined, clickable, deletable, onDelete/avatar/icon), Ant Design
(Tag — closable, CheckableTag, presets/status), Shopify Polaris (Tag —
removable + the disabled/clickable forms), GitHub Primer (Token /
AvatarToken / IssueLabelToken — the Token family + the remove button),
Microsoft Fluent (Tag / InteractionTag / TagGroup — dismissible), Adobe
Spectrum / React Aria (TagGroup — the grid pattern, removable, the
focus-management-after-removal reference implementation), IBM Carbon (Tag —
read-only / dismissible / selectable / operational / the filter tag),
Chakra UI (Tag + TagCloseButton + TagLeftIcon), Base Web (Uber) (Tag),
Atlassian (Tag — removable/linked). WAI-ARIA APG (no formal tag/chip
pattern — the grid pattern for a removable token list; listbox/radiogroup
for selection chips; button for action chips). Mobile reference where
relevant. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Icon + Button substrates, the
Combobox token-field composition, and the Badge/Banner color-not-sole-
carrier severity pattern where a tag encodes status; flag unverified
claims under notes.unverified).

1. Framing — what it is (the interactive/removable token across action/
   selection/input archetypes) and what it isn't (a passive Badge); the
   genre split + the naming morass + the three interaction archetypes up
   front; the Badge-vs-Tag boundary from Tag's side; why systems disagree.
2. Anatomy and parts — the tag body, the leading icon/avatar/dot, the
   label, the trailing remove "×" (an embedded icon button), the selected
   indicator; the hit-target structure (whole-tag vs the × only).
3. Properties / API — label, variant/genre (assist/filter/input/suggestion
   or action/selection/input), selected, onRemove/onDelete, onClick,
   disabled, leadingIcon/avatar, size, tone/color, removable, the
   accessible-name wiring for the remove button.
4. States and variants — the genres; selected/unselected (filter/choice);
   removable; clickable/action; read-only/static; disabled; the tones;
   filled-vs-outlined; sizes.
5. Usage guidance — Tag (interactive/removable token) vs Badge (passive
   indicator) vs Button (a true action) vs Checkbox/Radio (a form control)
   vs the multi-select Combobox (the token field); when assist vs filter vs
   input vs suggestion; the filter-chips-vs-checkboxes call.
6. Accessibility — the removable-tag-group GRID pattern (role=grid / row /
   gridcell, arrow-nav + Delete/Backspace + focus-management-after-removal,
   never drop to <body>), the selection roles (listbox/radiogroup), the
   action chip = button, the remove button's accessible name, the
   whole-tag-vs-× hit target, color-not-sole-carrier for status tags, WCAG
   SCs (2.1.1, 2.4.3 focus order, 2.5.5/2.5.8 target size, 1.4.1).
7. Content guidelines — short label, the remove button's name ("Remove
   [tag]"), truncation + full-text-on-hover, sentence case, don't-overload,
   the tag-vs-badge content distinction.
8. Motion and transition — the remove/dismiss animation (the tag
   collapsing out + the group reflowing), the add animation, selected
   transition, reduce-motion.
9. Internationalization — RTL (the remove × flips to the leading edge, the
   leading icon flips), label expansion + truncation, the token-field
   wrapping.
10. Naming — Tag / Chip / Token / Pill / Label; the genre names
    (assist/filter/input/suggestion); the practice's default; the
    Badge-vs-Tag + Chip-vs-Tag disambiguation; aliases.
11. Implementation notes — the grid-pattern removable group (roving focus
    across tags + the remove cell) + the focus-management-after-removal
    algorithm, the embedded-button-in-a-small-tag target-size trap, the
    whole-tag-vs-× click handling, the Backspace-removes-last-token in a
    field, truncation + overflow ("+N more"), the token-field composition
    with Combobox, headless vs opinionated.
12. Related and alternative components — typed relationships (Icon + Button
    substrates, the multi-select Combobox token-field composition, the
    Badge passive-indicator boundary, Checkbox/Radio the selection-control
    borders, the Banner/Badge color-not-sole-carrier severity pattern).
13. Field POV evolution — recent shifts (Material's four-chip taxonomy
    settling, the removable-tag-group grid pattern (React Aria) hardening,
    the Token/Tag/Chip naming convergence-or-not, the Badge-vs-Tag
    clarification, target-size 2.5.8 raising the remove-button bar).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a tag is — explain the genre
split (assist/filter/input/suggestion) + the naming morass + the three
interaction archetypes (action/selection/input), the Badge-vs-Tag boundary
from Tag's side, the removable-tag-group GRID accessibility pattern (grid/
row/gridcell + Delete/Backspace + focus-management-after-removal) and how
it differs from the selection roles (listbox/radiogroup) and the action
chip (button), the remove/dismiss contract + the embedded-button target-
size trap, the truncation/overflow model, and the token-field composition
with the multi-select Combobox that field leaders still diverge on.
