# Architectural Decision Brief: The Tree (TreeView) Component
**Category:** Data (Hierarchical Sibling)
**Target Audience:** Senior Design Systems Practitioners, Component Engineers

---
## 1. Framing
The Tree (`TreeView`) is the hierarchical sibling of the List and the 2D Table. It completes the Data component triad (1D List, 2D Table, Hierarchical Tree) by managing deep, nested relationships. Of all components in a design system, the Tree inherits the most architectural debt and composable baggage. It is highly prone to structural over-reach and accessibility failures.

### The Core Architectural Tension: `role="tree"` vs. Disclosure Navigation
The most persistent architectural trap in design systems is the misapplication of `role="tree"` to website hierarchies, documentation sidebars, or application menus. This structural over-reach conflates **Navigation** with **Data Interaction**:

1. **The Disclosure Navigation Model:** If the user is navigating to pages (e.g., a docs site sidebar), the component is a **Side Navigation** component. It must be built using nested `<ul>`/`<li>` containers containing semantic anchor (`<a>`) tags and native disclosure buttons (`aria-expanded`). Every link is a tab stop. It does **not** use `role="tree"`, `role="treeitem"`, or tree-specific arrow-key handling.
2. **The `role="tree"` Data Widget Model:** If the user is selecting, checking, dragging, or running actions on a hierarchical structure within an application (e.g., a file directory browser, a permissions hierarchy picker, or a category manager), it is a **Data Tree Widget**. It must use `role="tree"`, act as a single focusable tab stop, manage focus via roving `tabindex` or `aria-activedescendant`, and support complex directional keyboard traversal.

### Key Conceptual Pillars
* **The APG Keyboard Model:** Unlike standard document flow, a Tree widget operates in "Widget Mode." It captures arrow keys to expand, collapse, and traverse visible nodes, reducing keyboard fatigue by exposing only one tab stop to the page document flow.
* **The Tri-State Cascading Checkbox Tree:** When selection is multi-state and hierarchical, child selections must propagate upward to set parent states to checked, unchecked, or indeterminate. This requires synchronized bottom-up and top-down state-resolution passes.
* **The Virtualization vs. Hierarchy Tension:** Modern high-performance Trees flatten the nested tree data structure into a linear, single-level array of visible items to allow DOM virtualization. This flattening destroys natural DOM nesting, forcing screen readers to rely exclusively on precise, programmatically calculated ARIA properties (`aria-level`, `aria-setsize`, `aria-posinset`) on every node.

### Divergence in System Practice
* **React Aria (Adobe Spectrum)** treats the tree as an accessible collection model, emphasizing strict keyboard navigation, robust selection management, and clean programmatic focus.
* **Microsoft Fluent** implements a "Flat Tree" model by default, optimizing for raw performance and virtualization in complex enterprise applications.
* **Ant Design** focuses on feature density, shipping built-in drag-and-drop, inline directories, and cascading search filters natively inside the component.
* **GitHub Primer** implements a highly polished, lightweight, accessible `TreeView` optimized specifically for repository navigation and file-system browsing.

---
## 2. Anatomy and Parts
The physical DOM layout of a `role="tree"` component changes significantly depending on whether it is virtualized or non-virtualized.

### Component Parts
#### 1. The Tree Container (`role="tree"` or `role="treegrid"`)
The structural root wrapper. It owns the global interaction model (e.g., `aria-multiselectable="true"`) and serves as the single interactive keyboard tab stop.

#### 2. The Group Container (`role="group"`)
In non-virtualized markup, this container wraps the child nodes of an expanded parent `treeitem`. It programmatically groups related children, allowing screen readers to communicate context shifts when entering or leaving a nest level.

#### 3. The Tree Node (`role="treeitem"`)
The focal structural element representing a single point in the hierarchy.
* **Indentation/Guide-line Region:** An empty inline-start area that scales dynamically with the node's `aria-level`. For readability, design systems often render vertical "guide lines" down these channels.
* **Expand/Collapse Twisty:** The disclosure toggle button. It must display a chevron or pointer icon that rotates 90 degrees based on state.
* **Leading Icon:** Typically a contextual folder (parent node) or file (leaf node) icon. It provides a visual shortcut for structural classification.
* **Checkbox:** A native or custom checkbox wrapper. It handles tri-state visualization (`checked`, `unchecked`, `indeterminate`) in checkbox trees.
* **Node Label:** The primary text node describing the element.
* **Trailing Actions/Badges:** Contextual controls (e.g., "Add folder," "Delete item," status badges) that appear on hover or focus.

