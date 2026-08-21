# Claude run — surface context in white-label, multi-brand and owned-code systems (2026-08-20)

Raw output. Every URL opened **2026-08-20**. Quotations verbatim. Counts were taken by me from shipped
files and the commands are shown so they can be re-run.

**This pass extends `2026-08-20-surface-context-modeling` and corrects one of its claims.** That run
characterised the SLDS `:not()` carve-out as an *"exclusion list … maintained by hand"*. Counted
properly here, it is **one component, repeated across 10 selectors** — not a list. The maintenance
argument I built on it was overstated, and §6 restates it at the size it actually is.

---

## 1. Multi-brand and white-label systems

**I sourced one of the seven suggested systems and could not source the other six. Stating that up
front rather than padding the section.** What I did establish is directly responsive to the question
the brief calls the one that matters.

### Telefónica Mística

Genuinely multi-brand: skins ship for **Movistar, Vivo, O2, Telefónica and Blau**
(`github.com/Telefonica/mistica-web`, `doc/theme-config.md`; `github.com/Telefonica/mistica-android`).

Two mechanisms, and **they are different ones**:

- **Brand** is a **JavaScript config object** implementing a typed `Skin` interface. Custom brands are a first-class path: a consumer imports the `Skin` type and creates a new skin config, and can extend an existing skin such as Movistar with custom colour tokens.
- **Colour scheme** is a **DOM attribute** — `data-mistica-color-scheme` — and by default follows the user's system preference, with light/dark forcible via that attribute.

**So the brand layer and the appearance layer do not collide, because they are not the same
mechanism.** Brand is resolved in JS before render; scheme is resolved in CSS at render. That is a
clean separation and it is the single most useful thing this section found.

**What I could not establish:** whether Mística has any *surface/inverse* concept distinct from
light/dark. A direct grep of `src/utils/theme.tsx` on `main` returned **0** matches for "inverse", and
that file path may simply be the wrong one. See COULD NOT VERIFY.

### The other six

Volkswagen Group, Marriott/IHG, Mercado Libre (Andes), Zeta, ING and Santander — **not sourced.** I
did not find primary documentation or public repositories for their surface-context handling within
this pass. I am not substituting blog posts or design-award write-ups. **§1 is therefore a
one-system section, not the seven-system survey the brief asked for.**

---

## 2. Owned-code / theming-first libraries

This is the section the brief weights heaviest and it is the best-evidenced one.

### shadcn/ui — global, class-scoped, no documented nesting

`ui.shadcn.com/docs/theming`.

> "Dark mode works by overriding the same tokens inside a `.dark` selector."

```css
:root { --primary: oklch(0.205 0 0); }
.dark  { --primary: oklch(0.922 0 0); }
```

**The extension contract is documented, which matters for Q5:**

> "To add a new token, define it under `:root` and `.dark`, then expose it to Tailwind with `@theme inline`."

**Nesting is not documented.** The page describes `:root` and `.dark` only. A `.dark` class would in
fact apply to any subtree by ordinary CSS selector semantics, but the library does not say so, and a
consumer building a dark band inside a light page is off-documentation.

### Radix Themes — nesting is a documented, first-class feature

`radix-ui.com/themes/docs/components/theme`. The `Theme` component *"wraps all or part of a React tree
to provide theme configuration."* Props include `appearance` (`"inherit" | "light" | "dark"`),
`accentColor`, `grayColor`, `panelBackground`, `radius`, `scaling`.

Under **Nesting**:

> "Nest another theme to modify configuration for a specific subtree. Configuration is inherited from the parent."

```jsx
<Theme accentColor="cyan" radius="full">
  <Card size="2">
    <Theme accentColor="orange">
      {/* grandchild content */}
    </Theme>
  </Card>
</Theme>
```

**Two things worth pulling out.** `appearance` has an explicit **`"inherit"`** value — the same shape
as the cascade-prop-defaulting-to-inherit that this project already ships on one component, so that
pattern has a major published precedent. And *"Configuration is inherited from the parent"* is the
nesting semantics stated as a contract rather than left to CSS accident.

