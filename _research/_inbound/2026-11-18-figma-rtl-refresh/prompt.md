You are refreshing one platform-state position in a design systems practice knowledge base: has Figma's right-to-left support changed since the position in `13-internationalization-and-rtl.md` (timestamp 2026-06-29)? The relevant sections are "Figma for RTL" and "Figma workflow for multi-locale design".

That position: Figma's RTL support is incomplete; bidi rendering can diverge from browsers; there are no logical properties; mode-based workarounds are partial; design LTR, prove RTL in code, don't make Figma the RTL authority.

Research, with current primary sources (Figma release notes, help center, Config announcements, the plugin API docs and changelog, and Figma's own blog), each claim dated and linked:

1. Text: RTL scripts (Arabic, Hebrew, Persian, Urdu), bidi and mixed-direction strings, paragraph direction controls, and font shaping. What changed in 2025–2026?
2. Layout: does auto layout have a direction or mirroring control, or logical start/end padding? Can a frame or variable mode flip direction? What about slots and nested instances?
3. Variables and modes: any direction-aware variable support, or patterns Figma now recommends.
4. Plugin API: anything a plugin can use to mirror a frame or set text direction (properties, methods, limits). This decides whether a "make an RTL copy" helper and an RTL specimen in component specs are feasible.
5. Dev Mode and Code Connect: how direction and logical properties reach code.
6. What leading design systems with RTL (Material, Fluent, Atlassian, Polaris, Carbon, and Arabic/Hebrew-market systems if documented) say they do in Figma today.

Deliverables: a research run per `_research/README.md`; a proposed update to file 13 if anything changed (or a statement that nothing material changed); and a feasibility read on two downstream ideas — an RTL specimen inside component specs, and a "make an RTL copy" helper for screen mock-ups — saying what would block each.

Mark anything you couldn't verify as unverified, and never guess a date or capability.
