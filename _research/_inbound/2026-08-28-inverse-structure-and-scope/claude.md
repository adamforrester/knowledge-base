# Claude run — inverse/emphasis token structure and scope (2026-08-28)

Raw output. **Single-agent run.** Every claim below is tagged with where it came from.
Sourcing tiers used throughout:

- **[SOURCE]** — read directly out of a shipped token artifact or vendor API doc this run.
- **[DOC]** — vendor prose documentation, read this run.
- **[SECONDARY]** — a search summary or third-party page; I did not read the primary.
- **[REASONING]** — my inference. Not evidence.

**Headline: there is no field consensus on placement, and I am not going to manufacture
one.** Two of six systems are internally consistent; three are internally mixed in exactly
the way ours is; one is positionally consistent but has an orphan. What the field *does*
agree on is narrower and more useful than a placement rule — see §1.3.

**On scope, the field's set is differently shaped from our candidate set, not simply
wider or narrower** — and the mismatch runs in both directions. See §2.4.

---

## Part 1 — Structure

### 1.1 The table

| System | Where the marker sits | Exact names, from source | Internally consistent? |
|---|---|---|---|
| **Material 3** | **Prefix**, wrapping the whole role including the `on` | `inversePrimary`, `inverseSurface`, `inverseOnSurface` **[SOURCE]** | **Yes** (3/3) |
| **Primer** | **Suffix at fixed depth 1**, on a property root; ground named bare, ink named `on`+ground | `bgColor.inverse`, `fgColor.onInverse`, `bgColor.emphasis`, `fgColor.onEmphasis`, `bgColor.{semantic}.emphasis` **[SOURCE]** | **Yes — the cleanest surveyed** |
| **Fluent** | **Infix**, always before state: `color`+`{ramp}`+`{property}`+`Inverted`+`{state}` | `colorNeutralForegroundInverted`, `colorNeutralForegroundInvertedHover`, `colorNeutralBackgroundInvertedPressed`, `colorBrandForegroundInverted`, `colorSubtleBackgroundInvertedSelected`, `colorNeutralStrokeInvertedDisabled` **[SOURCE]** | **Position yes; set no** — see 1.2 |
| **Carbon** | **Mixed** — terminal in most, non-terminal in one, and after a state in another | `text.inverse`, `background.inverse`, **`background.inverse.hover`**, `border.inverse`, `icon.inverse`, `link.inverse`, **`layer.selected.inverse`**, `support.error.inverse`, `support.{info,success,warning}.inverse` **[SOURCE]** | **No** |
| **Polaris** | **Mixed** — terminal on most, non-terminal before a state | `text-inverse`, `text-inverse-secondary`, `text-link-inverse`, `icon-inverse`, `border-inverse`, **`border-inverse-hover`**, **`border-inverse-active`**, `bg-inverse`, `bg-surface-inverse`, `bg-fill-inverse`, **`bg-fill-inverse-hover`**, **`bg-fill-inverse-active`** **[SOURCE]** | **No** |
| **Atlassian** | **Mixed** — terminal for text/icon/border, non-terminal for background | `color.text.inverse`, `color.icon.inverse`, `color.border.inverse`, `color.text.warning.inverse`, `color.icon.warning.inverse`, **`color.background.inverse.subtle`**, `color.background.inverse.subtle.hovered`, `color.background.inverse.subtle.pressed` **[SOURCE]** | **No** |

Sources, all fetched 2026-08-28:

- M3 — `androidx-main`, `compose/material3/.../ColorScheme.kt`. This is the framework's own
  source, not documentation about it.
- Primer — `primer/primitives`, `src/tokens/functional/color/{fgColor,bgColor}.json5`.
- Fluent — `microsoft/fluentui`, `packages/tokens/src/alias/lightColor.ts`.
- Carbon — the published npm package `@carbon/themes@11.80.0`, `src/dtcg/g100.json` plus
  `src/dtcg/components/notification.json`.
- Polaris — `Shopify/polaris`, `polaris-tokens/src/themes/base/color.ts`.
- Atlassian — the published npm package `@atlaskit/tokens`,
  `dist/types/artifacts/token-names.d.ts`.

