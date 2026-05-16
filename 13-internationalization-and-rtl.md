# 13 — Internationalization, Localization, and RTL

> Internationalization is a design system architecture concern, not a content concern. A DS that bakes i18n in from the first component absorbs the cost as a small tax on every component author. A DS that retrofits i18n later pays a six-to-twelve-month project tax. The choice is made implicitly, every day, by every component author who reaches for `margin-left`. Most published DS material is silent on this; this file is the corrective.

---

## Why this is a DS architecture concern

Most design systems are built on an unstated assumption: English, Latin script, left-to-right reading. That assumption rarely surfaces in the moment of authoring — it just shows up in fixed-width buttons, hardcoded `padding-left`, type scales tuned for Latin x-heights, and color tokens named after Western connotations. Each of those is cheap to write LTR-only and expensive to retrofit. **The DS is the only place the cost can be amortized.** If every consuming product solves i18n independently, every product solves it differently and most solve it badly.

### The four DS layers, each affected

- **Tokens.** Spacing, line-height, and density may need locale-aware values (CJK can sustain higher density; Arabic and Devanagari need more line-height). Color tokens must be semantic, never named after Western connotations. Type tokens must accommodate multi-script font-stack fallback chains, not assume a single brand font covers every locale.
- **Components.** Containers must grow with content — never fixed width. Layouts must use logical properties so they mirror automatically. Icons must declare whether they're directional and ship RTL variants when they are. Date, number, and currency components must be slot-shaped, accepting locale-formatted output rather than baking format logic into the component.
- **Layout patterns.** Patterns that imply temporal direction (steppers, breadcrumbs, progress bars) must mirror in RTL. Patterns that don't (media controls, charts that aren't time-axis) must not. The DS must specify which is which — leaving it to consumers produces inconsistent application.
- **Documentation.** Every component's docs must declare RTL behavior and text-expansion behavior. Default-LTR-only documentation is a tell that the DS isn't actually global-ready.

### The retrofit tax

Retrofitting i18n into a system that wasn't built for it is asymmetrically expensive. The work falls in four buckets (sometimes itemized in practitioner writing as six engineering stages — discovery, documentation, triage, fixing, review, regression):

1. **CSS refactor.** Every `margin-left`, `padding-right`, `text-align: left`, `border-radius` corner reference becomes a logical-property migration. Mechanical but high-volume.
2. **String externalization.** Every hardcoded string in JSX/templates extracted to translation keys. Tooling helps; missed strings show up at QA.
3. **Layout audit.** Every fixed-width container, every component that assumed text length within a known range. The most invisible category until pseudo-localization surfaces it.
4. **Component contract changes.** Components that baked in formatting (a date picker that produces `MM/DD/YYYY`) need rebuilding around locale-agnostic shape with formatting injected.

A team that built i18n into the system from day one writes the same code at near-zero incremental cost. A team retrofitting it is doing the same work plus discovery, regression testing, and coordination across every consuming product. **The "build it in" cost is a small tax on every component; the "retrofit" cost is a multi-quarter project, and that's optimistic.** This is the strongest argument the practice has for raising i18n in Discovery (see 01-discovery-and-strategy) even on engagements where the client hasn't named it as a requirement, because it changes the architecture irreversibly.

### The spectrum of support

A useful staged framing — each level demanding more from the DS, and the level shipped should be deliberate, not accidental:

- **Translation-ready.** Strings externalized. Components grow with content. Logical properties used throughout. RTL works. This is the floor — the cost of a single component author thinking globally as they write.
- **Multi-script typography.** Type stack includes script-appropriate fallbacks. Line-height and spacing tokens are locale-aware. Component metrics (input height, button padding) accommodate scripts with taller glyphs.
- **Locale-aware components.** Date pickers, address forms, number/currency displays, phone fields — components whose internal logic varies by locale — designed and documented around locale-injection patterns rather than fixed conventions.
- **Cultural localization.** Color semantics, iconography, imagery, tone considered per market. Beyond what most DS teams ship; usually owned by content/brand teams in collaboration with the DS.

An alternative four-level maturity ladder — Locally Targeted → Globally Aware → Fully Localized → Globally Optimized — appears in some practitioner writing and maps roughly onto the same stages with more business-flavored vocabulary. The stage names above are more useful for engineering scoping; the maturity-ladder vocabulary may be more useful in pitch decks or stakeholder briefs.

**Most of our engagements should target the first two stages reliably and provide patterns for the third.** Cultural localization is rarely a DS deliverable.

