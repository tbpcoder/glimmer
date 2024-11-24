from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
import os

class WindowManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_system_tray()
        self.restore_timer = QTimer()
        self.restore_timer.setSingleShot(True)
        self.restore_timer.timeout.connect(self._delayed_restore)

    def setup_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self.main_window)
        
        # Use absolute path for the icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.png")
        self.tray_icon.setIcon(QIcon(icon_path))

        # Create tray menu
        tray_menu = QMenu()
        restore_action = tray_menu.addAction("Show")
        restore_action.triggered.connect(self.restore)
        quit_action = tray_menu.addAction("Exit")
        quit_action.triggered.connect(self.quit_application)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def minimize(self):
        self.main_window.hide()
        self.tray_icon.show()
        self.tray_icon.showMessage(
            "Glimmer",
            "Application minimized to tray. Click the tray icon to restore.",
            QSystemTrayIcon.Information,
            2000
        )

    def restore(self):
        # Schedule the restore operation
        self.restore_timer.start(100)

    def _delayed_restore(self):
        # Ensure window is visible and has correct flags
        self.main_window.setWindowState(self.main_window.windowState() & ~Qt.WindowMinimized)
        self.main_window.show()
        self.main_window.activateWindow()
        self.main_window.raise_()
        
        # Force window to be active and on top
        self.main_window.setWindowFlags(
            self.main_window.windowFlags() | Qt.WindowStaysOnTopHint
        )
        self.main_window.show()
        
        # Remove the stay-on-top flag after a brief moment
        QTimer.singleShot(100, lambda: self._reset_window_flags())

    def _reset_window_flags(self):
        self.main_window.setWindowFlags(
            self.main_window.windowFlags() & ~Qt.WindowStaysOnTopHint
        )
        self.main_window.show()

    def quit_application(self):
        self.tray_icon.hide()
        QApplication.quit()

    def tray_icon_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            if self.main_window.isVisible():
                self.minimize()
            else:
                self.restore()