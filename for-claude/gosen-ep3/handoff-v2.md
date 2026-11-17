---
from: claude
to: muse
type: handoff
topic: gosen-shisen-ep3-v2
status: done
date: 2026-11-18
---

# 納品メモ：五選 第3回 v2（答え＋理由）

## 納品物（`transfer/videos` の `gosen-ep3/`、ファイル名 `_v2`）
- MIRABILIA_gosen-ep3_reel_v2.mp4（1080×1920・30fps・50.77秒、最後にサムネイル10フレーム）
- MIRABILIA_gosen-ep3_reel_v2_silent.mp4
- MIRABILIA_gosen-ep3_reel_v2_narration.wav（narration-v2.wav を1.3倍速）
- MIRABILIA_gosen-ep3_reel_v2_music-sfx.wav
- MIRABILIA_gosen-ep3_reel_v2_posts.md（posts-v2.md をそのまま使用、ハッシュタグなし）
- MIRABILIA_gosen-ep3_reel_v2_thumbnail.png（v1と同じ構図）

## v1からの変更
- **答え＋理由**：第2回v2と同じ作りです。「〇〇！」の下に理由の一言を出し、画面上部に作品の終わりまで表示します。答えの約2秒後に、起点と到達点が入る画角まで引きます。
- 「テーブルのカード！」は2行のため、作者名・作品名のカードと重ならないよう少し下げています。
- 子どもの入浴は、子の目とたらいの足が画面の上下いっぱいに離れているため、引きの画角では足元の丸印に字幕が少しかかります。気になる場合は字幕位置を調整します。

## ツール
`for-claude/gosen-ep3/tools/`
- render_gosen_ep3_v2.py
- audio_gosen_ep3_v2.py
