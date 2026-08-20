# Claude run — how should a design system model surface context (inverse / on-color)? (2026-08-20)

Raw output. Every URL below was opened during this run on **2026-08-20**. Quotations are verbatim;
where I paraphrase I say so. Classification of each system into options 1–4 is my reasoning, not the
system's own words, and is labelled INFERRED at the end.

**Two environment limits that shaped what could be sourced**, stated up front because they explain
gaps rather than excuse them: `carbondesignsystem.com` and `archive-1_0_5.lightningdesignsystem.com`
would not resolve from this environment ("Unable to verify if domain … is safe to fetch"). For both
systems I went to shipped source instead, which the brief's own rule prefers anyway.

---

## 1. Field survey

### Adobe Spectrum — a **component prop**, and it names the INK, not the surface

`react-spectrum.adobe.com/react-spectrum/Button.html`

> **Prop name:** `staticColor` · **Allowed values:** `'white' | 'black'`
> "The static color style to apply. Useful when the button appears over a color background."

**This is a fifth option, not option 1.** A variant axis called `surface: default | inverse` tells the
component *what it is standing on* and leaves it to resolve the ink. `staticColor` tells the component
*what colour to be* and leaves the surface entirely undescribed. The distinction is load-bearing for a
token-driven system: `staticColor` cannot be resolved from tokens, because "white" is not a role — it
is an escape from the role system for the case where the background is an arbitrary image and no token
can know its luminance.

### IBM Carbon — a **container that emits a class**, and inverse is folded into the theme axis

`raw.githubusercontent.com/carbon-design-system/carbon/main/packages/react/src/components/Theme/index.tsx`

Props: `as`, `className`, `children`, and `theme` with options `'white' | 'g10' | 'g90' | 'g100'`. It
renders:

```js
className = cx(customClassName, {
  [`${prefix}--white`]: theme === 'white',
  [`${prefix}--g10`]: theme === 'g10',
  [`${prefix}--g90`]: theme === 'g90',
  [`${prefix}--g100`]: theme === 'g100',
  [`${prefix}--layer-one`]: true,
});
```

and wraps children in `ThemeContext.Provider` and `LayerContext.Provider`.

**Carbon has no "inverse" concept at all — a dark band is `<Theme theme="g100">`.** That is option 3
and option 4 at once: a container publishes context (a class + React context), and the thing it
publishes is a *theme*, the same axis as light/dark. There is no separate surface axis to cross with
anything, which is precisely how Carbon avoids the combinatorics the brief worries about in option 4.

Note the `--layer-one` class shipping unconditionally: Carbon's answer to nesting is a separate
**layer** concept, not a second inversion.

### Salesforce Lightning — **both patterns, shipping simultaneously**

Read from the compiled `salesforce-lightning-design-system.min.css` (967 KB) as served at
`help.openstax.org/assignable-chat/assets/styles/salesforce-lightning-design-system.min.css`. This is
shipped build output, not documentation.

Container classes present: `.slds-theme_inverse` (16 occurrences), `.slds-theme--inverse` (16),
`.slds-theme_alt-inverse` (8).

Component-level inverse variants present: `.slds-button_inverse` (18), `.slds-dropdown_inverse` (8),
`.slds-spinner_inverse` (6), `.slds-text-color_inverse` (2), `.slds-badge_inverse` (1),
`.slds-avatar-grouped_inverse` (1).

**So the single most-deployed enterprise design system has exactly the inconsistency that prompted this
research, at scale, in production.** That is worth more than any prose recommendation any of these
systems publish.

**And the container class is not a cascade.** Its entire rule body paints itself:

```css
.slds-theme_inverse{color:var(--slds-g-color-neutral-base-100,#fff);
  background-color:var(--slds-g-color-brand-base-10,#001639);
  border-color:var(--slds-g-color-brand-base-10,#001639)}
```

The **only** descendant selectors it carries anywhere in the stylesheet are for links:

```css
.slds-theme_inverse a:not(.slds-button--neutral){color:var(--slds-g-color-neutral-base-100,#fff);text-decoration:underline}
```

— plus `:link`, `:visited`, `:hover`, `:focus`, `:active` and `[disabled]` variants of the same
selector, and nothing else. **The `:not(.slds-button--neutral)` is the finding**: a hand-written
exclusion for the one component that must not invert, compiled into the container's own rule. That is
the partial-inversion failure mode of question 2, visible in shipped CSS.

By contrast the component variant works by **re-declaring custom properties on itself**:

