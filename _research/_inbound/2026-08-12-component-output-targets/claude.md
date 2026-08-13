# Claude run — component output targets (2026-08-13)

Raw output. Every external claim below was fetched during this run; URLs and fetch dates are inline.
Nothing here is authoritative until synthesised.

---

## Headline

**Web-components-primary does not survive contact with AEM and Drupal. CSS over server-rendered markup
is the primary projection; web components are a secondary, earned by the interactive tier only.**

The stronger finding sits underneath it: **`27` Idea 2's Phase 1 is aimed at the path Adobe now tells
new projects not to take.** That is not a small correction — it is the same shape as the SPA Editor
mistake KB 10 warns about, one generation later.

Confidence: **high** on the platform facts, **medium-high** on the ranking. What would change it is
named in the last section.

---

## Two corrections before the answers

**`docs/38` does not exist.** The brief says to read it, and #252's comment refers to "Arcs 1–3 of
`docs/38`" as the definition layer. There is no `docs/38-*` on `main` or on any of the 14 remote
branches (checked by `git ls-tree` per branch, 2026-08-13). Either it is unpushed, lives somewhere
else, or the arcs are a plan that was discussed but never written down. **Anything in this pass that
"feeds Arcs 1–3" is therefore feeding a document nobody can currently read**, which is worth fixing
before that dependency is load-bearing.

**KB 10 is stale in one named place** — see Drupal below. Its AEM material held up; its Drupal
material has been overtaken.

---

## 1. What an AEM engagement actually consumes

### The SPA Editor deprecation: KB 10 is correct

> "Adobe deprecated the SPA Editor with release 2025.01 of AEM as a Cloud Service, meaning that no
> further enhancements or updates will be made to its SDKs." … "The deprecation of the SPA Editor does
> not mean immediate removal, and if you have existing implementations, you can continue using it as
> long as it meets your needs." … "Adobe encourages you to use the Universal Editor for any new
> projects."

— Adobe, *SPA Editor Deprecation*, experienceleague.adobe.com (AEMaaCS), fetched 2026-08-13.

KB 10's "deprecated in January 2025" and "target Universal Editor or HTL-native, do not scope new SPA
Editor work" are both confirmed. **Deprecated, not removed** is the nuance to keep: existing estates
are supported, so this is migration debt rather than a cliff.

### But `27` Idea 2's Phase 1 now points at the wrong path for new work

Adobe's Core Components documentation — **last updated 2026-08-07, six days before this run** —
carries this:

> "for new projects, Adobe recommends leveraging Edge Delivery Services"

and frames Core Components as something to "continue using … for existing projects." Latest version
**2.32.4**; still maintained; still implements the Style System with BEM markup.

— Adobe, *Core Components Introduction*, experienceleague.adobe.com, fetched 2026-08-13.

`27` Idea 2 Phase 1 is *"tokens clientlib + a Prism3 skin layer over AEM Core Components' predictable
markup + Style System policies."* Every element of that is real and still works — **for the installed
base.** As the default bet for new AEM work it is now one generation behind Adobe's own guidance.

**This is the finding worth carrying.** KB 10 warns, correctly, not to scope new work to the SPA
Editor. The same reasoning now applies one level up: do not scope *new* AEM work to a clientlib +
Core Components skin without first asking whether the client is going to EDS.

### What Edge Delivery actually consumes, which decides this whole question

> "The javascript is loaded as a module (ESM) and exports a default function that is executed as part
> of the block loading."

— Adobe, *Anatomy of a Project*, aem.live, fetched 2026-08-13. The same page describes a **buildless**
approach served from GitHub: global `styles.css` plus `lazy-styles.css`, per-block CSS and JS under
`/blocks`, **no build step, no frameworks, no npm dependencies in the delivered front end.**

And EDS is not a hard cutover:

> "Edge Delivery Services and AEM Sites can co-exist on the same domain, which is a common use case
> for larger websites."

— Adobe, *Edge Delivery Services Overview*, experienceleague.adobe.com, fetched 2026-08-13. Two
authoring models: the Universal Editor (in-context WYSIWYG) or document-based authoring (Word /
SharePoint / Google Drive).

