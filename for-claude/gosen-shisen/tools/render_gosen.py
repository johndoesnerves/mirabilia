"""MIRABILIA 五選 #1「視線の先には何がある？」 (brief 2026-11-17). Five paintings; a white arrow follows each gaze.
Main part at 1.3x, end card at 1x. Times below are on the original narration at 1x; frame_at() maps output time."""
import sys, os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
A = W / H
D = '/tmp/gos/'
OX, OY = 0, 0
TEE = Image.open(D + 'osorio-blacktee-mockup.jpg').convert('RGBA')
LOGO = Image.open('/tmp/iri/mirabilia-logo-white.png').convert('RGBA')
LOGO = LOGO.crop(LOGO.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox())
RED = (0xE3, 0x4B, 0x3F)
CJK = '/usr/share/fonts/opentype/noto/'
def F(name, size): return ImageFont.truetype(CJK + name + '.ttc', size, index=0)

f_sub = F('NotoSansCJK-Bold', 54)
f_cover = F('NotoSansCJK-Black', 86)
f_tag = F('NotoSansCJK-Bold', 32)
f_artist = F('NotoSansCJK-Bold', 44)
f_work = F('NotoSerifCJK-Bold', 96)
f_meta = F('NotoSansCJK-Medium', 30)
f_copy = F('NotoSansCJK-Black', 60)
f_url = F('NotoSansCJK-Medium', 36)
f_end_copy = F('NotoSansCJK-Bold', 44)
f_cta = F('NotoSansCJK-Black', 52)

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def eo(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def lerp(a, b, k): return a + (b - a) * k
PUNCT_TAIL = '、。」』）'

# ---------- text ----------
def jp_width(s, font, track):
    return sum(font.getlength(c, features=['palt']) for c in s) + track * (len(s) - 1)

def draw_line(d, cx, y, s, font, fill, track=0, stroke=0, stroke_fill=None, colors=None):
    ws = [font.getlength(c, features=['palt']) for c in s]
    tw = sum(ws) + track * (len(s) - 1)
    eff = tw - (ws[-1] * 0.5 if s and s[-1] in PUNCT_TAIL else 0)
    x = cx - eff / 2
    for i, (c, w) in enumerate(zip(s, ws)):
        col = colors[i] if colors else fill
        d.text((x, y), c, font=font, fill=col, features=['palt'], stroke_width=stroke, stroke_fill=stroke_fill)
        x += w + track
    return tw

_cache = {}
def layer(key, fn, size=(W, H)):
    if key not in _cache:
        im = Image.new('RGBA', size, (0, 0, 0, 0)); fn(ImageDraw.Draw(im)); _cache[key] = im
    return _cache[key]

def blit(fr, im, x, y, a):
    if a <= 0: return
    if a < 1:
        im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    fr.alpha_composite(im, (int(x), int(y)))

def text_block(key, lines, font, lh, track=2, stroke=4, colors=None):
    def fn(d):
        for i, l in enumerate(lines):
            draw_line(d, W / 2, 10 + i * lh, l, font, (255, 255, 255, 255), track, stroke, (0, 0, 0, 200),
                      colors[i] if colors else None)
    im = layer(key, fn, (W, lh * len(lines) + 40))
    skey = str(key) + '_sh'
    if skey not in _cache:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').point(lambda v: int(v * 0.55)))
        _cache[skey] = sh.filter(ImageFilter.GaussianBlur(8))
    return im, _cache[skey]

def put_block(fr, key, lines, font, lh, y, a, slide=0, track=2, stroke=4, colors=None):
    if a <= 0: return
    im, sh = text_block(key, lines, font, lh, track, stroke, colors)
    blit(fr, sh, 0, y + 4 + slide, a); blit(fr, im, 0, y + slide, a)

# ---------- camera ----------

def cam_at(keys, t):
    if t <= keys[0][0]: return keys[0][1:]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if t <= t1:
            k = ease((t - t0) / (t1 - t0)); return tuple(lerp(p, q, k) for p, q in zip(a, b))
    return keys[-1][1:]

def view(src, cam, off=True):
    cx, cy, w = cam; h = w / A
    if off: cx, cy = cx - OX, cy - OY
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return src.transform((W, H), Image.EXTENT, box, Image.BICUBIC, fillcolor=(0, 0, 0, 0))



# ---------- the five paintings ----------
def load(name):
    im = Image.open(D + name + '.jpg').convert('RGBA'); sw, sh = im.size
    sc = max(W / sw, H / sh)
    bg = im.convert('RGB').resize((int(sw * sc) + 1, int(sh * sc) + 1), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new('RGB', (W, H), (0, 0, 0)), 0.5).convert('RGBA')
    return dict(src=im, bg=bg, w=sw, h=sh)
P = {k: load(k) for k in ['las-meninas', 'narcissus', 'sistine-madonna', 'milkmaid', 'osorio']}
def px(name, xp, yp): return (P[name]['w'] * xp / 100, P[name]['h'] * yp / 100)

# each work: start time, camera keys (t, cx, cy, w) in that painting's pixels, arrow (from, to, t0, t1),
# telop span, answer (text, t0, t1, y), name card (artist, title, t0, t1), optional ring on the target
WORKS = [
    dict(name='las-meninas', t0=0.0,
         cam=[(0.0, 700, 805, 906), (3.4, 700, 820, 860), (5.3, 700, 820, 860), (6.6, 616, 999, 560), (8.7, 610, 985, 540),
              (9.3, 610, 985, 540), (10.6, 581, 902, 250), (15.3, 581, 902, 236)],
         arrow=(px('las-meninas', 47.5, 66.5), px('las-meninas', 42.2, 57.5), 6.7, 8.6),
         telop=(3.5, 9.6), answer=('王さまと王妃！', 9.75, 11.75, 1180),
         card=('ディエゴ・ベラスケス', '《ラス・メニーナス》', 12.0, 15.3)),
    dict(name='narcissus', t0=15.35,
         cam=[(15.35, 560, 847, 953), (16.0, 560, 847, 953), (17.6, 392, 560, 520), (19.4, 400, 600, 560), (21.3, 560, 847, 953),
              (27.3, 560, 847, 920)],
         arrow=(px('narcissus', 28.5, 30.5), px('narcissus', 30, 87), 19.6, 21.3), ring=(px('narcissus', 30, 89), 21.4, 23.4, 95),
         telop=(15.6, 21.4), answer=('自分の顔！', 21.45, 23.3, 1180),
         card=('カラヴァッジョ', '《ナルキッソス》', 23.6, 27.3)),
    dict(name='sistine-madonna', t0=27.35,
         cam=[(27.35, 714, 1500, 700), (28.6, 714, 1500, 700), (31.4, 690, 956, 1075), (32.6, 650, 640, 700), (36.6, 650, 650, 660)],
         arrow=(px('sistine-madonna', 51, 89), px('sistine-madonna', 46, 16.5), 28.7, 31.4),
         telop=(27.6, 32.1), answer=('聖母！', 32.2, 33.7, 1180),
         card=('ラファエロ', '《システィーナの聖母》', 33.9, 36.6)),
    dict(name='milkmaid', t0=36.7,
         cam=[(36.7, 760, 500, 560), (37.4, 720, 575, 640), (39.0, 620, 720, 700), (41.4, 520, 860, 560), (45.6, 520, 860, 540)],
         arrow=(px('milkmaid', 54.5, 27.5), px('milkmaid', 34.5, 56.5), 37.5, 39.0),
         telop=(36.9, 39.2), answer=('注がれる牛乳！', 39.2, 41.4, 1180),
         card=('ヨハネス・フェルメール', '《牛乳を注ぐ女》', 41.6, 45.6)),
    dict(name='osorio', t0=45.75,
         cam=[(45.75, 700, 950, 1068), (46.6, 700, 950, 1068), (47.9, 360, 1300, 640), (50.4, 380, 1400, 700), (56.4, 380, 1390, 680)],
         arrow=(px('osorio', 22, 64.5), px('osorio', 28, 80.5), 48.2, 50.4), ring=(px('osorio', 27, 81), 50.9, 52.6, 110),
         telop=(46.0, 51.0), answer=('カササギ！', 51.0, 52.5, 560),
         card=('フランシスコ・デ・ゴヤ', '《マヌエル・オソーリオ》', 52.6, 56.4)),
]
T_COLLAGE = 56.45; T_PROD = 59.30; T_END = 64.08; T_FIN = 67.28
XF = 0.4

def work_at(t):
    return max(i for i, w in enumerate(WORKS) if t >= w['t0'])

def work_frame(i, t):
    w = WORKS[i]; p = P[w['name']]
    fr = p['bg'].copy(); fr.alpha_composite(view(p['src'], cam_at(w['cam'], t), off=False))
    return fr

def to_screen(cam, x, y):
    cx, cy, w = cam; h = w / A
    return (x - (cx - w / 2)) / w * W, (y - (cy - h / 2)) / h * H

def arrow(fr, a, b, k):
    if k <= 0: return
    (x0, y0), (x1, y1) = a, b
    xe, ye = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    L = math.hypot(xe - x0, ye - y0)
    if L < 4: return
    ux, uy = (xe - x0) / L, (ye - y0) / L
    hl = min(56, L * 0.6); hw = hl * 0.62
    bx, by = xe - ux * hl, ye - uy * hl
    head = [(xe, ye), (bx - uy * hw, by + ux * hw), (bx + uy * hw, by - ux * hw)]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line([(x0, y0), (bx, by)], fill=(0, 0, 0, 150), width=20); d.polygon(head, fill=(0, 0, 0, 150))
    sh = lay.filter(ImageFilter.GaussianBlur(5))
    lay2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d2 = ImageDraw.Draw(lay2)
    d2.line([(x0, y0), (bx + ux * 2, by + uy * 2)], fill=(255, 255, 255, 255), width=11)
    d2.ellipse([x0 - 11, y0 - 11, x0 + 11, y0 + 11], fill=(255, 255, 255, 255))
    d2.polygon(head, fill=(255, 255, 255, 255))
    fr.alpha_composite(sh); fr.alpha_composite(lay2)

def ring_at(fr, x, y, k, r=62):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    r = r * (1.3 - 0.3 * k)
    d.ellipse([x - r, y - r, x + r, y + r], outline=(0, 0, 0, int(120 * k)), width=9)
    d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255, int(255 * k)), width=5)
    fr.alpha_composite(lay)

