You are researching i18n, l10n, and RTL (right-to-left) support in design systems, for a senior design systems practitioner at a digital agency. The output is a structured knowledge document. Most design system source material is silent on this topic — this research should fill that gap with current, practical guidance.

Research scope — cover all of the following:

1. Why this is a DS architecture concern, not just a content concern

How internationalization requirements affect token architecture, component structure, layout patterns, and documentation
The cost of retrofitting i18n into a DS that wasn't designed for it vs. building it in from the start
The spectrum from "globally aware" to "fully localized" and what each level of support requires from the DS

2. RTL layout support

CSS logical properties vs. physical properties: how to structure component CSS for bidirectional support
Layout mirroring: which components mirror in RTL and which do not (and why)
Icon directionality: which icons are directional and need RTL variants
Figma for RTL: how to design and organize RTL variants in a component library
Testing RTL: tools and approaches for validating RTL layout

3. Typography for international content

Type scale considerations for languages with longer average word length (German, Finnish, etc.) — text expansion budgets
Non-Latin script support: Arabic, Hebrew, CJK (Chinese/Japanese/Korean), Devanagari — how font selection and line-height conventions need to adapt
Variable fonts and their role in multi-script typography
System font stacks for international scripts when brand fonts don't support the script
Font loading strategy for multi-script deployments

4. Token architecture for locale-specific values

Whether and how to encode locale-specific design decisions in a token system
Spacing and density adjustments for scripts with different character density
Color and cultural meaning: how DS documentation handles color conventions that vary by market
Date, time, and number formatting: where thDS concern vs. an application concern

5. Component-level i18n considerations

Components that are particularly sensitive to text expansion (buttons, labels, navigation items, badges)
Form components for international input: date pickers, phone number fields, address forms
Number, currency, and date display components — how to design for locale-agnostic structure
Navigation patterns for RTL: how common patterns (breadcrumbs, tabs, steppers) should behave

6. Figma workflow for multi-locale design

How to manage RTL and LTR variants in Figma component libraries without doubling maintenance burden
Figma's current RTL support and its limitations
Variable-based approaches to locale switching in Figma

7. Implementation and handoff

How the DS communicates i18n requirements to consuming teams
The boundary between DS responsibility and application responsibility for i18n
CSS logical properties as the current best practice for directional layouts — browser support, adoption status

Output format: Structured markdown. Where the field has established consensus (CSS logical properties for RTL, text expansion budgets), state it clearly. Where decisions are context-dependent, provide decision frameworks. Flag areas where DS tools (Figma, Style Dictionary, etc.) have known limitations for i18n support. Include references to primary sources (W3C internationalization, MDN, platform HIG i18n guidance, practitioner case studies).
