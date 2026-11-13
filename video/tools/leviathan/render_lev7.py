import sys, os, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
SRC = Image.open('/tmp/lev/leviathan-original-2000.jpg').convert('RGB').crop((8, 8, 1992, 2482))
TEE_PATH = os.environ.get('TEE', '/tmp/lev/leviathan-blacktee-product.png')
TEE = Image.open(TEE_PATH).convert('RGB')
LOGO_PATH = os.environ.get('LOGO')  # black logo PNG (transparent) when provided
SW, SH = SRC.size

INK = (17, 17, 17); GREY = (120, 120, 120); PAPER = (255, 255, 255)
CJK = '/usr/share/fonts/opentype/noto/'
def fj(name, size): return ImageFont.truetype(CJK + name + '.ttc', size, index=0)
def fl(path, size, var=None):
    f = ImageFont.truetype(path, size)
    if var: f.set_variation_by_axes(var)
    return f
BASK = '/usr/share/fonts/truetype/baskerville/GFSBaskerville.otf'
LORA_I = '/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
INTER_L = '/usr/share/fonts/opentype/inter/Inter-Light.otf'
INTER_M = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'

f_meta = fj('NotoSansCJK-Regular', 26)
f_title = fj('NotoSerifCJK-SemiBold', 62)
f_sub = fj('NotoSansCJK-Medium', 43)
f_idx = fl(LORA_I, 30, [400])
f_idx_s = fl(INTER_L, 20)

# layout
LOGO_Y = 168
META_Y = 252
TITLE_Y = 296
FX, FY, FW, FH = 90, 418, 900, 830
A = FW / FH
IDX_Y = FY + FH + 22
SUB_Y = 1292
BAND_Y = 1546
CX = 540

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def eo(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def lerp(a, b, k): return a + (b - a) * k

PUNCT_TAIL = '、。，．）」』'
def is_cjk(text): return any(ord(c) > 0x2E80 for c in text)
def tracked(d, xy, text, font, fill, track, anchor_center=False):
    feats = ['palt'] if is_cjk(text) else None
    ws = [font.getlength(c, features=feats) for c in text]; tw = sum(ws) + track * (len(text) - 1)
    x, y = xy
    if anchor_center:
        eff = tw - (ws[-1] * 0.5 if text and text[-1] in PUNCT_TAIL else 0)
        x -= eff / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=font, fill=fill, features=feats); x += w + track
    return tw

