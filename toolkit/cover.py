# usage: cover.py FRAME OUT.jpg Y "LINE 1" "LINE 2" [HIGHLIGHT_WORD]  -> clean frame + 2-line teaser, no logo (JPEG for IG cover_url)
import sys
from PIL import Image, ImageDraw, ImageFont
fr, out, y0, l1, l2 = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
hl = sys.argv[6] if len(sys.argv) > 6 else ""
im = Image.open(fr).convert('RGB').resize((1080, 1920))
g = Image.new('L', (1, 1920))
for y in range(1920): g.putpixel((0, y), int(max(0, 1 - abs(y - (y0 + 100)) / 380) * 120))
im.paste(Image.new('RGB', (1080, 1920), (10, 6, 14)), (0, 0), g.resize((1080, 1920)))
f = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', 84)
d = ImageDraw.Draw(im); y = y0
for ln in (l1, l2):
    parts = []
    for w in ln.split(' '): parts.append((w + ' ', (255, 214, 10) if hl and w.strip('.,!?') == hl else (255, 255, 255)))
    parts[-1] = (parts[-1][0].rstrip(), parts[-1][1])
    W = sum(d.textlength(t, font=f) for t, _ in parts); x = (1080 - W) / 2
    for t, c in parts: d.text((x, y), t, font=f, fill=c, stroke_width=7, stroke_fill=(20, 12, 20)); x += d.textlength(t, font=f)
    y += 112
im.save(out, quality=95)
