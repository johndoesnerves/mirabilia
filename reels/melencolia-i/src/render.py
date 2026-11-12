import sys, math, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H, FPS = 1080, 1920, 30
VX, VY, VW, VH = 60, 430, 960, 940
FD = '/usr/share/fonts/opentype/noto/'
def F(name, size): return ImageFont.truetype(FD + name + '.ttc', size, index=0)
SERIF_B = lambda s: F('NotoSerifCJK-Bold', s)
SERIF_SB = lambda s: F('NotoSerifCJK-SemiBold', s)
SANS_M = lambda s: F('NotoSansCJK-Medium', s)
SANS_B = lambda s: F('NotoSansCJK-Bold', s)

P = 1600
art0 = Image.open(os.path.join(ASSETS, 'melencolia.jpg')).convert('RGB')
AW, AH = art0.size
art = Image.new('RGB', (AW + 2 * P, AH + 2 * P), 'white'); art.paste(art0, (P, P))
tee0 = Image.open(os.path.join(ASSETS, 'tee-black.jpg')).convert('RGB')
TW, TH = tee0.size
tee = Image.new('RGB', (TW + 2 * P, TH + 2 * P), 'white'); tee.paste(tee0, (P, P))

ZF = VH / AH
FULL = (AW / 2, AH / 2, ZF)
HOOKZ = (900, 1150, ZF * 1.1)
FACE = (1420, 1000, 1.6)
CROWN = (1490, 880, 1.25)
SQ = (1712, 542, 2.0)
BAT0 = (262, 440, 2.0)
BAT1 = (352, 455, 2.0)
IPOS = (445, 440, 2.2)

C_FACE = (1405, 1005, 80, 100)
C_CROWN = (1495, 865, 215, 115)
C_SQ = (1712, 542, 205, 205)
C_BAT = (250, 398, 72, 62)
C_I = (442, 433, 34, 44)

def ease(p):
    p = min(max(p, 0), 1); return p * p * (3 - 2 * p)
def lerp(a, b, p): return a + (b - a) * p
def cam_lerp(c1, c2, p):
    p = ease(p)
    z = math.exp(lerp(math.log(c1[2]), math.log(c2[2]), p))
    return (lerp(c1[0], c2[0], p), lerp(c1[1], c2[1], p), z)
def seg(t, a, b): return (t - a) / (b - a)

def camera(t):
    if t < 2.5: return FULL
    if t < 3.5: return cam_lerp(FULL, HOOKZ, seg(t, 2.5, 3.5))
    if t < 7.5:
        c = cam_lerp(HOOKZ, FACE, seg(t, 3.5, 4.1))
        return (c[0], c[1], c[2] * (1 + 0.04 * max(0, seg(t, 4.1, 7.5))))
    if t < 11.7: return cam_lerp((FACE[0], FACE[1], FACE[2] * 1.04), CROWN, seg(t, 7.5, 8.3))
    if t < 17.3: return cam_lerp(CROWN, SQ, seg(t, 11.7, 12.3))
    if t < 21.6:
        if t < 19.1: return cam_lerp(SQ, BAT0, seg(t, 17.3, 18.0))
        return cam_lerp(BAT0, BAT1, seg(t, 19.1, 21.1))
    if t < 27.0:
        if t < 24.2: return cam_lerp(BAT1, IPOS, seg(t, 21.6, 22.1))
        return cam_lerp(IPOS, FULL, seg(t, 24.2, 24.9))
    return None

def to_screen(c, x, y):
    cx, cy, z = c
    return (VW / 2 + (x - cx) * z, VH / 2 + (y - cy) * z)

def view(src, c, pad=P):
    cx, cy, z = c
    w, h = VW / z, VH / z
    box = (cx - w / 2 + pad, cy - h / 2 + pad, cx + w / 2 + pad, cy + h / 2 + pad)
    return src.resize((VW, VH), Image.BICUBIC, box=box)

