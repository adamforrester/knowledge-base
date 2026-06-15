# Glossary

Vault-specific and practice-adjacent vocabulary. Common DS terms (token, component, variant) are assumed and not defined here. People and project names are not in this glossary; they appear in provenance footers and are searchable directly. Where a term is most fully developed in a particular file, the file is linked.

---

## A

**ACR (Accessibility Conformance Report)** — Public artifact stating a system's accessibility conformance, based on the VPAT template. The procurement-grade version of an "accessibility promise." (See 14-accessibility.)

**`.ai.json`** — Internal-tier component metadata schema from the practice's *AI-Compatible Design Systems* doc (Feb 2025). Per-component structured data including `component_id`, `primary_purpose`, `when_to_use`, `avoid_when`, slot contracts, and accessibility metadata. The practice's instantiation of components-as-data. (See 03-component-library, 15-ai-in-ds.)

**APCA (Accessible Perceptual Contrast Algorithm)** — Perceptual contrast model that more accurately predicts readability than WCAG 2.x's relative-luminance ratio. Candidate for WCAG 3; not yet a compliance standard as of early 2026. Use as internal target; cite WCAG 2.2 for compliance. In token validation pipelines, the discipline is to **block on WCAG failures and warn on APCA failures** — regulatory floor plus readability signal. (See 14-accessibility, 24-tokens-at-scale, 31-color-systems.)

**APG (ARIA Authoring Practices Guide)** — W3C's canonical pattern catalog for composite widgets (combobox, menu, tabs, listbox, dialog, treegrid, etc.). Components implementing composite patterns should conform to APG. (See 14-accessibility.)

**Annotation contract** — Practice term for the structured accessibility specification designers fill in for each component in Figma so engineers can implement faithfully — name, role, state, value, focus behaviour, scaling behaviour, system-preference responses, gesture alternatives, live-region intent. The artefact that closes the inference gap between visual design and accessibility implementation. (See 17-accessibility-annotation-contract.)

**Atomic Design** — Brad Frost's mental-model framing (atoms / molecules / organisms / templates / pages). The practice treats this as a *mental model, not a folder structure*. (See 03-component-library.)

---

## B