```css
.slds-button_inverse{ … --slds-c-button-color-background:var(--slds-c-button-inverse-color-background, var(--sds-c-button-inverse-color-background, transparent));
  --slds-c-button-color-border:var(--slds-c-button-inverse-color-border, …) }
```

### Shopify Polaris — **tokens only; no component prop**

Token family, from `polaris-tokens/src/themes/base/color.ts`: `bg-fill-inverse`, `bg-fill-inverse-hover`,
`bg-fill-inverse-active`, `bg-inverse`, `bg-surface-inverse`, `border-inverse`, `border-inverse-hover`,
`border-inverse-active`, `icon-inverse`, `text-inverse`, `text-inverse-secondary`, `text-link-inverse`.

But `polaris-react/src/components/Button/Button.tsx` exposes no inverse anything:

```ts
tone?: 'critical' | 'success';
variant?: 'plain' | 'primary' | 'secondary' | 'tertiary' | 'monochromePlain';
```

**A complete inverse token family with no component API to reach it.** The nearest thing is
`monochromePlain`, which takes its colour from surrounding text rather than from a surface declaration
— a cascade-flavoured answer expressed as a variant value.

### GitHub Primer — **tokens only**

`primer.style/foundations/primitives/color` lists `--fgColor-onEmphasis` and `--fgColor-onInverse`
(both `#ffffff` in the active theme). The page carries no usage prose for them and no container or
data-attribute mechanism; it notes only *"This page only shows colors in the site's active theme
('light' or 'dark')."*

### Material Design 3 — **three token roles, no component surface**

From `material-components/material-web/tokens/_md-sys-color.scss`, the complete set of inverse system
roles is exactly three: `inverse-surface`, `inverse-on-surface`, `inverse-primary`. `m3.material.io`
renders client-side and returned only a page title to this run, so the *guidance* around those roles is
unverified — but the token surface itself is source-confirmed and it is small.

### Microsoft Fluent 2 and Atlassian — not established

See COULD NOT VERIFY.

### Classification

| System | Mechanism | Option |
|---|---|---|
| Spectrum | `staticColor="white" \| "black"` on the component | **5th** — names the ink, not the surface |
| Carbon | `<Theme theme="g100">` → class + React context | **3 + 4** — inverse *is* the theme axis |
| SLDS | `.slds-theme_inverse` container **and** `.slds-button_inverse` variant | **1 and 3 simultaneously** |
| Polaris | inverse token family, no component prop | **4-ish** — token layer only |
| Primer | `--fgColor-onEmphasis` / `--fgColor-onInverse` | **4-ish** — token layer only |
| Material 3 | 3 sys roles | **4-ish** — token layer only |

**The disagreement is the result.** Three systems put it only in tokens and give the component author
nothing; one makes it a theme; one ships both a container and per-component variants; one refuses the
surface framing entirely and names the ink. There is no convergent field answer to adopt.

---

## 2. The container-cascade pattern, mechanically

**What SLDS actually does** (above): the container class paints *itself* and carries one hand-written
descendant rule for links, with a `:not()` carve-out for a button variant. It does **not** re-declare a
palette that arbitrary descendants read.

**What Carbon actually does**: a class plus React context. The class is the CSS channel; the context is
the JS channel, and Carbon ships both because a class alone cannot tell a component *in JavaScript*
what theme it is in.

**The documented failure modes, from evidence rather than speculation:**

- **Partial inversion needs a hand-written exclusion.** `.slds-theme_inverse a:not(.slds-button--neutral)` is exactly that, compiled in. Every component that must *not* invert costs a `:not()` in the container's rule — and that list is maintained by hand, in the container, far from the component it names.
- **A class cannot reach JavaScript.** Carbon shipping `ThemeContext.Provider` beside the class is the evidence: if a component needs to *branch* on surface (choose an icon, pick a chart palette), CSS custom properties do not carry that. On a server-rendered platform there is no context provider to fall back on.
- **Nested inversion is unsolved in the systems examined.** Carbon's answer is a *different* concept (`--layer-one`), not a second inversion. I found no system documenting inverse-inside-inverse.

---

## 3. The platform question — AEM EDS and Drupal SDC

**This is the question with the cleanest answer, and both platforms give the same one.**

### AEM Edge Delivery Services — yes, a container mechanism exists, and it publishes a CSS class and nothing else

`aem.live/developer/markup-sections-blocks`:

> "The names of the data attributes can be chosen by the authors, and the only well-known section
> metadata property is `Style` which will be turned into additional CSS classes added to the
> containing section element."

and:

> "Blocks and default content are always wrapped in a section, even if the author doesn't specifically
> introduce section breaks."