### Externalization and pseudo-localization

The most basic architectural requirement for i18n is the **complete externalization of all user-facing strings.** Translation keys live in the codebase; values live in structured locale files (typically JSON, sometimes XLIFF for translation-tool round-trip). Translators work without touching source code; engineers ship features with English as just-another-locale.

**Avoid string concatenation.** Building sentences by joining variables (`"You have " + count + " new messages"`) breaks in languages with different word orders, grammatical genders, or pluralization rules. The consensus is **ICU MessageFormat**, which keeps the entire sentence structure inside a single translation key and lets translators handle locale-specific grammar:

```
{count, plural,
  =0 {You have no new messages}
  one {You have # new message}
  other {You have # new messages}}
```

**Pseudo-localization is the cheapest layout-validation tool we have.** It replaces source strings with elongated, accented, bracketed text — `[Ĥéééļļļööö Ŵööörļļļḑ]` — that simultaneously tests for hardcoded strings (anything un-bracketed leaked through) and for layout fragility (anything that breaks reveals a fixed-width container). Pair it with a bidi pseudo-locale to test direction at the same time. **Every multi-locale engagement should ship pseudo-localization in the build pipeline by default.**

---

## RTL layout support

### CSS logical properties

The 2026 best practice for bidirectional layout is to write CSS in **logical properties** — properties that resolve to physical sides based on the document's writing mode and direction.

| Physical | Logical | Resolves in LTR | Resolves in RTL |
|---|---|---|---|
| `margin-left` | `margin-inline-start` | Left | Right |
| `padding-right` | `padding-inline-end` | Right | Left |
| `border-left` | `border-inline-start` | Left | Right |
| `text-align: left` | `text-align: start` | Left | Right |
| `left: 0` | `inset-inline-start: 0` | Left | Right |
| `border-top-left-radius` | `border-start-start-radius` | Top-left | Top-right |
| `width` | `inline-size` | Horizontal | Horizontal |
| `height` | `block-size` | Vertical | Vertical |

A single rule using `margin-inline-start: 16px` works in both LTR and RTL contexts without overrides. The page or component root sets `dir="rtl"` and the entire layout flips.

**Browser support is now near-universal** for the core logical properties (margins, padding, borders, inset, text-align, sizing). Corner-radius logical equivalents and intrinsic-sizing logical equivalents shipped later but are also widely supported by 2026. **We treat physical properties as legacy and write logical from new code.** Whether to refactor existing CSS depends on whether the product is going RTL — and we should be asking that in Discovery.

**For inline content that bucks the document direction** — a Latin URL inside an Arabic paragraph, a code snippet inside an RTL UI — the right tool is the `<bdi>` element or `dir="ltr"` attribute on a span, plus `unicode-bidi: isolate` in CSS. These prevent the bidi algorithm from re-ordering content that has its own internal direction.

### Component mirroring rules

Mirroring is not "flip every pixel." It's "flip what reflects directionality of reading or time; preserve what reflects physical objects, brand, or universal conventions."

| Element class | Mirror in RTL? | Reasoning |
|---|---|---|
| Layout containers | Yes | Reading order flips; layout follows. |
| Navigation (breadcrumbs, tabs, steppers) | Yes | Sequence direction follows reading order. |
| Back/forward arrows | Yes | "Back" points toward the past — opposite direction in RTL. |
| Progress bars, sliders | Yes | Fill direction follows reading direction. |
| Icons of directional motion (airplane departing) | Yes | Direction is meaningful. |
| Text alignment / indent icons | Yes | Indent direction reflects script direction. |
| Numbers, phone numbers, dates within RTL text | No | Numerals are read LTR even within RTL paragraphs. |
| Code, URLs, file paths | No | Technical syntax has fixed direction. |
| Media playback controls (play, FF, RW) | No | Represent tape direction, not time. Universal convention. |
| Brand logos, wordmarks | No | Identity must be preserved. |
| Charts and graphs | Sometimes | If x-axis represents time, mirror; if it represents a category set, do not. Decide per chart type. |
| Icons of physical objects (pencil, magnifier, key) | Usually no | Object orientation is a real-world convention, not a reading one. |
| Clock and analog time icons | No | Clock face is universal. |

**The mistake teams make most often** is mirroring everything, then having to manually un-mirror logos, numbers, and media controls. **The right default is to mirror layout via logical properties; declare per-icon whether it mirrors via metadata in the icon library.**

### Icon directionality in the library

