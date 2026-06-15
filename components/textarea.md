---
okf_version: "0.1"
type: component-brief
title: Textarea
description: Text Field's multi-line sibling, where 80% is the shared form-field substrate and the contested 20% is the sizing model. A field-truth study of where the leading systems converge (distinct component over a multiline prop, vertical-only resize, soft over hard maxLength, the threshold-based polite counter, field-sizing:content) and where they fracture (auto-grow vs. fixed-height default, who owns Enter, how far to mirror the Text Field API), with the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [text-area, multiline-input, multiline-text-field, textbox, comment-box]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Textarea

> Text Field is contested on its anatomy; Textarea is contested on its *physics*. Eighty per cent of this component is Text Field — the same label, helper, error, and `aria-describedby` substrate (see text-field) — and re-deriving it here would be waste. The remaining twenty per cent is everything a single-line field never has to answer: how tall, what happens when the content overruns, who owns the Enter key, and where the boundary to a rich-text editor sits. Every divergence below descends from one fact: a multi-line field is fluid in the block direction, and the field has never agreed on how to tame that fluidity. If Text Field is the calibration brief for *encapsulation and accessibility wiring*, Textarea is the calibration brief for *the sizing model and the inherited-substrate discipline* — the first brief that explicitly stands on another.

---

## 1. Framing

A textarea is the control for free-form text expected to wrap and span multiple lines — comments, descriptions, messages, feedback, notes, an address as a blob. What it *isn't*: a single-line value (Text Field), a value from a known set (Select / Combobox), or formatted, structured rich text (a rich-text editor). The boundary that recurs and bites is **textarea-versus-rich-text-editor**: the moment a product wants bold, links, @-mentions, headings, or embedded media, a `<textarea>` is the wrong primitive — it holds a plain string and nothing else (both agents). Teams routinely stretch a textarea toward rich text with `contenteditable` and ship an inaccessible, un-undoable editor; a native `<textarea>` gives you undo/redo, spellcheck, IME, and form submission for free, and `contenteditable` gives you none of them reliably (both agents). Cross the boundary to a real editor (ProseMirror / Slate / Lexical) rather than hacking the textarea (external).

The field's first ontological disagreement is **whether Textarea is a component at all**. Two paradigms (external):

- **The variant architecture** — Polaris and Material 3 model multi-line as a *behavioural variant* of a universal text field, invoked by a boolean or a line-count prop (`multiline={4}`). The appeal is absolute DRY: label, error binding, and slot orchestration are shared with the single-line input by construction.
- **The distinct-component architecture** — Primer, Carbon, Atlassian, Fluent, and Base Web enforce a hard boundary and ship `Textarea` as a standalone entity.

**The practice ships a distinct `Textarea`.** This is the same call the Text Field brief made from the other side (see text-field §10) — and it is the right one here for a concrete reason, not symmetry. Multi-line input carries heavy, performance-sensitive, non-overlapping machinery the single-line field never touches: auto-grow measurement on every keystroke, a manual resize affordance, scroll-region management, line-break normalization, grapheme-aware counting, and the Enter-key contract. Folding that into the universal `TextField` taxes the render path of every plain input in the application and bloats it with conditionals (external). Isolating Textarea lets that machinery be optimised — and documented — where it lives. The cost of the call is honesty about the overlap, which is what §3 is for.

The defining tension, then, is the component's relationship to the layout viewport. A single-line input has fixed physical height; a textarea is fluid in the block direction and must accommodate unpredictable volume while avoiding both traps — excessive whitespace when empty, claustrophobic confinement when full (external). Every sizing decision in §3 is an answer to that one tension.

## 2. Anatomy and parts

Textarea inherits the Text Field anatomy wholesale — root/container, label, required indicator, helper text, error message, and the `aria-describedby` wiring that binds them (see text-field §2). That substrate is not repeated here. What is genuinely Textarea's own (both agents):

