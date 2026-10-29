# Raw findings — option-row control size, label alignment and description styling

Field scan, 2026-10-29. Findings only, recorded as delivered with owner decision Q854 A; sources per row.
Single-sourced — there is no external-agent pass for this run (see `external-agent.md`). Sources were
not re-fetched when this folder was filed.

---

## Per system

**Material 3 Compose.** Checkbox has no label. You compose it in a `Row` with
`verticalAlignment = CenterVertically`.
Source: developer.android.com/develop/ui/compose/components/checkbox

**IBM Carbon.**
- Fixed 16px box; label body-compact-01 at 14px; no size prop.
- `helperText` is helper-text-01 at 12px in `$text-secondary`.
- Top alignment: the box is absolutely positioned 2px from the top, and the label has 1px top padding.
- 6px between items.

Sources: carbondesignsystem.com/components/checkbox/style; carbon repo `_checkbox.scss`, `Checkbox.tsx`.

**Shopify Polaris.**
- Fixed 18px control, 20px at the md breakpoint and below; no size prop.
- `helpText` (React) / `details` (web components), indented by space-200 plus the control size.
- `.Choice` uses `align-items: center`.

Sources: polaris `Choice.module.css`; shopify.dev polaris-web-components checkbox.

**Spectrum 2 / React Spectrum S2.**
- Size S/M/L/XL couples the box (14/16/18/20) with the font (ui-sm/ui/ui-lg/ui-xl).
- `CenterBaseline` centers the box on the label's first line.
- The group's row gap is set per size.

Source: react-spectrum `s2/src/Checkbox.tsx`, `style-utils.ts`.

**Atlassian.** Fixed medium size. The size prop was deprecated in v14 and removed in v15 ("less
accessible"). v12 restored top alignment after an accidental switch to center.
Source: unpkg @atlaskit/checkbox CHANGELOG.

**GitHub Primer.**
- Fixed; no size prop.
- `FormControl.Caption` is text-body-size-small in fgColor-muted.
- Centered only when there is a leading visual.

Source: primer/react `FormControl.module.css`.

**Fluent 2.**
- Size medium/large sets the indicator to 16/20px; the label stays at the 14/20 base.
- The label's margin is (indicator − 20px line height)/2, which centers its first line on the box.

Sources: fluentui `useCheckboxStyles.styles.ts`; tokens `fonts.ts`.

**SLDS 2.** Fixed size, `vertical-align: middle`.
Source: design-system `checkbox/base/_index.scss`.

**GOV.UK.**
- Standard 40px, `--small` 24px: only the control shrinks; the label font is unchanged.
- The hint (`govuk-hint`) is the same 19px in secondary colour, indented by the 44px touch target plus
  padding.
- The small control sits at top 10px inside the 44px target, which gives first-line alignment.

Sources: design-system.service.gov.uk/components/radios; govuk-frontend `radios/_mixin.scss`,
`hint/_mixin.scss`.

**Base Web.** Fixed checkmark (scale700); label LabelMedium with its line height forced to 24px;
flex-start with a small top offset.
Source: baseweb `checkbox/styled-components.ts`.

**Radix Themes.** Control size 1/2/3 is separate from Text size. The box height equals the surrounding
text's `--line-height`, so "composing Checkbox within Text automatically centers it with the first line".
Sources: radix-ui.com/themes/docs/components/checkbox; themes `base-checkbox.css`.

**Chakra v3.**
- xs/sm/md/lg = box 12/16/20/24, label xs/sm/sm/md, gap 1.5/2/2.5/3.
- sm and md share the label style but differ in box size.
- `alignItems: center`.

Source: chakra recipes `checkbox.ts`.

**Mantine.**
- xs–xl: box 16/20/24/30/36, with the label line height equal to the box size.
- The description is the same size as the label, with a top margin of xs/2.

Source: mantine `InlineInput.module.css`.

**Ant Design.** Fixed, `controlInteractiveSize` 16; no description; inline-flex baseline alignment.
Source: ant.design/components/checkbox.

**Apple HIG.** Align along the leading edge; a group label's baseline aligns with the first checkbox.
Sizes not documented.

**Shopify checkout UI / Stripe.** No size prop, label only. Stripe not documented.

## Density

No system documents a lever that changes row spacing without changing type.

---

## Tally (derived from the rows above, not additional findings)

| question | finding |
|---|---|
| ships a single fixed control | Carbon, Polaris, Primer, SLDS 2, Ant, Base Web, Atlassian (after removing size), Shopify checkout UI |
| size couples box and font step | Spectrum 2, Chakra (partly — sm/md share a label), Mantine |
| size changes the control only | Fluent 2 (indicator grows), GOV.UK (control shrinks), Radix (control tracks inherited line-height) |
| top / first-line alignment | Carbon, Atlassian (restored v12), GOV.UK, Base Web, Fluent 2, Spectrum 2, Radix |
| center or middle alignment | Material 3 Compose (Row recipe), Polaris, SLDS 2, Chakra |
| baseline | Ant |
| center only with a leading visual | Primer (default otherwise not stated in the source) |
| description one step smaller and muted | Carbon, Primer |
| description same size | GOV.UK (secondary colour), Mantine |
| description indented to the label's start | Polaris, GOV.UK |
| type-independent density lever | none |