f_ans = F('NotoSansCJK-Black', 128); f_tel = F('NotoSansCJK-Black', 64); f_cart = F('NotoSansCJK-Bold', 40); f_ctit = F('NotoSerifCJK-Bold', 70)

def overlays(fr, i, t):
    w = WORKS[i]; cam = cam_at(w['cam'], t)
    a, b = w['telop']
    if a <= t < b:
        k = min(eo((t - a) / 0.3), eo((b - t) / 0.3))
        put_block(fr, ('tel', i), ['視線の先には', '何がある？'], f_tel, 84, 270, k, int(6 * (1 - k)), track=3, stroke=5)
    (s, e, a0, a1) = w['arrow']
    if t >= a0:
        k = ease((t - a0) / (a1 - a0)) if t < a1 else 1.0
        fade = 1.0 if t < w['answer'][2] else max(0.0, 1 - (t - w['answer'][2]) / 0.4)
        if fade > 0:
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            arrow(lay, to_screen(cam, *s), to_screen(cam, *e), k)
            if fade < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * fade)))
            fr.alpha_composite(lay)
    if 'ring' in w:
        (rx, ry), r0, r1, rr = w['ring']
        if r0 <= t < r1:
            k = min(eo((t - r0) / 0.3), eo((r1 - t) / 0.3)); ring_at(fr, *to_screen(cam, rx, ry), k, rr)
    txt, a, b, y = w['answer']
    if a <= t < b:
        k = min(eo((t - a) / 0.18), eo((b - t) / 0.25)); sc = 1.0 + 0.12 * (1 - eo((t - a) / 0.25))
        im, sh = text_block(('ans', i), [txt], f_ans, 150, track=3, stroke=7)
        if sc != 1.0:
            im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS); sh = sh.resize(im.size, Image.LANCZOS)
        x = (W - im.width) / 2; yy = y - (im.height - 150 * 1) / 2 * (sc - 1)
        blit(fr, sh, x, yy + 6, k); blit(fr, im, x, yy, k)
    art, tit, a, b = w['card']
    if a <= t < b + 0.3:
        k = min(eo((t - a) / 0.35), 1.0 if t < b else max(0.0, 1 - (t - b) / 0.3))
        put_block(fr, ('cart', i), [art], f_cart, 56, 270, k, int(6 * (1 - k)), track=3, stroke=3)
        put_block(fr, ('ctit', i), [tit], f_ctit, 92, 330, k, int(6 * (1 - k)), track=3, stroke=4)

