#!/usr/bin/env python3
"""
Pandoc-based converter: turn Markdown section files into styled PDFs.

- Mirrors layout: chapters/**/section-*.md -> pdf/chapters/**/section-*.pdf
- Or convert only some files: --files path1.md path2.md ...
- Uses CSS + header/footer (wkhtmltopdf) or XeLaTeX if you prefer.
"""
from __future__ import annotations
import argparse, subprocess, sys, shutil, re, tempfile
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = "chapters/**/section-*.md"

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
H1_RE = re.compile(r"^\s*#\s+(.*)$", re.M)
def file_uri(p: Path) -> str:
    # absolute file:/// URI (wkhtmltopdf needs a scheme for local files)
    return "file:///" + str(p.resolve()).replace("\\", "/")

def parse_frontmatter(text: str) -> dict:
    m = FRONT_RE.match(text)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta

def guess_title(md_path: Path, text: str, meta: dict) -> str:
    if meta.get("title"):
        return meta["title"]
    m = H1_RE.search(text)
    return m.group(1).strip() if m else md_path.stem.replace("-", " ").title()

def newer(src: Path, dst: Path) -> bool:
    return (not dst.exists()) or (src.stat().st_mtime > dst.stat().st_mtime)

def ensure_tools(engine: str):
    if shutil.which("pandoc") is None:
        sys.exit("ERROR: pandoc not found. Install pandoc.")
    if engine == "wkhtmltopdf" and shutil.which("wkhtmltopdf") is None:
        sys.exit("ERROR: wkhtmltopdf not found. Install it or use --engine xelatex.")
    if engine == "xelatex" and shutil.which("xelatex") is None:
        sys.exit("ERROR: xelatex not found. Install TeX Live xetex or use wkhtmltopdf.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="*", help="specific Markdown files to convert")
    ap.add_argument("--glob", default=DEFAULT_GLOB, help="glob used when --files is missing")
    ap.add_argument("--out", default="pdf", help="output root directory")
    ap.add_argument("--engine", default="wkhtmltopdf", choices=["wkhtmltopdf","xelatex"])
    ap.add_argument("--css", default="docs/pdf.css")
    ap.add_argument("--header-template", default="docs/header.tpl.html")
    ap.add_argument("--footer-template", default="docs/footer.tpl.html")
    ap.add_argument("--project", default="ARM Mazidi Solutions")
    ap.add_argument("--toc", action="store_true")
    ap.add_argument("--fail-fast", action="store_true")
    args = ap.parse_args()

    ensure_tools(args.engine)

    out_root = (ROOT / args.out).resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    md_files = [Path(f).resolve() for f in args.files] if args.files else \
               [p for p in ROOT.glob(args.glob) if p.is_file()]

    css_path = (ROOT / args.css) if args.css else None
    header_tpl = (ROOT / args.header_template)
    footer_tpl = (ROOT / args.footer_template)

    built = skipped = failed = 0

    for md in sorted(md_files):
        rel = md.relative_to(ROOT)
        out_dir = out_root / rel.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = out_dir / (md.stem + ".pdf")

        if not newer(md, pdf_path):
            print(f"[skip] {rel} (up-to-date)")
            skipped += 1
            continue

        text = md.read_text(encoding="utf-8", errors="ignore")
        meta = parse_frontmatter(text)
        title = guess_title(md, text, meta)

        # Build header/footer on the fly for this file
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            hp = td / "header.html"
            fp = td / "footer.html"
            hp.write_text(
                header_tpl.read_text(encoding="utf-8")
                .replace("{{PROJECT}}", args.project)
                .replace("{{TITLE}}", title),
                encoding="utf-8"
            )
            fp.write_text(
                footer_tpl.read_text(encoding="utf-8")
                .replace("{{PROJECT}}", args.project)
                .replace("{{TITLE}}", title),
                encoding="utf-8"
            )

            cmd = ["pandoc", str(md), "-o", str(pdf_path), "--from", "gfm",
                   "--metadata", f"title={title}",
                   "--metadata", f"date={datetime.today():%Y-%m-%d}"]
            if args.toc:
                cmd += ["--toc", "--toc-depth=3"]
            #######################
            if args.engine == "wkhtmltopdf":
                cmd += ["--pdf-engine=wkhtmltopdf"]

                # Allow local files (CSS, header/footer, images) to load
                cmd += ["--pdf-engine-opt", "--enable-local-file-access"]

                # Use absolute file:/// for CSS so wkhtmltopdf has a scheme
                if css_path and css_path.exists():
                    cmd += ["-c", file_uri(css_path)]

                # header/footer: use file:/// URIs as well
                cmd += ["--pdf-engine-opt", "--header-html", "--pdf-engine-opt", file_uri(hp)]
                cmd += ["--pdf-engine-opt", "--footer-html", "--pdf-engine-opt", file_uri(fp)]

                # Set ALL margins with the SAME unit
                cmd += [
                    "--pdf-engine-opt","--margin-top","--pdf-engine-opt","20mm",
                    "--pdf-engine-opt","--margin-bottom","--pdf-engine-opt","15mm",
                    "--pdf-engine-opt","--margin-left","--pdf-engine-opt","18mm",
                    "--pdf-engine-opt","--margin-right","--pdf-engine-opt","18mm",
                ]
            else:
                # xelatex route unchanged…
                cmd += ["--pdf-engine=xelatex",
                        "-V","mainfont=DejaVu Serif",
                        "-V","monofont=DejaVu Sans Mono",
                        "-V","geometry:margin=1in"]
            # if args.engine == "wkhtmltopdf":
            #     cmd += ["--pdf-engine=wkhtmltopdf"]
            #     if css_path and css_path.exists():
            #         cmd += ["-c", str(css_path)]
            #     # pass wkhtmltopdf options via --pdf-engine-opt
            #     cmd += ["--pdf-engine-opt","--header-html","--pdf-engine-opt",str(hp),
            #             "--pdf-engine-opt","--footer-html","--pdf-engine-opt",str(fp),
            #             "--pdf-engine-opt","--margin-top","--pdf-engine-opt","20mm",
            #             "--pdf-engine-opt","--margin-bottom","--pdf-engine-opt","15mm"]
            # else:
            #     cmd += ["--pdf-engine=xelatex",
            #             "-V","mainfont=DejaVu Serif",
            #             "-V","monofont=DejaVu Sans Mono",
            #             "-V","geometry:margin=1in"]

            print(f"[build] {rel} → {pdf_path.relative_to(ROOT)}")
            rc = subprocess.run(cmd).returncode
            if rc != 0:
                print(f"[error] pandoc failed for {rel}", file=sys.stderr)
                failed += 1
                if args.fail_fast:
                    sys.exit(rc)
            else:
                built += 1

    print(f"\nDone. OK: {built}, skipped: {skipped}, errors: {failed}")
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
