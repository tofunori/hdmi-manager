# HDMI 4K Hotplug Fix for NVIDIA on Linux

Workaround for NVIDIA HDMI black screen issue on Linux. When connecting an external 4K monitor via HDMI, the screen stays black until you manually change to a lower resolution first.

This script automates the workaround: it sets 1080p briefly to "wake" the display, then switches to 4K.

## The Problem

On some NVIDIA + Linux setups (especially hybrid GPU laptops), connecting a 4K monitor via HDMI results in a black screen. The monitor only works after manually switching to a lower resolution (like 1080p) and then back to 4K.

## How It Works

1. **systemd user service** monitors HDMI status via polling (every 2 seconds)
2. When HDMI connection is detected, **hdmi-4k.sh** runs:
   - Sets display to 1080p (wakes the monitor)
   - Waits 1 second
   - Sets display to 4K
3. Display works in 4K

> **Why polling instead of udev?** NVIDIA drivers don't reliably emit udev hotplug events. Polling `/sys/class/drm/card1-HDMI-A-1/status` is more reliable.

## Installation

1. **Copy the scripts:**
```bash
cp hdmi-4k.sh hdmi-monitor.sh ~/.local/bin/
chmod +x ~/.local/bin/hdmi-4k.sh ~/.local/bin/hdmi-monitor.sh
```

2. **Edit hdmi-4k.sh** - change the `output` variable if needed:
```bash
nano ~/.local/bin/hdmi-4k.sh
```

3. **Edit hdmi-monitor.sh** - update `STATUS_FILE` if your HDMI is on a different card:
```bash
nano ~/.local/bin/hdmi-monitor.sh
```

4. **Install and enable the systemd service:**
```bash
mkdir -p ~/.config/systemd/user
cp hdmi-monitor.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now hdmi-monitor.service
```

5. **Verify it's running:**
```bash
systemctl --user status hdmi-monitor.service
```

## Configuration

### hdmi-4k.sh

| Variable | Default | Description |
|----------|---------|-------------|
| `output` | `HDMI-A-1` | Display output name |

### hdmi-monitor.sh

| Variable | Default | Description |
|----------|---------|-------------|
| `STATUS_FILE` | `/sys/class/drm/card1-HDMI-A-1/status` | Path to HDMI status file |

### Finding your display name

```bash
cosmic-randr list
# or
xrandr --query
```

### Finding your GPU card number

```bash
ls /sys/class/drm/
```

Look for `card0-HDMI-A-1` or `card1-HDMI-A-1` - update the paths in both scripts accordingly.

## Tested On

- **OS:** Pop!_OS 24.04 with COSMIC desktop (Wayland)
- **GPU:** NVIDIA RTX 3060 Mobile + AMD Cezanne (hybrid)
- **Monitor:** ASUS VG289 (4K)

## Manual Fix (after suspend/resume)

After waking from sleep, the HDMI may stay black. Use the manual fix:

### Option 1: Terminal alias
```bash
# Add to ~/.bashrc
alias hdmi="~/.local/bin/hdmi-resume.sh"

# Then just type:
hdmi
```

### Option 2: Desktop launcher
```bash
cp hdmi-fix.desktop ~/.local/share/applications/
cp hdmi-resume.sh hdmi-fix-launcher.sh ~/.local/bin/
chmod +x ~/.local/bin/hdmi-resume.sh ~/.local/bin/hdmi-fix-launcher.sh
```
Then search "HDMI Fix" in your app menu.

## Logs

```bash
# Monitor service log
cat /tmp/hdmi-monitor.log

# Script execution log
cat /tmp/hdmi-4k.log
```

## Uninstall

```bash
systemctl --user disable --now hdmi-monitor.service
rm ~/.config/systemd/user/hdmi-monitor.service
rm ~/.local/bin/hdmi-4k.sh ~/.local/bin/hdmi-monitor.sh
```

## License

MIT
