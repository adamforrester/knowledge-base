---
type: practice-area
title: Agency Context
description: VML as agency context — how DS work fits agency commercial reality, and the gap between "what good looks like" and the world we operate in.
tags: [cross-cutting, agency, vml]
timestamp: 2026-05-05
---

# 00b — Agency Context

> This file contextualizes the knowledge base for how VML actually works. The rest of the knowledge base describes what good looks like. This file describes the world we operate in — and the gap between those two things is where most of the hard decisions live.

---

## Who we are

VML is a global creative, experience, and commerce agency. Design systems work at VML sits within a broader service offering that includes brand identity, product design, digital experience, and technology delivery. We are not a design systems consultancy. We are an agency that is increasingly asked to do design systems work — or work that requires design systems thinking — as part of larger engagements.

That distinction matters. It shapes our commercial model, our team structure, our client relationships, and the realistic scope of what we can deliver and maintain.

---

## How DS work comes to us

Design systems work rarely arrives as a clean, standalone engagement. It comes to us in a few recurring patterns:

- **Embedded in a product or redesign engagement.** A client hires us to redesign a website or app. The RFP mentions a "design system" or "component library." What they mean — and what we can realistically deliver in that timeline — are usually different things.
- **As an upsell or extension from Brand ID.** Our Brand Identity studio rebrands a client. The natural next question is: how does this brand live in digital product? A Figma library is the typical answer.
- **As an inherited or stabilization engagement.** A client has an existing design system or component library of unknown maturity. They want to extend it, scale it, or figure out what to do with it. Audit-first, then scope.
- **As a scoped DS-only engagement.** Less common, but it happens — a client who specifically wants design system strategy, architecture, or a Figma library as the primary deliverable.

In most of these, we are one part of a larger delivery chain. We may be handing off to a client's internal development team, a third-party developer, or a separate technology team within VML or a sister agency.

---

## The expertise gap on our teams

Most designers at VML understand how to build components. They understand Figma, auto-layout, variants, and the mechanics of a component library. After that, expertise drops off significantly. 

The deeper layers — token architecture, semantic naming, governance models, contribution frameworks, design-to-code parity, AI-readiness metadata — are not widely understood across the practice. This is normal for an agency of our type and size. It means that DS strategy and architecture decisions often fall to a small number of people (often one) who are asked to advise across many concurrent engagements.

The knowledge base exists partly to address this: to give those conversations a foundation, and eventually to raise the floor across the practice.

---

## The white-label kit (Prism2)

VML has an internal white-label design system called **Prism2**. As of early 2026, Prism2 is primarily realized as a Figma component kit — a token-based library with 219+ semantic tokens, multi-theme support (light/dark/wireframe), and a component library built on Figma Variables and auto-layout.

**What Prism2 is:**
- A Figma component kit for use as a client engagement starting point
- A token architecture (primitive + semantic) using W3C DTCG-compliant naming
- A React component library (in development/evolution) intended as a coded counterpart
- A strategic investment in accelerating the Design Foundations and Component Library phases of engagements

**What Prism2 is not yet:**
- Formally adopted by VML's technology teams — which limits its use on engagements where design and dev need to be tightly integrated
- A plug-and-play solution for AEM or Drupal-based projects (CMS integration is planned, not delivered)
- A fully documented, contribution-ready system — governance and contribution models are not yet established

**The commercial tension:** The question of whether Prism2 reduces estimates or raises quality for the same estimate is unresolved. The honest current position: scope at standard hours and use the kit as a quality and consistency accelerator. Until formal technology team adoption exists and engagement data supports it, quoting reduced hours based on the kit creates commercial risk. See `00d-commercial-model.md` for the full framing of this tension.

**What likely compresses when Prism2 is used:**
- Primitive token architecture (foundations exist; work is theming and client-specific extension)
- Core component design (starting from established patterns, not blank canvas)
- Figma library setup and governance structure

**What does not compress regardless:**
- Discovery and audit (always client-specific)
- Semantic token mapping for client's brand
- Accessibility review
- Handoff and development support
- Any CMS-specific component work

**The client conversation:** *"We have an internal foundation that means we're starting from a more mature baseline than a from-scratch build. We scope at standard hours, but the quality floor is higher and we spend less time on foundational decisions."*

**Update this section** as Prism2's adoption status changes, as technology team approval is received, and as engagement data accumulates on actual time savings.

---

