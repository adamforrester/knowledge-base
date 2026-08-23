# Claude run — the behaviour half of the vanilla projection (2026-08-21)

Raw output. Every external claim below was fetched during this run; URLs and fetch dates are inline.
Nothing here is authoritative until synthesised.

**Single-agent run.** No external pass exists. See `prompt.md` for why, and read the confidence
accordingly.

---

## Headline

**Option 1 is not a new invention — it is the native shape of both target platforms, and they
already require it.** AEM Edge Delivery gives every block a co-located `.js` that exports
`decorate()`; Drupal SDC auto-loads a same-named `.js` beside every component. A class-based skin
that ships *no* JS is the odd artefact on both platforms, not the conservative one.

**And the wall is in a different place than #882 assumes.** #882 lists *"`dialog`'s focus trap"*
first, as the hard case. Measured against Adobe's own reference blocks, that is exactly backwards:

| tranche-4 behaviour | what the platform gives | what Adobe's own block actually ships |
|---|---|---|
| dialog / focus trap | **solved natively** — `<dialog>` + `showModal()`, Baseline widely available since March 2022 | 71 lines, uses `showModal()`, no hand-rolled trap |
| accordion / disclosure | **solved natively** — `<details>`/`<summary>` | 23 lines, converts markup to `<details>` |
| **tabs / keyboard model** | **nothing native** | **47 lines, ZERO keyboard handling** — no arrow keys, no Home/End, no roving tabindex |
| select / listbox | `appearance: base-select` **not Baseline** | no block |
| menu | nothing native | **no block at all** |

**The hardest-sounding behaviour is free, and the easy-sounding one is where the gap is — and Adobe's
own published implementation does not close it.** That is the single most decision-relevant fact in
this run.

Confidence: **high** on the platform facts and the Adobe block measurements (all fetched, all
checkable). **Medium** on the prior-art reading. **Low** on anything about cost or maintenance —
see the last section, which is the half that matters for the developer conversation.

---

## 1. What the two named platforms actually do for behaviour

### AEM Edge Delivery Services — behaviour is per-block vanilla ESM, by design

`aem.live/developer/anatomy-of-a-franklin-project` (fetched 2026-08-21):

> "The block name is used as both the folder name of a block as well as the filename for the `.css`
> and `.js` files that are loaded by the block loader when a block is used on a page."

> "The javascript is loaded as a module (ESM) and exports a default function that is executed as part
> of the block loading."

The same page describes "a buildless approach that runs directly from your GitHub repo", and a
philosophy of avoiding proprietary frameworks — developers "write vanilla JavaScript that decorates
block markup".

**So EDS's unit of behaviour is exactly what option 1 proposes**, and it is buildless, which is the
same posture the engine already holds.

### Drupal SDC — behaviour is a same-named JS file, auto-loaded

`drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml`
(fetched 2026-08-21). CSS and JS named after the component load automatically; `libraryOverrides`
takes control when you need it:

> "This is how you take control of the keys in your library declaration. The overrides specified here
> will be merged (shallow merge) with the auto-generated library."

> "Here we are taking control of the JS assets. So we need to specify everything, even the parts that
> were auto-generated."

The documented dependency idiom for behaviour is `core/drupal` and `core/once`, which is Drupal's
standard `Drupal.behaviors` + `once()` re-initialisation pattern.

**Both platforms therefore already have the slot option 1 would fill.** Neither needs to be
convinced that a component can carry JS; both assume it.

---

## 2. How much of tranche 4 is now platform rather than library

All fetched 2026-08-21.

**`<dialog>` — Baseline Widely available, "available across browsers since March 2022"** (MDN). It
provides, natively, the things #882 names as the hard part:

- focus: *"When using `HTMLDialogElement.showModal()` to open a `<dialog>`, focus is set on the first
  nested focusable element."*
- ESC: *"Modal dialogs can also be closed by pressing the Esc key … this behavior is provided by the
  browser."*
- inert background + top layer: *"When using `<dialog>` along with the `HTMLDialogElement.showModal()`
  method, this behavior is provided by the browser."*
- `aria-modal="true"` implicitly.

What authors still owe: an explicit close control, and `autofocus` to place initial focus deliberately.

**Popover API — Baseline 2025, "Newly available. Since January 2025"** (MDN). Gives light dismiss,
ESC, and top layer:

> "this means that you can hide the popover by clicking outside it or pressing the Esc key"
> "popover elements will appear above all other elements in the top layer"

It explicitly does **not** give modality — *"Popovers created using the Popover API are always
non-modal"* — and MDN documents **no** arrow-key navigation and **no** focus trap. Those remain the
author's.

