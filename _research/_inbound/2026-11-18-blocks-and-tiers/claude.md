# Blocks, sections and the tiers above the component — Claude run (2026-11-18)

This is the raw output of the Claude half of the run. The prompt is `prompt.md` in this folder, unedited. Sections 1–6 follow the prompt's six scope items. After them come direct answers to questions A, B and C, a register of what this run corrects or contests, a proposed promotion target, an unverified register, and references.

**Method.** We read four kinds of source in parallel, all of them primary:

- vendor platform documentation: shopify.dev, Experience League and aem.live, developer.wordpress.org, the Storyblok, Sanity and Contentful docs, and the Figma Help Center and plugin changelog;
- open repositories and registries: `Shopify/dawn`, `Shopify/horizon`, `figma/sds`, and the shadcn/ui registry JSON, which we counted directly;
- design system documentation sites: GOV.UK, Carbon, Carbon for IBM.com, Cloudscape, Primer, Polaris and the Shopify App Home docs, React Spectrum, Ant Design, Android Developers for Material, and the W3C ARIA Authoring Practices Guide (APG);
- authors' own posts: Frost's blog and book, and Curtis's Substack.

Inside the vault we read `_source-text/ext-figma-ai.txt`, `ext-curtis-contracts-and-schemas.txt`, `ext-curtis-slots-repeating-items.txt` and `ext-vallaure-design-system-contracts.txt`. In Prism3 we read issues #4001, #3999 and #693, and `docs/37-block-layout-axes.md`.

Every URL was accessed on **2026-11-18**. Most documentation pages carry no date, and we say so wherever that is the case. Some sources could not be read directly: m3.material.io and fluent2.microsoft.design render client-side or returned errors, and Tailwind Plus is behind a login. For those we used search-index snippets or a neighbouring primary source and marked the claim. Anything we could not confirm against a primary page is marked **UNVERIFIED**.

---

## 1. Figma's argument for blocks, and what native slots change

**The argument.** Figma's report *How design systems power the new pace of product development* sits behind a form on its landing page (figma.com/reports/design-systems-power-the-pace/). The public page is undated. Figma's blog post *5 shifts redefining design systems in the AI era* (Emma Webster, 19 Nov 2025) links to it, which dates the report to about November 2025. The vault holds the text as `_source-text/ext-figma-ai.txt`, so the quote is verified from our own capture:

> "Design systems are built around modular components like buttons, inputs, and icons, but those smaller pieces can be difficult for AI tools to compose into coherent layouts on their own. Adding higher-order compositions—blocks and patterns that capture layout, color, and spacing logic—gives AI the context it needs to generate those interfaces."

> "Add larger, reusable blocks. Extend your existing system with blocks like headers, cards, or carousels that AI can draw from when generating layouts."

> "Instead of structuring your system around separate components like buttons, text fields, and image containers, create a reusable 'card' block where those elements are already grouped with defined spacing, color, and typography tokens."

**What the argument actually is.** Figma uses "block" for anything above an atomic component that has its spacing already decided. Its three examples belong to three different tiers in the Prism3 model:

- a header is a section;
- a card is a composed component;
- a carousel is a composed component, and on a marketing page it is often a section as well.

So Figma's word is not a tier name. It means "pre-composed," and its claim is about AI generation, not taxonomy. **The practice should cite Figma for the claim that pre-composition helps generation, and should not cite it as a definition of "block."** The 03 open question 7 wording ("cards, headers, carousels as the right unit") reads Figma as making a tier argument. It isn't making one.

**Figma's own reference system names the tier differently.** The Simple Design System repository (`github.com/figma/sds`, undated) splits `src/ui` into `primitives` ("can't be reduced further into sub components"), `layout` and `compositions`. Its README defines compositions as "Example arrangements of primitive components to demonstrate how you might use SDS to build a responsive website." So Figma's own engineering vocabulary is **compositions**, and those are examples, not contracts.

**Figma Sites uses "blocks" in a third sense.** The Help Center article on inserting blocks (undated; Sites entered open beta at Config, May 2025) describes layout blocks as "Ready-made design components you can drag and drop into to your website to quickly assemble a layout." That is the page-builder sense, which is closest to a section. The article does not list block names.

**Native slots are the change that matters for tier 2.** The history:

- introduced at Schema 2025;
- open beta announced on the Figma forum on 5 Mar 2026;
- GA recorded in the plugin API changelog on 10 Jun 2026, under "Slots GA". A 28 May date circulates in third-party coverage only and is UNVERIFIED.

The Help Center ("Use slots to build flexible components in Figma", undated, all plans) defines the contract surface: a slot is a component property, "flexible areas placed inside main components". **Preferred instances** let a team "Create a curated list of components for your team to choose from". An "Only allow preferred instances" setting turns that list into a restriction. Forum reports from 2026 say a variant cannot be a preferred instance; that comes from the community, not Figma.

**Consequence for the tier model.** Before slots, a Figma composed component could not express "this region accepts these fillers" except through instance swaps, hidden layers and count props. Curtis lists all three as anti-patterns in *Figma Slots for Repeating Items* (23 Jan 2026; vault capture `ext-curtis-slots-repeating-items.txt`). With slots, the **allowed-fillers clause of a tier-2 contract has a native Figma projection**: the slot plus its preferred-instance list. The same mechanism can carry a section's regions, so tier 4 gets a Figma projection too. Neither tier is Figma-blocked any more. One gap remains: there is no native cardinality (min/max items) on a slot. That has to stay in the contract and in a lint.

## 2. Code-side block distributions

**shadcn/ui.** Blocks launched in March 2024 (ui.shadcn.com/docs/changelog/2024-03-blocks): "Blocks are ready-made components that you can use to build your apps … fully responsive, accessible, and composable." The registry schema (registry-item-json, undated) gives `registry:block` its own type, "Use for complex components with multiple files," next to `registry:component`, `registry:ui` and `registry:page`.

We counted the live `new-york-v4` registry: **471 items, 97 of them blocks**. The families are:

- charts: 70
- sidebar: 16
- login: 5
- signup: 5
- dashboard: 1

There are **no marketing blocks in the official registry**. Marketing blocks come from community registries, such as the Initium library Prism3 already captured.

A block entry looks like this (`login-01`):

- a `description`;
- `registryDependencies: [button, card, input, label, field]`;
- a `files` list with a page file targeted at `app/login/page.tsx` plus a `login-form.tsx` component;
- `categories`.

**A shadcn block is a distribution manifest, not a contract.** It declares dependencies and file targets. It has no settings, no regions and no allowed fillers. Layout variation is expressed as **separate numbered blocks** (`login-01` … `login-05`).

**Tailwind Plus** sits behind a login from this environment. We could read only its category names, from search-index snippets of the official pages. The names are reliable; the counts are snapshots and UNVERIFIED. The catalogue is cut three ways:

- **Marketing.** Page Sections: Hero, Feature, CTA, Bento Grids, Pricing, Header, Newsletter, Stats, Testimonials, Blog, Contact, Team, Content, Logo Clouds, FAQs, Footers. Elements: Headers, Flyout Menus, Banners, and Promo Sections.
- **Ecommerce.** Fourteen groups: Product Overviews, Product Lists, Category Previews, Shopping Carts, Category Filters, Product Quickviews, Product Features, Store Navigation, Promo Sections, Checkout Forms, Reviews, Order Summaries, Order History, Incentives. Plus page examples.
- **Application UI.** Application Shells (Stacked, Sidebar, Multi-Column), Headings, Data Display, Lists, Forms, Feedback, Navigation, Overlays, Elements, and Page Examples.

Prism3's `37` §3 already rates Tailwind Plus the highest-value witness because it names its own variants. This run agrees, and adds that its **three-surface split (marketing, ecommerce, application) is the right top-level cut for a base catalog**. No other witness ships all three.

**Other kits.** Each names the tier differently, which is itself a finding:

