# Figma Variables vs. Styles, and the code → Figma round-trip

*Claude's run of the dual-agent brief. Researched 2026-06-28 against primary
sources: Figma Plugin API and REST API (developers.figma.com), the
machine-readable OpenAPI spec behind those docs
(`github.com/figma/rest-api-spec`), Figma Help Center, and the W3C DTCG spec.
Every load-bearing claim is cited; claims that depend on plan tier or recent
releases are dated and flagged. A confidence ledger closes the document.*

> **Two findings overturn the common mental model and should be read first:**
> (1) an Effect Style can bind a shadow's **numeric** fields (radius, spread,
> offsetX, offsetY) to variables, not only its colour; (2) as of **Config 2026 /
> Figma Motion (GA ≈24 Jun 2026)** Figma has **timing and easing variables** — so
> motion is no longer entirely "homeless" in the variable model. Both are recent
> and the second is days old at time of writing; treat the motion round-trip as
> not-yet-stable.

---

## 1. Why this is a Variables-vs-Styles problem, not a naming problem

A Figma **variable** can resolve to exactly **four** scalar types and nothing
else. Plugin API `VariableResolvedDataType`, verbatim: `"BOOLEAN" | "COLOR" |
"FLOAT" | "STRING"`. The REST API agrees (`resolvedType` enum: `BOOLEAN, FLOAT,
STRING, COLOR`). There is **no composite, array, gradient, dimension-with-unit,
or expression variable type**. (VERIFIED — Plugin API `VariableResolvedDataType`;
REST `variables-endpoints`.)

Three consequences fall straight out of that ceiling:

- A **dimension** is just a unitless `FLOAT` (`4`, not `"4px"`). Units live in the
  variable *name* or the consuming context, never the value.
- A **typography** or **shadow** token has **no single-variable representation at
  all**. It can only exist in Figma as a **Style** (a different object class) whose
  sub-properties are individually bound to atomic variables.
- Anything needing maths/expressions or a composite shape is pushed either to a
  Figma Style or out to a third-party layer (Tokens Studio).

So the round-trip problem is not "what do we call the token" — it is "this token
class does not exist as a variable, and must be reconstructed as a Style + bound
atoms." That is the whole game.

---

## 2. The variable model in detail

**The scope vocabulary — with a documented divergence to note.** The Plugin API
`VariableScope` page enumerates **22** values; the OpenAPI spec (`main`, fetched
today) lists **23**, the extra being **`FONT_VARIATIONS`**. The 22 common to both:

```
ALL_SCOPES, TEXT_CONTENT, CORNER_RADIUS, WIDTH_HEIGHT, GAP,
ALL_FILLS, FRAME_FILL, SHAPE_FILL, TEXT_FILL, STROKE_COLOR, EFFECT_COLOR,
STROKE_FLOAT, EFFECT_FLOAT, OPACITY,
FONT_FAMILY, FONT_STYLE, FONT_WEIGHT, FONT_SIZE, LINE_HEIGHT,
LETTER_SPACING, PARAGRAPH_SPACING, PARAGRAPH_INDENT
```

(+ `FONT_VARIATIONS` in the OpenAPI spec — VERIFIED present there; the rendered
Plugin API page omits it. Treat `FONT_VARIATIONS` as real but newer/under-
documented.)

**Validity by resolvedType** (VERIFIED, Plugin API `VariableScope`):

| resolvedType | valid scopes |
|---|---|
| **FLOAT** | `ALL_SCOPES`, `TEXT_CONTENT`, `CORNER_RADIUS`, `WIDTH_HEIGHT`, `GAP`, `OPACITY`, `STROKE_FLOAT`, `EFFECT_FLOAT`, `FONT_WEIGHT`, `FONT_SIZE`, `LINE_HEIGHT`, `LETTER_SPACING`, `PARAGRAPH_SPACING`, `PARAGRAPH_INDENT` |
| **COLOR** | `ALL_SCOPES`, `ALL_FILLS`, `FRAME_FILL`, `SHAPE_FILL`, `TEXT_FILL`, `STROKE_COLOR`, `EFFECT_COLOR` |
| **STRING** | `ALL_SCOPES`, `TEXT_CONTENT`, `FONT_FAMILY`, `FONT_STYLE` |
| **BOOLEAN** | none — scoping is "currently supported for FLOAT, STRING and COLOR variables" only |

Note `FONT_WEIGHT`/`FONT_SIZE` are **FLOAT** scopes while `FONT_FAMILY`/
`FONT_STYLE` are **STRING** scopes — consistent with how Figma stores those
fields. `ALL_SCOPES` and `ALL_FILLS` are exclusive (if set, no other scope may be
added).

