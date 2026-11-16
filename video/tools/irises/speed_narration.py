"""Speed up a narration by SPEED without drift: each speech chunk (split at pauses) is time-stretched on its own
and placed at original_start / SPEED, so the voice stays locked to a timeline scaled by SPEED.
usage: python3 speed_narration.py in.mp3 out.wav [speed]"""
import sys, re, subprocess, os, tempfile
import numpy as np
from scipy.io import wavfile

src, dst = sys.argv[1], sys.argv[2]
SPEED = float(sys.argv[3]) if len(sys.argv) > 3 else 1.3
SR = 44100
log = subprocess.run(['ffmpeg', '-v', 'info', '-i', src, '-af', 'silencedetect=noise=-40dB:d=0.15', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', log)]
ends = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', log)]
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                           capture_output=True, text=True).stdout)
# speech chunks = complement of silences
sil = sorted(zip(starts, ends + [dur] * (len(starts) - len(ends))))
chunks, cur = [], 0.0
for s, e in sil:
    if s - cur > 0.03: chunks.append((cur, s))
    cur = max(cur, e)
if dur - cur > 0.03: chunks.append((cur, dur))
out = np.zeros(int((dur / SPEED + 1) * SR))
with tempfile.TemporaryDirectory() as td:
    for i, (s, e) in enumerate(chunks):
        a, b = max(0, s - 0.03), min(dur, e + 0.03)
        p = os.path.join(td, '%d.wav' % i)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.4f' % a, '-t', '%.4f' % (b - a), '-i', src,
                        '-af', 'atempo=%g' % SPEED, '-ac', '1', '-ar', str(SR), p], check=True)
        _, x = wavfile.read(p); x = x.astype(np.float64) / 32768
        n = len(x); fade = min(int(0.008 * SR), n // 2)
        if fade: x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
        i0 = int(a / SPEED * SR); out[i0:i0 + n] += x[:len(out) - i0]
out = out[:int(dur / SPEED * SR)]
wavfile.write(dst, SR, (np.clip(out, -1, 1) * 32767).astype(np.int16))
print('chunks', len(chunks), 'out', round(len(out) / SR, 3), 's')
