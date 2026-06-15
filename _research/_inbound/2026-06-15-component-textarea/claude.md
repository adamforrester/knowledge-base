# Textarea — field-truth study

## 1. Framing

Textarea is Text Field's sibling, and 80% of it *is* Text Field — same label/helper/error stack, same `aria-describedby` chain, same placeholder-is-not-a-label rule, same read-only-vs-disabled distinction. This brief deliberately does not re-derive that shared substrate (see components/text-field.md); it concentrates on the 20% that is genuinely Textarea's own, and that 20% is where the field actually disagrees: **the sizing model**. A single-line input has a fixed height; a multi-line input must answer "how tall, and what happens when the content exceeds it?" — and there is no consensus answer.

What a Textarea *is*: a control for free-form text that is expected to wrap and span multiple lines — comments, descriptions, messages, notes, addresses-as-blob. What it *isn't*: a single-line value (Text Field), a value from a known set (Select/Combobox), or **formatted/structured rich text** (a rich-text editor / `contenteditable` surface). The boundary that recurs and bites is **textarea-versus-rich-text-editor**: the moment a product wants bold, links, @-mentions, or embedded media, a `<textarea>` is the wrong primitive — it holds a plain string and nothing else. Teams routinely stretch a textarea toward rich text with `contenteditable` hacks and ship an inaccessible, un-undoable editor (a `<textarea>` gives you native undo/redo, spellcheck, and IME for free; `contenteditable` gives you none of it reliably).

Why systems disagree:

- **Auto-resize vs. fixed height vs. manual resize.** Does the field grow with content (auto-grow), stay a fixed height with an internal scrollbar, or expose the browser's drag handle? Each has a different layout-stability cost.
- **The character counter is first-class here**, not optional — long-form input is exactly where limits are enforced, so the counter's a11y and over-limit behaviour are load-bearing (and inherit the polite-live-region pattern from Text Field §6).
- **Enter-key semantics.** In a form, Enter inserts a newline. In a chat/comment composer, Enter *submits* and Shift+Enter inserts a newline. The component cannot know which without being told — and getting this wrong is the single most-felt Textarea bug.
- **Paste handling** — large pastes, formatted pastes, and the resize/scroll jump they cause.

## 2. Anatomy and parts

Inherits the Text Field anatomy (root, label, helper, error, required indicator, `aria-describedby` wiring) — not repeated here. Textarea-specific parts:

- **Multi-line input control** — a `<textarea>`, not `<input>`. Owns `rows`, `wrap`, and the resize behaviour.
- **Resize affordance** — the browser's native drag handle (bottom-right corner, via CSS `resize`), or a custom one, or none. A first-class part because it is *visible chrome* the design must decide on, not just a behaviour.
- **Character counter** — far more prominent than on Text Field; typically bottom-aligned, often paired with `maxLength`. Frequently rendered in the same row as the resize handle, which creates a collision the layout must resolve.
- **Scroll region** — when content exceeds the (max) height, the textarea becomes its own scroll container; the scrollbar is a part with its own contrast/affordance concerns.
- **Auto-size mirror (implementation part)** — auto-grow is usually implemented with a hidden mirror element or `scrollHeight` measurement (§11); it is invisible but structurally real.

The adornment-slot vocabulary (prefix/suffix) mostly does *not* apply — a multi-line field rarely carries inline leading/trailing affixes the way Text Field does; where systems offer "footer" content (counter, actions), it sits below the input, not inside the text flow.

## 3. Properties / API

Inherits the Text Field core (`value`/`defaultValue`, `onChange`, `label`, `placeholder`, `helpText`, `error`, `disabled`, `readOnly`, `required`, `name`, `id`, `autoComplete`). Textarea-specific and contested props:

- **`rows`** (and sometimes `cols`) — the native height hint in lines. Near-universal as the *initial* height. `cols` is effectively dead on the web (width comes from CSS), but `rows` survives as the minimum/initial height.
- **The resize model — the load-bearing divergence.** Three stances:
  - **`autoSize` / auto-grow** — the field grows with content up to a cap. The modern default for composers (chat, comments). Spectrum's `Textarea` and many systems offer it; the cap is set by `maxRows`.
  - **Fixed height + internal scroll** — `rows` sets height, overflow scrolls. Predictable layout; the conservative form default.
  - **User resize** — expose the native drag handle via `resize`. Convenient but breaks layout stability and is awkward on touch.
  The practice default: expose a **`resize` prop** (`none | vertical | auto`), default `vertical` for forms, `auto` (auto-grow with `minRows`/`maxRows`) for composers, and **never `horizontal`/`both`** — horizontal resize breaks line-length and layout in every responsive context.
