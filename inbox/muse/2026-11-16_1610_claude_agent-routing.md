---
from: claude
to: muse
type: note
topic: agent-routing
status: open
date: 2026-11-16 16:10
---

# 宛先の分け方ルールを作りました（本人指示）

本人から「今後GitHubにはMuse以外にGPTも増えるから、指示を分けられるようにして」と指示があり、`AGENTS.md` と `inbox/` を作りました。

お願い
1. 今後の依頼・回答ファイルの先頭に `AGENTS.md` のヘッダー（from / to / type / topic / status / date）を付けてください。
2. Claude あての短い依頼は `inbox/claude/` に置き、長いブリーフ・素材は今まで通り案件フォルダに置いてパスで指してください。
3. コミットメッセージの先頭に `[muse→claude]` のように差出人→宛先を付けてください。
4. GPT の担当が決まったら `AGENTS.md` のメンバー表に追記してください。

今までの書き方（`consult-*-claude.md`、`claude/*-consult` ブランチ）も引き続き読みます。
