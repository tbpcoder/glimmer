from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy

class ButtonSection:
    """Button section component that contains theme and control buttons."""
    
    def __init__(self, parent):
        """
        Initialize the button section.
        
        Args:
            parent: Parent UI class that contains theme and pause methods.
        """
        self.parent = parent
        self.layout = QVBoxLayout()
        

        # Add a spacer at the top for spacing
        self.layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Minimum))

        self._create_theme_buttons()
        self._create_control_buttons()

        # Add a spacer at the bottom for spacing
        self.layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Minimum))
        
    def _create_theme_buttons(self):
        """Create and setup the theme selection buttons."""
        button_layout = QHBoxLayout()
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.outdoor_button = self._create_button(
            "Outdoor", 150, 45,
            lambda: self._debug_theme_change("Outdoor")
        )
        self.indoor_button = self._create_button(
            "Indoor", 150, 45,
            lambda: self._debug_theme_change("Indoor")
        )
        
        button_layout.addSpacerItem(spacer)
        button_layout.addWidget(self.outdoor_button)

        # Add space between the buttons
        button_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum))
        button_layout.addWidget(self.indoor_button)
        
        button_layout.addSpacerItem(spacer)
        
        self.layout.addLayout(button_layout)
        
    def _create_control_buttons(self):
        """Create and setup the control buttons (pause/resume and minimize)."""
        control_layout = QHBoxLayout()
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.pause_button = self._create_button(
            "Pause", 150, 45,
            self._debug_toggle_pause
        )
        
        self.minimize_button = self._create_button(
            "Minimize", 150, 45,
            self._debug_minimize
        )
        
        control_layout.addSpacerItem(spacer)
        control_layout.addWidget(self.pause_button)

        # Add space between the buttons
        control_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum))
        control_layout.addWidget(self.minimize_button)
        
        control_layout.addSpacerItem(spacer)
        
        self.layout.addLayout(control_layout)
        
    def _create_button(self, text, width, height, callback=None):
        """
        Create a styled button with specified parameters.
        
        Args:
            text (str): Button text
            width (int): Button width
            height (int): Button height
            callback (callable, optional): Function to call when button is clicked.
            
        Returns:
            QPushButton: Configured button.
        """
        button = QPushButton(text)
        button.setFixedSize(width, height)
        if callback:
            button.clicked.connect(callback)
        return button

    def _debug_theme_change(self, theme):
        """Debug method for theme change."""
        self.parent.set_theme(theme)

    def _debug_toggle_pause(self):
        """Debug method for toggling pause."""
        self.parent.toggle_pause()

    def _debug_minimize(self):
        """Debug method for minimizing the application."""
        self.parent.window_manager.minimize()
