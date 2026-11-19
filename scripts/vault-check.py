#!/usr/bin/env python3
"""Vault check: the five mechanical checks from issue #75.

Python 3 standard library only. Run from anywhere:

    python3 scripts/vault-check.py            # check the vault this script lives in
    python3 scripts/vault-check.py --root DIR # check another copy

1. Every numbered file has the five frontmatter keys, and its H1 matches `# NN — Title`.
2. Every inline "(See NN-...)" cross-ref names an existing numbered file.
3. No [[wikilinks]], and no relative markdown links outside the catalogue index files.
4. Every _source-text/ and _research/ path cited in a numbered file exists.
5. Every numbered file has a hook in index.md.

Exit status is 1 if any enforced check fails. A check listed in REPORT_ONLY
still prints its failures but does not fail the run, unless --strict is given.
"""

import argparse
import glob
import os
import re
import sys

# TODO: checks 2 and 4 fail on main today (a cross-ref to a 00c file that
# doesn't exist; two _research/_synthesis/ paths whose files moved to
# _research/_archive/). They print their failures but don't fail the run until
# a separate maintenance PR fixes the content. Then remove the number here so
# the check starts failing PRs. --strict ignores this set.
REPORT_ONLY = {2, 4}

NUMBERED = re.compile(r"^(\d\d[a-z]?)-[a-z0-9-]+\.md$")
FRONTMATTER_KEYS = ("type", "title", "description", "tags", "timestamp")
# Catalogue index files may use relative markdown links (check 3).
CATALOGUE_INDEXES = {"index.md", "components/index.md", "patterns/index.md"}
# Vault prose beyond the numbered files that checks 2 and 3 also read.
EXTRA_GLOBS = ("index.md", "GLOSSARY.md", "components/*.md", "patterns/*.md")

FENCE = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")
SEE_GROUP = re.compile(r"\(([^()]*)\)")
SEE_WORD = re.compile(r"\bsee\b", re.I)
SLUG_REF = re.compile(r"(?<![\w/.-])(\d\d[a-z]?-[a-z][a-z0-9-]*[a-z0-9])(?:\.md)?(?![\w/-])")
WIKILINK = re.compile(r"\[\[[^\]]*\]\]")
MD_LINK = re.compile(r"\]\(([^)\s]+)[^)]*\)")
ABSOLUTE = re.compile(r"^([a-z][a-z0-9+.-]*:|#)", re.I)
CITED_PATH = re.compile(r"(?<![\w/])((?:_source-text|_research)/[^\s`'\"()\[\]<>,;]*)")


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return f.read()


def numbered_files(root):
    return sorted(n for n in os.listdir(root) if NUMBERED.match(n))


def prose_files(root):
    files = set(numbered_files(root))
    for pattern in EXTRA_GLOBS:
        for path in glob.glob(os.path.join(root, pattern)):
            files.add(os.path.relpath(path, root).replace(os.sep, "/"))
    return sorted(files)


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
            keys = {ln.split(":", 1)[0].strip() for ln in m.group(1).splitlines()
                    if re.match(r"^[A-Za-z_][\w-]*\s*:", ln)}
            missing = [k for k in FRONTMATTER_KEYS if k not in keys]
            if missing:
                errors.append(f"{name}: frontmatter missing {', '.join(missing)}")
            body = text[m.end():]
        h1 = re.search(r"^# .*$", body, re.M)
        if not h1:
            errors.append(f"{name}: no H1")
        elif not re.match(rf"^# {re.escape(prefix)} — \S", h1.group(0)):
            errors.append(f"{name}: H1 is '{h1.group(0)}', expected '# {prefix} — Title'")
    return errors


def check_see_refs(root):
    stems = {n[:-3] for n in numbered_files(root)}
    errors = []
    for rel in prose_files(root):
        text = FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), read(root, rel))
        for group in SEE_GROUP.finditer(text):
            see = SEE_WORD.search(group.group(1))
            if not see:
                continue
            tail = group.group(1)[see.start():]
            for ref in SLUG_REF.finditer(tail):
                if ref.group(1) not in stems:
                    ln = line_of(text, group.start())
                    errors.append(f"{rel}:{ln}: cross-ref '{ref.group(1)}' names no numbered file")
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
    (2, "(See NN-...) cross-refs resolve", check_see_refs),
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
