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

## rhinoceros/（犀・4点セット）※第5段落の字幕は暫定
| ファイル | 中身 |
|---|---|
| `MIRABILIA_rhinoceros_reel.mp4` | 完成版（ミックス済み・58.6秒） |
| `MIRABILIA_rhinoceros_reel_silent.mp4` | 本編動画・音声なし |
| `MIRABILIA_rhinoceros_reel_narration.wav` | ナレーションのみ（同梱音声と同じ中身を0秒始まり・58.6秒にそろえたもの） |
| `MIRABILIA_rhinoceros_reel_music-sfx.wav` | 伴奏＋効果音のみ |

- 第5段落の文2（38.1–51.6秒）は音声確認待ち（`claude/rhinoceros-consult` の `video/consult-rhinoceros-claude.md`）。**ドライブ移動は確認後の確定版で**。
