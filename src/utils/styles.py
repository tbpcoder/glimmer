class StyleManager:
    @staticmethod
    def get_theme_styles():
        return """
            QMainWindow {
                background-color: rgb(25, 3, 35);
            }
            QPushButton {
                background-color: rgba(140, 60, 180, 200);
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(160, 80, 200, 220);
            }
            QPushButton:pressed {
                background-color: rgba(180, 100, 220, 255);
            }
            QLabel {
                color: rgb(240, 240, 245);
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: rgb(50, 15, 65);
            }
            QSlider::handle:horizontal {
                width: 14px;
                background: rgb(200, 100, 255);
                margin: -5px 0;
                border-radius: 7px;
            }
            QSlider::handle:horizontal:hover {
                background: rgb(220, 120, 255);
            }
            QGroupBox {
                color: rgb(240, 240, 245);
                font-weight: bold;
            }
        """