**Three of the six are mixed. That is the answer to "is there a consensus", and it is a
no.** Our own `on-inverse` vs `inverse` split is not an outlier; it is the majority
condition.

### 1.2 The two systems that are consistent are consistent in *opposite* directions

**Material 3 prefixes.** `inverseOnSurface`, not `onInverseSurface` **[SOURCE]**. The
marker outranks the `on`. Read as a grammar: *"the on-surface role, taken from the inverse
scheme."* The modifier applies to the scheme, and the role name rides along unchanged.

**Primer suffixes at a fixed depth, and it separates two concepts our repo conflates
[SOURCE]:**

| | names the ground | names the ink on that ground |
|---|---|---|
| emphasis | `bgColor.emphasis`, `bgColor.danger.emphasis` | `fgColor.onEmphasis` |
| inverse | `bgColor.inverse` | `fgColor.onInverse` |

**This is the single most directly useful finding in the run for our placement question.**
Primer ships `fgColor.onInverse` *and* `bgColor.inverse` deliberately, and the rule that
makes them consistent rather than mixed is: **the bare marker names a ground; `on` + the
marker names ink that sits on it.** Under that rule our `on-inverse` vs `inverse` pair is
not an inconsistency at all — it is the same grammar, and what we are missing is the
sentence stating it. Primer also documents the pairing as mandatory: `bgColor-*-emphasis`
**"MUST pair"** with `fgColor-onEmphasis` **[DOC]**.

**Fluent is positionally consistent and set-inconsistent.** Every `Inverted` sits before
the state segment. But the file ships `colorNeutralStrokeInvertedDisabled` **with no base
`colorNeutralStrokeInverted`** **[SOURCE]** — an orphan state with no rest value. Worth
naming because it is what happens when a modifier is applied per-token rather than as a
generated axis: gaps appear and nothing catches them.

### 1.3 What the field *does* agree on — and it is narrow, so it is worth trusting

**The marker binds tighter than state. Every system that has both puts inverse first:**

- Fluent — `colorNeutralForegroundInverted**Hover**` **[SOURCE]**
- Polaris — `bg-fill-inverse-**hover**`, `border-inverse-**active**` **[SOURCE]**
- Carbon — `background.inverse.**hover**` **[SOURCE]**
- Atlassian — `color.background.inverse.subtle.**hovered**` **[SOURCE]**

**4 for 4, across four unrelated naming grammars.** No counterexample found. This is a
real consensus on a small question, and it is worth more than a manufactured one on the
big question.

The corollary is also visible and points the other way for one system: **Carbon's
`layer.selected.inverse`** puts inverse *after* a state **[SOURCE]** — and it is the only
such name in Carbon's own file, which is why I read it as a lapse rather than a rule.

### 1.4 A second, separate family exists in three systems — and it is not the same concept

Carbon, Polaris and Primer each ship an "ink on a filled ground" family **alongside**
inverse, with a different name:

| System | the inverse family | the on-fill family **[SOURCE]** |
|---|---|---|
| Carbon | `text.inverse` | `text.on.color`, `text.on.color.disabled`, `icon.on.color`, `icon.on.color.disabled` |
| Polaris | `text-inverse` | `text-brand-on-bg-fill`, `text-critical-on-bg-fill`, `text-emphasis-on-bg-fill-hover`, `avatar-one-text-on-bg-fill`, … (22 names) |
| Primer | `bgColor.inverse` / `fgColor.onInverse` | `bgColor.*.emphasis` / `fgColor.onEmphasis` |

**Fluent conflates the two under one name.** `colorNeutralForegroundInverted` is reported
as the token used for the checkmark inside a filled checkbox and switch **[SECONDARY]** —
which is the on-fill case wearing an Inverted name. I did not verify this in Fluent's
component source and it should not be quoted without doing so.

**This matters to placement more than any table row.** Three of six systems decided these
are *two concepts* and gave them *two names*. If we treat them as one axis with one marker,
we are taking the minority position, and the majority took the other one on purpose.

