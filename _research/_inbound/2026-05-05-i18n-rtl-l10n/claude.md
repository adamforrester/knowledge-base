# Internationalization, Localization, and RTL in Design Systems

A practitioner's reference for senior design systems engineers and designers. Covers why i18n is a DS architecture concern, how to build for bidirectional layout, typography for international content, locale-aware tokens, component-level considerations, Figma workflow, and the boundary between DS and consuming application. Assumes fluency with design systems vocabulary and basic CSS; focuses on the current best practice and the gaps as of January 2026.

---

## 1. Why this is a DS architecture concern

Design systems built on the implicit assumption of English, Latin script, and left-to-right reading become global blockers the moment a product needs a second locale. The blockers are not surface-level (translating button labels) — they're architectural. Fixed-width buttons truncate German. Hardcoded `margin-left` strands Arabic. A type scale tuned for Latin x-heights leaves Devanagari clipped at the descender. Color tokens named `red-error` propagate a Western convention into markets where red signals positive prosperity.

**The DS is the right place to absorb this complexity.** If every consuming product team has to solve i18n independently, every product solves it differently and most solve it badly. The DS should ship with i18n already wired into tokens, components, and documentation — so that a product team adding a new locale is doing translation and content work, not architectural surgery.

### What i18n does to the four DS layers

- **Tokens.** Spacing tokens may need locale-aware values (CJK can sustain higher density; Arabic needs more line-height). Color tokens must be semantic, never named after Western connotations. Type tokens must accommodate multi-script font fallback chains, not assume a single brand font covers every locale.
- **Components.** Containers must grow with content — never fixed width. Layouts must use logical properties so they mirror automatically. Icons must declare whether they're directional (and ship RTL variants when they are). Date, number, and currency components must be slot-shaped, accepting locale-formatted output rather than baking format logic into the component.
- **Layout patterns.** Patterns that imply temporal direction (steppers, breadcrumbs, progress bars) must mirror in RTL. Patterns that don't (media controls, charts) must not. The DS must specify which is which — leaving it to consumers produces inconsistent application.
- **Documentation.** Every component's docs must declare RTL behavior and text-expansion behavior. Default-LTR-only documentation is a tell that the DS isn't actually global-ready.

### The cost of retrofitting

Retrofitting i18n into a system that wasn't built for it is expensive, asymmetrically. The work falls in four buckets:

1. **CSS refactor.** Every `margin-left`, `padding-right`, `text-align: left`, and `border-radius` corner reference becomes a logical-property migration. Mechanical but high-volume.
2. **String externalization.** Every hardcoded string in JSX/templates extracted to translation keys. Tooling helps; missed strings still show up at QA.
3. **Layout audit.** Every fixed-width container, every component that assumed text length within a known range. The most invisible category until pseudo-localization surfaces it.
4. **Component contract changes.** Components that baked in formatting (a date picker that produces "MM/DD/YYYY") need rebuilding around locale-agnostic shape with formatting injected.

A team that built i18n into the system from day one writes the same code at near-zero incremental cost. A team retrofitting it is doing the same work plus discovery, regression testing, and coordination across every consuming product. **The "build it in" cost is a small tax on every component; the "retrofit" cost is a six-to-twelve-month project, and that's optimistic.**

### The spectrum of support

Useful to think in stages, each demanding more from the DS:

- **Translation-ready.** Strings are externalized. Components grow with content. Logical properties used throughout. RTL works. This is the floor — the cost of a single component author thinking globally as they write.
- **Multi-script typography.** Type stack includes script-appropriate fallbacks. Line-height and spacing tokens are locale-aware. Component metrics (input height, button padding) accommodate scripts with taller glyphs.
- **Locale-aware components.** Date pickers, address forms, number/currency displays, phone fields — components whose internal logic varies by locale — are designed and documented around locale-injection patterns rather than fixed conventions.
- **Cultural localization.** Color semantics, iconography, imagery, tone of voice considered per market. Beyond what most DS teams ship; usually owned by content/brand teams in collaboration with the DS.

Most agencies should target the first two reliably and provide patterns for the third. The fourth is rarely a DS deliverable.

---

## 2. RTL layout support

### CSS logical properties: now the default

The 2026 best practice for bidirectional layout is to write CSS in logical properties — properties that resolve to physical sides based on the document's writing mode and direction.

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

