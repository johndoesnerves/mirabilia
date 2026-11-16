---
from: claude
to: muse
type: handoff
topic: goya
status: done
date: 2026-11-17
---

# 納品メモ：ゴヤ《理性の眠りは怪物を生む》リール v1

## 納品物（ブランチ `transfer/videos` の `goya/`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_goya_reel_v1.mp4 | 完成版（1080×1920・30fps・41.93秒、最後にサムネイル10フレーム） |
| MIRABILIA_goya_reel_v1_silent.mp4 | 音声なし（同じ映像） |
| MIRABILIA_goya_reel_v1_narration.wav | ナレーション単体（動画と同じ長さ） |
| MIRABILIA_goya_reel_v1_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_goya_reel_v1_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし、1行目は指示どおり） |
| MIRABILIA_goya_reel_v1_thumbnail.png | サムネイル（暗転なし、3:4 グリッドの切り抜き内にタイトル） |

## 仕様
- 本編はパンドラ／アイリス納品版と同じ1.3倍、エンドカードは等倍
- 白ロゴは常時表示。販売への言及は答え合わせのあとの商品カットとエンドカードだけ
- 冒頭テロップ「眠ると怪物が生まれる！？」（「怪物」を赤）
- カメラ：全景 → 羽ペンを差し出す1羽 → 背後の群れ → 机の文字で止める（この間は字幕を画面上部へ）→ 男の頭 → 全景で問い → タイトル → 商品 → エンドカード
- 色の演出なし（モノクロ原作のまま）
- 商品カットのモックアップは版面をそのまま黒Tに配置して作りました（`goya-blacktee-mockup.jpg`）。正式なモックアップがあれば差し替えます。

## 確認してほしい点：ナレーション冒頭の無音
- ナレーション v2 は「机で眠る男。」（0.3〜1.4秒）のあとに**約5秒の無音**があります（v1 にはありませんでした）。
- リールの冒頭で4秒近く無音が続くと離脱につながるため、この無音を0.6秒に詰めました。読みは変えていません。
- 意図した間であれば、元の長さに戻して作り直します。

## ツール（`for-claude/goya/tools/`）
- render_goya.py（映像）
- audio_goya.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル）
- make_mockup.py（モックアップ）
