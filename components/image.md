---
okf_version: "0.1"
type: component-brief
title: Image
description: The media primitive, and the one whose two load-bearing decisions sit at opposite ends of the stack — a reserved box that prevents layout shift, and an `alt` value whose correct answer is sometimes the empty string. A field-truth study of the aspect-ratio frame, the omitted-versus-empty alt distinction, the lazy-loading own-goal on the LCP image, focal-point cropping, and how much delivery responsibility a design system's Image should actually take.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [img, picture, media, thumbnail, figure]
last-audited: 2026-08-14
timestamp: 2026-08-14
---

# Image

> An `<img>` tag is four characters and a URL, which is why a design system's Image component is so often a thin styling wrapper that adds nothing. The two things that make it worth building are both invisible in a screenshot: a **reserved box**, so the page does not jump when the file arrives, and an **`alt` decision**, whose correct answer for most images in most product UI is the empty string — but only when it is written, never when it is omitted. Everything else is `object-fit` and a radius token. The brief is about the two.

---

## 1. Framing

Image renders content imagery — a photograph, an illustration, a product shot, a logo — inside a box the layout can reason about before the file has loaded. What it *isn't*: an **Icon** (a glyph from a versioned set, sized on a rung, inheriting ink — a different component with a different accessibility contract); an **Avatar** (identity, with a fallback chain to initials and its own inverse accessible-name rule — see `avatar`); a **decorative background**, which is CSS's job and gains nothing from a component; and it is not a delivery pipeline — the CDN, the format negotiation and the responsive source set are infrastructure the component may *expose* and should not *replace* (§11).

The contested core is **scope**: how much of the delivery problem the design system's Image takes on. The field runs from a styled `<img>` at one end to a full machine with blur-up placeholders, automatic format negotiation and required dimensions at the other. That range is real, and the answer is engagement-dependent rather than universal, which §11 says plainly rather than pretending otherwise.

## 2. Anatomy and parts

Three parts, and the first is the component's actual contribution:

- **The frame** — a box with a known aspect ratio, reserved before the image loads. This is the whole reason to have a component. An unframed `<img>` occupies zero height until its bytes arrive and then shoves everything below it down the page.
- **The media** — the image itself, fitted into the frame by `object-fit` and positioned by `object-position` (the focal point).
- **The state layer** — what occupies the frame while loading and what replaces it on error. Skeleton, solid placeholder, blur-up, or nothing; and a fallback for the failed case.

An optional fourth part is the **caption**, at which point the component is a `<figure>`/`<figcaption>` pair rather than an image. Most systems keep that separate and so does the practice — a caption is content structure, not media.

## 3. Properties / API

The converged surface: `src`, `alt` (§6 — always present, sometimes empty), `aspectRatio`, `fit` (`cover` / `contain` / `fill` / `none`), `position` (the focal point), `loading` (`lazy` / `eager`), `fetchPriority`, `fallback`, and `radius` from the radius scale.

**`alt` is required by the API even when its value is `""`.** This is the one place a component should be stricter than the platform, and §6 is the reason: HTML lets you omit `alt` and the omission is a silent defect, while the empty string is a positive declaration. A required prop makes "this image is decorative" a decision someone made rather than a line someone did not write.

**`aspectRatio` is effectively required in practice** even where it is optional in the type — an Image without one is an Image that shifts the layout, which is the defect the component exists to prevent. Where intrinsic `width`/`height` attributes are available they serve the same purpose and the component should pass them through rather than requiring the ratio twice.

**Tokens, not props:** radius. **Deliberately absent:** any prop that sets margin. Same argument as Text — spacing belongs to the container.

## 4. States and variants

Unlike most primitives in this category, Image genuinely **has runtime states**: `loading`, `loaded`, `error`. That is worth saying explicitly because the Foundations category is otherwise full of components whose states section collapses to `[]`, and a reader skimming the catalogue will expect this one to as well.

The error state is the one most often left unhandled, and its failure mode is a broken-image glyph plus the alt text rendered as bare text — visually the worst possible outcome and one that only appears in production.

Variants are the cartesian of `fit` × `radius` × the state layer's chosen placeholder style.

## 5. Usage guidance

**Use** for content imagery that carries meaning or is part of the page's substance — product photography, editorial images, illustrations, logos in content.

**Don't use** for icons (Icon), for identity (Avatar), or for purely decorative texture and backgrounds, which belong in CSS where they cost no DOM and carry no accessibility obligation.

**Don't use it to lay out a grid of images** — that is the layout primitive's job, and an Image with gap or column props is a layout component wearing a media component's name.