SUB_Y = 1335
SUBS = [
    (0.20, 3.00, ['絵の中の視線を、', '矢印で追います。']),
    (5.95, 9.00, ['宮廷の人々の視線を、', '奥の鏡へ。']),
    (11.75, 14.75, ['鏡の中に、', '二人の姿が映っています。']),
    (15.45, 17.25, ['水面へ向かう視線。']),
    (19.60, 21.35, ['矢印の先は……']),
    (23.35, 26.90, ['ナルキッソスは、水に', '映る自分に見入っています。']),
    (27.50, 30.40, ['下の天使たちの視線を、', '上へ。']),
    (30.50, 32.10, ['その先にいるのは……']),
    (33.70, 36.45, ['二人は、雲の上を', '見上げています。']),
    (36.85, 39.10, ['女性の目線をたどると……']),
    (41.40, 45.45, ['静かな画面で、動いて見える', 'のは牛乳の流れだけ。']),
    (46.00, 47.90, ['猫たちの視線の先には？']),
    (48.25, 50.90, ['矢印は、紐の先へ……']),
    (52.45, 56.10, ['子どもが紐でつなぎ、猫たちは', '鳥を見つめています。']),
    (56.60, 59.00, ['どの作品の視線が', '気になりましたか？']),
]
def subtitles(fr, t):
    for i, s in enumerate(SUBS):
        a, b, lines = s[:3]; y = s[3] if len(s) > 3 else SUB_Y
        if a <= t < b:
            k = min(eo((t - a) / 0.2), eo((b - t) / 0.18))
            put_block(fr, ('sub', i), lines, f_sub, 76, y, k, int(6 * (1 - k)))

