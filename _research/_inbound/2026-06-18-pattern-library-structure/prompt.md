You are advising a senior design systems practitioner at a digital agency
who is building a personal knowledge base of design-systems field-truth.
They have already built a ~45-component catalogue (each component a
field-truth brief: how the leading systems handle it, where they converge/
diverge, the practice's opinionated default). They are now opening a
PATTERNS LAYER above the component catalogue and need the scaffolding
VALIDATED before authoring individual patterns — because the authoring will
be parallelized across agents and the taxonomy/schema must be right first.

This is a META study, not a single-pattern brief. The deliverable is a
field-truth survey + recommendations that will refine three things:
(a) the pattern TAXONOMY (the tiers/categories), (b) the pattern-brief
SCHEMA (the documentation spine), and (c) the candidate PATTERN LIST. Do not
write a pattern brief; survey how the field actually structures pattern
libraries and critique the practitioner's proposed scaffolding.

This is not an introductory guide. Assume the reader knows what a design
system and a pattern library are, and has shipped multiple systems. Explain
the non-obvious — where leading systems genuinely disagree on what a pattern
is, how they categorize patterns, and how they document them.

=== THE PRACTITIONER'S PROPOSED SCAFFOLDING (critique this) ===

THE PATTERN-VS-COMPONENT BOUNDARY they've drawn: a component is a "thing"
with props/states/variants/an API (Button, Form); a pattern is a "recurring
composition of components that solves a problem," resolved as DECISION RULES,
that owns cross-component orchestration and does not ship as one importable
thing. The canonical line: Form is the component (the <form> primitive +
validation orchestration); Forms-as-a-system (the multi-step wizard,
save-and-resume) is the pattern.

THE PROPOSED FOUR-TIER TAXONOMY:
1. cross-component-recipe — a reusable assembly solving a recurring
   micro-problem (Forms-as-a-system, Filtering, Search, Common actions,
   Overflow content). Composition/decision-heavy.
2. state-convention — a cross-cutting rule for expressing one state
   consistently across components (Disabled, Read-only, Loading
   orchestration, Notifications orchestration). Decision/a11y-heavy.
3. flow-and-shell — a multi-step or app-frame interaction over time/space
   (Login/Auth, App shell/global header, multi-step wizard, destructive
   confirmation, save/unsaved-changes). Flow/layout-heavy.
4. page-template — a full-page composition archetype (master-detail,
   dashboard, settings, error pages, onboarding). Layout-heavy.

THE PROPOSED PATTERN-BRIEF SPINE (a flexible spine, not a locked key set):
a small ALWAYS core — problem & context, composition (typed component
references), decision rules, accessibility orchestration, anti-patterns,
related patterns & components, agent-consumable schema — plus tier-
conditional SCALES sections — flow & states, layout & structure, content &
copy, variants & responsive, field POV evolution.

=== WHAT TO RESOLVE ===

1. HOW LEADING SYSTEMS STRUCTURE THEIR PATTERN LIBRARIES (the survey): for
   each, what is the top-level taxonomy, what do they call this tier, and
   what lives in it — IBM Carbon (Patterns: "Dialog", "Loading", "Empty
   states", "Forms", "Notifications", etc.), Shopify Polaris (Patterns +
   the "patterns" vs "foundations" vs "components" split), Material Design
   (the "Foundations"/patterns + "Components"), Atlassian (Patterns +
   "Content" + "Resources"), GOV.UK Design System (the "Patterns" section:
   "Ask users for…", "Help users to…", "Pages"), Microsoft Fluent, Adobe
   Spectrum, Ant Design, Nielsen Norman Group + the pattern-library
   literature (the design-pattern lineage from Alexander → Tidwell's
   "Designing Interfaces" → UI-Patterns.com). Cite each with a version date.
   Surface the disagreement: systems do NOT agree on what a "pattern" is or
   how to slice the tier.

2. THE PATTERN-VS-COMPONENT BOUNDARY as the field draws it: where leading
   systems put the line (e.g. is a "Card" a component or a pattern? a
   "Search" a component or a pattern? a "Data table" a component or a
   pattern?), and whether the practitioner's "composition + decision-rules +
   cross-component-orchestration + doesn't-ship-as-one-thing" boundary holds
   up or needs sharpening. Note the systems that ship pattern SCAFFOLDING
   (an AppShell, a <Wizard>) and how that blurs the line.

3. VALIDATE/CRITIQUE THE FOUR-TIER TAXONOMY: is a four-tier split well-
   attested, or do leading systems use a different cut (e.g. functional
   "Ask users for X / Help users to Y" task-based grouping like GOV.UK, vs
   structural recipe/flow/template grouping)? Is "state-convention" really a
   pattern tier or is it cross-cutting guidance (closer to a foundations/
   accessibility doc)? Is "page-template" a pattern or a separate "templates/
   layouts" artifact? Recommend the taxonomy you'd defend, with the tradeoffs.

4. VALIDATE/CRITIQUE THE PATTERN-BRIEF SPINE: what sections do real pattern-
   library entries actually contain (problem/when-to-use, anatomy, the
   variants, the do's/don'ts, the a11y, the content/UX-writing, the code/
   examples)? Does the proposed ALWAYS/SCALES spine match, over-engineer, or
   miss anything? Is "decision rules" the right center of gravity? Should
   the agent-consumable schema differ in shape from the component schema?

5. VALIDATE/CRITIQUE THE CANDIDATE PATTERN LIST: go tier by tier. What is
   MISSING that the field treats as a first-class pattern (e.g. data
   visualization, in-context editing/inline-edit, bulk actions/selection,
   pagination-vs-infinite-scroll, comments/activity feeds, command palette,
   notifications center, comparison tables, pricing tables, comment threads,
   permissions/sharing, multi-step forms, "are you sure"/confirmation,
   progressive disclosure, responsive/adaptive layout, internationalization
   patterns, theming/dark-mode)? What in the list is MISCATEGORIZED, what is
   really a COMPONENT (belongs in the catalogue, not patterns), and what is
   really cross-cutting GUIDANCE (belongs in a numbered foundations file)?
   Recommend a validated seed list per tier with a priority order.

6. THE AGENT-CONSUMABILITY ANGLE: this knowledge base is intended to be
   exposed via an MCP server to coding/design agents. Briefly: does that
   intent change how patterns should be structured/tiered/schema'd vs a
   human-only pattern library? (e.g. machine-resolvable decision rules,
   typed composition references.)

=== OUTPUT ===

Structured markdown. Suggested sections:
1. Framing — the state of pattern libraries; why the field disagrees on
   what a pattern is.
2. The survey — how each leading system structures its pattern library
   (a table or per-system entries, with version dates).
3. The pattern-vs-component boundary — as the field draws it; verdict on
   the practitioner's boundary.
4. The taxonomy — verdict on the four tiers; the taxonomy you'd defend.
5. The pattern-brief spine — verdict on the ALWAYS/SCALES spine; the spine
   you'd defend.
6. The pattern list — tier-by-tier validation; the missing, the
   miscategorized, the really-a-component, the really-guidance; a
   prioritized validated seed list.
7. The agent-consumability angle.
8. Sources cited — with version dates.

Synthesize; where it's context-dependent give frameworks not winners; date
current-platform-state claims and note the verification path. Be willing to
tell the practitioner their scaffolding is wrong where it is — the point of
this run is to validate or correct it before authoring begins, not to
ratify it.
