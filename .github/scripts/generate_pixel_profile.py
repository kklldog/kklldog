#!/usr/bin/env python3
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1200, 420
FRAMES_PER_SCENE = 16
DURATION_MS = 250

BG = "#101426"
PANEL = "#171c35"
MIDNIGHT = "#202945"
BUILDING = "#252c4a"
WINDOW = "#384363"
TEXT = "#f2f4ff"
MUTED = "#9eacd2"
GOLD = "#f3d37a"
MINT = "#70e1d0"
PINK = "#ff6b7a"
PURPLE = "#c49bff"

FONT_DIR = Path("/usr/share/fonts/truetype/freefont")
FONT_REGULAR = FONT_DIR / "FreeMono.ttf"
FONT_BOLD = FONT_DIR / "FreeMonoBold.ttf"


def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(str(path), size)


def label(draw, xy, text, color=MINT, size=17):
    draw.text(xy, text, font=font(size, True), fill=color)


def base_scene(frame_index):
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    draw.rectangle((8, 8, WIDTH - 8, HEIGHT - 8), outline=GOLD, width=6)
    draw.rectangle((12, 12, WIDTH - 12, 260), fill="#11172b")

    stars = [
        (98, 56), (168, 102), (278, 49), (395, 76), (505, 48), (623, 92),
        (702, 58), (858, 80), (962, 45), (1090, 100), (1128, 56), (310, 142),
    ]
    for index, (x, y) in enumerate(stars):
        size = 6 if index % 3 == 0 else 4
        bright = (index + frame_index) % 4 != 0
        draw.rectangle((x, y, x + size, y + size), fill=GOLD if bright else "#384363")

    # A pixel moon and its horizontal scanlines.
    draw.rectangle((902, 42, 1002, 142), fill="#a96aa7")
    draw.rectangle((890, 54, 1014, 130), fill="#a96aa7")
    draw.rectangle((914, 46, 990, 134), fill=PINK)
    for y in (95, 106, 118, 130):
        draw.rectangle((886, y, 1018, y + 3), fill="#11172b")

    buildings = [
        (0, 212, 84, 280), (84, 232, 150, 280), (150, 186, 218, 280),
        (218, 224, 294, 280), (294, 142, 372, 280), (372, 205, 432, 280),
        (432, 180, 520, 280), (520, 218, 586, 280), (586, 160, 664, 280),
        (664, 200, 728, 280), (728, 124, 820, 280), (820, 192, 888, 280),
        (888, 170, 970, 280), (970, 202, 1050, 280), (1050, 154, 1200, 280),
    ]
    for left, top, right, bottom in buildings:
        draw.rectangle((left, top, right, bottom), fill=BUILDING)
        for wx in range(left + 14, right - 8, 28):
            for wy in range(top + 14, bottom - 8, 28):
                if (wx + wy + frame_index // 2) % 5:
                    draw.rectangle((wx, wy, wx + 8, wy + 8), fill=WINDOW)

    draw.rectangle((12, 280, WIDTH - 12, HEIGHT - 12), fill=PANEL)
    for y in (315, 350, 385):
        draw.line((12, y, WIDTH - 12, y), fill=BUILDING, width=2)
    for x in range(70, WIDTH, 70):
        draw.line((x, 280, x, HEIGHT - 12), fill=BUILDING, width=2)

    # A dark HUD keeps small text legible against the animated city.
    draw.rectangle((44, 43, 744, 334), fill="#11172b", outline="#384363", width=3)
    draw.rectangle((44, 43, 48, 334), fill=MINT)
    draw.rectangle((755, 43, 1128, 151), fill="#11172b", outline="#384363", width=3)
    label(draw, (778, 59), "NIGHT CITY  /  ONLINE", MINT, 15)
    label(draw, (778, 91), "SYSTEM STATUS:  READY", GOLD, 15)
    draw.rectangle((1101, 62, 1111, 72), fill=MINT if frame_index % 4 < 2 else WINDOW)

    return image


def draw_character(draw, frame_index):
    bob = (0, 0, -4, -4, -8, -8, -4, -4)[frame_index % 8]
    top = 184 + bob
    left = 1090

    draw.rectangle((left + 18, top, left + 62, top + 44), fill=GOLD)
    draw.rectangle((left + 10, top + 8, left + 70, top + 44), fill=GOLD)
    draw.rectangle((left + 18, top + 18, left + 26, top + 26), fill=BG)
    draw.rectangle((left + 46, top + 18, left + 54, top + 26), fill=BG)
    draw.rectangle((left + 30, top + 34, left + 42, top + 40), fill=PINK)
    draw.rectangle((left + 14, top + 44, left + 66, top + 98), fill=MINT)
    draw.rectangle((left, top + 52, left + 14, top + 90), fill=MINT)
    draw.rectangle((left + 66, top + 52, left + 80, top + 90), fill=MINT)
    draw.rectangle((left + 20, top + 98, left + 36, top + 128), fill=PURPLE)
    draw.rectangle((left + 44, top + 98, left + 60, top + 128), fill=PURPLE)
    draw.rectangle((left + 14, top + 122, left + 38, top + 132), fill=GOLD)
    draw.rectangle((left + 42, top + 122, left + 66, top + 132), fill=GOLD)


def draw_terminal(draw, frame_index, scene_index):
    left, top = 798, 182
    draw.rectangle((left, top, left + 270, top + 142), fill="#090d19")
    draw.rectangle((left + 8, top + 8, left + 262, top + 134), fill=MIDNIGHT)
    draw.rectangle((left + 8, top + 8, left + 262, top + 30), fill="#35405f")
    for offset, color in ((0, PINK), (16, GOLD), (32, MINT)):
        draw.rectangle((left + 18 + offset, top + 15, left + 26 + offset, top + 23), fill=color)

    code = [
        [(52, 48, 96, MINT), (108, 48, 164, MUTED), (52, 64, 118, GOLD), (130, 64, 198, MUTED)],
        [(38, 48, 104, GOLD), (116, 48, 204, MUTED), (38, 64, 152, MINT), (166, 64, 224, MUTED)],
        [(52, 48, 116, PURPLE), (128, 48, 214, MUTED), (38, 64, 102, MINT), (114, 64, 184, GOLD)],
        [(38, 48, 108, MINT), (120, 48, 184, MUTED), (52, 64, 142, GOLD), (154, 64, 220, PURPLE)],
    ][scene_index]
    for x1, y1, x2, color in code:
        draw.rectangle((left + x1, top + y1, left + x2, top + y1 + 6), fill=color)
    draw.rectangle((left + 38, top + 81, left + 38 + (frame_index % 8) * 18, top + 87), fill=PURPLE)
    draw.rectangle((left + 24, top + 98, left + 32, top + 106), fill=GOLD)
    if frame_index % 2 == 0:
        draw.rectangle((left + 40, top + 98, left + 84, top + 104), fill=MINT)


SCENES = [
    {
        "kicker": "PLAYER 01  /  PROFILE",
        "title": "MINJIE ZHOU",
        "lines": [
            (".NET ENGINEER  /  OPEN-SOURCE MAKER", TEXT),
            ("SUZHOU, CHINA", MUTED),
            ("MICROSOFT MVP 2025", GOLD),
        ],
        "terminal": "ABOUT",
    },
    {
        "kicker": "QUEST LOG  /  SELECTED BUILDS",
        "title": "OPEN-SOURCE QUESTS",
        "lines": [
            ("AGILECONFIG  /  DISTRIBUTED CONFIG", MINT),
            ("AGILEAI  /  .NET AI SDK", PURPLE),
            ("AGILEDT  /  RELIABLE MESSAGING", GOLD),
            ("+ JAVA CLIENT", TEXT),
        ],
        "terminal": "PROJECTS",
    },
    {
        "kicker": "SKILL TREE  /  ACTIVE LOADOUT",
        "title": "BUILT WITH .NET",
        "lines": [
            ("C# / ASP.NET  /  MAIN STACK", MINT),
            ("JAVASCRIPT / TYPESCRIPT", GOLD),
            ("JAVA", PURPLE),
            ("CURRENT QUEST: LEARN ENGLISH", TEXT),
        ],
        "terminal": "SKILLS",
    },
    {
        "kicker": "ACHIEVEMENT UNLOCKED",
        "title": "MICROSOFT MVP",
        "lines": [
            ("MICROSOFT MVP 2025", GOLD),
            ("CREATING BUGS SINCE 2010", PINK),
            ("BUILD  /  SHIP  /  REPEAT", MINT),
            ("BLOG: CNBLOGS.COM/KKLLDOG", TEXT),
        ],
        "terminal": "AWARDS",
    },
]


def draw_scene(scene, scene_index, frame_index):
    image = base_scene(frame_index)
    draw = ImageDraw.Draw(image)

    label(draw, (68, 59), scene["kicker"], MINT, 19)
    title_size = 48 if scene_index != 1 else 40
    title_font = font(title_size, True)
    draw.text((68, 98), scene["title"], font=title_font, fill="#7a395f")
    draw.text((64, 94), scene["title"], font=title_font, fill=GOLD)
    draw.rectangle((68, 159, 470, 164), fill=PINK)

    y = 179
    for text, color in scene["lines"]:
        draw.rectangle((72, y + 6, 80, y + 14), fill=color)
        draw.text((94, y), text, font=font(23, True), fill=color)
        y += 35

    draw_terminal(draw, frame_index, scene_index)
    label(draw, (798, 338), scene["terminal"] + "  //  BUILD  •  SHIP  •  REPEAT", MINT, 13)
    draw_character(draw, frame_index)

    draw.rectangle((60, 372, 508, 380), fill="#35405f")
    draw.rectangle((60, 372, 60 + int(frame_index / (FRAMES_PER_SCENE - 1) * 448), 380), fill=MINT)
    for index in range(len(SCENES)):
        color = GOLD if index == scene_index else "#4b567a"
        x = 550 + index * 24
        draw.rectangle((x, 370, x + 12, 382), fill=color)

    label(draw, (665, 364), "0" + str(scene_index + 1) + " / 04", GOLD, 16)
    x = 840 + frame_index * 14
    draw.rectangle((x, 374, x + 24, 380), fill=MINT)
    draw.rectangle((x + 8, 368, x + 16, 386), fill=GOLD)
    draw.rectangle((x - 12, 376, x - 4, 378), fill=PINK)
    draw.rectangle((8, 8, WIDTH - 8, HEIGHT - 8), outline=GOLD, width=6)
    return image.resize((600, 210), Image.Resampling.NEAREST).resize((WIDTH, HEIGHT), Image.Resampling.NEAREST)


def main():
    parser = argparse.ArgumentParser(description="Generate an animated pixel-art profile banner.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    frames = []
    for scene_index, scene in enumerate(SCENES):
        for frame_index in range(FRAMES_PER_SCENE):
            frames.append(draw_scene(scene, scene_index, frame_index))

    frames[0].save(
        args.output,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )


if __name__ == "__main__":
    main()
