from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

OUT = Path("/Users/kim/projects/_meta/agents/컨텐츠/outputs/approved")
W = H = 1080
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
SOURCE = "엔카 수집 데이터 | 2026년 W18~W23 | 매물 중앙값"

BG = "#F6F8FB"
INK = "#172033"
MUTED = "#6B7280"
BLUE = "#1F5EFF"
NAVY = "#102A56"
GREEN = "#16A34A"
RED = "#E11D48"
AMBER = "#D97706"
LINE = "#D9E1EF"
WHITE = "#FFFFFF"


def font(size, index=0):
    return ImageFont.truetype(FONT, size=size, index=index)


F = {
    "brand": font(26),
    "eyebrow": font(30),
    "title": font(72),
    "title2": font(58),
    "h1": font(52),
    "h2": font(38),
    "body": font(31),
    "body2": font(28),
    "small": font(23),
    "num": font(47),
    "big": font(86),
}


def draw_round(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, fill=INK, f="body", anchor=None, align="left"):
    draw.text(xy, value, fill=fill, font=F[f], anchor=anchor, align=align)


def text_size(draw, value, f):
    box = draw.textbbox((0, 0), value, font=F[f])
    return box[2] - box[0], box[3] - box[1]


def wrap_korean(value, chars):
    out = []
    for paragraph in value.split("\n"):
        if not paragraph:
            out.append("")
            continue
        out.extend(textwrap.wrap(paragraph, width=chars, break_long_words=True, replace_whitespace=False))
    return "\n".join(out)


def base(card_no, title):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 18), fill=BLUE)
    text(d, (72, 58), "CADAM MARKET NOTE", BLUE, "brand")
    text(d, (1008, 58), f"{card_no}/5", MUTED, "brand", anchor="ra")
    text(d, (72, 1008), SOURCE, MUTED, "small")
    text(d, (1008, 1008), "0~10만km 전 구간 포함 가중평균", MUTED, "small", anchor="ra")
    text(d, (72, 122), title, INK, "h1")
    return img, d


def card1():
    img = Image.new("RGB", (W, H), "#EEF4FF")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H), fill="#EEF4FF")
    d.rounded_rectangle((650, 150, 1030, 420), radius=32, fill="#DBEAFE")
    d.rounded_rectangle((700, 215, 980, 390), radius=55, fill="#FFFFFF", outline="#BDD7FF", width=4)
    d.ellipse((750, 355, 810, 415), fill=NAVY)
    d.ellipse((880, 355, 940, 415), fill=NAVY)
    d.rectangle((770, 250, 920, 305), fill="#93C5FD")
    text(d, (72, 72), "CADAM MARKET NOTE", BLUE, "brand")
    text(d, (72, 180), "쏘렌토 HEV\n중고 시세", NAVY, "title")
    text(d, (72, 360), "지금 어떻게 움직이나?", INK, "title2")
    draw_round(d, (72, 535, 465, 625), 22, WHITE, "#C7D2FE", 2)
    text(d, (102, 558), "2026년 W18~W23", BLUE, "h2")
    draw_round(d, (72, 660, 1008, 870), 34, WHITE, "#D9E1EF", 2)
    text(d, (118, 706), "2022~2023년식은 완만한 하락", RED, "h2")
    text(d, (118, 780), "2024년식은 소폭 상승", GREEN, "h2")
    text(d, (72, 1008), SOURCE, MUTED, "small")
    return img


def metric_row(d, y, year, w18, w23, delta, pct, color):
    draw_round(d, (72, y, 1008, y + 138), 26, WHITE, "#DCE4F2", 2)
    text(d, (105, y + 34), year, INK, "h2")
    text(d, (352, y + 36), f"{w18}", MUTED, "body")
    text(d, (497, y + 36), "->", MUTED, "body")
    text(d, (565, y + 34), f"{w23}만원", INK, "h2")
    text(d, (957, y + 32), f"{delta}만원", color, "h2", anchor="ra")
    text(d, (957, y + 83), f"({pct})", color, "body2", anchor="ra")


def card2():
    img, d = base(2, "시세 변화 W18→W23")
    text(d, (72, 192), "2024년식은 소폭 상승, 2022~2023년식은 완만한 하락", NAVY, "h2")
    metric_row(d, 300, "2022년식", "3,217", "3,124", "-93", "-2.9%", RED)
    metric_row(d, 468, "2023년식", "3,786", "3,706", "-80", "-2.1%", RED)
    metric_row(d, 636, "2024년식", "4,158", "4,211", "+53", "+1.3%", GREEN)
    draw_round(d, (72, 835, 1008, 930), 24, "#E8F1FF", "#BDD7FF", 2)
    text(d, (104, 862), "저주행·트림별로 실제 매물가는 달라질 수 있습니다.", NAVY, "body2")
    return img