A single rule using `margin-inline-start: 16px` works in both LTR and RTL contexts without overrides. The page or root element sets `dir="rtl"` and the entire layout flips.

**Browser support is now near-universal** for the core logical properties (margins, padding, borders, inset, text-align). The corner-radius logical equivalents (`border-start-start-radius`) shipped later but are also widely supported by 2026. Practitioners should treat physical properties as legacy and write logical from new code; whether to refactor existing CSS depends on whether the product is going RTL.

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
| Text alignment icons | Yes | Indent and align icons should match script direction. |
| Numbers, phone numbers, dates within RTL text | No | Numerals are read LTR even within RTL paragraphs. |
| Code, URLs, file paths | No | Technical syntax has fixed direction. |
| Media playback controls (play, FF, RW) | No | Represent tape direction, not time. Universal convention. |
| Brand logos, wordmarks | No | Identity must be preserved. |
| Charts and graphs (most cases) | Sometimes | If x-axis represents time, mirror; if it represents a category set, do not. Decide per chart type. |
| Icons of physical objects (pencil, magnifier, key) | Usually no | Object orientation is a real-world convention, not a reading convention. |
| Clock and analog time icons | No | Clock face is universal. |

**The mistake teams make most often** is mirroring everything, then having to manually un-mirror logos, numbers, and media controls. The right default is: mirror layout via logical properties; declare per-icon whether it mirrors via metadata in the icon library.

### Icon directionality in the library

Icons should carry a metadata flag — `directional: true` or `mirror: true` — that the build pipeline reads. Directional icons either ship as two assets (LTR and RTL versions) or render with a CSS `transform: scaleX(-1)` applied via the `[dir="rtl"]` selector. The latter is cheaper but breaks if the icon includes embedded text or a brand mark; in those cases ship two assets.

Common directional icons that need attention: arrows, chevrons, send/forward, back/return, undo/redo (sometimes), trending arrows, list-with-bullets (indent direction), text alignment, paragraph indent, attached file (clip orientation), reply arrows.

### Figma for RTL

Figma's native RTL support has improved through 2024–2025 but remains incomplete. The structural problems:

- **Bidi text rendering** in Figma sometimes diverges from browser rendering, particularly for mixed-direction strings (Latin within Arabic). What looks correct in Figma may render differently in the live product. Cross-validate in browser.
- **No native concept of logical properties** at the component level — designers must manually swap padding-left/padding-right when designing the RTL view, or wire it through variables (see §6).
- **Mirroring an Auto Layout frame** doesn't always handle nested instance directions correctly — children may need separate treatment.

The pragmatic approach: design the LTR component, validate the RTL behavior in code (or via a Figma plugin that simulates direction), and document the expected RTL state. Don't try to make Figma the authoritative RTL preview — it's not.

### Testing RTL

Three layers of validation:

1. **Static layout review** with `dir="rtl"` set on `<html>` or the component root. Catches CSS that didn't migrate to logical properties.
2. **Pseudo-localization** with a bidi pseudo-locale that sets direction *and* expands strings. Catches both directional and expansion issues simultaneously. Firefox has a built-in pseudo-locale flag (`intl.l10n.pseudo`) that practitioners report using; verify against current docs as flag names change. Chromium has equivalent capabilities via DevTools.
3. **Real-locale visual regression** — actual translated content in actual RTL renders, captured via Playwright/Cypress and diffed. The most expensive check; catches what synthetic locales miss.

Most teams stop at level 2 and ship. Level 3 belongs in the CI pipeline for products with significant RTL user bases.

---

## 3. Typography for international content

### Text expansion and component sizing

Translations from English expand or contract by language; the rule of thumb is that shorter strings expand more, often dramatically. IBM and W3C have published guidance with specific percentages — the consensus pattern is something like:

- Very short strings (< 10 chars): expect up to 2–3× expansion
- Short strings (10–20 chars): expect ~1.5–2× expansion
- Medium strings (20–50 chars): expect ~1.4× expansion
- Long strings (paragraph length): expect ~1.2–1.3× expansion

(Specific tables vary by source — for client-facing budgets, cite the source rather than asserting numbers without backing.)

The implication for component design is binary: **components that hold text must grow with content**. Fixed widths, fixed `min-width` without `max-width`, and any layout that requires text to fit a precise pixel count will break. Buttons, badges, navigation items, and labels are the most-affected components.

