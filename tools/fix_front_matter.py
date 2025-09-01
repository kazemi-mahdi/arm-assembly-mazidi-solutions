#!/usr/bin/env python3
"""
Normalize/add front-matter to all chapters/**/section-*.md

- Adds missing YAML front-matter.
- Fills/normalizes keys: chapter, section, file_role, title, notes, last_updated.
- Leaves existing body intact.
- Idempotent: safe to run multiple times.

Usage:
  python tools/fix_front_matter.py            # modify files in place
  python tools/fix_front_matter.py --dry-run  # show planned changes only
"""
from __future__ import annotations
import argparse, datetime, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root (assumes tools/..)
TODAY = datetime.date.today().isoformat()

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
H1_RE = re.compile(r"^\s*#\s+(.*)$", re.M)
SEC_RE = re.compile(r"section-([0-9]+(?:\.[0-9]+)?)\.md$", re.I)
CH_DIR_RE = re.compile(r"chapter[\s_-]*0*([0-9]+)$", re.I)
CH_ANY_RE = re.compile(r"ch(?:apter)?[\s_-]*0*([0-9]+)", re.I)

def infer_section_from_filename(p: Path) -> str | None:
    m = SEC_RE.search(p.name)
    return m.group(1) if m else None

def infer_chapter_from_path(p: Path) -> str | None:
    # Prefer parent dir like "chapter 03", else any "ch04-*" higher up
    for parent in [p.parent, *p.parents]:
        m = CH_DIR_RE.match(parent.name)
        if m:
            return str(int(m.group(1)))  # normalize to no leading zeros
        m2 = CH_ANY_RE.match(parent.name)
        if m2:
            return str(int(m2.group(1)))
    # Fallback: take integer part of section (e.g., "3.2" -> "3")
    sec = infer_section_from_filename(p)
    if sec and sec.split(".")[0].isdigit():
        return sec.split(".")[0]
    return None

def parse_frontmatter(text: str) -> tuple[dict, str, str]:
    """Return (meta_dict, body, raw_front)"""
    m = FRONT_RE.match(text)
    if not m:
        return {}, text, ""
    raw = m.group(1)
    body = text[m.end():]
    meta = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):  # allow comments
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"')
        meta[k] = v
    return meta, body, raw

def make_title(meta: dict, section: str, body: str) -> str:
    # If existing title present and not empty, keep it.
    t = meta.get("title", "").strip()
    if t:
        return t
    # Try to borrow the first H1 heading line if it exists.
    m = H1_RE.search(body)
    if m:
        guessed = m.group(1).strip()
        # Avoid echoing a giant heading; use if it contains "Section".
        if "Section" in guessed:
            return guessed
    # Fallback generic title
    return f"Section {section} — Exercises (Mazidi)"

def build_frontmatter(chapter: str, section: str, meta: dict, body: str) -> str:
    # Preserve existing notes if any
    notes = meta.get("notes", f"See Mazidi, Ch. {chapter} section {section}.")
    title = make_title(meta, section, body)
    file_role = 'Solutions'
    # Always refresh last_updated; keep chapter/section normalized
    lines = [
        "---",
        f"chapter: {chapter}",
        f'section: "{section}"',
        f'file_role: "{file_role}"',
        f'title: "{title}"',
        f'notes: "{notes}"',
        f"last_updated: {TODAY}",
        "---",
        "",
    ]
    return "\n".join(lines)

def process_file(md: Path, dry_run=False) -> bool:
    text = md.read_text(encoding="utf-8")
    meta, body, raw = parse_frontmatter(text)
    section = infer_section_from_filename(md)
    chapter = infer_chapter_from_path(md)

    if not section or not chapter:
        print(f"[skip] {md} (couldn't infer chapter/section)")
        return False

    new_front = build_frontmatter(chapter, section, meta, body)
    if raw:
        # Replace existing front-matter wholesale
        new_text = FRONT_RE.sub(new_front, text, count=1)
    else:
        new_text = new_front + text

    if new_text != text:
        rel = md.relative_to(ROOT)
        if dry_run:
            print(f"[dry-run] would update: {rel}")
        else:
            md.write_text(new_text, encoding="utf-8")
            print(f"[fix] {rel}")
        return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="show changes without writing")
    ap.add_argument("--glob", default="chapters/**/section-*.md", help="file glob to scan")
    args = ap.parse_args()

    changed = 0
    for md in sorted(ROOT.glob(args.glob)):
        if md.is_file():
            changed += process_file(md, dry_run=args.dry_run)
    print(f"Done. Files changed: {changed}")

if __name__ == "__main__":
    sys.exit(main())
