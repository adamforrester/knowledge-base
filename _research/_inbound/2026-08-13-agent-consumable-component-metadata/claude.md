# Claude run — failures in agent-consumable component metadata (2026-08-13)

Raw output, unedited. Findings only; no recommendations, per the brief. Every external claim carries a
source that was opened during this run. Where a claim could not be verified it is marked, not softened.

**Provenance discipline used throughout:** vendor documentation and package registries are treated as
primary; vendor marketing pages as positioning; third-party blogs as secondary and labelled as such.
Two pages returned 403 to this run and their content is reported second-hand with that noted.

---

## The shape of the evidence, before the four answers

**Almost nobody publishes numbers about their own payloads.** Across every candidate, exactly one hard
size figure for a component/design metadata surface was found in vendor documentation, and it is a
failure message rather than a specification. The category talks about token efficiency constantly and
measures it publicly almost never.

**The most reliable signal was not complaints — it was shipped remedies with dates.** Marketing says a
system is agent-ready; a changelog entry adding a scoping layer nine months after the export pipe says
undifferentiated exposure did not work. The second is evidence, the first is a claim.

**And one named candidate is dead.** backlight.dev carries the notice *"Backlight.dev is shutting down
June 1st 2025"* (backlight.dev, fetched 2026-08-13), for what it described as *"a unique, all-in-one
design system solution."* No reason is given on the page. It is the category's bluntest datapoint and
its causes are not public.

---

## 1. Context and payload size

### The one hard number, and it is in a vendor's own troubleshooting docs

Figma's developer documentation, page *"MCP clients issues"* (developers.figma.com, fetched
2026-08-13), documents this verbatim:

> "Error: MCP tool "get_design_context" response (351378 tokens) exceeds maximum allowed tokens
> (25000)."
>
> "Please use pagination, filtering, or limit parameters to reduce the response size."

**351,378 tokens against a 25,000 limit — roughly 14× over.** Two things about it are more interesting
than the number.

**First, the recommended remedy is to raise the client's ceiling, not to shrink the payload.** Figma's
documented fix is to increase `MAX_MCP_OUTPUT_TOKENS` "to a higher threshold (suggesting `50000` or
`100000`)". **Both suggested values are between three and seven times smaller than the error they are
offered as the fix for.** Whether that is an oversight or an implicit expectation that the 351k case is
pathological, the published guidance does not close the gap it documents.

**Second, the payload is treated as irreducible.** The error text advises pagination and filtering, but
the remedy Figma actually gives the user is a client configuration change. The design position is that
the response size is the consumer's problem.

### The same source data, the opposite design goal

Directed Edges' Specs — built to extract component specifications from Figma, the same upstream — states
its goal as the inverse (github.com/DirectedEdges/specs, fetched 2026-08-13):

> "compact, schema-valid specs — sidestepping the cost and errors of agentic Figma extraction"
>
> "The result is a spec that's compact yet complete — not noisy like Figma's REST API"

**Two tools over the same design data, one advertising 351k-token responses as a client-side problem
and the other selling compactness against "noisy" as its differentiator.** That contrast is the
clearest thing found in this pass, and neither side publishes a comparative measurement.

### Explicit tiering, from the largest system in the set

Astryx (Meta) — *"the most-used and largest design system in the company — powering 13,000+ apps"*,
150+ components — ships tiering as first-class CLI surface (astryx.atmeta.com/docs/cli and
packages/cli/README.md, both fetched 2026-08-13):

- `--detail <level>` with three levels: `brief` (names only), `compact` (names + one-line descriptions), `full` (complete documentation)
- `--dense` — described verbatim as *"Compressed format (token-efficient, useful for AI agents)"*
- `--json` for typed envelopes, and a **manifest** so, in its own words, *"Agents don't have to scrape `--help` to learn the CLI."*

**This is the most developed tiering design found.** It is also the clearest case of the pattern above:
the flags exist, the intent is stated in the docs, and **no file sizes, token counts or context
requirements are published anywhere on those pages.** The mechanism is documented; its necessity is
asserted rather than shown.

### The platform vendors converged on scoping and retrieval — one of them visibly late

**Supernova's changelog is the strongest behavioural evidence in this pass** (learn.supernova.io/changelog,
fetched 2026-08-13). In sequence:

| date | entry |
|---|---|
| September 2025 | *"Introducing Supernova Relay"* — "Our official remote MCP server is here!" |
| November 2025 | *"Export project data to MCP"* — "Stream your Supernova features and documents directly into AI coding assistants." |
| **June 2026** | **"Contexts: control what AI reads from your design system"** — *"Governance layer for AI guidelines: give each team and agent the right part of your design system."* |