**Scoping is a UI filter, not a constraint.** Verbatim: *"Setting scopes for a
variable does not prevent that variable from being bound in other scopes (for
example, via the Plugin API). This only limits the variables that are shown in
pickers within the Figma UI."* (VERIFIED.) **Implication:** scopes are
discoverability/UX, never validation or governance — a `CORNER_RADIUS`-scoped
variable can still be bound to a gap programmatically. Do not lean on scopes as a
guarantee.

**`codeSyntax`** is a per-variable, per-platform code-name map with optional keys
`WEB`, `ANDROID`, `iOS` (note lowercase `i`). Free-form strings, settable on
create and update; surfaced in Dev Mode. A pipeline should populate it with the
platform-idiomatic output name it already emits (e.g. `WEB:
"--nbds-font-size-body-xs"`). Emitting `{}` is valid (all keys optional).
(VERIFIED — `VariableCodeSyntax`.)

**Collections, modes, caps.** Modes are a single flat axis per collection;
multi-axis theming is done with *multiple* collections (the one-mode-dimension-
per-collection pattern — true in the data model; no single verbatim doc sentence).
Two layers of limits, both real and non-contradictory:

- **Per-plan editing caps (DATE-SENSITIVE, HIGH volatility — re-verify on
  figma.com/pricing):** Free/Starter = modes effectively unavailable (single
  default mode); Professional ≈ "up to 10 modes per collection"; Organization ≈
  "up to 20"; Enterprise = "unlimited (extended collections)." Figma has revised
  these repeatedly.
- **Hard platform caps (VERIFIED, REST):** max **40 modes** and **5000
  variables** per collection; mode names ≤ 40 chars; variable names unique within
  a collection and may not contain `.{}`; POST body ≤ 4 MB.

---

## 3. Figma Styles as a distinct object class

**Four style types, stored and created separately from variables.** Plugin API
`BaseStyle = PaintStyle | TextStyle | EffectStyle | GridStyle`, discriminated by
`type`: `'PAINT'`, `'TEXT'`, `'EFFECT'`, `'GRID'`. The REST API exposes them as a
separate `Style` resource with `style_type` enum **`FILL | TEXT | EFFECT | GRID`**
(note the REST `FILL` vs Plugin `'PAINT'` — same concept, different string per
surface). Styles carry their own ids (`key`/`node_id`), separate from
`VariableID:*`. (VERIFIED — `BaseStyle`, `component-types`.)

**What can bind to variables inside a style — current, and broader than the
legacy model:**

- **Text Styles.** `setBoundVariable(field, variable)` binds `fontFamily`,
  `fontStyle` (STRING vars) and `fontWeight`, `lineHeight`, `letterSpacing`,
  `paragraphSpacing`, `paragraphIndent` (FLOAT vars). `fontSize` is **omitted from
  the doc's prose bullet list** but `FONT_SIZE` is a real scope and font-size
  binding is shipped — treat the omission as a doc gap, not a capability gap.
  (VERIFIED with that caveat — `TextStyle`, `working-with-variables`.)
- **Effect Styles.** `VariableBindableShadowEffectField = 'radius' | 'color' |
  'spread' | 'offsetX' | 'offsetY'` — i.e. **the numerics bind too, not only
  colour**, via `setBoundVariableForEffect(effect, field, variable)`. Blur effects
  bind `radius`. Texture/noise effects do not support binding. (VERIFIED —
  `VariableBindableEffectField`, `EffectStyle`.) **This corrects the widespread
  "only a shadow's colour can be a variable" assumption.**

**The decomposition rule (the architectural crux):**

| DTCG token | Figma representation |
|---|---|
| `color` | single `COLOR` variable — clean 1:1 |
| `dimension` / `number` | single `FLOAT` variable — clean 1:1 |
| composite **`typography`** | **no single variable** → atomic STRING/FLOAT vars **bound into a Text Style**; the Style *is* the composite |
| composite **`shadow`** | **no single variable** → an **Effect Style** whose per-layer `color/radius/spread/offsetX/offsetY` bind to atomic vars; multi-layer = ordered `Effect[]` |
| `transition` / `duration` / `cubicBezier` / `spring` | **see motion update below** — historically no home; now partial |