**So the #1 platform's recommended path for new work consumes a CSS file and a folder of blocks, each
block being vanilla CSS plus an ESM function.** The owner's throwaway line — *"it could be vanilla
HTML and CSS for all I care"* — turns out to be the platform-aligned answer, not a shrug.

### The real AEM shape is two-headed, and both heads consume CSS

| | Classic AEM (AEMaaCS / 6.5 estates) | Edge Delivery Services |
|---|---|---|
| Token delivery | tokens clientlib at the bottom of the dependency graph | `styles.css` custom properties |
| Component unit | HTL + Sling Model + dialog + clientlib | a block folder: `block.css` + `block.js` |
| Build | Webpack → clientlib-generator → Maven → Cloud Manager | none |
| Adobe's position | "continue using … for existing projects" | "for new projects, Adobe recommends" |

**Phase 2 is not "web components via clientlib".** For EDS the natural unit is a block. For classic
AEM, KB 10's own conclusion still stands and should be quoted back at `19` §3: *"For most VML AEM
engagements, especially content sites for marketing or brand clients, HTL-native remains the safest
architecture."* KB 10 also lists the WC-in-AEM frictions honestly — slot composition across an HTL
boundary is awkward, SSR is non-trivial, and **shadow DOM can interfere with Universal Editor
click-target instrumentation**.

### Drupal: SDC confirmed, and one stale KB claim

**Confirmed.** > "Starting with Drupal 10.3, Single-Directory Components became part of Drupal Core's
render system." — drupal.org, *Using Single-Directory Components*, fetched 2026-08-13.

**Stale — KB 10 §"Single Directory Components", the sentence "SDC is also the substrate for Drupal's
upcoming Experience Builder".** Experience Builder is no longer upcoming and no longer called that:

> "The Experience Builder module for Drupal is now Drupal Canvas."

— drupal.org/project/experience_builder, fetched 2026-08-13; that project is "only retained for
historic reasons", last release `0.7.4-alpha1`, 25 August 2025.

**Drupal Canvas is stable**: version **1.10.0, released 7 August 2026**, "Works with Drupal: ^11.3",
and covered by the security advisory policy — drupal.org/project/canvas, fetched 2026-08-13.