**The pipe shipped first; the ability to send only part of the system arrived roughly nine months
later.** No blog post says "we shipped too much context." The changelog says it by what it adds.

The accompanying post (supernova.io/blog/we-just-shipped-ai-context-management, fetched 2026-08-13)
frames it as *"Not every team needs the same information"* and claims *"Reduced token usage; each team
gets only the context they need."* It contains **no numbers of any kind** — no context sizes, no token
counts, no before/after.

**zeroheight's tool surface is retrieval-shaped while its marketing page is aggregation-shaped.** The
public MCP page (zeroheight.com/mcp, fetched 2026-08-13) leads with *"Your whole system in one MCP"* and
publishes no sizes, limits or retrieval detail — the page describes what the MCP prevents, not how it
sizes anything. The tool list reported in search results is `list-pages`, `get-page`, `get-page-images`
and `list-releases` — an index-then-fetch design rather than a bulk dump. **Provenance caveat: the
zeroheight help article documenting those tools returned HTTP 403 to this run**, so the tool names are
second-hand and were not read at source.

### Ecosystem-level, and the numbers here are secondary sources

The problem is not specific to design systems. Reported figures, **all from third-party blogs rather
than vendor docs and flagged accordingly**: GitHub's official MCP server consuming ~17,600 tokens of
tool definitions per request; three servers connected simultaneously consuming ~143,000 of a 200,000
context on schema definitions alone (~71%); a platform exposing 270+ tools costing ~17,500 tokens before
the first question. Treat the magnitudes as indicative, not established.

The protocol-level response is dated and checkable: **MCP Tool Search, January 2026** — when tool
definitions exceed roughly 10% of the context window the client defers loading them and the model
discovers tools on demand. **That is the ecosystem conceding that bulk definition loading does not
scale**, and it arrived after most of the design-system MCP servers in this set had shipped.

### What nobody has

**Not one candidate publishes a measured size for its own component metadata surface.** Not Astryx, not
Supernova, not zeroheight, not Knapsack, not Specs. The only hard figure in the pass is Figma's error
message. **Any claim of the form "our metadata is token-efficient" in this category is currently
unfalsifiable from published material.**

---

## 2. Schema churn

### The most widely deployed component metadata generator does not version its output

react-docgen — the engine under Storybook's React props tables and much else — has changed its output
shape across majors, and its release notes (react-docgen.dev/docs/release-notes/react-docgen, fetched
2026-08-13) show **no output-format versioning mechanism**:

- **v6** — `parse` return type *"now always returns an array regardless of resolver"*; `parse` arguments reduced from five to two; `DocumentationBuilder.toObject()` renamed to `build()`; `handlers`/`resolver`/`importers` renamed to `builtinHandlers`/`builtinResolvers`/`builtinImporters`; function-based resolvers replaced with classes.
- **v7** — `getTypeFromReactComponent` returns *"array of paths to types instead of just one"*, migration given as `if (type)` becoming `if (type.length > 0)`.

**The always-an-array change is a change to the data consumers parse, shipped as an API major with no
separate schema version.** A consumer of the *generated metadata* has no version field to branch on.

### Storybook: two changes, and the second is the dangerous kind

**Configuration churn.** `docs.autodocs = false` worked in 8.x and *"will no longer work in 9.0"*; the
migration is to remove the `autodocs` tag instead (Storybook 9 migration material, fetched 2026-08-13).
Loud, documented, fixable.

**Silent surface shrinkage.** In the same release, for Svelte, *"argTypes are no longer automatically
generated for slots and events defined with `on:my-event`."* **That is a metadata surface getting
smaller without the consumer getting an error** — the props table simply has less in it. This is the
failure mode that matters for agent consumption: not a break, a quiet reduction in what the machine can
see.

**And a fidelity change with no schema change at all.** Storybook 8 switched the default React docgen
from `react-docgen-typescript` to `react-docgen`. The stated reason is cost — *"disabling TS-based
docgen alone improved Storybook build speeds by 25% to 50%!"* — and the stated tradeoff is fidelity:
*"There are certain patterns that it doesn't handle as well, but the speed is worth it in most cases"*
(storybook.js.org/blog/optimize-storybook-7-6/, fetched 2026-08-13). A maintainer in discussion #29021
puts it as *"`react-docgen` has Typescript support, although it is not as fully-fledged as
`react-docgen-typescript`"*, in a thread where a user upgrading 7.6.7 → 8.2.9 reported reload times of
about 20 seconds and *"It's absolutely impossible to use storybook like this"* (fetched 2026-08-13).

