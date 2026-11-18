# Figma RTL refresh — Claude run (2026-11-18)

Raw output of a single-agent refresh run. The prompt is `prompt.md` in this folder. No external-agent run was made; if one is added later, it goes in `external-agent.md` beside this file, unedited. The section spine follows the prompt's six scope items, then a verdict on file 13, a feasibility read on two downstream ideas, and an unverified register.

**Method.** Every source was accessed on **2026-11-18**. Primary sources:

- Figma help center articles, fetched directly.
- Figma release notes (`figma.com/release-notes/`). Only the first page of entries loads without scripting, covering 2026-11-02 to 2026-11-17. Older entries were searched for by keyword rather than read in full.
- The plugin API changelog (`developers.figma.com/docs/plugins/updates/`). Its latest entry is Update 142, dated 2026-11-12.
- The published `@figma/plugin-typings` package, version **1.142.0** (npm publish time 2026-10-16T00:20Z), downloaded and searched directly. This is the authoritative surface of what a plugin can read and write.
- The published `@figma/rest-api-spec` package, version **0.47.0** (npm publish time 2026-10-30), searched directly.
- Figma forum threads, cited only to show what is requested and whether staff answered. They are not cited as evidence of capability.

Config 2026 coverage (June 23–25, 2026) was read through secondary recaps only. None of the recaps mentions RTL or direction. Figma's own Config posts were not read in full, which is noted in the unverified register. Anything we could not confirm against a primary page is marked **UNVERIFIED**.

---

## 1. Text: RTL scripts, bidi, paragraph direction, shaping

**Nothing changed in 2025–2026 that we can find.** The capability set is the one that launched in March 2022, when Figma and FigJam added support for RTL languages including Arabic, Hebrew and Urdu. That date comes from the unofficial Figma Releases mirror and from contemporaneous third-party posts; we did not find the original official announcement page.