Languages that consistently expand from English: German (compound nouns), Finnish, Russian, French, Polish, Portuguese, Italian. Languages that often contract: Chinese, Japanese, Korean. **A button reading "Save" at 32px in English may need 80px in German and 24px in Chinese** — designs that look balanced in English will look wrong in either direction without flexibility.

### Non-Latin script support

Different scripts have different vertical metrics, descender depths, and density. A type scale tuned for Latin will fail other scripts in predictable ways:

- **Arabic and Hebrew** — descenders extend below the Latin baseline; diacritics extend above. Line-height tuned for Latin clips both. The convention is to use a larger line-height (typically 1.5–1.7× font size minimum, vs. 1.4× for Latin) and slightly larger paragraph spacing.
- **Devanagari (Hindi, Marathi, Sanskrit)** — characters hang from a top line ("shirorekha") rather than sitting on a baseline; ascenders matter more than descenders. Line-height needs to be generous; default Latin line-heights crowd the script.
- **CJK (Chinese, Japanese, Korean)** — ideographic, square character grid. No real ascenders/descenders; vertical rhythm is more uniform. Line-height conventions differ — typical recommendation is around 1.5–1.7× for body text, but the visual effect of "tightness" is very different from Latin and requires script-specific tuning. CJK also lacks word spaces in Chinese and Japanese, which affects line-break behavior.
- **Thai, Lao, Khmer** — complex stacked diacritics; line-height needs even more generosity (1.7×+ is common).

A type scale that works globally needs **per-script line-height tokens**, not a single global value. The pattern: define `line-height/body/latin`, `line-height/body/arabic`, `line-height/body/cjk`, etc., and apply via `:lang()` selectors or per-locale mode.

### Multi-script font stacks

A common misunderstanding: variable fonts solve multi-script support. They don't. **Variable fonts vary axes (weight, width, slant) within a single script.** A variable Latin font has no Arabic glyphs; a variable Arabic font has no CJK.

Multi-script support is a font-stack problem. Three common patterns:

1. **Brand font + script-specific fallbacks.** Brand font for Latin; Noto Sans Arabic for Arabic; Noto Sans CJK for Chinese/Japanese/Korean. Browser falls through the stack based on character coverage. Works but produces visually inconsistent typography across languages.
2. **Universal-coverage font.** Noto family is the most common — Google's "no tofu" project covering virtually every Unicode script. Visually consistent, but means giving up the brand font for non-Latin locales.
3. **System font stack.** `system-ui` falls through to the OS default (San Francisco on macOS/iOS, Segoe on Windows, Roboto on Android, Cantarell or similar on Linux). Each OS ships fonts that cover its primary locales well. Performance is excellent (no download); brand consistency is sacrificed.

**`system-ui` covers Latin and major scripts on most modern OSs but is not a guarantee for less-common scripts.** A font stack like `system-ui, "Noto Sans Arabic", "Noto Sans CJK SC", sans-serif` is often the right shape — system font as the primary, script-specific Noto for guaranteed coverage, generic fallback as the floor.

### Font loading strategy

Loading a CJK font is a performance event — full Chinese coverage runs into multiple megabytes. Strategies for managing this:

- **Subsetting.** The webfont service (or build pipeline) generates per-script subsets of the brand font. The locale's HTML loads only its script's subset. Google Fonts and most font CDNs support unicode-range subsetting that browsers handle automatically.
- **Lazy-load by detection.** Latin font loaded synchronously; non-Latin font loaded async after the user's locale is detected. Trades initial render latency for non-Latin users for unblocked first-paint.
- **CDN-served system fonts.** Serve `system-ui` for as much as possible; pull script-specific fonts only where the brand font doesn't cover.
- **`font-display: swap` and FOUT acceptance.** Show fallback text while the script-specific font loads; swap when ready. Better than holding render. The initial flash is acceptable; the failed render isn't.

The DS should specify the loading strategy as part of typography token documentation. Leaving it to consuming products produces wildly inconsistent perceived performance across locales.

---

## 4. Token architecture for locale-specific values

### What belongs in tokens

