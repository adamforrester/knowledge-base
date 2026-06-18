# File Upload — external-agent pass

## 1. Component Identity & Metadata
* **Name**: `FileUpload`
* **Aliases**: `FileUploader`, `Upload`, `DropZone`, `FileTrigger`, `Dragger`, `FileInput`
* **Hierarchy**: Form Composite (stands on `TextField` substrate; composes `Button`, `Icon`, `List`, `Progress`; borders `EmptyState`, `Tag`/`Badge`)
* **Async Heritage**: Reuses the `AbortController` cancellation/race model (`Combobox`) and the `aria-live` status announcement contract (`Toast`, `Progress`).

## 2. Executive Summary & Framing
The `FileUpload` component is the most architecturally complex form control in a design system. Unlike basic controls (e.g., `TextField` or `Checkbox`) which operate synchronously within local client memory, `FileUpload` manages a complex, multi-state asynchronous network lifecycle directly coupled to the browser’s filesystem APIs.

### What it is
A specialized, composite form control that enables users to select, validate, queue, upload, and manage files. It acts as a bridge between the browser's native file system, the application state, and remote storage. It is structured around three core pillars:
1. **The Native Baseline**: A securely styled, hidden native HTML `<input type="file">` control.
2. **The Assistive Layer**: A focusable keyboard/screen-reader path paired with an `aria-live` announcement region.
3. **The Progressive Drag-and-Drop Layer**: A pointer-only spatial enhancement overlay.

### What it is not
* **A generic, uncoupled drag-and-drop zone**: It is not an arbitrary drop target. It must resolve to a valid form submission value.
* **An inline media editor**: It does not handle image cropping, rotation, or audio/video editing (though it may trigger them as subsequent modal flows).
* **A complete digital asset manager (DAM)**: It manages the ingest pipeline, not long-term asset retrieval, versioning, or complex metadata editing.

### The Systemic Tension: Core Divergences
Design systems fundamentally diverge on how far the component's scope should extend. The primary point of friction is the **boundary between UI presentation and network execution**:

| Archetype | Philosophy | Key Examples | Pros | Cons |
| --- | --- | --- | --- | --- |
| **The Pure Presentational Component** | The UI only manages the file selection queue (`File` objects). Network requests are handled entirely by the consumer on form submission. | Shopify Polaris (`DropZone`), IBM Carbon (`FileUploader`) | Extreme flexibility; zero coupling to network clients, CORS, or storage protocols. | High consumer boilerplate; local memory issues with large files; no out-of-the-box progress/retry UI. |
| **The Headless-Integrated Composite** | The system provides structured UI slots or hooks designed to wrap a dedicated upload engine. | React Aria (`FileTrigger` + `DropZone`), Ant Design (`Upload` paired with customizable actions) | Maintains strict accessibility separation while supporting complex async lifecycles. | Requires consumers to learn composite coordination patterns. |
| **The Full-Service Async Widget** | The component expects an endpoint URL, autonomously managing XHR/Fetch, progress tracking, chunks, and cancellation. | Atlassian (`MediaPicker`), FilePond (Standalone) | Drop-in ease of use for product teams; standardized upload performance and error handling. | Rigid; difficult to customize authentication headers, handle custom chunking, or bypass intermediate servers. |

## 3. Anatomy & Substrate Composition
The `FileUpload` component is a high-level composite. Rather than implementing layout elements from scratch, it coordinates several low-level primitives:
```
[FileUpload (Form Substrate: Label, Helper Text, Error State)]
 ├── [DropZone Area (Borders EmptyState, receives drag events)]
 │    ├── [Visual Affordance: Dashed Border, Upload Icon]
 │    └── [Trigger: Button (Proxying clicks to hidden input via Ref)]
 ├── [Hidden native <input type="file" tabIndex={-1} aria-hidden="true">]
 └── [FileList (List Substrate)]
      └── [FileListItem (composes Progress, Tag/Badge)]
           ├── [File Type Icon / Thumbnail Preview]
           ├── [Metadata: Name, Formatted Size]
           ├── [Status / Progress Bar (determinate/indeterminate)]
           └── [Action Actions: Cancel (AbortController) / Retry / Remove Button]
```

### The Substrates
* **Text Field (Form Field Substrate)**: Inherits the top-level form layout structure—specifically the label, optional/required indicators, helper text, and the validation error message display container. It links the hidden input to its validation messages using `aria-describedby` and `aria-invalid`.
* **Button**: Provides the primary interactive element (the "Browse" or "Choose File" control) that triggers the file selection dialog.
* **Icon**: Supplies context-specific glyphs, including generic file markers, mime-type indicators, status icons (success, error), and action triggers (such as close/remove crosses).
* **List & Progress**: Organizes active uploads and displays their real-time state using a determinate progress indicator.
* **Empty State**: Governs the layout, messaging, and visual presentation of the drop target before files are dropped or selected.