- **Multi-line input control** — a `<textarea>`, not `<input>`. Owns `rows`, `wrap`, and the resize behaviour. As on Text Field, it is normalised (`appearance: none`, transparent background, no native outline) so the container owns the visual surface (external).
- **Resize affordance** — the drag handle at the bottom trailing corner (bottom-right in LTR), exposed via CSS `resize` or removed via `resize: none`. A *first-class part* because it is visible chrome the design must decide on, not merely a behaviour.
- **Character counter** — far more prominent than on Text Field; usually bottom-trailing, in the form-control footer rather than inside the text flow. Frequently shares that footer row with the resize handle, a collision the layout must resolve.
- **Scroll region and gutter** — when content exceeds the (max) height the textarea becomes its own scroll container; the scrollbar is a part with its own contrast and, on Windows, its own interaction with the error border (§4).
- **Ghost sizer / mirror node** *(implementation part)* — a visually hidden element duplicating the textarea's typography, padding, and width, used to measure `scrollHeight` for JavaScript auto-grow before paint (external). Invisible but structurally real — and, as §11 covers, increasingly obsolete.

The decorative-vs-interactive adornment split that dominates Text Field's anatomy (see text-field §2) mostly **does not apply** — a multi-line field rarely carries inline leading/trailing affixes. Where systems do place an interactive icon (clear, copy, AI-assist), there is a Textarea-specific trap: because the box grows downward, an icon vertically centred with `translateY(-50%)` *drifts* as the user types. The field-truth fix is to anchor internal trailing controls to the **top** trailing corner, aligned to the first line, fixed regardless of how far the box expands; Primer sidesteps the problem by forcing supplementary actions outside the container entirely (external).

Two layout postures, paralleling Text Field's label archetypes: **fixed-height-plus-scroll** (the conservative form default) vs. **auto-grow** (the composer default). The practice treats these as a variant axis, not two components (§4).

## 3. Properties / API

Textarea inherits the Text Field core unchanged — `value` / `defaultValue`, `onChange` / `onBlur` / `onFocus`, `label`, `placeholder`, `helpText`, `error`, `disabled`, `readOnly`, `required`, `autoComplete`, `size`, `id` / `name` (see text-field §3 for the full contract and the encapsulation hybrid). The hybrid decision carries over identically: ship `label` / `helpText` / `error` as props for the common vertical-form case, expose the composed slots for custom layout, and own the `id` / `aria-describedby` / `aria-invalid` wiring internally. **Do not re-litigate the substrate; inherit it.** What follows is only the Textarea-specific surface.

**The sizing model — the load-bearing divergence.** This is Textarea's equivalent of Text Field's encapsulation question. Three field stances (both agents):

- **Auto-grow** — the field grows with content up to a cap. The modern default for composers (chat, comment, message). Spectrum, Fluent (`autoAdjustHeight`), and most current systems offer it.
- **Fixed height + internal scroll** — `rows` sets the height, overflow scrolls. Predictable layout; the conservative form default.
- **User resize** — expose the native drag handle. Convenient on desktop, awkward on touch, destabilising to layout.

The practice exposes a single **`resize`** prop — `none | vertical | auto` — and defaults it to **`vertical` for standalone form fields** and **`auto` (auto-grow, bounded by `minRows` / `maxRows`) for composer contexts**. The one hard rule both agents reach independently: **never `horizontal` or `both`**. Horizontal resize shatters grid layouts, overflows flex containers, and breaks responsive and mobile viewports; altering a field's inline dimension is pure layout thrashing for no user gain (external). (The external pass models auto-grow as a separate `autoGrow` boolean rather than a `resize: auto` value — a defensible API shape; we fold it into `resize` so the sizing model has one prop, not two that can contradict each other.)

**`rows` / `minRows` / `maxRows`.** `rows` survives as the initial/minimum height **expressed in lines, not pixels** — and the line-count framing is load-bearing, not stylistic. A pixel `minHeight` doesn't scale when the user bumps their browser font size or responsive typography scales up; line-count bounds recompute against the *current* computed line-height, staying locked to the type scale (external; Material 3 Compose formalises this as `TextFieldLineLimits`). `cols` is dead on the web — width comes from CSS. `minRows` / `maxRows` are the auto-grow bounds: grow from `minRows`, stop at `maxRows`, then scroll. **Always set `maxRows` when auto-growing** — an uncapped auto-grow textarea pushes the submit button off-screen on a long paste (Claude; external reports Polaris's early unbounded-growth bug as exactly this failure). Right-size the initial `rows` to the expected input: two rows signals brevity, six signals "write more" — the initial height is a content cue (Claude).

