# Tooltip — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/tooltip.md`; version numbers (incl. a stale-looking Radix figure) and the inherited CSS-anchor/Popover-API platform-state flagged unverified. The two passes converged almost completely — no substantive disagreement.*

---

Field-Truth Study: Tooltip Component Architecture

## 1. Framing
The Tooltip is the cleanest, most specialized closure to the overlay arc — a restrictive specialization of Popover. It stands entirely on the Popover substrate (anchored surface, viewport-aware positioning via CSS Anchor Positioning, top layer, origin-aware motion); its definition is found not in how it is positioned but in its severe behavioural and content constraints. It diverges via one sharp restriction: content composition — short, non-interactive text tied to a focusable, interactive trigger. Governed by WCAG 1.4.13 (dismissable without moving the pointer, hoverable without vanishing, persistent until focus/pointer leaves). The defining reality: touch devices lack a hover state, so tooltips are invisible/inaccessible on touch — a tooltip must NEVER contain essential, workflow-critical information. popover="hint" creates a subordinate ephemeral stack so a tooltip renders without force-closing an active auto popover (menu). Ideological divergence: Material 3's "Plain vs Rich Tooltips" (rich allows subheads/buttons/links) is rejected by Carbon/Polaris/Primer/WAI-ARIA — interactive elements in a hover/focus surface create a keyboard trap; interactivity escalates to Popover or Toggletip.

## 2. Anatomy and Parts
Trigger (button/a/input; MUST be focusable — tooltip on a div/p/span is inaccessible). Surface (top-layer div, role="tooltip", ideally popover="hint"; portaled/Top Layer to escape z-index/overflow clipping; re-related via ARIA). Content (plain text, zero interactive children; drives fluid dimensions; high-contrast small type e.g. Carbon $text-inverse/$background-inverse). Arrow/Caret (geometric connector; updates with Popover collision math — inverts on flip).

## 3. Properties / API
Timing/Delay: delay/delayDuration/openDelay (warm-up, React Aria 1500ms, Radix 700ms); closeDelay/hideTimeout (cool-down 300-500ms, allows transit to surface); skipDelayDuration (300ms global window where siblings open instantly); disableHoverableContent (escape hatch disabling 1.4.13 pointer tracking on the surface). Accessible wiring: aria-describedby (default — supplementary, trigger has its own label; "Submit, button" + tooltip); aria-labelledby (the tooltip IS the name — standalone icon; Primer type="label" switches the wiring).