#### 4. The Loading/Empty Node Regions
Dynamic structural slots within the node or group container. If a node is lazy-loaded, its group container should temporarily render an interactive skeleton loading state or a spinner with `aria-busy="true"`.

(Virtualized / flattened DOM: virtualized nodes are siblings in the DOM, absolute-positioned vertically via `transform: translateY()`, each carrying its own `aria-level`/`aria-setsize`/`aria-posinset`.)

---
## 3. Properties / API
An enterprise Tree API must cleanly separate the underlying raw hierarchical data model from the UI presentation, navigation state, and virtualization engines.

### 1. Data Contract Representation
We recommend a normalized, flat-map database pattern internally, even if the user passes nested JSON.

```typescript
interface TreeNode<T = Record<string, any>> {
  id: string;
  label: string;
  children?: string[]; // References to child IDs (Normalized representation)
  isBranch?: boolean;  // Explicitly forces branch behavior even if children array is empty
  icon?: string | React.ReactNode;
  isDisabled?: boolean;
  value?: T;           // Associated metadata or domain entity
}
type TreeDataMap<T> = Record<string, TreeNode<T>>;
```

### 2. Core Tree Properties
| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `data` | `TreeNode[] \| TreeDataMap` | `[]` | The primary data source. Can be structured hierarchically or flattened. |
| `expandedKeys` | `string[]` | — | Controlled key array representing currently expanded node IDs. |
| `defaultExpandedKeys` | `string[]` | `[]` | Uncontrolled initial expansion state. |
| `selectionMode` | `"none" \| "single" \| "multiple"` | `"none"` | The selection engine behavior. |
| `selectedKeys` | `string[]` | — | Controlled collection of selected node IDs. |
| `onSelectionChange` | `(keys: string[]) => void` | — | Selection state event handler. |
| `onNodeExpand` | `(nodeId: string) => void` | — | Event fired when a node expands. |
| `onNodeCollapse` | `(nodeId: string) => void` | — | Event fired when a node collapses. |
| `selectionBehavior` | `"toggle" \| "replace"` | `"replace"` | Sets selection behavior on node click/interaction. |
| `checkboxMode` | `"none" \| "cascade" \| "independent"` | `"none"` | Configures structural cascading and indeterminate state behavior. |
| `loadOnExpand` | `(nodeId: string) => Promise<void>` | — | Triggers async data fetching for lazy-loaded children. |
| `virtualize` | `boolean` | `false` | Enables absolute-positioned virtualization rendering engine. |
| `dragAndDrop` | `boolean` | `false` | Enables native or HTML5 drag-and-drop tree reordering API. |

---
## 4. States and Variants
Trees combine micro-states (node-level states) and macro-states (component-level structural layouts).

### Node-Level States
* **Unfocused / Hovered / Focused:** Focused state is strictly bound to roving focus. Only the active node receives focus outlines. When using `aria-activedescendant`, the container element owns physical browser focus, and the pseudo-focused node is styled via an active state class (e.g., `is-active-node`).
* **Expanded / Collapsed / Leaf:** Expanded (parent showing children, `aria-expanded="true"`); Collapsed (parent hiding children, `aria-expanded="false"`); Leaf (no children, no toggle chevron, does not expose `aria-expanded`).
* **Selection States:** Selected (`aria-selected="true"`); Unselected (`aria-selected="false"` or omitted when selection is not active).
* **Checkbox Propagation States:** Checked (all descendants checked); Unchecked (all descendants unchecked); Indeterminate (some but not all descendants checked).
* **Loading (Lazy Children):** The parent node has been expanded and an asynchronous process is fetching its children. The node renders a busy spinner or skeleton placeholders, accompanied by `aria-busy="true"`.
* **Disabled:** Disables interactions, keyboard navigation, and selection events for the targeted node and its nested descendants.

### Variant Permutations
#### 1. Checkbox Tree
Adds structural multiselect mechanics. Selecting a node automatically toggles the checked states of its recursive child branches. It also updates its upstream ancestor chain's indeterminate states.

