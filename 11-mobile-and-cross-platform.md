---
type: practice-area
title: Mobile and Cross-Platform
description: iOS, Android, Flutter. Tokens as the shared layer; native vs. custom component decisions; platform-specific token delivery.
tags: [extension, mobile, ios, android, flutter, cross-platform]
timestamp: 2026-05-16
---

# 11 — Mobile and Cross-Platform Design Systems

> Mobile design systems are not a mobile version of a web design system. They are a parallel rendering target for the same design decisions — which means the token architecture is shared, but the component implementations are not. Understanding that distinction early determines whether a mobile DS engagement is scoped correctly or not.

---

## How this is different from web DS work

Web DS work assumes a browser as the rendering environment — HTML, CSS, and JavaScript. Mobile changes this fundamentally. Native iOS renders via UIKit or SwiftUI. Android renders via Views or Jetpack Compose. Flutter renders its own widget tree, bypassing native UI entirely. None of these environments consume CSS.

The implication: **the design system cannot deliver the same artifact to all platforms.** What can be shared is design decisions — color, spacing, typography scales, border radius, elevation — expressed as tokens. What cannot be shared is component implementation. Each platform requires its own component layer, built against that platform's paradigm.

The practical question in every mobile DS engagement is: where does the shared layer end and the platform-specific layer begin? Getting that line right is the difference between a DS that scales across platforms and a set of parallel libraries that drift apart over time.

---

## VML context

Mobile DS work at VML most commonly arrives as:

1. **Mobile-first or mobile-only.** The engagement is building for iOS and/or Android (and increasingly Flutter) with no concurrent web work. The DS is built to serve the mobile product and may be extended to web later.
2. **Mobile alongside a web project.** Less common, and rarely concurrent — typically the DS serves one platform first, then is extended to the other. The extension is its own scoped effort, not an automatic inclusion.

**Flutter is growing.** The single-codebase advantage is increasingly compelling to clients. Wendy's is a VML reference example of Flutter at scale: a Material-based Flutter app customized extensively to feel on-brand, with its own challenges around Material token vs. custom token conflicts. Expect Flutter engagements to increase.

**The team is typically native.** Most mobile DS work at VML has been native Swift (iOS) and Kotlin/Compose (Android), with Flutter becoming more common. React Native is less frequent.

---

## Token architecture as the shared layer

Tokens are the mechanism that makes a single design system serve multiple platforms. W3C DTCG-compliant token JSON is platform-agnostic by design. Style Dictionary's platform transforms convert that JSON into platform-specific outputs:

| Platform | Style Dictionary output | Consumed as |
|---|---|---|
| Web | CSS custom properties, SCSS variables | Imported in stylesheet |
| iOS (UIKit/SwiftUI) | Swift enums, UIColor extensions, CGFloat constants | Imported in Swift package |
| Android (XML) | `colors.xml`, `dimens.xml` | Android resource references |
| Android (Compose) | Kotlin objects | Imported in Compose theme |
| Flutter | Dart constants | Imported in theme file |
| Figma | Variables (via Tokens Studio or native Variables) | Applied in design file |

**The token pipeline is the highest-leverage investment in a multi-platform DS.** Get the architecture right once — primitive tokens → semantic tokens → component tokens — and every platform consumes from the same source of truth. Skip it or defer it, and each platform builds its own values independently and they drift.

**Figma as the design source across platforms.** Figma Variables feed all platforms from a single library when the token architecture is correct. Tokens Studio can push to the token JSON; Style Dictionary processes it from there. This is the design-to-development pipeline for multi-platform work — not perfect, but the most mature path currently available.

**Motion as a cross-platform token category.** Motion tokens (duration, easing, springs, composite motion tokens) sit in the same token pipeline as color and space. The architectural treatment lives in 18-motion-foundations; the per-framework spelling — SwiftUI's perceptual springs, Compose's classical springs, Flutter's `SpringDescription`, Reanimated's worklets, shared element transitions, reduce-motion APIs — lives in 20-motion-implementation-mobile. The cross-platform calibration problem (the same `spring/snappy` token must feel the same across all four frameworks) is the practical extension of this file's token-architecture argument into the motion layer.

---

## The native vs. custom component decision

This is the most common strategic conversation in a mobile DS engagement and almost always comes down to **budget, timeline, and customization requirements** — not a pure technical preference.

### Why native (Material, iOS UIKit/SwiftUI) wins under constraints

Using platform-native components — Material Design for Android and Flutter, UIKit/SwiftUI components for iOS — is faster and cheaper to build. Accessibility is largely handled by the platform. Interaction patterns match platform conventions, which benefits usability. The cost is customization: these components have limits on how far they can be pushed to feel on-brand.

This is the right default when:
- Timeline or budget is constrained (which is most engagements)
- The brand's visual language is compatible with material design conventions
- The client's team will maintain the app post-delivery and has platform-native development expertise