Icons should carry a metadata flag — `directional: true` or `mirror: true` — that the build pipeline reads. Directional icons either ship as two assets (LTR and RTL versions) or render with `transform: scaleX(-1)` applied via the `[dir="rtl"]` selector. The latter is cheaper but breaks if the icon includes embedded text or a brand mark; in those cases ship two assets.

Common directional icons that need attention: arrows, chevrons, send/forward, back/return, undo/redo (sometimes), trending arrows, list-with-bullets (indent direction), text alignment, paragraph indent, attached file (clip orientation), reply arrows.

### Figma for RTL

Figma's native RTL support has improved through 2024–2025 but remains incomplete. Mode-based workarounds (covered below) are real partial solves, but residual issues — particularly around mixed-direction strings — bite in production, so we land cautious.

The structural problems:

- **Bidi text rendering** in Figma sometimes diverges from browser rendering, particularly for mixed-direction strings (Latin within Arabic). What looks correct in Figma may render differently in the live product. Cross-validate in browser.
- **No native concept of logical properties** at the component level — designers manually swap padding-left/padding-right when designing the RTL view, or wire it through Figma Variables (see §Figma workflow below).
- **Mirroring an Auto Layout frame** doesn't always handle nested instance directions correctly — children may need separate treatment.
- **No vertical text flow** — traditional Japanese and Chinese vertical text is unsupported.

The pragmatic stance: design the LTR component, validate the RTL behavior in code (or via a Figma plugin that simulates direction), and document the expected RTL state. **Don't try to make Figma the authoritative RTL preview.**

### Testing RTL

Three layers of validation, in order of cost:

1. **Static layout review** with `dir="rtl"` set on `<html>` or the component root. Catches CSS that didn't migrate to logical properties.
2. **Pseudo-localization** with a bidi pseudo-locale that sets direction *and* expands strings. Catches both directional and expansion issues simultaneously. Firefox has a built-in pseudo-locale flag (commonly cited as `intl.l10n.pseudo` set to `bidi`; verify the exact flag name against current Firefox docs as flag names change). Chromium has equivalent capabilities via DevTools.
3. **Real-locale visual regression** — actual translated content in actual RTL renders, captured via Playwright/Cypress and diffed. The most expensive check; catches what synthetic locales miss.

Most teams stop at level 2 and ship. Level 3 belongs in the CI pipeline for products with significant RTL user bases.

---

## Typography for international content

The depth of typography-specific tokenisation (the three-tier mandatory stack, modular scales, fluid type, variable fonts, line-height discipline, the native platform translation) lives in 23-typography-tokenisation. This section covers the i18n-specific concerns; 23 covers the typography-as-architecture concerns the multi-script discipline sits within.

### Text expansion and component sizing

Translations from English expand or contract by language; the rule of thumb is that **shorter strings expand more, often dramatically.** IBM and W3C have published guidance with specific percentages. A commonly-cited budget table appears below; for client-facing recommendations, cite the source rather than asserting the numbers as our practice POV:

| English source length | Average expansion | Suggested design budget |
|---|---|---|
| Up to 10 chars | 200–300% | 4× original width |
| 11–20 chars | 180–200% | 3× original width |
| 21–30 chars | 160–180% | 2.5× original width |
| 31–50 chars | 140–160% | 2× original width |
| Over 70 chars | 130% | 1.5× original width |

(Broadly aligned with IBM/W3C published guidance. Verify the specific numbers against current published sources before using them in client materials.)

The implication is binary: **components that hold text must grow with content.** Fixed widths, fixed `min-width` without `max-width`, and any layout that requires text to fit a precise pixel count will break.

Languages that consistently expand from English: German (compound nouns), Finnish, Russian, French, Polish, Portuguese, Italian. Languages that often contract: Chinese, Japanese, Korean. **A button reading "Save" at 32px in English may need 80px in German and 24px in Chinese** — designs that look balanced in English will look wrong in either direction without flexibility.

### Non-Latin scripts: line-height and density

Different scripts have different vertical metrics, descender depths, and density. A type scale tuned for Latin will fail other scripts in predictable ways. Material Design's three-category framing is the established convention:

- **English-like (Latin, Greek, Cyrillic).** Standard 1.4–1.5× line-height for body text.
- **Tall (Arabic, Hebrew, Devanagari, Thai, Vietnamese).** Descenders below the Latin baseline, diacritics above; line-height tuned for Latin clips both. Convention: 1.5–1.7× minimum, with extra paragraph spacing.
- **Dense (Chinese, Japanese, Korean).** Square logographic grid; uniform vertical rhythm; no real ascenders/descenders. Convention: ~1.5–1.7× for body text. The visual effect of "tightness" differs substantially from Latin and requires script-specific tuning.