_cache = {}
def layer_text(key, draw_fn, size=(W, 140)):
    if key not in _cache:
        im = Image.new('RGBA', size, (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(im)); _cache[key] = im
    return _cache[key]

def blit(fr, im, x, y, alpha):
    if alpha <= 0: return
    if alpha < 1:
        im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    fr.paste(im, (int(x), int(y)), im)

def logo_layer(width):
    key = ('logo', width)
    if key in _cache: return _cache[key]
    if LOGO_PATH:
        lg = Image.open(LOGO_PATH).convert('RGBA')
        lg = lg.crop(lg.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox())
        h = int(lg.height * width / lg.width); lg = lg.resize((width, h), Image.LANCZOS)
    else:
        size = int(42 * width / 330)
        f = fl('/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf', size, [500]); s = 'MIRABILIA'; tr = size * 0.30
        tw = sum(f.getlength(c) for c in s) + tr * (len(s) - 1)
        lg = Image.new('RGBA', (int(tw) + 4, int(size * 1.3)), (0, 0, 0, 0))
        tracked(ImageDraw.Draw(lg), (0, 0), s, f, INK + (255,), tr)
    _cache[key] = lg; return lg

def draw_logo(fr, alpha=1.0, width=300, cy=LOGO_Y):
    lg = logo_layer(width); blit(fr, lg, CX - lg.width / 2, cy - lg.height / 2, alpha)

def centered_lines(key, lines, font, lh, track=0, fill=INK):
    def fn(d):
        for i, l in enumerate(lines):
            tracked(d, (CX, i * lh), l, font, fill + (255,), track, anchor_center=True)
    return layer_text(key, fn, (W, lh * len(lines) + 30))

# ---------- camera ----------
def cam_at(keys, t):
    if t <= keys[0][0]: return keys[0][1:]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if t <= t1:
            k = ease((t - t0) / (t1 - t0)); return tuple(lerp(p, q, k) for p, q in zip(a, b))
    return keys[-1][1:]

def view(src, cam, fill=PAPER):
    cx, cy, w = cam; h = w / A
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    im = src.transform((FW, FH), Image.EXTENT, box, Image.BICUBIC, fillcolor=fill)
    def to_s(x, y): return ((x - box[0]) / w * FW, (y - box[1]) / h * FH)
    return im, to_s, FW / w

def ring(im, to_s, sc, cx, cy, r, prog, alpha=1.0):
    if prog <= 0 or alpha <= 0: return
    sx, sy = to_s(cx, cy); sr = r * sc
    end = -90 + 360 * eo(prog)
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.arc([sx - sr - 3, sy - sr - 3, sx + sr + 3, sy + sr + 3], -90, end, fill=(0, 0, 0, int(110 * alpha)), width=7)
    d.arc([sx - sr, sy - sr, sx + sr, sy + sr], -90, end, fill=(255, 255, 255, int(255 * alpha)), width=4)
    im.paste(lay, (0, 0), lay)

def ring_track(stops):
    def f(im, to_s, sc, t):
        if t < stops[0][0]: return
        cur = stops[0][1:]
        for (t0, *a), (t1, *b) in zip(stops, stops[1:]):
            if t >= t0:
                k = ease((t - t0) / (t1 - t0)) if t < t1 else 1
                cur = tuple(lerp(p, q, k) for p, q in zip(a, b))
        cx, cy, r, al = cur
        ring(im, to_s, sc, cx, cy, r, (t - stops[0][0]) / 0.6, al)
    return f

FULL = (SW / 2, SH / 2, (SH + 70) * A)
MON = (950, 1600, 560); HEAD = (690, 1640, 230); GOD = (1330, 400, 270); SWORD = (1155, 540, 165)

CUTS = [
    (0.0, 4.13, [(0, FULL[0], FULL[1], FULL[2] * 1.02), (4.5, FULL[0], FULL[1] + 20, FULL[2] * 0.95)], []),
    (4.13, 12.58, [(0, FULL[0], FULL[1], FULL[2] * 0.96), (8.45, FULL[0], FULL[1], FULL[2] * 0.9)],
     [ring_track([(0.6, *MON, 1), (1.9, *MON, 1), (2.5, *GOD, 1), (4.3, *GOD, 1), (4.8, *GOD, 0)])]),
    (12.58, 19.89, [(0, 900, 1650, 1300), (1.3, 780, 1680, 900), (7.31, 770, 1680, 820)],
     [ring_track([(1.2, *HEAD, 1), (2.6, *HEAD, 1), (3.1, *HEAD, 0)])]),
    (19.89, 27.42, [(0, 1100, 800, 1700), (1.5, 1320, 450, 950), (7.53, 1320, 440, 880)], []),
    (27.42, 32.34, [(0, 1320, 440, 880), (0.9, 1170, 540, 600), (4.92, 1165, 540, 560)],
     [ring_track([(1.1, *SWORD, 1), (4.92, *SWORD, 1)])]),
    (32.34, 38.47, [(0, 820, 1650, 1250), (6.13, 780, 1680, 880)], []),
    (38.47, 44.30, [(0, 780, 1680, 880), (2.6, *FULL), (5.83, FULL[0], FULL[1], FULL[2] * 0.97)], []),
]
XF = 0.4  # crossfade

SUBS = [
    (0.00, 3.90, ['この怪物、戦う前から', '負けている？']),
    (4.08, 8.30, ['画面いっぱいに暴れる怪物と、', '雲の上の小さな神。']),
    (8.60, 12.30, ['でも、体の大きさで', '勝敗は決まりません。']),
    (12.53, 14.95, ['この怪物は、リヴァイアサン。']),
    (15.18, 19.60, ['聖書のヨブ記では、', '人間の槍さえ通じない存在です。']),
    (19.84, 22.80, ['ところが、この絵の', 'もとになったイザヤ書では、']),
    (22.88, 27.10, ['神が剣でこの怪物を罰すると、', '予告されています。']),
    (27.37, 28.55, ['見てください。']),
    (28.68, 32.05, ['絵の中の剣は、', 'まだ振り下ろされていません。']),
    (32.29, 34.25, ['それでも、預言を知ると、']),
    (34.30, 38.20, ['怪物の大暴れが、', '最後のあがきに見えてくる。']),
    (38.42, 40.85, ['描かれているのは、決着の前。']),
    (41.02, 44.30, ['けれど、結末はもう、', '語られているのです。']),
]

def cut_image(i, tg):
    a, b, keys, rings = CUTS[i]; t = tg - a
    im, to_s, sc = view(SRC, cam_at(keys, t))
    for rr in rings: rr(im, to_s, sc, t)
    return im

def frame_rule(fr):
    d = ImageDraw.Draw(fr)
    d.rectangle([FX - 1, FY - 1, FX + FW, FY + FH], outline=(200, 200, 200), width=1)

def header(fr, meta, title_lines, t_in=None, tg=0):
    m = centered_lines(('meta', meta), [meta], f_meta, 34, track=4, fill=GREY)
    blit(fr, m, 0, META_Y, 1)
    tl = centered_lines(('title', tuple(title_lines)), title_lines, f_title, 84, track=4)
    k = 1 if t_in is None else eo((tg - t_in) / 0.4)
    blit(fr, tl, 0, TITLE_Y + 10 * (1 - k), k)

def index_line(fr, n, total, label):
    d = ImageDraw.Draw(fr)
    s = '%02d' % n
    d.text((FX, IDX_Y), s, font=f_idx, fill=INK)
    x = FX + f_idx.getlength(s) + 14
    d.line([(x, IDX_Y + 22), (x + 46, IDX_Y + 22)], fill=INK, width=1)
    d.text((x + 58, IDX_Y + 7), ('%02d' % total), font=f_idx_s, fill=GREY)

f_band = fj('NotoSansCJK-Medium', 30)
def band(fr, alpha=1.0):
    def fn(d):
        s = '限定アパレル販売中'
        tw = sum(f_band.getlength(c, features=['palt']) for c in s) + 7 * (len(s) - 1)
        d.line([(FX, 0), (FX + FW, 0)], fill=(205, 205, 205, 255), width=1)
        tracked(d, (CX, 26), s, f_band, INK + (255,), 7, anchor_center=True)
    im = layer_text('band2', fn, (W, 80))
    blit(fr, im, 0, BAND_Y, alpha)

import glob
CAR_Y = 1640; CAR_S = 120; CAR_GAP = 16; CAR_SPEED = 45.0
_car = {}
def carousel_strip():
    if 'strip' in _car: return _car['strip'], _car['mask'], _car['period']
    fs = sorted(glob.glob('/tmp/lev/car/*.jpg'))
    tiles = [Image.open(f).convert('RGB').resize((CAR_S, CAR_S), Image.LANCZOS) for f in fs]
    period = len(tiles) * (CAR_S + CAR_GAP)
    strip = Image.new('RGB', (period * 2 + CAR_S, CAR_S), PAPER)
    for k in range(2 * len(tiles) + 1):
        strip.paste(tiles[k % len(tiles)], (k * (CAR_S + CAR_GAP), 0))
    mask = Image.new('L', (W, CAR_S), 255)
    md = ImageDraw.Draw(mask); fade = 150
    for x in range(fade):
        v = int(255 * ease(x / fade)); md.line([(x, 0), (x, CAR_S)], fill=v); md.line([(W - 1 - x, 0), (W - 1 - x, CAR_S)], fill=v)
    _car.update(strip=strip, mask=mask, period=period)
    return strip, mask, period

CAR_N = 6
def carousel(fr, tg, alpha=1.0):
    if alpha <= 0: return
    if 'row' not in _car:
        fs = sorted(glob.glob('/tmp/lev/car/*.jpg'))[:CAR_N]
        tw = CAR_N * CAR_S + (CAR_N - 1) * CAR_GAP
        row = Image.new('RGB', (tw, CAR_S), PAPER)
        for k, f in enumerate(fs):
            row.paste(Image.open(f).convert('RGB').resize((CAR_S, CAR_S), Image.LANCZOS), (k * (CAR_S + CAR_GAP), 0))
        _car['row'] = row
    row = _car['row']
    x = CX - row.width // 2
    if alpha >= 1: fr.paste(row, (x, CAR_Y))
    else: fr.paste(Image.blend(fr.crop((x, CAR_Y, x + row.width, CAR_Y + CAR_S)), row, alpha), (x, CAR_Y))

def subtitles(fr, tg):
    for i, (a, b, lines) in enumerate(SUBS):
        if a <= tg < b:
            k = min(eo((tg - a) / 0.25), eo((b - tg) / 0.2))
            im = centered_lines(('sub', i), lines, f_sub, 68, track=2)
            blit(fr, im, 0, SUB_Y + 8 * (1 - k), k)

LABELS = ['THE DESTRUCTION OF LEVIATHAN', 'GIANT / SMALL GOD', 'LEVIATHAN', 'ISAIAH 27:1', 'THE SWORD', 'LAST STRUGGLE', 'BEFORE THE END']

def story(tg):
    fr = Image.new('RGB', (W, H), PAPER)
    draw_logo(fr)
    header(fr, 'ドレ｜1866年', ['戦う前から、負けている？'])
    idx = max(i for i, c in enumerate(CUTS) if tg >= c[0])
    im = cut_image(idx, tg)
    if idx > 0 and tg - CUTS[idx][0] < XF:
        prev = cut_image(idx - 1, tg)
        im = Image.blend(prev, im, ease((tg - CUTS[idx][0]) / XF))
    fr.paste(im, (FX, FY)); frame_rule(fr)
    band(fr)
    carousel(fr, tg)
    subtitles(fr, tg)
    return fr

T_PROD, T_END, T_FIN = 44.30, 47.30, 51.30
f_avail = fl(INTER_L, 23)
f_sale = fj('NotoSerifCJK-SemiBold', 62)
f_url = fl(INTER_M, 30)

def product(tg):
    t = tg - T_PROD
    fr = Image.new('RGB', (W, H), PAPER)
    draw_logo(fr)
    s = centered_lines('sale', ['販売中'], f_sale, 84, track=10); k = eo((t - 0.1) / 0.45)
    blit(fr, s, 0, TITLE_Y + 10 * (1 - k), k)
    kk = ease(t / 3.0) * 0.8 + (t / 3.0) * 0.2
    cam = (lerp(1060, 975, kk), lerp(640, 650, kk), lerp(1470, 840, kk))
    im, _, _ = view(TEE, cam, fill=(222, 222, 222))
    if t < XF:
        im = Image.blend(cut_image(len(CUTS) - 1, tg), im, ease(t / XF))
    fr.paste(im, (FX, FY)); frame_rule(fr)
    band(fr)
    carousel(fr, tg)
    u = centered_lines('url', ['mirabilia.base.shop'], f_url, 40, track=2)
    blit(fr, u, 0, SUB_Y + 20, eo((t - 0.4) / 0.4))
    d = ImageDraw.Draw(fr); k2 = eo((t - 0.6) / 0.5)
    if k2 > 0:
        uw = f_url.getlength('mirabilia.base.shop') + 2 * 18
        d.line([(CX - uw / 2 * k2, SUB_Y + 72), (CX + uw / 2 * k2, SUB_Y + 72)], fill=INK, width=2)
    return fr

f_tag = fj('NotoSerifCJK-Medium', 46)
f_box = fj('NotoSansCJK-Regular', 38)
f_cta = fj('NotoSansCJK-Bold', 50)

def endcard(tg):
    t = tg - T_END
    fr = Image.new('RGB', (W, H), PAPER)
    # small persistent logo hands over to the large one
    draw_logo(fr, 1 - eo(t / 0.35))
    band(fr, 1 - eo(t / 0.35))
    carousel(fr, tg, 1 - eo(t / 0.35))
    steps = [0.0, 0.35, 0.7, 1.05, 1.4]
    k = eo((t - steps[0]) / 0.45)
    lg = logo_layer(560); blit(fr, lg, CX - lg.width / 2, 640 - lg.height / 2 + 14 * (1 - k), k)
    d = ImageDraw.Draw(fr); k = eo((t - steps[1]) / 0.45)
    if k > 0: d.line([(CX - 170 * k, 760), (CX + 170 * k, 760)], fill=INK, width=1)
    tl = centered_lines('tag', ['失われた記憶を身にまとう。'], f_tag, 60, track=4)
    k = eo((t - steps[2]) / 0.45); blit(fr, tl, 0, 810 + 12 * (1 - k), k)
    k = eo((t - steps[3]) / 0.45)
    if k > 0:
        s = '各図案×仕様は10着限り'
        tw = sum(f_box.getlength(c) for c in s) + 3 * (len(s) - 1)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        y = 975 + 12 * (1 - k)
        ld.rectangle([CX - tw / 2 - 40, y, CX + tw / 2 + 40, y + 92], outline=INK + (int(255 * k),), width=2)
        tracked(ld, (CX, y + 19), s, f_box, INK + (int(255 * k),), 3, anchor_center=True)
        fr.paste(lay, (0, 0), lay)
    k = eo((t - steps[4]) / 0.45)
    if k > 0:
        s = '購入はプロフィールから'
        tw = sum(f_cta.getlength(c) for c in s) + 3 * (len(s) - 1)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        y = 1140 + 12 * (1 - k)
        tracked(ld, (CX, y), s, f_cta, INK + (int(255 * k),), 3, anchor_center=True)
        ld.rectangle([CX - tw / 2, y + 84, CX + tw / 2, y + 88], fill=INK + (int(255 * k),))
        fr.paste(lay, (0, 0), lay)
    return fr

def frame_at(tg):
    if tg < T_PROD: return story(tg)
    if tg < T_END: return product(tg)
    return endcard(tg)

SEGS = [(0.0, 12.58), (12.58, 27.42), (27.42, T_PROD), (T_PROD, T_END), (T_END, T_FIN)]

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for ts in sys.argv[2:]: frame_at(float(ts)).save('/tmp/lev/v7_%s.png' % ts)
    else:
        i = int(sys.argv[2]); a, b = SEGS[i]
        tmp = '/tmp/lev/v7seg%d.tmp.mp4' % i
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H),
                              '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                              '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
        for n in range(round(a * FPS), round(b * FPS)): p.stdin.write(frame_at(n / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.rename(tmp, '/tmp/lev/v7seg%d.mp4' % i)
        else: sys.exit(1)