**The risk:** Customization limitations become real friction when the brand has strong opinions about visual language. Some brand decisions simply cannot be expressed within Material's theming constraints without fighting the framework. Surface these limits early — preferably in discovery, with a concrete component example.

### Why custom components are sometimes the right call

Fully custom components — built from first principles without a platform component as the base — give maximum visual fidelity to the brand. The tradeoff: significantly more time to build, significantly more to maintain, and accessibility must be implemented explicitly (nothing is inherited from the platform).

Custom makes sense when:
- The brand's visual language is genuinely incompatible with Material or UIKit conventions
- The engagement has adequate timeline and budget
- There is a dedicated team that can maintain the components post-delivery
- The product has specific interaction patterns not supported by native components

**The Wendy's example:** The Flutter app was customized to the point that it no longer feels like Material UI. That level of customization is achievable in Flutter and delivers strong brand fidelity — but it comes with ongoing challenges, particularly around Flutter's expectation that Material tokens govern theming and the friction that creates when using a fully custom token system alongside Material's own theming layer.

### The hybrid reality

In practice, most mobile DS engagements are neither fully native nor fully custom. The typical approach:
- Use native components as the structural base (handling behavior, accessibility, interaction)
- Apply aggressive theming to override visual presentation (colors, typography, shape, spacing)
- Build fully custom only for components where native has no equivalent or where the brand requirement is irreconcilable with native theming

This is often the right answer but requires an explicit decision, documented as part of Discovery. Left implicit, the team makes component-by-component calls inconsistently and the DS accumulates a mix of approaches with no coherent rationale.

---

## Platform-specific considerations

### iOS (UIKit and SwiftUI)

UIKit is the older paradigm (imperative, view-based); SwiftUI is Apple's current direction (declarative, struct-based). New iOS work should default to SwiftUI unless the client's existing codebase is UIKit-based.

**Theming model:** SwiftUI has a richer theming story than UIKit. Environment values and the `.environment()` modifier allow token values to propagate through the view hierarchy cleanly — the closest iOS gets to CSS custom properties. Color assets in the Asset Catalog support light/dark mode variants and high contrast without code changes.

**Token delivery:** Style Dictionary outputs Swift enums or Color/Font extensions that are added to a Swift package or directly to the Xcode project. The consuming view applies `Color.brandPrimary` rather than a hex value — same semantic token model as web, Swift syntax.

**Customization limits:** iOS UIKit components (UIButton, UINavigationBar, UITabBar) have well-documented customization APIs. SwiftUI's ViewModifier system is more flexible. The practical ceiling: structural changes to native components (reorganizing internal layout, changing affordance geometry) are difficult or impossible. Visual overrides (color, typography, shape) are generally well-supported.

### Android (Views and Jetpack Compose)

Android has undergone the same paradigm shift as iOS — from View-based XML layouts to Jetpack Compose (declarative). New Android work should default to Compose unless the existing codebase requires View compatibility.

**Theming model:** Compose's Material theming is well-structured for DS integration: `MaterialTheme` wraps the composition tree and exposes `colors`, `typography`, and `shapes` as design token slots. Override the `MaterialTheme` with client-specific values and every component that consumes `MaterialTheme.colorScheme.primary` gets the brand color. This is the intended theming path and it works well for brand alignment within Material's structure.

**Token delivery:** Style Dictionary outputs Kotlin objects or data classes that plug into the Compose `MaterialTheme`. The token pipeline → Kotlin objects → `MaterialTheme(colorScheme = clientTokens.colorScheme)` is a clean, maintainable pattern.

**Customization limits:** Similar to iOS. Color, typography, shape, and spacing are highly customizable. Component structure — the spatial relationship between elements inside a Material component — is harder to override without building a replacement.

### Flutter

Flutter is its own rendering engine — it does not use native iOS or Android widgets. It draws everything itself using Skia/Impeller. This means visual output is pixel-identical across iOS and Android (an advantage) but also means no native accessibility affordances are inherited automatically (a consideration to scope explicitly).

**Flutter's Material preference:** Flutter's component library is built on Material Design. Most Flutter widgets are Material widgets. While Flutter can render without Material, the default toolkit, theming system, and documentation all assume Material. Going off-Material means building more from scratch.

**The Wendy's lesson:** You can customize Flutter's Material theme extensively — to the point that the app no longer reads as Material. This is achievable but creates ongoing tension:
- Flutter's theming is designed around Material's token structure (`colorScheme`, `textTheme`, `shapeTheme`). A fully custom token system running alongside Material's theme creates two sources of truth for styling decisions, which is a maintenance problem.
- Updates to Flutter and Material3 may reset or conflict with custom overrides, requiring periodic reconciliation.
- The recommended mitigation: use Material's token slots as the vehicle for custom values wherever possible (`ThemeData.colorScheme.primary = clientBrandPrimary`), rather than building a parallel theming system. Minimizes the surface area of conflict.

