"""Hi-res (2x) mockup: irises print (white-logo data) on the black long-sleeve blank. Composite, not a photo."""
from PIL import Image
import numpy as np
D = '/tmp/cm/'
tee = Image.open(D + 'longtee-blank-black.jpg').convert('RGB')
tee = tee.resize((tee.width * 2, tee.height * 2), Image.LANCZOS)
pr = Image.open(D + 'irises-print-white-1400.png').convert('RGBA'); pr = pr.crop(pr.getchannel('A').getbbox())
W_P = 1040; H_P = round(pr.height * W_P / pr.width); pr = pr.resize((W_P, H_P), Image.LANCZOS)
x0 = 1928 - W_P // 2; y0 = 640
lum = np.asarray(tee.convert('L')).astype(float)[y0:y0 + H_P, x0:x0 + W_P]
shade = np.clip(1 + (lum - lum.mean()) / 60.0, 0.85, 1.12)
a = np.asarray(pr).astype(float); rgb = a[..., :3] * 0.93 * shade[..., None]; al = a[..., 3:] / 255
base = np.asarray(tee).astype(float)[y0:y0 + H_P, x0:x0 + W_P]
out = tee.copy(); out.paste(Image.fromarray(np.clip(rgb * al + base * (1 - al), 0, 255).astype(np.uint8)), (x0, y0))
out.save(D + 'irises-longtee-mockup-2x.jpg', quality=93)
out.resize((960, 640)).save(D + 'lt_mock_small.jpg', quality=85)
print(x0, y0, W_P, H_P)