**A type scale that works globally needs per-script line-height tokens, not a single global value.** The pattern: define `line-height/body/latin`, `line-height/body/arabic`, `line-height/body/cjk`, etc., and apply via `:lang()` selectors or per-locale mode.

When mixing Latin and CJK in the same string, Latin characters often appear optically smaller at the same point size. Some shops compensate by scaling Latin up slightly within CJK contexts; others accept the visual difference. Document the decision either way.

### The variable-fonts misunderstanding

A common misunderstanding worth correcting directly: **variable fonts do not solve multi-script support.** This conflation comes up often enough that the practice should call it out explicitly.

Variable fonts vary axes (weight, width, slant, optical size) within a single script. A variable Latin font has no Arabic glyphs; a variable Arabic font has no CJK. Multi-script support is a **font-stack** problem — choosing which fonts cover which scripts and how they fall through.

Three common patterns:

1. **Brand font + script-specific fallbacks.** Brand font for Latin; Noto Sans Arabic for Arabic; Noto Sans CJK for Chinese/Japanese/Korean. Browser falls through the stack based on character coverage. Works but produces visually inconsistent typography across languages.
2. **Universal-coverage font.** Noto family is the most common — Google's "no tofu" project covering virtually every Unicode script. Visually consistent, but means giving up the brand font for non-Latin locales. Often the right tradeoff for product UI.
3. **System font stack.** `system-ui` falls through to the OS default (San Francisco on macOS/iOS, Segoe on Windows, Roboto on Android, Cantarell or similar on Linux). Each OS ships fonts that cover its primary locales well. Performance is excellent (no download); brand consistency is sacrificed.

| OS / Platform | Default system font | Notes |
|---|---|---|
| macOS / iOS | San Francisco | Variable; high legibility |
| Windows | Segoe UI | Optimized for screen rendering |
| Android | Roboto / Noto fallback | Broad Unicode coverage via Noto |
| Linux | Cantarell / Ubuntu / others | Distribution-dependent |

**`system-ui` covers Latin and major scripts on most modern OSs but is not a guarantee for less-common scripts.** A font stack like `system-ui, "Noto Sans Arabic", "Noto Sans CJK SC", sans-serif` is often the right shape — system font as the primary, script-specific Noto for guaranteed coverage, generic fallback as the floor.

Variable fonts *do* help within a script: a single variable font file replaces 4–8 weight files, reducing payload. They're a performance and consistency win within a script, not a multi-script solution.

### Font loading strategy

Loading a CJK font is a performance event — full Chinese coverage runs into multiple megabytes. Strategies for managing this:

- **Subsetting.** The webfont service (or build pipeline) generates per-script subsets of the brand font. The locale's HTML loads only its script's subset. Google Fonts and most font CDNs support unicode-range subsetting that browsers handle automatically.
- **Lazy-load by detection.** Latin font loaded synchronously; non-Latin font loaded async after locale detection. Trades initial render latency for non-Latin users for unblocked first-paint.
- **System fonts where possible.** Serve `system-ui` for as much as possible; pull script-specific fonts only where the brand font doesn't cover.
- **`font-display: swap` and FOUT acceptance.** Show fallback text while the script-specific font loads; swap when ready. Better than holding render. The initial flash is acceptable; the failed render isn't.

The DS should specify the loading strategy as part of typography token documentation. Leaving it to consuming products produces wildly inconsistent perceived performance across locales.

---

## Token architecture for locale-specific values

### What belongs in tokens

The principle: **tokens hold design decisions; locale data is application concern.** A token is the right home for a decision the design team made (e.g., "Arabic body text uses 1.6× line-height"). It's not the right home for a piece of regional data (e.g., "the Saudi Arabia date format is DD/MM/YYYY").

That distinction makes the boundary clear:

- **In tokens:** locale-specific spacing, line-height, density, font stacks, font sizes. Anything visual that the design team has decided varies per locale.
- **Not in tokens:** date formats, number formats, calendar systems, address structures, currency symbols. These are computed by the consuming application using `Intl.*` APIs (or platform equivalents) at runtime.

### Locale-aware tokens via modes

The mechanism to encode locale-specific design values in a token system depends on the tooling:

