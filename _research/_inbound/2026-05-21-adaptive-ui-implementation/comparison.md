# Implementation Pair — Agent Comparison

Comparison of the two **implementation paper** outputs. Analytical scaffolding for synthesis — surfaces convergence, divergence, and rigor gaps. Does not adjudicate.

- **CC** = Claude Code — `research-2/adaptive-interfaces-implementation-paper.md`
- **GEM** = Gemini Deep Research — `research-2/Implementing Adaptive Interfaces: Archit.md`

> **Read §5 and §7 first.** The implementation pair has a sharper rigor asymmetry than the foundation pair, and one GEM claim (the Promptfoo acquisition) is a specific, consequential, likely-unverified factual assertion that should be checked before any synthesis relies on GEM's evaluation section.

---

## 1. Metadata snapshot

| Attribute | CC (Claude Code) | GEM (Gemini) |
|---|---|---|
| Length | ~12,000 words | ~5,000–5,500 words (≈2.3× shorter) |
| File size | 83 KB | 31 KB |
| Structure | Preface (3 flags) + 10 numbered sections + Open Questions + What to Read Next + What Surprised Me + Bibliography | Title/abstract + 10 numbered sections + Open Questions + What to Read Next + What Surprised You |
| Closing sections | 6 open questions / 10 ranked reads / 8 surprises | 3 open questions / 4 ranked reads / 3 surprises |
| Citation apparatus | **78 numbered footnotes, all resolved** — full author/title/date/URL; internal footnote audit logged in `progress.md` | **24 inline numeric markers `[1]`–`[24]` — NO reference list.** The numbers resolve to nothing. 4 URLs appear in "What to Read Next" only |
| Voice / posture | Discursive, skeptical, hedge-heavy; "weighted to shipped reality"; flags unverified figures | Polished, technical, confident; declarative; reads like an engineering brief |
| Distinctive devices | Inline `*[speculative]*` tags; spectrum table; self-critical "what surprised me" | 3 ASCII architecture diagrams; a YAML Promptfoo config; a TypeScript snippet; LaTeX-style cost math |
| Working notes available | Yes — `progress.md`, `findings.md`, `task_plan.md` document a 5-research-agent process + a footnote-integrity audit | None |

---

## 2. Topical coverage map

Depth: ●●● substantial · ●● moderate · ● mention · — absent

| Topic | CC | GEM | Notes |
|---|---|---|---|
| The 5-rung spectrum | ●●● | ●●● | Near-identical rungs and the same "work happens in the middle" thesis |
| Tool calling as UI primitive | ●●● | ●●● | Both use the same AI SDK lifecycle states (input-available / output-available / output-error) |
| Structured outputs / schema enforcement | ●●● | ●●● | Both: JSON Schema + Zod, constrained decoding |
| RAG for context grounding | ●● | ●● | Comparable |
| Multi-step / agentic flows | ●● | ●● | Comparable; both name LangChain/LlamaIndex |
| Streaming mechanics (partial JSON) | ●●● | ●●● | Comparable |
| Interop standards (MCP / MCP Apps / AG-UI) | ●●● | ● | CC treats MCP/AG-UI as an emerging interop layer; GEM mentions MCP only re: Notion security |
| Vercel AI SDK RSC walk-back | ●●● | — | **CC only.** GEM presents RSC as current (see §4) |
| Multimodal input modalities | ●●● | ●●● | GEM uses a 5-row modality table; comparable coverage |
| Voice | ●●● | ●● | CC: turn-taking still unsolved, gpt-realtime specifics. GEM: "<300ms speech-to-text" target |
| Cross-device handoff | ●●● | ●● | CC: genuinely unsolved (no way to serialize generative-UI state). GEM: solvable via Kafka/DynamoDB-style sync (see §4) |
| Ambient / proactive surfaces | ●● | ●● | Comparable |
| Memory tiers / architecture | ●●● | ●●● | Both: session → profile → vector → context window. GEM adds a nested ASCII diagram |
| Shipped memory features (ChatGPT/Claude/Gemini memory) | ●●● | — | **CC only** — ChatGPT memory = dossier injection, not RAG |
| Notion vector-DB infrastructure (sharding, S3) | — | ●●● | **GEM only** — decoupled storage/compute, serverless S3, workspace-ID sharding |
| Privacy / GDPR / data residency | ●●● | ●●● | CC: machine-unlearning near-impossibility, residency pricing. GEM: EU AI Act Art. 50 in detail, Notion JP/KR residency |
| Streaming UI as a primitive | ●●● | ●●● | Both: breaks the binary loaded/loading model |
| Eval / QA frameworks | ●●● | ●●● | Both name Promptfoo; both: evals replace manual QA |
| Accessibility QA at scale | ●●● | ● | CC: weakest-tooled area, essentially unsolved. GEM: lists axe-core runners as a working checklist item (see §4) |
| HITL / telemetry / red-teaming | ●●● | ●● | CC broader (telemetry taxonomy, regret signals); GEM has a concrete eval-layer metrics table |
| Governance | ●● | ●● | Both: compliance → outcomes |
| Cost / token economics | ●●● | ●●● | Both do a worked cost calculation (different scenarios) |
| Latency budgets / caching | ●●● | ●●● | Comparable; both cover exact-match + semantic caching |
| Model routing / cascading | ●●● | ●● | CC: 25–35% need frontier models, routing+cascading. GEM: hybrid routing, mini vs. frontier |
| Authoring tooling | ●●● | ●●● | Both: Figma ill-equipped; Storybook+evals; component-prompt pairs; variability unsolved |
| DS implications | ●●● | ●●● | Both: primitives over composed components; semantic contracts; automated governance |
| Where headed [speculative] | ●●● | ●● | CC labels speculation; **GEM drops `[speculative]` tags entirely** in §10 |

