#!/usr/bin/env bash
# Simple HDMI fix - just cycle resolution

output="HDMI-A-1"

# 1080p first
cosmic-randr mode "$output" 1920 1080 --refresh 60 2>/dev/null

sleep 2

# Then 4K
cosmic-randr mode "$output" 3840 2160 --refresh 60 2>/dev/null

notify-send "HDMI Fix" "Résolution changée en 4K" 2>/dev/null || true
