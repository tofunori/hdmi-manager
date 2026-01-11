# HDMI 4K Hotplug Fix for NVIDIA on Linux

Workaround for NVIDIA HDMI black screen issue on Linux. When connecting an external 4K monitor via HDMI, the screen stays black until you manually change to a lower resolution first.

This script automates the workaround: it sets 1080p briefly to "wake" the display, then switches to 4K.

## The Problem

On some NVIDIA + Linux setups (especially hybrid GPU laptops), connecting a 4K monitor via HDMI results in a black screen. The monitor only works after manually switching to a lower resolution (like 1080p) and then back to 4K.

## How It Works

1. **udev** detects HDMI hotplug event
2. **Script** runs automatically:
   - Sets display to 1080p (wakes the monitor)
   - Waits 1 second
   - Sets display to 4K
3. Display works in 4K

## Installation

1. **Copy the script:**
```bash
cp hdmi-4k.sh ~/.local/bin/
chmod +x ~/.local/bin/hdmi-4k.sh
```

2. **Edit the script** - change `TARGET_USER` to your username:
```bash
nano ~/.local/bin/hdmi-4k.sh
```

3. **Install udev rule:**
```bash
sudo cp 99-hdmi-hotplug.rules /etc/udev/rules.d/
```

4. **Edit udev rule** - update the path to match your username:
```bash
sudo nano /etc/udev/rules.d/99-hdmi-hotplug.rules
```

5. **Reload udev:**
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Configuration

Edit `hdmi-4k.sh` to customize:

| Variable | Default | Description |
|----------|---------|-------------|
| `output` | `HDMI-A-1` | Display output name |
| `TARGET_USER` | `tofunori` | Your Linux username |

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

Look for `card0-HDMI-A-1` or `card1-HDMI-A-1` - use the corresponding card number in the udev rule.

## Tested On

- **OS:** Pop!_OS with COSMIC desktop (Wayland)
- **GPU:** NVIDIA RTX 3060 Mobile + AMD Cezanne (hybrid)
- **Monitor:** ASUS VG289 (4K)

## Logs

View logs at `/tmp/hdmi-4k.log`:
```bash
cat /tmp/hdmi-4k.log
```

## License

MIT
