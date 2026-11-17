"""MIRABILIA 五選 #2「視線の先には何がある？」 v2 (brief-v2 2026-11-18: answer + reason): camera follows the arrow tip. Five paintings; a white arrow follows each gaze.
Main part at 1.3x, end card at 1x. Times below are on the original narration at 1x; frame_at() maps output time."""
import sys, os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
A = W / H
D = '/tmp/gep2/'
OX, OY = 0, 0
TEE = None   # no product cut in this episode
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
P = {k: load(k) for k in ['painting-01-matthew', 'painting-02-adam', 'painting-03-anatomy', 'painting-04-swing', 'painting-05-kajikazawa']}
def px(name, xp, yp): return (P[name]['w'] * xp / 100, P[name]['h'] * yp / 100)

# each work: start time, camera keys (t, cx, cy, w) in that painting's pixels, arrow (from, to, t0, t1),
# telop span, answer (text, t0, t1, y), name card (artist, title, t0, t1), optional ring on the target
def W_(name, t0, S, E, a0, a1, ws, we, expl_cam, t_end, answer, card, ring_r=None, track_lim=True, reason=''):
    """camera: zoom on the gaze source, then follow the arrow tip from S to E (same easing as the arrow), then settle"""
    S = px(name, *S); E = px(name, *E)
    cam = [(t0, S[0], S[1], ws * 1.25), (a0, S[0], S[1], ws), (a1, E[0], E[1], we), (a1 + 1.4, E[0], E[1], we * 0.96),
           (answer[1] + 2.0, E[0], E[1], we * 0.96), (answer[1] + 3.3, *expl_cam), (t_end, expl_cam[0], expl_cam[1], expl_cam[2] * 0.97)]
    w = dict(name=name, t0=t0, cam=cam, arrow=(S, E, a0, a1), telop=(t0 + 0.15, answer[1] - 0.05),
             answer=answer, card=card, clamp=track_lim, reason=reason)
    if ring_r: w['ring'] = (E, answer[1], answer[2] + 0.6, ring_r)
    return w

WORKS = [
    W_('painting-01-matthew', 0.0, (65.5, 40.5), (31.5, 45.5), 0.7, 2.95, 520, 460, (690, 600, 700), 13.45,
       ('マタイ！', 3.0, 13.45, 430), ('カラヴァッジョ', '《聖マタイの召命》', 5.0, 13.45), ring_r=90, reason='キリストが弟子に呼ぶ瞬間'),
    W_('painting-02-adam', 13.5, (11.5, 38.5), (40.5, 48.5), 14.3, 16.7, 380, 340, (420, 393, 440), 27.15,
       ('神の指先！', 16.75, 27.15, 430), ('ミケランジェロ', '《アダムの創造》', 18.75, 27.15), ring_r=70, reason='命が与えられる瞬間'),
    W_('painting-03-anatomy', 27.2, (36.5, 52.5), (59, 67.5), 28.1, 30.55, 460, 460, (680, 660, 593), 40.95,
       ('解剖中の腕！', 30.6, 40.95, 430), ('レンブラント', '《テュルプ博士の解剖学講義》', 32.6, 40.95), ring_r=95, reason='筋の仕組みを学ぶ授業'),
    W_('painting-04-swing', 41.0, (11.5, 80), (50, 58), 41.8, 44.15, 600, 640, (600, 1250, 900), 55.05,
       ('ぶらんこの女性！', 44.2, 55.05, 430), ('フラゴナール', '《ぶらんこ》', 46.2, 55.05), reason='人目を忍ぶ視線'),
    W_('painting-05-kajikazawa', 55.1, (56, 37), (85, 72), 55.9, 58.2, 460, 460, (940, 400, 522), 69.55,
       ('波間の糸の先！', 58.25, 69.55, 430), ('葛飾北斎', '《冨嶽三十六景 甲州石班沢》', 60.25, 69.55), ring_r=80, reason='糸先で魚を確かめる漁師'),
]
T_COLLAGE = 69.60; T_END = 73.90; T_PROD = T_END; T_FIN = T_END + 3.2   # no product cut this time
XF = 0.4

def work_at(t):
    return max(i for i, w in enumerate(WORKS) if t >= w['t0'])

def wcam(i, t):
    w = WORKS[i]; p = P[w['name']]; cx, cy, cw = cam_at(w['cam'], t); ch = cw / A
    if w.get('clamp') and t < w['answer'][1] + 2.0:
        if cw <= p['w']: cx = min(max(cx, cw / 2), p['w'] - cw / 2)
        if ch <= p['h']: cy = min(max(cy, ch / 2), p['h'] - ch / 2)
    return (cx, cy, cw)

def work_frame(i, t):
    w = WORKS[i]; p = P[w['name']]
    fr = p['bg'].copy(); fr.alpha_composite(view(p['src'], wcam(i, t), off=False))
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

f_ans = F('NotoSansCJK-Black', 128); f_rsn = F('NotoSansCJK-Black', 60); f_tel = F('NotoSansCJK-Black', 64); f_cart = F('NotoSansCJK-Bold', 40); f_ctit = F('NotoSerifCJK-Bold', 70)

