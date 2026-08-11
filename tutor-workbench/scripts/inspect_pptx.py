#!/usr/bin/env python3
"""Render image-based PPTX slides locally for authorised material ingestion."""
import argparse
import json
import re
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
from xml.etree import ElementTree as ET

from PIL import Image

P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def target_for_slide(zf, slide_no):
    rel_path = f"ppt/slides/_rels/slide{slide_no}.xml.rels"
    if rel_path not in zf.namelist():
        return {}
    root = ET.fromstring(zf.read(rel_path))
    return {
        node.attrib["Id"]: str(PurePosixPath("ppt/slides") / node.attrib["Target"]).replace("ppt/slides/../", "ppt/")
        for node in root.findall(f"{REL}Relationship")
        if node.attrib.get("Type", "").endswith("/image")
    }


def emu_box(node, sx, sy):
    xfrm = node.find(f".//{A}xfrm")
    if xfrm is None:
        return None
    off, ext = xfrm.find(f"{A}off"), xfrm.find(f"{A}ext")
    if off is None or ext is None:
        return None
    return (
        round(int(off.attrib.get("x", 0)) * sx),
        round(int(off.attrib.get("y", 0)) * sy),
        round(int(ext.attrib.get("cx", 0)) * sx),
        round(int(ext.attrib.get("cy", 0)) * sy),
    )


def native_text(root):
    texts = []
    for sp in root.findall(f".//{P}sp"):
        runs = [t.text or "" for t in sp.findall(f".//{A}t")]
        if runs:
            texts.append("".join(runs))
    return texts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--width", type=int, default=1600)
    args = parser.parse_args()
    out = args.out.resolve()
    slides_out = out / "slides"
    slides_out.mkdir(parents=True, exist_ok=True)

    with ZipFile(args.pptx) as zf:
        presentation = ET.fromstring(zf.read("ppt/presentation.xml"))
        size = presentation.find(f"{P}sldSz")
        sw, sh = int(size.attrib["cx"]), int(size.attrib["cy"])
        width, height = args.width, round(args.width * sh / sw)
        sx, sy = width / sw, height / sh
        slide_nos = sorted(int(m.group(1)) for name in zf.namelist() if (m := re.fullmatch(r"ppt/slides/slide(\d+)\.xml", name)))
        summary = []
        for slide_no in slide_nos:
            root = ET.fromstring(zf.read(f"ppt/slides/slide{slide_no}.xml"))
            canvas = Image.new("RGBA", (width, height), "white")
            relationships = target_for_slide(zf, slide_no)
            image_count = 0
            for pic in root.findall(f".//{P}pic"):
                blip = pic.find(f".//{A}blip")
                box = emu_box(pic, sx, sy)
                rel_id = blip.attrib.get(f"{R}embed") if blip is not None else None
                image_path = relationships.get(rel_id)
                if not image_path or not box or image_path not in zf.namelist():
                    continue
                x, y, w, h = box
                if w <= 0 or h <= 0:
                    continue
                with zf.open(image_path) as data:
                    image = Image.open(data).convert("RGBA").resize((w, h))
                    canvas.alpha_composite(image, (x, y))
                image_count += 1
            rendered = slides_out / f"slide-{slide_no:02d}.png"
            canvas.convert("RGB").save(rendered, "PNG")
            summary.append({"slide": slide_no, "image_count": image_count, "native_text": native_text(root), "rendered": str(rendered)})
    (out / "slide-index.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rendered {len(summary)} slides")


if __name__ == "__main__":
    main()