**`maxLength` / character limit — soft over hard.** Both agents converge hard here, and it is the practice default: **do not use the native `maxlength` attribute for substantial text.** A hard cap silently swallows pasted overflow — paste 600 characters into a 500 limit and the browser truncates the last 100 with no feedback, and the user may submit unaware (external). It is also hostile to assistive tech: input simply stops being accepted with no announcement. The soft pattern instead *allows* the overflow, flips the field to `aria-invalid`, shows the counter in error, disables submit, and announces the overage — preserving the essential **paste-and-prune** workflow (both agents). See §6 for the announcement contract and §9 for what "a character" even means.

**`showCount` / character counter.** First-class here (a boolean, or a render-prop for custom formatting), paired with the limit. Show it **only when a real limit exists** — a counter on an unlimited field implies a cap that isn't there (Claude).

**Enter-key semantics.** Natively, Enter inserts a newline; that is the correct default and most systems leave it alone (external). Composers invert it — Enter submits, Shift+Enter inserts a newline. The practice position: **do not bake submit-on-Enter into the base Textarea.** Provide it as an explicit opt-in — a `MessageComposer` / `ChatInput` specialisation or a documented `onKeyDown` recipe with a `submitOnEnter` flag — because silently hijacking Enter breaks the platform expectation for every non-chat use and can lose a screen-reader user's drafted text to an unexpected submit (both agents). And whenever Enter submits, there must still be a real, visible submit button and a visible "Shift+Enter for a new line" hint — Enter-submits is never the *only* path (§6).

**Paste handling.** Two Textarea-specific obligations. First, large pastes should trigger a *single* resize, not one per inserted line. Second, normalise line breaks: operating systems put `\r\n` (Windows) or `\n` (Unix/macOS) on the clipboard, and the difference skews byte-counted backends and off-by-one limit enforcement — intercept `onPaste` and normalise to `\n` before counting or storing (external). Formatted paste into a `<textarea>` is auto-stripped to plain text by the platform; that is a feature, not a bug — needing to *keep* the formatting is the rich-text-editor signal (§1).

**`spellCheck`, `wrap`** — native passthroughs; `spellCheck` worth surfacing (often disabled for structured input), `wrap` (`soft | hard`) rarely touched.

## 4. States and variants

Textarea inherits Text Field's runtime state set and contracts — rest, hover, focus-visible, disabled, read-only, loading, error, empty (see text-field §4). Only the Textarea-specific deltas are recorded here:

| State | Textarea-specific contract |
| --- | --- |
| focus-visible | Same ring contract (WCAG 1.4.11 / 2.4.13), but a textarea spanning many rows is a *large* surface — a thick, saturated ring around a 600×400 box is visual noise. Decouple the native outline and apply a controlled inset indicator on the container; Atlassian leans on a subtle background/border-tint shift instead (external). |
| error | Two traps. (1) The counter-over-limit is the most common error trigger here, so reserve footer space — the error must not shove the resize handle. (2) On Windows, the opaque native scrollbar docks against the right border; apply the error stroke to the **container**, not the input, so the scrollbar sits *inside* the error boundary rather than breaking the ring (external). |
| read-only | A long read-only textarea must stay scrollable and selectable so the whole value is reachable — the disabled-traps-content failure (see text-field §4) is worse here because far more text is hidden. |
| loading | Rarer historically; the emerging case is AI-generated content streaming into the field (rewrite / summarise / draft). Carry `aria-busy`, and do not fight the user's caret while content streams (Claude; external flags Carbon's AI-explainability direction). |

There is **no meaningful `pressed` state** — multi-line fields aren't pressed the way mobile single-line fields are.

**Intentional variants.** `size` {small, medium, large} scales typography and padding **only** — height is owned by `rows` / auto-grow, so the single-line height tiers don't transfer (external). Density and the single-bordered (outline) default carry over from Text Field; filled/underline are theming, not API (see text-field §4). The genuinely Textarea-specific variant axis is the **resize model** (`none | vertical | auto`, §3), which behaves more like an author-chosen variant than a runtime state; `showCount` and auto-grow are orthogonal modifiers on top.

## 5. Usage guidance

**Use** for free-form text expected to exceed one line: comments, descriptions, messages, feedback, multi-line addresses, commit-message bodies. The rough threshold both agents cite is input predictably past the ~40–60 characters a single-line field shows comfortably, or any input that legitimately needs user-authored line breaks (external).

**Don't use** for single-line values (→ Text Field — and don't drop a one-row textarea in as a "bigger input"; the semantics and Enter behaviour differ), for formatted or structured content (→ rich-text editor), for source code (→ a real code editor — Monaco / CodeMirror; a textarea has no syntax highlighting, line numbers, or bracket matching), or for choosing from options (→ Select / Combobox) (both agents).

