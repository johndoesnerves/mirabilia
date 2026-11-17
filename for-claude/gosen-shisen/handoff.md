---
from: claude
to: muse
type: handoff
topic: gosen-shisen
status: done
date: 2026-11-17
---

# 納品メモ：五選 第1回「視線の先には何がある？」 v1

## 納品物（ブランチ `transfer/videos` の `gosen-shisen/`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_gosen-shisen_reel_v1.mp4 | 完成版（1080×1920・30fps・52.83秒、最後にサムネイル10フレーム） |
| MIRABILIA_gosen-shisen_reel_v1_silent.mp4 | 音声なし（同じ映像、サムネイル10フレーム付き） |
| MIRABILIA_gosen-shisen_reel_v1_narration.wav | ナレーション単体（動画と同じ長さ） |
| MIRABILIA_gosen-shisen_reel_v1_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_gosen-shisen_reel_v1_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし。種の文面を土台に、5作の答えを並べました） |
| MIRABILIA_gosen-shisen_reel_v1_thumbnail.png | サムネイル（システィーナの聖母の天使アップ＋タイトル、暗転なし） |

## 型（5作品とも同じ順）
1. 絵を見せる
2. 視線の元へ寄る
3. 上部にテロップ「視線の先には何がある？」
4. 白い矢印（黒い縁と影付き）が視線の先へ伸びる
5. 画面中央に「〇〇！」を大きく表示
6. 一言解説の字幕
7. 上部に作者名・作品名カード

締めは5作のコラージュで「どの作品の視線が気になりましたか？」と問いかけ、オソーリオのTシャツ（`osorio-print-white-1100.png` を黒Tに合成）、エンドカードの順です。

- ナレーションは1.3倍速。区切りごとに速度を変えています（同期確認済み）。エンドカードは等倍のため、全体は約49秒＋エンドカード約3秒です。
- 回答の効果音（チャイム）・矢印の効果音・作品の切り替え音は、5作でそろえています。

## 矢印の位置：ブリーフの座標とずれていたもの
実画像のグリッドで確認したところ、いくつかの座標がブリーフとずれていたため、実画像に合わせました。
- ナルキッソス：目元はブリーフの（20%,26%）ではなく（28%,30%）付近。水面の顔は（30%,88%）付近。
- 牛乳を注ぐ女：目元は（55%,27%）付近、牛乳の流れは（34%,57%）付近（ブリーフは（40%,30%）→（42%,52%））。
- システィーナの聖母：聖母の顔は（46%,15%）付近。
- ラス・メニーナス：鏡は（42%,57%）付近。矢印は王女の顔から鏡へ引いています。
- オソーリオ：猫たち（22%,65%）からカササギ（28%,81%）へ。カササギに丸印を付けています。

## ツール（`for-claude/gosen-shisen/tools/`）
- render_gosen.py（映像。作品ごとの設定は WORKS）
- audio_gosen.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル）
- make_mockup.py（モックアップ）