The principle: **tokens hold design decisions; locale data is application concern.** A token is the right home for a decision the design team made (e.g., "Arabic body text uses 1.6× line-height"). It's not the right home for a piece of regional data (e.g., "the Saudi Arabia date format is DD/MM/YYYY").

That distinction makes the boundary clear:

- **In tokens:** locale-specific spacing, line-height, density, font stacks, font sizes. Anything visual that the design team has decided varies per locale.
- **Not in tokens:** date formats, number formats, calendar systems, address structures, currency symbols. These are computed by the consuming application using `Intl.*` APIs (or platform equivalents) at runtime.

### Locale-aware tokens via modes

The mechanism to encode locale-specific design values in a token system depends on the token tooling:

- **Figma Variables modes.** Define a Locale mode dimension (`Latin`, `Arabic`, `CJK`) and let semantic spacing/line-height variables resolve differently per mode. Frames inherit the mode from their context. This works for design but doesn't translate to runtime CSS automatically.
- **Style Dictionary themes / DTCG token sets.** Generate locale-specific stylesheets (`tokens.latin.css`, `tokens.arabic.css`) and switch them at runtime via attribute selectors (`html[lang="ar"]`). The build pipeline materializes the token differences into discrete CSS variable values.
- **CSS custom properties with `:lang()` selectors.** Define base tokens and override at the language level. `--line-height-body: 1.5;` globally; `:lang(ar) { --line-height-body: 1.7; }` for Arabic.

The third pattern is the most direct and most readable, but spreads the locale logic across the stylesheet rather than centralizing it.

### Density and spacing

CJK scripts pack more semantic content per character than Latin — a Chinese sentence carrying the same meaning as an English one is shorter. Some teams adapt by using **denser spacing tokens for CJK locales**: smaller padding inside buttons, tighter list spacing, smaller default font sizes. The argument is that CJK readers are accustomed to denser layouts and that retaining Latin-density spacing wastes screen real estate. The counter-argument is that consistent density across locales is simpler to maintain and that tightening CJK risks legibility for older users.

**Most agencies should not tune density per locale unless the client explicitly asks.** It's a real concern but the maintenance cost outweighs the benefit for most products. Document the decision either way.

### Color and cultural meaning

Color carries cultural connotations that vary substantially by market: red signals luck and prosperity in much of East Asia, danger in most Western markets, communism politically in some, hospitality elsewhere. Green carries Islamic religious meaning in Muslim-majority regions. White is purity in some markets, mourning in others.

The DS response is **never name a color token after a connotation**. `color/red-error` propagates a Western convention. `color/status/danger` is semantic — and the value that resolves can be remapped per market if the brand makes that decision. (Most don't; visual consistency across markets is usually prioritized over cultural color reskinning. But the architecture must support remapping if it's needed.)

The DS can also document **complementary signals** for status that don't rely solely on color: an error icon, a warning icon, a checkmark for success. Color alone failing is also an accessibility issue (color blindness), so this practice is doubly valuable. (See 02-design-foundations and 03-component-library.)

### Where formatting lives

Formatting is application concern, full stop. The DS's job is to define the **component slot** that holds formatted output, not the formatting logic.

- A `DateDisplay` component takes a formatted string as a prop and lays it out — it doesn't take a `Date` object and format it internally.
- A `Currency` component takes the formatted currency string and styles it; the application uses `Intl.NumberFormat` to produce the string per locale.
- A `PhoneNumber` component takes the formatted number and applies the visual treatment; the application validates and formats per ITU/E.164 rules and locale conventions.

This separation means the DS doesn't need to ship a localization runtime, doesn't need to track every market's formatting rules, and doesn't break when a new locale is added. The DS provides the visual contract; the application provides the data.

---

## 5. Component-level i18n considerations

### Expansion-sensitive components

The components most often broken by translation:

- **Buttons.** Must grow with text. Use `inline-flex`, set a `min-width` for visual balance but no `max-width`. Truncation with ellipsis is a fallback, not a primary strategy — clipped button labels degrade usability.
- **Tabs.** Tab labels can expand significantly; static tab widths break. Either let tabs grow naturally and overflow into a "More" menu, or use scroll containers. Both have tradeoffs (overflow menus hurt discovery; scrollers hurt scannability).
- **Navigation items.** Sidebar nav with fixed-width labels breaks fast. Either use icon-only nav with text on hover/expand, or design for the expanded case as the default.
- **Badges and counters.** Numeric badges grow when numbers grow ("99+" is shorter than "10,000+"); some locales use longer separators. Allow horizontal growth.
- **Form labels.** Above-the-input labels translate cleanly; inline labels (label-on-the-left-of-input) break with expansion. Default to above-the-input.
- **Empty states and headers.** Often have generous English copy; designs that look "right" in English become wrong in expansion-heavy locales. Mock translations during design review.