**The generalisable finding: the payload's *accuracy* changed because of a *performance* decision, and
no schema version moved.** A consumer reading the props table gets different data before and after,
with nothing in the data saying so.

### The one system doing decision records, and it still has no version

Directed Edges' Specs ships `@directededges/specs-schema` (JSON schema + TypeScript types) and discusses
schema modification through **Architectural Decision Records in an `adr/` directory** — but **no explicit
versioning mechanism, no backwards-compatibility or breaking-change protocol** is documented in what was
fetched (github.com/DirectedEdges/specs, 2026-08-13). Its own positioning describes evolving *"into a
robust engine to produce and version specs over time"*, which reads as intent rather than shipped
policy.

**This is worth flagging against this vault's own register:** `09` §1.35 files the absence of an ADR
equivalent for `.ai.json`'s schema as an open gap. Specs is the field example of the ADR half — and it
demonstrates that ADRs alone do not give consumers a version to branch on. **The two halves are
separable, and the field example has only one of them.**

### The direct answer to the brief's question

**No candidate was found that versions a component *name surface* separately from its *content*.** The
split this repo runs — `ENGINE_VERSION` for "what code produced this" against `CONTRACT_VERSION` for
"can my app still resolve the names it references" — has **no peer in this set**. What exists instead is
package semver covering everything at once, and in react-docgen's case not covering the output shape at
all.

Supernova's changelog documents **no breaking changes, deprecations or schema migrations** in what was
fetched. That is either genuinely none or not published; **the two are indistinguishable from outside**,
and for a platform whose data consumers depend on, the absence of a published compatibility record is
itself the observation.

---

## 3. The metadata-versus-implementation split

### The clearest documented move is toward one authored file per component, colocated and typed

**Astryx** keeps a `{Name}.doc.mjs` beside each component under `packages/core/src/`, exporting a typed
`ComponentDoc`. Two details matter:

- **It explicitly replaced per-component `README.md`.** The direction of travel is documented: prose file out, typed data file in.
- **Its failure modes are validation failures, not silent ones.** A component's docs *"can fail validation if the `.doc.mjs` file is malformed"*, and *"a component can exist but have no typed `.doc.mjs` file"* — the second being the gap-shaped failure, where the component is real and the machine-readable record is simply absent.

One registry is built from those files and drives docsite navigation, search and CLI output —
one source, several projections.

**Storybook is split by construction rather than by choice**: the component, the CSF story file, and the
*generated* docgen output. The generated part is derived, which is exactly why the Storybook 8 default
change altered the payload without anybody editing a doc.

**Specs** ships schema, types and CLI as separate packages, with spec-per-component implied by its own
throughput claim (*"Generate 50 component specs in a minute"*), though the repo material fetched does
not state the file layout explicitly.

**Drupal SDC** — from the prior pass in this vault — is one directory per component: `*.component.yml`
schema, `*.twig`, optional CSS/JS. The schema and the implementation live together and the render system
validates one against the other.

### What determined the split, where it is observable

Where a reason is documented at all, it is **who writes it**: authored intent stays with the component
(Astryx's `.doc.mjs`, SDC's `component.yml`), while anything *derived* from the implementation is
generated at build time and not stored beside it. **No case was found of a system that started with
several files per component and consolidated to one.** Astryx's README → `.doc.mjs` move is the only
documented direction change in the set, and it is a format change rather than a count change.

---

## 4. Consistency across a catalogue

**The brief predicted this would be the thinnest area. That is confirmed, and the negative result is
the finding.**

### The canonical article on component API does not address it

Nathan Curtis's *"Crafting Component API, Together"* (EightShapes, fetched 2026-08-13) is the field's
most-cited treatment and is about **individual** components: API drafts *"composed in a visible tool"*
like Google Docs, *"started from a template"* to *"embed hints"*, critiqued *"as a multi-disciplinary
team"* with *"asynchronous review"*. It organises around anatomy, properties and layout.

**It contains no mechanism for consistency across a catalogue** — no automated enforcement, no shared
vocabulary artifact, no cross-component tracking, and no numbers about props or component counts. The
guidance is process, applied one component at a time.

### What ships is consumer-facing linting, not author-facing API enforcement

Atlassian publishes an `eslint-plugin-design-system` with 40+ rules; the visible rule names include
*"Consistent css prop usage"*, *"Ensure design token usage"*, *"Ensure icon color"*, *"No margin"*,
*"Prefer primitives"*, *"Use primitives"* (atlassian.design, fetched 2026-08-13).

**Read by name, these govern how consumers *use* the system, not whether the system's own components
agree with each other.** *"Ensure design token usage"* stops an app hard-coding a colour; nothing in the
visible list checks that `Button`'s `variant` and `Badge`'s `variant` mean the same thing. **Caveat: the
individual rule pages were not opened in this run** — the index page carries names without descriptions,
so this reading is an inference from naming and should be checked before being quoted.