**Decision frameworks rather than rules:**

- **Auto-grow for composers, fixed-height-plus-scroll for forms.** A chat or comment box should grow with the message; a "Notes" field inside a long form should hold a stable height so the form doesn't reflow as the user types.
- **Set `maxRows` whenever auto-growing.** Uncapped growth pushes the submit affordance off-screen on a long paste (§3).
- **Right-size the initial `rows` to the expected input** — the initial height is a content cue (§3).
- **Counter only when there's a real limit** (§3).
- **Mobile: prefer dictation and minimise typing** where the platform offers it; when a textarea is necessary, the right `inputmode` still applies (see text-field §5).

## 6. Accessibility

The theory is in 14-accessibility, 17-accessibility-annotation-contract, and 28-web-accessibility-implementation; the shared field substrate — label association, the `aria-describedby` helper+error chain, `aria-invalid`, focus contrast, `autocomplete` as the SC 1.3.5 obligation — is in text-field §6 and is not restated. Only what is Textarea-specific:

- **Role and `aria-multiline`.** The native `<textarea>` maps to `role="textbox"` with the implicit `aria-multiline="true"` — the payload that tells assistive tech the Enter key inserts a newline rather than submitting (external). Preserve it; don't reach for a `contenteditable` div that has to reconstruct it by hand.
- **The character counter is the central a11y problem** (the same shape as text-field §6, but more frequent and more load-bearing here). The visual counter updates instantly but is `aria-hidden="true"`; a *separate* visually-hidden node carries the announcement. Two channels (external, converging with GOV.UK/USWDS research):
  - **Static limit on focus** — fold the counter's limit text into the field's `aria-describedby` so tabbing in announces "…, 500 character limit." The user knows the ceiling before typing.
  - **Threshold-based live announcements** — the live region speaks only near the ceiling, not per keystroke (machine-gunning "99… 98… 97…" makes the field unusable). Announce politely at the warning tiers (e.g. last 20 characters, or 80/90/100%), and escalate to `aria-live="assertive"` only when the limit is breached ("Character limit exceeded by 12 characters").
- **Over-limit must be announced, not just coloured.** Crossing the soft cap routes the overage through the live region and sets `aria-invalid`; the error text states the overage. A hard native `maxlength` that silently blocks input is *worse* for AT users — they get no signal that input was dropped (§3).
- **Enter-key semantics are an accessibility contract, not only UX.** If Enter submits (composer), the override must be discoverable — a visible "Shift+Enter for a new line" hint satisfies WCAG **SC 3.3.2 Labels or Instructions** — and there must always be a real submit button so a keyboard or screen-reader user is never trapped or surprised into losing a draft (both agents).
- **Auto-resize must not move the caret or scroll the viewport.** The measurement has to be synchronous with input so the cursor stays put; a resize that jumps the page or strands the caret is a serious failure (Claude).
- **WCAG SCs the component participates in:** the Text Field set (1.3.5, 1.3.1, 3.3.1, 3.3.2, 3.3.3, 1.4.3, 1.4.11, 2.4.13, 4.1.2, 2.5.8 — the resize handle as a target), plus **4.1.3 Status Messages** for the counter/over-limit live region, and **1.4.4 Resize Text / 1.4.10 Reflow** which bite harder here — the textarea and its counter must survive 200% zoom and 320px reflow without the counter colliding with the resize handle or the text clipping (Claude; external supplied 3.3.2 / 4.1.2 / 4.1.3 and the role/`aria-multiline` payload).

## 7. Content guidelines

Inherits the Text Field content discipline — label as a concise noun phrase in sentence case, helper carrying the format before failure, the placeholder-is-not-a-label rule (see text-field §7). Textarea-specific:

- **The placeholder may model the expected *shape*** — "Describe the issue, including steps to reproduce" — but it still vanishes on the first keystroke, so it is a prompt, never instructions to keep. The recall cost is higher here: a user may write several paragraphs, tab away to research, and return to a placeholder that's long gone (external). Anything load-bearing lives in helper text.
- **Counter copy:** "240 / 280" or "40 characters remaining"; over-limit "12 characters over the limit" — constructive and numeric, never "Too long."
- **Error copy** follows SC 3.3.3 — what is wrong *and* how to fix it, with the precise number: "Description must be under 500 characters. Remove 24 to continue." To conserve vertical space the error message may replace the helper text, provided it still carries the original constraint (external — Spectrum).
- **Composer affordance copy:** if Enter submits, say so near the field ("Press Enter to send, Shift+Enter for a new line").
- **Empty/CTA** belongs to the host form, not the textarea (see text-field §7).