## 4. States and Variants
Hidden (unmounted — shouldn't exist in DOM until warm-up; SSR uses display:none/hidden). Delayed-Open (timer counting, DOM unaffected). Showing (mounted; while trigger focused / pointer on trigger / pointer transited onto surface). Closing (cool-down; re-entry reverts). Plain vs Rich divergence: Material 3 Rich Tooltip (subheads, supporting text, hyperlinks, up to 2 buttons) categorically rejected — focus leaving the trigger to a child fires onBlur and destroys the surface. Icon-Button Label variant: tooltip is the accessible name; enforce checks against dual-announcement ("Edit, button, Edit") — Primer routes the string to the naming tree.

## 5. Usage Guidance
Never-Essential rule (touch lacks hover). Permitted: icon-only button labels, truncated-data reveal, brief non-critical definitions (definition tooltip, dotted underline). Not permitted: password constraints (-> inline helper aria-describedby), validation errors (-> persistent block aria-live), interactive tertiary actions (-> Toggletip/Popover). Deploy with parsimony. Never on static non-interactive text (keyboard can't focus a span). Polaris/Base Web: avoid "wall of text," 1-2 sentences.

## 6. Accessibility
WCAG 1.4.13: Dismissable (Escape global keydown, no pointer move), Hoverable (pointer can move onto surface — "safe triangle"/hover bridge so mouseleave doesn't unmount if trajectory heads to tooltip; critical for magnifier users), Persistent (no arbitrary setTimeout auto-hide). Focusable trigger requirement (tabindex=0 + role for inline definitions). Disabled-control trap: native disabled removes from a11y tree/tab order/pointer events -> tooltip unreachable; use aria-disabled=true (keeps focus + mouseenter/focus events) + JS suppress onClick/onKeyDown. (Table: <button disabled> anti-pattern; wrapper span fallback; aria-disabled=true industry standard.) Title attribute anti-pattern (unstyleable, vendor-delay, SR-inconsistent, no touch); sanitize to prevent double tooltips.

## 7. Content Guidelines
Plain text only (no links/buttons/rich markup/forms). Brevity (1-2 short sentences, Polaris). Casing: label = noun phrase, no terminal period; descriptive sentence = sentence case + punctuation. No redundancy with the trigger's visible text.

## 8. Motion and Transition
Origin-aware opacity fade + micro-scale (95->100% over 150ms), origin from the Popover engine. Skip-delay siblings bypass the entry animation (instant tracking). prefers-reduced-motion: disable scale, instant or 50ms crossfade.

## 9. Internationalization
RTL: logical properties (start/end) not physical (left/right); bottom-start aligns leading edge in both directions. Text expansion up to 300% (German); max-width cap (Carbon 288px, Atlassian 240px) then wrap; NEVER truncate own content; fluid height.

## 10. Naming
Tooltip: hover/focus, transient, plain text, touch-inaccessible. Toggletip: explicit click/tap/Enter-Space, disclosure pattern, works on touch, aria-expanded + managed focus, can house interactive content. Carbon + a11y practice enforce the distinction; "Tooltip that works on mobile" -> route to Toggletip. "Rich Tooltip" discouraged outside Material.

## 11. Implementation Notes
popover="hint": secondary subordinate top-layer stack for ephemeral UI; renders on top of an open popover="auto" without closing it (eliminates z-index wars / manual portaling). Event model + global timers: PointerEnter (if skipDelay active fire immediately, else setTimeout delayDuration); Focus (bypasses warm-up, mounts instantly for keyboard predictability); MouseLeave/Blur (closeDelay; if pointer enters surface bounds before expiry, clear — satisfies Hoverable). Centralised provider/hook (React Aria useTooltipTriggerState). Headless (Radix/React Aria/Ariakit — Provider/Root/Trigger/Content) vs opinionated (Carbon/Polaris/Atlassian — render prop / HOC enforcing layout + aria wiring).

## 12. Related and Alternative Components
(Table: Tooltip — hover/focus, no touch, no interactive, describedby/labelledby. Toggletip — click/tap/Enter, touch yes, interactive yes, aria-expanded + DOM order. Popover — click/tap/Enter, touch yes, interactive yes, aria-haspopup/expanded. Title attribute — browser default, anti-pattern. Visible text — always visible, the ultimate accessible fallback.) Popover = foundational substrate (top-layer positioning, no content/focus restriction). Toggletip = immediate fallback when touch/interactivity required.

## 13. Field POV Evolution
Eradication of title attribute (now an accessibility failure; sanitized + replaced by ARIA-wired surfaces). WCAG 1.4.13 hardening (abandon CSS :hover for JS state machines tracking intent + hover bridges + Escape). Mobile/touch fork (abandoned long-press hacks that interfere with text selection/context menus; accepted hover is desktop-centric -> never-essential rule + Toggletip bifurcation). Platform substrate popover="hint" (shed heavy JS portal/z-index libs for native top-layer stacks).

## 14. Sources Cited
GitHub Primer (React v38; tooltip a11y rebuild, type="label"). React Aria/Adobe Spectrum (v3.49.0; useTooltipTrigger, delay/closeDelay). Radix UI (TooltipProvider, delayDuration/skipDelayDuration, disableHoverableContent). IBM Carbon (v11, June 2026; Tooltip vs Toggletip, 288px). Google Material 3 (Rich Tooltip divergence). Shopify Polaris (1-2 sentences, interestFor). Atlassian (v22.6.3; 240px, disabled-control/title directives). Ariakit (v0.4.29; timeout/hideTimeout). Microsoft Fluent (disabled-control trap). Base Web (prompted vs unprompted). WAI-ARIA APG (role=tooltip, aria-describedby, 1.4.13). W3C HTML Popover API (Jan 2025; popover="hint"). Apple HIG.

## 15. Agent-Consumable Schema
Component: Tooltip
- Identity: Tooltip; aliases Hint, Data Tooltip (anti-pattern: Rich Tooltip; sibling: Toggletip); inherits Popover (CSS Anchor Positioning, Top Layer); element role="tooltip", <div popover="hint">.
- Description: transient non-interactive overlay, plain text describing an adjacent interactive element, hover/focus only, degrades (vanishes) on touch.
- Anatomy: Trigger (focusable), Surface (role=tooltip top layer), Content (plain text), Arrow (optional).
- API: delay (~700-1500ms), closeDelay (~300-500ms), skipDelayDuration (~300ms), placement (inherited), describedby/labelledby.
- States: hidden, delayed-open, showing (Escape listener active), closing.
- Variants: plain, icon-label (semantic switch to labelledby); Rejections: rich (-> Popover/Toggletip).
- Accessibility: 1.4.13 Dismissible/Hoverable/Persistent; aria-describedby; disabled-control trap -> aria-disabled + JS suppression; touch inaccessible by definition -> never essential info.
- Content: plain text, 1-2 sentences, sentence casing, no trailing punctuation for labels, never duplicates trigger text.
- Motion: fade + micro-scale from origin; instant during skipDelay; prefers-reduced-motion.
- I18n: logical alignments; max-width then wrap (prevents truncation of 300% blooms).
- Implementation: popover="hint" to prevent stacking collisions with auto dropdowns; avoid title attribute universally.
- Composition: composes over Popover positioning; frequently wraps Button (icon-only variant).
