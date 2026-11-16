# transfer/videos（動画の一時置き場・mainにはマージしない）

Claude → スシ の受け渡し専用。mainとは履歴がつながっていない。ドライブへ移したらブランチごと削除してよい（manual STEP 7）。

## leviathan/（v7 分離納品・4点セット）
| ファイル | 中身 |
|---|---|
| `MIRABILIA_leviathan_reel_v7.mp4` | 完成版（ミックス済み）。前回納品と同一（ドライブ移動済みなら不要） |
| `MIRABILIA_leviathan_reel_v7_video-only.mp4` | 本編動画・**音声なし**（1080×1920・30fps・51.3秒） |
| `MIRABILIA_leviathan_reel_v7_narration.wav` | ナレーションのみ（44.1kHz・ステレオ・51.3秒、0秒始まりで映像と位置合わせ済み） |
| `MIRABILIA_leviathan_reel_v7_music-sfx.wav` | 伴奏＋効果音のみ（同上） |

- ナレーション＋伴奏・効果音を足すと完成版の音声と一致（誤差は丸めの1段階のみ）。伴奏には「声に重なる間だけ下げる」音量調整が焼き込み済み。別の音源に付け替える場合は伴奏ファイルを使わず、ナレーション＋新しい音源で組む。
- 音声2点はWAV（MP3は先頭に約0.03秒の無音が入り、映像とずれるため）。

## rhinoceros/（犀 v2・4点セット・確定版）
| ファイル | 中身 |
|---|---|
| `MIRABILIA_rhinoceros_reel_v2.mp4` | 完成版（ミックス済み・46.97秒） |
| `MIRABILIA_rhinoceros_reel_v2_silent.mp4` | 本編動画・音声なし |
| `MIRABILIA_rhinoceros_reel_v2_narration.wav` | ナレーションのみ（再生成版を0秒始まり・46.97秒にそろえたもの） |
| `MIRABILIA_rhinoceros_reel_v2_music-sfx.wav` | 伴奏＋効果音のみ |

- 暫定だった v1（旧音声）はこのブランチから削除済み。ドライブへはこの v2 を移してください。

## pandora/（パンドラ v1・新ライン1本目・4点セット＋カバー画像）
| ファイル | 中身 |
|---|---|
| `MIRABILIA_pandora_reel_v1.mp4` | 完成版（ミックス済み・49.1秒） |
| `MIRABILIA_pandora_reel_v1_silent.mp4` | 本編動画・音声なし |
| `MIRABILIA_pandora_reel_v1_narration.wav` | ナレーションのみ（確定版音声を0秒始まり・49.1秒にそろえたもの） |
| `MIRABILIA_pandora_reel_v1_music-sfx.wav` | 伴奏＋効果音のみ |
| `MIRABILIA_pandora_reel_v1_cover.png` | カバー画像（動画の0秒目と同じ。カバー文入り） |

### pandora/ v2（1.3倍速版・本人指定）
| ファイル | 中身 |
|---|---|
| `MIRABILIA_pandora_reel_v2.mp4` | 完成版（38.5秒。本編を1.3倍速、エンドカードは等倍3.2秒） |
| `MIRABILIA_pandora_reel_v2_silent.mp4` | 本編動画・音声なし |
| `MIRABILIA_pandora_reel_v2_narration.wav` | ナレーション1.3倍速（声の高さは変えていない） |
| `MIRABILIA_pandora_reel_v2_music-sfx.wav` | 伴奏＋効果音（新しい尺に合わせて作り直し。テンポは等倍） |
| `MIRABILIA_pandora_reel_v2_cover.png` | カバー画像（v1と同じ） |

## irises/（アイリス v1・新ライン2本目・4点セット）
| ファイル | 中身 |
|---|---|
| `MIRABILIA_irises_reel_v1.mp4` | 完成版（39.7秒。本編1.3倍速、エンドカード等倍3.2秒） |
| `MIRABILIA_irises_reel_v1_silent.mp4` | 本編動画・音声なし |
| `MIRABILIA_irises_reel_v1_narration.wav` | ナレーション1.3倍速（声の高さは変えていない、0秒始まり・39.7秒） |
| `MIRABILIA_irises_reel_v1_music-sfx.wav` | 伴奏＋効果音 |

## 投稿テキスト（2026-11-16〜・本人指示）
完成版と同じフォルダに `…_posts.md`（Instagram／TikTok／YouTubeショートの投稿文）を置く。
- `pandora/MIRABILIA_pandora_reel_v2_posts.md`
- `irises/MIRABILIA_irises_reel_v1_posts.md`

## サムネイル画像（2026-11-16〜・本人指示）
完成版と同じフォルダに `…_thumbnail.png`（1080×1920。冒頭の絵＋動画タイトルを大きく。文字はプロフィール一覧の3:4切り抜き内に収めてある）を置く。
- `pandora/MIRABILIA_pandora_reel_v2_thumbnail.png`
- `irises/MIRABILIA_irises_reel_v1_thumbnail.png`

## 最新版（2026-11-16 15:3x・本人指示を反映）— **投稿はこの版を全媒体で使う**
- `pandora/…_v3.*`、`irises/…_v2.*`（それぞれ6点：完成版／音声なし／ナレーション／伴奏＋効果音／投稿テキスト／サムネイル）
- 変更点：**動画の最後10フレーム（約0.33秒）にサムネイルを追加**（YouTubeショートのサムネイル選択用。本人「サムネを最後につけた版をどの媒体も使う」）。ナレーション・伴奏の音声ファイルも同じ長さに無音で合わせた
- サムネイルは背景を暗くしない版に変更（本人指示）。読みやすさは文字の縁取りと影で確保
- 旧版（パンドラ v1・v2、アイリス v1）は不要になった。ドライブに移す場合は最新版だけでよい

- 投稿テキストはハッシュタグなし（2026-11-16 15:38 本人指示。YouTubeタイトルの #Shorts も外した）