# ---------- text helpers ----------
def text_block(lines, font, fill=(0, 0, 0), lh=1.3, maxw=980):
    size = font.size
    while True:
        ws = [font.getlength(l) for l in lines]
        if max(ws) <= maxw or size < 30: break
        size -= 2; font = ImageFont.truetype(font.path, size, index=0);
    lhp = int(size * lh)
    im = Image.new('RGBA', (W, lhp * len(lines) + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        d.text(((W - font.getlength(l)) / 2, i * lhp), l, font=font, fill=fill)
    return im

def pill(text):
    f = SANS_B(34)
    tw = f.getlength(text)
    pw, ph = int(tw + 56), 64
    im = Image.new('RGBA', (W, ph + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0 = (W - pw) // 2
    d.rounded_rectangle((x0, 0, x0 + pw, ph), radius=32, outline=(0, 0, 0), width=3, fill=(255, 255, 255))
    d.text((x0 + 28, 9), text, font=f, fill=(0, 0, 0))
    return im

def paste_fade(base, layer, xy, a):
    if a <= 0: return
    if a < 1:
        layer = layer.copy(); al = layer.getchannel('A').point(lambda v: int(v * a)); layer.putalpha(al)
    base.alpha_composite(layer, (int(xy[0]), int(xy[1])))

HL_Y, SUB_Y, LAB_Y = 196, 1405, 104
SHOW_REAL_SIZE_FRAME = False  # v3で廃止（サイズ表記なし）
SCENES = [
    (0.0, 3.5, 'デューラー｜1514年', ['絵の題名が', '「鬱よ、去れ」！？'], [(0.0, ['憂鬱を描いた絵なのに、', 'なぜ「去れ」？'])]),
    (3.5, 7.5, 'サイン 1 / 5', ['顔だけ、', '影で真っ暗'], [(3.5, ['暗い顔は、当時の', '「憂鬱な人」のお約束'])]),
    (7.5, 11.7, 'サイン 2 / 5', ['頭には、', '水辺の草の冠'], [(7.5, ['乾いた憂鬱をうるおす薬草、', 'という読み方があるんです'])]),
    (11.7, 17.3, 'サイン 3 / 5', ['壁には、', '魔方陣のお守り'], [(11.7, ['どこを足しても34の表。', '昔は星のお守りでした']), (14.5, ['憂鬱をしずめるお守り、', 'という説もあるんです'])]),
    (17.3, 21.6, 'サイン 4 / 5', ['題名を運ぶのは、', 'コウモリ'], [(17.3, ['憂鬱の星・土星の生き物とされた', 'コウモリが、題名を掲げてる'])]),
    (21.6, 27.0, 'サイン 5 / 5', ['そして、', '最後の「I」'], [(21.6, ['別の読み方では、この「I」は', 'ラテン語の「行け」']), (24.2, ['つまり「憂鬱よ、去れ」。', 'そう読む説があるんです'])]),
    (27.0, 29.5, None, ['この傑作を、', '時代を越え、現代の装いに。'], []),
]
LAYERS = []
for s in SCENES:
    lab = pill(s[2]) if s[2] else None
    hl = text_block(s[3], SERIF_B(84), lh=1.22, maxw=1000)
    subs = [(st, text_block(ls, SANS_M(48), lh=1.45, maxw=1000)) for st, ls in s[4]]
    LAYERS.append((lab, hl, subs))

def tag(text, font):
    tw = font.getlength(text); a, dsc = font.getmetrics()
    im = Image.new('RGBA', (int(tw + 48), a + dsc + 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), radius=14, fill=(255, 255, 255, 240), outline=(0, 0, 0), width=3)
    d.text((24, 10), text, font=font, fill=(0, 0, 0))
    return im
TAG_REAL = tag('実物 24×19cm', SANS_M(30))
TAG_34 = tag('＝34', SERIF_B(60))
TAG_I = tag('i ＝ 行け', SERIF_B(56))

# ---------- overlay (2x supersampled) ----------
SS = 2
def overlay_draw(c, items):
    """items: list of ('ell', (x,y,rx,ry), prog, alpha) or ('line', (x1,y1,x2,y2), prog, alpha) in image coords"""
    ov = Image.new('RGBA', (VW * SS, VH * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for kind, g, prog, a in items:
        if prog <= 0 or a <= 0: continue
        A = int(255 * a)
        if kind == 'ell':
            x, y, rx, ry = g
            sx, sy = to_screen(c, x, y); z = c[2]
            rxs, rys = max(rx * z, 22), max(ry * z, 22)
            bb = [(sx - rxs) * SS, (sy - rys) * SS, (sx + rxs) * SS, (sy + rys) * SS]
            end = -90 + 360 * min(prog, 1)
            d.arc(bb, -90, end, fill=(0, 0, 0, int(A * 0.45)), width=14 * SS)
            d.arc(bb, -90, end, fill=(255, 255, 255, A), width=7 * SS)
        else:
            x1, y1, x2, y2 = g
            p = min(prog, 1)
            a1 = to_screen(c, x1, y1); a2 = to_screen(c, lerp(x1, x2, p), lerp(y1, y2, p))
            pts = [(a1[0] * SS, a1[1] * SS), (a2[0] * SS, a2[1] * SS)]
            d.line(pts, fill=(0, 0, 0, int(A * 0.4)), width=10 * SS)
            d.line(pts, fill=(255, 255, 255, A), width=5 * SS)
    return ov.resize((VW, VH), Image.LANCZOS)

SQ_LINES = []
xs = [1572, 1642, 1712, 1782, 1852]; ys = [400, 471, 542, 614, 685]
for i in range(4):
    yc = (ys[i] + ys[i + 1]) / 2; SQ_LINES.append((xs[0] + 8, yc, xs[4] - 8, yc))
for i in range(4):
    xc = (xs[i] + xs[i + 1]) / 2; SQ_LINES.append((xc, ys[0] + 8, xc, ys[4] - 8))
SQ_LINES.append((xs[0] + 8, ys[0] + 8, xs[4] - 8, ys[4] - 8))
SQ_LINES.append((xs[4] - 8, ys[0] + 8, xs[0] + 8, ys[4] - 8))

def fade_a(t, t0, t1, fin=0.12, fout=0.15):
    if t < t0 or t > t1: return 0
    return min(1, (t - t0) / fin, (t1 - t) / fout)

def overlays(t):
    it = []
    if 3.5 <= t < 7.5: it.append(('ell', C_FACE, seg(t, 4.2, 4.55), fade_a(t, 4.2, 7.5, 0.01)))
    if 7.5 <= t < 11.7: it.append(('ell', C_CROWN, seg(t, 8.35, 8.7), fade_a(t, 8.35, 11.7, 0.01)))
    if 11.7 <= t < 17.3:
        for i, L in enumerate(SQ_LINES):
            st = 12.45 + i * 0.075
            it.append(('line', L, seg(t, st, st + 0.15), fade_a(t, st, st + 0.42, 0.01, 0.2)))
        it.append(('ell', C_SQ, seg(t, 14.6, 14.95), fade_a(t, 14.6, 17.3, 0.01)))
    if 17.3 <= t < 21.6: it.append(('ell', C_BAT, seg(t, 18.1, 18.45), fade_a(t, 18.1, 19.15, 0.01, 0.25)))
    if 21.6 <= t < 27.0:
        it.append(('ell', C_I, seg(t, 22.2, 22.5), fade_a(t, 22.2, 24.3, 0.01, 0.2)))
        for k, C in enumerate([C_CROWN, C_SQ, C_BAT]):
            st = 25.0 + 0.3 * k
            it.append(('ell', C, 1.0, fade_a(t, st, st + 0.45, 0.08, 0.15)))
    return it

def compose_view(t):
    c = camera(t)
    if c is not None:
        v = view(art, c)
        if 3.5 <= t < 8.0:
            k = ease(seg(t, 4.0, 4.6)) * (1 - ease(seg(t, 7.5, 8.0)))
            if k > 0:
                v = ImageEnhance.Contrast(v).enhance(1 + 0.22 * k)
                v = ImageEnhance.Brightness(v).enhance(1 - 0.05 * k)
        v = v.convert('RGBA')
        its = overlays(t)
        if its: v.alpha_composite(overlay_draw(c, its))
        if 11.7 <= t < 17.3:
            a = fade_a(t, 13.25, 14.3, 0.1, 0.15)
            sx, sy = to_screen(c, 1852, 542)
            paste_fade(v, TAG_34, (sx + 22, sy - TAG_34.size[1] / 2), a)
        if 21.6 <= t < 24.4:
            a = fade_a(t, 22.5, 24.35, 0.15, 0.15)
            sx, sy = to_screen(c, C_I[0], C_I[1])
            paste_fade(v, TAG_I, (sx - TAG_I.size[0] / 2, sy + 110), a)
        return v, c
    # product
    tc = cam_lerp((TW / 2, TH / 2, 0.5), (TW / 2, 600, 0.62), seg(t, 27.0, 29.5))
    return view(tee, tc).convert('RGBA'), None

def end_card(t):
    im = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    d0 = []
    # MIRABILIA letterspaced
    f = SERIF_B(112); sp = 14
    txt = 'MIRABILIA'
    tw = sum(f.getlength(ch) for ch in txt) + sp * (len(txt) - 1)
    l1 = Image.new('RGBA', (W, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(l1); x = (W - tw) / 2
    for ch in txt: d.text((x, 0), ch, font=f, fill=(0, 0, 0)); x += f.getlength(ch) + sp
    l2 = text_block(['失われた記憶を身にまとう。'], SERIF_SB(54))
    f3 = SANS_M(44); t3 = '各図案×仕様は10着限り'; w3 = f3.getlength(t3)
    l3 = Image.new('RGBA', (W, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(l3)
    x0 = (W - w3) / 2 - 34; d.rectangle((x0, 4, x0 + w3 + 68, 96), outline=(0, 0, 0), width=3)
    d.text(((W - w3) / 2, 18), t3, font=f3, fill=(0, 0, 0))
    f4 = SANS_B(54); t4 = '購入はプロフィールから'; w4 = f4.getlength(t4)
    l4 = Image.new('RGBA', (W, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(l4)
    d.text(((W - w4) / 2, 0), t4, font=f4, fill=(0, 0, 0))
    d.rectangle(((W - w4) / 2, 86, (W + w4) / 2, 91), fill=(0, 0, 0))
    for layer, st, y in [(l1, 29.5, 690), (l2, 29.9, 880), (l3, 30.3, 1010), (l4, 30.7, 1160)]:
        p = ease(seg(t, st, st + 0.25))
        if p > 0: paste_fade(im, layer, (0, y + 18 * (1 - p)), p)
    return im

END_CACHE = {}
def frame(t):
    if t >= 29.5: return end_card(t).convert('RGB')
    im = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    si = max(i for i, s in enumerate(SCENES) if s[0] <= t + 1e-9)
    s = SCENES[si]; lab, hl, subs = LAYERS[si]
    v, c = compose_view(t)
    im.alpha_composite(v, (VX, VY))
    # real-size frame in hook
    if SHOW_REAL_SIZE_FRAME and si == 0 and t >= 0.8:
        cc = camera(t)
        x0, y0 = to_screen(cc, 0, 0); x1, y1 = to_screen(cc, AW, AH)
        p = ease(seg(t, 0.8, 1.6))
        mx, my = lerp(VW / 2, (x0 + x1) / 2, p), lerp(VH / 2, (y0 + y1) / 2, p)
        hw, hh = lerp(VW / 2 - 4, (x1 - x0) / 2 + 10, p), lerp(VH / 2 - 4, (y1 - y0) / 2 + 10, p)
        a = min(1, seg(t, 0.8, 1.0))
        fr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fr)
        d.rectangle((VX + mx - hw, VY + my - hh, VX + mx + hw, VY + my + hh), outline=(0, 0, 0, int(255 * a)), width=4)
        im.alpha_composite(fr)
        ta = fade_a(t, 1.5, 9, 0.2)
        paste_fade(im, TAG_REAL, (VX + mx + hw - TAG_REAL.size[0] - 14, VY + my + hh - TAG_REAL.size[1] - 14), ta)
    lt = t - s[0]
    pa = ease(lt / 0.3)
    if lab: paste_fade(im, lab, (0, LAB_Y), 1)
    paste_fade(im, hl, (0, HL_Y + 18 * (1 - pa)), pa)
    for j, (st, sl) in enumerate(subs):
        en = subs[j + 1][0] if j + 1 < len(subs) else s[1]
        a = min(1, (t - (st + 0.15)) / 0.25) if t >= st + 0.15 else 0
        if j + 1 < len(subs) and t > en - 0.12: a = 0
        if st <= t < en: paste_fade(im, sl, (0, SUB_Y + 10 * (1 - min(a, 1))), a)
    return im.convert('RGB')

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for ts in sys.argv[2:]:
            frame(float(ts)).save('still_%s.jpg' % ts, quality=88)
    else:
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        tmp = out[:-4] + '.part.mp4'
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
        for n in range(a, b):
            p.stdin.write(frame(n / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.rename(tmp, out)
        else: sys.exit(1)
