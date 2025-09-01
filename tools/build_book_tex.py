#!/usr/bin/env python3
r"""
Build a single, printable book PDF from all chapter/section Markdown files
without modifying any .md. Uses Pandoc + XeLaTeX with latex/preamble.tex.

- Orders files by chapter then section.
- Inserts "# Chapter N" and "## Section N.M" headings.
- Removes each file's first H1 and demotes inner headings (so only Chapter/Section
  appear in the ToC).
- Short ToC (chapter + section only).
"""

from __future__ import annotations
import argparse, subprocess, sys, shutil, re, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"

FRONT_RE    = re.compile(r"^---\n(.*?)\n---\n", re.S)
ATX_H1_RE   = re.compile(r"^\s*#\s+.*?$", re.M)
ATX_HEAD_RE = re.compile(r"^(?P<Hashes>#{1,6})(?P<Space>\s+)(?P<Text>.+)$", re.M)
SEC_RE      = re.compile(r"^section-(\d+)(?:\.(\d+))?\.md$", re.I)
CHP_RE      = re.compile(r"^chapter\D*(\d+)$", re.I)

def die(msg: str):
    print(msg, file=sys.stderr); sys.exit(1)

def ensure_tools():
    if shutil.which("pandoc") is None:
        die("ERROR: pandoc not found on PATH.")
    if shutil.which("xelatex") is None:
        die("ERROR: xelatex not found on PATH (install MiKTeX/TeX Live).")

def parse_ch_num(name: str) -> int:
    m = CHP_RE.match(name); return int(m.group(1)) if m else 10**6

def parse_sec_num(name: str) -> tuple[int,int]:
    m = SEC_RE.match(name)
    return (int(m.group(1)), int(m.group(2) or 0)) if m else (10**6, 10**6)

def sec_label(name: str) -> str:
    m = SEC_RE.match(name)
    return f"{m.group(1)}.{m.group(2)}" if (m and m.group(2) is not None) else (m.group(1) if m else name)

def strip_frontmatter(s: str) -> str:
    m = FRONT_RE.match(s); return s[m.end():] if m else s

def remove_first_h1(s: str) -> str:
    m = ATX_H1_RE.search(s)
    if not m: return s
    end = m.end()
    while end < len(s) and s[end] in "\r\n": end += 1
    return s[end:].lstrip()

def demote_internal_headings(s: str, by: int = 1) -> str:
    # demote ##..###### by one level so book H1/H2 dominate
    def repl(m: re.Match) -> str:
        hashes = m.group("Hashes")
        if len(hashes) >= 2:
            new = min(6, len(hashes) + by)
            return "#" * new + m.group("Space") + m.group("Text")
        return m.group(0)
    return ATX_HEAD_RE.sub(repl, s)

def collect_sections() -> list[tuple[int, Path]]:
    items: list[tuple[int, Path]] = []
    for ch in sorted([d for d in CHAPTERS_DIR.iterdir() if d.is_dir()], key=lambda p: parse_ch_num(p.name)):
        files = sorted([f for f in ch.iterdir() if f.is_file() and SEC_RE.match(f.name)],
                       key=lambda f: parse_sec_num(f.name))
        for f in files:
            items.append((parse_ch_num(ch.name), f))
    return items

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="pdf/book/arm-assembly-mazidi-solutions-xelatex.pdf",
                    help="Output PDF path")
    ap.add_argument("--title", default="ARM Mazidi Solutions — All Sections")
    ap.add_argument("--toc", action="store_true", help="Include ToC (chapter + section)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    ensure_tools()

    preamble = ROOT / "latex/preamble.tex"
    if not preamble.exists():
        die("Missing latex/preamble.tex")

    sections = collect_sections()
    if not sections:
        die("No section files found under chapters/**/section-*.md")

    out_pdf = (ROOT / args.out).resolve()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Build one temporary combined Markdown
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        combined = td / "book.md"
        parts: list[str] = []

        # Metadata (no date)
        parts.append("---\n")
        parts.append(f'title: "{args.title}"\n')
        parts.append("...\n\n")

        last_ch = None
        for ch_num, f in sections:
            # Chapter page break & heading
            if ch_num != last_ch:
                if last_ch is not None:
                    parts.append("\n\\newpage\n\n")
                parts.append(f"# Chapter {ch_num}\n\n")
                last_ch = ch_num

            # Section page break & heading
            parts.append("\n\\newpage\n\n")
            parts.append(f"## Section {sec_label(f.name)}\n\n")

            raw = f.read_text(encoding="utf-8", errors="ignore")
            raw = strip_frontmatter(raw)
            raw = remove_first_h1(raw)
            raw = demote_internal_headings(raw, by=1)
            parts.append(raw.rstrip() + "\n")

            if args.verbose:
                print(f"[add] Chapter {ch_num} :: {f.relative_to(ROOT)}")

        combined.write_text("".join(parts), encoding="utf-8")

        # Pandoc → XeLaTeX
        cmd = [
            "pandoc", str(combined),
            "--from", "markdown+pipe_tables+table_captions+fenced_code_blocks+fenced_divs+link_attributes",
            "--pdf-engine", "xelatex",
            "-H", str(preamble),                       # include our preamble (defines geometry, \tightlist, fonts, listings)
            "-V", "documentclass=report",              # chapters available
            "--top-level-division=chapter",            # map H1 -> \chapter, H2 -> \section
            "-V", f"title={args.title}",
            "-V", "author=arm-assembly-mazidi-solutions",
            "-V", "date=",                             # drop date
            "-V", "colorlinks=false",
            "-V", "linkcolor=black",
            "-V", "urlcolor=black",
            "-V", "citecolor=black",
            "-o", str(out_pdf),
        ]
        if args.toc:
            cmd += ["--toc", "--toc-depth=2"]          # chapter + section only

        print(f"[book-xelatex] {out_pdf.relative_to(ROOT)}")
        rc = subprocess.run(cmd).returncode
        if rc != 0:
            die("Pandoc/XeLaTeX failed while building the book.")
    print("Done.")

if __name__ == "__main__":
    main()