### StyleX — themes are element-scoped by construction

`stylexjs.com/docs/learn/theming/creating-themes/`. Themes are created with `stylex.createTheme()`
over a variable group and applied through `props()`:

```javascript
<div {...stylex.props(dracula, styles.container)}>{children}</div>
```

> "Any variables that are not overridden will revert back to their default value."

> "If multiple themes for the same variable group are applied on the same HTML element, the last applied theme wins."

**Nesting is inherent** — a theme applies to an element and its descendants, so an inner element
carrying a second theme overrides for its own subtree. Partial override is explicit: unlisted
variables fall back rather than resetting.

### The pattern across all three

**Every owned-code library that supports scoped context implements it the same way: re-declare custom
properties on an element, and let descendants inherit.** shadcn does it globally with a class, Radix
wraps it in a component with documented nesting, StyleX makes the element the unit. None uses a
per-component variant axis for context. **That is a strong convergence and it is option 3.**

**Base Web, Panda CSS and Astryx — not reached.** See COULD NOT VERIFY.

---

## 3. The content-author experience

Neither prior pass covered this, and it turns out to be the most decision-relevant section.

### AEM Edge Delivery Services

`aem.live/developer/block-collection/section-metadata`. The author types a table in a document,
*"an intuitive name/value pair structure where the name is in the first column of the table and the
value is in the second column."*

Treatment of the keys:

- `Style` → *"added as a `class` attribute. You can add multiple classes"*
- `Id` → *"added as an `id` attribute"*
- everything else → `data-*` attributes

So the literal authoring step for an inverted band is: insert a **Section Metadata** block, type
`Style` in the left cell and a style name in the right cell.

**Two findings, and the second is the one that matters.**

**Adobe's own documentation discourages the mechanism:**

> "As `Section Metadata` generally adds complexity for authors, it is recommended to avoid it, until it is really necessary."

**And consumption is undocumented.** Asked directly whether blocks inside the section consume the
resulting class or data attributes, the page yields nothing: *the document does not specify how blocks
or components inside a section consume these resulting class or data attributes.* This corroborates
the earlier pass, which found the same silence on `markup-sections-blocks`. **Publishing is
documented on two pages; consuming is documented on neither.**

### Drupal

Core Layout Builder does not give an author a class field. The idiomatic mechanism is a **contributed
module**, `layout_builder_styles` (`drupal.org/project/layout_builder_styles`), which lets site
builders *"select from a list of styles to apply to layout builder blocks and layout builder
sections"*, where a style is *"a representation of one or more CSS classes that will be applied"*, and
*"Styles and style groups are config entities and can therefore be exported/imported as any other
configuration."*

So the Drupal authoring step is: a **site builder** predefines named styles; a **content author**
picks one from a select list; classes land on the section or block.

### The convergence

**On both platforms the author-facing mechanism is the same act — put a class on a wrapper — chosen
from a set someone technical predefined.** On Drupal it is not even in core. Neither platform passes
structured context; both pass a class and stop.

**INFERRED consequence for a white-label kit:** the client's content author is the person who decides
a band is dark, and the only thing they can hand downward is a class name. A component API that
requires a *developer* to set a `surface` prop is asking the wrong person, at the wrong time, in a
system where the right person has only a class to give.

---

## 4. The unanticipated-surface problem

Thin, and honestly so.

**shadcn/ui is the only surveyed system with a documented "add your own" path** — *"To add a new
token, define it under `:root` and `.dark`, then expose it to Tailwind with `@theme inline`."* That is
an extension point for a **token**, not for a **surface**: it tells a consumer how to add
`--warning`, not how to declare "this band is a photographic hero and here is what components should
do on it."

**Mística's `Skin` interface** is the strongest custom-context path found: a typed contract a consumer
implements to create a brand the system never shipped. Again, brand — not surface.

**I found no system that documents "define your own surface context."** Radix's `appearance` is a
closed enum (`inherit | light | dark`). StyleX comes closest structurally — a consumer can
`createTheme` over an existing variable group for any context they invent, with no enumeration to
extend — but the docs frame that as theming, not as surface context.

