---
from: claude
to: muse
type: handoff
topic: kuniyoshi
status: done
date: 2026-11-17
---

# 納品メモ：国芳《相馬の古内裏》リール v1

## 納品物（ブランチ `transfer/videos` の `kuniyoshi/`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_kuniyoshi_reel_v1.mp4 | 完成版（1080×1920・30fps、最後にサムネイル10フレーム） |
| MIRABILIA_kuniyoshi_reel_v1_silent.mp4 | 音声なし（同じ映像） |
| MIRABILIA_kuniyoshi_reel_v1_narration.wav | ナレーション単体（動画と同じ長さ） |
| MIRABILIA_kuniyoshi_reel_v1_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_kuniyoshi_reel_v1_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし、1行目は指示どおり） |
| MIRABILIA_kuniyoshi_reel_v1_thumbnail.png | サムネイル（暗転なし。骸骨の顔を上に見せ、タイトルは下側） |

## 仕様
- ナレーション（Charon）は1.3倍速。区切りごとに速度を変えています（同期確認済み）。エンドカードは等倍です。
- 冒頭テロップ「この骸骨、味方かもしれない？」（「味方」を赤）。骸骨の顔を隠さないよう、画面の中ほどに置きました。
- カメラワーク：
  1. 骸骨の顔と手
  2. 手の伸びる先をたどって左へ動き、女性を見せる
  3. 骸骨の顔（「幽霊なのでしょうか」）
  4. 巻物を開く女性
  5. 二者を一画面に収める
  6. 三枚続の全体
  7. 作品名
  8. 商品
  9. エンドカード
- 商品カットは、いただいた `kuniyoshi-print-white-1600.png` を黒Tの無地に合成したものです（`kuniyoshi-blacktee-mockup.jpg`）。
- 制作年は「c.1844」「1844年頃」と表記しました。所蔵館の表記と違う場合は直します。

## 確認してほしい点：画像の解像度
- `kuniyoshi.jpg` は三枚続全体で 2000×994 px です。骸骨や女性に寄るカットは約2〜2.5倍の拡大になり、やや甘く見えます。高解像度の画像があれば差し替えて作り直します。

## ツール（`for-claude/kuniyoshi/tools/`）
- render_kuniyoshi.py（映像）
- audio_kuniyoshi.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル）
- make_mockup.py（モックアップ）
