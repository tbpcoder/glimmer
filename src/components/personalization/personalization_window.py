from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QSpinBox, QPushButton, QGroupBox)
from utils.styles import StyleManager

class PersonalizationWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Personalization")
        self.setFixedSize(400, 500)
        self.init_ui()
        self.setStyleSheet(StyleManager.get_theme_styles())

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Outdoor Settings
        outdoor_group = self._create_theme_group("Outdoor", "outdoor")
        layout.addWidget(outdoor_group)

        # Indoor Settings
        indoor_group = self._create_theme_group("Indoor", "indoor")
        layout.addWidget(indoor_group)

        # Save Button
        save_button = QPushButton("Save Settings")
        save_button.setFixedSize(150, 40)
        save_button.clicked.connect(self.save_settings)
        
        # Close Application Button
        close_button = QPushButton("Close Application")
        close_button.setFixedSize(150, 40)
        close_button.clicked.connect(self.close_application)
        
        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()

    def _create_theme_group(self, title, theme_key):
        group = QGroupBox(title)
        layout = QVBoxLayout()

        # Max Brightness
        max_layout = QHBoxLayout()
        max_label = QLabel("Maximum Brightness:")
        max_spinbox = QSpinBox()
        max_spinbox.setRange(0, 100)
        max_spinbox.setValue(self.parent.THEMES[title][0])
        max_layout.addWidget(max_label)
        max_layout.addWidget(max_spinbox)
        layout.addLayout(max_layout)

        # Store the spinbox reference with the correct name
        setattr(self, f"{theme_key}_max_spinbox", max_spinbox)

        # Min Brightness
        min_layout = QHBoxLayout()
        min_label = QLabel("Minimum Brightness:")
        min_spinbox = QSpinBox()
        min_spinbox.setRange(0, 100)
        min_spinbox.setValue(self.parent.THEMES[title][1])
        min_layout.addWidget(min_label)
        min_layout.addWidget(min_spinbox)
        layout.addLayout(min_layout)

        # Store the spinbox reference with the correct name
        setattr(self, f"{theme_key}_min_spinbox", min_spinbox)

        # Add valueChanged signal to enforce constraints
        max_spinbox.valueChanged.connect(lambda value: self._sync_brightness_limits(theme_key, value, "max"))
        min_spinbox.valueChanged.connect(lambda value: self._sync_brightness_limits(theme_key, value, "min"))

        group.setLayout(layout)
        return group

    def _sync_brightness_limits(self, theme_key, value, changed):
        max_spinbox = getattr(self, f"{theme_key}_max_spinbox")
        min_spinbox = getattr(self, f"{theme_key}_min_spinbox")

        if changed == "max" and value < min_spinbox.value():
            min_spinbox.setValue(value)
        elif changed == "min" and value > max_spinbox.value():
            max_spinbox.setValue(value)

        self.parent.THEMES["Outdoor"] = (
            self.outdoor_max_spinbox.value(),
            self.outdoor_min_spinbox.value(),
        )
        self.parent.THEMES["Indoor"] = (
            self.indoor_max_spinbox.value(),
            self.indoor_min_spinbox.value(),
        )

    def save_settings(self):
        # Update the THEMES dictionary in the parent UI with new values from the spinboxes
        self.parent.THEMES["Outdoor"] = (
            self.outdoor_max_spinbox.value(),
            self.outdoor_min_spinbox.value()
        )
        self.parent.THEMES["Indoor"] = (
            self.indoor_max_spinbox.value(),
            self.indoor_min_spinbox.value()
        )
        
        # Update the current theme if needed
        self.parent.set_theme(self.parent.theme)
        
        # Save the updated THEMES dictionary to the file
        self.parent.save_themes(self.parent.THEMES)
        
        # Close the personalization window after saving
        self.hide()

    def close_application(self):
        self.parent.window_manager.quit_application()