---

## 5. Extension and the name surface

**Documented contracts found:** shadcn's two-place token rule above, and Mística's typed `Skin`
interface (a compile-time contract — a custom skin that omits a required token fails to typecheck).

**StyleX's variable group is a contract by construction**: `createTheme` takes a variable group, so a
theme can only override variables that group declares. A consumer cannot invent a variable the system
does not know about and have it participate.

**No ESLint rule or token-usage gate was sourced in this pass.** I know Atlassian publishes an
`eslint-plugin-design-system` — named in the earlier surface-context run from its rule index — but I
did not open a rule page here and will not characterise what it enforces. See COULD NOT VERIFY.

**INFERRED:** across these systems, conformance for a consumer-authored component is enforced by
*type system* (Mística, StyleX) or by *convention* (shadcn), never by a lint rule I could source. For
a white-label kit shipping to clients, a type contract does not survive the eject into a
server-rendered Drupal or EDS project where there is no TypeScript in the render path.

---

## 6. Cost of the token layer — counted

Taken from the shipped compiled SLDS stylesheet (967,467 bytes),
`help.openstax.org/assignable-chat/assets/styles/salesforce-lightning-design-system.min.css`. SLDS is
the closest surveyed system to a white-label model, which is why it is the one worth counting.

Commands, so this is reproducible:

```
grep -o -- "--slds-g-[a-z0-9-]*" slds.css | sort -u | wc -l                      → 455
grep -o -- "--slds-g-[a-z0-9-]*inverse[a-z0-9-]*" slds.css | sort -u | wc -l     → 11
grep -o -- "--slds-c-[a-z0-9-]*" slds.css | sort -u | wc -l                      → 476
grep -o -- "--slds-c-[a-z0-9-]*inverse[a-z0-9-]*" slds.css | sort -u | wc -l     → 21
```

| Layer | Total distinct hooks | Carrying `inverse` | Share |
|---|---|---|---|
| Global (`--slds-g-*`) | 455 | **11** | **2.4%** |
| Component (`--slds-c-*`) | 476 | **21** | **4.4%** |

The 11 global inverse hooks, in full:

```
--slds-g-color-border-inverse-1 / -2
--slds-g-color-on-surface-inverse-1 / -2
--slds-g-color-surface-container-inverse-1 / -2
--slds-g-color-surface-inverse-1 / -2
--slds-g-shadow-inset-inverse-focus-1
--slds-g-shadow-insetinverse-focus-1
```

(The last two are a near-duplicate pair differing only by a hyphen — `inset-inverse` versus
`insetinverse`. I am reporting it as observed; whether it is a typo that shipped or two deliberate
hooks, I did not establish.)

**Only three components carry inverse hooks at all** — `avatar`, `badge`, `button` — derived by
stripping the component segment from the 21 names.

**The correction to my earlier pass.** The `:not()` carve-out is **one component**, `.slds-button--neutral`,
appearing in **10** of the container's selectors. Not an exclusion *list*. The earlier run's
maintenance argument was built on a bigger number than exists.

**INFERRED reading of the shape:** the global inverse layer is small (11) because its job is to
describe *the surface*. The component layer is larger (21) and per-component because its job is to
describe *how a given control behaves on that surface* — a thing 11 surface tokens structurally
cannot say. `--slds-g-color-on-surface-inverse-1` is an ink; it cannot tell a button what its border
does. **The two layers are not the same fact stated twice.**

---

## 7. Falsification, for a white-label system specifically

**What would show the cascade is wrong for a white-label kit — and not merely for a first-party one:**

