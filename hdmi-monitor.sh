#!/usr/bin/env bash
# Monitor HDMI status changes using polling
# More reliable than udev with NVIDIA drivers (which don't emit hotplug events)

STATUS_FILE="/sys/class/drm/card1-HDMI-A-1/status"
SCRIPT="$HOME/.local/bin/hdmi-4k.sh"
LAST_STATUS=""

while true; do
    CURRENT_STATUS=$(cat "$STATUS_FILE" 2>/dev/null)

    if [[ "$CURRENT_STATUS" != "$LAST_STATUS" ]]; then
        if [[ "$CURRENT_STATUS" == "connected" && "$LAST_STATUS" != "" ]]; then
            echo "$(date) - HDMI connected, running script" >> /tmp/hdmi-monitor.log
            "$SCRIPT"
        fi
        LAST_STATUS="$CURRENT_STATUS"
    fi

    sleep 2
done