**Invoker commands (`command` / `commandfor`) — Baseline newly available 2025-12-12**
(web-platform-dx web-features explorer, fetched 2026-08-21; Chrome 135 2025-04-01, Firefox 144
2025-10-14, Safari 26.2 2025-12-12; "Expected to be Widely Available on 2028-06-12"). Built-in
commands include `show-modal`, `close`, `show-popover`, `hide-popover`, `toggle-popover` — i.e. **a
declarative open/close wiring with no JavaScript at all**, on `<button>` only.

**Customizable select (`appearance: base-select`) — NOT Baseline.** MDN: *"This feature is not
Baseline because it does not work in some of the most widely-used browsers."* MDN additionally warns
*"Some JavaScript frameworks block these features; in others, they cause hydration failures when
Server-Side Rendering (SSR) is enabled."*

**`<details>`/`<summary>`** needs no JS at all, and the `name` attribute now groups them into an
exclusive accordion natively. (Secondary sources only for the `name` grouping — flagged.)

### The measurement that matters — Adobe's own blocks

`github.com/adobe/aem-block-collection` (fetched 2026-08-21). Blocks present: accordion, cards,
carousel, columns, embed, footer, form, fragment, header, hero, **modal**, quote, search, table,
**tabs**, video. **No menu block. No combobox block.**

- **`blocks/accordion/accordion.js` — 23 lines.** Creates native `<details>`, appends `summary` and
  body, `row.replaceWith(details)`. No ARIA authored; the browser supplies it.
- **`blocks/modal/modal.js` — 71 lines.** `document.createElement('dialog')` … `dialog.showModal()`.
  Native focus management; no hand-rolled trap.
- **`blocks/tabs/tabs.js` — 47 lines.** Sets `role=tab`, `aria-selected`, `aria-controls`,
  `aria-hidden`, and binds exactly one listener:

  > `button.addEventListener('click', () => { … })`

  **Zero keyboard event listeners.** No arrow keys, no Home/End, no roving tabindex. It does not
  implement the APG tabs pattern.

That is Adobe's published reference implementation for the platform we rank #1, and on the one
tranche-4 component with no native element it ships an incomplete keyboard model.

---

## 3. Prior art for option 1 — class-based skin plus a small vanilla layer

**GOV.UK Frontend.** The most rigorous progressive-enhancement system in the field, and it does
exactly option 1.

- Binding: `data-module` initialises a component. `frontend.design-system.service.gov.uk/import-javascript/`
  (fetched 2026-08-21) documents `initAll()`, and per-component:
  ```js
  const $skipLinks = document.querySelectorAll('[data-module="govuk-skip-link"]')
  $skipLinks.forEach(($skipLink) => { new SkipLink($skipLink) })
  ```
  or `createAll(SkipLink)`.
- **It separates three hook kinds.** Its own JS coding standards
  (`github.com/alphagov/govuk-frontend/docs/contributing/coding-standards/js.md`, fetched 2026-08-21)
  distinguish `data-module` for *initialisation* from **`govuk-js-*` classes to target DOM elements**
  — separate again from the `govuk-*` styling classes.
- Scale: roughly ten JS-enhanced components (accordion, button, character count, checkboxes, error
  summary, exit this page, password input, radios, skip link, tabs) out of a catalogue several times
  that, and all work without JS.
- **It publishes no modal/dialog component at all.** `alphagov/govuk-design-system-backlog` issue #30
  ("Modal dialogue") is *Not published*.

**USWDS.** Vanilla JS, CommonJS modules, `receptor` for event delegation. Binds via **the styling
class**: *"The components store an HTML class (like `.usa-accordion__button[aria-controls]`) used to
link HTML elements with the JavaScript component."* (`github.com/uswds/uswds` README, fetched
2026-08-21.) Known consequence, documented on Drupal's `uswds_base` issue queue: components that
require explicit initialisation break for elements added later by AJAX.

**Bootstrap 5.** Vanilla, no jQuery. Data-attribute API is the *preferred* path:
*"Nearly all Bootstrap plugins can be enabled and configured through HTML alone with data attributes
(our preferred way of using JavaScript functionality)."* Hooks are `data-bs-toggle` etc.
(`getbootstrap.com/docs/5.3/getting-started/javascript/`, fetched 2026-08-21.)

**Three systems, three different binding conventions** — `data-module` (GOV.UK), styling class
(USWDS), `data-bs-*` (Bootstrap). There is no field consensus. This is its own decision and is filed
separately.

---

## 4. Prior art for option 3 — a documented behaviour contract

**The ARIA Authoring Practices Guide is already this, and it is already implementation-agnostic.**
`w3.org/WAI/ARIA/apg/patterns/` (fetched 2026-08-21) publishes Dialog (Modal), Menu and Menubar,
Tabs, Listbox and Combobox patterns, each with keyboard-interaction and roles/states/properties
tables. It is prose guidance, not machine-readable, and it is not per-design-system. *I could not
retrieve an explicit self-description of its normative status* — the About page fetch did not
contain one, so the common claim that "the APG is non-normative" is **unverified in this run**.

