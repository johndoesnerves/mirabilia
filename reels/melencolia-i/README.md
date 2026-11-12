# メランコリア I（デューラー, 1514）リール

MIRABILIA の Instagram リール。「鬱よ、去れ」軸。

- 企画・台本・キャプション・事実確認メモ：[plan.md](plan.md)
- 完成動画：[output/MIRABILIA_melencolia_reel_v4.mp4](output/MIRABILIA_melencolia_reel_v4.mp4)

## 構成

```
assets/   原画（melencolia.jpg）と商品画像（tee-black.jpg）
src/      render.py（映像）、audio.py（伴奏・効果音を合成）
output/   書き出した動画
build.sh  一式を書き出すスクリプト
```

## 書き出し

必要なもの：Python 3（Pillow, NumPy, SciPy）、ffmpeg（libx264, aac）、Noto CJK フォント（`/usr/share/fonts/opentype/noto/`）

```bash
./build.sh output/MIRABILIA_melencolia_reel_v5.mp4
```

既存のファイル名を指定すると止まり、上書きしません。

特定の時刻のコマを確認するとき：

```bash
python3 src/render.py still 13.6 24.5   # still_13.6.jpg などを書き出す
```

字幕・見出しは `src/render.py` の `SCENES`、カメラの動きは `camera()`、白丸や白線は `overlays()`、効果音のタイミングは `src/audio.py` にあります。