def cover_text(fr, t):
    if t > 3.45: return
    k = eo((3.45 - t) / 0.3)
    cols1 = [RED + (255,) if i <= 1 else (255, 255, 255, 255) for i in range(len('視線の先には'))]
    put_block(fr, 'cover', ['視線の先には', '何がある？'], f_cover, 116, 520, k, 0, track=3, stroke=5, colors=[cols1, None])

# collage for the closing question: the five works in a 2-3 grid
def _collage():
    fr = Image.new('RGBA', (W, H), (12, 12, 12, 255))
    cells = [(60, 330, 470, 560), (550, 330, 470, 560), (60, 920, 310, 400), (385, 920, 310, 400), (710, 920, 310, 400)]
    order = ['las-meninas', 'sistine-madonna', 'narcissus', 'milkmaid', 'osorio']
    for (x, y, w, h), n in zip(cells, order):
        im = P[n]['src'].convert('RGB'); sw, sh = im.size; sc = max(w / sw, h / sh)
        im = im.resize((int(sw * sc) + 1, int(sh * sc) + 1), Image.LANCZOS)
        im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
        fr.paste(im, (x, y))
    return fr
COLLAGE = _collage()
BG = P['osorio']['bg']

def painting_frame(t):
    if t >= T_COLLAGE:
        fr = COLLAGE.copy()
        if t < T_COLLAGE + XF: fr = Image.blend(work_frame(4, t), fr, ease((t - T_COLLAGE) / XF))
        return fr
    i = work_at(t); fr = work_frame(i, t)
    if i > 0 and t < WORKS[i]['t0'] + XF:
        prev = work_frame(i - 1, t); overlays(prev, i - 1, t)
        fr = Image.blend(prev, fr, ease((t - WORKS[i]['t0']) / XF)); return fr, i, True
    return fr, i, False
def product_img(t):
    k = (t - T_PROD) / (T_END - T_PROD); kk = ease(k) * 0.8 + k * 0.2
    cam = (962, lerp(640, 600, kk), lerp(720, 640, kk))
    return view(TEE, cam, off=False)

def _grad(y0, y1, a0, a1):
    g = np.zeros((H, W, 4), np.uint8)
    ys = np.arange(H)
    k = np.clip((ys - y0) / (y1 - y0), 0, 1)
    g[..., 3] = (np.clip(lerp(a0, a1, k), 0, 1) * 255).astype(np.uint8)[:, None]
    return Image.fromarray(g, 'RGBA')
TOPG = _grad(0, 560, 0.55, 0.0)
BOTG = _grad(1150, 1920, 0.0, 0.62)

def logo(fr, a=1.0, width=300, cy=175):
    key = ('logo', width)
    if key not in _cache:
        _cache[key] = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    lg = _cache[key]; blit(fr, lg, W / 2 - lg.width / 2, cy - lg.height / 2, a)


