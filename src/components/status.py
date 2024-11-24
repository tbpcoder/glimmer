from PyQt5.QtWidgets import QLabel, QVBoxLayout, QGroupBox
import logging

# Setting up logging
logging.basicConfig(level=logging.DEBUG)

class StatusSection:
    """Status section component that displays brightness information."""
    
    def __init__(self):
        """Initialize the status section."""
        logging.debug("Initializing StatusSection.")
        self.layout = QVBoxLayout()
        self._create_status()
        
    def _create_status(self):
        """Create and setup the status display."""
        logging.debug("Creating status display group.")
        self.group = QGroupBox("Status")
        self.group.setFixedHeight(100)
        status_layout = QVBoxLayout()
        self.status_label = QLabel("Average Brightness: 0\nAdjusted Brightness: 0%")
        status_layout.addWidget(self.status_label)
        self.group.setLayout(status_layout)
        self.group.setStyleSheet("color: rgb(230, 180, 255);")
        self.layout.addWidget(self.group)
        logging.debug("Status display group created.")

    def update_status(self, avg_brightness, adjusted_brightness):
        logging.debug(
            f"Updating status with average brightness: {avg_brightness:.2f} "
            f"and adjusted brightness: {adjusted_brightness:.2f}%"
        )
        self.status_label.setText(
            f"Average Brightness: {avg_brightness:.2f}\n"
            f"Adjusted Brightness: {adjusted_brightness:.2f}%"
        )
        logging.debug("Status updated successfully.")
