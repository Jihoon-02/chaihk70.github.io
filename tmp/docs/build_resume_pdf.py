from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"E:\3D\chaihk70.github.io")
OUTPUT = ROOT / "output" / "pdf" / "Choi_Jihoon_Resume_CoverLetter.pdf"
QR = ROOT / "assets" / "jihoon-portfolio-qr.png"
REGULAR = r"C:\Windows\Fonts\malgun.ttf"
BOLD = r"C:\Windows\Fonts\malgunbd.ttf"

pdfmetrics.registerFont(TTFont("Malgun", REGULAR))
pdfmetrics.registerFont(TTFont("MalgunBold", BOLD))

NAVY = colors.HexColor("#17283B")
BLUE = colors.HexColor("#2A6EA6")
TEXT = colors.HexColor("#232A31")
MUTED = colors.HexColor("#5F6B76")
LINE = colors.HexColor("#D9E0E6")
PALE = colors.HexColor("#F5F7F9")
WHITE = colors.white


styles = getSampleStyleSheet()
S = {
    "name": ParagraphStyle("name", fontName="MalgunBold", fontSize=25, leading=28, textColor=NAVY, spaceAfter=2),
    "role": ParagraphStyle("role", fontName="MalgunBold", fontSize=8.8, leading=11, textColor=BLUE, tracking=1.1, spaceAfter=5),
    "title": ParagraphStyle("title", fontName="MalgunBold", fontSize=10.8, leading=14, textColor=TEXT, spaceAfter=4),
    "contact": ParagraphStyle("contact", fontName="Malgun", fontSize=8.3, leading=11, textColor=MUTED),
    "page_title": ParagraphStyle("page_title", fontName="MalgunBold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=1),
    "page_sub": ParagraphStyle("page_sub", fontName="MalgunBold", fontSize=10.2, leading=13, textColor=BLUE, spaceAfter=5),
    "section": ParagraphStyle("section", fontName="MalgunBold", fontSize=12.5, leading=16, textColor=NAVY),
    "section_en": ParagraphStyle("section_en", fontName="MalgunBold", fontSize=7.0, leading=10, textColor=BLUE, tracking=0.8, alignment=TA_RIGHT),
    "body": ParagraphStyle("body", fontName="Malgun", fontSize=9.2, leading=13.4, textColor=TEXT, wordWrap="CJK"),
    "body_small": ParagraphStyle("body_small", fontName="Malgun", fontSize=8.3, leading=11.6, textColor=TEXT, wordWrap="CJK"),
    "body_intro": ParagraphStyle("body_intro", fontName="Malgun", fontSize=8.55, leading=12.55, textColor=TEXT, wordWrap="CJK"),
    "label": ParagraphStyle("label", fontName="MalgunBold", fontSize=7.0, leading=9, textColor=BLUE),
    "value": ParagraphStyle("value", fontName="MalgunBold", fontSize=8.8, leading=12, textColor=TEXT),
    "comp_title": ParagraphStyle("comp_title", fontName="MalgunBold", fontSize=8.7, leading=11, textColor=NAVY, spaceAfter=3),
    "bullet": ParagraphStyle("bullet", fontName="Malgun", fontSize=8.75, leading=12.2, textColor=TEXT, leftIndent=4.5*mm, firstLineIndent=-3.5*mm, bulletIndent=0, wordWrap="CJK", spaceAfter=2.2),
    "intro_head_num": ParagraphStyle("intro_head_num", fontName="MalgunBold", fontSize=8, leading=10, textColor=BLUE),
    "intro_head": ParagraphStyle("intro_head", fontName="MalgunBold", fontSize=9.7, leading=12, textColor=NAVY),
    "footer": ParagraphStyle("footer", fontName="MalgunBold", fontSize=7.2, leading=9, textColor=MUTED, alignment=TA_RIGHT),
}


def P(text, style):
    return Paragraph(text, S[style])


def section_heading(title, english, top=4*mm):
    table = Table(
        [[P(title, "section"), P(english.upper(), "section_en")]],
        colWidths=[115*mm, 61*mm],
        hAlign="LEFT",
        spaceBefore=top,
        spaceAfter=3.2*mm,
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LINEBELOW", (0, 0), (-1, -1), 1.2, BLUE),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return table


def label_value(label, value):
    return [P(label, "label"), Spacer(1, 1.2*mm), P(value, "value")]


def grid_style(backgrounds=None, padding=7):
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), padding),
        ("RIGHTPADDING", (0, 0), (-1, -1), padding),
        ("TOPPADDING", (0, 0), (-1, -1), padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
    ]
    if backgrounds:
        commands.extend(backgrounds)
    return TableStyle(commands)