So an author writing `Style: dark` in a Section Metadata block produces a section `<div>` carrying that
class, wrapping every block inside it. That is idiomatic, author-controlled, and requires no component
to declare anything.

**But the same page does not address propagation.** It says only that development involves *"usually
not much interaction with sections beyond CSS styling"* and gives no guidance on how blocks respond to
a section's classes, and no example markup for the mechanism. **Stated plainly, as the brief asks: EDS
has an established way for a container to publish context, and no established pattern for a component
to consume it. The consumption is whatever CSS you write.**

### Drupal SDC — no

`drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml`.
Props are explicit, declared in `component.yml`, JSON-Schema shaped:

> "Props are always an object with keys. Each key is a variable in your component template."

> "If your component has required properties, you list them here."

**The page documents no mechanism for implicit context from a parent component.** Everything is an
explicitly declared, validated prop. I looked for a context/inheritance concept and found none on that
page.

### The convergence, which is the actual finding

**On both primary delivery platforms the only ambient channel from a container to a descendant is the
CSS cascade.** EDS gives you a class on a wrapper. SDC gives you explicit props and nothing implicit.
Neither passes a prop down without the component declaring it, and neither has a React-style provider.

That cuts hard against option 1 in one specific way worth stating: **on EDS the surface is chosen by a
content author in a spreadsheet, after the component was built.** A variant axis requires the component
instance to know its surface at authoring time — which, in a document-authored section, it does not.

---

## 4. Figma: is inverse a mode?

`help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables`:

> "The number of modes you can create per variable collection depends on your plan"

The article's own examples of what modes are for:

> "Create accessible color themes, like high contrast mode or different themes for color blindness, using color variables"

> "Account for multiple device sizes, like watch, mobile, and desktop, to see how elements respond to varying spacing and padding sizes"

**Two things I could not establish and one thing that follows.** The numeric per-plan mode ceilings are
not on that page and not on the general variables guide (see COULD NOT VERIFY). And I found no
published design system documenting Figma modes used for *surface context as distinct from
light/dark*.

What does follow from the docs I did read: Figma's own framing treats a collection's modes as **one
axis** (theme, or device size), and the multi-axis case is not addressed. The standard way to avoid two
axes multiplying is therefore to put them in **separate collections**, one axis each, since a frame
resolves a mode per collection independently — but that is my inference from the single-axis framing,
not something the page states.

---

## 5. Cost and regret

**I could not find a public record of a team regretting a surface variant axis and migrating away, and
I am reporting that as a null result rather than filling it.** See COULD NOT VERIFY for what I looked
for.

What the evidence *does* support, without needing a regret narrative:

- **SLDS's `:not(.slds-button--neutral)` is a cost record.** It is the maintenance tax of the cascade approach written into shipped CSS: one exclusion per component that must resist the container.
- **Carbon's `--layer-one`** shipping on every `<Theme>` is a cost record of the same kind for nesting — a second concept was needed because inversion did not compose with itself.
- **Polaris's stranded token family** — a complete inverse palette with no component prop that reaches it — is the cost of option 4 alone: the tokens exist and a component author cannot use them without hand-writing overrides per instance, which is the third of the three behaviours the brief says this project already has.

---

## 6. Accessibility

`w3.org/WAI/WCAG22/Understanding/non-text-contrast.html`, SC 1.4.11:

> "The visual presentation of the following have a contrast ratio of at least 3:1 against adjacent color(s):"

and, decisively for this decision:

> "For user interface components 'adjacent colors' means the colors adjacent to the component."

**So yes — surface context changes what the component must guarantee, and it does so by definition
rather than by convention.** The requirement is *relational*: the obligation is stated against adjacent
colours, and the surface is one of the adjacent colours. A control that clears 3:1 on the default
surface has no inherited claim to clearing it on an inverse one. The contrast contract is a property of
the *pair*, and a component API that cannot name the surface cannot state the pair.

On focus indicators specifically, the Understanding text is weaker than the brief's premise assumes:

> "the visual focus indicator for a component must have sufficient contrast against the adjacent background when the component is focused"

but the normative text **does not specify what a focus indicator must contrast against** — it defers to
the general "adjacent color(s)" language, which varies with whether the indicator sits inside, outside,
or across the component boundary. That ambiguity is exactly the three-colour relationship the brief
describes, and WCAG does not resolve it for you.

I did not find published guidance specific to focus indicators over **image** backgrounds.

---

## 7. Falsification

**What would show the cascade (option 3) is wrong:**