```
       [─] Folder Parent (Indeterminate: Some children checked)
        ├── [X] Subfolder A (Checked: All children checked)
        │    ├── [X] Document 1 (Checked)
        │    └── [X] Document 2 (Checked)
        └── [ ] Subfolder B (Unchecked)
             └── [ ] Document 3 (Unchecked)
```

#### 2. Directory Tree (File Explorer Mode)
Optimized for high-density navigation. Clicking anywhere on the node row toggles expansion rather than selection, mimicking native operating system explorer behavior (like macOS Finder or VS Code). It typically uses a twin selection mechanism: a single-click sets visual highlighting, while a double-click triggers node execution.

#### 3. Treegrid (The Multi-Column Data Grid Tree)
This variant merges a Tree with a Table, making it highly effective for nested hierarchical data lists (such as financial balance sheets or file details displays with name, size, and modified-date columns). It must implement custom two-axis keyboard navigation: Row Focus Mode (Left/Right collapse/expand) and Grid Mode (Left/Right cell navigation).

#### 4. Density Scale
* **Compact (High-Density):** 24px-28px row heights. Designed for professional utility tools and asset managers (file trees, layers panels).
* **Comfortable (Default):** 32px-40px row heights. Optimized for standard web interfaces and setup forms (permissions trees, category selections).

---
## 5. Usage Guidance
1. **Do not use a `Tree` widget for Main Application Navigation or Documentation Sidebars.** If clicking an item changes the page URL and triggers a full page render, build it as a standard HTML `<nav>` element containing semantic nested unordered lists (`<ul>`, `<li>`) and disclosure buttons. Using `role="tree"` in this context breaks standard page-navigation accessibility, prevents screen reader users from using tab-key site discovery, and forces them into an unexpected application key-interception mode.
2. **Do not use an `Accordion` for deeply nested hierarchies.** Accordions are flat collections of disclosure panels. Nesting Accordions more than two levels deep breaks accessibility and visual readability. For deep structural nesting, use a true hierarchical Tree.
3. **Use a `Treegrid` when a parent-child hierarchy requires supplementary metadata columns.** If users must sort, filter, or evaluate sibling nodes by multiple columns (file size, owner, status), use `role="treegrid"` instead of a standard `role="tree"`.
4. **Use Virtualization when displaying more than 150-200 nodes simultaneously.** Rendering hundreds of nested DOM elements degrades performance and impacts interactions like scroll fluidity and toggle animations.

---
## 6. Accessibility (A11y)
Writing a reliable `role="tree"` component requires precise screen reader support. It represents one of the most complex accessibility challenges in component engineering.

### 1. The ARIA Role Taxonomy
* **`role="tree"`:** Applied to the root element. It must contain the global accessible label (`aria-label` or `aria-labelledby`).
* **`role="treeitem"`:** Applied to every interactive node (both branch parents and leaf children). *Critical detail:* Focus styles must target the `treeitem` element, not nested wrappers inside it.
* **`role="group"`:** Applied to child node containers. This role acts as a grouping element, allowing screen readers to declare hierarchy nesting transitions when entering or leaving a node list.

### 2. The Structural-to-AT Crux: Hierarchical Attributes
For assistive technologies (AT) to build an accurate mental model of a tree, every active `role="treeitem"` must expose four properties:
1. **`aria-expanded`:** Controls branch states. Set to `true` when parent nodes are expanded, `false` when collapsed. **Do not** add this attribute to leaf nodes, as doing so tricks screen readers into identifying the leaf node as an empty branch.
2. **`aria-level`:** An integer starting at `1` that explicitly defines the node's nest depth. It must scale sequentially (1, 2, 3...) as nesting deepens.
3. **`aria-setsize`:** Defines the total number of sibling items at the current `aria-level` within the current `role="group"`.
4. **`aria-posinset`:** An integer (starting at `1`) that defines the node's current sequence position within its peer set.

### 3. Virtualization & The Flattened Tree Paradox
DOM Virtualization poses a significant accessibility challenge: it replaces nested element hierarchies with flat lists of absolutely-positioned nodes. This removes child elements from parent DOM wrappers and strips out child `role="group"` containers entirely. **The Solution:** You must explicitly calculate and inject the correct structural attributes (`aria-level`, `aria-setsize`, and `aria-posinset`) onto every flattened node manually. Screen readers rely entirely on these programmatic markers to announce nesting levels and list counts, ignoring the flat physical DOM layout.

