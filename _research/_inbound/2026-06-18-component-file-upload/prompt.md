You are researching the File Upload component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of how
the leading design systems handle this component — what they converge on,
where they diverge, and what the practice's opinionated default should be
when starting from scratch.

This is not an introductory guide. Assume the reader knows what a file
upload is, knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the choices field leaders disagree on,
the accessibility decisions still contested, the implementation traps that
recur across codebases.

File Upload is A FORM COMPOSITE — one of the components closing the Form
category (the second of the Form-composite arc, after Date Picker). It
STANDS ON a briefed substrate and is the catalogue's component most
entangled with an asynchronous network lifecycle. DON'T re-derive the
substrates; reference them and concentrate on the File-Upload-specific
substance:
- IT STANDS ON TEXT FIELD (components/text-field.md): the uploader is a form
  field — it inherits the label / helper / error / aria-describedby chain and
  the validation model (presentational-by-default, the error state). The
  REAL control is a native <input type=file>. Don't re-derive the form-field
  substrate.
- IT COMPOSES BUTTON (the browse/choose trigger — components/button.md), ICON
  (the upload glyph + per-file-type icons + the remove ×), LIST (the file
  list is a List of upload items — components/list.md), PROGRESS (per-file +
  aggregate upload progress, the determinate/indeterminate contract —
  components/progress.md), and borders EMPTY STATE (the empty drop zone) and
  TAG/BADGE (file chips / status).
- IT REUSES THE ASYNC PATTERNS the catalogue has already drawn: the
  AbortController cancel/race model (components/combobox.md — the debounced
  async fetch), the optimistic/pending lock (components/switch.md), and the
  live-region announcement pattern (components/toast.md, progress.md) for
  upload progress / complete / error.

THE DEFINING FILE-UPLOAD-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE NATIVE <input type=file> + THE STYLE-THE-UNSTYLABLE PATTERN (the
  foundation): the real control is a native file input, which is notoriously
  unstylable. Resolve the ONLY accessible styling pattern — the
  visually-hidden native <input type=file> paired with a <label> (or a Button
  that proxies a .click() to the input via ref) — vs the anti-patterns
  (opacity:0 input overlay positioning hacks, a div with role=button that
  isn't a real input). The accept attribute as a HINT not enforcement; the
  multiple attribute; capture (mobile camera); webkitdirectory (folder
  upload).
- THE DRAG-AND-DROP-IS-AN-ENHANCEMENT-NOT-THE-MECHANISM A11Y CRUX (the
  headline): a drop zone is a pointer-only affordance — keyboard and screen-
  reader users CANNOT drag — so the browse Button is the ALWAYS-PRESENT
  baseline (WCAG 2.1.1) and drag-and-drop is layered on top. Resolve the
  React Aria DropZone + FileTrigger split as the reference encoding of
  exactly this (the FileTrigger is the keyboard/SR path; the DropZone is the
  pointer enhancement). And the DnD implementation traps: the dragover
  preventDefault requirement (drop never fires without it), the dragleave
  flicker (fires on child elements — the enter/leave counter or
  pointer-events:none fix), the DataTransfer.items / .files model, paste-to-
  upload, and the whole-window drop-zone pattern.
- THE UPLOAD LIFECYCLE STATE MACHINE (the async crux): the per-file state
  machine (queued → validating → uploading [progress] → success | error →
  retry / cancel), the progress reporting (XHR upload.onprogress / fetch +
  the abort), the AbortController cancel (the Combobox race lineage), retry
  on failure, the aggregate vs per-file progress, and the
  immediate-upload-on-select vs upload-on-form-submit decision (and how the
  uploaded value — a file ID / URL — feeds the surrounding Form).
- CLIENT-VALIDATION-IS-UX-NOT-SECURITY + THE SECURITY MODEL: client-side
  type/size/count validation is for fast feedback ONLY — the server MUST
  re-validate (the accept attribute and the extension/MIME are trivially
  spoofed; magic-byte sniffing + malware scan + size caps live server-side).
  Resolve the validation UX (reject-before-upload, the error copy) and flag
  the security boundary clearly.
- THE FILE-LIST + PREVIEW ANATOMY: the uploaded-files list (each item: a
  type Icon / image thumbnail, the filename + size, a Progress bar, a
  status, a remove/cancel/retry Button — a List of upload items), the image
  preview via URL.createObjectURL (+ the revokeObjectURL memory-leak trap),
  the single-file/replace (avatar) vs multi-file (the list) vs picture-card-
  grid variants.
- RESUMABLE / CHUNKED / DIRECT-TO-CLOUD (the scale boundary): large-file
  uploads need chunking + resumability (the tus protocol, S3 multipart) and
  direct-to-cloud presigned URLs (bypassing the app server); the headless
  upload engines (Uppy) own this. Resolve as a framework — the simple
  XHR-to-endpoint default vs when the resumable/direct-to-cloud pipeline is
  warranted — and keep it a forward boundary, not the core.

Field-leader systems to survey (web): Adobe Spectrum / React Aria (DropZone +
FileTrigger — the gold-standard a11y split: the keyboard/SR file trigger vs
the pointer drop zone), Ant Design (Upload — the most feature-complete: the
upload list, drag Dragger, picture-card, avatar, the controlled fileList),
IBM Carbon (FileUploader + FileUploaderDropContainer + FileUploaderItem),
Shopify Polaris (DropZone), Microsoft Fluent, Atlassian (the media picker),
the headless/standalone libraries — react-dropzone (the DnD primitive),
Uppy / Transloadit (the resumable + S3-multipart + dashboard engine),
FilePond, Dropzone.js, Uploadcare / Filestack (SaaS widgets). The platform:
the native <input type=file>, the File API, DataTransfer + the HTML Drag and
Drop API, the tus resumable-upload protocol, S3 multipart / presigned URLs.
WAI-ARIA APG (no dedicated upload pattern — it is a labelled file input +
a button + a status live region; cite the relevant building blocks). Cite
each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits for the Text Field form-field substrate;
composes Button/Icon/List/Progress; borders Empty State/Tag/Badge; reuse the
AbortController async model from Combobox + the live-region pattern from
Toast/Progress; flag unverified/volatile platform claims under
notes.unverified).

