---
okf_version: "0.1"
type: practice-area
title: Pattern Briefs
description: Field-truth studies of cross-component patterns — the recurring compositions of components that solve a problem (Forms-as-a-system, Filtering, wizards, app shells, page templates). The patterns layer sits above the component catalogue: a component is a thing with props; a pattern is a way of composing things, resolved as decision rules. Upstream of an engagement's pattern library and the practice's POV on composition (03).
tags: [index, patterns]
timestamp: 2026-06-18
---

# Pattern Briefs

A catalogue of cross-component **pattern** briefs. Where the component catalogue (`components/`) studies individual things — a Button, a Form — the patterns layer studies the recurring *compositions* of those things: how the leading systems assemble components to solve a problem, where they converge, where they diverge, and the decision rules the practice lands on. A pattern is mostly decisions and orchestration, not markup; it composes briefed components and records only the delta.

The patterns layer opened once the component catalogue reached the point where whole categories had closed and components were forward-referencing assemblies no single brief could own — the Form brief's "Forms-as-a-system" hand-off being the trigger.

---

## How this layer works

**Relationship to the catalogue.** A pattern names the components it composes as typed references into `components/` and never re-derives them. The pattern-vs-component boundary is the line the Form brief drew: `Form` is the component (the `<form>` primitive + validation orchestration); *Forms-as-a-system* (the multi-step wizard, save-and-resume) is the pattern. When a candidate has a stable prop surface and ships as one importable thing, it's a component, not a pattern.

**Brief shape.** Patterns follow the flexible spine in `_schema.md` — a small ALWAYS core (problem, composition, decision rules, accessibility orchestration, anti-patterns, related, schema) plus SCALES sections (flow & states, layout & structure, content, variants) that appear only when the pattern's tier gives them weight. Unlike the component spine (a locked 15 keys), the pattern spine bends to the tier. Voice and depth match the catalogue and the numbered files.

**The four tiers.** Every pattern declares a `tier`, which predicts its shape: `cross-component-recipe` (composition/decision-heavy), `state-convention` (decision/a11y-heavy, cross-cutting), `flow-and-shell` (flow/layout-heavy), `page-template` (layout-heavy). See `_schema.md` for the definitions.

**Research workflow.** Patterns use the `_research/` dual-agent workspace — the same flow as the catalogue (a prompt run against two agents, synthesized to `patterns/<slug>.md`). Dual-agent is the default; patterns are contested by nature. The run folder is `_research/_inbound/YYYY-MM-DD-pattern-<slug>/`.

**Promotion.** When a pattern lands: flip its entry below from a `scope:` stub to a link + one-line hook + status; add inline cross-references from the component briefs and numbered files where the pattern is now relevant.

---

## The catalogue

The seed list spans the four tiers. The list is the discipline; engagement need pulls a pattern forward. Patterns without briefs carry a `scope:` note.

### Cross-component recipes

