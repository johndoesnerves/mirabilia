#!/usr/bin/env bash
# 「メランコリア I」リールを書き出す（1080×1920 / 30fps / 33.5秒）
# 使い方: ./build.sh [出力ファイル名]   既存ファイルは上書きしない
set -euo pipefail
cd "$(dirname "$0")"
OUT="${1:-output/MIRABILIA_melencolia_reel.mp4}"
if [ -e "$OUT" ]; then echo "既に存在します: $OUT（別名を指定してください）" >&2; exit 1; fi
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# シーン境界（フレーム番号, 30fps）
# フック 0–3.5 / サイン1 –7.5 / サイン2 –11.7 / サイン3 –17.3 / サイン4 –21.6 / サイン5 –27.0 / 商品 –29.5 / エンド –33.5
B=(0 105 225 351 519 648 810 885 1005)
for i in 0 1 2 3 4 5 6 7; do echo "${B[$i]} ${B[$((i+1))]} $i"; done \
  | xargs -P 2 -n 3 sh -c 'python3 src/render.py scene $0 $1 '"$WORK"'/sc$2.mp4'

python3 src/audio.py "$WORK/audio.wav"
for i in 0 1 2 3 4 5 6 7; do echo "file '$WORK/sc$i.mp4'"; done > "$WORK/list.txt"
ffmpeg -loglevel error -f concat -safe 0 -i "$WORK/list.txt" -c copy "$WORK/video.mp4"
ffmpeg -n -loglevel error -i "$WORK/video.mp4" -i "$WORK/audio.wav" -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "書き出し完了: $OUT"
