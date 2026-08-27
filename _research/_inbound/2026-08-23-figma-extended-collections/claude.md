# Claude run — extended collections, the alias-resolution claim, and the last three systems (2026-08-23)

Raw output. Every external claim was fetched during this run; URLs and fetch dates inline. Nothing
here is authoritative until synthesised. **Single-agent run** — see `prompt.md`.

---

## Headline, and it starts with a correction to my own previous run

**I was wrong about the biggest risk I reported.** The first run concluded that Figma does not
document how a cross-collection alias resolves when two collections' modes are set independently, and
told the owner to hand that to a skeptical developer as *"observed behaviour, not a contract."*

**It is documented, with a worked example, in the plugin API.** I searched the Help Center and stopped
there. The contract lives in `developers.figma.com`, and it says exactly what prism3 needs it to say:

> **`resolveForConsumer`** — *"If that value is an alias, then the resolved value is determined using
> the selected modes of **each collection in the alias chain**."*

**The risk I reported does not exist.** That correction matters more than anything else in this run,
because the previous run's advice would have sent the owner into a developer conversation conceding a
weakness that is not there.

And on the new thread: **extended collections are real, shipped, and are not a third option for this
problem** — because an extension *cannot add a mode*, which is precisely what a second axis requires.

Confidence: **high** on both, they are quotes from Figma's own API reference. **High** on the three
new systems. **Spectrum's Figma variables remain unverified** — see §4.

---

## 1. Extended collections — what they are, and why they do not solve this

**Shipped November 2025.** REST API fields documented 2025-11-18; plugin API update 121 dated
2025-11-20. **Enterprise plan only** (Figma Help Center, *"Available on the Enterprise plan"*). All
fetched 2026-08-23.

**Figma's own framing is theming, not axes.** The plugin API type description: an
`ExtendedVariableCollection` *"extends `VariableCollection` to enable **theming** by inheriting modes
and variables from a parent collection, with the ability to override specific variable values."*

### The decisive constraint

Figma Help Center, *Extend a variable collection*:

> *"An extended collection's mode and variable names, settings, and order are inherited from the
> parent collection."*
>
> **"You cannot add additional variables or modes, or change a variable's description or scope from an
> extended collection."**

Confirmed by the plugin API type, where `modes` is `readonly` and each entry carries a
`parentModeId` — *"The modes inherited from the parent collection"* — i.e. a 1:1 correspondence with
the parent's modes, not a new set.

**So an extension is a VALUE-override along the parent's existing axis.** The override map is keyed
that way explicitly:

```ts
variableOverrides: { [variableId: string]: { [extendedModeId: string]: VariableValue } }
```

REST API: *"The outer map is keyed by `variableId`, and the inner map is keyed by `modeId`."*

### Why that answers the owner's question in the negative

Prism3's `surface` is a **second dimension that must compose with appearance** — four appearances ×
two surfaces. An extension **cannot add a mode**, so it cannot introduce that dimension. What it can
do is produce a whole parallel copy of a collection with some values overridden, along the *same*
modes.

Modelling inverse as an extension would therefore mean *"the inverse variant of the entire colour
system"*, selected wholesale — not *"this band is inverse while the page around it is not"*, which is
the thing prism3's surface mode actually does.

**Extended collections are a brand/theme mechanism.** They are the right tool for *"brand A's primary
is green, brand B's is red"* — which is exactly the example Figma and its ecosystem use.

### The question Figma does not answer

**How a layer or designer SELECTS an extension rather than its parent is undocumented.** Checked, all
2026-08-23:

- Help Center *Extend a variable collection* — describes publishing and reapplying modes; does not
  state whether selection is per-frame, per-file or library-scoped.
- Plugin API `ExtendedVariableCollection` — data structure only; *"does not explain how consumers or
  layers select between an extension and its parent."*
- REST API variables types — override map only; nothing on consumption.

