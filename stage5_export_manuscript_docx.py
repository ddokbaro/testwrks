"""[Stage 5] 논문 초안 Markdown → Word(docx) 변환

KADH 논문투고규정(제3조 2항)은 MS Word 양식 제출을 요구한다. 이 스크립트는
paper/manuscript_draft_ko.md 를 docx 로 변환하고, '그림' 절에 나열된 PNG를 본문 끝에 삽입한다.
협의회 공식 양식(docx)에 옮겨 붙이기 전의 작업용 파일이다.

규정 반영: 표제 번호(1. / 1.1.), 문단 첫 행 두 칸 들여쓰기(제9조 2항), 미주 번호 1) 형식.
"""

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "paper" / "manuscript_draft_ko.md"
DST = ROOT / "paper" / "manuscript_draft_ko.docx"
FONT = "맑은 고딕"
FIG_LINE = re.compile(r"^그림 (\d)\. (\S+\.png)$")


def set_font(run, size: float | None = None, bold: bool | None = None) -> None:
    run.font.name = FONT
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold


def add_inline(paragraph, text: str, size: float = 10.5) -> None:
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part:
            set_font(paragraph.add_run(part), size, bold=(i % 2 == 1))


def convert() -> None:
    doc = Document()
    for section in doc.sections:
        section.left_margin = section.right_margin = Cm(2.5)
        section.top_margin = section.bottom_margin = Cm(2.5)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    normal.font.size = Pt(10.5)

    lines = SRC.read_text(encoding="utf-8").splitlines()
    in_figures = False
    first_h1 = True
    for raw in lines:
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("# "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_font(p.add_run(line[2:]), 16 if first_h1 else 13, bold=True)
            first_h1 = False
            continue
        if line.startswith("## "):
            title = line[3:]
            in_figures = title == "그림"
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            set_font(p.add_run(title), 13, bold=True)
            continue
        if line.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            set_font(p.add_run(line[4:]), 11.5, bold=True)
            continue
        if line.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
            add_inline(p, line[2:], 9)
            continue
        m = FIG_LINE.match(line)
        if in_figures and m:
            img = ROOT / m.group(2)
            if img.exists():
                doc.add_picture(str(img), width=Cm(15.5))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_font(cap.add_run(f"그림 {m.group(1)}"), 9)
            continue
        p = doc.add_paragraph()
        is_body = not re.match(r"^(\d+\)|\s*\d+\.\d*\.?\s|[A-Z가-힣].{0,40}\(\d{4}\)|Keywords:|주제어:|Cross-Catalysis|김바로)", line)
        if is_body and not line.startswith(" "):
            p.paragraph_format.first_line_indent = Pt(21)
        p.paragraph_format.line_spacing = 1.5
        add_inline(p, line.strip())

    DST.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(DST))
    print(f"[Stage 5] {DST}")


if __name__ == "__main__":
    convert()