## 4. API & Properties
*(See claude.md and the synthesized brief §3 for the reconciled prop surface; the external pass's `FileObject` / `FileUploadProps` TypeScript interface is the fullest articulation of the per-file shape, the `uploadStrategy` immediate/on-submit toggle, the `onUploadFile(fileObj, onProgress, abortSignal)` headless hook, and the controlled `value` / uncontrolled `defaultValue` split.)*

Key resolved API shape:
- `FileObject`: `{ id, file, status, progress, name, size, type, previewUrl?, remoteId?, error? }`.
- Native: `accept` (hint), `multiple`, `capture` ('user'|'environment'), `webkitdirectory`.
- Validation: `maxFileSize`, `minFileSize`, `maxFilesLimit`, `onValidate(file)`.
- Execution: `uploadStrategy` ('immediate'|'on-submit'), `uploadUrl`, `onUploadFile(fileObj, onProgress, abortSignal) => Promise<{remoteId, previewUrl?}>`.
- State: controlled `value` / uncontrolled `defaultValue`, `onChange`, granular `onFileQueued`/`onUploadSuccess`/`onUploadError`/`onFileRemove`.

## 5. Architectural States & Structural Variants
### Drop Zone Visual States
1. **Idle / Empty** — dashed border, upload icon, instructional text.
2. **Drag-over** — solid brand border + background shift + "release to drop" copy on dragenter.
3. **Drag-reject** — destructive theme when hovered files violate `accept`/`maxFileSize` (instant feedback before drop).
4. **Disabled / Read-only** — grayed, `pointer-events: none`, the browse button disabled.

### The Per-File Upload State Machine
`Selected → Validating → (Passed) Queued → Uploading [determinate progress] → Success | Error → Retry`; `(Failed) Rejected` (never queued). Uploading shows progress + cancel; Success swaps cancel→remove; Error shows the message + Retry + Remove.

### Layout Variants
1. **Single-File / Minimalist (Avatar Uploader)** — compact circular/square; on upload the zone is replaced by a preview with hover Edit/Delete; no external list.
2. **Standard Multi-File List** — a prominent Drop Zone above a vertical list of items (progress + metadata + status).
3. **Picture Card Grid** — a responsive grid of square cards (e.g. 80–120px) with the "Add File" trigger as a trailing empty card; progress as a circular overlay.

## 6. Accessibility (a11y) & Platform Integration
### The Core Crux: Drag-and-Drop is Only an Enhancement
A drop zone is pointer-only — keyboard/screen-reader users cannot drag. Per **WCAG 2.1.1**, drag-and-drop can never be the sole method; the focusable browse button opening the native dialog is the primary mechanism. React Aria's reference split: `FileTrigger` (makes any button an accessible native chooser) + `DropZone` (pointer-only drag state/visuals/drop). For keyboard/SR users the DropZone is purely presentational; the browse button inside stays interactive.

### The Style-the-Unstylable Pattern
* **Anti-pattern**: `display:none`/`visibility:hidden` (removes from the a11y tree); an `opacity:0` absolutely-positioned overlay (brittle, misaligns tap targets/zoom).
* **Correct**: visually-hide the native input (clip rect utility class), pair with an explicit `<label>` or proxy via a `ref` (`inputRef.current?.click()`), with `tabIndex={-1}` + `aria-hidden` on the hidden input so keyboard users land on the styled button, not the raw input. Reset `value` after handling so the same file re-fires `change`.

### Live Region Communication
1. Queue additions — `aria-live="polite"`: "Successfully added document.pdf to upload queue."
2. Uploading — announce at intervals (~every 25%), not every percent: "Uploading document.pdf, 50% complete."
3. Completion — "document.pdf uploaded successfully."
4. Failures — `role="alert"`/`aria-live="assertive"`: "Error: document.pdf exceeded the maximum size limit of 10 Megabytes."

### List Item Semantics
Render files in a `<ul>`/`<ol>` (count exposed); each remove/cancel button has a unique file-named label ("Remove report.docx", "Cancel report.docx upload"), never bare "Delete"; per-item errors associate via `aria-describedby`.

### WCAG SC Mapping
1.3.1 (label/error/helper association via `aria-describedby`), 1.4.13 (dismissable/hoverable hover content), 2.1.1 (all functions keyboard-operable), 3.3.1 (error identification in text, associated), 4.1.2 (name/role/value on the hidden input + triggers), 4.1.3 (status messages via live regions).

## 7. Operational Implementation Notes & Traps
### Trap 1: The Missing `dragover` Prevention
Browsers open dropped files in a new tab by default — `preventDefault()` (and `stopPropagation()`) on `dragover`/`dragenter` is mandatory or drop never fires.

### Trap 2: The Drag-Leave Flicker
`dragleave` fires when crossing onto child elements, flickering the active styling. Fixes: **CSS** — `pointer-events: none` on all drop-zone children while dragging (simplest, best perf); **JS counter** — increment on enter / decrement on leave, active while > 0, reset to 0 on drop.

### Managing Object URL Memory Leaks
`URL.createObjectURL(file)` for previews leaks until tab close if not revoked — `URL.revokeObjectURL()` on unmount/removal (a `useEffect` cleanup keyed on the file).

### Client-Side Validation is UX, Not Security
`accept` and extension/MIME are trivially spoofed. The server MUST re-validate — magic-byte sniffing, strict size limits, malware scan, filename sanitization (prevent execution attacks).

### Asynchronous Lifecycle & Network Operations
**Fetch does not support upload progress.** Use `XMLHttpRequest` with `xhr.upload.onprogress` (or axios) for granular progress; wire `abortSignal.addEventListener('abort', () => xhr.abort())` for cancellation (the AbortController model).

### Scale Boundary: Large Files & Cloud Storage
1. **Direct-to-Cloud** — client requests a presigned URL from the app server, then uploads the payload straight to S3/GCS, bypassing the app server.
2. **Resumable Multipart (`tus`)** — for files > ~100MB, chunk + track received chunks; resume from the last successful chunk on a dropped connection.
3. **Headless engines** — Uppy / Dropzone.js own the resumable/multipart logic; the design system styles the wrapper.

## 8. Content & Editorial Guidelines
- High-density: "Drag files here or browse" + "Supports PDF, DOCX, and PNG up to 10MB."
- Single image: "Drag your photo here or browse to upload." + "PNG or JPG, maximum 2MB."
- Errors — specific with a solution: invalid format → "Cannot upload system_log.txt. Only image files (.jpg, .png) are supported."; size → "annual_report.pdf is 25MB and exceeds the maximum allowed size of 15MB."; limit → "You can only upload a maximum of 3 images. Please remove an existing image before adding another."; network → "The upload of photo.jpg was interrupted. Check your internet connection and try again."

## 9. Motion & Interaction Design
- Drag-over highlight: `transition: border-color 150ms ease-in-out, background-color 150ms ease-in-out`.
- List additions: entrance (slide-down / fade-in, ~200ms).
- List removals: scale-down + collapse height (~200ms) before DOM removal.
- Progress: animate `transform: scaleX(progress)` not `width` (60fps).
- `@media (prefers-reduced-motion: reduce)` — disable transitions/entries, instant state changes.

## 10. Internationalization (i18n)
- Translate all microcopy ("Drag and drop files here", "Browse files", "Cancel upload", "Retry upload", "Remove file").
- File sizes via `Intl.NumberFormat(locale, ...)`, binary (KiB/MiB) or decimal (KB/MB) per system standard.
- RTL — mirror the whole layout: drop-zone icon/text alignment, file thumbnails/names align right, progress fills right-to-left, cancel/remove align far left.

## 11. Component Relationships & Composition
Stands on Text Field (form layout/label/helper/error); the FileUpload container composes Empty State (drop-zone structure) and borders Tag/Badge (file tags / state chips); sub-components: the trigger Button (native selector), the List (queue), Icon (mime-types + X/Retry), the Progress bar.

## 12. Field POV Evolution
Era 1 Native Baseline (raw unstyled inputs) → Era 2 Styled Labels (visually-hidden input + styled `<label>`) → Era 3 Drag-and-Drop Zones (visual targets; accessible browse buttons reintroduced to fix pointer-only limits) → Era 4 Modern Async Composites (state-driven, React Aria separating trigger logic from drop-zone layout). React Aria (2025/2026) is the reference: separating file triggers from drop zones makes the component accessible by default.

## 13. System Default Recommendation (Opinionated Specification)
Default architecture: `[FileUpload] → [FileTrigger (accessibility node: focusable browse button + hidden native input + keyboard trigger)] + [DropZone (interaction handler: dragover highlights, prevent default file-opens, translate drops into File objects)]`.

- **Decoupled execution** — adopt the **Headless-Integrated** pattern: the component does NOT manage raw HTTP internally; expose clean hooks (`onUploadFile`/`onChange`) + a standardized UI wrapper for the queue, so consumers wire any network client/auth/direct-to-S3 without forking the library.
- **Standard selection hook** — default to **immediate-upload**: validate client-side, add to the visible queue, begin upload immediately (instant progress, early error catch). On success, store the server-returned identifier/URL in the parent form; the form submits only those remote IDs (fast, lightweight).
- **Robust DnD** — visually-hidden input + ref-proxied browse button + `pointer-events:none` on drop-zone children + revoke object URLs on remove/unmount.

## 14. Sources Cited
* **Adobe Spectrum / React Aria** (`react-aria-components` v1.2.0, Nov 2024 / updates Feb 2026) — the decoupled `FileTrigger` + `DropZone` pattern.
* **Shopify Polaris** (v13.8.0, Dec 2024) — presentational drop-zone layout + queue UI.
* **IBM Carbon** (v11.60.0, Jan 2025) — modular composition (file container vs active upload item).
* **Ant Design** (v5.24.0, Feb 2025) — multiple uploader layouts (Avatar, Photo Card Grid, Standard List).
* **tus Resumable Upload Protocol** (v1.0.0 spec, active draft 2025/2026) — large-file chunking/recovery.

## 15. Agent-Consumable Schema
*(JSON-schema form in the external pass; reconciled into the YAML §15 of the synthesized brief, conformant to components/_schema.md.)*