### Form components for international input

Forms are where i18n complexity concentrates because they intersect locale, script, and region.

- **Date pickers.** Different locales have different week-start conventions (Sunday in US, Monday in most of Europe, Saturday in some Middle Eastern countries). Different month/year orderings (DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD). Different calendar systems (Gregorian, Hijri/Islamic, Buddhist, Japanese imperial). The DS should provide a date picker whose week-start, format, and calendar are configurable, not baked in. This is a substantial component; many DSs lean on third-party (e.g., Adobe Spectrum's, MUI X's) rather than building it.
- **Phone number fields.** International phone numbers vary in length, formatting, and country-code conventions. The pattern is a country selector + national number field, with formatting applied per country (libphonenumber is the common engine). The DS provides the layout; the application provides the formatting library.
- **Address forms.** Address structure varies wildly: Japanese addresses are big-to-small (prefecture → city → street), Western addresses are small-to-big (street → city → state). Some countries don't use postal codes; some have multiple postal-code formats. Many countries have no concept of "state" — using a fixed "Street / City / State / ZIP" template excludes them. The DS pattern is **slot-shaped address forms** where the application supplies a country-specific template and the DS provides the field-level styling. Avoid baking address structure into the component.
- **Name fields.** Single name field is the right default; "first name / last name" assumes a Western name structure that fails for many cultures. Some users have one name; some have multiple given names; some have patronymics; the order of given/family names varies.

### Number, currency, and date display components

The pattern for display components:

```
<DateDisplay value={formatDateForLocale(date, locale)} />
<Currency value={formatCurrencyForLocale(amount, currency, locale)} />
<NumberDisplay value={formatNumberForLocale(value, locale)} />
```

The component receives a string and styles it. The locale-aware formatting is application work using `Intl.*` APIs. This keeps the component free of locale knowledge and makes new locales additive (no DS changes needed).

### Navigation patterns in RTL

- **Breadcrumbs.** Mirror entirely. `Home > Products > Shoes` becomes `Shoes < Products < Home` (with `<` actually being `>` in the RTL rendering — the chevron mirrors too). The home icon moves to the right.
- **Tabs.** Mirror order. The first tab in source order renders rightmost in RTL.
- **Steppers.** Mirror direction. Step 1 on the right; arrows point left.
- **Pagination.** Mirror direction. "Previous" on the right; "Next" on the left.
- **Carousels.** Mirror swipe direction; auto-advance moves right-to-left.
- **Dropdowns/menus.** Open from the start of the trigger (right side in RTL).
- **Modals and toasts.** Position mirrors — top-right toast in LTR becomes top-left in RTL.

The general rule: anything tied to reading or temporal direction mirrors. Anything universal (close button at top-right, modal centered) does not — but `top-right` becomes `top-end` (logical) so it lands correctly per direction.

---

## 6. Figma workflow for multi-locale design

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
- **Component structural mirroring.** A component whose Auto Layout structure assumes LTR (e.g., icon-then-label) doesn't auto-flip when mode changes; the structure remains as designed. Workarounds involve nested instances with mode-aware swaps, which gets complex fast.
- **Vertical writing modes.** Traditional Japanese and Chinese vertical text — Figma has no native support. Designers either skip it or use rotated frames as approximations.

### A workable pattern

For most engagements, the right Figma pattern is:

1. **Design components in LTR with logical-property-style variable bindings** (padding-start, padding-end, alignment-start). Treat LTR as the source.
2. **Provide a small set of RTL exemplar pages** showing key components and patterns in RTL via mode switch, so designers and reviewers can validate.
3. **Document RTL behavior in component descriptions** — what mirrors, what doesn't, what edge cases the engineer needs to know about.
4. **Don't try to maintain full RTL parity in Figma.** Validate critical RTL behavior in the live product.

### The "Locale" mode question

