#!/usr/bin/env python3
"""按 voice/checks.txt 检查中文稿件。只提醒，不改文。

用法  python3 -I scripts/check.py 稿件.md
      cat 稿件.md | python3 -I scripts/check.py -
"""

from __future__ import annotations

import re
import statistics
import sys
from pathlib import Path

CHECKS = Path(__file__).resolve().parent.parent / "voice" / "checks.txt"
SENT_END = re.compile(r"[^。！？!?\n]+[。！？!?]+")
CODE_SPAN = re.compile(r"`[^`]*`")
URL = re.compile(r"https?://\S+")


def load_checks(path: Path) -> list[tuple[str, str, re.Pattern[str]]]:
    rules = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        kind, _, value = line.partition(" ")
        value = value.strip()
        if not value:
            continue
        pattern = re.compile(value) if kind == "regex" else re.compile(re.escape(value))
        rules.append((kind, value, pattern))
    return rules


def prose_lines(text: str) -> list[tuple[int, str]]:
    """去掉代码块、行内代码和网址，返回 (行号, 文本)。"""
    out, in_fence = [], False
    for no, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out.append((no, URL.sub("", CODE_SPAN.sub("", line))))
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    src = sys.argv[1]
    text = sys.stdin.read() if src == "-" else Path(src).read_text(encoding="utf-8")
    lines = prose_lines(text)
    rules = load_checks(CHECKS)

    hits = []
    for no, line in lines:
        for kind, value, pattern in rules:
            for m in pattern.finditer(line):
                hits.append((no, kind, m.group(0), line.strip()))

    # 连续反问，同一段里连着三句以上问句
    questions = []
    for no, line in lines:
        sents = SENT_END.findall(line)
        run = 0
        for s in sents:
            run = run + 1 if s.rstrip()[-1] in "？?" else 0
            if run == 3:
                questions.append(no)

    # 句长分布
    sentences = [s for _, line in lines for s in SENT_END.findall(line) if not line.lstrip().startswith("#")]
    lengths = [len(re.sub(r"\s", "", s)) for s in sentences]

    han = sum(len(re.findall(r"[一-鿿]", line)) for _, line in lines)
    print(f"汉字 {han}，句子 {len(lengths)}，词表命中 {len(hits)}，连续反问 {len(questions)} 处")

    for no, kind, found, line in hits:
        snippet = line if len(line) <= 40 else line[:40] + "…"
        print(f"  第 {no} 行 [{kind}] 「{found}」 {snippet}")
    for no in questions:
        print(f"  第 {no} 行 连着三句以上问句，留一两个最相关的，或者直接说")

    if len(lengths) >= 10:
        mean = statistics.mean(lengths)
        cv = statistics.pstdev(lengths) / mean if mean else 0
        note = "，句子长短太整齐，放开几句、压短几句" if cv < 0.45 else ""
        print(f"句长 平均 {mean:.0f} 字，最短 {min(lengths)}，最长 {max(lengths)}，变异系数 {cv:.2f}{note}")

    if hits or questions:
        print("命中只是提醒。引用原话、时间顺序、正常否定等情况可以保留。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