- **Figma Variables modes.** Define a Locale (or Direction) mode dimension and let semantic spacing/line-height variables resolve differently per mode. Frames inherit the mode from their context.
- **Style Dictionary themes / DTCG token sets.** Generate locale-specific stylesheets (`tokens.latin.css`, `tokens.arabic.css`) and switch them at runtime via attribute selectors (`html[lang="ar"]`). The build pipeline materializes the differences into discrete CSS variable values.
- **CSS custom properties with `:lang()` selectors.** Define base tokens and override at the language level. `--line-height-body: 1.5` globally; `:lang(ar) { --line-height-body: 1.7 }` for Arabic.

The third pattern is the most direct and most readable, but spreads the locale logic across the stylesheet rather than centralizing it. (See 02-design-foundations on the broader token architecture.)

### Density adjustments — handle with care

CJK scripts pack more semantic content per character than Latin — a Chinese sentence carrying the same meaning as an English one is shorter. Some teams adapt by using denser spacing tokens for CJK locales: smaller padding inside buttons, tighter list spacing, smaller default font sizes. The argument is that CJK readers are accustomed to denser layouts and that retaining Latin-density spacing wastes screen real estate. The counter-argument is that consistent density across locales is simpler to maintain and that tightening CJK risks legibility for older users.

**Most agencies should not tune density per locale unless the client explicitly asks.** It's a real concern but the maintenance cost outweighs the benefit for most products. If we do tune, document the rationale clearly so it's not accidentally undone by a later contributor.

### Color and cultural meaning

Color carries cultural connotations that vary substantially by market: red signals luck and prosperity in much of East Asia, danger in most Western markets, communism politically in some, hospitality elsewhere. Green carries Islamic religious meaning in Muslim-majority regions. White is purity in some markets, mourning in others.

The DS response is **never name a color token after a connotation.** `color/red-error` propagates a Western convention into the architecture. `color/status/danger` is semantic — and the value that resolves can be remapped per market if the brand makes that decision. Most won't (visual consistency across markets is usually prioritized over cultural color reskinning), but the architecture must support remapping if it's needed.

The DS should also document **complementary signals** for status that don't rely solely on color: an error icon, a warning icon, a checkmark for success. This is good practice for two reasons at once — color alone failing is also an accessibility issue (color blindness), and it makes status communication robust to cultural color variation. (See 02-design-foundations on the accessibility-as-foundational stance.)

### Where formatting lives

Formatting is application concern, full stop. The DS's job is to define the **component slot** that holds formatted output, not the formatting logic.

- A `DateDisplay` component takes a formatted string as a prop and lays it out — it doesn't take a `Date` object and format it internally.
- A `Currency` component takes the formatted currency string and styles it; the application uses `Intl.NumberFormat` to produce the string per locale.
- A `PhoneNumber` component takes the formatted number and applies the visual treatment; the application validates and formats per ITU/E.164 rules and locale conventions (typically via libphonenumber).

This separation means the DS doesn't need to ship a localization runtime, doesn't track every market's formatting rules, and doesn't break when a new locale is added. **The DS provides the visual contract; the application provides the data.**

---

## Component-level i18n considerations

### Expansion-sensitive components

The components most often broken by translation:

- **Buttons.** Must grow with text. Use `inline-flex`, set a `min-width` for visual balance but no `max-width`. Truncation with ellipsis is a fallback, not a primary strategy — clipped button labels degrade usability.
- **Tabs.** Tab labels can expand significantly; static tab widths break. Either let tabs grow naturally and overflow into a "More" menu, or use scroll containers. Both have tradeoffs (overflow menus hurt discovery; scrollers hurt scannability).
- **Navigation items.** Sidebar nav with fixed-width labels breaks fast. Either use icon-only nav with text on hover/expand, or design for the expanded case as the default.
- **Badges and counters.** Numeric badges grow when numbers grow ("99+" is shorter than "10,000+"); some locales use longer separators. Allow horizontal growth.
- **Form labels.** Above-the-input labels translate cleanly; inline labels (label-on-the-left-of-input) break with expansion. Default to above-the-input.
- **Empty states and headers.** Often have generous English copy; designs that look right in English become wrong in expansion-heavy locales. Mock translations during design review.

### Form components for international input

Forms are where i18n complexity concentrates because they intersect locale, script, and region.