1. **The client's components do not participate.** A cascade only reaches components that read the published custom properties. A client-authored component that hard-codes a colour sits inside the inverted band unchanged, and **nothing in the shipped kit can detect that**. A first-party system never has this problem because it wrote every component.
2. **The class name is a public API nobody versioned.** If context arrives as `.inverse` on a wrapper, that string is now part of the contract with the client's content authors and their CMS configuration. Renaming it is a breaking change to a surface the token contract does not cover.
3. **The client inverts a surface the tokens cannot describe.** A photographic hero has no single luminance. If the kit's answer is "set the inverse context", the result is legal, resolvable and sometimes unreadable — and the failure lands on the client's page, not ours.
4. **Two platforms, two class mechanisms.** EDS gives a class from a document table; Drupal gives a class from a contrib module's config entity. If the projection has to emit different context plumbing per platform, the "one definition" claim weakens at exactly the point the client sees it.

**What would show a variant axis is wrong for the same case:**

1. **The wrong person is being asked.** §3 establishes that the surface is chosen by a *content author* selecting a style, after the component was built and shipped. A prop requires a *developer* to have known.
2. **It cannot be set at all on EDS.** A block's markup comes from a document. There is no place for an author to type `surface="inverse"` on a button inside a section; the only lever they have is Section Metadata, which is a class.
3. **It ships a decision the client must repeat everywhere.** Every instance inside a dark band needs the prop. Miss one and it is invisible in review and wrong in production — the same failure the cascade has, but distributed across every call site instead of one container.
4. **The matrix cost lands on the client too.** A doubled variant matrix is doubled Figma members in the kit the client rebrands and browses, not just in our repo.

---

## VERIFIED

All accessed 2026-08-20.

- Mística ships skins for Movistar, Vivo, O2, Telefónica, Blau; custom skins via a typed `Skin` interface; colour scheme forced via `data-mistica-color-scheme` — Telefonica/mistica-web `doc/theme-config.md`, Telefonica/mistica-android
- shadcn/ui: *"Dark mode works by overriding the same tokens inside a `.dark` selector"*; the `:root`/`.dark` example; *"To add a new token, define it under `:root` and `.dark`, then expose it to Tailwind with `@theme inline`"* — ui.shadcn.com/docs/theming
- Radix Themes `Theme` props incl. `appearance: "inherit" | "light" | "dark"`; *"Nest another theme to modify configuration for a specific subtree. Configuration is inherited from the parent."*; the two-level nested example — radix-ui.com/themes/docs/components/theme
- StyleX: theme applied via `props()` to an element and its descendants; *"Any variables that are not overridden will revert back to their default value."*; *"If multiple themes for the same variable group are applied on the same HTML element, the last applied theme wins."* — stylexjs.com/docs/learn/theming/creating-themes/
- EDS Section Metadata: name/value table; `Style` → *"added as a `class` attribute. You can add multiple classes"*; `Id` → id; others → `data-*`; *"As `Section Metadata` generally adds complexity for authors, it is recommended to avoid it, until it is really necessary."*; page does not specify how blocks consume the result — aem.live/developer/block-collection/section-metadata
- `layout_builder_styles` is a **contributed** module; styles are *"a representation of one or more CSS classes that will be applied"*; authors *"select from a list of styles to apply to layout builder blocks and layout builder sections"*; styles are config entities — drupal.org/project/layout_builder_styles
- SLDS counts: 455 global hooks / 11 inverse (2.4%); 476 component hooks / 21 inverse (4.4%); inverse component hooks span exactly avatar, badge, button; `:not(.slds-button--neutral)` appears in 10 container selectors — counted from the compiled stylesheet, commands shown in §6

## INFERRED

- That Mística's brand-versus-scheme split is a clean separation of concerns — my reading of two different mechanisms, not a claim Telefónica makes.
- The convergence claim in §2 that all three scoping libraries implement context as element-scoped custom-property re-declaration.
- §3's consequence: the content author is the decider and a class is all they can hand down.
- §6's reading that the 11 global and 21 component hooks do different jobs rather than duplicating one.
- All of §7.
- That a type-system conformance contract does not survive an eject into a server-rendered platform.

## COULD NOT VERIFY

