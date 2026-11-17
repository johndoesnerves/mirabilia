---
from: claude
to: muse
type: handoff
topic: hokusai
status: done
date: 2026-11-17
---

# 納品メモ：北斎《神奈川沖浪裏》リール v1

## 納品物（ブランチ `transfer/videos` の `hokusai/`）
| ファイル | 内容 |
|---|---|
| MIRABILIA_hokusai_reel_v1.mp4 | 完成版（1080×1920・30fps・44.30秒、最後にサムネイル10フレーム） |
| MIRABILIA_hokusai_reel_v1_silent.mp4 | 音声なし（同じ映像） |
| MIRABILIA_hokusai_reel_v1_narration.wav | ナレーション単体（動画と同じ長さ） |
| MIRABILIA_hokusai_reel_v1_music-sfx.wav | 伴奏＋効果音（動画と同じ長さ） |
| MIRABILIA_hokusai_reel_v1_posts.md | 投稿テキスト（Instagram／TikTok／YouTube Shorts、ハッシュタグなし、1行目は指示どおり） |
| MIRABILIA_hokusai_reel_v1_thumbnail.png | サムネイル（暗転なし、富士山が見える位置にタイトルを配置、3:4 の切り抜き内） |

## 仕様
- ナレーション（Charon）は1.3倍速。区切りごとに速度を変えて元の時間軸の1/1.3に合わせたので、ずれはありません。エンドカードは等倍です。
- 冒頭テロップ「この富士山、大波より小さい！？」（「小さい」を赤）
- カメラワーク：
  1. 冒頭は波と富士を同時に見せる切り取り
  2. 富士に寄る
  3. 引いて、波との位置関係を見せる
  4. 全景にして3隻の舟に番号付きの丸印を付ける
  5. 右の舟の人々に寄る
  6. 「もう一度、富士へ」で止める
  7. 波と富士の切り取りに戻る
  8. 全景で問いかけ
  9. タイトル
  10. 商品
  11. エンドカード
- 字幕が富士山に重ならないよう、波と富士の切り取りでは富士山を字幕の帯より上に置いています。
- 商品カットのモックアップは、作品画像をそのまま黒Tに配置して作りました（`hokusai-blacktee-mockup.jpg`、アイリスと同じ位置）。正式なモックアップがあれば差し替えます。

## 補足
- 音源の WAV は途中から読み込むと無音になる形式だったため、一度通常の WAV に変換してから使いました。中身は変えていません。

## ツール（`for-claude/hokusai/tools/`）
- render_hokusai.py（映像）
- audio_hokusai.py（音声）
- speed_narration.py（1.3倍化）
- check_sync.py（同期確認）
- make_thumb.py（サムネイル）
- make_mockup.py（モックアップ）
