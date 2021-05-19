#!/bin/sh

xinput set-prop "MSFT0004:00 06CB:CD98 Touchpad" "libinput Tapping Enabled" 1

source /home/igg/.fehbg
dunst &
picom &

# exec dwm
qtile start
