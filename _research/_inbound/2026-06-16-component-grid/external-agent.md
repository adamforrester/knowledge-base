# The Grid Component: Field-Truth Study & System Specification

## 1. Framing

### The Triad Systemic Model
In modern component-driven layout engineering, the design system layout engine is fully realized by the `Box` → `Stack` → `Grid` triad. Within this model, `Grid` represents the **two-dimensional layout engine**.

```
┌────────────────────────────────────────────────────────┐
│                        Box                             │  <- Substrate (Polymorphism, Spacing Scale, Logical RTL)
└───────────────────────────┬────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│         Stack         │       │         Grid          │
│   (1D Layout Engine)  │       │   (2D Layout Engine)  │  <- Simultaneous Tracks (Row & Column Alignment)
└───────────────────────┘       └───────────────────────┘
```

1. **`Box` (The Substrate):** The root primitive. It owns zero-runtime style delivery, logical-property RTL mapping, the spacing token scale, and the polymorphic render pipeline (`as`/`asChild` via Radix Slot).
2. **`Stack` (The 1D Engine):** Manages layout flow along a single axis (even when wrapping is permitted). It enforces the "no external margin" discipline, using modern CSS Flexbox `gap` to distribute spacing.
3. **`Grid` (The 2D Engine):** Manages two-dimensional relationships simultaneously along horizontal and vertical axes (tracks). It inherits the polymorphic capabilities and spacing scale of `Box`, behaves as a sibling to `Stack`, and solves complex structural alignment where vertical and horizontal coordinates must remain aligned.

### The 12-Column Legacy vs. Native CSS Grid
The major architectural dividing line in design system history is the transition from **12-Column Float/Flexbox emulate-grids** to **Native CSS Grid**.

| Architectural Dimension | 12-Column Legacy (Bootstrap Row/Col, Ant Design Row/Col) | Native CSS Grid (MUI Grid2, Radix Themes Grid, Tailwind) |
| --- | --- | --- |
| **Underlying Engine** | CSS Float / CSS Flexbox | Native CSS Grid Specification (`display: grid`) |
| **Layout Definition** | Defined on the *children* (e.g., `<Col span={6}>`, percentage-based `width` / `flex-basis`). | Defined on the *parent* container (`grid-template-columns`, `grid-template-rows`). |
| **Track Enforcement** | Rigid, virtual grid. True vertical track alignment is fragile and requires explicit row nesting. | Explicit, engine-enforced tracks. Layout structures are declared centrally on the container. |
| **Markup Overhead** | High. Requires nested structural wrappers (`Row` wrappers wrapping `Col` wrappers wrapping nested `Row`s). | Low. Typically flat markup trees (`Grid` wrapping arbitrary structural elements). |
| **Spacing Control** | Negative margins on `Row` intersecting with horizontal padding on `Col` (gutters). | Native CSS `gap` / `row-gap` / `column-gap` resolved against spacing tokens. |

#### The Migration Prototype: Material UI (MUI) `Grid` → `Grid2`
MUI's migration path provides an illustrative look at this transition:
* **MUI v5 `Grid` (Legacy):** Built on Flexbox. It used negative margins on the parent wrapper combined with padding on child items to emulate gutters. It was plagued by horizontal overflow bugs, required wrapper elements to reset padding, and could not easily support automated 2D track alignment.
* **MUI v5/v6 `Grid2` (Native CSS Grid):** Introduced as an alternative and subsequently established as the default. It leverages CSS Grid and native CSS `gap`. It eliminated negative margin calculation issues, reduced HTML output by removing structural wrapping containers, and added support for features like `subgrid` and auto-generated tracks.

### The Three Grid Genres
When designing a unified design system API, a single `Grid` primitive (or a small, cohesive component family) must cleanly serve three structural patterns:

```
GENRE 1: LAYOUT / COLUMN GRID             GENRE 2: AUTO-GRID / RAM                 GENRE 3: TEMPLATE GRID
┌───┬───┬───┬───┬───┬───┬───┬───┐         ┌─────────┬─────────┬─────────┐         ┌─────────────────────────────────┐
│   │   │   │   │   │   │   │   │         │         │         │         │         │             Header              │
├───┴───┴───┴───┼───┴───┴───┴───┤         ├─────────┼─────────┼─────────┤         ├─────────┬───────────────────────┤
│    Span 4     │    Span 4     │         │         │         │         │         │         │                       │
└───────────────┴───────────────┘         └─────────┴─────────┴─────────┘         │ Sidebar │         Main          │
Explicit responsive column splits.        auto-fit / auto-fill minmax()           │         │                       │
                                          Reflows without media queries.          └─────────┴───────────────────────┘
                                                                                  grid-template-areas positioning.
```