- **Date pickers.** Different locales have different week-start conventions (Sunday in US, Monday in most of Europe, Saturday in some Middle Eastern countries). Different month/year orderings (DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD). Different calendar systems (Gregorian, Hijri/Islamic, Buddhist, Japanese imperial era). The DS should provide a date picker whose week-start, format, and calendar are configurable, not baked in. Most agencies don't ship a fully calendar-system-aware date picker from scratch and lean on third-party (Adobe Spectrum's, MUI X's, react-aria's).
- **Phone number fields.** International phone numbers vary in length, formatting, and country-code conventions. The pattern is a country selector plus national number field, with formatting applied per country (libphonenumber is the common engine). The DS provides the layout; the application provides the formatting library.
- **Address forms.** Address structure varies wildly: Japanese addresses are big-to-small (prefecture → city → street), Western addresses are small-to-big (street → city → state). Some countries don't use postal codes; some have multiple postal-code formats. Many countries have no concept of "state." Using a fixed "Street / City / State / ZIP" template excludes them. The DS pattern is **slot-shaped address forms** where the application supplies a country-specific template and the DS provides the field-level styling. **Avoid baking address structure into the component.**
- **Name fields.** Single name field is the right default; "first name / last name" assumes a Western name structure that fails for many cultures. Some users have one name; some have multiple given names; some have patronymics; the order of given/family names varies by culture.

### Number, currency, and date display components

The pattern for display components:

```
<DateDisplay value={formatDateForLocale(date, locale)} />
<Currency value={formatCurrencyForLocale(amount, currency, locale)} />
<NumberDisplay value={formatNumberForLocale(value, locale)} />
```

The component receives a string and styles it. The locale-aware formatting is application work using `Intl.*` APIs. **This keeps the component free of locale knowledge and makes new locales additive — no DS changes needed.**

### Navigation patterns in RTL

- **Breadcrumbs.** Mirror entirely. `Home > Products > Shoes` becomes `Shoes < Products < Home` — the chevron mirrors too. The home icon moves to the right.
- **Tabs.** Mirror order. The first tab in source order renders rightmost in RTL.
- **Steppers.** Mirror direction. Step 1 on the right; arrows point left.
- **Pagination.** Mirror direction. "Previous" on the right; "Next" on the left.
- **Carousels.** Mirror swipe direction; auto-advance moves right-to-left.
- **Dropdowns/menus.** Open from the start of the trigger (right side in RTL).
- **Modals and toasts.** Position mirrors — top-right toast in LTR becomes top-left in RTL. Use `top-end` (logical) so it lands correctly per direction.

The general rule: **anything tied to reading or temporal direction mirrors. Anything universal does not.**

---

## Figma workflow for multi-locale design

### The maintenance trap

Without intervention, multi-locale Figma libraries double in maintenance burden — every component has an LTR copy and an RTL copy, every typography update happens twice, every spacing change happens twice. **This is the wrong default.** A DS at any scale cannot sustain it.

### Variable-driven locale modes

Figma Variables with mode dimensions partially solve the problem. Define a `Direction` mode (`LTR`, `RTL`) and bind component padding, text alignment, and instance-swap properties to mode-aware variables. Switching the frame's mode flips the component without duplicating it.

What this works for:

- **Padding/margin direction.** `padding-start` and `padding-end` variables that resolve differently per mode.
- **Text alignment.** `text-align/start` resolves to `left` in LTR mode and `right` in RTL mode.
- **Mirrored icons via instance swap.** A directional icon's instance-swap property points to the LTR icon in LTR mode, the RTL variant in RTL mode.

What it doesn't work for:

- **Bidi text rendering.** Figma's text engine handles Arabic and Hebrew but with known inconsistencies vs. browser rendering. Mixed-direction strings particularly suffer.
- **Component structural mirroring.** A component whose Auto Layout structure assumes LTR (icon-then-label) doesn't auto-flip when mode changes; the structure remains as designed. Workarounds involve nested instances with mode-aware swaps, which gets complex fast.
- **Vertical writing modes.** Traditional Japanese and Chinese vertical text — Figma has no native support. Designers either skip it or use rotated frames as approximations.

Modes are a real partial solution and worth implementing, but they don't make Figma the authoritative RTL preview.

### A workable pattern

For most engagements, the right Figma pattern is:

1. **Design components in LTR with logical-property-style variable bindings** (padding-start, padding-end, alignment-start). Treat LTR as the source.
2. **Provide a small set of RTL exemplar pages** showing key components and patterns in RTL via mode switch, so designers and reviewers can validate.
3. **Document RTL behavior in component descriptions** — what mirrors, what doesn't, what edge cases the engineer needs to know about.
4. **Don't try to maintain full RTL parity in Figma.** Validate critical RTL behavior in the live product.

