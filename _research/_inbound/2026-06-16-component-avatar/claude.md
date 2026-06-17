# Avatar — field-truth study (Claude pass)

## 1. Framing
An Avatar is the **visual representation of a person or entity** (a user, an org/team, a bot) — a small, usually-circular surface carrying a photo, the person's initials, or a generic placeholder. It is a Foundations primitive, but unlike the truly inert primitives (Divider, Icon-as-decoration) it carries a small machine: a **fallback chain** and an **identity-announcement contract**. Three things define it and are where systems diverge:

- **The fallback chain (the headline).** image → initials → generic icon. An avatar must degrade gracefully when the image is missing or fails to load: attempt the photo, fall back to initials derived from the name, fall back again to a generic person/placeholder icon. The contract is about *order, timing, and failure* — the `onError` swap, the loading state (a circular **Skeleton**, not a layout jump or a flash of broken-image), and SSR (where `onError` never fires on the server). This is the defining Avatar problem.
- **The accessible-name contract (the accessibility crux).** What does an avatar *announce*? It depends on context, and the rule is the **inverse of Icon's decorative-by-default**: an avatar is often *informative*. A **bare avatar** carrying the only identity (a photo with no adjacent name) needs the person's name as its accessible name (`alt="Jane Doe"`); an avatar **adjacent to a visible name** (a list row, a comment header) is *redundant* and should be **decorative** (empty `alt` / `aria-hidden`) so the name isn't announced twice. And every fallback must **preserve the name** — initials/icon still expose "Jane Doe", never "JD" or "person icon".
- **The group / face-pile.** Avatars cluster into an overlapping stack ("5 people on this thread") with a **"+N more"** overflow — parallel to Tag's "+N more" and Badge's count cap. The group has its own accessible name announcing the *count*, not N separate images.

It stands on **Icon** (the generic placeholder fallback — see icon) and **Skeleton** (the circular loading placeholder — see skeleton), is the **host for Badge's PresenceBadge** (the online/away/busy dot is a Badge overlaid on the avatar — see badge), and is **hosted by** Tag (Primer's `AvatarToken`), the multi-select Combobox tokens, list items, comments, and nav (see tag, combobox). What it *isn't*: an **Icon** (a symbol/glyph, not a person — see icon) or a generic **Image** (an avatar is a *masked, fallback-backed identity surface* with a fixed aspect ratio, not arbitrary media). Why systems disagree: the fallback timing/SSR, the initials + color-from-name algorithm, and the shape/entity-type convention.

## 2. Anatomy and parts
- **the image** — the photo: `object-fit: cover` (never distort), masked to the shape, with `srcset`/DPR handling and lazy-loading (§11). The first link in the fallback chain.
- **the initials fallback** — 1–2 letters derived from the name, on a deterministic background color hashed from the name (§ initials/color); the second link.
- **the icon placeholder** — a generic person/org/bot glyph (inherits Icon — see icon); the final link when there's no image *and* no name.
- **the shape / mask** — circle (the person default) or rounded-square/square (often the org/entity convention); a `border-radius` + `overflow: hidden` clip (which creates the presence-dot trap — §11).
- **the presence-dot anchor** — the overlay slot for Badge's PresenceBadge (online/away/busy), anchored to a corner (bottom-trailing common); a **non-clipping wrapper** so the avatar's `overflow: hidden` doesn't eat the dot (the trap Badge named, resolved from the host side — §11). Inherits the Badge overlay substrate (see badge).
- **the AvatarGroup ring/stroke** — in a stack, each avatar carries a ring (a canvas-color stroke) to separate it from the overlapping neighbor — the same cutout-stroke idea Badge uses for the count pill (see badge).
- **the loading skeleton** — a circular Skeleton occupying the avatar's box while the image loads (inherits Skeleton — see skeleton); reserves the layout (no CLS).