## The scoping and sizing role

One of the most recurring demands on DS leadership at VML is participating in scoping, sizing, and resourcing exercises — often with limited information, compressed timelines, and a client or account team that has a number in mind before the conversation starts.

This is a different skill than doing the work. It requires:
- Quickly diagnosing what the client actually has and what they actually need
- Translating DS work into hours, roles, and phases that non-DS stakeholders can evaluate
- Making defensible tradeoff recommendations when full scope isn't possible
- Distinguishing between what we will deliver, what we won't have time to deliver, and what we should name as a risk

The knowledge base should be useful for this kind of rapid-synthesis scoping conversation, not just for in-depth strategic work.

---

## What "design system" usually means in practice

By the definitions used in the rest of this knowledge base, most of what we build at VML in client engagements is not a design system in the full sense. It is most commonly one of these:

| What we build | What it actually is |
|---|---|
| Figma component library | A set of design components in Figma, possibly with token variables, possibly not. No code. |
| Figma library + handoff specs | Figma library plus documentation sufficient for a developer to build from. Still no code. |
| Component library (design + code) | Figma components plus corresponding coded components, typically for one framework. |
| Tokenized foundation | A token architecture (primitive + semantic), possibly with Style Dictionary pipeline. |
| Full design system | The above, plus governance, documentation, contribution model, adoption strategy, and ongoing maintenance. Rare. |

Being honest about which of these we're building — with ourselves and with clients — is one of the most valuable things we can do at the start of any engagement. "Design system" in an RFP almost always means something in the first two rows. Scoping, resourcing, and client expectations should reflect that, not the last row.

---

## Common constraints we work within

**Timeline pressure.** We are almost always building a component library to support a product that is already in motion. There is rarely lead time to build the system before the product work starts. The system is built in parallel with, or slightly ahead of, the design work it is meant to support.

**Budget pressure.** Full design system engagements are expensive and long. Most client budgets are sized for a component library, whether or not the RFP says "design system." This means tradeoffs are inevitable, and the question is which layers to skip and which to protect.

**Handoff without continuity.** In the majority of engagements, we will not be around to maintain, evolve, or govern the system after delivery. We hand off to a client team, a third-party developer, or a separate technology team. The quality of that handoff — and the degree to which what we leave behind is maintainable — is one of the highest-impact decisions in any engagement.

**Documentation and usage guidelines are the first to go.** Under timeline and budget pressure, documentation is almost always the first thing cut. This is the right short-term tradeoff and the wrong long-term one. The knowledge base should help us identify the minimum viable documentation layer that actually protects adoption — so we can argue for it and scope it efficiently.

**We are not usually around for the Run phase.** Long-term maintenance, governance operations, and adoption support are where the greatest value is created — and where we rarely have scope or presence. This is the largest structural gap between what the field says good looks like and what our commercial model supports.

---

## Active engagement examples (as of early 2026)

These represent real, recent engagements that illustrate the range of DS work in practice:

**CareCentrix (Walgreens-owned health client)**
Design-only Figma design system. Client's development team will build from the Figma library. No code deliverable. Constrained scope with tight timeline. Represents the most common engagement type: Figma library as the deliverable, developer team as the consumer.

**Hills Pet (Colgate-owned)**
Rebrand engagement. Client has an existing Figma library they've maintained internally, but it is not connected to their production websites. Design and dev are visually similar but architecturally disconnected. The ask: how do we approach closing that gap, and what resources does it require? Represents the audit-and-reconnect scenario — where the problem is not absence of a system but disconnection between design and code layers.

**New Balance (Australian site → regional scale)**
VML built a Figma library for an Australian site launch (tied to Australian Open). Client dev team built from it. Now they want to scale that look and feel across other regions. Complications: existing design system of unknown maturity, unclear regional adoption, potential migration to Salesforce Commerce Cloud (Chakra UI). Represents the inherited-system-plus-scale scenario with additional platform complexity.

**Brand ID → DS upsell (unnamed client)**
Brand ID studio completes a rebrand. Client is considering a design system as the next step — likely a Figma library at minimum. Represents the brand-to-digital extension scenario, where the DS work starts from a brand artifact rather than a product or engineering context.

---

*This file should be updated as the agency context evolves: new engagements, changes to the white-label kit, shifts in team structure or expertise, changes to commercial model. It is intentionally separate from the phase-level knowledge so it can be updated independently.*