**Token delivery:** Style Dictionary outputs Dart constants that populate the Flutter `ThemeData`. The pattern: `ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: ClientTokens.brandPrimary))` for simpler cases; custom `ColorScheme` construction for full token control.

**Single codebase advantage — and its limits:** Flutter's pitch is one codebase for iOS, Android, and web. The web story is maturing but not yet strong for complex production apps. For mobile-only (iOS + Android), Flutter's single codebase is a genuine advantage and increasingly worth recommending over maintaining separate native codebases. Factor this into the platform recommendation during Discovery.

---

## Typography system

**VML's position:** Brand fonts for headlines and display. System fonts (or a neutral digital-first font) for body copy and UI text.

**The rationale:**
- Brand fonts at display sizes carry identity weight and render well at large point sizes
- Brand fonts at small body sizes frequently have legibility problems: optical sizing not optimized for 14–16pt screen rendering, missing hinting, file size overhead from loading the full font family
- System fonts (San Francisco on iOS, Roboto on Android, or a brand-approved neutral like Inter) are optimized for screen legibility at small sizes, load instantly, and respect accessibility settings including Dynamic Type

**The client conversation:** This position occasionally requires explanation — some clients interpret "use system fonts for body" as backing away from the brand. The reframe: system fonts at body sizes are invisible to users; what they notice is readability and comfort. Brand font weight is preserved where it matters (display, headlines, key CTAs) and not wasted where it doesn't.

**When to deviate:** If the client's brand font genuinely performs well at small sizes — good optical sizing, strong hinting, sufficient weights — there is no reason to push for system fonts. Evaluate with a real rendered test at 14–16pt on device, not in Figma. Most of the time the legibility problem becomes obvious immediately.

**Platform-specific type scales:**
- **iOS:** Apple's Human Interface Guidelines define a Dynamic Type scale. Semantic text styles (`headline`, `body`, `caption1`, etc.) scale with user accessibility settings. DS typography should map to these styles, not hardcode point sizes.
- **Android:** Material's type scale (`displayLarge` through `labelSmall`) follows the same principle. Map DS typography to Material type roles in the Compose `TextTheme`.
- **Flutter:** Same as Android Compose — map to `ThemeData.textTheme`.

The DS should define semantic type roles that map to platform type systems, not fixed point sizes. Fixed sizes break with accessibility settings and user preferences.

---

## Figma for multi-platform DS design

Figma is the consistent design tool across all mobile platforms at VML. A few principles for multi-platform use:

**One library, platform-specific components where needed.** Shared foundations (color tokens, type tokens, spacing) live in a single library. Components that are platform-specific (iOS nav bar, Android FAB, Flutter bottom sheet) live in platform-specific Figma component pages or separate libraries, but reference the same token variables.

**Figma Variables as the token bridge.** Figma Variables (2023+) allow tokens to be defined once and applied across all components. When the token architecture is correct, updating the brand primary color in Figma Variables propagates to every component on every platform page. This is the design-side equivalent of the Style Dictionary pipeline.

**Design for the target platform's conventions.** A component designed in Figma for iOS should use iOS interaction patterns, spacing conventions, and navigation paradigms. Do not copy-paste web components into a mobile frame and call it mobile design. Platform conventions exist for usability reasons; violating them creates user friction even when the visual design is good.

---

## Extending from web to mobile (or vice versa)

When the DS starts on one platform and is extended to another, the token layer is what enables the extension to be systematic rather than a re-build.

**If web DS was built with a good token foundation:** Extension to mobile means:
1. Running the existing token JSON through Style Dictionary's mobile platform transforms
2. Auditing the token set for mobile-specific gaps (elevation/shadow behaves differently on mobile; spacing may need a mobile-specific scale)
3. Building mobile-specific components that consume the shared token values

**If web DS was built without a token foundation (raw hex values, no semantic layer):** Extension to mobile is essentially a rebuild. There is no shared source of truth to translate. Budget for a token architecture pass before attempting the extension.

**The practical implication for scoping:** The extension is never free and is rarely as simple as clients expect. The question is not "can we use the web DS for mobile?" but "is the web DS architected in a way that supports multi-platform consumption?" Audit this in Discovery if an extension engagement is anticipated.

---

## Scoping considerations

**Discovery must address platform.** Which platforms? Native or cross-platform? Existing codebase? These questions change the architecture and the estimate. Native iOS + Android is two separate component libraries; Flutter is one. Factor this explicitly.

**Component count multiplies by platform.** A 20-component DS on web is a 20-component DS. A 20-component DS on iOS + Android native is 40 component implementations (or 20 in Flutter). Estimates must reflect this. The token layer is shared; the components are not.

