"""MIRABILIA pinned carousel slides (1080x1350, white bg, black text). Text is used verbatim from the brief
(only line breaks are added)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H = 1080, 1350
D = '/tmp/pin/'; OUT = D + 'output/'; os.makedirs(OUT, exist_ok=True)
INK = (20, 20, 20); GREY = (110, 110, 110)
CJK = '/usr/share/fonts/opentype/noto/'
def F(n, s): return ImageFont.truetype(CJK + n + '.ttc', s, index=0)
f_head = F('NotoSansCJK-Light', 50); f_head_l = F('NotoSansCJK-Light', 62)
f_body = F('NotoSansCJK-Regular', 34); f_copy = F('NotoSansCJK-DemiLight', 40); f_lab = F('NotoSansCJK-Regular', 28)

LOGO = Image.open(D + 'mirabilia-logo-black.png').convert('RGBA')
LOGO = LOGO.crop(LOGO.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox())
def logo(img, width, cy):
    lg = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    img.alpha_composite(lg, (W // 2 - lg.width // 2, int(cy - lg.height / 2)))

def tw(s, f, tr=0): return sum(f.getlength(c, features=['palt']) for c in s) + tr * (len(s) - 1)
def line(d, cx, y, s, f, fill=INK, tr=1, align='center', x0=90):
    x = cx - tw(s, f, tr) / 2 if align == 'center' else x0
    for c in s:
        d.text((x, y), c, font=f, fill=fill, features=['palt']); x += f.getlength(c, features=['palt']) + tr
def block(d, y, lines, f, lh, **kw):
    for i, l in enumerate(lines):
        assert tw(l, f) <= W - 160, (l, tw(l, f))
        line(d, W / 2, y + i * lh, l, f, **kw)
    return y + lh * len(lines)

def page(): return Image.new('RGBA', (W, H), (255, 255, 255, 255))
def footer(img): logo(img, 190, H - 70)
def paste_fit(img, im, box, cover=False):
    x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
    s = (max if cover else min)(bw / im.width, bh / im.height)
    r = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    if cover:
        r = r.crop(((r.width - bw) // 2, (r.height - bh) // 2, (r.width - bw) // 2 + bw, (r.height - bh) // 2 + bh))
    img.alpha_composite(r.convert('RGBA'), (x0 + (bw - r.width) // 2, y0 + (bh - r.height) // 2))
def save(img, name): img.convert('RGB').save(OUT + name); print('saved', name)

# ---------- shared images ----------
TEE = Image.open('/tmp/pan/pandora-blacktee-mockup.jpg').convert('RGB')
TEE_SQ = TEE.crop((392, 30, 1532, 1170))          # shirt, square
BLANK = Image.open('/tmp/pan/tee_blank.jpg').convert('RGB')
def fabric(w, h):  # black fabric texture from the blank tee chest, enlarged
    return BLANK.crop((820, 420, 1100, 420 + int(280 * h / w))).resize((w, h), Image.BICUBIC).convert('RGBA')
def print_on(bg, pr_path, crop, size):
    pr = Image.open(pr_path).convert('RGBA').crop(crop)
    arr = np.asarray(pr, np.float32)
    if bg == 'black':  # black ink invisible on black body
        arr[..., 3] *= np.clip((arr[..., :3].mean(-1) - 18) / 30, 0, 1)
        base = fabric(*size)
    else:
        base = Image.new('RGBA', size, (246, 245, 242, 255))
    pr = Image.fromarray(arr.astype(np.uint8), 'RGBA').resize(size, Image.LANCZOS)
    base.alpha_composite(pr); return base
def frame(img, box):
    ImageDraw.Draw(img).rectangle(box, outline=(225, 225, 225), width=2)

# ---------- 固定1 ----------
im = page(); d = ImageDraw.Draw(im)
logo(im, 600, 600); d.line([(W / 2 - 140, 720), (W / 2 + 140, 720)], fill=INK, width=2)
block(d, 770, ['名画を着る、知ればもっと着たくなる。'], f_copy, 60, tr=3)
save(im, 'pin1-01.png')

im = page(); d = ImageDraw.Draw(im)
wave = Image.open(D + 'work/16_hokusai_great-wave.jpg'); paste_fit(im, wave, (90, 110, 990, 726)); frame(im, (90, 110, 990, 726))
y = block(d, 790, ['名画の物語を、動画で解説する', 'アカウントです。'], f_head, 76, tr=2)
block(d, y + 34, ['ゴッホ、モネ、北斎……有名な絵の', '「なぜ？」を、細部からひもときます。'], f_body, 58)
footer(im); save(im, 'pin1-02.png')

im = page(); d = ImageDraw.Draw(im)
pan = Image.open(D + 'work/41_redon_pandora.jpg').convert('RGB')
_a = np.asarray(pan.convert('L'), np.float32); _c = np.where(_a.mean(0) > 40)[0]; _r = np.where(_a.mean(1) > 40)[0]
pan = pan.crop((_c[0] + 4, _r[0] + 4, _c[-1] - 4, _r[-1] - 4))  # trim the black scan border
paste_fit(im, pan, (90, 110, 400, 790))
paste_fit(im, TEE_SQ, (430, 110, 990, 790), cover=True); frame(im, (430, 110, 990, 790))
y = block(d, 850, ['動画で気になった名画は、', 'そのまま着られます。'], f_head, 76, tr=2)
block(d, y + 34, ['解説で好きになった一枚を、日常の一着に。'], f_body, 58)
footer(im); save(im, 'pin1-03.png')

im = page(); d = ImageDraw.Draw(im)
y = block(d, 300, ['画家10名 × 5作品 ＝ 全50作品'], f_head, 76, tr=2)
order = [('ゴッホ', 'vangogh'), ('モネ', 'monet'), ('フェルメール', 'vermeer'), ('北斎', 'hokusai'), ('ルノワール', 'renoir'),
         ('スーラ', 'seurat'), ('ルソー', 'rousseau'), ('ゴヤ', 'goya'), ('ルドン', 'redon'), ('カサット', 'cassatt')]
ts, gap = 170, 13; gx = (W - (5 * ts + 4 * gap)) // 2
for i, (jp, key) in enumerate(order):
    r, c = divmod(i, 5); x = gx + c * (ts + gap); yy = 470 + r * (ts + 90)
    t = Image.open(D + 'painter/%s.jpg' % key).convert('RGB').resize((ts, ts), Image.LANCZOS)
    im.alpha_composite(t.convert('RGBA'), (x, yy))
    line(d, x + ts / 2, yy + ts + 14, jp, f_lab, tr=1)
footer(im); save(im, 'pin1-04.png')

im = page(); d = ImageDraw.Draw(im)
detail = print_on('black', D + 'pandora-print-white-1100.png', (500, 2000, 1100, 2492), (900, 738))
im.alpha_composite(detail, (90, 90))
y = block(d, 960, ['パブリックドメインの名画を、', '大きくプリント。'], f_head, 76, tr=2)
block(d, y + 26, ['図案の右下に、小さなMIRABILIAロゴ。'], f_body, 58)
footer(im); save(im, 'pin1-06.png')

im = page(); d = ImageDraw.Draw(im)
y = block(d, 360, ['まずは動画から。', '気になった作品は、', 'プロフィールのリンクへ。'], f_head, 80, tr=2)
logo(im, 520, 760); d.line([(W / 2 - 140, 870), (W / 2 + 140, 870)], fill=INK, width=2)
block(d, 915, ['名画を着る、知ればもっと着たくなる。'], f_copy, 60, tr=3)
save(im, 'pin1-07.png')

# ---------- 固定3 ----------
im = page(); d = ImageDraw.Draw(im)
block(d, 120, ['買う前に、知ってほしいこと'], f_head_l, 90, tr=3)
paste_fit(im, TEE_SQ, (140, 290, 940, 1090), cover=True); frame(im, (140, 290, 940, 1090))
footer(im); save(im, 'pin3-01.png')

im = page(); d = ImageDraw.Draw(im)
detail = print_on('black', D + 'pandora-print-white-1100.png', (250, 950, 1000, 1550), (900, 720))
im.alpha_composite(detail, (90, 90))
y = block(d, 960, ['名画を大きくプリントしています', '（Tシャツは約32×38cmの枠いっぱい）。'], f_body, 56)
block(d, y + 22, ['カラーインクジェットプリントで、', '名画の色彩をそのまま再現。'], f_body, 56)
footer(im); save(im, 'pin3-02.png')

im = page(); d = ImageDraw.Draw(im)
crop = (650, 2330, 1100, 2510)
a = print_on('white', D + 'pandora-print-black-1100.png', crop, (900, 360))
b = print_on('black', D + 'pandora-print-white-1100.png', crop, (900, 360))
im.alpha_composite(a, (90, 110)); frame(im, (90, 110, 990, 470))
im.alpha_composite(b, (90, 500))
y = block(d, 960, ['図案の右下に、小さなMIRABILIAロゴ。'], f_head, 76, tr=2)
block(d, y + 30, ['白・淡色のボディは黒ロゴ、', '黒ボディは白ロゴです。'], f_body, 58)
footer(im); save(im, 'pin3-03.png')

im = page(); d = ImageDraw.Draw(im)
y = block(d, 300, ['受注生産です。'], f_head, 76, tr=2)
y = block(d, y + 30, ['ご注文後にプリント工場へ発注し、', '約2週間で発送します。', '送料は無料です。'], f_body, 60)
paste_fit(im, TEE_SQ, (390, y + 80, 690, y + 380), cover=True); frame(im, (390, y + 80, 690, y + 380))
footer(im); save(im, 'pin3-05.png')

im = page(); d = ImageDraw.Draw(im)
y = block(d, 420, ['サイズ表は各商品ページに載せています。'], f_head, 76, tr=2)
block(d, y + 40, ['受注生産のため、返品・交換は', '原則お受けできません。', 'サイズ表をご確認の上、ご注文ください。'], f_body, 62)
footer(im); save(im, 'pin3-06.png')
