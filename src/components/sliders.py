import logging
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QSlider, QGroupBox, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SliderSection:
    """Slider section component that contains all brightness control sliders."""

    def __init__(self, parent):
        self.parent = parent
        self.layout = QVBoxLayout()
        self._create_sliders()
        logging.debug("SliderSection initialized.")

    def _create_sliders(self):
        self.group = QGroupBox("Brightness Control")
        slider_layout = QVBoxLayout()

        # Manual Brightness Control (Hidden by default)
        self.manual_brightness_label = QLabel("Manual Brightness")
        self.manual_brightness_label.setStyleSheet("color: rgb(230, 180, 255);")
        self.manual_brightness_slider = QSlider(Qt.Horizontal)
        self.manual_brightness_slider.setRange(0, 100)
        self.manual_brightness_slider.setValue(80)
        self.manual_brightness_value_label = QLabel(f"{self.manual_brightness_slider.value()}")
        self.manual_brightness_value_label.setStyleSheet("color: rgb(230, 180, 255);")
        self.manual_brightness_slider.valueChanged.connect(
            lambda: self._update_value_label(self.manual_brightness_slider, self.manual_brightness_value_label)
        )
        logging.debug("Manual brightness slider created with default value: 80.")

        # Create sliders with values using the new method
        self.sensitivity_slider, self.sensitivity_label, self.sensitivity_value_label = self._create_slider_with_value("Sensitivity:", 1, 10, 7)
        self.max_brightness_slider, self.max_brightness_label, self.max_brightness_value_label = self._create_slider_with_value("Maximum Brightness:", 0, 100, 80)
        self.min_brightness_slider, self.min_brightness_label, self.min_brightness_value_label = self._create_slider_with_value("Minimum Brightness:", 0, 100, 20)

        self.manual_brightness_slider.setVisible(False)
        self.manual_brightness_label.setVisible(False)
        self.manual_brightness_value_label.setVisible(False)

        self.manual_brightness_slider.valueChanged.connect(self.parent.set_manual_brightness)
        self.min_brightness_slider.valueChanged.connect(self._ensure_min_max_order)
        self.max_brightness_slider.valueChanged.connect(self._ensure_min_max_order)

        # Add widgets for manual brightness sliders and automatic ones
        slider_layout.addWidget(self.manual_brightness_label)
        slider_layout.addWidget(self.manual_brightness_value_label)
        slider_layout.addWidget(self.manual_brightness_slider)

        # Add automatic sliders and their values
        slider_layout.addLayout(self._create_slider_layout(self.sensitivity_label, self.sensitivity_value_label, self.sensitivity_slider))
        slider_layout.addLayout(self._create_slider_layout(self.max_brightness_label, self.max_brightness_value_label, self.max_brightness_slider))
        slider_layout.addLayout(self._create_slider_layout(self.min_brightness_label, self.min_brightness_value_label, self.min_brightness_slider))

        self.group.setLayout(slider_layout)
        self.group.setStyleSheet("color: rgb(230, 180, 255);")
        self.group.setFixedHeight(250)  # Adjusted height to accommodate value labels

        self.layout.addWidget(self.group)
        logging.debug("Sliders created and added to the layout.")

    def _create_slider_with_value(self, label_text, min_val, max_val, default_val):
        """Helper method to create sliders with a label and value."""
        label = QLabel(label_text)
        label.setStyleSheet("color: rgb(230, 180, 255);")

        value_label = QLabel(f"{default_val}")
        value_label.setStyleSheet("color: rgb(230, 180, 255);")

        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default_val)
        slider.valueChanged.connect(lambda: self._update_value_label(slider, value_label))

        logging.debug(f"Slider created: {label_text} (Range: {min_val}-{max_val}, Default: {default_val}).")
        return slider, label, value_label

    def _create_slider_layout(self, label, value_label, slider):
        """Creates a layout for the label, value, and slider."""
        layout = QVBoxLayout()

        # Horizontal layout for label and value
        label_layout = QHBoxLayout()
        label_layout.addWidget(label)
        label_layout.addWidget(value_label)
        label_layout.addStretch()

        # Add label and value to the vertical layout
        layout.addLayout(label_layout)
        layout.addWidget(slider)

        return layout

    def _update_value_label(self, slider, label):
        """Updates the value label whenever the slider value changes."""
        label.setText(f"{slider.value()}")
        logging.debug(f"Slider value updated: {slider.value()}")

    def _ensure_min_max_order(self, value):
        """Ensures that min value is always less than max value."""
        min_value = self.min_brightness_slider.value()
        max_value = self.max_brightness_slider.value()

        if min_value > max_value:
            if value == self.min_brightness_slider.value():
                self.min_brightness_slider.setValue(max_value)
                logging.warning("Min value adjusted to match Max value.")
            else:
                self.max_brightness_slider.setValue(min_value)
                logging.warning("Max value adjusted to match Min value.")
        logging.debug(f"Min-Max values ensured: Min = {min_value}, Max = {max_value}.")

    def show_automatic_controls(self):
        """Show automatic control sliders and hide manual control sliders."""
        self.sensitivity_slider.setVisible(True)
        self.sensitivity_label.setVisible(True)
        self.sensitivity_value_label.setVisible(True)
        self.max_brightness_slider.setVisible(True)
        self.max_brightness_label.setVisible(True)
        self.max_brightness_value_label.setVisible(True)
        self.min_brightness_slider.setVisible(True)
        self.min_brightness_label.setVisible(True)
        self.min_brightness_value_label.setVisible(True)
        self.manual_brightness_slider.setVisible(False)
        self.manual_brightness_label.setVisible(False)
        self.manual_brightness_value_label.setVisible(False)
        logging.debug("Automatic controls shown, manual controls hidden.")

    def show_manual_controls(self):
        """Show manual control sliders and hide automatic control sliders."""
        self.sensitivity_slider.setVisible(False)
        self.sensitivity_label.setVisible(False)
        self.sensitivity_value_label.setVisible(False)
        self.max_brightness_slider.setVisible(False)
        self.max_brightness_label.setVisible(False)
        self.max_brightness_value_label.setVisible(False)
        self.min_brightness_slider.setVisible(False)
        self.min_brightness_label.setVisible(False)
        self.min_brightness_value_label.setVisible(False)
        self.manual_brightness_slider.setVisible(True)
        self.manual_brightness_label.setVisible(True)
        self.manual_brightness_value_label.setVisible(True)
        self.group.setFixedHeight(250)  # Adjusted height for manual controls
        logging.debug("Manual controls shown, automatic controls hidden.")