1. **The Column Grid (Layout Grid):** The classical N-column responsive layout (typically 12 or 16 columns) where items are explicitly positioned by spanning column counts across responsive breakpoints.
2. **The Auto-Grid (The "RAM" Pattern - Repeat, Auto-fit, Minmax):** An intrinsically responsive grid of equal-sized cells that reflows dynamically *without viewport media queries*. It relies on `repeat(auto-fit, minmax(minWidth, 1fr))` to drop items to new lines when container space shrinks.
3. **The Template Grid (Named-Areas):** An explicit 2D placement engine that uses `grid-template-areas` and matching `grid-area` assignments to lay out structural layouts like page shells, complex dashboard headers/sidebars, or specialized application layouts.

### The Container Query Inflection
Design systems have historically driven layout responsiveness via viewport-based media queries (`@media`). The modern standard has shifted to **Container Queries (`@container`)**, supported natively across all major browsers since early 2023.

Layout elements (such as a card gallery inside a `Grid`) should layout based on the *space allocated to their parent container*, rather than the global viewport width. A `Grid` placed within a narrow sidebar column must render a 1-column layout, while the exact same `Grid` placed in a wide main content area should render a 3-column layout at the same viewport width.

```css
/* Intrinsic container-driven responsiveness via RAM */
.grid-auto-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));
}
/* Explicit container query adaptation */
@container layout-context (max-width: 600px) {
  .grid-responsive-layout {
    grid-template-columns: 1fr;
  }
}
```

By shifting the layout engine's primary responsive API from viewport-based breakpoints to a hybrid of intrinsic `RAM` scaling and explicit `@container` props, design systems can isolate components from the global layout state.

---

## 2. Anatomy and Parts
The `Grid` component is composed of two distinct element types: a single parent wrapper container and optional, explicit child wrapper cells.

```
Grid (Container: display: grid)
├── Grid.Item (Cell: grid-column / grid-row / grid-area)
├── Grid.Item (Cell: grid-column: span 2)
└── [Arbitrary Direct Child] (Implicitly placed in track)
```

### The Grid Container
The outer shell that instantiates the 2D formatting context by delivering `display: grid` or `display: inline-grid`. It is structurally invisible, generating no visual borders, backgrounds, or spacing markers of its own. It holds the structural definitions for the layout:
* **Tracks:** Defined explicitly or implicitly via columns and rows.
* **Gaps:** The empty spacing buffers separating tracks, defined along row and column axes.

### The Grid Item / Cell
An optional, explicit child element used to control spanning, custom placement, visual ordering, or alignment overrides within the grid.
* Direct children of the Grid container that do not use the explicit Cell component are auto-placed into the layout based on the container's `grid-auto-flow` settings.
* Explicit Grid Cells do not create independent nesting context boundaries unless they also declare `display: grid` (or inherit layout tracks via `subgrid`).

### Subgrid
The CSS Grid Level 2 `subgrid` capability (which achieved universal browser support in early 2024) allows a nested `Grid` component to adopt the track definitions of its parent `Grid`.

This solves a common design system challenge: aligning interior card elements (headers, body content, footers) across a row of cards that have varying content lengths.

```css
/* Parent Grid defining 3 columns */
.parent-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto auto auto;
}
/* Child Card spanning rows, utilizing subgrid for row alignment */
.card-item {
  grid-row: span 3;
  display: grid;
  /* Align interior tracks to the parent's row tracks */
  grid-template-rows: subgrid; 
}
```

---

## 3. Properties / API
The API design below defines a robust interface that integrates with the base `Box` substrate while providing comprehensive, type-safe control over native CSS Grid features.

### Container Props (`Grid`)

