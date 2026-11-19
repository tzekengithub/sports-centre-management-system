"""Phase 2: adds a red circle, a red arrow and a number label to copies of the
REAL screenshots for Figures 55-75 (the user-manual guide marks). It reads
Screenshots_Real/boxes.json (the real widget positions recorded while the
screenshots were taken) and writes to Screenshots_Real/Annotated/. The
originals are never changed, and nothing else in the picture is touched."""

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "Screenshots_Real")
ANNOTATED = os.path.join(OUT_DIR, "Annotated")
RED = (220, 30, 30)


def draw_marks(image, box, number):
    """Circle round the target, an arrow pointing at it, and a number badge."""
    draw = ImageDraw.Draw(image)
    centre_x = box["x"] + box["w"] / 2
    centre_y = box["y"] + box["h"] / 2
    radius_x = box["w"] / 2 + 12
    radius_y = box["h"] / 2 + 10
    draw.ellipse((centre_x - radius_x, centre_y - radius_y, centre_x + radius_x, centre_y + radius_y),
                 outline=RED, width=4)
    # the arrow comes from the lower right (or the upper left near the bottom edge)
    length = 70
    if centre_y + radius_y + length * 0.7 < image.height - 5 and centre_x + radius_x + length * 0.7 < image.width - 5:
        direction = (1, 1)
    elif centre_y - radius_y - length * 0.7 > 5:
        direction = (1, -1)
    else:
        direction = (-1, -1)
    tip_x = centre_x + direction[0] * (radius_x * 0.75 + 4)
    tip_y = centre_y + direction[1] * (radius_y * 0.75 + 4)
    tail_x = tip_x + direction[0] * length * 0.7
    tail_y = tip_y + direction[1] * length * 0.7
    draw.line((tail_x, tail_y, tip_x, tip_y), fill=RED, width=5)
    angle = math.atan2(tip_y - tail_y, tip_x - tail_x)
    for turn in (math.radians(155), math.radians(-155)):
        draw.line((tip_x, tip_y, tip_x + 18 * math.cos(angle + turn), tip_y + 18 * math.sin(angle + turn)),
                  fill=RED, width=5)
    # number badge at the arrow's tail
    try:
        font = ImageFont.truetype("arialbd.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    badge_x, badge_y = tail_x, tail_y
    draw.ellipse((badge_x - 15, badge_y - 15, badge_x + 15, badge_y + 15), fill=RED)
    draw.text((badge_x, badge_y), str(number), fill="white", font=font, anchor="mm")


def main():
    """Annotate Figures 55-75 from boxes.json."""
    with open(os.path.join(OUT_DIR, "boxes.json"), encoding="utf-8") as handle:
        boxes = json.load(handle)
    os.makedirs(ANNOTATED, exist_ok=True)
    done = []
    for number in range(55, 76):
        name = f"Figure_{number}.png"
        if name not in boxes:
            print("no recorded target for", name)
            continue
        image = Image.open(os.path.join(OUT_DIR, name)).convert("RGB")
        draw_marks(image, boxes[name], 1)
        image.save(os.path.join(ANNOTATED, name))
        done.append(name)
    print("annotated", len(done), "pictures into", ANNOTATED)


if __name__ == "__main__":
    main()