- **Relume** (relume.ai/components) has Marketing, Ecommerce and Application UI sets. Section names are listed in §C.
- **Mantine UI** (ui.mantine.dev) groups items as "Page sections" and still calls every item a "component."
- **Untitled UI** advertises "components, sections, and example pages."
- **Chakra UI Pro** calls them "blocks" and installs them by CLI category. That claim is secondary.

**The code-kit pattern is consistent.** Code kits express layout variation as separate numbered or named blocks. Platforms express it as a setting, preset, style or option on one block (§3). That is a real fork, and the contract has to pick a side; §B picks the platform side.

## 3. Commerce theme and CMS section models

This is where the field has written section contracts down. Every platform below declares, in a schema, what Prism3 #3999 asks a section contract to record. They differ in vocabulary, not in shape.

**Shopify Online Store 2.0** (shopify.dev; the pages are undated).

- **The section schema** declares:
  - `name`;
  - `tag`, one of `article | aside | div | footer | header | section`;
  - `class`;
  - `limit` (1 or 2 per page);
  - `settings`;
  - `blocks`, each with a `type`, a `name` and an optional per-type `limit`;
  - `max_blocks` ("There's a limit of 50 blocks per section");
  - `presets`, each with a `name` and optional `category`, `settings` and `blocks`;
  - `default`;
  - `locales`;
  - `enabled_on` or `disabled_on` by template or section group.
- **JSON templates** render up to 25 sections. **Section groups** (`header`, `footer`, `aside`, `custom.<name>`) also hold up to 25.
- **The limits page** sets, among others:
  - 1,250 blocks per template;
  - theme-block nesting to 8 levels;
  - 300 theme-block files.
- **Theme blocks** were introduced on the partner blog on 31 Jan 2024: "Theme blocks allow you to define a block once and then reuse it across sections". A section accepts them through `@theme`, or defines its own section blocks, but not both. **Static blocks** are placed by the developer, are not removable by the merchant, and don't count toward `max_blocks`.
- **Layout variation** is expressed as **settings plus multiple presets**. One section ships several named presets, and each one appears as its own entry in the merchant's Add-section picker.

**Dawn and Horizon show the platform's own trajectory.** Dawn (`Shopify/dawn/sections`) has 49 section files, most of them purpose-named:

- image-banner, image-with-text, multicolumn, multirow;
- collage, slideshow, video;
- featured-collection, featured-product, collection-list;
- collapsible-content, contact-form, email-signup-banner, newsletter;
- featured-blog, related-products, rich-text, announcement-bar;
- and the `main-*` template sections.

Horizon, the Summer '25 reference theme, has **fewer and more generic sections**: hero, media-with-content, product-list, carousel, slideshow, marquee, product-hotspots, a bare `section`, and `_blocks`. It moves composition into **about 95 theme blocks**, including `_card`, `_content`, `_heading`, `_slide`, `_product-card`, `price`, `variant-picker`, `group` and `review`. Horizon's launch is documented only by third parties, so its framing is UNVERIFIED; the repository contents are primary.

**The trajectory is the finding.** Shopify moved from many purpose-named sections with fixed internals to a few layout sections whose regions accept reusable blocks. That is the same move as from a contract per layout to one contract with regions and options. #3999 is aligned with where the largest commerce theme platform went in 2024–25.

