You are researching the Date Picker component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of how
the leading design systems handle this component — what they converge on,
where they diverge, and what the practice's opinionated default should be
when starting from scratch.

This is not an introductory guide. Assume the reader knows what a date
picker is, knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the choices field leaders disagree on,
the accessibility decisions still contested, the implementation traps that
recur across codebases.

Date Picker is A FORM COMPOSITE — one of the components closing the Form
category, and it STANDS ON two briefed substrates while being the catalogue's
most internationalization-sensitive component. DON'T re-derive the substrates;
reference them and concentrate on the Date-Picker-specific substance:
- IT STANDS ON TEXT FIELD (components/text-field.md): the date INPUT is a
  form field — it inherits the label / helper / error / aria-describedby
  chain, the validation model (presentational-by-default, the error state),
  and read-only ≠ disabled. Don't re-derive the form-field substrate.
- IT STANDS ON POPOVER (components/popover.md): the CALENDAR is an anchored
  overlay — it inherits the positioning + light-dismiss + focus substrate
  Popover formalised. Don't re-derive the overlay.
- THE CALENDAR GRID IS A role=grid (components/table.md, grid.md, tag.md,
  tree.md): a date grid is an interactive grid — the same role=grid pattern
  the catalogue has drawn for Table / Tag's removable group / Tree (NOT the
  CSS display:grid layout). Resolve the calendar as the APG grid keyboard
  model.
- IT BORDERS Select + Combobox (the native-vs-custom platform decision, like
  Select; the type-to-fill analogue — components/select.md, combobox.md), and
  the Time Picker / DateTime / Date Range FAMILY (forward-reference).
- IT COMPOSES Button (the trigger + the month/year nav) and Icon (the
  calendar icon + the nav chevrons).

THE DEFINING DATE-PICKER-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE INPUT-vs-CALENDAR DUALITY + THE SEGMENTED-INPUT-vs-MASKED-INPUT A11Y
  PATTERN (the headline): a date picker glues a TEXT INPUT (typed date) to a
  CALENDAR popover (visual grid). Resolve: text-input-first (type a known
  date — the efficiency/a11y default) vs calendar-first (browse/pick an
  unknown date — booking) — and the best-practice BOTH. And the input model:
  the modern SEGMENTED INPUT (separate day/month/year segments, each a
  role=spinbutton, arrow-keys increment, type-to-fill, locale-ordered —
  React Aria DateField) vs the legacy MASKED single input (an input mask
  `__/__/____` — parsing-fragile, screen-reader-hostile). Resolve why the
  segmented input is the modern accessible answer (it sidesteps freeform-text
  parsing + handles locale order + announces per-segment).
- THE CALENDAR AS THE APG GRID PATTERN (the keyboard crux): the calendar is a
  role=grid of days — arrow-key nav (Left/Right days, Up/Down weeks,
  PageUp/Down months, Shift+PageUp/Down years, Home/End week), aria-selected
  on the chosen date, the roving focus, the month/year navigation header, the
  today indicator, the disabled/unavailable dates (min/max + blackout dates),
  the optional week-number column, and the focus-management on open
  (focus the selected date or today). Resolve the full grid keyboard contract.
- THE NATIVE <input type=date> vs CUSTOM DECISION (the platform call, like
  Select's native-vs-custom): native (free, accessible, but unstylable,
  browser-inconsistent, no range, limited min/max UX) vs CUSTOM (full
  control + range + branded, but you own the entire a11y/keyboard model).
  Resolve as a framework not a winner — native for simple/low-stakes; custom
  (React Aria-style segmented + calendar) for branded/range/complex — and DATE
  the emerging CSS customizable-date-input / styleable native path (volatile).
- SINGLE vs RANGE (the range crux): single date vs a date RANGE (start/end —
  one calendar with range highlighting + hover-preview, or dual calendars;
  the "which end am I editing" state machine; the range-selection model;
  presets like "Last 7 days"). Resolve why range is materially harder + the
  range UX model.
- THE i18n + TEMPORAL DEPTH (the deepest i18n in the catalogue): the date-
  format ORDER (MDY/DMY/YMD via Intl, never hardcoded), the FIRST-DAY-OF-WEEK
  (Sun vs Mon by locale), the CALENDAR SYSTEM (Gregorian/Islamic/Hebrew/
  Buddhist/Japanese — Intl/Temporal), the month/day NAMES, RTL (the calendar
  grid mirrors), and the parsing/formatting via Intl.DateTimeFormat. AND the
  TEMPORAL API + the JS-Date-is-broken reality (Date is mutable/timezone-
  hostile/no-date-only-type; Temporal PlainDate/ZonedDateTime — stage-3/
  shipping ~2025-2026 — is the modern foundation; React Aria's
  @internationalized/date the current standard). Resolve the practice's
  date-representation + locale + calendar-system model.
