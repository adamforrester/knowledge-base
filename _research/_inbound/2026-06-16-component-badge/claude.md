# Badge — field-truth study (Claude pass)

## 1. Framing
A Badge is a **small, non-interactive indicator** that annotates a host or a piece of content with a tiny quantum of state. The headline problem is that **"Badge" names three different components** across the field, and the practice has to resolve the genre split before anything else:
- **The count badge** — a number overlaid on a host (a notification bell with "3", a tab with "12"). The host is the interactive thing; the count is an annotation on it.
- **The dot badge** — a small filled dot, *no number* (an unread indicator, a "something new here", an avatar **presence** dot). It says "attention/changed" without quantifying.
- **The status / label badge** — a small pill of text indicating state, usually **standalone inline** in a table cell or beside a title ("Active", "Draft", "Beta", "New"). It is not overlaid on a host; it sits in the content flow.

The naming morass is real and is the thing systems most disagree on. **Fluent** is the cleanest: it splits `Badge` (status pill) / `CounterBadge` (count) / `PresenceBadge` (dot). **MUI** and **Ant** use `Badge` to mean *the count/dot overlay on a child*, with the status pill being a different thing (Ant's `Badge status` / `Tag`). **Polaris**, **Chakra**, **Spectrum**, **Carbon** use `Badge` to mean *the standalone status pill*. **Primer** splits again: `Label` (status) / `CounterLabel` (count) / `StateLabel` (issue/PR state). So the same word points at the count overlay in one system and the status pill in the next.

What it **isn't**: a **Tag/Chip** (the interactive, removable token — Badge holds the boundary at *non-interactive, non-removable*; if it has an `×`, an `onClick`, or selection, it's a Tag, not a Badge — Tag not yet briefed; draw the boundary here); a **Toast/Banner** (the transient/persistent *feedback surfaces* — Badge is a passive standing indicator, not an announcement; see toast, banner). Why systems disagree: the genre model and naming, the count-vs-dot-vs-status default, and where the count's meaning lives for a screen reader.