## 8. Motion and transition

State transitions (focus/error border, helper→error swap) follow Text Field's ~100–150ms token-driven, eased contract (see text-field §8). The one signature motion here is **auto-grow**, and it is the one most likely to feel broken. The height change should be effectively **instant** on keystroke — do *not* ease a `height` transition, because an animated height lags behind typing and reads as jank, and animating `height` reflows the layout below on every frame (both agents). If a transition is used at all, keep it ≤100ms and drop it entirely under `prefers-reduced-motion: reduce` — honestly, auto-grow is better with no height transition in any case. A second, separate rule: when the user is **dragging the manual resize handle**, strip any transition off the node, or the boundary rubber-bands behind the cursor (external). (See 18-motion-foundations and 19-motion-implementation-web.)

## 9. Internationalization

Inherits the Text Field i18n contract — logical-property RTL mirroring, text expansion of labels/messages with no fixed width, the IME-composition validation guard (see text-field §9). Textarea-specific:

- **RTL mirrors the Textarea-specific chrome too.** The resize handle migrates from the bottom-right to the bottom-left corner, and the trailing-aligned character counter anchors left (external). As on Text Field, set `dir="auto"` on the `<textarea>` so the *content* direction can differ from the UI — a Latin URL or code snippet typed into an Arabic interface renders correctly (both agents).
- **Auto-grow must measure the rendered line box, not an assumed Latin line-height.** Scripts with taller line boxes (Arabic, Thai, Devanagari) grow differently; `minRows` / `maxRows` computed against a hard-coded Latin line-height clip or over-grow (Claude).
- **The IME guard matters more here** than on a single-line field — composing a long CJK passage fires many composition events, and auto-grow measurement and counting must not run mid-composition or the field thrashes (Claude).
- **"A character" is a grapheme, not a code unit.** `value.length` counts UTF-16 code units: a flag emoji costs 4, a ZWJ family sequence up to 11, each rendering as one glyph. Enforcing a limit by `.length` makes non-Latin and emoji users hit the ceiling artificially fast — count with `Intl.Segmenter({ granularity: 'grapheme' })` for any user-facing limit (both agents; this corrects the naive default and is the single most-missed i18n bug in counted fields). (See 13-internationalization-and-rtl.)

## 10. Naming

Nomenclature splits along the architectural line from §1: the variant camp exposes `TextField` + a `multiline` prop (Polaris, Material 3); the distinct camp ships `Textarea` / `TextArea` (Primer, Carbon, Base Web, Atlassian, Fluent) (both agents). **The practice default is `Textarea`** — one word, matching the HTML element, treating "area" as part of the root rather than a `TextArea` compound. The naming follows the structural call (§1): a standalone name signals the standalone machinery. Aliases consumers and designers will reach for, to map as documentation search keywords: `MultilineInput`, `MultilineTextField` / `TextField multiline` (the Material/MUI shape), `TextBox`, `CommentBox`. Composer specialisations get their own names: `MessageComposer` / `ChatInput` (§3).

## 11. Implementation notes

Inherits the Text Field implementation contract — `useId` for the label/describedby chain, `forwardRef` to the input node (here the `<textarea>`, not the wrapper), controlled *and* uncontrolled support, a real `<input name>`-equivalent for native forms and Server Actions, headless-substrate-plus-opinionated-skin (see text-field §11). Textarea-specific:

