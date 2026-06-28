# Responsive Type: How Mobile↔Desktop Sizes Are Actually Set

*Claude's run of the dual-agent brief. Researched 2026-06-28 against Utopia, IBM
Carbon source (`_styles.scss`/`_scale.scss`), Material 3, Apple HIG, Shopify
Polaris, WCAG, and practitioner sources. Validating/replacing a flat per-group
shrink factor (display 0.75, title 0.875, body 1.0) used to derive the `clamp()`
min (mobile) from the max (desktop) on a curated rem ladder. Confidence flags and
citations inline.*

## TL;DR — model recommendation

**The flat shrink factor is the wrong model.** No major fluid-type system uses a
single uniform scale-down. The field uses one of two patterns, and they agree on
the *shape*:

1. **Dual-scale (Utopia / canonical):** a *calmer* (smaller) modular ratio at the
   min viewport and a *punchier* (larger) ratio at the max viewport. The base/body
   size barely changes; the hierarchy **compresses on mobile** and the gap between
   mobile and desktop **grows with step height**. ([Utopia calculator](https://utopia.fyi/type/calculator/), [Smashing/Utopia](https://www.smashingmagazine.com/2021/04/designing-developing-fluid-type-space-scales/))
2. **Explicit per-step min/max (IBM Carbon):** body/UI is fixed; each fluid
   heading/display token names a small-breakpoint step and a large-breakpoint step,
   and **the bigger the role, the more scale steps it spans.** ([Carbon `_styles.scss`](https://github.com/carbon-design-system/carbon/blob/main/packages/type/scss/_styles.scss), [`_scale.scss`](https://github.com/carbon-design-system/carbon/blob/main/packages/type/scss/_scale.scss))

For a **curated (non-ratio) ladder**, the correct analog is a **size-dependent
rung drop**: small text drops 0 rungs (body/UI static), titles drop ~1 rung, and
display drops progressively *more* rungs as the desktop size climbs. A flat 0.75
factor is wrong because it shrinks a 96px hero and a 28px heading by the same
*proportion* — the opposite of what shipping systems do (they shrink big things by
*more*). Recomputing two full ratios is the "purest" approach but overkill for a
fixed curated ladder; the rung-drop table below reproduces the same behaviour.
**Confidence: high** on model shape; the exact rung-drop counts are a tunable
judgement call (flagged below).

---

## 1. Flat factor vs dual-scale vs rung-drop

A flat factor (`mobile = desktop × k`) keeps *ratios between steps constant* and
just moves the whole scale down. That is **not** how responsive type works in
practice. Utopia's premise is two different *type scales*: e.g. ratio 1.2 at the
small viewport and 1.25 at the large viewport. Because a larger ratio compounds,
the top of the scale pulls away far more than the bottom — so on mobile the
hierarchy is "calmer" and on desktop "punchier." The base size is nearly stable;
the spread between mobile and desktop is small for body and large for display.
([Utopia calculator defaults](https://utopia.fyi/type/calculator/); rationale: [Smashing/Utopia](https://www.smashingmagazine.com/2021/04/designing-developing-fluid-type-space-scales/)).

Practitioner consensus echoes this: *"Larger viewports benefit from more
exaggerated scales… without it [headings] lose impact, are less scannable, and
simply look a bit wrong"*; custom scales deliberately *"compress the middle range…
while expanding the top range for display typography"* ([Blake Crosley, Type Scales](https://blakecrosley.com/blog/typography-systems)).

**Conclusion:** the right model is *size-dependent* shrink, not uniform. For a
curated ladder, implement it as a rung drop that increases with desktop size.

---

## 2. Utopia's concrete defaults

From the live calculator ([utopia.fyi/type/calculator](https://utopia.fyi/type/calculator/), fetched 2026-06-28):

| Parameter | Value |
|---|---|
| Min viewport | **360px** |
| Max viewport | **1240px** |
| Min base font | **18px** |
| Max base font | **20px** |
| Min ratio | **1.2** (minor third) |
| Max ratio | **1.25** (major third) |

Resulting per-step mobile→desktop:

| Step | Min (mobile) | Max (desktop) | Mobile % of desktop |
|---|---|---|---|
| 0 (body) | 18.0px | 20.0px | **90%** |
| 1 | 21.6px | 25.0px | 86% |
| 2 (mid heading) | 25.9px | 31.3px | 83% |
| 3 | 31.1px | 39.1px | 80% |
| 4 | 37.3px | 48.8px | 76% |
| 5 (large display) | 44.8px | 61.0px | **73%** |

Body effectively stays ~16–20px; a large-display step lands ~73% on mobile — but
Utopia gets there by *compression*, so smaller headings sit at 80–90%, not 73%.
**Confidence: high** (primary source; version-dependent — June 2026 defaults;
Utopia has previously shipped 320/1140).

---

## 3. Real numbers from shipping systems

### IBM Carbon — fluid heading/display (explicit per-step min/max)
Scale steps ([`_scale.scss`](https://github.com/carbon-design-system/carbon/blob/main/packages/type/scss/_scale.scss)): step1=12, 2=14, 3=16, 4=18, 5=20, 6=24, 7=28, 8=32, 9=36, 10=40, 11=48, 12=56, 13=64, 14=72, 15=80, 16=92 … 23=176px. Fluid tokens ([`_styles.scss`](https://github.com/carbon-design-system/carbon/blob/main/packages/type/scss/_styles.scss)):

| Token | Mobile (sm/320) | Desktop (max/1584) | Mobile % |
|---|---|---|---|
| fluid-heading-03 | 20px | 24px | 83% |
| fluid-heading-04 | 28px | 32px | 88% |
| fluid-heading-05 | 32px | 64px | 50% |
| fluid-display-01/02 | 40px | 80px | 50% |
| fluid-display-03 | 40px | 92px | 43% |
| fluid-display-04 | 40px | 176px | **23%** |

Clearest empirical proof: **bigger roles shrink far more.** Carbon's body/productive
type is **fixed** at 14/16px. **Confidence: high** (primary source code).

### Material 3
One type scale (Display L 57 / M 45 / S 36 / Headline L 32 … Body L 16 / M 14 / S
12 / Label S 11). M3 does **not** define per-breakpoint px; it advises keeping text
40–60 chars/line and swapping roles at breakpoints rather than interpolating.
([M3 type scale](https://m3.material.io/styles/typography/type-scale-tokens), [M3 layout](https://m3.material.io/foundations/layout/applying-layout)). Body constant; display change by role substitution. **Confidence: high.**

### Apple HIG / Dynamic Type
Dynamic Type scales by *user setting*, not viewport. **iPhone and iPad use the same
Dynamic Type sizes.** SF Pro Text/Display optical boundary at 20pt; **minimum 11pt**;
body 17pt, constant across screen width. ([Apple HIG typography](https://developer.apple.com/design/human-interface-guidelines/typography)). **Confidence: high.**

### Shopify Polaris
Polaris **collapsed two scales into one** after finding the viewport difference was
*"often a difference of 1px… the added complexity wasn't worth it; users often
didn't even realise a change happened."* One 1.2 ratio (rounded to 4px), shared
across viewports. ([Polaris v10 typography](https://polaris-react.shopify.com/previous-releases/version-10-typography)). A real-world vote against aggressive responsive type for UI. **Confidence: high.**

---

## 4. Does body/UI stay constant?

**Yes — strong consensus.** Apple holds body across devices; Carbon body is fixed;
Polaris shares one scale; reading comfort tracks *reading distance*, not viewport
width (we sit ~the same distance from phone and laptop) ([Blake Crosley](https://blakecrosley.com/blog/typography-systems)). The one nuance: Utopia's default nudges the base 18→20 (+11%), and many teams run 16→18 — so "bump body very slightly" is defensible, but "hold body constant" is the more common shipped choice. **A static body/UI tier is correct and well-supported. Confidence: high.**

---

## 5. How much should a hero shrink?

- **Carbon fluid-display-04: 176→40px (23%).** fluid-display-03: 92→40 (43%).
- **Utopia** tops out ~61px (73% at its top), and doesn't natively produce 160px
  heroes; extrapolating its ratio upward would shrink a 160px hero far below 0.75.
- Practitioner top-of-scale mobile heroes cluster ~40–62px regardless of desktop.

**Verdict on a 0.75 flat factor:** roughly right for *small* displays (48→36 is
sane) but **far too little shrink for true heroes.** 160→120 keeps a 120px headline
on a 360px phone — ~3 chars/line, wrapping a two-word headline to 3+ lines. Real
systems put a 160px-class desktop hero at **~40–56px** on mobile (a 0.25–0.35
factor at the top). The driver is **line/character count**: ~324px usable at 360px
viewport × 90% fits ~3 chars at 120px, ~9–11 chars at ~48px. **The shrink must
increase with size precisely to keep heroes from exploding into lines.**
**Confidence: high** on direction; exact mobile-hero target a judgement call ~40–64px.

---

## 6. Floors (minimum readable on mobile)

- **iOS/iPadOS minimum 11pt** (Apple HIG) — hard platform floor.
- **Web body 16px** — de-facto floor (avoids mobile-Safari input auto-zoom; readability).
- **WCAG** sets no absolute px min but requires 200% resize without loss (SC 1.4.4)
  and 4.5:1 / 3:1 (large ≥18.66px bold / 24px regular) contrast. Don't set a min
  that breaks 200% reflow.
- Practical: body/UI ≥ 14–16px, caption ≥ 12px (11px absolute), any heading ≥ ~18–20px.

---

## Recommended mapping for a curated ladder

Ladder (px): 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 80,
96, 112, 128, 144, 160.

**Model: size-dependent rung drop.** Body/UI = 0 rungs (static). Title = ~1 rung,
floored ~20px. Display = a growing rung drop, converging to a ~40–48px mobile band.

**Title** (≈ Carbon small fluid-headings + Utopia mids): 20→18/20, 24→20, 28→24,
32→28, 36→32, 40→36. **Display** (anchored to Carbon's fluid-display curve):
48→36, 64→40, 80→40, 96→48, 128→48, **160→48** (≈Carbon fluid-display-04 23%).

**Sourced (high confidence):** body static; shrink increases with size; the
~40–48px mobile hero band; floors (heading ≥18–20, body ~16, 11pt absolute);
Carbon's published pairs; Utopia defaults. **Judgement calls (anchored, not
guessed):** exact rung-drop counts; display mobile floor 40 vs 48; whether to allow
a 16→18 body nudge. *(Adopted in the Prism3 engine: body static, title 1 rung,
display interpolated against Carbon's curve — replacing the original flat factor.)*

## Sources
- [Utopia fluid type calculator](https://utopia.fyi/type/calculator/) · [Smashing: Meet Utopia](https://www.smashingmagazine.com/2021/04/designing-developing-fluid-type-space-scales/)
- [Carbon `_styles.scss`](https://github.com/carbon-design-system/carbon/blob/main/packages/type/scss/_styles.scss) · [Carbon `_scale.scss`](https://github.com/carbon-design-system/carbon/blob/main/packages/type/scss/_scale.scss) · [Carbon typography](https://carbondesignsystem.com/elements/typography/type-sets/)
- [Material 3 type scale](https://m3.material.io/styles/typography/type-scale-tokens) · [M3 layout](https://m3.material.io/foundations/layout/applying-layout)
- [Apple HIG typography](https://developer.apple.com/design/human-interface-guidelines/typography)
- [Shopify Polaris v10 typography](https://polaris-react.shopify.com/previous-releases/version-10-typography)
- [Clagnut (Rutter): In defence of fluid typography](https://clagnut.com/blog/2441) · [Blake Crosley: Type Scales](https://blakecrosley.com/blog/typography-systems) · [OneNine: mobile typography](https://onenine.com/10-mobile-typography-tips-for-better-readability/)
