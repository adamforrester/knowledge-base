# File Upload — field-truth study (Claude pass)

## 1. Framing
A File Upload lets a user **select files from their device and send them to a server** — and the component is the orchestration of a notoriously-unstylable native control, an optional pointer-only drop zone, and an asynchronous network lifecycle with per-file progress, cancel, retry, and error. It is a **Form composite** (the second of the Form-composite arc, after Date Picker — see date-picker) standing on **Text Field** (the uploader is a form field: label/helper/error/`aria-describedby` + the validation model — see text-field), with the *real* control always a native **`<input type=file>`**. It is the catalogue's component most entangled with a **network lifecycle**: unlike every prior control, "the value" isn't set synchronously — it's uploaded over time, can fail, and can be canceled.

Three decisions define it:
- **The native `<input type=file>` + the style-the-unstylable pattern (the foundation).** The real control is a native file input, which can't be meaningfully styled. The *only* accessible pattern is the **visually-hidden native `<input type=file>` paired with a `<label>`** (or a Button that proxies a `.click()` to the input via ref) — never an `opacity:0` overlay hack or a `role=button` div that isn't a real input (§11).
- **The drag-and-drop-is-an-enhancement-not-the-mechanism a11y crux (the headline).** A drop zone is pointer-only — keyboard and screen-reader users *cannot drag* — so the **browse Button is the always-present baseline** (WCAG 2.1.1) and drag-and-drop is layered on top. React Aria's **DropZone + FileTrigger** split is the reference encoding: the FileTrigger is the keyboard/SR path, the DropZone the pointer enhancement (§6).
- **The upload lifecycle state machine (the async crux).** A per-file state machine (queued → validating → uploading [progress] → success | error → retry/cancel), built on XHR `upload.onprogress` / fetch + the **AbortController** cancel (the Combobox async-race lineage — see combobox) and the **live-region** progress/complete/error announcements (the Toast/Progress lineage — see toast, progress) (§11).

What it *isn't*: a plain **Text Field** (it's a file control, not text — see text-field), a generic **Dropzone** with no upload (the drop zone is one affordance, not the component), or an **image editor / media library / asset manager** (the uploader hands off to those — §5). Why systems disagree: the drop-zone-vs-button baseline, immediate-vs-on-submit upload, the controlled-fileList model, and the resumable/direct-to-cloud scale boundary.

## 2. Anatomy and parts
- **the (visually hidden) native `<input type=file>`** — the real control: `accept`, `multiple`, `capture` (mobile camera), `webkitdirectory` (folder upload); visually hidden but in the DOM and labelled (§11).
- **the browse Button trigger** — a **Button** (see button) that opens the OS file picker (via the `<label htmlFor>` or a `.click()` ref proxy); the **always-present baseline** (§6).
- **the drop zone** — the pointer enhancement: a dashed-border target with **instructional copy** ("Drag files here, or browse"), an upload **Icon** (see icon), and an **empty-state** treatment (see empty-state); the drag-over / drag-reject highlight (§4).
- **the file list** — a **List** of upload items (see list); each item:
  - **the thumbnail / type Icon** — an image preview (via `createObjectURL` — §11) or a file-type Icon (see icon).
  - **the filename + size** — the name (truncated) + the locale-formatted size (§9).
  - **the Progress** — a per-file **Progress** bar (determinate while uploading, the no-fake-determinate rule — see progress).
  - **the status** — uploading / success / error (a Badge/Tag or an Icon — see badge, tag).
  - **the action Button** — remove (queued/done) / cancel (uploading) / retry (error) — a per-file Button (see button).
- **the image preview / picture-card** — the thumbnail grid variant (avatar/gallery).
- **the layouts** — single-file/replace (avatar) vs multi-file (the list) vs picture-card grid (§4).
- **the aggregate region** — an overall progress + a summary ("3 of 5 uploaded") + the live region (§6).

