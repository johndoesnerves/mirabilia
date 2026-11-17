"""MIRABILIA reel: Caravaggio《David with the Head of Goliath》 (horror line #3, brief 2026-11-17). Main part at 1.3x, end card at 1x.
Times in SUBS / camera keys are on the original narration at 1x (image pixel coords); frame_at() maps output time."""
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
A = W / H
D = '/tmp/car/'
OX, OY = 0, 0
SRC = Image.open(D + 'caravaggio.jpg').convert('RGBA')
SW, SH = SRC.size
TEE = Image.open(D + 'caravaggio-blacktee-mockup.jpg').convert('RGBA')
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

# blurred painting behind views that do not fill the frame
_sc = max(W / SW, H / SH)
_bg = SRC.convert('RGB').resize((int(SW * _sc) + 1, int(SH * _sc) + 1), Image.LANCZOS)
_bg = _bg.crop(((_bg.width - W) // 2, (_bg.height - H) // 2, (_bg.width - W) // 2 + W, (_bg.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(40))
BG = Image.blend(_bg, Image.new('RGB', (W, H), (0, 0, 0)), 0.45).convert('RGBA')

# whole painting, slightly inside the width, sitting low (screen y ~560..1775) so the title fits above it
_wf = SW * 1.1; _hf = _wf / A
FULLV = (SW / 2, -560 / H * _hf + _hf / 2, _wf)
BOTH = (820, SH / 2, SH * A)            # height-fit: boy and head together
BOY = (641, 600, 560); BOY2 = (641, 570, 470); HEAD = (1110, 1234, 560)
SHOTS = [
    (0.0,  [(0.0, *BOTH), (1.2, *BOTH), (3.9, *BOY), (6.8, 641, 590, 520),                                  # boy and head -> the boy's face
            (7.6, 641, 590, 520), (10.3, *HEAD),                                                              # follow his gaze down to the head
            (11.0, *HEAD), (12.6, *BOY), (14.4, *BOY2), (16.3, *BOY2), (17.6, 1100, 1220, 520),               # back to the boy, closer; the head again
            (19.2, 1100, 1225, 500)]),
    (19.4, [(19.4, 641, 575, 480), (20.6, 641, 575, 480), (23.4, *BOTH)]),                                   # last look at the boy -> both
    (23.9, [(23.9, *FULLV), (28.85, FULLV[0], FULLV[1], FULLV[2] * 0.98)]),                                  # whole painting + title above it
]
T_PROD = 28.85; T_END = 33.68; T_FIN = 36.88
XF = 0.45
def painting(t):
    idx = max(i for i, (ts, _) in enumerate(SHOTS) if t >= ts)
    im = view(SRC, cam_at(SHOTS[idx][1], t))
    ts = SHOTS[idx][0]
    if idx > 0 and t < ts + XF:
        im = Image.blend(view(SRC, cam_at(SHOTS[idx - 1][1], t)), im, ease((t - ts) / XF))
    return im

def to_screen(cam, x, y):
    cx, cy, w = cam; h = w / A
    return (x - (cx - w / 2)) / w * W, (y - (cy - h / 2)) / h * H

def ring_at(fr, x, y, k, r=62):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    r = r * (1.3 - 0.3 * k)
    d.ellipse([x - r, y - r, x + r, y + r], outline=(0, 0, 0, int(120 * k)), width=9)
    d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255, int(255 * k)), width=5)
    fr.alpha_composite(lay)

def product_img(t):
    k = (t - T_PROD) / (T_END - T_PROD); kk = ease(k) * 0.8 + k * 0.2
    cam = (962, lerp(660, 650, kk), lerp(720, 680, kk))
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

SUB_Y = 1335; SUB_TOP = 300
SUBS = [
    (0.10, 3.60, ['少年が、切り落とされた', '男の頭を持っています。']),
    (4.15, 7.00, ['勝ったはずなのに、', '少年は笑っていません。']),
    (7.30, 10.55, ['その視線は、', '手に持つ首へ向かっています。']),
    (11.20, 13.75, ['どうしてこんなに', '悲しそうな顔なのでしょう。']),
    (14.45, 16.10, ['勝者の顔を見ていると、']),
    (16.20, 19.40, ['喜びよりも哀れみに近い', '感情が見えてきます。']),
    (20.10, 23.35, ['あなたはこの顔を、', '勝利の表情だと思いますか。']),
]

def subtitles(fr, t):
    for i, s in enumerate(SUBS):
        a, b, lines = s[:3]; y = s[3] if len(s) > 3 else SUB_Y
        if a <= t < b:
            k = min(eo((t - a) / 0.2), eo((b - t) / 0.18))
            put_block(fr, ('sub', i), lines, f_sub, 76, y, k, int(6 * (1 - k)))

def cover_text(fr, t):
    if t > 2.6: return
    k = eo((2.6 - t) / 0.3)
    l1, l2 = '勝った少年が', '笑っていない？'
    white = (255, 255, 255, 255); red = RED + (255,)
    cols2 = [red if i <= 5 else white for i in range(len(l2))]
    put_block(fr, 'cover', [l1, l2], f_cover, 116, 860, k, 0, track=3, stroke=5, colors=[None, cols2])

f_work2 = F('NotoSerifCJK-Bold', 64)
def title_card(fr, t):
    a, b = 24.40, T_PROD
    if not (a <= t < b + XF): return
    k = min(eo((t - a) / 0.5), 1.0 if t < b else max(0.0, 1 - (t - b) / XF))
    put_block(fr, 'artist', ['カラヴァッジョ'], f_artist, 60, 262, k, int(8 * (1 - k)), track=4, stroke=3)
    put_block(fr, 'work', ['《ゴリアテの頭を持つダヴィデ》'], f_work2, 84, 322, k, int(8 * (1 - k)), track=3, stroke=4)
    put_block(fr, 'meta', ['c.1610｜ボルゲーゼ美術館'], f_meta, 44, 420, k * 0.95, 0, track=2, stroke=3)

def product_text(fr, t):
    kk = eo((t - T_PROD - 0.2) / 0.5)
    put_block(fr, 'copy', ['名画を着る、', '知ればもっと着たくなる。'], f_copy, 86, 1490, kk, int(10 * (1 - kk)), track=3, stroke=4)
    ku = eo((t - T_PROD - 0.9) / 0.5)
    put_block(fr, 'url', ['mirabilia.base.shop'], f_url, 50, 1690, ku, 0, track=1, stroke=3)

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
    cover_text(fr, t); subtitles(fr, t); title_card(fr, t)
    if t >= T_PROD: product_text(fr, t)
    return fr

def frame_at(t_out):
    return frame_at_orig(src_time(t_out))

SEGS = [(0.0, 8.0), (8.0, 16.0), (16.0, 24.0), (24.0, T_FIN_OUT)]

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
