---
okf_version: "0.1"
type: component-brief
title: Date Picker
description: The catalogue's most internationalization-sensitive Form composite — a field-truth study of the input-vs-calendar duality and the segmented-input-vs-masked-input a11y pattern (why segmented won), the calendar-as-role=grid + the full APG grid keyboard model (Left/Right day, Up/Down week, PageUp/Down month, Shift+PageUp/Down year, Home/End week, focus-on-open), the native-<input type=date>-vs-custom platform decision (+ the emerging styleable-native path), single-vs-range (the "which end" state machine + the reverse-selection trap), the Temporal/@internationalized/date representation over broken JS Date (the off-by-one-day timezone trap), and the deepest i18n in the catalogue (format order / first-day-of-week / calendar system / RTL) — standing on Text Field (the field) + Popover (the calendar overlay), the calendar a role=grid (the Table/Tag/Tree lineage), composing Button/Icon, with the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [DatePicker, DateField, Calendar, DateRangePicker, RangeCalendar, DateInput, DatePickerDialog, TimeField, DateTimePicker]
last-audited: 2026-06-18
timestamp: 2026-06-18
---

# Date Picker

> A Date Picker lets a user enter a date by **typing it** and/or **picking it from a calendar** — and that duality is the whole component. It is a **Form composite** (one of the briefs closing the Form category) and the catalogue's **most internationalization-sensitive component**: a date's *meaning*, *order*, *first day of week*, and *calendar system* all vary by locale, so a picker that hardcodes "MM/DD/YYYY, Sunday-first, Gregorian" is broken for most of the world. It stands on two briefed substrates — **Text Field** (the date input is a form field: label/helper/error/`aria-describedby`, the validation model, read-only ≠ disabled — see text-field) and **Popover** (the calendar is an anchored, light-dismiss overlay — see popover) — and the **calendar grid is a `role=grid`**: the interactive-grid pattern the catalogue has now drawn for **Table**, **Tag**'s removable group, and **Tree** (a date grid *is* an interactive grid, not CSS `display:grid` — see table, tag, tree, grid). Three decisions define it: **the input-vs-calendar duality + the segmented-vs-masked input** (the headline — segmented won), **native `<input type=date>` vs custom** (the platform call, like Select's — a framework not a winner), and **the Temporal / i18n depth** (the date *representation* + the locale model, deeper here than anywhere else). What it *isn't*: a plain **Text Field** (a typed date with no calendar — see text-field), a **Select** (a date isn't a small fixed option set), or a **Time Picker / DateTime / Date Range** (the *family* it anchors). Why systems disagree: the input model, native-vs-custom, single-vs-range, and the calendar-system depth.

---

## 1. Framing
A date picker glues a **text input** (type a known date — the efficiency/a11y default) to a **calendar popover** (browse/pick an unknown date — booking); the field-truth is that the best practice is **both**, and the component's whole difficulty is orchestrating the two against the deepest localization surface in the catalogue. It is not a Text Field with a regex mask bolted on, nor a Select of dates — it is an orchestration of two system substrates plus a date model and a locale model that field leaders are still converging on.

