"""Step 2 of the numbered-marks job: draws numbered marks on copies of the REAL
screenshots in Screenshots_Real/Steps_Base/, using the real widget boxes
recorded by take_step_marks.py (boxes_steps.json). Output goes to
Screenshots_Real/Annotated_v2/. Nothing else in a picture is changed.
Each box gets a red rounded rectangle, a filled red number badge (white bold
number) and a short red arrow from the badge to the box. A badge is put on the
quietest spot beside the box (lowest pixel variance), never on another mark."""

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Screenshots_Real")
BASE = os.path.join(OUT, "Steps_Base")
V2 = os.path.join(OUT, "Annotated_v2")
RED = (220, 30, 30)
PAD = 4
RADIUS = 15
LINE = 4
BUSY_LIMIT = 14.0     # grayscale std-dev above this under a badge means "something is there"


def font():
    """Bold font for the badge number."""
    try:
        return ImageFont.truetype("arialbd.ttf", 19)
    except OSError:
        return ImageFont.load_default()


def padded(box):
    """The rectangle that will be drawn round a box."""
    return (box[0] - PAD, box[1] - PAD, box[0] + box[2] + PAD, box[1] + box[3] + PAD)


def intersects(a, b, margin=0):
    """True if rectangles (x1,y1,x2,y2) overlap."""
    return not (a[2] + margin <= b[0] or b[2] + margin <= a[0] or a[3] + margin <= b[1] or b[3] + margin <= a[1])


def busy(gray, region):
    """Std-dev of grayscale inside region: high means text or widgets are there."""
    left, top, right, bottom = [int(v) for v in region]
    left, top = max(0, left), max(0, top)
    right, bottom = min(gray.width, right), min(gray.height, bottom)
    if right - left < 2 or bottom - top < 2:
        return 999.0
    return ImageStat.Stat(gray.crop((left, top, right, bottom))).stddev[0]


def not_background(gray, region):
    """Fraction of pixels in region that differ from the region's main colour (any border, text or widget)."""
    left, top, right, bottom = [int(v) for v in region]
    left, top = max(0, left), max(0, top)
    right, bottom = min(gray.width, right), min(gray.height, bottom)
    if right - left < 2 or bottom - top < 2:
        return 1.0
    histogram = gray.crop((left, top, right, bottom)).histogram()
    mode = histogram.index(max(histogram))
    near = sum(histogram[max(0, mode - 3):mode + 4])
    return 1.0 - near / float(sum(histogram))


def candidates(rect):
    """Badge centres around a rectangle, each with the arrow's far end on the rectangle."""
    x1, y1, x2, y2 = rect
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    gap = RADIUS + 20
    spots = [
        (x1 - gap, mid_y, x1, mid_y), (x2 + gap, mid_y, x2, mid_y),
        (mid_x, y1 - gap, mid_x, y1), (mid_x, y2 + gap, mid_x, y2),
        (x1 - gap, y1 - gap, x1, y1), (x2 + gap, y1 - gap, x2, y1),
        (x1 - gap, y2 + gap, x1, y2), (x2 + gap, y2 + gap, x2, y2),
        (x1 + 20, y1 - gap, x1 + 20, y1), (x1 + 20, y2 + gap, x1 + 20, y2),
        (x2 - 20, y1 - gap, x2 - 20, y1), (x2 - 20, y2 + gap, x2 - 20, y2),
        (x1 - gap, mid_y - 18, x1, mid_y - 18), (x1 - gap, mid_y + 18, x1, mid_y + 18),
        (x2 + gap, mid_y - 18, x2, mid_y - 18), (x2 + gap, mid_y + 18, x2, mid_y + 18),
    ]
    # slide along each side to find a quiet spot (arrow goes to the nearest point of that side)
    for step in range(-4, 13):
        slide = x1 + (x2 - x1) * step / 8.0
        for_y = min(max(mid_y, y1), y2)
        spots.append((slide, y2 + gap, min(max(slide, x1), x2), y2))
        spots.append((slide, y1 - gap, min(max(slide, x1), x2), y1))
    for step in range(-2, 11):
        slide = y1 + (y2 - y1) * step / 8.0
        spots.append((x1 - gap, slide, x1, min(max(slide, y1), y2)))
        spots.append((x2 + gap, slide, x2, min(max(slide, y1), y2)))
    for extra in (50, 80, 120, 170):
        for step in range(-4, 13):
            slide = x1 + (x2 - x1) * step / 8.0
            spots.append((slide + extra, y2 + gap, x2, y2))
            spots.append((slide + extra, y1 - gap, x2, y1))
            spots.append((slide - extra, y2 + gap, x1, y2))
            spots.append((slide - extra, y1 - gap, x1, y1))
    return spots


def place_badge(gray, rect, all_rects, placed, size):
    """Choose the quietest free spot for this rectangle's badge. Returns (cx, cy, tx, ty, score)."""
    best = None
    for cx, cy, tx, ty in candidates(rect):
        badge = (cx - RADIUS - 1, cy - RADIUS - 1, cx + RADIUS + 1, cy + RADIUS + 1)
        if badge[0] < 2 or badge[1] < 2 or badge[2] > size[0] - 2 or badge[3] > size[1] - 2:
            continue
        blocked = False
        for other in all_rects:
            if intersects(badge, other, 2):
                blocked = True
        for other in placed:
            if intersects(badge, other, 3):
                blocked = True
        if blocked:
            continue
        # the arrow runs from the badge edge to (tx, ty)
        angle = math.atan2(ty - cy, tx - cx)
        start_x, start_y = cx + (RADIUS + 1) * math.cos(angle), cy + (RADIUS + 1) * math.sin(angle)
        arrow_box = (min(start_x, tx) - 2, min(start_y, ty) - 2, max(start_x, tx) + 2, max(start_y, ty) + 2)
        score = (busy(gray, badge) + 0.5 * busy(gray, arrow_box) + 0.03 * math.hypot(cx - tx, cy - ty)
                 + 120.0 * not_background(gray, badge) + 40.0 * not_background(gray, arrow_box))
        if best is None or score < best[4]:
            best = (cx, cy, tx, ty, score)
    return best


