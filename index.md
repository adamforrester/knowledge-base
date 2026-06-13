---
okf_version: "0.1"
type: practice-area
title: Design Systems Knowledge Base
description: Adam Forrester's vault on design systems consulting at VML. Numbered files imply both reading order and DS engagement phase.
tags: [index]
timestamp: 2026-06-13
---

# Design Systems Knowledge Base

A personal knowledge base on design systems consulting, maintained by Adam Forrester for day-to-day reference at VML. The audience is one practitioner; the voice is opinionated and first-person plural. Numbered files follow a phase model: 00 cross-cutting, 01–08 engagement phases, 09 gaps, 10+ extensions. Numbering anomalies (00, 00b, 00d) reflect when files were added; they aren't gaps to fix.

## Cross-cutting

* [Principles and Philosophy](/00-principles-and-philosophy.md) - The practice's POV: the ten principles, where we converge with and diverge from the field.
* [Agency Context](/00b-agency-context.md) - VML as agency context: how DS work fits the agency commercial reality, and the gap between "what good looks like" and the world we operate in.
* [Commercial Model](/00d-commercial-model.md) - How VML scopes, resources, and prices DS engagements. Working document, not fixed formula.

## Engagement phases

* [Discovery and Strategy](/01-discovery-and-strategy.md) - Discovery phase: strategic alignment, audits, stakeholder mapping, maturity baseline, pilot scoring.
* [Design Foundations](/02-design-foundations.md) - Tokens, theming, naming, the Figma → DTCG → Style Dictionary pipeline. The bedrock layer.
* [Component Library](/03-component-library.md) - Component model: anatomy, properties, layout, composition primitives, components-as-data.
* [Documentation](/04-documentation.md) - Docs strategy for two audiences (humans and machines). Storybook/MDX plus machine-readable metadata and registries from one source.
* [Development Support](/05-development-support.md) - Dev pipeline, Storybook, headless vs. opinionated, CI quality gates, MCP/AI integration, adoption enablement.
* [Pilot and Implementation](/06-pilot-and-implementation.md) - Running the pilot product team: validating the system in production, building the executive coalition for scale.
* [Governance and Adoption](/07-governance-and-adoption.md) - Governance models, contribution flow, adoption mechanics. The phase that decides whether the system survives the engagement.
* [Ongoing Maintenance](/08-ongoing-maintenance.md) - Post-launch operating model, retainer shapes, KPIs. The phase the practice sells the least.

## Gaps

* [Gaps and Open Questions](/09-gaps-and-open-questions.md) - Practice gaps and unanswered questions across the corpus. Sourced inventory of what we don't yet have a POV on.

## Extensions

* [CMS and Platform Integration](/10-cms-and-platform-integration.md) - DS in CMS environments. The seam between component governance and content governance.
* [Mobile and Cross-Platform](/11-mobile-and-cross-platform.md) - iOS, Android, Flutter. Tokens as the shared layer; native vs. custom component decisions; platform-specific token delivery.
* [Figma Practice](/12-figma-practice.md) - Figma at professional depth. Library architecture, component construction, Variables, Dev Mode/Code Connect/MCP, branching, performance, deprecation.
* [Internationalization and RTL](/13-internationalization-and-rtl.md) - i18n, l10n, and RTL as DS architecture. Logical properties, text expansion, multi-script typography, locale-aware tokens, RTL component mirroring.
* [Accessibility](/14-accessibility.md) - Accessibility encoded into the DS architecture. Pair tokens for contrast, ARIA encapsulation, focus management, the four-layer model, conformance under EAA / Section 508.
* [AI in Design Systems](/15-ai-in-ds.md) - AI integration across the DS lifecycle. Components-as-data as architectural prerequisite. MCP server architecture, Figma MCP and Code Connect, three-level context maturity.
* [Mobile Accessibility Implementation](/16-mobile-accessibility-implementation.md) - Mobile accessibility implementation depth across Flutter, Jetpack Compose, SwiftUI/UIKit, and React Native.
* [Accessibility Annotation Contract](/17-accessibility-annotation-contract.md) - What designers specify in Figma so engineers can implement accessibility faithfully. Per-concern annotation spec. Mobile-scoped today.
* [Motion Foundations](/18-motion-foundations.md) - Motion as a first-class foundation primitive. Three-tier motion tokens, choreography vocabulary, reduce-motion as a system contract, performance budget.
* [Motion Implementation - Web](/19-motion-implementation-web.md) - Web motion in 2026. CSS / WAAPI / View Transitions primitives, the linear() spring revolution, library landscape, INP / LoAF / compositor-only performance.
* [Motion Implementation - Mobile](/20-motion-implementation-mobile.md) - Mobile motion across SwiftUI / UIKit, Compose, Flutter, RN. Cross-framework spring parameter mapping, shared element transitions, threading and 120Hz.
* [Motion Spec and Handoff](/21-motion-spec-and-handoff.md) - The designer-to-developer micro-interaction spec gap. Why Figma is structurally inadequate for motion, the eight-field sufficient spec, the layered handoff contract.
* [Token Architecture Extensions](/22-token-architecture-extensions.md) - The spec-and-architecture layer beneath 02. DTCG 2025.10 at practitioner depth, composite-token fidelity gap, computed/relational tokens, density as a theming dimension.
* [Typography Tokenisation](/23-typography-tokenisation.md) - Three-tier mandatory typography stack, modular scales with the display pivot, fluid type with clamp() + container queries, variable fonts as a tokenisation problem.
* [Tokens at Scale](/24-tokens-at-scale.md) - Operational layer for enterprise multi-brand token systems. Multi-collection-not-multi-mode, Generative Token pattern, blast-radius-weighted RACI, the Cascade Report, semver-for-tokens.
* [AI-Aware Patterns and Conversational UI](/25-ai-aware-patterns-and-conversational-ui.md) - AI patterns the DS ships to consumers (chat, streaming, citation, refusal, tool-call). Field survey, production-grade triad, EU AI Act Article 50.
* [Adaptive Interfaces - Foundations](/26-adaptive-interfaces-foundations.md) - Six lineages of adaptive UI, Sentient Design as adopted vocabulary, four-tier pattern catalogue, agent typology, personalization vs. adaptation, EU AI Act Article 5.
* [Adaptive Interfaces - Implementation](/27-adaptive-interfaces-implementation.md) - Engineering companion to 26. Five-rung spectrum, tool-calls as UI primitive, RAG, multi-step agentic flows, four-tier memory, streaming UI, eval-driven QA, cost modelling.

## Vocabulary

* [Glossary](/GLOSSARY.md) - Vault-specific and practice-adjacent vocabulary. Common DS terms not defined; reach for it when a term reads as internal-tier IP.

## Working directories

These are not authoritative content. They sit alongside the numbered files as inputs and drafts.

* `_source-text/` - raw `.txt` source material (external articles, internal decks, transcripts). Read-only inputs; cited when synthesising.
* `_research/` - dual-agent research workspace. Drafts only. See `_research/README.md` for the convention.
* `_notes/` - intermediate synthesis notes that fed the numbered files. Lower authority than the numbered files.