There is a reasonable inference available (an extension presumably appears as its own collection in a
node's mode map, making it per-frame selectable), **and I am not making it**, per the brief. It is
undocumented, and that is the finding.

**One caveat on how much this matters:** because an extension cannot add a mode, even the most
favourable answer to the selection question would not give prism3 the composing surface axis. The
selection gap is worth recording, but it is not load-bearing for this decision.

---

## 2. The alias-resolution claim — RESOLVED, against my previous finding

All from `developers.figma.com`, fetched 2026-08-23.

**`resolvedVariableModes`** — type `{ [collectionId: string]: string }`, defined as *"The resolved mode
for this node **for each variable collection in this file**."* The published example shows two
collections resolved on one node simultaneously:

```js
// { 'VariableCollectionId:1:2': '1:1', 'VariableCollectionId:1:3': '1:2' }
console.log(childFrame.resolvedVariableModes);
```

and inheritance is stated: *"The set of resolved modes on a node includes the explicitly set modes on
the node, as well as the explicitly set modes on **ancestors** of the node."*

**`explicitVariableModes`** — same map type, *"The explicitly set modes for this node."*

**`setExplicitVariableModeForCollection`** — sets a mode for one collection on a node, taking a
collection object.

**`resolveForConsumer`** — the one that settles it:

> *"If that value is an alias, then the resolved value is determined using the selected modes of **each
> collection in the alias chain**."*

with a documented example producing **four outcomes from two collections × two modes each**.

**That is prism3's architecture, documented by the vendor, with a worked example.** Two collections'
modes are set independently on one node; an alias across the boundary resolves using both.

### Why I got it wrong, recorded because the method error is the reusable part

The first run searched the **Help Center**, which is written for designers and genuinely does not
cover this. The **plugin API reference** is written for implementers and does. I concluded "Figma does
not document it" from one surface's silence.

**A vendor's documentation is not one corpus.** Help Center, plugin API, REST API and changelog have
different audiences and different completeness, and an absence in one is not an absence. The durable
rule: **before reporting something as undocumented, name which surfaces were checked** — which is what
the brief asked for this time, and is why the error was caught in one round.

---

## 3. The last three systems — the survey now covers seven

All fetched 2026-08-23.

**Polaris (Shopify)** — `text-inverse` and `text-inverse-secondary` are **tone values on the `Text`
component**, i.e. distinct token names selected by the component. Binding changes. ✅ name-encoded

**Atlassian** — `color.text.inverse`, *"designed for use on bold filled backgrounds"*, with inverse
variants for text, borders and icons. Binding changes. ✅ name-encoded

> **And the most interesting single detail in this run's survey half:** Atlassian carries an
> **exception** — warning backgrounds use `color.text.warning.inverse` instead of the general
> `color.text.inverse`. **Name-encoding needs hand-maintained special cases** where one ground behaves
> differently from the rest. That is a maintenance cost the first run did not have evidence for.

**Fluent 2 (Microsoft)** — `NeutralForegroundInverted` with **Rest / Hover / Pressed / Selected**
states, plus `NeutralForegroundInvertedLink` and `NeutralForegroundInvertedDisabled`. Binding changes.
✅ name-encoded

> **This is the clearest evidence of what name-encoding costs at scale:** the inverse dimension
> **multiplies through the name space**. Every state and every variant that needs an inverted form
> gets its own name. That is the cost the engine lane is measuring internally, visible in a shipped
> system.

### The full picture, seven systems

| system | surface context | appearance | binding changes? |
|---|---|---|---|
| Spectrum | `static-white` / `static-black` — **name** | `sets` (light/dark/wireframe) | yes |
| Material 3 | `inverseSurface`, `inversePrimary` — **named roles** | schemes | yes |
| Primer | `fgColor-onEmphasis` — **name** | modes, 9 themes | yes |
| Carbon | `$text-inverse`, `$inverse-link` — **name** | themes | yes |
| **Polaris** | `text-inverse` — **name** | — | **yes** |
| **Atlassian** | `color.text.inverse` (+ warning exception) — **name** | themes | **yes** |
| **Fluent 2** | `NeutralForegroundInverted*` — **name** | themes | **yes** |
| Prism3 | **mode on a pointer collection** | mode on a value collection | **no** |

**Seven of seven name-encode surface context. #27's caveat resolves: the claim covers seven systems,
not four.**

---

## 4. What remains unverified

**Whether Adobe publishes an official Spectrum Figma library with variables.** Still open after two
runs, and I want to be precise about the state of the evidence rather than let it drift into a claim:

- `spectrum.adobe.com/page/ui-kits/` **could not be read** — the site is a JS application and returns
  title-only content to a fetch. The same failure hit `/page/color-system/` in the first run.
- Search results indicate Adobe's UI kits are published as **XD** files covering both scales and all
  colour themes, and that the Spectrum Figma files in the community are **third-party**. I did not
  confirm authorship or currency of any of them.

**So: not established either way.** Searches run across both sessions: *"Adobe Spectrum Figma library
variables modes collections"*, *"Spectrum 2 Figma variables released"*, *"Adobe Spectrum 2 official
Figma UI kit variables collections modes"*. Someone with Figma access can settle it in a minute; a
fetch cannot.

**Note what is NOT unverified:** Spectrum's *token* encoding was read directly from shipped token JSON
in the first run (`adobe/spectrum-design-data`, `packages/tokens/src/color-aliases.json`), so
priority 3's *"tokens not docs"* requirement is met for Spectrum, and docs and tokens **agreed**.
For Polaris, Atlassian and Fluent this run read documentation rather than token files, so a
docs/tokens disagreement there would still not have been visible.

**Also still not investigated:** Adobe AEM / Experience Cloud surfaces. Asked in the first brief,
unanswered in both runs.

---

## 5. What this changes for the decision

Three things, in order of how much they move it.

1. **The exposure the first run reported is gone.** Cross-collection alias resolution is a documented
   contract with a published example, not observed behaviour. The mode-encoded architecture does not
   carry the platform risk I attributed to it.
2. **Extended collections are not an option here.** They cannot add a mode, so they cannot carry a
   composing axis. Worth knowing so the decision is not deferred waiting for a feature that does not
   do this. They *are* the right mechanism for multi-brand value overrides, which is a different
   question prism3 may face later.
3. **The survey's verdict is unchanged but its cost evidence is stronger.** Seven of seven still
   name-encode — the field consensus is real and a developer citing it is citing something true. But
   Fluent's multiplied name space and Atlassian's warning exception are the first concrete evidence of
   what that consensus *costs* to maintain, and both point at the quantity the engine lane is
   measuring.

**What this run does not do is decide it.** The internal measurement — how many of 128 pointer roles
actually flip, and how many variants name-encoding adds — is still the thing that should. This run
removes a false risk from one side of the scale and adds two cost data points to the other.

---

## 6. For the vault

**Promotes into `31-color-systems.md` §1**, extending the promotion already filed as #27:

- The encoding universal now rests on **seven** systems, not four. #27's scoping caveat can be
  dropped.
- Add the **cost** evidence, which is new and is the part a practitioner can act on: name-encoding
  multiplies through the name space (Fluent's inverted × state × variant) and needs hand-maintained
  exceptions (Atlassian's warning ground).
- The `static-*` correction from #27 stands unchanged.

**Does not change `09` gap #28** — *when should a context axis be a mode versus a name* is still open,
and this run sharpens rather than answers it. The mode option is now known to be *supported*; that
removes an argument against it without supplying one for it. The gap's third candidate discriminator
(*is the axis set by the component or by its container*) is untouched and still the best starting
point.