def bullet(text):
    return Paragraph("•  " + text, S["bullet"])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 11.2*mm, A4[0] - doc.rightMargin, 11.2*mm)
    canvas.setFont("MalgunBold", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - doc.rightMargin, 7.7*mm, f"CHOI JIHOON  ·  3D BACKGROUND & PROP ARTIST    {doc.page}")
    canvas.restoreState()


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=17*mm,
        rightMargin=17*mm,
        topMargin=14*mm,
        bottomMargin=15*mm,
        title="최지훈 이력서 · 프로젝트 기술서 · 자기소개서",
        author="최지훈",
        subject="3D 배경·프랍 아티스트 지원서",
    )
    story = []

    # PAGE 1
    left_header = [
        P("CHOI JIHOON", "name"),
        P("3D BACKGROUND &amp; PROP ARTIST", "role"),
        P("팀 프로젝트와 UE5 에셋 제작 경험을 갖춘 3D 배경·프랍 아티스트", "title"),
        Paragraph(
            "chaihk70@gmail.com  ·  <link href='https://jihoon-02.github.io/chaihk70.github.io/' color='#2A6EA6'><b>Portfolio Website</b></link>",
            S["contact"],
        ),
    ]
    right_header = []
    if QR.exists():
        qr = Image(str(QR), width=20*mm, height=20*mm)
        qr.hAlign = "CENTER"
        right_header.append(qr)
    right_header.append(Spacer(1, 1*mm))
    right_header.append(Paragraph("PORTFOLIO", ParagraphStyle("qr_caption", parent=S["label"], alignment=TA_CENTER, textColor=MUTED)))
    header = Table([[left_header, right_header]], colWidths=[151*mm, 25*mm], hAlign="LEFT")
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header)
    story.append(section_heading("프로필", "Professional Profile", 5*mm))
    story.append(P("게임 속 오브젝트의 구조와 실루엣을 설득력 있게 설계하고, 재질별 마모와 사용 흔적을 세밀하게 표현하는 3D 배경·프랍 아티스트입니다. 모델링부터 UV, 텍스처링, 베이킹, 라이팅과 UE5 씬 세팅까지 전 과정을 직접 진행하며, 현재는 마차 제작과 사암을 포함한 다양한 돌 스컬프팅으로 표현 범위를 확장하고 있습니다.", "body"))

    story.append(section_heading("핵심 역량", "Core Competencies", 3.7*mm))
    comp_data = [
        [
            [P("01  게임 에셋 전 과정", "comp_title"), P("3ds Max·ZBrush 모델링부터 UV, PBR 텍스처링, 베이크, 렌더링과 UE5 적용까지 직접 진행", "body_small")],
            [P("02  스컬프팅과 재질 표현", "comp_title"), P("무기·가구·석재·건축 프랍의 실루엣, 표면 변화, 마모와 노화 표현에 집중", "body_small")],
        ],
        [
            [P("03  구매 에셋 컨버팅", "comp_title"), P("원본 구조 분석 후 모델·UV·텍스처·머티리얼·피벗·충돌·LOD를 프로젝트 규격에 맞게 수정", "body_small")],
            [P("04  실무형 팀 협업", "comp_title"), P("현직자 15명이 참여하는 인디게임 팀에서 일정 공유, 리뷰·피드백, 엔진 적용 및 수정 경험", "body_small")],
        ],
    ]
    comp = Table(comp_data, colWidths=[88*mm, 88*mm], hAlign="LEFT")
    comp.setStyle(grid_style([
        ("BACKGROUND", (0, 0), (0, 0), PALE),
        ("BACKGROUND", (1, 1), (1, 1), PALE),
    ], padding=7))
    story.append(comp)

    story.append(section_heading("학력", "Education", 3.8*mm))
    edu = Table([[label_value("기간", "2021 – 2027"), label_value("학교", "한국항공대학교"), label_value("전공", "항공우주 및 기계공학부")]], colWidths=[32*mm, 61*mm, 83*mm])
    edu.setStyle(grid_style(padding=7))
    story.append(edu)

    story.append(section_heading("작업 분야 및 도구", "Focus & Tools", 3.8*mm))
    focus_data = [
        [P("FOCUS", "label"), P("<b>Environment Art · Props · Material · Lighting</b>", "body_small")],
        [P("TOOLS", "label"), P("<b>3ds Max · ZBrush · Marvelous Designer · RizomUV · Substance 3D Painter · Marmoset Toolbag · Unreal Engine 5</b>", "body_small")],
    ]
    focus = Table(focus_data, colWidths=[34*mm, 142*mm])
    focus.setStyle(grid_style([
        ("BACKGROUND", (0, 0), (0, -1), NAVY),
        ("TEXTCOLOR", (0, 0), (0, -1), WHITE),
    ], padding=6))
    story.append(focus)

    story.append(PageBreak())

    # PAGE 2
    story.extend([P("PROJECT &amp; SKILLS", "page_title"), P("프로젝트 경험과 제작 역량", "page_sub")])
    story.append(section_heading("팀 프로젝트", "Team Project", 3*mm))
    project_info = [
        label_value("프로젝트", "WeIND UP"),
        label_value("형태", "2인 협동 퍼즐 인디게임"),
        label_value("역할", "프랍 모델러"),
        label_value("진행", "개발 진행 중"),
    ]
    project = Table([project_info], colWidths=[37*mm, 50*mm, 37*mm, 52*mm])
    project.setStyle(grid_style(padding=6))
    story.append(project)
    story.append(Spacer(1, 2.4*mm))
    story.append(P("현직자 15명이 참여하는 팀에서 파트별 업무 분담, 일정 관리, 작업물 리뷰와 피드백, UE5 엔진 적용 및 수정까지 실무와 유사한 프로세스를 경험하고 있습니다.", "body"))
    story.append(Spacer(1, 1.5*mm))
    for text in [
        "챕터별 환경에 필요한 프랍을 제작하고, 게임 플레이 거리에서도 형태가 명확히 읽히도록 실루엣과 비례를 조정",
        "작업 의도와 진행 상황을 공유하고 리뷰·피드백을 반영해 수정 방향과 우선순위를 조율",
        "완성 에셋의 UE5 적용 상태를 확인하고 다른 파트의 요구사항에 맞춰 재질, 스케일, 피벗과 품질을 보완",
    ]:
        story.append(bullet(text))

    story.append(section_heading("개인 포트폴리오", "Personal Work", 3.5*mm))
    story.append(P("무기, 가구, 석재, 건축 프랍 등 서로 다른 구조와 재질을 가진 오브젝트를 제작했습니다. 현재는 복합 구조와 재질을 가진 마차를 제작하고 있으며, 사암을 포함한 여러 종류의 돌 스컬프팅을 지속적으로 추가하고 있습니다.", "body"))
    story.append(Spacer(1, 1.5*mm))
    for text in [
        "형태와 실루엣을 먼저 명확히 설계한 뒤, 재질별 마모·노화·사용 흔적을 근거 있게 표현",
        "하드서피스와 유기적 스컬프팅을 병행하고, PBR 텍스처와 라이팅으로 재질의 차이를 효과적으로 전달",
        "모델링 → UV → 베이킹 → 텍스처링 → 렌더링 → UE5 씬 세팅의 전 과정을 직접 수행",
    ]:
        story.append(bullet(text))

    story.append(section_heading("구매 에셋 활용 및 컨버팅", "Asset Conversion", 3.5*mm))
    conversion_data = [[
        [P("01  분석", "label"), Spacer(1, 1*mm), P("원본 구조·품질·재사용 범위 점검", "body_small")],
        [P("02  수정", "label"), Spacer(1, 1*mm), P("모델·UV·텍스처·머티리얼 보완", "body_small")],
        [P("03  적용", "label"), Spacer(1, 1*mm), P("피벗·충돌·LOD·최적화 후 UE5 적용", "body_small")],
    ]]
    conversion = Table(conversion_data, colWidths=[58*mm, 59*mm, 59*mm])
    conversion.setStyle(grid_style([("BACKGROUND", (1, 0), (1, 0), PALE)], padding=6))
    story.append(conversion)

    story.append(section_heading("기술 역량", "Technical Skills", 3.5*mm))
    skills_data = [[P("도구", "label"), P("활용 역량", "label")]]
    skills_data += [
        [P("<b>3ds Max · RizomUV</b>", "body_small"), P("로우·하이폴 모델링, 리토폴로지, UV 언랩과 패킹, 게임 에셋 최적화", "body_small")],
        [P("<b>ZBrush · Marvelous</b>", "body_small"), P("하이폴 스컬프팅, 석재·자연물 디테일, 패브릭 제작과 자연스러운 주름 표현", "body_small")],
        [P("<b>Substance 3D Painter</b>", "body_small"), P("PBR 텍스처링, 베이킹, 재질별 마모·노화·사용 흔적 표현", "body_small")],
        [P("<b>Marmoset · Unreal 5</b>", "body_small"), P("베이킹, 라이팅과 렌더링, 에셋 임포트, 머티리얼, 씬 세팅", "body_small")],
        [P("<b>AI 도구</b>", "body_small"), P("레퍼런스 조사, 아이디어 정리와 반복 업무 효율화에 활용", "body_small")],
    ]
    skills = Table(skills_data, colWidths=[44*mm, 132*mm], repeatRows=1)
    skills.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 2), (-1, 2), PALE),
        ("BACKGROUND", (0, 4), (-1, 4), PALE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ]))
    story.append(skills)

    story.append(PageBreak())

    # PAGE 3
    story.extend([P("SELF-INTRODUCTION", "page_title"), P("게임의 세계를 설득력 있게 만드는 3D 배경 아티스트", "page_sub")])
    intro_paragraphs = [
        ("지원 동기와 작업 방향", "게임을 즐기는 것을 넘어, 게임 속 공간과 오브젝트가 어떤 과정으로 만들어지는지에 깊은 관심을 가지면서 3D 배경 아티스트를 목표로 하게 되었습니다. 특히 모델링 작업 자체를 좋아하며, 형태를 분석하고 실루엣을 다듬어 하나의 오브젝트를 완성해 나가는 과정에서 큰 즐거움을 느낍니다. 플레이어가 작은 프랍 하나에서도 세계관과 이야기를 느끼고, 게임 속 공간에 더욱 깊이 몰입할 수 있도록 설득력 있는 환경을 만드는 것이 저의 목표입니다."),
        ("포트폴리오와 제작 역량", "포트폴리오를 제작하며 무기, 가구, 석재, 건축 프랍 등 다양한 소재와 형태의 오브젝트를 경험했습니다. 최근에는 복합적인 구조와 재질을 가진 마차를 제작하고 있으며, 사암을 비롯한 여러 종류의 돌을 지속적으로 스컬프팅하면서 자연물의 형태와 표면을 관찰하고 표현하는 역량을 넓히고 있습니다. 단순히 디테일을 많이 추가하기보다는 실루엣과 구조를 먼저 명확히 하고, 재질마다 다른 마모와 노화, 사용 흔적이 자연스럽게 드러나도록 작업하고 있습니다. 또한 모델링부터 UV, 텍스처링, 베이킹, 라이팅과 UE5 씬 세팅까지 환경 제작의 전 과정을 직접 진행할 수 있습니다."),
        ("구매 에셋 활용 및 컨버팅", "구매 데이터를 활용하고 프로젝트에 맞게 컨버팅하는 능력도 갖추고 있습니다. 구매 에셋을 그대로 배치하는 데 그치지 않고, 원본 데이터의 구조와 품질을 분석한 뒤 프로젝트의 아트 방향과 엔진 규격에 맞게 모델과 UV, 텍스처, 머티리얼을 수정합니다. 스케일과 피벗, 충돌, LOD 및 최적화 요소를 점검하고, 서로 다른 제작 방식의 데이터를 일관된 품질과 규격으로 정리해 UE5 환경에 적용할 수 있습니다. 이를 통해 제한된 제작 일정 안에서도 기존 데이터를 효율적으로 활용하면서 필요한 부분은 직접 보완하는 유연한 작업 방식을 익혔습니다."),
        ("실무형 협업 경험", "현재는 현직자 15명이 함께하는 인디게임 개발 팀 프로젝트에 프랍 모델러로 참여하고 있습니다. 인디 프로젝트이지만 파트별 업무 분담과 일정 관리, 작업물 리뷰와 피드백, 엔진 적용 및 수정 과정을 거치는 실무와 유사한 프로세스로 진행되고 있습니다. 작업 의도와 진행 상황을 명확하게 공유하고, 다른 파트의 요구사항을 확인해 수정 방향을 조율하는 과정에서 협업과 의사소통의 중요성을 배웠습니다. 피드백을 방어적으로 받아들이기보다 프로젝트의 완성도를 높이기 위한 과정으로 생각하며, 팀원들과 적극적으로 의견을 나누고 책임감 있게 작업을 마무리하고 있습니다."),
        ("성장 방향", "게임과 모델링을 좋아하는 마음을 꾸준한 작업과 학습으로 이어가며, 새로운 제작 방식과 피드백을 빠르게 흡수하는 아티스트가 되고자 합니다. 맡은 오브젝트의 완성도뿐 아니라 전체 게임 환경과 제작 과정까지 고려하며, 플레이어가 자연스럽게 믿고 몰입할 수 있는 세계를 만드는 3D 배경 아티스트로 성장하겠습니다."),
    ]
    for idx, (label, text) in enumerate(intro_paragraphs, 1):
        heading = Table([[P(f"{idx:02d}", "intro_head_num"), P(label, "intro_head")]], colWidths=[11*mm, 165*mm], hAlign="LEFT", spaceBefore=2.1*mm if idx > 1 else 1*mm, spaceAfter=1.2*mm)
        heading.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(heading)
        story.append(P(text, "body_intro"))

    story.append(Spacer(1, 3*mm))
    sign_style = ParagraphStyle("sign", parent=S["body_small"], fontName="MalgunBold", textColor=MUTED, alignment=TA_RIGHT)
    story.append(Paragraph("최지훈  ·  3D Background &amp; Prop Artist", sign_style))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
