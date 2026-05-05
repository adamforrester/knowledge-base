# Notes: UI Components Series (Nov 2024, internal practice)

Source: Directed Edges LLC, "UI Components" internal practice education series, November 2024. Six PDFs extracted to plain text. Heavyweight IP for component-building methodology — load-bearing for Component Library scoping.

## Per-doc summary

**uic-intro.txt** (203 lines) — Frames the series. Opens with the question "When describing a UI component, what kinds of details do you include?" and defines a "Specification" (a.k.a. "Design spec" or "Spec") as the document that describes how an interface is composed, configured, visually designed, behaves, and more — whether component, page or otherwise. Lists the full set of UI component considerations (Naming and metadata, Anatomy, Dependencies, Properties, Layout and spacing, Composition, Behavior, Motion, Theming, Accessibility) and narrows the series' focus to five: Naming and metadata, Anatomy, Properties, Layout and spacing, Composition. The intro deck also visualizes a generic spec template (anatomy panel, properties panel with defaults, accessibility panel with reading order/role/example, component tokens table with Token / Alias / Figma style / Value, and a Version history with New features / Enhancements / Fixes sections — Version #.#.# • MMM DD, YYYY).

**uic-1-naming.txt** (183 lines, Naming and Metadata) — Five key questions: (1) What is the component name? (2) How are component names formatted? (3) Does it include a namespace? (4) Does the name vary by platform? (5) What is the component's version and status? Walks through case conventions, delimiter conventions, namespace strategies (None / Acronym / Name), and the design-vs-code parity question, including multi-platform isomorphism (Figma / React / iOS / Android).

**uic-2-anatomy.txt** (588 lines, Anatomy) — Decomposes components into named parts and asks five anatomy questions. Walks Button, Input, and Card examples. Introduces vocabulary axes for naming positional parts (Physical/Ordinal/Abstract/Logical), the "content-or-component" decision, the "subcomponent vs nested component" distinction, the "separate vs integrated component" choice (DsButton with no-label vs DsIconButton), and the integrated-vs-composed pattern (e.g., DSTextInput integrating a label vs composing DSFormLabel + DSTextInput).

**uic-3-props.txt** (867 lines, Properties — longest section) — The deepest content in the series. Surveys variant naming across IBM Carbon, GitHub Primer, Material, MUI, Reshaped, Salesforce Lightning, Atlassian, Polaris. Covers default selection ("most common / most important / most prominent"), qualitative vs ordinal scales, design–code parity, naming alternatives (icon / hasIcon / showIcon / iconName), interacting props (independent vs mutually exclusive), state modeling (consolidated vs distinct, complete vs partial vs conditional combination sets), prop dispersion across subcomponents, and "prop smell" (when a single property name on a parent silently overloads child properties).

**uic-4-layout.txt** (211 lines, Layout and Spacing) — Compares hugging vs fixed-height vs special-shape spacing approaches across iOS 16, Material, Reshaped, Atlassian, IBM Carbon, GitHub Primer, Polaris, Salesforce Lightning. Covers nesting and where padding/spacing lives in the hierarchy (DsTextInput vs DsTextInput/DsLabel vs DsTextInput/Container/Left etc.), groups (orientation horizontal/vertical, width default/fill), Group vs GroupItem spacing patterns (DsListGroup/DsListItem; the same logic applies to DsCheckboxGroup/DsCheckbox, DsTabs/DsTab, DsRadioButtonGroup/DsRadioButton), and density (small/medium/large with explicit token bindings).

**uic-5-composition.txt** (1181 lines, Composition) — The series' philosophical climax. Distinguishes Configuring from Composing, defines container concepts (Block, Area, Slot, Substitution), names "Custom Areas" as the Figma realization of slots, contrasts a "supercomponent" (don't), made-to-order components (caution) with composable component parts (do), and surfaces the gap between how designers compose in Figma and how developers compose in code. Includes empirical observations from a workshop experiment (Configure / Compose 1 / Compose 2 / Play with measured success rates 100% / ~80% / ~50%) and ends with a "trust them" stance: design systems enable teams to achieve their destiny rather than solving for every feature.

---

## Synthesized methodology (the practice's component-building philosophy)

### Intro — what the series is and isn't

The series treats a "Specification" / "Spec" as the canonical artifact of a component, regardless of whether it describes a component, page, or larger structure. A spec describes how an interface is **composed, configured, visually designed, and behaves**.

The full inventory of UI component considerations is ten: **Naming and metadata, Anatomy, Dependencies, Properties, Layout and spacing, Composition, Behavior, Motion, Theming, Accessibility**. The series scopes to five — Naming, Anatomy, Properties, Layout/Spacing, Composition — and explicitly omits Behavior, Motion, Theming, and Accessibility from deep treatment. Dependencies appear inside the Anatomy unit rather than as a standalone unit.

