"""Promotion Catalogues cover images: the merchant's logo, legible, on a brand-coloured banner.

deterministic + idempotent — the same logo, text and theme render the same image.

The DB is a gallery with page-cover preview (user, 2026-09-30), so each page
needs a cover, and the cover must carry the merchant's logo where it can be
read. Brand logos are usually the colour of their own brand background (Makro
red on Makro red), so the logo sits on a white rounded plate. The plate and the
month sit in the middle band (y ≈ 270–630 of 900): the page banner shows about
y 240–660, the gallery card the whole image.

A logo reference is one of:
  commons:<File name>   a Wikimedia Commons file, fetched as a PNG render
                        (e.g. `commons:Makro logo.svg`, `commons:Shopee.svg`)
  https://…             an image URL
  <path>                a local image file
Transparent margins are cropped; an opaque logo on white has its white keyed out.
`logo_text` sets a wordmark beside the logo, for a brand with only an icon on
file (TikTok Shop: the TikTok icon + "TikTok Shop").
"""

from __future__ import annotations

import io
import json
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1800, 900
_PLATE = (110, 270, 930, 630)
_UA = {"User-Agent": "Mozilla/5.0 (takumi-supplement-card-manager catalogue covers)"}
# By file name: Pillow searches the system font folders (macOS keeps these in
# /System/Library/Fonts and its Supplemental/ subfolder; Linux, /usr/share/fonts).
# Loma (TLWG) is the Thai font on the Linux cloud image, where macOS's are absent.
_FONTS = ("SukhumvitSet.ttc", "Thonburi.ttc", "Loma.otf")


@dataclass(frozen=True)
class CoverTheme:
    bg: str                       # banner colour
    stripe: str                   # the darker diagonal stripes
    deep: str                     # the floor band
    subcolor: str = "#FFFFFF"     # the subtitle
    pad: int = 60                 # the logo's padding inside the plate
    cards: tuple[tuple[str, str], ...] = field(default_factory=tuple)  # (colour, label), the issuers on the page

    @classmethod
    def of(cls, spec: str | dict) -> CoverTheme:
        """A preset name or a dict of fields (`cards` as [[colour, label], …])."""
        if isinstance(spec, str):
            return PRESETS[spec]
        spec = dict(spec)
        spec["cards"] = tuple(tuple(c) for c in spec.get("cards", ()))
        return cls(**spec)


_KB, _KS, _UOB, _TTB = ("#00663F", "KBank"), ("#FFC400", "Krungsri"), ("#002E6C", "UOB"), ("#0054A6", "ttb")
_CX, _KTC, _SCB, _FC = ("#141414", "CardX"), ("#1B3F94", "KTC"), ("#4F2D7F", "SCB"), ("#E2231A", "First Choice")

PRESETS: dict[str, CoverTheme] = {
    "makro": CoverTheme("#E2231A", "#D61E16", "#9E110C", "#FFE08A",
                        cards=(_KB, _KS, _UOB, _TTB, ("#7D267C", "AEON"), _CX)),
    "go-wholesale": CoverTheme("#D7141A", "#C81016", "#8E0A0E", "#FFE3E3", pad=40,
                               cards=(("#1A1A1A", "The 1"), ("#E4002B", "The 1 REDZ"), _KB, _CX, _KS, _TTB)),
    "shopee": CoverTheme("#EE4D2D", "#E4431F", "#B8321A", "#FFF0D6",
                         cards=(("#F05D23", "Shopee KBank"), ("#FF7A33", "SPayLater"), _UOB, _KS, _SCB, _KTC)),
    "lazada": CoverTheme("#0F146D", "#151B7E", "#F36F21", "#FFC7E6", cards=(_KB, _KS, _UOB, _SCB, _KTC, _FC)),
    "tiktok-shop": CoverTheme("#101010", "#1A1A1A", "#FE2C55", "#25F4EE", pad=70,
                              cards=(("#25F4EE", "TikTok"), _KS, _UOB, _FC, _SCB, ("#FE2C55", "KTC"))),
    # Black, like the T1 mark (user, 2026-10-01): a red The 1 cover left the gallery all red and orange.
    "central-the-1": CoverTheme("#111111", "#1B1B1B", "#E4002B", "#FFB8C4", pad=80,
                                cards=(("#6E6E6E", "T1 Grey"), ("#1A1F71", "Visa"), _KS,
                                       ("#F79E1B", "Mastercard"), ("#2B2B2B", "T1 Black"), ("#E4002B", "T1 REDZ"))),
}


def _rgb(h: str) -> tuple[int, int, int]:
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def font(size: int, face: int = 5) -> ImageFont.FreeTypeFont:
    """Sukhumvit Set (face 5 = Bold, 4 = Semi Bold, 3 = Medium) — Thai and Latin — or Thonburi, or Loma."""
    for name in _FONTS:
        try:
            if name.startswith("Loma"):  # one file per weight, not a collection
                return ImageFont.truetype("Loma-Bold.otf" if face >= 4 else name, size)
            return ImageFont.truetype(name, size, index=face if name.startswith("Sukhumvit") else min(face, 1))
        except OSError:
            continue
    raise FileNotFoundError(f"no Thai font found (tried {', '.join(_FONTS)})")