### The closest thing to structural enforcement found

**Astryx's typed `ComponentDoc`**, where metadata drift becomes a validation failure. But it enforces the
*shape of the documentation object* — that every component has the required fields — not a *shared
vocabulary* across components. A catalogue can be fully valid against that type and still call the same
concept `variant`, `kind` and `appearance` in three places.

### What could not be verified, and was expected to be the strongest example

**Zag.** The expectation going in was that its machines share a uniform API by construction — a
`connect()` returning a consistently named prop-getter surface across every machine — which would be the
best available example of consistency enforced structurally rather than socially. **The introduction page
opened (zagjs.com/overview/introduction, 2026-08-13) does not state this.** It lists **73 components and
utilities** and describes framework-agnostic machines with adapters, and says nothing about API
uniformity. **Not asserted here.** It remains the most promising place to look and would need the
per-machine API pages read to settle.

**Knapsack** markets *"connecting and comparing properties and data to ensure consistency and alignment
as your system scales"* and that *"Structured data is readable by humans and AI tools."* **No published
mechanism, schema, or breaking-change record was found** for any of it in this run.

### The finding, stated plainly

**No evidence was found of any system automatically enforcing a shared prop vocabulary, state-name
vocabulary or API shape across its own catalogue.** What exists is: process and review (Curtis),
consumer-side linting (Atlassian), and doc-shape validation (Astryx). The gap between "every component
has a valid metadata record" and "every component uses the same words for the same ideas" appears to be
unaddressed by tooling anywhere in this set — and largely unwritten-about.

---

## Where marketing and the record disagree

Collected, since the brief names this as the highest-value signal:

| Vendor | Positioning | What the record shows |
|---|---|---|
| Figma | Dev Mode MCP launch blog: bringing Figma into your workflow | Own docs page documents a 351,378-token response against a 25,000 limit, with a suggested remedy of 50k–100k |
| zeroheight | *"Your whole system in one MCP"* | Tool surface is index-then-fetch (`list-pages`/`get-page`); no sizes or limits published (help page 403 to this run) |
| Supernova | AI context management *"generally available"*, not beta | Remote MCP Sept 2025 → data export Nov 2025 → **scoping layer June 2026**; benefit claimed as "reduced token usage" with no numbers |
| Astryx | Tiering and dense output documented as agent-facing features | No published sizes to show why tiering is needed |
| Knapsack | Structured data *"readable by humans and AI tools"* | No public schema, versioning or compatibility record found |
| Backlight | *"a unique, all-in-one design system solution"* | **Shut down June 1st 2025**; no reason published |

---

## What this run could not establish

Stated rather than papered over:

- **Zag's API uniformity** — the strongest candidate for question 4 and unverified; needs the per-machine pages.
- **zeroheight's actual tool contract** — help article 403; tool names are second-hand.
- **Whether Supernova has had breaking changes** — none published, which does not mean none occurred.
- **Knapsack's data model** — nothing public found; may exist behind login or in customer docs.
- **Backlight's reasons for shutting down** — the notice gives none, and no post-mortem was found. The most interesting question in the pass has no public answer.
- **Any first-hand user complaint about a design-system MCP being too large.** The Figma number is a vendor doc; the ecosystem numbers are blogs. **No issue tracker was found where a design-system vendor's own users complain about metadata payload size** — which may mean the surfaces are small enough, or that adoption is thin enough that nobody has hit it yet. Those two are not distinguishable from outside, and the distinction matters.

---

## Sources opened in this run (all 2026-08-13)

Vendor documentation and registries — developers.figma.com *MCP clients issues*; astryx.atmeta.com/docs/cli;
github.com/facebook/astryx packages/cli/README.md; react-docgen.dev release notes; storybook.js.org
*optimize-storybook-7-6*; storybook.js.org Storybook 9 migration guide; github.com/storybookjs/storybook
discussion #29021; learn.supernova.io/changelog; github.com/DirectedEdges/specs; zagjs.com/overview/introduction;
backlight.dev.

Vendor marketing — supernova.io *we-just-shipped-ai-context-management*; zeroheight.com/mcp;
atlassian.design eslint-plugin-design-system index; knapsack.cloud (via search).

Third-party / secondary, labelled as such in the text — EightShapes/Medium (Curtis); MCP token-cost blogs.

**Returned 403 and reported second-hand:** help.zeroheight.com MCP overview; api.github.com repo endpoint.
**404 during the run:** supernova.io/mcp (correct paths found by search).
