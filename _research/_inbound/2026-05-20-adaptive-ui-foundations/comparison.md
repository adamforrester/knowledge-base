# Foundation Pair — Agent Comparison

Comparison of the two **foundation paper** outputs. Analytical scaffolding for synthesis — surfaces convergence, divergence, and rigor gaps. Does not adjudicate.

- **CC** = Claude Code — `adaptive-interfaces-foundation-paper.md`
- **GEM** = Gemini Deep Research — `Synthesizing the Adaptive Interface-Agent2.md`

---

## 1. Metadata snapshot

| Attribute | CC (Claude Code) | GEM (Gemini) |
|---|---|---|
| Length | ~11,000–13,000 words | ~5,800 words (≈2.2× shorter) |
| File size | 74 KB | 35 KB |
| Structure | Preface + 9 numbered sections + Open Questions + What to Read Next + What Surprised Me + Bibliography | Title/abstract + ~10 titled sections + Open Questions + What to Read Next + What Surprised Us (no preface, no bibliography) |
| Closing sections | 6 open questions / 10 ranked reads / 8 surprises | 3 open questions / 6 ranked reads / 2 surprises |
| Citation apparatus | 74 numbered footnotes + ~21 "additional sources" — full author/title/date/URL | None. 6 sources in "What to Read Next" only; all other claims uncited |
| Voice / posture | Discursive analytical essay; skeptical-practitioner; hedges explicitly; sits with tensions | Polished strategic-academic prose; declarative, confident; few hedges; resolves tensions cleanly |
| Distinctive devices | Inline `*[speculative]*` tags; "what surprised me" self-critique | Comparison tables; one formal integer-programming equation; ASCII transformation diagram |
| Copy quality | Clean | Several errors: "proactivity surfacing/modifies" (×3), "Predictive predictability," "no longer routing global user profiles" |

---

## 2. Topical coverage map

Depth: ●●● substantial · ●● moderate · ● mention · — absent

| Topic | CC | GEM | Notes |
|---|---|---|---|
| Six converging lineages | ●●● | ●●● | Same six, near-identical names. GEM adds a 5-column taxonomy table |
| Personalization vs. adaptation | ●●● | ●●● | Both treat as central; both use a comparison table (GEM) / prose (CC) |
| Foundational theory (Weiser, Victor) | ● | ●● | GEM makes calm-tech / dynamic-media a synthesizing move; CC relegates to "read next" / additional sources |
| UX — trust / Clippy / creepiness | ●●● | ●●● | Both anchor on Clippy + Lumiere |
| UX — mental-model / muscle-memory cost | ●●● | ●●● | CC cites Findlater & McGrenere; GEM cites Hick's/Fitts's Law |
| UX — disclosure / agency / control | ●●● | ●● | CC has dedicated treatment (visible thinking, cheap dismissal, side-by-side) |
| When users want adaptation vs. predictability | ●●● | ●● | CC has explicit empirical cut; GEM covers via "predictive predictability" |
| Empirical-thinness acknowledgement | ●●● | — | CC §3.5 names the thin evidence base; GEM never flags it |
| Problems solved — accessibility / ability-based design | ●●● | ●●● | Strongest shared claim. GEM adds a SUPPLE optimization equation |
| Problems solved — discovery / cognitive load | ●●● | ●● | GEM frames as novice/power-user info density |
| Problems solved — onboarding / time-to-value | ●●● | ●● | GEM frames as "onboarding → progression phase" |
| Where it underperforms | ●●● | ●● | Both name EHR/healthcare, power users, regulated, brand surfaces |
| Ethics — EU AI Act | ●●● | ●● | CC cites Article 5(1)(a–b), Recital 29; GEM cites the Act generically |
| Ethics — US state law | ●●● | ● | CC names Colorado SB24-205, CA SB942, AB2013; GEM says "California's legislative actions" (vague) |
| Ethics — LLM manipulability / decoy effect | ●●● | — | **CC only.** Liu & He decoy-dilemma finding; GEM absent |
| Ethics — epistemic risk / "dark forest" | ●● | — | CC (Appleton dark-forest); GEM absent |
| Ethics — algorithmic/generative dark patterns | ●● | ●●● | GEM's framing of a metric-driven engine self-deploying dark patterns is sharper |
| Industries / use cases | ●●● | ●●● | Both use a fit table; **disagree on e-commerce** (see §4) |
| Production examples | ●●● (11) | ●● (8) | CC adds Google AI Mode, Perplexity Comet, Dia; GEM omits these |
| Where this is headed [speculative] | ●●● | ●● | Both label speculation; GEM 2 scenarios, CC more |
| Design system thread | ●● | ●●● | GEM gives it a fuller named section ("Design System Paradox"); CC keeps "brief" by design |

---

## 3. Areas of agreement