---

## 3. Areas of agreement

- **The 5-rung spectrum — and that production work sits in the middle.** Both independently produce the same five positions (rule-based → catalog selection → template composition → structured-data/deterministic shell → direct code emission) and both state explicitly that real production work concentrates in the middle three, not at the extremes. CC §1 / GEM §1. This is the strongest convergence in the pair.
- **Tool calling as the core UI primitive,** with the *same* Vercel AI SDK lifecycle state names: `input-available`, `output-available`, `output-error`. CC §2 / GEM §2.
- **Structured outputs are the load-bearing pattern** — force the model to schema-conforming JSON (Zod), let a deterministic renderer take over. Both.
- **Streaming UI breaks the binary model.** Both open the streaming section by rejecting "loaded vs. loading" and describe skeleton → partial-structure → hydrated → error progression. CC §5 / GEM §5.
- **Latency tolerance is conditional on feedback.** Both: users tolerate multi-second (2–8s) waits *if* given continuous progress feedback.
- **Memory is multi-tiered.** Both describe the same four tiers and both flag the vector-store "right to be forgotten" problem.
- **Traditional QA is dead; evals replace it.** Both: non-deterministic UI cannot be manually QA'd; automated eval suites in CI/CD. Both name **Promptfoo** specifically and **LLM-as-judge**.
- **Cost compounds per-interaction.** Both run an explicit token-cost calculation and both prescribe hybrid model routing (cheap model for routing, frontier model for complex reasoning).
- **Authoring tooling is unsolved.** Both: Figma is built for static design; current practice is Figma-to-prompt, Storybook+evals, and "component-prompt pairs"; designing for variability is an open problem.
- **DS shifts to primitives + semantic contracts.** Both: deliver atomic primitives not pre-composed components; attach machine-readable metadata/JSON schema + semantic description so a model can select components; governance moves to automated validation.
- **EU AI Act Article 50 transparency, enforceable Aug 2026.** Both cite it (GEM in more provision-level detail).

---

## 4. Areas of disagreement

State both versions; do not adjudicate.

**4.1 Vercel AI SDK RSC — current standard or walked back?**
- **CC:** Vercel **walked back** its RSC-based generative-UI primitive — flagged "experimental," published a migration guide to AI SDK UI; CC makes this its Preface flag #2 and a recurring structural theme.
- **GEM:** presents RSC streaming as a current implementation model — "the backend streams React Server Components (RSCs)"; cites "[8] Vercel AI SDK RSC — Generative UI State" documentation approvingly; "What to Read Next" #1 is the AI SDK docs with no walk-back noted.
- Same opposed framings as the foundation pair (foundation-comparison §4.1).