The intro template visualizes the moving parts of a finished spec: numbered anatomy panel (with `Depends on:` callouts and `{Name}: {Style/token}` rows), variant property panels with default markers, an accessibility panel (Reading / Role / Example, plus Focus order numbered list, plus Announced order), a component-tokens table with columns **Token / Alias / Figma style / Value** with a description, and Version history split into **New features / Enhancements / Fixes**, with `Version #.#.# • MMM DD, YYYY`.

### 1. Naming & Metadata

**Five key questions:** name? format? namespace? platform variation? version and status?

**The naming dilemma is real and contested.** A single artifact can credibly be called Button, Card, Tile, Module, Container, or — for an input — Text input, Text field, Input, Input field. The series doesn't pick a winner; it shows the field of options and pushes the team to commit consciously.

**Format via case** (verbatim):
- Title case → `Text Input`
- Sentence case → `Text input`
- Camelcase → `text Input`
- Lower case → `text input`

**Format via delimiters** (verbatim):
- No space → `TextInput`
- Dash → `Text-Input`
- Underscore → `Text_Input`
- Space → `Text Input`

**Namespace** (verbatim rationale): "Including a namespace in component names is useful for **Specificity**, Clarity to distinguish system assets from local assets; **Traceability** to quickly find, replace, maintain and upgrade instances; **Analytics** to track and measure use." Three options: None (`Text Input`), Acronym (`MDS Text Input`), Name (`Cedar Text Input`).

**Design and code consistency.** The good pattern is **Consistent, Deterministic**: `DS Button → DSButton`, `DS Text input → DSTextInput`, `DS Card → DSCard`. The bad pattern is Figma calls it `DS Card` while React calls it `DSTile`.

**Multi-platform consistency** adds two more standards on top of "consistent and deterministic": **isomorphic** across Figma / React / iOS / Android. Worked example: `DS Badge / DSBadge / DSBadge / DSABadge`, with iOS getting an `A` for Android-prefix conflict and Android adding `DSABadgeDot` as a sibling. Some components legitimately don't exist on all platforms (Card has `Not available` on Android in their illustration).

**Metadata fields** explicitly named: Name, Format, Namespace, Platform consistency, Version and status.

### 2. Anatomy

**Five anatomy questions** (verbatim, asked of every component):
1. What elements could it include?
2. Which elements are required?
3. What is each element's name?
4. Does an element depend on another component?
5. If so, is it a subcomponent or nested component?

**Vocabulary of anatomical parts (Button worked example):** Container, Icon, Label, Focus ring. Required vs optional further splits as: required-always (Label) vs **depends on property** (Icon) vs **depends on behavior** (Focus ring).

**Element naming axes** — four orthogonal vocabularies for naming positional parts (left/right):
- Physical → Left / Right
- Ordinal → Before / After
- Abstract → Leading / Trailing
- Logical → Start / End

The take is that teams should pick one axis intentionally; the choice has implications for RTL, layout direction, and code/design parity.

**Content-or-component decision (Button + glyph example):** A leading icon could be either (a) a full nested `DsIcon` component with its own `name / color / size` properties, or (b) plain `Icon/Plus "glyph" content` with no properties. The handwritten annotation is **"Atomic ≠ Atom!"** with "But to" cut off — the point being that a system's atomic unit need not be a discrete component if it has no configurability of its own.

**Nested components within Button** (each with their own props): `DsIcon (name, color, size)`, `DsCounter (scheme, size)`, `DsSpinner (size)` — OR fall back to flat `Icon content (name)`.

**Separate or integrated components?** Major decision: one `DsButton` that handles both labelled and label-less cases via a property, **OR** two distinct components `DsButton` + `DsIconButton`. The "separate" example shows divergent prop spaces: DsButton has `size: small|medium|large`, `variant: solid|outline|flat`; DsIconButton has `size: small|large`, `variant: solid|lowContrast|flat`, plus a unique `surfaceType: colorFill|media`. The lesson: when prop spaces diverge enough, splitting is the honest move.

**Input anatomy elements:** Container, Left Icon, Value, Placeholder, Right content, Inline action, Right icon — with explicit token bindings (Container: `DS Color/Forms/Control/Background`, `DS Color/Forms/Control/Border`, border weight 1, `DS Shape/border radius/input control (4)`).

**Default content rule (placeholder content choices in spec art):**
- "Labeled Data" — `{Label}` `{Help text}` `{Value}` `{error text}` (generic slots)
- "Real Data" — actual example like "Address / Include street name… / 123 Main St. / Address must include a valid house number." (ready-made examples win when feasible)
- "Element names" vs "Lorem Ipsum" — what's fixed vs editable matters

