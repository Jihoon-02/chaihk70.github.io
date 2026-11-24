from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor


ROOT = Path(r"E:\3D\chaihk70.github.io")
OUTPUT = ROOT / "output" / "docx" / "Choi_Jihoon_Resume_CoverLetter.docx"
QR = ROOT / "assets" / "jihoon-portfolio-qr.png"

NAVY = "17283B"
BLUE = "2A6EA6"
BLUE_LIGHT = "EAF2F8"
TEXT = "232A31"
MUTED = "5F6B76"
LINE = "D9E0E6"
PALE = "F5F7F9"
WHITE = "FFFFFF"
FONT = "Malgun Gothic"


def set_run_font(run, size=None, bold=None, color=None, name=FONT):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)
    return run


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=120, start=130, bottom=120, end=130):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color=LINE, size=5, inside=True, outer=True):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    names = []
    if outer:
        names += ["top", "left", "bottom", "right"]
    if inside:
        names += ["insideH", "insideV"]
    for edge in names:
        tag = f"w:{edge}"
        node = borders.find(qn(tag))
        if node is None:
            node = OxmlElement(tag)
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), str(size))
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)


def remove_table_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "nil")
        borders.append(node)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    tr_pr.append(repeat)


def keep_row_together(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def add_hyperlink(paragraph, text, url, color=BLUE, underline=True, bold=False, size=9.5):
    part = paragraph.part
    rel_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), rel_id)
    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    r_fonts = OxmlElement("w:rFonts")
    for attr in ("ascii", "hAnsi", "eastAsia"):
        r_fonts.set(qn(f"w:{attr}"), FONT)
    r_pr.append(r_fonts)
    color_el = OxmlElement("w:color")
    color_el.set(qn("w:val"), color)
    r_pr.append(color_el)
    size_el = OxmlElement("w:sz")
    size_el.set(qn("w:val"), str(int(size * 2)))
    r_pr.append(size_el)
    size_cs = OxmlElement("w:szCs")
    size_cs.set(qn("w:val"), str(int(size * 2)))
    r_pr.append(size_cs)
    if underline:
        u = OxmlElement("w:u")
        u.set(qn("w:val"), "single")
        r_pr.append(u)
    if bold:
        r_pr.append(OxmlElement("w:b"))
    run.append(r_pr)
    text_el = OxmlElement("w:t")
    text_el.text = text
    run.append(text_el)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)
    return hyperlink


def add_field(paragraph, instruction):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, placeholder, end])
    set_run_font(run, 8.2, color=MUTED)


def set_paragraph(paragraph, before=0, after=0, line=1.0, keep_next=False, keep_together=False):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line
    fmt.keep_with_next = keep_next
    fmt.keep_together = keep_together
    return paragraph


def add_section_heading(doc, title, english=None, top=12):
    p = doc.add_paragraph()
    set_paragraph(p, before=top, after=6, line=1.0, keep_next=True)
    p.paragraph_format.border_bottom = None
    r = p.add_run(title)
    set_run_font(r, 13, bold=True, color=NAVY)
    if english:
        r2 = p.add_run(f"   {english.upper()}")
        set_run_font(r2, 7.5, bold=True, color=BLUE)
        r2.font.letter_spacing = Pt(0.8)
    p_pr = p._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), BLUE)
    p_bdr.append(bottom)
    p_pr.append(p_bdr)
    return p


def add_body(doc, text, size=9.5, after=5.5, color=TEXT, indent=0, line=1.42, keep_together=False):
    p = doc.add_paragraph()
    set_paragraph(p, after=after, line=line, keep_together=keep_together)
    if indent:
        p.paragraph_format.left_indent = Mm(indent)
    r = p.add_run(text)
    set_run_font(r, size, color=color)
    return p