def _fetch(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=_UA), timeout=30) as resp:
        return resp.read()


def _commons_png(name: str, width: int = 1600) -> str:
    """The PNG render URL of a Wikimedia Commons file."""
    title = name if name.startswith("File:") else f"File:{name}"
    api = ("https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url"
           f"&iiurlwidth={width}&format=json&titles={urllib.parse.quote(title)}")
    pages = json.loads(_fetch(api))["query"]["pages"]
    info = next(iter(pages.values())).get("imageinfo")
    if not info:
        raise LookupError(f"Wikimedia Commons has no file {title!r}")
    return info[0].get("thumburl") or info[0]["url"]


def load_logo(ref: str) -> Image.Image:
    """The logo as RGBA, cropped to its drawn area."""
    if ref.startswith("commons:"):
        raw = _fetch(_commons_png(ref.removeprefix("commons:")))
    elif ref.startswith(("http://", "https://")):
        raw = _fetch(ref)
    else:
        raw = Path(ref).read_bytes()
    im = Image.open(io.BytesIO(raw)).convert("RGBA")
    if im.getchannel("A").getextrema()[0] == 255:            # opaque: key out a white background
        im.putalpha(im.convert("L").point(lambda v: 0 if v > 235 else 255))
    box = im.getbbox()
    return im.crop(box) if box else im


def with_wordmark(logo: Image.Image, text: str, colour: str = "#000000") -> Image.Image:
    """The logo with `text` set beside it, as one image."""
    icon = logo.resize((420, int(420 * logo.height / logo.width)) if logo.width > logo.height
                       else (int(420 * logo.width / logo.height), 420), Image.LANCZOS)
    f = font(250)
    asc, desc = f.getmetrics()
    canvas = Image.new("RGBA", (icon.width + 60 + int(f.getlength(text)), max(icon.height, asc + desc)), (0, 0, 0, 0))
    canvas.alpha_composite(icon, (0, (canvas.height - icon.height) // 2))
    ImageDraw.Draw(canvas).text((icon.width + 60, (canvas.height - (asc + desc)) // 2 - 10), text, font=f,
                                fill=_rgb(colour) + (255,))
    return canvas.crop(canvas.getbbox())


def render(logo: Image.Image, period: str, subtitle: str, theme: CoverTheme, out: Path) -> Path:
    """Draw the cover and save it as a JPEG at `out`."""
    bg, stripe, deep, white = _rgb(theme.bg), _rgb(theme.stripe), _rgb(theme.deep), (255, 255, 255)
    img = Image.new("RGBA", (W, H), bg)
    d = ImageDraw.Draw(img)
    for i, x in enumerate(range(-H, W, 120)):
        d.polygon([(x, H), (x + 60, H), (x + 60 + H, 0), (x + H, 0)], fill=stripe if i % 2 else bg)

    cards = [(_rgb(c), label) for c, label in theme.cards][-6:]
    mid = (len(cards) - 1) / 2
    for n, (col, label) in enumerate(cards):
        card = Image.new("RGBA", (330, 208), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, 329, 207], radius=20, fill=col + (255,), outline=(255, 255, 255, 110), width=3)
        cd.rounded_rectangle([26, 62, 82, 102], radius=8, fill=(236, 200, 110, 255))
        cd.text((26, 136), label, font=font(36), fill=(white if sum(col) < 500 else (40, 30, 0)) + (255,))
        rot = card.rotate(-30 + (n - mid) * 10, expand=True, resample=Image.BICUBIC)
        shadow = Image.new("RGBA", rot.size, (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 80), mask=rot.split()[3])
        cx, cy = int(1500 + (n - mid) * 20), int(660 + abs(n - mid) * 6)
        img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)), (cx - rot.width // 2 + 8, cy - rot.height // 2 + 14))
        img.alpha_composite(rot, (cx - rot.width // 2, cy - rot.height // 2))

    x0, y0, x1, y1 = _PLATE
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shade).rounded_rectangle([x0 + 10, y0 + 16, x1 + 10, y1 + 16], radius=44, fill=(0, 0, 0, 90))
    img.alpha_composite(shade.filter(ImageFilter.GaussianBlur(16)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x1, y1], radius=44, fill=white)
    mark = logo.copy()
    mark.thumbnail((x1 - x0 - 2 * theme.pad, y1 - y0 - 2 * theme.pad), Image.LANCZOS)
    img.alpha_composite(mark, (x0 + (x1 - x0 - mark.width) // 2, y0 + (y1 - y0 - mark.height) // 2))

    d = ImageDraw.Draw(img)
    d.text((1000, 300), period, font=font(86), fill=white)
    d.text((1004, 420), subtitle, font=font(44, 3), fill=_rgb(theme.subcolor))
    d.rectangle([0, H - 110, W, H], fill=deep)
    d.text((116, H - 88), "Promotion Catalogues", font=font(48), fill=white)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, quality=93)
    return out