**Integrated vs Composed (Text Input + Form Label):** Integrated puts label inside the input (`<DsTextInput label="…" helpText="">`), Composed wires them together (`<DsFormLabel>{Label}</DsFormLabel><DsTextInput>{Value}</DsTextInput>`). Figma representation diverges accordingly: integrated has properties on one variant (`required, label, helpText, leftIcon, value`); composed has two variants whose prop sets overlap.

**Card anatomy (essential elements):** `DsCardContainer` OR/AND `DsCard`. The Required/Optional table:
- Container — Required
- Media — Optional?
- Metadata — Optional
- Title — Required
- Description — Optional
- Actions Area — Optional
- Action 1 — Optional
- (Depends on behavior)

**Element-name debates for Card:** Media vs Image vs CardMedia vs Asset; Metadata vs Eyebrow vs something else; Title vs Heading vs Header; Subtitle vs Subheader vs Description vs Body. Again the deck does not pick — the *practice* is to inventory candidates and choose explicitly.

### 3. Properties (longest section — extracted thoroughly)

**Six key questions** (verbatim):
1. What properties can you configure?
2. What is each property type?
3. What is each property default?
4. What options are available for each property?
5. Do properties interact? If so, how?
6. What properties and options are exposed by parent component(s)?

**Variant naming across the industry (Button hierarchy/appearance prop):**
- IBM Carbon → `style`: primary / tertiary / ghost (Hierarchy & appearance)
- GitHub Primer → `variant`: primary / secondary / invisible (Hierarchy & appearance)
- Google Material → `type`: filled / outlined / text (Appearance)
- MUI → `variant`: contained / outlined / text (Appearance)
- Reshaped → `type`: solid / outlined / ghost (Appearance)
- Salesforce Lightning → `type`: brand / outline / base (Purpose & appearance)

The lesson: every system invents its own vocabulary; there is no canonical answer; the team must pick a single property name and a single set of values consciously.

**Completeness across systems (states matrix):** rest, hover, focus, disabled, pressed, active, loading. Coverage is uneven — Polaris has skeleton, Carbon has inactive, Atlassian has highlighted, Lightning lacks some. Implication: the system must declare which states it commits to supporting.

**Default selection criteria** (verbatim three-way framing):
- Most common?
- Most important?
- Most prominent?

These can conflict (the default is named `primary` in design but `default` in code in their Primer reference example). Worth resolving deliberately.

**Blending qualitative and ordinal scales (Carbon Button):** code uses `size: 'sm' | 'md' | 'lg' | 'xl' | '2xl'` plus `isExpressive: boolean`. Figma flattens that into `size: 'Small' | 'Medium' | 'Large' | 'Extra large' | '2xl' | 'Expressive'` — adding `Expressive` as a sibling on the scale. The point: a code-side boolean and a design-side enum value can describe the same thing with different shapes; teams must reconcile.

**Design ↔ Code parity (Polaris Button):** code has `size: 'micro' | 'medium' | 'large' | 'slim'`; Figma has `size: 'micro' | 'medium' | 'large'`. `slim` is missing in design — a real divergence. This is shown as a problem to flag, not a feature.

**Property naming alternatives** for "does this button have an icon":
- `icon` (boolean) vs `showIcon`
- `icon?` vs `Show icon?`
- `hasIcon?` vs `With icon?`
- For the icon name itself: `icon` / `iconName` / `Icon name` / `name`

**Visual variation ≠ property variation (exactly).** A button at small/medium/large doesn't just resize — it changes height, item spacing, padding L/R, leftIcon size, and label text style:
- Small: H 28, item-spacing `padding/0_25x (4)`, padding `padding/0_375x (6)`, leftIcon 16×16, label `Body/Small`
- Medium: H 36, item-spacing `padding/0_375x (6)`, padding `padding/0_5x (8)`, leftIcon 20×20, label `Body/Medium`
- Large: H 42, item-spacing `padding/0_5x (8)`, padding `padding/0_75x (12)`, leftIcon 20×20, label `Body/Medium`

Lesson: a single property triggers a coordinated cascade across child elements and tokens.

**Abbreviations: clarity vs brevity.** `button` vs `btn`; `Small` vs `Sm` vs `S`; `3 Extra Large` vs `XXXL` vs `3XL`. The practice frames it as a clarity-vs-brevity tradeoff with no universal answer.

**Interacting props — three patterns:**
- **Independent**: `leadingIcon`, `leadingIcon name`, `trailingIcon`, `trailingIcon name` (each axis its own boolean+name pair)
- **Mutually exclusive (model A)**: `icon` (boolean) + `iconPosition: leading | trailing` + `name`
- **Mutually exclusive (model B)**: `icon: 'none' | 'leading' | 'trailing'` + `name`

