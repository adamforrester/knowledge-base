#!/usr/bin/env python3
"""Vault check: the five mechanical checks from issue #75.

Python 3 standard library only. Run from anywhere:

    python3 scripts/vault-check.py            # check the vault this script lives in
    python3 scripts/vault-check.py --root DIR # check another copy

1. Every numbered file has the five frontmatter keys, each with a non-empty
   value, and its H1 matches `# NN — Title`.
2. Every "(See ...)" cross-ref names an existing numbered file, whether as a
   slug (`See 15-ai-in-ds`) or a bare number (`See 00b`, `See 15 §3`), and
   however deeply the parenthesis nests.
3. No [[wikilinks]], and no relative markdown links (inline or reference-style)
   outside the catalogue index files.
4. Every _source-text/ and _research/ path cited in a numbered file exists.
5. Every numbered file has a hook in index.md.

Exit status is 1 if any enforced check fails. A check listed in REPORT_ONLY
still prints its failures but does not fail the run, unless --strict is given.

Files are read as UTF-8 with an optional BOM, and CRLF or CR line endings are
normalized to LF before any check runs.
"""

import argparse
import glob
import os
import re
import sys

# Checks listed here print their failures but don't fail the run. Use it to
# land a new check before main passes it; empty it once main does (#79).
# --strict ignores this set.
REPORT_ONLY = set()

NUMBERED = re.compile(r"^(\d\d[a-z]?)-[a-z0-9-]+\.md$")
FRONTMATTER_KEYS = ("type", "title", "description", "tags", "timestamp")
# Catalogue index files may use relative markdown links (check 3).
CATALOGUE_INDEXES = {"index.md", "components/index.md", "patterns/index.md"}
# Vault prose beyond the numbered files that checks 2 and 3 also read.
EXTRA_GLOBS = ("index.md", "GLOSSARY.md", "components/*.md", "patterns/*.md")

FENCE = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")
SEE_WORD = re.compile(r"\bsee\b", re.I)
SLUG_REF = re.compile(r"(?<![\w/.-])(\d\d[a-z]?-[a-z][a-z0-9-]*[a-z0-9])(?:\.md)?(?![\w/-])")
# A bare file number in reference position: `See 00b`, `see 15 §3`,
# `see 18, 21 and 22`. It must open the "see" tail or follow a list joiner, so a
# count such as "~40 components" isn't read as a file. Not part of a year,
# version, section number or percentage.
BARE_REF = re.compile(r"(?:^|\band|\bor|\balso|\bplus|\bsee|[,;/])[ \t\n]*(\d\d[a-z]?)(?![\w%/.-]|\.\d)", re.I)
WIKILINK = re.compile(r"\[\[[^\]]*\]\]")
MD_LINK = re.compile(r"\]\(([^)\s]+)[^)]*\)")
REF_DEF = re.compile(r"^ {0,3}\[[^\]\n]+\]:[ \t]*<?([^\s>]+)", re.M)
ABSOLUTE = re.compile(r"^([a-z][a-z0-9+.-]*:|#)", re.I)
CITED_PATH = re.compile(r"(?<![\w/])((?:_source-text|_research)/[^\s`'\"()\[\]<>,;]*)")


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8-sig", newline="") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n")


def numbered_files(root):
    return sorted(n for n in os.listdir(root) if NUMBERED.match(n))


def prose_files(root):
    files = set(numbered_files(root))
    for pattern in EXTRA_GLOBS:
        for path in glob.glob(os.path.join(root, pattern)):
            files.add(os.path.relpath(path, root).replace(os.sep, "/"))
    return sorted(files)


def frontmatter_values(block):
    """Map each top-level key to its value: the inline value, else any indented
    continuation lines (a block list or folded scalar). Empty means no value."""
    values, key = {}, None
    for ln in block.splitlines():
        top = re.match(r"^([A-Za-z_][\w-]*)\s*:(.*)$", ln)
        if top:
            key = top.group(1)
            values[key] = top.group(2).strip()
            if values[key] in ('""', "''", "[]", "~", "null", "|", ">", "|-", ">-"):
                values[key] = ""
        elif key and ln.strip() and ln[:1] in " \t":
            item = ln.strip()
            if item not in ("-", '- ""', "- ''"):
                values[key] = (values[key] + " " + item).strip()
    return values


def paren_groups(text):
    """Yield (start, end) of every balanced (...) group, nested ones included.
    A blank line closes any group still open, so a stray "(" can't swallow the
    rest of the file."""
    stack = []
    i = 0
    while i < len(text):
        c = text[i]
        if c == "(":
            stack.append(i)
        elif c == ")" and stack:
            yield stack.pop(), i + 1
        elif c == "\n" and re.match(r"\n[ \t]*\n", text[i:i + 64]):
            stack.clear()
        i += 1