| Prop Name | Type | Description | CSS Mapping |
| --- | --- | --- | --- |
| `columns` | `Responsive<PropValue>` | Sets track count or explicit column sizing. Can be a raw number (mapped to `repeat(N, 1fr)`), a token, or a template string. | `grid-template-columns` |
| `rows` | `Responsive<PropValue>` | Sets track count or explicit row sizing. Can be a raw number, token, or template string. | `grid-template-rows` |
| `gap` | `Responsive<SpacingToken>` | Resolves against `Box` spacing scale to apply uniform spacing between all tracks. | `gap` |
| `rowGap` | `Responsive<SpacingToken>` | Resolves against `Box` spacing scale to apply spacing between rows only. | `row-gap` |
| `columnGap` | `Responsive<SpacingToken>` | Resolves against `Box` spacing scale to apply spacing between columns only. | `column-gap` |
| `areas` | `Responsive<string[]>` | Defines a multi-line visual template layout mapping named areas. | `grid-template-areas` |
| `autoFlow` | `Responsive<'row' \| 'column' \| 'row dense' \| 'column dense'>` | Controls how auto-placed items are inserted into the tracks. | `grid-auto-flow` |
| `justifyItems` | `Responsive<'start' \| 'end' \| 'center' \| 'stretch'>` | Sets alignment of items within their grid cells along the inline axis. | `justify-items` |
| `alignItems` | `Responsive<'start' \| 'end' \| 'center' \| 'stretch' \| 'baseline'>` | Sets alignment of items within their grid cells along the block axis. | `align-items` |
| `justifyContent` | `Responsive<...>` | Aligns grid tracks relative to the container boundary along the inline axis. | `justify-content` |
| `alignContent` | `Responsive<...>` | Aligns grid tracks relative to the container boundary along the block axis. | `align-content` |
| `asChild` | `boolean` | Activates polymorphism via Radix Slot, shifting rendering target. | N/A |

### Item/Cell Props (`Grid.Item`)

| Prop Name | Type | Description | CSS Mapping |
| --- | --- | --- | --- |
| `colSpan` | `Responsive<number \| 'full'>` | The number of column tracks the cell should span. `'full'` resolves to `1 / -1`. | `grid-column: span N` or `1 / -1` |
| `rowSpan` | `Responsive<number \| 'full'>` | The number of row tracks the cell should span. `'full'` resolves to `1 / -1`. | `grid-row: span N` or `1 / -1` |
| `colStart` | `Responsive<number \| 'auto'>` | Explicit track line where the item column starts. | `grid-column-start` |
| `colEnd` | `Responsive<number \| 'auto'>` | Explicit track line where the item column ends. | `grid-column-end` |
| `rowStart` | `Responsive<number \| 'auto'>` | Explicit track line where the item row starts. | `grid-row-start` |
| `rowEnd` | `Responsive<number \| 'auto'>` | Explicit track line where the item row ends. | `grid-row-end` |
| `area` | `Responsive<string>` | Places the item directly in a matching named area template. | `grid-area` |
| `justifySelf` | `Responsive<'start' \| 'end' \| 'center' \| 'stretch'>` | Overrides inline alignment for this item specifically. | `justify-self` |
| `alignSelf` | `Responsive<'start' \| 'end' \| 'center' \| 'stretch' \| 'baseline'>` | Overrides block alignment for this item specifically. | `align-self` |

### Responsive Typings
To maintain consistency across the design system, properties accept values in three formats:

```typescript
// 1. Scalar / Simple Token
<Grid columns={3} gap={4} />
// 2. Viewport Breakpoint Object (Legacy/Standard)
<Grid columns={{ xs: 1, md: 3, lg: 4 }} gap={{ xs: 2, md: 4 }} />
// 3. Auto-Grid Intrinsic Layout Prop (Bypasses viewport breakpoints)
<Grid columns="auto-fit" minChildWidth="250px" />
```

---

## 4. States and Variants
As a structural component, the `Grid` has no built-in interaction states (like `:hover`, `:focus`, or `:active`). Instead, its visual variations are defined by the structural layout genres it represents.

### Genre 1: The Column Grid (Fixed Columns)
This variation uses a set number of columns (typically 12 or 16) where child elements use explicit column spans to align to the layout grid.

```tsx
<Grid columns={12} gap={4}>
  <Grid.Item colSpan={{ xs: 12, md: 4 }}>
    <Sidebar />
  </Grid.Item>
  <Grid.Item colSpan={{ xs: 12, md: 8 }}>
    <MainContent />
  </Grid.Item>
</Grid>
```