def arrow_head(draw, tip_x, tip_y, angle):
    """Small arrow head at the tip."""
    for turn in (math.radians(155), math.radians(-155)):
        draw.line((tip_x, tip_y, tip_x + 14 * math.cos(angle + turn), tip_y + 14 * math.sin(angle + turn)),
                  fill=RED, width=LINE)


def annotate(figure, steps):
    """Draw all marks of one figure. Returns (image, marks, worst_score, problems)."""
    image = Image.open(os.path.join(BASE, figure + ".png")).convert("RGB")
    gray = image.convert("L")
    draw = ImageDraw.Draw(image)
    items = []
    for step in steps:
        for box in step["boxes"]:
            items.append((step["step"], box))
    rects = []
    for _number, box in items:
        rects.append(padded(box))
    # rectangles of different steps that touch are trimmed back so they never overlap
    rects = [list(r) for r in rects]
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            if items[i][0] != items[j][0] and intersects(rects[i], rects[j]):
                a, b = rects[i], rects[j]
                over_x = min(a[2], b[2]) - max(a[0], b[0])
                over_y = min(a[3], b[3]) - max(a[1], b[1])
                if over_x <= over_y:
                    cut = (over_x + 1) // 2
                    if a[0] < b[0]:
                        a[2] -= cut; b[0] += cut
                    else:
                        b[2] -= cut; a[0] += cut
                else:
                    cut = (over_y + 1) // 2
                    if a[1] < b[1]:
                        a[3] -= cut; b[1] += cut
                    else:
                        b[3] -= cut; a[1] += cut
    rects = [tuple(r) for r in rects]
    problems = []
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            if intersects(rects[i], rects[j]) and items[i][0] != items[j][0]:
                problems.append(f"marks {items[i][0]} and {items[j][0]} overlap")
    for rect in rects:
        draw.rounded_rectangle(rect, radius=8, outline=RED, width=LINE)
    placed = []
    worst = 0.0
    badge_font = font()
    # higher steps first would hide low ones; place in step order
    for index, (number, box) in enumerate(items):
        own = rects[index]
        spot = place_badge(gray, own, rects, placed, image.size)
        if spot is None:
            problems.append(f"no free spot for badge {number}")
            continue
        cx, cy, tx, ty, score = spot
        worst = max(worst, score)
        angle = math.atan2(ty - cy, tx - cx)
        start = (cx + RADIUS * math.cos(angle), cy + RADIUS * math.sin(angle))
        draw.line((start[0], start[1], tx, ty), fill=RED, width=LINE)
        arrow_head(draw, tx, ty, angle)
        draw.ellipse((cx - RADIUS, cy - RADIUS, cx + RADIUS, cy + RADIUS), fill=RED)
        draw.text((cx, cy), str(number), fill="white", font=badge_font, anchor="mm")
        placed.append((cx - RADIUS - 1, cy - RADIUS - 1, cx + RADIUS + 1, cy + RADIUS + 1))
        covered = not_background(gray, (cx - RADIUS, cy - RADIUS, cx + RADIUS, cy + RADIUS))
        worst = max(worst, covered * 100)
        if covered > 0.03:
            problems.append(f"badge {number} covers something ({covered * 100:.0f}% of its area)")
    return image, len(items), worst, problems


def contact_sheet(names):
    """Thumbnails of the annotated pictures (for scanning only)."""
    columns, thumb_w, thumb_h, label_h = 4, 400, 244, 16
    rows = (len(names) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, name in enumerate(names):
        picture = Image.open(os.path.join(V2, name)).convert("RGB")
        picture.thumbnail((thumb_w - 6, thumb_h - 4))
        x, y = (index % columns) * thumb_w + 3, (index // columns) * (thumb_h + label_h)
        sheet.paste(picture, (x, y + label_h))
        draw.text((x, y + 2), name[:-4], fill="black")
    sheet.save(os.path.join(V2, "_contact_sheet.png"))


def main():
    """Annotate every figure in boxes_steps.json and print the check table."""
    with open(os.path.join(OUT, "boxes_steps.json"), encoding="utf-8") as handle:
        data = json.load(handle)
    os.makedirs(V2, exist_ok=True)
    names = []
    print(f"{'figure':12} {'size':>9} {'steps':>5} {'marks':>5} {'busiest':>8}  result")
    for figure in sorted(data, key=lambda f: int(f.split("_")[1])):
        steps = data[figure]
        numbers = [s["step"] for s in steps]
        image, marks, worst, problems = annotate(figure, steps)
        if numbers != list(range(1, len(numbers) + 1)):
            problems.append("step numbers not 1..n in order")
        if len(numbers) > 5:
            problems.append("more than 5 numbers")
        if image.size != (1000, 610):
            problems.append("size changed")
        image.save(os.path.join(V2, figure + ".png"))
        names.append(figure + ".png")
        print(f"{figure:12} {image.width}x{image.height} {len(numbers):>5} {marks:>5} {worst:8.1f}  "
              f"{'PASS' if not problems else 'CHECK: ' + '; '.join(problems)}")
    contact_sheet(names)


if __name__ == "__main__":
    main()