**Motion — the part that changed in June 2026.** Pre-2026, duration/easing/spring
had no Figma variable or style home; they could only be exported as
documentation-shaped FLOAT/STRING variables binding to nothing, and real motion
lived in prototype interaction settings. As of **Config 2026 / Figma Motion (GA
rollout ≈24 Jun 2026)** Figma introduced **timing and easing variables** and an
animation/keyframe model, with a **beta Plugin Motion API** (`figma.motion.*`,
`applyAnimationStyle()`, `applyManualKeyframeTrack()`, and `MotionEasing |
VariableAlias` value types). (VERIFIED that the feature exists; the exact
tokens-round-trip mechanics are UNCONFIRMED and the API is explicitly beta.)
**Practitioner takeaway:** motion tokens now have a *plausible* Figma home for the
first time, but no stable composite-motion round-trip exists yet — do not assume a
DTCG `transition` survives a code→Figma write. Re-verify before building on it.

---

## 4. Writing tokens back into Figma (code → Figma)

**The headline constraint: the REST Variables API — read *and* write — is
Enterprise-only.** Verbatim on all three endpoints: *"This API is available to
full members of Enterprise orgs"*; overview: *"you must have a Full seat in an
Enterprise org; guests cannot use the API."* Read = Tier 2 `file_variables:read`;
write = Tier 3 `file_variables:write` + edit access to the file. There is **no
"read cheap, write Enterprise" split** — both gate on Enterprise. (VERIFIED, doc
wording quoted. DATE note: Figma has loosened API gating before; re-check if it's
load-bearing.) After a REST write you must **publish** before consuming files see
the change.

**The POST payload model** (VERIFIED — `variables-endpoints`, OpenAPI):

- Four top-level **arrays applied in order**: `variableCollections`,
  `variableModes`, `variables`, `variableModeValues`. (GET returns id-keyed
  *maps*; POST takes *arrays* — the shapes are not symmetric.)
- Every collection/mode/variable change carries an `action`: `CREATE | UPDATE |
  DELETE`.
- **`tempId`**: a CREATE can carry a temporary id referenced by dependent objects
  in the same request; the response returns a **`tempIdToRealId`** map (the only
  thing echoed back) so the caller can persist real ids.
- Values are written **separately** in `variableModeValues` (`{variableId,
  modeId, value}`), not nested in the variable. `value` is a literal (boolean /
  number / string / `RGB` or `RGBA` / null) or a `VariableAlias`.
- **Atomic**: any validation failure → 400, nothing persisted. Clean for an
  importer.

**The Plugin API write path (the any-plan alternative).**
`figma.variables.createVariableCollection()`, `createVariable(name, collection,
resolvedType)`, `collection.addMode()`, `variable.setValueForMode()`,
`createVariableAlias()`, `setBoundVariableForPaint/Effect()`. This works on **any
plan** — it runs in the editor under the file's permissions. Only **mode count**
(`addMode` throws `Limited to N modes only` past the plan cap) and **extended/
themed collections** (Enterprise) are tier-gated. The trade-off: the Plugin API is
**interactive** (a human or manually-triggered run inside the open file), not
headless; REST is **headless/CI-friendly** but Enterprise-only. (VERIFIED.)

**Styles can only be created via the Plugin API.** REST exposes styles **read-
only** (`GET .../styles`, `GET /styles/:key` — no POST/PUT/DELETE). Plugin API has
`figma.createTextStyle()`, `createEffectStyle()`, `createPaintStyle()`,
`createGridStyle()` (Figma Design only). (VERIFIED — `component-endpoints`,
`figma` create functions.) **Therefore any code→Figma pipeline that needs
typography or shadow styles requires a plugin, regardless of plan** — REST cannot
do it even on Enterprise.

---

## 5. Idempotent re-import: update-in-place vs build-from-scratch

Variables are referenced by stable `VariableID:*` ids; component bindings, style
bindings, and alias chains all point at those ids. **Delete-and-recreate mints new
ids and breaks every binding and alias. Update-in-place preserves ids, so bindings
survive.** This is the difference between an importer safe to run weekly and one
that detonates the file.

- **REST supports true update-in-place:** `UPDATE`/`DELETE` operate on existing
  ids you supply; `CREATE` mints new (optionally via `tempId`). But Figma does
  **not** match by name — there is **no upsert-by-name primitive**. The caller
  must know each existing id. (VERIFIED.)
- **Recommended strategy — persisted id map:** store the `VariableID` /
  `VariableCollectionId` / `modeId` next to each logical token. Each run: known id
  → `UPDATE`; unknown → `CREATE` + capture from `tempIdToRealId`; present in Figma
  but absent from tokens → optional `DELETE`. (This is exactly what a
  `$extensions.figma.variableId` linkage on each token enables — a token engine
  that already keeps that linkage is most of the way to idempotent re-import.)
