# 00d — Commercial Model

> This file covers how VML scopes, resources, and prices design systems work. It is intentionally a working document — commercial model specifics are built over time from engagement data, not defined up front. What follows is a framework, not a fixed formula.

---

## The Core Scoping Problem

Design systems work at VML is almost always scoped under one of two conditions:

1. **You know what engagement pattern you're in** (see `00c-engagement-patterns.md`) but the client has a budget number before the scope is defined
2. **You don't yet know what you're in** — the RFP says "design system" but the actual need is unclear until discovery

Both conditions require the same discipline: scope to what will actually be delivered, not to what the client thinks they want. Over-scoping to ideal-state and then cutting under pressure produces worse outcomes than honest scoping up front.

The task library (`DS_TaskLibrary_Schema_v02_1.xlsx`) is the source of truth for task-level estimates. This file provides the interpretive layer — how to read those estimates against real engagement conditions.

---

## Roles and Disciplines

The following roles appear in DS engagements at VML. Not all are required for every engagement — see the pattern-specific guidance below.

| Role | Typical Allocation | Notes |
|---|---|---|
| Strategy Lead | 25–50% | Scoping, POV, governance definition. Often reduced in delivery-heavy engagements. |
| Sr. UX Designer | 50–100% | Leads UX direction, component behavior, pattern decisions. |
| UX Designer | 50–100% | Execution — wireframes, annotations, flows. Can be replaced by Sr. UX on smaller scopes. |
| Sr. Visual Designer | 50–100% | Owns visual language, token decisions, typography. |
| Visual Designer | 50–100% | Visual execution — component design, documentation. |
| Design Technologist | 50–100% | Token implementation, Figma Variables, design-to-dev bridge. Core for DS work. |
| Frontend Developer | 50–100% | Component development, framework implementation. Only required when dev build is in scope. |
| Accessibility Specialist | 10–25% | WCAG review, annotations. Often fractional. |
| Project Manager | 50% | Schedule, status, risk, client comms logistics. |
| Account Lead | Non-billable or reduced | Relationship and commercial accountability. |

**Minimum viable team for a Figma-only engagement:** Sr. Visual Designer (or Sr. UX), Design Technologist, PM (part-time). Strategy Lead as needed for client-facing scoping and POV work.

**Minimum viable team for a design + code engagement:** Add Sr. UX, Frontend Developer, and Accessibility Specialist at fractional allocation.

**CareCentrix 2026 as a reference team composition:**
- Project Lead / Design Director: 25%
- Design Systems Lead: 50%
- UX Designer: 100%
- UI (Visual) Designer: 100%
- Delivery Lead (PM): 50%
- UX Copywriter: 75 hours fixed
- Accessibility Specialist: 10 hours fixed

This is a 5-person production core plus 2 specialists, appropriate for a 12–24 week design-only engagement of moderate component scope.

---

## Hour Ranges by Phase

The following ranges come from the task library and represent standard complexity. Complexity drivers (component count, brand count, framework count, stakeholder group count) scale these up. See the task library for full multiplier logic.

### Discovery & Strategy
| Task | Base Hours | Min | Max |
|---|---|---|---|
| Stakeholder interviews | 28 | 16 | 48 |
| Application & design audit | 40 | 24 | 80 |
| Brand & visual asset review | 16 | 12 | 24 |
| Technical environment assessment | 20 | 12 | 40 |
| Design direction & principles | 32 | 20 | 48 |
| **Phase total (standard)** | **~136** | **84** | **240** |

### Design Foundations
| Task | Base Hours | Min | Max |
|---|---|---|---|
| Primitive token architecture | 32 | 20 | 48 |
| Semantic token mapping | 28 | 20 | 56 |
| Theme architecture | 20 | 12 | 48 |
| Typography system | 24 | 16 | 36 |
| Color system & palette | 28 | 20 | 48 |
| Iconography approach | 20 | 12 | 36 |
| **Phase total (standard)** | **~152** | **100** | **272** |

### Component Library
| Task | Base Hours | Min | Max |
|---|---|---|---|
| Core components — Tier 1 (~15 components) | 80 | 48 | 140 |
| Extended library — Tier 2 (~25 components) | 120 | 80 | 200 |
| Pattern & template library | 80 | 48 | 140 |
| Accessibility review & annotation | 40 | 24 | 80 |
| **Phase total (standard, Tier 1 only)** | **~120** | **72** | **220** |
| **Phase total (standard, Tier 1 + 2)** | **~320** | **200** | **560** |

