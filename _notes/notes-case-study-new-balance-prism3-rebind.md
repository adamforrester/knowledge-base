# Case study — New Balance: rebinding an existing Figma file onto Prism3 (October 2026)

Private working note. Client-identifying; nothing here goes into the Prism3 repository. The brand-agnostic
method lives in Prism3 as the `prism3-rebind` skill and its never-detach decision (docs/46); this note is
the story behind them and the client specifics.

## The engagement in one paragraph

We took a disposable copy of the New Balance Stance design-system master file, where Prism3 had already
been materialized as local variables, text styles and components, and moved the product screens on its
"Testing (Update Here)" page off the legacy NB library and onto Prism3. The page held six sections
(Wishlist ×3, Launch Calendar, Minibag, Log In). A protected copy of the original screens sat on a
"DO NOT TOUCH" backup page. The work ran over three days (October 6–8, 2026) through the Figma Console MCP
desktop bridge, because the cloud runtime couldn't load the brand fonts (Suisse Int'l and ITC Garamond Std).
The point was not a pixel-perfect migration. It was to prove that Prism3 bindings and component swaps hold
up on real product UI, and to find every gap, in values and in components, before the NB library ships.

## What we did

- **A read-only mapping pass first.** Every value on the page went into one master table of colors (C1–C35),
  type (T1–T21) and spacing/radius/stroke (S, R, B), each with a confidence. Fifteen owner questions came out
  of it before anything was written. About 250k tokens.
- **Log In: all eight screens.** The rest got **one representative screen per pattern**, by owner direction
  once it was clear that similar screens add nothing: Wishlist add-to-wishlist (both), Filter & Sort (mobile
  drawer, mobile filter-applied), Minibag (mobile, unauthenticated), Launch Calendar (mobile image hero).
- **Final state of 14 rebuilt screens: 0 remote variables, 0 remote styles, 0 remote instances; 5,656 Prism3
  bindings; 274 attached Prism3 component instances.** The backup page was fingerprinted before every
  section's first write and checked at the end.

## The moment that defined the method

The first Log In pass rebuilt the form fields as plain frames bound to Prism3 variables, because Prism3's
`text-field` input is 16px and the NB design's is 12px. It looked closer, and it taught nothing. The owner
stopped it the same day: **never detach a Prism3 component to match a design; place it attached and list
the differences.** Re-placed as attached `text-field` instances, the fields produced a measured list of
differences (label 14 vs 10px, a 4 vs 8px gap, padding, input size, a missing "focused with a value" state,
an input box that hugs at 320 instead of filling its column) that became filed component work. That's the
whole argument in miniature: a lookalike frame closes the visual gap and hides the system gap. This is the
same principle as the vault's view on detachment rates (See 12-figma-practice): fix the component.

The owner then added a second rule that kept the gap list honest: **sort every difference** into a Prism3
improvement (keep it), a Prism3 gap (file it), or brand-only (NB's library or settings). And check the
**settings first**. Three apparent gaps turned out to be existing levers: button minimum width, button label
weight, radius.

## The near-miss

The Log In screens on the work page were **main components**, and the backup page's Log In screens were
**instances of them**. Editing the work screens in place would have rewritten the protected backup through
component propagation. We caught it in the read-only inventory, rebuilt detached copies instead, and parked
the untouched mains in a hidden, locked frame, which is still the backup's source today. The lesson for any
client file: ask what renders a node elsewhere before writing to it.

## Owner decisions that shaped NB (the brand-specific record)

- Q61 A: 12px body → `caption/lg`. Revisit with the 12px `body/xs` coming in #2266.
- Q62: off-palette grays (#4B4B4B, #444344, and a stacked "Grey - 50" style that renders about #4C4C4C)
  → `text/secondary` #6A6868. 54 runs logged for review; Prism3 reads lighter than NB's grays.
- Q63: error → danger roles; visibly brighter red.
- Q64 B, superseded the same day by the never-detach rule: fields are attached `text-field` instances.
- Q65: navigation is link-styled text; real actions are text buttons (36px, Medium, no underline).
- Urgency ("Selling fast"): kept as text, bound to `text/warning`. NB's #AC5C00 only scrapes 4.57:1 on the
  #F7F7F7 product ground; Prism3's #7E5300 is 6.27:1 and browner. The value should move toward NB's orange
  while keeping margin (#2346).
- Semibold and Garamond Bold Condensed overrides → our existing styles and weights. Neither weight was
  installed; the license question is open.
- Row heights (47px radio/checkbox rows) kept as a hit-target improvement. Veil 70% accepted. Close buttons
  are `icon-button`.
- **NB-only, for NB's own library:** the flat 24px filter chip, blur effects (glass card footers, sticky bars),
  a checkout button with a price slot.

The operational checklist of settings to change in the NB master file lives in the owner's notes app, not
here.

## Gaps filed in Prism3 (scrubbed of client identifiers)

#2292 field input boxes hug at 320 (and the checkbox/radio-row floor) · #2315 blur (DTCG/Style Dictionary
spike first) · #2318 focused-with-a-value state · #2319 ordered/unordered list · #2340 strikethrough ·
#2342 icons (social, payment, edit, menu) · #2343 social and payment buttons (provider specs rule) · #2344
radio/checkbox-group up to ~8 rows (Prism2 parity) · #2345 image-placeholder ratios and behavior (NB's
imagery is mostly portrait: 3:4, 4:5, 2:3, none supported) · #2346 `text/warning` value · #2347 the
missing-components backlog (tabs, sheet, accordion, banner, segmented control, stepper, carousel, code
input). The `prism3-rebind` skill and docs/46 shipped as a Prism3 PR.

## What it cost, and where the time went

The mapping pass and pilot preparation took about 490k tokens before a single write. Once the runner was
stable, each screen rebuilt in 1–2 seconds; a 514-node, 12,800px screen took 1.6s. Nearly all the elapsed
time went into decisions and gap triage, which is the right place for it. The real time sinks were the
traps, each costing a rerun or a bad screenshot before it was understood:
- the bridge runtime has no `createAutoLayout`;
- bound paints rendered their placeholder color;
- mixed text kept stale remote bindings;
- remote grid styles counted as rogue bindings;
- an uninstalled font took ~24s to fail to load and timed out whole runs;
- `swapComponent` carried the legacy overrides into Prism3 instances;
- a whole-screen hash flagged a hidden layer Figma had re-laid out.

All of them are now in the skill.

## What we'd tell the next client team

**Treat the rebind as a component audit that happens to rebind the file.** The deliverable that mattered was
the measured difference table and the issues it produced, not the 5,656 bindings. **Do one screen per
pattern**, not every screen. **Protect the original by fingerprint, not by trust**, and fingerprint what's
visible. And **settle the brand settings before calling anything a gap**: three of our "gaps" turned out to be existing levers.
