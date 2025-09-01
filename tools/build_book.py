#!/usr/bin/env python3
"""
Build a single printable 'book' PDF from all sections with a short TOC.

- TOC shows only "Chapter N" and "Section N.M".
- Per section: drop its top H1, demote internal headings so they don't show in TOC.
- Preserves your CSS (same look as individual PDFs), repo-slug header/footer.
"""

from __future__ import annotations
import argparse, os, platform, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"

# ---------- regex helpers ----------
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)          # YAML front matter
ATX_H1_RE = re.compile(r"^\s*#\s+.*?$", re.M)              # first-level ATX heading
ATX_HEAD_RE = re.compile(r"^(?P<Hashes>#{1,6})(?P<Space>\s+)(?P<Text>.+)$", re.M)

SEC_RE = re.compile(r"^section-(\d+)(?:\.(\d+))?\.md$", re.I)
CHP_RE = re.compile(r"^chapter\D*(\d+)$", re.I)

def strip_frontmatter(text: str) -> str:
    m = FRONT_RE.match(text)
    return text[m.end():] if m else text

def remove_first_h1(text: str) -> str:
    """
    Remove the first ATX H1 and any immediate blank lines after it.
    (We insert our own compact 'Section N.M' H2 for the book TOC.)
    """
    m = ATX_H1_RE.search(text)
    if not m:
        return text
    end = m.end()
    # also remove following empty lines
    while end < len(text) and text[end] in "\r\n":
        end += 1
    return text[end:].lstrip()

def demote_internal_headings(text: str, by: int = 1) -> str:
    """
    Demote headings inside the section so they do not compete with the book's H1/H2.
    - We demote level-2+ headings by 'by' levels (cap at 6).
    - H1 is assumed removed already.
    """
    def _repl(m: re.Match) -> str:
        hashes = m.group("Hashes")
        if len(hashes) >= 2:  # only demote ## and deeper
            new_level = min(6, len(hashes) + by)
            return "#" * new_level + m.group("Space") + m.group("Text")
        else:
            return m.group(0)
    return ATX_HEAD_RE.sub(_repl, text)

def parse_chapter_num(folder_name: str) -> int:
    m = CHP_RE.match(folder_name)
    return int(m.group(1)) if m else 10**6  # unknown to end

def parse_section_num(file_name: str) -> tuple[int, int]:
    m = SEC_RE.match(file_name)
    if not m:
        return (10**6, 10**6)
    a = int(m.group(1))
    b = int(m.group(2) or 0)
    return (a, b)

def section_label_from_name(name: str) -> str:
    """'section-2.3.md' -> '2.3'  |  'section-3.md' -> '3'"""
    m = SEC_RE.match(name)
    if not m:
        return name
    a = m.group(1)
    b = m.group(2)
    return f"{a}.{b}" if b is not None else a

def file_uri(p: Path) -> str:
    return "file:///" + str(p.resolve()).replace("\\", "/")