def overlays(fr, i, t):
    w = WORKS[i]; cam = wcam(i, t)
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
        nl = len(txt.split('\n'))
        im, sh = text_block(('ans', i), txt.split('\n'), f_ans, 150, track=3, stroke=7)
        if sc != 1.0:
            im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS); sh = sh.resize(im.size, Image.LANCZOS)
        x = (W - im.width) / 2; yy = y - (im.height - 150 * 1) / 2 * (sc - 1)
        blit(fr, sh, x, yy + 6, k); blit(fr, im, x, yy, k)
        if w.get('reason'):
            kr = min(eo((t - a - 0.35) / 0.3), eo((b - t) / 0.25))
            put_block(fr, ('rsn', i), [w['reason']], f_rsn, 80, y + 150 * nl + 10, kr, int(6 * (1 - kr)), track=3, stroke=5)
    art, tit, a, b = w['card']
    if a <= t < b + 0.3:
        k = min(eo((t - a) / 0.35), 1.0 if t < b else max(0.0, 1 - (t - b) / 0.3))
        put_block(fr, ('cart', i), [art], f_cart, 56, 270, k, int(6 * (1 - k)), track=3, stroke=3)
        put_block(fr, ('ctit', i), [tit], f_ctit, 92, 330, k, int(6 * (1 - k)), track=3, stroke=4)

SUB_Y = 1335
SUBS = [
    (4.60, 8.05, ['キリストは、収税所にいた', 'マタイを弟子に呼びます。']),
    (8.65, 13.10, ['髭の男は自分を指し、「私ですか？」', 'と問い返すようです。']),
    (18.20, 22.55, ['神がアダムに命を与えようと', '手を伸ばす場面です。']),
    (23.20, 26.80, ['アダムは神を見上げ、', '二人の指は触れる寸前。']),
    (32.10, 36.25, ['テュルプ博士が腕の筋の', '仕組みを示す授業です。']),
    (36.80, 40.75, ['生徒たちは学ぶため、開かれた', '前腕へ身を乗り出します。']),
    (46.15, 50.10, ['茂みの男は、女性を', '人目を忍んで見つめています。']),
    (50.70, 54.75, ['勢いよく飛ぶ靴も、この秘密めいた', '場面を印象づけます。']),
    (59.95, 65.20, ['漁師は、魚がかかったか', '糸先の動きで確かめているようです。']),
    (65.85, 69.25, ['釣り糸は、波が打ちつける', '岩場の先へ伸びています。']),
    (70.10, 73.40, ['5枚の中で、どの視線が', '気になりましたか？']),
]
def subtitles(fr, t):
    for i, s in enumerate(SUBS):
        a, b, lines = s[:3]; y = s[3] if len(s) > 3 else SUB_Y
        if a <= t < b:
            k = min(eo((t - a) / 0.2), eo((b - t) / 0.18))
            put_block(fr, ('sub', i), lines, f_sub, 76, y, k, int(6 * (1 - k)))

def cover_text(fr, t):
    return
    k = eo((3.45 - t) / 0.3)
    cols1 = [RED + (255,) if i <= 1 else (255, 255, 255, 255) for i in range(len('視線の先には'))]
    put_block(fr, 'cover', ['視線の先には', '何がある？'], f_cover, 116, 520, k, 0, track=3, stroke=5, colors=[cols1, None])

# collage for the closing question: the five works in a 2-3 grid
def _collage():
    fr = Image.new('RGBA', (W, H), (12, 12, 12, 255))
    cells = [(60, 330, 470, 560), (550, 330, 470, 560), (60, 920, 310, 400), (385, 920, 310, 400), (710, 920, 310, 400)]
    order = ['painting-01-matthew', 'painting-02-adam', 'painting-03-anatomy', 'painting-04-swing', 'painting-05-kajikazawa']
    for (x, y, w, h), n in zip(cells, order):
        im = P[n]['src'].convert('RGB'); sw, sh = im.size; sc = max(w / sw, h / sh)
        im = im.resize((int(sw * sc) + 1, int(sh * sc) + 1), Image.LANCZOS)
        im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
        fr.paste(im, (x, y))
    return fr
COLLAGE = _collage()
BG = P['painting-05-kajikazawa']['bg']

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
    if t < T_PROD or T_PROD >= T_END:
        r = painting_frame(min(t, T_END - 1e-3))
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

SEGS = [(0.0, 8.0), (8.0, 16.0), (16.0, 24.0), (24.0, 30.0), (30.0, T_FIN_OUT)]

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for ts in sys.argv[2:]: frame_at(float(ts)).save(D + 'v2b_%s.png' % ts)
    elif sys.argv[1] == 'cover':
        frame_at(0.0).save(D + 'st_cover.png')
    else:
        i = int(sys.argv[2]); a, b = SEGS[i]
        tmp = D + 'v2bseg%d.tmp.mp4' % i
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H),
                              '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                              '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
        for n in range(round(a * FPS), round(b * FPS)): p.stdin.write(frame_at(n / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.rename(tmp, D + 'v2bseg%d.mp4' % i)
        else: sys.exit(1)
