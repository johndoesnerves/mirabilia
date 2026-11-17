---
from: claude
to: muse
type: handoff
topic: bosch
status: on-hold
date: 2026-11-17
---

# 納品メモ：ボス《快楽の園》リール v1

> **【保留中の版】** この v1 は、ブリーフに「制作保留（台本改稿中）」の注記が入る前に、改稿前の台本・ナレーションで作ったものです。投稿には使わないでください。改稿版の台本とナレーションが届いたら、同じ構成（カメラ・サムネイル・モックアップ）のまま作り直します。

## 納品物（ブランチ `transfer/videos` の `bosch/`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_bosch_reel_v1.mp4 | 完成版（1080×1920・30fps・28.80秒、最後にサムネイル10フレーム） |
| MIRABILIA_bosch_reel_v1_silent.mp4 | 音声なし（同じ映像） |
| MIRABILIA_bosch_reel_v1_narration.wav | ナレーション単体（動画と同じ長さ） |
| MIRABILIA_bosch_reel_v1_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_bosch_reel_v1_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし、1行目は指示どおり） |
| MIRABILIA_bosch_reel_v1_thumbnail.png | サムネイル（暗転なし。右扉を表示し、楽器が見える位置より上にタイトル） |

## 仕様
- ナレーション（Charon）は1.3倍速。区切りごとに速度を変えています（同期確認済み）。エンドカードは等倍です。
- 冒頭テロップ「地獄で楽器が拷問道具に？」（「拷問道具」を赤）
- カメラワーク：
  1. 三連画の全景で、右扉に白い枠を付ける
  2. 右扉へ寄る
  3. 巨大な楽器（ハープ・リュート・ハーディ・ガーディ）
  4. 楽器のそばで押し潰される人々に寄って止める
  5. ハープの人物
  6. 右扉全体（答え）
  7. タイトル
  8. 商品（プリントは三連画全体）
  9. エンドカード

## 確認してほしい点：画像の解像度
- `bosch.jpg` は三連画全体で 2000×1138 px のため、右扉の幅は約460 px しかありません。細部に寄るカットは3〜4倍の拡大になり、やや甘く見えます。
- プラドの高解像度画像（右扉だけで幅2000 px 以上）を用意してもらえれば、同じ構成のまま差し替えて作り直します。

## ツール（`for-claude/bosch/tools/`）
- render_bosch.py（映像）
- audio_bosch.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル）
- make_mockup.py（モックアップ）
