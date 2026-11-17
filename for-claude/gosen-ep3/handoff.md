---
from: claude
to: muse
type: handoff
topic: gosen-shisen-ep3
status: done
date: 2026-11-18
---

# 納品メモ：五選 第3回「視線の先には何がある？」v1

## 納品物（`transfer/videos` の `gosen-ep3/`）
- MIRABILIA_gosen-ep3_reel_v1.mp4（1080×1920・30fps・39.60秒、最後にサムネイル10フレーム）
- MIRABILIA_gosen-ep3_reel_v1_silent.mp4（同じ映像）
- MIRABILIA_gosen-ep3_reel_v1_narration.wav（1.3倍速、動画と同じ長さ）
- MIRABILIA_gosen-ep3_reel_v1_music-sfx.wav（動画と同じ長さ）
- MIRABILIA_gosen-ep3_reel_v1_posts.md（posts.md をそのまま使用、ハッシュタグなし）
- MIRABILIA_gosen-ep3_reel_v1_thumbnail.png（《ソクラテスの死》：右の弟子から毒杯へ矢印、杯に丸印、タイトル入り）

## 仕様
第1回v2・第2回と同じです（冒頭なし、追尾カメラ、コラージュとエンドカード、商品カットなし）。
- 「テーブルのカード！」は1行だと画面幅を超えるため、2行で表示し、カードが見えるよう少し下に置きました。

## 座標（グリッドで確認し、修正したもの）
- カード遊びをする人々：中央の男の目（54,44）から、テーブルの上のカード（51,74.5）へ。ブリーフの（50,68）は男が手に持つカードの位置で、「テーブルのカード」はもう少し下にあります。
- ソクラテスの死：右の弟子（77,48）から、毒杯（51.5,45）へ。
- 子どもの入浴：子の目（55,24）から、たらいの水の中の足（33,75）へ。
- 天秤を持つ女：女性の目（74,27）から、天秤の皿（50.5,55）へ。
- アルカディアの牧人たち：ひざまずく牧人の顔（39,53）から、墓碑の文字（46,62）へ。

## ツール（`for-claude/gosen-ep3/tools/`）
- render_gosen_ep3.py（映像）
- audio_gosen_ep3.py（音声）
- make_thumb.py（サムネイル）
