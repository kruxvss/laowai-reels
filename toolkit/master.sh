#!/bin/bash
# Upload master for IG/TikTok: ONE encode straight from the rendered frames
# (no intermediate mp4), captions + watermark composited in the same pass.
# COVER=/path/cover.png appends the cover as the last 0.2 s (TikTok picks its cover from a frame:
#   set videoCoverMilliseconds to (DURATION + 0.1) * 1000)
# usage: master.sh FRAMES_PATTERN SRC_FPS START_NUM CAP_DIR WM_END AUDIO DURATION OUT
#   e.g. master.sh '/root/remotion-shorts/out/meng/f/%04d.jpeg' 15 0 /home/claude/mengshort/cap 80.25 mix.wav 85.5 out.mp4
# Why: platforms re-encode everything to ~3-6 Mbps. Feeding them a 3-6 Mbps
# file that was already encoded twice (crf18 -> crf18) stacks a third
# generation of loss on flat cartoon colours (banding, blocky edges).
set -e
FR=$1; FPS=$2; SN=$3; CAP=$4; WMEND=$5; AUD=$6; DUR=$7; OUT=$8
WM=/home/claude/parisshort/wm.png
LAST=m; [ -n "$COVER" ] && LAST=m2
ffmpeg -loglevel error -y \
  -framerate $FPS -start_number $SN -i "$FR" \
  -framerate 30 -i "$CAP/c%04d.png" \
  -i $WM -i "$AUD" ${COVER:+-loop 1 -framerate 30 -t 0.2 -i "$COVER"} \
  -filter_complex "[0:v]fps=30,format=rgb24[b];[b][1:v]overlay=0:0:eof_action=pass[a];[a][2:v]overlay=0:0:enable='lt(t,$WMEND)',trim=duration=$DUR,setpts=PTS-STARTPTS,format=rgb24[m];${COVER:+[4:v]scale=1080:1920,fps=30,format=rgb24,setsar=1[cv];[m][cv]concat=n=2:v=1:a=0,format=rgb24[m2];}[$LAST]scale=1080:1920:flags=lanczos+accurate_rnd+full_chroma_int:out_color_matrix=bt709:out_range=tv,format=yuv420p[v];[3:a]apad[au]" \
  -map "[v]" -map "[au]" \
  -c:v libx264 -preset slow -tune animation -crf ${CRF:-12} -maxrate 30M -bufsize 60M \
  -profile:v high -level 4.2 -g 60 -keyint_min 30 -sc_threshold 0 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -c:a aac -b:a 320k -ar 48000 -ac 2 \
  -t $(python3 -c "print($DUR+(0.2 if \"$COVER\" else 0))") -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration,bit_rate -of csv=p=0 "$OUT"
# GitHub refuses files >100 MB (raw URLs are how Metricool fetches media)
SZ=$(stat -c %s "$OUT")
if [ "$SZ" -gt 95000000 ]; then echo "WARN: $SZ bytes > 95 MB: re-run with CRF=14"; fi
