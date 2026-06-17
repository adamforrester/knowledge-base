You are researching the Avatar component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what an avatar
is, knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Avatar is a Foundations primitive — the visual representation of a person
or entity (a user, an org/team, a bot). It STANDS ON substrates and is the
HOST for two components already briefed:
- THE FALLBACK PLACEHOLDER ICON inherits ICON (components/icon.md), and the
  IMAGE-LOADING STATE inherits SKELETON (components/skeleton.md — a circular
  skeleton while the image loads). Don't re-derive Icon or Skeleton.
- AVATAR IS THE PRESENCE-DOT HOST that Badge's PresenceBadge composes
  (components/badge.md): the presence/status dot (online/away/busy) is a
  Badge overlaid on the Avatar — and Badge named THE TRAP here: a circular
  Avatar with overflow:hidden (masking its image) CLIPS the presence dot
  unless the dot lives on a non-clipping wrapper. Resolve this from the
  Avatar (host) side.
- AVATAR IS HOSTED BY Tag (Primer's AvatarToken — a person token; see
  components/tag.md) and the multi-select Combobox tokens, list items,
  comments, and nav.

THE DEFINING AVATAR-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE FALLBACK CHAIN (the headline): image → initials → generic
  icon/placeholder. The graceful-degradation contract when the image is
  missing or fails to load (the onError swap), the loading state (a
  Skeleton placeholder, not a layout jump), and the precedence order. This
  is THE defining Avatar problem and where implementations most diverge
  (eager vs lazy onError, the flash-of-broken-image, SSR).
- THE ACCESSIBLE-NAME CONTRACT (the accessibility crux): what does an
  avatar announce? Resolve the informative-vs-decorative decision — an
  avatar carrying the ONLY identity (a bare avatar) needs the person's name
  as its accessible name (img alt = "Jane Doe"); an avatar ADJACENT TO a
  visible name (a list row, a comment header) is REDUNDANT and should be
  decorative (empty alt / aria-hidden) so the name isn't announced twice.
  And the fallback must PRESERVE the name (initials/icon still expose "Jane
  Doe", not "JD" or "person icon"). This is the inverse of Icon's
  decorative-by-default (avatars are often informative) — resolve the rule.
- THE AVATAR GROUP / FACE-PILE (parallels Tag's "+N more" overflow and
  Badge's count cap): the overlapping stack (the overlap offset, the
  z-index/ring-stroke separation echoing Badge's cutout, the
  left-vs-right stacking), the "+N more" overflow (maxCount/total/the
  surplus counter), and the GROUP's accessible name ("5 collaborators",
  announcing the count — NOT reading N separate images). Resolve the
  group model.
- INITIALS GENERATION + COLOR-FROM-NAME — the algorithm (1 vs 2 initials,
  first+last, single-word names, the non-Latin/CJK family-name-first and
  Arabic-RTL name-order problem), and the deterministic background color
  hashed from the name (decorative identity, NOT meaning — the contrast
  requirement on the initials, and the rule that color must never be the
  sole differentiator between people, WCAG 1.4.1).
- SHAPE + ENTITY TYPE — circle (the person default) vs rounded-square/square
  (often the org/team/entity convention); the person-vs-organization-vs-bot
  distinction; the shape's effect on the presence-dot anchor and the
  AvatarGroup ring.
- SIZING — the size scale (xs/sm/md/lg/xl), the token mapping, the
  host-relative sizing (an avatar in a Tag token vs a profile header), and
  how initials/icon scale with it.
- IMAGE HANDLING — object-fit: cover (never distort), the srcset/responsive
  + DPR concern, lazy-loading, and the broken-image / load-error handling
  that feeds the fallback chain.