**The judgment worth stating: decorative or not is a content decision, not a technical one,** and it has to be made per instance rather than per component. The same photograph is informative in an article and decorative in a hero band beside a heading that already says what it shows. §6 and §7 carry the rule; the point here is that a system cannot default it correctly.

## 6. Accessibility

Two things, and the first is more subtle than it looks.

- **`alt` omitted and `alt=""` are different, and the difference is the whole contract (WCAG 1.1.1).** An empty `alt` marks the image decorative and assistive technology skips it — correct, and the right answer for a large share of product imagery. An **omitted** `alt` leaves the image with no accessible name, and screen readers commonly fall back to announcing the **filename**, which is how users end up hearing `hero-banner-v3-final-2.jpg`. The two look identical in a browser and behave oppositely. This is why §3 makes the prop required.
- **Informative images need an alt that describes the function, not the picture.** If the image is a link or a control, the alt describes the destination or action, not the artwork. If the image conveys information the surrounding text does not, the alt carries that information.
- **Images of text (1.4.5).** Text baked into an image cannot be resized, restyled, translated, or read. Logos are the standing exception. This is a content-governance issue more than a component one, but the component is where it becomes visible.
- **Complex images need more than `alt`** — a chart or diagram needs a long description adjacent or linked (1.1.1 again). An `alt` is one sentence; a data visualization is not.
- **Never let an image be the sole carrier of information** — the same rule as colour, and it applies to status imagery in exactly the way it applies to status colour.

(See 14-accessibility and 28-web-accessibility-implementation.)

## 7. Content guidelines

Alt text: describe **function over appearance**; do not open with "image of" or "picture of" (the role is already announced); keep it to roughly one sentence — long alt is a signal that a long description is what is actually needed; and write `alt=""` deliberately for decorative images rather than leaving the prop off. For an image inside a link, the alt is the link's accessible name and should read as a destination.

Filenames are not alt text, and the reason is §6's fallback — a filename is what gets announced when the contract is broken, so treating filenames as descriptive is optimizing the failure case instead of fixing it.

## 8. Motion and transition

A fade-in on load is the field default and is worth having — it converts a hard pop into a soft arrival and costs nothing. Blur-up (a tiny placeholder scaled and blurred, resolving to the full image) is the richer version and is a delivery-layer feature more than a component one.

Under `prefers-reduced-motion`, an opacity fade is generally acceptable — it is not vestibular-triggering — while any zoom, scale or parallax on load must resolve to none. (See 18-motion-foundations.)

## 9. Internationalization

- **Images containing text need localized assets**, which is the practical argument behind 1.4.5 (§6) rather than the accessibility one.
- **Directional imagery mirrors in RTL; photographs must not.** A screenshot with an arrow pointing at a UI element, or a diagram with left-to-right flow, needs a mirrored variant. A photograph of a person, a product, or anything containing real-world text mirrors into nonsense. Systems that apply a blanket `transform: scaleX(-1)` in RTL get this wrong in the second case, and it is a memorable failure.
- **Culturally specific imagery** — gestures, foods, settings — carries meaning that does not travel. Out of a component's control and in a content-governance remit, noted here because the component is where the asset is chosen.

(See 13-internationalization-and-rtl.)

## 10. Naming

`Image` is the field default (Polaris, Spectrum, Chakra, Ant, Mantine). `Img` appears as the element-mirroring alternative; `Picture` names the art-direction element specifically; `Media` is broader and usually covers video too.

Polaris ships a separate `Thumbnail` for the small fixed-size case. **The practice treats thumbnail as a size, not a component** — a second component for the same media at a smaller box duplicates every decision in this brief for no gain.

**The practice default is `Image`,** with `Img`, `Picture`, `Media`, `Thumbnail` and `Figure` documented as aliases.

## 11. Implementation notes

- **Reserve the box, and prefer intrinsic `width`/`height` attributes where the dimensions are known.** Modern browsers compute an aspect ratio from the attribute pair and reserve the space before load, which fixes Cumulative Layout Shift without a wrapper. CSS `aspect-ratio` covers the case where the ratio is a design decision rather than the file's own.
- **Do not lazy-load the LCP image.** This is the standing own-goal: `loading="lazy"` applied indiscriminately delays the one image the Largest Contentful Paint metric is measuring, making the page measurably slower while looking like an optimization. Above-the-fold hero images want `loading="eager"` and `fetchpriority="high"`; everything below the fold wants `lazy`. A component that defaults `lazy` for everything needs an escape hatch that people actually know about.
- **`object-fit` requires an explicitly sized box** to fit into. Without the frame it does nothing, which reads as the prop being broken.
- **`srcset`/`sizes` and `<picture>` solve different problems.** `srcset` is resolution switching — the same image at different pixel densities and widths. `<picture>` with `<source media>` is art direction — a *different crop or composition* per breakpoint. Conflating them produces a responsive image that is correctly sized and badly composed on small screens.
- **Compose with the framework's image component; do not replace it.** `next/image` and its equivalents own format negotiation, CDN routing and placeholder generation, and reimplementing that inside a design system is a large maintenance surface for a problem the platform layer already solved. The DS Image should own the *frame, fit, focal point, radius and alt contract* and delegate delivery. This is the practical answer to §1's scope question, and it is the one an engagement is most likely to override.
- **Handle the error state explicitly.** The default failure — broken-image glyph plus rendered alt text — is worse than any deliberate fallback.

