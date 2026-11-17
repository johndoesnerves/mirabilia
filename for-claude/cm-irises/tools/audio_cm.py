"""CM audio (15 s, no narration): one clear tone, soft cloth rustles, a minimal piano-like line, quiet ending."""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 44100; DUR = 15.0; N = int(SR * DUR); rng = np.random.default_rng(11)
M = np.zeros(N)
def add(sig, t, g):
    i = int(t * SR); j = min(N, i + len(sig)); M[i:j] += sig[:j - i] * g
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def piano(m, dur=2.2):
    t = np.arange(int(dur * SR)) / SR; f = hz(m)
    env = np.exp(-t * 2.2) * np.minimum(1, t / 0.006)
    return env * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 4) + 0.1 * np.sin(6 * np.pi * f * t) * np.exp(-t * 6))
def bell(f, dur=3.0):
    t = np.arange(int(dur * SR)) / SR
    return np.exp(-t * 1.4) * np.minimum(1, t / 0.003) * (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3))
def rustle(dur=0.5):
    n = int(dur * SR); x = sosfilt(butter(2, [1500, 7000], btype='band', fs=SR, output='sos'), rng.standard_normal(n))
    x *= np.sin(np.pi * np.arange(n) / n) ** 1.5 * (0.6 + 0.4 * rng.random(n)); return x / np.max(np.abs(x))
def pad(ms, dur):
    t = np.arange(int(dur * SR)) / SR; env = np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.2)
    return env * sum(np.sin(2 * np.pi * hz(m) * t) for m in ms) / len(ms)
add(bell(1568), 0.05, 0.22)                      # clear single tone
add(rustle(0.45), 1.45, 0.05)                   # the shirt appears
add(rustle(0.6), 4.5, 0.04); add(rustle(0.5), 6.6, 0.035)
beat = 60 / 84
mel = [76, 79, 81, 79, 76, 74, 76, 0, 72, 74, 76, 79, 76, 74, 72, 0]   # E G A G E D E - C D E G E D C -
bass = [(1.8, [52, 59]), (1.8 + 4 * beat, [48, 55]), (1.8 + 8 * beat, [50, 57]), (1.8 + 12 * beat, [45, 52])]
for i, m in enumerate(mel):
    t0 = 1.8 + i * beat
    if m and t0 < 11.0: add(piano(m), t0, 0.12 if t0 < 8.5 else 0.08)
for t0, ms in bass:
    if t0 < 11: add(pad(ms, 4 * beat + 1.0), t0, 0.07)
for k, m in enumerate([64, 67, 72]):            # quiet closing chord on the end card
    add(piano(m, 3.5), 11.2 + k * 0.12, 0.09)
add(pad([48, 55, 64], 3.6), 11.2, 0.06)
fade = np.clip((DUR - np.arange(N) / SR) / 1.2, 0, 1)
x = M * fade; x = x / np.max(np.abs(x)) * 0.8
wavfile.write('/tmp/cm/cm_audio.wav', SR, (np.stack([x, x], 1) * 32767).astype(np.int16))
print('ok')