def inventory_row(d, y, year, before, after, delta, pct, width, color):
    text(d, (92, y), year, INK, "h2")
    draw_round(d, (265, y + 12, 845, y + 56), 20, "#E5EAF3")
    draw_round(d, (265, y + 12, 265 + width, y + 56), 20, color)
    text(d, (878, y + 2), f"{before}→{after}건", INK, "body2")
    text(d, (878, y + 42), f"{delta}건 ({pct})", color, "small")


def card3():
    img, d = base(3, "매물 수 변화")
    text(d, (72, 192), "전 연식 매물 감소. 선택지는 좁아지는 중입니다.", NAVY, "h2")
    inventory_row(d, 310, "2022", 581, 508, -73, "-12.6%", 506, BLUE)
    inventory_row(d, 450, "2023", 399, 359, -40, "-10.0%", 358, BLUE)
    inventory_row(d, 590, "2024", 350, 286, -64, "-18.3%", 285, AMBER)
    draw_round(d, (72, 780, 1008, 925), 30, WHITE, "#DCE4F2", 2)
    text(d, (110, 822), "2024년식 매물 감소 폭이 가장 큽니다.", AMBER, "h2")
    text(d, (110, 878), "가격 흐름과 함께 원하는 트림의 재고도 확인해야 합니다.", INK, "body2")
    return img


def temp_block(d, box, year, price, count, note, color):
    draw_round(d, box, 26, WHITE, "#DCE4F2", 2)
    x1, y1, x2, y2 = box
    d.rectangle((x1, y1, x1 + 12, y2), fill=color)
    text(d, (x1 + 38, y1 + 30), year, color, "h2")
    text(d, (x1 + 38, y1 + 82), price, INK, "num")
    text(d, (x1 + 38, y1 + 148), f"매물 {count}", MUTED, "body2")
    text(d, (x1 + 38, y1 + 190), wrap_korean(note, 16), INK, "small")


def card4():
    img, d = base(4, "연식별 시세 온도차")
    text(d, (72, 192), "W23 기준, 예산대와 선택 폭이 다릅니다.", NAVY, "h2")
    temp_block(d, (72, 280, 520, 560), "2022년식", "약 3,100만원대", "508건", "선택 폭이 가장 넓은 구간", BLUE)
    temp_block(d, (560, 280, 1008, 560), "2023년식", "약 3,700만원대", "359건", "가격과 연식 균형 구간", GREEN)
    temp_block(d, (72, 600, 520, 880), "2024년식", "약 4,200만원대", "286건", "소폭 상승, 재고 감소 빠름", AMBER)
    temp_block(d, (560, 600, 1008, 880), "2025년식", "참고 수준", "120건", "표본·트림 편차 주의", "#EA580C")
    return img


def guide_item(d, y, label, title, body, color):
    draw_round(d, (72, y, 1008, y + 180), 28, WHITE, "#DCE4F2", 2)
    draw_round(d, (104, y + 38, 178, y + 112), 20, color)
    text(d, (141, y + 53), label, WHITE, "h2", anchor="ma")
    text(d, (210, y + 35), title, color, "h2")
    text(d, (210, y + 88), wrap_korean(body, 31), INK, "body2")


def card5():
    img, d = base(5, "구매 판단 가이드")
    text(d, (72, 192), "내 상황에 맞는 연식을 고르는 관점입니다.", NAVY, "h2")
    guide_item(d, 290, "1", "가격 방어 중인 2024년식", "6주간 53만원 상승. 단, 매물 감소 속도가 빨라 선택지가 줄고 있습니다.", GREEN)
    guide_item(d, 500, "2", "선택 폭이 넓은 2022년식", "W23 기준 508건. 3,100만원대 진입 가능성이 있는 구간입니다.", BLUE)
    guide_item(d, 710, "3", "2025년식은 개별 매물 확인", "표본이 적고 트림 편차가 커 단순 비교보다 조건별 확인이 필요합니다.", AMBER)
    return img


def save_all():
    cards = [card1(), card2(), card3(), card4(), card5()]
    paths = []
    for idx, img in enumerate(cards, start=1):
        path = OUT / f"cardnews-sorento-hev-usedprice-20260604-{idx:02d}.png"
        img.save(path, "PNG")
        paths.append(path)
    return paths


if __name__ == "__main__":
    for p in save_all():
        print(p)
