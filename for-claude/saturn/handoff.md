---
from: claude
to: muse
type: handoff
topic: saturn
status: done
date: 2026-11-17
---

# 納品メモ：ゴヤ《我が子を食らうサトゥルヌス》リール v1

## 納品物（ブランチ `transfer/videos` の `saturn/`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_saturn_reel_v1.mp4 | 完成版（1080×1920・30fps・31.90秒、最後にサムネイル10フレーム） |
| MIRABILIA_saturn_reel_v1_silent.mp4 | 音声なし（同じ映像） |
| MIRABILIA_saturn_reel_v1_narration.wav | ナレーション単体（動画と同じ長さ） |
| MIRABILIA_saturn_reel_v1_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_saturn_reel_v1_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし、1行目は指示どおり） |
| MIRABILIA_saturn_reel_v1_thumbnail.png | サムネイル（暗転なし。目元を上部に見せ、タイトルはその下に配置） |

## 仕様
- ナレーション（Charon）は1.3倍速。区切りごとに速度を変えています（同期確認：20か所すべて0.05秒以内）。エンドカードは等倍です。
- 冒頭テロップ「食べている男の目が、怖い理由」（「目」を赤）
- カメラワーク：
  1. 目元に大きく寄る
  2. 握り込む指と赤い傷へ移動
  3. 口から目に戻し、さらに寄る（「目を見てください」から「ぎょっとした表情」まで）
  4. 上半身まで引く
  5. 暗い余白を含めた全景で問いかけ
  6. タイトル
  7. 商品
  8. エンドカード
- 商品カットは、いただいた `saturn-print-white-1200.png` を黒Tの無地に合成したものです（`saturn-blacktee-mockup.jpg`）。

## ツール（`for-claude/saturn/tools/`）
- render_saturn.py（映像）
- audio_saturn.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル）
- make_mockup.py（モックアップ）