- **Six of the seven suggested multi-brand systems** — Volkswagen Group, Marriott/IHG, Mercado Libre (Andes), Zeta, ING, Santander. No primary source found in this pass for how any of them handles surface context. §1 is one system deep.
- **Whether Mística has an inverse/surface concept distinct from light/dark.** Grepped `src/utils/theme.tsx` on `main`: 0 matches for "inverse". The path may be wrong; this is not evidence of absence.
- **Base Web, Panda CSS, Astryx** — named in the brief, not reached. No claims made.
- **Any ESLint rule or token-usage gate enforcing surface-context conformance.** Atlassian's `eslint-plugin-design-system` exists (rule index seen in the earlier pass) but I did not open a rule page here and will not characterise it.
- **Whether the `--slds-g-shadow-inset-inverse-focus-1` / `insetinverse` pair is a shipped typo** or two intentional hooks.
- **Published token-count tables** for any system's contextual layer. The §6 figures are mine, counted from shipped CSS, because I found none published.

---

## Recommendation

**For a white-label system: option 3 to publish the context, plus a declared per-component response —
and that combination is genuinely different from what I would recommend first-party.**

**First-party**, I would recommend the cascade alone. You design the bands, so you can enumerate the
surfaces, and every component in the page is yours.

**White-label**, the cascade alone is insufficient for a reason §7 makes concrete: you are shipping
into surfaces you have never seen, assembled by someone else, containing components you did not write.
So:

1. **A container publishes context as a class that re-declares custom properties.** This is the only thing both platforms can carry (§3), and it is what every owned-code library converged on (§2).
2. **Each component declares which of its own properties are surface-responsive** — in the definition, so it is data rather than convention. This is the part first-party systems can skip and a white-label kit cannot, because it is the only thing that survives into a client's repo alongside components we did not write.
3. **The context vocabulary is closed and versioned** — surface names are part of the name contract, not an ad-hoc class string, precisely because falsifier 2 says an unversioned class name becomes a breaking change nobody can see.

Point 2 is, deliberately, the shape SLDS arrived at. See below.

## The strongest argument against it

**It is two mechanisms, and eliminating two mechanisms is why this research was commissioned.**

The project's stated problem is three answers shipping at once. My recommendation ends with two, and
asks seventeen components to each declare a surface-response surface — authoring burden across the
whole catalogue for a capability that, in the one system I could count, **only three of its components
actually needed** (§6: avatar, badge, button). That is a real possibility that I am generalising from
SLDS's *architecture* while ignoring SLDS's *usage*, which says most components never needed the second
mechanism at all.

And the cheaper reading is available: if only a handful of components are ever placed on inverse
surfaces, the cascade alone plus per-instance overrides for those few is less machinery than a
catalogue-wide contract — and it is what SLDS's own numbers suggest is sufficient.

## Is the Salesforce Lightning both-mechanisms pattern a defect or an adaptation?

**Adaptation, with one small defect inside it.**

**The adaptation.** The 11 global inverse hooks describe a *surface*; the 21 component hooks describe
*how a specific control behaves on one*. `--slds-g-color-on-surface-inverse-1` is an ink value and
cannot express that a button's border becomes transparent while its outline stays. Those are two
different facts, and a system that ships to organisations building their own pages needs both: the
container declares "this is inverse" without knowing what is inside it, and each component answers
"then I look like this" without knowing what the surface is. **Neither half can be derived from the
other**, which is the test for whether two mechanisms are duplication.

That only 3 of ~40+ components carry inverse hooks supports the reading: this is not a blanket second
system, it is a targeted response added where the surface declaration was not enough.

**The defect** is narrower than I claimed in the previous pass, and I am correcting myself: the
`:not(.slds-button--neutral)` exclusion, appearing in 10 selectors. It exists because the container
rule reaches into descendants to restyle links, and one component had to be exempted. The defect is
not "two mechanisms" — it is **one mechanism reaching past its own boundary**, which forced a carve-out
in the container for a component the container should never have been styling.

**The lesson to take is therefore the opposite of the obvious one.** The problem is not that SLDS has
both a container and component variants. It is that the container does not stay in its lane. A
container that publishes context and paints only itself, with every component responding on its own
terms, needs no exclusion list at all.
