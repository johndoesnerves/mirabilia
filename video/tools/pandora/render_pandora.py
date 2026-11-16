"""MIRABILIA reel: Redon《Pandora》 (new line, 2026-11-16 brief)."""
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
A = W / H
D = '/tmp/pan/'
OX, OY = 86, 85  # crop away the black scan border; camera keys stay in full-image coordinates
SRC = Image.open(D + 'pandora-original-full.jpg').convert('RGBA').crop((OX, OY, 1746, 3922))
SW, SH = SRC.size
TEE = Image.open(D + 'pandora-blacktee-mockup.jpg').convert('RGBA')
LOGO = Image.open(D + 'mirabilia-logo-white.png').convert('RGBA')
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

# blurred painting behind full-height shots
_bg = SRC.convert('RGB').resize((W, int(SH * W / SW)), Image.LANCZOS)
_bg = _bg.crop((0, (_bg.height - H) // 2, W, (_bg.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(40))
BG = Image.blend(_bg, Image.new('RGB', (W, H), (0, 0, 0)), 0.45).convert('RGBA')

FULLFIT = (OX + SW / 2, OY + SH / 2, SH * A + 40)
COVERV = (OX + SW / 2, OY + SH / 2, SW)

# painting camera, segment A (box & hands) and B (flowers -> face -> both -> full)
CAM_A = [(0.0, 1060, 1700, 560), (3.6, 1050, 1705, 500), (6.4, 1045, 1715, 470), (9.4, 1040, 1720, 380),
         (11.0, 1040, 1720, 370), (16.3, 1060, 1560, 880), (17.6, 1060, 1550, 900)]
CAM_B = [(17.52, 1000, 3110, 900), (19.7, 1290, 3110, 900), (22.0, 1290, 2500, 900), (22.7, 1290, 2480, 900),
         (24.4, 1060, 1380, 700), (26.28, 1060, 1375, 670),
         (28.6, 1050, 1540, 800), (29.3, 1050, 1540, 800), (31.3, 1050, 1540, 800),   # hold: 「知るだけで」
         (34.3, *COVERV), (35.6, *FULLFIT), (41.94, FULLFIT[0], FULLFIT[1], FULLFIT[2] * 0.97)]
T_B = 17.52; T_PROD = 41.94; T_END = 45.90; T_FIN = 49.10
XF = 0.45

def painting(t):
    if t < T_B:
        return view(SRC, cam_at(CAM_A, t))
    im = view(SRC, cam_at(CAM_B, t))
    if t < T_B + XF:
        im = Image.blend(view(SRC, cam_at(CAM_A, t)), im, ease((t - T_B) / XF))
    return im

def product_img(t):
    k = (t - T_PROD) / (T_END - T_PROD); kk = ease(k) * 0.8 + k * 0.2
    cam = (lerp(962, 962, kk), lerp(640, 600, kk), lerp(760, 430, kk))
    return view(TEE, cam, off=False)

# overlays
def _grad(y0, y1, a0, a1):
    g = np.zeros((H, W, 4), np.uint8)
    ys = np.arange(H)
    k = np.clip((ys - y0) / (y1 - y0), 0, 1)
    g[..., 3] = (np.clip(lerp(a0, a1, k), 0, 1) * 255).astype(np.uint8)[:, None]
    return Image.fromarray(g, 'RGBA')
TOPG = _grad(0, 430, 0.50, 0.0)
BOTG = _grad(1150, 1920, 0.0, 0.62)

def logo(fr, a=1.0, width=300, cy=175):
    key = ('logo', width)
    if key not in _cache:
        _cache[key] = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    lg = _cache[key]; blit(fr, lg, W / 2 - lg.width / 2, cy - lg.height / 2, a)

SUBS = [
    (0.10, 3.70, ['箱は一つ。', '中身は、あらゆる災い。']),
    (3.80, 6.20, ['女性の手元を見てください。']),
    (6.30, 9.95, ['この小さな箱が、', '花園の意味を変えます。']),
    (10.25, 13.40, ['ギリシャ神話では、', '彼女が箱を開けると、']),
    (13.45, 17.20, ['人間を苦しめる災いが', '世界へ広がります。']),
    (17.45, 19.55, ['でも、周りの花に注目。']),
    (19.65, 22.45, ['何も壊れていないし、', '女性も穏やか。']),
    (22.55, 26.05, ['描かれているのは、', '開ける前の静けさなんです。']),
    (26.20, 29.05, ['もう一度、', '箱と顔を見比べてください。']),
    (29.20, 31.15, ['これから起こることを', '知るだけで、']),
    (31.20, 34.95, ['美しい花園に、', '不穏な気配が生まれます。']),
    (35.15, 38.95, ['あなたには、最初と同じ', '景色に見えますか。']),
]
SUB_Y = 1335

def subtitles(fr, t):
    for i, (a, b, lines) in enumerate(SUBS):
        if a <= t < b:
            k = min(eo((t - a) / 0.2), eo((b - t) / 0.18))
            put_block(fr, ('sub', i), lines, f_sub, 76, SUB_Y, k, int(6 * (1 - k)))

def cover_text(fr, t):
    if t > 3.9: return
    k = min(1.0 if t < 0.05 else 1.0, eo((3.9 - t) / 0.35))
    l1, l2 = '一つの箱から', '世界に災いが広がる。'
    white = (255, 255, 255, 255); red = RED + (255,)
    cols2 = [red if 3 <= i <= 4 else white for i in range(len(l2))]
    put_block(fr, 'cover', [l1, l2], f_cover, 116, 470, k, 0, track=3, stroke=5, colors=[None, cols2])

def greek_tag(fr, t):
    a, b = 10.25, 16.9
    if not (a <= t < b): return
    k = min(eo((t - a) / 0.3), eo((b - t) / 0.3))
    def fn(d):
        s = 'ギリシャ神話'; tw = jp_width(s, f_tag, 6)
        d.rounded_rectangle([W / 2 - tw / 2 - 30, 0, W / 2 + tw / 2 + 30, 60], radius=30, fill=(0, 0, 0, 150),
                            outline=(255, 255, 255, 170), width=2)
        draw_line(d, W / 2, 8, s, f_tag, (255, 255, 255, 255), 6)
    blit(fr, layer('tag', fn, (W, 64)), 0, 280, k)

def title_card(fr, t):
    a, b = 39.10, T_PROD
    if not (a <= t < b + XF): return
    k = min(eo((t - a) / 0.5), 1.0 if t < b else max(0.0, 1 - (t - b) / XF))
    put_block(fr, 'artist', ['オディロン・ルドン'], f_artist, 60, 1170, k, int(8 * (1 - k)), track=4, stroke=3)
    put_block(fr, 'work', ['《パンドラ》'], f_work, 120, 1240, k, int(8 * (1 - k)), track=6, stroke=4)
    put_block(fr, 'meta', ['c.1914｜メトロポリタン美術館'], f_meta, 44, 1385, k * 0.95, 0, track=2, stroke=3)

def product_text(fr, t):
    kk = eo((t - T_PROD - 0.2) / 0.5)
    put_block(fr, 'copy', ['名画を着る、', '知ればもっと着たくなる。'], f_copy, 86, 1230, kk, int(10 * (1 - kk)), track=3, stroke=4)
    ku = eo((t - T_PROD - 0.9) / 0.5)
    put_block(fr, 'url', ['mirabilia.base.shop'], f_url, 50, 1430, ku, 0, track=1, stroke=3)

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

def frame_at(t):
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
    cover_text(fr, t); greek_tag(fr, t); subtitles(fr, t); title_card(fr, t)
    if t >= T_PROD: product_text(fr, t)
    return fr

SEGS = [(0.0, 12.0), (12.0, 24.0), (24.0, 36.0), (36.0, T_FIN)]

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for ts in sys.argv[2:]: frame_at(float(ts)).save(D + 'st_%s.png' % ts)
    elif sys.argv[1] == 'cover':
        frame_at(0.0).save(D + 'cover.png')
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