- **`field-sizing: content` is the auto-grow story now.** Auto-grow historically meant a brittle JavaScript loop: a hidden ghost-sizer styled identically to the textarea, inject the value, read `scrollHeight`, write it back as inline height — notorious for caret jump, layout thrash, and framework-render timing bugs. The CSS property `field-sizing: content` makes the element shrink-wrap its content and grow within `min-block-size` / `max-block-size` natively, handing the calculation to the browser's layout engine (external). **The practice prioritises `field-sizing: content` behind an `@supports` query, falling back to the ghost-sizer polyfill only where unsupported.** This is the biggest near-term implementation shift in the component — but it is current-platform-state dependent: verify support (Chromium 123+, with Firefox following) before relying on it rather than treating these version numbers as settled.
- **The controlled-textarea caret jump.** A strictly controlled `<textarea value={state}>` can jump the caret to the end on rapid typing if React batches or drops a frame — and grapheme counting or synchronous auto-grow on every keystroke makes it worse. Mitigations: paint from an uncontrolled internal ref and flush to the parent asynchronously, or wrap the expensive validation/count in `useDeferredValue` to keep typing at 60fps (external).
- **Recompute height on programmatic value changes,** not only on user input. A reset, or AI-inserted text, that doesn't trigger a resize is a common auto-grow bug (Claude).
- **Single resize per paste, and normalise line breaks** on `onPaste` (§3).
- **Don't reach for `contenteditable`** to add formatting — it sacrifices native undo/redo, spellcheck, reliable IME, and form submission; cross to a real editor instead (§1, §12).

## 12. Related and alternative components

- **Composes with:** Label, Helper/Description text, FieldError, Character counter, Form (the composite owner), Button (the paired submit/send action), Spinner (AI-streaming loading).
- **Alternative to:** Text Field (single-line), Rich Text Editor (formatted/structured content), Combobox / Select (enumerable values), Code Editor (monospace/structured code). *(The external pass typed Textarea as `supersedes: TextField`; that is wrong — they are siblings a designer chooses between by input shape, neither superseding the other. The prose is authoritative; the schema below is corrected.)*
- **Supersedes:** a one-row `<textarea>` used as a "tall input"; a `contenteditable` div used for plain multi-line text.
- **Superseded by:** a rich-text editor when the content needs formatting; otherwise nothing for plain multi-line text.

(See text-field for the shared form-field substrate this brief stands on, 03-component-library for the system-level component model, and 29-per-component-documentation-template for the delivered docs page this brief feeds.)

## 13. Field POV evolution

Macro shifts over the last ~two years, both agents converging on direction:

1. **Auto-grow is becoming the composer default.** Where fixed-height-plus-scroll once ruled, chat/comment surfaces now expect the field to grow with the message; `maxRows`-plus-scroll is the safety valve, learned after early systems (Polaris) shipped unbounded growth that blew out the page on a large paste.
2. **`field-sizing: content` is retiring JS auto-grow** — the layout burden moving off the fragile main-thread loop back into the browser engine. The single biggest near-term implementation change (§11).
3. **Soft limits over hard `maxlength`** — the field is settling on allow-over-then-block-submit with clear feedback, away from silent native truncation.
4. **The character counter matured from afterthought to audited sub-component** — the `aria-hidden` visual plus threshold-based polite live region is now the assumed pattern (shared lineage with text-field §6).
5. **AI co-authoring is the emerging frontier** — streaming generated text into the field (rewrite, summarise, draft) makes a once-rare loading / `aria-busy` state newly relevant and raises open questions about editing while content streams; Carbon's AI-explainability direction is the signal to watch (external), not yet a practice default.
6. **The variant-prop vs. distinct-component split persists** — Material/MUI overload `TextField`; most others keep `Textarea` separate. The practice sides with separate (§1).

## 14. Sources cited

Field-leader systems, conservative version dates (the external pass supplied more precise numbers — Polaris v13.x, Primer React v36.x, Carbon React v11.x, Atlassian v17.x, Fluent v9, Base Web v18.1.0, Material 3 Compose 1.4.0-alpha — held loosely and unverified; `last-audited` in frontmatter is the re-run trigger):

- Shopify Polaris — `TextField` multiline (`maxHeight` / auto-size, `showCharacterCount`); the early unbounded-growth bug (Polaris, 2024–2025).
- Adobe Spectrum / React Aria — `TextArea` / `TextField`, auto-grow, native validation integration, error-replaces-helper guidance (Spectrum, 2024–2025).
- Google Material 3 — text fields `multiline` (the variant-prop model), `TextFieldLineLimits` min/max lines (Material 3 / Compose, 2024).
- IBM Carbon — `TextArea`, `enableCounter` / `maxCount`, AI-presence/explainability direction (Carbon, 2024).
- GitHub Primer — `Textarea`, `FormControl` id-stitching, `resize` control, actions-outside-container posture (Primer, 2024).
- Atlassian Design System — `TextArea`, `minimumRows` / resize, focus-tint treatment (Atlassian, 2024).
- Uber Base Web — `Textarea` overrides, deep sub-component targeting (Base Web, 2024).
- Microsoft Fluent UI (v9) — `Textarea`, `autoAdjustHeight`, `resize` (Fluent, 2024).
- Apple Human Interface Guidelines / Material 3 Compose — multi-line text entry, mobile keyboard behaviour, dictation-first input (Apple HIG / Material, 2024).
- GOV.UK Design System & USWDS — accessible character-counter research (the `aria-hidden` visual + polite-live-region bifurcation; shared lineage with the Text Field brief).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.3.5, 1.3.1, 3.3.1, 3.3.2, 3.3.3, 1.4.3, 1.4.4, 1.4.10, 1.4.11, 2.4.13, 4.1.2, 4.1.3, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: textarea
  name: Textarea
  aliases: [text-area, multiline-input, multiline-text-field, textbox, comment-box]
  category: form
  status: stable