- **Fallback — name-match reconciliation:** `GET .../variables/local`, build a
  name→id index, diff. Works without stored state but is **rename-fragile** (a
  rename looks like delete+create → broken bindings). Use only to bootstrap or
  self-heal a missing map.

---

## 6. The export/import JSON shape and the ecosystem

**Official REST `variables/local` schema** (VERIFIED — OpenAPI `LocalVariable`,
`RGBA`, `VariableAlias`, `LocalVariableCollection`):

- `meta.variables` and `meta.variableCollections` are **objects keyed by id**, not
  arrays. A single GET returns *all* modes for *all* collections.
- Each variable's values live in **`valuesByMode`** (keyed by `modeId`); there is
  no per-variable `$mode`/`$collection`.
- **Colour value = RGBA floats 0–1** (`{r,g,b,a}`, each 0–1). 
- **Alias value = `{ "type": "VARIABLE_ALIAS", "id": "VariableID:…" }`** — only
  `type` and `id`. An alias `name` field is **not** an API field and will not
  round-trip.
- Collection holds mode identity as `{modeId, name, parentModeId?}` + `variableIds[]`.

**POST vs GET asymmetry:** read = id-keyed maps with embedded `valuesByMode`;
write = action-tagged **arrays** with `tempId` cross-refs and values split into a
separate `variableModeValues` array, returning only `tempIdToRealId`.

**Community/ecosystem formats and the interop traps** (sources dated today):

- **Figma's official sample plugin** (`plugin-samples/variables-import-export`)
  uses **W3C DTCG** (`$value`/`$type`, brace aliases `{group.token}`), explicitly
  **no modes** ("no concept of modes in the W3C spec at this time") and only
  color/number/alias. Half the problem — variables, no styles.
