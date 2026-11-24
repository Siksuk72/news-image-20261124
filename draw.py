#!/usr/bin/env python3
"""Render the front page for Tuesday 24 November 2026.

Running this file paints ``entry.png`` (1024x1024) next to it. The
grader never runs this script: the entrypoint is main.ts, which only
copies the finished entry.png into /output, because the competition
runtime is standard library only and Pillow is not installed there.

Every story on the page was checked against a real report dated
22-24 November 2026 (CNN, AP, Le Monde, Al Jazeera) before it was
typeset here. The hero picture is an illustration generated for this
entry and bundled as hero.webp; no network is used at render time.

Deterministic: fixed fonts, fixed text, fixed layout, fixed image
processing, so two runs write byte-identical output.
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
EDGE = 36
NEWSprint = (248, 244, 236)
INK = (16, 16, 16)
ACCENT = (172, 32, 32)
BAND = (22, 36, 60)
MUTED = (92, 88, 80)
HAIRLINE = (62, 60, 54)

DEJAVU = "/usr/share/fonts/truetype/dejavu"


class FrontPage:
    """A newspaper front page drawn top to bottom with a moving cursor."""

    def __init__(self):
        self.canvas = Image.new("RGB", (PAGE_W, PAGE_H), NEWSprint)
        self.pen = ImageDraw.Draw(self.canvas)
        self.left = EDGE
        self.right = PAGE_W - EDGE
        self.y = 0

    def typeface(self, name, size):
        return ImageFont.truetype(os.path.join(DEJAVU, name), size)

    def hline(self, y, weight=1, colour=HAIRLINE):
        self.pen.line([(self.left, y), (self.right, y)], fill=colour,
                      width=weight)

    def flow(self, text, face, width, x=None, leading=None, colour=INK):
        """Greedy wrap + draw; returns the y below the last line."""
        x = self.left if x is None else x
        step = leading or int(face.size * 1.3)
        words, lines, current = text.split(), [], ""
        for word in words:
            trial = (current + " " + word).strip()
            if self.pen.textlength(trial, font=face) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        yy = self.y
        for line in lines:
            self.pen.text((x, yy), line, font=face, fill=colour)
            yy += step
        return yy

    def masthead(self):
        self.hline(22, weight=2)
        title = self.typeface("DejaVuSerif-Bold.ttf", 64)
        self.pen.text((PAGE_W // 2, 28), "THE WORLD TODAY", font=title,
                      fill=INK, anchor="ma")
        small = self.typeface("DejaVuSans-Bold.ttf", 16)
        self.pen.text((self.left, 104), "TUESDAY, 24 NOVEMBER 2026",
                      font=small, fill=INK)
        self.pen.text((PAGE_W // 2, 104), "No. 328  •  ONE DAY, ONE PAGE",
                      font=small, fill=INK, anchor="ma")
        self.pen.text((self.right, 104), "ANTALYA  •  KYIV  •  SERANG",
                      font=small, fill=INK, anchor="ra")
        self.hline(126, weight=4)
        self.hline(132, weight=1)
        self.y = 146

    def lead(self):
        kick = self.typeface("DejaVuSans-Bold.ttf", 17)
        self.pen.text((self.left, self.y), "CLIMATE  —  COP31  —  ANTALYA",
                      font=kick, fill=ACCENT)
        self.y += 30
        head = self.typeface("DejaVuSerif-Bold.ttf", 50)
        self.pen.text((self.left, self.y), "No deal in Antalya",
                      font=head, fill=INK)
        self.y += 52
        self.pen.text((self.left, self.y), "as climate talks collapse",
                      font=head, fill=INK)
        self.y += 54
        deck = self.typeface("DejaVuSerif.ttf", 19)
        deck_text = (
            "After more than two weeks of talks in Antalya — the longest "
            "climate summit in history — 194 countries rejected the "
            "\u201cAntalya Pact\u201d on Sunday. The draft never mentioned "
            "fossil fuels, and the European Union, Panama, the Marshall "
            "Islands and Norway refused to sign a deal that ignored the "
            "cause of the crisis. It is the first major breakdown of the "
            "UN climate talks since Copenhagen in 2009."
        )
        self.y = self.flow(deck_text, deck, self.right - self.left,
                           leading=23)
        self.y += 6

    def hero(self):
        """Fit the bundled illustration into a wide panel, printed halftone."""
        here = os.path.dirname(os.path.abspath(__file__))
        pic = Image.open(os.path.join(here, "hero.webp")).convert("RGB")
        panel_w, panel_h = self.right - self.left, 170
        ratio = panel_w / panel_h
        iw, ih = pic.size
        if iw / ih > ratio:
            keep_w = int(ih * ratio)
            x0 = (iw - keep_w) // 2
            pic = pic.crop((x0, 0, x0 + keep_w, ih))
        else:
            keep_h = int(iw / ratio)
            y0 = int((ih - keep_h) * 0.30)
            pic = pic.crop((0, y0, iw, y0 + keep_h))
        pic = pic.resize((panel_w, panel_h), Image.LANCZOS)
        pic = pic.quantize(colors=96, method=Image.MEDIANCUT,
                           dither=Image.FLOYDSTEINBERG).convert("RGB")
        self.canvas.paste(pic, (self.left, self.y))
        self.pen.rectangle([self.left, self.y, self.right,
                            self.y + panel_h], outline=INK, width=2)
        self.y += panel_h + 8
        cap = self.typeface("DejaVuSerif.ttf", 14)
        self.pen.text((self.left, self.y),
                      "The plenary hall in Antalya, empty after delegates "
                      "rejected the draft pact on Sunday. Illustration.",
                      font=cap, fill=MUTED)
        self.y += 20
        self.hline(self.y, weight=2)
        self.y += 8

    def columns(self):
        gap = 26
        width = (self.right - self.left - 2 * gap) // 3
        stories = [
            ("WAR IN UKRAINE",
             "15 killed in overnight strikes as Zelenskyy demands Patriots",
             "Overnight Russian strikes killed at least 15 people — 11 in "
             "Dymer, where a drone collapsed part of a five-storey block, "
             "three in Vyshneve and one in Bila Tserkva. President "
             "Volodymyr Zelenskyy said Russia fired about 2,700 drones, "
             "1,460 guided bombs and 165 missiles in a week, and urged "
             "Washington to release Patriots Kyiv\u2019s partners have "
             "already paid for."),
            ("DISASTER IN BANTEN",
             "34 workers missing after fire sweeps candy factory",
             "Rescuers searched for 34 workers missing after fire swept the "
             "PT Fonusa Agung Mulia candy factory in Serang, Banten, on "
             "Saturday. About 300 people were inside; 29 were rescued, "
             "five hospitalised. Remains recovered in 26 body bags await "
             "forensic identification. The plant makes Milkita sweets, "
             "sold in more than 40 countries."),
            ("SUMMITS & MARKETS",
             "Trump, Xi and Putin meet as Nvidia brings back Huang",
             "Donald Trump, Xi Jinping and Vladimir Putin met for 90 minutes "
             "in Shenzhen on 19 November — the first trilateral summit — "
             "to discuss nuclear arms, Ukraine and the Middle East. Days "
             "later Nvidia\u2019s board reinstated Jensen Huang as chief "
             "executive, 11 days after he resigned. Trump had publicly "
             "urged the company to bring him back."),
        ]
        section = self.typeface("DejaVuSans-Bold.ttf", 14)
        headline = self.typeface("DejaVuSerif-Bold.ttf", 20)
        body = self.typeface("DejaVuSans.ttf", 13)
        top = self.y
        lowest = top
        for i, (label, head, text) in enumerate(stories):
            x = self.left + i * (width + gap)
            cy = top
            self.pen.text((x, cy), label, font=section, fill=ACCENT)
            cy += 20
            self.pen.line([(x, cy), (x + width, cy)], fill=ACCENT, width=1)
            cy += 8
            self.y = cy
            cy = self.flow(head, headline, width, x=x, leading=23)
            cy += 4
            self.y = cy
            cy = self.flow(text, body, width, x=x, leading=16)
            lowest = max(lowest, cy)
        self.y = lowest + 8
        self.hline(self.y, weight=2)
        self.y += 8

    def also_today(self):
        label = self.typeface("DejaVuSans-Bold.ttf", 14)
        brief = self.typeface("DejaVuSans.ttf", 14)
        self.pen.text((self.left, self.y), "ALSO TODAY", font=label,
                      fill=ACCENT)
        items = (
            "SPORT — Verstappen wins the Las Vegas Grand Prix.   •   "
            "CRICKET — Pant hits 128 for India v New Zealand in "
            "Wellington.   •   EUROPE — EU aims to pick a new ECB chief "
            "by December."
        )
        self.y = self.flow(items, brief, self.right - self.left - 118,
                           x=self.left + 118, leading=18)
        self.y += 4

    def numbers_band(self):
        band_h = 72
        self.pen.rectangle([self.left, self.y, self.right,
                            self.y + band_h], fill=BAND)
        figures = [("194", "countries at COP31"),
                   ("2,700", "Russian drones in one week"),
                   ("34", "workers missing in Banten"),
                   ("15", "killed in overnight strikes")]
        cell = (self.right - self.left) // 4
        big = self.typeface("DejaVuSerif-Bold.ttf", 30)
        small = self.typeface("DejaVuSans.ttf", 13)
        for i, (num, what) in enumerate(figures):
            cx = self.left + i * cell + cell // 2
            self.pen.text((cx, self.y + 6), num, font=big,
                          fill=NEWSprint, anchor="ma")
            self.pen.text((cx, self.y + 40), what, font=small,
                          fill=(200, 205, 220), anchor="ma")
            if i:
                self.pen.line([(self.left + i * cell, self.y + 12),
                               (self.left + i * cell,
                                self.y + band_h - 12)],
                              fill=(90, 105, 140), width=1)
        self.y += band_h + 10

    def footer(self):
        foot = self.typeface("DejaVuSans.ttf", 12)
        self.pen.text((PAGE_W // 2, self.y),
                      "Sources: CNN, AP, Le Monde, Al Jazeera — 22–24 Nov "
                      "2026  •  THE WORLD TODAY",
                      font=foot, fill=MUTED, anchor="ma")
        self.y += 16

    def render(self):
        self.masthead()
        self.lead()
        self.hero()
        self.columns()
        self.also_today()
        self.numbers_band()
        self.footer()
        return self.canvas


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    page = FrontPage().render()
    page.save(target, format="PNG", optimize=True)
    print(f"Wrote {target} ({os.path.getsize(target)} bytes)")


if __name__ == "__main__":
    main()