## 3. Properties / API
- **`src` / `srcSet`** — the image source(s) (responsive/DPR).
- **`name`** — the person/entity name: drives **both** the initials *and* the accessible name. The single most load-bearing prop (the fallback and the a11y both read from it).
- **`alt` / `decorative`** — the accessible-name control: `alt` defaults to `name`; a `decorative`/`aria-hidden` flag for the redundant-adjacent-to-a-visible-name case (§6).
- **`icon`** — the custom fallback glyph (overrides the default person icon).
- **`shape` / `variant`** — circle / rounded / square (MUI `variant`, Ant `shape`).
- **`size`** — xs / sm / md / lg / xl (token-mapped); initials and icon scale with it (§ sizing).
- **the presence / status slot** — a `badge`/`presence`/`status` prop or a composed `<AvatarBadge>`/`<PresenceBadge>` child (Chakra's `AvatarBadge`, Fluent's `PresenceBadge`) — the Avatar is the host (see badge).
- **`colorFromName` / the deterministic color** — the initials background hashed from the name (Chakra/Fluent); decorative, not meaningful (§6).
- **the group:** `AvatarGroup` / `AvatarStack` with **`max` / `total` / `surplus`** (MUI `max`/`total`, Ant `maxCount`/`maxPopover`) — caps the visible avatars and renders the "+N" overflow counter; owns the overlap, the stacking direction, and the group accessible name (§6/§11).
- **the loading state** — a `loading`/`isLoading` flag or automatic (show the Skeleton until the image resolves — see skeleton).

## 4. States and variants
- **States (the fallback machine, not interaction states):** **loading** (the Skeleton placeholder), **image** (loaded), **initials** (no image / image failed, name present), **icon** (no image *and* no name), plus an optional **interactive** state if the avatar is a trigger (a clickable account avatar → Menu — then it inherits Button/Menu focus/hover, see button, menu). A bare display avatar has no interaction states.
- **Variants:**
  - **content:** image / initials / icon.
  - **shape:** circle (person) / rounded / square (org/entity).
  - **size:** xs / sm / md / lg / xl.
  - **with-presence:** the status-dot overlay (online/away/busy/offline).
  - **group / stacked:** the face-pile with "+N" overflow.
  - **entity type:** person / organization / bot (drives the shape + the default fallback icon).

## 5. Usage guidance
- **Use an Avatar for:** representing a *person or entity* — user menus, comment/message authorship, assignee/collaborator lists, profile headers, person tokens (in a Tag/Combobox — see tag, combobox).
- **Don't use an Avatar for:**
  - A **symbol / action glyph** → an **Icon** (see icon). An avatar is an identity, not a meaning.
  - **Generic media / a thumbnail** → an **Image** (an avatar is a masked, fallback-backed, fixed-aspect identity surface; a product thumbnail is not an avatar).
- **Decision frameworks:**
  - **Initials vs icon fallback:** if the name is known, fall back to **initials** (more identifying, more personal); fall back to the generic **icon** only when there's no name either (an anonymous/unknown user). Don't show a generic icon when initials are available.
  - **Decorative-when-adjacent (the load-bearing usage rule):** if the avatar sits next to a visible name, make it **decorative** so screen readers don't announce the name twice; if the avatar is the *only* identity, it carries the name (§6).
  - **AvatarGroup vs a list:** use the face-pile for a *compact, glanceable* count of collaborators (with "+N" + the full list on demand); use a real list when the names/roles matter and need to be read.
  - **Presence dot when:** only when real-time availability is meaningful (chat, collaboration); don't decorate every avatar with a status it doesn't have.

## 6. Accessibility
**The accessible-name contract is the crux, and it's contextual** — the inverse of Icon's decorative-by-default, because avatars are often the carrier of identity.

