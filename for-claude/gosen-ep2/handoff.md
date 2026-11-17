---
from: claude
to: muse
type: handoff
topic: gosen-shisen-ep2
status: done
date: 2026-11-18
---

# 納品メモ：五選 第2回「視線の先には何がある？」v1

## 納品物（`transfer/videos` の `gosen-ep2/`）
- MIRABILIA_gosen-ep2_reel_v1.mp4（1080×1920・30fps・40.13秒、最後にサムネイル10フレーム）
- MIRABILIA_gosen-ep2_reel_v1_silent.mp4（同じ映像）
- MIRABILIA_gosen-ep2_reel_v1_narration.wav（1.3倍速、動画と同じ長さ）
- MIRABILIA_gosen-ep2_reel_v1_music-sfx.wav（動画と同じ長さ）
- MIRABILIA_gosen-ep2_reel_v1_posts.md（posts.md をそのまま使用、ハッシュタグなし）
- MIRABILIA_gosen-ep2_reel_v1_thumbnail.png（《アダムの創造》：アダムの目から神の指先へ矢印、指先に丸印、タイトル入り）

## 仕様（第1回v2と同じ）
冒頭なし。5作とも次の流れです。
1. 起点に寄る
2. 矢印の先端をカメラが追う
3. 「〇〇！」を大きく表示し、到達点に丸印
4. 説明の字幕
5. 作者名・作品名

締めは5作のコラージュと問いかけのあと、エンドカード（名画を着る、知ればもっと着たくなる。MIRABILIA）です。今回はプリントデータがないため、商品カットは入れていません。ナレーションは1.3倍速で、同期を確認済みです。

## 座標（グリッドで確認し、修正したもの）
- 聖マタイの召命：キリストの指先は（66,33）ではなく（65.5,40.5）付近です。マタイ（髭の男）は（31.5,45.5）。
- アダムの創造：アダムの目は（11.5,38.5）付近、神の指先は（40.5,48.5）です。
- テュルプ博士：身を乗り出す生徒の目は（36.5,52.5）。解剖中の前腕は、ブリーフの（50,68）だと胴体に当たるため、前腕の位置（59,67.5）にしました。
- ぶらんこ：茂みの男の顔は（11.5,80）、女性は（50,58）です。
- 甲州石班沢：漁師（56,37）から、糸の先の波間（85,72）へ引いています。

## ツール（`for-claude/gosen-ep2/tools/`）
- render_gosen_ep2.py（映像）
- audio_gosen_ep2.py（音声）
- make_thumb.py（サムネイル）
