from pathlib import Path
import textwrap

from PIL import Image
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
TMP = ROOT / "tmp" / "pdfs" / "prepared"
OUT = ROOT / "output" / "pdf" / "Jihoon_Choi_3D_Portfolio.pdf"
QR = ROOT / "assets" / "jihoon-portfolio-qr.png"
PORTFOLIO_URL = "https://jihoon-02.github.io/chaihk70.github.io/"
EMAIL = "chaihk70@gmail.com"

PAGE_W, PAGE_H = landscape(A4)
BG = HexColor("#020305")
PANEL = HexColor("#0B0D10")
INK = HexColor("#F4F0E8")
MUTED = HexColor("#9B9CA0")
ACCENT = HexColor("#27A9FF")
LINE = Color(1, 1, 1, alpha=0.12)


pdfmetrics.registerFont(TTFont("Malgun", r"C:\Windows\Fonts\malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", r"C:\Windows\Fonts\malgunbd.ttf"))


def prepare(src: str, name: str, max_px: int = 1800) -> Path:
    TMP.mkdir(parents=True, exist_ok=True)
    source = ROOT / src
    target = TMP / f"{name}.jpg"
    with Image.open(source) as im:
        im = im.convert("RGB")
        im.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
        im.save(target, "JPEG", quality=88, optimize=True, progressive=True)
    return target


def image_size(path: Path):
    with Image.open(path) as im:
        return im.size


