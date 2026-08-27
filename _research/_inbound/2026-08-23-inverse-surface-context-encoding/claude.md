# Claude run — how shipping systems encode inverse / on-emphasis surface context (2026-08-23)

Raw output. Every external claim was fetched during this run; URLs and fetch dates inline. Nothing
here is authoritative until synthesised. **Single-agent run** — see `prompt.md`.

---

## Headline: nobody encodes it this way, and the pattern against us is unanimous

**Four systems checked against primary sources. All four encode appearance as a MODE and surface
context as a NAME SEGMENT. In all four, the component references a different token when the ground
changes.** No system was found that resolves surface context by mode on a pointer tier, and no system
was found splitting Figma collections by axis.

This is the finding the brief asked for and it is the uncomfortable one. Stated plainly for the
developer who will check it: **the majority of the field would have a checkbox on a dark band
reference `fgColor-onEmphasis` / `static-white` / `inverseOnSurface` explicitly, not reference
`color/foreground/primary` and let a mode resolve it.**

Confidence: **high** on the four token-source reads (they are quotes from published token data and
vendor docs). **Medium** on the absence claim — absence is hard to establish, and §6 says exactly how
hard.

---

## The comparison, in one table

| system | is there an inverse / on-emphasis concept? | encoded as | appearance encoded as | **does the binding change?** |
|---|---|---|---|---|
| **Adobe Spectrum** | yes — `static-white` / `static-black` | **name segment** | **`sets`** (`light`/`dark`/`wireframe`) | **YES** |
| **Material 3** | yes — `inverseSurface`, `inverseOnSurface`, `inversePrimary` | **named roles** in `ColorScheme` | schemes (light/dark, dynamic) | **YES** |
| **Primer** | yes — `fgColor-onEmphasis` | **name segment** | modes / 9 themes | **YES** |
| **Carbon** | yes — `$text-inverse`, `$background-inverse`, `$inverse-link` | **name segment** | themes (`white`/`g10`/`g90`/`g100`) | **YES** |
| **Prism3** | yes | **MODE on a pointer collection** | **MODE on a value collection** | **NO — same binding resolves** |

**The structural regularity is the finding, not any single row.** Every surveyed system splits the
two dimensions across two *different mechanisms*: appearance gets the mode/theme/set machinery,
surface context gets the naming machinery. Prism3 is the only one putting both into modes.

---

## 1. Adobe Spectrum — the owner's specific ask

**Settled from the shipped token source, not from docs.** `adobe/spectrum-design-data`,
`packages/tokens/src/color-aliases.json` (fetched 2026-08-23; the older `adobe/spectrum-tokens`
repo now redirects — *"maintained as a placeholder for redirects only"*).

**Appearance is `sets`:**

```json
"accent-background-color-default": {
  "$schema": ".../token-types/color-set.json",
  "sets": {
    "light":     { "value": "{accent-color-900}" },
    "dark":      { "value": "{accent-color-800}" },
    "wireframe": { "value": "{accent-color-900}" }
  }
}
```

**Surface context is a name segment.** Every `static-*` token found is a distinct name:

```
disabled-static-white-background-color   disabled-static-black-background-color
disabled-static-white-border-color       disabled-static-black-border-color
disabled-static-white-content-color      disabled-static-black-content-color
```

plus CSS customs `--spectrum-static-white-focus-indicator-color` /
`--spectrum-static-black-focus-indicator-color`.

**There is no `inverse` set, and no surface-context set of any kind.** The `sets` mechanism carries
appearance only. So a Spectrum component sitting on a coloured/emphasised background **binds to a
different token name** — `static-white-*` — rather than resolving the same name differently.

**Note the asymmetry this creates, because it is the real design consequence:** `static-white` is
*static*. It does not flip with light/dark, which is the point — it is for surfaces whose colour is
fixed regardless of theme (a coloured band, an image overlay). That is a **narrower** concept than
prism3's `inverse` surface, which does flip per appearance. **These are not the same feature**, and
treating Spectrum's `static-*` as the equivalent of our `inverse` would be an error.