## 12. Related and alternative components

- **Composes with:** Card (the dominant host, and the reason a fixed ratio matters — a row of cards with unframed images is a row of different heights), Skeleton (the loading state), List, Empty State, Banner, and a Figure/caption pairing where one exists.
- **Alternative to:** Icon (glyph from a set), Avatar (identity, with its own fallback chain), and a CSS `background-image` for decorative texture — which is usually the better answer when the image carries no meaning.
- **Supersedes:** a bare `<img>` with hand-applied sizing and no reserved box.
- **Superseded by:** nothing.

(See 03-component-library for the system-level model and 29-per-component-documentation-template for the docs page.)

## 13. Field POV evolution

1. **CSS `aspect-ratio` retired the padding hack.** The percentage-padding wrapper that reserved image space for a decade is legacy; new systems should not carry it, and old ones can drop the wrapper element entirely.
2. **The DS Image is thinning as the framework image component thickens.** As `next/image` and peers absorbed delivery, the component's remit narrowed to frame, fit and contract — which is a better-scoped component than the one that tried to own bytes.
3. **Format negotiation moved to the CDN.** AVIF/WebP with fallbacks is increasingly an infrastructure concern rather than a markup one, which is why §11 puts it outside the component.
4. **`fetchpriority` is the newer control worth knowing**, and it is what makes the eager/lazy split above actionable rather than binary.

## 14. Sources cited

Conservative version dates (claude-only run, per the convergent-primitive rule; `last-audited` is the re-run trigger):

- Shopify Polaris — `Image`, and `Thumbnail` as a separate component (2024–25).
- Adobe Spectrum — `Image` with `objectFit` (2024).
- Chakra UI — `Image` with `fallback` and `fit` (2024).
- Ant Design — `Image` with preview, placeholder and fallback (2024).
- Mantine — `Image` with `fit` and fallback (2024).
- Next.js — `next/image`: required dimensions, blur placeholder, format negotiation (2024–25).
- MDN / HTML Standard — `<img>` `alt`, `loading`, `fetchpriority`; `<picture>` and `srcset`/`sizes`.
- web.dev — Cumulative Layout Shift and Largest Contentful Paint guidance, including the lazy-loaded-LCP anti-pattern.
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.1.1, 1.4.5.

## 15. Agent-consumable schema