### Genre 2: The Auto-Grid (The "RAM" Variant)
This variation uses an intrinsic sizing mechanism, allowing the grid to adjust the number of columns automatically based on the width of its container. This removes the need to manually declare breakpoint arrays for standard responsive lists.

```tsx
// SimpleGrid pattern mapping to repeat(auto-fill, minmax(280px, 1fr))
<Grid variant="auto-fit" minChildWidth="280px" gap={4}>
  <Card />
  <Card />
  <Card />
</Grid>
```

### Genre 3: The Named-Areas Template Grid
This variation uses a structured area layout map to position elements. This pattern works well for top-level application layouts or complex, asymmetrical UI shells.

```tsx
<Grid 
  areas={{
    xs: [ "header", "main", "sidebar" ],
    md: [ "header header", "sidebar main" ]
  }}
  columns={{ xs: "1fr", md: "240px 1fr" }}
  rows="auto 1fr"
>
  <Grid.Item area="header"><Header /></Grid.Item>
  <Grid.Item area="sidebar"><Navigation /></Grid.Item>
  <Grid.Item area="main"><ContentContainer /></Grid.Item>
</Grid>
```

### Subgrid-Enabled Variants
This variant forces nested child elements to align to the row tracks of their parent grid. This ensures that interior layout rows (like card headers or CTA buttons) align horizontally across columns, regardless of content height differences.

```tsx
// Parent structural grid
<Grid columns={3} gap={4}>
  {/* Card Container functioning as Subgrid wrapper */}
  <Grid.Item rowSpan={3} display="grid" gridTemplateRows="subgrid">
    <h3>Card Title</h3> {/* Header row - aligns across cards */}
    <p>Flexible descriptive body content...</p> {/* Body row - aligns across cards */}
    <Button>Call to Action</Button> {/* Footer row - aligns across cards */}
  </Grid.Item>
</Grid>
```

---

## 5. Usage Guidance

### Grid vs. Stack: The Layout Decision Matrix
Choosing between `Stack` and `Grid` should be determined by the number of dimensions the layout needs to control.

```
                    Is layout alignment required along
                       BOTH columns AND rows?
                                │
               ┌────────────────┴────────────────┐
               ▼ YES                             ▼ NO
       ┌───────────────┐                 ┌───────────────┐
       │   Use GRID    │                 │   Use STACK   │
       └───────────────┘                 └───────────────┘
  (e.g., Dashboards, Cards,         (e.g., Simple lists, Forms,
   Asymmetric Page Layouts)          Buttons, wrapped tag rows)
```

* **Use `Stack` (1D)** when elements flow along a single direction (even if they wrap, like a list of tags). `Stack` handles simple item spacing and logical separation along a single axis.
* **Use `Grid` (2D)** when you need to align elements horizontally and vertically at the same time. If items in row 2 must align vertically with items in row 1, `Grid` is the appropriate layout engine.

#### The "Anti-Pattern" Rule: No 1D Grid Implementations
Do not use `Grid` to lay out simple 1D lists. Using `<Grid columns={1}>` as a wrapper for list elements increases browser layout calculation costs and duplicates the responsibilities of the `Stack` component.

```tsx
/* ❌ AVOID: Using Grid to emulate a basic vertical Stack */
<Grid columns={1} gap={3}>
  <Item /> <Item />
</Grid>
/* ✅ RECOMMENDED: Use Stack for single-axis flow control */
<Stack direction="vertical" gap={3}>
  <Item /> <Item />
</Stack>
```

### Choosing the Right Grid Genre
* **Use Column Grids** for top-level pages or nested columns that align to a global layout system (e.g., landing page hero grids).
* **Use Auto-Grids (RAM Pattern)** for dynamic lists where child elements have uniform dimensions (e.g., card displays, product matrices, search results).
* **Use Template Grids** when designing asymmetrical layouts where specific components belong in defined regions (e.g., app bars, control consoles, media players).

---

## 6. Accessibility (A11Y)
Because CSS Grid allows elements to be placed anywhere within a 2-dimensional space, it introduces potential accessibility risks.