## 2. Anatomy and parts
- **the badge surface** — the small shape: a **count pill** (a rounded-rect/circle holding a number), a **dot** (a filled circle, no content), or a **status pill** (a rounded-rect holding text, optionally a leading icon).
- **the content** — a number (count), nothing (dot), or a short text label (status). Counts cap to a max ("99+"); dots have no visible content (the meaning lives in a text equivalent — §6).
- **the optional leading icon** — status badges may carry a small severity icon (a check/warning/info) so color isn't the sole carrier (inherits Icon — see icon; §6).
- **the host-overlap anchor** — for count/dot badges, the **anchor point** on the host (top-trailing corner of an icon button / avatar / tab), the **offset**, and the **overlap mode** (rectangular host vs circular host — MUI's `overlap`). Standalone status pills have no anchor; they sit inline.
- **(no) interactivity** — there is no focusable, clickable, or removable part. The badge is decorative-plus-text; any interactivity belongs to the host or to a Tag.

## 3. Properties / API
- **`variant`** — `count` / `dot` / `status` (the genre). MUI: `variant="standard" | "dot"`. Fluent: separate components. The practice models one `Badge` with a `variant` axis plus a clear Tag boundary (§10).
- **`content` / `count`** — the number (count) or text (status). Dot has none.
- **`max`** — the count cap; over it renders `{max}+` (MUI default `99` → "99+").
- **`showZero`** — whether a zero count renders or hides (MUI `showZero` default `false` → hide at zero). The default is **hide-at-zero**; `showZero` opts in.
- **`tone` / `severity` / `color`** — the status palette: info / success / warning / error / neutral (Polaris `tone`, Spectrum/Carbon variants). Never the sole carrier (§6).
- **`overlap`** — `rectangular` / `circular` — how the count/dot anchors to the host's shape (MUI `overlap`).
- **`anchorOrigin`** — the corner: `{ vertical: top|bottom, horizontal: left|right }` (MUI). Default top-trailing; flips under RTL (§9).
- **`standalone` vs `overlaid`** — overlaid (positioned on a child host) vs standalone/inline (in content flow). Status pills are standalone; counts/dots are usually overlaid but can be standalone (a count beside a label).
- **`size`** — small / large (Material 3's small-dot vs large-number; §4).
- **the accessible-label wiring** — *not* a styling prop but the load-bearing API surface: the badge does not announce itself; the **host's accessible name** carries the count/dot meaning (§6). A well-designed Badge API exposes a way to set the host's label (or the consumer wires `aria-label` on the host).

## 4. States and variants
- **States:** effectively **none** — Badge is non-interactive, so no hover/focus/active/disabled of its own. The "runtime" axis is **count change** (a count incrementing, a dot appearing/clearing), which is a *content* change, announced via the host (§6), not an interaction state.
- **Variants:**
  - **genre:** count / dot / status(label).
  - **severity / tone** (status): info / success / warning / error / neutral.
  - **placement:** overlaid (anchored to a host corner) vs standalone/inline.
  - **size:** small (dot) / standard (count pill) / status pill; host-relative.
  - **count edge states:** zero (hidden by default / shown via `showZero`), overflow (`{max}+`), dot-on-overflow (some systems collapse a too-large count to a dot).

## 5. Usage guidance
- **Use a count badge** for an unread/pending *quantity* on a host (notifications, messages, cart items). The number must be **actionable and meaningful** — if the exact number doesn't matter, prefer a dot.
- **Use a dot badge** for "something changed / unread / new" where the count is irrelevant or unknown, and for **avatar presence** (online/away — Avatar the host, not yet briefed). Lower visual weight than a count.
- **Use a status badge** for the **state of an entity** in content flow — "Active/Draft/Archived", "Beta/New", "Open/Merged/Closed". Standalone, inline, color+text.
- **Don't use a Badge for:**
  - An **interactive/removable token** → a **Tag/Chip** (filter chips, removable selections, clickable categories). The boundary: a Badge has no `onClick`, no `×`, no selected state. (Tag not yet briefed.)
  - A **feedback announcement** → a **Toast** (transient) or **Banner** (persistent) — see toast, banner. A Badge is a standing indicator, not an event.
  - A **call to action** → a Button. A badge is read, not actioned.
- **Decision frameworks:**
  - **Count vs dot:** does the exact number carry information the user will act on? Yes → count; no → dot. (A "47 unread" inbox count is actionable; a "new content available" indicator is a dot.)
  - **Overlaid vs standalone:** is it annotating an interactive host (icon button/avatar/tab) → overlaid; is it describing an entity in the content → standalone status pill.
  - **The count-in-the-host-name rule (the load-bearing one):** the count belongs in the *host's* accessible name, never a floating "3" (§6).

## 6. Accessibility
**The announcement contract is the crux.** A count/dot badge is **not a standalone focusable element**, and its meaning must reach a screen reader through the **host's accessible name**, not as an isolated number:
- **The visual badge is `aria-hidden="true"`.** A screen reader landing on a bell that just says "3" is meaningless. So the visual count/dot is hidden from AT, and the **host carries an `aria-label`** that folds the count in: `aria-label="Notifications, 3 unread"`. The number is *described in context*, not read in isolation.
- **A dot needs a text equivalent.** A dot has no content, so the host's accessible name carries it: `aria-label="Messages, unread"` / `"Jane Doe, online"`. The dot itself is `aria-hidden`.
- **A dynamically-changing count uses a status live region.** When a count changes while the user is on the page (notifications incrementing), announce the change via a polite **`role="status"` / `aria-live="polite"`** region ("3 new notifications") — the same live-region pattern Toast established (see toast). Don't make the user re-navigate to the host to discover the change. Polite, not assertive — a count tick is not an interruption.
- **The standalone status pill announces its text.** A status pill is *content*, so it is **not** `aria-hidden` — its text ("Draft") is read in flow. If its meaning is color-coded (severity), the text must still stand alone (§ color-not-sole-carrier).
- **Color is never the sole carrier (WCAG 1.4.1 Use of Color).** A red status badge alone fails for color-blind users — severity must pair **color + text** (and optionally an icon/shape; inherits the Banner/Toast severity model — see banner, toast). info/success/warning/error/neutral each read as text, not just hue.
- **WCAG SCs:** **1.4.1 Use of Color** (severity not color-alone), **1.4.3 Contrast** (the badge text/background and the badge-against-host edge — a count pill on a busy host needs a separating stroke/halo), **4.1.2 Name Role Value** (the host's name folds the count), **4.1.3 Status Messages** (the dynamic-count live region). The badge has **no role of its own** when overlaid (it's `aria-hidden`); the standalone status pill is just text (no special role needed — don't invent `role="status"` for a static pill).

## 7. Content guidelines
- **The count cap** — cap large counts ("99+", "9+") so the pill stays small and the number stays scannable; the exact value above the cap rarely matters. Pick the cap to fit the pill width (single-host bells often "9+"; inboxes "99+").
- **Zero handling** — **hide at zero** by default (no badge = nothing pending); show zero only when "0" is itself meaningful (a deliberate `showZero`). Don't render an empty pill.
- **The status label** — short, clear, a single state word or two ("Active", "In review", "Beta"). Title case or sentence case per the system; consistent across the set. Don't put sentences in a badge.
- **The dot's hidden text** — every dot needs a text equivalent in the host's name ("unread", "online"); a silent dot is invisible to AT.
- **No color-only** — never rely on the badge color alone to convey severity; the text must carry it.
- **Don't overload** — one badge per host; don't stack a count and a dot and a status on one element. A badge is a single small signal.

## 8. Motion and transition
- **Minimal by design.** A count appearing or incrementing can use a brief scale/fade (MUI's badge transition); an attention dot may **pulse** sparingly. Motion is decorative reinforcement, never the carrier of meaning.
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops the pulse/scale to an instant appearance. The badge's information is the number/dot/text, not the motion, so dropping animation loses nothing (the easy case, like Skeleton — see skeleton).
- **Don't animate persistently** — a constantly-pulsing dot is a distraction and an accessibility problem; reserve pulse for genuine "act now" and keep it short or one-shot.

## 9. Internationalization
- **RTL flips the overlay anchor.** A top-**trailing** count badge sits top-right in LTR and **top-left in RTL** — anchor to logical (inline-start/end) corners, not physical left/right, so the flip is automatic (the same logical-property discipline the overlay substrate uses).
- **Number formatting** — counts run through `Intl.NumberFormat` for locale digits and grouping (Eastern Arabic numerals, grouping separators). The cap glyph ("+") and its position may localize.
- **Status label expansion** — translated status labels can be 30–50% longer ("Draft" → a longer word); the pill must grow, not clip or truncate the state word.
- **Dot neutrality** — a dot carries no text, so it's locale-neutral visually; its **text equivalent** (in the host name) must be translated.

## 10. Naming
- **The field set:** Fluent `Badge` / `CounterBadge` / `PresenceBadge`; Primer `Label` / `CounterLabel` / `StateLabel`; MUI/Ant `Badge` (= count/dot overlay); Polaris/Chakra/Spectrum/Carbon `Badge` (= status pill); Carbon also uses `Tag` with a status/notification dot; Material 3 `Badge` (small-dot vs large-number).
- **The practice's default:** one **`Badge`** component with a **`variant`** axis (`count` / `dot` / `status`) rather than three top-level names — the genres share a surface (small, non-interactive, color+text indicator) and differ by content and placement, which a variant models cleanly. Reserve the option to alias `CounterBadge`/`PresenceBadge` as thin presets if a consuming team wants Fluent-style explicitness, but the canonical is one `Badge`.
- **The Badge-vs-Tag disambiguation (the load-bearing naming call):** **Badge = non-interactive, non-removable indicator**; **Tag/Chip = interactive/removable token**. If it has an `onClick`, an `×`/dismiss, or a selected state, it is a **Tag**, not a Badge — regardless of what a vendor library calls it. This boundary is the thing that keeps the two components from collapsing into one over-propped blob. (Tag not yet briefed; this is the boundary it will inherit.)
- **Aliases:** Chip (→ Tag), Pill (→ status Badge or Tag depending on interactivity), Label (Primer's status word), Indicator, Counter, Notification dot.

## 11. Implementation notes
- **Host-overlap positioning** — the overlaid count/dot is `position: absolute` against a `position: relative` host wrapper, anchored to a **logical** corner (inset-block-start / inset-inline-end) so RTL flips for free (§9). `overlap` adjusts the offset for circular hosts (avatars) vs rectangular (icon buttons) so the badge sits on the visual edge, not floating off the corner.
- **Host clipping** — the host (or an ancestor) with `overflow: hidden` will clip a badge that extends past the host's box; the badge wrapper must not clip, or the badge anchors inside the host bounds. A recurring trap: an avatar with `overflow: hidden` (to clip the image to a circle) eats the presence dot — the dot must live on a non-clipping wrapper.
- **The count-in-the-aria-label wiring** — the host gets the composed `aria-label` ("Notifications, 3 unread"); the visual badge is `aria-hidden`. A headless Badge can't know the host's label, so the API must let the consumer supply it (or the Badge renders a visually-hidden text node the host's label references).
- **The dynamic-count live region** — a single polite `role="status"` region announces count changes; reuse one app-level region rather than one per badge (the pre-existing-region discipline from the Feedback live-region pattern — see toast). Debounce rapid increments so AT isn't flooded.
- **The max-cap / zero logic** — `count > max ? \`${max}+\` : count`; `count === 0 && !showZero ? render nothing : render`. Keep it in the component, not the consumer.
- **Contrast against the host** — a count pill overlaps host pixels; a separating stroke/halo (a host-colored ring) keeps the 1.4.3 edge contrast on busy hosts.
- **Headless vs opinionated** — the positioning/overlap/RTL and the aria wiring are the substrate worth owning; the palette and shape are theme. Most systems ship opinionated (MUI/Ant/Fluent) because the positioning math is the value.

## 12. Related and alternative components
- **Inherits / stands on:** **Icon** (the optional status-severity icon + the icon-button count host — see icon).
- **Inherits (pattern):** the **color-not-sole-carrier severity model** from the Feedback family (info/success/warning/error/neutral as color+text — see banner, toast); the **live-region announcement pattern** from Toast for the dynamic-count change (see toast).
- **Overlaid on (hosts):** Icon buttons, **Avatar** (the presence-dot host — not yet briefed), **Tabs** (a count on a tab — see tabs), nav items (a count on a side-nav item — see side-navigation).
- **Boundary:** **Tag/Chip** — the interactive/removable token (Badge is the non-interactive indicator; Tag not yet briefed; this brief draws the boundary).
- **Not:** **Toast** (transient feedback — see toast), **Banner** (persistent feedback — see banner). Badge is a passive standing indicator.

## 13. Field POV evolution
- **The tripartite split surfacing in naming.** Fluent's `Badge`/`CounterBadge`/`PresenceBadge` and Primer's `Label`/`CounterLabel`/`StateLabel` show the field separating the three genres explicitly rather than overloading one `Badge`. The practice keeps one component with a `variant` axis but acknowledges the genres are genuinely distinct.
- **The count-in-the-host-name a11y settling.** The field has converged on *the count's meaning belongs in the host's accessible name, the visual badge is `aria-hidden`* — away from the older pattern of a screen reader reading a bare "3". The dynamic-count `role="status"` live region is the newer refinement (4.1.3 Status Messages).
- **The color-not-sole-carrier hardening.** Status-badge severity pairing color with text/icon (not hue alone) is now table stakes (WCAG 1.4.1), aligned with the Feedback severity model.
- **The Badge-vs-Tag clarification.** Systems increasingly separate the non-interactive indicator (Badge/Label) from the interactive/removable token (Tag/Chip), reversing the earlier tendency to pile dismiss/click behavior onto a "badge".

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- Microsoft Fluent UI — `Badge` / `CounterBadge` / `PresenceBadge` (the tripartite split).
- MUI — `Badge` (count/dot overlay; `badgeContent` / `max` / `showZero` / `variant="dot"` / `overlap` / `anchorOrigin`).
- Ant Design — `Badge` (count / dot / status; `Ribbon`; standalone).
- Shopify Polaris — `Badge` (`tone`, progress; the status indicator).
- GitHub Primer — `Label` / `CounterLabel` / `StateLabel`.
- Adobe Spectrum — `Badge` (label/status).
- IBM Carbon — `Tag` with status + the notification dot.
- Chakra UI — `Badge` (status label).
- Google Material 3 — `Badge` (small dot vs large number).
- Base Web (Uber) — `Badge`.
- WAI-ARIA APG — no formal badge pattern; the accessible-name-on-host + `role="status"` + `aria-hidden` visual.
- WCAG 2.2 — 1.4.1, 1.4.3, 4.1.2, 4.1.3.

## 15. Agent-consumable schema
```yaml
identity:
  id: badge
  name: Badge
  aliases: [CounterBadge, PresenceBadge, Label, CounterLabel, StateLabel, Counter, Notification dot, Pill, Indicator]
  category: foundations
  status: stable
description: >
  A small, non-interactive indicator annotating a host or content with a quantum
  of state, across three genres: a count (a number overlaid on a host), a dot
  (a contentless attention/presence indicator), and a status/label pill (standalone
  inline state text). Non-interactive and non-removable — the boundary with Tag/Chip
  (interactive/removable). Not a Toast/Banner (the feedback surfaces). The headline
  problem is the genre split + the naming morass: "Badge" means the count/dot overlay
  in MUI/Ant, the status pill in Polaris/Chakra/Spectrum, and is split three ways in
  Fluent/Primer.
api:
  inherits:
    - icon            # optional status-severity icon + icon-button count host
    - banner/toast    # color-not-sole-carrier severity model (pattern)
    - toast           # live-region pattern for dynamic-count announcement (pattern)
  props:
    - name: variant
      type: "'count' | 'dot' | 'status'"
      default: count
      required: false
      description: The genre — number overlay / contentless dot / standalone status pill.
    - name: content
      type: number | string
      default: ~
      required: false
      description: The count (number) or status text. Dot has none.
    - name: max
      type: number
      default: 99
      required: false
      description: Count cap; over it renders `{max}+`.
    - name: showZero
      type: boolean
      default: false
      required: false
      description: Render a zero count. Default hides at zero.
    - name: tone
      type: "'info' | 'success' | 'warning' | 'error' | 'neutral'"
      default: neutral
      required: false
      description: Severity palette (status). Color paired with text/icon, never color alone.
    - name: overlap
      type: "'rectangular' | 'circular'"
      default: rectangular
      required: false
      description: How an overlaid count/dot anchors to the host's shape.
    - name: anchorOrigin
      type: "{ vertical: 'top'|'bottom', horizontal: 'left'|'right' }"
      default: "{ top, right }"
      required: false
      description: The overlay corner. Logical under RTL (flips to top-leading).
    - name: placement
      type: "'overlaid' | 'standalone'"
      default: overlaid
      required: false
      description: Anchored to a host vs inline in content flow (status pills are standalone).
    - name: size
      type: "'small' | 'large'"
      default: small
      required: false
      description: Dot vs count-pill vs status-pill; host-relative.
    - name: host-accessible-name
      type: wiring
      default: ~
      required: true
      description: >
        Not a style prop — the count/dot meaning lives in the HOST's aria-label
        ("Notifications, 3 unread"), not the badge. The API must let the consumer
        supply/compose it.
states:
  runtime: []          # non-interactive; no hover/focus/active/disabled of its own
  content-change: [count-increment, dot-appear, dot-clear]   # announced via host, not an interaction state
variants:
  genre: [count, dot, status]
  tone: [info, success, warning, error, neutral]
  placement: [overlaid, standalone]
  size: [small, large]
  count-edge: [zero-hidden, zero-shown, overflow-cap, dot-on-overflow]
accessibility:
  inherits:
    - banner/toast    # color-not-sole-carrier severity
    - toast           # live-region announcement
  wcag-criteria: ["1.4.1", "1.4.3", "4.1.2", "4.1.3"]
  aria-attributes:
    overlaid-badge: aria-hidden="true"        # the visual count/dot is hidden from AT
    host: aria-label folds the count/dot ("Notifications, 3 unread" / "Jane Doe, online")
    dynamic-count: role="status" aria-live="polite" announces count changes
    status-pill: not aria-hidden — its text is content, read in flow
  keyboard-model: none      # non-interactive, not focusable
  focus-behavior: none      # focus belongs to the host (icon button / tab / nav item)
content:
  count-pattern: cap large counts ("99+"/"9+"); the exact value above the cap rarely matters
  zero-pattern: hide at zero by default; showZero only when "0" is itself meaningful
  status-pattern: short clear state word ("Active"/"Draft"/"Beta"); consistent across the set
  dot-pattern: every dot has a text equivalent in the host's accessible name ("unread"/"online")
  color-rule: severity is color + text (+ optional icon), never color alone
  trap: don't stack count+dot+status on one host; one signal per badge
motion:
  enter: brief scale/fade on count appear/increment; sparing dot pulse for genuine "act now"
  reduce-motion: drop pulse/scale to instant appearance — the number/dot/text is the cue, not the motion
  note: never animate persistently; pulse is one-shot/short
i18n:
  rtl: overlay anchor flips to top-leading via logical inset properties (not physical left/right)
  number-formatting: counts via Intl.NumberFormat (locale digits/grouping); cap glyph may localize
  label-expansion: translated status labels run 30–50% longer — the pill grows, never clips the state word
  dot-neutrality: the dot is locale-neutral visually; its text equivalent must be translated
implementation:
  overlay-positioning: absolute against a relative host wrapper; logical-corner anchor; overlap offset for circular vs rectangular hosts
  host-clipping: a host/ancestor with overflow:hidden clips the badge (the avatar-presence-dot trap) — anchor on a non-clipping wrapper
  aria-wiring: host carries the composed aria-label; visual badge aria-hidden; headless badge can't know the host label so the API supplies it
  live-region: one shared app-level polite role=status for dynamic counts (the pre-existing-region discipline); debounce rapid increments
  count-logic: count>max ? `${max}+` : count; count===0 && !showZero ? render nothing
  contrast: separating stroke/halo against busy hosts for the 1.4.3 edge
  headless-vs-opinionated: positioning/overlap/RTL + aria wiring is the substrate; palette/shape is theme — most systems ship opinionated
composition:
  composes-with: [icon, avatar, tabs, side-navigation]   # the count/dot hosts
  alternative-to: [tag, toast, banner]                   # tag (interactive boundary), toast/banner (feedback surfaces)
  supersedes: null
  superseded-by: null
notes:
  contested:
    - One Badge with a variant axis vs three components (Fluent/Primer split) — the practice picks one Badge + variant, with optional CounterBadge/PresenceBadge presets.
    - Dot-on-overflow (collapse a too-large count to a dot) vs always-cap ("99+") — system-dependent.
    - showZero default — the field hides at zero; show only when 0 is meaningful.
  trap:
    - The floating bare "3" — a screen reader reading the count in isolation; the count must live in the host's accessible name.
    - The avatar overflow:hidden clipping the presence dot.
    - Color-as-sole-carrier severity (WCAG 1.4.1 failure).
  inherited:
    - color-not-sole-carrier severity (banner/toast)
    - the live-region announcement pattern (toast)
    - Icon (the status-severity icon + count host)
  evolution:
    - The tripartite genre split surfacing in naming (Fluent/Primer).
    - The count-in-the-host-name a11y settling + the dynamic-count role=status refinement.
    - The Badge-vs-Tag clarification (non-interactive indicator vs interactive/removable token).
  unverified:
    - External-pass library version dates pending reconciliation against the external-agent pass.
```
