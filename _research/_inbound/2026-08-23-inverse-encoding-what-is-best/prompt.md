# Prompt — inverse encoding: what is actually best (run 3)

Run date: 2026-08-23. Third run. **The previous framing is retracted.**

**Single-agent run**, as runs 1 and 2 were.

---

## Framing change

Runs 1 and 2 were scoped to *"is our decision defensible."* This one is scoped to **"what is actually
best,"** and **switching away from what we ship is a fully acceptable conclusion.**

## Answer these five, separately

1. Best and most common practice for **Figma**?
2. Best and most common practice for **developers**?
3. Best and most common practice for the **platforms we target** (web, iOS, Android, React Native,
   Flutter)?
4. **Best DEVELOPER experience**, where "best" means understood with little or no explanation?
5. **Best DESIGNER experience**, by the same standard?

4 and 5 are a new criterion and the most important addition. They are not "which is more powerful" —
they are **"which needs less explaining."**

## The central hypothesis — TEST IT, DO NOT CONFIRM IT

The orchestrator's hypothesis is that inverse splits into two problems the survey has treated as one:

- **ELEMENT-scoped** — "this label sits on a coloured fill." Primer's `fgColor-onEmphasis`, Spectrum's
  `static-*`, M3's `on-primary`. Universally NAME-encoded, including by prism3: the 16 non-flipping
  roles are exactly `text/on-*`, `icon/on-*` and the six `veil/*`.
- **REGION-scoped** — "this whole band has a dark ground." Prism3's 112 flipping roles, mode-encoded.

If that split is real, the 7/7 finding may be partly a category error, and the live question narrows
to region-inverse only.

**TREAT THIS AS SUSPECT.** The orchestrator finds it attractive and has been wrong twice today — once
amplifying a platform risk that did not exist, once on a measurement read through a truncated window.
**An attractive hypothesis from an interested party is exactly what a third run exists to break.** If
the systems do not draw this line, say so plainly; that is the more useful finding.

## The sharpest single test

Material 3 ships **both** an `on-*` family and an `inverse*` family. Find out whether M3 distinguishes
them **by scope** the way the hypothesis predicts, or whether `inverseSurface` is also element-scoped.
**M3's own component specs are the evidence, not its token list.** The Snackbar spec was decisive last
time; find the others. Do the same for any surveyed system shipping two families.

## Priority 3 is the biggest gap — nobody has looked at platforms

Every major target appears to have a native mechanism for "this subtree resolves the same names
differently." Verify each from primary sources and say **how idiomatic** it is, not merely whether it
exists:

- **Android**: `ThemeOverlay` on a view subtree. Believed to be exactly inverse-as-region. Confirm, and
  find whether Material's own guidance recommends it for this.
- **Web/CSS**: custom property scoping under a class or data attribute.
- **Flutter / React Native**: nested `Theme` / provider.
- **iOS**: THE ONE I LEAST TRUST. `UIColor` dynamic providers resolve by trait, and
  `overrideUserInterfaceStyle` does this for light/dark on a subtree — but whether a CUSTOM axis gets
  the same treatment as cleanly is unknown. **If iOS cannot express region-inverse idiomatically, that
  is a serious finding against mode-encoding and I want it stated loudly.**

## A measurable proxy for criteria 4 and 5

Comprehension cannot be surveyed directly, but this can: **how much does each system have to explain
its own mechanism?** Count the explanation each system's OWN documentation needs — words, worked
examples, caveats, "don't do this" warnings. A mechanism needing three paragraphs and two cautions is
worse on criterion 4 than one needing a line, regardless of which is more capable. **Report it as an
observation with the counts, not as a score.**

## Already known — cite, do not re-derive

- 7/7 name-encode inverse and swap the binding (runs 1–2).
- Fluent 2 multiplies it through the name space; Atlassian hand-maintains a warning exception.
- Figma **documents** cross-collection alias resolution (`resolveForConsumer`, `resolvedVariableModes`)
  — the platform risk does not exist.
- Extended collections cannot add modes, so they are not a third option.
- KB `24`: *"brand is a collection axis, not a mode axis… modes fail for brand because brand axes
  multiply rather than compose."* The stated criterion is multiply-vs-compose.
- prism3 #1128: the surface axis **composes** — 112 of 128 roles flip, injectively, identically on
  three brands.
- prism3 #1129: the mode encoding has **no expression in DTCG today** — the pointer tier is hard-aliased
  to `default` with zero inverse leaves. **Criterion 4 currently judges an unimplemented thing.**

## Still open from before, worth one more try

Whether Adobe ships an official Spectrum Figma library with variables, and AEM / Experience Cloud.

## Output

A research run under `_research/_inbound/`. **Answer all five questions separately — do not merge them
into a verdict** — then give one recommendation, which may be *"switch to name-encoding,"* *"keep
mode-encoding,"* or *"the split is real and each is right for its scope."* **State plainly which of the
five criteria your recommendation loses on, because it will lose on some.**

Post the recommendation to prism3 #1128. Open a KB promotion issue for anything durable; do not edit
the numbered file in the same run.
