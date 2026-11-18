# Prompt — blocks, sections and the tiers above the component (2026-11-18)

Filed against knowledge-base issue #65 (intake from the Prism3 engine, owner decision Q-BL1 A, 2026-11-18). Single-agent run so far: the Claude half is `claude.md`. An external half can be added under the same prompt, per `_research/README.md`; the prompt below is the one to send unchanged.

---

```
You are researching the tiers between an atomic UI component and a full
page — composed components, patterns, sections (blocks) and templates —
for a senior design systems practitioner at a digital agency whose work
is weighted to commerce and CMS-authored marketing sites. The output is a
structured knowledge document.

The practitioner's engine has just adopted a five-tier model: (1) atomic
component, one job, own anatomy, full component contract; (2) composed
component, own frame and behavior, built from atomics with named slots,
full contract plus slots and allowed fillers; (3) pattern, a task-level
recurring solution — rules, order, copy, few visuals; (4) section/block,
a page region with layout options, a looser "section contract" recording
regions, which components may fill each region, layout options and
responsive behavior; (5) template/page, composition only. Test that model
against the field rather than restating it. This is not an introductory
guide — assume the reader knows Atomic Design, slots, and what a CMS
content model is.

Research scope — cover all of the following, with dated, linked primary
sources:

1. Figma's 2025 argument for blocks
   - The report recommending "larger, reusable blocks like headers, cards,
     or carousels" as the unit for AI generation
   - Figma native slots (2025–2026) and what they change about composed
     components and repeating items

2. Code-side block distributions
   - shadcn/ui blocks and the registry item model
   - Tailwind Plus marketing / ecommerce / application UI categories
   - Any other library that names its own variants

3. Commerce theme and CMS section models
   - Shopify Online Store 2.0 sections and blocks, theme blocks, section
     schema, presets, limits, section groups
   - Contentful, Sanity, Storyblok, AEM (Core Components, Edge Delivery
     Services block collection), WordPress block patterns and template
     parts, Salesforce Page Designer
   - For each: the unit's name, what its schema declares, and how layout
     variation is expressed (a setting, or a separate block)

4. Atomic Design and its critiques
   - Frost's five stages and what he later said about them
   - The molecule/organism ambiguity; GOV.UK's styles/components/patterns;
     Mall's element/component/pattern; Frost's ecosystem "recipes" layer

5. Contracts, schemas and slots
   - Nathan Curtis on component contracts and schemas (2026), on slots and
     repeating items, and on subcomponents
   - What a contract can hold at a tier with no pixel anatomy

6. How major systems name and ship the upper tiers
   - Material 3, Polaris, Atlassian, Carbon (and Carbon for IBM.com),
     GOV.UK, Fluent, Spectrum, Cloudscape, Primer, Lightning
   - Where button group, card, date picker and carousel land in each

Answer three questions directly:
  A. How should each tier be defined? Where does the field disagree?
     Where do button group, card, date picker and carousel land?
  B. What does a pattern contract hold? What does a section contract hold?
  C. A base block catalog for marketing, commerce and app surfaces: names,
     regions, common layout variants, the components each composes, and how
     often the field ships each.

Output format: Structured markdown, headings matching the scope. Synthesize
— do not list sources mechanically. Where the field has consensus, say so;
where it is context-dependent, give a decision framework rather than a
winner. Date every claim that depends on current vendor state and give the
verification path. Include a references section of primary sources.

Depth: Expert audience. Do not explain what a slot or a CMS is — explain
where the tier lines fall, what each contract must carry to be portable
across code, Figma and a CMS, and what the catalog leaves out.
```
