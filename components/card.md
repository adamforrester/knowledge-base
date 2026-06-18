---
okf_version: "0.1"
type: component-brief
title: Card
description: The first styled surface and the Foundations-meets-Layout convergence host — a field-truth study of the surface/elevation model (elevated/filled/outlined + the elevation tokens), the slot model (compound Card.Header/Body/Footer/Media vs props + the full-bleed-media Bleed trap), the interactive-card nested-interactive problem + the stretched-link pattern (one real link + ::after, secondary actions z-indexed above; the Roselli verbosity data; the MUI CardActionArea button→div bug) vs CardActionArea vs whole-card-<a>, the equal-height / card-as-Grid-cell / subgrid (+ the flex footer-pinned fallback), and the padding/media-bleed trap — standing on Box (the surface) + Stack (the body), composing Avatar/Badge/Tag/Skeleton/Button/Text/Media, with the practice's defaults.
tags: [components, layout]
category: Layout
status: stable
aliases: [Tile, Panel, Well, Surface, ClickableTile, SelectableTile, ExpandableTile, CardView]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Card

> A Card is the **first styled surface** — the component where Box's deliberate neutrality *ends* and visual chrome (background, border, radius, **elevation**) *begins*, and the **convergence host where the Foundations cluster meets Layout**. It is the fourth Layout brief and the structural answer to the developer impulse to slap utility classes on a generic container: a fully-styled, **in-flow** surface that groups related content into a bounded, elevated unit. It is literally the answer to Box's rule — *"if you're adding chrome to a Box, you want a Card."* It stands on **Box** (the surface — the polymorphic `as`/`asChild` Slot, the token-mapped background/border/radius, the padding from the spacing scale, the zero-runtime delivery, the logical-property RTL — see box) and **Stack** (the body layout — header/media/body/footer stacked with `gap`, owning the no-external-margin discipline — see stack); Card adds the *delta* (the chrome, the slots, the interactivity). It **composes the Foundations cluster** — Avatar, Badge, Tag, Skeleton, Button, Heading/Text, Image/Media (see avatar, badge, tag, skeleton, button, link) — the brief where the Foundations work pays off. And it is the **cell of a Grid gallery** (the auto-grid RAM pattern; equal-height via subgrid — see grid). Three contested debates define it: **the surface/elevation model** (elevated / filled / outlined + the elevation tokens), **the slot model** (compound `Card.Header/Body/Footer/Media` vs a monolithic prop API + the full-bleed-media trap), and **the interactive-card problem** (the nested-interactive trap and the stretched-link pattern that resolves it — §6). What it *isn't*: a **Box** (neutral, no chrome — reach for Box when you *don't* want a surface), a **Section** (a *semantic region* / landmark, not a visual surface — not yet briefed), or a **Dialog/Popover** (overlay surfaces that float on the top layer and trap focus — a Card is *in-flow* — see dialog, popover).

---

