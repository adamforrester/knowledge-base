---
okf_version: "0.1"
type: component-brief
title: Avatar
description: The person/entity identity surface and presence-dot host — a field-truth study of the fallback chain (image → initials → icon) and its SSR/cached-image flash trap (the native-img-onError-plus-complete-check vs the JS-virtual-Image machine), the contextual accessible-name contract (informative bare avatar = the name; decorative when adjacent to a visible name; the fallback preserves the name — the inverse of Icon's decorative-by-default), the AvatarGroup face-pile (the overlap + "+N more" overflow + the group-name-and-count via role=group + aria-hidden children), initials generation + the deterministic color-from-name (the bitwise hash mod an accessibility-vetted palette + the name-order/CJK/RTL problem + color-not-sole-carrier + contrast), shape-as-entity-semantics (circle=person / square=org / hexagon=AI) + sizing, image handling, and the presence-dot overflow:hidden clipping trap resolved from the host side — with the practice's defaults.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [Persona, UserAvatar, Gravatar, ProfilePicture, AvatarStack, Avatar.Group, AvatarToken, Face pile, s-avatar]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Avatar

> An Avatar is the **visual representation of a person or entity** (a user, an org/team, a bot) — a masked, fallback-backed identity surface, not a generic image and not a symbolic icon. Three things define it and are where systems diverge. **The fallback chain** (the headline): image → initials → generic icon, gracefully degrading when identity data is missing or the image fails — a state machine whose hard parts are *failure and timing* (the `onError` swap, the loading **Skeleton**, and the **SSR/cached-image flash**). **The accessible-name contract** (the crux): an avatar that is the *only* identity carries the person's name (`alt="Jane Doe"`); an avatar *adjacent to a visible name* (a list row, a comment header) is redundant and must be **decorative** (`alt=""`/`aria-hidden`) so the name isn't announced twice — the **inverse of Icon's decorative-by-default**, because avatars are usually informative; and every fallback must **preserve the name** (initials/icon still expose "Jane Doe", never "JD"). **The group / face-pile**: an overlapping stack with a **"+N more"** overflow that announces the *count*, not N separate images — parallel to Tag's "+N more" and Badge's count cap. It stands on **Icon** (the generic placeholder fallback — see icon) and **Skeleton** (the circular loading placeholder — see skeleton), is the **host for Badge's PresenceBadge** (the online/away/busy dot — see badge; the host resolves the `overflow: hidden` clipping trap), and is **hosted by** Tag (Primer's `AvatarToken`), the multi-select Combobox tokens, list items, comments, and nav (see tag, combobox).

---

## 1. Framing
An Avatar is bound to **identity representation, stateful gracefulness, and a context-dependent accessibility contract** — its complexity lives in its failure modes and its composition, not its happy-path render. It is a *host and a substrate* at once: it anchors a presence Badge and nests inside Tags, Combobox selections, and list rows.

What it *isn't*: an **Icon** (a universal symbol/affordance for an action or concept — a generic person silhouette for a "Profile" nav link is an Icon; the *logged-in user's* face is an Avatar — see icon) or a generic **Image** (arbitrary content media — a product photo, an article thumbnail; an Avatar is media acting as an *identity anchor*, with a fixed aspect, a mask, and a fallback chain). Why systems disagree: the fallback **state management** (a JS-driven virtual-`Image()` machine vs a native `<img onError>` — and the SSR/cache flash each causes or fixes, §11), the **initials + color-from-name** algorithm (and its CJK/RTL breakdown, §9), and the **shape-as-entity-type** convention (§4).

## 2. Anatomy and parts
A resilient Avatar is a composite DOM structure separating positioning from masking from content — the separation is the load-bearing structural decision:
- **host wrapper** (`div`/`span`) — the bounding box, size, and the **relative positioning context**. **Must NOT be `overflow: hidden`** — the clip belongs on the inner mask, so an absolutely-positioned PresenceBadge can overhang without being cropped (§11).
- **masking layer** (`div`) — applies the shape (`border-radius` / `clip-path`) + `overflow: hidden` **on the inner media only**, preventing image/background bleed.
- **media node** (`img`) — the primary payload; `object-fit: cover` (never distort the face) + `srcset`/DPR.
- **initials fallback** (`span`) — a text node centered in the mask, on the deterministic name-hashed background (§ initials/color); the second fallback link.
- **icon placeholder** (`svg`) — a generic person/org/bot glyph (inherits Icon — see icon); the final link (no image *and* no name).
- **loading skeleton** (`div`) — a shape-matched Skeleton during network transit, reserving layout (no CLS — see skeleton).
- **presence anchor** (`div`) — the absolute slot (bottom-trailing) for the status Badge, on the *non-clipping* wrapper (§11; see badge).
- **group ring** (a stroke / pseudo-element) — in a face-pile, a canvas-color border separating overlapping instances (the same cutout idea as Badge's count pill — see badge).

## 3. Properties / API
The field has a converged surface; systems diverge on **data injection** (a single `name` prop fanning out, vs a compositional `Avatar.Image`/`Avatar.Fallback`):
- **`src` / `srcSet`** — the image source(s) (DPR/Retina).
- **`name`** — the identity string; drives **the initials, the accessible name, AND the color hash** simultaneously (Chakra/Fluent/Atlassian). The single most load-bearing prop.
- **`alt` / `decorative`** — the accessible-name control; defaults to `name`; a decorative/`aria-hidden` mode for the redundant-adjacent case (§6).
- **`icon`** — the custom fallback glyph (overrides the default person/org/bot icon).
- **`shape` / `variant`** — circle / rounded / square / **hexagon** (entity-type geometry — §4).
- **`size`** — xs / sm / md / lg / xl, token-mapped; initials and icon scale with it (§ sizing).
- **`delayMs`** — milliseconds to delay rendering the *fallback*, anticipating a fast network so a quick image doesn't flash initials first (Radix/Shadcn).
- **`getInitials`** — an override for the name→initials parsing (Chakra/Fluent); the i18n escape hatch (§9).
- **`color` / `idForColor`** — explicit control over the deterministic color hash, to disambiguate two users with identical names (Fluent).
- **the presence / status slot** — a `presence`/`status` prop or a composed `<PresenceBadge>`/`<AvatarBadge>` child — Avatar is the host (see badge).
- **the group:** `AvatarGroup` / `AvatarStack` with **`max` / `total` / `surplus`** (MUI `max`/`total`, Ant `maxCount`/`maxPopover`) — caps visible avatars, renders the "+N" overflow, owns the overlap/stacking/group-name.
- **the compositional alternative:** primitive-focused libraries (React Aria, Radix) split `<Avatar.Image>` / `<Avatar.Fallback>`, pushing the data-flow orchestration to the consumer rather than fanning out from `name`.

## 4. States and variants
- **States (the fallback state machine, negotiating network unreliability — not interaction states):**
  - **idle / loading** — `src` set, not yet painted → a **Skeleton** (or `delayMs`-debounced fallback to avoid a flash on fast networks).
  - **loaded (image)** — the `<img>` resolved 200; masked + `object-fit: cover`.
  - **error (initials)** — `src` missing / 404 / network fail, name present → initials over the hashed background.
  - **error (icon)** — no `src` *and* no parseable name → the generic icon.
  - **interactive** — only if the avatar is a *trigger* (a clickable account avatar → Menu), then it inherits the Button/Menu focus/hover contract (see button, menu); a bare display avatar has none.
- **Variants:**
  - **content:** image / initials / icon.
  - **shape = entity-type semantics:** **circle = person** (visual processing aligns circles with faces), **rounded-square / square = organization / team / project / app** (Primer/Atlassian enforce this for repos/projects), **hexagon = AI agent / bot** (Atlassian Rovo — an emerging convention distinguishing generative entities).
  - **size:** xs (20px, inline/Tags) / sm (24px, table rows) / md (32px, app headers) / lg (40px, profile cards) / xl+ (64px+, profile pages).
  - **with-presence:** the status-dot overlay (online/away/busy/offline).
  - **group / stacked:** the face-pile + "+N" overflow.

## 5. Usage guidance
- **Avatar vs Icon:** an Avatar always represents a *specific, unique identity* (a named user/org/bot); an **Icon** is a universal action/concept (see icon). A generic silhouette for a "User Profile" nav link is an Icon; the *current user's* face is an Avatar. Never use an Avatar for a UI metaphor.
- **Avatar vs Image:** generic **Image** handles content media (product photos, thumbnails); Avatar is media acting as an *identity anchor*.
- **Standalone vs paired:** a standalone avatar (an app header) leans on its image/initials for recognition; in dense displays (tables, lists) avatars should **almost always be paired with a visible name** — it cuts cognitive load when users share initials or fallback colors (and it flips the avatar to decorative — §6).
- **AvatarGroup vs a list:** use the face-pile for a *compact, glanceable* count of collaborators/participants where horizontal space is constrained; use a real **list** when names/roles matter or each user needs interaction.
- **Decision frameworks:**
  - **Initials vs icon fallback:** name known → **initials** (more identifying, more personal); fall back to the generic **icon** only when there's no name either (anonymous/unknown). Don't show a generic icon when initials are available.
  - **Decorative-when-adjacent (the load-bearing usage rule):** avatar next to a visible name → decorative; avatar as the *only* identity → it carries the name (§6).
  - **Presence dot when:** only when real-time availability is meaningful (chat, collaboration); don't decorate every avatar with a status it doesn't have.

## 6. Accessibility
**The accessible-name contract is the crux, and it's contextual** — the inverse of Icon's decorative-by-default, because avatars usually *carry* identity. An avatar is in one of two modes:

- **Informative (standalone).** The avatar is the sole indicator of identity → it needs an explicit accessible name: `<img alt="Jane Doe">`, or `aria-label="Jane Doe"` on the host wrapper for a background-image/SVG avatar. A bare avatar with an empty `alt` is an unlabeled image — a 1.1.1 failure.
- **Decorative (redundant).** The avatar sits beside a visible name (`[Avatar] Jane Doe` in a row/header) → an `alt` here makes the screen reader announce "Jane Doe, Jane Doe". So expose **`alt=""`** and ideally **`aria-hidden="true"`** on the wrapper, removing it from the accessibility tree. The most-missed Avatar a11y decision.
- **The fallback preserves the name.** Initials and the icon are *visual* shorthands, never the *accessible* name: an initials avatar still exposes "Jane Doe" (not "JD"); the icon fallback still exposes the name when informative, or is `aria-hidden` when decorative. (Common bug: the `onError` swap drops the `alt`.)
- **The AvatarGroup is a single semantic unit.** Exposing five overlapping images reads as a tedious five-name sequence. The default: `role="group"` + a descriptive `aria-label` on the wrapper ("5 collaborators" or "Jane Doe, John Smith, and 3 others"), with **all individual child avatars `aria-hidden="true"`** — a concise announcement matching the visual synthesis. The hidden avatars surface via the on-demand list, not the stack.
- **The presence dot has a text equivalent** (inherits Badge's contract — see badge): the status folds into the name ("Jane Doe, online"), the visual dot is `aria-hidden`, and color is never the sole carrier (online-green/away-amber/busy-red each need a text equivalent — 1.4.1).
- **Color-from-name is a decorative differentiator, not meaning.** It aids quick scanning; the *initials* (and adjacent text) carry the semantic differentiation — so it must never be the sole means of distinguishing people (two people can hash to the same color — 1.4.1), and the **initials must clear contrast against every palette entry** (≥4.5:1 normal text / 3:1 large — 1.4.3). Curate the algorithmic palette to remove swatches that fail against the initials' text color.
- **WCAG SCs:** **1.1.1** (the informative name / the decorative empty alt), **1.4.1** (color not sole carrier — presence + color-from-name), **1.4.3** (initials contrast on the generated background), **4.1.2** (the group, the presence). If the avatar is a trigger, it also takes the Button/Menu name/role contract (see button, menu).

## 7. Content guidelines
- **The name source** — the person's *real* display name (drives initials + accessible name); not a username/handle where a real name exists.
- **Initials generation rules:**
  - **Western (space-delimited):** first char of the first word + first char of the last word ("Jane Anne Doe" → "JD").
  - **Mononyms / organizations:** a single char ("Etsy" → "E", "Prince" → "P").
  - **Email fallback:** strip the domain, take initials from the local part (`jane.doe@…` → "JD", `admin@…` → "A").
  - **Capitalization:** normalize to uppercase regardless of input casing.
- **The alt-text pattern** — informative: `alt="[Name]"`; decorative: `alt=""`. Don't write "Avatar of Jane Doe" / "Jane Doe's profile picture" (verbose); the name alone is the contract.
- **The group "+N" label** — the surplus counter shows a numeric value with a plus ("+5"), *never* "+5 more" inside the circle (overflows/illegible at token sizes); the explanatory text lives in the `aria-label`/tooltip.
- **PII parity (the sharp rule).** Alt/`aria-label` must match the **visually-authorized** string, not the full database record. If the UI obscures the surname ("Jane D."), the accessible name must be "Jane D." too — extracting the full name for the a11y tree while hiding it visually violates parity and risks data exposure.

## 8. Motion and transition
- **Image fade-in on load** — the photo cross-fades in over the Skeleton/idle state (≈150ms opacity ease-in) to avoid a harsh paint flash; the shape-matched Skeleton means no layout shift (see skeleton).
- **Group spread on hover** — the face-pile's negative margins may transition to positive on hover, spreading the avatars to reveal full faces.
- **Reduce-motion** — gate the fade and the spread behind `prefers-reduced-motion: reduce`; disable the spread (or replace with a static tooltip) and drop to an instant swap. The image/identity is the information, not the motion.

## 9. Internationalization
- **The initials algorithm breaks on non-Latin scripts (the headline i18n problem).**
  - **CJK:** the Western "first letter of first + first letter of last" doesn't map — CJK names aren't space-delimited, and combining disparate characters changes the meaning; two dense CJK glyphs are illegible in a small mask. Detect the Unicode block and **extract only the first character** (the family name in CJK order — "鈴" from "鈴木 一郎"), or bypass initials and go straight to the icon to avoid misrepresentation.
  - **Arabic / Hebrew (RTL):** the name order flips; bidirectional handling required.
  - **General:** don't hardcode "first + last letter of a Latin string" — derive per locale (the `getInitials` override exists for this), and prefer the *image* (which sidesteps the problem) where possible.
- **RTL group stacking** — the face-pile mirrors: the first DOM avatar renders on the far **right** and subsequent avatars stack left, with the leading rightmost on top; achieved via logical properties / layout inversion, no JS.
- **Color-from-name across scripts** — hash over the *full* name string (not a Latin transliteration) so a person gets a stable color regardless of script.
- **The presence-dot anchor** mirrors under RTL (inherits the Badge RTL contract — see badge).

## 10. Naming
- **The field set:** **`Avatar`** is the overwhelming standard (MUI, Chakra, Radix, Primer, Atlassian, Base Web, Spectrum); **`Persona`** was Fluent's name for the *composite* lockup (avatar + text + presence + detail) — Fluent v9 has since separated `Avatar` as the primitive and reserved `Persona` for the composite pattern; **`UserAvatar`** appears in older Carbon to distinguish human from system entities; **`Gravatar`** is the service, not a component.
- **The practice's default — `Avatar`** for the primitive, **`AvatarGroup`** for the face-pile (the dominant API name, over Primer's `AvatarStack` and Ant's `Avatar.Group`). The richer name+avatar+metadata lockup (Fluent's `Persona`) is a *composed pattern* (Avatar + Text), not the primitive — keep the primitive small. The person-token form is **`AvatarToken`** in a Tag/Combobox context (see tag).
- **Entity type is a prop, not a component** — model person/org/bot as a `shape`/`type` variant (it drives the geometry + the default fallback icon), don't split into `UserAvatar`/`OrgAvatar`.
- **Aliases to map:** Persona, UserAvatar, Gravatar, ProfilePicture, AvatarStack, Avatar.Group, AvatarToken, Face pile, `<s-avatar>`.

## 11. Implementation notes
- **The SSR / cached-image flash trap (the headline, and a genuine fork).** Headless libraries (Radix) run the fallback chain through a JS hook (`useImageLoadingStatus`) that instantiates a virtual `window.Image()`, attaches `onload`/`onerror`, and only then renders the `<img>` — which **prevents the broken-image flash on slow loads** but **causes a flash on SSR + cached images**: on the server `window.Image` doesn't exist (the fallback initials ship in the HTML), and on the client the component must mount, instantiate the virtual image, and wait for an async `onload` that *for a cached image may have already fired* — so the user sees the fallback flash before the cached image swaps in, scaling with hydration delay. **The practice default: render the native `<img>` with `src` immediately** (a cached image then paints synchronously alongside the HTML — no flash), use the **native `onError`** to set the fallback, render the **fallback layer underneath** the image (so a slow load shows initials, not a broken glyph — the part both passes agree on), and **check `img.complete` on mount** (a ref/effect) to catch cached images whose `load` fired before React attached its handler. Add **`delayMs`** to debounce *showing* the fallback so a fast network doesn't flash it. (The fork: Radix's virtual-Image machine vs native-`<img onError>` — the practice leans native for the SSR/cache-common case.)
- **The presence-dot `overflow: hidden` clipping trap (resolved from the host side).** A circular avatar masks its image with `border-radius` + `overflow: hidden`, which **clips a PresenceBadge** overhanging the corner (the trap Badge named). The robust fix is **DOM separation**: a non-clipping `position: relative` **host wrapper** containing (a) a `overflow: hidden` **mask** with the image, and (b) the absolutely-positioned **badge** as a sibling — so the clip applies only to the image. (`clip-path: inset(0 round 50%)` is an alternative that in some engines lets pseudo-elements escape the box, but DOM separation is the most robust, cross-browser-predictable solution — the clip-path escape is flagged unverified.)
- **The deterministic color hash** — never random (jarring across sessions). Hash the name to a stable integer via a bitwise string-hash (`hash = name.charCodeAt(i) + ((hash << 5) - hash)`), then **modulo an accessibility-vetted array of design-system color tokens** — never generate arbitrary hex (that bypasses contrast validation and guarantees eventual 1.4.3 failures).
- **Initials sizing** — map the initials `font-size` to ≈**40% of the avatar's bounding width** so they stay legible across the size scale without overflowing.
- **`object-fit: cover`** — never `fill` (distorts faces); center the crop.
- **Lazy-loading** — `loading="lazy"` for off-screen avatars (long lists); eager above-the-fold (the profile header) to avoid a visible pop.
- **The AvatarGroup overlap + overflow** — negative `margin-inline-start` of ≈**20–25% of the width** (−8px on a 32px avatar) for the overlap, a ring-stroke per avatar, `z-index` ordering; the **"+N" counter** computed `total − max` (static) or via a **ResizeObserver** for a responsive count (the same JS-not-CSS reality as Tag's "+N more" — see tag); hidden avatars in a popover/list on demand.
- **The loading Skeleton** — a circular Skeleton sized to the box, swapped on image `load` (see skeleton).
- **Headless vs opinionated** — the fallback state machine, the a11y name contract, and the group overflow are the substrate worth owning; the shape/palette/ring is theme. Ship opinionated (MUI/Chakra/Fluent) — a bare `<img>` is not an Avatar.

## 12. Related and alternative components
- **Stands on:** **Icon** (the generic placeholder fallback — see icon) and **Skeleton** (the circular image-loading placeholder — see skeleton).
- **Hosts (composed, as the presence host):** **Badge** / **PresenceBadge** — the online/away/busy dot is a Badge positioned absolutely over the avatar host; the Avatar controls the geographic positioning (and resolves the `overflow: hidden` clipping trap), the Badge controls the status semantics (see badge).
- **Hosted by:** **Tag** (Primer's `AvatarToken` — a person token — see tag), the multi-select **Combobox** tokens (see combobox), list items, comment/message headers, nav, and user menus (a clickable avatar → **Menu** — see menu).
- **Boundary:** **Icon** (a symbol, not an identity — see icon) and **Image** (generic content media — the architectural boundary: an avatar is an identity anchor).
- **Composed into:** a name+avatar+metadata **lockup** (Fluent's `Persona`) — Avatar + Text, a pattern not a primitive.

(A Foundations primitive — the person/entity identity surface, the fallback-backed and presence-dot host. It stands on Icon (fallback) + Skeleton (loading), hosts Badge's PresenceBadge (the status dot), and is hosted by Tag/Combobox tokens + list/comment/nav. See icon/skeleton for the substrates, badge for the presence-dot composition + the clipping trap, tag/combobox for the token hosts, menu for the clickable-avatar trigger. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The fallback-chain hardening.** From a naive `<img alt="user">` to a multi-stage state machine (image → initials → icon) as broken-image glyphs became unacceptable in high-fidelity enterprise UI — and then the *refinement* that a purely JS-driven loading machine reintroduces a flash on SSR + cached images, pushing the field back toward native `<img onError>` + an `img.complete` check + a fallback-underneath.
2. **The decorative-when-redundant a11y settling.** Early implementations appended the name to *every* avatar's `alt`; standardized screen-reader testing exposed the double-announcement in lists, and the rule that avatars adjacent to visible text must be `aria-hidden` became settled best practice (the inverse of Icon's decorative-by-default).
3. **Color-from-name accessibility scrutiny.** The deterministic name-hashed palette came under 1.4.1/1.4.3 scrutiny — the initials must clear contrast against every palette entry, and color must never be the sole differentiator between people.
4. **Shape as entity-type semantics.** Squares/rounded-squares for orgs/repos (Primer, Atlassian) established shape as a primary entity-type signal, not an aesthetic variant — now extending to the **hexagon for AI agents/bots** (Atlassian Rovo).
5. **AvatarGroup overflow convergence.** The face-pile + "+N more" overflow (with a `role=group` + count and `aria-hidden` children) converged across MUI/Ant/Primer/Atlassian, paralleling Tag's "+N more" and Badge's count cap.
6. **The Web Component shift.** Systems like Polaris are migrating the avatar's fallback/hash logic into universal Web Components (`<s-avatar>`) for cross-stack interoperability without rewriting the chain.

## 14. Sources cited
(Conservative; reconcile with external.) **MUI** — `Avatar` (image/letter/icon fallback; `variant` circular/rounded/square; `AvatarGroup` `max`/`total`/`surplus`; string-to-color hashing; v5) (2024–2026); **Chakra UI** — `Avatar` (`name`→initials via `getInitials`; `AvatarBadge`; `AvatarGroup` `max`; color-from-name; v2/v3) (2024–2026); **Radix UI / Shadcn** — the headless `useImageLoadingStatus` state machine + `delayMs` (the fallback-debounce; the SSR/cache flash discussion) (2024–2026); **Microsoft Fluent UI v9** — `Avatar` / `Persona` (initials; the `idForColor` deterministic override; `PresenceBadge`; the primitive/composite split; ~v9.68) (2024–2026); **GitHub Primer** — `Avatar` / `AvatarStack` / `AvatarToken` (the square-for-orgs convention; v36) (2024–2026); **Atlassian Design System** — `Avatar` / `AvatarGroup` / `AvatarItem` (presence + status; the hexagon-for-AI/Rovo shape; v25) (2024–2026); **Shopify Polaris** — `Avatar` (initials; customer vs business; the `<s-avatar>` Web Component migration; v13) (2024–2026); **Adobe Spectrum / React Aria** — `Avatar` (the minimal img-with-alt primitive; strict WAI-ARIA group tagging; v3) (2024–2026); **IBM Carbon** — `UserAvatar` / the avatar pattern (2024–2026); **Base Web (Uber)** — `Avatar` (2024); **WAI-ARIA / HTML** — the `img` `alt` contract; no formal avatar pattern; decorative-vs-informative image; `role=group` for the face-pile. WCAG 2.2 (W3C Recommendation, Oct 2023) — 1.1.1, 1.4.1, 1.4.3, 4.1.2.

## 15. Agent-consumable schema

```yaml
identity:
  id: avatar
  name: Avatar
  aliases: [Persona, UserAvatar, Gravatar, ProfilePicture, AvatarStack, Avatar.Group, AvatarToken, Face pile, s-avatar]
  category: foundations
  status: stable
description: >
  The visual representation of a person or entity (user/org/bot) — a masked,
  fallback-backed identity surface. Three things define it: the FALLBACK CHAIN
  (image → initials → generic icon, with the onError/SSR/cached-image flash machine),
  the contextual ACCESSIBLE-NAME CONTRACT (informative bare avatar = the person's
  name; decorative when adjacent to a visible name; the fallback preserves the name —
  the inverse of Icon's decorative-by-default), and the GROUP / FACE-PILE (the overlap
  stack + '+N more' overflow + the group-name-and-count via role=group + aria-hidden
  children). NOT an Icon (a symbol/affordance), NOT a generic Image (arbitrary media).
  Stands on Icon (fallback) + Skeleton (loading); hosts Badge's PresenceBadge (the
  status dot); hosted by Tag/Combobox tokens + list/comment/nav.
anatomy:
  parts:
    - "host wrapper (div/span): the bounding box + RELATIVE positioning context; MUST NOT be overflow:hidden (else it clips the PresenceBadge)"
    - "masking layer (div): the shape (border-radius/clip-path) + overflow:hidden ON THE INNER MEDIA ONLY"
    - "media node (img): object-fit:cover (never distort), srcset/DPR"
    - "initials fallback (span): 1-2 letters centered in the mask, on the deterministic name-hashed background; the 2nd link"
    - "icon placeholder (svg): a generic person/org/bot glyph (inherits Icon); the final link (no image AND no name)"
    - "loading skeleton (div): a shape-matched Skeleton in transit (no CLS; inherits Skeleton)"
    - "presence anchor (div): the absolute bottom-trailing slot for the status Badge, on the NON-CLIPPING wrapper"
    - "group ring: a canvas-color stroke per stacked avatar (the cutout idea from Badge's count pill)"
api:
  inherits:
    - icon          # the generic placeholder fallback
    - skeleton      # the circular image-loading placeholder
  hosts:
    - badge         # PresenceBadge — the presence/status dot (Avatar is the host)
  props:
    - {name: src/srcSet, type: string, default: ~, required: false, description: "the image source(s) (DPR/Retina)"}
    - {name: name, type: string, default: ~, required: false, description: "drives the initials, the accessible name, AND the color hash — the most load-bearing prop"}
    - {name: alt/decorative, type: "string | boolean", default: "name", required: false, description: "the accessible-name control; alt defaults to name; decorative/aria-hidden for the redundant-adjacent case"}
    - {name: icon, type: node, default: "person glyph", required: false, description: "the custom fallback glyph (person/org/bot)"}
    - {name: shape/variant, type: "'circle' | 'rounded' | 'square' | 'hexagon'", default: circle, required: false, description: "entity-type geometry: circle=person, square=org, hexagon=AI/bot"}
    - {name: size, type: "'xs'|'sm'|'md'|'lg'|'xl'", default: md, required: false, description: "xs 20/sm 24/md 32/lg 40/xl 64+ px; initials font ~40% of width; icon scales"}
    - {name: delayMs, type: number, default: 0, required: false, description: "delay rendering the FALLBACK to avoid flashing it on a fast network (Radix/Shadcn)"}
    - {name: getInitials, type: function, default: ~, required: false, description: "override the name→initials parsing (the i18n escape hatch)"}
    - {name: color/idForColor, type: "enum | string", default: "hash(name)", required: false, description: "override the deterministic color hash (disambiguate identical names) (Fluent)"}
    - {name: presence/status, type: "slot | enum", default: ~, required: false, description: "the PresenceBadge slot (online/away/busy/offline) — Avatar is the host (see badge)"}
  group: "AvatarGroup/AvatarStack with max/total/surplus (MUI max/total, Ant maxCount/maxPopover) — caps visible avatars, renders the '+N' overflow, owns overlap/stacking/group-name"
  compositional-alt: "primitive libs (React Aria, Radix) split <Avatar.Image>/<Avatar.Fallback> — consumer orchestrates the data flow rather than fanning out from name"
states:
  runtime: [idle/loading, loaded-image, error-initials, error-icon]   # the FALLBACK machine, not interaction states
  interactive: "only if a trigger (clickable account avatar -> Menu) — then inherits Button/Menu focus/hover (see button, menu); a bare display avatar has none"
variants:
  content: [image, initials, icon]
  shape: [circle, rounded, square, hexagon]   # circle=person, square=org/team/project, hexagon=AI/bot
  size: [xs, sm, md, lg, xl]
  with-presence: [online, away, busy, offline, none]
  group: [single, stacked]
accessibility:
  inherits: [badge (presence-dot text-equivalent + color-not-sole-carrier)]
  wcag-criteria: ["1.1.1", "1.4.1", "1.4.3", "4.1.2"]
  name-contract: "CONTEXTUAL, the inverse of Icon's decorative-by-default (avatars usually CARRY identity)"
  informative: "a bare avatar = the sole identity -> alt='Jane Doe' (or aria-label on the wrapper for bg-image/SVG); an empty alt here is a 1.1.1 unlabeled-image failure"
  decorative-when-redundant: "an avatar ADJACENT to a visible name -> alt=''/aria-hidden, so the name isn't announced twice (the most-missed Avatar a11y decision)"
  fallback-preserves-name: "initials/icon are VISUAL shorthands, never the ACCESSIBLE name — an initials avatar still exposes 'Jane Doe' not 'JD' (common bug: onError drops the alt)"
  group: "role=group + a descriptive aria-label ('5 collaborators' / 'Jane, John, and 3 others') on the wrapper, ALL child avatars aria-hidden=true; hidden avatars via the on-demand list, NOT five 'image' announcements"
  presence-dot: "the status folds into the name ('Jane Doe, online'), the visual dot aria-hidden; color never the sole carrier (inherits Badge's contract)"
  color-from-name: "a DECORATIVE differentiator, never meaning (two people can hash to one color — 1.4.1); initials contrast >=4.5:1 (3:1 large) against EVERY palette entry (1.4.3) — curate the palette"
content:
  name-source: "the person's real display name (drives initials + accessible name); not a handle where a real name exists"
  initials:
    western: "first char of first word + first char of last word ('Jane Anne Doe' -> 'JD')"
    mononym-org: "single char ('Etsy'->'E')"
    email: "strip the domain, initials from the local part ('jane.doe@…'->'JD', 'admin@…'->'A')"
    capitalization: "normalize to uppercase regardless of input"
  alt-pattern: "informative: alt='[Name]'; decorative: alt=''; NOT 'Avatar of Jane Doe' (verbose)"
  group-label: "the surplus shows '+5' (numeric + plus), NEVER '+5 more' in the circle (overflow); the text goes in aria-label/tooltip"
  pii-parity: "alt/aria-label must match the VISUALLY-AUTHORIZED string ('Jane D.') not the full DB record — extracting the full name for the a11y tree while hiding it visually violates parity + risks exposure"
motion:
  image-fade-in: "the photo cross-fades in over the Skeleton/idle on load (~150ms opacity ease-in); shape-matched skeleton = no CLS"
  group-spread: "the face-pile's negative margins transition to positive on hover, revealing full faces"
  reduce-motion: "gate the fade + spread behind prefers-reduced-motion -> instant swap / static tooltip (the image/identity is the information, not the motion)"
i18n:
  initials-across-scripts: "the Western first+last rule breaks: CJK is family-name-first, not space-delimited, dense -> extract ONLY the first char (family name, '鈴' from '鈴木 一郎') or go straight to the icon; Arabic/Hebrew RTL flips the order; derive per locale (getInitials), prefer the IMAGE where possible"
  rtl-group: "the face-pile mirrors — first DOM avatar on the far RIGHT, subsequent stack left, leading rightmost on top; logical properties / layout inversion, no JS"
  color-hash-across-scripts: "hash over the FULL name string (not a Latin transliteration) for a stable color regardless of script"
  presence-anchor: "the presence-dot corner mirrors under RTL (inherits the Badge RTL contract)"
implementation:
  - "the SSR/cached-image flash trap (the headline + a fork): a JS virtual-Image() machine (Radix useImageLoadingStatus) prevents the broken-image flash but CAUSES a flash on SSR+cached images (window.Image absent server-side -> fallback ships; client waits for an async onload that for a cached image already fired). FIX (practice default): render the native <img src> immediately (cached paints synchronously), native onError sets the fallback, the fallback layer UNDERNEATH (slow load shows initials not a broken glyph), and CHECK img.complete on mount (catch cached images whose load fired pre-hydration); delayMs debounces showing the fallback. Fork: Radix virtual-Image vs native-<img onError> — practice leans native for the SSR/cache case"
  - "the presence-dot overflow:hidden clipping trap (resolved from the host side): DOM separation — a NON-CLIPPING relative HOST WRAPPER containing (a) an overflow:hidden MASK with the image and (b) the absolute BADGE as a sibling (the clip applies only to the image). clip-path:inset(0 round 50%) is an alt that lets pseudo-elements escape in some engines, but DOM separation is the robust cross-browser fix"
  - "the deterministic color hash: NEVER random; bitwise string-hash (hash = name.charCodeAt(i) + ((hash<<5)-hash)) mod an ACCESSIBILITY-VETTED token array; never arbitrary hex (bypasses contrast validation -> 1.4.3 failures)"
  - "initials sizing: map font-size to ~40% of the avatar's bounding width (legible across the scale, no overflow)"
  - "object-fit:cover (never fill — distorts faces), center the crop"
  - "lazy-load (loading=lazy) off-screen avatars (long lists); eager above-the-fold (profile header) to avoid a pop"
  - "AvatarGroup overlap (negative margin-inline-start ~20-25% of width, -8px on 32px) + ring-stroke + z-index; '+N' counter = total-max (static) or ResizeObserver (responsive, JS-not-CSS like Tag's '+N more'); hidden avatars in a popover/list on demand"
  - "the loading Skeleton: a circular Skeleton sized to the box, swapped on image load (see skeleton)"
  - "headless vs opinionated: the fallback state machine + the a11y name contract + the group overflow are the substrate; shape/palette/ring is theme. Ship OPINIONATED — a bare <img> is not an Avatar"
composition:
  stands-on: [icon, skeleton]
  hosts: [badge]                           # PresenceBadge — the presence dot (Avatar is the host)
  hosted-by: [tag, combobox]               # AvatarToken / multi-select tokens; + list/comment/nav/menu
  composed-into: [persona]                 # name+avatar+metadata lockup (Fluent Persona — a pattern, not the primitive)
  boundary: [icon, image]                  # a symbol / generic media
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "fallback loading: the JS virtual-Image() machine (Radix — no broken-image flash) vs native <img src onError> + img.complete check (no SSR/cache flash — the practice default)"
    - "initials count (1 vs 2) + the name-order/CJK/RTL derivation"
    - "shape: circle-for-everything vs square-for-orgs + hexagon-for-AI (entity-type signal)"
    - "color-from-name on by default vs off (decorative but contrast-risky)"
    - "single name-prop fan-out (Chakra/Fluent) vs compositional Avatar.Image/Avatar.Fallback (React Aria/Radix)"
    - "group naming: AvatarGroup (practice default) vs AvatarStack (Primer) vs Avatar.Group (Ant)"
  trap:
    - "the onError swap dropping the alt (fallback loses the accessible name)"
    - "SSR + cached-image flash (the JS virtual-Image machine waits for an onload that already fired) — render native <img src> + check img.complete"
    - "overflow:hidden on the HOST wrapper clipping the presence dot (needs DOM separation — clip only the mask)"
    - "initials failing contrast against a name-hashed background (1.4.3); generating arbitrary hex instead of a vetted palette"
    - "relying on color-from-name to distinguish people (1.4.1); announcing the name twice (avatar not decorative when adjacent)"
    - "object-fit:fill distorting faces; a face-pile read as N separate images instead of group+count"
    - "PII leak: full name in alt while the UI shows 'Jane D.' (parity violation)"
  inherited:
    - "Icon (the fallback placeholder) + Skeleton (the loading state)"
    - "the Badge presence-dot overlay substrate + its text-equivalent/color contract (Avatar is the host)"
  role-in-family: "a Foundations primitive — the person/entity identity surface; stands on Icon+Skeleton, hosts Badge's PresenceBadge, hosted by Tag/Combobox tokens + list/comment/nav; the inverse of Icon's decorative-by-default a11y"
  evolution:
    - "the fallback-chain hardening (multi-stage; then native-<img onError>+complete-check over the JS virtual-Image machine, for SSR/cache)"
    - "the decorative-when-redundant a11y settling (inverse of Icon)"
    - "color-from-name accessibility scrutiny (contrast + not-sole-differentiator)"
    - "shape-as-entity-type (square-for-orgs; hexagon-for-AI/Rovo)"
    - "AvatarGroup overflow convergence ('+N more' + role=group + count, paralleling Tag/Badge)"
    - "the Web Component shift (Polaris <s-avatar>)"
  unverified:
    - "external 2026 version numbers (Fluent ~v9.68, Primer v36, Atlassian v25, Polaris v13, React Aria v3)"
    - "the per-system initials algorithms + the color-hash palettes — verify against current implementations"
    - "the clip-path:inset() pseudo-element bounding-box escape across older browser engines — needs explicit QA before replacing DOM-separation"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-avatar/` (16 June 2026), the thirty-fourth brief and the Foundations primitive Badge and Tag forward-referenced (the presence-dot host / the `AvatarToken` host). It stands on Icon (the placeholder fallback) + Skeleton (the loading state), hosts Badge's PresenceBadge (the status dot — and resolves the `overflow: hidden` clipping trap from the host side), and is hosted by Tag's `AvatarToken` + the multi-select Combobox tokens + list/comment/nav. The two passes converged on the substance — the fallback chain (image → initials → icon), the contextual accessible-name contract (informative bare avatar = the name; decorative when adjacent to a visible name; the fallback preserves the name — the inverse of Icon's decorative-by-default), the AvatarGroup face-pile (overlap + "+N more" + the `role=group`/`aria-hidden`-children group-name-and-count), the deterministic color-from-name (contrast + not-sole-differentiator), shape-as-entity-type, and the presence-dot clipping trap. The one genuine reconciliation was the **SSR/cached-image flash**: the Claude pass framed the fix as "fallback-as-default, image-on-top revealed on `load`"; the external pass sharpened that a purely JS-driven virtual-`Image()` machine (Radix's `useImageLoadingStatus`) *causes* a flash on cached images during hydration (it waits for an `onload` that already fired), so the resolved practice default is the **native `<img src onError>` + the `img.complete`-on-mount check + the fallback underneath + `delayMs`** (a fork flagged in notes). The external pass also supplied the hexagon-for-AI shape (Atlassian Rovo), the `delayMs`/`getInitials`/`idForColor` props, the concrete bitwise hash algorithm + the ≈40%-of-width initials sizing + the ≈20–25% overlap offset, the email-local-part initials fallback, the PII-parity sharpening (alt matches the visually-authorized string), and the Polaris `<s-avatar>` Web Component shift. Claude-pass contributions: the fallback/identity/group framing, the substrate-and-host inheritance map, the Avatar-vs-Icon-vs-Image boundary, and the decorative-when-adjacent usage rule. The 2026 version numbers, the per-system initials/palette specifics, and the clip-path escape are flagged unverified. Conformant to `components/_schema.md`.*