- VALIDATION + MIN/MAX + UNAVAILABLE DATES: min/max bounds, blackout/
  unavailable dates (booked days), the invalid-date / out-of-range
  validation (inherits Text Field's error model), the time-picker / datetime
  sibling boundary.

Field-leader systems to survey (web): Adobe Spectrum / React Aria (DateField/
DatePicker/DateRangePicker/Calendar/RangeCalendar + @internationalized/date —
the gold-standard segmented-input + grid + i18n reference), MUI X (DatePicker/
DateRangePicker/DateField — the segmented field + calendar, the date-library
adapters, the Pro tier for range), Ant Design (DatePicker + RangePicker —
panels, presets), IBM Carbon (DatePicker — flatpickr-based + the calendar),
Shopify Polaris (DatePicker — the calendar), Microsoft Fluent (DatePicker /
Calendar), Atlassian (the date picker), flatpickr / react-day-picker (the
headless/standalone calendar libs), native <input type=date> + the Open UI
customizable date-input direction, the Temporal API + @internationalized/date.
WAI-ARIA APG (the Date Picker Dialog pattern + the grid keyboard model;
role=spinbutton segments; the native input contract). Cite each with a
version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits for the Text Field form-field substrate +
the Popover overlay substrate; the role=grid calendar; composes Button/Icon;
note the Select/Combobox native-vs-custom border + the Time/DateTime/Range
family; flag unverified/volatile platform claims under notes.unverified).

1. Framing — what it is (the typed-input + calendar-popover date selector;
   the most i18n-sensitive Form composite) and what it isn't (a plain Text
   Field; a Select; a Time Picker — the family); the input-vs-calendar
   duality + the segmented-vs-masked input + the native-vs-custom decision up
   front; why systems disagree.
2. Anatomy and parts — the segmented/masked text input (+ the field label/
   helper/error), the calendar trigger (Button + Icon), the calendar popover
   (the month/year header + nav, the day grid role=grid, the today/selected/
   disabled cells, the week-number column), the range (dual calendar / range
   highlight), the presets.
3. Properties / API — value (date/range), the segmented input, min/max,
   unavailable/blackout dates, the calendar system + locale + first-day-of-
   week, single/range/multiple, granularity (date/datetime/time), the native-
   vs-custom toggle, validation, controlled/uncontrolled.
4. States and variants — the field (empty/filled/focused-segment/invalid/
   disabled/read-only); the calendar (open/closed, the focused/selected/
   today/disabled/unavailable/range-in-progress cells); single vs range vs
   multiple; date vs datetime vs time; native vs custom; with-presets.
5. Usage guidance — Date Picker (segmented input + calendar) vs a plain Text
   Field (a typed date with no calendar) vs native <input type=date> (simple/
   low-stakes) vs a Select of dates (rare); when text-first vs calendar-first;
   when range vs two single pickers; the recent-date / birthdate / booking
   distinctions (the year-navigation problem for birthdates).
6. Accessibility — the segmented input (role=spinbutton segments + per-segment
   announcement + the locale order) vs the masked-input a11y failure; the
   calendar APG grid keyboard model (arrow/Page/Home-End + aria-selected +
   the grid roles + focus-on-open); the trigger + popover focus contract; the
   announce-the-selected-date + the min/max/unavailable announcement; the
   native-input a11y baseline; WCAG SCs (1.3.1, 2.1.1, 4.1.2, 2.4.3, 1.4.13).
7. Content guidelines — the format hint/placeholder (show the expected format,
   never as the label), the helper text, the error copy (invalid/out-of-range),
   the locale-correct format, the month/weekday labels, the range labels.
8. Motion and transition — the calendar open/close (the Popover animation),
   the month-slide transition, the range-hover preview, reduce-motion.
9. Internationalization — THE deepest i18n: the format order (Intl, never
   hardcoded MDY), the first-day-of-week, the calendar system (Gregorian/
   Islamic/Hebrew/Buddhist/Japanese), month/day names, RTL (the grid mirrors,
   the nav chevrons mirror), the parsing/formatting (Intl.DateTimeFormat),
   the Temporal/@internationalized/date foundation, the timezone concern.
10. Naming — DatePicker / DateField / Calendar / DateRangePicker / DateInput /
    DatePickerDialog; the field-vs-calendar-vs-composite naming; the practice's
    default; aliases; the time/datetime/range family naming.
11. Implementation notes — the segmented input (role=spinbutton per segment +
    the locale-ordered render + type-to-fill + arrow-increment) over the masked
    input; the calendar role=grid + the full keyboard model + focus-on-open;
    the native-vs-custom toggle + the styleable-native direction; the range
    state machine ("which end" + hover preview + dual calendar); the
    Temporal/@internationalized/date representation (PlainDate, no JS Date) +
    the Intl formatting/parsing; min/max + unavailable-date logic; the
    timezone trap; headless vs opinionated (React Aria / MUI X adapters).
12. Related and alternative components — typed relationships (STANDS ON Text
    Field [the field] + Popover [the calendar overlay]; the calendar is a
    role=grid [Table/Tag/Tree lineage]; COMPOSES Button/Icon; the Select/
    Combobox native-vs-custom border; the Time Picker / DateTime / Date Range /
    Calendar family; the native <input type=date> alternative).
13. Field POV evolution — the masked single input -> the segmented input
    (React Aria) for a11y + locale; native <input type=date> -> the styling
    limit -> custom -> the emerging CSS customizable date input; the JS-Date
    mess -> Temporal / @internationalized/date; the calendar-as-role=grid
    settling; range pickers maturing (dual-calendar + the range state machine).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a date picker is — explain the
input-vs-calendar duality + the segmented-input-vs-masked-input a11y pattern
(why segmented won), the calendar-as-role=grid + the full APG grid keyboard
model, the native-<input type=date>-vs-custom platform decision (+ the emerging
styleable-native path), single-vs-range (the "which end" state machine), the
Temporal/@internationalized/date + the deep i18n (format order / first-day /
calendar system / RTL), and the validation/min-max/unavailable-dates that
field leaders still diverge on.