- **variables2json** (community) uses a nested `collections → modes → variables[]`
  shape, slash-delimited names (`Colors/panelBg`), and **RGBA channels in 0–255**,
  *not* 0–1. **The biggest interop trap: the RGBA object is universal but the
  channel range is not standardized** (REST = 0–1; several plugins = 0–255). Check
  before ingesting any plugin's JSON. This plugin also exports text/effect/grid
  styles alongside variables (beyond the API's variables-only export).
- **Tokens Studio** is the de-facto two-way bridge (runs as a plugin, so it can do
  what REST can't — create/bind Text & Effect Styles). Mapping: collection = token-
  set folder, mode = token set, slash→dot on names. DTCG-aligned.
- **Style Dictionary** is a one-way *build* tool (tokens → CSS/iOS/Android/DTCG);
  it never writes to Figma — the Figma leg is a third-party plugin or the REST API.
- **Supernova** is Figma→Supernova→code; weak/absent on writing back into Figma.

**Where a custom engine's `variables[]` shape sits:** closest to the **Plugin API
objects** (keeps `resolvedType`, `scopes`, `codeSyntax`, alias `{type,id}`
verbatim), flattened — one file per `$mode`, a flat array instead of an id-keyed
map, plus a convenience `alias.name`. It is *not* the DTCG export shape (that's a
layer up, `$value`/`$type`/brace aliases). De-facto standards worth conforming to:
slash-delimited names, `VariableID:n:m` ids, RGBA objects, mode-keyed values.

---

## 7. What a code → Figma writer must therefore produce

A variables array alone is insufficient. To recreate the full token layer in
Figma a writer must emit three things, and assume the write step is a **plugin**
(because styles can't be created over REST, and REST variable writes are
Enterprise-gated):

1. **Atomic variables** for every composite leaf — typography: STRING
   (`fontFamily`, `fontStyle`) + FLOAT (`fontSize`, `fontWeight`, `lineHeight`,
   `letterSpacing`, …); shadow: COLOR (shadow colour) + FLOAT (`radius`, `spread`,
   `offsetX`, `offsetY`) — each with its collection/mode placement and correct
   scope so it lands in the right picker.
2. **Style definitions** — one Text Style per type role, one Effect Style per
   shadow token (multi-layer = ordered `Effect[]`), with literal fallback values.
3. **A binding map** — which variable binds which style field
   (`setBoundVariable("fontWeight", …)`; `setBoundVariableForEffect(effect,
   "radius", …)`). This is the part a plain variables/DTCG export has nowhere to
   put — the "style manifest."

**Disposition taxonomy — each category → its Figma home:**

| token category | Figma disposition |
|---|---|
| colour | `variable` (COLOR), 1:1 |
| dimension / radius / spacing / size / border-width / opacity | `variable` (FLOAT), 1:1 |
| typography | `style-part`: atomic STRING/FLOAT vars + a **Text Style** binding them |
| shadow | `style-part`: atomic COLOR/FLOAT vars + an **Effect Style** binding them |
| motion (duration/easing/spring/transition) | **experimental** — timing/easing variables exist (Config 2026); composite round-trip not yet stable → treat as `code-only` until proven |
| strokeStyle (solid/dashed) | no variable/style home → `code-only` |
| gradient | no single-variable home (paint-level) → Style/`code-only` |

**Plan-shaped decision framework:** Enterprise + CI → REST POST for variables
(atomic, idempotent by stored id) **plus** a plugin for styles. Non-Enterprise →
a single plugin that replays the generated JSON (variables + style manifest)
through the Plugin API, accepting an interactive run. Either way: persist the
token→id map so re-import is update-in-place, not destructive.

---

## Confidence ledger

**VERIFIED (primary-source, quoted):** four `resolvedType`s (Plugin + REST); the
scope enum and per-type validity (22 on the Plugin page; +`FONT_VARIATIONS` = 23
in OpenAPI); scopes are UI-filter-only; `codeSyntax` WEB/ANDROID/iOS; 40-mode /
5000-variable / 4 MB caps; four style types and their separate REST resource;
bindable text fields and bindable **effect numerics** (radius/spread/offset/
colour); styles REST is read-only, create is Plugin-only; Variables REST read+write
**Enterprise-only**; POST action/tempId/atomic model; GET id-keyed-map +
`valuesByMode`; RGBA 0–1; alias `{type,id}` only; official sample uses DTCG;
variables2json uses 0–255.

**PARTIALLY VERIFIED / inferred:** one-mode-dimension-per-collection (true in the
model, no verbatim sentence); `fontSize` text-style binding (scope exists; prose
bullet omits it); ecosystem tool specifics (Tokens Studio / SD / Supernova
behaviour inferred from architecture, not all quoted from a Figma primary doc).

**RECENT / IN FLUX — re-verify before relying:** **Figma Motion** timing/easing
variables and the beta Plugin Motion API (GA/beta ≈23–24 Jun 2026, days old; no
proven composite-motion round-trip); **per-plan mode caps** (10/20/unlimited —
Figma revises these); the **Enterprise write gate** (Figma has loosened API gating
before); `FONT_VARIATIONS` scope (in OpenAPI, absent from the rendered Plugin
page); exact `iOS` key casing.

## Primary sources
- Plugin API: [VariableResolvedDataType](https://developers.figma.com/docs/plugins/api/VariableResolvedDataType/) · [VariableScope](https://developers.figma.com/docs/plugins/api/VariableScope/) · [Variable](https://developers.figma.com/docs/plugins/api/Variable/) · [TextStyle](https://developers.figma.com/docs/plugins/api/TextStyle/) · [EffectStyle](https://developers.figma.com/docs/plugins/api/EffectStyle/) · [VariableBindableEffectField](https://developers.figma.com/docs/plugins/api/VariableBindableEffectField/) · [BaseStyle](https://developers.figma.com/docs/plugins/api/BaseStyle/) · [figma.variables](https://developers.figma.com/docs/plugins/api/figma-variables/) · [figma create* functions](https://developers.figma.com/docs/plugins/api/figma/) · [Working with Variables](https://developers.figma.com/docs/plugins/working-with-variables/) · [Motion](https://developers.figma.com/docs/plugins/api/Motion/) · [figma.motion](https://developers.figma.com/docs/plugins/api/figma-motion/)
- REST API: [Variables overview](https://developers.figma.com/docs/rest-api/variables/) · [Variables endpoints](https://developers.figma.com/docs/rest-api/variables-endpoints/) · [Component types](https://developers.figma.com/docs/rest-api/component-types/) · [Component endpoints](https://developers.figma.com/docs/rest-api/component-endpoints/) · [Changelog](https://developers.figma.com/docs/rest-api/changelog/) · [OpenAPI spec](https://raw.githubusercontent.com/figma/rest-api-spec/main/openapi/openapi.yaml)
- Help / releases: [Config 2026 — What's new](https://help.figma.com/hc/en-us/articles/39582753756695-What-s-new-from-Config-2026) · [Explore Figma Motion](https://help.figma.com/hc/en-us/articles/41274629073303-Explore-Figma-Motion) · [Modes for variables](https://help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables) · [Plans and features](https://help.figma.com/hc/en-us/articles/360040328273)
- Ecosystem: [Figma sample: variables-import-export](https://github.com/figma/plugin-samples/tree/main/variables-import-export) · [Tokens Studio — import variables](https://docs.tokens.studio/figma/import/variables/) · [DTCG 2025.10](https://www.designtokens.org/tr/2025.10/format/)
