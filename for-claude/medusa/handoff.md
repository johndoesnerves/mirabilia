---
from: claude
to: muse
type: handoff
topic: medusa
status: done
date: 2026-11-17
---

# 納品メモ：ジェリコー《メデューズ号の筏》リール v1

## 納品物（ブランチ `transfer/videos` の `medusa/`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_medusa_reel_v1.mp4 | 完成版（1080×1920・30fps・29.83秒、最後にサムネイル10フレーム） |
| MIRABILIA_medusa_reel_v1_silent.mp4 | 音声なし（同じ映像） |
| MIRABILIA_medusa_reel_v1_narration.wav | ナレーション単体（動画と同じ長さ） |
| MIRABILIA_medusa_reel_v1_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_medusa_reel_v1_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし、1行目は指示どおり） |
| MIRABILIA_medusa_reel_v1_thumbnail.png | サムネイル（暗転なし。水平線の船に丸印を付け、タイトルは船にかからない下側に配置） |

## 仕様
- ナレーション（Charon）は1.3倍速。区切りごとに速度を変え、元の時間軸の1/1.3に合わせました（ずれなし）。エンドカードは等倍です。
- 冒頭テロップ「この小さな船に、気づける？」（「小さな船」を赤）
- カメラワーク：
  1. 筏の右側の群像から始める
  2. 布を掲げる男に寄る
  3. 画面の高さいっぱいに戻し、水平線の船に丸印を付ける
  4. 船まで寄る（どれだけ小さいかが伝わる順）
  5. 倒れた人々（左下）から、救いを求める人々へ移動
  6. 全景で、船と筏を一緒に見せて問いかける（船に小さな丸印）
  7. タイトル
  8. 商品
  9. エンドカード
- 「倒れて動かない人と、」の字幕だけは画面上部に出しています。人物に重ならないようにするためです。
- 商品カットは、いただいた `medusa-print-white-1400.png` を黒Tの無地に合成したものです（`medusa-blacktee-mockup.jpg`）。
- 色の演出は入れていません。

## ツール（`for-claude/medusa/tools/`）
- render_medusa.py（映像）
- audio_medusa.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル。丸印と位置指定に対応）
- make_mockup.py（モックアップ）
