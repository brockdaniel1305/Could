#!/bin/sh
# One command for a finished episode on your own machine (VoiceStudio running):
#   sh tools/make_episode.sh episodes/001-neuer-titanic            # voice from narration.json (VoiceStudio)
#   sh tools/make_episode.sh episodes/001-neuer-titanic --preview  # Kokoro preview voice
set -e
EP="$1"; shift
NAME=$(basename "$EP")
python3 tools/build_episode.py "$EP" "$@"
sh "$EP/src/build_all.sh"
cd "$EP"
npx --yes hyperframes lint
mkdir -p renders
npx --yes hyperframes render --quality looks --output "renders/$NAME.mp4"
ffmpeg -y -loglevel error -i "renders/$NAME.mp4" -c:v copy -af loudnorm=I=-15:TP=-1.5:LRA=11 -c:a aac -b:a 192k \
  -movflags +faststart "renders/$NAME-final.mp4"
echo "Done: $EP/renders/$NAME-final.mp4"