**Accessibility scope on Flutter is explicit, not inherited.** Budget for explicit accessibility implementation on Flutter — screen reader support, focus management, semantic labels — in a way that iOS and Android native development does not require to the same degree, because native components carry these behaviors by default. (See 16-mobile-accessibility-implementation for the full framework-by-framework treatment — Flutter's semantics tree, Compose's mergeDescendants/clearAndSetSemantics, SwiftUI/UIKit traits and focus systems, React Native's prop divergence — and 17-accessibility-annotation-contract for what designers must specify in Figma to make that implementation faithful.)

**Font licensing for mobile.** Brand fonts on mobile require mobile-specific licenses in many cases. This is a client responsibility, but it should be raised early — missing font licenses have delayed launches. Raise it in Discovery.

**Dynamic Type / font scaling.** iOS and Android both support system-level font scaling for accessibility. DS typography must use semantic type styles (not fixed sizes) to support this. Scope the QA to include accessibility font size testing.

**The native vs. custom decision should be scoped as a Discovery output, not an assumption.** Entering a component build phase without a documented, agreed decision on this question creates scope creep. The decision belongs in the Discovery deliverable and should be explicit.

---

## Failure modes

- **No token architecture — parallel platform builds drift immediately.** Each platform hardcodes its own values. Brand color changes require updates in three places. Within two product cycles the platforms are visually inconsistent.
- **Web tokens translated to mobile without a mobile-specific audit.** Web spacing scales, shadow values, and type sizes often don't translate directly. A 4pt spacing unit that works on web may not map to mobile's 4dp grid correctly. Run a mobile-specific token audit before delivering mobile tokens.
- **Native component decision deferred and made per-component.** Half the component library is native, half is custom, with no coherent rationale. The result is inconsistent behavior, inconsistent accessibility, and a codebase that's hard to maintain.
- **Flutter Material conflicts from dual theming systems.** Custom token system built alongside Material's `ThemeData` rather than through it. Style conflicts emerge as Flutter updates or when Material3 migration is required.
- **Figma components designed at web scale.** Components designed at 1440px web conventions copied to mobile frames. Spacing, touch target sizes, and interaction patterns are wrong for mobile.
- **Brand font at all type sizes.** Legibility problems at body sizes accepted because "it's the brand font." Accessibility and readability sacrificed for brand consistency where it doesn't matter.
- **Font licensing not addressed.** Mobile font licenses assumed to be covered by web license. Launch delayed.
- **Accessibility scoped as a QA activity, not a design activity.** Screen reader behavior, focus order, and semantic labels are not designed — they are discovered in QA. Remediation at that stage is expensive.

---

## Tensions and open questions

1. **Flutter's growth vs. native expertise.** Flutter's single-codebase advantage is real and increasingly compelling. The question for VML is whether the team's native development expertise (Swift, Kotlin) is being matched by growing Flutter expertise, or whether Flutter engagements are stretching a team more comfortable with native. This is a staffing and capability question more than a technology question.

2. **How much Material customization is too much?** The Wendy's experience shows that deep Flutter/Material customization is achievable. The open question is where the maintenance cost of that customization becomes greater than the cost of building custom components that don't fight the framework. There is no universal answer; it depends on the client's investment in ongoing maintenance.

3. **Token tooling for mobile is less mature than for web.** Style Dictionary's mobile transforms work, but the end-to-end pipeline (Figma Variables → token JSON → Swift/Kotlin/Dart) has more friction than the web equivalent. Tokens Studio and the W3C DTCG format are the most reliable current path, but the tooling is still evolving. Budget for pipeline setup time accordingly.

4. **Multi-platform DS design in Figma.** Managing iOS, Android, and web in a single Figma library is achievable but complex. The right structure (one library with platform pages vs. separate libraries linked to a shared token library) depends on team size and how separately the platforms are designed. No single convention has emerged as standard.

5. **When does a mobile engagement warrant its own DS vs. a themed extension of an existing web DS?** The token layer is shareable; the components are platform-specific either way. The decision is really about whether the visual and interaction language is consistent enough across platforms to warrant a unified DS governance model. Clients with strong brand systems usually benefit from unified governance. Clients where web and mobile are built and maintained by separate teams often drift toward separate DS governance in practice regardless of what's intended.

---

*Provenance: Platform-specific token delivery (Style Dictionary transforms for Swift, Kotlin, Dart), Flutter theming architecture, native vs. custom component trade-offs, and typography system recommendations are original synthesis from VML practice experience. Specific Flutter Material customization patterns reflect lessons from the Wendy's app engagement. iOS Dynamic Type and Android TextTheme semantic type role guidance reflects Apple HCI and Material Design documentation. Mobile DS tooling maturity notes reflect the state of the ecosystem as of early 2026.*
