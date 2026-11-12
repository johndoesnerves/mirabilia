import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
SR = 48000; DUR = 33.5
N = int(SR * DUR)
rng = np.random.default_rng(7)
mus = np.zeros(N); sfx = np.zeros(N)

def add(buf, t0, sig, g=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig))
    if i < N: buf[i:j] += sig[:j - i] * g
def tt(d): return np.arange(int(d * SR)) / SR
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)

def piano(f, d=2.2):
    t = tt(d)
    s = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (2.2 + k * 1.3)) for k, a in [(1, 1), (2, .45), (3, .2), (4, .1)])
    return s * np.minimum(1, t / 0.006)
def bell(f, d, partials=((1, 1), (2.0, .5), (2.76, .35), (5.4, .15), (0.5, .3))):
    t = tt(d)
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * (1.0 + r * 0.9) * 3 / d) for r, a in partials)
    return s * np.minimum(1, t / 0.003)

# ---- music: gentle arpeggios, 84 bpm ----
beat = 60 / 84; bar = beat * 4
prog = [(57, [57, 64, 69, 72]), (53, [53, 60, 65, 69]), (48, [55, 60, 64, 67]), (55, [55, 62, 67, 71])]  # Am F C G
t0 = 0.0; k = 0
while t0 < 31.5:
    root, ch = prog[k % 4]
    pat = [ch[0], ch[1], ch[2], ch[3], ch[2], ch[1], ch[2], ch[3]]
    for e, m in enumerate(pat):
        add(mus, t0 + e * beat / 2, piano(midi(m + 12)), 0.10 if e % 2 == 0 else 0.07)
    add(mus, t0, piano(midi(root - 12), 3.2), 0.16)
    # soft pad
    t = tt(bar + 0.3)
    pad = sum(np.sin(2 * np.pi * midi(m) * t) for m in ch[:3]) * np.sin(np.pi * np.minimum(t / (bar + 0.3), 1)) ** 2
    add(mus, t0, pad, 0.018)
    t0 += bar; k += 1
tm = np.arange(N) / SR
env = np.clip(tm / 0.6, 0, 1) * np.clip((32.3 - tm) / 1.3, 0, 1)
mus *= env

# ---- sfx ----
add(sfx, 0.0, bell(98, 4.0), 0.55)                         # low bell
def swoosh(d=0.35):
    n = rng.standard_normal(int(d * SR)); t = tt(d)
    out = np.zeros_like(n); segs = 6
    for s in range(segs):
        a, b = s * len(n) // segs, (s + 1) * len(n) // segs
        f = 600 + 3000 * s / segs
        out[a:b] = bp(n, f, f * 1.8)[a:b]
    return out * np.sin(np.pi * t / d) ** 2
add(sfx, 4.2, swoosh(), 0.35)
t = tt(4.0); drone = (np.sin(2 * np.pi * 110 * t) + .5 * np.sin(2 * np.pi * 165 * t)) * np.sin(np.pi * t / 4.0) ** 2
add(sfx, 3.5, drone, 0.05)
def drop(f0=1400, f1=700, d=0.18):
    t = tt(d); f = f0 + (f1 - f0) * (t / d) ** 0.5
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 22)
add(sfx, 8.35, drop(), 0.3); add(sfx, 8.65, drop(1700, 900, 0.14), 0.18)
def tick(f=2600, d=0.05):
    t = tt(d); return np.sin(2 * np.pi * f * t) * np.exp(-t * 90)
for i in range(10): add(sfx, 12.45 + i * 0.075, tick(2200 + 60 * i), 0.22)
add(sfx, 14.6, bell(1568, 1.6, ((1, 1), (2.0, .3), (3.0, .12))), 0.22)
def flap(d=0.12):
    n = lp(rng.standard_normal(int(d * SR)), 700); t = tt(d)
    return n * np.sin(np.pi * t / d) ** 2
for i in range(8): add(sfx, 18.05 + i * 0.16, flap(), 0.5 * (1 - i / 10))
add(sfx, 22.2, tick(3200, 0.03), 0.4); add(sfx, 22.23, lp(rng.standard_normal(1200), 4000) * np.exp(-tt(0.025) * 200), 0.25)
add(sfx, 24.2, bell(392, 3.0), 0.28)
for i, f in enumerate([1047, 1175, 1319]): add(sfx, 25.0 + 0.3 * i, bell(f * 2, 0.6, ((1, 1), (2.0, .2))), 0.07)
t = tt(1.0); rust = bp(rng.standard_normal(len(t)), 1500, 6000) * (np.sin(np.pi * t) ** 1.5) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t))
add(sfx, 27.0, rust, 0.12)
for i, f in enumerate([1568, 1760, 1976, 2349]): add(sfx, 29.5 + 0.4 * i, bell(f, 1.2, ((1, 1), (2.0, .25), (3.0, .1))), 0.16)

mix = mus + sfx
# tiny stereo widening on music
L = mix + 0.0; R = np.concatenate([np.zeros(240), mus[:-240]]) + sfx
st = np.stack([L, R], 1)
st /= np.max(np.abs(st)) / 0.89
st[int(32.6 * SR):] = 0
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok', st.shape)