### Documentation
| Task | Base Hours | Min | Max |
|---|---|---|---|
| Figma component library (publish + govern) | 60 | 40 | 100 |
| Usage guidelines | 40 | 24 | 72 |
| Developer documentation | 32 | 20 | 64 |
| Contribution guide | 20 | 12 | 28 |
| **Phase total (full)** | **~152** | **96** | **264** |
| **Phase total (Figma library only)** | **~60** | **40** | **100** |

### Development Support
| Task | Base Hours | Min | Max |
|---|---|---|---|
| Design-to-dev handoff | 24 | 16 | 48 |
| Token implementation support | 40 | 24 | 80 |
| Component QA review | 32 | 20 | 60 |
| **Phase total** | **~96** | **60** | **188** |

### Pilot & Implementation
| Task | Base Hours | Min | Max |
|---|---|---|---|
| Pilot application design | 80 | 48 | 140 |
| Implementation coaching | 40 | 24 | 64 |
| Stakeholder reviews | 20 | 12 | 36 |
| **Phase total** | **~140** | **84** | **240** |

### Governance & Adoption
| Task | Base Hours | Min | Max |
|---|---|---|---|
| Governance model definition | 24 | 16 | 36 |
| Team training & workshops | 32 | 20 | 56 |
| Adoption roadmap | 20 | 12 | 32 |
| **Phase total** | **~76** | **48** | **124** |

### Ongoing Maintenance (per month)
| Task | Base Hours | Min | Max |
|---|---|---|---|
| Monthly system updates | 24 | 16 | 40 |
| Net-new component (per component) | 16 | 10 | 28 |
| Version management & changelog | 12 | 8 | 20 |
| Ongoing stakeholder reviews | 8 | 4 | 16 |
| **Monthly total (no new components)** | **~44** | **28** | **76** |

---

## Scoping by Engagement Pattern

### Pattern 1: Product-Support Component Build

**Typical phases in scope:** Partial Discovery, Design Foundations, Component Library (Tier 1), Figma library publish, Partial handoff

**Rough range:**
- Minimal: Discovery (partial) + Foundations + Tier 1 components + Figma library = ~200–320 hours
- Standard: Above + usage guidelines + handoff sessions = ~300–450 hours
- Extended: Above + Tier 2 components + dev support = ~500–700 hours

**What is almost always out of scope:** Governance model, adoption roadmap, contribution guide, ongoing maintenance, pilot. Name these explicitly.

---

### Pattern 2: Figma-Only Handoff

**Typical phases in scope:** Design Foundations, Component Library (design only), Figma library publish

**Rough range:**
- Minimal: Token foundations + core components + Figma library = ~150–250 hours
- Standard: Above + accessibility annotations + handoff documentation = ~220–350 hours

**Key variable:** Whether token architecture is included or components are designed on top of ad-hoc styles. Always argue for token architecture — it's 60–80 hours that prevents much larger future problems.

---

### Pattern 3: Audit & Reconnect

**Typical phases in scope:** Discovery (heavy — audit is the deliverable), then conditional build based on audit findings

**Rough range:**
- Audit only: ~80–160 hours depending on system complexity and page/component count
- Audit + gap remediation: Scope after audit. Cannot be estimated reliably before the audit is complete.

**Important:** Never commit to a full reconnect estimate without completing the audit first. The audit determines the scope. This is the most common place where under-scoping creates client conflict — assumptions about system quality are almost always wrong.

---

### Pattern 4: Inherited System + Scale

**Typical phases in scope:** Discovery (audit + maturity assessment), then extension or rebuild depending on findings

**Rough range:**
- Maturity assessment only: ~40–80 hours
- Assessment + extension scoping: ~80–120 hours
- Extension build: Depends entirely on audit findings. Ranges from 80 hours (token additions + a handful of new components) to 400+ hours (architectural remediation + full extension)

---

### Pattern 5: Brand → Digital Extension

**Typical phases in scope:** Design Foundations (heavy), Component Library (core set), Figma library

**Rough range:**
- Token translation + core components + Figma library: ~180–300 hours
- Above + pattern library + usage guidelines: ~280–450 hours

**Key variable:** Whether the brand has accessible color pairs and a usable type scale for UI. If not, color system and typography work expands significantly.

---

## The White-Label Kit Question

VML has an internal white-label Figma component kit (Prism2) that is intended to reduce setup time on client engagements. The commercial question — does this reduce our estimates, or does it raise the quality of what we deliver for the same estimate — is unresolved and should be treated honestly.

**Current position:** Scope at standard hours. Use the kit as a quality and consistency accelerator, not a line-item reduction. Until formal technology team adoption and engagement data exist to back up time savings, quoting reduced hours based on the kit creates commercial risk.

