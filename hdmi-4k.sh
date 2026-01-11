#!/usr/bin/env bash
set -euo pipefail

# HDMI 4K Hotplug Workaround for NVIDIA on Linux
# Fixes black screen on HDMI connect by cycling through lower resolution first

output="HDMI-A-1"

LOCKFILE="/tmp/hdmi-4k.lock"
LOGFILE="/tmp/hdmi-4k.log"
TARGET_USER="tofunori"  # Change this to your username
TARGET_UID=$(id -u "$TARGET_USER")

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
}

run_as_user() {
  runuser -u "$TARGET_USER" -- env \
    WAYLAND_DISPLAY=wayland-1 \
    XDG_RUNTIME_DIR="/run/user/$TARGET_UID" \
    "$@"
}

# Strict lock - exit if already running
if [[ -f "$LOCKFILE" ]]; then
  exit 0
fi

touch "$LOCKFILE"
(sleep 60 && rm -f "$LOCKFILE") &

log "Start"

sleep 2

# Check connection
if [[ -r "/sys/class/drm/card1-${output}/status" ]]; then
  if [[ "$(cat "/sys/class/drm/card1-${output}/status")" != "connected" ]]; then
    rm -f "$LOCKFILE"
    exit 0
  fi
fi

# 1080p first to wake the display, then 4K
log "1080p"
run_as_user cosmic-randr mode "$output" 1920 1080 --refresh 60 >> "$LOGFILE" 2>&1 || true

sleep 1

log "4K"
run_as_user cosmic-randr mode "$output" 3840 2160 --refresh 60 >> "$LOGFILE" 2>&1 || true

log "Done"