```yaml
identity:
  id: image
  name: Image
  aliases: [img, picture, media, thumbnail, figure]
  category: foundations
  status: stable
description: >
  Content imagery inside a box the layout can reason about before the file
  loads. Two load-bearing decisions: a RESERVED FRAME (prevents layout
  shift) and an ALT VALUE whose correct answer is often the empty string —
  but written, never omitted. Not an Icon (glyph from a set), not an Avatar
  (identity + fallback chain), not a decorative background (CSS).
anatomy:
  frame: "a box with a known aspect ratio, reserved BEFORE load — the component's actual contribution"
  media: "the image, fitted by object-fit and positioned by object-position (focal point)"
  state-layer: "placeholder while loading; fallback on error"
  not-included: "caption — that is a figure/figcaption pairing, content structure rather than media"
api:
  props:
    - {name: src, type: string, required: true}
    - {name: alt, type: string, required: true, description: "REQUIRED even when empty. '' = decorative and skipped; OMITTED = no accessible name and screen readers announce the FILENAME. Stricter than the platform on purpose."}
    - {name: aspectRatio, type: "string | number", required: false, description: "optional in the type, effectively required in practice — an Image without one shifts the layout"}
    - {name: fit, type: enum, values: [cover, contain, fill, none], default: cover, required: false, description: needs an explicitly sized box or it does nothing}
    - {name: position, type: string, default: center, required: false, description: the focal point (object-position)}
    - {name: loading, type: enum, values: [lazy, eager], default: lazy, required: false, description: "MUST be eager for the LCP image — see implementation"}
    - {name: fetchPriority, type: enum, values: [high, low, auto], default: auto, required: false}
    - {name: fallback, type: node, required: false, description: replaces the default broken-image glyph + bare alt text}
    - {name: radius, type: enum, values: "the radius scale", required: false}
  tokens-not-props: [radius scale values]
  deliberately-absent: [margin, gap, columns]   # spacing and grids belong to the layout primitive
states:
  runtime: [loading, loaded, error]
  note: "genuinely stateful, unlike most Foundations primitives whose states collapse to [] — the error state is the one most often unhandled and only appears in production"
variants:
  fit: [cover, contain, fill, none]
  radius: "the radius scale"
  placeholder: [none, solid, skeleton, blur-up]
accessibility:
  wcag-criteria: ["1.1.1", "1.4.5"]
  alt-contract: "omitted != empty. alt='' marks decorative and is SKIPPED; omitting alt leaves no accessible name and AT commonly announces the filename."
  informative: "alt describes FUNCTION, not appearance; for a linked image the alt is the destination"
  complex: "charts/diagrams need a long description adjacent or linked — an alt is one sentence"
  never: "let an image be the sole carrier of information (same rule as colour)"
content:
  alt-pattern: "function over appearance; never open with 'image of'; ~one sentence; write '' deliberately for decorative"
  empty-pattern: "alt='' — a positive declaration, not an omission"
  trap: "filenames are not alt text — a filename is what gets announced when the contract is BROKEN"
motion:
  enter: "fade-in on load is the field default; blur-up is the delivery-layer version"
  reduce-motion: "an opacity fade is acceptable (not vestibular); any zoom/scale/parallax resolves to none"
i18n:
  localized-assets: "images containing text need per-locale assets"
  rtl: "DIRECTIONAL imagery mirrors (diagrams, annotated screenshots); PHOTOGRAPHS must not — a blanket scaleX(-1) in RTL is the memorable failure"
  cultural: "gestures, foods and settings carry meaning that does not travel — content governance, noted because the component is where the asset is chosen"
implementation:
  - "reserve the box; prefer intrinsic width/height attributes where known (browsers derive the ratio and reserve space, fixing CLS with no wrapper)"
  - "DO NOT lazy-load the LCP image — loading=lazy applied indiscriminately delays the exact image LCP measures, making the page slower while looking like an optimization"
  - "object-fit requires an explicitly sized box or it silently does nothing"
  - "srcset/sizes is RESOLUTION SWITCHING; <picture> + source media is ART DIRECTION — different problems, and conflating them ships a correctly-sized badly-composed mobile crop"
  - "compose with the framework image component (next/image and peers own format negotiation, CDN routing, placeholders); the DS owns frame, fit, focal point, radius and the alt contract"
  - "handle error explicitly — the default failure (broken-image glyph + rendered alt) is worse than any deliberate fallback"
composition:
  composes-with: [card, skeleton, list, empty-state, banner, figure]
  alternative-to: [icon, avatar, "CSS background-image for decorative texture"]
  supersedes: ["bare <img> with hand-applied sizing and no reserved box"]
  superseded-by: null
notes:
  contested:
    - "SCOPE — how much delivery the DS Image owns. The field runs from a styled <img> to a full blur-up/format-negotiation machine. We land on frame + fit + focal point + radius + alt contract, delegating delivery — and this is the call an engagement is most likely to override."
    - "thumbnail as a size vs as a separate component (Polaris ships both) — we treat it as a size"
  evolution:
    - "CSS aspect-ratio retired the percentage-padding hack; new systems should not carry the wrapper"
    - "the DS Image is thinning as the framework image component thickens"
    - "format negotiation moved to the CDN"
    - "fetchpriority is what makes the eager/lazy split actionable rather than binary"
```

---

*Provenance: claude-only research run, 14 August 2026, sanctioned by the convergent-primitive rule (see `components/index.md`) — the field converges on the API and splits only on §1's scope question, which is recorded as contested rather than resolved because the honest answer is engagement-dependent. Written alongside `text.md` to close a gap found from the downstream direction: the Prism3 MVP catalogue (`Prism3/docs/40`) named `image` as a required dependency of Card with no brief behind it, which inverts the catalogue's pipeline. Two calls carry the brief. The first is making `alt` a REQUIRED prop whose value may be empty — stricter than HTML deliberately, because the platform's own permissiveness is what makes the defect silent, and `alt=""` versus omitted-`alt` behave oppositely while looking identical. The second is §11's lazy-loading bullet, which is the rare case of a well-intentioned default measurably harming the metric it appears to serve. §4 is called out against the category's pattern: unlike Divider, Icon and most Foundations primitives, this one is genuinely stateful. The §15 schema conforms to `_schema.md`.*
