# Synthesis — surface context (inverse / on-color)

> Reconciles two independent runs of the same brief: `claude.md` (Claude, in-repo) and
> `external-agent.md` (Gemini). Both recommend the same mechanism. The disagreements are where the
> value is, and one of them is a contradiction *within* the external agent's own work across two
> runs. Not authoritative — this is synthesis scratch, not the practice's POV.

---

## Where they agree, and it probably holds

**The cascade is the mechanism** *(both agents)*. Neither recommends a per-component variant axis.
Both identify the design-to-code synchronisation gap in Figma as the strongest objection, and both
arrive there independently of the other.

**Every surveyed first-party system is doing something other than a variant axis** *(both agents)*.
Material and Primer put it in tokens; Carbon uses a `<Theme>` container; Atlassian's `Text`
auto-inverts inside a bold-background `Box`. Spectrum is the exception and it refuses the framing
rather than accepting it — `staticColor="white"|"black"` names the ink and never describes the
surface, which is a fifth option neither the brief nor the external run anticipated *(Claude only)*.

**The convergence is not fully independent.** Both agents received the same brief, and that brief
named four options. Reading agreement between them as two confirmations overstates it. The
strongest evidence that the framing did not fully capture the field is Spectrum, which one run found
by refusing to classify it.

---

## Where they diverge

**Salesforce Lightning.** The external run reports COULD NOT VERIFY. The in-repo run counted the
shipped stylesheet: 455 distinct global `--slds-g-*` hooks with 11 carrying inverse (2.4%), and 476
component `--slds-c-*` hooks with 21 (4.4%), those 21 spanning exactly three components — avatar,
badge, button *(Claude only)*.

That is the most decision-relevant finding in either run and documentation-only research missed it
entirely. The lesson generalises: **when docs are unreachable, count the shipped code.** The same
move later found that Drupal's schema is richer than Drupal's documentation.

**Material Design 3's classification.** The external run files it under Option 4, a theme mode. Its
own quoted evidence — *"inverse roles are applied selectively to components"* — describes tokens,
not modes. The classification is looser than the citation supporting it. We take the tokens read.

---

## Reliability flags on `external-agent.md`

Recorded so that a later synthesis does not treat the two runs as equally sourced throughout.

**The Figma mode ceilings are uncited and wrong.** The external run states *"standard professional
plans to 4 modes and enterprise plans to 40 modes"* in prose, outside its own VERIFIED section, with
no source. The in-repo run explicitly declined to repeat the commonly-cited figure without one. The
owner subsequently confirmed the real numbers from a live account: **Pro 10, Organisation 20,
Enterprise 40.** Both external figures are wrong, and the recommendation had been argued partly on
the strength of a ceiling that does not exist.

**The Drupal claim rests on an open core issue.** The external run cites drupal.org issue #3531854
and concludes *"Drupal core is actively standardising on CSS custom properties… Option 3 is the
native paradigm for both environments."* An issue is a proposal, not shipped documentation, and *"is
actively standardising"* is a present-tense claim about mutable state.

**And the same agent contradicts this in its own later run.** The white-label brief produced: *"In
contrast to AEM EDS's implicit section-level cascading metadata, Drupal SDC authors explicitly pass
the variant down to the component via form fields."* The two statements are incompatible; the second
is better sourced, because it describes SDC's actual authoring model. Combined with the in-repo run's
*"SDC has no documented implicit-context mechanism at all,"* two of three passes now stand against
the first answer. **The platforms diverge** — EDS is a container cascade, SDC is an explicit prop —
and any synthesis asserting that both platforms want a cascade is repeating the unsupported version.

**The Polaris regret citation is weaker than presented.** The quote describes *"multiple checks for
variants that apply different classes leading to code that's harder to maintain"* — regret about how
variant checks were implemented, not evidence that a variant axis is architecturally wrong. Real, and
not the migration-away-from-variants finding the section claims.

---

## What we measured ourselves, which neither run covered

Both runs argue about whether inverse should be a mode. Neither asks whether inverse and dark mode
are the *same values*. Measured across all four generated brands, comparing every inverse-named token
against its dark-mode counterpart:

| | match | differ | no counterpart |
|---|---|---|---|
| aurora | 24 | 10 | 2 |
| harbor | 24 | 11 | 1 |
| nb | 24 | 10 | 2 |
| wendys | 24 | 9 | 3 |
| **all** | **96** | **40** | **8** |

**67% identical, 33% deliberately different** — and the divergence is not scattered. It clusters on
`interactive.*.fill.*` and `on-fill`, in the same places, in all four brands. A primary button on a
dark band inside a light page takes a near-white fill; the same button in full dark mode takes a
mid-tone brand fill.

So **an inverse surface is not a dark-mode surface**, and collapsing them would silently change forty
values, all of them on interactive fills, with every value still resolving and no gate able to see it.

This corroborates the sharpest finding of the white-label run: Mística required *"entirely different
accessible text tokens"* for an inverse surface in Blau versus Movistar, *"necessitating unique token
resolutions rather than generic inversion."* Two systems, independently: inversion is authored, not
computed.

---

## Open, and worth carrying forward

- **Whether the consumption half is documented anywhere.** Both platforms document publishing
  context. Neither documents how a component inside consumes it. The in-repo run found Adobe's own
  guidance on Section Metadata says *"it is recommended to avoid it, until it is really necessary"* —
  we have not established the scope of *"it"*, and that matters before treating it as a blocker.
- **Nested inversion is named by both runs and tested by neither** — a light card inside a dark band.
  Both call it the cascade's sharpest failure mode.
- **shadcn/ui went unsourced in both external runs.** For a library that well documented, that is a
  search failure rather than an absence.
