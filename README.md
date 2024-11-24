# Glimmer

Glimmer is an automatic screen brightness controller for laptops that adjusts brightness based on real-time screen item brightness. Built with Python and PyQt5, it provides a seamless and customizable experience, designed to optimize screen brightness for comfort.

## Features

- **Automatic Brightness Adjustment**: Uses screen capture and analysis to adjust brightness automatically based on the screen light.
- **Customizable Sensitivity**: Fine-tune the sensitivity for personalized brightness control.
- **System Tray Integration**: Run Glimmer in the background, accessible via a system tray icon.
- **Modern and Intuitive UI**: Smooth, responsive interface.
- **Manual Override**: Pause auto-brightness adjustments when manually adjusting brightness using keyboard controls.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/tbpcoder/glimmer.git
    cd glimmer
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python src/main.py
    ```

## Usage

1. Launch Glimmer from your terminal.
2. Use the system tray icon for quick access to enable or disable auto-brightness.
3. Adjust settings from the UI to personalize sensitivity and UI themes.

## Configuration

- **Sensitivity**: Adjust how responsive Glimmer is to changes in screen light.
- **Theme Options**: Customize colors, slider design, and more for an aesthetically pleasing interface.

## Contributing

We welcome contributions! Please submit a pull request or open an issue to suggest improvements.

## License

MIT License.