Field-leader systems to survey (web): MUI (Avatar — image/letter/icon
fallback, variant circular/rounded/square, AvatarGroup max/total/surplus,
Badge for presence), Ant Design (Avatar — src/srcSet/icon/children, shape,
size, Avatar.Group maxCount/maxPopover), Chakra UI (Avatar — name→initials
via getInitials, AvatarBadge for presence, AvatarGroup max, the
color-from-name), Microsoft Fluent (Avatar / Persona — initials, the
name-derived color, PresenceBadge, AvatarGroup), GitHub Primer (Avatar /
AvatarStack / AvatarToken — the square-for-orgs convention), Shopify
Polaris (Avatar — initials, customer vs business, size), Adobe Spectrum /
React Aria (Avatar — the minimal img-with-alt primitive), IBM Carbon
(UserAvatar / the avatar pattern), Atlassian (Avatar / AvatarGroup /
AvatarItem — presence + status, the borderlessness), Base Web (Uber)
(Avatar). WAI-ARIA / HTML (the img alt contract; no formal avatar pattern;
decorative-vs-informative img). Mobile reference where relevant. Cite each
with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Icon fallback + the Skeleton
loading state, and note the Badge/PresenceBadge presence-dot composition
(Avatar is the host) and the Tag/Combobox token hosting; flag unverified
claims under notes.unverified).

1. Framing — what it is (the person/entity representation, the fallback
   chain, the presence-dot host) and what it isn't (an Icon, a generic
   Image); the fallback chain + the accessible-name contract + the
   group/face-pile up front; why systems disagree.
2. Anatomy and parts — the image, the initials fallback, the icon
   placeholder, the shape/mask, the presence-dot anchor (the Badge host),
   the AvatarGroup ring/stroke; the loading skeleton.
3. Properties / API — src/srcSet, name (→ initials + accessible name),
   alt/decorative, icon (fallback), shape, size, variant, the
   presence/status slot, AvatarGroup max/total, the color-from-name.
4. States and variants — image / initials / icon fallback; loading;
   shape (circle/square); size scale; with-presence; the group/stacked;
   entity type (person/org/bot).
5. Usage guidance — Avatar (identity) vs Icon (a symbol) vs Image (generic
   media); when initials vs icon fallback; the decorative-when-adjacent-to-
   a-name rule; the AvatarGroup vs a list; presence-dot when.
6. Accessibility — the accessible-name contract (informative bare avatar =
   the name; decorative-when-redundant = empty alt/aria-hidden; the
   fallback preserves the name), the AvatarGroup group-name + count (not N
   images), the presence-dot text equivalent (inherits Badge's contract),
   color-from-name not-sole-carrier, WCAG SCs (1.1.1, 1.4.1, 1.4.3, 4.1.2).
7. Content guidelines — the name source, the initials rules (1 vs 2,
   name-order), the alt-text pattern, the group "+N" label, no-PII-leak.
8. Motion and transition — the image fade-in on load (over the skeleton),
   the group hover-expand/spread, reduce-motion.
9. Internationalization — initials for non-Latin/CJK (family-name-first)
   and Arabic, the name-order problem, RTL group stacking direction, the
   color-from-name across scripts.
10. Naming — Avatar / Persona / UserAvatar / Gravatar; the group
    (AvatarGroup / AvatarStack / Avatar.Group); the entity-type naming;
    aliases.
11. Implementation notes — the fallback-chain onError + the
    flash-of-broken-image + SSR (no onError on the server) trap, the
    presence-dot overflow:hidden clipping trap (Badge named it — the
    non-clipping wrapper), the initials algorithm + the deterministic
    color hash, object-fit: cover, lazy-load, the AvatarGroup overlap +
    overflow counter + ResizeObserver, the loading Skeleton, headless vs
    opinionated.
12. Related and alternative components — typed relationships (Icon fallback
    + Skeleton loading substrates, Badge/PresenceBadge the presence-dot
    composition (Avatar is the host), Tag's AvatarToken + Combobox tokens +
    list/comment/nav hosts, Image the generic-media boundary).
13. Field POV evolution — recent shifts (the fallback-chain hardening, the
    decorative-when-redundant a11y settling, the color-from-name
    accessibility scrutiny, the AvatarGroup overflow convergence, the
    square-for-orgs convention).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what an avatar is — explain the
fallback chain (image → initials → icon, the onError/SSR/flash traps), the
accessible-name contract (informative bare avatar = the name vs decorative-
when-adjacent-to-a-visible-name; the fallback preserves the name), the
AvatarGroup face-pile (the overlap + "+N more" overflow + the group-name-
and-count), the initials-generation + color-from-name (the name-order/CJK/
RTL problem + color-not-sole-carrier), the presence-dot host contract
(Avatar hosts Badge's PresenceBadge + the overflow:hidden clipping trap),
and the shape/entity-type + sizing that field leaders still diverge on.