description: >
  Control for free-form text expected to wrap across multiple lines —
  comments, descriptions, messages. Shares the form-field substrate with
  text-field; differs in the sizing model, character-counter prominence,
  and Enter-key semantics. Not single-line (text-field), not formatted
  (rich-text-editor), not code (code-editor).
api:
  inherits: text-field   # label, value/defaultValue, onChange/onBlur/onFocus, placeholder, helpText, error, disabled, readOnly, required, autoComplete, size, id, name + the bundled-props/composed-slots hybrid and internal aria wiring
  props:
    - name: rows
      type: number
      default: 3
      required: false
      description: Initial/min height in LINES (not px); also a content cue. cols is dead on web.
    - name: resize
      type: enum
      values: [none, vertical, auto]
      default: vertical        # 'auto' (auto-grow) is the composer default
      required: false
      description: Sizing model in one prop. vertical for form fields, auto (grow within minRows/maxRows) for composers. NEVER horizontal/both — breaks layout.
    - name: minRows
      type: number
      required: false
      description: Auto-grow floor (with resize:auto).
    - name: maxRows
      type: number
      required: false
      description: Auto-grow cap; beyond it the field scrolls. Always set when auto-growing or growth pushes submit off-screen.
    - name: maxLength
      type: number
      required: false
      description: Character limit, counted by GRAPHEME not code unit. Enforce SOFT (allow over, flag invalid, block submit) — never the hard native maxlength, which silently drops paste overflow.
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
      description: Composer opt-in (Enter submits, Shift+Enter newline). NOT the base default. Always pair with a real submit button + a visible hint.
states:
  inherits: text-field    # rest, hover, focus-visible, disabled, read-only, loading, error, empty
  not-applicable: [pressed]
  textarea-specific:
    focus-visible: large-surface — decouple native outline, inset indicator on container (1.4.11/2.4.13)
    error: error stroke on CONTAINER so the OS scrollbar sits inside the boundary; reserve footer space for counter/resize collision
    read-only: must stay scrollable + selectable so the full value is reachable
    loading: AI-streamed content — aria-busy, do not fight the caret
variants:
  size: [small, medium, large]   # scales type/padding only — height is rows/auto-grow
  resize: [none, vertical, auto]
  style: [outline]               # filled/underline are theming, not API
  modifiers: [auto-grow, show-count]
accessibility:
  inherits: text-field    # label association, aria-describedby chain, aria-invalid, focus contrast, autocomplete as SC 1.3.5
  wcag-criteria: ["1.3.5", "1.3.1", "3.3.1", "3.3.2", "3.3.3", "1.4.3", "1.4.4", "1.4.10", "1.4.11", "2.4.13", "4.1.2", "4.1.3", "2.5.8"]
  aria-attributes:
    - role=textbox          # native
    - aria-multiline=true   # native; preserve — do not reconstruct via contenteditable
    - aria-invalid          # on over-limit / error
    - aria-describedby      # static limit folded in for focus announcement
    - aria-live             # polite on the visually-hidden counter node; assertive on breach
    - aria-busy             # AI streaming
  keyboard-model:
    enter: newline (default) | submit (composer opt-in, with Shift+Enter newline + visible hint + real submit button)
    typing: native multi-line editing, undo/redo, spellcheck, IME
  focus-behavior:
    focus-visible: required
    caret-stability: auto-resize must not move caret or scroll viewport; recompute on programmatic value change too
    ref: forwardRef reaches the <textarea>
  character-counter:
    visual: aria-hidden=true, instant
    announced: separate visually-hidden node; static limit via describedby on focus; polite near limit; assertive on breach
