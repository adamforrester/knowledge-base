# Card — field-truth study (Claude pass)

## 1. Framing
A Card is the **first styled surface** — the component where Box's deliberate neutrality *ends* and visual chrome (background, border, radius, elevation) *begins*. It is the fourth Layout brief and the **convergence host where the Foundations cluster meets Layout**: a Card is the in-flow container that groups related content (a title, media, text, an avatar, badges, tags, actions) into one bounded, elevated surface. It is literally the answer to the rule Box stated — *"if you're adding chrome to a Box, you want a Card"* — so Card formalises the surface that Box/Stack/Grid deliberately lack.

It stands on the layout primitives and composes the Foundations work:
- **The surface is a Box** (the polymorphic `as`/`asChild` Slot, the token-mapped background/border/radius, the padding from the spacing scale, the zero-runtime delivery, the logical-property RTL — see box); **the body layout is a Stack** (header/media/body/footer stacked with `gap`, owning the no-external-margin discipline — see stack). Card adds the *delta*: the chrome, the slots, and the interactivity.
- **It composes the Foundations cluster** — Avatar (the author), Badge (a status), Tag (categories), Skeleton (the loading card), Button (actions), Heading/Text, Image/Media (see avatar, badge, tag, skeleton, button, link). This is the brief where the Foundations work pays off.
- **It is the cell of a Grid gallery** — cards tile in the auto-grid RAM pattern; equal-height cards align their internal rows via **subgrid** (the Grid brief's subgrid case — see grid).

Three things define it: **the surface / elevation model** (elevated / filled / outlined — what makes a Card a Card), **the slot model** (header / media / body / footer — the compositional anatomy), and **the interactive-card problem** (the whole-card-clickable nested-interactive trap, and the stretched-link pattern that resolves it — §6). What it *isn't*: a **Box** (the neutral substrate with no chrome — reach for Box when you *don't* want a surface; see box), a **Section** (a *semantic region* / landmark, not a visual surface — Section not yet briefed), or a **Dialog/Popover** (overlay surfaces that float above the page — a Card is *in-flow*, part of the document; see dialog, popover). Why systems disagree: the slot API (compound vs props), the variant/elevation model, and the interactive-card pattern.