- **Forms-as-a-system** — *not yet briefed (the patterns layer's first run).* `scope: the multi-field form beyond a single Form component — multi-section composition, the field-dependency/conditional-reveal model, the cross-field validation orchestration, save-and-resume, the long-form-vs-wizard threshold, and the autosave-vs-explicit-submit decision. Composes Form + all the controls; borders the multi-step wizard (flow-and-shell).`
- **Filtering** — *not yet briefed.* `scope: the filter set (controls applied without a submit) — inline vs panel vs drawer, applied-filter chips (Tag), the clear-all + result-count contract, faceted vs simple, URL/state persistence. Composes Combobox/Select/Checkbox/Tag/Button; the Form-vs-Filter-set boundary.`
- **Search** — *not yet briefed.* `scope: the search experience — the input (SearchField/Combobox), suggestions/typeahead, recent/scoped search, the results + empty/no-results state, instant vs submit. Composes Combobox/Empty State/List.`
- **Common actions (action priority & overflow)** — *not yet briefed.* `scope: the action-priority model — primary/secondary/tertiary, the toolbar, the overflow menu, the responsive action-collapse, destructive-action placement. Composes Button/Menu/Toolbar; the Common actions recipe Carbon names.`
- **Overflow content** — *not yet briefed.* `scope: handling content that exceeds its container — truncation/line-clamp, "show more", responsive collapse, the tooltip-on-truncate pattern. Composes Tooltip/Button/Disclosure.`

### State conventions

- **Disabled** — *not yet briefed.* `scope: the cross-component disabled convention — disabled vs aria-disabled (focusable inactive), when to disable vs hide vs explain, the never-disable-submit rule, the tooltip-on-disabled trap. A cross-cutting rule citing Button/Form/Text Field.`
- **Read-only** — *not yet briefed.* `scope: the read-only convention across controls — read-only ≠ disabled (focusable, copyable, submitted), the display-vs-edit boundary, when read-only vs plain text. Cites Text Field/Form/the controls.`
- **Loading & skeleton orchestration** — *not yet briefed.* `scope: orchestrating loading across a view — the three-loading-patterns choice at page scale (Spinner/Skeleton/Progress), staggered vs all-at-once, optimistic UI, the page-load-vs-in-place-update distinction. Cites Spinner/Skeleton/Progress/Empty State.`
- **Notifications orchestration** — *not yet briefed.* `scope: the notification system — Toast vs Banner vs Inline vs a notification center, priority/severity routing, the do-not-disturb/batching model, the live-region budget. Cites Toast/Banner/Inline Message.`

### Flows & shells

- **App shell / global header** — *not yet briefed.* `scope: the application frame — the global header, the primary nav (Side Navigation), the content region, the responsive collapse, the skip-link + landmark structure. Composes Side Navigation/Link/Menu/Avatar; the page-template substrate.`
- **Login & authentication** — *not yet briefed.* `scope: the auth flow — sign-in/sign-up/reset/MFA, the credential form, the OAuth/passkey options, the error/lockout states, the autofill/one-time-code contract. Composes Form/Text Field/Button.`
- **Multi-step wizard** — *not yet briefed.* `scope: the segmented flow — the step model, progress indication (Stepper), per-step vs end validation, back/next/save-draft, the linear-vs-non-linear decision, the wizard→accordion responsive transform. Composes Form/Button/Progress; the Forms-as-a-system flow sibling.`
- **Destructive confirmation** — *not yet briefed.* `scope: confirming irreversible actions — the confirmation dialog (alertdialog), type-to-confirm, the undo-instead-of-confirm alternative, the never-autofocus-destructive rule. Composes Dialog/Button; the Toast undo lineage.`
- **Save & unsaved-changes** — *not yet briefed.* `scope: the save model — explicit-save vs autosave, the dirty-state guard (beforeunload/route guard), save status feedback, draft persistence. Cites Form/Toast/Banner.`

### Page templates

- **Master–detail (list–detail)** — *not yet briefed.* `scope: the list + detail archetype — split-view vs drill-down, the responsive stack, selection-to-detail, the deep-link/URL model. Composes List/Table + the detail region.`
- **Dashboard** — *not yet briefed.* `scope: the dashboard archetype — the card/widget grid, the responsive reflow, the data-density/refresh model, the empty/loading dashboard. Composes Card/Grid/the data viz boundary.`
- **Settings** — *not yet briefed.* `scope: the settings archetype — the sectioned settings page, immediate-save vs form-submit, the settings-row (label-leading Switch), nav-within-settings. Composes Form/Switch/Side Navigation.`
- **Error pages** — *not yet briefed.* `scope: the full-page error archetype — 404/500/403/offline, the recovery action, the empty-state lineage at page scale, the don't-blame voice. Composes Empty State/Button/Link.`
- **Onboarding** — *not yet briefed.* `scope: the onboarding archetype — first-run, the empty-state-as-onboarding, product tours/coachmarks, progressive setup checklists. Composes Empty State/Dialog/the wizard.`

---

## Provenance

The patterns layer and this index were opened after the component catalogue closed its seventh category (Form). The flexible spine is defined in `_schema.md`; **Forms-as-a-system** is the first worked example, chosen because the Form component explicitly forward-referenced it as the pattern boundary. See `03-component-library` for the practice's POV on the component model the patterns compose, and `CLAUDE.md` for the vault conventions.
