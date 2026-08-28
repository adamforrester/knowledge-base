# Claude run — inverse encoding: what is actually best (2026-08-23, run 3)

Raw output. Every external claim fetched this run; URLs and dates inline. **Single-agent run.**

**Framing change, recorded because it retracts the earlier one.** Runs 1 and 2 were scoped to *"is our
decision defensible."* This run is scoped to **"what is actually best,"** and switching away from what
prism3 ships is a fully acceptable conclusion.

---

## Headline

**The hypothesis is wrong as stated, and the thing it was reaching for is real but sits in a different
place.**

Material 3 does **not** split `on-*` from `inverse*` by element-vs-region scope. Both families are
element-scoped. `inverseSurface` is for *"high-contrast **elements** like tooltips"* — snackbars and
tooltips, which are components, not page bands.

**But the survey's 7/7 finding was still comparing unlike things, for a reason the hypothesis did not
name.** No surveyed design system ships a *region*-inverse token concept at all. Their inverse tokens
are for components. **Region-inverse is handled one layer down, by the platform** — Android's
`ThemeOverlay`, iOS's trait overrides, CSS custom-property scoping, Flutter's nested `Theme`, React's
nested `ThemeProvider` — and **every one of those is mode-encoding**: the same name resolving
differently for a subtree.

So the honest picture is not *"seven systems disagree with prism3."* It is:

> **The token systems name-encode ELEMENT-inverse. The platforms mode-encode REGION-inverse. Both, in
> the same stacks.** Prism3 does both too — it just does the second one in the token layer rather than
> leaving it to the platform.

That reframing is the main output of this run, and §3 states what would falsify it.

---

## The five questions, answered separately

### 1. Best and most common practice for Figma?