- **`minRows` / `maxRows`** — the auto-grow bounds. The pair that makes auto-size safe: grow from `minRows`, stop at `maxRows`, then scroll. Naming varies (`minRows`/`maxRows`, `minHeight`/`maxHeight`, `autoSize={{minRows, maxRows}}`).
- **`maxLength` / character limit** — present widely, but the *enforcement* model diverges: hard cap (native `maxLength`, browser blocks further input) vs. soft cap (allow over-typing, show the counter in error, block submit). **Soft cap is the better default** — a hard `maxLength` silently swallows pasted overflow with no feedback and is hostile to editing; the soft pattern tells the user *by how much* they are over. (See §6 for the counter's a11y.)
- **`showCount` / character counter** — first-class here. A boolean or a render-prop; pairs with `maxLength` to show "240 / 280."
- **Enter-key behaviour** — most systems leave this to the consumer (native: Enter = newline). Composers need a `submitOnEnter` / `onSubmit` convention (Enter submits, Shift+Enter newline). The practice position: **do not bake submit-on-Enter into the base Textarea**; provide it as an explicit opt-in (a `MessageComposer`/`ChatInput` variant or a documented `onKeyDown` recipe), because silently hijacking Enter breaks the platform expectation for every non-chat use.
- **`spellCheck`, `wrap`** — native passthroughs; `spellCheck` worth surfacing (often disabled for code/structured input), `wrap` (`soft|hard`) rarely touched.

## 4. States and variants

Runtime states are Text Field's set (rest / hover / focus-visible / disabled / read-only / loading / error / empty), with Textarea-specific notes:

| State | Textarea-specific contract |
| --- | --- |
| focus-visible | same ring contract (1.4.11/2.4.13); the larger target makes the ring more prominent |
| error | counter-over-limit is a common error trigger; reserve layout space so the error doesn't shove the resize handle |
| empty | placeholder spanning the larger area; same not-a-label rule |
| read-only | a long read-only textarea must stay scrollable and selectable so the full value is reachable (the disabled-traps-content failure is worse here than on Text Field — more text is hidden) |
| loading | rarer; AI-generated content streaming into a textarea is the emerging case (`aria-busy`, don't fight the user's cursor) |

No `pressed` state of note (multi-line fields aren't pressed the way mobile single-line fields are).

**Intentional variants:** `size` {small, medium, large} (scales typography/padding, not height — height is `rows`/auto-grow), density, and the same single-bordered/outline default as Text Field. The genuinely Textarea-specific variant axis is the **resize model** (§3) — `none | vertical | auto` — which behaves more like a variant than a runtime state. The counter (`showCount`) and auto-grow are orthogonal modifiers.

## 5. Usage guidance

- **Use** for free-form text expected to exceed one line: comments, descriptions, messages, feedback, notes, multi-line addresses.
- **Don't use** for single-line values (→ Text Field — and don't use a one-row textarea as a "bigger input"; semantics and Enter behaviour differ), for formatted/structured content (→ rich-text editor), or for choosing from options (→ Select/Combobox).
- **Decision frameworks:**
  - **Auto-grow for composers, fixed+scroll for forms.** A chat/comment box should grow with the message; a "Notes" field in a long form should hold a stable height so the form doesn't reflow as the user types.
  - **Set `maxRows` whenever auto-growing.** An uncapped auto-grow textarea can push the submit button off-screen on a long paste.
  - **Right-size the initial `rows` to the expected input.** Two rows for a short note signals brevity; six rows for a description signals "write more." The initial height is a content cue.
  - **Counter only when there's a real limit.** Don't show a counter on an unlimited field — it implies a cap that doesn't exist.

## 6. Accessibility

Shared contract with Text Field (label association, describedby chain, error wiring, focus contrast) is not repeated; Textarea-specific:

- **The character counter is the central a11y problem** (as on Text Field §6, but more frequent here): the visual counter updates instantly but is `aria-hidden="true"`; a separate visually-hidden `aria-live="polite"` node announces the remaining count *on pause*, not per keystroke. Add a threshold so it only starts announcing near the limit (e.g. last 20 chars) rather than from the first character — continuous counting on a long-form field is even more punishing than on a short one.
- **Over-limit must be announced, not just coloured.** When the user crosses `maxLength` (soft cap), the counter's over-by message goes through the live region and the field gets `aria-invalid`; the error text states the overage. A hard native `maxLength` that silently blocks input is *worse* for AT users — they get no feedback that input was dropped.
- **Enter-key semantics are an a11y/usability contract, not just UX.** If Enter submits (composer), the affordance must be discoverable (visible "Shift+Enter for newline" hint or an explicit send button); a screen-reader user must not lose their drafted text to an unexpected submit. Never make Enter-submits the only way to submit — always provide a real submit button.
- **Auto-resize must not move focus or the caret.** A resize on input that scrolls the viewport or loses the cursor position is a serious failure; the measurement must be synchronous with input so the caret stays put.
- **WCAG SCs:** same set as Text Field — 1.3.5 Identify Input Purpose (e.g. a "street address" textarea), 3.3.1/3.3.2/3.3.3 (error/labels/suggestion), 1.4.11/2.4.13 (focus and boundary contrast), 4.1.2, 2.5.8 (the resize handle as a target). Plus **1.4.4 Resize Text / 1.4.10 Reflow** bite harder here: the textarea and its counter must survive 200% zoom and 320px reflow without the counter colliding with the resize handle or the text clipping.

## 7. Content guidelines

- **Label and helper:** same rules as Text Field (noun phrase, sentence case, format-hint in helper before failure).
- **Placeholder for a textarea can model the expected shape** — "Describe the issue, including steps to reproduce" — but it still vanishes on input, so it's a prompt, not instructions to keep.
- **Counter copy:** "240 / 280" or "40 characters remaining"; over-limit "12 characters over the limit," constructive, not "Too long."
- **Composer affordance copy:** if Enter submits, say so ("Press Enter to send, Shift+Enter for a new line") near the field.
- **Empty/CTA:** belongs to the host form, not the textarea (same as Text Field).

## 8. Motion and transition

- **Auto-grow is the signature motion** and the one most likely to feel janky. Growing the height should be effectively instant on keystroke (no eased transition on the height itself — an animated height lags behind typing and feels broken). If a transition is used at all, keep it ≤100ms and **disable it under `prefers-reduced-motion`** (and honestly, auto-grow height is better with no transition at all).
- **State transitions** (focus/error border) follow Text Field's ~100–150ms token-driven contract.
- **Reduce-motion:** drop any height-transition entirely; the resize itself is functional and instantaneous, not decorative.

## 9. Internationalization

- **Inherits Text Field's i18n** (logical-property RTL, `dir="auto"` so typed content direction can differ from UI, text expansion of labels/messages, IME-composition guard on validation).
- **Textarea-specific:** auto-grow height is line-count driven, so **scripts with taller line-heights (Arabic, Thai, Devanagari) and vertical text grow differently** — `minRows`/`maxRows` must be computed from the *rendered* line box, not an assumed Latin line-height, or the cap clips or over-grows.
- **The IME guard matters more here** than on Text Field: composing a long CJK passage means many composition events; auto-grow measurement and any character-count enforcement must not fire mid-composition or the field thrashes.
- **`maxLength` counts UTF-16 code units, not grapheme clusters** — emoji and combining characters can "cost" 2+ toward the limit, surprising users in non-Latin scripts. If the limit is user-facing, count by grapheme (`Intl.Segmenter`) rather than `.length`.

## 10. Naming

The component is near-universally **`Textarea`** (Polaris, Spectrum, Carbon, Atlassian, Base Web) or **`TextArea`** (casing splits). Primer uses `Textarea`. Practice default: **`Textarea`** (one word, matching the HTML element). Aliases consumers reach for: `MultilineTextField` / `TextField multiline` (Material and MUI model it as a `multiline` *prop* on TextField rather than a separate component — a real divergence: one component with a `multiline` boolean vs. a distinct `Textarea`). The practice ships a **distinct `Textarea`**, not a `multiline` prop on TextField — the sizing model, Enter semantics, and counter prominence are different enough that overloading TextField muddies both. Composer specialisations: `MessageComposer` / `ChatInput` (the submit-on-Enter variant).

## 11. Implementation notes

- **Auto-grow measurement is the core implementation trap.** Two techniques: (a) a hidden **mirror element** that holds a copy of the content and whose natural height drives the textarea; (b) reset `height: auto` then read `scrollHeight` on every input. Both must run synchronously on input to avoid caret jump and layout flicker; `scrollHeight` is simpler but forces a synchronous reflow (perf cost on every keystroke for very long content). React: `field-sizing: content` (modern CSS) is starting to replace JS auto-grow entirely — flag it as the emerging path but verify browser support before relying on it.
- **`maxRows` cap then scroll** — once content exceeds `maxRows`, switch from growing to internal scroll; the handoff is where janky implementations flicker.
- **Controlled value + auto-grow** needs the height recomputed when `value` changes programmatically (e.g. reset, AI-inserted text), not only on user input — a common bug is a programmatic value that doesn't trigger a resize.
- **Inherits Text Field's wiring** (`useId` for label/describedby, `forwardRef` to the `<textarea>`, real `name` for forms/Server Actions, controlled/uncontrolled both). The ref targets the `<textarea>` node.
- **Paste handling:** large pastes should trigger a single resize, not one per inserted line; formatted paste into a `<textarea>` is auto-stripped to plain text by the platform (a feature — don't fight it). If the product needs formatted paste, that's the rich-text-editor signal (§1).
- **Don't reach for `contenteditable`** to add formatting — it sacrifices native undo/redo, spellcheck, reliable IME, and form submission. Cross the boundary to a real editor instead (§12).

## 12. Related and alternative components

- **Composes with:** Label, Helper/Description text, FieldError, Character counter, Form, Button (the paired submit/send action), Spinner (AI-streaming loading).
- **Alternative to:** Text Field (single-line), Rich Text Editor (formatted/structured content), Combobox/Select (enumerable values), Code Editor (monospace/structured code input — a specialised sibling).
- **Supersedes:** a one-row `<textarea>` used as a "tall input"; `contenteditable` divs used for plain multi-line input.
- **Superseded by:** a rich-text editor when the content needs formatting; otherwise nothing for plain multi-line text.

(See components/text-field.md for the shared form-field substrate, 03-component-library for the component model, and 29-per-component-documentation-template for the docs page this feeds.)

## 13. Field POV evolution

- **Auto-grow is becoming the default** for composer contexts (chat, comments) where fixed-height used to rule; `maxRows`+scroll is the safety valve.
- **CSS `field-sizing: content`** is poised to retire JS auto-grow — the biggest near-term implementation shift; date-and-verify browser support before adopting.
- **Soft character limits over hard `maxLength`** — the field is moving toward allow-over-then-block-submit with clear feedback, away from silent native truncation.
- **AI changes the loading story** — streaming generated text into a textarea (rewrite, summarise, draft) makes a once-rare loading/`aria-busy` state newly relevant, and raises new questions about editing while content streams.
- **The TextField-`multiline`-prop vs. distinct-`Textarea` split persists** — Material/MUI overload TextField; most others keep Textarea separate. The practice sides with separate.

## 14. Sources cited

(To be reconciled against the external pass; conservative dates.)

- Shopify Polaris — Textarea (multiline field, `maxHeight`/auto-size, showCharacterCount) (Polaris, 2024–2025).
- Adobe Spectrum / React Aria — TextArea / TextField, auto-grow, validation integration (Spectrum, 2024–2025).
- Google Material 3 — text fields `multiline` (the multiline-prop model) (Material 3, 2024).
- IBM Carbon — TextArea, counter, `enableCounter`/`maxCount` (Carbon, 2024).
- GitHub Primer — Textarea, FormControl wiring, `resize` control (Primer, 2024).
- Atlassian Design System — TextArea, `minimumRows`/resize (Atlassian, 2024).
- Base Web (Uber) — Textarea overrides (Base Web, 2024).
- Microsoft Fluent — Textarea, `autoAdjustHeight`, `resize` (Fluent, 2024).
- Apple HIG / Material 3 Compose — multi-line text entry, keyboard behaviour (2024).
- WCAG 2.2 (W3C, Oct 2023) — SC 1.3.5, 3.3.1, 3.3.2, 3.3.3, 1.4.4, 1.4.10, 1.4.11, 2.4.13, 4.1.2, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: textarea
  name: Textarea
  aliases: [text-area, multiline-text-field, multiline-input]
  category: form
  status: stable
description: >
  Control for free-form text expected to wrap across multiple lines —
  comments, descriptions, messages. Shares the form-field substrate with
  text-field; differs in the sizing model, character-counter prominence,
  and Enter-key semantics. Not single-line (text-field), not formatted
  (rich-text-editor).
api:
  inherits: text-field   # label, value, onChange, placeholder, helpText, error, disabled, readOnly, required, autoComplete, name, id
  props:
    - name: rows
      type: number
      default: 3
      required: false
      description: Initial/min height in lines; content cue. cols is dead on web.
    - name: resize
      type: enum
      values: [none, vertical, auto]
      default: vertical
      required: false
      description: vertical for forms, auto (grow) for composers; never horizontal/both.
    - name: minRows
      type: number
      required: false
      description: Auto-grow floor (with resize:auto).
    - name: maxRows
      type: number
      required: false
      description: Auto-grow cap; beyond it the field scrolls. Always set when auto-growing.
    - name: maxLength
      type: number
      required: false
      description: Character limit. Prefer SOFT enforcement (allow over, show counter error, block submit) over a hard native cap that silently drops paste overflow.
    - name: showCount
      type: boolean
      default: false
      required: false
      description: Character counter; first-class here. Only when a real limit exists.
    - name: spellCheck
      type: boolean
      required: false
    - name: submitOnEnter
      type: boolean
      default: false
      required: false
      description: Composer opt-in (Enter submits, Shift+Enter newline). NOT the base default; always pair with a real submit button.
composition:
  composes-with: [label, helper-text, field-error, character-counter, form, button, spinner]
  alternative-to: [text-field, rich-text-editor, combobox, select, code-editor]
  supersedes: ["one-row textarea as a tall input", "contenteditable div for plain multi-line text"]
  superseded-by: ["rich-text-editor when content needs formatting"]
accessibility:
  inherits: text-field   # label association, aria-describedby chain, error wiring, focus contrast
  wcag-criteria: ["1.3.5", "3.3.1", "3.3.2", "3.3.3", "1.4.4", "1.4.10", "1.4.11", "2.4.13", "4.1.2", "2.5.8"]
  aria-attributes:
    - aria-invalid
    - aria-describedby
    - aria-live        # polite, on the visually-hidden counter node; threshold near the limit
    - aria-busy        # AI streaming
  keyboard-model:
    enter: newline (default) | submit (composer opt-in, with Shift+Enter newline + visible hint)
    typing: native multi-line editing, undo/redo, spellcheck, IME
  focus-behavior:
    focus-visible: required
    caret-stability: auto-resize must not move caret or scroll viewport
    ref: forwardRef reaches the <textarea>
  character-counter:
    visual: aria-hidden=true, instant
    announced: visually-hidden aria-live=polite, threshold near limit, over-limit announced not colour-only
states:
  runtime: [rest, hover, focus-visible, disabled, read-only, loading, error, empty]
  not-applicable: [pressed]
variants:
  size: [small, medium, large]   # scales type/padding, not height
  resize: [none, vertical, auto]
  style: [outline]
  modifiers: [auto-grow, show-count]
content:
  label-pattern: "noun phrase, sentence case; same as text-field"
  placeholder-pattern: "may model expected shape; still vanishes on input, not instructions"
  counter-pattern: "'240 / 280' or 'N remaining'; over-limit 'N over the limit', constructive"
  error-pattern: "what + how to fix (SC 3.3.3); over-limit announced via live region, not colour-only"
  empty-pattern: "label + optional placeholder; no separate empty UI"
i18n:
  inherits: text-field   # logical-prop RTL, dir=auto, expansion, IME guard
  textarea-specific:
    - "minRows/maxRows from rendered line box, not assumed Latin line-height (Arabic/Thai/Devanagari)"
    - "maxLength counts UTF-16 code units; count by grapheme (Intl.Segmenter) for user-facing limits"
notes:
  contested:
    - resize model (none/vertical/auto) — vertical default forms, auto composers
    - hard vs soft maxLength (soft preferred)
    - Enter-submits as opt-in, never base default
    - distinct Textarea vs multiline-prop-on-TextField (we ship distinct)
  emerging:
    - "CSS field-sizing:content retiring JS auto-grow (verify browser support)"
    - "AI-streamed content as a new loading/aria-busy case"
```
