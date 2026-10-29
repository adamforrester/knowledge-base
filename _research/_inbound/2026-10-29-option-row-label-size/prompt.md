# Field scan — option-row control size, label alignment and description styling

> Narrow field scan for the Checkbox and Radio briefs (`components/checkbox.md`, `components/radio.md`), run
> to test one position they held: that the `size` variant means **the control scales with the type**. Run
> per `_research/README.md`; this folder holds the question and the raw findings. Owner decision Q854 A
> (2026-10-29) adopted the result.

---

**The question:** in the leading design systems, how is the option row of a checkbox or radio built —
and does the control's size follow the label's type step?

**Four things specifically:**

1. **Control size.** Does the system ship a size prop for the control at all? If it does, what does a size
   step change — the box, the label font, or both — and by how much?
2. **Alignment.** How is the control aligned to the label: top / first line, baseline, or center? What
   happens on a label that wraps to two lines? Has any system changed its alignment, and why?
3. **The description.** What is the secondary text under the label called, what size and colour is it
   relative to the label, and where does it indent from — the control or the label?
4. **Density.** Is there any lever that changes row spacing (gap between options, row padding) without
   changing type?

**Candidates:** Material 3 (Compose), IBM Carbon, Shopify Polaris, Adobe Spectrum 2 / React Spectrum S2,
Atlassian, GitHub Primer, Microsoft Fluent 2, Salesforce SLDS 2, GOV.UK Design System, Uber Base Web,
Radix Themes, Chakra v3, Mantine, Ant Design, Apple HIG, Shopify checkout UI extensions, Stripe.

**Method:** read source where it exists (stylesheets, recipes, component files), not only docs pages;
cite each finding to its file or URL; say plainly where a system does not document the answer. Findings
only, no recommendation.
