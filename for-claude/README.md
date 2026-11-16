# for-claude/ — Claude への指示置き場

スシ（司令塔）から **Claude** への指示はここに入る。GPT への指示は `for-gpt/` にあるので混ぜない。

## 置き方
- トピックごとにフォルダを作る：`for-claude/<topic>/`
- フォルダの中身：
  - `brief.md` — 指示書（作るもの・仕様・文面・締切）
  - 素材ファイル（音声・画像など、そのトピックで使うもの）
  - `handoff.md` — Claude が納品時に書くメモ（Claude が作成）
  - `request.md` — Claude からスシへの依頼・確認（Claude が作成）
- 納品物そのものは `transfer/` ブランチへ（下記 README の運用ルール参照）
