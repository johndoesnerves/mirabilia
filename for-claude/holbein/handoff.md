---
from: claude
to: muse
type: handoff
topic: holbein
status: done
date: 2026-11-17
---

# 納品メモ：ホルバイン《大使たち》リール v1

## 納品物（ブランチ `transfer/videos` の `holbein/`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_holbein_reel_v1.mp4 | 完成版（1080×1920・30fps、最後にサムネイル10フレーム） |
| MIRABILIA_holbein_reel_v1_silent.mp4 | 音声なし（同じ映像） |
| MIRABILIA_holbein_reel_v1_narration.wav | ナレーション単体（動画と同じ長さ） |
| MIRABILIA_holbein_reel_v1_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_holbein_reel_v1_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし、1行目は指示どおり） |
| MIRABILIA_holbein_reel_v1_thumbnail.png | サムネイル（暗転なし。タイトルを上に置き、床の白い形を下に見せる） |

## 仕様
- ナレーション（Charon）は1.3倍速。区切りごとに速度を変えています（同期確認済み）。エンドカードは等倍です。
- 冒頭テロップ「斜めから見るとドクロになる絵？」（「ドクロ」を赤）
- **頭蓋骨が現れる動き**：白い形の長い軸（右上がり約24°）に沿って、画面全体を約1/4まで縮めています。左下から斜めに見たときと同じ見え方になるため、本物の頭蓋骨が現れます。「斜め下から見ると」から縮め始め、「頭蓋骨に見えてくるのです」まで止め、元の全景に戻します。縮めている間は「↙ 左下から見ると」と表示します。
- 前半は白い形が画面中央に来るため、字幕を画面上部に置いています。
- 全景では絵を上側に置き、字幕と作品名はその下に出しています。
- 商品カットは、いただいた `holbein-print-white-1400.png` を黒Tの無地に合成したものです（`holbein-blacktee-mockup.jpg`）。

## ツール（`for-claude/holbein/tools/`）
- render_holbein.py（映像。縮める処理は painting() と SQ）
- audio_holbein.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル）
- make_mockup.py（モックアップ）
