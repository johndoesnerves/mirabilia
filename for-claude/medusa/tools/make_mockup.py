"""Medusa print (Muse's white-logo print data) on the black-tee blank, irises-mockup scale."""
from PIL import Image
import numpy as np
D = '/tmp/med/'
tee = Image.open('/tmp/iri/tee_blank.jpg').convert('RGB')
pr = Image.open(D + 'medusa-print-white-1400.png').convert('RGBA')
pr = pr.crop(pr.getchannel('A').getbbox())
W_P = 520; H_P = round(pr.height * W_P / pr.width)
pr = pr.resize((W_P, H_P), Image.LANCZOS)
x0 = 967 - W_P // 2; y0 = 320
lum = np.asarray(tee.convert('L')).astype(float)[y0:y0 + H_P, x0:x0 + W_P]
shade = np.clip(1 + (lum - lum.mean()) / 60.0, 0.85, 1.12)
a = np.asarray(pr).astype(float)
rgb = a[..., :3] * 0.93 * shade[..., None]; al = a[..., 3:] / 255
base = np.asarray(tee).astype(float)[y0:y0 + H_P, x0:x0 + W_P]
out = tee.copy(); out.paste(Image.fromarray(np.clip(rgb * al + base * (1 - al), 0, 255).astype(np.uint8)), (x0, y0))
out.save(D + 'medusa-blacktee-mockup.jpg', quality=94); out.resize((960, 640)).save(D + 'mock_small.jpg', quality=85)
print(x0, y0, W_P, H_P)