Three decisions define it:
- **The input-vs-calendar duality + the segmented-vs-masked input (the headline).** The input model is the field-truth crux: the modern **segmented input** (separate day/month/year segments, each a `role=spinbutton`, arrow-keys increment, type-to-fill, **locale-ordered** — React Aria's DateField) vs the legacy **masked single input** (`__/__/____`). The segmented input won because it sidesteps freeform-text *parsing*, handles locale order natively, and announces per-segment — the masked input is parsing-fragile and screen-reader-hostile (§6).
- **The native `<input type=date>` vs custom decision** (the platform call, like Select's native-vs-custom): native is free + accessible but unstylable, browser-inconsistent, and can't do range; custom gives full control + range + branding at the cost of owning the entire a11y/keyboard model. A framework, not a winner — and the emerging styleable-native path could collapse the trade (§5, §11).
- **The Temporal / i18n depth.** The date *representation* (JS `Date` is broken — mutable, timezone-coupled, no date-only type; Temporal / `@internationalized/date` is the modern foundation) plus the locale model (format order, first-day-of-week, calendar system) is deeper here than anywhere else (§9).

What it *isn't*: a plain Text Field (a typed date with no calendar — see text-field), a Select (a date isn't a small fixed set), or a Time Picker / DateTime / Date Range (the *family* it anchors — forward-referenced).

## 2. Anatomy and parts
The input relies on a **segmented model** rather than a continuous string, and the overlay on a strictly tabulated **grid**. The anatomy expands sharply for ranges and date-time.
- **the date input (the field)** — the **segmented input**: locale-ordered day/month/year segments (each a `role=spinbutton`), with **literal separators** (the localized, non-interactive `/`, `-`, `.` between segments) and a placeholder showing the *format* (not the label); inherits the Text Field label/helper/error chain (see text-field). (Legacy: a masked single `<input>` — §6.)
- **the calendar trigger** — a **Button** with a calendar **Icon** opening the popover (see button, icon); the field + trigger together form the "combo" picker.
- **the calendar popover** — an anchored **Popover** (see popover) containing:
  - **the header** — the month/year label + **navigation** (prev/next month chevrons — Icon Buttons; a month/year jump for fast travel, critical for birthdates — §5).
  - **the day grid** — a `role=grid` of weeks × days: the weekday **column headers** (localized, shifted to the locale's first day), the **selected** date (`aria-selected`), **today** (a marker, not selection), **disabled/unavailable** cells (min/max + blackout), the **outside-month** cells (faint, trailing/leading days that keep the grid rectangular and trigger pagination on click), and the optional **week-number** column (the ISO week, a European-enterprise affordance).
  - **the grid cells** — the individual selectable days, each an interactive node in the roving tabindex (composing Button — see button).
  - **the footer / presets** — optional quick selections ("Today", "Last 7 days", "This month") or an explicit confirm action.
- **the range affordances** — for a range the input becomes **dual** (two fields, or a single multi-input separated by a range literal `MM/DD/YYYY – MM/DD/YYYY`) and the popover expands to **dual calendars** (two sequential months side by side), with **range highlighting** spanning the cells between start and end + a hover-preview.
- **the (absence of) freeform parsing** — the segmented input means there's no fragile free-text date string to parse (the key anatomical consequence of the segmented model).

## 3. Properties / API
Systems converge tightly here — the convergence is driven by the constraints of date math and i18n.
- **`value` / `defaultValue`** — a date (or a `{ start, end }` range), as a **Temporal `PlainDate`** / `@internationalized/date` `CalendarDate` value, *not* a JS `Date` (§9/§11). Controlled and uncontrolled; `onChange` emits the new value (a tuple/object for ranges).
- **`granularity`** — `date` / `datetime` / `time` (the family: DateField vs DateTimePicker vs TimeField); `datetime` automatically renders a time-selection interface alongside the calendar.
- **`selectionMode`** — single / range / multiple (range is the materially-harder one — §5; multiple turns the field into a tokenized list of dates).
- **`minValue` / `maxValue`** — the hard absolute bounds; cells outside are muted, stripped of pointer events, and skipped in keyboard navigation.
- **`isDateUnavailable(date)`** — a predicate evaluated against every rendered cell; `true` marks the date unavailable (blackout/booked days, weekends). The interaction of min/max (a *continuous* valid range) with `isDateUnavailable` (discrete *holes*) is the validation crux — the state machine must handle a user spanning a range across an unavailable date.
- **the locale model** — `locale` (drives the format ORDER + month/day names), `firstDayOfWeek` (Sun/Mon/Sat, usually locale-derived, overridable), `calendar` (Gregorian/Islamic/Hebrew/Buddhist/Japanese/Persian — `Intl`/Temporal), `formatOptions` (an `Intl.DateTimeFormatOptions`, *not* a hardcoded string mask).
- **`native` vs custom** — render the native `<input type=date>` (simple) vs the custom segmented+calendar (branded/range — §5).
- **`closeOnSelect`** — dismiss on selection; defaults `true` for single dates, **`false` for ranges** (until the end is confirmed).
- **validation** — `isInvalid` / `isRequired` + the error message (inherits Text Field's presentational-by-default model — see text-field); out-of-range and invalid-date errors.
- **the segmented-input behavior** — type-to-fill (auto-advance segments), arrow-increment per segment (incrementing a segment wraps without affecting its neighbours), the locale-ordered render.
- **what it withholds** — Date Picker doesn't reinvent the form-field chrome (Text Field) or the overlay (Popover); it adds the calendar + the date model + the locale.

## 4. States and variants
- **The field states:** empty (showing the format placeholder `mm/dd/yyyy`) / filled / **focused-segment** (one segment active, `:focus`/`[data-focus-visible]` on it while the others stay idle) / invalid (`aria-invalid`, the error typography/border) / disabled (muted, no interaction) / read-only. **Read-only ≠ disabled:** a read-only picker stays focusable and screen-reader-accessible, rejects mutation, and — a deliberate enterprise nuance — typically **still opens the popover for browsing** (see text-field for the substrate distinction).
- **The calendar cell states:** open / closed; per-cell — **focused** (roving tabindex), **selected** (`aria-selected`, the primary-fill prominence), **today** (a marker — weight/underline/tint, an orienting landmark, *not* selection), **disabled** (out of min/max — muted, not focusable), **unavailable** (blackout), **outside-month** (faint, keeps the grid rectangular), and for ranges — **range-start/end** (endpoint prominence), **in-range** (a subtle full-width tint connecting the endpoints), **range-in-progress** (the volatile hover-preview tracking the pointer between the chosen start and the hovered end).
- **Variants:**
  - **selection:** single / range / multiple.
  - **granularity:** date / datetime / time.
  - **input model:** segmented (modern) / masked (legacy) / native.
  - **calendar layout:** single / dual (range) / with-presets / with-week-numbers / **inline** (the calendar detached from the popover, rendered directly in flow — scheduling apps, sidebars).
  - **native vs custom.**

## 5. Usage guidance
The selector decision turns on the user's intent — **text-first data entry** vs **calendar-first exploration**.
- **The text-first vs calendar-first call:** for a *known* date the user holds in mind (a birthdate, a card expiry, a deadline), **lead with the segmented text input** — typing `04 15 1985` is faster than clicking through a calendar, and it's the a11y-efficient path; the calendar is the assist. For an *unknown/browsed/relational* date (an available appointment slot, a flight, a delivery window) where the user needs to see weekdays/weekends/availability, **lead with the calendar** for the spatial context. Ship both; bias the affordance to the use case.
- **The year-navigation problem (the birthdate trap):** a calendar defaulting to the current month is hostile for a birthdate 40 years ago (40 month-clicks backward — a catastrophic usability failure). For far-from-today dates the **segmented input is the right primary** (type "1985"), and the calendar needs a **fast year/month jump** (a year dropdown/grid), not just month chevrons.
- **Date Picker vs the alternatives:**
  - **vs a plain Text Field** — if there's no benefit to a calendar (a pure typed date), a Text Field with a date mask *can* suffice, but the segmented Date Picker is more accessible and locale-correct (see text-field).
  - **vs native `<input type=date>`** — native for *simple, low-stakes, single-date* cases (a quick form, an MVP, aggressively mobile-first contexts where the OS tumbler is ergonomically best) where free + accessible beats branded; **custom** for branded UI, **range**, complex min/max/unavailable, or consistent cross-browser rendering. Native can't do range and is unstylable — that's the decision boundary (see select for the parallel).
  - **vs a Select** — a date isn't a small fixed set; don't build three Selects (day/month/year) — that's the segmented input's job, done worse (see select).
- **Single vs range:** a unified **Date Range Picker** is optimal when start and end are interdependent and close in proximity (a three-day hotel stay — the whole span is visible on one or two adjacent months). **Two standalone single pickers** are preferred when the dates are conceptually distinct or widely separated (an employment start and end spanning years — a range UI would force dragging across dozens of paginated months). Use presets for common ranges.

## 6. Accessibility
Date Picker is one of the catalogue's hardest a11y components — it has *two* interaction models (the input and the grid) and the deepest locale surface. The standard has decisively moved from masked single-string inputs to the segmented model and the strict APG grid.
- **The segmented input vs the masked-input failure (the input crux).** The historical masked single `<input type=text>` with a regex mask is fundamentally hostile to screen readers: AT announces the punctuation verbatim ("underscore slash underscore"), can't convey structure, and single-string parsing is fragile (typing `31` for a month silently breaks the regex or builds an invalid date). The modern accessible input is **segmented**: each component (day/month/year) is a separate **`role=spinbutton`** with its own `aria-label` and `aria-valuemin`/`max`/`now`/`text`; arrow keys increment/decrement (the day at 31 wraps to 1 without touching the month), typing fills and auto-advances, and the segments render in **locale order**. This announces cleanly ("Month, December, 12 of 12") and sidesteps the freeform-text parsing nightmare. The practice default is **segmented** (React Aria's DateField is the reference).
- **The calendar as the APG grid pattern (the keyboard crux).** The calendar is `role="grid"` (with `role="row"`/`role="gridcell"` and weekday column headers); **one tab stop** into the grid (roving tabindex — only one cell holds `tabindex=0`; Tab exits the grid), then:
  - **Left/Right** — previous/next day; **Up/Down** — previous/next week (7 days); **PageUp/PageDown** — previous/next month; **Shift+PageUp/PageDown** — previous/next year; **Home/End** — first/last day of the current week (row).
  - the **selected** date carries `aria-selected="true"`; **today** is marked (visually + an accessible hint, not via selection); **disabled/unavailable** dates are `aria-disabled` and kept in the DOM (not stripped) so the grid stays spatially consistent.
  - **focus-on-open** — `Enter`/`Space` on the trigger opens the dialog and moves focus to the **selected date** (or today if none); selecting a cell closes the dialog and **returns focus to the trigger**.
- **The popover/dialog contract** — the calendar is in a Popover/dialog (named via `aria-label`/`labelledby`); the month/year **header is an `aria-live="polite"` region** (PageUp announces "February 2026"); the nav buttons have accessible names ("Previous month").
- **Validation announcement** — invalid/out-of-range errors via the Text Field `aria-describedby`/`aria-invalid` chain (see text-field); the trigger's accessible name updates with the selection ("Change date, selected June 18, 2026"); announce *why* a date is unavailable where possible.
- **The native baseline** — `<input type=date>` is accessible out of the box (the OS picker + the field) — its a11y advantage, at the cost of styling/range.
- **WCAG SCs:** **1.3.1** (info & relationships — the grid + the segmented field structure), **2.1.1** (keyboard — the full grid model + the segments, no mouse needed), **4.1.2** (name/role/value — the spinbutton segments, `aria-selected`, the nav), **2.4.3** (focus order — focus-on-open, return-on-close), **1.4.13** (the calendar popover dismiss/hover contract — see tooltip/popover). One of the deepest a11y briefs in Form.

## 7. Content guidelines
- **The format hint** — show the expected format as a **placeholder/segment hint** (`MM/DD/YYYY` rendered by the segments), *locale-correct*, and **never as the label** (placeholder-is-not-a-label — see text-field). The segmented input shows the format implicitly via its segments.
- **The label** — a clear field label ("Start date", "Date of birth"); helper text for constraints ("Must be in the future", "Select a delivery window").
- **The error copy** — specific to the violation: "Date must be after June 18, 2026" / "This date is unavailable for booking", *not* a generic "Invalid date".
- **The month/weekday labels** — locale-correct full + abbreviated names (via `Intl` — §9); the weekday header row uses short forms with an accessible full name.
- **The range labels** — "Start" / "End" (or the dual-calendar headers); the selected-range summary ("Jun 1 – Jun 7, 2026").

## 8. Motion and transition
- **The calendar open/close** — inherits the Popover enter/exit animation (the `@starting-style`/top-layer transition — see popover); a brief scale/fade from the trigger anchor.
- **The month transition** — navigating months slides the grid directionally (Next pushes the current month out left, the new one in from the right — correlating the UI with the linear progression of time); keep it fast and skip it for keyboard rapid-nav.
- **The range hover-preview** — the in-progress range highlights on hover between the chosen start and the hovered end, and must track the pointer **instantly with no transition delay** (a `transition: background 0.2s` makes the highlight lag sluggishly behind the cursor during rapid scanning); the keyboard equivalent is the focus moving through the range.
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops the month-slide and the open animation to instant; the date is the information, not the motion.

## 9. Internationalization
This is **the deepest i18n in the catalogue** — a date picker is i18n-*critical*, not i18n-optional. Hardcoding formats, month-name arrays, or weekday order is a systemic anti-pattern.
- **The format order** — MDY (US) / DMY (most of Europe and the world) / YMD (ISO, East Asia) — driven by **`Intl.DateTimeFormat`** per locale, **never hardcoded**; the segmented input reorders its segments to match the locale string.
- **The first day of the week** — Sunday (US/JP) vs Monday (most of Europe, ISO) vs Saturday (parts of the Middle East) — the grid headers and the leading-blank offset are computed from locale rules, not assumed.
- **The calendar system** — Gregorian is *not* universal: **Islamic (Hijri), Hebrew, Buddhist (Thai), Japanese (era), Persian, Ethiopic** calendars are first-class needs; the modern foundation (`Intl`/Temporal/`@internationalized/date`) renders non-Gregorian grids, and the picker must render the right one per locale/preference.
- **RTL** — the calendar grid **mirrors** (the week runs right-to-left, Sunday/Monday on the right moving leftward), the popover anchors to the opposite side, and the "Next month" chevron points left — via logical properties; the day-of-week columns reverse.
- **Month/day names** — localized full + abbreviated (via `Intl`).
- **The representation (the Temporal foundation).** The native JS `Date` is the source of profound, systemic bugs: it is mutable, secretly attaches the user's local timezone to every instance, and has no date-only primitive — so a birthday selected as midnight Oct 5 in New York serializes to UTC and renders as Oct 4 in California (the classic off-by-one-day bug). Use **Temporal `PlainDate`** (a calendar date with zero timezone awareness — the gold standard for date-only pickers: birthdays, holidays), **`ZonedDateTime`** only when a timezone genuinely matters (a time-bound event across timezones), and **`PlainTime`** for the Time Picker sibling. Format/parse via `Intl.DateTimeFormat`. The timezone trap is the most common date bug; dropping timezone context where it doesn't belong prevents the serialization drift. See 13-internationalization-and-rtl for the locale/calendar-system depth this brief leans on.

## 10. Naming
- **The field set:** **`DatePicker`** (the composite: field + calendar — MUI X, Ant, Carbon, Polaris, Fluent, React Aria); **`DateField`** (the segmented input *alone* — React Aria/Spectrum, MUI X); **`Calendar`** (the grid *alone* — React Aria, MUI's `DateCalendar`); **`DateRangePicker`** / **`RangeCalendar`** (the range — React Aria, MUI X); **`DatePicker` + `RangePicker`** (Ant); the APG term **"Date Picker Dialog"**.
- **The practice's default — `DatePicker`** for the composite (the field + the calendar popover), built from **`DateField`** (the segmented input, usable standalone) + **`Calendar`** (the grid, usable standalone) + **Popover**. The range is **`DateRangePicker`** (composite) / **`RangeCalendar`** (grid). The **family** — `TimeField`, `DateTimePicker` (date + time), `Calendar`/`RangeCalendar` — shares the segmented-input + grid substrate.
- **Aliases to map:** DateField, Calendar, DateRangePicker, RangeCalendar, DateInput, DatePickerDialog, TimeField, DateTimePicker.

## 11. Implementation notes
- **The segmented input over the masked input** — render locale-ordered segments (each `role=spinbutton` with min/max/value), type-to-fill with auto-advance, arrow-increment, and a non-parsing value model (each segment holds a number, assembled into the `PlainDate`) — this is why the segmented input avoids the freeform-text-parsing nightmare. React Aria's `useDateField`/`useDateSegment` is the reference; don't build a regex date parser.
- **The calendar `role=grid` + the full keyboard model** — `role=grid` of weeks/days, roving tabindex over the focused date, the arrow/Page/Home-End model (§6), focus-on-open to the selected/today date, return focus on close. The grid keyboard model is the bulk of the work (shared lineage with Table/Tree's grid — see table, tree).
- **The native-vs-custom toggle (+ the styleable-native direction)** — offer a `native` mode (`<input type=date>` — free a11y, no range, unstylable) and the custom mode (segmented + calendar). Track the **emerging CSS customizable date input** (the Open UI direction toward a styleable native picker via `appearance: base` + pseudo-elements like `::picker()`, akin to `appearance: base-select` for Select — see select). As of mid-2026 `appearance: base-select` is shipping for dropdowns but **native date-input styling remains volatile and polyfill-dependent** — ship fully custom JS date grids until it reaches baseline. Date this; it would collapse the native-vs-custom trade if it lands (`notes.unverified`).
- **The range state machine** — track `{ anchor, focus }`: the first click sets the anchor and enters a `selecting_end` state; while in it, hovering computes the highlight array from anchor → hovered date; the second valid forward click sets the end, normalizes so start ≤ end, fires `onChange`, and (typically) closes. Handle the **reverse-selection trap** — clicking a date *before* the anchor: the established best practice (MUI X, React Aria) is to **reset** — the earlier date overwrites and becomes the new anchor, staying in `selecting_end` awaiting a forward selection. Dual calendars share one state. The hardest UX logic in the component.
- **The Temporal / `@internationalized/date` representation** — model values as **`PlainDate`** (date-only), `ZonedDateTime` (datetime with timezone), `PlainTime` (time) — *never* a JS `Date` (mutable, timezone-coupled, no date-only type). Format/parse via `Intl.DateTimeFormat`. This avoids the off-by-one-day timezone bug and gives non-Gregorian calendar support for free. React Aria ships `@internationalized/date` today; the **Temporal API (ES2026)** is the platform's eventual replacement — shipping in major engines (Firefox 139, Chrome 144) with `@js-temporal/polyfill` for older environments (`notes.unverified` on exact version/baseline).
- **min/max + unavailable** — `minValue`/`maxValue` clamp the navigable/selectable range; `isDateUnavailable(date)` marks blackout days `aria-disabled`; the segmented input also rejects out-of-range.
- **Headless vs opinionated** — the segmented-input state machine, the calendar grid keyboard model, the range state machine, and the calendar-system/locale math are heavy headless logic (React Aria `useDatePicker`/`useCalendarGrid` / MUI X own this, with date-library *adapters* — day.js/luxon/date-fns/Temporal). **Build on a headless engine + a date library** — the i18n + Temporal + grid keyboard model is far too much to hand-roll.

## 12. Related and alternative components
- **Stands on:** **Text Field** (the date input is a form field — label/helper/error/`aria-describedby` + validation + read-only≠disabled — see text-field) and **Popover** (the calendar is an anchored light-dismiss overlay — see popover).
- **The calendar is a `role=grid`** — the interactive-grid pattern shared with **Table** / **Tag**'s removable group / **Tree** (a date grid is an interactive grid, not CSS `display:grid` — see table, tag, tree, grid).
- **Composes:** **Button** (the trigger + month/year nav + the grid cells) + **Icon** (the calendar icon + nav chevrons — see button, icon).
- **Borders:** **Select** + **Combobox** (the native-vs-custom platform decision, like Select; the type-to-fill analogue the segmented input rendered obsolete — see select, combobox).
- **The family:** **Time Picker** / **DateTime Picker** (date + time) / **Date Range Picker** / **Calendar** (the standalone grid) — all share the segmented-input + grid + Temporal substrate.
- **Alternative to:** a plain **Text Field** with a date mask (no calendar), the **native `<input type=date>`** (simple/low-stakes), and (anti-pattern) three Selects for day/month/year.

(A Form composite — the typed-input + calendar-popover date selector, and the catalogue's most i18n-sensitive component. It stands on Text Field (the field) + Popover (the calendar overlay), the calendar is a role=grid (the Table/Tag/Tree lineage), and it composes Button/Icon. See text-field for the field substrate, popover for the overlay, table/tree for the grid keyboard lineage, select for the native-vs-custom decision, 13-internationalization-and-rtl for the locale/calendar-system depth. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The Masked Era (pre-2020).** A single `<input type=text>` forced into a rigid regex mask (`DD/MM/YYYY`), paired with bulky inaccessible popovers (jQuery UI, Bootstrap). Screen readers failed to interpret the masked input; timezone bugs were rampant from the unmitigated JS `Date`.
2. **The ARIA & Headless Era (2020–2025).** The industry adopted the segmented `role=spinbutton` input (led forcefully by React Aria) and enforced the APG `role=grid` calendar; the field accepted that date parsing is too complex/localized for regex, leaning on adapter libraries (date-fns, day.js) and headless logic separating the state machine from the styled DOM.
3. **The Temporal & Platform Era (2025–present).** The systematic deprecation of JS `Date` for UI state in favour of the **ES2026 Temporal API** (`PlainDate`), permanently solving cross-timezone mutation; simultaneously the early emergence of the **Open UI `appearance: base`** direction hints at a future where fully custom JS calendar logic may no longer be strictly required — though the spec remains in active development and the calendar-as-`role=grid` and the dual-calendar range state machine are by now settled.

## 14. Sources cited
*(Conservative; 2026 platform-version specifics flagged unverified under §15.)* **Adobe Spectrum / React Aria** — `DateField`/`DatePicker`/`DateRangePicker`/`Calendar`/`RangeCalendar` + `@internationalized/date` and `useDateField`/`useDateSegment`/`useCalendarGrid` (the gold-standard segmented-input + grid + i18n reference); **MUI X** — `DatePicker`/`DateRangePicker`/`DateField`/`DateCalendar` (the segmented field + calendar; the date-library adapters; the Pro tier for range); **Ant Design** — `DatePicker` + `RangePicker` (panels, presets); **IBM Carbon** — `DatePicker` (flatpickr-based); **Shopify Polaris** — `DatePicker`; **Microsoft Fluent** — `DatePicker` / `Calendar`; **Atlassian** — the date picker; **flatpickr / react-day-picker** — the headless/standalone calendar libraries; native **`<input type=date>`** + the **Open UI customizable date-input** (`appearance: base`) direction; the **Temporal API** (`PlainDate`/`ZonedDateTime`, ES2026) + `@internationalized/date`; **WAI-ARIA APG** — the **Date Picker Dialog** pattern + the grid keyboard model and `role=spinbutton` segments. WCAG 2.2 — 1.3.1, 2.1.1, 4.1.2, 2.4.3, 1.4.13.

## 15. Agent-consumable schema
```yaml
identity:
  id: date-picker
  name: Date Picker
  aliases: [DatePicker, DateField, Calendar, DateRangePicker, RangeCalendar, DateInput, DatePickerDialog, TimeField, DateTimePicker]
  category: form
  status: stable
description: >
  A Form composite for entering a date by TYPING (a segmented input) and/or PICKING from
  a CALENDAR popover — the catalogue's most i18n-sensitive component. Stands on Text Field
  (the date input is a form field) + Popover (the calendar overlay); the calendar is a
  role=grid (the interactive-grid pattern of Table/Tag/Tree, NOT CSS display:grid). NOT a
  plain Text Field (a typed date, no calendar), NOT a Select (a date isn't a small fixed
  set), NOT a Time Picker (the family it anchors). Three decisions: the input-vs-calendar
  duality + the segmented-vs-masked input (segmented won), native <input type=date> vs
  custom (a framework not a winner), and the Temporal/i18n depth (format order / first-day
  / calendar system, on Temporal/@internationalized/date, never JS Date).
anatomy:
  parts:
    - "the date input (the field): a SEGMENTED input — locale-ordered day/month/year segments, each a role=spinbutton, with literal separators (localized /,-,.) + a format placeholder (not the label); inherits the Text Field label/helper/error chain. (Legacy: a masked single input)"
    - "the calendar trigger: a Button + calendar Icon opening the popover"
    - "the calendar popover (a Popover): header (month/year label + prev/next chevrons + a month/year jump for fast travel) + the DAY GRID (role=grid of weeks x days: weekday column headers, selected/today/disabled/unavailable/outside-month cells, optional ISO week-number column) + grid cells (Buttons) + a footer/presets"
    - "the range affordances: dual inputs (two fields, or one multi-input with a range literal) + dual calendars (two sequential months) with range-highlight + hover-preview"
    - "the presets: optional quick ranges (Today / Last 7 days / This month)"
    - "the (absence of) freeform parsing: the segmented input means no fragile free-text date string to parse"
api:
  inherits:
    - text-field   # the date input is a form field — label/helper/error/aria-describedby + validation + read-only != disabled
    - popover      # the calendar is an anchored light-dismiss overlay
  calendar-is: [grid]   # role=grid (the interactive-grid pattern of Table/Tag/Tree)
  composes: [button, icon]
  props:
    - {name: value/defaultValue, type: "PlainDate | {start,end}", default: ~, required: false, description: "a Temporal PlainDate / @internationalized/date value — NOT a JS Date"}
    - {name: granularity, type: "'date'|'datetime'|'time'", default: date, required: false, description: "the family: DateField / DateTimePicker / TimeField; datetime renders a time interface alongside the calendar"}
    - {name: selectionMode, type: "'single'|'range'|'multiple'", default: single, required: false, description: "range is the materially-harder one (the 'which end' state machine); multiple = a tokenized list of dates"}
    - {name: "minValue/maxValue", type: PlainDate, default: ~, required: false, description: "hard absolute bounds — cells outside are muted + pointer-stripped + skipped in keyboard nav"}
    - {name: isDateUnavailable, type: "(date)=>boolean", default: ~, required: false, description: "blackout/unavailable predicate (booked days) -> aria-disabled; discrete holes vs min/max's continuous range"}
    - {name: locale, type: string, default: "system", required: false, description: "drives the format ORDER + month/day names"}
    - {name: firstDayOfWeek, type: "0-6", default: "locale-derived", required: false, description: "Sun/Mon/Sat by locale, not assumed"}
    - {name: calendar, type: "'gregorian'|'islamic'|'hebrew'|'buddhist'|'japanese'|'persian'|...", default: "locale-derived", required: false, description: "Gregorian is NOT universal (Intl/Temporal)"}
    - {name: formatOptions, type: Intl.DateTimeFormatOptions, default: ~, required: false, description: "controls the visual string via native Intl, NOT a hardcoded string mask"}
    - {name: native, type: boolean, default: false, required: false, description: "render <input type=date> (simple) vs the custom segmented+calendar (branded/range)"}
    - {name: closeOnSelect, type: boolean, default: "true (single) / false (range)", required: false, description: "dismiss on selection; range stays open until the end is confirmed"}
    - {name: "isInvalid/isRequired + error", type: "boolean/string", default: ~, required: false, description: "inherits Text Field's presentational-by-default validation; out-of-range + invalid-date"}
  withholds: "doesn't reinvent the form-field chrome (Text Field) or the overlay (Popover); adds the calendar + the date model + the locale"
states:
  field: [empty, filled, focused-segment, invalid, disabled, read-only]   # read-only != disabled — read-only stays focusable + typically still opens the popover for browsing
  calendar: [open, closed]
  cell: [focused, selected, today, disabled, unavailable, outside-month, range-start, range-end, in-range, range-in-progress]   # today is a MARKER not selection; outside-month keeps the grid rectangular
variants:
  selection: [single, range, multiple]
  granularity: [date, datetime, time]
  input-model: [segmented, masked, native]
  calendar-layout: [single, dual, with-presets, with-week-numbers, inline]
  delivery: [native, custom]
accessibility:
  wcag-criteria: ["1.3.1", "2.1.1", "4.1.2", "2.4.3", "1.4.13"]
  inherits: [text-field (the validation/aria-describedby chain), popover (the overlay focus/dismiss)]
  segmented-vs-masked: "the modern accessible input is SEGMENTED — each day/month/year segment a role=spinbutton (aria-label day/month/year + valuemin/max/now/text), arrow-increment (wraps without touching neighbours), type-to-fill+auto-advance, LOCALE-ORDERED; announces cleanly ('Month, December, 12 of 12') + sidesteps freeform-text parsing. The MASKED single input (__/__/____) is screen-reader-hostile (AT announces punctuation verbatim, can't parse the partial mask, locale baked in, regex-fragile) — the anti-pattern. Practice default: segmented (React Aria DateField)"
  calendar-grid: "role=grid (+ role=row/gridcell + weekday column headers); ONE tab stop (roving tabindex, Tab exits); Left/Right=day, Up/Down=week, PageUp/Down=month, Shift+PageUp/Down=year, Home/End=week; selected = aria-selected; today MARKED (not via selection); disabled/unavailable = aria-disabled and KEPT in the DOM (grid stays spatially consistent). FOCUS-ON-OPEN to the selected date (or today); return to the trigger on close"
  popover-contract: "the calendar in a Popover/dialog named via aria-label; the month/year HEADER is aria-live=polite (PageUp announces 'February 2026'); the nav buttons named ('Previous month'); the trigger's accessible name updates with the selection ('Change date, selected June 18, 2026')"
  validation: "invalid/out-of-range via the Text Field aria-describedby/aria-invalid chain; announce WHY a date is unavailable where possible"
  native-baseline: "<input type=date> is accessible out of the box (OS picker + field) — its advantage, at the cost of styling/range"
content:
  format-hint: "show the expected format as a locale-correct segment hint (MM/DD/YYYY), NEVER as the label (placeholder-is-not-a-label)"
  label: "a clear field label ('Date of birth'); helper text for constraints ('Must be in the future')"
  error-copy: "specific to the violation ('Date must be after June 18, 2026' / 'This date is unavailable for booking'), not 'Invalid date'"
  names: "locale-correct month/weekday full + abbreviated (via Intl); the weekday header short form + an accessible full name"
  range-labels: "Start / End (or dual-calendar headers); the selected-range summary ('Jun 1 - Jun 7, 2026')"
motion:
  calendar-open: "inherits the Popover enter/exit (@starting-style/top-layer); a brief scale/fade from the trigger anchor"
  month-transition: "navigating months slides the grid directionally (Next pushes current out left, new in from right — correlates UI with time); fast, skipped for keyboard rapid-nav"
  range-hover-preview: "the in-progress range highlights on hover between start and the hovered end — must track the pointer INSTANTLY (no transition delay; a 0.2s transition lags the highlight behind the cursor). Keyboard equivalent = focus moving through the range"
  reduce-motion: "drop the month-slide + open animation to instant; the date is the information, not the motion"
i18n:
  the-deepest-i18n: "a date picker is i18n-CRITICAL, not optional; hardcoding formats/month-arrays/weekday-order is a systemic anti-pattern"
  format-order: "MDY (US) / DMY (most of the world) / YMD (ISO/East Asia) via Intl.DateTimeFormat per locale, NEVER hardcoded; the segmented input renders segments in locale order"
  first-day-of-week: "Sun (US/JP) / Mon (Europe/ISO) / Sat (parts of the Middle East) — locale-derived; the grid headers + the leading-blank offset computed from locale rules, not assumed"
  calendar-system: "Gregorian is NOT universal — Islamic(Hijri)/Hebrew/Buddhist(Thai)/Japanese(era)/Persian/Ethiopic are first-class (Intl/Temporal/@internationalized/date render non-Gregorian grids)"
  rtl: "the calendar grid MIRRORS (week runs right-to-left, Sun/Mon on the right moving left), the popover anchors to the opposite side, the nav chevron points left; the day-of-week columns reverse (logical properties)"
  representation: "use Temporal PlainDate (date-only, no timezone) — NOT a JS Date (mutable, secretly local-tz-coupled, no date-only type -> the classic off-by-one-day bug: a birthday at midnight NY serializes to UTC and renders a day earlier in CA); ZonedDateTime only when a timezone genuinely matters; PlainTime for the Time sibling. Format/parse via Intl.DateTimeFormat. The timezone trap is the most common date bug"
implementation:
  - "the SEGMENTED input over the masked: locale-ordered segments (each role=spinbutton with min/max/value), type-to-fill+auto-advance, arrow-increment, a non-parsing value model (each segment a number, assembled into the PlainDate). React Aria useDateField/useDateSegment is the reference — DON'T build a regex date parser"
  - "the calendar role=grid + the full keyboard model (arrow/Page/Home-End) + focus-on-open to the selected/today date + return-on-close; the grid keyboard model is the bulk of the work (shared lineage with Table/Tree)"
  - "the native-vs-custom toggle (+ the styleable-native direction): a native mode (<input type=date>, free a11y, no range, unstylable) + the custom mode (segmented+calendar). Track the emerging CSS customizable date input (Open UI, appearance:base + ::picker(), akin to appearance:base-select for Select) — as of mid-2026 base-select ships for dropdowns but native date styling is VOLATILE/polyfill-dependent; ship custom JS grids until baseline. Would collapse the native-vs-custom trade if it lands"
  - "the range state machine: track {anchor, focus}; first click sets the anchor (enter selecting_end), hover previews anchor->hovered; second forward click sets the end (normalize start<=end), fires onChange, closes. The REVERSE-SELECTION TRAP — a click before the anchor RESETS (the earlier date becomes the new anchor, stays selecting_end; MUI X / React Aria). Dual calendars share one state. The hardest UX logic"
  - "the Temporal/@internationalized/date representation: PlainDate (date-only) / ZonedDateTime (datetime+tz) / PlainTime — NEVER a JS Date. Format/parse via Intl.DateTimeFormat -> avoids off-by-one + gives non-Gregorian for free. React Aria ships @internationalized/date today; the Temporal API (ES2026) is the platform replacement (Firefox 139 / Chrome 144; @js-temporal/polyfill for older)"
  - "min/max + unavailable: minValue/maxValue clamp the navigable/selectable range; isDateUnavailable marks blackout days aria-disabled; the segmented input also rejects out-of-range"
  - "headless vs opinionated: the segmented-input state machine + the calendar grid keyboard model + the range state machine + the calendar-system/locale math are heavy HEADLESS logic (React Aria useDatePicker/useCalendarGrid / MUI X, with date-library ADAPTERS — day.js/luxon/date-fns/Temporal). BUILD ON A HEADLESS ENGINE + a date library — too much to hand-roll"
composition:
  inherits: [text-field, popover]
  calendar-is: [grid]   # role=grid (Table/Tag/Tree lineage), NOT CSS display:grid
  composes: [button, icon]
  borders: [select, combobox]   # the native-vs-custom platform decision + the type-to-fill analogue (the segmented input rendered the type-ahead combobox obsolete)
  family: ["time-picker", "datetime-picker", "date-range-picker", "calendar"]   # share the segmented-input + grid + Temporal substrate
  alternative-to: ["plain Text Field + date mask", "native <input type=date>", "(anti-pattern) three Selects day/month/year"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "segmented input (modern, accessible — practice default) vs masked single input (legacy, parsing-fragile) vs native"
    - "native <input type=date> (simple/low-stakes) vs custom (branded/range/complex) — a framework not a winner; the emerging styleable-native path"
    - "single calendar with range-highlight vs dual calendars vs two separate single pickers (for range)"
    - "the date representation: Temporal PlainDate / @internationalized/date (practice) vs JS Date (broken)"
    - "the reverse-selection handling (click before the anchor): reset-to-new-anchor (MUI X / React Aria) vs swap"
  trap:
    - "the masked single input (screen-reader-hostile, locale-baked, parsing-fragile) — use the segmented input"
    - "the JS-Date off-by-one-day timezone bug (a date-only value as a timestamp crossing midnight UTC) — use PlainDate"
    - "hardcoding MDY / Sunday-first / Gregorian (broken for most locales) — Intl/Temporal-derive everything"
    - "the calendar as CSS display:grid instead of role=grid (it's an INTERACTIVE grid)"
    - "the birthdate year-navigation trap (40 month-clicks) — segmented-input-primary + a fast year jump"
    - "a transition on the range hover-preview (lags behind the cursor) — track instantly"
    - "building a regex free-text date parser; hand-rolling the calendar-system/locale math (use a date library)"
  inherited: "Text Field's form-field substrate (label/helper/error/validation/read-only) + Popover's overlay substrate (positioning/dismiss/focus); the role=grid pattern from Table/Tag/Tree; the native-vs-custom framework from Select"
  role-in-family: "a Form composite — the typed-input + calendar-popover date selector, the most i18n-sensitive component; stands on Text Field + Popover, the calendar is a role=grid, composes Button/Icon; anchors the Time/DateTime/Range/Calendar family"
  evolution:
    - "the Masked Era (pre-2020): a single text input + a regex mask + bulky inaccessible popovers; rampant JS-Date timezone bugs"
    - "the ARIA & Headless Era (2020-2025): the segmented role=spinbutton input (React Aria) + the APG role=grid calendar + headless adapters (date-fns/day.js)"
    - "the Temporal & Platform Era (2025-present): JS Date deprecated for Temporal PlainDate (ES2026); the Open UI appearance:base styleable-native direction emerging; the calendar-as-role=grid + the dual-calendar range state machine settled"
  unverified:
    - "external 2026 version numbers (React Aria, MUI X DatePicker/Pro range tier, Ant, Carbon flatpickr)"
    - "the Temporal API ship/baseline status (ES2026; Firefox 139 / Chrome 144) + the Open UI appearance:base customizable-date-input direction (base-select shipping for dropdowns ~mid-2026; native date styling volatile) — verify against current platform state"
    - "MUI X DateRangePicker commercial-licensing (Pro) tier — verify current"
```