## 1. Framing
A Card marks the architectural boundary where abstract layout neutrality concludes and opinionated visual containment begins. Its value is *composition*: it invents no new typography or interactive primitives, it hosts the Foundations cluster within rigid anatomical slots without local CSS overrides. It forces the practice to resolve three field-wide debates:
- **The surface / elevation model** — how the interface communicates depth and interactivity without hardcoded shadows, aligning to a token system (Material 3's elevated/filled/outlined — §4).
- **The slot model** — the bundled-prop-driven vs compound-component API tension (the same Text Field resolved), plus the full-bleed-media edge case (§3).
- **The interactive-card accessibility trap** — making a large surface clickable without violating HTML5, overwhelming screen readers, or breaking text selection (§6) — the most fiercely debated topic.

Modern consensus: a Card inherits Box's polymorphism + zero-runtime delivery, uses a Stack internally for deterministic `gap`, acts as a Grid child leveraging subgrid for equal-height alignment, and resolves interactivity via the stretched-link pattern. What it *isn't*: a **Box** (no chrome — the constrained-over-open reach is Box when there's no surface; see box), a **Section** (a full-width semantic document landmark, not an in-flow bounded object — not yet briefed), or a **Dialog/Popover** (the overlay layer, focus-trapping; a Card stays in the document flow — see dialog, popover). Why systems disagree: the slot API, the variant/elevation model, and the interactive-card pattern.

## 2. Anatomy and parts
- **the surface (exterior)** — structurally a **Box**: the bounding container with the **background** token (a "Surface"/"Layer" color), the **border** / **border-radius** / **elevation** tokens, and the **inset** (internal padding from the spacing scale). The chrome Box deliberately lacks (see box).
- **the interior (the body Stack)** — a vertical **Stack** enforcing the no-external-margin discipline on the slots (no margin-collapse, deterministic `gap` — see stack). The slots, top to bottom:
  - **header** — the primary heading + optional Avatar/overline + secondary actions (an overflow menu / "Edit" button); horizontal.
  - **media** — image/video/data-viz; the **full-bleed** challenge (breaking the inset to go edge-to-edge — §11).
  - **body** *(required)* — the primary content (typography, lists, tag clusters); drives the card's vertical expansion.
  - **footer / actions** — primary/secondary Buttons, often justified to opposite edges; + metadata (Tags, timestamp).
- **the optional interactive layer** — an invisible masking layer (the stretched-link `::after`, or a `CardActionArea`) when the whole surface is one clickable target, separating pointer events from the visual structure (§6).
- **the composed Foundations contents** — Avatar (author), Badge (status), Tag (categories), Skeleton (loading), Button (actions), Heading/Text, Image/Media. Card is the *host*, not the author.

## 3. Properties / API
The field has **overwhelmingly converged on the compound-component pattern** for complex surfaces — it mitigates prop-drilling, enhances semantic flexibility, and lets consumers inject Foundations components between slots and control HTML semantics granularly:
- **the slot API (compound):** `Card.Header` / `Card.Media` / `Card.Body` / `Card.Footer` (+ `Card.Actions`) — MUI `CardHeader`/`CardMedia`/`CardContent`/`CardActions`; Chakra `Card.Root`/`Header`/`Body`/`Footer`; Ant `Card.Meta` (avatar/title pairing) + `Card.Grid`; React Aria `CardPreview`/`Content`/`Footer`. The practice leans **compound** (a monolithic `title`/`media`/`footer` prop API is the convenience layer for the simplest case — the bundled-vs-composed tension Text Field resolved; see text-field).
- **`variant` / appearance** — **elevated** / **filled** / **outlined** (§4). The headline visual axis.
- **`size` / density** — small / medium / large → the internal padding scale (spacing tokens); `padding={0}` for full-bleed media.
- **`interactive` / `clickable` (+ `href` / `onClick`)** — whether the whole card is one target (→ the hover-elevation + focus ring + the stretched-link wiring — §6).
- **`selected`** — for card *collections* (selectable card grids — `SelectableTile`/`CardView`; `aria-selected`).
- **`elevation`** — the shadow-depth token (resting vs hover).
- **`as` / `asChild`** — inherited from Box: morph the `div` into `article`/`li`/`section` for semantics (§6).
- **the full-bleed media solutions (the API divergence):** **(a)** a dedicated **`Card.Media`** that lives as a *sibling* of the padded content so it ignores the inset (MUI `CardMedia`); **(b)** a standalone **`Bleed`** component that pulls nested content outside the padding via negative logical margins (Chakra `Bleed`, Polaris `Bleed` — composable, axis-specific); **(c)** the consumer hand-rolls the negative margin (§11). The practice ships a `Card.Media` slot *and* a `Bleed` escape hatch.

## 4. States and variants
- **States:**
  - **default (non-interactive)** — a static surface; no interaction states (as light as Box).
  - **interactive** — **hover** (a token shift: a background transition on *filled*, an **elevation lift** on *elevated* — increasing the shadow blur + `translateY(-2px)`), **focus-visible** (a high-contrast focus ring on the **whole card** — WCAG 2.4.7), **active** (a press).
  - **selected** — card collections: a prominent border + background shift + an injected `SelectionIndicator` (checkbox/radio); `aria-selected` (IBM Carbon `SelectableTile`, React Aria `CardView`).
  - **loading** — the card rendered as a **Skeleton**: the structural container stays intact, the internal typography/avatars/media become shimmer placeholders, holding the grid's height stable while data resolves (see skeleton).
- **Variants:**
  - **surface:** **elevated** (base surface + a drop-shadow elevation token, pulls forward on the z-axis — separation from noisy backgrounds) / **filled** (a tonal offset, *zero* shadow — low-emphasis grouping in dense views) / **outlined** (transparent bg + a 1px high-contrast border — strict boundaries, no depth).
  - **interactivity:** static / whole-card-clickable / actions-inside.
  - **media:** no-media / top-media / full-bleed.
  - **structure:** plain / **sectioned** (multiple divided regions — Polaris).
  - **density:** comfortable / compact.

## 5. Usage guidance
- **Use a Card for:** grouping related content into a **bounded, in-flow surface** — a product/article tile, a profile, a dashboard widget, a settings group, a media preview. The signal: the content forms a *unit* that benefits from a visual boundary and often tiles alongside peers.
- **Card vs the alternatives (the boundaries):**
  - **vs Box** — the boundary is *visual chrome*: if the container needs a border/background/shadow to demarcate it from the canvas → Card; if it purely orchestrates spacing/alignment → **Box/Stack** (see box).
  - **vs Section** — the boundary is *semantics and flow*: a **Section** is a semantic document landmark spanning the layout width; a Card is an in-flow *object/entity* (a profile, an article preview). (Not yet briefed.)
  - **vs Dialog/Popover** — those are *overlay* surfaces (top layer, focus-trapping); a Card is *in-flow* — same elevation vocabulary, different layer (see dialog, popover).
  - **vs a list/table row** — the boundary is *data heterogeneity*: Cards for heterogeneous, image-heavy content; **lists/tables** for homogeneous, dense, comparable records that need rapid vertical scanning (don't card-ify a data table — see table).
- **The cardinal constraints:**
  - **Don't nest cards** — nesting surfaces destroys the elevation scale, clutters, and breaks the interface's mental model.
  - **Avoid "card fatigue"** — boxing *every* piece of text makes interfaces cluttered, disconnected, and hard to scan; the surface should be *meaningful*, not a default wrapper.
  - **The whole-card-clickable vs actions-inside call:** if the card is a *single unified entity* (an article, a product link) → the whole surface routes to it (maximize the target), via the stretched-link. If it's a *widget with multiple distinct tools* or needs text selection → the surface stays **passive**, housing independent buttons (§6).
- **Equal-height in a gallery** — when cards tile, align titles/bodies/footers across the row via the Grid auto-grid + **subgrid** (or the flex footer-pinned fallback — §11).

## 6. Accessibility
Card has **no implicit role by default** — a generic container (inherits Box's neutrality; the element it renders via `as` carries semantics — `article` for a self-contained piece, `li`/`listitem` within a grid gallery, `section`/`region` only *with* a label). The crux is **the interactive card**, the most fiercely debated topic in front-end UI.

- **The nested-interactive trap (two failures).** Wrapping the whole card in an `<a>`/`<button>`:
  - **HTML-validity:** a `<button>` permits only *phrasing* content, so block `<div>`s inside it violate the spec — *the exact bug that forced MUI's `CardActionArea` to switch its DOM from `<button>` to `<div role="button">`*. And an interactive element *inside* the card link (a bookmark button) is **interactive-in-interactive** — browsers boot the inner control out of the hierarchy, rendering it unusable.
  - **Screen-reader verbosity:** a whole-card link forces the SR to announce the *entire* textual content (timestamps, body, metadata) as one massive link label. Adrian Roselli documented tabbing onto such a link taking **upward of 25 seconds of continuous speech** before the role "link" is announced; arrowing re-announces every chunk as a link — obfuscating the interface.
- **The stretched-link pattern (the settled accessible answer — Heydon Pickering's *Inclusive Components*).** Keep the card a **non-interactive container** (`position: relative`); wrap **only the heading text** in one `<a>` and give that link a **`::after { position: absolute; inset: 0 }`** stretched over the whole surface. Result: the entire card is clickable, but there's exactly **one real link** in the a11y tree, named concisely by the title (not "read more", not the whole body). **Secondary actions** get `position: relative` (+ `z-index`) to sit *above* the stretched mask and stay independently clickable without nesting violations.
  - **The costs:** the invisible `::after` **prevents text selection** over the card (a known trade-off — JS workarounds with mouse-down duration thresholds exist but are brittle; the practice **accepts the text-selection cost** for bulletproof SR support); and the **focus ring must render on the whole card** (style the card from the link's `:focus-within`), not just the title.
- **The alternatives:** **`CardActionArea`** (MUI — a `<div role="button">` wrapping *only* the clickable region, actions *outside* it; avoids nesting by separation, but constrains the layout) vs **whole-card-`<a>`** (valid *only* when there are no inner interactives — a pure navigation tile).
- **Heading structure** — the card title is a real heading at the right outline level; a gallery is often `<ul>`/`<li>` so the count + relationship reach AT (the list-semantics rule from Stack — see stack).
- **WCAG SCs:** **2.1.1** (keyboard — the target operable), **2.4.7** (focus visible — the whole-card ring), **4.1.2** (name/role/value — the link's name from the title; `aria-selected` for collections), **1.3.1** (info & relationships — `article`/`li`/heading), **2.5.5 / 2.5.8** (target size — the stretched link is large, which helps; secondary actions inside must still meet the minimum). The interactive-card pattern is the whole a11y story; a static card is as light as Box.

## 7. Content guidelines
- **The card title** — concise, descriptive, and the **accessible name** of the clickable card (the sole stretched-link target). Make it *specific* ("2024 Annual Report", not "Document") — it's what a screen-reader user hears as the link — and a real heading.
- **Scannable + truncation-resilient** — a card is glanced at in a gallery; enforce truncation limits (`-webkit-line-clamp` — typically a 2-line title / 3-line body max), but **critical distinguishing information must not live only in truncated text** (it disappears at the clamp).
- **Mitigate action overload** — one primary action per card; secondary actions limited to one or two icon buttons (hit-area crowding, misclicks, cognitive load); collapse more into an overflow menu in the header. If the whole card is clickable, footer actions are *secondary* (and z-indexed above the stretched link — §6).
- **Don't overload the card** — one unit of meaning; a title + media + five tags + three buttons + an avatar + a chart is two components.

## 8. Motion and transition
- **The hover-elevation lift** — interactive *elevated* cards transition `box-shadow` + a subtle `transform: translateY(-2px)` over ~200ms ease-out on hover/focus; *filled* cards shift background. The headline Card motion, token-driven.
- **The loading→content swap** — the Skeleton card crossfades/opacity-interpolates to the real content on resolve, avoiding a jarring flash (the shape-matched, no-CLS swap — see skeleton).
- **Gallery enter/reflow** — cards filtered/sorted/removed in a Grid gallery reflow via **FLIP** (the technique Stack/Grid/Tag share — see stack, grid), applied by the consumer/an animation primitive, not by Card.
- **Reduce-motion** — `prefers-reduced-motion: reduce` collapses all transition durations to 0 (the cue is the elevation/background, not the transition) and disables gallery reflow. Card ships only the hover transition.

## 9. Internationalization
- **RTL is inherited from Box/Stack** — the entire card structure uses **CSS logical properties** (`padding-inline-start` not `padding-left`, `margin-inline-end` not `margin-right`), so Avatar positioning, text alignment, and footer actions mirror automatically under `dir="rtl"` (Arabic/Hebrew) with no JS, inheriting the Box/Stack bidirectional substrate (see box, stack). The card needs no RTL logic of its own.
- **Content expansion + equal-height** — German/Russian can expand text ~30%; the internal Stack must let text wrap natively without breaking bounds, and — critically — the parent Grid must use **subgrid** so that when one card's body row expands for a long translation, all neighbouring cards in that row expand symmetrically to maintain horizontal alignment (§11; see grid).
- The media and chrome are direction-agnostic; only the *content layout* mirrors.

## 10. Naming
- **The field set:** **`Card`** is near-universal (Material, MUI, Chakra, Polaris, Ant, Spectrum, Atlassian, Base Web); **`Tile`** is IBM Carbon's term (`ClickableTile`/`SelectableTile`/`ExpandableTile` — emphasising the tessellating grid-item role over the paper metaphor, and splitting *by interactivity*); **`Panel`**/**`Well`** are older/Bootstrap-era aliases; **`Surface`** is the *underlying concept* (Material's Surface — the elevation primitive a Card specializes); **`CardView`** is React Aria's selectable-collection wrapper.
- **The practice's default — `Card`** with the compound slots **`Card.Header` / `Card.Media` / `Card.Body` / `Card.Footer`** (+ `Card.Actions`). MUI prefers verbose names (`CardActionArea`, `CardContent`); Chakra prefers clean object notation (`Card.Header`, `Card.Body`). Pick **`Body`** over `Content` and hold it consistently (the one slot-naming wobble). Model interactivity as a *prop* + the stretched-link rather than splitting into `ClickableCard`/`SelectableCard` components (Carbon's Tile split is defensible but the practice keeps one `Card`).
- **`Surface` as the shared primitive** — if multiple elevated surfaces exist (Card, Dialog, Popover, Menu), an internal `Surface` (the elevation/radius/background tokens) they all build on is a clean factoring — the elevation equivalent of Box. (Optional; name it if the surfaces proliferate.)
- **Aliases to map:** Tile, Panel, Well, Surface, ClickableTile, SelectableTile, ExpandableTile, CardView.

## 11. Implementation notes
- **The surface on Box** — a Box with token-mapped `background`/`border`/`border-radius`/`box-shadow`(elevation)/`padding`; the variant switches which tokens apply (elevated → shadow, no border; outlined → border, no shadow; filled → tonal bg). Inherit Box's `as`/`asChild` Slot, the spacing scale, the zero-runtime delivery, and the logical-property RTL (see box) — Card adds only the chrome.
- **The slot / compound API** — `Card.Header`/`Media`/`Body`/`Footer` as compound children sharing context (the `Card.Root` provides padding/variant context the slots consume); the body is a **Stack** with a token `gap` (see stack).
- **The full-bleed media (the recurring trap), three approaches:** **(a) sibling slot** — the media lives *outside* the padded content wrapper so it ignores the inset (MUI `CardMedia` as a sibling of `CardContent`) — structural, cleanest; **(b) the `Bleed` component** — a dedicated wrapper applying **negative logical margins** equal to the padding (`margin-inline: calc(var(--card-padding) * -1)`) to pull content edge-to-edge along chosen axes (Chakra/Polaris `Bleed`) — composable; **(c)** the consumer hand-rolls the negative margin. In all cases the radius must clip the media (`overflow: hidden` / matched corners).
- **The stretched-link** — `position: relative` on the card; the primary link's `::after { position: absolute; inset: 0 }`; secondary interactives `position: relative` (+ `z-index`) to sit above the mask (without this explicit z-management the invisible mask intercepts *all* pointer events, making secondary actions dead); style the card's `:focus-within` for the whole-card focus ring; accept the `user-select` cost (§6).
- **Equal-height: subgrid + the flex fallback.** **Subgrid (modern):** the card is *both* a grid item and a grid container — `display: grid; grid-template-rows: subgrid; grid-row: span 3` — so it inherits the parent grid's row tracks and the tallest card's header dictates every card's header height, aligning body and footer rows across the row (replaces the old `ResizeObserver` height-equalization JS — see grid). **Flexbox fallback (legacy / non-subgrid grid):** `display: flex; flex-direction: column; height: 100%` on the card + `flex-grow: 1` on `Card.Body` pins `Card.Footer` to the bottom (the footer-pinned pattern).
- **The interactive elevation/focus** — the hover-lift is a GPU-composited `box-shadow`/`transform` transition; the focus ring is the whole-card outline (§6/§8).
- **Headless vs opinionated** — ship the surface tokens + the slot structure + the interactive/stretched-link wiring + the `Bleed`/`Card.Media` full-bleed solution as the opinionated value; the elevation scale and radius are theme. Own the stretched-link and the full-bleed media so every consumer doesn't re-solve them.

## 12. Related and alternative components
- **Stands on:** **Box** (the surface — bg/border/radius/elevation/padding + the polymorphic `as`/`asChild` + the logical-property RTL — see box) and **Stack** (the body layout — header/media/body/footer with `gap` — see stack).
- **Composes (the Foundations cluster — the convergence):** **Avatar** (the author — see avatar), **Badge** (a status — see badge), **Tag** (categories — see tag), **Skeleton** (the loading card — see skeleton), **Button** (footer actions — see button), **Heading/Text** (title/body), **Image/Media** (the cover). The brief where the Foundations work pays off.
- **The cell of:** a **Grid** gallery (the auto-grid RAM pattern; equal-height via subgrid — see grid).
- **Relates to (interactivity):** **Link** (the stretched-link is a block-link — see link) and **Button** (the link-vs-button-on-a-card decision — see button).
- **Boundary with:** **Dialog/Popover** (overlay surfaces — same elevation vocabulary, different layer; Card is in-flow — see dialog, popover), **Section** (a semantic region, not a visual surface — not yet briefed), and a **list/table row** (dense comparable records — see table; the responsive stacked-table row is a Card).
- **Alias:** IBM Carbon's **Tile** (the same component, split by interactivity); React Aria's **CardView** (the selectable-collection form).

(The first styled surface — where Box's neutrality ends and the Foundations cluster meets Layout. It stands on Box (the surface) + Stack (the body), composes Avatar/Badge/Tag/Skeleton/Button/Text/Media, and is the cell of a Grid gallery. See box/stack for the substrate, avatar/badge/tag/skeleton/button for the composed contents, grid for the gallery + subgrid equal-height, link for the stretched-link, dialog/popover for the overlay-surface boundary, section for the semantic-region boundary. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The monolithic card → the slotted/compound card.** Early React systems used massive prop interfaces (`title="X" avatar={Z}`); too rigid as requirements evolved. Modern systems use compound slots (`Card.Header`/`Body`) + children to maximize composability and inversion of control — the same maturation Text Field shows.
2. **Material's three-variant elevation model settling.** Elevated / filled / outlined (Material 3) became the shared variant vocabulary, formalising the surface/elevation token system over ad-hoc shadows.
3. **The interactive-card a11y settling — the stretched-link over the whole-card-button.** The whole-card-`<button>` wrapper has been thoroughly deprecated by accessibility experts (catastrophic SR verbosity — Roselli's 25-second readout — and interactive-in-interactive HTML violations — MUI's `CardActionArea` `<button>`→`<div role=button>` fix). The CSS **stretched-link** (Heydon Pickering) is the opinionated standard.
4. **Subgrid replacing the height-equalization JS.** The `ResizeObserver` calculations once required to equalize card heights have been replaced by CSS **subgrid** (~2024 — see grid) — a shift in how grids communicate dimensions to children, enabling resilient aligned galleries in pure CSS.
5. **Cards-as-collections.** React Aria's `CardView` abstracted interactive cards into selectable, drag-and-drop, multiselect *data items* with built-in state hooks — pushing the Card from a visual box into an application data component (`aria-selected`/roving focus).

## 14. Sources cited
(Conservative; reconcile with external.) **Google Material 3** — `Card` (the elevated/filled/outlined tri-variant model + shadow mechanics) (2024–2026); **MUI** — `Card` + `CardHeader`/`CardMedia`/`CardContent`/`CardActions`/`CardActionArea` (the compound API + the `<button>`→`<div role="button">` validation fix) (2024–2026); **Chakra UI** — `Card.Root`/`Header`/`Body`/`Footer` + `Bleed` (compound + negative-margin bleed; v2.4+/v3) (2024–2026); **Shopify Polaris** — `Card` + `Bleed` + `BlockStack` (the workhorse surface; sectioned cards; monolithic→composed; `s-card`) (2024–2026); **GitHub Primer** — the Box-based card; link previews (2024–2026); **Adobe React Aria** — `Card`/`CardPreview`/`Content`/`Footer` + `CardView` (selectable/drag-and-drop collections; ~v1.17) (2024–2026); **IBM Carbon** — `Tile` (`ClickableTile`/`SelectableTile`/`ExpandableTile`) (2024–2026); **Ant Design** — `Card` (`Card.Meta`, `Card.Grid`, cover, actions, tabs; v5) (2024–2026); **Atlassian** — `Card` (link-preview cards) (2024–2026); **Base Web (Uber)** — `Card` (2024); **Heydon Pickering** — *Inclusive Components* "Cards" (the stretched-link / pseudo-content pattern + secondary z-index handling; 2018); **Adrian Roselli** — block links / clickable regions (the SR verbosity + nested-button-violation analysis; updated 2025); **CSS** — subgrid equal-height card architecture (~2024). WCAG 2.2 (W3C Recommendation, Oct 2023) — 2.1.1, 2.4.7, 4.1.2, 1.3.1, 2.5.5/2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: card
  name: Card
  aliases: [Tile, Panel, Well, Surface, ClickableTile, SelectableTile, ExpandableTile, CardView]
  category: layout
  status: stable
description: >
  The first styled SURFACE — where Box's deliberate neutrality ends and visual chrome
  (background, border, radius, ELEVATION) begins; the in-flow container that groups
  related content into a bounded, elevated unit, and the convergence host WHERE THE
  FOUNDATIONS CLUSTER MEETS LAYOUT. Literally the answer to Box's 'if you're adding
  chrome to a Box, you want a Card.' NOT a Box (neutral, no chrome), NOT a Section (a
  semantic region/landmark, not a visual surface), NOT a Dialog/Popover (overlay
  surfaces — a Card is IN-FLOW). Stands on Box (the surface) + Stack (the body);
  composes Avatar/Badge/Tag/Skeleton/Button/Text/Media; the cell of a Grid gallery.
anatomy:
  parts:
    - "the surface (exterior): a Box — background ('Surface'/'Layer' token) + border/radius/ELEVATION tokens + the inset (padding from the spacing scale); the chrome Box lacks"
    - "the body Stack (interior): a vertical Stack enforcing no-external-margin + deterministic gap on the slots"
    - "slots: header (heading + Avatar + secondary actions; horizontal) / media (image/video, often FULL-BLEED) / body [required] (the primary content, drives vertical expansion) / footer-actions (primary/secondary Buttons + metadata Tags)"
    - "the optional interactive layer: the stretched-link ::after (or a CardActionArea) masking the surface, separating pointer events from the visual structure"
    - "the composed Foundations contents: Avatar/Badge/Tag/Skeleton/Button/Text/Media — Card is the HOST not the author"
api:
  inherits:
    - box        # the surface — bg/border/radius/elevation/padding + the as/asChild Slot + the logical-property RTL + zero-runtime delivery
    - stack      # the body layout — header/media/body/footer with gap (no-external-margin discipline)
  composes: [avatar, badge, tag, skeleton, button, link, "heading/text", "image/media"]   # the Foundations cluster — the convergence
  props:
    - {name: "slots (Card.Header/Media/Body/Footer/Actions)", type: "compound components", default: ~, required: false, description: "the COMPOUND API (the field converged here — MUI CardHeader/Media/Content/Actions; Chakra Card.Root/Header/Body/Footer; Ant Card.Meta); a monolithic title/media/footer prop API is the convenience layer (bundled-vs-composed, cf. text-field)"}
    - {name: variant/appearance, type: "'elevated' | 'filled' | 'outlined'", default: elevated, required: false, description: "Material 3's three cards: elevated (shadow, z-axis) / filled (tonal bg, zero shadow, low-emphasis) / outlined (1px border, no depth)"}
    - {name: size/density, type: "'sm'|'md'|'lg'", default: md, required: false, description: "the internal padding scale; padding=0 for full-bleed media"}
    - {name: "interactive/clickable (+ href/onClick)", type: "boolean | link", default: false, required: false, description: "whole-card target -> hover-elevation + focus ring + the stretched-link pattern (a11y)"}
    - {name: selected, type: boolean, default: false, required: false, description: "for card COLLECTIONS (SelectableTile/CardView) — a border/bg shift + a SelectionIndicator (checkbox/radio); aria-selected"}
    - {name: elevation, type: "token", default: ~, required: false, description: "the shadow-depth token (resting vs hover)"}
    - {name: as/asChild, type: "ElementType/boolean", default: div, required: false, description: "inherited from Box — morph to article/li/section for semantics"}
  full-bleed-media-solutions: "(a) Card.Media as a SIBLING of the padded content (MUI — ignores the inset; cleanest); (b) a Bleed component applying negative logical margins = the padding (Chakra/Polaris; composable, axis-specific); (c) hand-rolled negative margin. Radius must clip the media (overflow:hidden)"
  withholds: "doesn't author content (hosts it); doesn't expose arbitrary style props (that's Box) — exposes the SURFACE tokens (variant/elevation/padding) + the slots"
states:
  runtime: [default, hover, focus-visible, active, selected, loading]   # interaction states ONLY when interactive
  default-non-interactive: "a static surface has NO interaction states (as light as Box)"
  interactive: "hover = elevation lift (shadow blur + translateY(-2px)) on elevated / bg shift on filled; focus-visible = a high-contrast ring on the WHOLE card (2.4.7); active = a press"
  selected: "card collections — border + bg shift + an injected SelectionIndicator; aria-selected (Carbon SelectableTile, React Aria CardView)"
  loading: "rendered as a Skeleton — the structural container stays intact, internal slots become shimmer placeholders, holding the grid height stable"
variants:
  surface: [elevated, filled, outlined]
  interactivity: [static, whole-card-clickable, actions-inside]
  media: [no-media, top-media, full-bleed]
  structure: [plain, sectioned]            # sectioned = divided regions (Polaris)
  density: [comfortable, compact]
  rendered-element: [article, section, li, div]
accessibility:
  wcag-criteria: ["2.1.1", "2.4.7", "4.1.2", "1.3.1", "2.5.5", "2.5.8"]
  implicit-role: "NONE by default — a generic container (inherits Box's neutrality); the element via as carries semantics (article=self-contained, li/listitem=in a gallery, section/region only WITH a label)"
  nested-interactive-trap:
    html-validity: "a <button> permits only PHRASING content, so block divs inside it violate the spec (the bug that forced MUI CardActionArea from <button> to <div role=button>); an interactive element inside a card-link = interactive-in-interactive (browsers boot the inner control out)"
    verbosity: "a whole-card link forces the SR to announce the ENTIRE textual content as one link label — Roselli documented 25+ SECONDS of speech before 'link' is announced; arrowing re-announces every chunk as a link"
  stretched-link-pattern: "THE settled answer (Heydon Pickering, Inclusive Components 'Cards'): card position:relative (non-interactive); ONE primary link wraps ONLY the heading + gets ::after {position:absolute; inset:0} over the surface -> whole card clickable, ONE real link named concisely by the title; SECONDARY actions get position:relative + z-index to sit ABOVE the mask + stay clickable"
  stretched-link-costs: "the invisible ::after PREVENTS text selection over the card (JS mouse-down-threshold workarounds are brittle; the practice ACCEPTS the cost for bulletproof SR support); the focus ring must render on the WHOLE card (style from :focus-within), not just the title"
  alternatives: "CardActionArea (MUI — a <div role=button> wrapping ONLY the clickable region, actions OUTSIDE it; valid but constrains layout) vs whole-card-<a> (valid ONLY when no inner interactives — a pure nav tile)"
  heading-structure: "the card title is a real heading at the right outline level; a gallery is often ul/li (count + relationship reach AT — the list-semantics rule from Stack)"
content:
  card-title: "concise, descriptive, SPECIFIC ('2024 Annual Report' not 'Document') — the accessible name / the sole stretched-link target; a real heading"
  truncation: "scannable; -webkit-line-clamp limits (~2-line title / 3-line body), BUT critical distinguishing info must NOT live only in truncated text"
  action-overload: "one primary action; secondary limited to 1-2 icon buttons; collapse more into an overflow menu in the header; whole-card-clickable -> footer actions are secondary (z-indexed above the stretched link)"
  dont-overload: "one unit of meaning per card; title + media + 5 tags + 3 buttons + avatar + chart = two components"
motion:
  hover-elevation-lift: "interactive elevated cards transition box-shadow + translateY(-2px) over ~200ms ease-out on hover/focus; filled cards shift bg — the headline Card motion, token-driven"
  loading-swap: "the Skeleton card crossfades/opacity-interpolates to the real content (shape-matched, no CLS)"
  gallery-reflow: "cards filtered/sorted/removed reflow via FLIP (shared with Stack/Grid/Tag), applied by the consumer/an animation primitive"
  reduce-motion: "collapse all transition durations to 0 (the cue is the elevation/bg, not the transition) + disable gallery reflow; Card ships only the hover transition"
i18n:
  rtl-inherited: "the entire structure uses CSS LOGICAL properties (padding-inline-start not padding-left) so Avatar/text/footer actions mirror under dir=rtl with no JS — inherited from Box/Stack; no card-specific RTL logic"
  content-expansion: "DE/RU expand ~30%; the internal Stack must wrap natively; the parent Grid must use SUBGRID so a card expanding its body row for a long translation expands neighbours symmetrically (horizontal alignment)"
  chrome-direction-agnostic: "media + chrome are direction-agnostic; only the content LAYOUT mirrors"
implementation:
  - "the surface on Box: token-mapped background/border/border-radius/box-shadow(elevation)/padding; the variant switches which tokens apply (elevated->shadow no-border; outlined->border no-shadow; filled->tonal bg). Inherit Box's Slot + scale + zero-runtime + logical RTL; Card adds only the chrome"
  - "the slot/compound API: Card.Header/Media/Body/Footer share context from Card.Root (padding/variant); the body is a Stack with a token gap"
  - "the FULL-BLEED MEDIA trap, 3 approaches: (a) Card.Media as a SIBLING of the padded content (MUI — ignores the inset; cleanest); (b) a Bleed component applying negative logical margins = the padding (margin-inline:calc(var(--card-padding)*-1); Chakra/Polaris; composable); (c) hand-rolled. Radius must clip (overflow:hidden)"
  - "the stretched-link: card position:relative; primary link ::after{position:absolute; inset:0}; secondary interactives position:relative + z-index (else the mask intercepts ALL pointer events -> dead actions); style :focus-within for the whole-card ring; accept the user-select cost"
  - "equal-height: SUBGRID (modern) — the card is both a grid item AND container (display:grid; grid-template-rows:subgrid; grid-row:span 3) so the tallest card's header dictates every header height + body/footer align (replaces ResizeObserver JS — see grid). FLEX FALLBACK (legacy) — display:flex; flex-direction:column; height:100% + flex-grow:1 on Card.Body pins Card.Footer to the bottom"
  - "the interactive elevation/focus: hover-lift = a GPU-composited box-shadow/transform transition; the focus ring = the whole-card outline"
  - "headless vs opinionated: ship the surface tokens + the slot structure + the interactive/stretched-link wiring + the Bleed/Card.Media full-bleed solution (the value); the elevation scale + radius are theme. Own the stretched-link + full-bleed so consumers don't re-solve them"
composition:
  stands-on: [box, stack]                  # the surface + the body
  composes: [avatar, badge, tag, skeleton, button, link, "heading/text", "image/media"]   # the Foundations cluster
  cell-of: [grid]                          # the auto-grid gallery + subgrid equal-height
  relates-to: [link, button]               # the stretched-link (a block-link) + the link-vs-button-on-a-card decision
  boundary: [dialog, popover, section, table]   # overlay surfaces (in-flow vs floating) / semantic region / dense comparable rows
  alias-of: ["Carbon Tile", "React Aria CardView"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "the slot API: COMPOUND (Card.Header/Body/Footer/Media — the field converged here, the practice default) vs a monolithic title/media/footer prop API (the bundled-vs-composed tension, cf. text-field)"
    - "Body vs Content slot naming (Chakra CardBody vs MUI CardContent) — pick one (practice: Body)"
    - "interactivity as a PROP + the stretched-link (practice) vs split components (Carbon ClickableTile/SelectableTile)"
    - "the interactive pattern: stretched-link (one ::after link + z-indexed secondary actions — practice default) vs CardActionArea (<div role=button> wrapping the region, actions outside) vs whole-card-<a> (only when no inner interactives)"
    - "a shared Surface primitive (Card/Dialog/Popover build on it) vs Card owning its chrome"
    - "full-bleed: Card.Media sibling (MUI) vs a Bleed component (Chakra/Polaris)"
  trap:
    - "the NESTED-INTERACTIVE trap: a clickable card (a/button) containing a link/button = invalid HTML + 25s SR verbosity (Roselli) — use the stretched-link; block divs in a <button> violate phrasing-content (MUI's CardActionArea button->div fix)"
    - "the stretched-link breaking text selection + the focus ring landing on only the title (style the whole card from :focus-within)"
    - "burying secondary actions UNDER the stretched link (they need position:relative + z-index above to stay clickable)"
    - "the FULL-BLEED MEDIA breaking the padding (Card.Media sibling / Bleed / negative-margin + overflow:hidden)"
    - "card overuse ('card fatigue') / nested cards (destroys the elevation scale); card-ifying a dense data table (-> list/table row)"
    - "a generic 'read more' link name instead of the title; a card without a real heading; critical info living only in -webkit-line-clamp'd text"
  inherited: "Box's surface tokens / as-asChild Slot / spacing scale / zero-runtime / logical-property RTL; Stack's gap + no-external-margin discipline"
  role-in-family: "the first styled surface — where Box's neutrality ends + the Foundations cluster meets Layout; stands on Box (surface) + Stack (body), composes Avatar/Badge/Tag/Skeleton/Button/Text/Media, the cell of a Grid gallery"
  evolution:
    - "the monolithic card -> the slotted/compound card (Card.Header/Body/Footer/Media)"
    - "Material's three-variant elevation model (elevated/filled/outlined) settling"
    - "the interactive-card a11y settling: the stretched-link over the whole-card-button (Heydon Pickering; Roselli's verbosity data; MUI's button->div fix)"
    - "subgrid (~2024) replacing the ResizeObserver height-equalization JS"
    - "cards-as-collections (React Aria CardView — selectable/drag-and-drop data items; aria-selected/roving focus)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "the Polaris s-card web-component state + per-system slot naming"
    - "the Roselli 25-second verbosity figure + the stretched-link user-select/pointer-events restoration specifics — verify against current implementations"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-card/` (16 June 2026), the thirty-eighth brief and the **first styled surface** — where Box's deliberate neutrality ends and **the Foundations cluster meets Layout** (the fourth Layout brief). It stands on Box (the surface — the polymorphic `as`/`asChild` Slot, the token-mapped bg/border/radius, the padding from the spacing scale, the zero-runtime delivery, the logical-property RTL) and Stack (the body — header/media/body/footer with `gap`, the no-external-margin discipline), composes the Foundations cluster (Avatar/Badge/Tag/Skeleton/Button/Text/Media), and is the cell of a Grid gallery (auto-grid + subgrid equal-height) — the brief where the Foundations work pays off. The two passes converged with no genuine fork — the surface/elevation model (elevated/filled/outlined), the slot model (compound over monolithic + the full-bleed-media trap), the interactive-card nested-interactive problem + the stretched-link pattern (one real link + `::after`, secondary actions z-indexed above), the equal-height/subgrid case, and the padding/media-bleed trap. The external pass sharpened with decisive concrete detail: the **Adrian Roselli verbosity data** (a whole-card link forcing 25+ seconds of screen-reader speech before "link" is announced), the **MUI `CardActionArea` `<button>`→`<div role="button">` validation bug** (block divs violate phrasing-content), the **named `Bleed` component** (Chakra/Polaris) as a third full-bleed solution alongside MUI's CardMedia-as-sibling, the `-webkit-line-clamp` truncation limits + the don't-bury-critical-info rule, the subgrid + flex-`flex-grow` footer-pinned fallback (subgrid replacing the old `ResizeObserver` height-equalization JS), and React Aria's **CardView** cards-as-selectable-collections. Claude-pass contributions: the Foundations-meets-Layout convergence framing, the Box-surface-plus-Stack-body inheritance map, the Card-vs-Box-vs-Section-vs-Dialog boundary set, the don't-nest-cards / card-fatigue discipline, and the whole-card-clickable-vs-actions decision. The 2026 version numbers, the Polaris `s-card` state, and the Roselli figure are flagged unverified. Conformant to `components/_schema.md`. With Card, the Foundations and Layout clusters interlock — only Section remains to close the Layout category.*
