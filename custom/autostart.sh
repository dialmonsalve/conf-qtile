#!/bin/sh

#Configurar teclado espanol
setxkbmap latam &

sleep 2
#Configuracion de la resolucion
xrandr --output eDP1 --primary --mode 1366x768 --pos 0x0 --rotate normal --output HDMI1 --mode 1366x768 --pos 1366x0 --rotate normal --output VIRTUAL1 --off

#Icono del sistema
udiskie -t &

nm-applet &

volumeicon &

cbatticon -u 5 &

nitrogen --restore &