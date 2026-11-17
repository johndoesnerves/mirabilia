"""Thumbnail (cover) image: opening shot of the painting + big video title, kept inside the 3:4 profile-grid crop.
usage: python3 make_thumb.py pandora|irises|goya|hokusai|medusa|saturn|caravaggio|bosch|bosch"""
import sys, importlib.util
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

name = sys.argv[1]
cfg = {
    'pandora': dict(script='/tmp/pan/render_pandora.py', t=0.0, cam=(1000, 1850, 1560),
                    lines=['この花園、', '災いが始まる', '直前！？'], accent=('災い', (0xE3, 0x4B, 0x3F)),
                    sub='ルドン《パンドラ》', out='/tmp/posts/MIRABILIA_pandora_reel_v3_thumbnail.png'),
    'irises': dict(script='/tmp/iri/render_irises.py', t=0.0,
                   lines=['この青い花、', 'もとは紫', 'だった！？'], accent=('紫', (176, 132, 236)),
                   sub='ゴッホ《アイリス》', out='/tmp/posts/MIRABILIA_irises_reel_v2_thumbnail.png'),
    'goya': dict(script='/tmp/goya/render_goya.py', t=0.0,
                 lines=['眠ると', '怪物が', '生まれる！？'], accent=('怪物', (0xE3, 0x4B, 0x3F)),
                 sub='ゴヤ《理性の眠りは怪物を生む》', out='/tmp/posts/MIRABILIA_goya_reel_v1_thumbnail.png'),
    'hokusai': dict(script='/tmp/hok/render_hokusai.py', t=0.0, cam=(2100, 1290, 1200),
                    lines=['この富士山、', '大波より', '小さい！？'], accent=('小さい', (0xE3, 0x4B, 0x3F)),
                    sub='北斎《神奈川沖浪裏》', out='/tmp/posts/MIRABILIA_hokusai_reel_v1_thumbnail.png'),
    'medusa': dict(script='/tmp/med/render_medusa.py', t=0.0, cam=(1800, 819, 921),
                   lines=['この', '小さな船に、', '気づける？'], accent=('小さな船', (0xE3, 0x4B, 0x3F)), top=960, ring=(1952, 655),
                   sub='ジェリコー《メデューズ号の筏》', out='/tmp/posts/MIRABILIA_medusa_reel_v1_thumbnail.png'),
    'saturn': dict(script='/tmp/sat/render_saturn.py', t=0.0, cam=(560, 862, 900), top=780,
                   lines=['食べている', '男の目が、', '怖い理由'], accent=('目', (0xE3, 0x4B, 0x3F)),
                   sub='ゴヤ《我が子を食らうサトゥルヌス》', out='/tmp/posts/MIRABILIA_saturn_reel_v1_thumbnail.png'),
    'caravaggio': dict(script='/tmp/car/render_caravaggio.py', t=0.0, cam=(820, 866, 974), top=720, sub_size=44,
                   lines=['勝った少年が', '笑って', 'いない？'], accent=('笑って', (0xE3, 0x4B, 0x3F)),
                   sub='カラヴァッジョ《ゴリアテの頭を持つダヴィデ》', out='/tmp/posts/MIRABILIA_caravaggio_reel_v1_thumbnail.png'),
    'bosch': dict(script='/tmp/bos2/render_bosch.py', t=0.0, cam=(330, 1100, 680), top=320,
                  lines=['地獄の楽器が、', '人を苦しめる', '理由は？'], accent=('苦しめる', (0xE3, 0x4B, 0x3F)),
                  sub='ボス《快楽の園》', out='/tmp/posts/MIRABILIA_bosch_reel_v2_thumbnail.png'),
    'kuniyoshi': dict(script='/tmp/kun/render_kuniyoshi.py', t=0.0, cam=(870, 497, 559), top=950,
                  lines=['この骸骨、', '味方かも', 'しれない？'], accent=('味方', (0xE3, 0x4B, 0x3F)),
                  sub='国芳《相馬の古内裏》', out='/tmp/posts/MIRABILIA_kuniyoshi_reel_v1_thumbnail.png'),
    'holbein': dict(script='/tmp/hol/render_holbein.py', t=0.0, cam=(760, 960, 886), top=300,
                  lines=['斜めから', '見るとドクロ', 'になる絵？'], accent=('ドクロ', (0xE3, 0x4B, 0x3F)),
                  sub='ホルバイン《大使たち》', out='/tmp/posts/MIRABILIA_holbein_reel_v1_thumbnail.png'),
    'gosen-shisen': dict(script='/tmp/gos/render_gosen.py', t=0.0, cam=(714, 1530, 760), top=330, painting='sistine-madonna',
                  lines=['視線の先には', '何がある？'], accent=('視線', (0xE3, 0x4B, 0x3F)),
                  sub='名画の視線を追う五選', out='/tmp/posts/MIRABILIA_gosen-shisen_v1_thumbnail.png'),
    'gosen-shisen-v2': dict(script='/tmp/gos/render_gosen_v2.py', t=0.0, cam=(1060, 477, 537), top=980, painting='painting-medusa', ring=(1139, 382),
                  lines=['視線の先には', '何がある？'], accent=('視線', (0xE3, 0x4B, 0x3F)),
                  sub='名画の視線を追う五選', out='/tmp/posts/MIRABILIA_gosen-shisen_reel_v2_thumbnail.png'),
}[name]
spec = importlib.util.spec_from_file_location('R', cfg['script']); R = importlib.util.module_from_spec(spec)
sys.argv = ['x', 'none']; spec.loader.exec_module(R)
W, H = R.W, R.H