The current help article, "Add right-to-left text" (https://help.figma.com/hc/en-us/articles/4972283635863), says:

- Direction is set automatically from language detection. It can be overridden in Figma Design from the right sidebar (when an RTL script is detected), from quick actions, or from Text › Text direction. FigJam has the same override through quick actions and the menu.
- Overrides apply **per paragraph**, and bidi text mixing RTL and LTR scripts in one paragraph is supported.
- Arrow keys move forward and backward relative to the text direction.
- **"Each text layer can have one text alignment."** Alignment values are physical: `LEFT`, `CENTER`, `RIGHT`, `JUSTIFIED` (`textAlignHorizontal` in the plugin typings, 1.142.0).
- RTL fonts are available by default, and missing glyphs fall back to Noto.
- Text formatted earlier by RTL plugins is preserved and can be upgraded to native RTL.
- The article does not discuss shaping quality, Persian- or Urdu-specific behaviour (Nastaliq, for example), or known divergences from browser bidi.

No last-updated date is shown on the fetched page.

Release notes (the visible page), the plugin changelog, and keyword searches of figma.com returned **no 2025–2026 entry** mentioning RTL, bidi, text direction, Arabic or Hebrew.

**Bidi divergence from browsers** (file 13's claim) is **UNVERIFIED in both directions**. Figma documents no divergence, and we found no primary source demonstrating one. It remains a practitioner caution, not a sourced fact.

## 2. Layout: direction, mirroring, logical padding, slots, nested instances

**No direction or mirroring control exists.**

- The help article "Use the horizontal and vertical flows in auto layout" (https://help.figma.com/hc/en-us/articles/31289464393751) gives Horizontal ("from left to right") and Vertical ("from top to bottom") flows, with wrap as a toggle. It has no RTL or reverse-order option. Its only "reverse" setting, "Last on top", is canvas stacking (z-order), not flow. The page is undated.
- The plugin typings (1.142.0) define `layoutMode: 'NONE' | 'HORIZONTAL' | 'VERTICAL' | 'GRID'`. They have no direction property on auto layout or grid, padding is `paddingLeft` / `paddingRight` / `paddingTop` / `paddingBottom` only, and `itemReverseZIndex` is z-order only.
- The REST API spec (0.47.0) likewise has no direction, RTL or bidi field. Its only "direction" matches are grid-child alignment, overflow and prototype transitions.
- The 2025–2026 layout changes we found are direction-neutral:
  - vertical auto layout wrap (plugin changelog Update 140, 2026-09-30);
  - `SPACE_EVENLY` and `SPACE_AROUND` alignment (Update 137, 2026-08-31);
  - grid auto layout, which appears in the typings as `layoutMode: 'GRID'`. We did not pin its launch date.
- **Slots** exist as a component property type (`'SLOT'` in the typings, and "Slot frames" cannot use `GRID`). They carry no direction semantics.
- **Nested instances.** The typings state that children of instances "cannot be reparented". A mirror operation therefore cannot re-order layers inside an instance. It can only swap the instance's variant or override properties that Figma allows to be overridden, such as padding.
- Community requests are open:
  - a July 2025 forum thread asking for language-driven RTL switching of fonts, alignment, auto layout order and icons. Its only reply (2026-09-13, not from staff) says auto layout direction cannot be bound to a variable.
  - RTL-wrap feature requests from 2023 onward.
  - None has a Figma staff response or a "launched" status that we could see.

## 3. Variables and modes

**No direction-aware variable type or Figma-recommended RTL pattern exists.** The help article "Apply variables to designs" (https://help.figma.com/hc/en-us/articles/15343107263511) and the typings agree on what can be bound:

- **Bindable:**
  - Number variables bind to padding (all four sides), gap, sizes, radii, stroke weights and opacity (`VariableBindableNodeField`, 1.142.0). The article warns that on-canvas padding or gap edits detach the binding.
  - Boolean variables bind to layer visibility.
  - Boolean, number and string variables bind to **variant properties**: "Boolean, number, and string variables can be applied to instances with variant properties to switch between variants of a component set". The article says this switches variants "depending on the mode of the parent frame".
  - String variables bind to text content and text properties.
  - Text-style fields bind: font family, size, style, weight, letter spacing, line height, paragraph spacing and paragraph indent (`VariableBindableTextField`).
- **Not bindable:**
  - text alignment (`textAlignHorizontal` is absent from both lists);
  - auto layout direction or order, which is not a property at all;
  - text direction, which is not exposed at all.
  - Instance-swap properties are not documented as variable-bindable in the help article. **UNVERIFIED**: we found no positive or negative statement.

**Consequence for file 13.** File 13 (2026-06-29) said a Direction mode could drive "text alignment (`text-align/start` resolves to left/right)" and "mirrored icons via instance swap". The first is **wrong**. The second is **unsupported by any source we found**. The working mechanism for structural and alignment flips is a `dir` variant property bound to a string variable in a Direction collection. That flips structure on a mode switch, at the cost of authoring the RTL variant.

## 4. Plugin API: mirroring and text direction

Checked against `@figma/plugin-typings` 1.142.0 and the plugin changelog to Update 142 (2026-11-12).

**What a plugin can do:**

- Re-order children of non-instance frames (`insertChild`, `appendChild`).
- Swap `paddingLeft` and `paddingRight`, and swap `primaryAxisAlignItems` / `counterAxisAlignItems` where the meaning flips.
- Flip `textAlignHorizontal` between `LEFT` and `RIGHT`.
- Set `relativeTransform` to a horizontal flip, for icons.
- Swap variants (`setProperties`) and instance-swap targets.
- Bind variables and set an explicit variable mode on a frame.
- Replace text content (`characters`), after which Figma's language detection sets the direction.
- Read and write per-segment styles (`getStyledTextSegments`). The segment fields carry no direction.
- Set OpenType features, including `RTLA` / `RTLM`, which are font-level glyph alternates, not paragraph direction.

**What a plugin cannot do:**

- **Read or set paragraph text direction.** No `textDirection` or equivalent exists on `TextNode`, `StyledTextSegment` or text styles. A forum request dated 2025-12-05 asks for exactly this and has no reply. The thread is closed (https://forum.figma.com/report-a-problem-6/why-isn-t-textdirection-exposed-in-the-plugin-api-48298).
- Set layout direction, which does not exist.
- Re-order or reparent children inside an instance.
- Know whether an icon is directional unless the library encodes it, for example in the component description, plugin data or a variant property.

Community plugins (RTL Converter, versions dated 2026-06-15 and 2026-06-17; RTL Master; Arabase; RTL Hero; RTL Layout) advertise frame and component mirroring within these limits. We did not install or test them, and their claims are **UNVERIFIED**.

## 5. Dev Mode and Code Connect

- **Dev Mode.** We found no Figma documentation saying Dev Mode's generated CSS emits logical properties (`padding-inline-*`, `margin-inline-*`, `text-align: start`). The node model only holds physical padding and alignment (see §2–§3), so Dev Mode has no logical signal to emit. Inference: Dev Mode CSS is physical. **UNVERIFIED by direct inspection.** We did not render an RTL fixture in Dev Mode.
- **Code Connect** maps Figma component properties, including variants, to code props (developers.figma.com/docs/code-connect). We found nothing RTL- or `dir`-specific in its docs. Direction reaches code only if a library models it as a property, such as a `dir` variant. Even then, the better contract is that the code component reads direction from context (`dir` attribute or provider), and the Figma variant maps to nothing.
- **Codegen plugins** can emit whatever CSS they like, so a custom codegen plugin is the one route to logical-property output from Figma. That is a build, not a feature.

## 6. What leading design systems do in Figma

*(Appended below from a parallel sub-run of this session.)*

These findings come from a parallel sub-run of this session. The main run did not re-fetch the pages, so they carry the sub-run's own caveats.

**Headline: none of the five major systems publicly documents RTL handling in its Figma kit.** We found no RTL variants, no direction mode or variable, and no mirrored-component library in any of them. Where they have RTL guidance, it is a design principle or lives in code.

| System | RTL in the Figma kit | Bidirectionality guidance | Source (date) |
|---|---|---|---|
| Material 3 | No Figma-specific RTL guidance found. | Mirror layouts and the navigation rail; the FAB moves left; mirror directional icons, not clocks, media controls, numbers or charts. | m3.material.io/foundations/layout/bidirectionality-rtl (undated; JS-rendered, read from search-indexed text only). The M3 kit announcement (material.io/blog/material-3-figma-design-kit, 2022-10-18) does not mention RTL. |
| Fluent 2 | No Figma-specific RTL guidance found. The UI kits page lists Web, iOS, Android, Copilot and Labs kits with no RTL mention. | One typography line: right-align for RTL languages. No mirroring page found. | fluent2.microsoft.design/get-started/design and /typography (undated) |
| Atlassian | No Figma-specific RTL guidance found. The Figma libraries page is client-rendered. | No RTL or i18n topic among the 14 Foundations pages. | atlassian.design/foundations/ (undated) |
| Polaris | No Figma-specific RTL guidance found. | Nothing found. The old polaris.shopify.com docs, including /foundations/internationalization and /contributing/figma-ui-kit, now 301-redirect to shopify.dev/docs/api/polaris. | shopify.dev "Polaris unified and for the web" (2025-05-21, updated 2026-10-06). We found no official statement on the Figma kit's status (**UNVERIFIED**). |
| Carbon | No Figma-specific RTL guidance found on the v11 Figma kit page. | No RTL or bidi guidance page found. | carbondesignsystem.com/designing/kits/figma/ (last updated 2026-07-01) |
| UAE Design System (TDRA) | 4.0 Figma file on Community. The docs instruct designers to "Check every screen in Arabic (right to left) and English" and to "Review mirrored layouts and directional icons in Arabic". No RTL variant, mode or variable is documented. | Set the `dir` attribute; mirror layout and navigation; Noto Kufi Arabic where RTL is the base. | designsystem.gov.ae/resources/assets-and-tools (undated) |
| Saudi DGA / Platforms Code | **UNVERIFIED.** The sites could not be reached from this environment. | — | — |
| Israel gov.il (IGDS) | **UNVERIFIED.** Only third parties point to a Community file, which we could not confirm is official. | — | — |

Practitioner precedent: Wikimedia Codex has an open proposal to add an RTL variant to every Figma component (phabricator.wikimedia.org/T300053). It is a proposal, not a shipped kit.

**Reading:** the field's actual practice matches file 13's stance. The kits are LTR, RTL is proven in code, and an RTL-first system (the UAE one) treats Figma RTL as a review checklist, not a mode. Nobody publishes a direction-mode pattern we could cite as precedent, so ours remains practice IP rather than field convention.

---

## Verdict on file 13

**Figma itself: nothing material changed** between 2026-06-29 and 2026-11-18, and nothing RTL-related changed in 2025–2026 that we could find. The stance holds: design LTR, prove RTL in code, and don't make Figma the RTL authority.

**File 13 still needed correction**, because the re-check exposed errors and soft claims in its own Figma sections:

1. **"Text alignment via a Direction mode" is wrong.** Alignment is not variable-bindable.
2. **"Mirrored icons via a mode-bound instance swap" is unsupported.** We could not source it.
3. **"Improved through 2024–2025" has no primary source.** The capability dates to March 2022.
4. **"Bidi diverges from browsers" is unsourced.** It is now flagged as a practitioner observation.
5. **The variant-bound-to-variable mechanism was missing.** It is the one sanctioned way to flip structure and alignment on a mode switch.
6. **The instance-reparenting limit was missing.** It is the real blocker for mirroring nested instances.
7. **The Dev Mode / Code Connect handoff of direction was missing.**

These are landed in file 13 on this branch (Path B: direct to the numbered file).

---

## Feasibility: two downstream ideas

**An RTL specimen inside component specs: feasible now, with conditions.**

The specimen is a frame showing the component in RTL beside LTR, generated or maintained per component.

- **What works.** Figma renders RTL text correctly enough for review once the strings are real RTL content. A Direction mode can swap padding. A `dir` variant bound to a Direction variable flips structure and alignment.
- **What blocks it:**
  1. Every directional component needs an authored RTL variant, or the specimen shows a broken layout. The authoring cost is real and per-component.
  2. Text direction follows content, and a plugin cannot set it, so the specimen needs real translated strings. Mirrored Latin placeholder text will not render RTL.
  3. Icons need directionality metadata in the library to be mirrored correctly.
  4. The specimen is illustrative, not authoritative. Bidi edge cases still need a browser check.

**A "make an RTL copy" helper for screen mock-ups: feasible as a best-effort plugin, not as a faithful mirror.**

- **What a plugin can do.** It can duplicate a frame and walk it. For each non-instance auto layout frame, it can re-order children and swap left and right padding. It can flip `LEFT`/`RIGHT` text alignment, swap instances to a `dir=rtl` variant where one exists, and flip icons flagged as directional.
- **What blocks a faithful result:**
  1. **Children inside instances cannot be re-ordered.** Any component without an RTL variant stays LTR inside the copy, or must be detached, which breaks library linkage.
  2. **There is no plugin access to text direction.** Copy that is still English stays LTR, and neutral or mixed strings cannot be forced RTL.
  3. **Absolute-positioned and non-auto-layout content** needs coordinate mirroring, which is approximate.
  4. **Icon directionality is unknowable** without library metadata.
  5. The copy is a fork. It is not linked to the LTR source and drifts on the next edit.
- **What would unblock it:** a variable-bindable or plugin-settable layout direction, plus plugin access to paragraph direction. Neither exists or has been announced.

---

## Unverified register

- Bidi rendering divergence between Figma and browsers. No primary source either way.
- Whether instance-swap properties can be bound to variables.
- Whether Dev Mode's generated CSS ever emits logical properties. Not inspected against an RTL fixture.
- Figma's own Config 2026 posts. Only secondary recaps were read, and none mentions RTL.
- Release notes older than 2026-11-02. Keyword search only; the page could not be paged without scripting.
- The launch date of grid auto layout. Not pinned.
- Community RTL plugin capabilities. Not installed or tested.
- Saudi DGA / Platforms Code and Israel IGDS Figma handling.
- Polaris Figma kit status.
- The official 2022 RTL launch post. Only the unofficial Figma Releases mirror (figmareleases.blogspot.com/2022/03/figma-now-supports-rtl.html) was found.

## References (all accessed 2026-11-18)

- Figma help center, "Add right-to-left text": https://help.figma.com/hc/en-us/articles/4972283635863-Add-right-to-left-text
- Figma help center, "Use the horizontal and vertical flows in auto layout": https://help.figma.com/hc/en-us/articles/31289464393751
- Figma help center, "Apply variables to designs": https://help.figma.com/hc/en-us/articles/15343107263511-Apply-variables-to-designs
- Figma help center, "Explore component properties": https://help.figma.com/hc/en-us/articles/5579474826519-Explore-component-properties
- Figma release notes: https://www.figma.com/release-notes/
- Figma plugin API updates: https://developers.figma.com/docs/plugins/updates/
- `@figma/plugin-typings` 1.142.0: https://www.npmjs.com/package/@figma/plugin-typings
- `@figma/rest-api-spec` 0.47.0: https://www.npmjs.com/package/@figma/rest-api-spec
- Code Connect docs: https://developers.figma.com/docs/code-connect
- Figma forum, textDirection in the plugin API (2025-12-05): https://forum.figma.com/report-a-problem-6/why-isn-t-textdirection-exposed-in-the-plugin-api-48298
- Figma forum, Arabic RTL switching request (2025-07-09): https://forum.figma.com/suggest-a-feature-11/arabic-rtl-support-for-switching-font-font-style-text-direction-and-component-elements-direction-42624
- Design-system pages as listed in §6.
