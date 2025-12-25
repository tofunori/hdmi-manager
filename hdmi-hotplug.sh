#!/bin/bash
# Script de hotplug HDMI - s'exécute automatiquement quand le HDMI est branché
# Ce script est appelé par udev

export DISPLAY=:0
export XAUTHORITY=/home/tofunori/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"

# Log pour debug
logger "HDMI Hotplug: Script déclenché"

# Attendre que le système soit prêt
sleep 2

# Vérifier si HDMI connecté
HDMI_STATUS=$(cat /sys/class/drm/card0-HDMI-A-1/status 2>/dev/null)

if [ "$HDMI_STATUS" == "connected" ]; then
    logger "HDMI Hotplug: HDMI connecté, application du fix..."

    # Fix: baisser puis remonter la résolution
    /usr/bin/kscreen-doctor output.HDMI-A-1.mode.1920x1080@60 2>/dev/null
    sleep 1
    /usr/bin/kscreen-doctor output.HDMI-A-1.mode.3840x2160@60 2>/dev/null
    /usr/bin/kscreen-doctor output.HDMI-A-1.position.1920,0 2>/dev/null

    logger "HDMI Hotplug: Fix appliqué"
else
    logger "HDMI Hotplug: HDMI déconnecté"
fi