if 'painting' in cfg:
    _p = R.P[cfg['painting']]; fr = _p['bg'].copy(); fr.alpha_composite(R.view(_p['src'], cfg['cam'], off=False))
else:
    fr = R.BG.copy(); fr.alpha_composite(R.view(R.SRC, cfg['cam']) if 'cam' in cfg else R.painting(cfg['t']))
if 'ring' in cfg:
    x, y = R.to_screen(cfg['cam'], *cfg['ring']); R.ring_at(fr, x, y, 1.0, 58)
# no overall darkening (owner: show the painting as it is); legibility comes from outline + shadow
fr.alpha_composite(R.TOPG); R.logo(fr)

f_big = R.F('NotoSansCJK-Black', 150); f_sub = R.F('NotoSansCJK-Bold', cfg.get('sub_size', 52))
word, col = cfg['accent']
lh = 186; top = cfg.get('top', 960 - lh * len(cfg['lines']) / 2 - 40)
lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
for i, l in enumerate(cfg['lines']):
    cols = []
    j = l.find(word)
    for k in range(len(l)):
        cols.append(col + (255,) if j >= 0 and j <= k < j + len(word) else (255, 255, 255, 255))
    w = R.jp_width(l, f_big, 4); assert w < 1000, (l, w)
    R.draw_line(d, W / 2, top + i * lh, l, f_big, None, 4, 10, (0, 0, 0, 235), cols)
y_sub = top + lh * len(cfg['lines']) + 30
d.rectangle([W / 2 - 122, y_sub - 3, W / 2 + 122, y_sub + 4], fill=(0, 0, 0, 200)); d.line([(W / 2 - 120, y_sub), (W / 2 + 120, y_sub)], fill=(255, 255, 255, 240), width=3)
R.draw_line(d, W / 2, y_sub + 30, cfg['sub'], f_sub, (255, 255, 255, 255), 4, 6, (0, 0, 0, 230))
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(lay.getchannel('A').point(lambda v: int(v * 0.75)))
fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (0, 6)); fr.alpha_composite(lay)
fr.convert('RGB').save(cfg['out'])
# preview with the 3:4 grid crop marked
pv = fr.convert('RGB').copy(); ImageDraw.Draw(pv).rectangle([0, 240, W - 1, 1680], outline=(0, 255, 0), width=6)
pv.resize((360, 640)).save(cfg['out'].replace('.png', '_check.jpg'), quality=85)
print(cfg['out'], 'title block y', int(top), '-', int(y_sub + 100))