**Spectrum Figma variables: NOT VERIFIED — needs a source.** I could not establish from primary
sources whether Spectrum's public Figma library ships variables with modes, or how many collections
it uses. Search surfaced a community Figma file (`Adobe Spectrum Design System`, community file
1211274196563394418) but I did not confirm authorship, currency, or variable structure. **Do not
quote a Spectrum Figma variable structure on the strength of this run.** This is the single biggest
hole relative to the brief's priority 1.

**Adobe AEM / Experience Cloud surfaces: NOT INVESTIGATED.** Out of budget, and flagged rather than
guessed. The brief asked; this run did not answer it.

---

## 2. Material 3

`m3.material.io` role documentation could not be fetched directly (the page returned title-only
content), so this rests on the Compose `ColorScheme` API and the Snackbar specs, fetched 2026-08-23.

`inverseSurface`, `inverseOnSurface` and `inversePrimary` are **named properties of `ColorScheme`**,
sitting alongside `surface`, `onSurface` and `primary`. Light and dark are separate **schemes**.

**The crux is answered explicitly by M3's own component spec.** For Snackbar: *the container uses
`inverseSurface` **or** `surface`, and the action uses `inversePrimary` **or** `primary`.*

That "or" is the whole finding. **The component chooses.** There is no mode under which `surface`
resolves to the inverse value; a component that wants inverse treatment references a different role.

---

## 3. Primer (GitHub)

`primer.style` foundations and `primer/primitives`' `DESIGN_TOKENS_GUIDE.md`, fetched 2026-08-23.

`fgColor-onEmphasis` is a **distinct token name**, and the guide states the pairing as a rule:
**`--bgColor-*-emphasis` must pair with `--fgColor-onEmphasis`.** Emphasis backgrounds are
*"always combined with `fgColor-onEmphasis` tokens for text and icons."*

Light and dark are **colour modes**, across **nine themes**, with values adjusting automatically.

So Primer is the cleanest statement of the majority pattern: **the mode machinery carries appearance;
the naming machinery carries surface context; and the pairing is a documented authoring obligation on
the component author.**

---

## 4. Carbon (IBM)

`carbondesignsystem.com/elements/themes` and the `@carbon/themes` package, plus two GitHub issues,
fetched 2026-08-23.

Themes are `white`, `g10`, `g90`, `g100` — the mode-like dimension. Inverse is **name segments**:
`$text-inverse`, `$background-inverse`, `$inverse-link`.