def draw_cover_image(c, path: Path, x, y, w, h, radius=0):
    iw, ih = image_size(path)
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    c.saveState()
    clip = c.beginPath()
    if radius:
        clip.roundRect(x, y, w, h, radius)
    else:
        clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(str(path), dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")
    c.restoreState()


def draw_contain_image(c, path: Path, x, y, w, h):
    iw, ih = image_size(path)
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.setFillColor(PANEL)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.drawImage(str(path), x + (w - dw) / 2, y + (h - dh) / 2,
                dw, dh, preserveAspectRatio=True, mask="auto")


def draw_rule(c, x1, y, x2):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(x1, y, x2, y)


def draw_footer(c, page_no):
    c.setFont("Malgun", 7.5)
    c.setFillColor(MUTED)
    c.drawString(36, 22, "JIHOON CHOI - 3D BACKGROUND & PROP ARTIST")
    c.drawRightString(PAGE_W - 36, 22, f"{page_no:02d} / 06")


def wrapped_lines(text, width_chars):
    return textwrap.wrap(text, width=width_chars, break_long_words=False, break_on_hyphens=False)


def draw_project_page(c, page_no, number, title, subtitle, pipeline, description,
                      main_img, side_img_1, side_img_2, contain_main=False):
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setFillColor(ACCENT)
    c.setFont("MalgunBold", 9)
    c.drawString(36, PAGE_H - 42, f"{number} / SELECTED WORK")

    c.setFillColor(INK)
    c.setFont("MalgunBold", 27)
    c.drawString(36, PAGE_H - 76, title)
    c.setFont("Malgun", 10)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - 36, PAGE_H - 66, subtitle.upper())
    c.drawRightString(PAGE_W - 36, PAGE_H - 82, pipeline)
    draw_rule(c, 36, PAGE_H - 96, PAGE_W - 36)

    main_x, main_y, main_w, main_h = 36, 144, 516, 338
    side_x, side_w = 564, PAGE_W - 600
    gap = 10
    side_h = (main_h - gap) / 2
    if contain_main:
        draw_contain_image(c, main_img, main_x, main_y, main_w, main_h)
    else:
        draw_cover_image(c, main_img, main_x, main_y, main_w, main_h)
    draw_cover_image(c, side_img_1, side_x, main_y + side_h + gap, side_w, side_h)
    draw_cover_image(c, side_img_2, side_x, main_y, side_w, side_h)

    c.setFont("Malgun", 10.2)
    c.setFillColor(INK)
    y = 118
    for line in wrapped_lines(description, 92)[:3]:
        c.drawString(36, y, line)
        y -= 15

    c.setFillColor(ACCENT)
    c.setFont("MalgunBold", 8.5)
    c.drawRightString(PAGE_W - 36, 78, "VIEW FULL PROJECT ONLINE")
    c.setFillColor(MUTED)
    c.setFont("Malgun", 8)
    c.drawRightString(PAGE_W - 36, 64, PORTFOLIO_URL)
    c.linkURL(PORTFOLIO_URL, (PAGE_W - 290, 58, PAGE_W - 36, 86), relative=0, thickness=0)
    draw_footer(c, page_no)
    c.showPage()


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    images = {
        "axe_main": prepare("images/Personal/20260825_Stylized Axe/Axe_main.png", "axe_main"),
        "axe_1": prepare("images/Personal/20260825_Stylized Axe/Axe_1.png", "axe_1"),
        "axe_maps": prepare("images/Personal/20260825_Stylized Axe/Axe_Maps.png", "axe_maps"),
        "axegun_main": prepare("images/Personal/20260710_Axegun/Main.png", "axegun_main"),
        "axegun_2": prepare("images/Personal/20260710_Axegun/T_2.png", "axegun_2"),
        "axegun_maps": prepare("images/Personal/20260710_Axegun/Maps2.png", "axegun_maps"),
        "rock_main": prepare("images/Personal/20260710_Zbrush Study/Rock-B_main1.png", "rock_main"),
        "rock_wire": prepare("images/Personal/20260710_Zbrush Study/Rock-B_wire.png", "rock_wire"),
        "rock_a": prepare("images/Personal/20260710_Zbrush Study/Rock-A_main.png", "rock_a"),
        "fire_main": prepare("images/Personal/20260302_Antique Fireplace/main.png", "fire_main"),
        "fire_1": prepare("images/Personal/20260302_Antique Fireplace/shot_0001_Ultra.png", "fire_1"),
        "fire_maps": prepare("images/Personal/20260302_Antique Fireplace/maps.png", "fire_maps"),
        "windup_main": prepare("images/Personal/20260902_WeIND UP/Main.png", "windup_main"),
        "windup_1": prepare("images/Personal/20260902_WeIND UP/Ch1-3.png", "windup_1"),
        "windup_2": prepare("images/Personal/20260902_WeIND UP/Ch2-2.png", "windup_2"),
    }

    c = canvas.Canvas(str(OUT), pagesize=landscape(A4), pageCompression=1)
    c.setTitle("Jihoon Choi - 3D Background & Prop Artist Portfolio")
    c.setAuthor("Jihoon Choi")
    c.setSubject("3D Background and Prop Art Portfolio")

    # Cover
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, PAGE_H - 9, PAGE_W, 9, fill=1, stroke=0)
    c.setFont("Malgun", 10)
    c.setFillColor(ACCENT)
    c.drawString(36, PAGE_H - 48, "3D BACKGROUND ARTIST - ENVIRONMENT - PROPS")
    c.setFillColor(INK)
    c.setFont("MalgunBold", 42)
    c.drawString(36, PAGE_H - 101, "JIHOON CHOI")
    c.setFont("MalgunBold", 20)
    c.setFillColor(ACCENT)
    c.drawString(38, PAGE_H - 133, "3D BACKGROUND & PROP ARTIST")
    c.setFont("Malgun", 10)
    c.setFillColor(MUTED)
    c.drawString(38, PAGE_H - 160, "3ds Max  /  ZBrush  /  Substance Painter  /  Marmoset  /  Unreal Engine 5  /  RizomUV")
    c.drawString(38, PAGE_H - 180, EMAIL)

    qr_size = 94
    qr_x, qr_y = PAGE_W - 138, PAGE_H - 158
    c.setFillColor(INK)
    c.roundRect(qr_x - 8, qr_y - 8, qr_size + 16, qr_size + 16, 4, fill=1, stroke=0)
    c.drawImage(str(QR), qr_x, qr_y, qr_size, qr_size, preserveAspectRatio=True, mask="auto")
    c.linkURL(PORTFOLIO_URL, (qr_x - 8, qr_y - 8, qr_x + qr_size + 8, qr_y + qr_size + 8), relative=0, thickness=0)
    c.setFont("MalgunBold", 7.5)
    c.setFillColor(ACCENT)
    c.drawCentredString(qr_x + qr_size / 2, qr_y - 21, "SCAN TO VIEW FULL PORTFOLIO")

    collage_y, collage_h = 46, 310
    gap = 7
    col_w = (PAGE_W - 72 - gap * 2) / 3
    draw_cover_image(c, images["axe_main"], 36, collage_y, col_w, collage_h)
    draw_cover_image(c, images["axegun_main"], 36 + col_w + gap, collage_y, col_w, collage_h)
    draw_cover_image(c, images["rock_main"], 36 + (col_w + gap) * 2, collage_y, col_w, collage_h)
    c.setFillColor(Color(0, 0, 0, alpha=0.32))
    c.rect(36, collage_y, PAGE_W - 72, 42, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("MalgunBold", 9)
    c.drawString(49, collage_y + 16, PORTFOLIO_URL)
    c.linkURL(PORTFOLIO_URL, (36, collage_y, PAGE_W - 36, collage_y + 42), relative=0, thickness=0)
    draw_footer(c, 1)
    c.showPage()

    draw_project_page(
        c, 2, "01", "STYLIZED AXE", "Stylized Weapon",
        "3ds Max - RizomUV - ZBrush - Substance Painter - Marmoset - Photoshop",
        "강한 실루엣과 과장된 형태감을 중심으로 제작했습니다. 게임 에셋을 고려해 형태를 유지하면서 불필요한 면을 줄이고, 필요한 부분에 폴리곤을 효율적으로 배분했습니다.",
        images["axe_main"], images["axe_1"], images["axe_maps"]
    )
    draw_project_page(
        c, 3, "02", "AXEGUN", "Concept Weapon",
        "3ds Max - RizomUV - Substance Painter - Marmoset - Photoshop",
        "도끼와 총을 결합한 판타지 무기입니다. 넓은 날과 기계식 발사부를 하나의 실루엣으로 구성하고, 목재와 금속, 가죽, 황동의 광택과 마모 차이를 표현했습니다.",
        images["axegun_main"], images["axegun_2"], images["axegun_maps"]
    )
    draw_project_page(
        c, 4, "03", "ZBRUSH STUDY", "Stone Sculpting Study",
        "3ds Max - ZBrush - Substance Painter - Marmoset - Photoshop",
        "여러 석조 구조물을 통해 스컬프팅과 석재 표현을 연습했습니다. 깨진 모서리와 풍화된 표면을 조형해 오랜 시간 노출된 돌의 무게감과 재질을 표현했습니다.",
        images["rock_main"], images["rock_wire"], images["rock_a"]
    )
    draw_project_page(
        c, 5, "04", "ANTIQUE FIREPLACE", "Environment Prop",
        "3ds Max - Substance Painter - Marmoset - Unreal Engine 5 - Photoshop",
        "고풍스러운 서재를 상상해 벽난로와 주변 공간을 구성했습니다. 고전 양식의 장식과 소품, 빛의 세기와 색을 조율해 오래된 공간의 격식과 따뜻한 분위기를 표현했습니다.",
        images["fire_main"], images["fire_1"], images["fire_maps"], contain_main=True
    )
    draw_project_page(
        c, 6, "05", "WeIND UP", "Team Project - 3D Prop Modeling",
        "3ds Max - RizomUV - Substance Painter - Unreal Engine 5",
        "개발 중인 2인 협동 퍼즐 게임의 프랍 모델러로 참여했습니다. 챕터별 분위기와 콘셉트에 맞는 프랍을 제작하고, 실제 게임 데이터에 필요한 최적화와 실루엣 표현을 함께 고려했습니다.",
        images["windup_main"], images["windup_1"], images["windup_2"]
    )

    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
