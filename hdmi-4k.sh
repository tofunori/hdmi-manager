#!/usr/bin/env bash
set -euo pipefail

# HDMI 4K Hotplug Workaround for NVIDIA on Linux
# Fixes black screen on HDMI connect by cycling through lower resolution first

output="HDMI-A-1"

# Use user runtime dir for lockfile (avoids root ownership issues with udev)
LOCKFILE="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/hdmi-4k.lock"
LOGFILE="/tmp/hdmi-4k.log"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
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
cosmic-randr mode "$output" 1920 1080 --refresh 60 >> "$LOGFILE" 2>&1 || true

sleep 1

log "4K"
cosmic-randr mode "$output" 3840 2160 --refresh 60 >> "$LOGFILE" 2>&1 || true

log "Done"
