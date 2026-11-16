# mirabilia

MIRABILIA（BASEショップ https://mirabilia.base.shop）の制作ファイル置き場。
AIエージェント（Claude／GPT）とのファイルやりとり用リポジトリ（2026-11-12 設置、2026-11-16 に担当別構成へ改定）。

## 担当別の指示分け（2026-11-16〜）

複数のAIが参加するため、**指示は担当ごとにフォルダとブランチを分ける**。

- **フォルダ**
  - `for-claude/<topic>/` — Claude への指示（brief.md＋素材）。納品メモ `handoff.md` と依頼 `request.md` も Claude がここへ戻す
  - `for-gpt/<topic>/` — GPT（ASTRA）への指示。同上
  - `shared/` — 担当を問わない確定資料（ブランドルール・台本の正本など）
  - `theme/` — BASEテーマ
  - `video/` — 旧ラインの動画ドキュメント（記録用）
- **ブランチ名**：`<担当>/<topic>`（例：`claude/goya-reel`、`gpt/scripts-batch2`）
- **納品**：完成品は `transfer/videos` ブランチへ（現行運用を継続）。納品メモは担当フォルダの `handoff.md` にも残す
- 既存の `claude/*-consult` ブランチ上のファイルは移行しない。新規の指示からこの構成を使う

## 中身
- `theme/` — BASEカスタムテーマ（HTML編集App用）
  - `mirabilia-theme.html` — Claude制作・検品済みのテーマ単一HTML（画像URLはBASEアップロード済みのものに差し替え済み）
- `video/` — Instagramリール動画の量産ドキュメント
  - `video-production-system.md` — 量産工程・固定フォーマット・20図案キュー
  - `video-conte-prompt.md` — コンテ標準プロンプト＋タイトル制作ルール
  - `melencolia-reel-plan-goaway-final.md` — メランコリア I「鬱よ、去れ」軸 最終改訂案（動画完成済み）
  - `melencolia-reel-plan-final.md` — 同「作者自身」軸案（不採用・記録用）

## 運用
- 正本はこのリポジトリ。編集したらコミットして push する。
- 動画ファイル（MP4）などの大きなバイナリはここには置かない。