## 3. Properties / API
- **`accept`** — the file-type hint (`image/*`, `.pdf`) — a *hint*, not enforcement (the security boundary — §11); **`multiple`** — single vs multi; **`capture`** / **`directory`** (`webkitdirectory`).
- **`maxSize` / `maxFiles` / `minSize`** — the client-side validation limits (UX, not security — §11).
- **`onSelect` / `onChange`** — the selected `File[]`; **`onUpload`** / the **upload handler** (the endpoint or an async `(file, onProgress, signal) => Promise<result>`); **`onError`** / **`onRemove`** / **`onRetry`**.
- **`uploadMode`** — **immediate** (upload on select) vs **on-submit** (defer to the Form submit); how the uploaded *value* (a file ID/URL) feeds the surrounding Form (§5).
- **the controlled `fileList`** vs uncontrolled — the per-file state (Ant's controlled `fileList` is the reference; React Aria leans uncontrolled-with-callbacks).
- **`validator`** — a custom per-file predicate (type/size/dimensions/count → an error).
- **`disabled` / `readOnly`** — inherits the Text Field states (see text-field).
- **the per-file shape** — `{ id, file, name, size, status, progress, error, url }` (the state machine — §4/§11).
- **what it withholds** — File Upload doesn't reinvent the form-field chrome (Text Field), the list rendering (List), the progress bar (Progress), or the button (Button); it adds the file-selection affordances + the upload lifecycle.

## 4. States and variants
- **The drop-zone states:** **idle** / **drag-over** (a file is being dragged over — the accept highlight) / **drag-reject** (a wrong-type file dragged over — the reject highlight, where detectable) / **disabled**.
- **The per-file state machine:** **queued** (selected, not yet uploading) → **validating** → **uploading** (the Progress) → **success** | **error** (with a message) | **canceled**; **error** offers **retry**.
- **Variants:**
  - **selection:** single-file / multi-file.
  - **layout:** the drop zone + list / the **picture-card grid** (thumbnails) / the **avatar/replace** (a single circular image upload — the Avatar sibling, see avatar) / the inline button-only (no drop zone).
  - **with-preview** (image thumbnails) vs filename-only.
  - **the whole-window drop zone** (drag anywhere on the page — §11).
  - **upload mode:** immediate / on-submit.

## 5. Usage guidance
- **Use a File Upload for:** letting a user attach/send files — documents, images, media, data. The drop zone + browse button is the default for multi-file/desktop; a plain button suffices for a single low-stakes file.
- **The drag-and-drop worth-it call:** drag-and-drop is a genuine efficiency win for **multi-file** and **desktop** (drag a batch from the file explorer) — but it is **always an enhancement**, never the only path (the browse Button is the baseline — §6). For a single mobile upload, the button alone is often better (the drop zone is dead weight on touch).
- **Single vs multi:** single-file/replace (an avatar, a profile doc) → the avatar/replace control or a button; multi-file (attachments, a gallery) → the drop zone + the file list.
- **Immediate-upload vs on-submit:** **immediate** (upload on select, show progress, store the returned ID/URL) is the default for most flows — it parallelizes the wait with the rest of the form and surfaces errors early; **on-submit** (hold the files, upload with the form) suits small files or when the upload must be transactional with the form. The uploaded *value* the Form submits is the returned **file ID/URL**, not the raw file.
- **File Upload vs the alternatives:**
  - **vs a plain `<input type=file>`** — for a bare, unstyled, no-progress single file, the native input *is* the answer; the composite earns its weight with drag-and-drop, multi-file, progress, and previews.
  - **vs an avatar/image-replace control** — a single circular image upload with crop is the Avatar sibling (see avatar), not the multi-file list.
  - **vs a full media library / asset manager** — browsing/reusing previously-uploaded assets is a different component; the uploader *feeds* it.
- **The large-file / resumable boundary:** for large files (video, datasets) or flaky networks, the simple XHR-to-endpoint upload isn't enough — reach for **resumable/chunked** (tus) and **direct-to-cloud presigned** (S3 multipart), typically via a headless engine (Uppy) (§11). A forward boundary, not the default.

## 6. Accessibility
File Upload's a11y headline is the **drag-and-drop crux**, and it has a network lifecycle to announce.
- **Drag-and-drop is an enhancement, not the mechanism (the crux).** Keyboard and screen-reader users cannot perform a drag-and-drop; a drop zone alone is a **WCAG 2.1.1 (keyboard) failure**. The **browse Button must always be present** as the baseline path, and drag-and-drop is layered on for pointer users. **React Aria's split encodes this exactly**: `FileTrigger` (a Button wrapping the hidden input — the keyboard/SR path) and `DropZone` (the pointer enhancement). Build the FileTrigger first; add the DropZone as progressive enhancement.
- **The native-input label contract.** The real `<input type=file>` is **visually hidden but present and labelled** (a `<label>` associated by `htmlFor`/wrapping, or `aria-label`); the visible Button either *is* the label or proxies a `.click()` to the input. Never replace the input with a non-input `role=button` div (it loses the OS file-picker semantics and the SR "file upload" announcement).
- **The upload lifecycle announcements (the Toast/Progress lineage).** Upload **progress**, **complete**, and **error** are announced via a **live region** (`role=status`/polite for progress+complete; `role=alert`/assertive for errors — see toast, progress); throttle progress to milestones (not per-percent), and announce per-file completion ("document.pdf uploaded") + the aggregate ("3 of 5 uploaded").
- **The file-list item semantics.** Each item's **remove/cancel/retry** Button has a per-file accessible name ("Remove document.pdf", not a bare "Remove" × N — the icon-only-button trap from Icon/Button); the per-file Progress is labelled with the filename.
- **The error association.** Validation errors (too big / wrong type / failed) associate via the Text Field `aria-describedby`/`aria-invalid` chain (see text-field), and the drag-reject is announced (not color-only).
- **WCAG SCs:** **2.1.1** (keyboard — the drop zone needs the button baseline; the headline), **4.1.3** (status messages — the progress/complete/error live region), **1.4.13** (any hover/focus affordance — see tooltip/popover), **3.3.1** (error identification — the validation copy), **1.3.1** (info & relationships — the list + label structure), **4.1.2** (name/role/value — the input, the per-file buttons).

## 7. Content guidelines
- **The drop-zone copy** — "**Drag files here, or browse**" (the browse word is the button affordance); keep it instructional, and state the constraints nearby.
- **The constraints hint** — show **accepted types + max size + max count** up front ("PNG or JPG, up to 10 MB, max 5 files") — not only in an error after the fact.
- **The per-file error copy** — specific to the violation: "File is too large (max 10 MB)" / "Only PNG or JPG allowed" / "Upload failed — retry", *not* a generic "Invalid file".
- **The progress/status labels** — "Uploading… 60%" / "Uploaded" / "Failed"; the aggregate "3 of 5 uploaded".
- **The success confirmation** — confirm completion (a status, not necessarily a Toast); for an avatar, show the new image.

## 8. Motion and transition
- **The drag-over highlight** — a quick border/background transition on dragenter (and revert on dragleave/drop); keep it fast and unmistakable.
- **The list insert/remove** — animate a file item in on add and out on remove (height/opacity); the same restraint as the List/Tree reveal (see list).
- **The progress fill** — the Progress bar's determinate fill (see progress); don't fake it (the no-fake-determinate rule).
- **The success/error transition** — a state change on the item (the Progress → a check/error Icon).
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops the highlight transition and the list-insert animation to instant; the upload state is the information, not the motion.

## 9. Internationalization
- **The copy** — the instructional + status + error copy translates (the drop-zone, the buttons, the per-file status).
- **The file-size formatting** — the size number is **locale-formatted** (`Intl.NumberFormat`) and the unit (KB/MB/GB) localized; don't hardcode "1.5 MB" string-building.
- **RTL** — the drop zone, the file list, the thumbnail-then-text item layout, and the **remove-button placement** mirror to the inline-start/end via logical properties (see box); the upload Icon is direction-agnostic.
- **The upload timestamp** — if shown, locale-format it (the Date Picker `Intl` lineage — see date-picker).

## 10. Naming
- **The field set:** **`FileUpload`** / **`FileUploader`** (Carbon — `FileUploader` + `FileUploaderDropContainer` + `FileUploaderItem`); **`Upload`** (Ant — `Upload` + `Upload.Dragger`, the controlled `fileList`); **`DropZone`** (Polaris, React Aria — the pointer target) + **`FileTrigger`** (React Aria — the keyboard/SR button); **`FileInput`** (the bare control).
- **The practice's default — `FileUpload`** for the composite, built from a **`FileTrigger`** (the Button + hidden input — the a11y baseline) + an optional **`DropZone`** (the pointer enhancement) + a **`FileList`** (the upload-items List) + per-item **Progress**. Expose the **avatar/image-replace** as a variant (or the Avatar's upload affordance — see avatar), and the **picture-card** grid as a layout. The drop zone is never the sole mechanism (the name shouldn't be `DropZone` for the composite — that hides the button baseline).
- **Aliases to map:** FileUpload, FileUploader, Upload, Dragger, DropZone, FileTrigger, FileInput, Uploader.

## 11. Implementation notes
- **The visually-hidden-input + label/button-proxy pattern** — render a real `<input type=file>` visually hidden (the clip/sr-only pattern, *not* `display:none` which can break some AT/submit behavior), and either wrap it in / associate it with a `<label>` styled as a Button, or render a Button whose `onClick` calls `inputRef.current.click()`. This is the only pattern that keeps the OS file-picker + the SR "file upload, button" semantics. Reset `input.value = ''` after handling so selecting the same file again re-fires `change`.
- **The DnD event model** — handle `dragenter`/`dragover`/`dragleave`/`drop`; **`preventDefault()` on `dragover` is mandatory** (the browser's default is to navigate to the file — drop never fires without it). **The dragleave flicker:** `dragleave` fires when crossing onto child elements, flickering the highlight — fix with an **enter/leave counter** (increment on enter, decrement on leave, highlight while > 0) or `pointer-events: none` on the zone's children. Read `DataTransfer.files` / `.items` on drop; support **paste-to-upload** (the `paste` event's `clipboardData.files`) and optionally a **whole-window drop zone** (listen on `document`, show a full-screen overlay on dragenter).
- **The per-file upload state machine** — model each file as `{ id, file, status, progress, error, url, abort }`; on upload, create an **`AbortController`** (the Combobox cancel/race lineage — see combobox), report progress via **XHR `upload.onprogress`** (fetch's request-upload progress is still not universally available — XHR remains the pragmatic choice for upload progress; verify the current `fetch`/streams state) or a fetch + `ReadableStream`, resolve to success (store the returned ID/URL) or error (offer **retry** — a new attempt reusing the `File`). Cancel calls `abort()`.
- **Client validation is UX, not security** — validate type/size/count **client-side for fast feedback only**; the `accept` attribute and the extension/MIME are **trivially spoofed**, so the **server MUST re-validate** (magic-byte content sniffing, a malware scan, a hard size cap, auth). State this boundary explicitly — a brief that implies client validation is a security control is dangerous.
- **The image preview + the leak** — generate a thumbnail with **`URL.createObjectURL(file)`**, and **`URL.revokeObjectURL()` when the item unmounts/removes** — the classic memory leak is forgetting to revoke (object URLs live until the document unloads otherwise).
- **Resumable / chunked / direct-to-cloud (the scale boundary)** — for large files / flaky networks: chunked + **resumable** uploads (the **tus** protocol), **direct-to-cloud** via **presigned URLs** / **S3 multipart** (the browser uploads straight to storage, bypassing the app server's bandwidth/timeout). The headless engine (**Uppy**) owns the dashboard + tus + S3-multipart + retry/resume. Default to the simple XHR-to-endpoint; reach for this when file size / reliability demands it.
- **Controlled vs uncontrolled** — Ant's controlled `fileList` (you own the array + the per-file status) vs React Aria's uncontrolled-with-callbacks. The controlled model is clearer for custom upload pipelines.
- **Headless vs opinionated** — react-dropzone (the DnD primitive), Uppy (the full pipeline), React Aria (the a11y split) own the hard parts; the styling is theme. **Build the FileTrigger + the state machine on a headless base**; don't hand-roll the DnD flicker fix and the abort/retry from scratch.

## 12. Related and alternative components
- **Stands on:** **Text Field** (the uploader is a form field — label/helper/error/`aria-describedby` + validation — see text-field); the real control is a native `<input type=file>`.
- **Composes:** **Button** (the browse trigger + the per-file cancel/retry/remove — see button), **Icon** (the upload glyph + file-type icons + the remove × — see icon), **List** (the file list is a List of upload items — see list), **Progress** (per-file + aggregate progress — see progress).
- **Borders:** **Empty State** (the empty drop zone — see empty-state), **Tag** / **Badge** (file chips / status — see tag, badge).
- **Reuses:** the **AbortController** cancel/race model (the Combobox async lineage — see combobox), the **optimistic/pending lock** (see switch), and the **live-region** announcement pattern (see toast, progress).
- **The Avatar sibling:** the single-image-replace/upload affordance (an avatar upload is a single-file image upload with crop — see avatar).
- **Alternative to:** a plain **`<input type=file>`** (bare/unstyled/no-progress), a full **media library / asset manager** (browsing reused assets — the uploader feeds it).

(A Form composite — the file-selection + upload control, the catalogue's most network-lifecycle-entangled component, and the second of the Form-composite arc after Date Picker. It stands on Text Field (the form field), composes Button/Icon/List/Progress, borders Empty State + Tag/Badge, and reuses Combobox's AbortController + Toast/Progress's live region. See text-field for the field substrate, list for the file-list, progress for the per-file progress, combobox for the async-abort model, avatar for the image-upload sibling, date-picker for the Form-composite arc it continues. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The bare `<input type=file>` → the styled hidden-input + label.** The unstylable native input gave way to the visually-hidden-input + a styled `<label>`/Button — the only accessible way to brand the control.
2. **The drag-and-drop drop zone → the button baseline reasserted.** Drop zones spread (Dropzone.js, react-dropzone), and the field then re-learned that **drag-and-drop is an enhancement** — the keyboard/SR button must always be present (WCAG 2.1.1); React Aria's **FileTrigger/DropZone split** codified the model.
3. **The async progress/abort/retry lifecycle.** Uploaders matured from fire-and-forget to a per-file state machine with progress (XHR `upload.onprogress`), **AbortController** cancel, and retry — and the live-region announcements (the Toast/Progress lineage).
4. **The resumable/chunked/direct-to-cloud era.** Large files + flaky networks drove **resumable** uploads (**tus**), **direct-to-cloud** presigned/S3-multipart, and the headless **Uppy** engine — moving the upload off the app server.

## 14. Sources cited
*(External-pass version dates to be reconciled; flag any unverified under notes.unverified.)*
- Adobe Spectrum / React Aria — **`DropZone` + `FileTrigger`** (the gold-standard a11y split: the keyboard/SR trigger vs the pointer drop zone).
- Ant Design — **`Upload`** / `Upload.Dragger` (the most feature-complete: the upload list, drag, picture-card, avatar, the controlled `fileList`).
- IBM Carbon — **`FileUploader`** + `FileUploaderDropContainer` + `FileUploaderItem`.
- Shopify Polaris — **`DropZone`**.
- Microsoft Fluent / Atlassian (the media picker).
- **react-dropzone** (the DnD primitive), **Uppy / Transloadit** (the resumable + S3-multipart + dashboard engine), **FilePond**, **Dropzone.js**, **Uploadcare / Filestack** (SaaS widgets).
- The platform — native **`<input type=file>`**, the **File API**, **DataTransfer** + the **HTML Drag and Drop API**, the **tus** resumable-upload protocol, **S3 multipart / presigned URLs**.
- WAI-ARIA APG — no dedicated upload pattern (a labelled file input + a button + a status live region); the relevant building blocks.
- WCAG 2.2 — 2.1.1, 4.1.3, 1.4.13, 3.3.1, 1.3.1, 4.1.2.

## 15. Agent-consumable schema
```yaml
identity:
  id: file-upload
  name: File Upload
  aliases: [FileUpload, FileUploader, Upload, Dragger, DropZone, FileTrigger, FileInput, Uploader]
  category: form
  status: stable
description: >
  A Form composite for selecting files from the device and uploading them to a server —
  the catalogue's component most entangled with an asynchronous network lifecycle (the value
  is uploaded over time, can fail, can be canceled). Stands on Text Field (the uploader is a
  form field); the REAL control is always a native <input type=file>. NOT a plain Text Field,
  NOT a generic Dropzone with no upload, NOT an image editor / media library (it feeds those).
  Three decisions: the native <input type=file> + the style-the-unstylable pattern (the
  visually-hidden input + a label/button-proxy — the only accessible one), the
  drag-and-drop-is-an-enhancement-not-the-mechanism a11y crux (the browse Button is the
  always-present WCAG 2.1.1 baseline; React Aria's FileTrigger/DropZone split encodes it),
  and the upload lifecycle state machine (queued->uploading[progress]->success|error->retry,
  on the AbortController cancel from Combobox + the Toast/Progress live region).
anatomy:
  parts:
    - "the (visually hidden) native <input type=file>: the REAL control — accept/multiple/capture/webkitdirectory; hidden but in the DOM and labelled"
    - "the browse Button trigger: a Button opening the OS file picker (via label htmlFor or a .click() ref proxy) — the ALWAYS-PRESENT baseline"
    - "the drop zone (the pointer enhancement): a dashed-border target + instructional copy ('Drag files here, or browse') + an upload Icon + an empty-state; the drag-over/drag-reject highlight"
    - "the file list: a List of upload items — each: a thumbnail/type-Icon + filename + size + a Progress bar + a status + a remove/cancel/retry Button"
    - "the image preview / picture-card: the thumbnail grid variant (createObjectURL)"
    - "the layouts: single-file/replace (avatar) vs multi-file (the list) vs picture-card grid"
    - "the aggregate region: overall progress + a summary ('3 of 5 uploaded') + the live region"
api:
  inherits:
    - text-field   # the uploader is a form field — label/helper/error/aria-describedby + validation
  composes: [button, icon, list, progress]
  props:
    - {name: accept, type: string, default: ~, required: false, description: "the file-type HINT (image/*, .pdf) — NOT enforcement (the security boundary)"}
    - {name: multiple, type: boolean, default: false, required: false, description: "single vs multi-file; + capture (mobile camera) / directory (webkitdirectory)"}
    - {name: "maxSize/maxFiles/minSize", type: "number", default: ~, required: false, description: "client-side validation limits — UX, NOT security"}
    - {name: "onSelect/onChange", type: "(files: File[]) => void", default: ~, required: false, description: "the selected files"}
    - {name: "upload handler", type: "(file, onProgress, signal) => Promise<result>", default: ~, required: false, description: "the endpoint / async uploader; + onError/onRemove/onRetry"}
    - {name: uploadMode, type: "'immediate'|'on-submit'", default: immediate, required: false, description: "upload on select vs defer to the Form submit; the uploaded VALUE the Form gets is the returned file ID/URL, not the raw file"}
    - {name: fileList, type: "UploadFile[]", default: ~, required: false, description: "controlled (Ant) vs uncontrolled-with-callbacks (React Aria)"}
    - {name: validator, type: "(file)=>error|null", default: ~, required: false, description: "a custom per-file predicate (type/size/dimensions/count)"}
    - {name: "disabled/readOnly", type: boolean, default: false, required: false, description: "inherits the Text Field states"}
  per-file-shape: "{ id, file, name, size, status, progress, error, url, abort } — the state machine"
  withholds: "doesn't reinvent the form-field chrome (Text Field), the list (List), the progress bar (Progress), or the button (Button); adds the file-selection affordances + the upload lifecycle"
states:
  drop-zone: [idle, drag-over, drag-reject, disabled]
  per-file: [queued, validating, uploading, success, error, canceled]   # error offers retry
variants:
  selection: [single, multi]
  layout: [dropzone-and-list, picture-card-grid, avatar-replace, button-only]
  preview: [with-preview, filename-only]
  drop-target: [zone, whole-window]
  upload-mode: [immediate, on-submit]
accessibility:
  wcag-criteria: ["2.1.1", "4.1.3", "1.4.13", "3.3.1", "1.3.1", "4.1.2"]
  inherits: [text-field (the validation/aria-describedby chain)]
  drag-is-an-enhancement: "THE crux — keyboard/SR users CANNOT drag, so a drop zone alone is a WCAG 2.1.1 failure. The browse Button MUST always be present as the baseline; drag-and-drop is layered on. React Aria's FileTrigger (the Button + hidden input — keyboard/SR path) + DropZone (the pointer enhancement) encodes it. Build the FileTrigger first"
  native-input-label: "the real <input type=file> is VISUALLY HIDDEN but present + labelled (a label htmlFor/wrapping, or aria-label); the visible Button is the label or proxies a .click(). NEVER a non-input role=button div (loses the OS picker + the SR 'file upload' announcement)"
  lifecycle-announcements: "upload progress/complete/error via a LIVE REGION (role=status/polite for progress+complete, role=alert/assertive for errors — the Toast/Progress lineage); throttle progress to milestones (not per-percent); announce per-file ('document.pdf uploaded') + aggregate ('3 of 5 uploaded')"
  file-list-items: "each item's remove/cancel/retry Button has a per-file accessible name ('Remove document.pdf', not a bare 'Remove' xN — the icon-only-button trap); the per-file Progress labelled with the filename"
  error-association: "validation errors (too big/wrong type/failed) via the Text Field aria-describedby/aria-invalid chain; the drag-reject announced, not color-only"
content:
  drop-zone-copy: "'Drag files here, or browse' (the browse word is the button affordance); instructional"
  constraints-hint: "show accepted types + max size + max count UP FRONT ('PNG or JPG, up to 10 MB, max 5 files'), not only in an after-the-fact error"
  error-copy: "specific to the violation ('File is too large (max 10 MB)' / 'Only PNG or JPG allowed' / 'Upload failed - retry'), not 'Invalid file'"
  status-labels: "'Uploading... 60%' / 'Uploaded' / 'Failed'; the aggregate '3 of 5 uploaded'"
  success: "confirm completion (a status, not necessarily a Toast); for an avatar, show the new image"
motion:
  drag-over-highlight: "a quick border/background transition on dragenter, revert on dragleave/drop; fast + unmistakable"
  list-insert-remove: "animate a file item in on add / out on remove (height/opacity); the List/Tree reveal restraint"
  progress-fill: "the Progress determinate fill (the no-fake-determinate rule)"
  state-transition: "the per-item Progress -> a check/error Icon"
  reduce-motion: "drop the highlight transition + the list-insert to instant; the upload state is the information, not the motion"
i18n:
  copy: "the instructional + status + error copy translates"
  file-size: "the size number is locale-formatted (Intl.NumberFormat) + the KB/MB/GB unit localized; don't hardcode '1.5 MB' string-building"
  rtl: "the drop zone + the file list + the thumbnail-then-text item + the remove-button placement mirror via logical properties; the upload Icon is direction-agnostic"
  timestamp: "if an upload time is shown, locale-format it (the Date Picker Intl lineage)"
implementation:
  - "the visually-hidden-input + label/button-proxy: render a REAL <input type=file> visually hidden (clip/sr-only, NOT display:none which can break some AT/submit), associate a <label>/Button or call inputRef.current.click(). The only pattern keeping the OS picker + the SR 'file upload, button' semantics. Reset input.value='' after handling so the same file re-fires change"
  - "the DnD event model: handle dragenter/over/leave/drop; preventDefault() on DRAGOVER is MANDATORY (default is navigate-to-file; drop never fires without it). The DRAGLEAVE FLICKER (fires crossing onto children) -> an enter/leave COUNTER (highlight while >0) or pointer-events:none on children. Read DataTransfer.files/.items; support paste-to-upload (clipboardData.files) + optionally a whole-window drop zone"
  - "the per-file upload state machine: { id, file, status, progress, error, url, abort }; per upload create an AbortController (the Combobox cancel/race lineage), report progress via XHR upload.onprogress (fetch request-upload progress still not universal — XHR is the pragmatic choice; VERIFY current fetch/streams state), resolve to success (store the returned ID/URL) or error (offer RETRY, reusing the File). Cancel calls abort()"
  - "CLIENT VALIDATION IS UX, NOT SECURITY: validate type/size/count client-side for fast feedback ONLY; accept + extension/MIME are trivially SPOOFED -> the SERVER MUST re-validate (magic-byte sniffing, malware scan, hard size cap, auth). State this boundary explicitly"
  - "the image preview + the LEAK: URL.createObjectURL(file) for the thumbnail, and URL.revokeObjectURL() on unmount/remove — forgetting to revoke is the classic memory leak (object URLs live until document unload)"
  - "resumable/chunked/direct-to-cloud (the scale boundary): large files / flaky networks -> chunked + RESUMABLE (tus), DIRECT-TO-CLOUD presigned / S3 multipart (browser uploads straight to storage, bypassing the app server). The headless Uppy engine owns the dashboard + tus + S3-multipart + resume. Default to the simple XHR-to-endpoint; reach for this when size/reliability demands it"
  - "controlled (Ant fileList — you own the array + per-file status) vs uncontrolled-with-callbacks (React Aria); controlled is clearer for custom pipelines"
  - "headless vs opinionated: react-dropzone (the DnD primitive) / Uppy (the full pipeline) / React Aria (the a11y split) own the hard parts; styling is theme. BUILD THE FILETRIGGER + the state machine on a headless base — don't hand-roll the DnD flicker fix + the abort/retry"
composition:
  inherits: [text-field]
  composes: [button, icon, list, progress]
  borders: [empty-state, tag, badge]   # the empty drop zone / file chips + status
  reuses: [combobox, toast, progress, switch]   # the AbortController async model / the live-region announcement / the optimistic-pending lock
  sibling: [avatar]   # the single-image-replace/upload affordance (avatar upload = single-file image + crop)
  alternative-to: ["plain <input type=file> (bare/unstyled/no-progress)", "a media library / asset manager (browsing reused assets — the uploader feeds it)"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "the drop zone as the sole mechanism (a11y FAILURE) vs the always-present browse Button baseline + DnD as enhancement (practice; React Aria FileTrigger/DropZone)"
    - "immediate-upload-on-select (practice default — parallelize the wait, surface errors early) vs on-submit (transactional with the form)"
    - "controlled fileList (Ant — you own the state) vs uncontrolled-with-callbacks (React Aria)"
    - "the simple XHR-to-endpoint upload vs resumable/chunked/direct-to-cloud (tus / S3 multipart / Uppy) — a scale boundary, not a default"
    - "naming the composite FileUpload (practice) vs DropZone (hides the button baseline) vs Upload (Ant)"
  trap:
    - "a drop zone with no keyboard/SR button (WCAG 2.1.1 failure) — the browse Button is the baseline"
    - "styling via an opacity:0 overlay hack or a role=button div instead of the visually-hidden real <input type=file> + label/button-proxy"
    - "forgetting preventDefault() on dragover (drop never fires); the dragleave flicker (needs an enter/leave counter or pointer-events:none on children)"
    - "treating client-side validation as a security control (accept/MIME/extension are spoofed — the server MUST re-validate)"
    - "the createObjectURL memory leak (forgetting revokeObjectURL on remove/unmount)"
    - "a bare 'Remove' xN on the file-list buttons (the icon-only-button trap — name them per-file); not resetting input.value so the same file won't re-select"
    - "spamming the live region per-percent (throttle progress to milestones)"
  inherited: "Text Field's form-field substrate (label/helper/error/validation); the List file-list rendering; the Progress per-file bar + no-fake-determinate; Button's loading/icon-only-name discipline; Combobox's AbortController async-race model; Toast/Progress's live-region pattern"
  role-in-family: "a Form composite — the file-selection + upload control, the most network-lifecycle-entangled component; the second of the Form-composite arc (after Date Picker); stands on Text Field, composes Button/Icon/List/Progress, borders Empty State + Tag/Badge; the Avatar image-upload sibling"
  evolution:
    - "the bare <input type=file> -> the styled visually-hidden-input + label"
    - "the drag-and-drop drop zone -> the button baseline reasserted for a11y (React Aria FileTrigger/DropZone split)"
    - "the async progress/abort/retry lifecycle (XHR upload.onprogress + AbortController + the live region)"
    - "the resumable/chunked/direct-to-cloud era (tus / S3 multipart / Uppy — off the app server)"
  unverified:
    - "external 2026 version numbers (React Aria DropZone/FileTrigger, Ant Upload, Carbon FileUploader, Polaris DropZone, Uppy)"
    - "the fetch request-upload-progress / ReadableStream upload state (whether XHR is still required for upload progress) — verify against current platform"
    - "the tus protocol version + S3-multipart presigned specifics — verify current"
```
