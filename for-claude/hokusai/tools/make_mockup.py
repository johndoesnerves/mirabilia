"""Hokusai print on the black-tee blank (same placement scale as the irises mockup)."""
from PIL import Image, ImageFilter, ImageChops
import numpy as np
D = '/tmp/hok/'
tee = Image.open('/tmp/iri/tee_blank.jpg').convert('RGB')
src = Image.open(D + 'hokusai_great-wave.jpg').convert('RGB')
plate = src.crop((40, 40, src.width - 40, src.height - 40))
W_P = 514; H_P = round(plate.height * W_P / plate.width)
pr = plate.resize((W_P, H_P), Image.LANCZOS)
x0 = 967 - W_P // 2; y0 = 336
# fabric shading: tee luminance relative to its local mean around the chest
lum = np.asarray(tee.convert('L')).astype(float)
ref = lum[y0:y0 + H_P, x0:x0 + W_P].mean()
shade = np.clip(1 + (lum[y0:y0 + H_P, x0:x0 + W_P] - ref) / 60.0, 0.85, 1.12)
p = np.asarray(pr).astype(float) * 0.93 * shade[..., None]
# slight ink texture: soften very fine noise
out = tee.copy()
out.paste(Image.fromarray(np.clip(p, 0, 255).astype(np.uint8)), (x0, y0))
logo = Image.open('/tmp/iri/mirabilia-logo-white.png').convert('RGBA')
logo = logo.crop(logo.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox())
lw = 118; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
la = logo.getchannel('A').point(lambda v: int(v * 0.9)); logo.putalpha(la)
out.paste(logo, (x0 + W_P - lw, y0 + H_P + 26), logo)
out.save(D + 'hokusai-blacktee-mockup.jpg', quality=94)
out.resize((960, 640)).save(D + 'mock_small.jpg', quality=85)
print(x0, y0, W_P, H_P)
