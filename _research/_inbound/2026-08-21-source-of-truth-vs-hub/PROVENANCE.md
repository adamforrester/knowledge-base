# Provenance — read before citing anything in this folder

**Supersedes `gemini-NOT-CAPTURED.md`, deleted 2026-08-23.** That file recorded an audit gap. The gap
was real, and it was **a different shape than recorded** — which is why this file replaces it rather
than being quietly swapped for a "closed" note.

## What this folder now contains

| file | what it is | status |
|---|---|---|
| `prompt.md` | the #876 brief, verbatim | issued |
| `claude.md` | Claude's run, in-repo, 2026-08-21 | matched brief ✅ |
| `gemini.md` | Gemini's run, captured 2026-08-23 | matched brief ✅ |

**Two runs against one brief. The dual-agent convention is satisfied for this run**, as of 2026-08-23.

## The gap, and why it was not the gap that was recorded

**What was originally recorded (2026-08-21):** a second run existed, its raw text had not been
supplied, and reconciliation had been done against an owner-supplied summary of it. The stated
problem was *missing text*.

**What was actually true (established 2026-08-23):** the report reconciled against on 2026-08-21 is
of **uncertain provenance**. The owner could not confirm it was run from `prompt.md`, and believes it
may have been a recollection of a *different* run on a different brief. **It was never established as
a matched-brief second pass**, which is what it was presented and treated as.

So the original file understated the problem. A missing raw text is a gap in the audit trail. **A
summary of unknown origin, treated as a matched second pass, is a gap in the reasoning** — it shaped a
published reconciliation, in this repo and in a comment on prism3 #876.

**The genuine second pass — `gemini.md` — was run afterwards, on the actual brief, and captured here.**

## The earlier report: classified, not discarded

It is cited in prism3 #876's comment and in knowledge-base PR #24, so it cannot simply vanish. Its
status:

- **Provenance: UNESTABLISHED.** Not confirmed to be a run of `prompt.md`. Possibly a different
  question, possibly a different brief, possibly a recollection.
- **Text: NOT HELD.** Only the owner's structured summary of it was ever available; that summary is
  not reproduced here, because reproducing a summary of an unverified source would give it a
  durability it has not earned.
- **Use: NONE, going forward.** Nothing in the rebuilt synthesis rests on it.

**Two claims entered the 2026-08-21 write-up from it alone and are now withdrawn as sourced claims:**

1. **That a "Design System Contracts" conflict existed between the two runs.** The real second pass
   (`gemini.md`) **does not mention Design System Contracts, Southleft, Christine Vallaure,
   `ds-contracts-poc`, a "three-way differ", or any A/B test.** That conflict was entirely an artifact
   of the unverified report. The underlying artifact is real — Claude's own `#882` run fetched
   `ds-contracts-spec.pages.dev` independently — but **the disagreement about it was not between two
   runs of this brief.**
2. **That Lona was cited as hub-failure evidence by a matched second pass.** It *was* so cited — but
   by the unverified report on 2026-08-21, and independently again by `gemini.md` on 2026-08-23. Only
   the second instance counts as corroboration. The conflict is real; its provenance needed fixing.

**If the earlier report is identifiable, it should be filed in its own dated folder against whatever
brief it answers.** An unciteable source that shaped a conclusion is worse than a weak one that is
labelled — which is the whole reason this file is long.

## What a reader should carry

1. **The 2026-08-21 reconciliation was rebuilt, not patched.** The superseded version is in git
   history and in PR #24's earlier commits; do not cite it.
2. **"Two independent runs agree" is a claim with a date now.** Before 2026-08-23 it was not
   established. After it, it is — for the four agreements named in the synthesis.
3. **The lesson is about the relay, not the model.** A summary of a run is not a run. It cannot be
   audited, its brief cannot be checked, and it is indistinguishable from a recollection at the point
   of use. The convention in `_research/README.md` — raw outputs, untouched, in-repo — exists exactly
   to make that failure impossible, and this run is the instance that shows what happens when it is
   bypassed even with good intentions on both sides.