def add_bullet(doc, text, size=9.2, after=2.7, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Mm(5 + level * 5)
    p.paragraph_format.first_line_indent = Mm(-3.4)
    set_paragraph(p, after=after, line=1.32, keep_together=True)
    set_run_font(p.add_run(text), size, color=TEXT)
    return p


def add_label_value(cell, label, value, value_color=TEXT):
    p = cell.paragraphs[0]
    set_paragraph(p, after=0, line=1.25)
    set_run_font(p.add_run(label + "\n"), 7.3, bold=True, color=BLUE)
    set_run_font(p.add_run(value), 9.3, bold=True, color=value_color)


def set_col_width(cell, width_mm):
    cell.width = Mm(width_mm)
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.find(qn("w:tcW"))
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(int(width_mm * 56.6929)))
    tc_w.set(qn("w:type"), "dxa")


def add_page_break(doc):
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


def configure_section(section):
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(14)
    section.bottom_margin = Mm(14)
    section.left_margin = Mm(17)
    section.right_margin = Mm(17)
    section.header_distance = Mm(7)
    section.footer_distance = Mm(7)


def configure_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_paragraph(p, before=0, after=0, line=1.0)
    set_run_font(p.add_run("CHOI JIHOON  ·  3D BACKGROUND & PROP ARTIST    "), 7.5, bold=True, color=MUTED)
    add_field(p, "PAGE")
    set_run_font(p.add_run(" / "), 8.2, color=MUTED)
    add_field(p, "NUMPAGES")
    p_pr = p._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    top = OxmlElement("w:top")
    top.set(qn("w:val"), "single")
    top.set(qn("w:sz"), "5")
    top.set(qn("w:space"), "6")
    top.set(qn("w:color"), LINE)
    p_bdr.append(top)
    p_pr.append(p_bdr)