### 4. The Canonical Keyboard Model (APG)
A tree component must run on a single-tab-stop model. Only the active `treeitem` should have `tabindex="0"`; all other items must have `tabindex="-1"`. Alternatively, use `aria-activedescendant` on the root container.
* **`ArrowDown` / `ArrowUp`:** Navigates vertically through the flattened list of visible nodes. It skips collapsed nested nodes, targeting only the next or previous elements currently visible.
* **`ArrowRight`:** On a collapsed parent node — Expands the branch (does not change focus). On an expanded parent node — Moves focus to the first nested child node. On a leaf node — Does nothing.
* **`ArrowLeft`:** On an expanded parent node — Collapses the branch (does not change focus). On a collapsed parent or leaf node — Moves focus up to the parent node.
* **`Enter` / `Space`:** Selects or activates the focused node.
* **`Home` / `End`:** Jumps focus to the first or last visible node.
* **Asterisk (`*`):** Recursively expands the currently focused node and all of its sibling branches at the same hierarchical level.
* **Typeahead (Character Search):** Focuses the next visible node that starts with the pressed character sequence.

### 5. Checkbox Trees Accessibility Model
In checkbox trees, avoid adding selection roles directly to the checkbox element. Instead, make the checkbox a purely presentational layout element inside the node. Manage selection states directly on the parent structure using `aria-selected` or `aria-checked` on the host `role="treeitem"`.

```html
<div role="treeitem" id="node-p1" aria-checked="mixed" aria-expanded="true" aria-level="1" aria-setsize="3" aria-posinset="1" tabindex="0">
  <span class="custom-checkbox custom-checkbox--indeterminate" aria-hidden="true"></span>
  <span class="label">Project Files</span>
</div>
```

### 6. Critical WCAG Compliance Rules
* **WCAG 1.3.1 - Info and Relationships:** The hierarchical relationship between parents, children, and nesting levels must be accurately announced via correct ARIA levels, sizes, and group associations, even when virtualized.
* **WCAG 2.1.1 - Keyboard Accessibility:** Every node interaction (branch toggles, checkbox selection, action triggers) must be fully accessible using standard keyboard controls.
* **WCAG 4.1.2 - Name, Role, Value:** Expanded, collapsed, checked, and unchecked states must dynamically update their ARIA attributes instantly when toggled.

---
## 7. Content Guidelines
### 1. Labeling & Text Wrap Limits
Keep node labels concise. Long names should truncate with an ellipsis if they overflow the row width. Users should be able to hover over truncated items to view the full text in a native browser tooltip or localized micro-popup.

### 2. Nesting Guidelines
Avoid deep nesting. Design systems should encourage builders to limit hierarchies to a maximum of 4–5 levels. Deeper nesting increases visual noise, squashes horizontal space, and creates layout fatigue on mobile or narrow viewports.

### 3. Count Indicators & Badges
If a node includes an item count (such as the number of unread messages in an inbox folder), render the count in a trailing badge. Use screen reader-only helper text to provide explicit context for assistive technologies (e.g., `aria-label="Folder Inbox, 14 unread items"`).

### 4. Action Accessibility
If a node includes action buttons (such as "Delete" or "Add Item"), make sure these buttons do not steal focus during standard vertical arrow-key navigation. The user must be able to focus and trigger these actions by pressing `Tab` once they have navigated to the parent node.

---
## 8. Motion and Transition
### 1. Height Reveal Transition
Animates the nested group expansion state container from height `0` to its dynamic, natural height. Recommended approach: use modern CSS layout features to interpolate elements directly from height `0` to `auto`.

```css
.tree-group-container {
  display: block; overflow: hidden; height: 0;
  transition: height 200ms cubic-bezier(0.4, 0, 0.2, 1);
  interpolate-size: allow-keywords; /* Unlocks smooth transition to height: auto */
}
.tree-group-container.is-expanded { height: auto; }
```

### 2. Twist Icon Rotation
Toggling a branch should smoothly rotate its chevron `90deg` using a CSS transform (`transition: transform 180ms ease-in-out`).

### 3. The Large-Trees Exception (Performance Guard)
**Do not run expansion height animations on virtualized lists or trees rendering more than 100 items.** Virtualization dynamically mounts and unmounts DOM nodes on the fly; running custom height calculations during these lifecycle changes causes layout thrashing and stuttering. In virtualized trees, expansion states should toggle instantly without slide animations.