- **The six-lineage taxonomy.** Both independently land on the same six: Sentient Design, Generative UI, (Legacy) Personalization, Malleable Software, Academic Adaptive Interfaces (Gajos lineage), Agentic UX. Naming is near-identical.
- **Personalization vs. adaptation is the load-bearing distinction.** Both: personalization = segment/cohort-driven, slow, deterministic variant-selection; adaptation = context-driven, real-time, generative. CC §2 / GEM "Personalization vs. Adaptation."
- **The two can coexist.** Both use the same example shape — server-side personalization choosing the content library, client-side adaptation restructuring the live layout. CC §2 (Spotify Home vs. AI DJ); GEM "These models can coexist."
- **Ability-based design is the strongest empirical case.** Both center Gajos / Wobbrock / SUPPLE and ability-based design as the most defensible evidence for adaptive UI. CC §4.1 / GEM "Accessibility: Ability-Based Design." Both also flag this work is ~20 years old and under-cited today.
- **Clippy is the cautionary anchor.** Both trace Clippy to Microsoft Research's Lumiere project and to the social-response mechanism (CC: Reeves & Nass *Media Equation*; GEM: "Nass and Reeves's Computers Are Social Actors"). Both conclude the fix is deference.
- **Muscle memory / spatial stability is a real cost.** Both: structural layout shifts reset learned motor paths; certain frames must stay static. CC §3.2 / GEM "Cognitive Cost of Shifting Mental Models."
- **Appleton's squish/structure.** Both cite it, both with the same resolution: translate "squishy" NL intent into structured/validated parameters (JSON/Zod) that render predictable GUI components.
- **Healthcare/EHR is a weak fit; productivity SaaS and education are strong.** Industry tables converge here.
- **The design system survives but transforms.** Both: from a static library of pre-composed components → a system of tokens, constraints, semantic metadata, and layout slots that an engine composes against. CC §9 / GEM "Design System Paradox."
- **Regulation is a live constraint, not a someday problem.** Both foreground the EU AI Act and US state-level disclosure law as already shaping design.
- **Speculative futures.** Both [speculative]-label the same two: disposable/short-lived single-session UI, and the accessibility tree becoming the agent-facing API.

---

## 4. Areas of disagreement

State both versions; do not adjudicate.

