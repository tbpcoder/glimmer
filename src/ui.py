import sys
import os
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(project_root))
sys.path.insert(0, project_root)
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget, QVBoxLayout, QDesktopWidget, QSystemTrayIcon, QMessageBox
from PyQt5.QtCore import QTimer
from src.controllers.brightness_controller import BrightnessController
from src.components.title import TitleSection
from src.components.buttons import ButtonSection
from src.components.sliders import SliderSection
from src.components.status import StatusSection
from src.utils.styles import StyleManager
from src.utils.window_manager import WindowManager
from utils.theme_file import load_themes, save_themes

class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glimmer")
        self.setFixedSize(500, 600)
        self.center()
        self.theme = "Indoor"
        self.brightness_controller = BrightnessController(self)
        self.prev_target_brightness = 0

        self.THEMES = load_themes()

        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "Glimmer",
                               "System tray is not available on this system")
            sys.exit(1)
        else:
            print("system tray access available")
        
        self.save_themes = save_themes

        self.window_manager = WindowManager(self)

        self.init_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        # Set up main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.set_manual_brightness = self.brightness_controller.set_manual_brightness

        # Initialize components
        self.title_section = TitleSection(self)
        self.button_section = ButtonSection(self)
        self.slider_section = SliderSection(self)
        self.status_section = StatusSection()
        # Add components to main layout
        try:
            # Existing initialization code
            if not self.title_section.layout:
                raise ValueError("Title section layout not initialized")
            self.layout.addLayout(self.title_section.layout or QVBoxLayout())
            self.layout.addLayout(self.slider_section.layout or QVBoxLayout())
            self.layout.addLayout(self.button_section.layout or QVBoxLayout())
            self.layout.addLayout(self.status_section.layout or QVBoxLayout())

        except Exception as e:
            print(f"UI Initialization Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

        # Set up timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_brightness)
        self.timer.start(1000)
        # Apply styles
        self.setStyleSheet(StyleManager.get_theme_styles())

    def closeEvent(self, event):
        event.ignore()
        self.window_manager.minimize()

    def set_theme(self, theme):
        self.theme = theme
        max_brightness, min_brightness = self.THEMES[theme]
        if(theme == 'Indoor'):
            self.slider_section.min_brightness_slider.setValue(min_brightness)
            self.slider_section.max_brightness_slider.setValue(max_brightness)
        else:
            self.slider_section.max_brightness_slider.setValue(max_brightness)
            self.slider_section.min_brightness_slider.setValue(min_brightness)
        self.brightness_controller.set_brightness_limits(max_brightness, min_brightness)

    def update_brightness(self):
        avg_brightness, target_brightness = self.brightness_controller.adjust_brightness(
            self.prev_target_brightness,
            sensitivity=self.slider_section.sensitivity_slider.value(),
            max_brightness=self.slider_section.max_brightness_slider.value(),
            min_brightness=self.slider_section.min_brightness_slider.value(),
        )
        self.prev_target_brightness = target_brightness
        self.status_section.status_label.setText(
            f"Average Brightness: {avg_brightness:.2f}\n"
            f"Adjusted Brightness: {target_brightness:.2f}%"
        )

    def toggle_pause(self):
        if self.brightness_controller.paused:
            self.resume_automatic_control()
        else:
            self.pause_automatic_control()

    def resume_automatic_control(self):
        self.brightness_controller.resume()
        self.button_section.pause_button.setText("Pause")
        self.slider_section.show_automatic_controls()

    def pause_automatic_control(self):
        self.brightness_controller.pause()
        self.button_section.pause_button.setText("Resume")
        self.slider_section.show_manual_controls()