Carbon is the useful case because **its inverse tokens take different values per theme**, which is
exactly the two-axis problem: `$inverse-link` is `blue-40` on white/g10 (*"inverted background ui
color is dark"*) and `blue-60` on g90/g100 (*"inverted background ui color is light"*)
(carbon issue #3329).

**So Carbon has both axes and resolves them differently: appearance by theme, surface by name.** It
is the closest any surveyed system comes to prism3's problem, and it still splits the mechanisms.

---

## 5. The axis-split question — no precedent found, and one dated source on why

**No system was found that splits Figma variable collections by AXIS.** The documented split is by
TIER (Material / Tokens Studio ref-vs-sys), which the brief already holds and told me not to
re-derive.

**But the problem prism3's split solves is documented, and the community's answer is different.**
Figma forum feature request #49690, *"hierarchical mode dimensions for variables"*, **posted
2026-01-15** (fetched 2026-08-23), describes the cross-product exactly:

> *"Adding one surface means adding two modes. Adding one theme means duplicating all surfaces."*

and describes the workaround people actually use — **merged mode names inside one collection**:
`default/light`, `default/dark`, `prominent/light`, `prominent/dark`. The request asks for
combinations *"defined within the token's value table, not as separate modes cluttering the
collection's mode switcher."*

**Nobody in that thread proposes separate collections per dimension.** That is a genuine negative
data point and it cuts two ways, both worth stating:

- **(a)** prism3 found a workaround the community has not converged on.
- **(b)** there is a reason nobody does it that this run did not find.

**I cannot distinguish (a) from (b) from the evidence, and saying so is more useful than picking.**
A skeptical developer is entitled to ask which, and the honest answer today is that the run does not
know.

---

## 6. The risk this run turned up, which is sharper than the survey

**Figma's own documentation does not describe how modes resolve when a variable aliases a variable in
a different collection that has its own modes.**

`help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables` (fetched 2026-08-23) documents
that objects default to `Auto` mode and *"take on the mode of their parent container… objects
continue up their layer hierarchy until they reach a container with a specified mode."* It says the
mode count per collection *"depends on your plan."* It does **not** state whether multiple
collections' modes can be set independently on one frame, and it does **not** state how a
cross-collection alias resolves.

**Prism3's architecture depends entirely on that behaviour, and the platform does not document it.**
The engine's own measurement (`docs/00-progress.md` #1082, 2560/0 vs 1050/1510) shows it works in
practice — which is evidence of *observed* behaviour, not of a *contract*.

That is the thing to hand the skeptical developer, because it is the one that could actually bite:
not "is this weird" but **"is this guaranteed."** An undocumented platform behaviour can change
without a deprecation notice, and nothing in the emitted artifacts would fail loudly if it did.

---

## 7. The strongest form of the objection, stated fairly

The name-segment approach that four systems ship has a real advantage that this run should not
soften: **it is explicit at the call site.** A developer reading `fgColor-onEmphasis` knows exactly
what they get and can grep for every use. With mode resolution, the same name resolves differently
depending on a cascade the reader cannot see from the binding, and answering "what colour is this"
requires knowing which frame set which mode.

That is a legibility cost, and it is the likely shape of the developer's objection. The counter is
prism3's own #1082 measurement, and the counter is about a different property — **how many bindings
change when a component moves onto an inverse ground** — not about legibility. **Both can be true.**
The trade is: explicit-and-greppable versus context-agnostic-and-unchanged. Neither is free.

---

## 8. What I could not determine

1. **Whether Spectrum ships Figma variables, with how many collections and what modes.** The brief's
   priority 1, unanswered. Needs someone to open the library.
2. **Adobe AEM / Experience Cloud surfaces** — not investigated at all.
3. **Polaris, Fluent, Atlassian** — not reached. Priority 2 is 2/5 covered (Material 3, Primer) plus
   Carbon. **The absence claim in the headline is therefore weaker than it reads**; three unchecked
   systems could each be a counterexample, though the regularity across four makes it less likely.
4. **Whether any system's docs disagree with its shipped tokens.** The brief asked for this
   explicitly as a finding. Spectrum was the only system where I read the shipped token source
   directly, and it agreed with the docs. For the others I read docs and issues rather than token
   files, so a docs/tokens disagreement would not have been visible.
5. **Whether (a) or (b) is true about the axis split** — see §5.
6. **Whether cross-collection mode resolution is a supported contract or observed behaviour** —
   see §6. This is the one I would resolve first.

---

## 9. What this suggests for the vault

**Durable enough for `31-color-systems.md`, and it is an addition rather than a correction.** §1
already records that the `on-*` pair token is universal across seven systems and lists the per-system
names — including Spectrum's `static-white/black`. What §1 does not say, and what this run
establishes, is **how it is encoded**: universally as a NAME, never as a MODE, with the mode
machinery reserved for appearance. That is a second universal in the same place as the first, and it
is the one a system architect needs.

Worth carrying with it: **Spectrum's `static-*` is not equivalent to an `inverse` surface** — it is
static across appearance by design — so §1's list conflates two different concepts under one bullet.
That is a small correction to an existing line, not just an addition.

**And a gap for `09`:** the practice has no stated POV on *when a context axis should be a mode
versus a name*. Every system surveyed chose name; prism3 chose mode; nothing in the corpus says what
decides it. That is exactly the shape `09` exists for.
