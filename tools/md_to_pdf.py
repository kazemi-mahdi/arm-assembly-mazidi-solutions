#!/usr/bin/env python3
"""
Pandoc-based converter: turn Markdown section files into styled PDFs.

- Mirrors layout: chapters/**/section-*.md -> pdf/chapters/**/section-*.pdf
- Or convert only some files: --files path1.md path2.md ...
- Uses CSS + header/footer (wkhtmltopdf) or XeLaTeX if you prefer.
- Windows-hardened: prefers real Program Files installs over stale shims.
"""
from __future__ import annotations
import argparse, subprocess, sys, shutil, re, tempfile, os, platform
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = "chapters/**/section-*.md"

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
H1_RE = re.compile(r"^\s*#\s+(.*)$", re.M)

def file_uri(p: Path) -> str:
    """Absolute file:/// URI (wkhtmltopdf needs a scheme for local files)."""
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

def needs_build(pdf: Path, sources: list[Path]) -> bool:
    """Rebuild if PDF doesn't exist or any source (md/css/templates) is newer."""
    if not pdf.exists():
        return True
    pdf_mtime = pdf.stat().st_mtime
    for s in sources:
        if s and s.exists() and s.stat().st_mtime > pdf_mtime:
            return True
    return False

def locate_exe(name: str, win_hints: list[str] | None = None) -> str:
    """
    Robustly find an executable. On Windows, prefer Program Files locations
    over AppData shims if both exist.
    """
    p = shutil.which(name)
    if p:
        p = str(Path(p).resolve())
    if platform.system() == "Windows":
        # Prefer Program Files paths if present
        candidates = []
        if win_hints:
            candidates += win_hints
        # Default hints
        if name.lower() == "pandoc":
            candidates.append(r"C:\Program Files\Pandoc\pandoc.exe")
        if name.lower() == "wkhtmltopdf":
            candidates.append(r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

        for c in candidates:
            if Path(c).exists():
                # If which() returned an AppData shim, override it
                if (not p) or ("AppData\\Local\\pandoc" in p) or ("\\WindowsApps\\" in p):
                    return c
        if p:
            return p
        # Fall through: try candidates anyway
        for c in candidates:
            if Path(c).exists():
                return c
        return ""  # not found
    else:
        return p or ""

def ensure_tools(engine: str) -> tuple[str, str | None, dict]:
    """
    Return (pandoc_cmd, wkhtmltopdf_cmd_or_None, base_env) or exit with message.
    Ensures PATH for subprocess prefers real installs.
    """
    pandoc_cmd = locate_exe("pandoc")
    if not pandoc_cmd or not Path(pandoc_cmd).exists():
        sys.exit("ERROR: pandoc not found. Install pandoc, or add it to PATH.")

    wk_cmd = None
    env = os.environ.copy()

    if engine == "wkhtmltopdf":
        wk_cmd = locate_exe("wkhtmltopdf")
        if not wk_cmd or not Path(wk_cmd).exists():
            sys.exit("ERROR: wkhtmltopdf not found. Install it or use --engine xelatex.")
        # Prepend folders to PATH so pandoc finds the right binaries
        path_parts = env.get("PATH", "").split(os.pathsep)
        pf_pandoc = str(Path(pandoc_cmd).parent)
        pf_wk = str(Path(wk_cmd).parent)
        # put Program Files paths first
        new_path = os.pathsep.join([pf_pandoc, pf_wk] + [p for p in path_parts if p not in (pf_pandoc, pf_wk)])
        env["PATH"] = new_path
    else:
        # XeLaTeX required
        xel = locate_exe("xelatex", win_hints=[r"C:\Program Files\MiKTeX\miktex\bin\x64\xelatex.exe"])
        if not xel or not Path(xel).exists():
            sys.exit("ERROR: xelatex not found. Install MiKTeX/TeX Live or use --engine wkhtmltopdf.")
        pf_pandoc = str(Path(pandoc_cmd).parent)
        pf_xel = str(Path(xel).parent)
        new_path = os.pathsep.join([pf_pandoc, pf_xel] + env.get("PATH","").split(os.pathsep))
        env["PATH"] = new_path

    return pandoc_cmd, wk_cmd, env

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="*", help="specific Markdown files to convert")
    ap.add_argument("--glob", default=DEFAULT_GLOB, help="glob used when --files is missing")
    ap.add_argument("--out", default="pdf", help="output root directory")
    ap.add_argument("--engine", default="wkhtmltopdf", choices=["wkhtmltopdf","xelatex"])
    ap.add_argument("--css", default="docs/pdf.css")
    ap.add_argument("--header-template", default="docs/header.tpl.html")
    ap.add_argument("--footer-template", default="docs/footer.tpl.html")
    # ap.add_argument("--project", default="ARM Mazidi Solutions")
    ap.add_argument("--project", default="arm-assembly-mazidi-solutions")
    ap.add_argument("--toc", action="store_true")
    ap.add_argument("--force", action="store_true", help="rebuild even if PDF appears up-to-date")
    ap.add_argument("--fail-fast", action="store_true")
    args = ap.parse_args()

    pandoc_cmd, wk_cmd, base_env = ensure_tools(args.engine)

    out_root = (ROOT / args.out).resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    md_files = [Path(f).resolve() for f in args.files] if args.files else \
               [p for p in ROOT.glob(args.glob) if p.is_file()]
    md_files = sorted(md_files)

    css_path = (ROOT / args.css) if args.css else None
    header_tpl = (ROOT / args.header_template)
    footer_tpl = (ROOT / args.footer_template)

    built = skipped = failed = 0

    for md in md_files:
        rel = md.relative_to(ROOT)
        out_dir = out_root / rel.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = out_dir / (md.stem + ".pdf")

        deps = [md]
        if args.engine == "wkhtmltopdf":
            if css_path: deps.append(css_path)
            deps.extend([header_tpl, footer_tpl])

        if not args.force and not needs_build(pdf_path, deps):
            print(f"[skip] {rel} (up-to-date)")
            skipped += 1
            continue

        text = md.read_text(encoding="utf-8", errors="ignore")
        meta = parse_frontmatter(text)
        title = guess_title(md, text, meta)

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            hp = td / "header.html"
            fp = td / "footer.html"
            # build per-file header/footer
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
            #prints date in header
            # cmd = [pandoc_cmd, str(md), "-o", str(pdf_path), "--from", "gfm",
            #        "--metadata", f"title={title}",
            #        "--metadata", f"date={datetime.today():%Y-%m-%d}"]
            cmd = [pandoc_cmd, str(md), "-o", str(pdf_path), "--from", "gfm",
                    "--metadata", f"title={title}"]
            if args.toc:
                cmd += ["--toc", "--toc-depth=3"]

            if args.engine == "wkhtmltopdf":
                cmd += ["--pdf-engine=wkhtmltopdf"]
                # allow local files & honor print CSS
                cmd += ["--pdf-engine-opt", "--enable-local-file-access",
                        "--pdf-engine-opt", "--print-media-type"]
                # use absolute file:/// URIs
                if css_path and css_path.exists():
                    cmd += ["-c", file_uri(css_path)]
                cmd += ["--pdf-engine-opt", "--header-html", "--pdf-engine-opt", file_uri(hp),
                        "--pdf-engine-opt", "--footer-html", "--pdf-engine-opt", file_uri(fp)]
                # ONE set of margins (same unit)
                cmd += [
                    "--pdf-engine-opt","--margin-top","--pdf-engine-opt","14mm",
                    "--pdf-engine-opt","--margin-bottom","--pdf-engine-opt","10mm",
                    "--pdf-engine-opt","--margin-left","--pdf-engine-opt","14mm",
                    "--pdf-engine-opt","--margin-right","--pdf-engine-opt","14mm",
                ]
            else:
                cmd += ["--pdf-engine=xelatex",
                        "-V","mainfont=DejaVu Serif",
                        "-V","monofont=DejaVu Sans Mono",
                        "-V","geometry:margin=1in"]

            print(f"[build] {rel} → {pdf_path.relative_to(ROOT)}")
            rc = subprocess.run(cmd, env=base_env).returncode
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