def build_document():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    for section in doc.sections:
        configure_section(section)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = FONT
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    normal.font.size = Pt(9.5)
    normal.font.color.rgb = RGBColor.from_string(TEXT)
    normal.paragraph_format.space_after = Pt(0)

    for style_name in ("List Bullet", "List Bullet 2"):
        style = styles[style_name]
        style.font.name = FONT
        style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        style.font.size = Pt(9.2)
        style.font.color.rgb = RGBColor.from_string(TEXT)

    doc.core_properties.title = "최지훈 이력서 · 프로젝트 기술서 · 자기소개서"
    doc.core_properties.subject = "3D 배경·프랍 아티스트 지원서"
    doc.core_properties.author = "최지훈"
    doc.core_properties.keywords = "3D Background Artist, Prop Artist, Unreal Engine 5, ZBrush, Substance Painter"

    # PAGE 1 — Resume overview
    header = doc.add_table(rows=1, cols=2)
    header.alignment = WD_TABLE_ALIGNMENT.CENTER
    header.autofit = False
    remove_table_borders(header)
    left, right = header.rows[0].cells
    set_col_width(left, 151)
    set_col_width(right, 25)
    set_cell_margins(left, 0, 0, 0, 0)
    set_cell_margins(right, 0, 0, 0, 0)
    left.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    right.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    p = left.paragraphs[0]
    set_paragraph(p, after=1, line=1.0)
    set_run_font(p.add_run("CHOI JIHOON"), 25, bold=True, color=NAVY)
    p2 = left.add_paragraph()
    set_paragraph(p2, after=4, line=1.0)
    r = p2.add_run("3D BACKGROUND & PROP ARTIST")
    set_run_font(r, 9.2, bold=True, color=BLUE)
    r.font.letter_spacing = Pt(1.0)
    p3 = left.add_paragraph()
    set_paragraph(p3, after=1, line=1.2)
    set_run_font(p3.add_run("팀 프로젝트와 UE5 에셋 제작 경험을 갖춘 3D 배경·프랍 아티스트"), 11.2, bold=True, color=TEXT)
    p4 = left.add_paragraph()
    set_paragraph(p4, after=0, line=1.2)
    set_run_font(p4.add_run("chaihk70@gmail.com  ·  "), 8.8, color=MUTED)
    add_hyperlink(p4, "Portfolio Website", "https://jihoon-02.github.io/chaihk70.github.io/", size=8.8, bold=True)

    rp = right.paragraphs[0]
    rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if QR.exists():
        rp.add_run().add_picture(str(QR), width=Mm(21))
    caption = right.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph(caption, before=1, after=0, line=1.0)
    set_run_font(caption.add_run("PORTFOLIO"), 6.5, bold=True, color=MUTED)

    add_section_heading(doc, "프로필", "Professional Profile", top=9)
    add_body(
        doc,
        "게임 속 오브젝트의 구조와 실루엣을 설득력 있게 설계하고, 재질별 마모와 사용 흔적을 세밀하게 표현하는 3D 배경·프랍 아티스트입니다. 모델링부터 UV, 텍스처링, 베이킹, 라이팅과 UE5 씬 세팅까지 전 과정을 직접 진행하며, 현재는 마차 제작과 사암을 포함한 다양한 돌 스컬프팅으로 표현 범위를 확장하고 있습니다.",
        size=9.5,
        after=4,
        line=1.45,
        keep_together=True,
    )

    add_section_heading(doc, "핵심 역량", "Core Competencies", top=7)
    comp = doc.add_table(rows=2, cols=2)
    comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp.autofit = False
    set_table_borders(comp, color=LINE, size=5)
    entries = [
        ("01  게임 에셋 전 과정", "3ds Max·ZBrush 모델링부터 UV, PBR 텍스처링, 베이크, 렌더링과 UE5 적용까지 직접 진행"),
        ("02  스컬프팅과 재질 표현", "무기·가구·석재·건축 프랍의 실루엣, 표면 변화, 마모와 노화 표현에 집중"),
        ("03  구매 에셋 컨버팅", "원본 구조 분석 후 모델·UV·텍스처·머티리얼·피벗·충돌·LOD를 프로젝트 규격에 맞게 수정"),
        ("04  실무형 팀 협업", "현직자 15명이 참여하는 인디게임 팀에서 일정 공유, 리뷰·피드백, 엔진 적용 및 수정 경험"),
    ]
    for idx, (title, desc) in enumerate(entries):
        cell = comp.cell(idx // 2, idx % 2)
        set_col_width(cell, 88)
        set_cell_margins(cell, 120, 160, 120, 160)
        if idx in (0, 3):
            set_cell_shading(cell, PALE)
        p = cell.paragraphs[0]
        set_paragraph(p, after=3, line=1.15, keep_together=True)
        set_run_font(p.add_run(title), 9.0, bold=True, color=NAVY)
        d = cell.add_paragraph()
        set_paragraph(d, after=0, line=1.32, keep_together=True)
        set_run_font(d.add_run(desc), 8.35, color=TEXT)
    for row in comp.rows:
        keep_row_together(row)

    add_section_heading(doc, "학력", "Education", top=9)
    edu = doc.add_table(rows=1, cols=3)
    edu.alignment = WD_TABLE_ALIGNMENT.CENTER
    edu.autofit = False
    set_table_borders(edu, color=LINE, size=5, inside=True, outer=True)
    values = [
        ("기간", "2021 – 2027", 32),
        ("학교", "한국항공대학교", 61),
        ("전공", "항공우주 및 기계공학부", 83),
    ]
    for cell, (label, value, width) in zip(edu.rows[0].cells, values):
        set_col_width(cell, width)
        set_cell_margins(cell, 130, 140, 130, 140)
        add_label_value(cell, label, value)
    keep_row_together(edu.rows[0])

    add_section_heading(doc, "작업 분야 및 도구", "Focus & Tools", top=9)
    focus = doc.add_table(rows=2, cols=2)
    focus.alignment = WD_TABLE_ALIGNMENT.CENTER
    focus.autofit = False
    set_table_borders(focus, color=LINE, size=5)
    focus_rows = [
        ("FOCUS", "Environment Art · Props · Material · Lighting"),
        ("TOOLS", "3ds Max · ZBrush · Marvelous Designer · RizomUV · Substance 3D Painter · Marmoset Toolbag · Unreal Engine 5"),
    ]
    for row, (label, value) in zip(focus.rows, focus_rows):
        set_col_width(row.cells[0], 34)
        set_col_width(row.cells[1], 142)
        set_cell_shading(row.cells[0], NAVY)
        for c in row.cells:
            set_cell_margins(c, 105, 140, 105, 140)
        p = row.cells[0].paragraphs[0]
        set_paragraph(p, after=0, line=1.1)
        set_run_font(p.add_run(label), 7.5, bold=True, color=WHITE)
        q = row.cells[1].paragraphs[0]
        set_paragraph(q, after=0, line=1.25)
        set_run_font(q.add_run(value), 8.7, bold=True, color=TEXT)
        keep_row_together(row)

    add_page_break(doc)

    # PAGE 2 — Project experience and technical skills
    p = doc.add_paragraph()
    set_paragraph(p, after=2, line=1.0)
    set_run_font(p.add_run("PROJECT & SKILLS"), 20, bold=True, color=NAVY)
    sp = doc.add_paragraph()
    set_paragraph(sp, after=1, line=1.25)
    set_run_font(sp.add_run("프로젝트 경험과 제작 역량"), 10.5, bold=True, color=BLUE)

    add_section_heading(doc, "팀 프로젝트", "Team Project", top=7)
    project = doc.add_table(rows=1, cols=4)
    project.alignment = WD_TABLE_ALIGNMENT.CENTER
    project.autofit = False
    set_table_borders(project, color=LINE, size=5)
    project_info = [
        ("프로젝트", "WeIND UP", 37),
        ("형태", "2인 협동 퍼즐 인디게임", 50),
        ("역할", "프랍 모델러", 37),
        ("진행", "개발 진행 중", 52),
    ]
    for cell, (label, value, width) in zip(project.rows[0].cells, project_info):
        set_col_width(cell, width)
        set_cell_margins(cell, 110, 125, 110, 125)
        add_label_value(cell, label, value)
    keep_row_together(project.rows[0])
    add_body(
        doc,
        "현직자 15명이 참여하는 팀에서 파트별 업무 분담, 일정 관리, 작업물 리뷰와 피드백, UE5 엔진 적용 및 수정까지 실무와 유사한 프로세스를 경험하고 있습니다.",
        size=9.2,
        after=3.5,
        line=1.38,
        keep_together=True,
    )
    for item in [
        "챕터별 환경에 필요한 프랍을 제작하고, 게임 플레이 거리에서도 형태가 명확히 읽히도록 실루엣과 비례를 조정",
        "작업 의도와 진행 상황을 공유하고 리뷰·피드백을 반영해 수정 방향과 우선순위를 조율",
        "완성 에셋의 UE5 적용 상태를 확인하고 다른 파트의 요구사항에 맞춰 재질, 스케일, 피벗과 품질을 보완",
    ]:
        add_bullet(doc, item)

    add_section_heading(doc, "개인 포트폴리오", "Personal Work", top=8)
    add_body(
        doc,
        "무기, 가구, 석재, 건축 프랍 등 서로 다른 구조와 재질을 가진 오브젝트를 제작했습니다. 현재는 복합 구조와 재질을 가진 마차를 제작하고 있으며, 사암을 포함한 여러 종류의 돌 스컬프팅을 지속적으로 추가하고 있습니다.",
        size=9.2,
        after=3.5,
        line=1.38,
        keep_together=True,
    )
    for item in [
        "형태와 실루엣을 먼저 명확히 설계한 뒤, 재질별 마모·노화·사용 흔적을 근거 있게 표현",
        "하드서피스와 유기적 스컬프팅을 병행하고, PBR 텍스처와 라이팅으로 재질의 차이를 효과적으로 전달",
        "모델링 → UV → 베이킹 → 텍스처링 → 렌더링 → UE5 씬 세팅의 전 과정을 직접 수행",
    ]:
        add_bullet(doc, item)

    add_section_heading(doc, "구매 에셋 활용 및 컨버팅", "Asset Conversion", top=8)
    conversion = doc.add_table(rows=1, cols=3)
    conversion.alignment = WD_TABLE_ALIGNMENT.CENTER
    conversion.autofit = False
    set_table_borders(conversion, color=LINE, size=5)
    conversion_data = [
        ("01  분석", "원본 구조·품질·재사용 범위 점검", 58),
        ("02  수정", "모델·UV·텍스처·머티리얼 보완", 59),
        ("03  적용", "피벗·충돌·LOD·최적화 후 UE5 적용", 59),
    ]
    for idx, (title, desc, width) in enumerate(conversion_data):
        cell = conversion.cell(0, idx)
        set_col_width(cell, width)
        set_cell_margins(cell, 110, 130, 110, 130)
        if idx == 1:
            set_cell_shading(cell, PALE)
        p = cell.paragraphs[0]
        set_paragraph(p, after=2, line=1.15)
        set_run_font(p.add_run(title), 8.2, bold=True, color=BLUE)
        q = cell.add_paragraph()
        set_paragraph(q, after=0, line=1.25)
        set_run_font(q.add_run(desc), 8.2, color=TEXT)
    keep_row_together(conversion.rows[0])

    add_section_heading(doc, "기술 역량", "Technical Skills", top=8)
    skills = doc.add_table(rows=1, cols=2)
    skills.alignment = WD_TABLE_ALIGNMENT.CENTER
    skills.autofit = False
    set_table_borders(skills, color=LINE, size=5)
    set_repeat_table_header(skills.rows[0])
    headers = [("도구", 44), ("활용 역량", 132)]
    for cell, (label, width) in zip(skills.rows[0].cells, headers):
        set_col_width(cell, width)
        set_cell_shading(cell, NAVY)
        set_cell_margins(cell, 90, 120, 90, 120)
        p = cell.paragraphs[0]
        set_paragraph(p, after=0, line=1.0)
        set_run_font(p.add_run(label), 8.0, bold=True, color=WHITE)
    skill_rows = [
        ("3ds Max · RizomUV", "로우·하이폴 모델링, 리토폴로지, UV 언랩과 패킹, 게임 에셋 최적화"),
        ("ZBrush · Marvelous", "하이폴 스컬프팅, 석재·자연물 디테일, 패브릭 제작과 자연스러운 주름 표현"),
        ("Substance 3D Painter", "PBR 텍스처링, 베이킹, 재질별 마모·노화·사용 흔적 표현"),
        ("Marmoset · Unreal 5", "베이킹, 라이팅과 렌더링, 에셋 임포트, 머티리얼, 씬 세팅"),
        ("AI 도구", "레퍼런스 조사, 아이디어 정리와 반복 업무 효율화에 활용"),
    ]
    for idx, (tool, ability) in enumerate(skill_rows):
        row = skills.add_row()
        if idx % 2 == 1:
            for c in row.cells:
                set_cell_shading(c, PALE)
        for cell, value, width, is_tool in zip(row.cells, (tool, ability), (44, 132), (True, False)):
            set_col_width(cell, width)
            set_cell_margins(cell, 85, 120, 85, 120)
            p = cell.paragraphs[0]
            set_paragraph(p, after=0, line=1.22, keep_together=True)
            set_run_font(p.add_run(value), 8.1, bold=is_tool, color=NAVY if is_tool else TEXT)
        keep_row_together(row)

    add_page_break(doc)

    # PAGE 3 — Cover letter
    p = doc.add_paragraph()
    set_paragraph(p, after=2, line=1.0)
    set_run_font(p.add_run("SELF-INTRODUCTION"), 20, bold=True, color=NAVY)
    sp = doc.add_paragraph()
    set_paragraph(sp, after=7, line=1.25)
    set_run_font(sp.add_run("게임의 세계를 설득력 있게 만드는 3D 배경 아티스트"), 12.5, bold=True, color=BLUE)

    intro_paragraphs = [
        "게임을 즐기는 것을 넘어, 게임 속 공간과 오브젝트가 어떤 과정으로 만들어지는지에 깊은 관심을 가지면서 3D 배경 아티스트를 목표로 하게 되었습니다. 특히 모델링 작업 자체를 좋아하며, 형태를 분석하고 실루엣을 다듬어 하나의 오브젝트를 완성해 나가는 과정에서 큰 즐거움을 느낍니다. 플레이어가 작은 프랍 하나에서도 세계관과 이야기를 느끼고, 게임 속 공간에 더욱 깊이 몰입할 수 있도록 설득력 있는 환경을 만드는 것이 저의 목표입니다.",
        "포트폴리오를 제작하며 무기, 가구, 석재, 건축 프랍 등 다양한 소재와 형태의 오브젝트를 경험했습니다. 최근에는 복합적인 구조와 재질을 가진 마차를 제작하고 있으며, 사암을 비롯한 여러 종류의 돌을 지속적으로 스컬프팅하면서 자연물의 형태와 표면을 관찰하고 표현하는 역량을 넓히고 있습니다. 단순히 디테일을 많이 추가하기보다는 실루엣과 구조를 먼저 명확히 하고, 재질마다 다른 마모와 노화, 사용 흔적이 자연스럽게 드러나도록 작업하고 있습니다. 또한 모델링부터 UV, 텍스처링, 베이킹, 라이팅과 UE5 씬 세팅까지 환경 제작의 전 과정을 직접 진행할 수 있습니다.",
        "구매 데이터를 활용하고 프로젝트에 맞게 컨버팅하는 능력도 갖추고 있습니다. 구매 에셋을 그대로 배치하는 데 그치지 않고, 원본 데이터의 구조와 품질을 분석한 뒤 프로젝트의 아트 방향과 엔진 규격에 맞게 모델과 UV, 텍스처, 머티리얼을 수정합니다. 스케일과 피벗, 충돌, LOD 및 최적화 요소를 점검하고, 서로 다른 제작 방식의 데이터를 일관된 품질과 규격으로 정리해 UE5 환경에 적용할 수 있습니다. 이를 통해 제한된 제작 일정 안에서도 기존 데이터를 효율적으로 활용하면서 필요한 부분은 직접 보완하는 유연한 작업 방식을 익혔습니다.",
        "현재는 현직자 15명이 함께하는 인디게임 개발 팀 프로젝트에 프랍 모델러로 참여하고 있습니다. 인디 프로젝트이지만 파트별 업무 분담과 일정 관리, 작업물 리뷰와 피드백, 엔진 적용 및 수정 과정을 거치는 실무와 유사한 프로세스로 진행되고 있습니다. 작업 의도와 진행 상황을 명확하게 공유하고, 다른 파트의 요구사항을 확인해 수정 방향을 조율하는 과정에서 협업과 의사소통의 중요성을 배웠습니다. 피드백을 방어적으로 받아들이기보다 프로젝트의 완성도를 높이기 위한 과정으로 생각하며, 팀원들과 적극적으로 의견을 나누고 책임감 있게 작업을 마무리하고 있습니다.",
        "게임과 모델링을 좋아하는 마음을 꾸준한 작업과 학습으로 이어가며, 새로운 제작 방식과 피드백을 빠르게 흡수하는 아티스트가 되고자 합니다. 맡은 오브젝트의 완성도뿐 아니라 전체 게임 환경과 제작 과정까지 고려하며, 플레이어가 자연스럽게 믿고 몰입할 수 있는 세계를 만드는 3D 배경 아티스트로 성장하겠습니다.",
    ]
    intro_labels = [
        "지원 동기와 작업 방향",
        "포트폴리오와 제작 역량",
        "구매 에셋 활용 및 컨버팅",
        "실무형 협업 경험",
        "성장 방향",
    ]
    for idx, (label, text) in enumerate(zip(intro_labels, intro_paragraphs), start=1):
        h = doc.add_paragraph()
        set_paragraph(h, before=3 if idx > 1 else 0, after=2.8, line=1.0, keep_next=True)
        set_run_font(h.add_run(f"{idx:02d}"), 8.0, bold=True, color=BLUE)
        set_run_font(h.add_run(f"   {label}"), 9.8, bold=True, color=NAVY)
        b = doc.add_paragraph()
        set_paragraph(b, after=4.8, line=1.38, keep_together=True)
        set_run_font(b.add_run(text), 8.75, color=TEXT)

    closing = doc.add_paragraph()
    closing.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_paragraph(closing, before=4, after=0, line=1.0, keep_together=True)
    set_run_font(closing.add_run("최지훈  ·  3D Background & Prop Artist"), 8.5, bold=True, color=MUTED)

    for section in doc.sections:
        configure_section(section)
        configure_footer(section)

    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build_document()
