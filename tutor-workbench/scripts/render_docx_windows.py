"""Render DOCX files reliably on Windows, including Chinese paths.

The renderer stages input/output in an ASCII-only temporary directory, uses a
valid file:/// URI for LibreOffice's isolated profile, and falls back to local
Microsoft Word when LibreOffice conversion genuinely fails.
"""

from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def find_soffice() -> Path | None:
    candidates = [
        shutil.which("soffice.com"),
        shutil.which("soffice.exe"),
        r"C:\Program Files\LibreOffice\program\soffice.com",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.com",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    return None


def find_pdftoppm() -> Path | None:
    direct = shutil.which("pdftoppm.exe")
    if direct and Path(direct).is_file():
        return Path(direct)
    runtime_root = Path.home() / ".cache" / "codex-runtimes"
    matches = list(runtime_root.glob("**/native/poppler/Library/bin/pdftoppm.exe"))
    return matches[0] if matches else None


def run_quiet(command: list[str]) -> subprocess.CompletedProcess[str]:
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    return subprocess.run(
        command,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=flags,
        check=False,
    )


def libreoffice_to_pdf(docx: Path, pdf_dir: Path, profile_dir: Path) -> tuple[Path | None, str]:
    soffice = find_soffice()
    if not soffice:
        return None, "LibreOffice not found"
    profile_dir.mkdir(parents=True, exist_ok=True)
    profile_uri = profile_dir.resolve().as_uri()
    result = run_quiet([
        str(soffice),
        f"-env:UserInstallation={profile_uri}",
        "--invisible",
        "--headless",
        "--norestore",
        "--convert-to",
        "pdf",
        "--outdir",
        str(pdf_dir),
        str(docx),
    ])
    pdf = pdf_dir / f"{docx.stem}.pdf"
    log = f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    if result.returncode == 0 and pdf.is_file() and pdf.stat().st_size > 0:
        return pdf, log
    return None, f"exit={result.returncode}\n{log}"


def word_to_pdf(docx: Path, pdf: Path) -> tuple[Path | None, str]:
    ps = f"""
$ErrorActionPreference='Stop'
$word=New-Object -ComObject Word.Application
$word.Visible=$false
try {{
  $doc=$word.Documents.Open('{str(docx).replace("'", "''")}',$false,$true)
  $doc.ExportAsFixedFormat('{str(pdf).replace("'", "''")}',17)
  $doc.Close($false)
}} finally {{ $word.Quit() }}
"""
    encoded = base64.b64encode(ps.encode("utf-16le")).decode("ascii")
    result = run_quiet(["powershell.exe", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded])
    log = f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    if result.returncode == 0 and pdf.is_file() and pdf.stat().st_size > 0:
        return pdf, log
    return None, f"exit={result.returncode}\n{log}"


def rasterize(pdf: Path, output_dir: Path, dpi: int) -> list[Path]:
    pdftoppm = find_pdftoppm()
    if not pdftoppm:
        raise RuntimeError("pdftoppm.exe not found; cannot create page PNGs")
    prefix = output_dir / "page"
    result = run_quiet([str(pdftoppm), "-png", "-r", str(dpi), str(pdf), str(prefix)])
    pages = sorted(output_dir.glob("page-*.png"))
    if result.returncode != 0 or not pages:
        raise RuntimeError(f"PDF rasterization failed (exit {result.returncode}):\n{result.stderr}")
    return pages


def render(input_path: Path, output_dir: Path, dpi: int, emit_pdf: bool) -> list[Path]:
    input_path = input_path.resolve()
    output_dir = output_dir.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ASCII-only staging prevents legacy Windows code pages from corrupting paths.
    with tempfile.TemporaryDirectory(prefix="codex_docx_render_") as raw_temp:
        stage = Path(raw_temp)
        staged_docx = stage / "input.docx"
        shutil.copy2(input_path, staged_docx)
        staged_pdf, lo_log = libreoffice_to_pdf(staged_docx, stage, stage / "lo_profile")
        engine = "LibreOffice"
        if staged_pdf is None:
            staged_pdf, word_log = word_to_pdf(staged_docx, stage / "input.pdf")
            engine = "Microsoft Word"
            if staged_pdf is None:
                raise RuntimeError(
                    "Both render engines failed.\n\nLibreOffice:\n"
                    + lo_log
                    + "\n\nMicrosoft Word:\n"
                    + word_log
                )
        pages = rasterize(staged_pdf, stage, dpi)
        delivered = []
        for index, page in enumerate(pages, 1):
            target = output_dir / f"page-{index}.png"
            shutil.copy2(page, target)
            delivered.append(target)
        if emit_pdf:
            shutil.copy2(staged_pdf, output_dir / f"{input_path.stem}.pdf")
        print(f"Rendered {len(delivered)} pages with {engine}")
        return delivered


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("--output_dir", required=True, type=Path)
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--emit_pdf", action="store_true")
    args = parser.parse_args()
    render(args.input_docx, args.output_dir, args.dpi, args.emit_pdf)


if __name__ == "__main__":
    main()
