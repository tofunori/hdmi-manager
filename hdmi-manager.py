#!/usr/bin/env python3
"""
HDMI Manager - Gestionnaire d'écran externe pour ASUS ProArt
Icône system tray pour gérer l'écran HDMI
"""

import sys
import subprocess
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QMessageBox
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer, QProcess

class HDMIManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Créer l'icône system tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon.fromTheme("video-display"))
        self.tray.setToolTip("HDMI Manager")

        # Créer le menu
        self.menu = QMenu()

        # Actions
        self.fix_action = QAction("Fix HDMI (1080p → 4K)")
        self.fix_action.triggered.connect(self.fix_hdmi)
        self.menu.addAction(self.fix_action)

        self.menu.addSeparator()

        # Sous-menu position
        position_menu = self.menu.addMenu("Position écran externe")

        self.pos_right = QAction("À droite du laptop")
        self.pos_right.triggered.connect(lambda: self.set_position("right"))
        position_menu.addAction(self.pos_right)

        self.pos_left = QAction("À gauche du laptop")
        self.pos_left.triggered.connect(lambda: self.set_position("left"))
        position_menu.addAction(self.pos_left)

        self.pos_above = QAction("Au-dessus du laptop")
        self.pos_above.triggered.connect(lambda: self.set_position("above"))
        position_menu.addAction(self.pos_above)

        self.menu.addSeparator()

        # Sous-menu scaling écran externe
        scale_ext_menu = self.menu.addMenu("Scaling écran externe")
        self.scale_ext_actions = []
        for scale in ["1", "1.25", "1.5", "1.75", "2"]:
            action = QAction(f"{int(float(scale)*100)}%", self.menu)
            action.triggered.connect(lambda checked, s=scale: self.set_scale("HDMI-A-1", s))
            scale_ext_menu.addAction(action)
            self.scale_ext_actions.append(action)

        # Sous-menu scaling laptop
        scale_laptop_menu = self.menu.addMenu("Scaling laptop")
        self.scale_laptop_actions = []
        for scale in ["1", "1.25", "1.5", "1.75", "2", "2.25"]:
            action = QAction(f"{int(float(scale)*100)}%", self.menu)
            action.triggered.connect(lambda checked, s=scale: self.set_scale("eDP-1", s))
            scale_laptop_menu.addAction(action)
            self.scale_laptop_actions.append(action)

        self.menu.addSeparator()

        # Activer/Désactiver
        self.enable_action = QAction("Activer écran externe")
        self.enable_action.triggered.connect(self.enable_hdmi)
        self.menu.addAction(self.enable_action)

        self.disable_action = QAction("Désactiver écran externe")
        self.disable_action.triggered.connect(self.disable_hdmi)
        self.menu.addAction(self.disable_action)

        self.menu.addSeparator()

        # Statut
        self.status_action = QAction("Statut: Vérification...")
        self.status_action.setEnabled(False)
        self.menu.addAction(self.status_action)

        self.menu.addSeparator()

        # Quitter
        self.quit_action = QAction("Quitter")
        self.quit_action.triggered.connect(self.quit)
        self.menu.addAction(self.quit_action)

        self.tray.setContextMenu(self.menu)
        self.tray.show()

        # Timer pour vérifier le statut
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_status)
        self.timer.start(5000)  # Toutes les 5 secondes

        # Vérifier le statut initial
        self.check_status()

        # Notification de démarrage
        self.tray.showMessage(
            "HDMI Manager",
            "Gestionnaire d'écran HDMI actif",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def run_kscreen(self, args):
        """Exécute kscreen-doctor avec les arguments donnés"""
        try:
            result = subprocess.run(
                ["kscreen-doctor"] + args,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def get_hdmi_status(self):
        """Vérifie si le HDMI est connecté"""
        try:
            status_file = Path("/sys/class/drm/card0-HDMI-A-1/status")
            if status_file.exists():
                return status_file.read_text().strip() == "connected"
        except:
            pass
        return False

    def check_status(self):
        """Met à jour le statut dans le menu"""
        connected = self.get_hdmi_status()
        if connected:
            self.status_action.setText("Statut: Connecté")
            self.tray.setIcon(QIcon.fromTheme("video-display"))
        else:
            self.status_action.setText("Statut: Déconnecté")
            self.tray.setIcon(QIcon.fromTheme("video-display"))

    def fix_hdmi(self):
        """Fix HDMI: baisser résolution puis remonter à 4K"""
        self.tray.showMessage(
            "HDMI Manager",
            "Fix en cours...",
            QSystemTrayIcon.MessageIcon.Information,
            1000
        )

        # Étape 1: Baisser à 1080p
        self.run_kscreen(["output.HDMI-A-1.mode.1920x1080@60"])

        # Attendre 1.5 seconde
        QTimer.singleShot(1500, self.fix_hdmi_step2)

    def fix_hdmi_step2(self):
        """Deuxième étape du fix: remonter à 4K"""
        # Étape 2: Remonter à 4K
        self.run_kscreen(["output.HDMI-A-1.mode.3840x2160@60"])

        # Repositionner
        self.run_kscreen(["output.HDMI-A-1.position.1920,0"])

        self.tray.showMessage(
            "HDMI Manager",
            "Fix terminé! Écran en 4K",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def set_position(self, position):
        """Change la position de l'écran externe"""
        if position == "right":
            self.run_kscreen(["output.HDMI-A-1.position.1920,0"])
            msg = "Écran externe à droite"
        elif position == "left":
            self.run_kscreen(["output.HDMI-A-1.position.0,0"])
            self.run_kscreen(["output.eDP-1.position.3840,0"])
            msg = "Écran externe à gauche"
        elif position == "above":
            self.run_kscreen(["output.HDMI-A-1.position.0,0"])
            self.run_kscreen(["output.eDP-1.position.0,2160"])
            msg = "Écran externe au-dessus"

        self.tray.showMessage(
            "HDMI Manager",
            msg,
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def set_scale(self, output, scale):
        """Change le scaling d'un écran"""
        self.run_kscreen([f"output.{output}.scale.{scale}"])
        percent = int(float(scale) * 100)
        screen_name = "externe" if output == "HDMI-A-1" else "laptop"
        self.tray.showMessage(
            "HDMI Manager",
            f"Scaling écran {screen_name}: {percent}%",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def enable_hdmi(self):
        """Active l'écran externe"""
        self.run_kscreen(["output.HDMI-A-1.enable"])
        self.tray.showMessage(
            "HDMI Manager",
            "Écran externe activé",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def disable_hdmi(self):
        """Désactive l'écran externe"""
        self.run_kscreen(["output.HDMI-A-1.disable"])
        self.tray.showMessage(
            "HDMI Manager",
            "Écran externe désactivé",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def quit(self):
        """Quitte l'application"""
        self.tray.hide()
        self.app.quit()

    def run(self):
        """Lance l'application"""
        sys.exit(self.app.exec())


if __name__ == "__main__":
    manager = HDMIManager()
    manager.run()