**4.2 "Promptfoo (acquired by OpenAI in March 2026)" — GEM only**
- **GEM:** states it as fact in §6 ("Promptfoo (acquired by OpenAI in March 2026)") **and elevates it to a headline finding** in "What Surprised You" #1: "OpenAI's Acquisition of Promptfoo (March 2026)."
- **CC:** treats Promptfoo as an independent open-source eval/red-team tool; CC's five research agents (which performed live web searches — see `findings.md`) surfaced **no such acquisition**.
- This is a specific, checkable, consequential claim asserted by one agent and unsupported by the other's research. **Flag: likely fabricated or at minimum unverified.** It is load-bearing for GEM's evaluation narrative and is presented as a "surprising" headline — high priority to verify. See §7 and §9.

**4.3 Accessibility QA at scale — solved or unsolved?**
- **CC:** §6 names accessibility-at-scale as the **weakest-tooled** part of generative-UI QA — essentially unsolved; static scanners assume fixed screens; in-pipeline DOM scanning is a logical-but-unproven extension. CC draws an explicit irony against the foundation paper (accessibility is the strongest *evidence* for adaptive UI but the hardest thing to *QA* once generative).
- **GEM:** lists "Accessibility Auditing — Dynamic client-side axe-core runners — Evaluates generated HTML to ensure WCAG AA compliance — Zero critical accessibility violations" in its eval-layer table, presenting it as a working, metric-backed checklist item.
- One agent flags the gap; the other presents it as solved.

**4.4 Cross-device handoff — tractable or genuinely unsolved?**
- **CC:** §3 — genuinely unsolved; there are three incompatible continuity models and *no standard way to serialize generative-UI state* (a prompt+context+output+render tuple is not a document).
- **GEM:** §3 — solvable: "the application's layout state, conversational context, and active tool calls must be normalized and synchronized in real-time … relies on a cloud-backed profile graph and event-driven data streaming pipelines, similar to … Kafka and DynamoDB."
- CC = hard/open problem; GEM = known-architecture problem.