**Adobe Spectrum is real prior art for "one spec, N implementations."** Spectrum is the design
system; React Spectrum and Spectrum Web Components are two separate implementations of it, with
`swc-react` wrapping the latter. React Spectrum's own composition — `react-aria` described as
implementing "patterns defined in the ARIA practices specification" — shows the APG functioning as
the behaviour contract in practice. (Search-derived; individual pages not each fetched — **flagged as
weaker sourcing** than the rest of this run.)

**Machine-readable component contracts exist but do not cover behaviour.** "Design System Contracts"
(`ds-contracts-spec.pages.dev`, fetched 2026-08-21; v1.0.1, page built 2026-08-17, GitHub org
`southleft`) specifies *"props and their legal values, anatomy, token bindings, slot constraints,
accessibility semantics, declared events"*. Keyboard interaction and focus management do **not**
appear. It names no production adopters — its evidence is compatibility scoring against "101
components from 8 third-party libraries". **Single source, no adoption evidence, treat as weak.**

---

## 5. Does #252 reappear inside option 1?

**Yes, and there may be nothing to wrap.**

Zag.js is the framework-agnostic behaviour engine `19` §3's own predecessor run identified. Its
installation docs (`zagjs.com/overview/installation`, fetched 2026-08-21) name **React, Vue 3,
Solid.js and Svelte**, and:

> "Zag is available for React, Vue 3, Svelte and Solid.js"

**There is no documented vanilla installation path.** All examples assume a framework adapter.

*Methodological note worth keeping.* An earlier fetch in this same run, against the GitHub README,
concluded that vanilla was supported — inferring it from the marketing line *"The component
interactions are modelled in a framework agnostic way."* The installation docs contradict that
inference. **"Framework-agnostic" in a README describes the core's architecture, not a supported
target**, and a single fetch of promotional prose produced a confident wrong answer inside this run.
The installation page is the load-bearing source.

So if option 1 is chosen, the sub-fork is: author ~4–6 small behaviours ourselves, or write and
maintain a vanilla adapter over someone else's core. That is #252's shape arriving at rank 2, which
`19` §3 currently says it does not govern.

---

## 6. What this run could NOT determine

The half that matters for the developer conversation.

1. **Whether Adobe's tabs gap is deliberate or an oversight.** Adobe publishes no rationale. It could
   be a performance-budget decision, an accepted defect, or unnoticed. Nothing fetched says which,
   and the answer changes whether we treat Adobe's blocks as a floor to beat or a standard to match.
2. **The cost of authoring vs wrapping.** No published figures for either, in any system surveyed.
   Nobody reports maintenance hours, defect rates, or a11y-audit outcomes for a hand-authored vanilla
   behaviour layer.
3. **Whether a vanilla behaviour layer stays vanilla.** No longitudinal evidence. GOV.UK's has held
   for years, which is one data point and not a trend.
4. **Whether a behaviour contract can be gated.** This is the sharpest gap. Prism3's whole discipline
   is that a claim nothing checks will drift — and **nothing in the surveyed literature describes
   testing that an implementation conforms to a published behaviour contract.** The APG has no
   conformance suite. Design System Contracts does not cover behaviour. So option 3's contract would
   be, on current evidence, prose that nothing verifies.
5. **Whether `select` gets platform relief, and when.** Customizable select is not Baseline and no
   shipping date is published for the browsers that lack it.
6. **Whether Drupal SDC's auto-loaded JS re-initialises correctly** for a component rendered many
   times, or after AJAX. `core/once` appears in the docs as a dependency you *add*, not a default,
   and the USWDS/Drupal issue queue shows this is a real failure mode in that combination — but I
   found no authoritative Drupal statement on SDC specifically.
7. **The APG's own normative status** — see §4. Commonly asserted, not verified here.

---

## 7. What I would put to a developer partner

Framed as decisions, since that is what the conversation needs.

1. **Do we match Adobe's floor or beat it?** Their tabs block has no keyboard model. Beating it is
   correct and costs us the thing they declined to build.
2. **Given `<dialog>` and invoker commands, is the residue small enough to author?** On this run the
   genuine residue for tranche 4 is: tabs keyboard model, menu roving tabindex, combobox/listbox.
   Dialog is mostly platform. That is a smaller list than #882 implies.
3. **If we author it, what binds behaviour to markup** — a styling class, a `js-` class, or a
   `data-*` attribute? Three surveyed systems, three answers, and for us the class names are a
   versioned contract, which raises the cost of getting it wrong.
4. **Can a behaviour contract be gated, or is it prose?** If it cannot be checked, option 3 is
   documentation, and this repo's own experience is that unchecked claims drift.
5. **Is `select` in or out?** It is the one component where the platform is not coming to help on any
   published timetable.