### The Presentational / Semantic Dualism
By default, applying `display: grid` on a standard block element creates an unstyled presentational container. It does not communicate any implicit semantic roles to assistive technologies.

#### The `role="grid"` Naming Collision
There is a common point of confusion between CSS Layout Engines and ARIA semantic roles:
* **`display: grid` (CSS):** A CSS layout mechanism used to position child elements in two dimensions. It has no impact on accessibility semantics.
* **`role="grid"` (ARIA):** An interactive data grid structure (similar to an editable spreadsheet) containing focusable grid cells (`role="gridcell"`) organized in rows (`role="row"`). This pattern requires keyboard navigation management (using arrow keys to focus cells) and is not intended for static page layout grids.

```tsx
/* ❌ AVOID: Do not apply role="grid" to a layout helper */
<div className="layout-grid" role="grid">
  <div role="row"><div role="gridcell">Content...</div></div>
</div>
/* ✅ RECOMMENDED: Keep layout containers presentationally neutral */
<div className="layout-grid">
  <div>Content...</div>
  <div>Content...</div>
</div>
```

### The DOM-Order-vs-Visual-Order Trap
Because properties like `grid-template-areas`, `grid-column-start`, and `order` make it easy to reposition elements visually, they can easily cause the visual layout to diverge from the DOM order.

```
DOM Order (Screen Readers & Keyboard Focus Order):
[ Box A ] ────► [ Box B ] ────► [ Box C ]
Visual Layout via CSS Grid Placement:
┌───────────────┬───────────────┬───────────────┐
│    Box C      │    Box A      │    Box B      │  <-- Visual Order diverges from DOM
└───────────────┴───────────────┴───────────────┘
```

When a keyboard user presses `Tab`, focus moves according to the underlying DOM order, not the visual placement. When visual ordering and keyboard focus order mismatch, it violates WCAG requirements:
* **WCAG 2.1 Success Criterion 1.3.2 (Meaningful Sequence):** Content must be presented in a sequence that preserves its meaning.
* **WCAG 2.1 Success Criterion 2.4.3 (Focus Order):** Focusable components must receive focus in an order that preserves usability and meaning.

### The No-Reorder Rule
Design systems should enforce the following standard for the `Grid` component:

> **The visual layout order of focusable items inside a grid must match their source code order in the DOM.**

Do not use grid placement properties or the `order` property to move focusable elements to a different order than they appear in the DOM. If an item needs to be displayed first visually, it must be declared first in the DOM structure.

```tsx
/* ❌ AVOID: Visually placing the primary button first while declaring it last in DOM */
<Grid columns={3}>
  <Grid.Item area="side">Secondary Info</Grid.Item>
  <Grid.Item area="main">Main Text</Grid.Item>
  <Grid.Item area="hero" colStart={1} colEnd={3}>Primary Action (Visual Start, DOM End)</Grid.Item>
</Grid>
/* ✅ RECOMMENDED: Arrange source order to match visual flow */
<Grid columns={3}>
  <Grid.Item area="hero" colStart={1} colEnd={3}>Primary Action (DOM and Visual Start)</Grid.Item>
  <Grid.Item area="main">Main Text</Grid.Item>
  <Grid.Item area="side">Secondary Info</Grid.Item>
</Grid>
```

### Semantic `as` Support for Interactive Grids
When grid containers are used to render standard HTML list structures (such as a list of blog posts or a navigation group), developers should map the output element to semantic tags like `<ol>` or `<ul>`.

```tsx
<Grid as="ul" columns={3} gap={4}>
  <Grid.Item as="li">Card Item 1</Grid.Item>
  <Grid.Item as="li">Card Item 2</Grid.Item>
  <Grid.Item as="li">Card Item 3</Grid.Item>
</Grid>
```

---

## 7. Content Guidelines
To maintain clean and accessible layout structures, design system guidelines should define clear boundaries between layout components and content.

### Separation of Layout and Content
* **Do not use `Grid` containers to apply visual styling** like borders, backgrounds, or custom scroll behaviors. The `Grid` component's sole responsibility is defining the track structure and spacing.
* **Do not scatter content source order** to achieve specific visual alignment. Instead of manually positioning scattered individual cells, use the parent grid's formatting controls (like `justify-content` and `align-items`) to manage general spacing.