**Most common: modes on collections, split by TIER (primitive/semantic), with appearance as the mode
axis.** Best is less settled. Figma documents multi-collection independent mode resolution
(`resolvedVariableModes`, `resolveForConsumer` — run 2), so an axis split is *supported*, but the
community's documented answer to the cross-product problem is merged mode names in one collection
(Figma forum #49690, 2026-01-15), and per-axis collections appear in no guidance I found.

**Verdict: common practice is tier-split; prism3's axis-split is supported but not idiomatic.**

### 2. Best and most common practice for developers?

**Most common: name-encoding for element-inverse, platform theming for region-inverse.** 7/7 systems
name-encode the element case (runs 1–2). For regions, developers reach for the platform mechanism —
CSS class scoping, `ThemeOverlay`, nested `Theme`/`ThemeProvider`.

**Best is the same split**, and it is not a compromise: the two cases have different shapes. An
element knows it sits on a fill (it renders the fill); a region's children do not know what band they
are in.

### 3. Best and most common practice for the target platforms?

**Unanimous, and it is mode-encoding.** Every target has a first-class subtree mechanism — §4. This is
the strongest single finding in the run and it points the opposite way from the token survey.

### 4. Best DEVELOPER experience — least explaining?

**Name-encoding, for the element case. Platform-native mode-encoding, for the region case.**

`fgColor-onEmphasis` needs no mechanism explained — the name says it. But it needs the *pairing rule*
taught (Primer: *"must pair with"*), and it needs exceptions taught (Atlassian's warning ground).

For a region, name-encoding is *worse* on this criterion, because every descendant must be told, and
that is what Fluent's multiplied name space is. `<div class="theme-inverse">` needs one sentence.

**A developer already knows their platform's theming mechanism.** That is the criterion-4 argument for
mode-encoding regions, and it is a strong one.

### 5. Best DESIGNER experience — least explaining?

**Name-encoding, clearly, and this is where mode-encoding loses.**

A designer picking `text/inverse` from a list sees what they get. A designer relying on a mode set on
an ancestor frame has to know (a) that a surface collection exists, (b) that a mode is set somewhere
up the tree, (c) that it composes with appearance. Figma's Help Center — the surface a designer
actually reads — **does not explain cross-collection composition at all**; that lives in the plugin
API (run 2). **The designer-facing documentation for the mechanism prism3 depends on does not exist.**

**This is prism3's weakest criterion and it is not close.**

---

## 2. The hypothesis, tested — and broken as stated

**Predicted:** `on-*` for elements, `inverse*` for regions.

**Found:** both element-scoped. Two independent sources, fetched 2026-08-23, describe M3's inverse
family as for *"high-contrast **elements** like tooltips."* The components using it are **Snackbar**
(container `inverseSurface`, action `inversePrimary`) and **Tooltip** — both small components.

Android's own role documentation defines the on-* family as *"a color for text or icons on top of its
paired parent color… on primary is used for text and icons against the primary fill color."* The same
page **does not define the inverse roles at all**, which is itself telling about their prominence.

**So the real M3 distinction is not scope, it is WHICH GROUND:**

| family | the ground | scope |
|---|---|---|
| `on-*` | a specific paired role's fill (`primary`, `error`) | element |
| `inverse*` | a neutral-inverted surface, for components that must contrast with everything | **element** |

Both are "an element on a known ground". Neither is a region.

**I could not verify the tooltip spec directly** — `m3.material.io` is a JS application returning
title-only content to a fetch, the same failure that blocked `spectrum.adobe.com` in runs 1–2. The
snackbar finding is from run 1 and the tooltip finding is from two secondary sources this run.
**Flagged: the sharpest single test rests on secondary sources**, because the primary is unfetchable.

**No other surveyed system ships two families**, so the cross-check the brief asked for has no other
subject. Fluent's `NeutralForegroundInverted` and Atlassian's `color.text.inverse` are single families
and are element-scoped by their own descriptions (*"for use on bold filled backgrounds"*).

### What survives, and it is not nothing

The **element/region distinction is real** — prism3's own 16/112 split lands exactly on it, and the 16
non-flipping roles being precisely `text/on-*`, `icon/on-*` and `veil/*` is a strong internal
corroboration.

What is wrong is the claim that **the surveyed systems draw it**. They do not, because **they do not
have a region-inverse concept in tokens at all.** The 7/7 was not comparing element-encoding to
region-encoding; it was comparing prism3's region mechanism to everyone's *element* mechanism, and
those systems' region answer was never in the token layer to be surveyed.

**So: partly a category error, yes — but not the one proposed, and the correction points somewhere
more useful.**

---

## 3. What would falsify the reframing

Stated because an attractive synthesis from a third run deserves the same suspicion as one from the
orchestrator:

1. **Find a design system that ships region-inverse in tokens.** One that says "apply this token set to
   a section" rather than "use this token for text on a fill." I found none; I did not exhaustively
   look.
2. **Find a platform's own design-system guidance recommending its theming mechanism for inverse
   sections.** I confirmed the *mechanisms* exist and are idiomatic; I did **not** confirm that
   Material's, Apple's or Shopify's design guidance says "use it for inverse regions." That link is
   inferred and is the weakest joint in the reframing.
3. **Show that region-inverse is rare enough not to need a mechanism** — if most products have three or
   fewer surfaces, the whole question is over-engineering (KB `31` §4 already says something close).

---

## 4. Priority 3 — the platforms. Every target mode-encodes regions natively.

All fetched 2026-08-23.

**Android — confirmed, and it is exactly region-inverse.** `android:theme` on a ViewGroup applies to
all views within it; *"Setting a theme at any level in the view tree doesn't replace the theme
currently in effect, **it overlays it**."* There is a naming convention — `ThemeOverlay.*` — for
*"narrowly-scoped themes… defining as few attributes as possible."* `MaterialThemeOverlay` and
`materialThemeOverlay` exist for component default styles.
**Idiomatic: yes, strongly — it has its own naming convention.**
**Not verified: whether Material's own design guidance recommends it for inverse sections specifically.**

**iOS — answerable, and the answer is better than feared, from iOS 17.** This was flagged as the one
least trusted and where a negative would be serious. It is not a negative:

- Custom axes are first-class since **iOS 17**: conform to `UITraitDefinition` with a `defaultValue`.
- `traitOverrides` exists on windows, views, view controllers and presentation controllers, and
  (WWDC23 session 10057) *"Trait overrides applied to the parent affect the parent's own trait
  collection. And then the values from the parent's trait collection are inherited to the child."*
  — subtree propagation, which is region scoping.
- Secondary sources report a `affectsColorAppearance` flag on a custom trait, whose whole purpose is
  to make dynamic `UIColor`s re-evaluate when that trait changes, and that reading a custom trait from
  a `UIColor` dynamic provider *"works exactly as you expect."*

**Two honest caveats.** `affectsColorAppearance` and the dynamic-provider claim came from
**secondary** sources (developer blogs); the WWDCNotes page I fetched confirms custom traits and
override propagation but **does not mention** either. And this is **iOS 17+ (Sept 2023)** — before
that there was no first-class custom axis. Older deployment targets are a real constraint.

**So the loud negative the brief asked me to look for is not there**, with those caveats.

**Web / CSS — the canonical idiom.** A class or data attribute on a root element, redefining custom
properties for all descendants. Explained in one sentence in every source that mentions it.

**Flutter — nested `Theme`.** Wrap a subtree in a `Theme` with its own `ThemeData`; *"localized
customizations without affecting the rest of the application."*

**React Native / styled-components — nested `ThemeProvider`, and the coincidence is worth noting:**
styled-components' own advanced docs use **inverting background and foreground** as the worked example
for a second nested `ThemeProvider`. **The library's canonical example of nesting is literally
inverse.**

**Every target platform mode-encodes region context, natively and idiomatically. None of them
name-encodes it.**

---

## 5. Documentation burden — an observation with counts, not a score

The brief's proxy for criteria 4 and 5: how much does each mechanism's own documentation need to make
it usable? Counted as sources needed, worked examples, and cautions.

| mechanism | explanation needed | cautions |
|---|---|---|
| **CSS class scoping** | one sentence, in every source | none found |
| **Flutter nested `Theme`** | one sentence + one example | none found |
| **styled-components nested `ThemeProvider`** | one example — and it is the inverse example | none found |
| **Name-encoding (element)** | zero for the *mechanism* — the name says it | **two**: the pairing rule (Primer *"must pair with"*), and exceptions (Atlassian's warning ground) |
| **Android `ThemeOverlay`** | a multi-part blog series is the standard reference; needs the naming convention, `android:theme` vs `materialThemeOverlay`, and *"overlays rather than replaces"* | **two+** |
| **iOS custom traits** | a WWDC session; `UITraitDefinition` + `defaultValue` + `traitOverrides` + change registration | **two+**, plus an OS floor |
| **Figma cross-collection modes** | **split across two documentation surfaces** — the Help Center does not cover composition; the plugin API does | **the split itself** |

**Two readings, both fair.** Name-encoding wins the mechanism column outright and loses the caution
column. And the Figma row is the criterion-5 problem in one line: **the explanation a designer needs is
in the developer documentation.**

---

## 6. Recommendation

**The split is real and each mechanism is right for its scope — but the line falls between the TOKEN
layer and the PLATFORM layer, not between two token families.**

Concretely, and this is close to what prism3 already ships:

1. **Keep name-encoding for element-inverse.** The 16 non-flipping roles — `text/on-*`, `icon/on-*`,
   `veil/*` — are exactly the field's universal, and 7/7 agreement on a case this narrow is worth
   deferring to.
2. **Keep mode-encoding for region-inverse**, because **every target platform does it that way
   natively.** A React developer writes a class; an Android developer writes a `ThemeOverlay`; an iOS
   17 developer writes a trait override. Emitting a region axis that lands on those mechanisms is
   *more* idiomatic per-platform than emitting 112 extra names for them to wire up by hand.
3. **Fix the criterion-5 problem rather than the architecture.** The weakness is not the encoding, it
   is that a designer cannot learn it from designer-facing documentation. That is answerable with a
   one-page explainer and a worked Figma file.

### What this recommendation loses on, plainly

- **Criterion 5 (designer comprehension) — it loses, and not narrowly.** A mode set on an ancestor is
  invisible from the binding, and Figma's designer-facing docs do not explain composition. Any adopting
  designer needs teaching that no vendor documentation will do for you.
- **Criterion 1 (Figma common practice) — it loses.** Axis-split collections appear in no guidance
  found across three runs. Supported ≠ idiomatic.
- **Criterion 2, partly.** Region-inverse in the *token layer* is not what developers currently expect
  to receive; they expect to implement it themselves. This may read as the token layer overreaching.
- **And one that is not a criterion but is real: #1129.** The mode encoding has no DTCG expression
  today — the pointer tier is hard-aliased to `default` with zero inverse leaves. **Criteria 4 and 5
  are currently judging an unimplemented thing**, and any comprehension claim in either direction is
  provisional until it emits.

**Where it wins:** criterion 3 outright and unanimously, and criterion 4 for the region case.

**What would change it:** if #1128's measurement showed the 112 flipping roles were mostly not used in
inverse regions in practice, the region axis would be machinery for a case that does not arise, and
name-encoding's simplicity would win on volume alone. **That measurement, not this survey, should
decide it** — this run's job was to make sure the options were not misjudged, and one of them was.

---

## 7. Still unverified

1. **Whether Adobe ships an official Spectrum Figma library with variables — third attempt, still not
   established.** New this run: `adobe/spectrum-design-data` ships a **Figma plugin** ("Component
   Options Editor") for *authoring schemas*, not a consumer design library. So Adobe's Figma investment
   in that repo is tooling. `spectrum.adobe.com` remains unfetchable (JS app). **AEM / Experience Cloud
   unanswered across all three runs.**
2. **M3's tooltip spec, read directly.** The sharpest single test rests on secondary sources because
   `m3.material.io` cannot be fetched.
3. **`affectsColorAppearance` and UIColor dynamic-provider custom-trait reading** — secondary sources
   only; not in the WWDC notes I fetched.
4. **Whether any platform's design guidance recommends its theming mechanism for inverse regions** —
   the weakest joint in §2's reframing, stated in §3.
5. **Whether any system ships region-inverse in tokens.** I found none and did not look exhaustively.