**Salesforce Commerce Cloud Page Designer.** This is already in the vault (10, Page Designer's component model). **Page types** declare **regions**, and each region has rules on which component types may drop into it. Each component's JSON meta-definition carries `region_definitions` (exclusion rules and instantiation limits) and `attribute_definitions` (the authoring form). That is the cleanest page/section/region split in the commerce set.

**AEM.**

- **Core Components** (Experience League, introduction last updated 16 Oct 2026) split into template components, page authoring components (Title, Text, Image, Button, **Teaser**, List, Embed and others), **container components** (Container, Carousel, Tabs, Accordion) and form components.
- **Teaser** is the field's generic card or promo. Its policy can hide the pretitle, title or description, or disable its calls to action. Its layout variation comes from the **Style System**.
- **Container's** policy carries "Allowed Components", "Default Components", "Responsive Settings", Background and Styles. In other words, allowed fillers, default fillers, responsive behaviour and surface.
- **Experience Fragments** are "fully laid out content; a fragment of a web page". Content Fragments are content without layout. So AEM separates content model from layout at the platform level.

**AEM Edge Delivery Services.** The block collection (aem.live/developer/block-collection, undated) states the membership rule verbatim: "to be included in the block collection a block must be used on more than half of all AEM projects." It sorts into three groups:

- **Boilerplate:** Hero, Columns, Cards, Header, Footer, plus Metadata and Section Metadata.
- **Default content** (not blocks): headings, text, images, lists, links, buttons, code, sections, icons.
- **Collection:** Embed, Fragment, Table, Video, Accordion, Carousel, Quote, Search, Tabs, Breadcrumbs, Modal; Form is deprecated.

**Variants are options in parentheses**: "Columns (wide)" becomes a CSS class. The Universal Editor's `component-models.json` types a block's fields, and filters limit "which children can be added to the block or section." **The EDS rule that a "section" is a separate thing from a "block"** (sections are separated by `---` and carry Section Metadata) is the one place where the field formally separates *the page band* from *the block in it*. It matters for §B.

**WordPress.** The units:

- **Block** (`block.json`): `allowedBlocks`, `parent`, `ancestor`, `styles` and `variations`.
- **Pattern**: a registration header with Title, Slug, Categories, Keywords, Block Types, Post Types, Template Types, Viewport Width and Inserter (developer.wordpress.org, updated 15 Jul 2024).
- **Synced pattern with overrides**: "let users make content-specific changes without changing the underlying layout or design of the pattern" (WordPress Developer Blog, June 2024).
- **Template part**: header and footer.

The core pattern categories are: featured, about, audio, banner, buttons, call-to-action, columns, contact, footer, gallery, header, media, portfolio, posts, services, team, testimonials, text, video. Variation has **two mechanisms**: `styles` (a class swap) and `variations` (preset attributes). **Overrides are the cleanest primary statement of "author-editable vs system-fixed"** anywhere in the field: the pattern fixes layout and design, and named bindings expose specific blocks' content.

**Storyblok** (docs last updated 13 Oct and 28 Sep 2026). There are three block kinds:

- **content type** blocks, which are stories ("post, article, or page");
- **nestable** blocks ("text, image, or hero");
- **universal** blocks, which can be either.

The Blocks field carries an allowed minimum and maximum, and can "Restrict which nestable blocks users can insert" by block, folder or tag.

**Sanity.** A page builder is an `array` field whose `of` lists object types. It has `min`, `max` and `unique` validation, and since 18 Jun 2024 `insertMenu.groups` and grid views with preview images. Layout variation is a field on the object type; there is no variant primitive.

**Contentful.**

- The content-modelling guidance (help page timestamp 2021-01-12) names **topics** and **assemblies**: "Assemblies use reference fields to refer to topics," fixed or flexible, and nestable.
- **Studio (Experiences)** adds three things:
  - layout structures: Section at 100% width, Container at a 1192px max width, Columns on a 12-column grid;
  - **patterns**: "a combination of components that you can group in an experience and save for reuse," capped at 200 per environment;
  - registered components whose `variables` carry `type`, `defaultValue`, `validations: { in: [...] }` and a `group: 'style'`.
- Variation is **an enumerated variable**.

**Builder.io** registers components with `inputs`, `models`, `canHaveChildren` and `childRequirements`. Only the first two are documented on the page we read; the child rules are UNVERIFIED there.

**The cross-platform table.**

| Platform | Unit | Regions / children | Allowed fillers | Cardinality | Layout variation | Author-editable vs fixed |
|---|---|---|---|---|---|---|
| Shopify | section → blocks (section, theme, static) | `blocks` | block types, `@theme`, `@app` | `max_blocks`, per-type `limit`, section `limit` 1–2 | settings + **presets** | settings vs static blocks |
| SFCC Page Designer | page type → region → component | `region_definitions` | component-type rules per region | instantiation limits | attributes | attribute definitions |
| AEM Sites | Container / Teaser / XF | container children | **Allowed Components** policy | policy | **Style System** | dialog vs design-dialog policy |
| AEM EDS | section → block | sections, block rows | filters | — | **options** → classes | model fields |
| WordPress | block / pattern / template part | `allowedBlocks`, `parent` | `allowedBlocks` | — | `styles` vs `variations` | **synced-pattern overrides** |
| Storyblok | content type → nestable | Blocks field | allow/deny by block, folder, tag | min / max | fields | fields |
| Sanity | array of object types | `of` | the `of` list | min / max / unique | fields | fields |
| Contentful Studio | section / container / pattern / component | layout structures | registered components | 200 patterns | enumerated `variables` | pre-binding |
| Figma | component with slot | slot | **preferred instances**, optionally enforced | — (none) | variants | slot vs props |
| shadcn | `registry:block` | files | `registryDependencies` | — | separate numbered blocks | n/a (source is copied) |

Two things in this table are load-bearing.

**First, every authoring platform separates "which fillers" from "how many" from "which layout option," and none treats layout variation as a separate unit.** Only code kits do that, and code kits have no authors.

**Second, every authoring platform has an explicit author-editable versus system-fixed line**: overrides, static blocks, design-dialog policy. Prism3's #693 already said "a definition capturing only layout cannot generate the AEM projection." The platforms confirm it, and they show the content model is not optional for a section contract. #3999 as filed does not list it.

## 4. Atomic Design and its critiques

**Frost's definitions moved between 2013 and 2016, and the move matters.**

- *Atomic Web Design* (10 Jun 2013): organisms are "groups of molecules joined together to form a relatively complex, distinct **section** of an interface."
- *Atomic Design* ch. 2 (2016): molecules are "relatively simple UI components" and organisms "relatively complex components that form discrete sections of an interface." Templates "place components within a layout and demonstrate the design's underlying content structure"; "Atomic design is not a linear process" but "a mental model."

**The tier line in Atomic Design is complexity, and complexity is the axis practitioners could never agree on.**

- Alla Kholmatova of FutureLearn, quoted by Trent Walton in *Atomic Classification* (26 Feb 2016), said her team was "struggling to understand exactly when a molecule is complex enough to become an organism." The original post returned 403.
- Sparkbox, *Iterating on Atomic Design* (Kasey Bonifacio, 1 Nov 2024): "The lines between what is an atom, molecule, etc. are too fuzzy … The rules for categorizing are subjective." Sparkbox recommends starting flat.
- A Qt blog post (26 Nov 2025, updated 25 Mar 2026) quotes Frost by email: "The specific labels … have never been the point." It also records the canonical arguments: whether a card is a molecule or an organism, and whether a button group is a molecule. That source is secondary.

We found no primary "atomic design is dead" piece. **The critique is that the middle labels are unsortable, not that the model is abandoned.**

**Frost replaced the complexity axis himself.** *The design system ecosystem* (21 Sep 2023) and *The art of design system recipes* (22 Apr 2024) define layers by **reuse scope and ownership**:

- core: "common, organization-wide UI building blocks";
- recipes: "composed UI components to be used consistently across specific contexts … but aren't reusable across the entire organization";
- smart components;
- product.

His examples: "The e-commerce team can compose a product card recipe, the marketing team can compose a promo card recipe"; "A product's website header is a great example of a recipe." **A card is core; a product card is a recipe.** The tier depends on who owns it and where it is reused, not on how many atoms it has.

**GOV.UK uses a third axis: user task.** It has three groups:

- styles;
- components ("reusable parts of a user interface", 37 of them, including Date input, with no card, carousel or button-group component);
- patterns, "best practice design solutions for specific user-focused tasks and page types". These are grouped as **Ask users for…**, **Help users to…**, and **Pages**.

**GOV.UK's page types are patterns, not a separate template tier.** "Dates" is a pattern that tells a team whether a calendar control is warranted. Date input is the component.

**Dan Mall** framed content patterns versus display patterns. It survives only through Frost's 4 Jan 2016 link post, because the original would not load: "every element on the screen needs a Content pattern and a Display pattern applied to it." That is the earliest statement of the content-model-plus-layout split that §3's platforms enforce. We found **no primary Mall source for an element/component/pattern taxonomy**. "Hot potato" is a handoff process, not a taxonomy. The vault's 03 tension 4 cites Mall's "rule of three" for promotion; that attribution stands from search snippets only.

**The vault already owns the overlay.** 09 §2.3 records that the "Subatomic / Atomic / Molecule / Organism / Template" stack is the practice's overlay and should not be attributed to Frost. Nothing here changes that.

## 5. Contracts, schemas and slots (Curtis)

**What a contract is.** From *Component Contracts and Schemas* (28 Jul 2026; vault capture):

- "A description informs. A contract arbitrates."
- "A schema is the model a contract is written in."
- He favours verifiable over readable, and determinism over inference: "When I can't verify something, I want to delete it."

**The test for an upper-tier contract is therefore whether each clause can be checked.** "Region `actions` accepts 0–2 of {button, link}" can be checked. "The hero should feel premium" cannot. This is the strongest argument for what a section contract should *leave out* (§B).

**Slots.**

- *Slots in Design Systems* (7 Nov 2025): "A slot is a designated place inside a component where custom content can be inserted … while preserving control of the component's surrounding layout, styling, and behavior." It nests accordions in a page row, page rows in a layout, and layouts in a page body slot. That is a slot-based account of the section and page tiers, but **he does not name where those compositions live**.
- *Configuration Collapse* (27 Feb 2026): "Make the common configurable, make the uncommon composable."
- *Implementing Slots in a Figma Library* (2 Mar 2026) gives a slot taxonomy: empty default, default content, configuration-first with a slot as an escape hatch, named slots, items slot, and subcomponent with or without a slot.
- *Figma Slots for Repeating Items* (23 Jan 2026): explicit groups (checkboxGroup, radioButtonGroup, avatarGroup, **buttonGroup**) and implicit groups (tabs, breadcrumbs, action list, list). "Count" props are "composition, not configuration."
- *Component Examples as Data* (26 May 2026): slot default content "is NOT part of the component's configurable contract," and examples are "demonstrating potential, not an exhaustive catalogue."

**Two consequences for the tier contracts.**

1. **A tier-2 contract's slot clause has three parts:** the slot name, its allowed fillers, and its cardinality. Default content is explicitly outside the contract; it is an example. #4001 says "slots and allowed fillers", so cardinality should be added.
2. **Curtis has no pattern tier and no recipe tier.** Examples sit beside a component; they are not a tier above it. So Curtis supplies the contract discipline for tiers 2 and 4, but gives no warrant for a pattern *contract* in the strict sense. That fits §A's finding that a pattern is guidance with lintable rules, not an arbitrating contract.

**Vallaure** (*Design system contracts*, vault capture) is already filed in 03 and was promoted with PR #52; we did not re-read it for this run beyond confirming it is component-scoped.

## 6. How major systems name and ship the upper tiers

| System | Names above component | What "pattern" means | Ships code above component? |
|---|---|---|---|
| **Material 3** | canonical layouts (list-detail, supporting pane, feed) | m3.material.io was not readable; UNVERIFIED | **Yes**: `ListDetailPaneScaffold`, `SupportingPaneScaffold` with slot lambdas |
| **Polaris** (App Home, 2025+) | **compositions** ("Smaller groupings of web components and APIs that solve specific tasks") and **templates** ("Full page patterns": Homepage, Index, Details, Settings) | an umbrella over both | Copy-paste JSX/HTML examples, not packages |
| **Polaris** (legacy React) | patterns ("Preferred solutions to common merchant goals"): card layout, date picking, resource index layout and others | task solutions | example code |
| **Atlassian** | patterns (First impressions, Forms, Messages; secondary) | guidance | no |
| **Carbon** (core) | patterns: login, forms, empty states, filtering, global header and others | "best-practice solutions"; patterns "differ from components, which are already designed, coded" | no |
| **Carbon for IBM.com** | UI components vs **layout components**: Content block, Content section, Content group, CTA block & section, Feature section, Lead space, Card group, Masthead, Footer | folded into components; the package name `ibmdotcom-patterns-react` survives | **yes**, as components |
| **GOV.UK** | patterns: Ask users for…, Help users to…, Pages | user task and page type | guidance + example markup |
| **Cloudscape** | patterns ("reusable combinations of components that solve common user problems") + **demos** ("an example of a layout template using components") | task solutions | demos are runnable reference apps |
| **Primer** | UI patterns, scenario patterns; `PageLayout` is a component | "Design guidelines covering common user workflows" | no |
| **SLDS 2** | patterns ("Design guidelines in SLDS 1 are what we call patterns in SLDS 2"), blueprints | guidance | blueprints are static HTML/CSS |
| **Spectrum S2** | none; everything is a component | — | — |
| **Ant Design** | design patterns, **templates** ("A page-level example"), ProComponents | "general solution to recurring design issues" | ProComponents are code (UNVERIFIED in detail) |
| **W3C APG** | "patterns" = widgets | an interaction and semantics contract | reference examples |

**Three readings of this table.**

1. **"Pattern" is a homonym, and the collision is live.** In product systems (Carbon, Cloudscape, Primer, GOV.UK, SLDS) a pattern is task guidance that does not ship as code. In APG a pattern is a widget contract: Carousel, Tabs, Combobox. In Contentful Studio a pattern is a saved composition. In WordPress a pattern is a saved block arrangement. **"The carousel pattern" means four different things depending on who says it.** The practice's tier names must say which sense they mean, every time.
2. **The tier above "pattern" is named by platforms that author pages, and almost never by product systems.** Carbon for IBM.com (marketing pages), Polaris App Home (templates and compositions), Shopify themes, AEM, WordPress and Tailwind/Relume/Mantine all name a section or block tier. Atlassian, Primer, Spectrum and core Carbon do not. **Sections are a property of authored, page-assembled surfaces.** That is why the vault's product-system-derived `patterns/` layer has no place for them, as 09 §1.36 found.
3. **Polaris App Home is the clearest three-tier precedent**: component → composition (section-sized, task-named: Metrics card, Media card, Setup guide, Index table) → template (page). Its compositions sit between Prism3's tiers 3 and 4: task-named like a pattern, region-sized like a section, and shipped as code like neither.

---

## A. How each tier should be defined

### The field disagrees on the axis, not the labels

Everyone agrees on the two ends: the atomic component and the page. The middle is cut along **four different axes**, and most taxonomy arguments are really two people using different axes:

| Axis | Who uses it | What it sorts |
|---|---|---|
| **Complexity** (how many parts) | Atomic Design | atom → molecule → organism |
| **Reuse scope / ownership** | Frost's ecosystem; Polaris compositions | core → recipe → product |
| **User task** | GOV.UK, Carbon, Cloudscape, Primer, `patterns/` here | component → pattern |
| **Page role** | Shopify, AEM, WordPress, Carbon for IBM.com, Tailwind/Relume | component → section → page |

**The Prism3 five-tier model mixes three of these, and that is its one structural problem.**

- Tiers 1 and 2 sort by complexity, with behaviour as the discriminator.
- Tier 3 sorts by task.
- Tiers 4 and 5 sort by page role.

Task and page role are not points on one ladder. **A pattern is not bigger than a composed component and smaller than a section.** It is a different kind of artefact, and it can be realised at any scale:

- GOV.UK's "Dates" pattern governs a component choice.
- Carbon's "Login" pattern is a whole page.
- A "newsletter signup" pattern is realised as a section on a marketing page.

### Recommended definitions

Keep the five names. **Draw tier 3 beside the ladder, not on it.**

1. **Atomic component.** One job, its own anatomy, goal-agnostic. A full component contract (the vault's §15 shape). Discriminator: it cannot be decomposed into other catalogue components without losing its behaviour.
2. **Composed component.** It has its own frame and its **own behaviour or state** (selection, overflow, open/closed, roving focus, pagination). It is built from atomics through **named slots**. It is still goal-agnostic. Full contract plus a slot clause (name, allowed fillers, cardinality). Discriminator: **it owns behaviour no filler owns.** If it only arranges things, it is a section region or a layout primitive, not a composed component.
3. **Pattern** (beside the ladder). A **task-level recurring solution**: which components, in what order, with what rules and copy. It carries a goal. It may ship no artefact at all, or it may be *realised by* a composed component, a section or a template. Its contract is guidance with lintable rules (§B). The discriminator is the vault's existing one (`patterns/_schema.md`): **opinionation and goal, not packaging.**
4. **Section** (block). A **page region keyed to page role**, not to a user task. It has named regions, layout options and a content model. It is authorable. A section owns **no behaviour of its own**. Interaction lives in the components that fill it: a section that needs a slide-advance behaviour contains a carousel. Discriminator: **it would appear as an entry in a CMS or theme editor's "add section" picker.**
5. **Template.** An ordered set of **page-level region slots** (header group, main, aside, footer group), the sections allowed in each, and the page's landmark skeleton. Composition only: it holds no content model of its own beyond page metadata.

**One sub-distinction inside tier 4, borrowed from EDS.** The **band** is the full-bleed page stripe that owns surface (light/dark/two-tone), vertical rhythm and the landmark decision. The **block** is the composition inside it. Shopify collapses the two; EDS separates them (section plus Section Metadata versus block). The practice should **contract them together but name them apart**, because the landmark rule in `components/section.md` attaches to the band, not the block. Twelve benefit blocks in one band make one landmark.

### Where the four borderline items land

| Item | Tier | Field evidence | Note |
|---|---|---|---|
| **Button group** | **2, composed** | A component in Polaris (slots `primary-action`, `secondary-actions`), Primer, Spectrum, Cloudscape and Material 3 Expressive (with a connected variant). An Atlassian subcomponent of Button. A wrapper class in GOV.UK. Layout guidance on Carbon's Button page. Curtis's canonical "explicit group." | Agrees with #4001. Its owned behaviour is **overflow** (Spectrum: "handles overflow"; M3: overflow into a menu) and ordering, which is what makes it more than a Stack. A group with no overflow and no ordering rule is just a Stack, and should be one. |
| **Card** | **2, composed** for the generic shell. A **domain card** (product, promo, metrics, article) is tier 2 *with a content model*, not a section. | Card is a component in Primer (with subcomponents), Spectrum (+ CardView), Carbon for IBM.com and Cloudscape (as a collection). **Polaris 2025 has no Card at all**: Section carries the surface, and specific cards are compositions. Atlassian and GOV.UK have none. Frost: a card is core, a product card is a recipe. Figma calls it a block. AEM's Teaser is the authorable card. | The most contested of the four. Its owned behaviour is the **stretched-link interaction** (the vault's `card` §6), which keeps it in tier 2. A **card grid** is a section (Carbon "Card group", EDS "Cards"). |
| **Date picker** | **2, composed** | Spectrum: "DatePickers combine a DateField and a Calendar popover," all three standalone. Carbon: field + calendar. Atlassian: Date time picker, Calendar separate. M3: components, with the field join left to the app. APG: a dialog + grid example. **Legacy Polaris called it a pattern** ("Date picking"); GOV.UK has a Date input component *and* a "Dates" pattern. | **The cleanest illustration of tier 3 sitting beside the ladder.** The picker is a composed component; "Dates" is the pattern that decides whether you need one. Legacy Polaris shipped the composition as a pattern because it had no composed DatePicker; that conflated the two tiers. |
| **Carousel** | **2, composed.** When used as a page region it is wrapped by a section (Shopify `slideshow` and `carousel`, EDS Carousel block). | A component in Material 3 (multi-browse, hero, full-screen) and Carbon for IBM.com. An AEM Core *container* component. Absent from Polaris, Atlassian, GOV.UK, Cloudscape, Primer and Spectrum. APG calls it a "pattern", in the widget sense, built from Tabs + Button. | **Absent from most product systems and present in every marketing/commerce platform**, which is the tier-4-surface signal again. Its owned behaviour (rotation, pause, slide picker, the APG semantics) keeps it in tier 2. The vault has no carousel brief: `tabs` and `pagination` both refer to it, and nothing defines it. |

## B. What a pattern contract holds, and what a section contract holds

### Pattern contract

The vault already has this shape: `patterns/_schema.md`, with an ALWAYS core of problem and context, composition (as typed references), decision rules and accessibility orchestration, plus SCALES sections. **We recommend the engine adopt it rather than re-derive it.** Three additions for engine use:

- **`realised-by`**: the composed components, sections or templates that instantiate the pattern, by contract id. This is what lets a pattern sit beside the ladder and still be machine-addressable. A sign-in form pattern is realised by a Form composition, an auth section and a sign-in template.
- **`rules` split into lintable and judgement.** Curtis's verifiability test, applied:
  - lintable: "the error summary precedes the first field and receives focus on submit"; "never more than one primary action";
  - judgement: "ask only for what you need".

  The lintable rules are the pattern's contract proper. The judgement rules are its guidance.
- **`copy`**: content rules with templated strings where the pattern owns them (GOV.UK's error-message formulas are the model). The vault's content-at-system-level work (04 and §1.31) is the home.

What a pattern contract **does not** hold: anatomy, tokens, layout options. Patterns that need those are being realised by something, and the realisation carries them.

### Section contract

#3999 lists four clauses: regions, allowed fillers, layout options, responsive behaviour. The platforms in §3 show **six more** are needed for portability to a CMS, and a seventh for accessibility. The proposed shape, each clause with the platform that already ships it:

1. **Identity and page role.**
   - id, name, aliases;
   - the **family**: hero, feature, social proof and so on (§C);
   - the **surface it is for**: marketing, commerce or app.
2. **Regions.** Each region gets four fields:
   - a name: media, eyebrow, headline, body, actions, proof, items;
   - required or optional;
   - **cardinality** as min and max (Shopify `max_blocks` and per-type `limit`, Storyblok and Sanity min/max);
   - **the allowed fillers** by contract id (Figma preferred instances, WordPress `allowedBlocks`, AEM Allowed Components, Storyblok allow/deny, Shopify `@theme`).
3. **Layout options** as **enumerated settings on one contract, never as separate contracts** (Contentful `validations.in`, EDS options, AEM Style System, WordPress `styles`, Shopify settings). From Prism3 `37` §2 the hero options are:
   - arrangement;
   - media side;
   - media kind;
   - content alignment;
   - surface;
   - action count.

   Each option gets its own allowed values, plus **the forbidden combinations**, which `37` calls the empty cells.
4. **Presets.** Named, curated combinations of option values and default fillers: Shopify presets, WordPress variations. **This is where a code kit's numbered variants (`hero-07`) map.** Each one is a preset of the contract, not a contract of its own. Presets are what the author picks. Options are what the contract permits.
5. **Content model.** The fields, their types, which are required, and the **author-editable versus system-fixed** line: WordPress overrides, Shopify static blocks, AEM dialog versus policy. #693 already established this is required for an AEM or EDS projection. Without it the contract cannot generate the authoring form.
6. **Placement rules.** Which templates or page regions may host it, and how many per page: Shopify `enabled_on` and `limit`, SFCC `region_definitions`.
7. **Landmark and heading contract.** This is the clause that makes the section contract the place the don't-over-landmark rule (`components/section.md`) is enforced rather than hoped for. It holds:
   - whether the band renders a named `<section>` landmark or a generic container;
   - where its accessible name comes from: the headline region, by `aria-labelledby`;
   - the heading level its headline takes, relative to its position in the template;
   - the `tag` choice (Shopify ships it as a schema attribute).
8. **Surface.** The colour scheme or band treatment the section may take: light, dark or two-tone (`37` §2; Dawn and Horizon colour schemes; AEM Container Background). Surface belongs to the **band**, and the fillers inherit it through token mode, not through props.
9. **Responsive behaviour.** Per brand breakpoint (`35`):
   - how regions reflow;
   - which options collapse (split → stacked);
   - which regions may hide.
10. **Limits and nesting.** The maximum nesting depth and whether a section may contain another section (Shopify: 8 levels of theme blocks; sections do not nest).

**What a section contract deliberately leaves out.** Each of these lives somewhere else:

- **Pixel anatomy, spacing values and token bindings** belong to the fillers' contracts and the layout primitives (`stack`, `grid`, `box`). The section names a spacing *rhythm* token, not values.
- **Any behaviour.** If the section needs behaviour, a composed component is missing.
- **Per-layout specs.** If two layout options need different specs, they are two families, or one option is really a preset.
- **Unverifiable prose** ("premium", "airy"), per Curtis.

### Template contract

This is the thinnest of the three, and it should stay thin:

- the page type (SFCC page types; Shopify JSON templates; Polaris App Home templates);
- ordered **page-region slots** (header group, main, aside, footer group, as with Shopify section groups) and which section families each accepts;
- a section cap (Shopify: 25 per template);
- the **landmark skeleton**: one `banner`, one `main`, one `contentinfo`, with navigation regions named.

That is all. A template holds no tokens and no content model beyond page metadata.

### Composed-component additions (tier 2), for completeness

The §15 shape gains a **`slots`** key with name, allowed fillers, cardinality and default-content note, and a **`subcomponents`** key. Both are SCALES. Per `components/_schema.md`, the shape is extended there first and then used.

## C. A base block catalog

**How the counts were made.** "How often the field ships it" counts **witnesses whose public catalogue names a section family**. It does not count variants. We used three witness sets:

- **Marketing (7):**
  - Tailwind Plus Marketing (TW)
  - Relume Marketing (RL)
  - WordPress core pattern categories (WP)
  - Shopify Dawn + Horizon (SH)
  - AEM EDS block collection (EDS)
  - Carbon for IBM.com layout components (CI)
  - Mantine UI page sections (MT)
- **Commerce (4):**
  - Tailwind Plus Ecommerce (TW)
  - Relume Ecommerce (RL)
  - Shopify Dawn + Horizon (SH)
  - Salesforce Page Designer page types (SF; vault file 10)
- **App (5):**
  - Tailwind Plus Application UI (TW)
  - Relume Application UI (RL)
  - shadcn blocks (SC)
  - Polaris App Home templates and compositions (PA)
  - Cloudscape patterns and demos (CS)

Counts come from names and are approximate. Where a family is folded into another under a different name, we counted it and say so. **These are frequencies of naming, not of use.** Adobe's ">50% of projects" rule needs project data the practice does not yet have (see the open items).

**Region names** follow one vocabulary throughout: eyebrow, headline, body, media, actions, proof, items, aside.

### Marketing

| Family | Regions (required in bold) | Common layout options | Composes | Witnesses (of 7) |
|---|---|---|---|---|
| **Hero** | **headline**, eyebrow, body, **actions** (0–2), media, proof (rating/avatar cluster *or* logo strip) | arrangement: beside / below / none / split-header; media side; media kind: image / video / multi-image / code; alignment start / center; surface; background media | Heading, Text, Button, Link, Image/Media, Avatar group, Rating, Logo | **7**: TW, RL, WP banner, SH image-banner/hero, EDS, CI Lead space, MT |
| **Header / navigation** | **brand**, **nav**, utilities (search, account, cart), announcement | stacked / inline; mega-menu yes/no; sticky | Navigation, Menu, Link, Button, Search field | **6** (MT not confirmed). Template-level: a page-region slot, not a body section |
| **Footer** | **nav columns**, legal, social, newsletter, locale | columns 2–5; condensed | Link list, Text, Icon button, Select (locale) | **6** (MT not confirmed). Template-level |
| **Feature grid / columns** | headline, body, **items** (2–n: icon/media + title + text + link) | columns 2/3/4; with media; alternating rows; bento | Card, Icon, Heading, Text, Link, Image | **7**: TW, RL, WP columns/services, SH multicolumn/multirow, EDS Columns, CI Feature section/Content block, MT |
| **Media with text** (split) | **media**, **headline**, body, actions | media side; ratio 50/50, 60/40; surface | Image/Video, Heading, Text, Button | **≈5**: SH image-with-text/media-with-content, EDS Columns, CI Callout with media, WP media, TW Content. Often folded into feature, so low confidence |
| **Contact / form** | headline, body, **form**, aside (address, map) | form beside info / stacked | Form, Text Field, Textarea, Select, Button | **6**: TW, RL, WP, SH contact-form, MT, EDS Form (deprecated) |
| **FAQ** | headline, **items** (question/answer) | single / two-column; with aside | Accordion, Heading, Text | **5**: TW, RL, SH collapsible-content, EDS Accordion, MT |
| **Blog / article list** | headline, **items** (post cards), actions | grid / list; featured-first | Card, Image, Tag, Text, Link | **5**: TW, RL, WP posts, SH featured-blog, MT Blog UI |
| **Carousel / slideshow band** | headline, **slides** | slides per view; auto-rotate off by default; hero vs content | Carousel, Card, Image | **4**: SH slideshow/carousel, EDS Carousel, CI carousel, MT (app set) |
| **CTA band** | **headline**, body, **actions** (1–2) | centered / split; surface; with media | Heading, Text, Button | **4**: TW, RL, WP call-to-action, CI CTA section. **EDS has no CTA block**; it is default content in a section |
| **Testimonial / quote** | **quote**, attribution (name, role, avatar), logo | single / grid / carousel | Blockquote, Avatar, Text, Image | **4**: TW, RL, WP, EDS Quote |
| **Gallery / video** | headline, **media items** | grid / masonry / single video | Image, Video, Embed | **4**: RL Gallery, WP gallery/media/video, SH collage/video, EDS Video/Embed |
| **Team** | headline, **people** | grid; with bios | Avatar, Card, Text, Link | **3**: TW, RL, WP |
| **Pricing** | headline, **tiers** (name, price, features, action), toggle (period) | 2–4 tiers; comparison table | Card, Segmented control, List, Button, Table | **2**: TW, RL. **Absent from every CMS and commerce witness** |
| **Logo wall** | headline, **logos** | grid / marquee | Image, Link | **2**: TW, RL. Often a hero *proof* region instead (`37` §2) |
| **Stats strip** | headline, **stats** (value + label) | 2–4 across; with body | Stat (unbriefed), Text | **2**: TW, RL |
| **Newsletter / email capture** | **headline**, **field + action**, legal | inline / stacked; surface | Text Field, Button, Inline Message | **2**: TW, SH. Often folded into CTA or footer |
| Long tail (1 witness each) | — | — | — | Bento (TW), timeline / comparison / career / event / portfolio (RL), marquee / product hotspots (SH Horizon) |

**The marketing finding.** The families every authoring platform ships are **hero, feature/columns, media-with-text, FAQ, contact and carousel**. **Pricing, stats and logo wall** appear only in the SaaS-marketing code kits. The vault's 09 §1.36 named pricing, logo wall and stats as typical marketing blocks; the CMS witnesses say they are **SaaS-genre**, not general marketing. For an agency weighted to commerce and brand sites, they are second wave.

### Commerce

| Family | Regions | Common layout options | Composes | Witnesses (of 4) |
|---|---|---|---|---|
| **Product grid / listing** | headline, toolbar (sort, count), **items** (product cards), pagination / load more | columns 2–4; list / grid toggle; with facets aside | Product card, Select, Pagination, Badge | **4**: TW Product Lists, RL Product List Sections, SH featured-collection/product-list/main-collection, SF Category page |
| **Product detail (buy box)** | **gallery**, **title / price / rating**, **variant selection**, **quantity + add to cart**, delivery promise, details (accordions) | gallery side; gallery thumbs / stacked / carousel; sticky buy box; sticky mobile buy bar | Image, Carousel, Rating, Price, Radio/Swatch, Select, Stepper, Button, Accordion, Inline Message | **4**: TW Product Overviews, RL Product Headers, SH main-product/product-information, SF Product page |
| **Facets / filters** | **facet groups**, applied-filter chips, clear-all | sidebar / top bar / drawer on mobile | Checkbox, Radio, Slider, Tag, Drawer, Accordion | **4**: TW Category Filters, RL Category Filters, SH (facets in main-collection), SF Search Results page |
| **Category / collection links** | headline, **collection tiles** | grid / carousel / list | Card, Image, Link | **3**: TW Category Previews, SH collection-list/collection-links, SF Category page entry points |
| **Cart** | **line items**, **summary**, actions, upsell | page / drawer | Table or List, Stepper, Button, Price | **2**: TW Shopping Carts, SH main-cart/cart-drawer. Platform-owned in SF |
| **Recommendations** | headline, **product cards** | grid / carousel | Product card, Carousel | **2**: SH related-products/product-recommendations, TW (inside Product Overviews). Always on the PDP skeleton (09 §1.36) |
| **Reviews** | summary (average, distribution), **review items**, actions | summary beside list / stacked | Rating, Progress, Avatar, Text, Pagination | **2**: TW Reviews, SH Horizon review block. Usually a third-party embed in practice |
| **Promo / incentives** | headline, **incentive items** (icon + text), media | strip / grid / announcement bar | Icon, Text, Banner | **2**: TW Promo Sections + Incentives, SH announcement-bar |
| **Product features / specs** | headline, **spec items** or media/text pairs | alternating / table / accordion | Table, Accordion, Image, Text | **1**: TW. On the PDP skeleton in practice |
| Platform-owned, not section-shaped | — | — | — | Checkout (TW Checkout Forms; Shopify checkout is not a theme section), Order summary and history (TW), Quickview (TW): flows and overlays, not sections |

**The commerce finding.** **Four commerce families are named by every commerce witness: listing, product detail, facets and category links.** Product detail is not one section. It is a template that owns five or six regions, each of which is a section or a composed component. Shopify's `main-product` is one section with roughly 20 block types. SFCC's Product page is a page type. Horizon splits it into product-information plus blocks. **The practice should model the PDP as a template with a fixed region skeleton, not as a hero-like section with layout options.** That resolves the 09 §1.36 observation ("high variation over a shared skeleton") into a specific tier.

### App

| Family | Regions | Common layout options | Composes | Witnesses (of 5) |
|---|---|---|---|---|
| **Data table / resource index** | page header, toolbar (search, filters, bulk actions), **table**, pagination, empty state | table / cards view; split view | Table, Search field, Menu, Pagination, Empty state | **5**: TW Lists/Data Display, RL Tables, SC dashboard (data table), PA Index template + Index table, CS Table view |
| **Metric / stat cards** | **metric items** (value, label, delta, sparkline) | 2–4 across; with chart | Card, Text, Badge, Chart | **5**: TW Stats, RL Stat Cards, SC dashboard section cards, PA Metrics card, CS Service dashboard |
| **App shell** | **nav** (sidebar or top bar), **main**, header, aside | sidebar / stacked / multi-column; collapsible | Side navigation, Menu, Avatar, Search | **4**: TW Application Shells, RL Shells/Sidebars/Topbars, SC Sidebar (16), CS (App layout). **Already briefed as `patterns/app-shell.md`** |
| **Detail / description page** | header, **description list**, related tables, actions | single / tabs / split | List, Tabs, Table, Button | **4**: RL Description Lists, PA Details template, CS Details / Resource details, TW (Data Display; UNVERIFIED) |
| **Page header** | **title**, breadcrumbs, description, actions, tabs | with or without tabs; with metadata | Heading, Breadcrumbs, Button, Tabs | **3**: TW Headings, RL Page/Section/Card Headers, CS Hero header |
| **Create / edit form** | header, **form sections**, actions bar | single / multipage | Form, Field family, Button | **3+**: RL Forms, CS Create/Edit resource + Multipage create, TW Forms. Covered by `patterns/forms-as-a-system.md` |
| **Settings** | nav (sections), **settings groups**, save bar | single page / tabbed / side-nav | Form, Switch, Side navigation | **3**: PA Settings template, TW Page Examples, CS (edit resource). Ant Design's templates also list Form page |
| **Dashboard** | header, **widgets** grid | fixed / configurable | Card, Chart, Table | **3**: SC dashboard-01, CS Configurable/Service dashboard, Ant Workbench |
| **Auth (sign-in / sign-up)** | **form**, brand, aside (media/testimonial) | centered card / split with media | Form, Text Field, Button, Link | **2**: RL Sign Up / Log In, SC login (5) + signup (5). Carbon has a Login pattern |
| **Onboarding / setup guide** | **steps** with progress, actions | checklist / wizard | Progress, Checkbox, Card | **2**: RL Onboarding Forms, PA Setup guide |
| **Empty / error page** | **message**, illustration, actions | in-region / full page | Empty state, Button | Product systems treat it as a **pattern** (Polaris, Cloudscape, Primer, Carbon, Atlassian), and GOV.UK as a "Pages" pattern. Already `patterns/view-state-orchestration.md` |

**The app finding.** **App "blocks" are mostly the vault's existing `patterns/`**: app shell, forms-as-a-system, view-state orchestration and search orchestration. Under another name they are the vault's layout-and-shell and composition tiers. **The block concept adds little to app surfaces.** Polaris App Home and Cloudscape call them templates and compositions, and Prism3's tier 5 plus the vault's patterns already cover them. Two app families have no vault home yet: **metric cards** and the **resource index** as a page. The resource index is a pattern ("view resources") realised by a template.

### What the catalog leaves out

These are the empty cells, which `37` says carry more than the filled ones:

- **No witness ships a section-level accessibility contract.** Shopify's `tag` attribute is the only landmark control in any schema, and it is a free choice. Nothing anywhere states the one-landmark-per-band rule. **The practice's section contract would be the first to make it a clause.**
- **No marketing witness ships a form in the hero** (`37` §2, still open). Email capture lives in CTA, newsletter or footer.
- **Personalisation slots are absent.** No witness declares a region as personalisable or variant-tested, though AEM Experience Fragments support "channel or context-specific variations." In composable commerce (10) this is where the variance lives. It is a gap in the field, not just the vault.
- **Localisation constraints are absent.** No section schema declares text-expansion budgets or RTL mirroring per option. Shopify `locales` covers strings only. The mirror rule (Prism3 #3986) would need a clause.

### Prune rule and first wave (proposal)

Adopt Adobe's rule as the long-run test: **a family earns inclusion by being used on more than half of the practice's projects.** We cannot apply it yet, because the practice has no project census. Until it can, use **witness frequency weighted to our surfaces**:

- **First wave (commerce-weighted):** hero, feature/columns, media with text, product grid, product detail (as a template), facets, category links, CTA band, FAQ, header and footer (as template regions).
- **Second wave:** carousel band, testimonial, contact, blog list, recommendations, promo/incentives.
- **SaaS-genre, on demand:** pricing, stats, logo wall, bento, team.

The first wave implies **component briefs the catalogue does not have**: Carousel, Button group, Rating, Price, and a swatch / variant picker. The second and on-demand waves add Stat, Logo and Quote/Blockquote.

---

## What this run corrects or contests

- **Prism3 #4001, tier 3 placement.** The pattern tier is not a rung between composed component and section. It sits beside the ladder, and it can be realised at any scale (§A). This does not change the build order; it changes the contract (`realised-by`).
- **Prism3 #4001, tier 2 contract.** It says "slots and allowed fillers." The contract should also state **cardinality**. Default content is explicitly outside it (Curtis).
- **Prism3 #3999, missing clauses.** The section contract should add:
  - the content model with an author-editable/fixed line;
  - presets;
  - placement rules;
  - the landmark/heading clause;
  - surface;
  - nesting limits.

  The first two are what make it portable to Shopify, AEM, WordPress and the headless CMSs. The landmark clause is what makes it accessible by construction.
- **03 open question 7.** It reads Figma (2025) as arguing that cards, headers and carousels are the right *tier*. Figma's "block" means pre-composed, and its three examples span tiers 2 and 4.
- **09 §1.36.** It lists pricing, logo wall and stats among the typical marketing blocks. The CMS and commerce witnesses don't ship them; they are SaaS-genre.
- **09 §1.36 and issue #10, facet versus layer.** The lean was "facet on `patterns/`." The evidence now leans the other way. Sections:
  - are keyed to page role, not goal;
  - carry a content model, options and presets that the pattern spine has no keys for;
  - are the one tier every authoring platform formalises.

  #10's own test ("can a hero brief fill the ALWAYS core without forced sections") is likely to fail on *decision rules* and *accessibility orchestration* as pattern-shaped sections. A hero's decisions are option constraints. Its accessibility clause is one landmark rule. **Lean layer: a `sections/` directory with its own `_schema.md`** next to `components/` and `patterns/`. This is a recommendation for the owner, not a decision.

## Proposed promotion target

**A new numbered file, `36-composition-tiers-and-sections.md`**, with targeted edits to 03, 10 and the catalogues. It should not go into 03 alone. Our reasoning:

- 03 is the component phase. The tier model spans components, `patterns/`, sections and templates, and its section half is CMS-shaped (10) as much as component-shaped.
- 03 is already 233 lines of system-level component model. A tier model plus a section contract plus a catalog roughly doubles it, and most of that is not about components.
- The precedent is 29 and 30, which split per-component documentation out of 04 when it became its own topic area.

The promotion would then:

- **36:**
  - the tier definitions and the four-axis disagreement;
  - the borderline placements;
  - the pattern, section and template contract shapes;
  - the base catalog and the prune rule;
  - the "pattern" homonym;
  - the commercial note from #10, that a block library is the most visible deliverable and not the most valuable.
- **03:**
  - close open question 7 with a cross-reference to 36;
  - add a one-paragraph tier summary under Composition;
  - correct the Figma reading.
- **10:** a cross-reference from "The DS-vs-block-pattern boundary" and "Page Designer's component model" to the section contract.
- **`components/_schema.md`:** the SCALES `slots` and `subcomponents` keys for tier 2, after the owner agrees.
- **`patterns/_schema.md`:** the `realised-by` key and the lintable/judgement rules split.
- **09:** close §1.36 and the new entry once 36 lands. Issue #10 is decided in 36.

## Open and unverified register

- **UNVERIFIED:**
  - Tailwind Plus counts and Application UI sub-lists (login wall);
  - Horizon's primary announcement;
  - the Figma slots GA date of 28 May (the primary changelog shows 10 Jun 2026);
  - Carbon React `ButtonSet` and Tile as Carbon's card;
  - the full Atlassian patterns list;
  - Fluent 2 and SLDS templates;
  - Ant ProComponents details;
  - Curtis's *Subcomponents* and *Components Versus Patterns* posts (snippets only);
  - Mall's rule of three (snippets only);
  - Frost's "labels have never been the point" (quoted secondhand).
- **Needs a `_source-text/` capture before promotion:**
  - shopify.dev section schema and limits;
  - aem.live block collection;
  - WordPress pattern registration and overrides;
  - Frost's ecosystem and recipes posts;
  - Polaris App Home patterns;
  - Curtis's slots posts beyond the one captured.
- **Not yet answerable:**
  - the >50%-of-projects prune rule needs a practice project census;
  - marketing frequencies come from names, not markup, and `37`'s method (read markup, name the empty cells per family) is still owed per family in Prism3 #693.
- **Single-agent run.** An external half under the same prompt would test the four-axis reading and the "pattern beside the ladder" claim, which are this run's two least conventional positions.

## References

Accessed 2026-11-18 unless dated otherwise.

**Figma**
- *How design systems power the new pace of product development* — https://www.figma.com/reports/design-systems-power-the-pace/ (gated; c. Nov 2025; text in `_source-text/ext-figma-ai.txt`)
- *5 shifts redefining design systems in the AI era* — https://www.figma.com/blog/5-shifts-redefining-design-systems-in-the-ai-era/ (19 Nov 2025)
- Simple Design System — https://github.com/figma/sds
- Slots open beta — https://forum.figma.com/product-updates-3/slots-is-rolling-out-in-open-beta-51584 (5 Mar 2026)
- Slots GA — https://developers.figma.com/docs/plugins/updates/2026/06/10/update/ (10 Jun 2026)
- Use slots — https://help.figma.com/hc/en-us/articles/38231200344599
- Figma Sites blocks — https://help.figma.com/hc/articles/31242773374615

**shadcn/ui**
- Blocks launch — https://ui.shadcn.com/docs/changelog/2024-03-blocks (Mar 2024)
- Registry item schema — https://ui.shadcn.com/docs/registry/registry-item-json
- Registry — https://ui.shadcn.com/r/styles/new-york-v4/registry.json

**Block kits**
- Tailwind Plus — https://tailwindcss.com/plus/ui-blocks
- Relume — https://www.relume.ai/components
- Mantine UI — https://ui.mantine.dev/
- Untitled UI — https://www.untitledui.com/react/marketing

**Shopify**
- Section schema — https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema
- JSON templates — https://shopify.dev/docs/storefronts/themes/architecture/templates/json-templates
- Section groups — https://shopify.dev/docs/storefronts/themes/architecture/section-groups
- Limits — https://shopify.dev/docs/storefronts/themes/architecture/limits
- Theme blocks — https://shopify.dev/docs/storefronts/themes/architecture/blocks/theme-blocks
- Static blocks — https://shopify.dev/docs/storefronts/themes/architecture/blocks/theme-blocks/static-blocks
- Partner blog — https://www.shopify.com/partners/blog/themeblocks (31 Jan 2024)
- Dawn — https://github.com/Shopify/dawn/tree/main/sections
- Horizon — https://github.com/Shopify/horizon

**AEM**
- Core Components introduction — https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/introduction (updated 16 Oct 2026)
- Teaser and Container (updated 13 May 2026)
- Experience Fragments — https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/fragments/experience-fragments (updated 9 Oct 2026)
- EDS block collection — https://www.aem.live/developer/block-collection
- Markup — https://www.aem.live/developer/markup-sections-blocks
- Component models — https://www.aem.live/developer/component-model-definitions

**WordPress**
- Registering patterns — https://developer.wordpress.org/themes/patterns/registering-patterns/ (updated 15 Jul 2024)
- Block metadata — https://developer.wordpress.org/block-editor/reference-guides/block-api/block-metadata/
- Overrides — https://developer.wordpress.org/news/2024/06/an-introduction-to-overrides-in-synced-patterns/ (Jun 2024)

**Headless CMSs and Builder.io**
- Storyblok blocks — https://www.storyblok.com/docs/concepts/blocks (updated 13 Oct 2026)
- Storyblok fields — https://www.storyblok.com/docs/concepts/fields (updated 28 Sep 2026)
- Sanity array — https://www.sanity.io/docs/studio/array-type
- Contentful modelling patterns — https://www.contentful.com/help/content-models/content-modeling-patterns/
- Contentful layout structures — https://contentful.com/developers/docs/experiences/layout-structures
- Contentful patterns — https://www.contentful.com/help/studio/experiences/create-a-pattern/
- Contentful custom components — https://contentful.com/developers/docs/experiences/register-custom-components
- Builder.io — https://www.builder.io/c/docs/custom-components-setup

**Frost and Atomic Design critiques**
- Frost, *Atomic Web Design* — https://bradfrost.com/blog/post/atomic-web-design/ (10 Jun 2013)
- Frost, *Atomic Design* ch. 2 — https://atomicdesign.bradfrost.com/chapter-2/ (2016)
- Frost, *Extending Atomic Design* — https://bradfrost.com/blog/post/extending-atomic-design (10 Jul 2019)
- Frost, *The design system ecosystem* — https://bradfrost.com/blog/post/the-design-system-ecosystem/ (21 Sep 2023)
- Frost, *The art of design system recipes* — https://bradfrost.com/blog/post/the-art-of-design-system-recipes/ (22 Apr 2024)
- Frost, on Mall's content and display patterns — https://bradfrost.com/blog/link/content-and-display-patterns (4 Jan 2016)
- Walton, *Atomic Classification* — https://trentwalton.com/2016/02/26/atomic-classification (26 Feb 2016)
- Sparkbox, *Iterating on Atomic Design* — https://sparkbox.com/foundry/iterating_on_atomic_design (1 Nov 2024)
- Qt blog — https://www.qt.io/blog/atomic-design-systems-why-the-labels-dont-matter (26 Nov 2025; secondary)

**Curtis**
- *Slots in Design Systems* — https://nathanacurtis.substack.com/p/slots-in-design-systems (7 Nov 2025)
- *Figma Slots for Repeating Items* — https://nathanacurtis.substack.com/p/figma-slots-for-repeating-items (23 Jan 2026)
- *Configuration Collapse* — https://nathanacurtis.substack.com/p/configuration-collapse (27 Feb 2026)
- *Implementing Slots in a Figma Library* — https://nathanacurtis.substack.com/p/implementing-slots-in-a-figma-library (2 Mar 2026)
- *Component Examples as Data* — https://nathanacurtis.substack.com/p/component-examples-as-data (26 May 2026)
- *Component Contracts and Schemas* — https://nathanacurtis.substack.com/p/component-contracts-and-schemas (28 Jul 2026; `_source-text/ext-curtis-contracts-and-schemas.txt`)
- *Component and Part Roles as Composites* — https://nathanacurtis.substack.com/p/component-and-part-roles-as-composites (28 Sep 2026)

**Design systems**
- GOV.UK components — https://design-system.service.gov.uk/components/
- GOV.UK patterns — https://design-system.service.gov.uk/patterns/
- Material canonical layouts — https://developer.android.com/develop/adaptive-apps/guides/canonical-layouts
- Polaris App Home patterns — https://shopify.dev/docs/api/app-home/patterns
- Polaris web components GA — https://shopify.dev/changelog/polaris-unified-web-components-are-now-stable (1 Oct 2025)
- Polaris ButtonGroup — https://shopify.dev/docs/api/app-home/polaris-web-components/actions/buttongroup
- Carbon patterns — https://carbondesignsystem.com/patterns/overview/
- Carbon for IBM.com components — https://www.ibm.com/standards/carbon/components/overview
- Carbon for IBM.com Content block — https://www.ibm.com/standards/carbon/components/content-block
- Cloudscape patterns — https://cloudscape.design/patterns/
- Cloudscape demos — https://cloudscape.design/demos/overview/
- Primer UI patterns — https://primer.style/product/ui-patterns/
- SLDS resources — https://trailhead.salesforce.com/content/learn/modules/lightning-design-system-basics/explore-slds-resources
- React Spectrum — https://react-spectrum.adobe.com/llms.txt
- Ant Design spec — https://ant.design/docs/spec/overview

**W3C**
- APG Carousel — https://www.w3.org/WAI/ARIA/apg/patterns/carousel/
- APG date picker dialog — https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/datepicker-dialog/
- WAI carousels tutorial — https://www.w3.org/WAI/tutorials/carousels/ (updated 13 Apr 2017)

**Vault and Prism3**
- Vault: 03, 09 §1.36 / §2.3, 10, `components/_schema.md`, `components/section.md`, `components/card.md`, `components/form.md`, `components/date-picker.md`, `patterns/_schema.md`, `patterns/app-shell.md`.
- Prism3: #4001, #3999, #693, `docs/37-block-layout-axes.md`.