1. Framing — what it is (the form control for selecting + uploading files;
   the native <input type=file> + the drop-zone enhancement + the upload
   lifecycle) and what it isn't (a plain Text Field; a generic Dropzone with
   no upload; an image editor / media library); the native-input foundation +
   the drag-is-an-enhancement crux + the async-lifecycle reality up front;
   why systems disagree.
2. Anatomy and parts — the (visually hidden) native <input type=file>, the
   browse Button trigger, the drop zone (the dashed-border target + the
   instructional copy + the icon + the empty state), the file list (per-item:
   thumbnail/type-icon + name + size + Progress + status + remove/cancel/retry
   Button), the image preview, the single-file vs picture-card vs list layouts.
3. Properties / API — accept, multiple, maxSize / maxFiles, the validation
   hooks, the upload handler / endpoint, controlled fileList vs uncontrolled,
   immediate-upload vs on-submit, the per-file state, capture/webkitdirectory,
   the disabled/read-only, the onChange/onUpload/onError/onRemove callbacks.
4. States and variants — the drop zone (idle / drag-over / drag-reject /
   disabled); the per-file state machine (queued / validating / uploading /
   success / error / canceled); single-file vs multi-file vs picture-card vs
   avatar; with-preview; the whole-window drop zone.
5. Usage guidance — File Upload (drop zone + browse) vs a plain file input vs
   an avatar/image replace control vs a full media library/asset manager;
   when drag-and-drop is worth it (and when the button alone suffices); single
   vs multi; immediate-upload vs on-submit; the large-file / resumable
   boundary.
6. Accessibility — the drag-is-an-enhancement-not-the-mechanism rule (the
   ALWAYS-present browse Button as the WCAG 2.1.1 baseline; React Aria's
   FileTrigger vs DropZone); the native-input label contract (the hidden
   input + label/button); the upload progress / complete / error live-region
   announcements (the Toast/Progress lineage); the file-list item semantics
   (the remove/retry buttons named per-file); the error association (the Text
   Field aria-describedby chain); WCAG SCs (2.1.1, 4.1.3, 1.4.13, 3.3.1,
   1.3.1, 4.1.2).
7. Content guidelines — the drop-zone instructional copy ("Drag files here or
   browse"), the accepted-types + max-size + max-count hint, the per-file
   error copy (too big / wrong type / upload failed — specific, not generic),
   the progress/status labels, the success confirmation.
8. Motion and transition — the drag-over highlight transition, the file-added
   list-insert / file-removed animation, the progress-bar fill, the
   success/error state transition, reduce-motion.
9. Internationalization — the instructional + status copy translation, the
   file-size formatting (locale number + the KB/MB units), RTL (the drop zone
   + the list + the remove-button placement mirror), the date/time of upload.
10. Naming — FileUpload / FileUploader / Upload / DropZone / FileTrigger /
    Dragger / FileInput; the trigger-vs-dropzone-vs-composite naming; the
    practice's default; aliases.
11. Implementation notes — the visually-hidden-input + label/button-proxy
    pattern (the .click() ref proxy); the DnD event model (dragenter/over/
    leave/drop + the preventDefault-on-dragover requirement + the dragleave-
    flicker counter fix + DataTransfer.files); the per-file upload state
    machine + XHR upload.onprogress / fetch + the AbortController cancel (the
    Combobox lineage) + retry; client validation (type/size/count) as UX with
    the server-revalidation security boundary; the image preview via
    URL.createObjectURL + the revokeObjectURL leak; the resumable/chunked
    (tus) + direct-to-cloud presigned (S3 multipart) boundary + the headless
    engines (Uppy); controlled-fileList vs uncontrolled.
12. Related and alternative components — typed relationships (STANDS ON Text
    Field [the form field]; COMPOSES Button/Icon/List/Progress; BORDERS Empty
    State [the empty drop zone] + Tag/Badge [file chips/status]; reuses the
    Combobox AbortController async model + the Toast/Progress live region; the
    Avatar image-upload sibling; the alternative — a plain <input type=file>,
    a full media-library/asset-manager).
13. Field POV evolution — the bare <input type=file> -> the styled
    hidden-input+label -> the drag-and-drop drop zone (with the button
    baseline reasserted for a11y) -> the async progress/abort/retry lifecycle
    -> the resumable/chunked/direct-to-cloud + headless engines (Uppy/tus);
    the React Aria FileTrigger/DropZone split codifying the a11y model.
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a file upload is — explain the
native-<input type=file>-styling pattern (the only accessible one), the
drag-is-an-enhancement-not-the-mechanism a11y crux (the FileTrigger/DropZone
split), the upload-lifecycle state machine (progress/abort/retry, the
AbortController lineage), the client-validation-is-UX-not-security boundary,
the file-list + preview anatomy (the createObjectURL leak), and the
resumable/chunked/direct-to-cloud scale boundary that field leaders diverge on.