**4.5 Speculation labeling**
- **CC:** §10 speculation is explicitly `[speculative]`-tagged.
- **GEM:** §10 ("Where This Might Be Headed") carries **no speculative markers** — on-device model synthesis, gaze-tracked cognitive-load styling, and "Universal Zero-UI Core Engines" are stated in the same declarative register as the shipped-reality sections. (Note: GEM's *foundation* doc did tag speculation; its implementation doc does not.)

**4.6 Token-cost scenario**
- Not a contradiction, but the worked examples differ and don't cross-check: **CC** — 4k input + 1k output, 10 renders/session, 1M sessions/month, current 2026 model prices → ~$37k/mo (Gemini Flash) vs. ~$450k/mo (Opus 4.7); headline = 12× model-choice swing. **GEM** — 1M interactions/day, 4k input + 500 output, generic $2.50/$10 per-M pricing → $15k/day. Different scales, different price assumptions; synthesis should pick one model.

---

## 5. Sources

### CC — sources cited
- **78 numbered footnotes, every one resolved** with author/title/date/URL. `progress.md` records an explicit footnote-integrity audit ("all 78 defined + referenced, no orphans, no dangling refs").
- Mix: official docs (Vercel AI SDK, OpenAI, Anthropic, Google), engineering blogs (Linear, Notion, Anthropic, Vercel), regulatory primary sources (EU AI Act Art. 50, CCPA/CPRA), HCI papers (CHI/UIST/DIS — UICrit, Lee, Stanford "Generative Interfaces," Google Research "Generative UI"), pricing pages, framework docs (Promptfoo, Inspect, Braintrust).
- CC flags its own uncertain figures inline (e.g. skeleton-screen speed percentages "direction solid, magnitudes untraceable"; several "unverified" labels).

### GEM — sources cited
- **24 inline numeric markers `[1]`–`[24]` with NO reference list anywhere in the document.** The markers are internally semi-consistent (e.g. `[1]` ≈ Vercel AI SDK docs, `[2]` ≈ Notion custom-agents security blog, `[15]` ≈ Notion engineering blog, `[8]` ≈ structured-outputs docs) but are **never keyed to actual sources**. No claim can be traced.
- **The only 4 resolvable sources** appear in "What to Read Next":
  1. Vercel AI SDK Core & UI Documentation — https://ai-sdk.dev/docs
  2. EU AI Act Guide, Article 50 — https://artificialintelligenceact.eu/article/50/
  3. Promptfoo Evaluation Configuration Guides — https://www.promptfoo.dev/docs/configuration/expected-outputs/
  4. Notion Engineering Blog: "How we built security into custom agents" — https://www.notion.com/blog/how-we-built-security-into-custom-agents

### Source observations
- **Asymmetry is extreme.** CC: 78 resolved citations. GEM: 0 resolved inline citations + 4 reading-list URLs. For an "implementation" paper making detailed architectural, pricing, and infrastructure claims, GEM's lack of a reference list is the dominant rigor fact of this pair.
- **Suspect — GEM (high priority):** "Promptfoo (acquired by OpenAI in March 2026)" — see §4.2. Specific, consequential, unverified, and used twice (body + headline surprise).
- **Suspect — GEM (unverifiable, not necessarily wrong):** the Notion infrastructure narrative — serverless S3 sharding, storage/compute decoupling, data residency to Japan and South Korea — is detailed and plausible and partly traceable to the one cited Notion blog, but the specific `[15]`/`[16]`/`[17]` markers resolve to nothing. Cannot be confirmed from the document itself.
- **Suspect — GEM:** "User research shows that … users … are willing to tolerate 2-to-8 second delays" — no study named.
- **Suspect — CC:** CC self-labels soft figures rather than hiding them; no undisclosed suspect source identified. The risk on CC's side is the opposite — citation volume so high it is impractical to spot-check all 78.

---

## 6. Unique substantive contributions

### CC only
- **The Vercel RSC walk-back** as a structural theme — and the broader argument that the field is moving *toward constraint*, not toward more generation.
- **MCP / MCP Apps / AG-UI as an emerging interop layer** — GEM mentions MCP only as a security concern.
- **Shipped memory features dissected** — ChatGPT memory works by injecting a structured "dossier" into the system prompt, *not* by RAG; Claude vs. Gemini memory architectures contrasted.
- **Machine unlearning** — "right to be forgotten" is near-impossible for data baked into model weights; architectural rule: keep personalization in deletable stores.
- **Accessibility-at-scale as unsolved**, with the explicit irony linking back to the foundation paper.
- **The 12× cost swing** for identical UX depending on model choice; data-residency pricing multipliers.
- **Academic framing of the authoring problem** — Lee's "variability by design," UICrit as the missing automated-critique primitive.
- **Linear Agent Interaction Guidelines**; **cross-device state as a serialization problem**.

### GEM only
- **Three ASCII architecture diagrams** (the integration coordination loop, the nested memory model, the streaming-vs-traditional contrast) — genuinely aid comprehension; CC has no diagrams.
- **A concrete YAML Promptfoo config** with `is-json` / `javascript` / `llm-rubric` assertions — executable, pedagogically useful.
- **A TypeScript "component-prompt pair" snippet** — makes the abstract artifact concrete (`component` + `schema` + `semanticPrompt`).
- **Notion vector-DB infrastructure depth** — storage/compute decoupling, serverless S3, workspace-ID sharding, cold-start penalty; multi-region data residency (Japan, South Korea). If accurate, this is real added value CC lacks.
- **An eval-layer metrics table** with concrete thresholds — cosine similarity >0.85, tool-execution success >99.5%, 100% schema compliance.
- **EU AI Act Article 50 broken down by sub-provision** — 50(1) direct interaction, 50(2) synthetic content, 50(4) public-interest disclosure.
- **More aggressive speculative futures** — on-device/client-edge UI synthesis, cognitive-load-adaptive styling via gaze tracking, "Universal Zero-UI Core Engines."
- **The IP-ownership open question** — who owns a single-session synthesized layout.
- **The (suspect) Promptfoo/OpenAI acquisition claim** — listed here for completeness; see §4.2.

---

## 7. Rigor and confidence asymmetries

**This is the pair where the brief's hypothesis is most strongly confirmed.**

- **GEM presents as the more "engineering-credible" document — and that impression is partly manufactured.** ASCII architecture diagrams, a runnable YAML config, a TypeScript snippet, and LaTeX-style cost math all signal implementation rigor. But the 24 inline citations resolve to nothing, so none of the architectural claims behind those artifacts can be checked. The form of rigor is present; the substance of verifiability is absent.
- **GEM states contested or unverified things in the same flat, confident register as settled ones.** The Promptfoo acquisition (likely false), RSC-as-current-standard (contested), accessibility-at-scale-as-solved (contested), and gaze-tracked adaptive styling (speculative) are all delivered with the same declarative confidence as genuinely settled facts like the AI SDK lifecycle states. There is no tonal signal separating tiers of certainty.
- **CC signals uncertainty structurally.** "Weighted to shipped reality" framing; inline `[speculative]` tags; "unverified"/"direction solid, magnitudes untraceable" hedges; an 8-item "what surprised me" that includes self-critical findings; 6 open questions written as genuine unknowns. CC's working notes (`progress.md`) even document a verification step (footnote audit). The reader is told, repeatedly, what is solid and what is not.
- **Where GEM is genuinely better, say so:** the diagrams and code samples make GEM's implementation sections more immediately *usable* for an engineer than CC's prose; the Notion infrastructure section is more concrete than anything in CC; the EU AI Act sub-provision breakdown is sharper. GEM is not thin on *ideas* — it is thin on *evidence and epistemic honesty*.
- **CC's offsetting weakness:** at 12k words with 78 footnotes, it is a reference document, not a brief. A reader wanting an architectural orientation in 15 minutes is better served by GEM — provided they do not trust any specific number without checking it.
- **Net:** GEM looks more like a shipped engineering doc; CC *is* the more reliable one. The gap between GEM's apparent authority and its actual verifiability is the single most important signal in this comparison — and it is wider than in the foundation pair, because the implementation domain (versions, prices, acquisitions, infra) is exactly where unverifiable confidence is most dangerous.

---

## 8. Apparent weaknesses

### CC
- **Length** — 12k words; a strategic reader may not finish it.
- **Citation volume** — 78 footnotes are internally audited but impractical for a reader to spot-check; rigor by assertion of rigor.
- Occasionally re-litigates the RSC walk-back across multiple sections (foundation paper makes the same point) — some redundancy.

### GEM
- **No reference list.** 24 orphaned inline citations. The defining weakness; it makes the entire document unverifiable as an evidence base.
- **The Promptfoo/OpenAI acquisition claim** — specific, consequential, unsupported by the other agent's live-search research, and promoted to a headline finding. If false, it discredits part of §6 and one of three "surprises."
- **Presents contested claims as settled** — RSC currency, accessibility-at-scale, cross-device tractability.
- **Drops speculative labeling** in §10 — futuristic claims (gaze tracking, Zero-UI engines) are not distinguished from shipped reality, directly against the brief's "speculation clearly labeled" requirement.
- **Unnamed evidence** — "User research shows," "User expectation studies show" with no study cited.
- **Possible feature mischaracterization** (carried from its foundation doc's register) — confident attributions without sourcing make it hard to tell analysis from assertion.

---

## 9. Open questions for synthesis

1. **Verify the Promptfoo/OpenAI acquisition claim immediately.** It is asserted by GEM as fact and as a headline surprise; CC's research found nothing. Resolve before trusting GEM's evaluation section. If false, treat GEM §6 and "What Surprised You" with elevated skepticism generally.
2. **Vercel AI SDK RSC — current or walked back?** Opposed framings (same as the foundation pair). Determines how the whole "tool-call-renders-a-component" mechanic is presented.
3. **Is accessibility QA at scale solved or unsolved?** GEM's axe-core checklist vs. CC's "weakest-tooled, essentially unsolved." A real divergence with downstream governance implications.
4. **Cross-device handoff — known-architecture problem or genuinely open?** GEM (Kafka/DynamoDB sync) vs. CC (no way to serialize generative-UI state).
5. **How much of GEM's Notion infrastructure narrative is reliable?** It is the most valuable GEM-unique material *if* accurate, but it rests on unresolvable citations. Worth verifying against the one real Notion blog URL GEM provides.
6. **Which token-cost model?** The two worked examples use different scales and price assumptions; the synthesis needs one defensible calculation.
7. **Speculation posture for §10.** GEM's aggressive un-labeled futures (on-device synthesis, gaze tracking, Zero-UI) vs. CC's conservative, tagged speculation. Decide both the labeling discipline and how far out the paper should reach.
8. **Diagrams and code samples.** GEM's ASCII diagrams / YAML / TS snippets are a genuine usability gain CC lacks. The synthesis should likely adopt the *device* (visuals, runnable examples) while sourcing the *content* to CC's verified citations.