## 2. Anatomy and parts
- **the surface** — a **Box** providing the visual container: background, border, **radius**, **elevation** (shadow), and **padding** (the internal inset from the spacing scale). The defining chrome Box lacks (see box).
- **the slots** — the compositional regions, top to bottom:
  - **header** — title + optional avatar/overline/actions (an avatar + a heading + a trailing menu button — composes Avatar, Heading, Button).
  - **media** — an image/video, often **full-bleed** (edge-to-edge, breaking the card's padding — §11).
  - **body / content** — the primary content (text, a Stack of detail).
  - **footer / actions** — the action row (Buttons, Links) and/or metadata (Tags, a timestamp).
- **the body Stack** — the slots are stacked vertically with a token `gap` (the card body *is* a Stack — see stack).
- **the optional interactive layer** — when the whole card is clickable, the primary link's stretched `::after` (or a `CardActionArea`) covering the surface (§6).
- **the composed Foundations contents** — what fills the slots: Avatar, Badge, Tag, Skeleton, Button, Text, Media. Card is the host, not the author, of these.

## 3. Properties / API
- **`variant`** — **elevated** (shadow, the default floating surface) / **filled** (a tonal background, no border/shadow) / **outlined** (a border, no shadow) — Material 3's three cards. The headline visual axis (§4).
- **the slot API (compound vs props):** the **compound-component** model (`Card.Header` / `Card.Media` / `Card.Body` / `Card.Footer` / `Card.Actions` — MUI `CardHeader`/`CardMedia`/`CardContent`/`CardActions`; Chakra `CardHeader`/`Body`/`Footer`; Ant `Card.Meta`) vs a **monolithic Card with props** (`title`/`media`/`footer`). The practice leans **compound** for flexibility (the bundled-vs-composed tension Text Field resolved, applied to a surface — see text-field); a monolithic prop API is the convenience layer for the common case.
- **`padding` / density** — the internal inset (from the spacing scale); density variants (comfortable/compact); **`padding={0}`** for the full-bleed-media case (§11).
- **`interactive` / `clickable` (+ `href` / `onClick`)** — whether the whole card is a single target (§6); drives the hover-elevation + focus ring.
- **`selected`** — for card *collections* (selectable card grids — Spectrum/React Aria).
- **`elevation`** — the shadow-depth token (when elevated); the resting vs hover level.
- **`as` / `asChild`** — inherited from Box: render the right element (`article`/`section`/`li`) for semantics (§6).
- **what it withholds** — Card doesn't author content (it hosts it), and it shouldn't expose arbitrary style props (that's Box); it exposes the *surface* tokens (variant/elevation/padding) and the slots.

## 4. States and variants
- **States:**
  - **default (non-interactive)** — a static surface; no interaction states.
  - **interactive** — hover (an **elevation lift** / background shift), focus-visible (a focus ring on the *whole card*), active (a press). Only when the card is clickable (§6).
  - **selected** — for card collections (a selected border/background + `aria-selected`).
  - **loading** — the card rendered as a **Skeleton** (the shape-matched placeholder — see skeleton).
- **Variants:**
  - **surface:** elevated / filled / outlined.
  - **interactivity:** static / whole-card-clickable / actions-inside.
  - **with-media** (top/full-bleed image) / **sectioned** (multiple divided regions — Polaris).
  - **density:** comfortable / compact.
  - **the rendered element:** `article` / `section` / `li` / `div` (via `as`).

## 5. Usage guidance
- **Use a Card for:** grouping related content into a **bounded, in-flow surface** — a product/article tile in a gallery, a summary panel, a dashboard widget, a settings group, a media preview. The signal: the content forms a *unit* that benefits from a visual boundary and (often) tiles alongside peers.
- **Card vs the alternatives:**
  - **vs Box** — Box is neutral (no chrome); reach for a Card when the group needs a *surface* (background/border/elevation). Adding chrome to a bare Box by hand is the smell Box warned about (see box).
  - **vs Section** — Section is a *semantic region* (a landmark + a heading-level contract); Card is a *visual surface*. A page region is a Section; a bounded content unit within it is a Card. (Section not yet briefed.)
  - **vs Dialog/Popover** — those are *overlay* surfaces (floating, top-layer, dismissible); a Card is *in-flow* (part of the document). Same visual vocabulary (elevation), different layer (see dialog, popover).
  - **vs a list/table row** — a Card is for richer, two-dimensional content with media and actions; a dense, scannable, comparable set of records is a **list or table row** (don't card-ify a data table — Table not yet briefed).
- **Decision frameworks:**
  - **The whole-card-clickable vs actions-inside call (the load-bearing one):** if the card has *one* destination and *no* other interactive elements → the whole card can be one link (or stretched-link). If it has *secondary* actions (a bookmark button, multiple links) → the stretched-link pattern (one primary link + the secondary actions z-indexed above it), never a card-wrapped-in-a-button-containing-buttons (§6).
  - **Don't overuse / don't nest cards** — a page that's all cards (or cards inside cards inside cards) loses the hierarchy cards are meant to create; the surface should be *meaningful*, not a default wrapper. Nested cards especially flatten the elevation language.
- **Equal-height in a gallery** — when cards tile, use the Grid auto-grid + **subgrid** to align titles/bodies/footers across the row, and pin the footer to the bottom (§11) so action rows line up regardless of body length.

## 6. Accessibility
Card has **no implicit role by default** — it's a generic container (inherits Box's neutrality; the element it renders via `as` carries any semantics — `article` for a self-contained piece, `li` within a list, `section`/`region` only with a label). The crux is **the interactive card**.

- **The nested-interactive trap.** A clickable card implemented as `<a>`/`<button>` **cannot contain** another link or button — nested interactive elements are **invalid HTML** and break keyboard/AT behavior (the same interactive-in-interactive trap Tag's grid pattern and Box's polymorphism named). So "make the whole card a button" only works when there are **no** other interactive elements inside.
- **The stretched-link pattern (the settled accessible answer).** Keep the card a **non-interactive container**; put **one primary link** inside it (usually wrapping the title) and give that link a **`::after` pseudo-element stretched over the whole card** (`position: absolute; inset: 0`), with the card `position: relative`. Result: the entire card surface is clickable, but there's exactly **one real link** in the accessibility tree (named by the title — a meaningful accessible name, not "read more"). **Secondary actions** (a bookmark button, a tag link) sit **above the stretched link in z-index** (`position: relative; z-index: 1`) so they remain independently clickable. (Heydon Pickering, *Inclusive Components* — "Cards".)
  - **The costs to manage:** the stretched link **breaks text selection** over the card (the `::after` intercepts pointer events — a known trade-off; some restore it with `user-select` + pointer-events juggling); and the focus ring must render on the **whole card** (style the card from the link's `:focus-within`), not just the title text, so the target is visible.
- **`CardActionArea` (the MUI alternative)** — a `<button>`/`<a>` wrapping *only* the clickable region (media + title), with actions *outside* it in the footer — avoids nesting by *separating* the clickable area from the actions, rather than z-indexing. Valid, but constrains the layout (the actions can't sit visually within the clickable region).
- **Whole-card `<a>`** — valid and simplest *only* when the card is purely a link with no inner interactives (a pure navigation tile).
- **Heading structure** — the card's title should be a real heading (`<h3>` etc.) at the right level for the page outline; a gallery of cards is often an `<ul>`/`<li>` so the count and relationship reach AT (the list-semantics rule from Stack — see stack).
- **WCAG SCs:** **2.1.1** (keyboard — the card target operable), **2.4.7** (focus visible — the whole-card ring), **4.1.2** (name/role/value — the link's accessible name from the title; `aria-selected` for collections), **1.3.1** (info & relationships — `article`/`li`/heading), **2.5.5 / 2.5.8** (target size — the stretched link is large, which *helps*, but secondary actions inside must still meet the minimum). The interactive-card pattern is the whole a11y story; a static card is as light as Box.

## 7. Content guidelines
- **The card title** — short, scannable, and the **accessible name** of the clickable card (the stretched-link target). Make it a real heading; make it *specific* ("2024 Annual Report", not "Document") since it's what a screen-reader user hears as the link.
- **Scannable content** — a card is glanced at in a gallery; lead with the title/media, keep body text to a few lines, truncate overflow (with the full text available — the Tag/Avatar truncation discipline).
- **Actions** — a primary action (the stretched link or a primary Button) + optional secondary actions; don't crowd the footer with equal-weight buttons. If the whole card is clickable, the footer actions are *secondary* (and must sit above the stretched link — §6).
- **Don't overload the card** — one unit of meaning per card; a card trying to show a title, media, five tags, three buttons, an avatar, and a chart is two components. Match the slot content to the card's job.

## 8. Motion and transition
- **The hover-elevation lift** — an interactive card raises its elevation (a deeper shadow) and/or shifts its background on hover/focus, signalling clickability; brief and token-driven. The headline Card motion.
- **The loading→content swap** — a Skeleton card swaps to the real content on load (the shape-matched, no-CLS swap — see skeleton).
- **Gallery enter/reflow** — cards entering or reordering in a Grid gallery reflow via **FLIP** (the technique Stack/Grid/Tag share — see stack, grid), applied by the consumer/an animation primitive, not by Card.
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops the hover-lift to an instant elevation/background change (the cue is the elevation, not the transition) and disables gallery reflow animation. Card itself ships only the hover transition.

## 9. Internationalization
- **RTL is inherited from Box/Stack** — the surface padding (logical properties), the header/media layout, and the footer actions all mirror under `dir="rtl"` with no JS: a leading avatar moves to the right, the actions flip to the leading edge (see box, stack). The card needs no RTL logic of its own beyond using the inherited logical-property substrate.
- **Content expansion + equal-height** — translated titles/body run longer; the equal-height-via-subgrid alignment must tolerate variable content length (the footer-pinned pattern + subgrid handle this — §11), and truncation must not clip the localized text mid-word.
- The card's media and chrome are direction-agnostic; only the *content layout* mirrors.

## 10. Naming
- **The field set:** **`Card`** is the near-universal name (Material, MUI, Chakra, Polaris, Ant, Spectrum, Atlassian, Base Web); **`Tile`** is IBM Carbon's term (`ClickableTile`/`SelectableTile`/`ExpandableTile` — note Carbon splits *by interactivity*, a useful precedent); **`Panel`**/**`Well`** are older/Bootstrap-era aliases; **`Surface`** is the *underlying concept* (Material's Surface — the elevation primitive a Card is a specialization of).
- **The practice's default — `Card`** (the dominant name), with the **compound slots** `Card.Header` / `Card.Media` / `Card.Body` / `Card.Footer` (+ `Card.Actions`). Use **`Body`** (or `Content`) consistently; MUI's `CardContent` vs Chakra's `CardBody` is the one naming wobble — pick one. Don't split into `ClickableCard`/`StaticCard` components (Carbon's Tile split is defensible but the practice models interactivity as a prop + the stretched-link pattern, keeping one `Card`).
- **`Surface` as the shared primitive** — if the system has multiple elevated surfaces (Card, Dialog, Popover, Menu), an internal `Surface` primitive (the elevation/radius/background tokens) that Card/Dialog/Popover all build on is a clean factoring — the elevation equivalent of Box. (Optional; name it if the surfaces proliferate.)
- **Aliases to map:** Tile, Panel, Well, Surface, ClickableTile, SelectableTile.

## 11. Implementation notes
- **The surface on Box** — Card is a Box with token-mapped `background`/`border`/`border-radius`/`box-shadow`(elevation)/`padding`; the variant switches which tokens apply (elevated → shadow, no border; outlined → border, no shadow; filled → tonal bg). Inherit Box's `as`/`asChild` Slot, the spacing scale, the zero-runtime delivery, and the logical-property RTL (see box) — Card adds only the chrome.
- **The slot / compound API** — `Card.Header`/`Media`/`Body`/`Footer` as compound children sharing context (the React `Card` provides padding/variant context the slots consume); the body is a **Stack** with a token `gap` (see stack). Each slot manages its own padding relationship to the card's inset.
- **The full-bleed media (the recurring trap)** — a cover image must break the card's padding to go edge-to-edge: either the **media slot lives outside the padded content wrapper** (the card pads the body but not the media), or the media uses a **negative inline margin** equal to the padding (`margin-inline: calc(-1 * var(--card-padding))`) to bleed to the edges. The first (structural) is cleaner than the second (negative-margin) — but both are common. The radius must clip the media (`overflow: hidden` on the card or the media corners rounded to match).
- **The stretched-link** — `position: relative` on the card; the primary link's `::after { position: absolute; inset: 0 }` covers the surface; secondary interactive elements get `position: relative; z-index: 1` to sit above; style the card's `:focus-within` (or `:has(:focus-visible)`) to show the whole-card focus ring. Restore `user-select` if text selection matters (the pointer-events trade-off — §6).
- **Equal-height via subgrid + the footer-pinned pattern** — in a Grid gallery, the card spans the row's tracks and uses `grid-template-rows: subgrid` so the title/body/footer rows align across cards (see grid); or, simpler, the card is a flex column with the footer pushed down (`margin-block-start: auto` on the footer, or the body `flex: 1`) so footers pin to the bottom regardless of body length.
- **The interactive elevation/focus** — the hover-lift is a `box-shadow`/`transform` transition (GPU-composited); the focus ring is the whole-card outline (§6/§8).
- **Headless vs opinionated** — ship the surface tokens + the slot structure + the interactive/stretched-link wiring as the opinionated value; the elevation scale and the radius are theme. The stretched-link and the full-bleed media are the bits worth owning so every consumer doesn't re-solve them.

## 12. Related and alternative components
- **Stands on:** **Box** (the surface — bg/border/radius/elevation/padding + the polymorphic `as`/`asChild` + the logical-property RTL — see box) and **Stack** (the body layout — header/media/body/footer with `gap` — see stack).
- **Composes (the Foundations cluster — the convergence):** **Avatar** (the author/owner — see avatar), **Badge** (a status overlay — see badge), **Tag** (categories/filters — see tag), **Skeleton** (the loading card — see skeleton), **Button** (footer actions — see button), **Heading/Text** (the title/body), and **Image/Media** (the cover). The brief where the Foundations work pays off.
- **The cell of:** a **Grid** gallery (the auto-grid RAM pattern; equal-height via subgrid — see grid).
- **Relates to (interactivity):** **Link** (the stretched-link is a block-link — see link) and **Button** (the link-vs-button-on-a-card decision — see button).
- **Boundary with:** **Dialog/Popover** (overlay surfaces — same elevation vocabulary, different layer; Card is in-flow — see dialog, popover), **Section** (a semantic region, not a visual surface — not yet briefed), and a **list/table row** (dense comparable records — Table not yet briefed).
- **Alias:** IBM Carbon's **Tile** (the same component, split by interactivity).

(The first styled surface — where Box's neutrality ends and the Foundations cluster meets Layout. It stands on Box (the surface) + Stack (the body), composes Avatar/Badge/Tag/Skeleton/Button/Text/Media, and is the cell of a Grid gallery. See box/stack for the substrate, avatar/badge/tag/skeleton/button for the composed contents, grid for the gallery + subgrid equal-height, link for the stretched-link, dialog/popover for the overlay-surface boundary, section when briefed for the semantic-region boundary. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The monolithic card → the slotted/compound card.** Early cards were monolithic (`<Card title= image= >`); the field moved to compound slots (`Card.Header`/`Body`/`Footer`/`Media`) for compositional flexibility — the same bundled-vs-composed maturation Text Field shows.
2. **Material's three-variant elevation model settling.** Elevated / filled / outlined (Material 3) became the shared variant vocabulary, formalising the surface/elevation token system over ad-hoc shadows.
3. **The interactive-card a11y settling — the stretched-link over the whole-card-button.** The field recognised that wrapping a card (with inner actions) in a button/link is invalid nested-interactive HTML, and converged on the **stretched-link pattern** (one real link + `::after`, secondary actions z-indexed above) as the accessible answer — Heydon Pickering's *Inclusive Components* "Cards" is the canonical reference.
4. **Subgrid enabling equal-height card content.** `subgrid` (~2024 — see grid) let cards align their internal title/body/footer rows across a gallery row, solving the long-standing equal-height-card-content problem that flexbox alone couldn't.
5. **Cards-as-collections.** Selectable card grids (React Aria/Spectrum's card collections) brought `aria-selected`/roving-focus selection semantics to galleries of cards — a card as a selectable option, not just a static surface.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- Google Material 3 — `Card` (elevated/filled/outlined; the elevation system; clickable cards).
- MUI — `Card` + `CardHeader`/`CardMedia`/`CardContent`/`CardActions`/`CardActionArea` (the slot model + the clickable-region button).
- Chakra UI — `Card` + `CardHeader`/`CardBody`/`CardFooter` (variants elevated/outline/filled).
- Shopify Polaris — `Card` (the workhorse surface; sectioned cards; the recent `s-card` web component).
- GitHub Primer — the Box-based card; link-preview cards.
- Adobe Spectrum / React Aria — `Card` (selectable cards / card collections).
- IBM Carbon — `Tile` (`ClickableTile`/`SelectableTile`/`ExpandableTile` — split by interactivity).
- Ant Design — `Card` (`Card.Meta`, cover, actions, tabs).
- Atlassian — `Card` (link-preview cards).
- Base Web (Uber) — `Card`.
- Heydon Pickering — *Inclusive Components* "Cards" (the stretched-link / pseudo-content pattern); the nested-interactive (interactive-in-interactive) HTML-validity rule; Sara Soueidan / WAI on block links.
- WCAG 2.2 — 2.1.1, 2.4.7, 4.1.2, 1.3.1, 2.5.5/2.5.8.

## 15. Agent-consumable schema
```yaml
identity:
  id: card
  name: Card
  aliases: [Tile, Panel, Well, Surface, ClickableTile, SelectableTile, ExpandableTile]
  category: layout
  status: stable
description: >
  The first styled SURFACE — where Box's deliberate neutrality ends and visual chrome
  (background, border, radius, ELEVATION) begins; the in-flow container that groups
  related content into a bounded, elevated unit, and the convergence host WHERE THE
  FOUNDATIONS CLUSTER MEETS LAYOUT. Literally the answer to Box's 'if you're adding
  chrome to a Box, you want a Card.' NOT a Box (the neutral substrate, no chrome —
  reach for Box when you don't want a surface), NOT a Section (a semantic region/
  landmark, not a visual surface), NOT a Dialog/Popover (overlay surfaces — a Card is
  IN-FLOW). Stands on Box (the surface) + Stack (the body); composes Avatar/Badge/Tag/
  Skeleton/Button/Text/Media; the cell of a Grid gallery (auto-grid + subgrid equal-height).
anatomy:
  parts:
    - "the surface: a Box providing bg/border/RADIUS/ELEVATION(shadow)/PADDING (the internal inset from the spacing scale) — the chrome Box lacks"
    - "the slots (top->bottom): header (title + optional avatar/overline/actions) / media (image/video, often FULL-BLEED) / body-content / footer-actions (Buttons + metadata Tags)"
    - "the body Stack: the slots stacked vertically with a token gap (the card body IS a Stack)"
    - "the optional interactive layer: the primary link's stretched ::after (or a CardActionArea) covering the surface"
    - "the composed Foundations contents: Avatar/Badge/Tag/Skeleton/Button/Text/Media — Card is the HOST not the author"
api:
  inherits:
    - box        # the surface — bg/border/radius/elevation/padding + the as/asChild Slot + the logical-property RTL + zero-runtime delivery
    - stack      # the body layout — header/media/body/footer with gap (the no-external-margin discipline)
  composes: [avatar, badge, tag, skeleton, button, link, "heading/text", "image/media"]   # the Foundations cluster — the convergence
  props:
    - {name: variant, type: "'elevated' | 'filled' | 'outlined'", default: elevated, required: false, description: "Material 3's three cards: elevated (shadow) / filled (tonal bg) / outlined (border)"}
    - {name: "slots (Card.Header/Media/Body/Footer/Actions)", type: "compound components", default: ~, required: false, description: "the COMPOUND API (MUI CardHeader/Media/Content/Actions; Chakra Header/Body/Footer; Ant Card.Meta) — practice leans compound over a monolithic title/media/footer prop API (the bundled-vs-composed tension, cf. text-field)"}
    - {name: padding/density, type: "token | 'comfortable'|'compact'", default: comfortable, required: false, description: "the internal inset (spacing scale); padding=0 for full-bleed media"}
    - {name: "interactive/clickable (+ href/onClick)", type: "boolean | link", default: false, required: false, description: "whole-card target -> the hover-elevation + focus ring + the stretched-link pattern (a11y)"}
    - {name: selected, type: boolean, default: false, required: false, description: "for card COLLECTIONS (selectable card grids) — aria-selected"}
    - {name: elevation, type: "token", default: ~, required: false, description: "the shadow-depth token (resting vs hover)"}
    - {name: as/asChild, type: "ElementType/boolean", default: div, required: false, description: "inherited from Box — render article/section/li for semantics"}
  withholds: "doesn't author content (hosts it); doesn't expose arbitrary style props (that's Box) — exposes the SURFACE tokens (variant/elevation/padding) + the slots"
states:
  runtime: [default, hover, focus-visible, active, selected, loading]   # interaction states ONLY when interactive; hover/focus = elevation lift + whole-card focus ring
  default-non-interactive: "a static surface has NO interaction states (as light as Box)"
  loading: "the card rendered as a Skeleton (shape-matched placeholder)"
variants:
  surface: [elevated, filled, outlined]
  interactivity: [static, whole-card-clickable, actions-inside]
  media: [no-media, top-media, full-bleed-media]
  structure: [plain, sectioned]            # sectioned = multiple divided regions (Polaris)
  density: [comfortable, compact]
  rendered-element: [article, section, li, div]
accessibility:
  wcag-criteria: ["2.1.1", "2.4.7", "4.1.2", "1.3.1", "2.5.5", "2.5.8"]
  implicit-role: "NONE by default — a generic container (inherits Box's neutrality); the element it renders via as carries semantics (article=self-contained piece, li=within a list, section/region only WITH a label)"
  nested-interactive-trap: "a clickable card as <a>/<button> CANNOT contain another link/button (interactive-in-interactive = INVALID HTML, breaks keyboard/AT — the same trap Tag's grid + Box's polymorphism named). Whole-card-button works ONLY with no inner interactives"
  stretched-link-pattern: "THE settled accessible answer (Heydon Pickering, Inclusive Components 'Cards'): keep the card a NON-interactive container; ONE primary link inside (wrapping the title) gets ::after {position:absolute; inset:0} over the card (card position:relative) -> whole surface clickable, ONE real link in the a11y tree (named by the title, not 'read more'); SECONDARY actions get position:relative + z-index:1 to stay independently clickable"
  stretched-link-costs: "breaks text-selection over the card (the ::after intercepts pointer events — restore via user-select/pointer-events juggling); the focus ring must render on the WHOLE card (style from :focus-within), not just the title"
  alternatives: "CardActionArea (MUI — a button/<a> wrapping ONLY the clickable region, actions OUTSIDE it; valid but constrains layout) vs whole-card-<a> (valid ONLY when no inner interactives — a pure nav tile)"
  heading-structure: "the card title is a real heading (h3 etc.) at the right outline level; a gallery is often ul/li (count + relationship reach AT — the list-semantics rule from Stack)"
  target-size: "the stretched link is large (helps 2.5.5/2.5.8); secondary actions inside must still meet the minimum"
content:
  card-title: "short, scannable, SPECIFIC ('2024 Annual Report' not 'Document') — it's the accessible name of the clickable card / the stretched-link target; a real heading"
  scannable: "glanced at in a gallery — lead with title/media, body to a few lines, truncate overflow (full text available)"
  actions: "a primary action + optional secondary; don't crowd the footer with equal-weight buttons; if whole-card-clickable, footer actions are secondary (z-indexed above the stretched link)"
  dont-overload: "one unit of meaning per card; title + media + 5 tags + 3 buttons + avatar + chart = two components"
motion:
  hover-elevation-lift: "an interactive card raises elevation (deeper shadow) / shifts bg on hover/focus, signalling clickability; brief, token-driven — the headline Card motion"
  loading-swap: "a Skeleton card -> the real content on load (shape-matched, no CLS)"
  gallery-reflow: "cards entering/reordering in a Grid gallery reflow via FLIP (shared with Stack/Grid/Tag), applied by the consumer/an animation primitive"
  reduce-motion: "drop the hover-lift to an instant elevation/bg change (the cue is the elevation, not the transition) + disable gallery reflow; Card ships only the hover transition"
i18n:
  rtl-inherited: "the surface padding (logical properties), header/media layout, and footer actions all mirror under dir=rtl with no JS (a leading avatar -> right, actions -> the leading edge); inherited from Box/Stack, no card-specific RTL logic"
  content-expansion: "translated titles/body run longer — equal-height-via-subgrid must tolerate variable length (footer-pinned + subgrid handle it); truncation must not clip localized text mid-word"
  chrome-direction-agnostic: "media + chrome are direction-agnostic; only the content LAYOUT mirrors"
implementation:
  - "the surface on Box: token-mapped background/border/border-radius/box-shadow(elevation)/padding; the variant switches which tokens apply (elevated->shadow no-border; outlined->border no-shadow; filled->tonal bg). Inherit Box's as/asChild Slot + scale + zero-runtime + logical RTL; Card adds only the chrome"
  - "the slot/compound API: Card.Header/Media/Body/Footer as compound children sharing context (the Card provides padding/variant context the slots consume); the body is a Stack with a token gap"
  - "the FULL-BLEED MEDIA trap: a cover image must break the card's padding edge-to-edge — either the media slot lives OUTSIDE the padded content wrapper (structural, cleaner) or uses a negative inline margin = the padding (margin-inline:calc(-1*var(--card-padding))); the radius must clip the media (overflow:hidden / matched corners)"
  - "the stretched-link: card position:relative; the primary link ::after {position:absolute; inset:0}; secondary interactives position:relative + z-index:1; style :focus-within for the whole-card ring; restore user-select if text selection matters (the pointer-events trade-off)"
  - "equal-height: in a Grid gallery the card spans the row + grid-template-rows:subgrid to align title/body/footer rows across cards (see grid); OR simpler — a flex column with the footer pinned (margin-block-start:auto on the footer / body flex:1)"
  - "the interactive elevation/focus: hover-lift = a GPU-composited box-shadow/transform transition; the focus ring = the whole-card outline"
  - "headless vs opinionated: ship the surface tokens + the slot structure + the interactive/stretched-link wiring (the value); the elevation scale + radius are theme. Own the stretched-link + full-bleed media so consumers don't re-solve them"
composition:
  stands-on: [box, stack]                  # the surface + the body
  composes: [avatar, badge, tag, skeleton, button, link, "heading/text", "image/media"]   # the Foundations cluster
  cell-of: [grid]                          # the auto-grid gallery + subgrid equal-height
  relates-to: [link, button]               # the stretched-link (a block-link) + the link-vs-button-on-a-card decision
  boundary: [dialog, popover, section, table]   # overlay surfaces (in-flow vs floating) / semantic region / dense comparable rows
  alias-of: ["Carbon Tile"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "the slot API: COMPOUND (Card.Header/Body/Footer/Media — practice default) vs a monolithic title/media/footer prop API (the bundled-vs-composed tension, cf. text-field)"
    - "Body vs Content slot naming (Chakra CardBody vs MUI CardContent) — pick one"
    - "interactivity as a PROP + the stretched-link (practice) vs split components (Carbon ClickableTile/SelectableTile)"
    - "the interactive pattern: stretched-link (one ::after link + z-indexed secondary actions — practice default) vs CardActionArea (button wrapping the clickable region, actions outside) vs whole-card-<a> (only when no inner interactives)"
    - "a shared Surface primitive (Card/Dialog/Popover all build on it) vs Card owning its chrome"
  trap:
    - "the NESTED-INTERACTIVE trap: a clickable card (a/button) containing a link/button = invalid HTML — use the stretched-link"
    - "the stretched-link breaking text selection + the focus ring landing on only the title (style the whole card from :focus-within)"
    - "burying secondary actions UNDER the stretched link (they need z-index above to stay clickable)"
    - "the FULL-BLEED MEDIA breaking the padding (media-outside-padding or negative-margin + overflow:hidden)"
    - "card overuse / nested cards (flattens the elevation hierarchy cards create); card-ifying a dense data table (-> list/table row)"
    - "a generic 'read more' link name instead of the title; a card without a real heading"
  inherited: "Box's surface tokens / as-asChild Slot / spacing scale / zero-runtime / logical-property RTL; Stack's gap + no-external-margin discipline"
  role-in-family: "the first styled surface — where Box's neutrality ends + the Foundations cluster meets Layout; stands on Box (surface) + Stack (body), composes Avatar/Badge/Tag/Skeleton/Button/Text/Media, the cell of a Grid gallery"
  evolution:
    - "the monolithic card -> the slotted/compound card (Card.Header/Body/Footer/Media)"
    - "Material's three-variant elevation model (elevated/filled/outlined) settling"
    - "the interactive-card a11y settling: the stretched-link over the whole-card-button (Heydon Pickering)"
    - "subgrid (~2024) enabling equal-height card content alignment"
    - "cards-as-collections (selectable card grids — aria-selected/roving focus)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "the Polaris s-card web-component state + per-system slot naming"
    - "the stretched-link user-select/pointer-events restoration specifics — verify against current implementations"
```