(See 12-figma-practice on Figma Variables and modes generally, including mode-multiplication costs.)

### The "Locale" mode question

Some teams push further and define modes for specific locales (Arabic, Japanese, German) rather than just direction (LTR/RTL). This makes sense for showcasing real translated content but multiplies modes quickly — especially when crossed with theme and density modes. **The simpler default is direction-as-mode plus translated content rendered in LTR/RTL frames as needed.** Reserve full locale modes for engagements where multi-locale design preview is the explicit deliverable.

---

## Implementation and handoff

### What the DS hands off

The DS should ship i18n requirements as an **explicit contract**, not as implicit expectations:

- **CSS guidance.** Logical properties are the convention. New code uses them; legacy code is migrated when touched. Document this in the engineering README and enforce via lint rules (`stylelint-use-logical` or equivalent).
- **Mirroring metadata.** Each icon in the icon library carries a `directional` flag; the build pipeline produces RTL variants automatically for directional icons. Each component's docs declare RTL behavior explicitly.
- **Token contract.** Locale-aware tokens are documented as such; consuming applications know to wire `:lang()` or `[dir]` selectors to switch token resolution.
- **Component contract.** Date/number/currency components take formatted strings; consuming applications produce them via `Intl.*`. This boundary is documented explicitly so neither side reinvents.
- **Pseudo-localization tooling.** The DS recommends and ideally provides a pseudo-locale build (a fake locale with bracketed, accented, expanded strings) for design and engineering validation.

(See 04-documentation on the broader docs strategy and 05-development-support on the dev pipeline.)

### The DS / application boundary

The clearest framing: **DS provides the shell; application provides the content.**

- DS provides: layout that mirrors, components that grow, tokens that adjust, icons with declared directionality.
- Application provides: translated strings, locale-formatted dates/numbers/currencies, address-form templates, calendar choice, font subsetting strategy, locale detection.

Where it gets blurry: address forms, date pickers, and complex form patterns that the DS *could* ship as locale-aware. **The right default is to ship the layout slots and let the application fill them.** Baking locale logic into the DS means updating the DS every time a market is added — which is the wrong place for that update to land.

### CSS logical properties: status

By 2026, all major browsers support the core logical properties. The remaining gaps are edge cases — some scroll-related logical properties shipped later, some intrinsic-sizing logical properties are still maturing. **For the working subset (margin, padding, border, inset, text-align, sizing) treat logical properties as the default.** Polyfills exist for legacy browsers but most products no longer need them.

The adoption status across DSs is uneven. Older systems carry physical-property legacy code that hasn't been migrated; newer systems are logical-first. **Auditing a client's existing CSS for physical-property usage is a useful Discovery activity if RTL is anticipated** — it surfaces the retrofit cost concretely. (See 01-discovery-and-strategy.)

### The future direction

Two trends worth flagging in client conversations:

- **TMS integration into design.** Translation management systems (Lokalise, Phrase, Crowdin) increasingly offer Figma plugins that show real translated content in design files, replacing pseudo-localization for visual review. The pseudo-locale stays in CI; the TMS preview becomes the design-review tool.
- **Logical properties as default.** The migration from physical to logical CSS is now well underway across major DSs; within a few years, physical-property usage will look like the kind of legacy that requires explanation, not the kind that requires defense.

---

## Failure modes