Some teams push further and define modes for specific locales (Arabic, Japanese, German) rather than just direction (LTR/RTL). This makes sense for showcasing real translated content but multiplies modes quickly — especially when crossed with theme and density modes. **The simpler default is direction-as-mode plus translated content rendered in LTR/RTL frames as needed.** Reserve full locale modes for engagements where multi-locale design preview is the explicit deliverable.

---

## 7. Implementation and handoff

### What the DS hands off

The DS should ship i18n requirements as an explicit contract, not as implicit expectations:

- **CSS guidance.** Logical properties are the convention. New code uses them; legacy code is migrated when touched. Document this in the engineering README and enforce via lint rules (`stylelint-use-logical` or equivalent).
- **Mirroring metadata.** Each icon in the icon library carries a `directional` flag; the build pipeline produces RTL variants automatically for directional icons. Each component's docs declare RTL behavior explicitly.
- **Token contract.** Locale-aware tokens are documented as such; consuming applications know to wire `:lang()` or `[dir]` selectors to switch token resolution.
- **Component contract.** Date/number/currency components take formatted strings; consuming applications produce them via `Intl.*`. This boundary is documented explicitly so neither side reinvents.
- **Pseudo-localization tooling.** The DS recommends and ideally provides a pseudo-locale build (a fake locale with bracketed, accented, expanded strings) for design and engineering validation.

### The DS / application boundary

The clearest framing: **DS provides the shell; application provides the content.**

- DS provides: layout that mirrors, components that grow, tokens that adjust, icons with declared directionality.
- Application provides: translated strings, locale-formatted dates/numbers/currencies, address-form templates, calendar choice, font subsetting strategy, locale detection.

Where it gets blurry: address forms, date pickers, and complex form patterns that the DS could ship as locale-aware. The right default is to ship the layout slots and let the application fill them; the wrong default is to bake locale logic into the DS and have to update it every time a market is added.

### CSS logical properties: status

By 2026, all major browsers support the core logical properties. The remaining gaps are edge cases — some scroll-related logical properties shipped later, some intrinsic-sizing logical properties are still maturing. **For the working subset (margin, padding, border, inset, text-align, sizing) treat logical properties as the default.** Polyfills exist for legacy browsers but most products no longer need them.

The adoption status across DSs is uneven. Older systems carry physical-property legacy code that hasn't been migrated; newer systems are logical-first. Auditing a client's existing CSS for physical-property usage is a useful Discovery activity if RTL is anticipated.

---

## References

Primary sources, current as of Jan 2026.

**W3C and Unicode:**
- W3C Internationalization Working Group: <https://www.w3.org/International/>
- W3C i18n techniques (text size, RTL): <https://www.w3.org/International/techniques/>
- Unicode CLDR (Common Locale Data Repository): <https://cldr.unicode.org/>
- Unicode Bidi Algorithm: <https://unicode.org/reports/tr9/>

**MDN:**
- CSS Logical Properties and Values: <https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values>
- `:dir()` pseudo-class: <https://developer.mozilla.org/en-US/docs/Web/CSS/:dir>
- `<bdi>` element: <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/bdi>
- Intl API: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl>

**Platform i18n guidance:**
- Material Design — bidi and language: <https://m3.material.io/foundations/customization/regional-customization>
- Apple HIG — Internationalization: <https://developer.apple.com/design/human-interface-guidelines/inclusion>
- Microsoft Globalization: <https://learn.microsoft.com/en-us/globalization/>

**Practitioner sources:**
- Robin Whittleton (Mozilla) — RTL CSS techniques
- Ahmad Shadeed — RTL-specific writing on logical properties and CSS
- IBM — text expansion guidance and i18n checklist
- Adobe Spectrum — internationalization documentation: <https://spectrum.adobe.com/page/internationalization/>
- Mozilla Developer Network — bidi-text-handling tutorials

**Tooling:**
- ICU MessageFormat: <https://unicode-org.github.io/icu/userguide/format_parse/messages/>
- libphonenumber: <https://github.com/google/libphonenumber>
- Noto fonts: <https://fonts.google.com/noto>
- Stylelint logical-properties rule: `stylelint-use-logical`

**Note on currency:** Browser logical-property support, Figma RTL feature scope, and specific platform i18n APIs all evolve. Verify against current docs before locking client-facing recommendations to a specific browser/version/feature claim.