def product_text(fr, t):
    kk = eo((t - T_PROD - 0.2) / 0.5)
    put_block(fr, 'copy', ['名画を着る、', '知ればもっと着たくなる。'], f_copy, 86, 1250, kk, int(10 * (1 - kk)), track=3, stroke=4)
    ku = eo((t - T_PROD - 0.9) / 0.5)
    put_block(fr, 'url', ['mirabilia.base.shop'], f_url, 50, 1450, ku, 0, track=1, stroke=3)

def endcard(t):
    te = t - T_END
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    steps = [0.0, 0.25, 0.5, 0.75]
    k = eo((te - steps[0]) / 0.4); logo(fr, k, 620, 690 + int(10 * (1 - k)))
    d = ImageDraw.Draw(fr); k = eo((te - steps[1]) / 0.4)
    if k > 0: d.line([(W / 2 - 180 * k, 840), (W / 2 + 180 * k, 840)], fill=(255, 255, 255, 255), width=2)
    k = eo((te - steps[2]) / 0.4)
    put_block(fr, 'ecopy', ['名画を着る、知ればもっと着たくなる。'], f_end_copy, 60, 890, k, int(8 * (1 - k)), track=3, stroke=0)
    k = eo((te - steps[3]) / 0.4)
    if k > 0:
        s = '購入はプロフィールから'
        put_block(fr, 'cta', [s], f_cta, 70, 1030, k, int(8 * (1 - k)), track=3, stroke=0)
        tw = jp_width(s, f_cta, 3); y = 1030 + 10 + 80 + int(8 * (1 - k))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rectangle([W / 2 - tw / 2, y, W / 2 + tw / 2, y + 5], fill=(255, 255, 255, int(255 * k)))
        fr.alpha_composite(lay)
    return fr

SPEED = 1.3
T_END_OUT = T_END / SPEED
T_FIN_OUT = T_END_OUT + (T_FIN - T_END)
def src_time(t_out):
    return t_out * SPEED if t_out < T_END_OUT else T_END + (t_out - T_END_OUT)

def frame_at_orig(t):
    if t >= T_END:
        fr = endcard(t)
        if t < T_END + 0.4:  # crossfade from product
            prev = frame_at_main(t)
            fr = Image.blend(prev, fr, ease((t - T_END) / 0.4))
        return fr.convert('RGB')
    return frame_at_main(t).convert('RGB')

def frame_at_main(t):
    fr = BG.copy()
    if t < T_PROD:
        fr.alpha_composite(painting(t))
    else:
        p = product_img(t)
        if t < T_PROD + 0.5:
            pa = BG.copy(); pa.alpha_composite(painting(t))
            pb = BG.copy(); pb.alpha_composite(p)
            fr = Image.blend(pa, pb, ease((t - T_PROD) / 0.5))
        else:
            fr.alpha_composite(p)
    fr.alpha_composite(TOPG); fr.alpha_composite(BOTG)
    logo(fr)
    cover_text(fr, t); ship_ring(fr, t); subtitles(fr, t); title_card(fr, t)
    if t >= T_PROD: product_text(fr, t)
    return fr


def frame_at_main(t):
    if t < T_PROD:
        r = painting_frame(t)
        if isinstance(r, tuple):
            fr, i, xf = r
            overlays(fr, i, t)
        else:
            fr = r
    else:
        p = product_img(t); pb = BG.copy(); pb.alpha_composite(p)
        if t < T_PROD + 0.5:
            fr = Image.blend(COLLAGE.copy(), pb, ease((t - T_PROD) / 0.5))
        else:
            fr = pb
    fr.alpha_composite(TOPG); fr.alpha_composite(BOTG)
    logo(fr)
    cover_text(fr, t); subtitles(fr, t)
    if t >= T_PROD: product_text(fr, t)
    return fr

def frame_at(t_out):
    return frame_at_orig(src_time(t_out))

SEGS = [(0.0, 10.0), (10.0, 20.0), (20.0, 30.0), (30.0, 40.0), (40.0, T_FIN_OUT)]

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for ts in sys.argv[2:]: frame_at(float(ts)).save(D + 'st_%s.png' % ts)
    elif sys.argv[1] == 'cover':
        frame_at(0.0).save(D + 'st_cover.png')
    else:
        i = int(sys.argv[2]); a, b = SEGS[i]
        tmp = D + 'seg%d.tmp.mp4' % i
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H),
                              '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                              '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
        for n in range(round(a * FPS), round(b * FPS)): p.stdin.write(frame_at(n / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.rename(tmp, D + 'seg%d.mp4' % i)
        else: sys.exit(1)