**Bidi (bidirectional text)** — Mixed-direction text (Latin URL inside Arabic paragraph). The Unicode Bidi Algorithm (UAX #9) handles ordering; `<bdi>`, `dir="ltr"`, and `unicode-bidi: isolate` are the practical CSS/HTML controls. (See 13-internationalization-and-rtl.)

**Brand version pinning** — A brand in a multi-brand portfolio explicitly pinning its semantic layer to a specific version of the Global Foundations primitives, while other brands track latest. Enables the portfolio to move forward without forcing an unreviewed change onto a sensitive brand. "Federated computational governance" — local autonomy within global constraints. (See 24-tokens-at-scale.)

**Block / Area / Slot / Substitution** — Core composition primitives from the UIC series. With *Lockup* and *Extension* added, these form the practice's composition vocabulary. (See 03-component-library.)

---

## C

**Code Connect** — Figma feature linking design components to production code. When set up, Dev Mode shows the actual code snippet from the consuming repo instead of generic CSS. The substrate that lets AI generation reference real component imports. (See 12-figma-practice, 15-ai-in-ds.)

**Components-as-data** — Curtis's POV (Sep 2025) that a component is structured data (anatomy, props, default, variants), and Figma + code + docs are *outputs* generated from that data. The architectural prerequisite for reliable AI-driven DS work. (See 03-component-library, 15-ai-in-ds.)

**Composite token** — A token holding multiple values as a unit (e.g., a shadow as `[x, y, blur, spread, color]` rather than five separate tokens). Stable in DTCG 2025.10 for typography, shadow, border, and transition. Tools support composites but most fail to faithfully preserve property-level aliases on round-trip (sub-properties that should be aliases export as literals). The practitioner discipline: **carry composites as the source-of-truth representation; flatten at the build pipeline into platform-specific atomic outputs** that runtime consumes. (See 22-token-architecture-extensions, 12-figma-practice, 23-typography-tokenisation.)

**Computed / relational token** — A token whose value is derived from other tokens via an expression (`{spacing-base} * 1.5`; modular-scale formulae). Not part of the DTCG stable spec; implemented by Tokens Studio's math syntax and Style Dictionary v4 preprocessors. The convergent discipline: **compute at authoring time, ship literals at runtime.** Expression resolution is a build-time artefact; the runtime artefact is the literal value. (See 22-token-architecture-extensions.)

**Cascade Report** — Generated CI artefact for primitive-tier token changes listing every brand and every component affected. Prevents the "we didn't realise this would change Brand Q" failure at multi-brand portfolio scale. Practice deliverable on portfolio engagements past three brands. (See 24-tokens-at-scale.)

**Configure-and-Compose** — Practice framing for component flexibility: components should be both configurable (props handle the common cases) and composable (slots handle the uncommon ones). Workshop empirical data: ~100% success on Configure, ~80% on Compose-1, ~50% on Compose-2. (See 03-component-library.)

---

## D

**DTCG (Design Tokens Community Group, W3C)** — The W3C community group defining the standard JSON format for design tokens. The Format Module reached its first stable version (**2025.10**) on **28 October 2025** (`designtokens.org/tr/2025.10/format/`). The stable spec covers file shape, the `$`-prefixed properties (`$value` / `$type` / `$description` / `$extensions`), the terminal-node rule, the `$type` allowlist, and alias resolution. It deliberately omits modes/theming, math, conditional values, and deprecation metadata — those live in `$extensions` until the Resolver Module stabilises. Treat DTCG as an interchange format, not an architecture format. (See 02-design-foundations, 22-token-architecture-extensions.)

**Dynamic Type** — iOS's system-wide text-scaling mechanism. Semantic text styles (`body`, `headline`, `caption1`, etc.) scale according to the user's accessibility setting, including the larger AX1–AX5 sizes. SwiftUI exposes the current size via `@Environment(\.dynamicTypeSize)`; UIKit via `traitCollection.preferredContentSizeCategory`. Custom fonts require explicit `UIFontMetrics` or `.relativeTo` declaration to participate. The iOS equivalent of Android's `fontScale`. (See 16-mobile-accessibility-implementation, 11-mobile-and-cross-platform.)

---

## E

**EAA (European Accessibility Act)** — EU regulatory framework requiring digital accessibility for products and services sold in the EU. Enforceable since June 28, 2025. Materially raises the regulatory floor for EU-facing consumer products. (See 14-accessibility.)

**Embedded handoff** — Practice operating model: engineering joins from Discovery, components ship into the consuming codebase as they complete (not at the end). Differentiates from consultancies that ship a Figma file and walk away. (See 00-principles-and-philosophy, 06-pilot-and-implementation.)

**EN 301 549** — EU's harmonised technical standard for accessibility, basis of EAA technical conformance, references WCAG 2.x. (See 14-accessibility.)

**Expression token** — A Figma Variable with conditional or computed logic (e.g., `if(is-dark, #FFF, #111)`). Reported as a 2026 capability; verify current Figma docs before recommending. (See 12-figma-practice, 15-ai-in-ds.)

---

## F

**Foundations Model** — Andrew Couldwell's framing (*Laying the Foundations*, 2019). The practice uses it for the foundation tokens layer beneath components and patterns. (See 02-design-foundations.)

**Fluid type** — Typography whose font-size scales smoothly across viewport (or container) sizes via CSS `clamp(min, preferred, max)`. The 2026 default for marketing-tier surfaces. The non-negotiable accessibility rule: the `preferred` value must include a `rem` component, never `vw` alone, or the type fails WCAG 1.4.4 under user-zoom. Encode tokens as primitive triplets (min / preferred / max), not single `clamp()` strings, for cross-platform utility. (See 23-typography-tokenisation.)

**Focus return** — Practice term for the contract that accessibility focus returns to the triggering element when a modal, sheet, dropdown, or overlay dismisses. Not automatic in any mobile framework — Flutter and React Native miss it by default on iOS; SwiftUI is reliable in iOS 17+ for system sheets, manual otherwise; Compose reliable in Material 3 1.3+; UIKit requires explicit notification posting. Treated as non-optional in the design system's modal primitives. (See 16-mobile-accessibility-implementation, 17-accessibility-annotation-contract.)

**Four-layer AI stack** — Internal practice POV from *AI-Compatible Design Systems* (Feb 2025). The architecture layers an AI agent needs to engage with a DS reliably. (See 02-design-foundations, 05-development-support, 15-ai-in-ds.)

**Full Keyboard Access (FKA)** — iOS system feature allowing full UI navigation via Tab and arrow keys on hardware keyboards (Bluetooth, iPad Smart Keyboard, Magic Keyboard). Distinct from VoiceOver focus. Long-standing gap in Flutter (issue #76497, blocked iOS WCAG 2.1.1 conformance for years) finally resolved in engine PRs landed early 2025. Confirm Flutter version includes FKA fixes before claiming iOS keyboard conformance. (See 16-mobile-accessibility-implementation.)

---

## G

**Generative Token pattern** — Multi-brand portfolio architecture in which a brand's full semantic layer is derived mechanically from 5–10 core primitives (a primary color, neutral hue, typeface, radius, density step) via standardised computation (OKLCH lightness math, contrast-pinned palettes, density-aware spacing). Mature systems doing this report ~10% per-brand onboarding cost relative to the first brand. Practice has not yet shipped the tooling as a default; opened as gap §1.20 in 09. (See 24-tokens-at-scale.)

**Group / GroupItem** — Component pattern from the UIC series for parent–child composition where the parent owns layout and styling and children are content slots. (See 03-component-library.)

---

## H

**Headless UI** — Architectural pattern (Tailwind Labs' Headless UI, Radix UI, React Aria): functionality (focus management, keyboard nav, ARIA) encapsulated in unstyled components; styling applied by the consumer. Mangialardi's recommendation for cross-framework systems. Counter-pattern to opinionated libraries like Material UI. (See 05-development-support.)

**Hierarchical Component Model** — Internal practice framing for organizing components by purpose and semantic role rather than visual category. (See 03-component-library.)

**Hybrid Variable Mode Model (density)** — The convergent density encoding: discrete sets of tokens for each density step (`spacing/md = 8 / 12 / 16` for Compact / Comfortable / Spacious), with the values *generated from a multiplier at authoring time and committed as literals*. Combines the precision of discrete sets with the consistency of a multiplier-derived scale. Density is a mode dimension at runtime; values are hand-tunable in source. (See 22-token-architecture-extensions.)

---

## I

**ICU MessageFormat** — Unicode/ICU standard for parameterized strings supporting pluralization, gender, and grammatical cases across locales. The replacement for string concatenation in i18n. (See 13-internationalization-and-rtl.)

**Influence Map** — Mall's Discovery artifact (90 Days Activity #3): green/yellow/red on supportive/undecided/opposed; thick/thin arrows on relational influence. The most useful single Discovery deliverable in the external corpus. (See 01-discovery-and-strategy.)

**Intl.* (JavaScript)** — The JS API for locale-aware formatting (`Intl.NumberFormat`, `Intl.DateTimeFormat`, `Intl.PluralRules`). The boundary the DS draws: the application uses `Intl.*` to produce formatted strings; DS components display them. (See 13-internationalization-and-rtl.)

**INP (Interaction to Next Paint)** — Core Web Vital that replaced FID in March 2024. Measures the latency between a user interaction (click, keypress, tap) and the next paint. Motion that runs on the main thread inflates INP; motion on the compositor (CSS transitions on transform/opacity, WAAPI, Motion v12) does not. The 2026 motion-performance discipline is "contribute zero ms to the INP budget." (See 19-motion-implementation-web, 18-motion-foundations.)

**Informational vs. vestibular motion** — The 2025–2026 refinement to blanket reduce-motion treatment. Vestibular triggers (large-scale translation, parallax, 3D rotation, scale) should be replaced with a cross-fade for users who request reduced motion. Informational motion (short fades, focus-state transitions, progress indicators) can be preserved unchanged or at reduced amplitude. Encoded as per-token reduce-motion variants, not a global override. (See 18-motion-foundations, 14-accessibility.)

---

## L

**Levers and dials** — Yesenia Perez-Cruz framing for system flexibility: levers are big choices (variant, density), dials are fine-grained (token overrides). (See 02-design-foundations.)

**Lift pattern (dark-mode elevation)** — Material 3-popularised pattern for signalling elevation in dark mode: instead of a drop shadow (invisible against a dark surface), the *surface itself* is incrementally lightened (white overlay or upward lightness shift) to simulate proximity to a light source. The semantic implication: a `color/surface/raised` token in dark mode resolves to a lighter primitive, and elevation tokens map to a lighter background rather than a shadow. (See 31-color-systems.)

**Logical properties** — CSS properties that resolve to physical sides based on the document's writing mode and direction (`margin-inline-start`, `padding-inline-end`, `text-align: start`). The 2026 default for bidirectional layout. (See 13-internationalization-and-rtl.)

**Lockup** — Composition primitive: a fixed arrangement of multiple components treated as a unit (e.g., logo + tagline). (See 03-component-library.)

**`linear()` easing** — CSS easing function (Baseline 2024) that takes a list of stops and interpolates between them. By baking a spring physics curve into the list at build time, springs become a pure-CSS animation that runs on the compositor thread — zero main-thread cost. The implementation layer for web spring tokens. Generators like CSS Spring Easing Generator (csstools.github.io) produce the string from physical parameters. (See 19-motion-implementation-web.)

---

## M

**MCP (Model Context Protocol)** — Anthropic standard for connecting AI applications to external data sources via a server-and-tool-call protocol. Used in DS work to expose Figma context (Figma Dev Mode MCP), production code (Code Connect via MCP), and DS metadata (custom DS MCP servers) to AI coding assistants. (See 12-figma-practice, 15-ai-in-ds.)

**MCP-first vs. screenshot-first** — Practice POV on design-to-code AI: MCP-first gives the agent structured DS context and produces system-compliant code; screenshot-first infers from pixels and produces "AI slop." The architectural choice that determines whether AI generation is production-acceptable. (See 15-ai-in-ds.)

**Motion token (composite)** — A single named token bundling duration, easing (or spring), and the properties animated as a unit. The token shape that lets components and AI coding agents reference a complete motion contract by name (e.g. `motion/modal/enter`) rather than composing primitives. The layer at which AI-generated motion converges on a system's identity. (See 18-motion-foundations, 19-motion-implementation-web, 21-motion-spec-and-handoff.)

**Modular scale** — A typography (or spacing) scale derived from a base value and a fixed ratio. Canonical ratios include Minor Second (1.067), Minor Third (1.200), Major Third (1.250), Perfect Fourth (1.333), Perfect Fifth (1.500), Golden Ratio (1.618). The 2026 practitioner pattern is the **display pivot**: one ratio for body and metadata (typically 1.200), a larger ratio for display headlines (typically 1.414 or 1.500). The split is encoded in tokens as `scale-ratio-text` and `scale-ratio-display`. (See 23-typography-tokenisation.)

**Mode multiplication problem** — The exponential cost of multiple theming dimensions on a single collection (3 brands × 2 themes × 3 densities = 18 modes). Architectural fix: **one mode dimension per collection.** Color themes in the color collection; brand in the brand collection; density in the spacing-and-sizing collection. Cost stays additive instead of multiplicative. (See 12-figma-practice, 22-token-architecture-extensions.)

---

## N

**North Star (Mall / Watkins)** — Discovery artifact mapping the *organization's* mission, network, strategy, and vision. Mall's pointed instruction: write the company's North Star, not the design system's. The system aligns to the org, not the other way around. (See 01-discovery-and-strategy.)

**Noto** — Google's universal-coverage font family ("no tofu" project) covering virtually every Unicode script. The default fallback in multi-script font stacks. (See 13-internationalization-and-rtl.)

---

## O

**`on-X` token (forced-foreground luminance flip)** — A semantic foreground token paired with a background token (`on-primary` paired with `action/primary`) whose value is mathematically computed to flip between black and white depending on the luminance of the swapped primitive. The load-bearing technique for keeping `color/action/primary` and its foreground both contrast-compliant when the underlying primitive swaps under multi-brand theming. The semantic-layer counterpart to the contrast-tier-named-step rule at the primitive layer. (See 31-color-systems, 24-tokens-at-scale.)

**OKLCH** — Perceptually-uniform color space (Lightness, Chroma, Hue) that the field has converged on as the default for ramp authoring 2024–2026. Native CSS function (`oklch()`); ships in stable Safari/Chrome/Firefox since 2023. Distinct from HCT (Material 3's CAM16-based tonal model) and from the legacy HSL space. A color *space*, not a *gamut* — describes coordinates outside any renderable display, requiring gamut-mapping for sRGB/P3 fallbacks. (See 31-color-systems.)

**Opinionated library** — Architectural pattern (Material UI as canonical example): functionality and styling tightly coupled. Faster to start with, harder to brand-extend. Counter-pattern to Headless UI. (See 05-development-support.)

**Overlay (accessibility overlay)** — Third-party scripts that promise automated accessibility compliance via JavaScript injection. Increasingly the target of accessibility lawsuits because they conflict with assistive technologies and don't address structural issues. The practice's position: not a substitute for built-in accessibility. (See 14-accessibility.)

---

## P

**Pair tokens** — Color tokens that encode contrast as a property of the foreground/background *pair* (e.g., `color/text/on-surface-primary` validated at 4.5:1 against `color/surface/primary`). The token-layer architecture that makes contrast compliance enforceable at build time. Adobe Spectrum's pattern, generalized. (See 14-accessibility.)

**Pantry vs. cookbook** — Yesenia Perez-Cruz framing: "Your design system is your pantry, not your cookbook." Components are ingredients; products are the recipes that compose them. (See 03-component-library.)

**Phase model** — The vault's numbering reflects an engagement phase model: Discovery (01) → Foundations (02) → Components (03) → Documentation (04) → Dev Support (05) → Pilot (06) → Governance (07) → Maintenance (08). (See CLAUDE.md.)

**Pseudo-localization** — Test technique replacing strings with elongated, accented, bracketed text (`[Ĥéééļļļööö]`) to surface hardcoded strings and layout fragility. Bidi pseudo-locales also test direction. The cheapest layout-validation tool i18n provides. (See 13-internationalization-and-rtl.)

**Productive vs. expressive motion** — IBM Carbon's split between motion of utility (short, calm, disposable — buttons, panel opens, sheets) and motion of brand (longer, deliberate, meant to be noticed — onboarding, hero moments, success states). The split is load-bearing because the same easing curve cannot do both: productive curves applied to expressive moments feel mean; expressive curves applied to buttons feel broken. A mature motion system ships two parallel token sets. (See 18-motion-foundations.)

---

## R

**RACI (Responsible / Accountable / Consulted / Informed)** — Stakeholder-mapping convention for clarifying who does what in a workflow (contribution, governance, escalation). Useful when client orgs already operate in those terms. (See 12-figma-practice, 07-governance-and-adoption.)

**Rotor (VoiceOver)** — iOS screen-reader interaction menu, accessed by twisting two fingers, that exposes custom accessibility actions, headings, links, and form controls as navigable lists. The Android equivalent is TalkBack's "local context menu" (swipe up then right). The mechanism by which screen-reader users invoke gesture alternatives — swipe-to-delete becomes a "Delete" action in the rotor. The annotation contract's gesture-alternative labels are what appears here. (See 16-mobile-accessibility-implementation, 17-accessibility-annotation-contract.)

**Roving tabindex** — Keyboard pattern for composite widgets (tabs, menus, toolbars): only one element of the composite is in the page tab order at a time; arrow keys navigate within. Counter-pattern to `aria-activedescendant`. (See 14-accessibility.)

**Rule of three** — Mall's heuristic for promoting patterns into the system: three independent uses justify systematization. (See 03-component-library.)

**Rive** — Interactive-motion runtime and authoring tool. Designers build a state machine in the Rive editor; engineers integrate the runtime (`.riv` file plus state-machine inputs wired to app state). The 2024–2026 successor to Lottie for any motion that needs to respond to app state — animated icons, stateful controls, motion-as-component. Trade-off: ~200KB WASM runtime on web (smaller relative cost on mobile). The 2026 decision rule: Rive for interactive motion, Lottie for deterministic playback. (See 19-motion-implementation-web, 20-motion-implementation-mobile, 21-motion-spec-and-handoff.)

---

## S

**Six rationales** — Practice framing for composition decisions: Expression / Efficiency / Delegation / Autonomy / Quality / Maintenance. Used to justify whether a component should be configurable, composable, or both. (See 03-component-library.)

**Smart Invert** — iOS accessibility feature that inverts the system UI colours while attempting to leave images, video, and apps using dark styles untouched. Classic Invert inverts everything. No public API distinguishes them, so the design system treats Smart Invert as the assumed case: photos and illustrative imagery must be excluded via `accessibilityIgnoresInvertColors`. The default-to-exclude policy for media is required by the design system. (See 16-mobile-accessibility-implementation, 17-accessibility-annotation-contract.)

**Six Signs** — VML library Section 5. Practice diagnostic for opportunity recognition (when a client should invest in a design system). Strong for first executive conversations; less precise as a maturity instrument. (See 01-discovery-and-strategy.)

**Section 508** — US federal procurement accessibility standard, references WCAG. Used as a regulatory floor in regulated-industry engagements. (See 14-accessibility.)

**Specs CLI** — Curtis's tool (github.com/DirectedEdges/specs) operationalizing components-as-data. Generates structured component specs from Figma files and packages design intent for developer/AI consumption. (See 03-component-library, 15-ai-in-ds.)

**Style Dictionary** — Token transformation tool by Amazon. Canonical pipeline component: takes DTCG JSON and produces platform-specific outputs (CSS, SCSS, Swift, Kotlin, Dart). Mangialardi spent 60 pages on it. **Style Dictionary v4** (late 2024) added native DTCG 2025.10 support, async transforms and preprocessors, and improved composite-type handling. The load-bearing engine in the practice's build pipeline. (See 02-design-foundations, 22-token-architecture-extensions, 24-tokens-at-scale.)

**Semver for tokens** — Treating tokens as a versioned API. Rename or delete is a major bump; new token or new mode is a minor bump; value change is a patch bump — **with one adapted rule: a `$value` change that breaks a contrast pair in any brand × theme × density combination is a major bump, even when the token's shape is unchanged.** Preserves consumer accessibility-conformance expectations under minor-version updates. (See 24-tokens-at-scale.)

**Shared element transition** — The same visual element persisting across a route change or major state transition (a card on a list page becoming the hero on a detail page). Per-framework primitives all stabilised by 2024: SwiftUI's `matchedGeometryEffect`, Compose's `SharedTransitionLayout` (1.7.0, July 2024), Flutter's `Hero`, React Native's Reanimated `sharedTransitionTag`, and the web's View Transitions API. Named at the system layer (e.g. `SharedHero`); spelled per platform. (See 18-motion-foundations, 19-motion-implementation-web, 20-motion-implementation-mobile.)

**Spring token (perceptual)** — A motion token named by perceptual outcome (`spring/snappy`, `spring/gentle`, `spring/bouncy`) rather than by physical parameters. The same perceptual outcome requires different parameters on each framework: SwiftUI uses `duration`/`bounce` (iOS 17+), Compose uses `dampingRatio`/`stiffness`, Flutter uses `mass`/`stiffness`/`damping`, Reanimated supports either. The token name is the contract; the parameters are the per-platform implementation. Cross-platform calibration (videos confirming the perceptual outcome matches) is a practice deliverable. (See 18-motion-foundations, 20-motion-implementation-mobile.)

**Substitution** — Composition primitive: replacing one component with another at the same slot position (e.g., swapping an `Avatar` for a custom element). (See 03-component-library.)

---

## T

**Theming dimensions (Curtis's seven)** — Curtis's catalog of dimensions a system may need to theme across, in ascending cost: Responsive, Light/Dark, Multi-brand, Campaigns, Design Generations, White Label, Density. (See 02-design-foundations.)

**Tokens Studio** — Figma plugin for token authoring, transformation, and DTCG export. Mature; widely used. Native Figma Variables have absorbed the basic authoring case; Tokens Studio remains the right tool for math expressions, multi-collection brand inheritance, and full DTCG composite-type fidelity. The 2026 position: advanced management suite, not the bridge it was three years ago. (See 02-design-foundations, 12-figma-practice, 22-token-architecture-extensions.)

**`text-box-trim`** — CSS property (with longhand `text-box-edge`) that removes the leading "slug" above and below text, enabling cap-height or x-height alignment. The web platform's equivalent to iOS `leading-trim` and Compose `LineHeightStyle.Trim`. **Limited Availability as of mid-May 2026** — shipped in Chrome 133+, Safari 18.2+, Edge 133+; Firefox has implemented but keeps it disabled by default through at least Firefox 149 (caniuse / MDN verified). Cap-height alignment as a system-level feature does not close until Firefox enables by default. (See 23-typography-tokenisation, 09-gaps-and-open-questions §1.21.)

**Three-layer composite scale** — The convergent 2026 pattern for tokenising scales (typography, spacing): a mathematical primitive layer (modular ratio applied to a base, output as literals via Tokens Studio or Style Dictionary); an internal numeric layer (`size-100`, `200`) for system-internal reference; a semantic surface layer (`size/md`, `font-size/body`) for consumer authoring. Each layer serves a different audience. (See 22-token-architecture-extensions, 23-typography-tokenisation.)

**Terminal-node rule (DTCG)** — Any object containing a `$value` property is definitively a design token; the same object cannot simultaneously serve as a group or parent to other tokens. Eliminates the ambiguity that plagued earlier token sets where a color name held both a base value and child variants. Settled in DTCG 2025.10. (See 22-token-architecture-extensions.)

---

## U

**UIC series** — The practice's *UI Components* series (Nov 2024, six docs covering Naming/Metadata, Anatomy, Properties, Layout/Spacing, Composition). The most operationally specific component-building methodology any consultancy publishes internally. Source of the anatomy five-questions, properties six-questions, layout patterns, composition primitives, and configure-and-compose framing. (See 03-component-library.)

---

## V

**View Transitions API** — Browser API (same-document Baseline 2024; cross-document shipping in Chromium and Safari 18.2+ as of May 2026; Firefox 144+ same-document) that snapshots before/after states of the DOM and interpolates between them. Browser-managed shared-element and route transitions. Key gotcha: does *not* automatically respect `prefers-reduced-motion` — DS must wrap calls in a reduce-motion check (`safeViewTransition` helper). (See 19-motion-implementation-web, 14-accessibility.)

**Variable font axes** — Registered axes controlling continuous font variation within a single file: `wght` (weight, 100–1000), `wdth` (width), `opsz` (optical size — the under-used axis), `slnt` (slant), `ital` (italic). Custom axes (per-typeface) like `GRAD` (grade) or `XHGT` (x-height) exist on some fonts. The architectural answer to the continuous-range / discrete-token tension is the **named-instance ladder**: the token system exposes a finite semantic ladder (`weight/regular` → 450, `weight/medium` → 550) over the continuous axis. `font-optical-sizing: auto` is the recommended default for any system using a font with an `opsz` axis. (See 23-typography-tokenisation.)

**Validation fatigue** — The failure mode in which a CI pipeline blocks too many PRs for minor concerns (naming convention drift, dead tokens, relationship-rule warnings), and engineers learn to ignore the warnings or paper over with override flags. Defeats the purpose of the validation infrastructure. The discipline: **block only on errors (structural and contrast); surface warnings to a dashboard, not the build.** (See 24-tokens-at-scale.)

**VPAT (Voluntary Product Accessibility Template)** — Standard template for documenting accessibility conformance against WCAG/Section 508. Source format for the ACR (the public artifact). (See 14-accessibility.)

---

## W

**WCAG 2.2** — Web Content Accessibility Guidelines, current stable version as of early 2026. Adds Focus Appearance (2.4.11), Target Size Minimum (2.5.8), and other criteria over 2.1. Practice baseline for product-led work. (See 14-accessibility.)

**WCAG 3** — In working draft as of early 2026. Will likely incorporate APCA. Not yet a compliance standard. (See 14-accessibility.)

---

## Z

**Zeroheight** — Documentation platform that bidirectionally syncs with Figma. Common docs surface for designers; complements Storybook on the engineering side. (See 04-documentation, 12-figma-practice.)

---

*This glossary is incremental — add terms as new files introduce vocabulary. Don't define common DS terms; assume the reader.*
