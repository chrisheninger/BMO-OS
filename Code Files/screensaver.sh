#!/bin/bash
process() {
while read input; do
	case "$input" in
		UNBLANK*) pkill vlc ;;
		BLANK*) vlc --loop --no-osd --fullscreen "/home/bmo/animations/BMO_Idle_loop_ColorAdjust.mp4" & ;;
	esac
done
}

/usr/bin/xscreensaver-command -watch | process
