#!/bin/bash
# Upload master for IG/TikTok: ONE encode straight from the rendered frames
# (no intermediate mp4), captions + watermark composited in the same pass.
# usage: master.sh FRAMES_PATTERN SRC_FPS START_NUM CAP_DIR WM_END AUDIO DURATION OUT
#   e.g. master.sh '/root/remotion-shorts/out/meng/f/%04d.jpeg' 15 0 /home/claude/mengshort/cap 80.25 mix.wav 85.5 out.mp4
# Why: platforms re-encode everything to ~3-6 Mbps. Feeding them a 3-6 Mbps
# file that was already encoded twice (crf18 -> crf18) stacks a third
# generation of loss on flat cartoon colours (banding, blocky edges).
set -e
FR=$1; FPS=$2; SN=$3; CAP=$4; WMEND=$5; AUD=$6; DUR=$7; OUT=$8
WM=/home/claude/parisshort/wm.png
ffmpeg -loglevel error -y \
  -framerate $FPS -start_number $SN -i "$FR" \
  -framerate 30 -i "$CAP/c%04d.png" \
  -i $WM -i "$AUD" \
  -filter_complex "[0:v]fps=30,format=rgb24[b];[b][1:v]overlay=0:0:eof_action=pass[a];[a][2:v]overlay=0:0:enable='lt(t,$WMEND)',scale=1080:1920:flags=lanczos+accurate_rnd+full_chroma_int:out_color_matrix=bt709:out_range=tv,format=yuv420p[v]" \
  -map "[v]" -map 3:a \
  -c:v libx264 -preset slow -tune animation -crf 12 -maxrate 30M -bufsize 60M \
  -profile:v high -level 4.2 -g 60 -keyint_min 30 -sc_threshold 0 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -c:a aac -b:a 320k -ar 48000 -ac 2 \
  -t $DUR -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration,bit_rate -of csv=p=0 "$OUT"
