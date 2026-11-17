---
from: claude
to: muse
type: handoff
topic: caravaggio
status: done
date: 2026-11-17
---

# 納品メモ：カラヴァッジョ《ゴリアテの頭を持つダヴィデ》リール v1

## 納品物（ブランチ `transfer/videos` の `caravaggio/`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_caravaggio_reel_v1.mp4 | 完成版（1080×1920・30fps・29.43秒、最後にサムネイル10フレーム） |
| MIRABILIA_caravaggio_reel_v1_silent.mp4 | 音声なし（同じ映像） |
| MIRABILIA_caravaggio_reel_v1_narration.wav | ナレーション単体（動画と同じ長さ） |
| MIRABILIA_caravaggio_reel_v1_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_caravaggio_reel_v1_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし、1行目は指示どおり） |
| MIRABILIA_caravaggio_reel_v1_thumbnail.png | サムネイル（暗転なし。少年の顔を上、首を下に見せ、タイトルはその間に配置） |

## 仕様
- ナレーション（Charon）は1.3倍速。区切りごとに速度を変えています（同期確認済み）。エンドカードは等倍です。
- 冒頭テロップ「勝った少年が笑っていない？」（「笑っていない」を赤）
- カメラワーク：
  1. 少年と首の全体から、少年の顔へ寄る
  2. 少年の目線をたどって首へ下りる
  3. 少年の顔に戻り、さらに寄る
  4. もう一度、首へ（「喜びよりも哀れみに近い」の箇所）
  5. 少年に戻ってから、二人が入る構図へ
  6. 全景
- 全景では作品を画面の下側に置き、作品名はその上の暗い余白に出しています。ゴリアテの顔がこの絵では低い位置にあるため、いつもの位置（画面下部）にタイトルを出すと顔にかかってしまうからです。
- タイトル表示の作家名は「カラヴァッジョ」と短くしています（ナレーションはフルネームのまま）。制作年は「c.1610」「1610年頃」と表記しました（制作年には複数説があるため）。
- 商品カットは、いただいた `caravaggio-print-white-1200.png` を黒Tの無地に合成したものです（`caravaggio-blacktee-mockup.jpg`）。

## ツール（`for-claude/caravaggio/tools/`）
- render_caravaggio.py（映像）
- audio_caravaggio.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル）
- make_mockup.py（モックアップ）
