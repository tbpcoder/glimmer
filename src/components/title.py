from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtGui import QFont
from components.personalization.personalization_window import PersonalizationWindow

class TitleSection:
    """Represents the title section of the UI with a title label and a personalization button."""

    def __init__(self, parent):
        """Initialize the title section."""
        self.parent = parent
        self.layout = QVBoxLayout()  # Main layout is a QVBoxLayout
        self.personalization_window = None

        self._setup_layout()

    def _setup_layout(self):
        """Set up the main vertical layout with the title bar at the bottom."""
        # Add spacer to push the title bar to the bottom
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addSpacerItem(spacer)

        # Add the horizontal title bar layout
        self._add_title_bar()

    def _add_title_bar(self):
        """Add a title bar layout with the title and personalization button at the corners."""
        title_bar_layout = QHBoxLayout()  # Horizontal layout for title bar

        # Add "Glimmer" title
        title_label = QLabel("Glimmer")
        title_label.setFont(QFont("Arial", 18))
        title_label.setStyleSheet("color: rgb(230, 180, 255);")
        title_label.setFixedHeight(50)

        # Add personalization button
        personalize_btn = QPushButton("⚙")
        personalize_btn.setFixedSize(30, 30)
        personalize_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgb(230, 180, 255);
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: rgb(255, 200, 255);
            }
        """)
        personalize_btn.clicked.connect(self._show_personalization)

        # Add items to the horizontal layout
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_bar_layout.addWidget(personalize_btn)

        # Add the horizontal layout to the main vertical layout
        self.layout.addLayout(title_bar_layout)

    def _show_personalization(self):
        """Display the personalization window."""
        if self.personalization_window is None:
            self.personalization_window = PersonalizationWindow(self.parent)
        self.personalization_window.show()
        self.personalization_window.raise_()