1. **A component needs to branch in code, not just repaint.** If a chart must choose a different series palette, or a logo must swap asset, custom properties cannot carry that on a server-rendered platform with no context provider. Carbon shipping `ThemeContext` beside its class is the field's admission of this limit.
2. **The exclusion list grows.** If, like SLDS, more than a couple of components must *resist* the container, the `:not()` list becomes a hand-maintained registry in the wrong file — and one nobody can gate.
3. **Figma cannot express it.** If the design kit ends up with an inverse *variant* on components while code has none, the two libraries have different component APIs, and Code Connect maps one to the other by hand.
4. **The definition cannot see it.** For this project specifically: a context that lives only in CSS is invisible to a def, so nothing checks that an inverse pairing meets 1.4.11. That is the "wrong value that resolves" class — it renders, and it is under-contrast.

**What would show the variant axis (option 1) is wrong:**

1. **The surface is chosen after the component is built.** On EDS the section style is authored in a spreadsheet by a content author. A prop the developer must set cannot express a decision made downstream of the developer.
2. **Combinatorics.** A component already at 648 Figma members doubles. If more than a few components need it, the kit becomes unusable before the code does.
3. **It has to be threaded.** Every intermediate wrapper has to pass `surface` down, which is the prop-drilling problem the cascade exists to solve — and on SDC, *every* level must declare it in `component.yml`.
4. **Nesting is expressible but wrong.** A prop lets a light card inside a dark band be authored as `surface="default"` — and equally lets an author forget, producing a legal, resolvable, under-contrast component.

---

## VERIFIED

All accessed 2026-08-20.

- Spectrum Button `staticColor: 'white' | 'black'`, "Useful when the button appears over a color background" — react-spectrum.adobe.com/react-spectrum/Button.html
- Carbon `Theme` props `'white' | 'g10' | 'g90' | 'g100'`, emits `${prefix}--{theme}` + `${prefix}--layer-one`, wraps `ThemeContext.Provider` + `LayerContext.Provider` — carbon `packages/react/src/components/Theme/index.tsx`
- SLDS ships container `.slds-theme_inverse` / `.slds-theme--inverse` / `.slds-theme_alt-inverse` **and** component `.slds-button_inverse`, `.slds-dropdown_inverse`, `.slds-spinner_inverse`, `.slds-text-color_inverse`, `.slds-badge_inverse`, `.slds-avatar-grouped_inverse` — compiled SLDS stylesheet
- `.slds-theme_inverse` paints itself; its only descendant rules target `a:not(.slds-button--neutral)` — same source
- `.slds-button_inverse` works by re-declaring `--slds-c-button-color-background` / `-border` — same source
- Polaris inverse token family (12 names listed above) — `polaris-tokens/src/themes/base/color.ts`
- Polaris Button exposes `tone?: 'critical' | 'success'` and `variant?: 'plain' | 'primary' | 'secondary' | 'tertiary' | 'monochromePlain'`, no inverse — `polaris-react/src/components/Button/Button.tsx`
- Primer `--fgColor-onEmphasis`, `--fgColor-onInverse` — primer.style/foundations/primitives/color
- Material 3 inverse sys roles are exactly `inverse-surface`, `inverse-on-surface`, `inverse-primary` — material-web `tokens/_md-sys-color.scss`
- EDS: Section Metadata `Style` → "additional CSS classes added to the containing section element"; blocks always wrapped in a section — aem.live/developer/markup-sections-blocks
- SDC: props explicit and schema-declared, required list documented; no implicit-context mechanism on the annotated component.yml page — drupal.org
- Figma: modes per collection "depends on your plan"; documented use cases are themes, localization, device sizes — help.figma.com Modes for variables
- WCAG 1.4.11: "3:1 against adjacent color(s)"; "For user interface components 'adjacent colors' means the colors adjacent to the component" — w3.org WCAG22 Understanding

## INFERRED

- The classification table in §1 — my mapping of each system onto options 1–4, not their words.
- **Spectrum's `staticColor` is a fifth option**, distinct from a surface axis because it names the ink and never describes the surface. My reading of the prop's values and its stated purpose.
- **Carbon has no inverse concept, only a theme axis** — inferred from `Theme` accepting only the four global theme names and from the absence of any inverse prop in that component.
- Separate Figma collections as the way to keep two mode axes from multiplying — inferred from Figma's single-axis framing; the page does not say it.
- SLDS's `:not()` carve-out as evidence of the partial-inversion failure mode — my reading of a compiled selector.
- The EDS "surface chosen after the component is built" argument — follows from Section Metadata being author-controlled, but Adobe does not frame it this way.

## COULD NOT VERIFY

Specific about what was searched, per the brief.