**4.1 Status of "Generative UI" / Vercel AI SDK RSC**
- **CC:** the term is "a 2024 artifact in active retreat by the company that coined it" — Vercel flagged its RSC generative-UI primitives "experimental" and published a migration guide away from them (CC §1.2, Preface flag #3).
- **GEM:** presents Generative UI / RSC straightforwardly as "the technical implementation of dynamic interface compilation"; "What to Read Next" calls Vercel AI SDK 3.0 "the industry-standard developer implementation model."
- Directly opposed framings of the same technology's maturity.

**4.2 E-commerce as a use-case fit**
- **CC:** "Strong fit" — "the fifteen-year personalization story … is the prototype" (CC §6.1).
- **GEM:** "Ambiguous" — rationale: variable user intent, "algorithmic dark patterns, brand-integrity degradation, checkout errors" (GEM industry table).
- A clean contradiction in the fit verdict. (Consumer fintech similar: CC "Strong"; GEM "Ambiguous.")

**4.3 Clippy's root cause**
- **CC:** primarily a *consistency* failure (cites Swartz 2003) and a productization decision — an always-visible animated agent imposed on a probabilistic system that was itself modest.
- **GEM:** "not poor intent-inference, but a lack of design deference"; explicitly asserts "Microsoft's Lumiere engine was mathematically advanced for its time."
- Compatible in spirit (both: not an inference failure) but different named mechanisms — consistency (CC) vs. deference (GEM).

**4.4 Evidence base for the mental-model cost**
- **CC:** anchors on Findlater & McGrenere 2004 (users often *prefer* the static menu) and Findlater et al. 2009 (ephemeral adaptation).
- **GEM:** anchors on Hick's Law and Fitts's Law; does not cite the Findlater empirical work.
- Not contradictory, but the agents support the same point with non-overlapping evidence — and CC's anchor is direct empirical UI research while GEM's is general cognitive law.

**4.5 Depth vs. economy as a deliberate posture**
- Not a factual disagreement, but a structural one the synthesis must reconcile: CC treats comprehensiveness and hedging as the job; GEM treats a tight, resolved, executive-readable brief as the job. They are not the same document compressed — they are different documents.

---

## 5. Sources

### CC — sources cited
- **74 numbered footnotes + ~21 "Additional sources."** Full author/title/date/URL throughout. Categories: academic HCI with DOIs (Gajos, Wobbrock, Findlater, Horvitz, Lim, Vaithilingam, Feng); practitioner essays (Clark/Big Medium ×~10, Saarinen/Linear ×3, Appleton ×4, Litt ×3, Butler ×2, Matuschak ×2); NN/g articles (×~8); regulatory primary sources (EU AI Act Article 5 & Recital 29, Colorado SB24-205, CA SB942, CA AB2013); vendor/product pages and engineering blogs (Vercel, Netflix, Spotify, Amazon Science, Granola, Linear).
- **Self-flagged weak sources** (CC discloses these itself): `[^62]` LayerX "CometJacking" — "primary disclosure URL not captured"; `[^66]` OpenAI "Introducing Canvas" — "Primary URL not retrievable … triangulated from secondary sources." Note the honesty: the suspect citations are labelled as suspect in the original.
- Full numbered bibliography lives in the source document (`[^1]`–`[^74]` + additional list).

### GEM — sources cited
**Formal (the only 6, all in "What to Read Next"):**
1. Litt, Horowitz, van Hardenberg & Matthews — *Malleable Software: Restoring User Agency in a World of Locked-Down Apps* — Ink & Switch, June 2025.
2. Wobbrock, Kane, Gajos & Harada — *Ability-Based Design: Concept, Principles and Examples* — ACM TACCESS, April 2011.
3. Vercel — *AI SDK 3.0: Generative UI* — Vercel Blog, March 2024.
4. Karri Saarinen — *Design is More Than Code* — Linear Blog, December 2025.
5. Gibbons & Moran — *AI Agents as Users* — Nielsen Norman Group, April 2026.
6. Maggie Appleton — *Squish Meets Structure* — MaggieAppleton.com, November 2023.

**Inline name-drops with no citation:** Mark Weiser (ubiquitous computing / calm technology), Bret Victor (dynamic media), Nass & Reeves (CASA / *Computers Are Social Actors*), Krzysztof Gajos / SUPPLE, Wobbrock/Kane/Gajos/Vanderheiden, Ink & Switch, Hick's Law, Fitts's Law, EU AI Act, "California's legislative actions."

### Source observations
- **Overlap:** all 6 GEM formal sources also appear in CC's bibliography (CC `[^16]`, `[^22]`, `[^7]`, additional-sources list, `[^27]`, `[^17]` respectively) — GEM's curated set is a strict subset of CC's.
- **The Saarinen citation, specifically.** GEM cites *Design is More Than Code* (Dec 2025). CC's headline Saarinen citations are *Design for the AI Age* (`[^35]`, April 2025) and *Output Isn't Design* (`[^50]`, April 2026); CC lists *Design Is More Than Code* only in its un-numbered "additional sources." Same author, three different essays — the agents are leaning on **different primary texts** for the Saarinen/Linear position, which may carry different claims. Worth checking before synthesis.
- **Suspect — GEM:** no fabricated source identified, but the structural problem is **absence of attribution**: ~95% of GEM's factual claims (the SUPPLE optimization equation, the Clippy/Lumiere history, the EU AI Act provisions, the production-example mechanics) carry no citation at all. The SUPPLE integer-programming equation in particular is presented with mathematical authority but **no source** — it cannot be verified as SUPPLE's actual cost model vs. a plausible reconstruction.
- **Suspect — GEM:** "California's legislative actions on algorithmic transparency" — vague attribution, no bill named.
- **Suspect — CC:** the two self-disclosed weak citations above. No un-disclosed suspect sources identified.

---

## 6. Unique substantive contributions

### CC only
- **The "molten UX" debunk.** CC's preface flag #1: the phrase commonly attributed to Josh Clark could not be verified in any reviewed public source. GEM never raises it.
- **LLMs are more susceptible to choice-architecture manipulation than humans** — the Liu & He decoy-effect finding. CC treats this as its single most important empirical claim. Entirely absent from GEM.
- **The personalization incumbents are statistically sophisticated** — Adobe Random Forests retrained every 24h, multi-armed bandits, Thompson sampling. GEM characterizes incumbents only as "static … pre-baked design variants."
- **Saarinen and Clark are publicly disagreeing** about the central thesis (CC "what surprised me" #8) — a live debate GEM presents as a settled consensus.
- **Specific regulatory instruments** — Colorado SB24-205, CA SB942, CA AB2013, EU Article 5(1)(a–b) + Recital 29 with the "effect, not intent" point.
- **Production examples GEM omits entirely:** Google AI Mode (query fan-out), Perplexity Comet (CometJacking), the Arc → Dia pivot.
- **Explicit empirical-thinness section** (§3.5) — names that NN/g's agentic-UX base is one n=6 study.

### GEM only
- **A formal SUPPLE optimization equation** — integer-programming cost-minimization with defined terms. CC describes SUPPLE as constrained optimization in prose but never formalizes it.
- **Weiser + Victor as a synthesizing frame.** GEM uses calm technology and dynamic media as the theoretical lens that reconciles the six lineages; CC mentions both only peripherally.
- **"Who holds final agency" as the organizing axis.** GEM's sharpest framing: the lineages "do not fully reconcile because they disagree on who holds final agency" (system vs. user). CC discusses agency but never crystallizes it into a single comparative axis.
- **The lineage taxonomy table** with Primary Driver / Target Interaction Node / Conceptual Stance / Technical Substrate columns — a compact artifact CC has no equivalent of.
- **Cleaner articulation of the generative dark-pattern mechanism** — a metric-driven engine *autonomously learning and deploying* a manipulative layout "without explicit human intervention."

---

## 7. Rigor and confidence asymmetries

The brief's hypothesis — GEM polished prose can mask thinness; CC scrappier but more rigorous about gaps — is **partially borne out** here (and more strongly in the implementation pair).

- **GEM reads as more authoritative than its evidence supports.** It is well-organized, declarative, and free of hedges; the SUPPLE equation and the clean taxonomy tables project rigor. But almost nothing is cited. A reader cannot trace a single claim in the body. The polish is real; the verifiability is near-zero.
- **CC surfaces uncertainty that GEM resolves silently.** CC has a whole section (§3.5) conceding the empirical base is thin; an 8-item "what surprised me" including self-correcting findings; and explicit "I cannot resolve this" language in its open questions. GEM's confident tone never signals that any claim is contested — e.g. it presents Generative UI/RSC as settled standard exactly where CC documents an active vendor retreat.
- **CC self-flags its own weak sources** (CometJacking, OpenAI Canvas). GEM has no mechanism to do so because it has no citation layer.
- **Where GEM is genuinely strong, say so:** its tables (lineage taxonomy, personalization-vs-adaptation, industry fit) are tighter and more scannable than CC's prose equivalents; the agency framing is a real analytical contribution; and at ~5,800 words it is far more executive-readable. GEM is not thin *everywhere* — it is under-evidenced, not under-thought.
- **Where CC over-delivers into a different risk:** at 2.2× the length, CC trades scannability for completeness. Its rigor is real but the document is long enough that a strategic reader may not finish it. "More rigorous" and "more usable for a 20-minute decision" are not the same axis.
- **Net:** CC is the more trustworthy evidence base; GEM is the more communicative artifact. The asymmetry is rigor vs. legibility, not competence vs. incompetence.

---

## 8. Apparent weaknesses

### CC
- **Length.** ~12k words for a "foundation" brief risks not being read by the intended audience.
- **Self-disclosed soft citations** (CometJacking, OpenAI Canvas) — honest, but still soft.
- Dense footnote apparatus can read as over-armored for a strategic document.

### GEM
- **No citation apparatus.** The defining weakness. No footnotes, no bibliography, ~6 sources total for a ~5,800-word survey making dozens of specific historical, legal, and technical claims.
- **The SUPPLE equation is uncited** and presented as fact — high authority, zero traceability.
- **Presents contested claims as settled** — most notably the "Generative UI / RSC is the industry standard" framing, which CC's evidence directly contradicts.
- **Vague legal attribution** — "California's legislative actions" with no instrument named.
- **Omits the LLM-manipulability finding** — arguably the most consequential ethics result of the period; its absence is a substantive coverage gap, not just a citation gap.
- **Copy-editing errors** ("proactivity" as adverb ×3, "Predictive predictability," "no longer routing") — minor, but a quality signal in a document whose main asset is polish.
- **Production examples are static-as-of-an-earlier-snapshot** — covers Arc Max but not the Arc→Dia pivot CC documents.

---

## 9. Open questions for synthesis

1. **Is "Generative UI" a current standard or a walked-back term?** CC and GEM give opposed answers. The synthesis must pick a framing — it shapes how the whole "Generative UI" lineage is presented.
2. **E-commerce fit: strong or ambiguous?** A direct contradiction in the industry verdict (and a softer one on fintech).
3. **Include the LLM-manipulability / decoy-effect finding?** CC treats it as the headline ethics result; GEM omits it. If included, it materially changes the ethics section's center of gravity.
4. **Which Saarinen text(s)?** Three different essays are in play across the two docs; confirm which claims each actually supports.
5. **Formalize SUPPLE or not?** GEM's equation adds rigor-by-appearance but is unsourced; decide whether to source-and-keep or drop.
6. **Target length and posture.** CC ≈ comprehensive reference; GEM ≈ executive brief. The synthesis needs a deliberate decision on which it is — they cannot simply be averaged.
7. **Clippy's named mechanism** — "consistency failure" (CC/Swartz) vs. "deference failure" (GEM). Minor, but they imply slightly different design prescriptions.
8. **How much foundational theory (Weiser, Victor)?** GEM makes it structural; CC makes it peripheral. Decide its weight.
