#!/usr/bin/env bash
# Wrapper pour lancer hdmi-resume avec les bonnes variables Wayland

export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"

/home/tofunori/.local/bin/hdmi-resume.sh