### 1.5 Carbon's own naming discussion says one thing and Carbon's tokens do another

Carbon's naming-convention discussion states a grammar of
`[element]-[role]-[style modifier]-[state]`, with inverse as a **style modifier**, and
gives `inverse-background` and `layer-selected-inverse` as examples **[SECONDARY — I read
a summary of discussion #7827, not the thread itself]**.

**The shipped tokens do not match that.** There is no `inverse-background` in
`@carbon/themes@11.80.0`; it is `background.inverse` **[SOURCE]**. And
`layer.selected.inverse` puts the modifier *after* the state, contradicting the stated
grammar in the same breath as illustrating it.

I am flagging this rather than resolving it: **a documented grammar drifting from the
shipped names is itself the finding**, and it is the strongest available evidence that
placement is hard to hold consistent over time even when a team has written the rule down.

---

## Part 2 — Scope

### 2.1 The table

| System | Roles with an inverse variant | Interactive/fill states on inverse? | Components |
|---|---|---|---|
| **Material 3** | **3** — `inverseSurface`, `inverseOnSurface`, `inversePrimary` **[SOURCE]** | **No** — no hover/pressed inverse roles exist | **Exactly 2**: Snackbar and plain Tooltip **[SOURCE]** |
| **Primer** | **2** — `bgColor.inverse`, `fgColor.onInverse` **[SOURCE]** | **No** | Not enumerated in the token files; pairing rule documented **[DOC]** |
| **Atlassian** | **4** — text, icon, border, `background.inverse.subtle` **[SOURCE]** | **Only on `background.inverse.subtle`** (hovered, pressed) | *"Inverse tokens are designed to show on bold backgrounds"* **[DOC]**; docs illustrate banners. No component list published. |
| **Carbon** | **9 theme roles** — background, border, icon, link, text, and four `support.*` **[SOURCE]** | **Yes** — `background.inverse.hover` **[SOURCE]** | *"Use for tooltips, inverse buttons, or dark-themed sections"* **[DOC, `$description` in the shipped DTCG]**; plus **inverse Notification** carrying a full tertiary button — `notification.action-tertiary-inverse{,-hover,-active,-text,-text-on-color-disabled}` **[SOURCE]** |
| **Polaris** | **12** — incl. `bg-fill-inverse`, `bg-surface-inverse`, `text-link-inverse`, `text-inverse-secondary` **[SOURCE]** | **Yes** — `bg-fill-inverse-hover/-active`, `border-inverse-hover/-active` **[SOURCE]** | Toast, and a `tone` option on the Text component **[SECONDARY]** |
| **Fluent** | **~27** — Foreground (+Link, +a second rank), Background (Neutral/Subtle/Brand), Stroke **[SOURCE]** | **Yes, extensively** — Hover, Pressed, Selected, Disabled across foreground and background **[SOURCE]** | Checkbox and Switch indicators **[SECONDARY, unverified]** |

### 2.2 The spread is enormous, and it correlates with something

**3 roles (M3) to ~27 (Fluent) — a factor of nine.** The correlation, offered as
**[REASONING]**: the systems with the smallest inverse sets are the ones that also ship a
separate on-fill family (M3's whole `on-*` family; Primer's emphasis pair). The systems
with the largest inverse sets are the ones treating "inverted" as a general-purpose second
palette. Fluent, with no documented naming grammar for `Inverted` that I could find
**[DOC — searched `docs/architecture/design-tokens.md` and `fluent2.microsoft.design`,
neither defines it]**, has the largest and least principled set.

**So set size is a symptom of whether the system separated the two concepts in §1.4.**

### 2.3 M3's two components, now from primary source

Run 3 (2026-08-23) reported M3's inverse family as element-scoped but flagged that the
tooltip half rested on secondary sources because `m3.material.io` is unfetchable. **That
gap is now closed from the framework source [SOURCE]:**

- `SnackbarTokens.kt` — `ContainerColor = InverseSurface`, `SupportingTextColor = InverseOnSurface`,
  `IconColor` + `FocusIconColor` + `HoverIconColor` + `PressedIconColor = InverseOnSurface`,
  and `ActionLabelTextColor` + its focus/hover/pressed variants all `= InversePrimary`.
- `PlainTooltipTokens.kt` — `InverseSurface` and `InverseOnSurface`, and nothing else.

The KDoc is equally explicit: `inversePrimary` is *"Color to be used as a 'primary' color
in places where the inverse color scheme is needed, such as the button on a SnackBar"*
**[SOURCE]**.

**Caveat I cannot remove:** I confirmed these two components *use* the roles. I could not
grep the whole M3 codebase, so I cannot assert no third component uses them. "Exactly 2" in
the table means "2 confirmed", not "2 and no more".

**Note the shape of the snackbar's usage, because it cuts against a small-set instinct:**
the action label alone consumes four inverse bindings — rest, focus, hover, pressed — all
resolving to the same role. M3 has no inverse *states*, but it does have an inverse
*interactive element*, and it handles the states by pointing all four at one value.

### 2.4 Against our candidate set — the mismatch runs in both directions

Our candidate set: **button, icon button, social button, progress indicator, snackbar,
tooltip.**

**Confirmed by the field:**

- **Snackbar / toast** — M3 **[SOURCE]**, Polaris Toast **[SECONDARY]**. Strong.
- **Tooltip** — M3 **[SOURCE]**, Carbon's own `$description` names tooltips first
  **[DOC]**. Strong.
- **Button** — Carbon's description says *"inverse buttons"* **[DOC]** and Carbon ships a
  real one inside the inverse notification **[SOURCE]**; Polaris `bg-fill-inverse` +
  hover + active is a button fill **[SOURCE]**; Fluent carries full inverted interaction
  states **[SOURCE]**. Strong.
- **Icon button** — indirect. Carbon and Polaris both ship `icon.inverse` / `icon-inverse`
  **[SOURCE]**, and Fluent's inverted foreground reportedly drives checkbox/switch
  indicators **[SECONDARY]**. Reasonable but not directly evidenced as a component.

**Not found anywhere:**

- **Progress indicator.** **No surveyed system ships an inverse progress token.** Zero of
  six. I did not find one under any spelling — no `progress`, `spinner`, `loader` or
  `meter` token carrying an inverse marker in any of the six token artifacts read.
- **Social button.** Not a category any surveyed system has at token level, so the field
  says nothing either way.

**In the field but missing from our set** — this is the direction I think matters most for
the trim:

- **Link.** Carbon `link.inverse`, Polaris `text-link-inverse`, Fluent
  `colorNeutralForegroundInvertedLink` + `Hover` + `Pressed` + `Selected` **[SOURCE]**.
  **Three of six systems, and Fluent gives it four states.** Links on an inverse ground
  need their own value because the default link hue usually fails contrast there — a
  component-shaped set will not surface this, because a link is not a component.
- **A text *hierarchy* on inverse, not one ink.** Polaris `text-inverse-secondary`, Fluent
  `colorNeutralForegroundInverted2` **[SOURCE]**. Two systems ship a second rank of
  inverse text. A single `text/on-inverse` cannot express "secondary text on a dark band".
- **Border.** Carbon, Polaris, Atlassian, Fluent all ship an inverse border **[SOURCE]** —
  **4 of 6, the most widely shipped inverse role after text.**
- **Status / support colors re-tuned for inverse.** Carbon ships four
  (`support.{error,info,success,warning}.inverse`) and Atlassian ships `warning.inverse`
  for text and icon **[SOURCE]**. Atlassian states the reason: bold warning backgrounds are
  yellow, so the inverse ink has to differ from the other inverse inks to pass WCAG AA
  **[DOC]**. **This is the one nobody would derive from first principles**, and two
  independent systems hit it.

**So: differently shaped.** The field's *component* set is narrower than ours — it is
essentially snackbar, tooltip, notification/banner, and buttons, with progress indicators
absent everywhere. The field's *role* set is wider than ours — link, a second text rank,
border, and per-status inverse inks. **A trim done by component would keep the wrong things
and drop the right ones.**

---

## Part 3 — The Figma variable picker

Mechanics, verified rather than reasoned. Where Figma does not document something, I say
so rather than inferring it from the UI.

### 3.1 Slash-nested paths — **confirmed**

*"Figma uses `/` as a separator to create nested groups, which helps keep large token
libraries organized."* **[DOC]** Figma also documents that on import, *"Figma will
normalize the names of tokens in nested groups using forward slashes"* — e.g.
`color.accent.light` becomes `color/accent/light` **[SECONDARY]**.

Groups are real objects, not just naming: the Help Center documents creating them via
*"New group with selection"* and *"Click and drag groups in the sidebar of the Variables
modal to reorder groups"* **[DOC]**.

**Not documented: whether the apply-time picker renders groups as collapsible folders.**
The Help Center's article on applying variables describes swatch shapes and a library
filter but says nothing about folder affordances **[DOC]**. **I could not verify this and
am not going to assume it.**

### 3.2 Search — **exists, and it is the mechanic that most reduces the cost of placement**

Two distinct surfaces, and they are documented differently. This distinction is easy to
miss and I nearly did:

- **The Variables modal (the editor):** *"Use the search bar in the variable modal to
  search for a specific variable or group in the collection you're viewing. You can search
  by variable name, variable value, or group name."* **[DOC]**
- **The apply-time picker:** *"Use the search bar to search by variable name or variable
  group."* **[DOC]** — name **or group**, but no value search documented here.

**So search matches both the leaf name and the group segment, in both surfaces.** That is
the property the brief was reaching for: **a search for "inverse" finds the token whether
"inverse" is a folder segment or part of the leaf name.**

**What is NOT documented, and I will not claim it:** whether the match is a substring or a
prefix, and whether it matches across a **full path** (i.e. does `inverse` match
`color/background/inverse/hover` when the user is scoped to a different group). Figma
states *what fields* are searched, never *how* they are matched.

### 3.3 Sorting — **the brief's assumption is wrong**

The brief asks to "confirm alphabetical". **I could not confirm it, and the available
evidence points the other way.**

- **No Figma documentation states that variables are sorted alphabetically** anywhere I
  read — not the create/manage article, not the apply article, not the guide **[DOC]**.
- What Figma *does* document is **manual** ordering: dragging groups to reorder them, and
  reordering collections, where *"Changing the order of variable collections will affect
  the order in which they appear from the variable mode selector and variable selectors"*
  **[DOC]**.
- Figma's own plugin API concedes the ordering is not clean: `variableIds` order is
  *"roughly the same as what is shown in Figma Design, however it does not account for
  groups"* **[SOURCE]**.
- Multiple user reports describe creation-order rather than alphabetical listing, and
  specifically that the fill-menu pick list does not sort even when other surfaces do
  **[SECONDARY]**.

**Consequence, and it is the one that changes a decision:** if ordering is authored rather
than alphabetical, then the "an alphabetical picker will group all the inverse tokens
together" argument for suffix-placement **does not hold** — a suffix does not cluster in a
list that is not sorted. Conversely the argument for *prefix* placement (a folder groups
them regardless of sort) gets stronger, because a group is a structural object that
survives arbitrary ordering.

**Confidence: medium.** The absence of a documented sort is solid; the positive claim that
it is creation-order rests on user reports. **Worth a five-minute check in a real file
before anyone leans on it.**

### 3.4 Scoping — **real, documented, and only half the help we want**

*"Scope a variable to limit which properties the variable can be applied to."* … *"if you
scope a number variable to corner radius, the variable can only be applied to corner
radius and won't appear as an option for any other supported properties."* **[DOC]** The
plugin API is blunter: *"Scopes allow a variable to be shown or hidden in the variable
picker for various fields."* **[SOURCE]**

The colour scopes are a closed list **[SOURCE]**: `ALL_SCOPES`, `ALL_FILLS`, `FRAME_FILL`,
`SHAPE_FILL`, `TEXT_FILL`, `STROKE_COLOR`, `EFFECT_COLOR`.

**What this buys us:** an inverse *surface* token can be scoped to `FRAME_FILL` and will
then never appear in a text-fill picker. That genuinely reduces the cost of placement — a
designer picking text colour sees a much shorter list, so where "inverse" sits in the path
matters less.

**What it cannot do, and this is the limit worth recording:** **scoping is by property,
never by context.** There is no scope that means "only show these when the frame is on an
inverse ground". `FRAME_FILL` cannot distinguish a default surface from an inverse one.
So scoping shortens the list but does nothing to help a designer pick the *right one of two
grounds* — which is the actual comprehension problem.

---

## Part 4 — Agents

### 4.1 What documentation actually exists — thinner than it looks, but not nothing

**There is one genuine primary source, and it is Figma's own.** Their best-practice article
for making a design system legible to AI says **[DOC]**:

> *"Names like `color/surface/primary` communicate how a value should be used, not just
> what it is."*
>
> *"A variable called `blue-500` tells agents nothing about when to apply it;
> `color/brand/primary` does."*
>
> *"Figma uses `/` as a separator to create nested groups, which helps keep large token
> libraries organized."*

**But read what it actually argues.** It argues for **semantic over primitive** naming. It
says nothing about where a modifier sits within a semantic name. **It does not answer our
question**, and quoting it as though it did would be the easiest mistake available here.

The other candidate source — Nathan Curtis's EightShapes naming essay, which does address
programmatic predictability (*parallel construction across sibling tokens so a set can be
iterated predictably; a part, when present, should always appear in the same position*) —
**I could not read.** Medium returned HTTP 403. **The wording above is from a search
summary [SECONDARY] and should not be quoted as a citation until someone reads the
original.**

**So: on the specific question of how modifier placement affects LLM consumption, I found
no evidence at all.** Not thin — absent. What follows is reasoning.

### 4.2 Reasoning, labelled as such — **[REASONING] throughout**

The operation an agent performs is *"give me the inverse of X"*. Mechanically that is a
**string transformation over a token name**, and its reliability depends on one property:
whether the transformation is *positional and uniform*.

- **Uniform prefix (M3):** `surface` → `inverseSurface`. One rule. Computable.
- **Uniform suffix at fixed depth (Primer):** `bgColor.default` → `bgColor.inverse`.
  One rule. Computable.
- **Mixed (Carbon, Polaris, Atlassian):** `text.inverse` but `background.inverse.hover` but
  `layer.selected.inverse`. **There is no rule.** An agent must either memorise the set or
  guess, and a wrong guess produces a name that does not resolve — which, as our own
  versioning policy already argues about renames, fails silently rather than loudly.

**The conclusion this supports is about uniformity, not position.** Prefix and fixed-depth
suffix are equally computable; mixed is not. That is a weaker claim than "put it here", and
it is the honest one.

**One asymmetry does favour prefix, and I flag it as reasoning because I could not
evidence it:** a prefix is a *prefix*, so under any list ordering — including the
non-alphabetical ordering §3.3 suggests Figma actually uses — the inverse tokens form one
contiguous group. A suffix relies on a sort to cluster. If §3.3 is right, that argument has
teeth; if the sort turns out alphabetical after all, it evaporates. **This is the one place
where Part 3's unresolved question changes Part 4's answer**, which is why §3.3 is worth
five minutes in a real file.

---

## Recommendation

Allowed but not decisive, and the brief was explicit that this run informs rather than
decides. Two separate recommendations, because placement and scope have different answers.

### On PLACEMENT — adopt Primer's grammar and state it

**Keep both spellings and write down the rule that makes them consistent:** the bare
marker names a **ground**; `on` + the marker names **ink that sits on that ground**.
`bgColor.inverse` / `fgColor.onInverse` **[SOURCE]**. Under this rule our `on-inverse` vs
`inverse` pair stops being a defect and becomes a grammar — and what we ship is already
almost exactly this.

Then hold two positional rules, both evidenced:

1. **Fixed depth.** The marker sits at the same depth in every name that has it. This is
   the only property the agent argument actually supports (§4.2), and it is what separates
   the two consistent systems from the three mixed ones.
2. **Always before state.** `inverse` then `hover`, never the reverse. **4 of 4 systems
   [SOURCE]**, no counterexample, and the one apparent exception — Carbon's
   `layer.selected.inverse` — is a single lapse inside a file that otherwise obeys it.

**What this loses on:**

- **It is the minority position at 1 clean instance of 6.** Primer is the only system that
  ships this grammar cleanly. Adopting a minority pattern needs the rule documented or it
  reads as the same mixedness we are trying to leave.
- **It is not what an M3-trained designer expects.** Anyone arriving from Material will
  look for a prefix, and `inverseOnSurface` teaches the opposite instinct — that the
  modifier outranks the `on`, which is precisely the reverse of Primer's rule.
- **Two spellings still look inconsistent to anyone who does not know the rule.** The cost
  is documentation, permanently, and §3.2 means a search for "inverse" will surface both —
  which helps discovery but makes the pair *more* visible, not less.
- **If §3.3 is wrong and Figma does sort alphabetically, prefix beats this** on picker
  clustering, and the recommendation should be revisited.

### On SCOPE — the trim is shaped wrong, in both directions

**Drop progress indicator** unless we have a first-party reason: zero of six systems ship
an inverse progress token **[SOURCE]**. **Add link, a second rank of inverse text, border,
and per-status inverse inks** — 3, 2, 4 and 2 systems respectively **[SOURCE]**, and the
status case comes with a stated accessibility reason that nobody would derive unaided
**[DOC]**.

**What this loses on:** it grows a set we were trying to bound, and it does so on field
precedent rather than on measured need in our own corpus. **The honest counter is that
prism3 #1128's measurement is the right instrument for the size question and this survey is
not** — the same conclusion run 3 reached. Treat this as "here is what the field found
necessary", not as a sizing.

---

## What belongs in `31-color-systems.md`

Flagged, not written — the numbered file is untouched this run, and a promotion issue
carries these.

1. **§1 — the placement finding, stated as a non-consensus.** Three of six systems are
   internally mixed. This is more useful to a consultant than a fabricated rule, and it
   pre-empts the question "what does everyone else do".
2. **§1 — the one real consensus: the marker binds tighter than state.** 4 of 4.
3. **§1 — Primer's ground/ink grammar**, which is the cleanest published answer to a
   question the vault currently has no line on.
4. **§1 — the two-family distinction** (inverse vs on-fill), shipped separately by 3 of 6.
5. **§4 — the Figma picker mechanics**: search matches name *and* group; scoping is by
   property and never by context; **ordering is not documented as alphabetical.** All
   three are citable facts about the tool, useful to any client weighing a naming scheme,
   and independent of prism3's decision.
6. **A caution worth its own sentence: Carbon's documented grammar has drifted from
   Carbon's shipped names.** Evidence that a naming rule needs enforcement, not just
   agreement — which is a POV this vault can hold.

---

## Still unverified

1. **Whether the Figma apply-picker renders groups as collapsible folders.** Not
   documented; I did not verify in a file.
2. **Whether picker search is substring or prefix, and whether it spans the full path.**
   Figma documents the fields searched, never the match semantics.
3. **Whether variable ordering is creation-order.** The *absence* of a documented
   alphabetical sort is solid; the positive claim rests on user reports **[SECONDARY]**.
   Cheap to settle in a real file.
4. **Fluent's checkbox/switch usage of `colorNeutralForegroundInverted`** **[SECONDARY]** —
   the sharpest evidence that Fluent conflates inverse with on-fill, and I did not read the
   component source.
5. **Carbon's naming-convention discussion #7827** — read as a summary, not the thread.
   The drift claim in §1.5 rests on comparing that summary against shipped tokens; the
   shipped side is solid, the stated-grammar side is not.
6. **The Curtis/EightShapes naming essay** — Medium returned 403. No usable citation for
   programmatic predictability.
7. **Whether any M3 component beyond Snackbar and plain Tooltip consumes the inverse
   roles.** I confirmed two; I could not search the whole codebase.
8. **Primer's and Atlassian's component-level consumers** — neither publishes a component
   list for inverse; both document only the pairing rule and the intended ground.
