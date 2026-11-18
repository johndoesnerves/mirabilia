---
from: claude
to: muse
type: handoff
topic: gosen-shisen-ep2-v3
status: done
date: 2026-11-18
---

# 納品メモ：五選 第2回 v3（1・2番入替）

## 納品物（`transfer/videos` の `gosen-ep2/`、ファイル名 `_v3`）
- MIRABILIA_gosen-ep2_reel_v3.mp4（1080×1920・30fps・60.37秒、最後にサムネイル10フレーム）
- MIRABILIA_gosen-ep2_reel_v3_silent.mp4
- MIRABILIA_gosen-ep2_reel_v3_narration.wav
- MIRABILIA_gosen-ep2_reel_v3_music-sfx.wav
- MIRABILIA_gosen-ep2_reel_v3_posts.md（posts-v3.md をそのまま使用、ハッシュタグなし）
- MIRABILIA_gosen-ep2_reel_v3_thumbnail.png（アダムの創造：アダムの目から神の指先への矢印、指先に丸印、タイトル入り）

## v2からの変更
- 順番を《アダムの創造》→《聖マタイの召命》→（以下v2と同じ）にしました。
- ナレーション：narration-v2.wav を、セグメント1（0〜13.45秒）とセグメント2（13.45〜27.15秒）の間の無音で切り、入れ替えてつなぎました。新規の収録はありません。そのうえで1.3倍速にしています（同期確認済み）。
- 映像・矢印・カメラ・テロップ・字幕・効果音も、セグメントごと入れ替えています。締めのコラージュの並びも新しい順番にしました。
- サムネイルは、v1・v2から《アダムの創造》の構図だったため、同じ構図のまま v3 名で出力しています。

## ツール
`for-claude/gosen-ep2/tools/`
- render_gosen_ep2_v3.py
- audio_gosen_ep2_v3.py
