"""MIRABILIA reel: Van Gogh《Irises》 (new line #2, 2026-11-16 brief). Main part at 1.3x, end card at 1x."""
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
A = W / H
D = '/tmp/iri/'
OX, OY = 0, 0
SRC = Image.open(D + 'irises-original-full.jpg').convert('RGBA')
SW, SH = SRC.size
TEE = Image.open(D + 'irises-blacktee-mockup.jpg').convert('RGBA')
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
_sc = max(W / SW, H / SH)
_bg = SRC.convert('RGB').resize((int(SW * _sc) + 1, int(SH * _sc) + 1), Image.LANCZOS)
_bg = _bg.crop(((_bg.width - W) // 2, (_bg.height - H) // 2, (_bg.width - W) // 2 + W, (_bg.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(40))
BG = Image.blend(_bg, Image.new('RGB', (W, H), (0, 0, 0)), 0.45).convert('RGBA')

FULLFIT = (SW / 2, SH / 2 + 780, SW + 120)  # painting sits in the upper part, clear of subtitles/title
COVERV = (SW / 2, SH / 2, SH * A)

# painting camera: A = blue iris close-up, B = background -> flowers+background -> full view
CAM_A = [(0.0, 1360, 485, 545), (3.5, 1355, 480, 520), (5.4, 1330, 450, 420), (9.65, 1320, 440, 400)]
CAM_B = [(9.65, 3300, 1100, 1000), (12.2, 3270, 1080, 950), (14.4, 3250, 1080, 930),
         (18.6, 2700, 1590, 1700), (19.9, 2700, 1590, 1700), (21.3, 2700, 1590, 1700),   # hold:「赤い色素が退色」
         (25.9, 2600, 1590, 1720), (26.7, *COVERV), (28.3, *FULLFIT), (43.4, FULLFIT[0], FULLFIT[1], FULLFIT[2] * 0.95)]
T_B = 9.65; T_PROD = 43.40; T_END = 47.45; T_FIN = 50.65
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
    cam = (lerp(962, 962, kk), lerp(640, 560, kk), lerp(720, 600, kk))
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
    (0.10, 3.40, ['この青い花、', 'もとは紫だった？']),
    (3.55, 5.30, ['花びらを見てください。']),
    (5.40, 9.45, ['いま見える青は、ゴッホが', '描いた当時の色とは違うんです。']),
    (9.65, 12.05, ['さらに、', '花の後ろに注目。']),
    (12.15, 14.30, ['淡い背景も、', 'もとはピンク。']),
    (14.40, 18.50, ['紫の花と合わせて、やわらかな', '調和をつくろうとしていました。']),
    (18.65, 21.55, ['ところが、使った', '赤い色素が退色。']),
    (21.62, 26.10, ['花も背景も変わり、絵全体の', '色の関係まで変わってしまいました。']),
    (26.75, 28.75, ['全体を見直してください。']),
    (28.90, 31.95, ['いま見ているのは、', '描かれた当時の姿に、']),
    (32.00, 34.60, ['時間が変化を重ねた', '絵なんです。']),
    (35.15, 39.40, ['当時の紫とピンクに会えたら、', '印象はどう変わると思いますか。']),
]
SUB_Y = 1335

def subtitles(fr, t):
    for i, (a, b, lines) in enumerate(SUBS):
        if a <= t < b:
            k = min(eo((t - a) / 0.2), eo((b - t) / 0.18))
            put_block(fr, ('sub', i), lines, f_sub, 76, SUB_Y, k, int(6 * (1 - k)))

PURPLE = (124, 92, 170); PINK = (236, 190, 204)
f_chip = F('NotoSansCJK-Black', 52); f_note = F('NotoSansCJK-Bold', 28)
def chip(fr, key, label, color, t, a, b, y=300):
    if not (a <= t < b): return
    k = min(eo((t - a) / 0.3), eo((b - t) / 0.3))
    def fn(d):
        tw = jp_width(label, f_chip, 4); bw = tw + 70 + 56
        x0 = W / 2 - bw / 2
        d.rounded_rectangle([x0, 0, x0 + bw, 92], radius=46, fill=(0, 0, 0, 150), outline=(255, 255, 255, 190), width=2)
        d.ellipse([x0 + 26, 22, x0 + 26 + 48, 70], fill=color + (255,), outline=(255, 255, 255, 230), width=3)
        draw_line(d, x0 + 26 + 48 + 18 + tw / 2, 12, label, f_chip, (255, 255, 255, 255), 4)
        draw_line(d, W / 2, 104, '※色のイメージ', f_note, (255, 255, 255, 220), 2, 2, (0, 0, 0, 160))
    blit(fr, layer(key, fn, (W, 150)), 0, y + int(6 * (1 - k)), k)

def cover_text(fr, t):
    chip(fr, 'chip_purple', 'もとは紫', PURPLE, t, 1.45, 5.30)
    chip(fr, 'chip_pink', 'もとはピンク', PINK, t, 13.15, 18.50)

def greek_tag(fr, t):
    return

def title_card(fr, t):
    a, b = 40.15, T_PROD
    if not (a <= t < b + XF): return
    k = min(eo((t - a) / 0.5), 1.0 if t < b else max(0.0, 1 - (t - b) / XF))
    put_block(fr, 'artist', ['フィンセント・ファン・ゴッホ'], f_artist, 60, 1170, k, int(8 * (1 - k)), track=4, stroke=3)
    put_block(fr, 'work', ['《アイリス》'], f_work, 120, 1240, k, int(8 * (1 - k)), track=6, stroke=4)
    put_block(fr, 'meta', ['1890｜メトロポリタン美術館'], f_meta, 44, 1385, k * 0.95, 0, track=2, stroke=3)

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
    cover_text(fr, t); greek_tag(fr, t); subtitles(fr, t); title_card(fr, t)
    if t >= T_PROD: product_text(fr, t)
    return fr

def frame_at(t_out):
    return frame_at_orig(src_time(t_out))

SEGS = [(0.0, 10.0), (10.0, 20.0), (20.0, 30.0), (30.0, T_FIN_OUT)]

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for ts in sys.argv[2:]: frame_at(float(ts)).save(D + 'x13_%s.png' % ts)
    elif sys.argv[1] == 'cover':
        frame_at(0.0).save(D + 'x13_cover.png')
    else:
        i = int(sys.argv[2]); a, b = SEGS[i]
        tmp = D + 'x13seg%d.tmp.mp4' % i
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H),
                              '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                              '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
        for n in range(round(a * FPS), round(b * FPS)): p.stdin.write(frame_at(n / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.rename(tmp, D + 'x13seg%d.mp4' % i)
        else: sys.exit(1)
