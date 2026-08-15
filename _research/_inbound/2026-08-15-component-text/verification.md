# Verification findings — Text

Run 2026-08-15 against primary sources. Three questions, **two confirmed, one falsified.**

---

## 1. Polaris ships `as` and `variant` as separate props — CONFIRMED

Read from `Shopify/polaris` → `polaris-react/src/components/Text/Text.tsx`, the TypeScript interface
rather than a docs page.

| prop | JSDoc, verbatim |
|---|---|
| `as: Element` | *"The element type"* |
| `variant?: Variant` | *"Typographic style of text"* |
| `alignment?: Alignment` | *"Adjust horizontal alignment of text"* |
| `fontWeight?: FontWeight` | *"Adjust weight of text"* |
| `tone?: Tone` | *"Adjust tone of text"* |
| `textDecorationLine?: TextDecorationLine` | *"Add a line-through to the text"* |
| `numeric?: boolean` | *"Use a numeric font variant with monospace appearance"* |
| `truncate?: boolean` | *"Truncate text overflow with ellipsis"* |
| `breakWord?: boolean` | *"Prevent text from overflowing"* |
| `visuallyHidden?: boolean` | *"Visually hide the text"* |

`as` is **required and un-suffixed**; every visual prop is optional. The two axes are separate in the
type, not merely by convention.

**Unplanned confirmation of the brief's §3 surface.** The brief proposed `as`, `size`/`variant`,
`weight`, `tone`, `align`, `truncate`/`lineClamp` and `visuallyHidden`. Polaris carries all of them
bar `lineClamp`, under near-identical names (`alignment` for `align`). That was arrived at
independently and matches — which is a real convergence rather than a restatement, since the brief
was written before this file was read.

## 2. Polaris *states the rationale* — **FALSIFIED**

The brief said, of the decoupling:

> *"Polaris is the reference API here and states the reasoning plainly — the element you need and the
> style you want are independent choices, and a system that fuses them forces you to break one to get
> the other."*

**Nothing in the source states that.** The JSDoc is `"The element type"` and `"Typographic style of
text"`. Polaris **demonstrates** the decoupling; it does not argue for it anywhere this pass could
reach.

That distinction is not pedantic. §3 leaned on Polaris as *authority for the reasoning*, and what
exists is authority for *the shape*. The argument for **why** — §6's heading-order case, that a
correct outline requires an `h2` that sometimes looks small — is **this vault's**, not Shopify's, and
presenting it as inherited borrowed credibility the source does not supply.

**Correction applied to `text.md` §3**: Polaris is now cited as the reference *API*, with the
rationale explicitly attributed to §6 and to this brief. If Shopify has argued it in a blog post or a
changelog, that would be a legitimate citation — this pass did not find one, and absence of a finding
is not evidence of absence.

## 3. Base Web ships per-style components — CONFIRMED, and larger than claimed

Read from `uber/baseweb` → `src/typography/index.tsx`. **36 exported components**, verbatim:

```
DisplayLarge · DisplayMedium · DisplaySmall · DisplayXSmall
HeadingXXLarge · HeadingXLarge · HeadingLarge · HeadingMedium · HeadingSmall · HeadingXSmall
LabelLarge · LabelMedium · LabelSmall · LabelXSmall
ParagraphLarge · ParagraphMedium · ParagraphSmall · ParagraphXSmall
```

…and a complete `Mono*` mirror of all eighteen.

No single `Text` component with a size prop. Each export is a distinct style-and-size combination.

**This strengthens §10 rather than merely confirming it.** The brief said per-style components
*"multiplies the API surface by the length of the ramp."* Measured, that multiplication is **36
exports for one concept**, and every ramp change is 36 potential API changes. The brief now carries
the number, because 36 argues the point better than the sentence did.

---

## What this pass did not establish

Named so the revised §14 is honest about its own coverage, and because a verification record that
lists only successes is the shape it exists to prevent:

- **Radix Themes, Chakra, Spectrum, Ant, Material, Carbon.** All six appeared in §14 with version
  dates and none were checked here. They are field-convention claims the author believes and cannot
  currently source. Downgraded in §14 and, where they carry weight, moved to `notes.unverified`.
- **`text-box-trim` support levels.** §11 and §13 treat it as recent and needing a fallback. Not
  checked against caniuse or the CSS WG.
- **The ~30% screen-reader heading-navigation figure.** Already flagged in `notes.unverified` in the
  first draft, and it stays there — this pass did not improve it.

## Method note worth carrying to the next brief

**The docs URL in the first draft does not resolve.** `polaris.shopify.com/components/typography/text`
301s to a general API index, and the obvious successor path 404s. The type definition in the repo
answered every question the docs page was cited for.

For an API claim, **read the type, not the page**: a docs page describes intent and can lag or move,
while a shipped interface is what a consumer actually meets. That is the same instinct as this vault's
preference for primary sources, applied one level in.