```tsx
/* ❌ AVOID: Adding visual boundaries to layout primitives */
<Grid className="border border-gray-200 bg-white p-6 shadow-sm" columns={3}>
  <Card />
</Grid>
/* ✅ RECOMMENDED: Nest a Styled Container inside a Layout Primitive */
<Grid columns={3}>
  <div className="border border-gray-200 bg-white p-6 shadow-sm">
    <Card />
  </div>
</Grid>
```

---

## 8. Motion and Transition
Layout engines generally avoid defining built-in animations. Transitions on structural containers can cause layout reflows that degrade application performance.

### Structural Reflow Guidelines
* **The FLIP Animation Pattern (First, Last, Invert, Play):** When grid items are added, removed, or reordered dynamically, do not animate the grid tracks directly. Instead, use the FLIP pattern to animate transition paths on the child elements.
* **Respect User Preferences:** Wrap layout animations in `@media (prefers-reduced-motion: reduce)` to disable transitions for users who prefer reduced motion.

```css
@media (prefers-reduced-motion: reduce) {
  .grid-item-transform {
    transition: none !important;
    transform: none !important;
  }
}
```

### The Grid-Template Animation Constraint
Be aware that transitioning `grid-template-columns` and `grid-template-rows` natively in CSS is not supported smoothly in all engines. Animating structural tracks can lead to jittery transitions and performance issues. For resizing panels, animate the `width` or `transform` properties of the child elements instead of altering the grid tracks directly.

---

## 9. Internationalization (I18N)
Because layout direction varies by language, the layout engine must adapt to different text directions.

### CSS Logical Properties for Bi-directional Layouts
Modern layout systems use CSS logical properties rather than physical sides (like `left` and `right`). This ensures that margins, padding, and positioning flip automatically when switching from Left-to-Right (LTR) to Right-to-Left (RTL) languages.

The parent `Grid` container's track alignment properties map cleanly to logical equivalents:
* `justify-items: start` aligns items to `left` in LTR, and automatically flips to `right` in RTL.
* `grid-column: 1 / -1` scales correctly across both directions because track numbers start from the logical inline start.

```
LTR: Tracks flow Left-to-Right
Track 1 ──────────► Track 2 ──────────► Track 3
[ Cell A ]          [ Cell B ]          [ Cell C ]
RTL: Tracks flow Right-to-Left
Track 3 ◄────────── Track 2 ◄────────── Track 1
[ Cell C ]          [ Cell B ]          [ Cell A ]
```

### Logical Area Templates
If a grid uses `grid-template-areas` with named zones, define columns based on semantic roles so they map logically when layout flow is reversed in RTL.

```tsx
// The browser automatically maps the columns visually from right-to-left
<Grid areas={["navigation main-content"]} columns="250px 1fr" />
```

---

## 10. Naming
Design system naming conventions vary across organizations. The tables below map common naming conventions for these layout patterns.

### Naming Conventions

| Strategy | Container Element | Child Cell Element | Representing Systems |
| --- | --- | --- | --- |
| **Grid Unified** | `Grid` | `Grid.Item` or `Grid.Cell` | Radix Themes, MUI, Polaris, Adobe Spectrum, Carbon, Base Web |
| **Split Specialty** | `Grid` / `SimpleGrid` | `GridItem` | Chakra UI |
| **Row/Col Legacy** | `Row` | `Col` | Bootstrap, Ant Design |
| **Direct Mapping** | `Columns` | `Column` | Braid, Seek |

### The System Default recommendation
For starting a modern design system from scratch, we recommend using a unified pattern:
* Use a single **`Grid`** component as the parent container.
* Use a **`Grid.Item`** component for child elements that need explicit sizing or alignment overrides.

This pattern clearly communicates parent-child relationships, prevents global scope pollution, and provides a clean naming convention that avoids collisions with interactive components (like a `DataGrid` or Table).

---

## 11. Implementation Notes

### Transitioning to CSS Grid
Modern design systems should build exclusively on native CSS Grid. Do not carry over legacy float-based structures, negative-margin flexbox grids, or percentage-based width calculations.

```typescript
// Core implementation style generation
export const serializeGridProps = (props: GridProps) => {
  const styles: React.CSSProperties = {};
  if (props.columns) {
    styles.gridTemplateColumns = typeof props.columns === 'number'
      ? `repeat(${props.columns}, minmax(0, 1fr))`
      : props.columns;
  }
  if (props.gap) {
    styles.gap = `var(--space-${props.gap})`;
  }
  return styles;
};
```

