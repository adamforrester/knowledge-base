# Verification findings — Image

Run 2026-08-15 against primary sources. Three questions: **two confirmed outright, one confirmed with
a caveat the brief had omitted.**

---

## 1. `alt=""` versus omitted `alt` — CONFIRMED, verbatim, including the filename fallback

MDN, `Web/HTML/Reference/Elements/img`, quoted rather than paraphrased:

> Setting this attribute to an empty string (`alt=""`) indicates that this image is *not* a key part
> of the content (it's decoration or a tracking pixel), and that non-visual browsers may omit it from
> rendering. Visual browsers will also hide the broken image icon if the `alt` attribute is empty and
> the image failed to display.

And, on omission:

> When an `alt` attribute is not present on an image, some screen readers may announce the image's
> file name instead. This can be a confusing experience if the file name isn't representative of the
> image's contents.

MDN also describes the attribute as **mandatory**.

**Both halves of §6's contract hold**, including the specific claim that led the brief — that the two
*look identical in a browser and behave oppositely*, and that the failure mode is a filename being
announced. §3's decision to make `alt` a **required prop whose value may be empty** is justified by
the source rather than by preference, and the brief now says so with the quotation attached.

One hedge in the source worth carrying rather than smoothing: MDN says *"some screen readers **may**
announce the file name."* The brief's first draft said screen readers *"commonly"* do. Softened to
match — the behavior is real and not universal, and overstating it is the same species of error as
the citations this pass exists to correct.

## 2. Lazy-loading the LCP image — CONFIRMED, with a conditionality the brief omitted

From web.dev's LCP lazy-loading article. WordPress lazy-loaded **all** images, including
above-the-fold:

| | median LCP |
|---|---|
| lazy-loading all images | **2,029 ms** |
| above-the-fold images exempted | **~1,749 ms** |
| baseline before the change | 1,759 ms |

**+13% slower on archive-desktop**, and the byte savings were retained once above-fold images were
exempted — so the cost bought nothing.

**The caveat the brief did not carry:** on **single pages the effect was minimal, within variance.**
The article's own framing is that the problem was lazy-loading *all* images rather than the technique
itself.

So §11's claim is **substantially right and was stated too broadly.** *"Applied indiscriminately"*
was doing real work in the original sentence and the rest of the sentence overrode it. Corrected to
carry the figures and the condition: the penalty lands when the lazily-loaded image **is** the LCP
element, which is a property of the page rather than of the attribute.

That refinement matters for a design system specifically. A DS `Image` cannot know whether a given
instance is the LCP element — **only the page can** — which is a further argument for §11's position
that the component owns frame, fit, focal point, radius and the alt contract while delivery decisions
belong to the consumer.

## 3. Polaris ships `Thumbnail` separately — CONFIRMED, and it supports §3

From `polaris-react/src/components/Thumbnail/Thumbnail.tsx`:

```ts
export interface ThumbnailProps {
  size?: Size;                    // 'extraSmall' | 'small' | 'medium' | 'large', default 'medium'
  source: string | React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  alt: string;
  transparent?: boolean;
}
```

Separate component, four sizes, and it renders either an `Image` or an `Icon` depending on whether
`source` is a URL or an SVG component.

**§10's position is unchanged** — the practice still treats thumbnail as a size rather than a
component, because a second component for the same media at a smaller box duplicates every decision
in this brief. Polaris shipping both is the evidence being argued *against*, and it is correctly
cited.

**The unplanned finding is `alt: string` — required, not optional.** Polaris makes the same call §3
makes, on the sibling component, independently. The brief presented required-`alt` as deliberately
stricter than HTML with no field witness; there is one, and it is now cited.

---

## What this pass did not establish

- **Spectrum, Chakra, Ant, Mantine.** In §14 with version dates, unchecked here. Downgraded.
- **`next/image`'s current behavior** — required dimensions, blur placeholder, format negotiation.
  Load-bearing for §11's *"compose with the framework's image component, do not replace it"* and not
  verified. Moved to `notes.unverified`.
- **AVIF/WebP CDN negotiation as the prevailing pattern** (§13). A trend claim, unsourced.
- **The RTL mirroring rule** — directional imagery mirrors, photographs must not. Stated from
  practice, not from a source, and it is one of the sharper claims in the brief. Flagged.

That last one is worth naming rather than burying: **§9's mirroring distinction is the most
confidently-written unverified claim in either brief.** It reads as established because it is stated
crisply, which is precisely the property that made §14 dangerous in the first place.
