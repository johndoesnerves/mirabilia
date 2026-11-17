---
from: claude
to: muse
type: handoff
topic: bosch
status: done
date: 2026-11-17
---

# 納品メモ：ボス《快楽の園》リール v2（改稿版）

## 納品物（ブランチ `transfer/videos` の `bosch/`、ファイル名は `_v2`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_bosch_reel_v2.mp4 | 完成版（1080×1920・30fps・30.23秒、最後にサムネイル10フレーム） |
| MIRABILIA_bosch_reel_v2_silent.mp4 | 音声なし（同じ映像） |
| MIRABILIA_bosch_reel_v2_narration.wav | ナレーション単体（改稿版、動画と同じ長さ） |
| MIRABILIA_bosch_reel_v2_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_bosch_reel_v2_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし、1行目は改稿版の指示どおり） |
| MIRABILIA_bosch_reel_v2_thumbnail.png | サムネイル（暗転なし。タイトルを上に置き、ハープと楽器を下側に見せる） |

同じフォルダにある `_v1` は改稿前の旧版です。投稿には使わないでください（フォルダの README.md にも記載）。

## 仕様
- ナレーション（Charon、改稿版）は1.3倍速。区切りごとに速度を変えています（同期確認済み）。エンドカードは等倍です。
- 冒頭テロップ「地獄の楽器が、人を苦しめる理由は？」（「苦しめる」を赤）
- 画像は、いただいた `bosch-right-panel.jpg`（980×2186）を使いました。寄りのカットも十分な解像度になっています。
- カメラワーク（ASTRA改稿版メモどおり）：
  1. 冒頭、ハープの弦に絡め取られた人へ寄る
  2. 引いて、ハープの巨大さを見せる
  3. リュートの下に押さえつけられた人物へ寄り、丸印を付ける
  4. 楽器群まで引く
  5. ハープ全体に戻して作品名
  6. 商品（プリントは三連画全体）
  7. エンドカード
- 商品カットは、いただいた `bosch-print-white-1600.png` を黒Tの無地に合成したものです（`bosch-blacktee-mockup.jpg`）。

## ツール（`for-claude/bosch/tools/`）
- render_bosch.py（映像）
- audio_bosch.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル）
- make_mockup.py（モックアップ）
