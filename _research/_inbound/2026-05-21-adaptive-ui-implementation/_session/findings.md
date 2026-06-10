# Findings: Adaptive Interfaces — Implementation Paper

## Foundation paper notes (tone, scope, what NOT to duplicate)

**Tone/format:** Long-form analytical essay. Weighted to shipped reality; speculation labeled
inline `*[speculative]*` or in a dedicated subsection. Sits with tensions, refuses to flatten
disagreements. Footnote citations `[^N]` + numbered Bibliography at end. Ends with: Open
questions / What I should read next (ranked) / What surprised me.

**Foundation paper already covered (DON'T re-explain, only reference):**
- Six lineages: Sentient Design, Generative UI, Personalization incumbents, Malleable software,
  Adaptive interfaces (HCI/Gajos), Agentic UX.
- Personalization (segment-driven) vs adaptation (context-driven) distinction.
- UX of adaptive UI: trust/creepiness, mental-model cost, disclosure/agency.
- Evidence base: Gajos/Wobbrock ability-based design = strongest empirical case.
- Ethics: EU AI Act Art.5 manipulation prohibition; Colorado SB24-205; CA SB942/AB2013;
  decoy-effect finding (Liu & He) — LLMs more manipulable than humans.
- Production examples described at *what they ship* level: v0/AI SDK, Linear AI, Notion AI,
  Anthropic Artifacts, ChatGPT Canvas, Granola, Arc/Dia, Apple Intelligence, Spotify/Netflix,
  Google AI Mode, Perplexity Comet.
- Brief DS thread: system prompt as design artifact; component intent metadata; variant logging.

**Continuity rules for implementation paper:**
- This paper = HOW (architecture, design decisions, operational reality). Reference foundation
  examples but go into MECHANICS, don't re-describe features.
- Vercel walked back "generative UI" coinage — AI SDK RSC flagged experimental. Stay consistent.
- "Slot-based generation" (hand-designed shell, generated content, inferred selection) is the
  dominant shipped shape — foundation paper's term; reuse it.
- DS = one section near end, not the spine. Foundation §9 says implementation work
  (component APIs, intent metadata, variant logging, compliance instrumentation) belongs HERE.
- Do NOT cite Josh Clark's unreleased book. "Molten UX" attribution unverified.

## Research findings by section
_(filled from research agent reports)_

## Citations master list
_(author, title, link, date — deduplicated)_
