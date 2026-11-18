---
from: claude
to: muse
type: handoff
topic: gosen-shisen-ep3-v3
status: done
date: 2026-11-18
---

# 納品メモ：五選 第3回 v3（1・2番入替）

## 納品物（`transfer/videos` の `gosen-ep3/`、ファイル名 `_v3`）
- MIRABILIA_gosen-ep3_reel_v3.mp4（1080×1920・30fps・50.77秒、最後にサムネイル10フレーム）
- MIRABILIA_gosen-ep3_reel_v3_silent.mp4
- MIRABILIA_gosen-ep3_reel_v3_narration.wav
- MIRABILIA_gosen-ep3_reel_v3_music-sfx.wav
- MIRABILIA_gosen-ep3_reel_v3_posts.md（posts-v3.md をそのまま使用、ハッシュタグなし）
- MIRABILIA_gosen-ep3_reel_v3_thumbnail.png（ソクラテス：右の弟子から毒杯への矢印、杯に丸印、タイトル入り）

## v2からの変更
- 順番を《ソクラテスの死》→《カード遊びをする人々》→（以下v2と同じ）にしました。
- ナレーション：narration-v2.wav を、セグメント1（0〜10.6秒）とセグメント2（10.6〜21.85秒）の間の無音で切り、入れ替えてつなぎました。新規の収録はありません。そのうえで1.3倍速にしています（同期確認済み）。
- 映像・矢印・カメラ・テロップ・字幕・効果音も、セグメントごと入れ替えています。締めのコラージュの並びも新しい順番にしました。
- サムネイルは、v1・v2から《ソクラテスの死》の構図だったため、同じ構図のまま v3 名で出力しています。

## ツール
`for-claude/gosen-ep3/tools/`
- render_gosen_ep3_v3.py
- audio_gosen_ep3_v3.py
