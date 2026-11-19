Research question for a design-system decision. Use web search and fetch. Cite sources with URLs. Be concise. Aim for 25–40 tool calls, not more.

Context: we are deciding how a design system models the overlays an e-commerce brand uses. Every overlay we found is a right-side drawer on desktop (492px or 550px) and full-screen on mobile. A few are bottom sheets on mobile: a size picker, and an added-to-cart sheet with rounded top corners. The cart drawer also starts below the site header. The use cases are:
- short capture forms (notify me);
- log-in/sign-up: no title, Log in / Create account tabs in the header;
- edit-record forms: title, pinned Cancel/Save footer;
- destructive confirms;
- filter & sort: title, grouped radios/checkboxes, pinned "See 27 items" button;
- picker sheets;
- added-to-cart confirmation.

Today the system has ONE Dialog component with `placement` center/bottom/full/end. Our knowledge base's position, which you should test, not repeat:
- a modal drawer is "a Dialog anchored to an edge", so it reuses the Dialog implementation;
- but name it as its own `Drawer` component, with `placement` and `modal` props;
- reserve `Sheet` for the bottom, gesture-driven, detent variant;
- prefer a composable Header/Body/Footer slot anatomy over a monolithic config.

The options on the table:
- **A.** One Dialog component, extended. It gets a titleless header that can hold tabs, a footer that is either pinned or in flow, end-placement widths, and separate header and footer dividers. Brand-specific shapes (log-in drawer, form drawer, filter drawer) are local wrappers built on it.
- **B.** A second component for sheets and drawers: filter, picker, cart. Dialog stays for forms and confirms.
- **C.** Brand-only hand edits.

Find out, as of 2025–2026, how these design systems handle it:
1. **Each system's modeling.** Does it ship Dialog and Drawer/Sheet as separate components or as one? If separate, do they share a base? Cover Material 3, Apple HIG, Fluent 2, Carbon, Polaris, Atlassian, Primer, Spectrum / React Aria, Radix/shadcn (Dialog vs Sheet), Chakra, Ant, Base Web, and SAP Fiori if useful.
2. **Header variations.** Is a titleless header (or one holding tabs) supported? How is the accessible name supplied when there's no visible title?
3. **Footers.** Pinned/sticky vs in-flow: which systems offer both, and how is it expressed (prop vs composition)?
4. **Filter panels specifically.** Are they a separate "filter drawer"/"side panel" pattern or a dialog? Check Polaris (Filters, IndexFilters), Carbon, Material, and any public e-commerce systems: Shopify Polaris, Nike, Zalando, ASOS, H&M, Farfetch, Adidas, if they document it.
5. **E-commerce cart/added-to-bag drawers that start below the header.** Is this a documented pattern anywhere?
6. **Bottom sheets** at content height with rounded corners: which systems model this as its own component?

Output:
- a table, one row per system, with columns: modeling; titleless/tabs header; pinned vs in-flow footer; filter-panel approach; source URL;
- a short synthesis: which of A, B or C the field supports, where our knowledge base's "separate Drawer on a shared Dialog base" position sits against the evidence, and any approach we haven't listed;
- flag anything unverified.