### Modern Platform Implementations

#### CSS Grid Gap Native Support
The `gap` property has been universally supported in CSS Grid since 2018 (while Flexbox `gap` support arrived later in 2021). Relying on native `gap` eliminates the need to use negative margin hacks on parent containers to spacing layout columns.

```css
.ds-grid {
  display: grid;
  gap: var(--space-4);
  row-gap: var(--space-3);
  column-gap: var(--space-4);
}
```

#### Container Queries for Responsive Sizing
Rather than relying on window resize listeners or media queries, use CSS container queries (`@container`) to create layouts that scale based on the space their parent element provides.

```css
.layout-parent-wrapper {
  container-type: inline-size;
  container-name: grid-host;
}
@container grid-host (max-width: 480px) {
  .responsive-grid-target {
    grid-template-columns: 1fr !important;
  }
}
```

#### Subgrid Support
`subgrid` is now supported in all major browsers (as of early 2024). It is a standard solution for aligning nested components across layout tracks.

```css
.ds-grid-subgrid {
  grid-row: span 3;
  display: grid;
  grid-template-rows: subgrid;
}
```

---

## 12. Related and Alternative Components

```
                ┌───────────────────────────────────┐
                │        Box (as / asChild)         │
                └─────────────────┬─────────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
      ┌───────────────────────┐       ┌───────────────────────┐
      │         Stack         │       │         Grid          │
      │   (1D Layout Engine)  │       │   (2D Layout Engine)  │
      └───────────────────────┘       └───────────┬───────────┘
                                                  ▼
                                      ┌───────────────────────┐
                                      │       Composes        │
                                      └───────────┬───────────┘
                ┌─────────────────────────────────┼─────────────────────────────────┐
                ▼                                 ▼                                 ▼
    ┌───────────────────────┐         ┌───────────────────────┐         ┌───────────────────────┐
    │     Card Gallery      │         │ AppShell / PageLayout │         │ Aligning Form Columns │
    └───────────────────────┘         └───────────────────────┘         └───────────────────────┘
```

### Triad Associations
* **`Box`:** The base primitive that `Grid` stands on. It provides polymorphism, spacing scale integration, and logical property mappings.
* **`Stack`:** The single-axis layout engine sibling. Use `Stack` for one-dimensional layouts, and `Grid` when control over two axes is required.

### Host Layout Compositions
* **Card Galleries:** Use `Grid` with the auto-fit "RAM" pattern to build self-responsive card layouts without media queries.
* **Application Shells / Page Layouts:** Use `Grid` with `grid-template-areas` to define structural regions (header, sidebar, content, footer) in a single component.
* **Form Layouts:** Use `Grid` to align input labels and field elements across rows without needing custom column wrappers.

### Interactive Components (Semantic Boundary)
* **Interactive Data Grids / Tables:** Keep structural layout grids distinct from data grids (`role="grid"` or `<table>`). Data grids manage active keyboard focus and require explicit semantic roles for viewing structured data.

---

## 13. Field POV Evolution

### 1. Grid Engine Realignment (2012–2026)
Historically, grid systems relied on CSS float structures and percentage-based width definitions on child items (e.g., Bootstrap Row/Col). With the wide adoption of CSS Grid, the industry has shifted to container-first track layouts. Modern systems (such as MUI Grid2 and Radix Themes) define layout structures directly on the parent container.

### 2. Spacing Control Evolution
In early flexbox grid implementations, spacing was achieved by applying horizontal padding on items and resetting the edges using negative margins on the parent wrapper. The widespread support for native CSS `gap` has removed this complexity, allowing systems to manage row and column spacing directly.

### 3. Responsive Web Design Shifts
Responsive web design has evolved from viewport-focused media queries (`@media`) to container-sensitive patterns. By combining CSS container queries (`@container`) with intrinsic track definitions (`auto-fit`/`minmax`), layout components can adapt dynamically to the space they are given.

### 4. Alignment of Nested Layouts
Historically, aligning card components with varying content lengths horizontally was a common layout challenge. With the general support of CSS `subgrid` across browser engines in 2024, nested components can now inherit and align to the layout tracks of their parent grid.