- **Informative (bare) avatar → the name is the accessible name.** An avatar that is the *only* representation of a person (a photo with no adjacent text) must expose the name: `<img alt="Jane Doe">`. A bare avatar with an empty `alt` is an unlabeled image — a 1.1.1 failure.
- **Decorative (redundant) avatar → silence it.** When the avatar sits beside a visible name (a list row, a comment header, a `name + avatar` lockup), the name is already in the DOM; the avatar should be **decorative** (`alt=""` / `aria-hidden="true"`) so the screen reader doesn't announce "Jane Doe, image, Jane Doe". This redundant-decorative rule is the most-missed Avatar a11y decision.
- **The fallback preserves the name.** Initials and the icon fallback are *visual* shorthands — they must not become the *accessible* name. An initials avatar still exposes "Jane Doe" (not "JD"); an icon fallback still exposes the name (not "person icon") when the avatar is informative, or is `aria-hidden` when decorative. (Common bug: the `onError` swap to initials drops the `alt`.)
- **The AvatarGroup announces the group + count, not N images.** A face-pile of 5 should read as "5 collaborators" (a group label + count), not five separate "image" announcements; the "+N" surplus is part of the count, and the hidden avatars are reachable via the on-demand list, not the stack. Mark the individual stacked images decorative and label the group, or expose a single composite name.
- **The presence dot has a text equivalent** (inherits Badge's contract — see badge): the status folds into the name ("Jane Doe, online"), the visual dot is `aria-hidden`; color is never the sole carrier of the status (online-green/away-amber/busy-red all need a text equivalent — 1.4.1).
- **Color-from-name is decorative, not meaningful.** The deterministic background color is identity *flavor*, never a differentiator the user must perceive (two people can hash to similar colors); don't rely on it to distinguish people (1.4.1), and keep the initials' contrast against the generated background ≥ 4.5:1 (1.4.3) — the recurring failure of name-hashed palettes.
- **WCAG SCs:** **1.1.1** (non-text content — the informative avatar's name; the decorative one's empty alt), **1.4.1** (color not sole carrier — presence + color-from-name), **1.4.3** (contrast — initials on the generated background), **4.1.2** (name/role/value — the group, the presence). If the avatar is a *trigger*, it also takes the Button/Menu contract (a real accessible name on the control, see button, menu).

## 7. Content guidelines
- **The name source** — the avatar's `name` should be the person's display name as the app knows it; it drives both the initials and the accessible name, so it must be the *real* name, not a username/handle where a real name exists.
- **Initials rules** — 1–2 letters; the common algorithm is first-name-initial + last-name-initial (2), or a single initial for mononyms; handle multi-word names (take first + last, not middle), and don't assume Latin order (§9).
- **The alt-text pattern** — informative: `alt="[Name]"`; decorative: `alt=""`. Don't write "Avatar of Jane Doe" or "Jane Doe's profile picture" (verbose); the name alone is the contract.
- **The group "+N" label** — the surplus counter reads as part of the group count ("+3", with the group labelled "8 collaborators"); the "+N" itself, if interactive, gets a name ("Show 3 more").
- **No PII leak** — initials and the name are visible; don't surface a fallback that exposes data the user shouldn't see (e.g., an email local-part as initials).

## 8. Motion and transition
- **Image fade-in on load** — the photo cross-fades in over the Skeleton placeholder when it resolves (a brief opacity fade), avoiding a hard pop; the shape-matched Skeleton means no layout shift (see skeleton).
- **Group hover-expand / spread** — an AvatarGroup may spread/fan on hover to reveal overlapped faces, or the "+N" expands to the full list; keep it subtle and optional.
- **Presence transition** — a status change (online→away) cross-fades the dot; sparing.
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops the fade/spread to an instant swap (the image/identity is the information, not the motion).

## 9. Internationalization
- **Initials across scripts (the name-order problem).** First+last-initial is a Latin/Western convention. **CJK** names are family-name-first and often better represented by the full given/family character(s) than two "initials"; **Arabic/Hebrew** run RTL and the initial order flips; some cultures use mononyms or patronymics. Don't hardcode "first letter + last letter of the Latin string" — derive per locale, and prefer the *image* (which sidesteps the problem) where possible.
- **RTL group stacking** — the face-pile's overlap/stacking direction flips under RTL (the first avatar on the right); anchor the stacking and the presence-dot corner via logical properties so it mirrors off `dir="rtl"`.
- **Color-from-name across scripts** — the hash must run over the *full* name string (not just Latin transliteration) so the same person gets a stable color regardless of script.
- **The presence-dot anchor** flips with RTL (the corner mirrors), inheriting the Badge RTL contract (see badge).

## 10. Naming
- **The field set:** `Avatar` (MUI, Ant, Chakra, Primer, Polaris, Spectrum, Atlassian, Base Web — the dominant name); `Persona` (Fluent's richer name+avatar+presence lockup); `UserAvatar` (Carbon); historically `Gravatar` (the service, not a component).
- **The practice's default — `Avatar`** for the primitive (the dominant, unambiguous name), with **`AvatarGroup`** for the face-pile (over Primer's `AvatarStack` and Ant's `Avatar.Group` — `AvatarGroup` is the most common and reads clearly). The richer name+avatar+metadata lockup (Fluent's `Persona`) is a *composed* pattern (Avatar + Text), not the primitive — keep the primitive small. The person-token form is **`AvatarToken`** in a Tag/Combobox context (see tag).
- **Entity-type naming** — don't split into `UserAvatar`/`OrgAvatar`/`BotAvatar` components; model entity type as a prop/variant (it drives shape + the default fallback icon).
- **Aliases to map:** Persona, UserAvatar, Gravatar, ProfilePicture, AvatarStack, Avatar.Group, AvatarToken, Face pile.

## 11. Implementation notes
- **The fallback-chain `onError` + flash-of-broken-image + SSR trap (the headline implementation problem).** The naive approach renders an `<img>` and swaps to initials in `onError` — but (a) on the **server** `onError` never fires, so SSR ships the broken-image state and only corrects after hydration (a flash); (b) a slow/failed image can **flash the broken-image glyph** before the swap. The robust pattern: render the **Skeleton/initials underneath** and the image *on top*, revealing the image only on `load` (fading it in), and treating `onError` as "keep showing the fallback" — so the fallback is the default state and the image is the enhancement, not the reverse. Preload/`decode()` to avoid the flash; on SSR, render the fallback as the initial paint.
- **The presence-dot `overflow: hidden` clipping trap (resolved from the host side).** A circular avatar uses `overflow: hidden` (or `border-radius` + a clip) to mask its image — which **clips a presence dot** anchored to the corner (the trap Badge named). The fix: the dot lives on a **non-clipping wrapper** *outside* the masked image element — a relative-positioned wrapper containing the clipped image *and* the absolutely-positioned dot as siblings, so the mask applies only to the image, not the dot. (See badge for the overlay/anchor substrate.)
- **The initials algorithm + the deterministic color hash** — derive initials per the name (locale-aware, §9); hash the name to a palette index (a stable string-hash mod the palette length) for the background; **verify the initials' contrast against every palette entry** (≥4.5:1) at build time, not by eye — the recurring name-hash failure.
- **`object-fit: cover`** — never `fill` (distorts faces); center the crop.
- **Lazy-loading** — `loading="lazy"` for off-screen avatars (long lists), but eager for above-the-fold (the profile header) to avoid a visible pop.
- **The AvatarGroup overlap + overflow** — negative `margin-inline-start` for the overlap, a ring-stroke per avatar, `z-index` ordering (or reverse, so the first reads on top); the **"+N" counter** computed from `total - max` (static) or via a `ResizeObserver` for a responsive count (the same JS-not-CSS reality Tag's "+N more" has — see tag). The hidden avatars surface in a popover/list on demand.
- **The loading Skeleton** — a circular Skeleton sized to the avatar's box, swapped on image `load` (see skeleton).
- **Headless vs opinionated** — the fallback-chain state machine, the a11y name contract, and the group overflow are the substrate worth owning; the shape/palette/ring is theme. Ship it opinionated (MUI/Chakra/Fluent) — the fallback machine is the value; a bare `<img>` is not an Avatar.

## 12. Related and alternative components
- **Stands on:** **Icon** (the generic placeholder fallback — see icon) and **Skeleton** (the circular image-loading placeholder — see skeleton).
- **Hosts (composed-by, as the presence host):** **Badge** / **PresenceBadge** — the online/away/busy dot is a Badge overlaid on the Avatar (Avatar is the host; the `overflow: hidden` clipping trap is resolved here — see badge).
- **Hosted by:** **Tag** (Primer's `AvatarToken` — a person token — see tag), the multi-select **Combobox** tokens (see combobox), list items, comment/message headers, nav, and user menus (a clickable avatar → **Menu** — see menu).
- **Boundary:** **Icon** (a symbol, not an identity — see icon) and **Image** (generic media — an avatar is a masked, fallback-backed identity surface).
- **Composed into:** a name+avatar+metadata **lockup** (Fluent's `Persona`) — Avatar + Text, a pattern not a primitive.

(A Foundations primitive — the person/entity representation, the fallback-backed identity surface, and the presence-dot host. It stands on Icon (fallback) + Skeleton (loading), hosts Badge's PresenceBadge (the status dot), and is hosted by Tag/Combobox tokens + list/comment/nav. See icon/skeleton for the substrates, badge for the presence-dot composition + the clipping trap, tag/combobox for the token hosts, menu for the clickable-avatar trigger. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The fallback-chain hardening — image-on-top-of-fallback.** The field moved from the naive `<img>` + `onError`-swap (which flashes on SSR and slow loads) toward rendering the **fallback as the default state and the image as the enhancement** (revealed on `load`), eliminating the flash and fixing SSR.
2. **The decorative-when-redundant a11y settling.** The rule that an avatar adjacent to a visible name should be *decorative* (not double-announce the name) — the inverse of Icon's decorative-by-default — became the settled guidance.
3. **Color-from-name accessibility scrutiny.** The deterministic name-hashed palette came under contrast/1.4.1 scrutiny — the realization that the initials must clear contrast against *every* palette entry and that color must never be the sole differentiator between people.
4. **AvatarGroup overflow convergence.** The face-pile + "+N more" overflow (with a group accessible name + count) converged across MUI/Ant/Primer/Atlassian, paralleling Tag's "+N more" and Badge's count cap.
5. **The square-for-orgs convention.** Primer and others adopted rounded-square/square avatars for organizations/teams vs circles for people — shape as an entity-type signal.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- MUI — `Avatar` (image/letter/icon fallback; `variant` circular/rounded/square; `AvatarGroup` `max`/`total`/`surplus`; Badge for presence).
- Ant Design — `Avatar` (`src`/`srcSet`/`icon`/`children`; `shape`; `size`; `Avatar.Group` `maxCount`/`maxPopover`).
- Chakra UI — `Avatar` (`name`→initials via `getInitials`; `AvatarBadge` for presence; `AvatarGroup` `max`; the color-from-name).
- Microsoft Fluent — `Avatar` / `Persona` (initials; the name-derived color; `PresenceBadge`; `AvatarGroup`).
- GitHub Primer — `Avatar` / `AvatarStack` / `AvatarToken` (the square-for-orgs convention).
- Shopify Polaris — `Avatar` (initials; customer vs business; size).
- Adobe Spectrum / React Aria — `Avatar` (the minimal img-with-alt primitive).
- IBM Carbon — `UserAvatar` / the avatar pattern.
- Atlassian — `Avatar` / `AvatarGroup` / `AvatarItem` (presence + status).
- Base Web (Uber) — `Avatar`.
- WAI-ARIA / HTML — the `img` `alt` contract; no formal avatar pattern; decorative-vs-informative image.
- WCAG 2.2 — 1.1.1, 1.4.1, 1.4.3, 4.1.2.

## 15. Agent-consumable schema
```yaml
identity:
  id: avatar
  name: Avatar
  aliases: [Persona, UserAvatar, Gravatar, ProfilePicture, AvatarStack, Avatar.Group, AvatarToken, Face pile]
  category: foundations
  status: stable
description: >
  The visual representation of a person or entity (user/org/bot) — a masked,
  fallback-backed identity surface. Three things define it: the FALLBACK CHAIN
  (image → initials → generic icon, with the onError/SSR/flash machine), the
  ACCESSIBLE-NAME CONTRACT (informative bare avatar = the person's name; decorative
  when adjacent to a visible name; the fallback preserves the name), and the GROUP /
  FACE-PILE (the overlap stack + '+N more' overflow + the group-name-and-count). NOT
  an Icon (a symbol, not an identity), NOT a generic Image (arbitrary media). Stands
  on Icon (fallback) + Skeleton (loading); hosts Badge's PresenceBadge (the status
  dot); hosted by Tag/Combobox tokens + list/comment/nav.
anatomy:
  parts:
    - "image: object-fit:cover (never distort), masked to the shape, srcset/DPR + lazy-load; the first fallback link"
    - "initials fallback: 1-2 letters from the name on a deterministic name-hashed background; the second link"
    - "icon placeholder: a generic person/org/bot glyph (inherits Icon); the final link (no image AND no name)"
    - "shape/mask: circle (person) / rounded-square / square (org/entity); border-radius + overflow:hidden (the presence-dot clip trap)"
    - "presence-dot anchor: the overlay slot for Badge's PresenceBadge — on a NON-CLIPPING wrapper so overflow:hidden doesn't eat the dot (inherits the Badge overlay substrate)"
    - "AvatarGroup ring/stroke: a canvas-color stroke per stacked avatar (the same cutout idea as Badge's count pill)"
    - "loading skeleton: a circular Skeleton in the avatar's box while the image loads (inherits Skeleton; no CLS)"
api:
  inherits:
    - icon          # the generic placeholder fallback
    - skeleton      # the circular image-loading placeholder
  hosts:
    - badge         # PresenceBadge — the presence/status dot (Avatar is the host)
  props:
    - {name: src/srcSet, type: string, default: ~, required: false, description: "the image source(s) (responsive/DPR)"}
    - {name: name, type: string, default: ~, required: false, description: "drives BOTH the initials AND the accessible name — the most load-bearing prop"}
    - {name: alt/decorative, type: "string | boolean", default: "name", required: false, description: "the accessible-name control; alt defaults to name; decorative/aria-hidden for the redundant-adjacent case"}
    - {name: icon, type: node, default: "person glyph", required: false, description: "the custom fallback glyph"}
    - {name: shape/variant, type: "'circle' | 'rounded' | 'square'", default: circle, required: false, description: "circle=person, square=org/entity"}
    - {name: size, type: "'xs'|'sm'|'md'|'lg'|'xl'", default: md, required: false, description: "token-mapped; initials + icon scale with it"}
    - {name: presence/status, type: "slot | enum", default: ~, required: false, description: "the PresenceBadge slot (online/away/busy/offline) — Avatar is the host (see badge)"}
    - {name: colorFromName, type: boolean, default: true, required: false, description: "the deterministic name-hashed initials background; DECORATIVE not meaningful"}
    - {name: loading, type: boolean, default: auto, required: false, description: "show the Skeleton until the image resolves (see skeleton)"}
  group: "AvatarGroup/AvatarStack with max/total/surplus (MUI max/total, Ant maxCount/maxPopover) — caps visible avatars, renders the '+N' overflow, owns the overlap/stacking/group-name"
states:
  runtime: [loading, image, initials, icon]   # the FALLBACK machine, not interaction states
  interactive: "only if the avatar is a trigger (clickable account avatar -> Menu) — then inherits Button/Menu focus/hover (see button, menu); a bare display avatar has none"
variants:
  content: [image, initials, icon]
  shape: [circle, rounded, square]
  size: [xs, sm, md, lg, xl]
  with-presence: [online, away, busy, offline, none]
  group: [single, stacked]
  entity-type: [person, organization, bot]   # drives shape + the default fallback icon
accessibility:
  inherits: [badge (presence-dot text-equivalent + color-not-sole-carrier)]
  wcag-criteria: ["1.1.1", "1.4.1", "1.4.3", "4.1.2"]
  name-contract: "CONTEXTUAL, the inverse of Icon's decorative-by-default (avatars are often informative)"
  informative: "a bare avatar carrying the ONLY identity -> alt='Jane Doe' (an empty alt here is an unlabeled-image 1.1.1 failure)"
  decorative-when-redundant: "an avatar ADJACENT to a visible name (list row/comment header) -> alt=''/aria-hidden, so the name isn't announced twice (the most-missed Avatar a11y decision)"
  fallback-preserves-name: "initials/icon are VISUAL shorthands, never the ACCESSIBLE name — an initials avatar still exposes 'Jane Doe' not 'JD' (common bug: onError drops the alt)"
  group-name-and-count: "a face-pile reads as '5 collaborators' (group label + count), NOT five 'image' announcements; the '+N' is part of the count; hidden avatars reachable via the on-demand list"
  presence-dot: "the status folds into the name ('Jane Doe, online'), the visual dot aria-hidden; color never the sole carrier (inherits Badge's contract)"
  color-from-name: "DECORATIVE identity flavor, never a differentiator the user must perceive (1.4.1); initials contrast >=4.5:1 against EVERY palette entry (1.4.3) — the recurring name-hash failure"
content:
  name-source: "the person's real display name (drives initials + accessible name); not a handle where a real name exists"
  initials: "1-2 letters; first+last-initial (2) or a single initial for mononyms; first+last not middle; locale-aware (not Latin-order-assumed)"
  alt-pattern: "informative: alt='[Name]'; decorative: alt=''; NOT 'Avatar of Jane Doe'/'Jane Doe's profile picture' (verbose)"
  group-label: "the '+N' surplus reads as part of the group count; if interactive, named ('Show 3 more')"
  no-pii-leak: "don't surface a fallback exposing data the user shouldn't see (e.g., an email local-part as initials)"
motion:
  image-fade-in: "the photo cross-fades in over the Skeleton on load (brief opacity fade); shape-matched skeleton = no CLS"
  group-expand: "an AvatarGroup may spread/fan on hover or the '+N' expands to the list; subtle/optional"
  presence: "a status change cross-fades the dot; sparing"
  reduce-motion: "drop the fade/spread to an instant swap (the image/identity is the information, not the motion)"
i18n:
  initials-across-scripts: "first+last-initial is a Latin convention; CJK is family-name-first (full char often better than 2 'initials'); Arabic/Hebrew RTL flips the order; mononyms/patronymics exist — derive per locale, prefer the IMAGE where possible"
  rtl-group: "the face-pile overlap/stacking direction flips under RTL (first avatar on the right) via logical properties"
  color-hash-across-scripts: "hash over the FULL name string (not Latin transliteration) for a stable color regardless of script"
  presence-anchor: "the presence-dot corner mirrors under RTL (inherits the Badge RTL contract)"
implementation:
  - "the fallback-chain onError + flash-of-broken-image + SSR trap (the headline): onError never fires on the SERVER (SSR ships the broken state, corrects after hydration = flash) + a slow/failed image flashes the broken glyph. FIX: render the fallback (Skeleton/initials) as the DEFAULT state + the image ON TOP, revealing it only on `load` (fade in); onError = keep the fallback. Image is the enhancement, not the reverse; preload/decode() to avoid the flash"
  - "the presence-dot overflow:hidden clipping trap (resolved from the host side): a circular avatar's overflow:hidden masks the image AND clips a corner dot (Badge named it). FIX: the dot on a NON-CLIPPING wrapper OUTSIDE the masked image — a relative wrapper with the clipped image + the absolute dot as siblings (the mask applies only to the image)"
  - "initials algorithm + deterministic color hash: locale-aware initials; stable string-hash mod palette length for the background; verify initials contrast >=4.5:1 against EVERY palette entry at BUILD time, not by eye"
  - "object-fit:cover (never fill — distorts faces), center the crop"
  - "lazy-load (loading=lazy) off-screen avatars (long lists); eager above-the-fold (profile header) to avoid a pop"
  - "AvatarGroup overlap (negative margin-inline-start + ring-stroke + z-index) + the '+N' counter (total-max static, or ResizeObserver responsive — JS not CSS, like Tag's '+N more'); hidden avatars in a popover/list on demand"
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
    - "fallback timing: naive <img>+onError-swap vs fallback-as-default + image-on-top-revealed-on-load (the SSR/flash-safe pattern — the practice default)"
    - "initials count (1 vs 2) + the name-order/CJK/RTL derivation"
    - "shape: circle-for-everything vs square-for-orgs (entity-type signal)"
    - "color-from-name on by default vs off (decorative but contrast-risky)"
    - "group naming: AvatarGroup (practice default) vs AvatarStack (Primer) vs Avatar.Group (Ant)"
  trap:
    - "the onError swap dropping the alt (fallback loses the accessible name)"
    - "SSR shipping the broken-image state (onError never fires on the server) + the flash-of-broken-image"
    - "the presence dot clipped by the avatar's overflow:hidden (needs a non-clipping wrapper)"
    - "initials failing contrast against a name-hashed background color (1.4.3)"
    - "relying on color-from-name to distinguish people (1.4.1) / announcing the name twice (avatar not decorative when adjacent)"
    - "object-fit:fill distorting faces; a face-pile read as N separate images instead of a group+count"
  inherited:
    - "Icon (the fallback placeholder) + Skeleton (the loading state)"
    - "the Badge presence-dot overlay substrate + its text-equivalent/color contract (Avatar is the host)"
  role-in-family: "a Foundations primitive — the person/entity identity surface; stands on Icon+Skeleton, hosts Badge's PresenceBadge, hosted by Tag/Combobox tokens + list/comment/nav; the inverse of Icon's decorative-by-default a11y"
  evolution:
    - "the fallback-chain hardening (image-on-top-of-fallback, SSR/flash-safe)"
    - "the decorative-when-redundant a11y settling (inverse of Icon)"
    - "color-from-name accessibility scrutiny (contrast + not-sole-differentiator)"
    - "AvatarGroup overflow convergence ('+N more' + group-name+count, paralleling Tag/Badge)"
    - "the square-for-orgs entity-type convention"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "the per-system initials algorithms + the color-hash palettes — verify against current implementations"
```