Each compresses differently in code (`<DsButton leadingIcon="plus" trailingIcon="chevronRight" />` vs `<DsButton icon="plus" iconPosition="leading" />`).

**Design and code alignment (ESDS Button real example).** The Figma property panel exposes: Icon, Text, ↪️Text, Variant, Size, Surface, State, Breakpoint. The reconciled spec separates these into:
- **Design and code:** `variant` (primary/flat/outline), `size` (medium/small/large), `iconName` (string), `label` (string), `colorMode` (light/dark)
- **Design only:** `content` (text only / leading icon / trailing icon / icon only), `breakpoint` (mobile/tablet/desktop)
- **Code only:** `href` (string), `type` (button/submit/reset)
- **Intentionally different:** `state` (initial/hover/press/focus/disabled — design-only), `disabled` boolean (code-only)

Big idea: design and code property sets are not 1:1 and shouldn't be forced to be — *but the divergences must be intentional and labeled*.

**State modeling: distinct vs consolidated.**
- Distinct properties: `Validation: error`, `Disabled: bool`, `Read only: bool`, `State: rest|hover|active|focus`
- Consolidated property: `State: rest|hover|active|focus|disabled|error|success|read only`

The "default state name" survey: `enabled` (MUI/Carbon), `default` (Lightning/Atlassian), `resting` (Polaris/Primer), `rest` — no industry consensus.

**Combination set patterns (a major contribution of the deck):**