---

## 14. Sources Cited
* **CSS Grid Layout Module Level 1 & Level 2 Specs** (W3C Recommendation, updated 2023/2024).
* **MUI (Material UI) - v5 & v6 System Documentation:** Details the transition from legacy Flexbox `Grid` to CSS Grid-based `Grid2` components.
* **Chakra UI System Architecture:** Reference for standard implementation of the `SimpleGrid` and child item spacing patterns.
* **Radix Themes:** Reference for standard polymorphism patterns using `asChild` and Radix Slot implementations.
* **Braid Design System (Seek):** Reference for container-based column design and 1D vs. 2D layout logic.
* **W3C WCAG 2.1 Guidelines:** References for Accessibility Success Criteria 1.3.2 (Meaningful Sequence) and 2.4.3 (Focus Order) regarding DOM vs. visual layout.

---

## 15. Agent-Consumable Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "name": "Grid",
  "type": "layout",
  "inherits": "Box",
  "sibling": "Stack",
  "description": "A two-dimensional layout engine built on native CSS Grid, managing track layout across columns and rows simultaneously.",
  "status": "stable",
  "lastUpdated": "2026-06-17",
  "props": {
    "columns": { "type": "ResponsiveValue<number | string>", "description": "Sets column tracks using explicit counts or standard grid template strings.", "responsive": true },
    "rows": { "type": "ResponsiveValue<number | string>", "description": "Sets row tracks using explicit counts or standard grid template strings.", "responsive": true },
    "gap": { "type": "ResponsiveValue<SpacingToken>", "description": "Sets uniform row and column spacing, resolving values against the design system spacing scale.", "responsive": true },
    "rowGap": { "type": "ResponsiveValue<SpacingToken>", "description": "Sets spacing between row tracks.", "responsive": true },
    "columnGap": { "type": "ResponsiveValue<SpacingToken>", "description": "Sets spacing between column tracks.", "responsive": true },
    "areas": { "type": "ResponsiveValue<string[]>", "description": "Defines named layout areas to place child components visually.", "responsive": true },
    "autoFlow": { "type": "ResponsiveValue<'row' | 'column' | 'row dense' | 'column dense'>", "default": "row", "responsive": true },
    "justifyItems": { "type": "ResponsiveValue<'start' | 'end' | 'center' | 'stretch'>", "default": "stretch", "responsive": true },
    "alignItems": { "type": "ResponsiveValue<'start' | 'end' | 'center' | 'stretch' | 'baseline'>", "default": "stretch", "responsive": true },
    "justifyContent": { "type": "ResponsiveValue<...>", "responsive": true },
    "alignContent": { "type": "ResponsiveValue<...>", "responsive": true }
  },
  "subcomponents": {
    "Item": {
      "name": "Grid.Item",
      "inherits": "Box",
      "description": "An optional child component used to control spacing, sizing, and position within the layout tracks.",
      "props": {
        "colSpan": { "type": "ResponsiveValue<number | 'full'>", "responsive": true },
        "rowSpan": { "type": "ResponsiveValue<number | 'full'>", "responsive": true },
        "colStart": { "type": "ResponsiveValue<number | 'auto'>", "responsive": true },
        "colEnd": { "type": "ResponsiveValue<number | 'auto'>", "responsive": true },
        "rowStart": { "type": "ResponsiveValue<number | 'auto'>", "responsive": true },
        "rowEnd": { "type": "ResponsiveValue<number | 'auto'>", "responsive": true },
        "area": { "type": "ResponsiveValue<string>", "responsive": true },
        "justifySelf": { "type": "ResponsiveValue<'start' | 'end' | 'center' | 'stretch'>", "responsive": true },
        "alignSelf": { "type": "ResponsiveValue<'start' | 'end' | 'center' | 'stretch' | 'baseline'>", "responsive": true }
      }
    }
  },
  "accessibility": {
    "role": "none",
    "collisionWarning": "CSS display:grid layout wrappers do not carry semantic grid roles. Do not apply role='grid' unless building an interactive keyboard-navigable spreadsheet interface.",
    "focusPolicy": "Source order in the DOM must match the visual layout order to ensure logical keyboard focus paths (WCAG SC 1.3.2 & 2.4.3)."
  }
}
```