content:
  inherits: text-field    # label/helper/error discipline, placeholder-is-not-a-label
  placeholder-pattern: "may model expected shape; still vanishes on input — higher recall cost here; nothing load-bearing"
  counter-pattern: "'240 / 280' or 'N remaining'; over-limit 'N over the limit', constructive/numeric"
  error-pattern: "what + how to fix with the number (SC 3.3.3); may replace helper if it keeps the constraint; over-limit announced, not colour-only"
i18n:
  inherits: text-field    # logical-prop RTL, dir=auto on the textarea, expansion, IME guard
  textarea-specific:
    - "RTL mirrors the resize handle (bottom-left) and the counter (left)"
    - "minRows/maxRows from the RENDERED line box, not assumed Latin line-height (Arabic/Thai/Devanagari)"
    - "count by grapheme (Intl.Segmenter), never value.length"
    - "IME guard covers auto-grow measurement + counting, not just validation"
implementation:
  inherits: text-field    # useId wiring, forwardRef to the node, controlled+uncontrolled, real name for forms/Server Actions, headless substrate
  textarea-specific:
    - "prefer CSS field-sizing:content behind @supports; ghost-sizer JS polyfill as fallback (verify browser support before relying on it)"
    - "controlled caret-jump: paint from uncontrolled ref + async flush, or useDeferredValue for heavy count/validation"
    - "single resize per paste; normalise \\r\\n -> \\n on paste before counting/storing"
    - "no contenteditable for formatting — cross to a rich-text editor"
composition:
  composes-with: [label, helper-text, field-error, character-counter, form, button, spinner]
  alternative-to: [text-field, rich-text-editor, combobox, select, code-editor]   # NOT supersedes text-field — siblings
  supersedes: ["one-row textarea as a tall input", "contenteditable div for plain multi-line text"]
  superseded-by: ["rich-text-editor when content needs formatting"]
notes:
  contested:
    - sizing model — resize:vertical default forms, resize:auto composers; never horizontal/both
    - hard vs soft maxLength (soft, grapheme-counted)
    - Enter-submits as opt-in, never the base default
    - distinct Textarea vs multiline-prop-on-TextField (we ship distinct)
  emerging:
    - "CSS field-sizing:content retiring JS auto-grow (verify support)"
    - "AI-streamed content as a new loading/aria-busy case"
  inherited: "~80% of the component is the text-field substrate; this schema records only the delta"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-textarea/` (15 June 2026). Both agents converged on the spine — the distinct-component call over a `multiline` prop, the sizing model as the load-bearing divergence with `resize` defaulting to vertical (never horizontal/both) and auto-grow for composers, `rows` as line-count not pixels, `maxRows`-or-overflow, soft over hard `maxLength`, the threshold-based polite character counter with the static limit folded into `aria-describedby`, `field-sizing: content` retiring the ghost-sizer, grapheme counting via `Intl.Segmenter`, `dir="auto"` and RTL mirroring of the resize handle and counter, the instant-or-no-transition auto-grow with the reduce-motion and drag-strip rules, paste line-break normalization, the controlled caret-jump, and the contenteditable/rich-text boundary. This is the first brief to explicitly stand on another — ~80% of Textarea is the Text Field substrate (text-field §§2–4, 6, 7, 9, 11), inherited rather than re-derived, which is itself the methodological point the brief calibrates. External-agent contributions: the ghost-sizer/mirror anatomy, the drifting-trailing-icon trap, the Windows scrollbar-vs-error-border interaction, OS line-break normalization, `useDeferredValue`, the assertive-on-breach escalation, the `role`/`aria-multiline` payload, and the Carbon AI-co-authoring frontier. Claude-pass contributions: Enter-key semantics as both a UX and a11y contract with submit-on-Enter as an opt-in that always keeps a real submit button, `maxRows` as the auto-grow safety valve, line-box-aware sizing and the broadened IME guard for tall scripts, the AI-streaming loading state, and `rows` as a content cue. Two errors in the external pass's §15 were corrected against the prose, which wins: `readOnly` is **not** deprecated (it is the first-class distinct property established in text-field §4), and Textarea is an **alternative to** Text Field, not a superseder — they are siblings. Version numbers are held conservatively per §14; `last-audited` is the re-run trigger. The §15 schema is free-form per the catalogue design spec and will be formalised after ~5 briefs.*