# ---------- tool discovery (Windows-hardened) ----------
def locate_exe(name: str, win_hints: list[str] | None = None) -> str:
    p = shutil.which(name)
    if p:
        p = str(Path(p).resolve())
    if platform.system() == "Windows":
        hints = win_hints or []
        if name.lower() == "pandoc":
            hints.append(r"C:\Program Files\Pandoc\pandoc.exe")
        if name.lower() == "wkhtmltopdf":
            hints.append(r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        # Prefer Program Files over AppData shims
        for h in hints:
            if Path(h).exists():
                if (not p) or ("AppData\\Local\\pandoc" in p) or ("\\WindowsApps\\" in p):
                    return h
        return p or next((h for h in hints if Path(h).exists()), "")
    return p or ""

def ensure_tools() -> tuple[str, str, dict]:
    pandoc = locate_exe("pandoc")
    wkhtml = locate_exe("wkhtmltopdf")
    if not pandoc:
        sys.exit("ERROR: pandoc not found.")
    if not wkhtml:
        sys.exit("ERROR: wkhtmltopdf not found.")
    env = os.environ.copy()
    pf_pandoc = str(Path(pandoc).parent)
    pf_wk = str(Path(wkhtml).parent)
    env["PATH"] = os.pathsep.join([pf_pandoc, pf_wk] + env.get("PATH","").split(os.pathsep))
    return pandoc, wkhtml, env

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description="Concatenate all sections into one printable PDF with a short TOC.")
    ap.add_argument("--css", default="docs/styles/print-friendly.css", help="CSS file (same one you use for sections).")
    ap.add_argument("--header-template", default="docs/header.tpl.html")
    ap.add_argument("--footer-template", default="docs/footer.tpl.html")
    ap.add_argument("--out", default="pdf/book/arm-assembly-mazidi-solutions.pdf")
    ap.add_argument("--title", default="ARM Mazidi Solutions — All Sections")
    ap.add_argument("--toc", action="store_true", help="Add a short TOC (Chapter/Section only).")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    pandoc, wkhtml, env = ensure_tools()

    # gather chapters in numeric order
    chapters = sorted(
        [d for d in CHAPTERS_DIR.iterdir() if d.is_dir()],
        key=lambda p: parse_chapter_num(p.name)
    )

    # for each chapter, gather section files in numeric order
    chapter_sections: list[tuple[int, list[Path]]] = []
    for ch in chapters:
        ch_num = parse_chapter_num(ch.name)
        files = sorted(
            [f for f in ch.iterdir() if f.is_file() and SEC_RE.match(f.name)],
            key=lambda f: parse_section_num(f.name)
        )
        if files:
            chapter_sections.append((ch_num, files))

    if not chapter_sections:
        sys.exit("No sections found under chapters/**/section-*.md")

    out_pdf = (ROOT / args.out).resolve()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    css_path = (ROOT / args.css).resolve()
    header_tpl = (ROOT / args.header_template).resolve()
    footer_tpl = (ROOT / args.footer_template).resolve()

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        combined_md = td / "book.md"

        parts: list[str] = []

        # Minimal metadata (no date)
        parts.append("---\n")
        parts.append(f'title: "{args.title}"\n')
        parts.append("...\n\n")

        # Title page
        parts.append(f"# {args.title}\n\n")

        # Build content: Chapter H1 + Section H2, then demoted section content
        first_chapter = True
        for ch_num, files in chapter_sections:
            # page break before every chapter except the very first
            if not first_chapter:
                parts.append('\n<div style="page-break-before: always;"></div>\n\n')
            first_chapter = False

            # Chapter heading (H1) — shows in TOC
            parts.append(f"# Chapter {ch_num}\n\n")

            for i, f in enumerate(files):
                # section label from filename only (short TOC)
                s_label = section_label_from_name(f.name)
                # page break before every section
                parts.append('\n<div style="page-break-before: always;"></div>\n\n')
                # Section heading (H2) — shows in TOC
                parts.append(f"## Section {s_label}\n\n")

                # content processing
                raw = f.read_text(encoding="utf-8", errors="ignore")
                raw = strip_frontmatter(raw)
                raw = remove_first_h1(raw)     # drop file's own big title
                raw = demote_internal_headings(raw, by=1)  # ## -> ###, etc.
                parts.append(raw.rstrip() + "\n")

                if args.verbose:
                    print(f"[add] Ch {ch_num}  {f.relative_to(ROOT)}  -> Section {s_label}")

        combined_md.write_text("".join(parts), encoding="utf-8")

        # Pandoc → single PDF via wkhtmltopdf
        cmd = [
            str(pandoc), str(combined_md),
            "-o", str(out_pdf),
            "--from", "gfm",
            "--metadata", f"title={args.title}",
            "--pdf-engine=wkhtmltopdf",
            "--pdf-engine-opt", "--enable-local-file-access",
            "--pdf-engine-opt", "--print-media-type",
            "-c", file_uri(css_path),
            "--pdf-engine-opt", "--header-html", "--pdf-engine-opt", file_uri(header_tpl),
            "--pdf-engine-opt", "--footer-html", "--pdf-engine-opt", file_uri(footer_tpl),
            "--pdf-engine-opt","--margin-top","--pdf-engine-opt","14mm",
            "--pdf-engine-opt","--margin-bottom","--pdf-engine-opt","10mm",
            "--pdf-engine-opt","--margin-left","--pdf-engine-opt","14mm",
            "--pdf-engine-opt","--margin-right","--pdf-engine-opt","14mm",
        ]
        if args.toc:
            # Short TOC: Chapters (H1) + Sections (H2)
            cmd += ["--toc", "--toc-depth=2"]

        print(f"[book] {out_pdf.relative_to(ROOT)}")
        rc = subprocess.run(cmd, env=env).returncode
        if rc != 0:
            sys.exit("Pandoc failed while building the book PDF.")

    print("Done.")

if __name__ == "__main__":
    main()
