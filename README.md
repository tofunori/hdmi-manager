# HDMI Manager

Gestionnaire d'écran HDMI externe pour laptops Linux avec configuration hybride NVIDIA/AMD.

Résout le problème d'écran noir lors du branchement HDMI sur les laptops ASUS ProArt (et similaires) sous Fedora/KDE Plasma.

## Fonctionnalités

- **Détection automatique** du branchement HDMI via udev
- **Fix automatique** : bascule la résolution 1080p → 4K pour activer l'écran
- **GUI system tray** avec menu pour contrôle manuel
- **Positionnement** de l'écran externe (gauche/droite/dessus)

## Installation

### Dépendances

```bash
sudo dnf install python3-pyqt6
```

### Installation des fichiers

```bash
# GUI
cp hdmi-manager.py ~/.local/bin/
chmod +x ~/.local/bin/hdmi-manager.py

# Script hotplug
sudo cp hdmi-hotplug.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/hdmi-hotplug.sh

# Règle udev
sudo cp 99-hdmi-hotplug.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules

# Autostart (optionnel)
cp hdmi-manager.desktop ~/.config/autostart/
```

## Utilisation

### Automatique
Branchez simplement le câble HDMI - l'écran devrait s'activer automatiquement.

### Manuel
Clic droit sur l'icône dans la barre système :
- **Fix HDMI** : Force le fix 1080p → 4K
- **Position** : Change la position de l'écran externe
- **Activer/Désactiver** : Active ou désactive l'écran externe

## Configuration

Modifiez `hdmi-hotplug.sh` et `hdmi-manager.py` pour ajuster :
- La résolution (par défaut 3840x2160)
- La position (par défaut à droite)
- Le délai d'attente

## Testé sur

- ASUS ProArt StudioBook H5600
- Fedora 43 KDE Plasma
- NVIDIA RTX 3060 + AMD Radeon Vega (hybride)

## Licence

MIT