- **Figma's numeric mode ceilings per plan.** Two Figma help articles opened (Modes for variables; Guide to variables in Figma). Both say limits depend on plan; neither gives numbers. **The commonly-cited "40 modes on Enterprise" figure is not something I confirmed and I have not repeated it as fact.**
- **Whether any published design system uses Figma modes for surface context distinct from light/dark.** Searched; nothing established. This may exist and I did not find it.
- **Microsoft Fluent 2** — not reached in this run. No claim made.
- **Atlassian Design System** — attempted `atlassian/design-system` raw token-names path; 404. No claim made.
- **Any public record of regret over a surface variant axis** (changelogs, RFCs, migration guides, talks, issues). Looked; found none. **A null result, not evidence of absence** — this is the weakest section of the report.
- **Any public record of a cascade approach failing at scale.** Same; the SLDS `:not()` is inferred cost, not a reported failure.
- **Material 3's guidance prose** for its three inverse roles — m3.material.io renders client-side and returned a title only. The token names are source-verified; the usage guidance is not.
- **Carbon and archived SLDS documentation** — both domains refused to resolve from this environment. Findings for both systems come from shipped source instead.
- **Published guidance on focus indicators against image backgrounds.** Not found.

---

## Recommendation

**Option 3 as the mechanism, option 4 as the representation, and explicitly not option 1 — with one
thing option 3 alone does not give you, added deliberately.**

1. **Components declare nothing.** No `surface` axis, no `inverse` appearance value. The variant matrix does not double, and the component API does not describe a decision made downstream of it.
2. **A container publishes context as a class that re-declares the component-facing custom properties.** On EDS that class is what Section Metadata `Style` already produces — the mechanism exists and content authors already drive it. On SDC it is a class on the wrapper component's root. This is the only ambient channel both platforms have.
3. **In Figma, surface is a mode on its own collection**, separate from light/dark, so the two axes resolve independently per frame rather than multiplying inside one collection.
4. **The one addition:** a component that must *resist* inversion declares that in its definition, not in the container's CSS. SLDS's `:not(.slds-button--neutral)` is the counter-example — an exclusion list living in the wrong file, maintained by hand, checkable by nothing. Make it a field on the component so the projector emits the carve-out and a gate can assert it in both directions.

The deciding evidence is §3, not §1. The field genuinely disagrees, so it cannot settle this. The
platforms agree, and they agree on CSS.

## The strongest argument against my own recommendation

**A cascade is invisible to the definition, and this project's entire thesis is that the definition is
checkable data.**

Every gate in this system compares two independently-authored halves and fails when they disagree. A
surface context that exists only as a class on an ancestor is authored in one place, consumed in
another, and *related to the component by nothing a gate can read*. Nothing can assert that a button on
an inverse band clears 1.4.11 — because nothing in the button's definition knows the band exists. That
is precisely the failure class this repo has been burned by repeatedly: a value that resolves, renders,
and is wrong.

Option 1 does not have that problem. A `surface` axis is *legible to the machinery*: the contrast
contract becomes a pairing the engine can enumerate and verify, per surface, at build time — exactly
what it already does for light/dark. The combinatorial cost is real and measurable; the verification
gap in option 3 is real and **not** measurable, which is worse.

And Figma makes it sharper. A cascade is inexpressible in a Figma library, so the design kit would grow
a surface *variant* the code library does not have. Two component APIs, reconciled by hand, is the
structural divergence the brief itself flags — and I am recommending accepting it.

I hold the recommendation because the platform evidence is strong and the author-time argument is
decisive on EDS. But if the project weighs verifiability over platform fit — which its own history
suggests it might — option 1 is the defensible choice, and I would not call that wrong.

## What to measure to settle it

Five numbers, all cheap, none of which anyone appears to have published:

1. **How many components actually need inverse?** If it is 6 of 18, a prop is affordable. If it is all of them, the cascade wins on cost alone.
2. **How many must RESIST it?** SLDS needed at least one carve-out. If our number is 0–1, the cascade's exclusion problem is theoretical; if it is 6, it is the dominant cost.
3. **Does any real page nest inversions** — a light card inside a dark band? If never, nesting can be declared out of scope and option 3 gets much cheaper. If it happens on the first real page, Carbon's need for a second concept (`--layer-one`) predicts the cost.
4. **What is the actual Figma member growth** on the 648-member component if surface becomes an axis? Measure it rather than assuming it doubles — it doubles only if surface crosses every existing axis.
5. **Who sets the band — a developer or a content author?** On EDS, instrument how often Section Metadata `Style` is set by someone who is not the component's developer. If it is usually the author, option 1 is answering a question the wrong person is being asked.
