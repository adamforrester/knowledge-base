# Date Picker — field-truth study (Claude pass)

## 1. Framing
A Date Picker lets a user enter a date by **typing it** and/or **picking it from a calendar** — and that duality is the whole component. It is a **Form composite** (one of the briefs closing the Form category) and the catalogue's **most internationalization-sensitive component**: a date's *meaning*, *order*, *first day of week*, and *calendar system* all vary by locale, so a date picker that hardcodes "MM/DD/YYYY, Sunday-first, Gregorian" is broken for most of the world. It stands on two briefed substrates — **Text Field** (the date input is a form field: label/helper/error/`aria-describedby`, validation, read-only ≠ disabled — see text-field) and **Popover** (the calendar is an anchored, light-dismiss overlay — see popover) — and the **calendar grid is a `role=grid`** (the interactive-grid pattern the catalogue has now drawn for Table, Tag's removable group, and Tree — a date grid *is* an interactive grid, not CSS `display:grid`).

Three decisions define it:
- **The input-vs-calendar duality + the segmented-vs-masked input (the headline).** A date picker glues a *text input* (type a known date — the efficiency/a11y default) to a *calendar popover* (browse/pick an unknown date — booking); the best practice is **both**. The input model is the field-truth crux: the modern **segmented input** (separate day/month/year segments, each a `role=spinbutton`, arrow-keys increment, type-to-fill, **locale-ordered** — React Aria's DateField) vs the legacy **masked single input** (`__/__/____`). The segmented input won because it sidesteps freeform-text *parsing*, handles locale order natively, and announces per-segment — the masked input is parsing-fragile and screen-reader-hostile.
- **The native `<input type=date>` vs custom decision** (the platform call, like Select's native-vs-custom): native is free + accessible but unstylable, browser-inconsistent, and can't do range; custom gives full control + range + branding at the cost of owning the entire a11y/keyboard model. A framework, not a winner (§5).
- **The Temporal / i18n depth** — the date *representation* (JS `Date` is broken; Temporal / `@internationalized/date` is the modern foundation) + the locale model (format order, first-day, calendar system) is deeper here than anywhere else (§9).

What it *isn't*: a plain **Text Field** (a typed date with no calendar — see text-field), a **Select** (a date isn't a small fixed option set), or a **Time Picker / DateTime / Date Range** (the *family* it anchors — forward-referenced). Why systems disagree: the input model, native-vs-custom, single-vs-range, and the calendar-system depth.

## 2. Anatomy and parts
- **the date input (the field)** — the **segmented input**: locale-ordered day/month/year segments (each a `role=spinbutton`), with a placeholder showing the *format* (not the label); inherits the Text Field label/helper/error chain (see text-field). (Legacy: a masked single `<input>` — §6.)
- **the calendar trigger** — a **Button** with a calendar **Icon** opening the popover (see button, icon); the field + trigger together (the "combo" form).
- **the calendar popover** — an anchored **Popover** (see popover) containing:
  - **the header** — the month/year label + **navigation** (prev/next month chevrons — Icon Buttons; a month/year jump for fast travel, critical for birthdates — §5).
  - **the day grid** — a `role=grid` of weeks × days: the **selected** date (`aria-selected`), **today** (a marker, not selection), **disabled/unavailable** cells (min/max + blackout), the optional **week-number** column, the weekday header row.
- **the range affordances** — for a range: one calendar with **range highlighting** + hover-preview, or **dual calendars** (start/end side by side); the "which end am I editing" state.
- **the presets** — optional quick ranges ("Today", "Last 7 days", "This month") beside the calendar.
- **the (absence of) freeform parsing** — the segmented input means there's no fragile free-text date string to parse (the key anatomical consequence of the segmented model).

## 3. Properties / API
- **`value` / `defaultValue`** — a date (or a `{ start, end }` range), as a **Temporal `PlainDate`** / `@internationalized/date` value, *not* a JS `Date` (§9/§11).
- **`onChange`** + controlled/uncontrolled.
- **`granularity`** — date / datetime / time (the family: DateField vs DateTimePicker vs TimeField).
- **`selectionMode`** — single / range / multiple (range is the materially-harder one — §5).
- **`minValue` / `maxValue`** + **`isDateUnavailable(date)`** — the bounds + the blackout/unavailable predicate (booked days).
- **the locale model** — `locale` (drives format order + month/day names), `firstDayOfWeek` (Sun/Mon, usually locale-derived), `calendar` (Gregorian/Islamic/Hebrew/Buddhist/Japanese — `Intl`/Temporal).
- **`native` vs custom** — render the native `<input type=date>` (simple) vs the custom segmented+calendar (branded/range — §5).
- **validation** — `isInvalid` / `isRequired`, the error message (inherits Text Field's presentational-by-default model — see text-field); out-of-range and invalid-date errors.
- **the segmented-input behavior** — type-to-fill (auto-advance segments), arrow-increment per segment, the placeholder format.
- **what it withholds** — Date Picker doesn't reinvent the form-field chrome (Text Field) or the overlay (Popover); it adds the calendar + the date model + the locale.

## 4. States and variants
- **The field states:** empty (showing the format placeholder) / filled / **focused-segment** (one segment active in the segmented input) / invalid (the error state) / disabled / read-only.
- **The calendar states:** open / closed; per-cell — **focused** (roving), **selected** (`aria-selected`), **today** (a marker), **disabled** (out of min/max), **unavailable** (blackout), **range-in-progress** (start chosen, hovering the end), **in-range** / **range-endpoint**.
- **Variants:**
  - **selection:** single / range / multiple.
  - **granularity:** date / datetime / time.
  - **input model:** segmented (modern) / masked (legacy) / native.
  - **calendar layout:** single / dual (range) / with-presets / with-week-numbers.
  - **native vs custom.**

## 5. Usage guidance
- **Use a Date Picker for:** entering a date (or range) where a calendar aids selection — bookings, scheduling, filters, deadlines. The composite (segmented input + calendar) is the default.
- **The text-first vs calendar-first call:** for a *known* date the user can type (a birthdate, a deadline they know), **lead with the segmented text input** (typing is faster than clicking through a calendar, and it's the a11y-efficient path) — the calendar is the assist. For an *unknown/browsed* date (pick an available appointment slot), **lead with the calendar**. Ship both; bias the affordance to the use case.
- **The year-navigation problem (the birthdate trap):** a calendar defaulting to the current month is hostile for a birthdate 40 years ago (40 month-clicks). For far-from-today dates, the **segmented input is the right primary** (type "1985"), and the calendar needs a **fast year/month jump** (a year dropdown/grid), not just month chevrons.
- **Date Picker vs the alternatives:**
  - **vs a plain Text Field** — if there's no benefit to a calendar (a pure typed date), a Text Field with a date mask *can* suffice, but the segmented Date Picker is more accessible and locale-correct.
  - **vs native `<input type=date>`** — native for *simple, low-stakes, single-date* cases (a quick form, an MVP) where free + accessible beats branded; **custom** for branded UI, **range**, complex min/max/unavailable, or consistent cross-browser rendering. Native can't do range and is unstylable — that's the decision boundary.
  - **vs a Select** — a date isn't a small fixed set; don't build three Selects (day/month/year) — that's the segmented input's job, done worse.
- **Single vs range:** a single date → one calendar; a **range** → a deliberate choice (one calendar with range highlight for short ranges; dual calendars for longer/cross-month; presets for common ranges). Two separate single pickers ("from" + "to") is the fallback when a true range UI is overkill — but it loses the range-highlight affordance and the cross-field validation.

## 6. Accessibility
Date Picker is one of the catalogue's hardest a11y components — it has *two* interaction models (the input and the grid) and the deepest locale surface.

- **The segmented input vs the masked-input failure (the input crux).** The modern accessible input is **segmented**: each component (day/month/year) is a separate **`role=spinbutton`** with its own `aria-label` ("day", "month", "year"), `aria-valuenow`/`min`/`max`/`text`; arrow keys increment/decrement, typing fills and auto-advances, and the segments render in **locale order**. This announces cleanly ("month, 6") and sidesteps the freeform-text parsing nightmare. The **masked single input** (`__/__/____`) is a screen-reader-hostile anti-pattern — AT can't parse the partial mask, the cursor/placeholder behavior is erratic, and locale order is baked in. The practice default is **segmented** (React Aria's DateField is the reference).
- **The calendar as the APG grid pattern (the keyboard crux).** The calendar is `role="grid"` (with `role="row"`/`role="gridcell"` and column headers for weekdays); **one tab stop** into the grid, then:
  - **Left/Right** — previous/next day; **Up/Down** — previous/next week; **PageUp/PageDown** — previous/next month; **Shift+PageUp/PageDown** — previous/next year; **Home/End** — first/last day of the week.
  - the focused date has roving `tabindex`; the **selected** date carries `aria-selected="true"`; **today** is marked (visually + an accessible hint, not via selection); **disabled/unavailable** dates are `aria-disabled` and not focusable-for-selection.
  - **focus-on-open** — opening the calendar moves focus to the **selected date** (or today if none); closing returns focus to the trigger/field.
- **The popover/dialog contract** — the calendar is in a Popover/dialog (`aria-label`/`labelledby` naming it); the field's value updates announce; the month/year nav buttons have accessible names ("Previous month").
- **Validation announcement** — invalid/out-of-range errors via the Text Field `aria-describedby`/`aria-invalid` chain (see text-field); the min/max and unavailable constraints should be discoverable (announce why a date is unavailable where possible).
- **The native baseline** — `<input type=date>` is accessible out of the box (the OS picker + the field) — its a11y advantage, at the cost of styling/range.
- **WCAG SCs:** **1.3.1** (info & relationships — the grid + the segmented field structure), **2.1.1** (keyboard — the full grid model + the segments, no mouse needed), **4.1.2** (name/role/value — the spinbutton segments, `aria-selected`, the nav), **2.4.3** (focus order — focus-on-open, return-on-close), **1.4.13** (the calendar popover dismiss/hover contract — see tooltip/popover). One of the deepest a11y briefs in Form.

## 7. Content guidelines
- **The format hint** — show the expected format as a **placeholder/segment hint** ("MM/DD/YYYY" rendered by the segments), *locale-correct*, and **never as the label** (placeholder-is-not-a-label — see text-field). The segmented input shows the format implicitly via its segments.
- **The label** — a clear field label ("Start date", "Date of birth"); the helper text for constraints ("Must be in the future").
- **The error copy** — specific: "Enter a date after 1 January 2020" / "This date is unavailable", not "Invalid date".
- **The month/weekday labels** — locale-correct full + abbreviated names (via `Intl` — §9); the weekday header row uses short forms with an accessible full name.
- **The range labels** — "Start" / "End" (or the dual-calendar headers); the selected-range summary ("Jun 1 – Jun 7, 2026").

## 8. Motion and transition
- **The calendar open/close** — inherits the Popover enter/exit animation (the `@starting-style`/top-layer transition — see popover); a brief scale/fade from the trigger.
- **The month transition** — navigating months can slide/cross-fade the grid (directional: forward slides left in LTR); keep it fast and skip it for keyboard rapid-nav.
- **The range hover-preview** — the in-progress range highlights on hover between the chosen start and the hovered end (a pointer affordance; the keyboard equivalent is the focus moving through the range).
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops the month-slide and the open animation to instant; the date is the information, not the motion.

## 9. Internationalization
This is **the deepest i18n in the catalogue** — a date picker is i18n-critical, not i18n-optional.
- **The format order** — MDY (US) / DMY (most of Europe/world) / YMD (ISO, East Asia) — driven by **`Intl.DateTimeFormat`** per locale, **never hardcoded**; the segmented input renders its segments in the locale order.
- **The first day of the week** — Sunday (US/JP) vs Monday (most of Europe, ISO) vs Saturday (parts of the Middle East) — locale-derived, not assumed.
- **The calendar system** — Gregorian is *not* universal: **Islamic (Hijri), Hebrew, Buddhist, Japanese (era), Persian** calendars are first-class needs; the modern foundation (`Intl`/Temporal/`@internationalized/date`) supports non-Gregorian calendars, and the picker must render the right one per locale/preference.
- **RTL** — the calendar grid **mirrors** (the week runs right-to-left), the month-nav chevrons mirror, via logical properties; the day-of-week columns reverse.
- **Month/day names** — localized full + abbreviated (via `Intl`).
- **The representation** — use **Temporal `PlainDate`** (a date with no time/timezone) for date-only pickers — *not* a JS `Date` (which is a timestamp with a timezone, the source of the classic "off by one day" bug when a date-only value crosses midnight UTC); use `ZonedDateTime` only when a timezone genuinely matters (datetime). The timezone trap is the most common date bug.

## 10. Naming
- **The field set:** **`DatePicker`** (the composite: field + calendar — MUI X, Ant, Carbon, Polaris, Fluent, React Aria); **`DateField`** (the segmented input *alone* — React Aria/Spectrum, MUI X); **`Calendar`** (the grid *alone* — React Aria, MUI's `DateCalendar`); **`DateRangePicker`** / **`RangeCalendar`** (the range — React Aria, MUI X); **`DatePicker` + `RangePicker`** (Ant); the APG term **"Date Picker Dialog"**.
- **The practice's default — `DatePicker`** for the composite (the field + the calendar popover), built from **`DateField`** (the segmented input, usable standalone) + **`Calendar`** (the grid, usable standalone) + **Popover**. The range is **`DateRangePicker`** (composite) / **`RangeCalendar`** (grid). The **family** — `TimeField`, `DateTimePicker` (date + time), `Calendar`/`RangeCalendar` — shares the segmented-input + grid substrate.
- **Aliases to map:** DateField, Calendar, DateRangePicker, RangeCalendar, DateInput, DatePickerDialog, TimeField, DateTimePicker.

## 11. Implementation notes
- **The segmented input over the masked input** — render locale-ordered segments (each `role=spinbutton` with min/max/value), type-to-fill with auto-advance, arrow-increment, and a non-parsing value model (each segment holds a number, assembled into the `PlainDate`) — this is why the segmented input avoids the freeform-text-parsing nightmare. React Aria's `useDateField`/`useDateSegment` is the reference; don't build a regex date parser.
- **The calendar `role=grid` + the full keyboard model** — `role=grid` of weeks/days, roving tabindex over the focused date, the arrow/Page/Home-End model (§6), focus-on-open to the selected/today date, return focus on close. The grid keyboard model is the bulk of the work (shared lineage with Table/Tree's grid).
- **The native-vs-custom toggle (+ the styleable-native direction)** — offer a `native` mode (`<input type=date>` — free a11y, no range, unstylable) and the custom mode (segmented + calendar). Track the **emerging CSS customizable date input** (the Open UI direction toward a styleable native picker, akin to `appearance: base-select` for Select — see select); date this, it's volatile and would collapse the native-vs-custom trade if it lands.
- **The range state machine** — track `{ anchor, focus }`; first click sets the anchor, second sets the end (normalize so start ≤ end), hover between them previews; handle the "click a third time restarts" and the "which end am I editing" (clicking inside an existing range). Dual calendars share one state. The hardest UX logic in the component.
- **The Temporal / `@internationalized/date` representation** — model values as **`PlainDate`** (date-only), `ZonedDateTime` (datetime with timezone), `PlainTime` (time) — *never* a JS `Date` (mutable, timezone-coupled, no date-only type). Format/parse via `Intl.DateTimeFormat`. This avoids the off-by-one-day timezone bug and gives non-Gregorian calendar support for free. (React Aria already ships `@internationalized/date`; Temporal is the platform's eventual replacement.)
- **min/max + unavailable** — `minValue`/`maxValue` clamp the navigable/selectable range; `isDateUnavailable(date)` marks blackout days `aria-disabled`; the segmented input also rejects out-of-range.
- **Headless vs opinionated** — the segmented-input state machine, the calendar grid keyboard model, the range state machine, and the calendar-system/locale math are heavy headless logic (React Aria / MUI X own this, with date-library *adapters* — day.js/luxon/date-fns/Temporal). **Build on a headless engine + a date library** — the i18n + Temporal + grid keyboard model is far too much to hand-roll.

## 12. Related and alternative components
- **Stands on:** **Text Field** (the date input is a form field — label/helper/error/`aria-describedby` + validation + read-only≠disabled — see text-field) and **Popover** (the calendar is an anchored light-dismiss overlay — see popover).
- **The calendar is a `role=grid`** — the interactive-grid pattern shared with **Table** / **Tag**'s removable group / **Tree** (a date grid is an interactive grid, not CSS `display:grid` — see table, tag, tree, grid).
- **Composes:** **Button** (the trigger + month/year nav) + **Icon** (the calendar icon + nav chevrons — see button, icon).
- **Borders:** **Select** + **Combobox** (the native-vs-custom platform decision, like Select; the type-to-fill analogue — see select, combobox).
- **The family:** **Time Picker** / **DateTime Picker** (date + time) / **Date Range Picker** / **Calendar** (the standalone grid) — all share the segmented-input + grid + Temporal substrate.
- **Alternative to:** a plain **Text Field** with a date mask (no calendar), the **native `<input type=date>`** (simple/low-stakes), and (anti-pattern) three Selects for day/month/year.

(A Form composite — the typed-input + calendar-popover date selector, and the catalogue's most i18n-sensitive component. It stands on Text Field (the field) + Popover (the calendar overlay), the calendar is a role=grid (the Table/Tag/Tree lineage), and it composes Button/Icon. See text-field for the field substrate, popover for the overlay, table/tree for the grid keyboard lineage, select for the native-vs-custom decision, 13-internationalization-and-rtl for the locale/calendar-system depth. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The masked single input → the segmented input.** The old `__/__/____` masked input (parsing-fragile, screen-reader-hostile, locale-baked) gave way to the **segmented input** (per-segment `role=spinbutton`, locale-ordered, no freeform parsing) — React Aria's DateField is the reference that hardened it as the accessible default.
2. **Native `<input type=date>` → the styling limit → custom → styleable-native.** Native is accessible-and-free but unstylable/inconsistent/no-range; the field built custom segmented+calendar pickers for control — and the **emerging CSS customizable date input** (Open UI) may eventually collapse the native-vs-custom trade (as `appearance: base-select` is doing for Select).
3. **The JS `Date` mess → Temporal / `@internationalized/date`.** JS `Date` (mutable, timezone-coupled, no date-only type — the off-by-one-day bug) gave way to **`@internationalized/date`** (React Aria) and the **Temporal API** (PlainDate/ZonedDateTime, stage-3/shipping ~2025–2026) as the modern, calendar-system-aware foundation.
4. **The calendar-as-`role=grid` settling** — the calendar standardized on the APG grid pattern (the same `role=grid` lineage as Table/Tag/Tree).
5. **Range pickers maturing** — the dual-calendar + range-highlight + the "which end" state machine + presets became the standard range UX.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- Adobe Spectrum / React Aria — `DateField`/`DatePicker`/`DateRangePicker`/`Calendar`/`RangeCalendar` + `@internationalized/date` (the gold-standard segmented-input + grid + i18n reference).
- MUI X — `DatePicker`/`DateRangePicker`/`DateField`/`DateCalendar` (the segmented field + calendar; the date-library adapters; the Pro tier for range).
- Ant Design — `DatePicker` + `RangePicker` (panels, presets).
- IBM Carbon — `DatePicker` (flatpickr-based + the calendar).
- Shopify Polaris — `DatePicker` (the calendar).
- Microsoft Fluent — `DatePicker` / `Calendar`.
- Atlassian — the date picker.
- flatpickr / react-day-picker — the headless/standalone calendar libraries.
- native `<input type=date>` + the **Open UI customizable date-input** direction.
- the **Temporal API** (PlainDate/ZonedDateTime) + `@internationalized/date`.
- WAI-ARIA APG — the **Date Picker Dialog** pattern + the grid keyboard model; `role=spinbutton` segments.
- WCAG 2.2 — 1.3.1, 2.1.1, 4.1.2, 2.4.3, 1.4.13.

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
    - "the date input (the field): a SEGMENTED input — locale-ordered day/month/year segments, each a role=spinbutton, a format placeholder (not the label); inherits the Text Field label/helper/error chain. (Legacy: a masked single input)"
    - "the calendar trigger: a Button + calendar Icon opening the popover"
    - "the calendar popover (a Popover): header (month/year label + prev/next chevrons + a month/year jump for fast travel) + the DAY GRID (role=grid of weeks x days: selected/today/disabled/unavailable cells, optional week-number column, weekday header row)"
    - "the range affordances: one calendar with range-highlight + hover-preview, or dual calendars (start/end); the 'which end' state"
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
    - {name: granularity, type: "'date'|'datetime'|'time'", default: date, required: false, description: "the family: DateField / DateTimePicker / TimeField"}
    - {name: selectionMode, type: "'single'|'range'|'multiple'", default: single, required: false, description: "range is the materially-harder one (the 'which end' state machine)"}
    - {name: "minValue/maxValue", type: PlainDate, default: ~, required: false}
    - {name: isDateUnavailable, type: "(date)=>boolean", default: ~, required: false, description: "blackout/unavailable predicate (booked days) -> aria-disabled"}
    - {name: locale, type: string, default: "system", required: false, description: "drives the format ORDER + month/day names"}
    - {name: firstDayOfWeek, type: "0-6", default: "locale-derived", required: false, description: "Sun/Mon/Sat by locale, not assumed"}
    - {name: calendar, type: "'gregorian'|'islamic'|'hebrew'|'buddhist'|'japanese'|...", default: "locale-derived", required: false, description: "Gregorian is NOT universal (Intl/Temporal)"}
    - {name: native, type: boolean, default: false, required: false, description: "render <input type=date> (simple) vs the custom segmented+calendar (branded/range)"}
    - {name: "isInvalid/isRequired + error", type: "boolean/string", default: ~, required: false, description: "inherits Text Field's presentational-by-default validation; out-of-range + invalid-date"}
  withholds: "doesn't reinvent the form-field chrome (Text Field) or the overlay (Popover); adds the calendar + the date model + the locale"
states:
  field: [empty, filled, focused-segment, invalid, disabled, read-only]
  calendar: [open, closed]
  cell: [focused, selected, today, disabled, unavailable, range-in-progress, in-range, range-endpoint]
variants:
  selection: [single, range, multiple]
  granularity: [date, datetime, time]
  input-model: [segmented, masked, native]
  calendar-layout: [single, dual, with-presets, with-week-numbers]
  delivery: [native, custom]
accessibility:
  wcag-criteria: ["1.3.1", "2.1.1", "4.1.2", "2.4.3", "1.4.13"]
  inherits: [text-field (the validation/aria-describedby chain), popover (the overlay focus/dismiss)]
  segmented-vs-masked: "the modern accessible input is SEGMENTED — each day/month/year segment a role=spinbutton (aria-label day/month/year + valuenow/min/max/text), arrow-increment, type-to-fill+auto-advance, LOCALE-ORDERED; announces cleanly + sidesteps freeform-text parsing. The MASKED single input (__/__/____) is screen-reader-hostile (AT can't parse the partial mask, locale baked in) — the anti-pattern. Practice default: segmented (React Aria DateField)"
  calendar-grid: "role=grid (+ role=row/gridcell + weekday column headers); ONE tab stop; Left/Right=day, Up/Down=week, PageUp/Down=month, Shift+PageUp/Down=year, Home/End=week; the focused date roving tabindex; selected = aria-selected; today MARKED (not via selection); disabled/unavailable = aria-disabled. FOCUS-ON-OPEN to the selected date (or today); return to the trigger on close"
  popover-contract: "the calendar in a Popover/dialog named via aria-label; the month/year nav buttons named ('Previous month'); the value update announces"
  validation: "invalid/out-of-range via the Text Field aria-describedby/aria-invalid chain; announce WHY a date is unavailable where possible"
  native-baseline: "<input type=date> is accessible out of the box (OS picker + field) — its advantage, at the cost of styling/range"
content:
  format-hint: "show the expected format as a locale-correct segment hint (MM/DD/YYYY), NEVER as the label (placeholder-is-not-a-label)"
  label: "a clear field label ('Date of birth'); helper text for constraints ('Must be in the future')"
  error-copy: "specific ('Enter a date after 1 January 2020' / 'This date is unavailable'), not 'Invalid date'"
  names: "locale-correct month/weekday full + abbreviated (via Intl); the weekday header short form + an accessible full name"
  range-labels: "Start / End (or dual-calendar headers); the selected-range summary ('Jun 1 - Jun 7, 2026')"
motion:
  calendar-open: "inherits the Popover enter/exit (@starting-style/top-layer); a brief scale/fade from the trigger"
  month-transition: "navigating months slides/cross-fades the grid (directional); fast, skipped for keyboard rapid-nav"
  range-hover-preview: "the in-progress range highlights on hover between start and the hovered end (pointer); keyboard equivalent = focus moving through the range"
  reduce-motion: "drop the month-slide + open animation to instant; the date is the information, not the motion"
i18n:
  the-deepest-i18n: "a date picker is i18n-CRITICAL, not optional"
  format-order: "MDY (US) / DMY (most of the world) / YMD (ISO/East Asia) via Intl.DateTimeFormat per locale, NEVER hardcoded; the segmented input renders segments in locale order"
  first-day-of-week: "Sun (US/JP) / Mon (Europe/ISO) / Sat (parts of the Middle East) — locale-derived, not assumed"
  calendar-system: "Gregorian is NOT universal — Islamic(Hijri)/Hebrew/Buddhist/Japanese(era)/Persian are first-class (Intl/Temporal/@internationalized/date support non-Gregorian)"
  rtl: "the calendar grid MIRRORS (week runs right-to-left), the nav chevrons mirror, the day-of-week columns reverse (logical properties)"
  representation: "use Temporal PlainDate (date-only, no timezone) — NOT a JS Date (a timestamp with a timezone -> the classic off-by-one-day bug when a date-only value crosses midnight UTC); ZonedDateTime only when a timezone genuinely matters. The timezone trap is the most common date bug"
implementation:
  - "the SEGMENTED input over the masked: locale-ordered segments (each role=spinbutton with min/max/value), type-to-fill+auto-advance, arrow-increment, a non-parsing value model (each segment a number, assembled into the PlainDate). React Aria useDateField/useDateSegment is the reference — DON'T build a regex date parser"
  - "the calendar role=grid + the full keyboard model (arrow/Page/Home-End) + focus-on-open to the selected/today date + return-on-close; the grid keyboard model is the bulk of the work (shared lineage with Table/Tree)"
  - "the native-vs-custom toggle (+ the styleable-native direction): a native mode (<input type=date>, free a11y, no range, unstylable) + the custom mode (segmented+calendar). Track the emerging CSS customizable date input (Open UI, akin to appearance:base-select for Select) — VOLATILE, would collapse the native-vs-custom trade"
  - "the range state machine: track {anchor, focus}; first click sets the anchor, second the end (normalize start<=end), hover previews between; handle 'third click restarts' + 'which end' (clicking inside a range); dual calendars share one state. The hardest UX logic"
  - "the Temporal/@internationalized/date representation: PlainDate (date-only) / ZonedDateTime (datetime+tz) / PlainTime — NEVER a JS Date (mutable, tz-coupled, no date-only type). Format/parse via Intl.DateTimeFormat -> avoids off-by-one + gives non-Gregorian for free"
  - "min/max + unavailable: minValue/maxValue clamp the navigable/selectable range; isDateUnavailable marks blackout days aria-disabled; the segmented input also rejects out-of-range"
  - "headless vs opinionated: the segmented-input state machine + the calendar grid keyboard model + the range state machine + the calendar-system/locale math are heavy headless logic (React Aria / MUI X, with date-library ADAPTERS — day.js/luxon/date-fns/Temporal). BUILD ON A HEADLESS ENGINE + a date library — too much to hand-roll"
composition:
  inherits: [text-field, popover]
  calendar-is: [grid]   # role=grid (Table/Tag/Tree lineage), NOT CSS display:grid
  composes: [button, icon]
  borders: [select, combobox]   # the native-vs-custom platform decision + the type-to-fill analogue
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
  trap:
    - "the masked single input (screen-reader-hostile, locale-baked, parsing-fragile) — use the segmented input"
    - "the JS-Date off-by-one-day timezone bug (a date-only value as a timestamp crossing midnight UTC) — use PlainDate"
    - "hardcoding MDY / Sunday-first / Gregorian (broken for most locales) — Intl/Temporal-derive everything"
    - "the calendar as CSS display:grid instead of role=grid (it's an INTERACTIVE grid)"
    - "the birthdate year-navigation trap (40 month-clicks) — segmented-input-primary + a fast year jump"
    - "building a regex free-text date parser; hand-rolling the calendar-system/locale math (use a date library)"
  inherited: "Text Field's form-field substrate (label/helper/error/validation/read-only) + Popover's overlay substrate (positioning/dismiss/focus); the role=grid pattern from Table/Tag/Tree; the native-vs-custom framework from Select"
  role-in-family: "a Form composite — the typed-input + calendar-popover date selector, the most i18n-sensitive component; stands on Text Field + Popover, the calendar is a role=grid, composes Button/Icon; anchors the Time/DateTime/Range/Calendar family"
  evolution:
    - "the masked single input -> the segmented input (React Aria) for a11y + locale"
    - "native <input type=date> -> the styling limit -> custom -> the emerging CSS customizable date input"
    - "the JS Date mess -> Temporal / @internationalized/date (PlainDate, non-Gregorian)"
    - "the calendar-as-role=grid settling"
    - "range pickers maturing (dual-calendar + the 'which end' state machine + presets)"
  unverified:
    - "external 2026 version numbers (React Aria, MUI X DatePicker/Pro range tier, Ant, Carbon flatpickr)"
    - "the Temporal API ship/baseline status (~2025-2026 stage-3/shipping) + the Open UI customizable-date-input direction — verify against current platform state"
    - "MUI X DateRangePicker commercial-licensing tier — verify current"
```