---
## 9. Internationalization (I18n)
### 1. The RTL Keyboard Key Swap
* **In LTR layouts:** `ArrowRight` expands a node, `ArrowLeft` collapses it.
* **In RTL layouts:** These keys swap functions. `ArrowLeft` expands the node, `ArrowRight` collapses it. Failing to swap these directions creates a disorienting, counter-intuitive keyboard experience for RTL users.

### 2. Layout & Guideline Mirroring
All directional properties must use logical, flow-relative CSS rules. Map physical margins/paddings using inline-start directives:

```css
.tree-node {
  padding-inline-start: calc(var(--tree-level-depth) * 16px);
  padding-inline-end: 16px;
}
```

Mirror twist chevrons automatically in RTL layouts to point left (`<`) when collapsed.

---
## 10. Naming
| Design System | Component Name | Node Child Name |
| --- | --- | --- |
| **MUI X** | `RichTreeView` / `SimpleTreeView` | `TreeItem` |
| **Ant Design** | `Tree` / `Tree.DirectoryTree` | `TreeProps['treeData']` / Internal Nodes |
| **Fluent UI** | `Tree` | `TreeItem` |
| **IBM Carbon** | `TreeView` | `TreeNode` |
| **React Aria** | `TreeView` | `TreeViewItem` |
| **GitHub Primer** | `TreeView` | `TreeView.Item` |

### Recommended Default Taxonomy
* **Component Class:** `TreeView`
* **Node Child Item:** `TreeViewItem`
* **Sub-Group Container:** `TreeViewGroup`

---
## 11. Implementation Notes
### 1. Managing Roving Tabindex
```typescript
const handleKeyDown = (event: React.KeyboardEvent, nodeId: string) => {
  const visibleNodes = getVisibleNodesList(treeData, expandedKeys);
  const currentIndex = visibleNodes.indexOf(nodeId);
  switch (event.key) {
    case 'ArrowDown': { event.preventDefault(); const next = visibleNodes[currentIndex + 1]; if (next) focusNode(next); break; }
    case 'ArrowUp': { event.preventDefault(); const prev = visibleNodes[currentIndex - 1]; if (prev) focusNode(prev); break; }
    // Implement arrow left, right, home, end, and typeahead...
  }
};
```

### 2. Tri-State Checkbox Propagation Logic
A programmatic checkbox tree requires two directional passes: (1) Downward Selection Pass — propagate the clicked node's checked state down to all nested descendants; (2) Upward Aggregation Pass — ascend the parent chain, inspect all child state permutations: all checked → parent Checked, all unchecked → parent Unchecked, mixed → parent Indeterminate.

```typescript
function computeCheckboxStates(nodeId, checked, currentSelected, currentIndeterminate, treeMap) {
  const nextSelected = new Set(currentSelected);
  const nextIndeterminate = new Set(currentIndeterminate);
  const setDescendantsState = (id, isChecked) => {
    if (isChecked) nextSelected.add(id); else nextSelected.delete(id);
    nextIndeterminate.delete(id);
    treeMap[id]?.children?.forEach((childId) => setDescendantsState(childId, isChecked));
  };
  setDescendantsState(nodeId, checked);
  const updateAncestors = (id) => {
    const parentId = findParentId(id, treeMap);
    if (!parentId) return;
    const siblings = treeMap[parentId].children || [];
    const checkedSiblings = siblings.filter((s) => nextSelected.has(s));
    const indeterminateSiblings = siblings.filter((s) => nextIndeterminate.has(s));
    if (checkedSiblings.length === siblings.length) { nextSelected.add(parentId); nextIndeterminate.delete(parentId); }
    else if (checkedSiblings.length === 0 && indeterminateSiblings.length === 0) { nextSelected.delete(parentId); nextIndeterminate.delete(parentId); }
    else { nextSelected.delete(parentId); nextIndeterminate.add(parentId); }
    updateAncestors(parentId);
  };
  updateAncestors(nodeId);
  return { nextSelected, nextIndeterminate };
}
```

### 3. Asynchronous Lazy Loading States
```typescript
const handleExpand = async (nodeId) => {
  const node = treeMap[nodeId];
  if (node.children && !node.isLoaded) {
    setLoadingNodeKeys((prev) => [...prev, nodeId]);
    try { const fetched = await loadOnExpand(nodeId); updateTreeStore(nodeId, fetched); }
    catch (err) { displayErrorNotification(err); }
    finally { setLoadingNodeKeys((prev) => prev.filter((k) => k !== nodeId)); }
  }
  setExpandedKeys((prev) => [...prev, nodeId]);
};
```

