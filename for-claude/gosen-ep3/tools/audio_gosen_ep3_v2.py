"""Gosen ep3 audio (1.3x main part): narration + calm BGM (+ light SFX), written as mix / narration / bed stems."""
import numpy as np, subprocess
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100; DUR = 50.431; N = int(SR * DUR)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', '/tmp/gep3/narr2_x13.wav', '-ac', '1', '-ar', str(SR),
                      '-f', 's16le', '-'], capture_output=True).stdout
voice = np.frombuffer(raw, np.int16).astype(np.float64) / 32768
v = np.zeros(N); v[:min(N, len(voice))] = voice[:N]
v = v / np.max(np.abs(v)) * 0.85

M = np.zeros(N); rng = np.random.default_rng(5)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, t, g):
    i = int(t * SR); j = min(N, i + len(sig)); M[i:j] += sig[:j - i] * g
def tone(m, dur=2.4):
    t = np.arange(int(dur * SR)) / SR; f = hz(m)
    env = np.exp(-t * 1.6) * np.minimum(1, t / 0.012)
    return env * (np.sin(2 * np.pi * f * t) + 0.12 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3))
def pad(ms, dur):
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
    return env * sum(np.sin(2 * np.pi * hz(m) * t) + 0.25 * np.sin(2 * np.pi * hz(m) * 1.003 * t) for m in ms) / len(ms)

beat = 0.833; bar = 4 * beat   # 72 bpm
chords = [[50, 54, 57, 61], [47, 50, 54, 57], [43, 47, 50, 54], [45, 49, 52, 57]]  # Dmaj7 Bm7 Gmaj7 A
t0 = 0.0; b = 0
while t0 < DUR - 0.5:
    c = chords[b % 4]
    add(pad([m - 12 for m in c[:3]], bar + 1.2), t0, 0.11)
    for k, idx in enumerate([0, 2, 1, 3]):
        tt = t0 + k * beat
        if tt < DUR - 0.5: add(tone(c[idx] + 12), tt, 0.11 if k else 0.14)
    t0 += bar; b += 1

def whoosh(dur=0.6):
    n = int(dur * SR); x = sosfilt(butter(2, [500, 3500], btype='band', fs=SR, output='sos'), rng.standard_normal(n))
    e = np.sin(np.pi * np.arange(n) / n) ** 2; x = x * e; return x / np.max(np.abs(x))
def chime(f=1319, dur=1.6):
    t = np.arange(int(dur * SR)) / SR
    return np.exp(-t * 3) * np.minimum(1, t / 0.004) * (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t * 3))
def tick(f):
    t = np.arange(int(0.08 * SR)) / SR; return np.exp(-t * 60) * np.sin(2 * np.pi * f * t)

S = np.zeros(N)
def sfx(sig, t, g):
    i = int(t * SR); j = min(N, i + len(sig)); S[i:j] += sig[:j - i] * g
for tc in [10.5, 21.9, 33.8, 44.95, 57.95]: sfx(whoosh(), tc / 1.3 - 0.3, 0.05)   # work changes
for tc in [0.6, 11.3, 22.7, 34.6, 45.7]: sfx(whoosh(0.9), tc / 1.3, 0.035)   # arrow grows
for tc in [2.55, 13.25, 24.45, 36.3, 47.45]: sfx(chime(1319), tc / 1.3, 0.08)   # answer   # shot changes + product
sfx(chime(1047), 45.40 / 1.3, 0.07)     # title card
TE = 61.40 / 1.3
for k, f in enumerate([880, 988, 1175, 1319]): sfx(tick(f), TE + 0.25 * k, 0.10)   # end-card steps
# ducking under the voice
env = np.convolve(np.abs(v), np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same')
active = np.convolve((env > 0.02).astype(float), np.ones(int(0.3 * SR)) / int(0.3 * SR), 'same')
gain = 0.55 - 0.30 * np.clip(active * 2, 0, 1)
t = np.arange(N) / SR
# climax: one step down on 'once more, to Fuji'
climax = 0 * t
gain *= 1 - 0.55 * climax
fade = np.clip((DUR - t) / 1.5, 0, 1) * np.clip(t / 0.05, 0, 1)
bed = M * gain * 0.6 * fade + S
mix = v + bed
norm = 0.89 / np.max(np.abs(mix))
for name, sig in [('stem_mix', mix), ('stem_narration', v), ('stem_bed', bed)]:
    x = sig * norm
    wavfile.write('/tmp/gep3/v2_%s.wav' % name, SR, (np.stack([x, x], 1) * 32767).astype(np.int16))
print('ok', DUR, 'peaks', [round(float(np.max(np.abs(z * norm))), 3) for z in (mix, v, bed)])
