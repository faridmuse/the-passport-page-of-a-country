"""Draw an invented passport spread to /output/entry.png.

The Republic of Thalassa, an island nation reachable only by sea:
a data page with a portrait and consistent dates, and a visa page whose
stamps agree with one another (all after the 02 FEB 2026 issue date).
Runs with no network; writes a PNG of at most 1024x1024 and 1 MiB.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
NAVY = (31, 58, 95)
GOLD = (176, 141, 60)
CREAM = (247, 243, 232)
PAPER = (252, 250, 244)
INK = (30, 30, 30)
RED = (168, 50, 50)
TEAL = (46, 110, 110)
PALE_BLUE = (205, 220, 228)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def stamp_circle(d, cx, cy, r, lines, color=RED, size=15):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - r + 7, cy - r + 7, cx + r - 7, cy + r - 7], outline=color, width=1)
    f = font("DejaVuSans-Bold.ttf", size)
    total = len(lines) * (size + 3)
    y = cy - total // 2
    for line in lines:
        w = d.textlength(line, font=f)
        d.text((cx - w / 2, y), line, fill=color, font=f)
        y += size + 3


def portrait(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PALE_BLUE, outline=NAVY, width=2)
    # faint guilloche arcs
    for i in range(6):
        d.arc([x0 - 40 + i * 8, y0 - 20 + i * 6, x1 + 40 - i * 8, y1 + 20 - i * 6],
              start=200, end=340, fill=(170, 190, 200), width=1)
    # shoulders + head silhouette
    d.ellipse([x0 + 52, y0 + 42, x0 + 128, y0 + 138], fill=(58, 90, 110))
    d.pieslice([x0 + 18, y0 + 128, x0 + 162, y0 + 235], start=180, end=360,
               fill=(58, 90, 110))
    # hair sweep
    d.pieslice([x0 + 52, y0 + 42, x0 + 128, y0 + 118], start=180, end=360,
               fill=(38, 60, 78))
    # collar line
    d.line([x0 + 80, y0 + 150, x0 + 100, y0 + 150], fill=(220, 225, 230), width=3)


def field(d, x, y, label, value, label_size=13, value_size=20):
    lf = font("DejaVuSans.ttf", label_size)
    vf = font("DejaVuSans-Bold.ttf", value_size)
    d.text((x, y), label, fill=(110, 110, 110), font=lf)
    d.text((x, y + label_size + 4), value, fill=INK, font=vf)
    return y + label_size + 4 + value_size + 12


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # outer frame + gutter
    d.rectangle([20, 20, W - 20, H - 20], outline=NAVY, width=3)
    d.line([512, 28, 512, H - 28], fill=(190, 180, 150), width=2)

    # ---- LEFT PAGE: data page ----
    # navy header band
    d.rectangle([28, 28, 504, 96], fill=NAVY)
    d.ellipse([44, 42, 82, 80], outline=GOLD, width=2)
    for k in range(3):
        d.arc([50, 48 + k * 8, 76, 74 + k * 8], start=200, end=340,
              fill=GOLD, width=2)
    tf = font("DejaVuSerif-Bold.ttf", 26)
    d.text((96, 40), "REPUBLIC OF THALASSA", fill=(240, 235, 210), font=tf)
    sf = font("DejaVuSans.ttf", 14)
    d.text((96, 70), "PASSPORT  \u00b7  PASSEPORT", fill=(200, 195, 170), font=sf)

    # photo
    portrait(d, (44, 120, 224, 330))
    # data fields
    y = 120
    y = field(d, 244, y, "SURNAME", "VOSS")
    y = field(d, 244, y, "GIVEN NAMES", "Elena Maris")
    y = field(d, 244, y, "NATIONALITY", "Thalassan")
    y = field(d, 244, y, "DATE OF BIRTH", "14 MAR 1994")
    y = field(d, 244, y, "PLACE OF BIRTH", "Port Meridian")

    y = 480
    y = field(d, 44, y, "PASSPORT NO.", "TH-4829137")
    y = field(d, 44, y, "DATE OF ISSUE", "02 FEB 2026")
    y = field(d, 44, y, "DATE OF EXPIRY", "02 FEB 2036")
    y = field(d, 44, y, "AUTHORITY", "Port Meridian Passport Office")
    y = field(d, 44, y, "SEX", "F")

    # issue stamp overlapping the photo corner
    stamp_circle(d, 208, 318, 46, ["ISSUED", "PORT MERIDIAN", "02 FEB 2026"],
                 size=12)

    # machine readable zone
    mf = font("DejaVuSansMono.ttf", 15)
    d.text((44, 884), "P<THAVOSS<<ELENA<MARIS<<<<<<<<<<<<<<<<<<", fill=INK, font=mf)
    d.text((44, 908), "TH4829137<5THA9403148F3602021<<<<<<<<<<04", fill=INK, font=mf)
    d.text((44, 936), "VOSS<<ELENA<MARIS", fill=INK, font=mf)

    # ---- RIGHT PAGE: visas ----
    hf = font("DejaVuSerif-Bold.ttf", 24)
    d.text((556, 36), "VISAS", fill=NAVY, font=hf)
    d.line([556, 70, 996, 70], fill=NAVY, width=2)

    # visa sticker: Kingdom of Kastel
    d.rectangle([556, 88, 996, 250], outline=NAVY, width=2, fill=(238, 240, 235))
    vf = font("DejaVuSans-Bold.ttf", 18)
    nf = font("DejaVuSans.ttf", 15)
    d.text((572, 100), "VISA \u2014 KINGDOM OF KASTEL", fill=NAVY, font=vf)
    d.text((572, 130), "Type: Tourist \u2014 30 days", fill=INK, font=nf)
    d.text((572, 154), "Issued: 10 MAR 2026   Valid until: 09 JUN 2026", fill=INK, font=nf)
    d.text((572, 178), "Entries: Single   Fee: 25 KORUN (paid)", fill=INK, font=nf)
    d.text((572, 206), "Condition: seafaring arrival only", fill=INK, font=nf)

    # entry / exit stamps, all dated after the 02 FEB 2026 issue
    stamp_circle(d, 640, 340, 58, ["THALASSA", "PORT MERIDIAN", "ENTRY", "18 MAR 2026"])
    stamp_circle(d, 880, 340, 58, ["KASTEL", "HARBOUR GATE", "ARRIVAL", "22 MAR 2026"])
    stamp_circle(d, 640, 500, 58, ["KASTEL", "HARBOUR GATE", "DEPARTURE", "02 APR 2026"])
    stamp_circle(d, 880, 500, 58, ["THALASSA", "PORT MERIDIAN", "ENTRY", "04 APR 2026"])

    # departure tax stamp
    d.rectangle([556, 600, 996, 660], outline=RED, width=3)
    bf = font("DejaVuSans-Bold.ttf", 22)
    d.text((576, 618), "DEPARTURE TAX PAID \u2014 40 KORUN", fill=RED, font=bf)

    # telling detail: the visa condition box
    d.rectangle([556, 690, 996, 830], outline=NAVY, width=2)
    cf = font("DejaVuSans-Bold.ttf", 16)
    d.text((572, 704), "CONDITION OF ISSUE", fill=NAVY, font=cf)
    body = font("DejaVuSans.ttf", 16)
    d.text((572, 730), "Valid for seafaring only \u2014 no overland", fill=INK, font=body)
    d.text((572, 754), "transit. The holder must arrive and", fill=INK, font=body)
    d.text((572, 778), "depart by sea; Thalassa has no land", fill=INK, font=body)
    d.text((572, 802), "border with any state.", fill=INK, font=body)

    # footer note
    ff = font("DejaVuSans.ttf", 13)
    d.text((556, 880),
           "This passport remains the property of the", fill=(110, 110, 110), font=ff)
    d.text((556, 900),
           "Republic of Thalassa and must be returned on demand.",
           fill=(110, 110, 110), font=ff)

    os.makedirs("/output", exist_ok=True)
    try:
        os.chmod("/output", 0o755)
    except OSError:
        pass
    path = "/output/entry.png"
    img.save(path, format="PNG")
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