---
## 12. Related and Alternative Components
* **Inherits From:** Accordion/Disclosure (toggles nested child rendering dynamically); List (standard vertical collection layouts and visual item styling).
* **Composes:** Icon (leading visual symbols + navigation twisty); Checkbox (structural select options + nested multi-select logic); Empty State / Skeleton (fallback states while rendering or async loading).
* **Structural Borders:** Side Navigation (clean anchor layouts + native link disclosures instead of application-widget keyboard capture); Menu (command lists + immediate trigger actions; does not manage structural selection); Table (treegrid) (multi-column tables with expandable hierarchical row groups).

---
## 13. Field POV Evolution
### 1. From Menu Roles to Custom Component Architectures
Early design systems often over-allocated roles like `role="menu"` or `role="tree"` to standard navigation menus. This created serious navigation issues for screen reader users by turning off standard browser navigation shortcuts. Modern design systems draw a clear line: navigation structures must use standard native link elements inside disclosures, while complex data trees are reserved for custom interactive application widget roles.

### 2. High-Performance Virtualization & Flattened Render Loops
Older tree libraries nested DOM structures recursively. This performed poorly with larger datasets. Modern libraries (including **react-arborist** and **Fluent UI**) convert nested tree structures into flat, visual arrays behind the scenes. This enables fast, high-performance DOM virtualization while maintaining accessible screen reader navigation using precise, dynamic ARIA properties.

### 3. Highly Accessible Headless Libraries
Modern libraries (like **React Aria** and **headlessui**) handle complex arrow-key traversal, roving focus, and screen reader announcements out of the box. This shift allows design system engineers to focus on styling, visual layout transitions, and bespoke user actions without rebuilding complex accessibility engines from scratch.

---
## 14. Sources Cited
* **WAI-ARIA APG — Tree View Pattern** *(Aug 2024)* — https://www.w3.org/WAI/ARIA/apg/patterns/treeview/
* **WAI-ARIA APG — Treegrid Pattern** *(Aug 2024)* — https://www.w3.org/WAI/ARIA/apg/patterns/treegrid/
* **React Aria TreeView (Adobe Spectrum)** *(Oct 2024)* — https://react-spectrum.adobe.com/react-aria/TreeView.html
* **GitHub Primer Design System TreeView API** *(2024 Edition)* — https://primer.style/react/TreeView
* **Microsoft Fluent UI React "Flat Tree" Engine** *(Fluent v9, 2024)*
* **MUI X Rich Tree View (Material-UI)** *(v7, Sep 2024)* — https://mui.com/x/react-tree-view/
* **React Arborist (Bespoke Headless Virtualized Tree Engine)** *(v3.4, 2023)* — https://github.com/brimdata/react-arborist

---
## 15. Agent-Consumable Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "name": "tree-view",
  "type": "component",
  "status": "stable",
  "inherits": ["accordion", "list", "table"],
  "composes": ["icon", "checkbox", "empty-state", "skeleton"],
  "properties": {
    "data": { "type": "array", "description": "Normalized array of structural items mapping hierarchical associations." },
    "expandedKeys": { "type": "array", "items": { "type": "string" }, "description": "Controlled key list mapping currently expanded parent node ids." },
    "selectionMode": { "type": "string", "enum": ["none", "single", "multiple"], "default": "none" },
    "selectedKeys": { "type": "array", "items": { "type": "string" }, "description": "Collection of chosen visual nodes." },
    "checkboxMode": { "type": "string", "enum": ["none", "cascade", "independent"], "default": "none", "description": "Determines checkbox behavior and propagation." },
    "virtualize": { "type": "boolean", "default": false, "description": "Enables performance virtualization optimization." }
  },
  "states": ["expanded", "collapsed", "leaf", "selected", "unselected", "indeterminate", "focused", "hovered", "disabled", "loading"],
  "accessibility": {
    "role": "tree",
    "itemRole": "treeitem",
    "groupRole": "group",
    "keyboardModel": "APG Roving Tabindex / Activedescendant",
    "essentialAttributes": ["aria-expanded", "aria-level", "aria-setsize", "aria-posinset", "aria-multiselectable"]
  }
}
```
