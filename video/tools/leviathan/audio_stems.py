import numpy as np, subprocess
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100; DUR = 51.3; N = int(SR * DUR)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', '/tmp/lev/leviathan-narration-final.mp3', '-ac', '1', '-ar', str(SR),
                      '-f', 's16le', '-'], capture_output=True).stdout
voice = np.frombuffer(raw, np.int16).astype(np.float64) / 32768
v = np.zeros(N); v[:min(N, len(voice))] = voice[:N]
v = v / np.max(np.abs(v)) * 0.85

M = np.zeros(N); rng = np.random.default_rng(3)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, t, g):
    i = int(t * SR); j = min(N, i + len(sig)); M[i:j] += sig[:j - i] * g
def pluck(m, dur=1.4):
    t = np.arange(int(dur * SR)) / SR; f = hz(m)
    return np.exp(-t * 2.8) * np.minimum(1, t / 0.005) * (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t) * np.exp(-t * 5))
def pad(ms, dur):
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.8)
    return env * sum(np.sin(2 * np.pi * hz(m) * t) + 0.3 * np.sin(2 * np.pi * hz(m) * 1.004 * t) for m in ms) / len(ms)

beat = 0.75; bar = 4 * beat
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G (light, story-like)
t0 = 0; b = 0
while t0 < DUR - 0.5:
    c = chords[b % 4]
    add(pad([m - 12 for m in c], bar + 0.8), t0, 0.12)
    for k, idx in enumerate([0, 1, 2, 1, 0, 2, 1, 2]):
        tt = t0 + k * beat / 2
        if tt < DUR - 0.3: add(pluck(c[idx] + 12), tt, 0.10 if k % 2 else 0.13)
    t0 += bar; b += 1

def whoosh(dur=0.45):
    n = int(dur * SR); x = sosfilt(butter(2, [700, 4500], btype='band', fs=SR, output='sos'), rng.standard_normal(n))
    e = np.sin(np.pi * np.arange(n) / n) ** 2; x = x * e; return x / np.max(np.abs(x))
def ding(f=1568, dur=0.9):
    t = np.arange(int(dur * SR)) / SR
    return np.exp(-t * 5) * np.minimum(1, t / 0.003) * (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t * 4))
def tick(f):
    t = np.arange(int(0.08 * SR)) / SR; return np.exp(-t * 60) * np.sin(2 * np.pi * f * t)

S = np.zeros(N)
def sfx(sig, t, g):
    i = int(t * SR); j = min(N, i + len(sig)); S[i:j] += sig[:j - i] * g
for tc in [4.13, 12.58, 19.89, 27.42, 32.34, 38.47, 44.30, 47.30]: sfx(whoosh(), tc - 0.2, 0.06)
for tc in [4.73, 13.68, 28.52]: sfx(ding(), tc, 0.07)
sfx(ding(1319, 1.2), 44.4, 0.10)
for tc, f in zip([47.3, 47.65, 48.0, 48.35, 48.7], [880, 988, 1175, 1319, 1568]): sfx(tick(f), tc, 0.12)

# duck music under voice
env = np.convolve(np.abs(v), np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same')
active = (env > 0.02).astype(float)
k = int(0.25 * SR); active = np.convolve(active, np.ones(k) / k, 'same')
gain = 0.55 - 0.30 * np.clip(active * 2, 0, 1)
t = np.arange(N) / SR
fade = np.clip((DUR - t) / 1.5, 0, 1) * np.clip(t / 0.05, 0, 1)
bed = M * gain * 0.6 * fade + S
mix = v + bed
norm = 0.89 / np.max(np.abs(mix))
for name, sig in [('stem_mix', mix), ('stem_narration', v), ('stem_bed', bed)]:
    x = sig * norm
    wavfile.write('/tmp/lev/%s.wav' % name, SR, (np.stack([x, x], 1) * 32767).astype(np.int16))
print('peaks', [round(float(np.max(np.abs(z * norm))), 3) for z in (mix, v, bed)])
print('ok', N / SR)