def check_frontmatter_and_h1(root):
    errors = []
    for name in numbered_files(root):
        text = read(root, name)
        prefix = NUMBERED.match(name).group(1)
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not m:
            errors.append(f"{name}: no YAML frontmatter block at the top")
            body = text
        else:
            values = frontmatter_values(m.group(1))
            missing = [k for k in FRONTMATTER_KEYS if k not in values]
            if missing:
                errors.append(f"{name}: frontmatter missing {', '.join(missing)}")
            empty = [k for k in FRONTMATTER_KEYS if k in values and not values[k]]
            if empty:
                errors.append(f"{name}: frontmatter value empty for {', '.join(empty)}")
            body = text[m.end():]
        h1 = re.search(r"^# .*$", body, re.M)
        if not h1:
            errors.append(f"{name}: no H1")
        elif not re.match(rf"^# {re.escape(prefix)} — \S", h1.group(0)):
            errors.append(f"{name}: H1 is '{h1.group(0)}', expected '# {prefix} — Title'")
    return errors


def check_see_refs(root):
    stems = {n[:-3] for n in numbered_files(root)}
    prefixes = {NUMBERED.match(n).group(1) for n in numbered_files(root)}
    errors = []
    for rel in prose_files(root):
        text = FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), read(root, rel))
        seen = set()
        for start, end in paren_groups(text):
            inner = text[start + 1:end - 1]
            see = SEE_WORD.search(inner)
            if not see:
                continue
            base = start + 1 + see.end()
            tail = inner[see.end():]
            for ref in SLUG_REF.finditer(tail):
                pos = base + ref.start(1)
                if ref.group(1) not in stems and pos not in seen:
                    seen.add(pos)
                    errors.append(f"{rel}:{line_of(text, pos)}: cross-ref '{ref.group(1)}' names no numbered file")
            for ref in BARE_REF.finditer(SLUG_REF.sub(lambda m: " " * len(m.group(0)), tail)):
                pos = base + ref.start(1)
                if ref.group(1) not in prefixes and pos not in seen:
                    seen.add(pos)
                    errors.append(f"{rel}:{line_of(text, pos)}: cross-ref '{ref.group(1)}' names no numbered file")
    return errors


def check_links(root):
    errors = []
    for rel in prose_files(root):
        text = read(root, rel)
        text = FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
        text = INLINE_CODE.sub(lambda m: " " * len(m.group(0)), text)
        for m in WIKILINK.finditer(text):
            errors.append(f"{rel}:{line_of(text, m.start())}: wikilink {m.group(0)}")
        if rel in CATALOGUE_INDEXES:
            continue
        for m in MD_LINK.finditer(text):
            if not ABSOLUTE.match(m.group(1)):
                errors.append(f"{rel}:{line_of(text, m.start())}: relative markdown link ({m.group(1)})")
        for m in REF_DEF.finditer(text):
            if not ABSOLUTE.match(m.group(1)):
                errors.append(f"{rel}:{line_of(text, m.start())}: relative reference-style link ({m.group(1)})")
    return errors


def check_cited_paths(root):
    errors = []
    for name in numbered_files(root):
        text = read(root, name)
        for m in CITED_PATH.finditer(text):
            path = m.group(1).rstrip(".:")
            target = os.path.join(root, path)
            exists = glob.glob(target) if any(c in path for c in "*?[") else os.path.exists(target)
            if not exists:
                errors.append(f"{name}:{line_of(text, m.start())}: cited path '{path}' does not exist")
    return errors


def check_index_hooks(root):
    index = read(root, "index.md")
    return [f"{name}: no hook in index.md" for name in numbered_files(root)
            if not re.search(rf"\(/?{re.escape(name)}\)", index)]


CHECKS = (
    (1, "frontmatter keys and H1", check_frontmatter_and_h1),
    (2, "(See NN...) cross-refs resolve", check_see_refs),
    (3, "no wikilinks or relative links", check_links),
    (4, "cited _source-text/ and _research/ paths exist", check_cited_paths),
    (5, "index.md hook for every numbered file", check_index_hooks),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument("--strict", action="store_true", help="enforce the report-only checks too")
    args = parser.parse_args()
    root = args.root
    report_only = set() if args.strict else REPORT_ONLY
    failed = False
    for num, label, fn in CHECKS:
        errors = fn(root)
        mode = " (report-only)" if num in report_only else ""
        status = "PASS" if not errors else ("WARN" if num in report_only else "FAIL")
        print(f"[{status}] {num}. {label}{mode}: {len(errors)} problem(s)")
        for e in errors:
            print(f"    {e}")
        if errors and num not in report_only:
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
