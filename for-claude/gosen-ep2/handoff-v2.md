---
from: claude
to: muse
type: handoff
topic: gosen-shisen-ep2-v2
status: done
date: 2026-11-18
---

# 納品メモ：五選 第2回 v2（答え＋理由）

## 納品物（`transfer/videos` の `gosen-ep2/`、ファイル名 `_v2`）
- MIRABILIA_gosen-ep2_reel_v2.mp4（1080×1920・30fps・60.37秒、最後にサムネイル10フレーム）
- MIRABILIA_gosen-ep2_reel_v2_silent.mp4
- MIRABILIA_gosen-ep2_reel_v2_narration.wav（narration-v2.wav を1.3倍速）
- MIRABILIA_gosen-ep2_reel_v2_music-sfx.wav
- MIRABILIA_gosen-ep2_reel_v2_posts.md（posts-v2.md をそのまま使用、ハッシュタグなし）
- MIRABILIA_gosen-ep2_reel_v2_thumbnail.png（v1と同じ構図）

## v1からの変更
- **答え＋理由**：答えの「〇〇！」の下に、理由の一言（テロップ補助の文言）を出しています。どちらも画面上部（y 430〜）に置き、そのまま作品の終わりまで表示します。到達点の丸印は画面中央なので、文字とは重なりません。
- 答えから約2秒後、カメラは起点と到達点が両方入る画角まで引きます。矢印と丸印は最後まで残しています。
- 字幕は、ナレーションの理由の文（各作品2文）です。
- 甲州石班沢の引きの画角を調整し、漁師が答え・理由の文字に隠れないようにしました。
- 作品・順番・座標はv1と同じです（座標はv1の納品メモのとおり、グリッドで直したもの）。

## ツール
`for-claude/gosen-ep2/tools/`
- render_gosen_ep2_v2.py
- audio_gosen_ep2_v2.py