- **The English-only default that wasn't decided.** No one chose to build LTR-only — the early authors just used `margin-left` because it was the obvious thing. Eighteen months later the product needs Arabic and the codebase is the obstacle. The cost is paid by the next team.
- **String externalization done partially.** Half the strings are in translation keys; the other half are hardcoded in JSX. Pseudo-localization surfaces the gaps; the project becomes "go find every untranslated string" for a quarter.
- **String concatenation for sentences.** `"You have " + count + " unread items"` ships, then breaks in every language with a different word order or grammatical structure. Refactoring to ICU MessageFormat is per-sentence work.
- **Fixed-width buttons and labels.** Designs that look "balanced" in English become broken in German. The fix is per-component; the discovery is per-screen.
- **Color tokens named after Western connotations.** `color/red-error` is in the codebase. Cultural reskinning becomes a refactor instead of a token override.
- **Date pickers that bake `MM/DD/YYYY`.** The DS ships a date picker that produces formatted strings internally; every locale beyond US-English needs the component rebuilt.
- **Address forms with fixed structure.** The DS's address form has Street / City / State / ZIP fields; expansion to markets without states or ZIPs requires rebuilding the form per market.
- **Icon directionality undeclared.** Icons ship without a mirroring flag; engineering teams make per-icon decisions inconsistently, ending up with backward arrows next to forward-pointing airplanes.
- **Variable fonts assumed to solve multi-script.** A team picks a beautiful variable Latin font and assumes it covers their global ambitions. CJK and Arabic don't render; the fix is rebuilding the font stack.
- **Figma RTL treated as authoritative.** The team validates RTL in Figma, ships it, and discovers that browser bidi handling differs from Figma's. Production bugs surface that the design review never caught.
- **Density tuned per locale without documentation.** A contributor sets CJK density tighter; another contributor doesn't know why and "fixes" it in a refactor; the locale-aware adjustment vanishes silently.
- **Pseudo-localization deferred to QA.** Layout breakage discovered weeks after design completion. Fixes ripple back through to component CSS and design.
- **The DS owning locale data.** The DS team starts maintaining an address-format library. Now the DS team is responsible for keeping address formats up to date globally — work that should never have entered the DS.

---

## Tensions and open questions

1. **How aggressive should we be in raising i18n in Discovery for clients who haven't named it as a requirement?** The retrofit cost argument is strong, but raising it on every engagement risks scope creep and may price us against competitors who don't. The defensible position is probably "always raise on engagements with global brand presence; raise on others when CSS architecture choices come up." Worth productizing as a Discovery question.

2. **How much locale-aware token work should we ship by default?** Per-script line-height, locale-aware spacing, multi-script font stacks — all real concerns, all add complexity. For clients with one or two locales, the floor (logical properties + externalized strings + growth-friendly components) is enough. For clients with five-plus locales, the floor isn't. Where's the threshold? An open question for our scoping framework.

3. **The Figma RTL preview gap.** TMS plugins and direction-mode patterns are partial solves. The honest answer is that Figma is not yet a reliable RTL preview surface, and we should validate in browser. This produces friction in client review processes that expect Figma to be authoritative. Worth a POV piece.

4. **Address forms and locale-aware patterns — DS or app?** The pure architectural answer is "app." The pragmatic answer for many clients is that they don't have the in-house engineering to build address forms per market, and they want the DS to ship it. Selling the architectural answer requires confidence in the client's engineering team or a clear path to a third-party (e.g., react-aria's address pattern). We don't currently have a defensible recommendation here.

5. **Cultural localization as a DS deliverable.** Most engagements stop at translation-readiness and multi-script typography; cultural color/iconography/imagery is usually owned by content/brand teams. Some clients with strong global brand presence want it brought into the DS. We don't have a productized framework for this; we'd be in pioneer mode.

6. **The bidi-icon catalog as practice IP.** Maintaining a curated, opinionated list of "icons that mirror, icons that don't, icons that need RTL variants" per common icon set (Material, Phosphor, Lucide, Tabler) is concrete, useful, defensible practice IP. No public catalog exists at the depth we'd want. A high-leverage internal investment if we want to differentiate on global readiness.

---

*Provenance: The CSS logical-properties pattern, the `<bdi>` / `unicode-bidi: isolate` controls for inline mixed-direction content, and the `:dir()` pseudo-class are documented at MDN and in W3C internationalization guidance. The Material Design three-script-category framing (English-like / Tall / Dense) for line-height comes from Material's regional customization guidance. The text-expansion budget is broadly aligned with IBM and W3C published numbers — the specific table presented should be verified against current sources before client-facing use. ICU MessageFormat is the established standard maintained by Unicode/ICU. Noto fonts and the "no tofu" universal-coverage strategy are from Google's Noto project. The `Intl.*` API delegation pattern is W3C/ECMA-262. The "DS provides the shell; application provides the content" boundary is the convergent practitioner framing, sharpened here as a defensible practice POV. The variable-fonts-don't-solve-multi-script correction is a misunderstanding the practice should call out explicitly when raised by clients or contributors. Practitioner sources include Robin Whittleton (Mozilla) on RTL CSS, Ahmad Shadeed on logical properties, and Adobe Spectrum's internationalization documentation. The four-level maturity ladder vocabulary (Locally Targeted → Globally Optimized) appears in some practitioner writing as a stakeholder-facing alternative to engineering stages. This file was synthesized from a dual-agent research run in May 2026 (see `_research/_archive/2026-05-05-i18n-rtl-l10n.md` for the editorial trail).*
