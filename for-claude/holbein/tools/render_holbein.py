"""MIRABILIA reel: Holbein the Younger《The Ambassadors》 (horror line #6, brief 2026-11-17). Main part at 1.3x, end card at 1x.
The anamorphic skull is revealed by squeezing the picture along the skull's long axis (as if seen from low left).
Times in SUBS / camera keys are on the original narration at 1x (image pixel coords); frame_at() maps output time."""
import math
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
A = W / H
D = '/tmp/hol/'
OX, OY = 0, 0
SRC = Image.open(D + 'holbein.jpg').convert('RGBA')
SW, SH = SRC.size
TEE = Image.open(D + 'holbein-blacktee-mockup.jpg').convert('RGBA')
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

# whole painting, width-fit, upper part of the frame (screen y 230..1294)
_wf = SW; _hf = _wf / A
FULLV = (SW / 2, -230 / H * _hf + _hf / 2, _wf)
SKULL = (752, 1392)                       # centre of the stretched skull
TH = math.atan2(-220, 490)                # its long axis (rising to the right)
S_MIN = 0.24                              # squeeze that turns it into a skull
CAM = [(0.0, 790, 1000, 886), (4.1, 752, 1180, 820), (7.4, 752, 1190, 800), (11.4, 752, 1230, 720),
       (15.9, 752, 1250, 660), (16.3, 752, 1250, 660), (18.8, *FULLV), (29.7, FULLV[0], FULLV[1], FULLV[2] * 0.97)]
SQ = [(0.0, 1.0), (8.4, 1.0), (11.4, S_MIN), (16.2, S_MIN), (18.4, 1.0)]
T_PROD = 29.70; T_END = 32.76; T_FIN = 35.96
XF = 0.45

def squeeze(t):
    return cam_at([(k, v) for k, v in SQ], t)[0]

def painting(t):
    cx, cy, w = cam_at(CAM, t); h = w / A; s = squeeze(t)
    # output pixel (x, y) -> painting coords before squeeze: p = C + Ai (p' - C), p' = view coords
    ca, sa = math.cos(TH), math.sin(TH)
    R = np.array([[ca, -sa], [sa, ca]]); Ai = R @ np.diag([1 / s, 1]) @ R.T
    sx, sy = w / W, h / H; ox, oy = cx - w / 2 - SKULL[0], cy - h / 2 - SKULL[1]
    a_, b_ = Ai[0, 0] * sx, Ai[0, 1] * sy; c_ = SKULL[0] + Ai[0, 0] * ox + Ai[0, 1] * oy
    d_, e_ = Ai[1, 0] * sx, Ai[1, 1] * sy; f_ = SKULL[1] + Ai[1, 0] * ox + Ai[1, 1] * oy
    return SRC.transform((W, H), Image.AFFINE, (a_, b_, c_, d_, e_, f_), Image.BICUBIC, fillcolor=(0, 0, 0, 0))

def to_screen(cam, x, y):
    cx, cy, w = cam; h = w / A
    return (x - (cx - w / 2)) / w * W, (y - (cy - h / 2)) / h * H

def view_hint(fr, t):
    """small label while the picture is tilted: 「斜め下から見ると…」"""
    a, b = 8.2, 11.6
    if not (a <= t < b): return
    k = min(eo((t - a) / 0.3), eo((b - t) / 0.3))
    put_block(fr, 'hint', ['↙ 左下から見ると'], f_sub, 76, 1560, k, 0, track=3, stroke=4)

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
    (0.10, 4.30, ['二人の男の間に、', '細長い骨の形が浮かんでいます。'], SUB_TOP),
    (4.50, 7.40, ['普通に見ると、', 'それが何か分かりません。'], SUB_TOP),
    (7.60, 11.60, ['でも画面を斜め下から見ると、', '形が変わります。'], SUB_TOP),
    (12.30, 16.10, ['床に伸びた白いものが、', '頭蓋骨に見えてくるのです。'], SUB_TOP),
    (16.95, 20.95, ['成功した二人のそばに、', '死の象徴が置かれています。'], 1380),
    (21.20, 24.95, ['人のそばに死があるとしたら、', '今をどう生きますか。'], 1380),
]

def subtitles(fr, t):
    for i, s in enumerate(SUBS):
        a, b, lines = s[:3]; y = s[3] if len(s) > 3 else SUB_Y
        if a <= t < b:
            k = min(eo((t - a) / 0.2), eo((b - t) / 0.18))
            put_block(fr, ('sub', i), lines, f_sub, 76, y, k, int(6 * (1 - k)))

def cover_text(fr, t):
    if t > 3.8: return
    k = eo((3.8 - t) / 0.3)
    l1, l2 = '斜めから見ると', 'ドクロになる絵？'
    white = (255, 255, 255, 255); red = RED + (255,)
    cols2 = [red if i <= 2 else white for i in range(len(l2))]
    put_block(fr, 'cover', [l1, l2], f_cover, 116, 560, k, 0, track=3, stroke=5, colors=[None, cols2])

def title_card(fr, t):
    a, b = 25.60, T_PROD
    if not (a <= t < b + XF): return
    k = min(eo((t - a) / 0.5), 1.0 if t < b else max(0.0, 1 - (t - b) / XF))
    put_block(fr, 'artist', ['ハンス・ホルバイン（子）'], f_artist, 60, 1330, k, int(8 * (1 - k)), track=4, stroke=3)
    put_block(fr, 'work', ['《大使たち》'], f_work, 120, 1400, k, int(8 * (1 - k)), track=6, stroke=4)
    put_block(fr, 'meta', ['1533｜ナショナル・ギャラリー（ロンドン）'], f_meta, 44, 1545, k * 0.95, 0, track=2, stroke=3)

def product_text(fr, t):
    kk = eo((t - T_PROD - 0.2) / 0.5)
    put_block(fr, 'copy', ['名画を着る、', '知ればもっと着たくなる。'], f_copy, 86, 1450, kk, int(10 * (1 - kk)), track=3, stroke=4)
    ku = eo((t - T_PROD - 0.9) / 0.5)
    put_block(fr, 'url', ['mirabilia.base.shop'], f_url, 50, 1650, ku, 0, track=1, stroke=3)

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
    cover_text(fr, t); view_hint(fr, t); subtitles(fr, t); title_card(fr, t)
    if t >= T_PROD: product_text(fr, t)
    return fr

def frame_at(t_out):
    return frame_at_orig(src_time(t_out))

SEGS = [(0.0, 7.0), (7.0, 14.0), (14.0, 21.0), (21.0, T_FIN_OUT)]

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