1. **Complete combination set** (DsRadioButton): every state × every selected value. DO: keep `selected` and `state` separate. Caution: `state` enumerated as `rest, hover, active, focus, rest selected, hover selected, active selected, focus selected` (8 values flatten the cross product but it's still tractable). DON'T: collapse to single `state` enum and lose the orthogonality.

2. **Partial combination set** (DsTextInput): not every state is meaningful with disabled. DO: keep `disabled` boolean separate from `state: rest|hover|active|focus`. Caution: bake disabled into state.

3. **Conditional partial set** (DsTextInput with disabled + readonly): readonly is conditional on disabled. DO: keep both as booleans plus separate `state`. Caution: combine readonly into state. DON'T: dump everything into one `state` enum.

   The deck explicitly notes Figma's limitation: "Ideally, Figma would instead not show hover and active when disabled or read only is true… but that's not how Figma works."

4. **Conditional sets on 2+ props.** Question: "Can focus vary independently of hover, active?" The answer drives whether `focus` is its own boolean alongside `state` or part of the `state` enum. Two valid models depending on accessibility behavior (focus-and-hover, focus-and-active being meaningful pairs).

**Prop dispersion** (Card example): a Card's properties get distributed across subcomponents:
- `DsCardContainer`: aspectRatio, background, imageFallbackColor, border, padding, state
- `DsCardMedia`: type, aspectRatio, state, zoomOnHover
- `DsCardText`: size, metadata, title, description (each text element with its own value)
- `DsCardActions`: type, actions count, size, plus per-Action (variant, state, label)

**Prop smell.** Concrete example: a single `size` on the parent card that silently controls text size *and* action size. The smell is: "What of configuring size in terms of *relating text size to action size* and *controlling action size at the group and item levels*?" The fix is the **Facade** pattern.

**Facade pattern.** A single parent property (e.g., `size`) maps to differently-named per-element values. Card example:
- card `size: Small` → DsCardText size Small, DsEyebrow (Metadata) size **Very small**, DsHeading (Title) size **4**, DsBody (Description) size Small
- card `size: Medium` → DsCardText Medium, Eyebrow Small, Heading 3, Body Medium
- card `size: Large` → DsCardText Large, Eyebrow Medium, Heading 2, Body Large

The facade lets a single parent prop trigger a coordinated, non-uniform resize across heterogeneous subcomponents.

**Flexible configuration.** Sometimes child sizes should be configurable independently (e.g., DsCardText Medium + DsButton Medium = DO, DsCardText Medium + DsButton Large = caution, DsCardText Large + DsButton Medium = caution). Both configurations may be valid; the system should expose them rather than fold everything into one parent enum.

**Six dimensions of properties** (closing slide vocabulary): **Props, Types, Options, Default, Exposure, Interactions.**

### 4. Layout & Spacing

**Three sizing approaches across systems:**
- **Hugging** (iOS 16, Material, Reshaped) — content drives height; padding values dominate
- **Fixed height** (Atlassian uses `minHeight`, IBM Carbon, GitHub Primer, Polaris) — explicit pixel heights
- **Special shape** (Salesforce Lightning) — explicit `height` prop

Worked numbers shown for each (e.g., Material 16/8/24/8/4/4/8 padding-internal-padding-internal pattern with height 4+label+4; iOS 14+(20/10/20)+14 etc.). The lesson: each system has internalized a layout philosophy and the spacing scale flows from it.

**Across-component concerns.** The Form Label + Text Input layout question: where do the gaps between label, help text, value, and error text live? Inside the input or outside?

**Nesting model (where padding lives in the hierarchy):** Six layers of nesting illustrated for a labelled text input:
1. `DsTextInput` (8/8 spacing block-internal)
2. `DsTextInput / DsLabel` (4 spacing inside label)
3. `DsTextInput / DsLabel / Label content` (4/4 inside label content)
4. `DsTextInput / Container` (12 in container)
5. `DsTextInput / Container / Left` (8 left side)
6. `DsTextInput / Container / Right` (8/8/8 right side, plus 4/4 around action)

The point: spacing is a hierarchical concern; the same visual gap can live at different levels of the tree, and the team must decide where.

**Groups.** Group component (e.g., Button group) takes `width: default | fill` and `orientation: horizontal (default) | vertical`. Spacing 32 outside the group, 16 between items inside. The pattern repeats: `DsListGroup / DsListItem`, `DsCheckboxGroup / DsCheckbox`, `DsTabs / DsTab`, `DsRadioButtonGroup / DsRadioButton`. The container handles inter-item spacing; the item handles intra-item spacing.

**Density.** Small/medium/large produce explicit token-bound differences (item-spacing/padding/0_25x/0_375x/0_5x/0_75x). The token names use a `0_25x / 0_375x / 0_5x / 0_75x / 1x / 2x` multiplier scale.

**Layout patterns vocabulary** (closing slide): **Patterns, Nesting, Groups, Group items, Density.**

### 5. Composition (extracted thoroughly)

**Four key composition questions** (verbatim):
1. What container(s) must be flexible?
2. What subcomponent(s) save time and improve consistency?
3. What examples best express component potential?
4. What content and components can be included?

**Configure vs Compose** is the central distinction.
- **Configure**: change properties on an existing component instance.
- **Compose**: assemble multiple parts inside a flexible container.
- **Configure AND Compose**: configure for *common* things, compose for *uncommon* things. (Verbatim closing slide.)

**Property quantity tradeoff.** A card with `{Title}` + three `{property}{value}` rows + `{Label}` action raises the question "do I make this a property explosion or do I provide composition zones?" The answer is: when many discrete pieces of structured content recur, expose them as named property fields; when the variety of content is open-ended, expose a slot.

**Permitted composition** (do/caution/don't graphic): Some compositions are clearly correct (NORM tag), some are wrong (NO tag), some are case-by-case (NO! tag). The deck doesn't enumerate rules — the takeaway is that the system designer must visually score sample compositions and convey which patterns are blessed.

**Efficiency tradeoff.** Without composition the workflow is: insert → configure → realize you can't do it (custom design) → wait for design systems team to do it → handoff. With composition: insert → configure → create & swap → create specs of custom design → handoff. Composition collapses the bottleneck.

**Container concepts (the four-way taxonomy — major contribution):**
- **Block** — the entire component as one substitutable unit (whole DsCard)
- **Area** — a defined region with predetermined content type ({Metadata} {Title} {Description})
- **Slot** — a placeholder area that allows custom content to be passed in (Custom area)
- **Substitution** — swap out a specific named child ({Label} swapped for an alternative)

Verbatim definition of Slot: **"A component placeholder or area that allows you to pass custom content into it."**

**Naming custom areas.** Team-vocabulary inventory: `Custom area`, `Customize`, `Slot`, `Swap`, `Compose`, `Composition`. Pick one; commit.

**Card subcomponent decomposition (the worked example):**
- `DSCard` is the root
- `DSCardImage` — Extension
- `DSCardTextLockup` — Lockup
- `DSCardActions` — Alternatives

**Lockup** rationale (DsCardTextLockup): used by every DsCard, resizes pairings predictably, affords required/optional, controls spacing by size. Props: `size: Small`, `metadata`, `description`. The lockup is a *typographic kit* sub-component: the metadata + title + description block as a coordinated unit.

**Extension** rationale (DsCardImage): constrains aspect ratios (16:9, 4:3, 1:1), adds hover zoom and other states. Props: `aspectRatio`, `hoverZoom`, `pressShadow`. An extension wraps a generic child (DsImage) with card-specific behavior.

**Container as (nested?) component.** `DsCardContainer` exposes both Figma props (`contained, containedPadding, aspectRadio, background, imageFallbackColor, border, state`) and code props (`aspectRatio, background, contained, containedPadding, imageFallbackColor, border, state`) — note the design–code parity.

**How designers compose in Figma ≠ how developers compose in code.** Verbatim. Developers write whole composition trees:

```
<esds-card contained>
  <esds-image aspectRatio="16:9" .../>
  <esds-card-content>
    <esds-card-text metadata="1889">Wheatfield</esds-card-text>
    <esds-card-actions>
      <esds-icon-button />
      <esds-icon-button />
      <esds-icon-button />
    </esds-card-actions>
  </esds-card-content>
</esds-card>
```

Designers don't do that. Designers configure views with custom areas pre-laid by the system.

**The pain of composition in Figma** (three-step procedure):
1. Compose it outside (place components, space via AutoLayout)
2. Make it a component (create a component to be swapped as an instance)
3. Swap it inside

This is high-friction. Workshop data: configure = 100% success, compose-1-thing = ~80% success, compose-2-things = ~50% success. Enthusiasm 4.75/5; confidence 4/5; observed autolayout skill is *lower* than self-assessed skill.

**Custom area alternatives** (six worked patterns):
- **Slot — Above text** / **Slot — Below text** (additive flex zones bracketing structured content)
- **Substitution — Actions** (swap the actions area for a custom action set)
- **Substitution — Media (Image)** (swap media for any visual)
- **Area — All the things** (one big slot containing the entire structured stack)
- **Block — Entire card** (the whole card is the slot — equivalent to "what a developer does")

The deck shows OR (use one of these patterns) and AND (use multiple, including compounding above-text + below-text + substitution patterns simultaneously).

**Beware the bento.** Don't start from a uniform grid (Above/Between/Below × Left/Center/Right). Start from real layouts (e.g., a list item with a credit-card title + amount + date) and abstract back. Bento-box composition zones are seductive but tend not to match real content.

**Nested layout swapping** (collaborator @SShuaiqi credit). Start from one block, divide horizontally/vertically, configure and nest. Tree of swap points proliferates rapidly — illustrating both the power and the maintenance cost of deeply nested composition.

**Three approaches — DON'T / Caution / DO:**
- **DON'T: Supercomponent.** One `DsCard` with 32 props, and counting. Tries to serve all needs centrally; collapses under its own weight.
- **Caution: Components made-to-order.** `DsProductCard, DsEventCard, DsArticleCard, DsVideoCard, DsActivityCard, DsActivityCard2, DsEventActivityCard, DsCoolExperimentCard, DsHighlightCard, DsWontBeUsedAfter2MonthsCard`. Made centrally for each adopter. Sprawl, duplication, eventually deprecation graveyard.
- **DO: Composable component parts.** `DsCardContainer + DsCardTextLockup + DsCardImage + DsCardActions`. Adopters DIY using offered containers, subcomponents, and examples. *If and when reuse scale suggests…* graduate a frequent composition into a named component (`DsProductCard`, `DsCardlet`) — promotion based on observed reuse, not anticipated reuse.

**Why compose? Six rationales** (verbatim):
- **Expression** — Maximize reasonable diversity of compositions
- **Efficiency** — Minimize time needed to experiment and make uncommon things
- **Delegation** — Maximize adopter responsibility for needs others don't share
- **Autonomy** — Minimize support needed from system team
- **Quality** — Make uncommon things better, more easily and consistently
- **Maintenance** — Minimize the cost of maintaining shared "core" things

**Concerns about quality** when composition is allowed (verbatim):
- **Usability** — "Can users succeed?"
- **Consistency** — "Were design tokens and layout applied well?"
- **Accessibility** — "Do outcomes have accessible contrast?" / "Do compositions work well with screen reading?"
- **Performance** — "Does it render quickly?" / "Is there a download size impact?"

**Trust** (the philosophical close). NOT THE FUTURE: trying to anticipate and serve every garish edge case (e.g., a card with five action buttons and metadata-about-metadata). THE FUTURE: **"Trust them. They won't make this."** "Design system practitioners cringe when a designer detaches a Figma component or developer codes a component from scratch" — but for most design systems, solving for every feature to support every case is a fool's errand.

Final two slides:
- "Teams control their destiny."
- "Design systems enable teams to achieve their destiny."

---

## Cross-cutting principles from the series

- **Specifications are the canonical artifact.** Anatomy + Properties + Layout + Composition + Accessibility + Tokens + Version history live together in one spec.
- **Naming is contested. Pick consciously.** The team's job is not to discover the right name but to commit to a coherent system.
- **Design and code are not 1:1, and shouldn't be forced to be.** Some props are shared, some are design-only, some are code-only. Mark divergences explicitly as intentional.
- **Properties cascade.** A single `size` triggers coordinated changes across height, padding, item-spacing, child icon size, child text style, and grandchild typography (the Facade pattern).
- **Visual variation ≠ property variation exactly.** Visual differences may not map to property differences cleanly; resolve case-by-case.
- **Variants vs booleans vs enums vs instance-swaps are modeling choices, not just naming choices.** Distinct booleans communicate orthogonality; consolidated enums communicate exclusivity. Choose to convey the right invariants.
- **Subcomponents are how prop dispersion is managed.** Don't collapse a component's whole prop set into the root.
- **Configure for common; compose for uncommon.** Don't choose; do both.
- **Composition is hard in Figma.** Plan for it; provide custom areas; teach autolayout.
- **Trust adopters.** They won't build the absurd cases you fear.
- **Promotion by observed reuse.** Graduate a composed pattern to a named component only after frequency justifies it.

---

## Phase-tagged findings (canonical 8 phases)

**Discovery & Strategy**
- Naming/namespace strategy is a strategic decision (Acronym vs Name vs None affects analytics, traceability, brand).
- Multi-platform scope (Figma / React / iOS / Android) determines isomorphism requirements.
- "Configure vs Compose vs Both" is a strategic stance the practice must take.

**Design Foundations**
- Token usage in spec art (`DS Color/Forms/Control/Background`, `DS Shape/border radius/input control (4)`, `DS Space/padding/0_25x` etc.) — token taxonomy is a prerequisite for the spec template.
- Density scale (small/medium/large) maps to spacing-token multipliers (`0_25x / 0_375x / 0_5x / 0_75x / 1x / 2x`).

**Component Library** (bulk of the series)
- Anatomy decomposition with the 5 questions
- Required vs optional with three reasons (always / depends-on-property / depends-on-behavior)
- Element-naming axes (Physical / Ordinal / Abstract / Logical)
- Subcomponent vs nested-component vs content-vs-component decision
- Separate vs integrated component decision
- Property modeling: types, options, defaults, exposure, interactions
- Distinct vs consolidated state property modeling
- Complete vs partial vs conditional combination sets
- Prop dispersion across subcomponents
- Facade pattern for coordinated cross-component resize
- Layout: hugging vs fixed-height vs special-shape
- Nesting and where padding lives
- Group / GroupItem pattern
- Composition container types: Block / Area / Slot / Substitution
- Lockup, Extension subcomponent patterns
- Custom areas naming and placement
- Supercomponent / Made-to-order / Composable parts approach selection
- Promotion-by-reuse rule

**Documentation**
- The intro spec template (anatomy panel, properties panel with defaults, accessibility, tokens table with Token/Alias/Figma style/Value, Version history New features/Enhancements/Fixes, Version #.#.# • MMM DD, YYYY)
- "Real Data" content over "Lorem Ipsum" content where feasible

**Development Support**
- Design ↔ Code parity tables, with explicit "Design only / Code only / Intentionally different" labeling
- Multi-platform name isomorphism

**Pilot & Implementation**
- Workshop measurements: Configure 100% success, Compose-1 ~80%, Compose-2 ~50%
- Enthusiasm 4.75/5, confidence 4/5, autolayout self-assessment higher than observed skill
- "How designers compose in Figma ≠ how developers compose in code" — implication for handoff workflow

**Governance & Adoption**
- Promotion by observed reuse (graduate `DsProductCard` only when justified)
- "Trust them" — adopters detaching/recoding is acceptable; don't try to solve every case
- Guardrails on quality concerns: usability, consistency, accessibility, performance

**Ongoing Maintenance**
- Version history structure (New features / Enhancements / Fixes)
- Multi-platform isomorphism upkeep (a name change must propagate)
- Minimize the cost of maintaining shared "core" things (one of the six rationales for composition)

---

## Notable verbatim language / quotes / rules of thumb

- **Spec definition:** "A document that describes how an interface is composed, configured, visually designed, behaves and more, whether a component, page or something else."
- **Five anatomy questions:** "What elements could it include? Which elements are required? What is each element's name? Does an element depend on another component? If so, is it a subcomponent or nested component?"
- **Six properties questions:** "What properties can you configure? What is each property type? What is each property default? What options are available for each property? Do properties interact? If so, how? What properties and options are exposed by parent component(s)?"
- **Four composition questions:** "What container(s) must be flexible? What subcomponent(s) save time and improve consistency? What examples best express component potential? What content and components can be included?"
- **Slot definition:** "A component placeholder or area that allows you to pass custom content into it."
- **Default selection:** "Most common? Most important? Most prominent?"
- **Element-naming axes:** "Physical / Ordinal / Abstract / Logical → Left/Right, Before/After, Leading/Trailing, Start/End"
- **Container concepts:** "Block / Area / Slot / Substitution"
- **Composition stance:** "Configure with properties OR Compose with parts → Configure AND Compose: common things AND uncommon things."
- **Approaches:** "Don't: Supercomponent. Caution: Components made-to-order. DO: Composable component parts."
- **Six rationales:** "Expression, Efficiency, Delegation, Autonomy, Quality, Maintenance."
- **Quality concerns:** "Usability, Consistency, Accessibility, Performance."
- **Trust:** "Trust them. They won't make this."
- **Closing:** "Teams control their destiny. Design systems enable teams to achieve their destiny."
- **Naming namespace value:** "Specificity, Traceability, Analytics."
- **Composition reality:** "How designers compose in Figma ≠ how developers compose in code."
- **Handwritten anatomy aside:** "Atomic ≠ Atom!" (a glyph need not be a discrete component)
- **Figma limitation acknowledgement:** "Ideally, Figma would instead not show hover and active when disabled or read only is true… But that's not how Figma works."

---

## Tensions / contradictions / open questions

- **Naming convention pluralism vs single answer.** The deck repeatedly inventories options and rarely picks one — leaving teams to converge themselves. Useful for teaching, not a usable default.
- **Integrated vs Composed (Form Label + Text Input).** The deck shows both as valid without strongly steering. In practice this decision has large downstream consequences.
- **Separate vs single component (DsButton with vs without label vs DsButton + DsIconButton).** Same as above.
- **Distinct vs consolidated state properties.** The deck shows DO and DON'T but the line is "depends on whether axes are orthogonal," which is a judgment call.
- **Custom areas vs property explosion.** When does a Card get more `{property}{value}` slots vs an "Above text" slot? Boundary unstated.
- **"Beware the bento"** — bento-box layouts are warned against but the alternative starting point ("real content first") is not formalized.
- **Composition difficulty in Figma vs philosophical commitment to composition.** The deck wants designers to compose, then admits composition is painful and most designers are below their self-perceived autolayout skill. The unresolved tension: how much should the system invest in teaching composition vs working around Figma's limits with custom areas?
- **"Trust them"** vs practitioner instinct to constrain. The deck preaches trust but doesn't address what to do when adopter-built compositions actually do violate brand or accessibility.
- **Promotion-by-reuse threshold.** "If and when reuse scale suggests" — but no metric, no cadence, no rule.

---

## Gaps (relative to a complete component methodology)

- **Accessibility annotations.** The intro template panel shows reading order, role, example, focus order, announced order — but the series explicitly scopes Accessibility *out*. There is no methodology here for screen-reader behavior, focus management, ARIA mappings, color contrast tokens, or accessibility annotation patterns.
- **Motion specs.** Listed as a consideration; not addressed. No duration tokens, easing curves, choreography, or reduced-motion handling.
- **Theming.** Listed; not addressed. Light/dark, high-contrast, brand-skinning, multi-brand all absent.
- **Behavior.** Listed; not addressed. State machines, async behavior, loading patterns, error patterns, validation timing, debouncing.
- **Multi-platform parity in depth.** Naming isomorphism is covered; but iOS/Android-specific anatomy, native control mapping, and platform conventions are not.
- **Contribution model.** No process for how external teams propose new components, get reviews, or contribute back.
- **Deprecation / lifecycle.** Version history shows New features / Enhancements / Fixes but not deprecation, sunset, breaking-change communication, or migration guidance.
- **Tokens taxonomy.** Token columns appear in the template (Token / Alias / Figma style / Value) but the taxonomy itself (semantic vs primitive vs component) is assumed, not taught.
- **Documentation site / IA.** No guidance on how spec pages assemble into a consumable site.
- **Code distribution and packaging.** Nothing on monorepos, build systems, semver discipline, or release cadence.
- **Testing.** No visual regression, unit, or accessibility test guidance.
- **Analytics & telemetry.** Mentioned as a benefit of namespacing but no instrumentation methodology.
- **Governance bodies.** "Trust them" is the closing posture but the governance structure (review board, RFC process, SLAs) is absent.
- **Quality gates.** "Concerns about quality" lists usability, consistency, accessibility, performance, but doesn't define how the system measures or enforces them.
- **Internationalization.** Element-naming axes nod at logical (Start/End) for RTL, but no broader i18n methodology — text expansion, locale-specific layout, bidi.
- **Forms framework.** Text Input is treated as a component but form-level concerns (validation orchestration, error summarization, submission) are not.
- **Density beyond small/medium/large.** Compact vs comfortable vs spacious user-pref toggles are not modeled.
- **Component tokens.** Template references a Component tokens panel (Token / Alias / Figma style / Value) but the methodology for *deriving* component tokens from foundation tokens is not articulated.