**When the kit is used, what likely compresses:**
- Primitive token architecture (foundations already exist; work is theming and extension)
- Core component design (starting from established patterns, not blank canvas)
- Figma library publish (structure and governance already established)

**What does not compress regardless of kit availability:**
- Discovery and audit (client-specific)
- Semantic token mapping for client's brand
- Accessibility review
- Client-specific pattern and template work
- Handoff and development support

**The honest client conversation:** *"We have an internal foundation that means we're starting from a more mature baseline than a from-scratch build. We scope at standard hours, but the quality floor is higher and we spend less time on foundational decisions. That translates to better work, not necessarily fewer hours — though on some engagements the foundation does let us move faster on the build phases."*

**Update this position as engagement data accumulates.** The first few engagements where the kit is formally used should track actual hours against estimates to build the empirical case.

---

## The Run-Phase Pricing Gap

The biggest unresolved commercial gap: VML scopes and prices the Build phase well. The Run phase — ongoing maintenance, governance operations, adoption support — is either absent from proposals or dramatically underweighted.

**What the Run phase actually costs a client (Curtis benchmark):**
- 3–8 person DS team
- 20–30 hours/week collectively
- Translates to roughly 80–320 hours/month of internal client effort

**What this means commercially for VML:**
Three productizable post-Build offerings that are currently unpriced:

| Offering | Description | Rough Scope |
|---|---|---|
| Run-phase retainer | Monthly ongoing support — updates, QA, governance facilitation | 20–40 hours/month |
| Quarterly governance review | One-shot per quarter — coverage assessment, backlog prioritization, health check | 16–24 hours/quarter |
| Ambassadors program | 4–6 week embedded adoption coaching post-launch | 80–120 hours fixed |

None of these are currently in standard proposals. They represent value the practice creates and gives away — clients either do this work themselves (badly) or it doesn't happen and the system decays.

**This should be added to every proposal as optional extension scope**, even if the client doesn't take it up front. Naming it creates the conversation and establishes that ongoing support is a professional service, not a courtesy.

---

## Complexity Drivers

The task library defines nine complexity drivers that scale base hours. These are the questions to ask in scoping conversations:

| Driver | What it affects most |
|---|---|
| Page / screen count | Audit, design, QA phases |
| Component count | All component library tasks |
| Number of brands / themes | Token mapping, theme architecture, QA |
| Dev frameworks in scope | Technical assessment, token implementation, dev support |
| Stakeholder group count | Discovery, governance, ongoing reviews |
| Design fidelity required | Visual and UX hours across all phases |
| Client design maturity | Discovery depth, education overhead, iteration cycles |
| Integration touchpoints | Dev support, token implementation |
| Regional variant count | Token mapping, QA, documentation |

**Rule of thumb:** Standard estimates assume a single brand, single framework, intermediate client maturity, and moderate component count (~15–20 components). Each additional brand, each additional framework, and each step down in client maturity adds meaningful hours — typically 30–80% above base depending on the phase.

---

## What Gets Cut First (and What Shouldn't Be)

Under timeline and budget pressure, work gets cut. Here is the honest order in which it happens and a note on each:

**Usually cut first — and sometimes defensibly so:**
- Usage guidelines and documentation beyond Figma annotations
- Contribution guide
- Governance model definition
- Adoption roadmap
- Pilot application design

**Cut frequently but shouldn't be:**
- Accessibility review and annotation — creates debt that is expensive to pay later, and for regulated industries is non-negotiable
- Token architecture — without this, every future engagement starts over
- Technical environment assessment — skipping this is the most common cause of mid-engagement scope surprises

**Never cut:**
- Stakeholder alignment on scope and deliverables — if this isn't done, everything else is at risk
- Handoff documentation sufficient for the consuming team — the minimum is a component inventory, prop intent, and annotation of non-obvious states

---

## SOW Language Considerations

*(This section is a placeholder — to be built as templates are developed)*

Key areas that need standard SOW language:
- Scope of Figma library deliverable (what is included, what is not)
- Design system vs. component library distinction — what the engagement delivers
- Handoff protocol — what VML provides at engagement close
- Assumptions and dependencies — client responsibilities during the engagement
- Out-of-scope items — explicit list to prevent scope creep
- Extension scope language — how to add Run-phase work post-delivery

---

*This is a working document. Priority additions: (1) tracked hours from completed engagements against these estimates, (2) SOW template language, (3) revised white-label kit impact once formal adoption and engagement data exist.*