**The KB's conclusion survives the rename, with a wrinkle it should name.** Canvas's own native unit
is a **React "code component" authored in the browser as JSX**; a companion module ("Canvas Code
Components as SDC") registers those as SDC so they can be used outside Canvas, and Canvas validates
props at render "to match SDC behavior" (drupal.org/project/code_component and drupal.org/node/3574121,
fetched 2026-08-13). So **betting on SDC is still safe** — it is core, and Canvas converges on it —
but Drupal's newest visual builder is React-flavoured at the authoring layer, which is a fact worth
having before anyone says "Drupal is the non-React platform."

---

## 2. Does web-components-primary survive? No — and that is a finding, not a failure

**The case against, in order of weight.**

1. **Neither top platform wants a component runtime.** AEM's recommended new path is buildless vanilla CSS + ESM. AEM's classic path is HTL-native, which KB 10 calls the safest architecture for most VML engagements. Drupal's native unit is SDC — a Twig template plus a typed schema, rendered server-side.
2. **Shadow DOM is a liability on exactly the platforms we ship to.** KB 10 records that shadow DOM can interfere with Universal Editor instrumentation. Adobe's own editor is the thing our components would sit inside.
3. **The a11y constraint bites the components that most need WC.** ARIA IDREF associations do not cross shadow-root boundaries. Reference Target — the fix — is Phase 1 in **Chrome Canary behind the Experimental Web Platform features flag**, being prototyped in WebKit, with Mozilla positive and a proposal for **Interop 2026** (chromestatus.com/feature/5188237101891584 and igalia.com write-ups, fetched 2026-08-13). **Not shipped unflagged anywhere.** The components needing a state machine — combobox, listbox, dialog, tabs — are precisely the ones whose labelling and ownership relationships cross that boundary. A WC-primary library today either abandons shadow DOM (losing the encapsulation that justified WC) or ships an accessibility hole in its hardest components. For an accessibility-led practice that is disqualifying as a *primary*.
4. **React is prototypes.** So the usual argument for a neutral core — "we need one behaviour layer under many frameworks" — is answering a question the agency does not have.

**The case for, stated fairly.**

1. **It is the only shared *runtime* artifact.** If a client wants one interactive component library across AEM, Drupal, microsites and email, WC is the only thing that spans them without re-implementation. Spectrum Web Components is Adobe's own precedent, cited in KB 10.
2. **Drupal makes it easy.** KB 10: Custom Elements drop into Twig output as tags; no SPA Editor to navigate, no shadow-DOM instrumentation problem.
3. **It ages well.** No framework runtime to be stranded by.

**Verdict.** CSS over server-rendered markup is the **primary** projection. Web components are a
**secondary** projection scoped to the interactive tier, deferred until a client needs one runtime
across platforms — and, when built, strongly biased toward **light DOM** until Reference Target ships.

This is a reversal of `docs/19` §3, and the reason is specific rather than fashionable: §3 reasoned
from deployment-neutrality in the abstract. Deployment-neutrality (`15`) is about keeping the *engine*
free of host assumptions. It does not imply that the *output* should be the most portable possible
runtime — and §3 quietly slid from one to the other.

---

## 3. The minimum set of projections, ranked by commercial value

1. **The CSS / token layer.** Serves the AEM tokens clientlib, EDS `styles.css`, Drupal
   `THEME.libraries.yml`, Sitecore, Page Designer and any prototype, from one artifact. Mostly built:
   DTCG ships, Style Dictionary consumption is a gate. **Highest value, lowest marginal cost, and the
   only projection every named platform consumes.**
2. **A class-based skin layer** — the token layer applied to predictable server-rendered markup
   (Core Components' BEM classes, SDC templates, EDS blocks). This is `27` Idea 2 Phase 1 generalised
   away from Core Components specifically, and it is what "vanilla HTML and CSS" cashes out to.
3. **Drupal SDC.** Ranked above the AEM component projection despite Drupal being #2, because SDC's
   `*.component.yml` is a schema we can generate *directly* and because it is one directory rather
   than four surfaces. Best value-per-hour of any component projection.
4. **EDS blocks** for AEM. Adobe's recommended path for new work, and the same artifact shape as
   `docs/37`'s block axes — one body of work serving two lanes.
5. **Classic AEM HTL + Sling Model + dialog.** Highest cost (four surfaces per component), but it is
   where the existing enterprise estates are. Demand-driven, not speculative.
6. **Web components**, interactive tier only, per §2.
7. **React**, prototypes only — cheap once a behaviour layer exists, and a Storybook concern before
   then.
8. **Native mobile.** The token layer already serves part of it; nothing else until a real engagement.

**The ordering principle worth stating:** rank by *how many named platforms consume the artifact*,
then by cost. That puts CSS first and a component runtime sixth, which is close to the inverse of
`19` §3.

---

## 4. What each projection demands of the definition layer

`component-schema.ts` is better than `13` implies — `PropDef` already carries `name`, `type`,
`default`, `required`, `values`, `deprecated`, `description`. But four things it cannot express are
each required by a CMS projection, and none by React or WC. **That asymmetry is the whole finding.**

**(a) Authoring provenance — which props an author edits vs which the system fixes.** Nothing in
`ComponentDef` says this; grepping the schema for `author`/`editable`/`cms` returns only comment
prose. Both an AEM dialog and an SDC schema need it, and `27` Idea 2 already names the governance
model it serves — *"code-owned CSS, content-owned policy"*. **Today the schema cannot say which side
of that line a given prop or variant sits on.**

**(b) Typed validation.** SDC validates props against the component's schema at render time. Our
`PropDef.type` is deliberately a **free-form string** — the schema's own comment says *"keys locked,
values prose"*. That is the right call for a Figma/docs projection and insufficient for SDC, which
wants a machine-checkable type. A Drupal projection forces a typed prop vocabulary the schema
currently declines to have.

**(c) Slot content models and cardinality.** Anatomy expresses *that* a slot exists. A CMS needs to
know what may go in it and how many — one rich-text field, a list of 3–6 cards, a reference to
another component. Nothing expresses accepted content or min/max.

**(d) Authoring order as structure.** EDS blocks are authored as **document tables**, so row and cell
order *is* the schema. Nothing in `ComponentDef` says which parts are author-ordered.

**Consequence for the arcs (whichever document ends up holding them):** the definition layer needs a
**content-model facet** alongside anatomy and props, and it should be designed against SDC's
`component.yml` and an AEM dialog together — those two are the strictest consumers, and anything that
satisfies both will satisfy EDS and Page Designer. Doing it later means retrofitting authoring
provenance onto every existing def.

---

## 5. The headless-behaviour fork, since WC survives as secondary

Urgency drops sharply — this is now a tier-6 decision, not a first-slice blocker — but the corrected
facts point somewhere specific.

- **Wrap the machines, author the bindings.** #252's comment establishes that `@zag-js/core` and the component machines carry **no peer dependencies**, while Radix, React Aria, Ark and `@zag-js/react` all peer on `react`/`react-dom`. Wrapping Ark or Radix under a WC output would make React a runtime dependency of the neutral artifact — a reversal of the intent, not an implementation of it.
- **Prefer light DOM until Reference Target ships.** Cross-root ARIA is unsolved in shipping browsers; the machine-worthy components are the ones that need cross-root references. Light-DOM custom elements keep the ARIA graph intact and give up encapsulation we were not relying on anyway, since the styling contract is tokens rather than shadow boundaries.
- **Carry the tier rule from #252.** All five current defs are native semantics; the machine arrives with the first combobox and not before.
- **Ejection cost stands.** A wrapped dependency travels into every ejected repo. Zag is MIT.

---

## Recommendation, with confidence and falsifiers

**Recommendation.** Make the **CSS/token layer plus a class-based skin over server-rendered markup**
the primary component output. Build **Drupal SDC** first among component projections and **EDS blocks**
second. Treat **web components as a deferred secondary** for the interactive tier, light-DOM-biased.
Rewrite `docs/19` §3 to say this, and re-scope `27` Idea 2 Phase 1 so it is explicit about serving the
installed base rather than new builds.

**Confidence: high** that WC-primary is wrong for these platforms — that rests on Adobe's and Drupal's
current published positions, all fetched this run, plus an unshipped web-platform feature.
**Medium-high** on the ordering of 3 vs 4, which rests on a judgement about VML's client mix rather
than a fetched fact.

**What would change it, specifically:**

- **The client mix.** If VML's AEM estates are overwhelmingly classic AEMaaCS with no EDS migration in sight, EDS blocks drop below classic HTL and item 5 rises. **This is the single biggest unknown in the pass and it is answerable internally, not by research.** Nobody has written down how many live AEM engagements exist and which path each is on.
- **A client wanting one interactive library across AEM + Drupal + email.** That is the scenario where WC stops being deferred, and it is a real commercial shape, not a hypothetical.
- **Reference Target shipping unflagged** (Interop 2026 is the thing to watch). It removes the strongest technical objection to shadow DOM and makes a WC tier meaningfully cheaper.
- **Drupal Canvas adoption pulling toward JSX code components** rather than hand-authored SDC. Canvas is stable as of 2026-08-07, so this is live, not speculative.
- **React becoming a delivery target rather than a prototyping one.** Stated as unlikely by the owner; it would reorder everything below item 2.

---

## Sources fetched this run (all 2026-08-13)

- Adobe, *SPA Editor Deprecation* (AEMaaCS) — experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/hybrid/spa-editor-deprecation
- Adobe, *Core Components Introduction* — experienceleague.adobe.com/en/docs/experience-manager-core-components/using/introduction
- Adobe, *Edge Delivery Services Overview* — experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/edge-delivery/overview
- Adobe, *Anatomy of a Project* — aem.live/developer/anatomy-of-a-franklin-project
- Adobe, *Block Collection* — aem.live/developer/block-collection
- Drupal, *Using Single-Directory Components* — drupal.org/docs/develop/theming-drupal/using-single-directory-components
- Drupal, *Experience Builder* (superseded) — drupal.org/project/experience_builder
- Drupal, *Canvas* — drupal.org/project/canvas
- Drupal, *Canvas Code Components as SDC* — drupal.org/project/code_component; *props validated at render* — drupal.org/node/3574121
- Chrome Platform Status, *Reference Target for Cross-root ARIA* — chromestatus.com/feature/5188237101891584

**One URL guessed and 404'd** before being found by search: the SPA Editor deprecation page under
`experience-manager-core-components`. Recorded because a guessed URL that happens to resolve is how a
fabricated citation gets made.
